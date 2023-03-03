https://blog.csdn.net/w17691058648x/article/details/100087113

隧道技术：是指在隧道的两端通过封装以及解封装技术在公网上建立一条数据通道，使用这条通道对数据报文进行传输

隧道技术比较：
---------------------------------------------------------------------------------------------------------------------┐
隧道协议    保护范围          使用场景                用户身份认证                        加密和验证                 │
---------------------------------------------------------------------------------------------------------------------┤
GRE         IP层及以上数据    Intranet VPN            不支持                              支持简单的关键字验证、校验 │
---------------------------------------------------------------------------------------------------------------------┤
L2TP        IP层及以上数据    Access VPN/ExtranetVPN  支持基于PPP的CHAP、PAP、EAP认证     不支持                     │
---------------------------------------------------------------------------------------------------------------------┤
IP sec      IP层及以上数据    Intranet VPN/           支持与共享密钥或证书认证、          支持                       │
                              Access VPN/Extranet VPN 支持IKEv2的EAP认证                                             │
---------------------------------------------------------------------------------------------------------------------┤
Sangfor VPN IP层及以上数据    Intranet VPN/           支持多种身份认证                    支持                       │
                              Extranet VPN                                                                           │
---------------------------------------------------------------------------------------------------------------------┤
SSL VPN     应用层特定数据    Access VPN              支持多种身份认证                    支持                       │
---------------------------------------------------------------------------------------------------------------------┘

用IPsec保护一个IP包之前，必须先建立安全关联（SA）
IPSec的安全关联可以通过手工配置的方式建立。但是当网络中节点较多时，手工配置将非常困难，而且难以保证安全性。
这时就可以使用IKE（ Internet Key Exchange）自动进行安全关联建立与密钥交换的过程。 
Internet密钥交换（ IKE）就用于动态建立SA，代表IPSec对SA进行协商

IKE：自动进行安全关联建立与密钥交换的过程
用途：
IKE为IPsec协商生成密钥，供AH/ESP加解密和验证使用。
在IPSec通信双方之间， 动态地建立安全关联（ SA： SecurityAssociation），对SA进行管理和维护

IKE的工作过程
第一阶段：彼此间建立了一个已通过身份验证和安全保护的通道，此阶段的交换建立了一个ISAKMP安全联盟

--------------------------------------------------------------------------------------------------

http://www.unixwiz.net/techtips/iguide-ipsec.html

ipsec的设置很复杂，一个原因是：
    Psec提供的是机制，而不是策略：它不是定义这样那样的加密算法或某个身份验证功能，
    而是提供了一个框架，允许实现提供几乎任何双方都同意的东西。
    
ip数据包可携带的协议类型（部分）
    Protocol code	Protocol Description
    1	            ICMP — Internet Control Message Protocol
    2	            IGMP — Internet Group Management Protocol
    4	            IP within IP (a kind of encapsulation)
    6	            TCP — Transmission Control Protocol
    17	            UDP — User Datagram Protocol
    41	            IPv6 — next-generation TCP/IP
    47	            GRE — Generic Router Encapsulation (used by PPTP)
    50	            IPsec: ESP — Encapsulating Security Payload
    51	            IPsec: AH — Authentication Header

AH和ESP都有身份认证的功能，这是借助HMAC提供的（因此设置ipsec的时候，需要指定hamc要用的盐值）

ipsec部署在网关时，数据是怎样被处理传送的：
    图：file://imgs/IPSec-VPN组网.gif
    
使用ESP还是AH ？    
    由于 AH 在网络地址转换方面的局限性，在实践中并不常用（不支持NAT）
    
SA 和 SPI
    当 IPsec 数据报（AH 或 ESP）到达接口时，接口如何知道要使用哪组参数（键、算法和策略）？
    任何主机都可以进行许多正在进行的对话，每个对话都有一组不同的密钥和算法，并且必须能够指导这种处理。
    这由安全关联 （SA）指定，SA 是连接特定参数的集合，每个伙伴可以有一个或多个安全关联。
    当数据报到达时，将使用三条数据在安全关联数据库 （SADB） 中查找正确的 SA:
        合作伙伴 IP 地址 + IPsec 协议（ESP 或 AH） + 安全参数索引
    安全关联是单向的，因此双向连接（典型情况）至少需要两个
    SADB中保存了大量信息，我们只能触及其中的一些：
        AH：身份验证算法
        AH：身份验证机密
        ESP：加密算法
        ESP：加密密钥
        ESP：身份验证已启用是/否
        许多密钥交换参数
        路由限制
        IP 筛选策略
    
