1. 环境准备
    搭建：
        https://docs.strongswan.org/docs/5.9/config/quickstart.html
        采用端到端的连接模式，sun:192.168.3.99  moon:192.168.3.108
    证书生成：
        https://docs.strongswan.org/docs/5.9/pki/pkiQuickstart.html
        file://使用strongswan的pki工具生成rsa证书.txt
        注1：生成的ed25519证书，swanctl加载私钥报错，改为生成rsa证书
        注2：证书的放置路径一定要正确
             charon在启动时会给出一些加载证书路径提示，如：
             00[DMN] Starting IKE charon daemon 
             00[LIB] openssl FIPS mode(2) - enabled 
             00[CFG] loading ca certificates from '/etc/strongswan/ipsec.d/cacerts'
             00[CFG] loading aa certificates from '/etc/strongswan/ipsec.d/aacerts'
             00[CFG] loading ocsp signer certificates from '/etc/strongswan/ipsec.d/ocspcerts'
             00[CFG] loading attribute certificates from '/etc/strongswan/ipsec.d/acerts'
             则需要将产生的证书放置在如下目录：
             /etc/strongswan/swanctl/x509ca/strongswanCert.pem
             /etc/strongswan/swanctl/x509/sunCert.pem
             /etc/strongswan/swanctl/private/sunKey.pem
     加载证书和连接配置：
        swanctl --help
        swanctl --load-creds  //load certificates and private keys into the charon
        swanctl --load-conns  //loads the connections defined in swanctl.conf    
        执行以上命令，charon会输出如下信息：
            12[CFG] loaded certificate 'C=CH, O=strongswan, CN=sun.strongswan.org'
            06[CFG] loaded certificate 'C=CH, O=strongSwan, CN=strongSwan Root CA'
            15[CFG] loaded RSA private key
            12[CFG]   id not specified, defaulting to cert subject 'C=CH, O=strongswan, CN=sun.strongswan.org'
            12[CFG] added vici connection: host-host
            12[CFG] installing 'host-host'
            //前面的12、06，表明是那个线程输出的信息， [CFG]表明这是配置类日志
    wireshark抓包
        在不启动charon时，3.99可以正常ping 3.108
        3.108 启动charon，未执行swanctl相关命令前，3.99可以正常ping通3.108
        3.108 启动charon，并执行swanctl相关命令后，3.99无法ping通3.108
        3.99 启动charon，并执行swanctl相关命令后，3.99可以ping通3.108
    注：以上需要防火墙事先放开udp 500/[4500]端口，
        如果无法ping通，建议优先找防火墙方面的原因，如添加放开ah/esp/icmp/tcp/udp等协议
        另外，需关注抓包的spi和ip xfrm status列出的spi是否一致，如果不一致，说明缓存的SA不对，重启解决
