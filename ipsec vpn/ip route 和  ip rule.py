https://blog.csdn.net/zhongmushu/article/details/108220232
    路由表
        所谓路由表，是指路由器或者其它互联网网络设备上存储的表，该表中存有到达特定网络终端的路径，
        在某些情况下，还有一些与这些路径相关的度量，表中包含的信息决定了数据转发的策略
        路由表根据其建立的方法，可以分为动态路由表和静态路由表。
        Linux 2.x以上，路由表由1~2^31范围内的数字或文件/etc/iproute2/rt_tables中的名称标识。
        其中，系统维护了4个路由表（0, 253, 254, and 255），其余管理员可自定义：
        0#表：系统保留表
        253#表：default table，是一个空表为一些后续处理保留的
        254#表：main table，所有没指明路由表的路由保存在该表
        255#表：local table，保存本地路由和广播路由，由系统维护
        注：路由表序号和表名的对应关系在/etc/iproute2/rt_tables 文件中，可手动编辑。
    策略路由
        策略路由简称PBR（Policy-Based Routing），是针对某种数据包，直接制定的选路策略
        策略路由是指按照用户制定的策略进行路由选择，是一种比基于目标网络进行路由更加灵活的数据包路由转发机制，
        它使网络管理员不仅能够根据目的地址，而且能够根据报文大小、应用或IP源地址等属性来选择转发路径。
    路由选择
        当TCP/IP需要向某个IP地址发起通信时，它会对路由表进行评估，以确定如何发送数据包。评估过程如下：
        (1) TCP/IP使用需要通信的目的IP地址和路由表中每一个路由项的网络掩码进行相与计算，
            如果相与后的结果匹配对应路由项的网络地址，则记录下此路由项。
        (2) 当计算完路由表中所有的路由项后:
            (a) TCP/IP选择记录下的路由项中的最长匹配路由
               （网络掩码中具有最多“1”位的路由项）来和此目的IP地址进行通信。
            (b) 如果存在多个最长匹配路由，那么选择具有最低跃点数的路由项。
            (c) 如果存在多个具有最低跃点数的最长匹配路由，那么：
                均根据最长匹配路由所对应的网络接口在网络连接的高级设置中的绑定优先级来决定
                一般有线(eth0) > 无线 (wlan0) > 移动信号(4G)。
            (d) 如果优先级一致，则选择最开始找到的最长匹配路由。(排在前面的路由)
        网络路由的优先级介于主机路由和默认路由之间，精度越高，优先级越高。
    route
        传统显示/操作内核IP路由表的工具（net-tools工具包的一部分）
        主要用途是通过接口设置到特定主机或网络的静态路由。
        1. 查看路由表信息
            route  [选项]
                -C  显示路由缓存
                -v  显示详细的操作
                -n  显示数字地址，不尝试确定主机名，加快显示速度
                -e  使用netstat格式显示路由表
                -ee 使用更详细的信息显示路由表
            路由表输出项说明：
                Destination 目标网络或目标主机
                Gateway     网关地址或”*”（如果未设置）
                Genmask     目标网络的网络掩码，”255.255.255.255”为主机，”0.0.0.0”为默认路由
                Flags       路由标记，可能的标记包括：
                            U--路由是活动的
                            H--主机路由
                            G--网关路由
                            R--恢复动态路由产生的表项
                            D--由路由的后台程序动态创建
                            M--由路由的后台程序修改
                            ! --阻塞路由
                Metric      路由距离，到达指定网络所需的跳跃数（linux内核没有使用）
                Ref         使用此路由的活动进程个数（linux内核没有使用）
                Use         查找此路由的次数
                Iface       该路由项对应的输出接口
        2. 操作静态路由
            命令格式：route [add|del] [-net|-host] target [netmask Nm] [gw Gw] [metric M] [[dev] If]
            add         添加路由 
            del         删除路由 
            -net        目标是一个网络 
            -host       目标是一个主机 
            target      目标网络或主机，可以是IP地址或网络主机名 
            netmask NM  添加网络路由时用到的网络掩码 
            netmask     匹配的位数越高该条路由匹配时的优先级也越高 
            gw GW       指定通过网关路由，后面接网关地址 
            metric M    设置路由的metric字段（路由跳数）。
                        它用在路由表里存在多个路由时选择与转发包中的目标地址最为匹配的路由，
                        所选的路由具有最少的跃点数，故Metric值越小，优先级越高。
            dev If      指定网络接口发送数据，如果dev If是最后一个选项，则dev可以省略
    ip route
        配置内核路由表中静态路由的工具，是iproute2工具包的一部分，可以和ip rule工具组合配置策略路由。
        ip route 功能和 route 差不多，但提供的功能更多，例如可以修改已有路由，
        route只能查看main表，ip route 则可以只能查看/修改哪个表
        但该命令使用较 route 命令复杂一些，而我们一般修改的又多是 main 表，所以这种情况下，用 route 命令比较方便
        在如果是查看/修改别的路由表[配合策略路由]，则只能用 ip route 命令
        1. 命令格式
            ip route { list | flush } SELECTOR
            ip route 操作命令 匹配条件 [ via [ FAMILY ] ADDRESS ] [ dev STRING ]
                ip route                查看默认路由表（main）路由
                ip route {add|append}   添加新路由
                    ip route add TARGET [via GW] [dev IFACE] [src SOURCE_IP] [table TABLEID]
                    TARGET可以是：主机路由：具体IP地址 或 网络路由：NETWORK/MASK
                ip route change         更改路由，修改当前存在的路由
                ip route replace        更改或添加新路由
                ip route {del|delete}   根据条件（to、tos、preference和table关键字值）删除指定路由
                    ip route del TARGET [via GW] [dev IFACE] [src SOURCE_IP] [table TABLEID]
                ip route {list|show}    显示路由表的内容或匹配特定条件的路由，缺省为显示main表
                    to SELECTOR             --显示特定目的地的路由
                    table TABLEID           --显示指定表的路由，TABLEID为路由表的id或all（所有路由表）、
                                              cache（路由缓存）其中之一
                    from SELECTOR           --显示特定源的路由
                    protocol RTPROTO        --显示指定协议的路由
                    scope SCOPE_VAL         --显示指定作用域的路由
                    type TYPE               --显示指定类型的路由
                    dev NAME                --显示经过指定设备接口的路由
                    via [ FAMILY ] PREFIX   --显示通过特定下一跳路由的路由
                    src PREFIX              --显示通过特定上一跳路由的路由
                    附注：
                        to TYPE PREFIX      路由目的地址，TYPE缺省为unicast，PREFIX缺省为0/0
                        metric NUMBER       路由跳数
                        preference NUMBER   路由权重
                        table TABLEID       将要操作的路由表
                        dev NAME            发送接口名称
                        via [ FAMILY ] ADDRESS  下一跳路由的地址，该字段取决于路由类型
                        src ADDRESS         指定使用特定源地址（多IP或多网卡情况），只对该主机产生的网络包有效
                        scope SCOPE_VAL     目的地作用域，SCOPE_VAL可以是数值或字符串（/etc/iproute2/rt_scopes），
                                            缺省时网关单播路由为global，直接单播和广播路由为link，本地路由为host
                        protocol RTPROTO    路由协议标记，RTPROTO可以是数值或字符串（/etc/iproute2/rt_protos），
                                            缺省时为boot，常见的有如下几种：
                                            redirect--ICMP重定义创建
                                            kernel--内核自动配置创建
                                            boot--系统启动过程创建，路由进程启动后将被删除
                                            static--管理员手动创建
                                            ra--路由发现协议创建
                ip route flush  删除特定条件的路由，参数同ip route show
                ip route get ADDRESS    获取特定IP的路由包信息
        2. 应用实例
            显示指定路由表的路由  ip route show table 10
            显示指定网段的路由  ip route list 192.168.7.0/24
            显示所有路由表的路由  ip route show table all
            通过添加路由方式添加路由表  ip route add 192.168.11.0/24 dev ens33 table 100
            通过配置文件方式添加路由表  echo "252 TEST" >> /etc/iproute2/rt_tables  //252 为路由表ID，TEST为路由表名
            添加默认路由  ip route add default via 192.168.7.1 table 10
            添加到指定网络的路由  ip route add 192.168.11.0/24 via 192.168.7.1 metric 10 table 10
            添加到指定主机的路由  ip route add 192.168.11.1 dev ens33
            追加路由  ip route append 192.168.5.0/24 via 192.168.7.1
            修改路由  ip route change 192.168.2.0/24 via 192.168.7.2
            修改路由  ip route replace 192.168.3.0/24 via 192.168.7.2
            删除指定表中默认路由  ip route del default table 100
            删除特定网络路由  ip route del 192.168.5.0/24 via 192.168.7.1
            删除指定表中特定网络路由  ip route del 192.168.1.0/24 table 100
            清空所有路由表  ip route flush
            清空指定网络的路由  ip route flush 192.168.2.0/24
    ip rule
        策略路由规则管理工具
        Linux系统在启动时，内核会为路由策略数据库配置三条缺省的规则： 
            1）优先级：0，匹配任何数据包，查询路由表local（ID 255）。
               local表是一个特殊的路由表，包含本地和广播地址的高优先级控制路由，使用者不应删除或重写它
            2）优先级：32766，匹配任何数据包，查询路由表main（ID 254）。
               main表是包含所有非策略路由的常规路由表。管理员可以删除或用其他规则重写此规则
            3）优先级：32767，匹配任何数据包，查询路由表default（ID 253）。
               default表是一个空表，它是为一些后续处理保留的。
               对于前面的缺省策略没有匹配到的数据包，系统使用这个策略进行处理，可以删除此规则
        1. 命令格式
            ip rule [ list | add | del | flush] SELECTOR ACTION           
                常见操作如下：
                    ip rule add             插入新规则
                        ip rule add 匹配条件 [优先级] [表id]
                    ip rule {del|delete}    删除特定规则
                        ip rule del [匹配条件] [优先级] [表id]
                    ip rule flush           删除所有规则，没有参数
                    ip rule show            显示规则，list和lst等同于show，没有参数
                        ip rule {show|list|lst}
                常见匹配条件如下：
                    type TYPE (default) 选择规则类型匹配
                    from PREFIX         选择源地址前缀匹配
                    to PREFIX           选择目的地址前缀匹配
                    iif NAME            选择要匹配的接收设备
                    oif NAME            选择要匹配的发送设备
                    fwmark MARK         选择fwmark值匹配
                    priority PREFERENCE 指定此规则的优先级，每个规则都有唯一优先级，preference和order等同于priority
                    table TABLEID       规则匹配时要查找的路由表标识
                附注：
                    TYPE     := unicast | blackhole | unreachable | prohibit | nat
                    ACTION   := [ table TABLE_ID ]
                                [ realms [SRCREALM/]DSTREALM ]
                                [ goto NUMBER ]
                    TABLE_ID := [ local | main | default | NUMBER ]
       2. 应用实例
            添加源IP段和目的IP策略路由  ip rule add from 192.168.7.0/24 to 8.8.8.8 prio 10 table 200
            添加接收设备策略路由  ip rule add dev ens33 table 1
            添加fwmark值策略路由  ip rule add fwmark 1 
            根据优先级删除  ip rule del prio 10
            根据匹配条件删除  ip rule del from 192.168.7.0/24 to 8.8.8.8
            根据路由表id删除  ip rule del table 200
            根据匹配条件、表id和优先级删除  ip rule del from 192.168.7.0/24 to 8.8.8.8 prio 10 table 200
            
