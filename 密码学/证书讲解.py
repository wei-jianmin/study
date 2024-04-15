<catalog s0/s2/s4 catalog_line_prefix=->
-证书结构    
  #在RFC5280中定义了X.509公钥数字证书和证书吊销列表的内容和格式        
  -签名原文
    版本号
    序列号
    签名算法        //使用公钥验证签名时，使用的算法
    颁发者信息
      E  : email
      CN : common name
      OU : organization unit
      O  : organization
      L  : local name
      S  : state or city name
      C  : country name
    有效期
    使用者信息       //使用者信息有时称为主题信息
      E  : email
      CN : common name
      OU : organization unit
      O  : organization
      L  : local name
      S  : state or city name
      C  : country name
    使用者公钥信息
    颁发者唯一识别号[可选]
    使用者唯一识别号[可选]
    其它扩展项[可选]
  -签名算法        //ca机构对原文签名的算法
  -签名值
  -其它扩展项举例：
    颁发机构信息访问
    证书策略
    CRL(吊销列表)分发点
    使用者备用名称
    增强型密钥用法
-网站使用的SSL证书类型：
    DV SSL证书 : 域名型证书     ：申请价格100-1000元左右
    OV SSL证书 ：企业型证书     ：申请价格300-2000元左右
    EV SSL证书 ：企业增强型证书 ：申请价格一千至两万元左右
    三者的区别在于审核等级不一样，
    域名型证书一般只验证网站的真实性，
    企业型证书还验证企业身份
    企业增强型证书则审核更加严格，打开这样的网站，浏览器地址栏会变成绿色
-查看电脑中安装的证书
    命令行： certmgr.msc
    ie浏览器： ie选项/内容/证书
-免费证书申请网站  如freessl.cn
  关于CSR（签名请求）生成的说明
    使用命令：openssl req -new -nodes -sha256 -newkey rsa:2048
                      -keyout myprivate.key -out mydomain.csr
    按照命令提示填写完C、S、L、O、OU、CN、E等信息后，
    便会在当前目录下生成myprivate.key和mydomain.csr两个文件，
    key文件里存的是私钥，mydomain.csr文件里存的是个人信息和公钥
    网上申请证书时，要用到mydomain.csr这个文件
  关于域名验证的说明
    CA需要对您是否拥有该域名进行验证，这样才能给您颁发证书。
    这里有多种验证方式，您可以采用对您较为方便的方式进行。
    在进行下一步的同时，你将同意Lets Encrypt service agreement 或 TrustAsia。
    如果您的网站有防火墙，请对 66.133.109.36 开放。
    如果您收到 504 网关超时，无法连接等其它错误，请刷新页面重试；
    如果您有自己的CSR文件，可上传CSR文件之后进行手动验证。
    文件验证（HTTP）
    CA 将通过访问特定 URL 地址来验证您是否有该域名的所有权。
    因此，您需要下载给定的验证文件，并上传到您的服务器。
    DNS 验证
    CA 将通过查询 DNS 的 TXT 记录来确定您对该域名的所有权。
    您只需要在域名管理平台将生成的 TXT 记录名与记录值添加到该域名下，等待大约 1 分钟即可验证成功。
    FreeSSL借助 Trustasia 和 Let’s Encrypt 提供的 API，以及使用 Web Cryptography API，
    完全使用浏览器生成证书，期间不存在数据传输，如果浏览器不支持 Web Cryptography API，
    那么我们会从后端服务器生成证书，所以在此强烈建议您使用支持 Web Cryptography API 的浏览器。
-x509 和 x509v3
    我们通常说的证书都是指 X.509 数字证书，
    如果不加特别说明，都是指 X.509 v3 版本的。 
    简单来说，v3 版本就是添加了扩展字段的证书。