2. ISAKMP报文封装
        参：https://blog.csdn.net/bytxl/article/details/36016141
        参：file://YDT1897.pdf:第26页
        图：file://../imgs/ISAKMP报文封装.png
        RFC2048定义了名为ISAKMP的安全框架
            RFC中文：https://blog.csdn.net/xqk709008281/article/details/78681781
        IP报文头
            源地址src：本端发起IKE协商的IP地址，可能是接口IP地址，也可能是通过命令配置的IP地址。
            目的IP地址Dst：对端发起IKE协商的IP地址，由命令配置。
        UDP报文头
            IKE协议使用端口号500发起协商、响应协商。
            在通信双方都有固定IP地址时，这个端口在协商过程中保持不变。
            当通信双方之间有NAT设备时（NAT穿越场景），IKE协议会有特殊处理（后续揭秘）。
        ISAKMP报文头
             0             8       12      16              24              32
             0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            !                            发起者                             !
            !                      Initiator Cookie                       !
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            !                            应答                               !
            !                      Responder Cookie                         !
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            !   下一个载荷  ! MjVer ! MnVer !    交换类型   !     标志      !
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            !                            消息  ID                           !
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            !                             长度                              !
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            Initiator’s Cookie（SPI）和responder’s Cookie（SPI）：
                在IKEv1版本中为Cookie，在IKEv2版本中Cookie为IKE的SPI，唯一标识一个IKE SA。
            Next Payload：
                标识消息中下一个载荷（携带的第一个载荷）的类型。
                一个ISAKMP报文中可能装载多个载荷，该字段提供载荷之间的“链接”能力。
                若当前载荷是消息中最后一个载荷，则该字段为0。
            Version：
                IKE版本号1/2。
            Exchange Type：
                IKE定义的交互类型。交换类型定义了ISAKMP消息遵循的交换顺序。
                        交换类型                值
                         NONE                    0
                         Base                    1
                         Identity Protection     2
                         Authentication Only     3
                         Aggressive              4
                         Informational           5
                         ISAKMP Future Use       6 - 31
                         DOI Specific Use        32 - 239   //34:IKE_SA_INIT
                         Private Use             240 - 255
            Flags：
                为 ISAKMP 交换设置的各种选项
            Message ID：
                唯一的信息标识符，用来识别第2阶段的协议状态。
            Message Length：
                全部信息（头＋有效载荷）长（八位）。
            Type Payload / ISAKMP Payload：
                载荷类型，ISAKMP报文携带的用于协商IKE SA和IPSec SA的“参数包”。
                载荷类型有很多种，不同载荷携带的“参数包”不同，包括：
                    厂商ID(V)、认证(AUTH)、证书(CERT)、
                    证书请求(CERTREQ)、可扩展认证协议(EAP)、
                    证书请求(CERTREQ)、可扩展认证协议(EAP)、
                    配置(CP)、删除(D)、加密(E)、通知(N)、
                    IKE头(HDR)、密钥交换(KE)、安全联盟(SA)、
                    发起者标识(IDi)、响应者标识(IDr)、
                    发起者临时随机数(Ni)、响应者临时随机数(Nr)、
                    发起者流量选择器(TSi)、响应者浏览选择器(TSr)、
                参：file://YDT1897.pdf:第8页
            说明：
                1：IKE诞生以来，有过一次大的改进。老的IKE被称为IKEv1，改进后的IKE被称为IKEv2。
                   二者可以看做是父子关系，血脉相承，基本功能不变；但青胜于蓝，后者有了长足的进步。
                2：IKEv1版本中可以在交换类型字段查看协商模式
                   阶段1分为两种模式：主模式和野蛮模式，阶段2采用快速模式。
                   主模式是主流技术，野蛮模式是为解决现实问题而产生的。
                   IKEv2版本中定义了查看创建IKE SA和CHILD SA（对应IKEv1的IPSec SA）的IKE_SA_INIT、
                   IKE_AUTH（创建第一对CHILD SA）、CREATE_CHILD_SA（创建后续的CHILD SA）。      
