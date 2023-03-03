相关文档资料：
file://../ipsec百度百科.txt
file://../ip-xfrm.man.txt
file://../IPSec之IKEv2协议详解.py
file://../ipsec协议.py
file://../ipsec百度百科.txt
file://../IPsec相关的一些基本概念.txt
file://../ipsec详解.txt
file://../Linux Netlink机制.py
file://../PF_KEY协议.txt
file://../ppp协议.txt
file://../xfrm.txt
file://../图解Linux网络包发送过程.pdf
file://../路由表.txt
file://../防火墙技术连载.py

https://blog.imkasen.com/strongswan-config.html
strongSwan简介
    strongSwan，是一个完整的开源 IPsec VPN 解决方案，
    可以运行在 Linux、Windows 和 Mac OS X 上，
    此外，它还兼容基于 Android 和 iOS 的产品所支持的 IPsec 功能。
    要注意的是，strongSwan 并不对 VPN 上的数据进行加密，
    而是由运行 strongSwan 的底层操作系统（比如 Linux）进行加密。
    strongSwan 负责使用网络密钥交换（internet key exchange, IKE）协议
    帮助同级协商用于对称加密的密钥。
    strongSwan 支持 IKEv1 和 IKEv2。
    strongSwan 在一个叫 pluto 的服务中实现了 IKEv1，
    而 IKEv2 则由一个叫 charon 的服务提供。
Linux IPsec 支持
    1998年开始的 KAME 项目是第一个努力实现 IPv4 和 IPv6 的免费 IPsec 协议栈的项目。
    该项目的实施是为了 BSD UNIX 系统，但很快就作为 Linux 内核的补丁。
    大约在同一时间，John Gilmore启动了 FreeS/WAN 项目，旨在将 IPsec 引入 Linux。
    这也需要给 Linux 内核打补丁。FreeS/WAN 补丁被称为 Kernel IP Security（KLIPS）。
    在这两种情况下(KAME 和 KLIPS)，都需要打补丁
    来允许在用户空间运行的 IKE 服务与内核空间的对应服务进行通信，
    以安装加密密钥和配置各种加密参数。
    IETF 在 RFC 2367 中定义了 PF_KEYv2，作为标准 API，
    允许用户空间进程在操作系统内核中配置 IPsec。
    KAME 和 KLIPS 都使用了 PF_KEYv2。
    为每个内核版本维护 KAME 和 KLIPS 的补丁是很有挑战性的，
    因此决定在 Linux 2.6 内核系列中把 KAME 作为默认的 IPsec 协议栈。
    2.6 内核下的 KAME 实现被称为 NETKEY。
    然而，2.6 内核的特点是修改了协议栈，其中一个新特性是一个叫做 NETLINK 的协议。
    与 PF_KEYv2 不同，NETLINK 是一个通用的协议，
    它允许用户空间实体与内核的各个部分交换消息。
    例如，RT_NETLINK 是一个 NETLINK 扩展，它可以让动态路由进程在内核中安装或删除路由。
    同样，XFRM_NETLINK 9 允许 IKE 或其他用户进程管理内核中维护的 IPsec 安全关联数据库
    （Security Association Database, SAD）和安全策略数据库（Security Policy Database, SPD）。