-命令行使用openssl工具生成证书
    -生成RSA密钥
        默认情况下，openssl 输出格式为 PKCS#1-PEM
        生成RSA私钥(无加密)  
            openssl genrsa -out rsa_private.key 2048
        生成RSA公钥  
            openssl rsa -in rsa_private.key -pubout -out rsa_public.key
        生成RSA私钥(使用aes256加密) 
            openssl genrsa -aes256 -passout pass:111111 -out rsa_aes_private.key 2048
            passout 代替shell 进行密码输入，否则会提示输入密码；
        生成RSA公钥（使用加密的RSA私钥）
            openssl rsa -in rsa_aes_private.key -passin pass:111111 -pubout -out rsa_public.key
        加密私钥与非加密私钥转换
            私钥转非加密
                openssl rsa -in rsa_aes_private.key -passin pass:111111 -out rsa_private.key
            私钥转加密
                openssl rsa -in rsa_private.key -aes256 -passout pass:111111 -out rsa_aes_private.key
            私钥PKCS 1转PKCS 8
                openssl pkcs8 -topk8 -in rsa_private.key -passout pass:111111 -out pkcs8_private.key
                -passout指定了密码，输出的pkcs8格式密钥为加密形式，pkcs8默认采用des3 加密算法
                使用-nocrypt参数可以输出无加密的pkcs8密钥
    -生成自签名证书
        生成RSA私钥和自签名证书
            openssl req -newkey rsa:2048 -keyout rsa_private.key 
                        -nodes -x509 -days 365 -out cert.crt
            req是证书请求的子命令
            -newkey rsa:2048 -keyout private_key.pem 表示生成私钥(PKCS8格式)
            -nodes 表示私钥不加密，若不带参数将提示输入密码
            -x509表示输出证书，
            -days365 为有效期，
            此后根据提示输入证书拥有者信息；
        使用已有RSA私钥生成自签名证书
            openssl req -new -x509 -days 365 -key rsa_private.key -out cert.crt
            -new 指生成证书请求，加上-x509 表示直接输出证书，
            -key 指定私钥文件
    -生成签名证书
        生成签名请求文件(.csr)
            使用私钥生成 
                openssl genrsa -aes256 -passout pass:111111 -out server.key 2048
                openssl req -new -key server.key -out server.csr 
            同时生成私钥和签名请求文件
                openssl req -new -nodes -sha256 -newkey rsa:2048
                            -keyout myprivate.key -out mydomain.csr
        使用根证书+根证书密钥，对请求(.csr)签名生成x509证书
            openssl x509 -req -days 3650 -in server.csr -CA ca.crt -CAkey ca.key 
                         [-passin pass:111111] -CAcreateserial -out server.crt
-命令行生成证书
    file://生成证书/openssl生成证书.txt
    file://生成证书/利用 gmssl 生成国密证书.txt
    file://生成证书/用easy-rsa 3制作证书.txt
-不同证书格式Der 、Cer 、Pfx 、Pem区别
    .DER：用二进制DER编码的证书；
    .PEM：用ASCLL(BASE64)编码的证书；
          这些文件包含前缀为“-BEGIN ...”行的ASCII（Base64）装甲数据
    .CER：存放公钥，没有私钥； 编码格式可能是der也可能是pem
    .PFX：存放公钥和私钥  
    PEM格式
        PEM格式通常用于数字证书认证机构(CA)，
        扩展名为.pem, .crt, .cer, and .key。
        内容为Base64编码的ASCII码文件，
        有类似"-----BEGIN CERTIFICATE-----" 
        和 "-----END CERTIFICATE-----"的头尾标记。
        PEM是一种格式化编码几乎任何一种二进制/ DER数据的方式，其方式更为方便
        更确切地说，PEM将一些数据编码为：(不限于)PKCS1或PKCS8密钥或证书，CSR等
    DER格式
        DER格式与PEM不同之处在于其使用二进制
        而不是Base64编码的ASCII。
        扩展名为.der，但也经常使用.cer用作扩展名，
        所有类型的认证证书和私钥都可以存储为DER格式。
        Java是其典型使用平台。
    使用openssl,可以在der、pen、pfx证书格式之间互转
        PEM to DER
            openssl x509 -outform der -in certificate.pem -out certificate.der
        DER to PEM
            openssl x509 -inform der -in certificate.cer -out certificate.pem
        PEM to PFX
            openssl pkcs12 -export -out certificate.pfx -inkey privateKey.key -in certificate.crt -certfile CACert.crt
        PFX to PEM
            openssl pkcs12 -in certificate.pfx -out certificate.cer -nodes  
