<catalog s0/s4/s8/s12/s16 catalog_line_prefix=->
-PKCS是什么
    全称是 Public-Key Cryptography Standards,
    翻译为公钥密码学标准，
    是由 RSA 实验室与其它安全系统开发商
    为促进公钥密码的发展而制订的一系列标准

-PKCS 目前共发布过 15 个标准
    -PKCS1：RSA加密标准。
        参看后面的P1详解
    -PKCS2：涉及了RSA的消息摘要加密，这已被并入PKCS1中。
    -PKCS3：Diffie-Hellman密钥协议标准。
        PKCS3描述了一种实现Diffie- Hellman密钥协议的方法。
    -PKCS4：最初是规定RSA密钥语法的，现已经被包含进PKCS1中。
    -PKCS5：基于口令的加密标准。
        PKCS5是个加密方法
        PKCS5描述了使用由口令生成的密钥来加密8位位组串
        并产生一个加密的8位位组串的方法。
        PKCS5可以用于加密私钥，以便于密钥的安全传输（这在PKCS8中描述）。
        描述一种利用从口令派生出来的安全密钥加密字符串的方法。
        使用MD2或MD5 从口令中派生密钥，并采用DES-CBC模式加密。
        主要用于加密从一个计算机传送到另一个计算机的私人密钥，
        不能用于加密消息。
    -PKCS6：扩展证书语法标准。
        PKCS6定义了提供附加实体信息的X.509证书属性扩展的语法
        （当PKCS6第一次发布时，X.509还不支持扩展。这些扩展因此被包括在X.509中）。
    -PKCS7：密码消息语法标准。
        PKCS7在RFC 2315中定义
        参后面的P7详解
    -PKCS8：私钥信息语法标准。
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
    -PKCS9：可选属性类型。
        PKCS9定义了PKCS6扩展证书、PKCS7数字签名消息、
        PKCS8私钥信息和PKCS10证书签名请求中要用到的可选属性类型。
        已定义的证书属性包括E-mail地址、无格式姓名、内容类型、
        消息摘要、签名时间、签名副本（counter signature）、
        质询口令字和扩展证书属性。
    -PKCS10：证书请求语法标准。
        PKCS10定义了证书请求的语法。
        证书请求包含了一个唯一识别名、公钥和可选的一组属性，
        它们一起被请求证书的实体签名（证书管理协议中的PKIX证书请求消息就是一个PKCS10）。
        PKCS10 常用的后缀有：.p10 .csr
    -PKCS11：密码令牌接口标准。
        PKCS11或“Cryptoki”为拥有密码信息（如加密密钥和证书）和执行密码学函数的单用户设备
        定义了一个应用程序接口（API）。
        智能卡(UsbKey)就是实现Cryptoki的典型设备。
        注意：Cryptoki定义了密码函数接口，但并未指明设备具体如何实现这些函数。
        而且Cryptoki只说明了密码接口，并未定义对设备来说可能有用的其他接口，如访问设备的文件系统接口。
        另：ukey驱动的接口有三种：csp是微软定义的、P11是RSA定义的、SKF是国内定义的。
    -PKCS12：个人信息交换语法标准。
        PKCS12定义了个人身份信息（包括私钥、证书、各种秘密和扩展字段）的格式。
        描述了将用户公钥、私钥、证书和其他相关信息打包的语法。
        PKCS12有助于传输证书及对应的私钥，于是用户可以在不同设备间移动他们的个人身份信息。
        PKCS12 常用的后缀有： .P12 .PFX
        PKCS12定义了通常用来存储Private Keys和Public Key Certificates
        （例如前面提到的X.509）的文件格式，使用基于密码的对称密钥进行保护。
        注意上述Private Keys和Public Key Certificates是复数形式，
        这意味着PKCS 12文件实际上是一个Keystore，详见RFC7292。
    -PDCS13：椭圆曲线密码标准。
        PKCS13标准当前正在完善之中。
        它包括椭圆曲线参数的生成和验证、密钥生成和验证、数字签名和公钥加密，
        还有密钥协定，以及参数、密钥和方案标识的ASN.1语法。
    -PKCS14：伪随机数产生标准。
        PKCS14标准当前正在完善之中。
        为什么随机数生成也需要建立自己的标准呢？
        PKI中用到的许多基本的密码学函数，
        如密钥生成和Diffie-Hellman共享密钥协商，都需要使用随机数。
        然而，如果“随机数”不是随机的，而是取自一个可预测的取值集合，
        那么密码学函数就不再是绝对安全了，因为它的取值被限于一个缩小了的值域中。
        因此，安全伪随机数的生成对于PKI的安全极为关键。
    -PKCS15：密码令牌信息语法标准。
        PKCS15通过定义令牌上存储的密码对象的通用格式来增进密码令牌的互操作性。
        在实现PKCS15的设备上存储的数据对于使用该设备的所有应用程序来说都是一样的，
        尽管实际上在内部实现时可能所用的格式不同。
        PKCS15的实现扮演了翻译家的角色，它在卡的内部格式与应用程序支持的数据格式间进行转换。
        
