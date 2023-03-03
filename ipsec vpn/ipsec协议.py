参：https://info.support.huawei.com/info-finder/encyclopedia/zh/IPsec.html
什么是IPSec
    IPsec（Internet Protocol Security）是为IP网络提供安全性的协议和服务的集合
    它是VPN（Virtual Private Network，虚拟专用网）中常用的一种技术
    由于IP报文本身没有集成任何安全特性，IP数据包在公用网络如Internet中传输
    可能会面临被伪造、窃取或篡改的风险。
    通信双方通过IPsec建立一条IPsec隧道，IP数据包通过IPsec隧道进行加密传输，
    有效保证了数据在不安全的网络环境如Internet中传输的安全性
什么是IPsec VPN
    VPN（Virtual Private Network，虚拟专用网）是一种在公用网络上建立专用网络的技术
    它之所以称之为虚拟网，主要是因为VPN的两个节点之间并没有像传统专用网那样使用端到端的物理链路，
    而是架构在公用网络如Internet之上的"逻辑网络"，用户数据通过逻辑链路传输
    按照VPN协议分，常见的VPN种类有：IPsec、SSL、GRE、PPTP和L2TP等,
    其中IPsec是通用性较强的一种VPN技术，适用于多种网络互访的场景。
    IPsec VPN是指采用IPsec实现远程接入的一种VPN技术
    通过在公网上为两个或多个私有网络之间建立IPsec隧道，并通过加密和验证算法保证VPN连接的安全
    参：file://imgs/ipsec vpn结构图.png
    IPsec VPN保护的是点对点之间的通信，通过IPsec VPN可以在主机和主机之间、
    主机和网络安全网关之间或网络安全网关（如路由器、防火墙）之间建立安全的隧道连接。
    其协议主要工作在IP层，在IP层对数据包进行加密和验证。
    相对于其他VPN技术，IPsec VPN安全性更高，数据在IPsec隧道中都是加密传输，
    但相应的IPsec VPN在配置和组网部署上更复杂。
IPsec是如何工作的
    IPsec的工作原理大致可以分为4个阶段：
    识别“感兴趣流”
        网络设备接收到报文后，通常会将报文的五元组等信息
        和IPsec策略进行匹配来判断报文是否要通过IPsec隧道传输，
        需要通过IPsec隧道传输的流量通常被称为“感兴趣流”。
        注：五元组：本地ip、本地端口、对方ip、对方端口、协议
        实现方式
            ACL
                简介：
                    访问控制列表ACL（Access Control List）是由一条或多条规则组成的集合
                    所谓规则，是指描述报文匹配条件的判断语句，
                    这些条件可以是报文的源地址、目的地址、端口号等。
                    ACL本质上是一种报文过滤器，规则是过滤器的滤芯
                    规则是过滤器的滤芯。设备基于这些规则进行报文匹配，可以过滤出特定的报文，
                    并根据应用ACL的业务模块的处理策略来允许或阻止该报文通过。
                工作原理：
                    ACL是路由器的功能，ACL可配置多条规则，如果检查到数据包命中某条规则，
                    就按该规则处理该数据包，如果所有规则都不能命中，则最终丢弃该数据包
                    通过ACL，路由器可以控制哪个网口的数据能发给哪个网口？
                ACL命令语法：
                    file://imgs/ACL语法格式.png
                当使用当采用ACL的方式来定义“感兴趣流”时，
                建立的IPsec 隧道是由高级ACL来指定需要保护的数据流范围，
                并从中过滤出需要进行IPsec隧道的报文。
                ACL规则允许的报文(permit)将被保护；ACL规则拒绝的报文(deny)将不会被保护。
            虚拟隧道接口
                在两端的IPsec设备创建一个虚拟的隧道接口Tunnel, 
                然后通过配置以该Tunnel接口为出接口的静态路由，
                以此来将到达某一个子网的数据流量通过IPSec隧道进行转发。
                因为Tunnel接口为点对点类型的接口，是运行PPP链路层协议的，
                因此以该接口为出接口的静态路由是可以不指定下一跳IP地址的。
                ?IPsec虚拟隧道接口是一种三层逻辑接口，
                采用这种方式时，所有路由到IPsec虚拟隧道接口上的报文都将进行IPSec保护，
                而不再对数据流类型进行细分。
                用户数据到达IPSec设备(如路由器)，需要被IPSec保护的报文(==感兴趣流==)
                会被转发到IPSec虚拟隧道接口上进行封装和加密
                加密具体流程：
                    1. Router将从入接口上收到的明文IP报文后发送到转发模块进行处理
                    2. 转发模块依据路由表查询结果进行转发，如果为相应的感兴趣流，
                       会被引到IPSec虚拟隧道接口上进行AH或ESP封装;
                    3. IPSec虚拟隧道接口完成对明文的封装处理后，
                       根据建立的IPSec SA安全策略再将封装后的报文进行加密，
                       然后再将加密后的报文交由转发模块进行处理
                    4. 转发模块通过第二次转发查询后，
                       将已经封装完毕的加密IPSec报文通过相应的物理接口发送出去，
                       最终密文到达对端的IPSec设备的虚拟隧道接口上。
                解密具体流程：
                    1. Router将从入接口上收到的加密的IP报文发送到转发模块进行处理
                    2. 转发模块识别到此密文的目的IP地址为本设备的隧道接口IP地址，
                       且IP报文协议号为ESP、AH、UDP时，
                       会将此报文发送到相应的虚拟隧道接口上进行解密和解封装处理;
                    3. IPSec虚拟隧道接口完成对密文的解封装处理后，
                       再将解封装后的报文交由转发模块进行处理
                    4. 转发模块通过第二次转发查询后，将IP明文通过相应的物理接口发送出去，
                       最终密文到达相应的主机上
    安全协商（Security Association，以下简称SA）
        SA是通信双方对某些协商要素的约定，比如双方使用的安全协议、数据传输采用的封装模式、
        协议采用的加密和验证算法、用于数据传输的密钥等，
        通信双方之间只有建立了SA，才能进行安全的数据传输。
        识别出感兴趣流后，本端网络设备会向对端网络设备发起SA协商。
        在这一阶段，通信双方之间通过IKE协议先协商建立IKE SA（用于身份验证和密钥信息交换），
        然后在IKE SA的基础上协商建立IPsec SA（用于数据安全传输）。
    数据传输
        IPsec SA建立成功后，双方就可以通过IPsec隧道传输数据了。
        IPsec为了保证数据传输的安全性，在这一阶段需要通过AH或ESP协议对数据进行加密和验证。
        加密机制保证了数据的机密性，防止数据在传输过程中被窃取；
        验证机制保证了数据的真实可靠，防止数据在传输过程中被仿冒和篡改。
        如图所示，IPsec发送方会使用加密算法和加密密钥对报文进行加密，即将原始数据“乔装打扮”封装起来。
        然后发送方和接收方分别通过相同的验证算法和验证密钥对加密后的报文进行处理得到完整性校验值ICV。
        如果两端计算的ICV相同则表示该报文在传输过程中没有被篡改，接收方对验证通过的报文进行解密处理；
        如果ICV不相同则直接丢弃报文。
        图：file://imgs/ipsec加密验证过程.png
    隧道拆除
        通常情况下，通信双方之间的会话老化（连接断开）即代表通信双方数据交换已经完成，
        因此为了节省系统资源，通信双方之间的隧道在空闲时间达到一定值后会自动删除