策略路由
    strongSwan 使用了一种叫做策略路由的网络功能。这与 SPD 和 IPsec 使用的安全策略不同。
    正常的 IP 路由是基于 IP 头中的目标 IP 地址字段。
    启用 IP 转发的主机将为所有前往特定目的地的数据包选择相同的路径。
    这种情况并不总是可取的。
    策略路由的一个早期案例是支持不同客户类别的不同 QoS 级别。
    金牌客户为获得高吞吐量和低延迟服务而付费，而青铜客户则为更便宜的尽力服务而解决。
    为这些客户选择路由时，除其他外，还需要将源 IP 地址和目的地址作为 IP 路由过程的一部分。
    Linux 策略路由的实现需要多个路由表和一个路由策略数据库（RPDB）。
    你可以通过输入以下命令列出 RPDB 中的策略：ip rule show
    输出应该显示这样的内容：
        0:     from all lookup local 
        220:   from all lookup 220 
        32766: from all lookup main 
        32767: from all lookup default
    要在表中列出可用的路由（例如，local），使用以下命令：
    ip route list table local
    输出应该是这样的：
        broadcast 127.0.0.0 dev lo proto kernel scope link src 127.0.0.1
        local 127.0.0.0/8 dev lo proto kernel scope host src 127.0.0.1
        local 127.0.0.1 dev lo proto kernel scope host src 127.0.0.1
        broadcast 127.255.255.255 dev lo proto kernel scope link src 127.0.0.1
        broadcast 192.168.3.0 dev br0 proto kernel scope link src 192.168.3.229
        local 192.168.3.229 dev br0 proto kernel scope host src 192.168.3.229
        broadcast 192.168.3.255 dev br0 proto kernel scope link src 192.168.3.229
        broadcast 192.168.122.0 dev virbr0 proto kernel scope link src 192.168.122.1
        local 192.168.122.1 dev virbr0 proto kernel scope host src 192.168.122.1
        broadcast 192.168.122.255 dev virbr0 proto kernel scope link src 192.168.122.1
    可用的规则从最高优先级（0）到最低优先级（32767）进行扫描，
    一旦 RPDB 策略匹配，就会使用指定的表来查找下一跳
    如果路由过程无法从规则所指示的路由表计算出数据包的下一跳，
    则继续处理到 RPDB 中的下一条规则
    from 关键字表示对源 IP 地址的选择符，
    但由于也使用了 all ，所以表示所有数据包都会匹配
    默认情况下，strongSwan 会插入一个优先级为 220 的策略规则。
    当 Ubuntu Linux 启动时，它会设置三个表：local（id 255）、main（254）和default（253）
    本地路由表包含本地和广播地址的高优先级控制路由。
    这个表是供内核内部使用的，不应该从用户空间修改。
    主路由表是在没有指定表时使用的普通表。
    默认表通常是空的，当没有其他表匹配时使用。
   
https://blog.csdn.net/wq897387/article/details/123446862
strongswan代码目录介绍
    https://docs.strongswan.org/docs/5.9/plugins/plugins.html
        这里是官方的对每个插件的功能说明
根目录
    文件夹	描述
    conf	配置文件
    doc	    RFC标准文档
    init	初始化信息
    src	    源代码文件
    scripts	脚本信息
    testing	测试程序
src目录
    Component	    Description
    aikgen	        Utility to generate an Attestation Identity Key bound to a TPM 1.2
    charon	        IKE 密钥守护进程
    charon-cmd	    命令行 IKE 客户端
    charon-nm	    NetworkManager D-BUS 插件的后端
    charon-svc	    Windows IKE 服务
    charon-systemd	一个 IKE 守护进程，类似于 charon，但专门设计用于 systemd
    charon-tkm	    由可信密钥管理器 (TKM) 支持的 charon 变体
    checksum	    生成已构建可执行文件和库的校验和的实用程序
    conftest	    一致性测试工具
    frontends/android	适用于 Android 的 VPN 客户端
    frontends/gnome	NetworkManager plugin
    frontends/osx	用于本机 macOS 应用程序的 charon-xpc 助手守护程序
    ipsec	        对传统的 ipsec 命令行工具的包装命令和其他工具
    libcharon	    包含charon守护进程的大部分代码和插件
    libfast	        使用 ClearSilver 和 FastCGI 构建本地 Web 应用程序的轻量级框架
    libimcv	        各种完整性测量收集器 (IMC), 完整性测量验证器 (IMVs) 和他们共享的库代码
    libipsec	    kernel-libipsec 和 Android VPN 客户端应用程序使用的用户级 IPsec 实现
    libpts	        包含基于 TPM 的平台信任服务 (PTS) 和 SWID 标签处理的代码
    libpttls	    实现 PT-TLS 协议
    libradius	    RADIUS 协议实现（被例如 eap-radius 和 tnc-pdp 插件等使用）
    libsimaka	    包含多个 EAP-SIM/AKA 插件共享的代码
    libstrongswan	具有守护进程和实用程序使用的基本功能的 strongSwan 库
    libtls	        eap-tls、eap-ttls、eap-peap 和其他插件使用的 TLS 实现
    libtnccs	    实现 IF-TNCCS 接口
    libtncif	    实现 IF-IMC/IF-IMV 接口
    manager	        一个废弃的基于 libfast 的 charon 图形管理应用程序
    medsrv	        基于 libfast 的中介服务器实验管理前端
    pki	            公钥基础设施实用程序
    pool	        用于管理 attr-sql 插件提供的属性和 IP 地址池的实用程序
    pt-tls-client	Integrity measurement（完整性测量） client using the PT-TLS protocol
    scepclient	    使用 SCEP 协议注册证书的实用程序
    sec-updater	    实用程序提取有关 Linux 存储库的安全更新和反向移植的信息
    starter	        读取 ipsec.conf 并控制监控守护进程 charon 的传统守护进程
    stroke	        通过 stroke 协议控制 charon 的传统命令行实用程序
    swanctl	        通过 vici 接口进行通信的配置和控制实用程序
    sw-collector	从 apt 历史日志中提取有关软件包安装、更新或删除事件的信息的实用程序
    tpm_extendpcr	Tool that extends a digest into a TPM PCR
    _updown	        Default script called by the updown plugin on tunnel up/down events
    xfrmi	        创建 XFRM 接口