-openssl命令简介：
  openssl支持几十个子命令，这里只列出了常用的几个
  每个子命令下的支持参数也只是部分列出
  openssl help : 列出openssl支持的子命令
  openssl 子命令 -help : 列出子命令支持的参数及相关说明
  openssl 部分子命令介绍：
    -asn1parse: 用于解释用ANS.1语法书写的语句
        -inform arg   
            指定输入文件的格式 ： DER/PEM
        -in arg       
            输入文件
        -out arg      
            输出文件格式，始终是DER
        -noout arg    
            不产生任何输出
        -offset arg   
            文件偏移量
        -length arg   
            文件中节的长度
        -dump         
            未知格式的数据以16进制输出
        -i            
            indent entries
        -dlimit arg   
            dump the first arg bytes of unknown data in hex form
        -oid file     
            file of extra oid definitions
        -strparse offset
            a series of these can be used to 'dig' into multiple
            ASN1 blob wrappings
        -genstr str   
            string to generate ASN1 structure from
        -genconf file 
            file to generate ASN1 structure from
      例：
        openssl asn1parse -in ec_pubkey.pem
        openssl asn1parse -inform DER -in file.der
    -ca: ca用于CA的管理 
        -selfsign
            使用对证书请求进行签名的密钥对来签发证书。
            即"自签名"，这种情况发生在生成证书的客户端、
            签发证书的CA都是同一台机器(也是我们大多数实验中的情况)，
            我们可以使用同一个密钥对来进行"自签名"
        -in file
            需要进行处理的PEM格式的证书
        -out file
            处理结束后输出的证书文件
        -cert file
            用于签发的根CA证书
        -days arg 
            指定签发的证书的有效时间
        -keyfile arg   
            CA的私钥证书文件
        -keyform arg
            CA的根私钥证书文件格式:
            PEM
            ENGINE 
        -key arg   
            CA的根私钥证书文件的解密密码(如果加密了的话)
        -config file    
            配置文件
                example1: 利用CA证书签署请求证书
                openssl ca -in server.csr -out server.crt -cert ca.crt -keyfile ca.key  
    -req: X.509证书签发请求(CSR)管理
        openssl req [options] <infile >outfile
        -inform arg
          输入文件格式
            DER
            PEM
        -nodes
          不使用des加密
        -outform arg   
          输出文件格式
            DER
            PEM
        -in arg
            待处理文件
        -out arg
            待输出文件
        -passin        
            用于签名待生成的请求证书的私钥文件的解密密码
        -key file
            用于签名待生成的请求证书的私钥文件
        -keyform arg  
            DER
            NET
            PEM
        -new
            新的请求
        -x509          
            输出一个X509格式的证书 
        -days
            X509证书的有效时间  
        -newkey rsa:bits 
            生成一个bits长度的RSA私钥文件，用于签发  
        -[digest] HASH算法
            md5
            sha1
            sha256
            md2
            mdc2
            md4
        -config file   
            指定openssl配置文件
        -text: 
            text显示格式
      例：
        example1: 利用CA的RSA密钥创建一个自签署的CA证书(X.509结构) 
            openssl req -new -x509 -days 3650 -key server.key -out ca.crt 
        example2: 用server.key生成证书签署请求CSR(这个CSR用于之外发送待CA中心等待签发)
            openssl req -new -key server.key -out server.csr
        example3: 查看CSR的细节
            openssl req -noout -text -in server.csr
    -genrsa: 生成RSA参数
        openssl genrsa [args] [numbits]
        [args]
          对生成的私钥文件是否要使用加密算法进行对称加密:
            -des: CBC模式的DES加密
            -des3: CBC模式的DES加密
            -aes128: CBC模式的AES128加密
            -aes192: CBC模式的AES192加密
            -aes256: CBC模式的AES256加密
          -passout arg: 
            arg为对称加密(des、des、aes)的密码(使用这个参数就省去了console交互提示输入密码的环节)
          -out file: 
            输出证书私钥文件
        [numbits]: 
            密钥长度
      例：
        example: 生成一个1024位的RSA私钥，并用DES加密(密码为1111)，保存为server.key文件
            openssl genrsa -out server.key -passout pass:1111 -des3 1024 
    -rsa: RSA数据管理
        openssl rsa [options] <infile >outfile
        -inform arg
          输入密钥文件格式:
            DER(ASN1)
            NET
            PEM(base64编码格式)
        -outform arg
          输出密钥文件格式
            DER
            NET
            PEM
        -in arg
            待处理密钥文件 
        -passin arg
            输入这个加密密钥文件的解密密钥(如果在生成这个密钥文件的时候，选择了加密算法了的话)
        -out arg
            待输出密钥文件
        -passout arg  
            如果希望输出的密钥文件继续使用加密算法的话则指定密码 
        -des
            CBC模式的DES加密
        -des3
            CBC模式的DES加密
        -aes128
            CBC模式的AES128加密
        -aes192
            CBC模式的AES192加密
        -aes256
            CBC模式的AES256加密
        -text
            以text形式打印密钥key数据 
        -noout
            不打印密钥key数据 
        -pubin
            检查待处理文件是否为公钥文件
        -pubout
            输出公钥文件
      例：
        example1: 对私钥文件进行解密
            openssl rsa -in server.key -passin pass:111 -out server_nopass.key
        example:2: 利用私钥文件生成对应的公钥文件
            openssl rsa -in server.key -passin pass:111 -pubout -out server_public.key
    -x509: 证书生成、显示、转换
        本指令是一个功能很丰富的证书处理工具。可以用来显示证书的内容，转换其格式，给CSR签名等X.509证书的管理工作
        -inform arg
            待处理X509证书文件格式
              DER
              NET
              PEM
        -outform arg   
            待输出X509证书文件格式
              DER
              NET
              PEM
        -in arg 
            待处理X509证书文件
        -out arg       
            待输出X509证书文件
        -req            
            表明输入文件是一个"请求签发证书文件(CSR,cert sign request)"，等待进行签发 
        -days arg       
            表明将要签发的证书的有效时间 
        -CA arg 
            指定用于签发请求证书的根CA证书 
        -CAform arg     
            根CA证书格式(默认是PEM) 
        -CAkey arg      
            指定用于签发请求证书的CA私钥证书文件，
            如果这个option没有参数输入，那么缺省认为私有密钥在CA证书文件里有
        -CAkeyform arg  
            指定根CA私钥证书文件格式(默认为PEM格式)
        -CAserial arg   
            指定序列号文件(serial number file)
        -CAcreateserial 
            如果序列号文件(serial number file)没有指定，则自动创建它 
      例：
        example1: 转换DER证书为PEM格式
            openssl x509 -in cert.cer -inform DER -outform PEM -out cert.pem
        example2: 使用根CA证书对"请求签发证书"进行签发，生成x509格式证书
            openssl x509 -req -days 3650 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt
        example3: 打印出证书的内容
            openssl x509 -in server.crt -noout -text 
    -crl: crl是用于管理CRL列表 
        -inform arg
            输入文件的格式
              DER(DER编码的CRL对象)
              PEM(默认的格式)(base64编码的CRL对象)
        -outform arg
            指定文件的输出格式 
              DER(DER编码的CRL对象)
              PEM(默认的格式)(base64编码的CRL对象)
        -text: 
            以文本格式来打印CRL信息值。
        -in filename
            指定的输入文件名。默认为标准输入。
        -out filename
            指定的输出文件名。默认为标准输出。
        -hash
            输出颁发者信息值的哈希值。
            这一项可用于在文件中根据颁发者信息值的哈希值来查询CRL对象。
        -fingerprint
            打印CRL对象的标识。
        -issuer
            输出颁发者的信息值。
        -lastupdate
            输出上一次更新的时间。
        -nextupdate
            打印出下一次更新的时间。 
        -CAfile file
            指定CA文件，用来验证该CRL对象是否合法。 
        -verify
            是否验证证书。
      例
        example1: 输出CRL文件，包括(颁发者信息HASH值、上一次更新的时间、下一次更新的时间)
            openssl crl -in crl.crl -text -issuer -hash -lastupdate –nextupdate 
        example2: 将PEM格式的CRL文件转换为DER格式
            openssl crl -in crl.pem -outform DER -out crl.der  
    -crl2pkcs7: 用于CRL和PKCS7之间的转换 
        openssl crl2pkcs7 [options] <infile >outfile
        转换pem到spc
        openssl crl2pkcs7 -nocrl -certfile venus.pem -outform DER -out venus.spc
        https://www.openssl.org/docs/apps/crl2pkcs7.html
    -pkcs12: PKCS12数据的管理
        pkcs12文件工具，能生成和分析pkcs12文件。
        PKCS12文件可以被用于多个项目，例如包含Netscape、 MSIE 和 MS Outlook
        openssl pkcs12 [options] 
        http://blog.csdn.net/as3luyuan123/article/details/16105475
        https://www.openssl.org/docs/apps/pkcs12.html
    -pkcs7: PCKS7数据的管理 
        用于处理DER或者PEM格式的pkcs7文件
        openssl pkcs7 [options] <infile >outfile
        http://blog.csdn.net/as3luyuan123/article/details/16105407
        https://www.openssl.org/docs/apps/pkcs7.html
    -dgst: dgst用于计算消息摘要 
        openssl dgst [args]
          -hex           
            以16进制形式输出摘要
          -binary        
            以二进制形式输出摘要
          -sign file    
            以私钥文件对生成的摘要进行签名
          -verify file    
            使用公钥文件对私钥签名过的摘要文件进行验证 
          -prverify file  
            以私钥文件对公钥签名过的摘要文件进行验证
            verify a signature using private key in file
          加密处理
            -md5: MD5 
            -md4: MD4         
            -sha1: SHA1 
            -ripemd160
      例：
        example1: 用SHA1算法计算文件file.txt的哈西值，输出到stdout
            openssl dgst -sha1 file.txt
        example2: 用dss1算法验证file.txt的数字签名dsasign.bin，验证的private key为DSA算法产生的文件dsakey.pem
            openssl dgst -dss1 -prverify dsakey.pem -signature dsasign.bin file.txt
    -sha1: 用于进行RSA处理
