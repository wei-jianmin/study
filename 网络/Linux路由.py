容器是一种新的虚拟化技术，每一个容器都是一个逻辑上独立的网络环境。
参：file://linux网络命名空间.py

Linux 上提供了软件虚拟出来的二层交换机 Bridge 
可以解决同一个宿主机上多个容器之间互连的问题，
但这是不够的,二层交换无法解决容器和宿主机外部网络的互通。
（veth方式只能将同网段的两个vnet连接起来，如果是不同网段，则没法使用）
容器肯定是需要和宿主机以外的外部网络互通才具备实用价值的。
回想在传统物理物理网络中，不同子网之间的服务器是如何互联起来的呢，
没错，就是在三层工作的路由器，也叫网关。
路由器使得数据包可以从一个子网中传输到另一个子网中，进而实现更大范围的网络互通。
如下图所示，一台路由器将 192.168.0.x 和 192.168.1.x 两个子网连接了起来。
file://imgs/路由器将两个子网连接.png
在容器虚拟化网络中，自然也需要这么一个角色，将容器和宿主机以外的网络连接起来
其实 Linux 天生就具备路由的功能

一、什么时候需要路由
    先来聊聊 Linux 在什么情况下需要路由过程。
    其实在发送数据时和接收数据时都会涉及到路由选择
    1.1 发送数据时选路
        Linux 之所以在发送数据包的时候需要进行路由选择，
        这是因为服务器上是可能会有多张网卡设备存在的。
        数据包在发送的时候，一路通过用户态、TCP 层到了 IP 层的时候，
        就要进行路由选择，以决定使用哪张网卡设备把数据包送出去。
        file://imgs/发送时路由选择.png
        网络层发送的入口函数是 ip_queue_xmit。
        int ip_queue_xmit(struct sk_buff *skb, struct flowi *fl)
        {
             // 路由选择过程
             // 选择完后记录路由信息到 skb 上
             rt = (struct rtable *)__sk_dst_check(sk, 0);
             if (rt == NULL) {
              // 没有缓存则查找路由项
              rt = ip_route_output_ports(...);
              sk_setup_caps(sk, &rt->dst);
             }
             skb_dst_set_noref(skb, &rt->dst);
             ...
             //发送
             ip_local_out(skb);
        }
        在 ip_queue_xmit 里我们开头就看到了路由项查找， 
        ip_route_output_ports 这个函数中完成路由选择。
        路由选择就是到路由表中进行匹配，然后决定使用哪个网卡发送出去。
        详参：file://../ipsec vpn/图解Linux网络包接收过程.py
        Linux 中最多可以有 255 张路由表，
        其中默认情况下有 local 和 main 两张。
        使用 ip 命令可以查看路由表的具体配置。
    1.2 接收数据时选路
        接收数据包的时候也需要进行路由选择。
        这是因为 Linux 可能会像路由器一样工作，
        将收到的数据包通过合适的网卡将其转发出去。
        Linux 在 IP 层的接收入口 ip_rcv 执行后调用到 ip_rcv_finish。
        在这里展开路由选择。
        如果发现确实就是本设备的网络包，
        那么就通过 ip_local_deliver 送到更上层的 TCP 层进行处理。
        file://imgs/接收数据包时路由.png
        如果路由后发现非本设备的网络包，
        那就进入到 ip_forward 进行转发，最后通过 ip_output 发送出去。
        file://imgs/接收并转发数据包.png
    1.3 linux 路由小结
        file://imgs/路由在内核协议栈中的位置.png
        网络包在发送的时候，需要从本机的多个网卡设备中选择一个合适的发送出去。
        网络包在接收的时候，也需要进行路由选择，
        如果是属于本设备的包就往上层送到网络层、
        传输层直到 socket 的接收缓存区中。
        如果不是本设备上的包，就选择合适的设备将其转发出去。
