PKCS 
    全称是 Public-Key Cryptography Standards,
    翻译为公钥密码学标准，
    是由 RSA 实验室与其它安全系统开发商
    为促进公钥密码的发展而制订的一系列标准

PKCS 目前共发布过 15 个标准
    PKCS1：RSA加密标准。
        参看后面的P1详解
    PKCS2：涉及了RSA的消息摘要加密，这已被并入PKCS1中。
    PKCS3：Diffie-Hellman密钥协议标准。
        PKCS3描述了一种实现Diffie- Hellman密钥协议的方法。
    PKCS4：最初是规定RSA密钥语法的，现已经被包含进PKCS1中。
    PKCS5：基于口令的加密标准。
        PKCS5是个加密方法
        PKCS5描述了使用由口令生成的密钥来加密8位位组串
        并产生一个加密的8位位组串的方法。
        PKCS5可以用于加密私钥，以便于密钥的安全传输（这在PKCS8中描述）。
        描述一种利用从口令派生出来的安全密钥加密字符串的方法。
        使用MD2或MD5 从口令中派生密钥，并采用DES-CBC模式加密。
        主要用于加密从一个计算机传送到另一个计算机的私人密钥，
        不能用于加密消息。
    PKCS6：扩展证书语法标准。
        PKCS6定义了提供附加实体信息的X.509证书属性扩展的语法
        （当PKCS6第一次发布时，X.509还不支持扩展。这些扩展因此被包括在X.509中）。
    PKCS7：密码消息语法标准。
        PKCS7在RFC 2315中定义
        参后面的P7详解
    PKCS8：私钥信息语法标准。
        PKCS8在RFC 5208中定义
        该标准的主要目的是私钥信息标准。 
        它定义了私钥信息（不仅仅是RSA）的语法。 
        使用"算法标识符+密钥数据"表示密钥结构。
        当算法标识是RSA时，密钥数据就使用P1编码。
        另外P8中还允许任意添加“属性”，尽管这很少使用。
        P8还提供了一个选项，可以使用P5来加密私钥，
        这很常用，特别是当P8作为P12/pfx的私钥部分时，
        ——尽管这不是通用的。
        由于当今大多数系统都需要支持多种算法，
        并且希望能够使用新算法的开发，
        因此P8对于私钥是首选的，
        而X509为公钥定义了类似的(任何算法)方案。
    PKCS9：可选属性类型。
        PKCS9定义了PKCS6扩展证书、PKCS7数字签名消息、
        PKCS8私钥信息和PKCS10证书签名请求中要用到的可选属性类型。
        已定义的证书属性包括E-mail地址、无格式姓名、内容类型、
        消息摘要、签名时间、签名副本（counter signature）、
        质询口令字和扩展证书属性。
    PKCS10：证书请求语法标准。
        PKCS10定义了证书请求的语法。
        证书请求包含了一个唯一识别名、公钥和可选的一组属性，
        它们一起被请求证书的实体签名（证书管理协议中的PKIX证书请求消息就是一个PKCS10）。
        PKCS10 常用的后缀有：.p10 .csr
    PKCS11：密码令牌接口标准。
        PKCS11或“Cryptoki”为拥有密码信息（如加密密钥和证书）和执行密码学函数的单用户设备
        定义了一个应用程序接口（API）。
        智能卡(UsbKey)就是实现Cryptoki的典型设备。
        注意：Cryptoki定义了密码函数接口，但并未指明设备具体如何实现这些函数。
        而且Cryptoki只说明了密码接口，并未定义对设备来说可能有用的其他接口，如访问设备的文件系统接口。
        另：ukey驱动的接口有三种：csp是微软定义的、P11是RSA定义的、SKF是国内定义的。
    PKCS12：个人信息交换语法标准。
        PKCS12定义了个人身份信息（包括私钥、证书、各种秘密和扩展字段）的格式。
        描述了将用户公钥、私钥、证书和其他相关信息打包的语法。
        PKCS12有助于传输证书及对应的私钥，于是用户可以在不同设备间移动他们的个人身份信息。
        PKCS12 常用的后缀有： .P12 .PFX
        PKCS12定义了通常用来存储Private Keys和Public Key Certificates
        （例如前面提到的X.509）的文件格式，使用基于密码的对称密钥进行保护。
        注意上述Private Keys和Public Key Certificates是复数形式，
        这意味着PKCS 12文件实际上是一个Keystore，详见RFC7292。
    PDCS13：椭圆曲线密码标准。
        PKCS13标准当前正在完善之中。
        它包括椭圆曲线参数的生成和验证、密钥生成和验证、数字签名和公钥加密，
        还有密钥协定，以及参数、密钥和方案标识的ASN.1语法。
    PKCS14：伪随机数产生标准。
        PKCS14标准当前正在完善之中。
        为什么随机数生成也需要建立自己的标准呢？
        PKI中用到的许多基本的密码学函数，
        如密钥生成和Diffie-Hellman共享密钥协商，都需要使用随机数。
        然而，如果“随机数”不是随机的，而是取自一个可预测的取值集合，
        那么密码学函数就不再是绝对安全了，因为它的取值被限于一个缩小了的值域中。
        因此，安全伪随机数的生成对于PKI的安全极为关键。
    PKCS15：密码令牌信息语法标准。
        PKCS15通过定义令牌上存储的密码对象的通用格式来增进密码令牌的互操作性。
        在实现PKCS15的设备上存储的数据对于使用该设备的所有应用程序来说都是一样的，
        尽管实际上在内部实现时可能所用的格式不同。
        PKCS15的实现扮演了翻译家的角色，它在卡的内部格式与应用程序支持的数据格式间进行转换。
        