-openssl配置文件
    openssl配置文件控制openssl命令的行为
    如果不明显指定配置文件，则使用默认的配置文件
    默认的配置文件位于openssl安装目录/bin/cnf/openssl.cnf
    对配置文件的介绍，可以参考 
    https://www.cnblogs.com/f-ck-need-u/p/6091027.html#auto_id_4 
    https://my.oschina.net/acmfly/blog/72208
-SSL证书中的“密钥用法”和“增强密钥用法”
    https://zhuanlan.zhihu.com/p/642818233
    密钥用法
        这个字段用于说明这张证书是干什么用的
        RSA算法SSL证书应该是“Digital Signature, Key Encipherment （数字签名，加密）”
        ECC算法SSL证书则是“Digital Signature （数字签名）
        这两种算法在https加密中的作用是不一样的。
    增强密钥用法
        不是关键字段，但是必须有的字段，这个字段进一步说明这张证书的用途，
        SSL证书的EKU字段值为
        “服务器身份验证 （1.3.6.1.5.5.7.3.1），
        客户端身份验证 （1.3.6.1.5.5.7.3.2）”，
        意思是这张SSL证书既用于服务器的身份认证，也
        可以用于同其他服务器通信时的一个客户端的身份认证，
        一般用于服务器与服务器之间的加密通信。
        SSL证书至少必须有“服务器身份验证”这个EKU，
        用于“向远程计算机证明服务器的身份”，
        没有这一项就无法实现同客户端证书的双向认证
