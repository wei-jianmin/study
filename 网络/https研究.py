单向认证
    1. 客户端->服务端 : ClientHello
        这一步，客户端主要向服务器提供以下信息：
        1.支持的协议版本，比如TLS 1.0版
        2.一个客户端生成的随机数，稍后用于生成”对话密钥”
        3.支持的加密方法，比如RSA公钥加密
        4.支持的压缩方法
    2. 服务端->客户端 : SSL 版本、随机数、服务器公钥
    
    
抓包分析
    过滤方法：
        ping百度获取ip为110.242.68.4，
        过滤字符串 ip.addr==110.242.68.4 && tcp.port==3046
    1. 客户端->服务器 ：建立tcp连接 syn
    2. 服务器->客户端 ：建立tcp连接 syn,ack
    3. 客户端->服务器 ：建立tcp连接 ack
    4. 客户端->服务器 ：发送tls请求 client hello
        Content Type : Handshake
        Version : TLS 1.0
        Length : 512
        Handshake Protocol （握手协议）: Client Hello
            Handshake Type : Client Hello
            
TLS与SSL的差异
    TLS并不是一个新协议，它是SSL(准确的说是SSL v3)的强化版，在整个协议格式上，和SSL类似
    1. 版本号：
        TLS记录格式与SSL记录格式相同，但版本号的值不同，
        TLS的版本1.0使用的版本号为SSLv3.1。
    2. 报文鉴别码：
        SSLv3.0和TLS的MAC算法及MAC计算的范围不同。
        TLS使用了RFC-2104定义的HMAC算法。SSLv3.0使用了相似的算法，
        两者差别在于SSLv3.0中，填充字节与密钥之间采用的是连接运算，
        而HMAC算法采用的是异或运算。但是两者的安全程度是相同的。
    3. 伪随机函数：
        TLS使用了称为PRF的伪随机函数来将密钥扩展成数据块，是更安全的方式。
    4. 报警代码：
        TLS支持几乎所有的SSLv3.0报警代码，而且TLS还补充定义了很多报警代码，如
        1) 解密失败(decryption_failed)
        2) 记录溢出(record_overflow)
        3) 未知CA(unknown_ca)
        4) 拒绝访问(access_denied)等。
    5. 密文族和客户证书：
        SSLv3.0和TLS存在少量差别，即TLS"不支持":
        1) Fortezza密钥交换
        2) 加密算法
        3) 客户证书。
    6. certificate_verify和finished消息：
        SSLv3.0和TLS在用certificate_verify和finished消息计算MD5和SHA-1散列码时，
        计算的输入有少许差别，但安全性相当。
    7. 加密计算：
        TLS与SSLv3.0在计算主密值(master secret)时采用的方式不同。
        但都是以客户端和服务端各自产生的随机数Ramdom作为输入
    8. 填充：
        用户数据加密之前需要增加的填充字节。
        在SSL中，填充后的数据长度要达到密文块长度的最小整数倍。
        而在TLS中，填充后的数据长度可以是密文块长度的任意整数倍
        (但填充的最大长度为255字节)，
        这种方式可以防止基于对报文长度进行分析的攻击。
            