src/libstrongswan目录
    文件	                                描述
    backtrace.c backtrace.h	                回溯
    chunk.c chunk.h	                        块
    debug.c debug.h	                        调试
    integrity_checker.c integrity_checker.h	完整性检查
    lexparser.c lexparser.h	                ？
    printf_hook/	                        ？
    utils/ utils.c utils.h	                ？
    compat/	                                兼容性
    enum.c enum.h	                        枚举
    optionsfrom.c optionsfrom.h	            参数
    process.c process.h	                    处理
    capabilities.c capabilities.h	        能力
    cpu_feature.c cpu_feature.h	            CPU特性
    leak_detective.c leak_detective.h	    丢包检测
    identification.c identification.h	    识别
    parser_helper.c parser_helper.h	        解析帮助
    test.c test.h	                        测试
   
https://blog.csdn.net/weixin_30472035/article/details/96492625   
ipsec.conf是stroke插件使用的配置文件，可以配置ike proposal、ike peer、ipsec proposal等属性   
注：ipsec.conf这个配置文件在strongswan后续版本慢慢会废弃了，代替的是使用swanctl.conf
   
https://blog.csdn.net/lz619719265/article/details/91041359
ipsec.conf各配置项的介绍   
   
https://docs.strongswan.org/docs/5.9/config/IKEv2.html
strongswan 配置文件各种应用示例   
   
https://wiki.strongswan.org/projects/strongswan/wiki/Fromipsecconf
从 ipsec.conf 迁移到 swanctl.conf
    Noel Kuntze写了一个python脚本，用于将ipsec.conf翻译成swanctl.conf。
    在ipsec.conf和ipsec.secrets中的每一项，都有在swanctl.conf中的对等转换，
    具体对应关系，请参看原链接
注：ipsec.conf这个配置文件在strongswan后续版本慢慢会废弃了，代替的是使用swanctl.conf
   
https://www.cnblogs.com/hugetong/p/11143357.html
charon进程初始化阶段的流程图
约定：
    实线代表流程图。
    虚线代表调用栈，箭头方向代表自上而下。
    黄线是辅助线，请自己理解
图：file://../imgs/strongswan流程图.png
图：file://../imgs/netlink模块的类图.png
图：file://../imgs/从Task到内核xfrm模块的调用关系图.png
说明：
    该图以kernel-netlink plugin为例分析了strongswan 5.7.1的主要代码架构。
    该图仅体现架构的部分侧面，不以展示全貌为目的。