二、Linux 的路由实现
    路由表
        路由表（routing table）在内核源码中的另外一个叫法是
        转发信息库（Forwarding Information Base，FIB）。
        所以你在源码中看到的 fib 开头的定义基本上就是和路由表相关的功能。
        路由表本身是用 struct fib_table 来表示的。
        struct fib_table {
             struct hlist_node tb_hlist;
             u32   tb_id;
             int   tb_default;
             int   tb_num_default;
             unsigned long  tb_data[0];
            };
        所有的路由表都通过一个 hash - fib_table_hash 来组织和管理。
        它是放在网络命名空间 net 下的。
        这也就说明每个命名空间都有自己独立的路由表。
        在默认情况下，Linux 只有 local 和 main 两个路由表。
        如果内核编译时支持策略路由，那么管理员最多可以配置  255 个独立的路由表。
        如果你的服务器上创建了多个网络命名空间的话，那么就会存在多套路由表。
    路由查找
        在上面的小节中我们看到，
        发送过程调用 ip_route_output_ports 来查找路由，
        接收过程调用 ip_route_input_slow 来查找。
        但其实这两个函数都又最终会调用到 fib_lookup 这个核心函数，
        这个函数就是依次到 local 和 main 表中进行匹配，
        匹配到后就返回，不会继续往下匹配。
        由于 local 表的优先级要高于 main 表，
        如果 local 表中找到了规则，则路由过程就结束了。
        这也就是很多同学说为什么 ping 本机的时候在 eth0 上抓不到包的根本原因。
        所有命中 local 表的包都会被送往 loopback 设置，不会过 eth0。
    路由的使用方法
        开启转发路由
            在默认情况下，Linux 上的转发功能是关闭的，
            这时候 Linux 发现收到的网络包不属于自己就会将其丢弃。
            但在某些场景下，例如对于容器网络来说，
            Linux 需要转发本机上其它网络命名空间中过来的数据包，需要手工开启转发。
            如下这两种方法都可以：
                sysctl -w net.ipv4.ip_forward=1
                sysctl net.ipv4.conf.all.forwarding=1
            开启后，Linux 就能像路由器一样对不属于本机
            （严格地说是本网络命名空间）的 IP 数据包进行路由转发了。
        查看路由表
            在 centos 上可以通过以下方式查看是否开启了 CONFIG_IP_MULTIPLE_TABLES 多路由表支持
            cat /boot/config-3.10.0-693.el7.x86_64 
            输出结果包含：CONFIG_IP_MULTIPLE_TABLES=y
            查看某个路由表的配置，通过使用 ip route list table {表名} 来查看
            如果是查看 main 路由表，也可以直接使用 route 命令
            # route -n
            Kernel IP routing table
            Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
            10.0.0.0        10.*.*.254      255.0.0.0       UG    0      0        0 eth0
            10.*.*.0        0.0.0.0         255.255.248.0   U     0      0        0 eth0
            
            Destination：目的地址，可以是一个具体的 IP，也可以是一个网段，和 Genmask 一起表示。
            Gateway：网关地址，如果是 0.0.0.0 表示不需要经过网关。
            Flags: U 表示有效，G 表示连接路由，H 这条规则是主机路由，而不是网络路由。
            Iface：网卡设备，使用哪个网卡将包送过去。
            
            上述结果中输出的第一条路由规则表示这台机器下，
            确切地说这个网络环境下，所有目标为 10.0.0.0/8
            （Genmask 255.0.0.0 表示前 8 位为子网掩码） 网段的网络包
            都要通过 eth0 设备送到 10...254 这个网关，由它再帮助转发。

            第二条路由规则表示，如果目的地址是 10...0/21
            （Genmask 255.255.248.0 表示前 21 位为子网掩码）
            则直接通过 eth0 发出即可，不需要经过网关就可通信。
        修改路由表
            默认的 local 路由表是内核根据当前机器的网卡设备配置自动生成的，不需要手工维护。
            对于main 的路由表配置我们一般只需要使用 route add 命令就可以了，删除使用 route del。
            修改主机路由
                # route add -host 192.168.0.100 dev eth0 //直连不用网关
                # route add -host 192.168.1.100 dev eth0 gw 192.168.0.254 //下一跳网关
            修改网络路由
                # route add -net 192.168.1.0/24 dev eth0 //直连不用网关
                # route add -net 192.168.1.0/24 dev eth0 gw 10.162.132.110 //下一跳网关
            也可以指定一条默认规则，不命中其它规则的时候会执行到这条。
                # route add default gw 192.168.0.1 eth0
            对于其它编号的路由表想要修改的话，就需要使用 ip route 命令了。
            这里不过多展开，只用 main 表举一个例子
                # ip route add 192.168.5.0/24 via 10.*.*.110 dev eth0 table main