https://blog.csdn.net/ZYJY2020/article/details/121517724            
    一、 什么是策略路由
        策略路由简称PBR（Policy-Based Routing），是针对某种数据包，直接制定的选路策略。
        都是选路，那策略路由和普通路由有什么区别？
        举个例子来看:   file://imgs/路由情形1.png
        现在希望张三访问外网走线路1，其他人访问外网走线路2。 如果在路由器上，用常规路由如何实现？
        是不是发现常规路由无法完成，因为常规路由都是按目标地址来选路，而这里的需求，是按源地址选路。
        只要源地址为张三的数据包，就走线路1，不管目标是什么。
        今天的主角，策略路由很容易解决这个问题。
        策略路由的做法是，首先用ACL来定义一种特别的数据包（比如源地址为张三的包），
        然后再针对这个ACL定义的包，配置一个选路策略（走线路1）
        有关 ACL（访问控制列表Access Control List）的知识，可参看： file://ipsec协议.py
    二、 为什么要做策略路由
        虽然策略路由配置起来相对复杂，选路策略也必须手动指定，不会像OSPF一样自动学习路由表，
        但是实际项目中还是经常会用到策略路由，来实现常规路由无法实现的需求。
        ospf
            开放式最短路径优先（Open Shortest Path First，OSPF）是广泛使用的一种动态路由协议
            实现过程
            1、初始化形成端口初始信息：
               在路由器初始化或网络结构发生变化(如链路发生变化，路由器新增或损坏)时，
               相关路由器会产生链路状态广播数据包LSA，该数据包里包含路由器上所有相连链路，
               也即为所有端口的状态信息。
            2、路由器间通过泛洪(Flooding)机制交换链路状态信息：
               各路由器一方面将其LSA数据包传送给所有与其相邻的OSPF路由器，
               另一方面接收其相邻的OSPF路由器传来的LSA数据包，根据其更新自己的数据库。
            3、形成稳定的区域拓扑结构数据库：
               OSPF路由协议通过泛洪法逐渐收敛，形成该区域拓扑结构的数据库，
               这时所有的路由器均保留了该数据库的一个副本。
            4、形成路由表：
               所有的路由器根据其区域拓扑结构数据库副本采用最短路径法计算形成各自的路由表。
               
