数字证书的基本架构是公开密钥PKI（Public Key Infrastructure）

数字证书有很多格式版本，
主要有X.509v1（1988）、X.509v3（1997）、X509v4（1997）等。
比较常用的版本是TUTrec.x.509V3，由国际电信联盟制定，
内容包括证书序列号、证书有效期和公开密钥等信息。

DER和PER编码：
    ASN.1有一套关联的编码规则，这些编码规则用来规定如何用二进制来表示数据结构，DER是其中一种，DER使用TLV结构存储数据。
    DER编码的内容是二进制的，不适合与邮件传输（早期Email不能发送附件），因此使用PEM把二进制内容转换成ASCII码，
    PEM实际上就是把DER编码的文件的二进制内容用base64编码一下，
    然后加上-----BEGIN label-----这样的头和-----END label-----这样的尾，中间则是DER文件的Base64编码，
    label用来区分内容到底是什么类型，和PEM相关的RFC有很多，与本文内容相关的则是RFC7468，这里面规定了很多label，
    不过要注意不是所有label都会有对应的RFC或Specification，这些label只是一种约定俗成。
    使用openssl命令可以完成pem和der之间的转换，一个私钥的pem结构如下：
    -----BEGIN RSA PRIVATE KEY-----
    BASE64Encoded
    -----END RSA PRIVATE KEY-----

X509和PKCS
    X.509是一个Public Key Certificates的格式标准,而所谓Public Key Certificates又被称为Digital Certificate 或 Identity Certificate。
    一个X.509 Certificate包含一个Public Key和一个身份信息，它要么是被CA签发的要么是自签发的。
    事实上X.509 Certificate这个名词通常指代的是IETF的PKIX Certificate和CRL Profile，见RFC5280。
    所以当你看到PKIX Certificate字样的时候可以认为就是X.509 Certificate。
    PKCS是Public Key密码学标准（PKCS stands for "Public Key Cryptography Standards"）
    此外Public-Key Cryptography虽然名字看上去只涉及Public Key，实际上也涉及Priviate Key，因此PKCS也涉及Private Key。

几种常见的PEM label
CERTIFICATE            :  X.509 Certificate类型            //RFC7468
PUBLIC KEY             :  X.509 Certificate Subject Public Key Info   //RFC7468
RSA PRIVATE KEY        :  PKCS 1 Private Key  //没有RFC或权威Specification，该格式有时候被称为traditional format、SSLeay format
RSA PUBLIC KEY         :  PKCS 1 Public Key   //同上没有RFC或权威Specification
PRIVATE KEY            :  PKCS 8 Unencrypted Private Key   //RFC7468
ENCRYPTED PRIVATE KEY  :  PKCS 8 Encrypted Private Key     //RFC7468

常见的证书文件后缀(.pem .der .cer .crt .pfx .p12 .jks)



参考资料：
https://www.jianshu.com/p/bc32cbfe49e7

