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
        IP报文头
            源地址src：本端发起IKE协商的IP地址，可能是接口IP地址，也可能是通过命令配置的IP地址。
            目的IP地址Dst：对端发起IKE协商的IP地址，由命令配置。
        UDP报文头
            IKE协议使用端口号500发起协商、响应协商。
            在通信双方都有固定IP地址时，这个端口在协商过程中保持不变。
            当通信双方之间有NAT设备时（NAT穿越场景），IKE协议会有特殊处理（后续揭秘）。
        ISAKMP报文头
            Initiator’s Cookie（SPI）和responder’s Cookie（SPI）：
                在IKEv1版本中为Cookie，在IKEv2版本中Cookie为IKE的SPI，唯一标识一个IKE SA。
            Next Payload：
                标识消息中下一个载荷的类型。
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
                载荷类型有很多种，不同载荷携带的“参数包”不同。
                参：file://YDT1897.pdf:第8页
            说明：
                1：IKE诞生以来，有过一次大的改进。老的IKE被称为IKEv1，改进后的IKE被称为IKEv2。
                   二者可以看做是父子关系，血脉相承，基本功能不变；但青胜于蓝，后者有了长足的进步。
                2：IKEv1版本中可以在交换类型字段查看协商模式
                   阶段1分为两种模式：主模式和野蛮模式，阶段2采用快速模式。
                   主模式是主流技术，野蛮模式是为解决现实问题而产生的。
                   IKEv2版本中定义了查看创建IKE SA和CHILD SA（对应IKEv1的IPSec SA）的IKE_SA_INIT、
                   IKE_AUTH（创建第一对CHILD SA）、CREATE_CHILD_SA（创建后续的CHILD SA）。      
2. 抓包分析        
    第一个IKE_SA_INIT
        可见该ISAKMP包的外层是个UDP协议，使用的端口号是500