密钥管理    
    如果没有身份验证和加密的加密功能，IPsec将几乎毫无用处
    IKE 使用 ISAKMP（互联网安全协会密钥管理协议）作为框架，支持建立与两端兼容的安全协会。
    支持多种密钥交换协议本身，其中Oakley是使用最广泛的协议。
    我们将注意到 IPsec 密钥交换通常通过端口 500/udp 进行
    
===============================================================================================
    
https://apprize.best/linux/kernel/11.html 
IPsec已成为世界上大多数IP虚拟专用网络（VPN）技术的标准。这样意味着，也有基于不同技术的VPN，
例如安全套接字层（SSL）和pptp（通过GRE协议隧道进行PPP连接）   

我首先简要讨论 IPsec 中的 Internet 密钥交换 （IKE） 
用户空间守护程序和加密。这些主题通常不是内核网络堆栈的一部分，但与 IPsec 操作相关，
需要这些主题才能更好地了解内核 IPsec 子系统。
接下来，我将讨论 XFRM 框架，该框架是 IPsec 用户空间部分和 IPsec 内核组件之间的配置和监视接口，
并解释了 IPsec 数据包在 Tx 和 Rx 路径中的遍历。
在本章的最后，我用一小节介绍 IPsec 中的 NAT 遍历，这是一个重要而有趣的功能

IKE （互联网密钥交换）
    最流行的开源用户空间Linux IPsec解决方案是
    Openswan（和libreswan，从Openswan分叉出来）、strongSwan和racoon（ipsec-tools）。
    Racoon是Kame项目的一部分，该项目旨在为BSD的变体提供免费的IPv6和IPsec协议栈实现。
    Openswan 和 strongSwan 实现提供了一个 IKE 守护程序
    （Openswan 中的 pluto 和 strongSwan 中的 charon）
    它使用 UDP 端口 500（源和目标）来发送和接收 IKE 消息
    两者都使用XFRM Netlink接口与Linux内核的本机IPsec堆栈进行通信。
    strongSwan项目是RFC 5996“Internet Key Exchange Protocol Version 2（IKEv2）”的唯一完整的开源实现，
    而Openswan项目仅实现一个小的强制子集
    
    您可以在 Openswan 和 strongSwan 5.x 中使用 IKEv1 Aggressive Mode
    （对于 strongSwan，应显式配置它，在这种情况下，charon 守护程序的名称更改为 weakSwan）;
    但此选项被认为是不安全的
    
    IKEv2 协议不区分阶段 1 和阶段 2，而是将第一个CHILD_SA作为IKE_AUTH消息交换的一部分。
    CHILD_SA_CREATE消息交换仅用于建立其他CHILD_SAs或定期重新生成 IKE 和 IPsec SA 的密钥。
    
