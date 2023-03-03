功能： ip命令用来显示或操纵Linux主机的路由、网络设备、策略路由和隧道
语法： ip [OPTIONS] OBJECT COMMAND
    OBJECT := { link | address | addrlabel | route | rule | neigh | ntable |
                tunnel | tuntap | maddress | mroute | mrule | monitor | xfrm |
                netns | l2tp | tcp_metrics | token }
    OPTIONS := { -V[ersion] | -h[uman-readable] | -s[tatistics] | -d[etails] |
                 -r[esolve] | -iec | -f[amily] {inet|inet6|ipx|dnet|link} |
                 -4 | -6 | -I | -D | -B | -0 | -rc[vbuf] [size] | -o[neline] |
                 -l[oops] { maximum-addr-flush-attempts } | -t[imestamp] | 
                 -ts[hort] | -n[etns] name | -a[ll] }
功能详解
    OPTIONS 是一些修改ip行为或者改变其输出的选项，
    所有的选项都是以-字符开头，分为长、短两种形式:
        -V： -Version打印ip的版本并退出
        -h： 人类可读输出
        -s： -stats –statistics，输出更多的信息，如果这个选项出现两次或以上，输出的信息将更为详尽
        -d： 输出更多的细节信息
        -l： 指定"IP地址刷新"逻辑将尝试的最大循环数，默认为10
        -f： -family 　指定要使用的协议族，协议可以是一个inet，inet6、bridge, ipx, dnet or link
        -4： 是 -family inet的简写
        -6： 是 -family inet6的简写
        -0： 是 -family link 的简写
        -I： 是-family ipx的简写
        -o： -oneline 单行输出，用"\"字符替换换行符
        -n： -netns交换机的IP到指定的网络空间netns
        -r： -resolve 使用系统名称解析来打印DNS名称而不是主机地址
        -t： 使用监视器选项时显示当前时间
        -a： -all对所有对象执行指定的命令，这取决于命令是否支持这个选项
        -rc：-rcvbuf (size) 设置Netlink套接字接收缓冲区的大小设置，默认为1MB
    OBJECT 是你要管理或者获取信息的对象
        link 网络设备
        address 一个设备的协议（IP或者IPV6）地址
        neighbour ARP或者NDISC缓冲区条目
        route 路由表条目
        rule 路由策略数据库中的规则
        maddress 多播地址
        mroute 多播路由缓冲区条目
        monitor 监控网络消息
        mrule 组播路由策略数据库中的规则
        tunnel IP上的通道
        l2tp 隧道以太网(L2TPV3)
        netns  - manage network namespaces
        ntable - manage the neighbor cache's operation
        tcp_metrics/tcpmetrics - manage TCP Metrics
        token  - manage tokenized interface identifiers
        tunnel - tunnel over IP.
        tuntap - manage TUN/TAP devices
        xfrm   - manage IPSec policies
        注意：所有的对象名都可以简写，例如：address可以简写为addr，甚至是a
通过man获取帮助
    man ip 只是简要列出了所支持的操作对象，要想过得该操作对象所支持的具体命令
    请使用man命令，后跟如下词条：
    ip-address, ip-addrlabel, ip-l2tp, ip-link, ip-maddress, ip-monitor, 
    ip-mroute, ip-neighbour, ip-netns, ip-ntable, ip-route, ip-rule, 
    ip-tcp_metrics, ip-token, ip-tunnel, ip-xfrm
    也可以使用 ip OBJECT help,获取指定对象的简要帮助
举例：
    增加IP地址
        格式： ip addr add ADDRESS/MASK dev DEVICE
        root@centos7 ~]# ip addr add 192.1.1.1/24 dev ens33
    删除IP地址
        [root@centos7 ~]# ip addr del 192.1.1.1/24 dev ens34
    查看网络信息
        [root@centos7 ~]# ip address show
    添加路由表
        格式：ip rouite add TARGET via GW
        TARGET为目标网络或主机，GW为网关或吓一跳。
        [root@centos7 ~]# ip route add 172.16.0.0/16 via 192.168.29.1
    删除路由表
        [root@centos7 ~]# ip route del 172.16.0.0/16
    显示路由表
        格式：ip route show|list
        [root@centos7 ~]# ip route list
    清空路由表
        格式：ip route flush [dev IFACE] [via PREFIX]
        [root@centos7 ~]# ip route flush dev ens33
    添加网关
        格式：ip route add default via GW dev IFACE
        [root@centos7 ~]# ip route add default via 192.168.29.1
    显示网络设备的运行状态
        [root@centos7 ~]# ip link list
    显示邻居表
        [root@centos7 ~]# ip neigh 
    查看网卡信息
        [root@centos7 ~]# ip -s link list 
    设置MTU
        [root@centos7 ~]# ip link set ens33 mtu 1400
    关闭网络设备
        [root@centos7 ~]# ip link set ens38 down
        [root@centos7 ~]# ip link show ens38
    开启网络设备
        [root@centos7 ~]# ip link set ens38 up
        [root@centos7 ~]# ip link show ens38