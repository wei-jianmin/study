https://www.jianshu.com/p/8dc93f3946c3
    SSL通信过程的官方规范是 RFC5246
    
参： https://blog.csdn.net/H_O_W_E/article/details/125247938
    握手消息中定义的密码套件：
    包含：密钥交换算法+身份认证&加密算法+摘要算法
    rfc5289 中定义的密码套件:
        CipherSuite TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256  = {0xC0,0x2B};
        CipherSuite TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384  = {0xC0,0x2C};
        CipherSuite TLS_ECDH_ECDSA_WITH_AES_128_GCM_SHA256   = {0xC0,0x2D};
        CipherSuite TLS_ECDH_ECDSA_WITH_AES_256_GCM_SHA384   = {0xC0,0x2E};
        CipherSuite TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256    = {0xC0,0x2F};
        CipherSuite TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384    = {0xC0,0x30};
        CipherSuite TLS_ECDH_RSA_WITH_AES_128_GCM_SHA256     = {0xC0,0x31};
        CipherSuite TLS_ECDH_RSA_WITH_AES_256_GCM_SHA384     = {0xC0,0x32};
    以 TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 为例：
        TLS ： 表明密码套件用于tls协议
        ECDHE ： 密钥交换
        ECDSA_WITH_AES_128_GCM ： 身份认证&加解密
        SHA256 ： 摘要
        
https://blog.csdn.net/fw0124/article/details/40983787
    握手过程实际上就是通信双方协商交换一个用于对称加密的密钥的过程
    这个过程实际上产生三个随机数:client random, server random, pre-master secret.
    前两个随机数都是明文传送的，只有pre-master secret是加密的（RSA或者DH)。  
    
    一般生成证书的时候，签名算法可以选择RSA或者DSA算法
        如果server使用RSA证书，
            RSA即可以用作签名也可以用作不对称加密，
            pre-master secret就是用server的RSA证书中包含的公钥加密的。
        如果server使用DSA证书，
            DSA只能用作签名，所以还需要使用DH算法来交换密钥。
    
    客户端发给服务端
        client_hello
            （1）支持的协议版本，比如TLS 1.0
            （2）支持的加密算法(Cipher Specs)
            （3）客户端生成的随机数1(Challenge)，稍后用于生成"对话密钥"。
    服务端发给客户端
        server_hello
            （1） 确认使用的协议版本
            （2） 服务器生成的随机数2，稍后用于生成"对话密钥"
            （3） session id
            （4） 确认使用的加密算法
        certificate
            服务器证书
        server_key_exchange
            如果是DH算法，这里发送服务器使用的DH参数。RSA算法不需要这一步。
        certificate_request
            要求客户端提供证书，包括
            （1）客户端可以提供的证书类型
            （2）服务器接受的证书distinguished name列表，
                 可以是root CA或者subordinate CA。
                 如果服务器配置了trust keystore, 
                 这里会列出所有在trust keystore中的证书的distinguished name。
        server_hello_done
            server hello结束
    客户端发给服务端
        certificate
            客户端证书
        client_key_exchange
            包含pre-master secret。客户端生成第三个随机数。
            如果是采用RSA算法，会生成一个48字节随机数，
            然后用server的公钥加密之后再放入报文中；
            如果是DH算法，这里发送的就是客户端的DH参数，
            之后服务器和客户端根据DH算法，各自计算出相同的pre-master secret。
        certificate_verify
            发送"使用客户端证书给<到这一步为止收到和发送的所有握手消息>签名"的结果。
        change_cipher_spec
            客户端通知服务器开始使用加密方式发送报文。
            客户端使用上面的3个随机数client random, server random, pre-master secret, 
            计算出48字节的master secret, 这个就是对称加密算法的密钥。
        finished
            客户端发送第一个加密报文。
            使用HMAC算法计算收到和发送的所有握手消息的摘要，
            然后通过RFC5246中定义的一个伪函数PRF计算出结果，加密后发送。
    服务端发给客户端
        change_cipher_spec
        finished
        
https://blog.csdn.net/fw0124/article/details/40875629
    图解SSL/TLS协议
    
随机数的作用
    https://blog.csdn.net/mrpre/article/details/77973464
        （1）生成master key
            主密钥计算过程如下
                第一步构造 buf1= “master secret” + client_random +  server_random
                第二步送入PRF运算。
                    PRF的入参label为 buf1，secret为pre_master_key，出参为master key
            master_secret = PRF(pre_master_secret, "master secret",
                                ClientHello.random + ServerHello.random) [0..47];
        （2）生成对称密钥symmetry key
            即使是会话复用流程，也会进行对称密钥计算，会话复用可以恢复之前的master key
            第一步构造 buf2 = “key expansion” + server_random + client_ranom
            第二步 送入 PRF运算。
                PRF入参label是 buf2，secret为master_key，出参为symmetry key
            key_block = PRF(SecurityParameters.master_secret,
                            "key expansion",
                            SecurityParameters.server_random +
                            SecurityParameters.client_random);
        （3）计算server key exchange 
            对server key exhange 签名前，
            需要对server key exchange 报文进行摘要计算，
            摘要不是简单的对报文进行hash，也需要随机数参与。
            第一步 构造 buf3 = client_random + server_random + value
            第二步 HASH(buf3)
        最后，抛开代码，从功能上来讲，随机数可以有效防止重放攻击。
            例如session resume时候，当前会话的master key是上一个会话的master key，
            如果直接使用这个master key进行加密，就很容易进行重放攻击，
            所以在生成对称秘钥时，使用当前的握手的随机数和master key进行一次prf，
            使得当前加解密的key和上一个会话的不一样，
            中间人就没办法重放一个有效的application data。

        
    