P1详解
    PKCS1有几种版本，分别在RCF 2313/2437/3447/8017中定义，
    2313/2437/3447这些是比较旧的版本，已弃用，以8017版为准。
    主要涉及使用RSA算法进行加密，包括加密，解密，签名和验证。
    PKCS1定义了RSA公、私钥的基本格式标准和语法。
    这有助于选择和计算用于RSA算法的密钥对。 
    也定义了数字签名如何计算，包括待签名数据和签名本身的格式；
    除此之外，它还定义了应该如何计算数字证书，如何对数据结构进行签名，数字签名的格式。
    由于通常在系统之间或至少在程序之间使用加密，因此具有定义好的、可互操作的密钥格式很方便，
    并且PKCS1在附录A.1中为RSA公钥和私钥定义了相当小的格式。
    在RCF8017中，定义了RSA Public Key和Private Key数学属性和格式，
    详细的介绍了RSA算法的计算过程，包括：key的产生，key的结构，
    对数字加密／解密／签名／验证签名的过程、对应算法。
    key
        关于key，分别记录了private和public的详细结构，以及存储哪些内容。
        并且在附录里面推荐了ASN.1 Syntax中的存储结构。注：没有规定实际的物理文件存储结构，比如pem等。
    加密／解密 
        详细描述了加密／解密的算法。包括，首先针对字符串，怎么转化成数字，之后，怎么根据数字进行加密。 
        这里可以看出，标准中没有对超长字符串处理的说明。而转化出的字符串的长度，全都是key的模长度k。
        在字符串转化成数字过程中，需要增加填充字符，所以，分成了两种不同算法：
        RSAES-OAEP（现有标准） RSAES-PKCS1-v1_5（兼容过去标准）。在实际加密过程中，就只有一种算法了
    哈希
        无论在加密还是签名过程中，都会进行hash操作，
        hash操作没有自己定义，而是从附录中可以选择需要的hash方式。
    PKCS1填充方式：
        在进行RSA运算时需要将源数据D转化为Encryption block（EB）。
        其中pkcs1padding V1.5的填充模式按照以下方式进行：
    RCF8017内容简介：
        第一章是简介部分
        第二章定义了一些本文中用到的术语
        第三章定义了RSA公钥和私钥类型
            公钥包含两个元素：n RSA 模数, e RSA 公共指数; n和e都是正整数。n和e的用法见规范原文
            私钥有两种形式：
                1. n RSA 模数，e RSA 私有指数； n和e都是正整数。
                2. 包含如下元素（均为正整数）：
                    p 第一乘数、
                    q 第二乘数、
                    dP 第一乘数的CRT因子、
                    dQ 第二乘数的CRT因子、
                    qInv （第一）CRT系数、
                    r_i 第i个因子、
                    d_i 第i个因子CRT指数、
                    t_i 第i个因子CRT系数
            附录 A.1.1 中给出了在实现之间交换 RSA 公钥的推荐语法； 一个实现的内部表示可能不同
        第四、五章定义了几个原语(基本的数学操作): 
            数据转换原语在第四章：
                OctetString I2OSP (uint x,int& xLen) ：整型转OCTET String原语，内部实现见规范原文
                uint OS2IP (OctetString X) ： OCTET String转整形原语，内部实现见规范原文
            密码原语（加密-解密和签名验证）在第五章：
                RSAEP ((n, e), m)： RSA加密原语，内部实现见规范原文
                RSADP (K, c)： RSA Decode Primitives，内部实现见规范原文
                RSASP1 (K, m)：RSA签名原语，内部实现见规范原文
                RSASP1 (K, m)：RSA验证签名原语，内部实现见规范原文
        第六、七、八章给出了加密和签名方案
            第六章给出了方案概述。 
            第七章与 PKCS1 v1.5 中的方法一起，定义了基于最佳非对称加密填充 (OAEP) OAEP 的加密方案。
            第八章定义了基于概率签名方案 (PSS) 的带有附录的签名方案 RSARABIN PSS。
        第九章定义了第八章中签名方案的编码方法
        附录A为第三章中定义的密钥和第七、八章中的方案定义了 ASN.1 语法。
        附录B定义了本文档中使用的散列函数和掩码生成函数 (MGF)，包括技术的 ASN.1 语法
        
