<catalog s0>
file://�������֪ʶ.py
file://../�����׼�.txt

ab���߲�֧�� sm2-with-sms4-sm3 ����
sm2-with-sms4-sm3 ������ gmtls.h ��
    ע��SM4���������㷨��ԭ��SMS4
    https://www.cnblogs.com/codingmengmeng/p/5476260.html
    SM4Ϊ�Գ��㷨����Կ���Ⱥͷ��鳤�Ⱦ�Ϊ128λ��
    ��ԭSMS4�ı�׼������
        �����㷨����Կ��չ�㷨������32�ַ����Ե����ṹ��
        �����㷨������㷨�Ľṹ��ͬ��ֻ������Կ��ʹ��˳���෴��
        ��������Կ�Ǽ�������Կ������
    ����������л�������sm4��C����ʵ��

AB ֧�ֵ������׼���
    ECC-SM4-CBC-SM3
    ECC-SM4-GCM-SM3
    ECDHE-SM4-CBC-SM3
    ECDHE-SM4-GCM-SM3
    ע��ECC �� ECDHE
        ECC �� RSA ���ƣ�Ҳ���ڷǶԳƼ����㷨
            ������Բ���ߵ����ԣ�����k��G���Լ����K��������K��G�޷������k
            ���ܹ��̣�
            1. A ѡ��һ��Բ�����ϵĵ� G
            2. A ����˽Կ k�����ɹ�Կ K = k*G
            3. A ����Բ���ߡ�K��G ���͸� B
            4. B ѡ����Բ�����ϵ�һ�� M������һ����� r
            5. B ����� C1 = M + r * K��C2 = r * G
            6. B �� C1��C2 ���͸� A
            7. A ���� C1 - key*C2 = M + r*KEY*G - key*r*G = M
        DH ����ԿЭ��Э�飩
        ECDH��ECC&DH��
        
nginx֧�ֵ������׼���
   SM2-WITH-SMS4-SM3:SM2DHE-WITH-SMS4-SM3 �� ���� SSL-VPN CipherSuites ��
   
GmSSL ֧�������׼���
   һ�������� TLS 1.2 (�Լ�δ����TLS 1.3�����׼���
   һ���� GM/T 0024 SSL VPN��׼�ж�����׼�
   ���� GM/T 0024 ���Э�������Ϊ�Ǻ�IETF TLSЭ����ȫ��ͬ��Э��
   ���GmSSL�е�GM/T 0024�׼�����Ӧ��GM/T 0024Э�飬
   �� TLS 1.2 Э�������� GM/T 0024 ���׼����ͻᱨ��
   
�� gmt 0024 ssl vpn �����淶 ��19ҳ  ������ �����׼��б�
   ��gmsslͷ�ļ����� 0X0300E0 �ؼ��֣��� GM/T SSL-VPN CipherSuites �ؼ���
   �ܸ�����������׼��б��Ӧ��
   ssl vpn �����淶�У��� ssl �����׼�����������
   
gmsslͷ�ļ���֧�ֵ��㷨
   ECDHE-SM2-WITH-SMS4-SM3
   ECDHE-SM2-WITH-SM1-SM3
   ECDHE-SM2-WITH-SM1-SHA256
   SM2DHE-WITH-SMS4-SM3
   SM2-WITH-SMS4-SM3
   SM9DHE-WITH-SMS4-SM3
   SM9-WITH-SMS4-SM3
   RSA-WITH-SMS4-SM3
   RSA-WITH-SMS4-SHA1
   ������
   
�����׼��ṹ���壺
   ��ͬ�ļ����׼���Ӱ����Կ�����������֤���ӽ��ܵȹ��� 
   struct ssl_cipher_st {
        uint32_t valid;
        const char *name;           /* �ı����� */
        uint32_t id;                /* id, 4 bytes, first is version */
        /*
         * changed in 1.0.0: these four used to be portions of a single value
         * 'algorithms'
         */
        uint32_t algorithm_mkey;    /* ��Կ�����㷨 ��key exchange algorithm */
        uint32_t algorithm_auth;    /* �������֤ ��server authentication */
        uint32_t algorithm_enc;     /* �ԳƼ��ܣ� symmetric encryption */
        uint32_t algorithm_mac;     /* �Գ������֤�� symmetric authentication */
        int min_tls;                /* minimum SSL/TLS protocol version */
        int max_tls;                /* maximum SSL/TLS protocol version */
        int min_dtls;               /* minimum DTLS protocol version */
        int max_dtls;               /* maximum DTLS protocol version */
        uint32_t algo_strength;     /* strength and export flags */
        uint32_t algorithm2;        /* Extra flags */
        int32_t strength_bits;      /* Number of bits really used */
        uint32_t alg_bits;          /* Number of bits for algorithm */
    };   
    
ssl �� vpn ��
    const SSL_METHOD *GMTLS_method(void);
    const SSL_METHOD *gmtls_server_method(void);
    const SSL_METHOD *gmtls_client_method(void);
    #define SSLv23_method           TLS_method
    #define SSLv23_server_method    TLS_server_method
    #define SSLv23_client_method    TLS_client_method
    
    �����ʼ��ʹ��SSL_CTX_new(GMTLS_method)��
    ʹ��GMTLS_method�ͱ�ɹ���VPNͨ�ţ������Ҫ�ο�����GM/T 0024
    
gmssl(v2.3.1) �� openssl
    gmssl ��չ���ܺ�ͨ�������֣�openssl��Ϊ����ģ��crypto��ͨ��ģ��ssl����
    ������Ҫָ����sm2 sm3 sm4�����㷨���Լ���صļ������
    ͨ��ָ����gmtls������һ�� GM/T 0024-2014�淶ʵ�ֵģ�����˫֤�飬ǩ��֤��+����֤��
    ���ʹ�ù���tls����ֻ֧�� ECDHE-SM2-WITH-SMS4-SM3 �� ECDHE-SM2-WITH-SMS4-SHA256 �׼�
    gmssl��˫֤���˫��Կ������
        ֱ����������sm2֤�����Կ�Ϳ��ԣ�û�������ӿڣ����Ǵ������Լ����䣺
        keyusagedigitalSignature���͵�֤����ǩ��֤�飬�����Ǽ���֤��,
        ��Կ�أ�����֤����ڵ�ʱ���Ǽ�����Կ��������ǩ����Կ
        �����ʵ����©���ģ�����������ǩ��֤�顣��Ȼ����Ǽ���֤��