IPsec的3个重要协议- IKE/AH/ESP
    IKE（Internet Key Exchange，因特网密钥交换）
        IKE协议是一种基于UDP的应用层协议，它主要用于SA协商和密钥管理。
        IKE协议分IKEv1和IKEv2两个版本，IKEv2与IKEv1相比，修复了多处公认的密码学方面的安全漏洞，
        提高了安全性能，同时简化了SA的协商过程，提高了协商效率。
        IKE协议属于一种混合型协议，它综合了ISAKMP（Internet Security Association and Key Management Protocol）、
        Oakley协议和SKEME协议这三个协议。
        其中，ISAKMP定义了IKE SA的建立过程，Oakley和SKEME协议的核心是DH（Diffie-Hellman）算法，
        主要用于在Internet上安全地分发密钥、验证身份，以保证数据传输的安全性。
        IKE SA和IPSec SA需要的加密密钥和验证密钥都是通过DH算法生成的，它还支持密钥动态刷新。
    AH（Authentication Header，认证头）
        AH协议用来对IP报文进行数据源认证和完整性校验，即用来保证传输的IP报文的来源可信和数据不被篡改，
        但它并不提供加密功能。AH协议在每个数据包的标准IP报文头后面添加一个AH报文头，
        AH协议对报文的完整性校验的范围是整个IP报文。
    ESP（Encapsulating Security Payload，封装安全载荷）
        ESP协议除了对IP报文进行数据源认证和完整性校验以外，还能对数据进行加密。
        ESP协议在每一个数据包的标准IP报头后方添加一个ESP报文头，并在数据包后方追加一个ESP尾
        （ESP Trailer和ESP Auth data）。
        ESP协议在传输模式下的数据完整性校验范围不包括IP头，因此它不能保证IP报文头不被篡改。
    AH和ESP可以单独使用，也可以同时使用。AH和ESP同时使用时，报文会先进行ESP封装，再进行AH封装；
    IPsec解封装时，先进行AH解封装，再进行ESP解封装。
IPsec使用的端口
    IPsec中IKE协议采用UDP 500端口发起和响应协商，因此为了使IKE协商报文顺利通过网关设备，
    通常要在网关设备上配置安全策略放开UDP 500端口。
    另外，在IPsec NAT穿越场景下，还需要放开UDP 4500端口。
    而AH和ESP属于网络层协议，不涉及端口。
    为了使IPsec隧道能正常建立，通常还要在网关设备上配置安全策略放开AH（IP协议号是51）
    和ESP（IP协议号是50）服务。
IPsec VPN和SSL VPN对比
    IPsec和SSL是部署VPN时最常用的两种技术，它们都有加密和验证机制保证用户远程接入的安全性。
    从以下几个方面对IPsec VPN和SSL VPN进行对比：
    OSI参考模型工作层级
        OSI定义了网络互连的七层框架：物理层、数据链路层、网络层、传输层、会话层、表示层、应用层。
        IPsec工作在网络层，它直接运行在IP（Internet Protocol，互联网协议）之上。
        而SSL工作在应用层，是一种应用层协议，它加密的是HTTP流量，而不是直接加密IP数据包。
    配置部署
        IPsec VPN通常适用于Site to Site（站点到站点）的组网，
        要求站点分别部署VPN网关和远程用户安装专用的VPN客户端，因此配置部署复杂度和维护成本都比较高。
        但SSL VPN通常适用于Client to Site（客户端到站点）的组网，
        只要求远程用户使用支持SSL的标准浏览器安装指定插件即可进行访问，
        通过数据中心部署VPN网关进行集中管理和维护，因此配置部署更简单，维护成本相对较低
    安全性
        IPSec工作在网络层，对站点间传输的所有数据进行保护。
        IPSec VPN要求远程用户安装专用的VPN客户端或在站点部署VPN网关设备，
        用户访问会受到客户端或网关在用户认证规则、安全策略规则或内容安全过滤方面的检查，因此安全性更高。
        而SSL VPN不要求安装专用客户端或接入站点部署网关设备，更容易受到安全威胁的影响。
    