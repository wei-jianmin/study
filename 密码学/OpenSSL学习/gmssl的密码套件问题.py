<catalog s0>
file://密码相关知识.py
file://../密码套件.txt

ab工具不支持 sm2-with-sms4-sm3 问题
sm2-with-sms4-sm3 定义在 gmtls.h 中
    注：SM4分组密码算法，原名SMS4
    https://www.cnblogs.com/codingmengmeng/p/5476260.html
    SM4为对称算法，密钥长度和分组长度均为128位。
    按原SMS4的标准描述：
        加密算法与密钥扩展算法都采用32轮非线性迭代结构。
        解密算法与加密算法的结构相同，只是轮密钥的使用顺序相反，
        解密轮密钥是加密轮密钥的逆序。
    上面的链接中还给出了sm4的C语言实现

AB 支持的密码套件：
    ECC-SM4-CBC-SM3
    ECC-SM4-GCM-SM3
    ECDHE-SM4-CBC-SM3
    ECDHE-SM4-GCM-SM3
    注：ECC 和 ECDHE
        ECC 和 RSA 类似，也属于非对称加密算法
            由于椭圆曲线的特性，给定k和G可以计算出K，但给定K和G无法计算出k
            加密过程：
            1. A 选定一椭圆曲线上的点 G
            2. A 创建私钥 k，生成公钥 K = k*G
            3. A 将椭圆曲线、K、G 发送给 B
            4. B 选择椭圆曲线上的一点 M，产生一随机数 r
            5. B 计算点 C1 = M + r * K，C2 = r * G
            6. B 把 C1，C2 发送给 A
            7. A 计算 C1 - key*C2 = M + r*KEY*G - key*r*G = M
        DH （秘钥协商协议）
        ECDH（ECC&DH）
        
nginx支持的密码套件：
   SM2-WITH-SMS4-SM3:SM2DHE-WITH-SMS4-SM3 （ 这是 SSL-VPN CipherSuites ）
   
GmSSL 支持两类套件，
   一类是用于 TLS 1.2 (以及未来的TLS 1.3）的套件，
   一类是 GM/T 0024 SSL VPN标准中定义的套件
   由于 GM/T 0024 这个协议可以视为是和IETF TLS协议完全不同的协议
   因此GmSSL中的GM/T 0024套件仅能应用GM/T 0024协议，
   在 TLS 1.2 协议中用了 GM/T 0024 的套件，就会报错
   
在 gmt 0024 ssl vpn 技术规范 第19页  定义了 密码套件列表
   在gmssl头文件中搜 0X0300E0 关键字，或 GM/T SSL-VPN CipherSuites 关键字
   能跟这里的密码套件列表对应上
   ssl vpn 技术规范中，对 ssl 密码套件进行了扩充
   
gmssl头文件中支持的算法
   ECDHE-SM2-WITH-SMS4-SM3
   ECDHE-SM2-WITH-SM1-SM3
   ECDHE-SM2-WITH-SM1-SHA256
   SM2DHE-WITH-SMS4-SM3
   SM2-WITH-SMS4-SM3
   SM9DHE-WITH-SMS4-SM3
   SM9-WITH-SMS4-SM3
   RSA-WITH-SMS4-SM3
   RSA-WITH-SMS4-SHA1
   。。。
   
密码套件结构定义：
   不同的加密套件，影响密钥交换、身份认证、加解密等规则 
   struct ssl_cipher_st {
        uint32_t valid;
        const char *name;           /* 文本名称 */
        uint32_t id;                /* id, 4 bytes, first is version */
        /*
         * changed in 1.0.0: these four used to be portions of a single value
         * 'algorithms'
         */
        uint32_t algorithm_mkey;    /* 密钥交换算法 ：key exchange algorithm */
        uint32_t algorithm_auth;    /* 服务端认证 ：server authentication */
        uint32_t algorithm_enc;     /* 对称加密： symmetric encryption */
        uint32_t algorithm_mac;     /* 对称身份认证： symmetric authentication */
        int min_tls;                /* minimum SSL/TLS protocol version */
        int max_tls;                /* maximum SSL/TLS protocol version */
        int min_dtls;               /* minimum DTLS protocol version */
        int max_dtls;               /* maximum DTLS protocol version */
        uint32_t algo_strength;     /* strength and export flags */
        uint32_t algorithm2;        /* Extra flags */
        int32_t strength_bits;      /* Number of bits really used */
        uint32_t alg_bits;          /* Number of bits for algorithm */
    };   
    
ssl 和 vpn ：
    const SSL_METHOD *GMTLS_method(void);
    const SSL_METHOD *gmtls_server_method(void);
    const SSL_METHOD *gmtls_client_method(void);
    #define SSLv23_method           TLS_method
    #define SSLv23_server_method    TLS_server_method
    #define SSLv23_client_method    TLS_client_method
    
    如果初始化使用SSL_CTX_new(GMTLS_method)，
    使用GMTLS_method就变成国密VPN通信，这个需要参考国标GM/T 0024
    
gmssl(v2.3.1) 和 openssl
    gmssl 扩展加密和通信两部分（openssl分为密码模块crypto和通信模块ssl），
    加密主要指的是sm2 sm3 sm4加密算法，以及相关的加密组件
    通信指的是gmtls，按照一个 GM/T 0024-2014规范实现的，采用双证书，签名证书+加密证书
    如果使用国密tls，则只支持 ECDHE-SM2-WITH-SMS4-SM3 和 ECDHE-SM2-WITH-SMS4-SHA256 套件
    gmssl对双证书和双密钥的设置
        直接设置两个sm2证书和密钥就可以，没有新增接口，都是代码里自己适配：
        keyusagedigitalSignature类型的证书是签名证书，否则是加密证书,
        密钥呢，加密证书存在的时候是加密密钥，否则是签名密钥
        这个其实是有漏洞的，必须先设置签名证书。。然后才是加密证书