https://blog.csdn.net/gengzhikui1992/article/details/103782077
    1. 策略路由简介
        对比传统的基于数据包目的地址的路由算法，基于策略的路由算法更加灵活。
        策略路由算法引入了多路由表以及规则的概念，
        支持按数据报属性（源地址、目的地址、协议、端口、数据包大小、内容等规则）选择不同路由表。
        Linux是在内核2.1开始采用策略性路由机制的。
    2. 策略路由原理
        2.1 多路由表（multiple Routing Tables)
            传统的路由算法是仅使用一张路由表的。
            但是在有些情形底下，我们是需要使用多路由表的。
            例如一个子网通过一个路由器与外界相连，
            路由器与外界有两条线路相连，其中一条的速度比较快，一条的速度比较慢。
            对于子网内的大多数用户来说对速度并没有特殊的要求，所以可以让他们用比较慢的路由；
            是子网内有一些特殊的用户却是对速度的要求比较苛刻，所以他们需要使用速度比较快的路由。
            如果使用一张路由表上述要求是无法实现的，
            而如果根据源地址或其它参数，对不同的用户使用不同的路由表，这样就可以大大提高路由器的性能。
        2.2 规则（rule)
            规则是策略性的关键性的新的概念。
            规则包含3个要素：
            什么样的包，将应用本规则（所谓的SELECTOR，可能是filter更能反映其作用）；
            符合本规则的包将对其采取什么动作（ACTION），例如用那个表；
            本规则的优先级别。优先级别越高的规则越先匹配（数值越小优先级别越高）。
     linux策略路由配置方式
        传统的linux下配置路由的工具是route，而实现策略性路由配置的工具是iproute2工具包。
        3.1 接口地址的配置 IP Addr
            添加/删除网络接口： ip addr [ add | del ] IFADDR dev STRING
            例：ip addr add 192.168.0.1/24 broadcast 192.168.0.255 label eth0 dev eth0
            上面表示，给接口eth0赋予地址192.168.0.1 掩码是255.255.255.0(24代表掩码中1的个数)，广播地址是192.168.0.255
        3.2 路由的配置 IP Route
            Linux最多可以支持255张路由表，其中有3张表是内置的：
            表255 本地路由表（Local table）
                本地接口地址，广播地址，已及NAT地址都放在这个表。
                该路由表由系统自动维护，管理员不能直接修改。
            表254 主路由表（Main table）
                如果没有指明路由所属的表，所有的路由都默认都放在这个表里，
                一般来说，旧的路由工具（如route）所添加的路由都会加到这个表。
                一般是普通的路由。
            表253 默认路由表（Default table）
                一般来说默认的路由都放在这张表，但是如果特别指明放的也可以是所有的网关路由。
            表 0 保留
        3.3 规则的配置 IP Rule
            在Linux里，总共可以定义232个优先级的规则，一个优先级别只能有一条规则，
            即理论上总共可以有232条规则。其中有3个规则是默认的
            首先我们可以看看路由表默认的所有规则：
                root@netmonster# ip rule list
                0: from all lookup local
                32766: from all lookup main
                32767: from all lookup default
                规则0，它是优先级别最高的规则，规则规定，所有的包，
                都必须首先使用local表（254）进行路由。本规则不能被更改和删除。
                规则32766，规定所有的包，使用表main进行路由。本规则可以被更改和删除。
                规则32767，规定所有的包，使用表default进行路由。本规则可以被更改和删除。
            规则的作用：
                首先会根据规则0在本地路由表里寻找路由，
                如果目的地址是本网络，或是广播地址的话，在这里就可以找到合适的路由；
                如果路由失败，就会匹配下一个不空的规则，
                在这里只有32766规则，在这里将会在主路由表里寻找路由;
                如果失败，就会匹配32767规则，即寻找默认路由表。
                如果失败，路由将失败。
            命令用法：
                Usage: ip rule [ list | add | del ] SELECTOR ACTION
                SELECTOR := [ from PREFIX ] [ to PREFIX ] [ tos TOS ] [ dev STRING ] [ pref NUMBER ]
                ACTION   := [ table TABLE_ID ] [ nat ADDRESS ] [ prohibit | reject | unreachable ] [ flowid CLASSID ]
                TABLE_ID := [ local | main | default | new | NUMBER
                附注：
                From -- 源地址
                To -- 目的地址（这里是选择规则时使用，查找路由表时也使用）
                Tos -- IP包头的TOS（type of sevice）域
                Dev -- 物理接口
                Fwmark -- 防火墙参数
                Table 指明所使用的表
            　  Nat 透明网关
            　　Action prohibit 丢弃该包，并发送 COMM.ADM.PROHIITED的ICMP信息
            　　Reject 单纯丢弃该包
            　　Unreachable丢弃该包，并发送 NET UNREACHABLE的ICMP信息

结合strongswan分析
    swanctl设置过后，ip rule list， 多出 220 这条规则 from all lookup 220 
    # ip route list table 220
    192.168.3.99 via 192.168.3.99 dev eno16777736 proto static src 192.168.3.29 
    trongswan默认安装路由到路由表220