3. isakmp 学习
    https://blog.csdn.net/bytxl/article/details/36016141
    RFC2048定义了名为ISAKMP的安全框架 
    ISAKMP它的主要作用就是协商和管理sa，以及密钥
    为了实现这一功能，ISAKMP定义了一系列的消息和过程
    但是ISAKMP只是一个框架而已，它并不规定采用什么样的算法
    现在的ISAKMP框架已经可以很好的处理DOS、连接劫持和中间人攻击。
    从宏观上来看，ISAKMP主要做了三件事情：
    1.  SA协商
        SA协商的目的是为了在通信双方间协商出一组双方都认可的安全参数。
        比如两端采用相同的加密算法和完整性算法
        一般说来，我们需要协商加密算法、认证机制，以及密钥建立算法
    2.  密钥交换
        密钥交换的目的是为已经协商好的算法生成必要的密钥信息
        在ISAKMP体系中，无论是数据加密算法还是认证算法，都需要一个双方都知道的密钥。
        如何才能够通过不安全的互联网环境建立起一个安全的密钥呢？
        一般有两种方式。第一种叫做密钥传输，第二种叫做密钥生成。
        顾名思义，密钥传输就是直接把密钥发给对方。
        一个典型的例子是，首先在客户端随机生成一个密钥，然后使用服务端的公开密钥进行加密。
        由于只有服务端知道如何对加密数据解密，所以保证了密钥的安全性。
        但是，如果服务端的私钥被窃取了，那么通信就变得不安全。
        密钥生成通常使用Diffie-Hellman算法。
        所以，现在主流的密钥交换协议，比如IPSec，都是基于DH算法来实现的。
    3.  认证
        认证的目的是鉴别对方的身份，保证自己不是在跟一个伪造的对象通信
        所有的认证协议都使用一个通用的模型：
        基于共享密钥的认证通常使用质询-回应协议：
            A 首先选择一个随机数 R 发给 B。
            B 使用共享密钥对随机数做一系列变换，然后送回给 A。
            A 在本地对随机数做相同的变化，然后同 B 发来的结果进行比较，
            如果相同，说明对方是 B。
            由于任何第三方不可能获取共享密钥，因而无法生成变换结果来欺骗 A。
            但是，这种认证有一种致命的缺陷：无法防御“反射攻击”
                C 可以利用一种被称为“反射攻击”的技术使得协议失败：
                C 截获了 A 发给 B 的质询消息，然后重新开启一个会话，声称自己是 B
                并给 A 发送随机数 R，要求 Al 证明自己的身份。
                于是 A 对 R 进行变换，把结果发给 C，
                然后 C 用这个结果来回应 A 最初的质询，于是成功的欺骗了 A。
            由此可见，设计一个正确的认证协议要比表面上复杂的多。
            下面的4条一般性原则通常会有所帮助：
                1. 让发起者首先证明自己是谁，然后轮到应答方。
                2. 让发起方和应答方使用不同的密钥做证明。不过，这意味着要有两个共享密钥。
                3. 让发起方和应答方从不同的质询集合选择随机数。
                   比如，发起方必须使用偶数，应答方必须使用奇数。
                4. 使协议可以抵抗这种牵扯到第二个并行会话的攻击。
            以上原则只要有一条违反了，则协议通常会被攻破。
            一个可行的认证协议是使用HMAC，过程如下：
                1. A 随机选择一个 RA ，用明文发送给 B。
                2. B 随机选择一个 RB， 并连同计算出的 HMAC(RA,RB,A,B,Key-AB) 
                   一起发回给 A 作为质询。要求 A 用这个随机数证明自己。
                   HMAC中的 A/B，是双方的身份标识信息，Key-AB表共享的密钥
                   A 收到后，与自己计算出来的（需要A知道B的身份标识信息）做比较
                3. A 回应 HMAC(RA,RB,Key-AB)。
                   告知 B 自己成功获得了 B 的回复信息，还能防止这个回复信息被别人伪造
                显然，C 无法伪造 B 的应答，因为它不知道 Key-AB。
        ISAKMP对于它的认证和密钥交换模块有一些基本的安全需求，
        以防止DOS、重放/反射、中间人攻击和连接劫持攻击。
        DH算法最大的一个缺陷在于，它无法防止中间人攻击。
        中间人攻击之所以能够成功的关键在于，通信双方没有对对方进行认证，从而无法确定对方的真实身份。
        所以，防范中间人攻击就必须进行双向认证。
        在ISAKMP体系中，通信双方首先交换DH值，最后进行身份认证。一旦有中间人，认证必然失败。 
        以数字签名认证为例，双方使用公钥签名(DSS或RSA)来验证对等体。
        公钥通常是通过证书获得的。
        在第三次和第四次消息交换中，发起方和应答放请求对方提供证书，
        同时向对方发送临时值(Ni和Nr)以及DH公开值。
        第五和第六次消息交换中，相互交换了证书。虽然证书是可选的，但是这已经成为一种标准实现。
        创建数字签名的方法如下：
        SIG_i= PrivateKey_i (Hash_i)
        SIG_r= PrivateKey_r (Hash_r)
        签名是不可伪造的，所以中间人不可能替换Hash_i和Hash_r，因为替换之后，它无法产生正确的签名 
    isakmp定义了信息包的格式来建立、协商、修改和删除安全连接（SA）
    ISAKMP 与密钥交换协议（ IKE ）的不同处是：
    把安全连接管理的详细资料从密钥交换的详细资料中彻底的分离出来？
    ISAKMP 被用来支持在所有网络堆栈（如 IPSEC、TLS、TLSP、OSPF 等等）的层上的安全协议的 SA 的谈判
    DOI（解释域）
        通俗来说，就是多个协议共同借助（共享）ISAKMP，完成协商sa
        共享 DOI 的安全协议从公共的命名空间选择安全协议和加密转换方式，并共享密钥交换协议标识
        同时它们还共享一个特定 DOI 的有效载荷数据目录解释，包括安全连接和有效载荷认证。
4. 抓包分析        
    第一个IKE_SA_INIT
        可见该ISAKMP包的外层是个UDP协议，使用的端口号是500