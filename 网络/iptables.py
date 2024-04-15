iptables是默认是黑名单机制，即没有加载黑名单里的，都是可以放行的

iptables [-t Table] COMMAND [Chain] [RuleNum] CRETIRIA -j ACTION
       具体：
       ip6tables [-t table] {-A|-C|-D} chain rule-specification
       iptables [-t table] {-A|-C|-D} chain rule-specification
       iptables [-t table] -I chain [rulenum] rule-specification
       iptables [-t table] -R chain rulenum rule-specification
       iptables [-t table] -D chain rulenum
       iptables [-t table] -S [chain [rulenum]]
       iptables [-t table] {-F|-L|-Z} [chain [rulenum]] [options...]
       iptables [-t table] -N chain
       iptables [-t table] -X [chain]
       iptables [-t table] -P chain target
       iptables [-t table] -E old-chain-name new-chain-name
       rule-specification = [matches...] [target]
       match = -m matchname [per-match-options]
       target = -j targetname [per-target-options]

规律：       
    iptables 'in' Table Add/Del/.. 'at' Chain [RuleNum] 'on' CRETIRIA 'do' -j ACTION
    对 ['表'] '增删改查' [针对特定'链'] [中的'第几行'] '过滤匹配' 的结果 '进行。。。操作'

注：[Chain] [RuleNum] 在这里并不是表示可选，
    而是指对某些 COMMNAD 必选，对另一些 COMMAND 不选或可选
    
-t：        指定需要维护的防火墙规则表 filter、nat、mangle或raw。
            在不使用 -t 时则默认使用 filter 表。

-m/--match: 指定使用匹配条件

COMMAND：   子命令，定义对规则的管理。
            -A	    追加防火墙规则
            -C      检查防火墙规则
            -D	    删除防火墙规则
            -F	    清空防火墙规则
            -I	    插入防火墙规则
            -L	    列出防火墙规则
            -R	    替换防火墙规则
            -S      打印防火墙规则
            -Z	    清空防火墙数据表统计信息
            -P	    设置链默认规则
            -n      表示不对 IP 地址进行反查，
                    加上这个参数显示速度将会加快。
            -v      表示输出详细信息，包含通过该规则的数据包数量、
                    总字节数以及相应的网络接口。
                    
Chain：     指明节点（规则链）。┌──────┬───┬──────┬───┐ 
            PREROUTING      匹配│      │nat│mangle│raw│表
            INPUT           匹配│filter│   │mangle│   │表
            FORWARD         匹配│filter│   │mangle│   │表
            OUTPUT          匹配│filter│nat│mangle│raw│表
            POSTROUTING     匹配│      │nat│mangle│raw│表
                                └──────┴───┴──────┴───┘
                                
CRETIRIA：  匹配过滤
            [!]-p	        匹配协议，! 表示取反
            [!]-s	        匹配源地址
            [!]-d	        匹配目标地址
            [!]-i	        匹配入站网卡接口
            [!]-o	        匹配出站网卡接口
            [!]--sport	    匹配源端口
            [!]--dport	    匹配目标端口
            [!]--src-range	匹配源地址范围
            [!]--dst-range	匹配目标地址范围
            [!]--limit	    四配数据表速率
            [!]--mac-source	匹配源MAC地址
            [!]--sports	    匹配源端口
            [!]--dports	    匹配目标端口
            [!]--stste	    匹配状态（INVALID、ESTABLISHED、NEW、RELATED)
            [!]--string	    匹配应用层字串
            [!]--icmp-type  匹配ICMP类型
    注： 上面的这些过滤条件，有时会与 -m 搭配使用 （这在 man 帮助中没讲到）
            https://blog.csdn.net/weixin_48190891/article/details/107815698
            多端口匹配:  -m multiport --sports 源端口列表
            IP范围匹配:  -m iprange --src-range IP范围
            MAC地址匹配: -m mac --mac-source MAC地址
            状态匹配:    -m state --state 连接状态
            
ACTION：    触发动作
            ACCEPT	    允许数据包通过
            DROP	    丢弃数据包
            REJECT	    拒绝数据包通过
            LOG	        将数据包信息记录 syslog 曰志
            DNAT	    目标地址转换（用于PREROUTING）
            SNAT	    源地址转换（用于POSTROUTING）
            MASQUERADE	地址欺骗（源地址自动转换，用于POSTROUTING）
            REDIRECT	重定向(通过改变目标IP和端口,实现端口映射)

iptables-save 和 iptables-restore
    iptables的配置文件 /etc/sysconfig/iptables
    iptables-save [-c] [-t table]
        参数-c的作用是保存包和字节计数器的值。
        这可以使我们在重启防火墙后不丢失对包和字节的统计。
        带-c参数的iptables-save命令使重启防火墙而不中断统计记数程序成为可能。
        这个参数默认是不使用的。
        参数-t指定要保存的表，默认是保存所有的表。
    iptables-save > /etc/sysconfig/iptables
    iptables-save是将规则追加到一个文件，主要是配合iptables-restore命令
    iptables-restore用来装载由iptables-save保存的规则集。
    不幸的是，它只能从标准输入接受输入，而不能从文件接受
    iptables-restore [-c] [-n]
    参数-c要求装入包和字节计数器。
    如果你用iptables-save保存了计数器，现在想重新装入，就必须用这个参数。
    它的另一种较长的形式是--counters。
    参数-n告诉iptables-restore不要覆盖已有的表或表内的规则。
    默认情况是清除所有已存的规则。
    这个参数的长形式是--noflush。
    
