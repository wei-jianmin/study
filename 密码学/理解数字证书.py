����֤��Ļ����ܹ��ǹ�����ԿPKI��Public Key Infrastructure��

����֤���кܶ��ʽ�汾��
��Ҫ��X.509v1��1988����X.509v3��1997����X509v4��1997���ȡ�
�Ƚϳ��õİ汾��TUTrec.x.509V3���ɹ��ʵ��������ƶ���
���ݰ���֤�����кš�֤����Ч�ں͹�����Կ����Ϣ��

DER��PER���룺
    ASN.1��һ�׹����ı��������Щ������������涨����ö���������ʾ���ݽṹ��DER������һ�֣�DERʹ��TLV�ṹ�洢���ݡ�
    DER����������Ƕ����Ƶģ����ʺ����ʼ����䣨����Email���ܷ��͸����������ʹ��PEM�Ѷ���������ת����ASCII�룬
    PEMʵ���Ͼ��ǰ�DER������ļ��Ķ�����������base64����һ�£�
    Ȼ�����-----BEGIN label-----������ͷ��-----END label-----������β���м�����DER�ļ���Base64���룬
    label�����������ݵ�����ʲô���ͣ���PEM��ص�RFC�кܶ࣬�뱾��������ص�����RFC7468��������涨�˺ܶ�label��
    ����Ҫע�ⲻ������label�����ж�Ӧ��RFC��Specification����Щlabelֻ��һ��Լ���׳ɡ�
    ʹ��openssl����������pem��der֮���ת����һ��˽Կ��pem�ṹ���£�
    -----BEGIN RSA PRIVATE KEY-----
    BASE64Encoded
    -----END RSA PRIVATE KEY-----

X509��PKCS
    X.509��һ��Public Key Certificates�ĸ�ʽ��׼,����νPublic Key Certificates�ֱ���ΪDigital Certificate �� Identity Certificate��
    һ��X.509 Certificate����һ��Public Key��һ�������Ϣ����Ҫô�Ǳ�CAǩ����Ҫô����ǩ���ġ�
    ��ʵ��X.509 Certificate�������ͨ��ָ������IETF��PKIX Certificate��CRL Profile����RFC5280��
    ���Ե��㿴��PKIX Certificate������ʱ�������Ϊ����X.509 Certificate��
    PKCS��Public Key����ѧ��׼��PKCS stands for "Public Key Cryptography Standards"��
    ����Public-Key Cryptography��Ȼ���ֿ���ȥֻ�漰Public Key��ʵ����Ҳ�漰Priviate Key�����PKCSҲ�漰Private Key��

���ֳ�����PEM label
CERTIFICATE            :  X.509 Certificate����            //RFC7468
PUBLIC KEY             :  X.509 Certificate Subject Public Key Info   //RFC7468
RSA PRIVATE KEY        :  PKCS 1 Private Key  //û��RFC��Ȩ��Specification���ø�ʽ��ʱ�򱻳�Ϊtraditional format��SSLeay format
RSA PUBLIC KEY         :  PKCS 1 Public Key   //ͬ��û��RFC��Ȩ��Specification
PRIVATE KEY            :  PKCS 8 Unencrypted Private Key   //RFC7468
ENCRYPTED PRIVATE KEY  :  PKCS 8 Encrypted Private Key     //RFC7468

������֤���ļ���׺(.pem .der .cer .crt .pfx .p12 .jks)



�ο����ϣ�
https://www.jianshu.com/p/bc32cbfe49e7