TLS协议详解
    参考资料：
        https://blog.csdn.net/s030602122/article/details/53538383
    TLS协议可以分为两部分
        记录协议（Record Protocol）
            通过使用客户端和服务端协商后的秘钥进行数据加密传输。
        握手协议（Handshake Protocol）
            客户端和服务端进行协商，确定一组用于数据传输加密的秘钥串
    SSL记录协议
        SSL记录协议是用来封装上层协议数据的协议，
        在SSL协议中，所有的传输数据都被封装在记录中
        录是由: "记录头 + 长度不为0的记录数据"组成的。
        SSL记录协议定义了要传输数据的格式，
        它位于一些可靠的的传输协议之上(如TCP)
        记录协议主要完成工作:
            1) 分组、组合
               每个上层应用数据被分成2^14(16K)字节或更小的数据块 
            2) 压缩、解压缩
               压缩是可选的，并且是无损压缩，压缩后内容长度的增加不能超过1024字节。
            3) 以及消息认证
               在压缩数据上计算消息认证MAC
            4) 加密传输等
               对压缩数据及MAC进行加密，
            5) 增加SSL记录头
               内容类型、主版本、次版本、压缩长度
        SSL记录协议的结构
            1. 内容类型(8位):
               1) 改变密码格式协议(change_cipher_spec): 20
               2) 警告协议(alert):                      21
               3) 握手协议(handshake):                  22
               4) 应用数据协议(application_data):       23
            2. 主要版本(8位):
               使用的SSL主要版本，目前的SSL版本是SSL v3，所以这个字段的值只有3这个值
            3. 次要版本(8位):
               使用的SSL次要版本。对于SSL v3.0，值为0。
            4. 数据包长度(16位):
               1) 明文数据包: 
                  这个字段表示的是明文数据以字节为单位的长度
               2) 压缩数据包
                  这个字段表示的是压缩数据以字节为单位的长度 
               3) 加密数据包
                  这个字段表示的是加密数据以字节为单位的长度
            5. 记录数据 
            6. MAC（0、16、20位）
    SSL握手协议
        协议格式
            1.  类型(Type)(1字节):
                该字段指明使用的SSL握手协议报文类型
                1) hello_request:
                2) client_hello:  
                3) server_hello: 
                4) certificate: 
                5) server_key_exchange:  
                6) certificate_request:  
                7) server_done: 
                8) certificate_verify:  
                9) client_key_exchange:  
                10) finished:  
            2.  长度(Length)(3字节):
                以字节为单位的报文长度。
            3.  内容(Content)(≥1字节):
                对应报文类型的的实际内容、参数
                1) hello_request: 空
                2) client_hello:  
                    2.1) 版本(ProtocolVersion)
                         代表客户端可以支持的SSL最高版本号
                         2.1.1) 主版本: 3
                         2.1.2) 次版本: 0
                    2.2) 随机数(Random)
                         客户端产生的一个用于生成主密钥(master key)的32字节的随机数
                         (主密钥由客户端和服务端的随机数共同生成)
                        2.2.1) uint32 gmt_unix_time;
                        2.2.2) opaque random_bytes[28];
                    2.3) 会话ID: 会话ID的长度 & 会话ID的内容
                    2.4) 密文族(加密套件): 
                        一个客户端可以支持的密码套件列表，2字节表示。
                        这个列表会根据使用优先顺序排列，每个密码套件都指定了
                        "密钥交换算法"、"加密算法"、"认证算法"、"加密方式"
                        注：
                            密钥交换算法使用Deffie-Hellman密钥交换算法、
                            基于RSA的密钥交换和另一种实现在Fortezza chip上的密钥交换
                            加密算法包括DES、RC4、RC2、3DES等
                            认证算法包括MD5或SHA-1
                            加密方式分为流式加密、分组加密
                        2.4.1) CipherSuite SSL_RSA_WITH_NULL_MD5                  
                        2.4.2) CipherSuite SSL_RSA_WITH_NULL_SHA                   
                        2.4.3) CipherSuite SSL_RSA_EXPORT_WITH_RC4_40_MD5          
                        2.4.4) CipherSuite SSL_RSA_WITH_RC4_128_MD5                
                        2.4.5) CipherSuite SSL_RSA_WITH_RC4_128_SHA                
                        2.4.6) CipherSuite SSL_RSA_EXPORT_WITH_RC2_CBC_40_MD5     
                        2.4.7) CipherSuite SSL_RSA_WITH_IDEA_CBC_SHA              
                        2.4.8) CipherSuite SSL_RSA_EXPORT_WITH_DES40_CBC_SHA     
                        2.4.9) CipherSuite SSL_RSA_WITH_DES_CBC_SHA               
                        2.4.10) CipherSuite SSL_RSA_WITH_3DES_EDE_CBC_SHA       
                        2.4.11) CipherSuite SSL_DH_DSS_EXPORT_WITH_DES40_CBC_SHA    
                        2.4.12) CipherSuite SSL_DH_DSS_WITH_DES_CBC_SHA             
                        2.4.13) CipherSuite SSL_DH_DSS_WITH_3DES_EDE_CBC_SHA        
                        2.4.14) CipherSuite SSL_DH_RSA_EXPORT_WITH_DES40_CBC_SHA    
                        2.4.15) CipherSuite SSL_DH_RSA_WITH_DES_CBC_SHA             
                        2.4.16) CipherSuite SSL_DH_RSA_WITH_3DES_EDE_CBC_SHA       
                        2.4.17) CipherSuite SSL_DHE_DSS_EXPORT_WITH_DES40_CBC_SHA   
                        2.4.18) CipherSuite SSL_DHE_DSS_WITH_DES_CBC_SHA            
                        2.4.19) CipherSuite SSL_DHE_DSS_WITH_3DES_EDE_CBC_SHA       
                        2.4.20) CipherSuite SSL_DHE_RSA_EXPORT_WITH_DES40_CBC_SHA   
                        2.4.21) CipherSuite SSL_DHE_RSA_WITH_DES_CBC_SHA           
                        2.4.22) CipherSuite SSL_DHE_RSA_WITH_3DES_EDE_CBC_SHA  
                        2.4.23) CipherSuite SSL_DH_anon_EXPORT_WITH_RC4_40_MD5     
                        2.4.24) CipherSuite SSL_DH_anon_WITH_RC4_128_MD5            
                        2.4.25) CipherSuite SSL_DH_anon_EXPORT_WITH_DES40_CBC_SHA  
                        2.4.26) CipherSuite SSL_DH_anon_WITH_DES_CBC_SHA           
                        2.4.27) CipherSuite SSL_DH_anon_WITH_3DES_EDE_CBC_SHA    
                        2.4.28) CipherSuite SSL_FORTEZZA_KEA_WITH_NULL_SHA          
                        2.4.29) CipherSuite SSL_FORTEZZA_KEA_WITH_FORTEZZA_CBC_SHA  
                        2.4.30) CipherSuite SSL_FORTEZZA_KEA_WITH_RC4_128_SHA      
                    2.5) 压缩方法：
                3) server_hello: 
                    3.1) 版本(ProtocolVersion)
                         代表服务端"采纳"的最高支持的SSL版本号
                         3.1.1) 主版本: 3
                         3.1.2) 次版本: 0
                    3.2) 随机数(Random)
                         服务端产生的一个用于生成主密钥(master key)的32字节的随机数
                         (主密钥由客户端和服务端的随机数共同生成)
                         3.2.1) uint32 gmt_unix_time;
                         3.2.2) opaque random_bytes[28];
                    3.3) 会话ID: opaque SessionID<0..32>;
                    3.4) 密文族(加密套件): 
                         代表服务端采纳的用于本次通讯的的加密套件
                    3.5) 压缩方法:
                         代表服务端采纳的用于本次通讯的的压缩方法
                         总体来看，server_hello就是服务端对客户端的的回应，表示采纳某个方案
                4) certificate: 
                   SSL服务器将自己的"服务端公钥证书(注意，是公钥整数)"发送给SSL客户端  
                   ASN.1Cert certificate_list<1..2^24-1>;
                5) server_key_exchange:   
                    1) RSA
                        执行RSA密钥协商过程
                        1.1) RSA参数(ServerRSAParams)
                            1.1.1) opaque RSA_modulus<1..2^16-1>;
                            1.1.2) opaque RSA_exponent<1..2^16-1>;
                        1.2) 签名参数(Signature)
                            1.2.1) anonymous: null
                            1.2.2) rsa
                              　　 1.2.2.1) opaque md5_hash[16];
                              　　 1.2.2.2) opaque sha_hash[20];
                            1.2.3) dsa
                                   1.2.3.1) opaque sha_hash[20];
                    2) diffie_hellman
                        执行DH密钥协商过程
                        2.1) DH参数(ServerDHParams)
                            2.1.1) opaque DH_p<1..2^16-1>;
                            2.1.2) opaque DH_g<1..2^16-1>;
                            2.1.3) opaque DH_Ys<1..2^16-1>;
                        2.2) 签名参数(Signature)
                            2.2.1) anonymous: null
                            2.2.2) rsa
                                2.2.2.1) opaque md5_hash[16];
                                2.2.2.2) opaque sha_hash[20];
                            2.2.3) dsa
                                2.2.3.1) opaque sha_hash[20];
                    3) fortezza_kea
                        执行fortezza_kea密钥协商过程
                        3.1) opaque r_s [128]
                6) certificate_request:   
                    6.1) 证书类型(CertificateType)
                        6.1.1) RSA_sign
                        6.1.2) DSS_sign
                        6.1.3) RSA_fixed_DH
                        6.1.4) DSS_fixed_DH
                        6.1.5) RSA_ephemeral_DH
                        6.1.6) DSS_ephemeral_DH  
                        6.1.7) FORTEZZA_MISSI
                    6.2) 唯一名称(DistinguishedName)
                    certificate_authorities<3..2^16-1>;
                7) server_done: 
                   服务器总是发送server_hello_done报文，指示服务器的hello阶段结束
                   struct { } ServerHelloDone;
                8) certificate_verify:  
                    签名参数(Signature)
                    8.1) anonymous: null
                    8.2) rsa
                        8.2.1) opaque md5_hash[16];
                        8.2.2) opaque sha_hash[20];
                    8.3) dsa
                        8.3.1) opaque sha_hash[20];
                9) client_key_exchange:  
                    9.1) RSA
                        9.1.1) PreMasterSecret
                            9.1.1.1) ProtocolVersion 
                            9.1.1.2) opaque random[46];
                    9.2) diffie_hellman: opaque DH_Yc<1..2^16-1>;
                    9.3) fortezza_kea
                        9.3.1) opaque y_c<0..128>;
                        9.3.2) opaque r_c[128];
                        9.3.3) opaque y_signature[40];
                        9.3.4) opaque wrapped_client_write_key[12];
                        9.3.5) opaque wrapped_server_write_key[12];
                        9.3.6) opaque client_write_iv[24];
                        9.3.7) opaque server_write_iv[24];
                        9.3.8) opaque master_secret_iv[24];
                        9.3.9) opaque encrypted_preMasterSecret[48];
                10) finished:  
                        10.1) opaque md5_hash[16];
                        10.2) opaque sha_hash[20];
                        