++++++++++++++++++++++++++++++  举例  ++++++++++++++++++++++++++++++++++++

使用 iptables 配置转发
    #关闭selinux
    setenforce 0
    #开启转发
    /etc/sysctl.conf 中的 net.ipv4.ip_forward=1
    sysctl -p
    #在经过 FORWARD 节点时，不要让 filter 表将之过滤掉
    iptables -P FORWARD ACCEPT
    #已建立连接的，允许转发
    iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
    iptables -t nat -A POSTROUTING -j MASQUERADE
    #将对 11.53.96.13:7777 的访问，转发到 11.0.34.204:8888
    iptables -t nat -A PREROUTING -d 11.53.96.13 -p tcp --dport 7777 
             -j DNAT --to-destination 11.0.34.204:8888
    iptables -t nat -A PREROUTING -d 192.168.2.72 -p udp --dport 10022 
             -j DNAT --to-destination 192.168.70.2:22
 
iptables实现端口映射（本地和远程端口映射）
    #上面<使用 iptables 配置转发>有提到，这里再说一遍
    1. 需要先开启linux的数据转发功能
       vim /etc/sysctl.conf，将net.ipv4.ip_forward=0更改为net.ipv4.ip_forward=1
       sysctl -p  //使数据转发功能生效
    2. 更改iptables，使之实现nat映射功能
       将外网访问60.208.23.14的1234端口转发到192.168.3.44:8000端口。
       iptables -t nat -A PREROUTING -d 60.208.23.14 -p tcp --dport 1234 
                -j DNAT --to-destination 192.168.3.44:8000
       将192.168.3.44 8000端口将数据返回给客户端时，将源ip改为60.208.23.14
       iptables -t nat -A POSTROUTING -d 192.168.3.44 -p tcp --dport 8000 
                -j SNAT --to 60.208.23.14
            
++++++++++++++++++++++++++++++++  深入理解  +++++++++++++++++++++++++++++++++

深入理解 SNAT 与 DNAT
    https://www.frozentux.net/iptables-tutorial/cn/iptables-tutorial-cn-1.1.19.html#MARKTARGET
        6.5.12. SNAT target
            这个target是用来做源网络地址转换的，就是重写包的源IP地址
            当我们有几个机子共享一个Internet 连接时，就能用到它了
            先在内核里打开ip转发功能，然后再写一个SNAT规则
            就可以把所有从本地网络出去的包的源地址改为Internet连接的地址了
            如果我们不这样做而是直接转发本地网的包的话，
            Internet上的机子就不知道往哪儿发送应答了，
            因为在本地网里我们一般使用的是IANA组织专门指定的一段地址，
            它们是不能在Internet上使用的。
            SNAT target的作用就是让所有从本地网出发的包看起来都是从一台机子发出的，
            这台机子一般就是防火墙。
            SNAT只能用在nat表的POSTROUTING链里。
            只要连接的第一个符合条件的包被SNAT了，
            那么这个连接的其他所有的包都会自动地被SNAT,
            而且这个规则还会应用于这 个连接所在流的所有数据包。
    https://blog.csdn.net/oyyy3/article/details/121099277
        一.SNAT
            1.原理
                原理：源地址转换，修改数据包中的源IP地址 #猜测还修改了源端口地址
                作用：可以实现局域网共享上网
                配置的表及链：nat表中的POSTROUTING
            2.转换前提条件
                局域网各主机已正确设置IP地址、子网掩码、默认网关地址
                Linux网关开启IP路由转发
                linxu想系统本身是没有转发功能 只有路由发送数据 
                临时打开:
                echo 1 > /proc/sys/net/ipv4/ip_forward
                sysctl -W net.ipv4.ip_forward=1
                永久打开:
                vim /etc/sysct1.conf
                net.ipv4.ip_forward = 1    #将此行写入配置文件   
                sysctl -p                  #将取修改后的配置，使之马上生效
    https://zhuanlan.zhihu.com/p/632713274
        SNAT是指在数据包从网卡发送出去的时候，把数据包中的源地址部分替换为指定的IP，
        这样，接收方就认为数据包的来源是被替换的那个IP的主机
        MASQUERADE是用发送数据的网卡上的IP来替换源IP，
        因此，对于那些IP不固定的场合，比如拨号网络或者通过dhcp分配IP的情况下，就得用MASQUERADE
        DNAT，就是指数据包从网卡发送出去的时候，修改数据包中的目的IP，表现为如果你想访问A，
        可是因为网关做了DNAT，把所有访问A的数据包的目的IP全部修改为B，那么，你实际上访问的是B
        DNAT是在PREROUTING链上来进行的，
        而SNAT是在数据包发送出去的时候才进行，因此是在POSTROUTING链上进行的
        