https://www.cnblogs.com/hugetong/p/11143366.html
strongswan SA分析（一）
1 概念
    下面主要介绍两个本文将要阐述的核心概念。
    他们是SA和SP。注意，这不是一篇不需要背景知识的文章。
    作者认为你适合阅读接下来内容的的前提是，你已经具备了一下三方面的知识：
    a. 什么是VPN。
    b. 什么是IPsec，包括IKE，ESP，strongswan都是什么等。
    c. 一般的linux使用方法和常见概念。
    1.1 什么是SAD，SPD
        SAD是Security Association Database的缩写。
        SPD是Security Policy Database的缩写。
        SAD是用来存储SA的数据库。SPD是用来存储SP的数据库。
    1.2 什么是SPI
        SPI是Security Parameter Index的缩写。是有一组数字（长度？）。
        被使用在SAD和SPD里作为索引的一部分。是由IKE协商的两侧客户端随机选择的UUID？。
        0-255是被保留的值，禁止在SPI中使用。
    1.3 什么是SA
        SA是Security Association的缩写。
        SA是一组算法和算法参数（包括key）的集合，用来完成单个方向的数据流加密和验证任务。
        通过SPI加数据包的目的地址可以唯一查找到一个SA。
        包含的属性：
            加密算法
                属性
                key
            验证算法
                属性
                key
            SPI
            目的地址
    1.4 什么是SP
        SP是Security Policy的缩写。
        SP是一条规则，决定一条流（flow）是否需要被IPsec处理。
        SP的处理有三种方式：
            丢弃
            不处理
            处理
        需要被IPsec处理的流，会被指向到一个template。
        一个template可以理解为指向一个SA，template包含以下属性：
            协议
                AH或ESP。
            模式
                transport或tunnel模式。
            pattern
                源IP加目的IP对。
                NAT的PORT对。
            SP有一个方向属性，取值分别为：
                out
                in
                fwd
    1.5 总结
        在整个IPsec的数据流转逻辑中，SP用来表达What todo。SA用来表达How todo。
2 数据流
    简单的说。明文报在通过IPsec VPN设备变成ESP发出去的过程是：
        查找路由。
        查找policy决定是否需要被ESP
        查找SA并加密封装。
        加密封装后的包再查路由。
    IPsec报在通过IPsec VPN设备变成非加密包发出去的过程：
        查找路由。
        查找policy决定是否需要要解ESP
        查找SA并解密解封装。
        解密解封装后的包再查路由。
    图：file://../imgs/网络包的流动图.png