-源码中的相关数据结构：
    #证书类型 -- 看起来像是与增强密钥用法挂钩的
    static BIT_STRING_BITNAME ns_cert_type_table[] = {
        {0, "SSL Client", "client"},
        {1, "SSL Server", "server"},  X509_TRUST_SSL_SERVER    NID_server_auth
        {2, "S/MIME", "email"},
        {3, "Object Signing", "objsign"},
        {4, "Unused", "reserved"},
        {5, "SSL CA", "sslCA"},
        {6, "S/MIME CA", "emailCA"},
        {7, "Object Signing CA", "objCA"},
        {-1, NULL, NULL}
    };
    #密钥用法
    static BIT_STRING_BITNAME key_usage_type_table[] = {
        {0, "Digital Signature", "digitalSignature"},   #数字签名
        {1, "Non Repudiation", "nonRepudiation"},       #认可签名，Non Repudiation：不可否认性
        {2, "Key Encipherment", "keyEncipherment"},     #密钥加密
        {3, "Data Encipherment", "dataEncipherment"},   #数据加密
        {4, "Key Agreement", "keyAgreement"},           #密钥协商
        {5, "Certificate Sign", "keyCertSign"},         #证书签名
        {6, "CRL Sign", "cRLSign"},                     #CRL 签名
        {7, "Encipher Only", "encipherOnly"},           #仅仅加密
        {8, "Decipher Only", "decipherOnly"},           #仅仅解密
        {-1, NULL, NULL}
    };
    #结构
    typedef struct BIT_STRING_BITNAME_st {
        int bitnum;
        const char *lname;
        const char *sname;
    } BIT_STRING_BITNAME;