REDIRECT 和 DNAT 区别
    https://www.cnblogs.com/zhangpeiyao/p/14448036.html
    DNAT可以将其数据包发送到除本机以外的其他主机和端口，
    而REDIRECT则可以将收到的数据包转发到本机的其他端口，
    所以我理解就是DNAT的策略一般都制定在专门的NAT服务器上，
    而REDIRECT的策略一般制定在目标主机上当然也可以用来代替DNAT
    https://blog.csdn.net/zhangge3663/article/details/101518356
    redirect是针对本机的，本机产生的包转到localhost的某个端口，
    适合用redirect，会比DNAT效率高点。
    而外部地址只能用DNAT了。
    
https://www.linuxso.com/linuxxitongguanli/1070.html
IPtables中SNAT和MASQUERADE的区别
一、SNAT与DNAT概念
    IPtables中可以灵活的做各种网络地址转换（NAT），网络地址转换主要有两种：SNAT和DNAT。
    
    SNAT是source network address translation的缩写，即源地址目标转换。
    比如，多个PC机使用ADSL路由器共享上网，每个PC机都配置了内网IP，
    PC机访问外部网络的时候，路由器将数据包的报头中的源地址替换成路由器的ip，
    当外部网络的服务器比如网站web服务器接到访问请求的时候，
    他的日志记录下来的是路由器的ip地址，而不是pc机的内网ip，
    这是因为，这个服务器收到的数据包的报头里边的“源地址”，
    已经被替换了，所以叫做SNAT，基于源地址的地址转换。
    注：ADSL
        传统的电话线系统使用的是铜线的低频部分（4kHz以下频段）。
        而ADSL采用DMT（离散多音频）技术，
        将原来电话线路4kHz到1.1MHz频段划分成256个频宽为4.3125khz的子频带。
        其中，4khz以下频段仍用于传送POTS（传统电话业务），
        20KhZ到138KhZ的频段用来传送上行信号，
        138KhZ到1.1MHZ的频段用来传送下行信号。
        DMT技术可以根据线路的情况调整在每个信道上所调制的比特数，以便充分地利用线路。
        一般来说，子信道的信噪比越大，在该信道上调制的比特数越多，
        如果某个子信道信噪比很差，则弃之不用。
        ADSL可达到上行640kbps、下行8Mbps的数据传输率。

    DNAT是destination network address translation的缩写，即目标网络地址转换，
    典型的应用是，有个web服务器放在内网配置内网ip，前端有个防火墙配置公网ip，
    互联网上的访问者使用公网ip来访问这个网站，当访问的时候，客户端发出一个数据包，
    这个数据包的报头里边，目标地址写的是防火墙的公网ip，
    防火墙会把这个数据包的报头改写一次，将目标地址改写成web服务器的内网ip，
    然后再把这个数据包发送到内网的web服务器上，这样，数据包就穿透了防火墙，
    并从公网ip变成了一个对内网地址的访问了，即DNAT，基于目标的网络地址转换。
    
二、MASQUERADE概念
    MASQUERADE，地址伪装，在iptables中有着和SNAT相近的效果，但也有一些区别，
    但使用SNAT的时候，出口ip的地址范围可以是一个，也可以是多个，例如：
    如下命令表示把所有10.8.0.0网段的数据包SNAT成192.168.5.3的ip然后发出去，
    iptables -t nat -A POSTROUTING -s 10.8.0.0/255.255.255.0 -o eth0 
             -j SNAT --to-source 192.168.5.3
    如下命令表示把所有10.8.0.0网段的数据包SNAT成192.168.5.3/.4/.5等几个ip然后发出去
    iptables -t nat -A POSTROUTING -s 10.8.0.0/255.255.255.0 -o eth0 
             -j SNAT --to-source 192.168.5.3-192.168.5.5
    这就是SNAT的使用方法，即可以NAT成一个地址，也可以NAT成多个地址，
    
    但是，对于SNAT，不管是几个地址，必须明确的指定要SNAT的ip，
    假如当前系统用的是ADSL动态拨号方式，那么每次拨号，出口ip192.168.5.3都会改变，
    而且改变的幅度很大，不一定是192.168.5.3到192.168.5.5范围内的地址，
    这个时候如果按照现在的方式来配置iptables就会出现问题了，
    因为每次拨号后，服务器地址都会变化，而iptables规则内的ip是不会随着自动变化的，
    每次地址变化后都必须手工修改一次iptables，
    把规则里边的固定ip改成新的ip，这样是非常不好用的。

    MASQUERADE就是针对这种场景而设计的，他的作用是，
    从服务器的网卡上，自动获取当前ip地址来做NAT。
    比如下边的命令：
    iptables -t nat -A POSTROUTING -s 10.8.0.11/255.255.255.255 -o eth0 -j MASQUERADE
    如此配置的话，不用指定SNAT的目标ip了，不管现在eth0的出口获得了怎样的动态ip，
    MASQUERADE会自动读取eth0现在的ip地址然后做SNAT出去，
    这样就实现了很好的动态SNAT地址转换。
    
    iptables [-t filter] 