-P1详解
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
    -key
        关于key，分别记录了private和public的详细结构，以及存储哪些内容。
        并且在附录里面推荐了ASN.1 Syntax中的存储结构。注：没有规定实际的物理文件存储结构，比如pem等。
    -加密／解密 
        详细描述了加密／解密的算法。包括，首先针对字符串，怎么转化成数字，之后，怎么根据数字进行加密。 
        这里可以看出，标准中没有对超长字符串处理的说明。而转化出的字符串的长度，全都是key的模长度k。
        在字符串转化成数字过程中，需要增加填充字符，所以，分成了两种不同算法：
        RSAES-OAEP（现有标准） RSAES-PKCS1-v1_5（兼容过去标准）。在实际加密过程中，就只有一种算法了
    -哈希
        无论在加密还是签名过程中，都会进行hash操作，
        hash操作没有自己定义，而是从附录中可以选择需要的hash方式。
    -PKCS1填充方式：
        在进行RSA运算时需要将源数据D转化为Encryption block（EB）。
        其中pkcs1padding V1.5的填充模式按照以下方式进行：
    -RCF8017内容简介：
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
        
-P7详解
    -用途：
        加密消息语法（pkcs7），是各种消息存放的格式标准
        换句话说，PKCS7为使用密码算法的数据规定了通用语法，
        这些消息包括：数据、签名数据、数字信封、签名数字信封、摘要数据和加密数据。
        PKCS7 常用的后缀是： .P7B .P7C .SPC
    -数据结构：
      签名数据：
        -struct PKCS7
            //unsigned char *asn1;  //用用于包含该结构的asn1编码
            //long length;
            //int state;          //在处理时用
            //int detached;
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
        -struct PKCS7_SIGNED
            ASN1_INTEGER                *version;           /* version 1 */
            STACK_OF(X509_ALGOR)        *md_algs;           /* md used */
            PKCS7 *contents;
            STACK_OF(X509)              *cert;              /* [ 0 ] ，可选*/
            STACK_OF(X509_CRL)          *crl;               /* [ 1 ] ，可选*/
            STACK_OF(PKCS7_SIGNER_INFO) *signer_info;
        -struct PKCS7_SIGNER_INFO
            ASN1_INTEGER 			    *version;	        /* version 1 */
            PKCS7_ISSUER_AND_SERIAL		*issuer_and_serial;
            X509_ALGOR			        *digest_alg;
            STACK_OF(X509_ATTRIBUTE)	*auth_attr;	        /* [ 0 ] */
            X509_ALGOR			        *digest_enc_alg;
            ASN1_OCTET_STRING		    *enc_digest;
            STACK_OF(X509_ATTRIBUTE)	*unauth_attr;	    /* [ 1 ] */
            EVP_PKEY			        *pkey;              /* The private key to sign with */
    -结构特点：
        当使用PKCS7进行数字签名时，
        结果包含签名证书（一列相关证书撤回列表）和已证明路径上任何其他证书。
        如果使用PKCS7加密数据，
        通常包含发行者的参考消息和证书的序列号，
        它与用于解密已加密数据的公共密钥相关。
        PKCS7也支持另外一些特征，如：
        ·递归，在一个数字信封上附上一个数字信封，还可再附上一个数字信封，如此等等。
        ·加密消息和数字签名的时间标记。
        ·签名计数和用户定义属性。
        
-P1 vs. P8
    P1规范存储的私钥是不加密的，
    还定义了公钥的格式，待签名数据和签名本身的格式，数字签名如何计算等
    PKCS8，Private-Key Information Syntax Standard，详细的描述了私钥的存储格式。
    用于加密、非加密地存储Private Certificate Keypairs（不限于RSA），详见RFC5858。