总结
    file://imgs/linux收发数据包的路由.png
    路由选择过程其实不复杂，就是根据各个路由表的配置找到合适的网卡设备，
    以及下一跳的地址，然后把包转发出去就算是完事。
    通过合适地配置路由规则，容器中的网络环境和外部的通信不再是难事。
    通过大量地干预路由规则就可以实现虚拟网络互通。
                
==================================================================================

https://www.jianshu.com/p/369e50201bce                
让网络命名空间可以连外网

1.  创建一个新的network namespace
    $ ip netns add blue
    查看新创建network namespace   
    $ ip netns list    
2.  分配一个网络接口给Network Namespaces
    创建一个veth对：
    $ ip link add veth0 type veth peer name veth1
    这个时候这两个网卡还都属于“default”或“global”命名空间，和物理网卡一样。
    把其中的一个veth转移到blue命名空间中去
    $ ip link set veth1 netns blue 
    这个时候veth1以及设置到了blue命名空间中了，运行如下命令查看
    $ ip netns exec blue ip link list
    这个时候你可以看到里面有两个网络接口
    一个是回环网络lo、另一个是veth1
3.  配置Network Namespaces里面的网络接口 
    配置blue命名空间中的veth1接口
    $ ip netns exec blue ip addr add 10.1.1.1/24 dev veth1
    $ ip netns exec blue ip link set veth1 up
    $ ip netns exec blue ip link set lo up
    查看一下blue命名空间里面的两个网卡的状态
    $ ip netns exec blue ip addr show
    配置host上面对端vnet0网卡的ip
    $ ip addr add 10.1.1.2/24 dev veth0
    $ ip link set veth0 up
    这个时候在blue命名空间里面ping 10.1.1.1（自己的veth1）已经ok了
    但是依旧ping不通10.1.1.2（默认网络命名空间中的veth0）
    这是因为blue命名空间中的路由还没有设置。
4.  设置命名空间内的路由
    $ ip netns exec blue ip route add default via 10.1.1.1
    $ ip netns exec blue ip route show
      default via 10.1.1.1 dev veth1
    所有找不到目的地址的数据包都通过设备veth1转发出去。
    这个时候就可以成功ping通host上的veth0网卡了
    但是到了这里依旧还不够，
    blue命名空间中已经可以联通主机上的网络，
    但是依旧连不同主机以外的外部网络。
    * 这个时候必须在host主机上启动转发，并且在iptables中设置伪装
5. 使能IP转发：IP_FORWARD
    Linux系统的IP转发的意思是，
    当Linux主机存在多个网卡的时候，
    允许一个网卡的数据包转发到另外一张网卡；
    在linux系统中默认禁止IP转发功能，
    可以打开如下文件查看，如果值为0说明禁止进行IP转发
    cat /proc/sys/net/ipv4/ip_forward
    运行如下的命令，其中ens160是host的一个对外网卡，
    这样的就允许ens160和veth0之间的转发；
    也就是说blue命名空间可以和外网联通了   
    #使能ip转发
    echo 1 > /proc/sys/net/ipv4/ip_forward
    #刷新forward规则
    iptables -F FORWARD
    #清空nat表规则链
    iptables -t nat -F
    #显示nat表规则
    iptables -t nat -L -n
    #使能IP伪装
    iptables -t nat -A POSTROUTING -s 10.1.1.0/255.255.255.0 -o ens160 -j MASQUERADE
    #允许veth0和ens160之间的转发
    iptables -A FORWARD -i ens160 -o veth0 -j ACCEPT
    iptables -A FORWARD -o ens160 -i veth0 -j ACCEPT
    使能IP伪装这条语句，添加了一条规则到NAT表的POSTROUTING链中，
    对于源IP地址为10.1.1.0网段的数据包，用ens160网口的IP地址替换并发送。
    iptables -A FORWARD这两条语句使能物理网口ens160和veth0之间的数据转发