XFRM 框架
    该框架起源于USAGI项目，旨在提供生产有质量的IPv6和IPsec协议栈
    XFRM 基础设施独立于协议族，这意味着 IPv4 和 IPv6 都有一个通用部分，位于 net/xfrm 下。
    IPv4 和 IPv6 都有自己的 ESP、AH 和 IPCOMP 实现。
    例如，IPv4 ESP 模块是 net/ipv4/esp4.c，IPv6 ESP 模块是 net/ipv6/esp6.c。
    网络命名空间
        XFRM 框架支持网络命名空间，这是一种轻量级进程虚拟化形式，
        它使单个进程或一组进程能够拥有自己的网络堆栈
        每个网络命名空间（结构网的实例）都包含一个名为 xfrm 的成员，它是netns_xfrm结构的一个实例。
        struct netns_xfrm {
            struct hlist_head *state_bydst;
            struct hlist_head *state_bysrc;
            struct hlist_head *state_byspi;
            . . .
            unsigned int state_num;
            . . .
            struct work_struct state_gc_work;
            . . .
            u32 sysctl_aevent_etime;
            u32 sysctl_aevent_rseqth;
            int sysctl_larval_drop;
            u32 sysctl_acq_expires;
            };
    XFRM 初始化
        在 IPv4 中，XFRM 初始化是通过从 net/ipv4/route.c 中的 
        ip_rt_init（） 方法调用 xfrm_init（） 方法和 xfrm4_init（） 方法来完成的
        用户空间和内核之间的通信是通过创建NETLINK_XFRM网络链接套接字并发送和接收网络链接消息来完成的
        netlink NETLINK_XFRM内核套接字是通过以下方法创建的：
        static int __net_init xfrm_user_net_init（struct net *net）
        {
            struct sock *nlsk;
            struct netlink_kernel_cfg cfg = {
                .groups = XFRMNLGRP_MAX，
                .input = xfrm_netlink_rcv，
                };
            nlsk = netlink_kernel_create（net， NETLINK_XFRM， &cfg）;
            ...
            return 0;
        }
        从用户空间发送的消息
        （如用于创建新安全策略的XFRM_MSG_NEWPOLICY或用于创建新安全关联的XFRM_MSG_NEWSA）
        由xfrm_netlink_rcv（）方法（net/xfrm/xfrm_user.c）处理，
        该方法又调用thexfrm_user_rcv_msg（）方法
        
        XFRM 策略和 XFRM 状态是 XFRM 框架的基本数据结构。
        （策略和状态的内核结构，可见本目录下的其他文件）
        xfrm_policy结构的重要成员：
            · refcnt: 
                The XFRM policy reference counter; initialized to 1 in the xfrm_policy_alloc( ) method, 
                incremented by the xfrm_pol_hold() method, and decremented by the xfrm_pol_put() method.
            · timer: 
                Per-policy timer; the timer callback is set to be xfrm_policy_timer() in the xfrm_policy_alloc() method. 
                The xfrm_policy_timer() method handles policy expiration: it is responsible for deleting a policy 
                when it is expired by calling thexfrm_policy_delete() method, 
                and sending an event (XFRM_MSG_POLEXPIRE) to all registered Key Managers 
                by calling the km_policy_expired() method.
            · lft: 
                The XFRM policy lifetime (xfrm_lifetime_cfg object).
                 Every XFRM policy has a lifetime, which is a time interval (expressed as a time or byte count).
                You can set XFRM policy lifetime values with the ip command and the limit parameter—for example:
                ip xfrm policy add src 172.16.2.0/24 dst 172.16.1.0/24 limit byte-soft 6000 ...
            · sets 
                the soft_byte_limit of the XFRM policy lifetime (lft) to be 6000; see man 8 ip xfrm.
                You can display the lifetime (lft) of an XFRM policy by inspecting the lifetime configuration entry 
                when running ip -stat xfrm policy show.
            · curlft: 
                The XFRM policy current lifetime, which reflects the current status of the policy in context of lifetime. 
                The curlft is an xfrm_lifetime_cur object. It consists of four members
                 (all of them are fields of 64 bits, unsigned):
            · bytes: 
                The number of bytes which were processed by the IPsec subsystem, 
                incremented in the Tx path by the xfrm_output_one() method and in the Rx path by the xfrm_input() method.
            · packets: 
                The number of packets that were processed by the IPsec subsystem, 
                incremented in the Tx path by the xfrm_output_one() method, 
                and in the Rx path by the xfrm_input() method.
            · add_time
                The timestamp of adding the policy, initialized when adding a policy, 
                in the xfrm_policy_insert() method and in the xfrm_sk_policy_insert() method.
            · use_time: 
                The timestamp of last access to the policy. The use_time timestamp is updated,
                 for example, in the xfrm_lookup() method or in the __xfrm_policy_check() method. 
                 Initialized to 0 when adding the XFRM policy, in thexfrm_policy_insert() method 
                 and in the xfrm_sk_policy_insert() method.
                image Note You can display the current lifetime (curlft) object of an XFRM policy 
                by inspecting the lifetime current entry when running ip -stat xfrm policy show.
            · polq: 
                A queue to hold packets that are sent while there are still no XFRM states associated with the policy. 
                As a default, such packets are discarded by calling the make_blackhole() method. 
                When setting the xfrm_larval_drop sysctl entry to 0 (/proc/sys/net/core/xfrm_larval_drop), 
                these packets are kept in a queue (polq.hold_queue) of SKBs; 
                up to 100 packets (XFRM_MAX_QUEUE_LEN) can be kept in this queue. 
                This is done by creating a dummy XFRM bundle, 
                by thexfrm_create_dummy_bundle() method (see more in the “XFRM lookup” section later in this chapter). 
                By default, the xfrm_larval_drop sysctl entry is set to 1 
                (see the __xfrm_sysctl_init() method in net/xfrm/xfrm_sysctl.c).
            · type: 
                Usually the type is XFRM_POLICY_TYPE_MAIN (0). 
                When the kernel has support for subpolicy (CONFIG_XFRM_SUB_POLICY is set), 
                two policies can be applied to the same packet, and you can use the XFRM_POLICY_TYPE_SUB (1) type. 
                Policy that lives a shorter time in kernel should be a subpolicy. 
                This feature is usually needed only for developers/debugging and for mobile IPv6, 
                because you might apply one policy for IPsec and one for mobile IPv6. 
                The IPsec policy is usually the main policy with a longer lifetime than the mobile IPv6 (sub) policy.
            · action: 
                Can have one of these two values:
            · XFRM_POLICY_ALLOW (0): 
                Permit the traffic.
            · XFRM_POLICY_BLOCK(1): 
                Disallow the traffic (for example, when using type=reject or type=drop in /etc/ipsec.conf).
            · xfrm_nr: 
                Number of templates associated with the policy—can be up to six templates (XFRM_MAX_DEPTH). 
                The xfrm_tmpl structure is an intermediate structure between the XFRM state and the XFRM policy. 
                It is initialized in the copy_templates()method, net/xfrm/xfrm_user.c.
            · family: 
                IPv4 or IPv6.
            · security: 
                A security context (xfrm_sec_ctx object) that allows the XFRM subsystem to restrict the sockets 
                that can send or receive packets via Security Associations (XFRM states). 
                For more details, see http://lwn.net/Articles/156604/.
            · xfrm_vec: An array of XFRM templates (xfrm_tmpl objects).
                The kernel stores the IPsec Security Policies in the Security Policy Database (SPD). 
                Management of the SPD is done by sending messages from a userspace socket. For example:
            · Adding 
                an XFRM policy (XFRM_MSG_NEWPOLICY) is handled by the xfrm_add_policy() method.
            · Deleting 
                an XFRM policy (XFRM_MSG_DELPOLICY) is handled by the xfrm_get_policy() method.
            · Displaying 
                the SPD (XFRM_MSG_GETPOLICY) is handled by the xfrm_dump_policy() method.
            · Flushing 
                the SPD (XFRM_MSG_FLUSHPOLICY) is handled by the xfrm_flush_policy() method.
        xfrm_state结构的重要成员：
            · refcnt: 
                A reference counter, incremented by the xfrm_state_hold() method and decremented 
                by the __xfrm_state_put() method or by the xfrm_state_put() method 
                (the latter also releases the XFRM state by calling the__xfrm_state_destroy() method 
                when the reference counter reaches 0).
            · id: 
                The id (xfrm_id object) consists of three fields, which uniquely define it: 
                destination address, spi, and security protocol (AH, ESP, or IPCOMP).
            · props: 
                The properties of the XFRM state. For example:
            · mode: 
                Can be one of five modes (for example, XFRM_MODE_TRANSPORT for transport mode 
                or XFRM_MODE_TUNNEL for tunnel mode; see include/uapi/linux/xfrm.h).
            · flag: 
                For example, XFRM_STATE_ICMP. These flags are available in include/uapi/linux/xfrm.h. 
                These flags can be set from userspace, 
                for example, with the ip command and the flag option: ip xfrm add state flag icmp ...
            · family: 
                IPv4 of IPv6.
            · saddr: 
                The source address of the XFRM state.
            · lft: 
                The XFRM state lifetime (xfrm_lifetime_cfg object).
            · stats: 
                An xfrm_stats object, representing XFRM state statistics. 
                You can display the XFRM state statistics by ip –stat xfrm show.
        内核将 IPsec 安全关联存储在安全关联数据库 （SAD） 中。
        xfrm_state对象存储在netns_xfrm（前面讨论的 XFRM 命名空间）的三个哈希表中：
        state_bydst、state_bysrc、state_byspi。
        这些表的键分别由 xfrm_dst_hash（）、xfrm_src_hash（） 和 xfrm_spi_hash（） 方法计算
        添加xfrm_state对象时，会将其插入到这三个哈希表中。
        如果 spi 的值为 0（值 0 通常不用于 spi — 我很快就会提到当它是 0 时），
        则 xfrm_state 对象不会添加到state_byspi哈希表中
        值为 0 的 spi 仅用于获取状态。
            内核向密钥管理器发送获取消息，
            如果流量与策略匹配，但状态尚未解析，则添加 spi 0 的临时获取状态。
            只要获取状态存在，内核就不会费心发送进一步的获取;
            如果状态得到解决，则此获取状态将替换为实际状态。
        SAD 中的查找可以通过以下方式完成：
            ·xfrm_state_lookup（） 方法：在state_byspi哈希表中。
            ·xfrm_state_lookup_byaddr（） 方法：在state_bysrc哈希表中。
            ·xfrm_state_find（） 方法：在state_bydst哈希表中。