只验证服务器的SSL握手过程
    1. Client Hello
        SSL客户端通过Client Hello消息向SSL服务端发送:
        1) 支持的SSL版本
        2) 客户端生成的一个用于生成主密钥(master key)的32字节的随机数(主密钥由客户端和服务端的随机数共同生成)
        3) 会话ID
        3) 加密套件
            3.1) 加密算法
            3.2) 密钥交换算法
            3.3) MAC算法
            3.4) 加密方式(流、分组)
        4) 压缩算法(如果支持压缩的话)
    2. Server Hello
        SSL服务器确定本次通信采用的SSL版本和加密套件，并通过Server Hello消息通知给SSL客户端。
        如果SSL服务器允许SSL客户端在以后的通信中重用本次会话，则SSL服务器会为本次会话分配会话ID，
        并通过Server Hello消息发送给SSL客户端。
        1) 服务端采纳的本次通讯的SSL版本
        2) 服务端生成的一个用于生成主密钥(master key)的32字节的随机数(主密钥由客户端和服务端的随机数共同生成)
        3) 会话ID
        3) 服务端采纳的用于本次通讯的加密套件(从客户端发送的加密套件列表中选出了一个)
            3.1) 加密算法
            3.2) 密钥交换算法
            3.3) MAC算法
            3.4) 加密方式(流、分组)
        4) 压缩算法(如果支持压缩的话)
    3. Certificate
        SSL服务器将"携带自己公钥信息的数字证书"和到根CA整个链发给客户端通过Certificate消息发送给SSL客户端(整个公钥文件都发送过去)，
        客户端使用这个公钥完成以下任务:
            1) 客户端可以使用该公钥来验证服务端的身份，因为只有服务端有对应的私钥能解密它的公钥加密的数据
            2) 用于对"premaster secret"进行加密，这个"premaster secret"就是用客户端和服务端生成的Ramdom随机数来生成的，
               客户端用服务端的公钥对其进行了加密后发送给服务端
    4. Server Key Exchange
        密钥交换阶段(可选步骤)，之所以说是可选步骤，是因为只有在下列场景下这个步骤才会发生
        1) 协商采用了RSA加密，但是服务端的证书没有提供RSA公钥
        2) 协商采用了DH加密，但是服务端的证书没有提供DH参数
        3) 协商采用了fortezza_kea加密，但是服务端的证书没有提供参数
        总结来说，"Server Key Exchange"这个步骤是对上一步"Certificate"的一个补充，为了让整个SSL握手过程能正常进行
    5. Server Hello Done
        SSL服务器发送Server Hello Done消息，通知SSL客户端版本和加密套件协商结束 
    6. Client Key Exchange
        SSL客户端验证SSL服务器的证书合法后，利用证书中的公钥加密SSL客户端随机生成的"premaster secret"
        (通过之前客户端、服务端分别生成的随机数生成的)，
        并通过Client Key Exchange消息发送给SSL服务器。
        注意，这一步完成后，客户端和服务端都已经保存了"主密钥"(之所以这里叫预备主密钥，是因为还没有投入使用)。
        这个"主密钥"会用于之后的SSL通信数据的加密
    7. Change Cipher Spec
        SSL客户端发送Change Cipher Spec消息，通知SSL服务器后续报文将采用协商好的"主密钥"和加密套件进行加密和MAC计算。
    8. Finished
        SSL客户端计算已交互的握手消息(除Change Cipher Spec消息外所有已交互的消息)的Hash值，
        利用协商好的密钥和加密套件处理Hash值(计算并添加MAC值、加密等)，并通过Finished消息发送给SSL服务器。
        SSL服务器利用同样的方法计算已交互的握手消息的Hash值，并与Finished消息的解密结果比较，
        如果二者相同，且MAC值验证成功，则证明密钥和加密套件协商成功。
    9. Change Cipher Spec
        同样地，SSL服务器发送Change Cipher Spec消息，通知SSL客户端后续报文将采用协商好的密钥和加密套件进行加密和MAC计算。
    10. Finished
        SSL服务器计算已交互的握手消息的Hash值，利用协商好的密钥和加密套件处理Hash值(计算并添加MAC值、加密等)，
        并通过Finished消息发送给SSL客户端。SSL客户端利用同样的方法计算已
        交互的握手消息的Hash值，并与Finished消息的解密结果比较，如果二者相同，且MAC值验证成功，则证明密钥和加密套件协商成功。
        SSL客户端接收到SSL服务器发送的Finished消息后，如果解密成功，则可以判断SSL服务器是数字证书的拥有者，
        即SSL服务器身份验证成功，因为只有拥有私钥的SSL服务器才能从Client Key Exchange消息中解密得到premaster secret，
        从而间接地实现了SSL客户端对SSL服务器的身份验证。