P7详解
    用途：
        加密消息语法（pkcs7），是各种消息存放的格式标准
        换句话说，PKCS7为使用密码算法的数据规定了通用语法，
        这些消息包括：数据、签名数据、数字信封、签名数字信封、摘要数据和加密数据。
        PKCS7 常用的后缀是： .P7B .P7C .SPC
    数据结构：
      数据：
        OCTET STRING
      签名数据：
        struct PKCS7
            ASN1_OBJECT *type
            union d 
                char *ptr;
                ASN1_OCTET_STRING *data;                    /* NID_pkcs7_data */
                PKCS7_SIGNED *sign;                         /* NID_pkcs7_signed */
                PKCS7_ENVELOPE *enveloped;                  /* NID_pkcs7_enveloped */
                PKCS7_SIGN_ENVELOPE *signed_and_enveloped;  /* NID_pkcs7_signedAndEnveloped */
                PKCS7_DIGEST *digest;                       /* NID_pkcs7_digest */
                PKCS7_ENCRYPT *encrypted;                   /* NID_pkcs7_encrypted */
                ASN1_TYPE *other;                           /* Anything else */
            其中type用于表示是何种类型的pkcs7消息：
            data、sign、enveloped、signed_and_enveloped、digest和ncrypted
            oher用于存放任意数据类型（也可以是pkcs7结构），
            所以，本结构可以是一个嵌套的数据结构。   
        struct PKCS7_SIGNED
            ASN1_INTEGER                *version;           /* version 1 */
            STACK_OF(X509_ALGOR)        *md_algs;           /* md used */
            STACK_OF(X509)              *cert;              /* [ 0 ] */
            STACK_OF(X509_CRL)          *crl;               /* [ 1 ] */
            STACK_OF(PKCS7_SIGNER_INFO) *signer_info;
            PKCS7 *contents;
        struct PKCS7_SIGNER_INFO
            ASN1_INTEGER 			    *version;	        /* version 1 */
            PKCS7_ISSUER_AND_SERIAL		*issuer_and_serial;
            X509_ALGOR			        *digest_alg;
            STACK_OF(X509_ATTRIBUTE)	*auth_attr;	        /* [ 0 ] */
            X509_ALGOR			        *digest_enc_alg;
            ASN1_OCTET_STRING		    *enc_digest;
            STACK_OF(X509_ATTRIBUTE)	*unauth_attr;	    /* [ 1 ] */
            EVP_PKEY			        *pkey;              /* The private key to sign with */
    特点：
        当使用PKCS7进行数字签名时，
        结果包含签名证书（一列相关证书撤回列表）和已证明路径上任何其他证书。
        如果使用PKCS7加密数据，
        通常包含发行者的参考消息和证书的序列号，
        它与用于解密已加密数据的公共密钥相关。
        PKCS7也支持另外一些特征，如：
        ·递归，在一个数字信封上附上一个数字信封，还可再附上一个数字信封，如此等等。
        ·加密消息和数字签名的时间标记。
        ·签名计数和用户定义属性。
        
P1 vs. P8
    P1规范存储的私钥是不加密的，
    还定义了公钥的格式，待签名数据和签名本身的格式，数字签名如何计算等
    PKCS8，Private-Key Information Syntax Standard，详细的描述了私钥的存储格式。
    用于加密、非加密地存储Private Certificate Keypairs（不限于RSA），详见RFC5858。

