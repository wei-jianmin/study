https://www.spoto.net/hcna/799.html
IKEv1 的阶段
    IKE分两个阶段运行，以确定IKE和IPSec的SA
    第一阶段让IKE对等体彼此验证对方并并确定会话秘钥
    这个阶段使用DH交换、cookie和ID交换创建一个ISAKMP SA，
    确定ISAKMP SA后，发起方和应答方之间的所有IKE通信都将通过
    加密和完整性校验检查从而进行保护，
    该阶段的目的是在对等体之间建立一条安全的通信信道，
    以便对阶段二的协商进行保护
    阶段二则使用ESP或者AH来保护IP数据流，以协商并确定IPSec SA
第一阶段（IKEv1-1）    
    管理连接都是在第一阶段完成的，该连接使用UDP_500端口进行通信，
    协商完成后产生一条双向的IKE SA。
    主要完成内容
        ①协商管理连接如何被保护
        ②使用DH来共享密钥信息从而保护管理连接
        ③验证对等体
    完成上述内容主要由以下两种模式：
        ①主模式（main_mode）
            该模式通过6个包，三次交互完成第一阶段协商
            思科设备默认使用该模式（因为该模式更安全，但效率更低）
        ②主动模式（aggressive_mode）
            该模式也被叫做野蛮模式
            该模式通过3个包，三次交互来完成第一阶段协商
            安全性比较低，协商的特性少于主模式，不提供对等体认证
            一般当使用远程拨号VPN+域共享秘钥认证场景时，才会使用到该模式。
    主模式数据包交互
        图：file://imgs/主动模式建立IKE SA.png
        1）IKE Phase 1 Messages Types 1-2
            发起方发送一个包含SA有效的数据载荷（SAi）
            主要协商保护管理连接的参数：
            加密算法、散列算法、DH组选择、验证方法、生存时间
            应答方基于SAi字段回复所挑选的协商结果
            数据包是明文交互的，使用UDP-500端口
            图：file://imgs/ikev1 主模式 第1、2个包.jpg
        2）IKE Phase 2 Messages Types 3-4
            第3、4个数据包交换 用于交换和秘钥相关的信息
            参数X、Y、Ni、Nr都是和DH算法产生秘钥的必要元素
            第3、4次交换后产生一条双向的IKE安全关联
            数据包是明文交互，UDP_500端口
            图：file://imgs/ikev1 主模式 第3、4个包.jpg
        3）IKE Phase 1 Messages Types 5-6
            主要用于认证对等体
            从第5个数据包开始，数据将执行加密和完整性校验（用第1、2个包协商的方式进行）
            如果认证通过，则进行第二阶段的协商
            使用第3、4个数据包产生的双向安全关联进行通信，UDP_500。
            图：file://imgs/ikev1 主模式 第5、6个包.jpg
        小结：
            步骤1：协商都使用哪些算法（明文）
            步骤2：进程DH密钥交换（明文）
            步骤3：完成身份互验，创建IKE SA（密文）
            注：步骤3的创建IKE SA，指的应该是操纵xfrm创建SA内核数据结构
第二阶段（IKEv1-2）
    只有一个快速模式
    快速模式的主要作用
        ①协商安全参数来保护数据连接
        ②周期性的对数据连接更新密钥信息
    第二阶段关注内容
        ①哪些感兴趣流需要被保护（SP策略）
        ②使用什么封装协议来加密流量（AH/ESP）
        ③基于什么算法来保护数据流量（例如使用什么样的HMAC）
        ④使用什么工作模式（传输模式还是隧道模式）
        疑问与理解：
            SP策略、AH/ESP选择、工作模式等，为什么不放在第一阶段的第一步完成？
            猜测这可能就是IKEv1的设计缺陷，IKEv2对此进行了改进
            也有可能是SP策略、AH/ESP选择、工作模式等，每对通信双方都不是完全一样的
            如可能 server-client1 选用传输模式进行通信，server-client2 选用隧道模式进行通信
            所以这应该属于 IPSEC SA 的内容，而不属于 IKE SA 的内容
    该模式定义通过3个数据包，三次交互来拿完成阶段二的协商
    阶段二所有的协商流量均使用UDP_500端口，由第一阶段的IKE安全关联保护
    阶段二协商完成后，产生两条单向的IPSec安全关联
        一条用于本设备发送加密数据（加密作用）
        一条用于本设备接收加密数据（解密作用）
    快速模式数据包交互
        1）IKE Phase 1 Messages Types 1-2 协商数据传输的保护提案（策略）
            协商用于数据传输的策略
            数值Ni2和Nr2用于生成新的秘钥
            数据是密文交互，UPD_500，使用IKE安全关联
            图：file://imgs/ikev1 快速模式 第1、2个包.jpg
            疑问与理解：
                为什么不直接使用阶段一步骤三协商好的密钥？
                因为只会有一个ike sa，却会有多个ipsec sa，
                ipsec sa各自使用不同的密钥，保证安全
                为什么会有多个ipsec sa？
                允许建立多个ipsec sa，可以对命中不同策略的浏览进行不同的封装
                如何触发创建新的 ipsec sa？
        2）IKE Phase 1 Messages Types 3
            确认隧道建立后，后续即可开始传输实际流量
            协商成功后建立隧道
            产生两条单向的IPSec安全关联用于保护通信流量
            数据包的交互是密文，在IPSec安全关联里面
            图：file://imgs/ikev1 快速模式 第3个包.jpg
            