3 理解linux kernel中的sa概念和管理
    3.1 提供给用户的sa接口
        理解kernel sa对用户展示的形态，可以帮助我们理解linux kernel对于ipsec sa的建模和抽象。
        对我们在VPN产品的sa模块设计中将提供帮助。
        3.1.1 使用racoon配置sa
            setkey add 192.168.0.1 192.168.1.2 esp 0x10001
                        -m tunnel
                        -E des-cbc 0x3ffe05014819ffff
                        -A hmac-md5 "authentication!!"
            从以上信息可以很容易看出各个参数表达的含义，
            其中-E代表加密算法和它的key，-A代表验证算法和它的key。0x10001为spi
        3.1.2 使用racoon配置policy(有关racoon，参：https://blog.csdn.net/zhangyang0402/article/details/5730123）
            setkey spdadd 10.0.11.41/32[21] 10.0.11.33/32[any] any
                          -P out ipsec esp/tunnel/192.168.0.1-192.168.1.2/require
            第一行代表五元组，any代表协议。
            第二行代表policy的具体描述：方向，action，template
        3.1.3 总结
            通过以上两个小节的描述，读者应该已经很容易的总结出了配置一个SA和一个policy所需要提供的最基本的信息了。
            作者将在本章的最后，对sa和policy所包含的所有必须信息进行一个统一的总结。
            另外，通过上文的语法，我们应该能够发现，policy与sa之间的match操作，
            是需要一个稍复杂的匹配逻辑来实现的，而不仅仅是一个简单的匹配关系。
    3.2 netlink的SA接口
        strongswan是目前使用两种方式与内核进行ipsec的配置交互，
        分别为netlink和pfkey：<file://../Linux Netlink机制.py> <file://../PF_KEY协议.txt>
        如官方文档所述，netlink是strongswan默认启用的，变成stable的接口方式。
        整个调研工作也是以netlink方式为出发点展开的，现简单介绍如下
        3.2.1 什么是netlink
            netlink是复用了socket方式的内核与用户态IPC方法
            Why and How to Use Netlink Socket: https://www.linuxjournal.com/article/7356
        3.2.2 接口方式
            用netlink方式配置ipsec的方法
            netlink的一般用法
                初始化socket
                    与常规的socket用法相同，只是传入参数是netlink定义的特有参数
                下发配置信息到kernel
                    使用socket的标准send，write接口将特定格式的参数下发给kernel
                    参数格式如下
                        struct nlmsghdr
                        {
                          __u32 nlmsg_len;   /* Length of message */
                          __u16 nlmsg_type;  /* Message type*/
                          __u16 nlmsg_flags; /* Additional flags */
                          __u32 nlmsg_seq;   /* Sequence number */
                          __u32 nlmsg_pid;   /* Sending process PID */
                        };
                    这个参数结构体是传入参数的头部，紧接着这个头部之后的内存是真正的参数的值。
                    它的解析方法由nlmsg_type的值来确定。它的结尾由nlmsg_len的数值来决定
                添加sa
                    添加sa的时候，nlmsghdr后面的参数为结构体
                    struct xfrm_usersa_info
                    nlmsg_type的值为：XFRM_MSG_NEWSA
                    这部分内容定义在系统文件 /usr/include/linux/xfrm.h
                    这个结构体后边，还需要追加算法部分的信息，如下
                    struct xfrm_algo
                    struct xfrm_algo_auth
                添加policy
                    添加policy的时候，nlmsghdr后面的参数为结构体
                    struct xfrm_userpolicy_info
                    nlmsg_type的值为：XFRM_MSG_NEWPOLICY
                    这部分内容定义在系统文件 /usr/include/linux/xfrm.h
    3.3 xfrm的SA接口
        3.3.1 什么是xfrm
            xfrm(transform)是一个IP包转发框架。主要实现以下三部分功能：
                IPsec protocol suite
                IP Payload Compression Protocol
                Mobile IPv6
        3.3.2 内核代码
            linux/net/xfrm/
            主要函数
                Xfrm_lookup()            xfrm lookup(SPD and SAD) method
                Xfrm_input()             xfrm processing for an ingress packet
                Xfrm_output()            xfrm processing for an egress packet
                Xfrm4_rcv()              IPv4 specific Rx method
                Xfrm6_rcv()              IPv6 specific Rx method
                Esp_input()              ESP processing for an ingress packet
                Esp_output()             ESP processing for an egress packet
                Ah_output()              AH processing for an ingress packet
                Ah_input()               ESP processing for an egress packet
                xfrm_policy_alloc()      allocates an SPD object
                Xfrm_policy_destroy()    frees an SPD object
                xfrm_policy_lookup       SPD lookup
                xfrm_policy_byid()       SPD lookup based on id
                Xfrm_policy_insert()     Add an entry to SPD
                Xfrm_Policy_delete()     remove an entry from SPD
                Xfrm_bundle_create()     creates a xfrm bundle
                Xfrm_policy_delete()     releases the resources of a policy object
                Xfrm_state_add()         add an entry to SAD
                Xfrm_state_delete()      free and SAD object
                Xfrm_state_alloc()       allocate an SAD object
                xfrm_state_lookup_byaddr()     src address based SAD lookup
                xfrm_state_find()        SAD look up based on dst
                xfrm_state_lookup()      SAD lookup based on spi
        3.3.3 API
            api文件  include/uapi/linux/xfrm.h ？？
        3.3.4 sa的传入参数
            struct xfrm_usersa_info {
                    struct xfrm_selector            sel; // 被加密网段？为啥要有这个？
                    struct xfrm_id                  id; // 目的ip，spi，协议ah/esp
                    xfrm_address_t                  saddr; // 源ip
                    struct xfrm_lifetime_cfg        lft;
                    struct xfrm_lifetime_cur        curlft;
                    struct xfrm_stats               stats;
                    __u32                           seq;
                    __u32                           reqid;
                    __u16                           family;
                    __u8                            mode; // transport / tunnel
                    __u8                            replay_window;
                    __u8                            flags;
            };  
            算法参数是追加在SA结构体之后的内存块，根据不同的类型决定不同的结构。示例：
            struct xfrm_algo {
                    char            alg_name[64];
                    unsigned int    alg_key_len;    /* in bits */
                    char            alg_key[0];
            };
            struct xfrm_algo_auth {
                    char            alg_name[64];
                    unsigned int    alg_key_len;    /* in bits */
                    unsigned int    alg_trunc_len;  /* in bits */
                    char            alg_key[0];
            };
        3.3.5 policy的传入参数
            struct xfrm_userpolicy_info {
                    struct xfrm_selector            sel; //网段：ip，port，协议
                    struct xfrm_lifetime_cfg        lft;
                    struct xfrm_lifetime_cur        curlft;
                    __u32                           priority; //
                    __u32                           index;
                    __u8                            dir;  //方向：in out fwd
                    __u8                            action; // allow, block
                    __u8                            flags;
                    __u8                            share;
            };
    4 xfrm的实现
        4.1 用于存储sa的内部数据结构
            struct xfrm_state  参：file://xfrm.txt
        4.2 用于存储sp的内部数据结构
            struct xfrm_policy 参：file://xfrm.txt
        4.3 关键函数
            xfrm_lookup()
            xfrm_output()
            xfrm4_policy_check() // 在ipv4中被调用。
    5 strongswan中的sa
        5.1 概述
            从IKE协议的角度上，有两个SA，一个叫IKE_SA，一个叫CHILD_SA。
            本章讨论的sa，特指下图中的CHILD_SA。
                  +---------------------------------+       +----------------------------+
                  |          Credentials            |       |          Backends          |
                  +---------------------------------+       +----------------------------+

                   +------------+    +-----------+          +------+            +----------+
                   |  receiver  |    |           |          |      |  +------+  | CHILD_SA |
                   +----+-------+    | Scheduler |          | IKE- |  | IKE- |--+----------+
                        |            |           |          | SA   |--| SA   |  | CHILD_SA |
                   +-------+--+      +-----------+          |      |  +------+  +----------+
                <->|  socket  |            |                | Man- |
                   +-------+--+      +-----------+          | ager |  +------+  +----------+
                        |            |           |          |      |  | IKE- |--| CHILD_SA |
                   +----+-------+    | Processor |----------|      |--| SA   |  +----------+
                   |   sender   |    |           |          |      |  +------+
                   +------------+    +-----------+          +------+

                  +---------------------------------+       +----------------------------+
                  |               Bus               |       |      Kernel Interface      |
                  +---------------------------------+       +----------------------------+
                         |                    |                           |
                  +-------------+     +-------------+                     V
                  | File-Logger |     |  Sys-Logger |                  //////
                  +-------------+     +-------------+
            本篇文章，通篇讨论的SA指的都是这里的CHILD_SA。
            CHILD_SA在strongswan的框架里，主要存在与两个部分。
                IKE协商过程。
                    CHILD_SA是IKE协商过程中的输出（理解：IKE协商过程通过CHILD_SA进行输出操作）
                    IKE协商过程结束后，IKE-SA Manager将CHILD_SA交给strongswan框架。
                IPsec隧道建立过程。
                    CHILD_SA是IKE协商过程中的输入（理解：IKE协商过程通过CHILD_SA进行输入操作）
                    strongswan框架将CHILD_SA交给libcharon plugin
                    由特定的plugin与kernel通信，
                    在kernel中完成IPsec tunnel的建立过程。
                IPsec在转发过程。
                    这部分和strongswan的框架没有了关系，由内核完成。
            5.1.1 strongswan中的plugin
                上一小节提到了plugin，接下来讲解plugin。
                有两类plugins。一类是libstrongswan的plugin，一类是libcharon的plugin。
                libstrongswan的plugin主要提供加密，认证，数据库相关的功能。
                libcharon的plugin主要提供“specific needs”。。。
                我们接下来要讨论的与sa下发相关的plugin都在libcharon这一类里。他们包括：
                    kernel-libipsec
                        用户态的转发平面，目前还处于高实验性阶段。转发性能没用kernel。
                        主要用来满足不能使用kernel转发的场景。
                    kernel-netlink
                        使用netlink接口与linux kernel的xfrm模块交互。目前输出稳定使用阶段，默认首选。
                    kernel-pfkey
                        使用pkkey接口与linux kernel的xfrm模块进行交互，高实验性阶段。
                    kernel-iph
                        windows操作系统的接口。
                    kernel-wfp
                        windows操作系统的接口。
                本文，只关心kernel-netlink的plugin
        5.2 启动过程
            5.2.1 概述
                strongswan的启动方式有多种。可以和各种不同的系统对接，包括systemd，networkmanager等。
                    starter
                        ipsec命令使用的守护进程。用ipsec start命令，就会启动这个进程。
                    charon-nm
                        networkmanager的plugin。什么是nm的plugin？
                    charon-systemd
                        按照systemd的daemon style实现的一个进程。由systemd启动。
                    charon-svc
                        windows的服务。
                各种启动方式的最终目的都是启动最终目的都是启动charon进程。所以，最简的启动方法就是：
                直接运行 charon 进程
                当然，这种方式没有daemon守护，但是功能完整。
            5.2.2 调试方法
                如上一小节所述。charon进程可以直接运行。所以调试的时候直接使用gdb运行charon就可以了
                # gdb `which charon`
            5.2.3 starter的启动过程
                ipsec实用程序调用了“参与控制和监控IPsec加密/认证系统的”几个实用程序中的任何一个，
                用指定的参数和选项运行指定的命令，就像直接调用它一样。
                这在很大程度上消除了与其他软件可能出现的名称冲突，同时也允许一些集中的服务。
                对于其他命令，ipsec为被调用的命令提供了合适的环境变量。
                ipsec start 的功能是调用starter，而starter又解析ipsec.conf并启动IKE守护程序charon
                starter的启动方法是通过ipsec脚本执行start命令(ipsec start)，这样便启动了strongswan服务。
                脚本位置：strongswan-5.7.1/src/ipsec/_ipsec
                ipsec脚本解析start参数后，会执行如下命令，启动守护进程starter
                ${IPSEC_DIR}/starter --daemon charon
                starter进程的源码位置：strongswan-5.7.1/src/starter/starter.c
                starter的主要功能是启动charon进程，并进行守护。
                    ● daemon的初始工作，重定向输出，signal响应等。
                    ● 启动charon
                    ● 加载ipsec.conf中的配置
            5.2.4 systemd的启动过程
                systemd的启动过程首先使用systemd的service配置脚本
                然后启动systemd的charon守护进程（charon-systemd进程）
                最后通过守护进程启动charon进程
                systemd脚本位置：
                strongswan-5.7.1/init/systemd-swanctl/strongswan-swanctl.service.in
                service脚本在启动过程执行两个操作
                1. 启动charon-systemd进程。
                2. 执行swanctl --load-all --noprompt命令
                charon-systemd进程
                    源码位置：strongswan-5.7.1/src/charon-systemd/charon-systemd.c
                    charon-systemd进程是charon进程的另一个入口。
                    charon-systemd进程不会在启动新的进程，
                    charon-systemed进程就是处理业务的主进程，有systemd进行守护。
                    所以，charon-systemd只有main函数中的少量内容与charon不同。
                    其他逻辑与charon进程完全相同
        5.3 调用过程
                运行过程中，与SA相关的两个部分主要就是add_sa与add_policy两个地方
                当charon进程收到一个message的时候，会以job的形式分发给standby的业务线程进行处理
                最后通过kernel对象调用kernel_interface接口中的add_sa和add_policy两个函数。
                接口会根据具体注册的plugin调用各plugin的相应，add_as, add_policy函数
                例如，netlink的plugin，在该plugin的这两个函数中，
                会通过netlink的接口最终调用内核的xfrm接口完成sa和policy的下发和更新等操作
        5.4 strongswan中的数据结构
                sa数据结构
                    定义在文件 kernel_ipsec.h 中，由id和data两个结构共同组成
                    struct kernel_ipsec_sa_id_t {
                            /** Source address */
                            host_t *src;
                            /** Destination address */
                            host_t *dst;
                            /** SPI */
                            uint32_t spi;
                            /** Protocol (ESP/AH) */
                            uint8_t proto;
                            /** Optional mark */
                            mark_t mark;
                    }; 
                    //Data required to add an SA to the kernel
                    struct kernel_ipsec_add_sa_t {
                            /** Reqid */
                            uint32_t reqid;
                            /** Mode (tunnel, transport...) */
                            ipsec_mode_t mode;
                            /** List of source traffic selectors */
                            linked_list_t *src_ts;
                            /** List of destination traffic selectors */
                            linked_list_t *dst_ts;
                            /** Network interface restricting policy */
                            char *interface;
                            /** Lifetime configuration */
                            lifetime_cfg_t *lifetime;
                            /** Encryption algorithm */
                            uint16_t enc_alg;
                            /** Encryption key */
                            chunk_t enc_key;
                            /** Integrity protection algorithm */
                            uint16_t int_alg;
                            /** Integrity protection key */
                            chunk_t int_key;
                            /** Anti-replay window size */
                            uint32_t replay_window;
                            /** Traffic Flow Confidentiality padding */
                            uint32_t tfc;
                            /** IPComp transform */
                            uint16_t ipcomp;
                            /** CPI for IPComp */
                            uint16_t cpi;
                            /** TRUE to enable UDP encapsulation for NAT traversal */
                            bool encap;
                            /** no (disabled), yes (enabled), auto (enabled if supported) */
                            hw_offload_t hw_offload;
                            /** Mark the SA should apply to packets after processing */
                            mark_t mark;
                            /** TRUE to use Extended Sequence Numbers */
                            bool esn;
                            /** TRUE to copy the DF bit to the outer IPv4 header in tunnel mode */
                            bool copy_df;
                            /** TRUE to copy the ECN header field to/from the outer header */
                            bool copy_ecn;
                            /** Whether to copy the DSCP header field to/from the outer header */
                            dscp_copy_t copy_dscp;
                            /** TRUE if initiator of the exchange creating the SA */
                            bool initiator;
                            /** TRUE if this is an inbound SA */
                            bool inbound;
                            /** TRUE if an SPI has already been allocated for this SA */
                            bool update;
                    }; 
                policy数据结构
                    定义在文件 kernel_ipsec.h 和 ipsec_types.h 中
                    struct kernel_ipsec_policy_id_t {
                            /** Direction of traffic */
                            policy_dir_t dir;
                            /** Source traffic selector */
                            traffic_selector_t *src_ts;
                            /** Destination traffic selector */
                            traffic_selector_t *dst_ts;
                            /** Optional mark */
                            mark_t mark; 
                            /** Network interface restricting policy */
                            char *interface;
                    };
                    // Data required to add/delete a policy to/from the kernel
                    struct kernel_ipsec_manage_policy_t {
                            /** Type of policy */
                            policy_type_t type;
                            /** Priority class */
                            policy_priority_t prio;
                            /** Manually-set priority (automatic if set to 0) */
                            uint32_t manual_prio;
                            /** Source address of the SA(s) tied to this policy */
                            host_t *src;
                            /** Destination address of the SA(s) tied to this policy */
                            host_t *dst;
                            /** Details about the SA(s) tied to this policy */
                            ipsec_sa_cfg_t *sa;
                    };
                    struct ipsec_sa_cfg_t {
                        /** mode of SA (tunnel, transport) */
                        ipsec_mode_t mode;
                        /** unique ID */
                        uint32_t reqid;
                        /** number of policies of the same kind (in/out/fwd) attached to SA */
                        uint32_t policy_count;
                        /** details about ESP/AH */
                        struct {
                            /** TRUE if this protocol is used */
                            bool use;
                            /** SPI for ESP/AH */
                            uint32_t spi;
                        } esp, ah;
                        /** details about IPComp */
                        struct {
                            /** the IPComp transform used */
                            uint16_t transform;
                            /** CPI for IPComp */
                            uint16_t cpi;
                        } ipcomp;
                    }; 
        5.5 charon进程
            charon进程运行启动成功后，启动16个子线程执行不同的job
            整个charon中的任务调度围绕着task和job两个核心概念进行
            图：file://imgs/charon进程流程图.png
    6 sa的抽象模型
        sa
            目的地址（dip）加 spi 唯一确定一个sa条目
            属性	    取值	        说明
            id		
            spi		                    协商过程带过来的
            mode	    transport/tunnel	
            protocol	esp/ah/ipcom	加密协议的方式
            sip		                    另一条隧道是sip和dip互换的，故两个sa
            dip		
            life		                生存时间
            enc_alg		
            enc_key		
            integrity_alg		        完整性验证
            integrity_key		
            nat		                    是否做nat
        policy
            属性	取值	        说明
            id		
            action	drop/pass/ipsec	命中此策略后的行为
            priority		        优先级
            dir	    in/out/fwd	    方向
            s_ts		            source traffic selector
            d_ts		            destination traffic selector
        traffic selector
            ts就是五元组，ip使用掩码掩起来的一个段。port也可以掩
            属性	        说明
            source ip	
            sip_prefixlen	
            dest ip	
            dip_prefixlen	
            sport	
            sport_mask	
            dport	
            dport_mask	
            protocol	
    7 问题
        7.1 policy与路由的关系
            在我的测试虚机环境里，删掉了策略路由之后，功能正常。目前还不清楚为什么。
            路由与policy之间的关系，以及路由和policy在内核包转发过程中的逻辑关系，
            都需要进一步的调研。
            
https://www.cnblogs.com/hugetong/p/11143369.html
strongwan sa分析(二)  rekey/reauth 机制分析