ESP 实施 （IPv4）   
    在 RFC 4303 中指定的 ESP 协议;它支持加密和身份验证。
    虽然它还支持仅加密和仅身份验证模式，
    但它通常与加密和身份验证一起使用，因为它更安全。
    图：file://imgs/接收 IPsec 数据包（传输模式）流程图.jpg
    注意： 上图描述了一个 IPv4 ESP 数据包。
    对于 IPv4 AH 数据包，调用 ah_input（） 方法而不是 esp_input（ ） 方法;
    同样，对于 IPv4 IPCOMP 数据包，将调用 ipcomp_input（） 方法
    而不是 esp_input（ ） 方法
    图中xfrm_state_lookup（） 方法在 SAD 中执行查找。
    如果查找失败，则会丢弃数据包。
    如果出现查找命中，则调用相应 IPsec 协议的输入回调方法
    图：file://imgs/发送 IPsec 数据包（传输模式）流程图.jpg
    上图中的xfrm_lookup()方式是一种非常复杂的方法
    图：file://imgs/xfrm_lookup流程图.jpg
    
在 IPsec 中 NAT 遍历
    为了解决NAT转换问题，开发了 IPsec 的 NAT 遍历标准
    （或者，在 RFC 3948 中正式称为“IPsec ESP 数据包的 UDP 封装”）。
    UDP 封装可以应用于 IPv4 数据包以及 IPv6 数据包。
    NAT 遍历解决方案不仅限于 IPsec 流量;
    客户端到客户端网络应用程序通常需要这些技术，
    特别是对于对等和 Internet 协议语音 （VoIP） 应用程序。
    我应该在这里提到，strongSwan实现了IKEv2中介扩展服务
    （http://tools.ietf.org/html/draft-brunner-ikev2-mediation-00），
    它允许位于NAT路由器后面的两个VPN端点(使用了一种机制)建立直接的对等IPSec隧道。
    NAT 遍历如何工作？
        首先，请记住，NAT-T 是仅用于 ESP 流量而不适用于 AH 的良好解决方案。
        另一个限制是NAT-T不能与手动键控一起使用，而只能与IKEv1和IKEv2一起使用。
        这是因为 NAT-T 与交换 IKEv1/IKEv2 消息有关。
        首先，您必须告诉用户空间守护程序 （pluto） 您要使用 NAT 遍历功能，
        因为默认情况下不会激活该功能。
        您可以在 Openswan 中通过在 /etc/ipsec.conf 中的连接参数中添加 
        nat_traversal=yes 来执行此操作。
        不位于 NAT 后面的客户端不受添加此条目的影响。
        在 strongSwan 中，IKEv2 charon 守护程序始终支持 NAT 遍历，并且此功能无法停用。
        在 IKE（主模式）的第一阶段，检查两个对等方是否都支持 NAT-T。
        在 IKEv1 中，当对等体支持 NAT-T 时，
        其中一个 ISAKAMP 标头成员（供应商 ID）会告知它是否支持 NAT-T。
        在IKEv2中，NAT-T是标准的一部分，不必宣布。
        如果满足此条件，您可以通过发送 NAT-D 负载消息
        来检查两个 IPsec 对等体之间的路径中是否存在一个或多个 NAT 设备
        如果同时满足此条件，NAT-T 将通过在 IP 报头和 ESP 报头之间插入 UDP 报头
        来保护原始 IPsec 编码的数据包。
        UDP 标头中的源端口和目标端口均为 4500。
        此外，NAT-T 每 20 秒发送一次保持活动状态的消息，以便 NAT 保留其映射。
        保持活动状态的消息也在 UDP 端口 4500 上发送，
        并通过其内容和值（即一个字节，0xFF）进行识别。
        当此数据包到达 IPsec 对等体时，在通过 NAT 后，
        内核会剥离 UDP 标头并解密 ESP 有效负载。
        
        