-P1 vs. P7
    P1签名:即裸签名,签名值中只有签名信息.
    p7签名:即,签名中可以带有其他的附加信息,例如签名证书信息,签名原文信息,时间戳信息等.
    验证PKCS7 signedData结构涉及验证RSA PKCS1 v1.5签名，
    但在此之前还需要执行许多重要步骤，包括解析该数据结构，
    并检查依赖于上下文的内容。
    signedData具有引导加载程序可能不需要的功能，例如带有吊销列表的证书。
    
-P7格式 -- 签名数据
    由任意类型的内容和加密的（ 0或多个签名者）消息摘要组成。
    对于一个签名者来说加了密的摘要就是他对该内容的“数字签名”
    任何类型的内容能够同时被任意数量的签名者签名。 
    此外，该语法有一个简化版本 ，其中的内容没有签名者
    -签名数据的产生过程：
        1. 对于每一个签名者，可以使用自己的摘要算法，如SM3,MD5，对原文计算出摘要值
           如果还要保护除原文（的摘要值）之外的其它信息，则应把摘要和其它信息，
           进行二次摘要，得到一个“消息摘要”。
        2. 对于每一个签名值，把消息摘要和相关信息，用自己的私钥加密
        3. 对于每一个签名者，把加密的消息摘要，和其它的签名者相关信息，放入SignerInfo结构中
           每个签名者的证书、crl，以及那些不特定于某一签名着的通用信息，也在这一步被填充进来
        4. 把消息摘要算法、SignerInfo值、内容等，放到SignedData中，得到签名数据
    -验证过程:
        用签名者的公钥，解开加密的信息摘要，然后与签名结构中的摘要对比
        公钥可以是在签名者证书中(SignerInfo结构中)，
        也可以由一个“颁发者可辨别名 和 颁发序列号”来指引，它能唯一标识一个公钥证书。
    file://p7签名结构对照图.png | file://sample.p7b
    -SignedData 结构定义:
        SignedData ::= SEQUENCE
            version Version,                #为1
            digestAlgorithms DigestAlgorithmIdentifiers,  #各个签名者使用的摘要算法的集合，可以为0个
            contentInfo ContentInfo,        #被签名内容，可以是任何一种定义了的内容类型
            certificates IMPLICIT ExtendedCertificatesAndCertificates OPTIONAL,  #证书信任链，可选
            crls IMPLICIT CertificateRevocationLists OPTIONAL,  #吊销列表，可选
            signerInfos SignerInfos         #每个签名者信息的集合
        DigestAlgorithmIdentifiers ::= SET OF DigestAlgorithmIdentifier
        ContentInfo ::= SEQUENCE 
            contentType ContentType,        #定义内容类型的权威机构分配的唯一整数串
            content EXPLICIT ANY DEFINED BY contentType OPTIONAL #通常是六种内容类型之一，也可以是自定义类型
        ContentType ::= OBJECT IDENTIFIER
        SignerInfos ::= SET OF SignerInfo
        注：版本1的SignedData vs 版本0的SignedData
            版本1中，digestAlgorithms和signerInfos域可能包含0元素， 而版本0则不能
            版本1中，可有crls 域，而版本0中则不行。
        SignerInfo ::= SEQUENCE 
            version Version,                             #版本号，为1
            issuerAndSerialNumber IssuerAndSerialNumber, #颁发者的可辨别名和颁发序列号来指定签名者的证书（因为certificates中可能有多个证书）
            digestAlgorithm DigestAlgorithmIdentifier,   #指定对内容和待鉴别属性(若存在的话)进行摘要计算的信息摘要算法
            authenticatedAttributes IMPLICIT Attributes OPTIONAL,    #经由签名者签名的属性的集合
            digestEncryptionAlgorithm DigestEncryptionAlgorithmIdentifier,  #摘要签名算法，如Sm2WithSm3
            encryptedDigest EncryptedDigest,             #用签名者私钥加密消息摘要和相关信息后的结果
            unauthenticatedAttributes IMPLICIT Attributes OPTIONAL   #不被签名者签名的属性的集合 
        EncryptedDigest ::= OCTET STRING
        注: authenticatedAttributes 是可选的，但当签名原文 contentInfo 不是data类型时，则必须包含至少下面两个属性
            content-type 属性
            message-digest 属性
    -理解
        针对 SignedData 的 version = 1 时，使用私钥（可以n个）对 contentInfo 记录的原文，先进行摘要，再加密/签名；
        私钥所对应的证书（验证用）放在 certificates 中（也要相应有n个），而摘要算法、加密/签名结果、签名算法、
        私钥所对应证书的标识等信息，则分别记录在 SignerInfos 下，各个 SignerInfo 中的 digestAlgorithm 、
        encryptedDigest 、 digestEncryptionAlgorithm 、 issuerAndSerialNumber 中，同时，还把各个 SignerInfo 用到的
        digestAlgorithm ，综合记录在 digestAlgorithms 中
    -p7b 中只存证书的情况
        其实更常见的p7b文件的结构是下面这样的：
        file://常见p7b文件结构.png | file://samples2.p7b
        可见，这里面只存了一个证书，其它的条目，能省略的省略，能为空的为空，
        也就是说，这个p7b文件唯一的目的，只是对证书提供一个外层包装，
        这有什么意义呢？ 因为 p7 结构更为通用（如其可存储签名数据、数字信封、签等），
        所以，经过 p7 包装的 x509，就变成了更为通用的 p7 结构，
        而像如 PKCS12（个人信息交换语法标准）中为了更通用，
        所以就理所当然的选用了 p7 结构作为其内部子成员结构，
        于是，x509，经过 p7 包装后，就能放在 p12 中的，
        这里也就能总结出上面问题的答案：
        为了将 x509 变为一种更通用的结构，方面传输或嵌入在其他结构(如p12)中
        另外，在 p7 的 version 为 1 时，不但可以通过 certificates 存多个证书（如证书链），
        还可将通过 crls 存放证书吊销列表，
        应用：像如oes签章组件，可以把所有的根证书，以及吊销列表，放在一个 p7b 文件中（有点类似压缩包的意思）
    -消息摘要的处理
        摘要处理的是待签名的内容或附带签名者鉴别属性的内容
        不管是哪种，初始的输入是ContentInfo的content域中的der编码的内容字节
        ————不包括 identifier字节或length字节
        摘要处理的结果，依赖于authenticatedAttributes域是否存在，
        当该域不存在时，结果就是内容的消息摘要值，
        如果存在，结果是包含authenticatedAttributes中的属性值的完全DER编码的消息摘要
        当待签名内容的content type是data且authenticatedAttributes域不存在时
        仅该数据的值(e.g.，文件的内容)进行摘要计算
 