https://blog.csdn.net/huangjinjin520/article/details/100035003   
-密钥用法
    用法          lname                   sname
    数字签名      Digital Signature       digitalSignature
    认可签名      Non Repudiation         nonRepudiation
    密钥加密      key Encipherment        keyEncipherment
    数据加密      Data Encipherment       dataEncipherment
    密钥协商      key Agreement           keyAgreement
    证书签名      Key CertSign            keyCertSign
    CRL 签名      Crl Sign                cRLSign
    仅仅加密      Encipher Only           encipherOnly
    仅仅解密      Decipher Only           decipherOnly
    例： Add_X509V3_extensions(newcert, cacert, NID_key_usage, "Digital Signature, Key Encipherment")
-增强密钥用法：         
    Microsoft 信任列表签名      (1.3.6.1.4.1.311.10.3.1)          Microsoft Trust List Signing,             msCTLSign              Microsoft Trust List Signing
    合格的部属                  (1.3.6.1.4.1.311.10.3.10)        
    密钥恢复                    (1.3.6.1.4.1.311.10.3.11)        
    生存时间签名                (1.3.6.1.4.1.311.10.3.13)        
    Microsoft 时间戳            (1.3.6.1.4.1.311.10.3.2)         
    加密文件系统                (1.3.6.1.4.1.311.10.3.4)          Microsoft Encrypted File System,          msEFS                  Microsoft Encrypted File System
    文件恢复                    (1.3.6.1.4.1.311.10.3.4.1)                
    Windows 硬件驱动程序验证    (1.3.6.1.4.1.311.10.3.5)  
    Windows 系统组件验证        (1.3.6.1.4.1.311.10.3.6)  
    OEM Windows 系统组件验证    (1.3.6.1.4.1.311.10.3.7)  
    内嵌 Windows 系统组件验证   (1.3.6.1.4.1.311.10.3.8) 
    根列表签名者                (1.3.6.1.4.1.311.10.3.9) 
    文档签名                    (1.3.6.1.4.1.311.10.3.12)
    数字权利                    (1.3.6.1.4.1.311.10.5.1) 
    许可证服务器确认            (1.3.6.1.4.1.311.10.6.2) 
    密钥数据包许可证            (1.3.6.1.4.1.311.10.6.1) 
    证书申请代理                (1.3.6.1.4.1.311.20.2.1) 
    智能卡登录                  (1.3.6.1.4.1.311.20.2.2)          Microsoft Smartcardlogin,
    私钥存档                    (1.3.6.1.4.1.311.21.5)           
    密钥恢复代理                (1.3.6.1.4.1.311.21.6)           
    目录服务电子邮件复制        (1.3.6.1.4.1.311.21.19)      
    服务器身份验证              (1.3.6.1.5.5.7.3.1)               TLS Web Server Authentication,             serverAuth             SSL/TLS Web Server Authentication.
    客户端身份验证              (1.3.6.1.5.5.7.3.2)               TLS Web Client Authentication,             clientAuth             SSL/TLS Web Client Authentication.
    安全电子邮件                (1.3.6.1.5.5.7.3.4)               E-mail Protection,                         emailProtection        E-mail Protection (S/MIME).
    代码签名                    (1.3.6.1.5.5.7.3.3)               Code Signing,                              codeSigning            Code signing.
    IP 安全终端系统             (1.3.6.1.5.5.7.3.5)               IPSec End System,
    IP 安全隧道终止             (1.3.6.1.5.5.7.3.6)               IPSec Tunnel,
    IP 安全用户                 (1.3.6.1.5.5.7.3.7)               IPSec User,
    时间戳                      (1.3.6.1.5.5.7.3.8)               Time Stamping,                             timeStamping           Trusted Timestamping
    IP 安全 IKE 中级            (1.3.6.1.5.5.8.2.2)               
    所有颁发的策略              (2.5.29.32.0)                     X509v3 Any Policy