--------------------------------------------------------------------------------------
https://forum.huawei.com/enterprise/zh/thread-291879.html
防火墙技术连载 VPN篇 IPSec携手IKE，珠联璧合显神威

IKEv2协商IPSec SA的过程跟IKEv1有很大差别：
    1. 初始交换4条消息同时搞定IKE SA和IPSec SA。
        初始交换包括IKE安全联盟初始交换（IKE_SA_INIT交换）和IKE认证交换（IKE_AUTH交换）
        图：file://imgs/IKE V2 -- IKE 联盟初始化交换.png
        第一个消息对（IKE_SA_INIT）：（把ikev1的步骤一、二：协商算法，密钥交换合并为一步了）
            负责IKE安全联盟参数的协商，包括IKE Proposal，临时随机数（nonce）和DH值
            图：file://imgs/IKE_SA_INIT抓包_1.png
            图：file://imgs/IKE_SA_INIT抓包_2.png : SA载荷,主要用来协商IKE Proposal >
            图：file://imgs/IKE_SA_INIT抓包_3.png : KE（Key Exchange）载荷和Nonce载荷主要用来交换密钥材料
            IKEv2通过IKE_SA_INIT交换后最终也生成三类密钥：
            SK_e：用于加密第二个消息对。
            SK_a：用于第二个消息对的完整性验证。
            SK_d：用于为Child SA（IPSec SA）衍生出加密材料。
        第二个消息对（IKE_AUTH）（把ikev1第一阶段的第三步身份认证和第二阶段合成一步了）
            负责身份认证，并创建第一个Child SA（一对IPSec SA）
            目前三种身份认证技术比较常用：
                预共享密钥方式（pre-share）：设备的身份信息为IP地址或名称。
                数字证书方式：设备的身份信息为证书和通过证书私钥加密的部分消息Hash值（签名）。
                EAP方式：采用EAP认证的交换过程属于扩展交换的内容，将在后面讲解。
            以上身份信息都通过SKEYID_e加密
            创建Child SA时，当然也要协商IPSec安全提议、被保护的数据流。
            IKEv2通过TS载荷（TSi和TSr）来协商两端设备的ACL规则，
            最终结果是取双方ACL规则的交集（这点跟IKEv1不同，IKEv1没有TS载荷不协商ACL规则）。
            当一个IKE SA需要创建多对IPSec SA时，例如两个IPSec对等体之间有多条数据流的时候，
            需要使用创建子SA交换来协商后续的IPSec SA。
    2. 子SA交换2条消息建立一对IPSec SA。
        子SA交换必须在IKE初始交换完成之后才能进行，
        交换的发起者可以是IKE初始交换的发起者，也可以是IKE初始交换的响应者
        这2条消息由IKE初始交换协商的密钥进行保护。
        IKEv2也支持PFS功能，创建子SA交换阶段可以重新进行一次DH交换，生成新的IPSec SA密钥。
        
IKEv1和IKEv2大PK
    ----------------------------------------------------------------------------------------------------------------
    功能项              IKEv1                                         IKEv2
    ----------------------------------------------------------------------------------------------------------------
    IPSec SA建立过程    分两个阶段，阶段1分两种模式：                 不分阶段，最少4条消息即可建立IPSec SA。
                        主模式和野蛮模式，阶段2为快速模式。
                        主模式+快速模式需要9条信息建立IPSec SA。
                        野蛮模式+快速模式需要6条信息建立IPSec SA。
    ----------------------------------------------------------------------------------------------------------------
    ISAKMP              二者支持的载荷类型不同
    ----------------------------------------------------------------------------------------------------------------
    认证方法            预共享密钥/数字证书/数字信封（较少使用）      预共享密钥/数字证书/EAP/数字信封（较少使用）
    ----------------------------------------------------------------------------------------------------------------
    IKE SA完整性算法    不支持                                        支持
    ----------------------------------------------------------------------------------------------------------------
    PFS                 支持                                          支持
    ----------------------------------------------------------------------------------------------------------------
    远程接入            通过L2TP over IPSec来实现                     支持  
    ----------------------------------------------------------------------------------------------------------------            