P1 vs. P7
    P1签名:即裸签名,签名值中只有签名信息.
    p7签名:即,签名中可以带有其他的附加信息,例如签名证书信息,签名原文信息,时间戳信息等.
    验证PKCS7 signedData结构涉及验证RSA PKCS1 v1.5签名，
    但在此之前还需要执行许多重要步骤，包括解析该数据结构，
    并检查依赖于上下文的内容。
    signedData具有引导加载程序可能不需要的功能，例如带有吊销列表的证书。
    
P7格式 -- 签名数据
    由任意类型的内容和加密的（ 0或多个签名者）消息摘要组成。
    对于一个签名者来说加了密的摘要就是他对该内容的“数字签名”
    任何类型的内容能够同时被任意数量的签名者签名。 
    此外，该语法有一个简化版本 ，其中的内容没有签名者
    签名数据的产生过程：
        1. 对于每一个签名者，可以使用自己的摘要算法，如SM3,MD5，对原文计算出摘要值
           如果还要保护除原文（的摘要值）之外的其它信息，则应把摘要和其它信息，
           进行二次摘要，得到一个“消息摘要”。
        2. 对于每一个签名值，把消息摘要和相关信息，用自己的私钥加密
        3. 对于每一个签名者，把加密的消息摘要，和其它的签名者相关信息，放入SignerInfo结构中
           每个签名者的证书、crl，以及那些不特定于某一签名着的通用信息，也在这一步被填充进来
        4. 把消息摘要算法、SignerInfo值、内容等，放到SignedData中，得到签名数据
    验证过程:
        用签名者的公钥，解开加密的信息摘要，然后与签名结构中的摘要对比
        公钥可以是在签名者证书中(SignerInfo结构中)，
        也可以由一个“颁发者可辨别名 和 颁发序列号”来指引，它能唯一标识一个公钥证书。
    SignedData:
        ContentInfo ::= SEQUENCE 
            contentType ContentType,        #定义内容类型的权威机构分配的唯一整数串
            content EXPLICIT ANY DEFINED BY contentType OPTIONAL #通常是六种内容类型之一，也可以是自定义类型
        ContentType ::= OBJECT IDENTIFIER
        SignedData ::= SEQUENCE
            version Version,                #为1
            digestAlgorithms DigestAlgorithmIdentifiers,  #各个签名者使用的摘要算法的集合，可以为0个
            contentInfo ContentInfo,        #被签名内容，可以是任何一种定义了的内容类型
            certificates IMPLICIT ExtendedCertificatesAndCertificates OPTIONAL,  #证书信任链
            crls IMPLICIT CertificateRevocationLists OPTIONAL,  #吊销列表
            signerInfos SignerInfos         #每个签名者信息的集合
        DigestAlgorithmIdentifiers ::= SET OF DigestAlgorithmIdentifier
        SignerInfos ::= SET OF SignerInfo
        注：版本1的SignedData vs 版本0的SignedData
            版本1中，digestAlgorithms和signerInfos域可能包含0元素， 而版本0则不能
            版本1中，可有crls 域，而版本0中则不行。
        SignerInfo ::= SEQUENCE 
            version Version,                             #版本号，为1
            issuerAndSerialNumber IssuerAndSerialNumber, #颁发者的可辨别名和颁发序列号来指定签名者的证书
            digestAlgorithm DigestAlgorithmIdentifier,   #指定对内容和待鉴别属性(若存在的话)进行摘要计算的信息摘要算法
            authenticatedAttributes IMPLICIT Attributes OPTIONAL,    #经由签名者签名的属性的集合
            digestEncryptionAlgorithm DigestEncryptionAlgorithmIdentifier,  #摘要签名算法，如Sm2WithSm3
            encryptedDigest EncryptedDigest,             #用签名者私钥加密消息摘要和相关信息后的结果
            unauthenticatedAttributes IMPLICIT Attributes OPTIONAL   #不被签名者签名的属性的集合 
        EncryptedDigest ::= OCTET STRING
        注：authenticatedAttributes是可选的，但当签名原文contentInfo不是data类型时，则必须包含至少下面两个属性
            content-type 属性
            message-digest 属性
    消息摘要的处理
        摘要处理的是待签名的内容或附带签名者鉴别属性的内容
        不管是哪种，初始的输入是ContentInfo的content域中的der编码的内容字节
        ————不包括 identifier字节或length字节
        摘要处理的结果，依赖于authenticatedAttributes域是否存在，
        当该域不存在时，结果就是内容的消息摘要值，
        如果存在，结果是包含authenticatedAttributes中的属性值的完全DER编码的消息摘要
        当待签名内容的content type是data且authenticatedAttributes域不存在时
        仅该数据的值(e.g.，文件的内容)进行摘要计算
 
 