-证书使用场合及其相应的 “密钥用法&增加密钥用法” ：
    (1)根证书
        密钥用法：认可签名，证书签名，CRL签名
        keyUsage=nonRepudiation, keyCertSign,cRLSign
    (2)代码签名
        密钥用法：数字签名
        增强密钥用法：代码签名
        keyUsage=digitalSignature
        extendedKeyUsage=codeSigning
    (3)计算机
        密钥用法：数字签名，密钥协商
        增强密钥用法：服务器验证，客户端验证
        keyUsage=digitalSignature,keyAgreement
        extendedKeyUsage=serverAuth,clientAuth
    (4)WEB服务器
        密钥用法：数字签名，认可签名，密钥加密，数据加密，密钥协商
        增强密钥用法：服务器验证
        keyUsage=digitalSignature,nonRepudiation,keyEncipherment,dataEncipherment,keyAgreement
        extendedKeyUsage=serverAuth
    (5)客户端
        密钥用法：数字签名，认可签名，密钥加密，数据加密
        增强密钥用法：客户端验证
        keyUsage=digitalSignature,nonRepudiation,keyEncipherment,dataEncipherment
        extendedKeyUsage=clientAuth
    (6)信任列表签名
        密钥用法：数字签名
        增强密钥用法：信任列表签名
        keyUsage=digitalSignature
        extendedKeyUsage=msCTLSign
    (7)时间戳
        密钥用法：数字签名，认可签名，密钥加密，数据加密
        增强密钥用法：时间戳
        keyUsage=digitalSignature,nonRepudiation,keyEncipherment,dataEncipherment
        extendedKeyUsage=timeStamping
    (8)IPSEC
        密钥用法：数字签名，认可签名，密钥加密，数据加密
        增强密钥用法：IP安全IKE中级
        keyUsage=digitalSignature,nonRepudiation,keyEncipherment,dataEncipherment
        extendedKeyUsage=1.3.6.1.5.5.8.2.2
    (9)安全Email
        密钥用法：数字签名，认可签名，密钥加密，数据加密
        增强密钥用法：安全电子邮件
        keyUsage=digitalSignature,nonRepudiation,keyEncipherment,dataEncipherment
        extendedKeyUsage=emailProtection
    (10)智能卡登陆
        密钥用法：数字签名，密钥协商，仅仅解密
        增强密钥用法：密钥恢复，加密文件系统，智能卡登陆
        keyUsage=digitalSignature,keyAgreement,decipherOnly
        extendedKeyUsage=1.3.6.1.4.1.311.10.3.11,msEFS,1.3.6.1.4.1.311.20.2.2        
        Digital Signature, Key Encipherment, Data Encipherment (b0)        
        客户端身份验证 (1.3.6.1.5.5.7.3.2)
        
-国密ssl证书的使用说明
    https://blog.csdn.net/qingzhuyuxian/article/details/120904372
    -什么是双证书？
        《GMT0024-2014 SSL VPN 技术规范》5.2.2章节里说明了服务端双证书的性质和作用
        -5.2.2 服务端密钥
            服务端密钥为非对称密码算法的密钥对，包括签名密钥对和加密密钥对，
            其中签名密钥对有VPN自身密码模块产生，
            加密密钥对应通过CA认证中心向KMC申请，用于握手过程中服务端身份鉴别和预主密钥的协商。
            这里需要解释说明一下，KMC: key management center 是密钥管理中心的简称。
            其实不单单是服务端用到了双证书，在客户端的秘钥也是采用双证书体系，如下 5.2.3
        -5.2.3 客户端密钥
            客户端密钥为非对称密码算法的密钥对，包括签名密钥对和加密密钥对，
            其中签名密钥对由VPN自身密码模块产生，
            加密密钥对应通过CA认证中心向KMC申请，用于握手过程中客户端身份鉴别和预主密钥的协商。
        我们在之前的文章《关于国密https的那些事》里面就介绍了
        file://OpenSSL学习/SSL协议详解---看这一篇就够了.py@关于国密https的那些事
        使用"ECC-SM4-SM3"套件握手的秘钥交换过程中有服务端的双证书参与。
        而在另一个加密套件"ECDHE-SM4-SM3"中就需要客户端双证书的参与，
        详细见《GMT0009-2012SM2 密码算法使用规范》的9.6密钥协商版块。
        file://sm2规范0003、0004、0009学习记录.py
    -密钥用法
        在《GMT 0015-2012 基于SM2密码算法的数字证书格式》协议5.2.4.2.2中
        就说明了证书的各种密钥用法，如下图：
        file://imgs/国密证书密钥用法.png
        《GM T 0015-2012公钥密码基础设施应用技术体系基于SM2算法的证书认证系统证书格式标准.pdf》
        中，第 11 节，对各种用途的证书，每一项的取值做了详细描述
            终端实体签名证书
                file://imgs/签名证书的密钥用法规定.png
            终端实体加密证书
                file://imgs/加密证书的密钥用法规定.png
        
    -双向认证 vs 双证书
        这两个是完全不同的概念
        双向认证是指客户端对服务端证书进行认证的同时，服务端对客户端的身份也进行认证
        通常很多情况下浏览器会对服务端证书是否可信进行验证。
        而服务端对客户端的身份是不做限制的，如我们的常用的购物网站，视频网站等
        但是有些特殊的场景（如vpn），为了安全性，服务端会鉴别客户端的身份，
        这时候就需要在双方握手的过程中，客户端需要将证明自己身份的证书传递给服务端。
        