-PKCS12详解
    -P12结构：
        struct PKCS12_st {
            ASN1_INTEGER *version;
            PKCS7 *authsafes;
            PKCS12_MAC_DATA *mac;   //可选
        };
        struct PKCS12_MAC_DATA {
            X509_SIG *dinfo;
            ASN1_OCTET_STRING *salt;
            ASN1_INTEGER *iter;         /* defaults to 1 */
        };
        struct X509_sig {
            X509_ALGOR *algor;
            ASN1_OCTET_STRING *digest;
        };
        struct X509_algor {
            ASN1_OBJECT *algorithm;
            ASN1_TYPE *parameter;
        } ;
    -p12 中的 authsafes 详解
        为pkcs7结构，用于存放的证书、crl以及私钥等各种信息。
        该结构的内容类型为data，data的实际类型为 STACK OF PKCS7
        将 STACK 中的 p7 解出来后，其内容类型为 NID_pkcs7_data 或 NID_pkcs7_encrypted，
        如果不是，则忽略该 STACK item，处理下一个item，
        NID_pkcs7_data时，data 的实际类型应为 STACK OF PKCS12_SAFEBAG
        NID_pkcs7_encrypted时，此时p7的data类型为 PKCS7_ENCRYPT *encrypted
        struct PKCS7_ENCRYPT {
            ASN1_INTEGER *version;      /* version 0 */
            PKCS7_ENC_CONTENT *enc_data;
        } ;
        struct PKCS7_ENC_CONTENT {
            ASN1_OBJECT *content_type;
            X509_ALGOR *algorithm;
            ASN1_OCTET_STRING *enc_data; /* [ 0 ] */
            const EVP_CIPHER *cipher;
        } PKCS7_ENC_CONTENT;
        此时，根据 enc_data->algorithm, 结合密码，对 enc_data->enc_data 解密，
        解密后，得到的结构也应该是 STACK OF PKCS12_SAFEBAG
        如果得不到 STACK OF PKCS12_SAFEBAG，则报错
        如果能得到，因为这是个 STACK ，所以分别取出每个 item
    -p12结构整理
        struct PKCS12_st {
            ASN1_INTEGER *version;
            PKCS7 *authsafes;
                ASN1_OBJECT *type;   # 固定为 NID_pkcs7_data
                union d {
                    ASN1_OCTET_STRING *data;  # 固定为 STACK OF PKCS7 或 NID_pkcs7_encrypted
                        PKCS7_item1
                            ASN1_OBJECT *type;   # = NID_pkcs7_data
                            union d {
                                ASN1_OCTET_STRING *data;  # 固定为 STACK OF PKCS12_SAFEBAG
                                    PKCS12_SAFEBAG_item1
                                        ASN1_OBJECT* type;   # = NID_keyBag
                                        union value{
                                            struct pkcs8_priv_key_info_st* keybag;  # pkcs8 私钥保存结构
                                        }
                                    PKCS12_SAFEBAG_item2
                                        ASN1_OBJECT* type;   # = NID_pkcs8ShroudedKeyBag
                                        union value{
                                            X509_SIG* shkeybag;    # 解密后为 pkcs8_priv_key_info_st 
                                        }
                                    PKCS12_SAFEBAG_item3
                                        ASN1_OBJECT* type;   # = NID_certBag 或 NID_crlBag 或 NID_secretBag
                                        union value{
                                            struct PKCS12_BAGS* bag; 
                                                ASN1_OBJECT* type;   
                                                union {
                                                    ASN1_OCTET_STRING* x509cert;
                                                    ASN1_OCTET_STRING* x509crl;
                                                    ASN1_OCTET_STRING* octet;       #type = NID_x509Certificate
                                                    ASN1_IA5STRING* sdsicert;
                                                    ASN1_TYPE* other;
                                                } value;
                                        }
                            }
                        PKCS7_item2
                            ASN1_OBJECT *type;   # = NID_pkcs7_encrypted ，
                            union d {
                                ASN1_OCTET_STRING *data;  # 固定为 PKCS7_ENCRYPT，解密结果固定为 STACK OF PKCS12_SAFEBAG
                            }
                };
    -p12中的 PKCS12_MAC_DATA 
        该结构用于存放pkcs12中的MAC信息（对authsafes的加盐摘要），防止他人篡改
        盐值key由 salt、iter、pass 综合得到。
        dinfo用于存放MAC值和摘要算法，
        salt和iter用于根据口令来生成对称密钥(pbe)。
    -PKCS12_SAFEBAG 结构讲解
        在使用中，用户根据证书、私钥以及crl等信息来构造PKCS12_SAFEBAG数据结构
        然后将这些结构转化为pkcs12中的pkcs7结构
        struct PKCS12_SAFEBAG {
            ASN1_OBJECT* type;  
            union {
                struct PKCS12_BAGS* bag;  
                #bag 对应 type = NID_certBag 或 NID_crlBag 或 NID_secretBag 时
                struct pkcs8_priv_key_info_st* keybag;  
                #keybag 对应 type 为 NID_keyBag 时，从 pkcs8 中解密出私钥
                X509_SIG* shkeybag;    
                #keybag 对应 type 为 NID_pkcs8ShroudedKeyBag 时，
                #shkeybag->digest 此时为加密后的数据，
                #结合 shkeybag->algor 和用户输入的密码，
                #可将之解密为 PKCS8_PRIV_KEY_INFO
                STACK_OF(PKCS12_SAFEBAG) * safes;  
                #safes 对应 type = NID_safeContentsBag 时
                ASN1_TYPE* other;
            } value;
            STACK_OF(X509_ATTRIBUTE) * attrib;
        };
        struct PKCS12_BAGS {
            ASN1_OBJECT* type;   
            union {
                ASN1_OCTET_STRING* x509cert;
                ASN1_OCTET_STRING* x509crl;
                ASN1_OCTET_STRING* octet;       //type = NID_x509Certificate
                ASN1_IA5STRING* sdsicert;
                ASN1_TYPE* other;
            } value;
        } ;
        上面这两种结构与pkcs7数据结构的相互转化可参考p12_add.c
    -国密ssl源码中解析p12的相关函数
        PKCS12_verify_mac(p12, pfx密钥, -1)
        dump_certs_keys_p12 : pkcs12.c   //该函数效果基本等同于 PKCS12_parse/parse_pk12
            STACK_OF(PKCS7) *asafes = KCS12_unpack_authsafes(p12)
            STACK_OF(PKCS12_SAFEBAG) *bags = null
            foreach(int i,sk_PKCS7_num(asafes))
                PKCS7 *p7 = sk_PKCS7_value(asafes, i);
                switch(OBJ_obj2nid(p7->type))
                    NID_pkcs7_data:
                        bags = PKCS12_unpack_p7data(p7);
                    NID_pkcs7_encrypted:
                        bags = PKCS12_unpack_p7encdata(p7, pass, passlen);
                if(bags)
                    dump_certs_pkeys_bags(out, bags, pass, passlen,
                                          options, pempass, enc)
                        for (i = 0; i < sk_PKCS12_SAFEBAG_num(bags); i++)
                            PKCS12_SAFEBAG* bag = sk_PKCS12_SAFEBAG_value(bags, i)
                            dump_certs_pkeys_bag(out, bag, pass, passlen, options, pempass, enc)
                                switch (PKCS12_SAFEBAG_get_nid(bag))
                                    case NID_keyBag:
                                        const PKCS8_PRIV_KEY_INFO *p8c = PKCS12_SAFEBAG_get0_p8inf(bag);
                                        EVP_PKEY *pkey = EVP_PKCS82PKEY(p8c)
                                        PEM_write_bio_PrivateKey(out, pkey, enc, NULL, 0, NULL, pempass);
                                    case NID_pkcs8ShroudedKeyBag: 
                                        PKCS8_PRIV_KEY_INFO *p8 = PKCS12_decrypt_skey(bag, pass, passlen)
                                        EVP_PKEY *pkey = EVP_PKCS82PKEY(p8)
                                        PEM_write_bio_PrivateKey(out, pkey, enc, NULL, 0, NULL, pempass)
                                    case NID_certBag:
                                        X509 *x509 = PKCS12_SAFEBAG_get1_cert(bag)
                                        dump_cert_text(out, x509);
                                        PEM_write_bio_X509(out, x509);
                                    case NID_safeContentsBag:
                                        const STACK_OF(PKCS12_SAFEBAG) *bags = PKCS12_SAFEBAG_get0_safes(bag)
                                        dump_certs_pkeys_bags(out, bags, pass, passlen, options, pempass, enc)
                                            。。。（递归调用）
        其它解析p12的例子：
            https://gearyyoung.gitbooks.io/openssl-program/content/PKCS12/PKCS12.html
    -PKCS12所有相关函数                                
        https://gearyyoung.gitbooks.io/openssl-program/content/PKCS12/PKCS12.html
        PKCS12_gen_mac
            参数：PKCS12 *p12, const char *pass, int passlen, 
                  unsigned char *mac, unsigned int *maclen
            生成MAC值，pass为用户口令，passlen为口令长度，mac和maclen用于存放MAC值。
            当p12中pkcs7为数据类型时，本函数有效。
        PKCS12_verify_mac
            参数：PKCS12 *p12, const char *pass, int passlen
            验证pkcs12的MAC，pass为用户口令，passlen为口令长度。
            PKCS12的MAC值存放在p12-> mac-> dinfo->digest中。
            本函数根据pass和passlen调用PKCS12_gen_mac生成一个MAC值，与p12中已有的值进行比较。
        PKCS12_create 
            成PKCS12数据结构。
        PKCS12_parse 
            解析PKCS12，得到私钥和证书等信息。
        PKCS12_key_gen_asc/PKCS12_key_gen_uni 
            生成pkcs12密钥，输入口令为ASCII码/UNICODE。
        unsigned char * PKCS12_pbe_crypt
            参数：X509_ALGOR *algor, const char *pass,int passlen, unsigned char *in, 
                  int inlen, unsigned char **data,int *datalen, int en_de
            PKCS12加解密，algor为对称算法，pass为口令，passlen为口令长度，in为输入数据，
            inlen为输入数据长度，data和datalen用于存放结果，en_de用于指明时加密还是解密。
        PKCS7 *PKCS12_pack_p7data(STACK_OF(PKCS12_SAFEBAG) *sk) 
            打包PKCS12_SAFEBAG堆栈，生成PKCS7数据结构并返回。
        PKCS12_unpack_p7data 
            上面函数的逆过程。
        PKCS12_pack_p7encdata 
            将PKCS12_SAFEBAG堆栈根据pbe算法、口令和salt加密，生成pkcs7并返回。
        PKCS12_unpack_p7encdata 
            上述过程的逆过程。
        int PKCS12_newpass
            参数：PKCS12 *p12, char *oldpass, char *newpass
            替换pkcs12的口令。
        PKCS12_setup_mac 
            设置pkcs12的MAC数据结构。
        PKCS12_set_mac 
            设置pkcs12的MAC信息。
        PKCS12_pack_authsafes 
            将pkcs7堆栈信息打包到pkcs12中。
        PKCS12_unpack_authsafes 
            上面函数的逆过程，从pkcs12中解出pkcs7堆栈，并返回。
        PKCS12_init
            参数：int mode
            生成一个pkcs12数据结构，mode的值必须为NID_pkcs7_data，即pkcs12中的pkcs7类型必须是data类型。
        PKCS12_PBE_add 
            加载各种pbe算法。
        PKCS12_PBE_keyivgen 
            根据口令生成对称密钥，并做加解密初始化。
        PKCS12_item_pack_safebag 
            将输入的数据打包为PKCS12_SAFEBAG并返回。
        PKCS12_x5092certbag 
            将证书打包为PKCS12_SAFEBAG并返回。
        PKCS12_certbag2x509 
            上述过程的逆过程。
        PKCS12_x509crl2certbag 
            将crl打包为PKCS12_SAFEBAG并返回。
        PKCS12_certbag2x509crl 
            上述过程的逆过程。
        PKCS12_item_i2d_encrypt 
            将数据结构DER编码，然后加密，数据存放在ASN1_OCTET_STRING中并返回。
        PKCS12_item_decrypt_d2i 
            上面函数的逆过程，解密输入数据，然后DER解码出数据结构，并返回。
        PKCS12_add_friendlyname_uni
            参数：PKCS12_SAFEBAG *bag,const unsigned char *name, int namelen
            给PKCS12_SAFEBAG添加一个属性，属性类型为NID_friendlyName，name为unicode编码。
        PKCS12_add_friendlyname_asc
            参数：PKCS12_SAFEBAG *bag, const char *name,int namelen
            给PKCS12_SAFEBAG添加一个属性，属性类型为NID_friendlyName，name为ASCII码。
        PKCS12_get_friendlyname 
            上面函数的逆过程，返回一个ASCII码值。
        PKCS12_add_CSPName_asc 
            给PKCS12_SAFEBAG添加一个NID_ms_csp_name属性，输入参数为ASCII码。
        PKCS12_add_localkeyid 
            给PKCS12_SAFEBAG添加一个NID_localKeyID属性。
        PKCS12_MAKE_SHKEYBAG 
            将pkcs8密钥转化为PKCS12_SAFEBAG。
        PKCS12_decrypt_skey
            参数：PKCS12_SAFEBAG *bag, const char *pass, int passlen
            返回类型：PKCS8_PRIV_KEY_INFO *
            上面函数的逆过程，从bag中提取pkcs8密钥信息。
    -源码crypto/pkcs12下各文件介绍
        p12_add.c   ：处理PKCS12_SAFEBAG，PKCS12_SAFEBAG用于存放证书和私钥相关的信息；
        p12_attr.c  ：属性处理；
        p12_crt     ：生成一个完整的pkcs12；
        p12_init.c  ：构造一个pkcs12数据结构；
        p12_kiss.c  ：解析pkcs12结构，获取证书和私钥等信息；
        p12_npas    ：设置新口令；
        p12_p8e.c   ：加密处理用户私钥(pkcs8格式)；
        p12_p8d.c   ：解密出用户私钥；
        pk12err.c   ：错误处理；
        p12_asn.c   ：pkcs12各个数据结构的DER编解码实现；
        p12_crpt.c  ：pkcs12的pbe(基于口令的加密)函数；
        p12_decr.c  ：pkcs12的pbe解密；
        p12_key.c   ：根据用户口令生成对称密钥；
        p12_mutl.c  ：pkcs12的MAC信息处理；
        p12_utl.c   ：一些通用的函数。
    -使用 openssl 工具，从p12导出私钥、证书
        openssl pkcs12 -nodes -nokeys -in 1.pfx -passin pass:证书密码 -out 1.cer
        如无需加密pem中私钥，可以添加选项-nodes；
        如无需导出私钥，可以添加选项-nokeys；