-详解国密SSL ECC_SM4_SM3套件
    https://blog.csdn.net/mogoweb/article/details/105190337
    -协议版本
        TLS协议定义有三个版本号，为0x0301、0x0302、0x0303，分别对应TLS 1.0、1.1、1.2。
        国密SSL估计是担心与未来的TLS版本号冲突，选择了0x0101。
        国密SSL协议规范是TLS 1.1和TLS 1.2的混合体，
        大部分情况下参考TLS 1.1就可以了，少数地方又参考了TLS 1.2
    -加密算法
        在ECC_SM4_SM3套件中，非对称加密算法为SM2，对称加密算法为SM4，摘要算法为SM3。
        注意，PRF算法和TLS 1.2类似，而不是像TLS 1.1那样
    -Certificate报文
        国密规范规定发送证书时需要发送两个证书：签名证书和加密证书（双证书体系）
        与标准TLS报文格式一样，但至少要包含两个证书，签名证书在前，加密证书在后。
        通常情况下，服务器会部署一张证书，用于签名和加密，这就是所谓的单证书:
        签名时，
            服务器使用自己的私钥，对信息的摘要进行加密（签名），
            客户端使用服务器的公钥（包含在证书中）进行解密，对比该摘要是否正确，
            若正确，则客户端就确定了服务器的身份，即验签成功。
        加密时，服务器和客户端协商出会话密钥（一般为对称密钥），
            会话密钥的产生根据密钥协商算法的不同，过程有所不同，
            但都会用到证书的公钥和私钥，也就是说证书也用在加密场景中。

           
X509结构：
    struct x509 {
        X509_CINF cert_info;
        X509_ALGOR sig_alg;
        ASN1_BIT_STRING signature;
        int references;
        CRYPTO_EX_DATA ex_data;
        /* These contain copies of various extension values */
        long ex_pathlen;
        long ex_pcpathlen;
        uint32_t ex_flags;
        uint32_t ex_kusage;
        uint32_t ex_xkusage;
        uint32_t ex_nscert;
        ASN1_OCTET_STRING *skid;
        AUTHORITY_KEYID *akid;
        X509_POLICY_CACHE *policy_cache;
        STACK_OF(DIST_POINT) *crldp;
        STACK_OF(GENERAL_NAME) *altname;
        NAME_CONSTRAINTS *nc;
    #ifndef OPENSSL_NO_RFC3779
        STACK_OF(IPAddressFamily) *rfc3779_addr;
        struct ASIdentifiers_st *rfc3779_asid;
    # endif
        unsigned char sha1_hash[32 /*SHA_DIGEST_LENGTH*/];
        X509_CERT_AUX *aux;
        CRYPTO_RWLOCK *lock;
    };
    struct x509_cinf_st {
        ASN1_INTEGER *version;      /* [ 0 ] default of v1 */
        ASN1_INTEGER serialNumber;
        X509_ALGOR signature;
        X509_NAME *issuer;
        X509_VAL validity;
        X509_NAME *subject;
        X509_PUBKEY *key;
        ASN1_BIT_STRING *issuerUID; /* [ 1 ] optional in v2 */
        ASN1_BIT_STRING *subjectUID; /* [ 2 ] optional in v2 */
        STACK_OF(X509_EXTENSION) *extensions; /* [ 3 ] optional in v3 */
        ASN1_ENCODING enc;
    };