������֤
    1. �ͻ���->����� : ClientHello
        ��һ�����ͻ�����Ҫ��������ṩ������Ϣ��
        1.֧�ֵ�Э��汾������TLS 1.0��
        2.һ���ͻ������ɵ���������Ժ��������ɡ��Ի���Կ��
        3.֧�ֵļ��ܷ���������RSA��Կ����
        4.֧�ֵ�ѹ������
    2. �����->�ͻ��� : SSL �汾�����������������Կ
    
    
ץ������
    ���˷�����
        ping�ٶȻ�ȡipΪ110.242.68.4��
        �����ַ��� ip.addr==110.242.68.4 && tcp.port==3046
    1. �ͻ���->������ ������tcp���� syn
    2. ������->�ͻ��� ������tcp���� syn,ack
    3. �ͻ���->������ ������tcp���� ack
    4. �ͻ���->������ ������tls���� client hello
        Content Type : Handshake
        Version : TLS 1.0
        Length : 512
        Handshake Protocol ������Э�飩: Client Hello
            Handshake Type : Client Hello
            
TLS��SSL�Ĳ���
    TLS������һ����Э�飬����SSL(׼ȷ��˵��SSL v3)��ǿ���棬������Э���ʽ�ϣ���SSL����
    1. �汾�ţ�
        TLS��¼��ʽ��SSL��¼��ʽ��ͬ�����汾�ŵ�ֵ��ͬ��
        TLS�İ汾1.0ʹ�õİ汾��ΪSSLv3.1��
    2. ���ļ����룺
        SSLv3.0��TLS��MAC�㷨��MAC����ķ�Χ��ͬ��
        TLSʹ����RFC-2104�����HMAC�㷨��SSLv3.0ʹ�������Ƶ��㷨��
        ���߲������SSLv3.0�У�����ֽ�����Կ֮����õ����������㣬
        ��HMAC�㷨���õ���������㡣�������ߵİ�ȫ�̶�����ͬ�ġ�
    3. α���������
        TLSʹ���˳�ΪPRF��α�������������Կ��չ�����ݿ飬�Ǹ���ȫ�ķ�ʽ��
    4. �������룺
        TLS֧�ּ������е�SSLv3.0�������룬����TLS�����䶨���˺ܶ౨�����룬��
        1) ����ʧ��(decryption_failed)
        2) ��¼���(record_overflow)
        3) δ֪CA(unknown_ca)
        4) �ܾ�����(access_denied)�ȡ�
    5. ������Ϳͻ�֤�飺
        SSLv3.0��TLS����������𣬼�TLS"��֧��":
        1) Fortezza��Կ����
        2) �����㷨
        3) �ͻ�֤�顣
    6. certificate_verify��finished��Ϣ��
        SSLv3.0��TLS����certificate_verify��finished��Ϣ����MD5��SHA-1ɢ����ʱ��
        ����������������𣬵���ȫ���൱��
    7. ���ܼ��㣺
        TLS��SSLv3.0�ڼ�������ֵ(master secret)ʱ���õķ�ʽ��ͬ��
        �������Կͻ��˺ͷ���˸��Բ����������Ramdom��Ϊ����
    8. ��䣺
        �û����ݼ���֮ǰ��Ҫ���ӵ�����ֽڡ�
        ��SSL�У���������ݳ���Ҫ�ﵽ���Ŀ鳤�ȵ���С��������
        ����TLS�У���������ݳ��ȿ��������Ŀ鳤�ȵ�����������
        (��������󳤶�Ϊ255�ֽ�)��
        ���ַ�ʽ���Է�ֹ���ڶԱ��ĳ��Ƚ��з����Ĺ�����
            
TLSЭ�����
    �ο����ϣ�
        https://blog.csdn.net/s030602122/article/details/53538383
    TLSЭ����Է�Ϊ������
        ��¼Э�飨Record Protocol��
            ͨ��ʹ�ÿͻ��˺ͷ����Э�̺����Կ�������ݼ��ܴ��䡣
        ����Э�飨Handshake Protocol��
            �ͻ��˺ͷ���˽���Э�̣�ȷ��һ���������ݴ�����ܵ���Կ��
    SSL��¼Э��
        SSL��¼Э����������װ�ϲ�Э�����ݵ�Э�飬
        ��SSLЭ���У����еĴ������ݶ�����װ�ڼ�¼��
        ¼����: "��¼ͷ + ���Ȳ�Ϊ0�ļ�¼����"��ɵġ�
        SSL��¼Э�鶨����Ҫ�������ݵĸ�ʽ��
        ��λ��һЩ�ɿ��ĵĴ���Э��֮��(��TCP)
        ��¼Э����Ҫ��ɹ���:
            1) ���顢���
               ÿ���ϲ�Ӧ�����ݱ��ֳ�2^14(16K)�ֽڻ��С�����ݿ� 
            2) ѹ������ѹ��
               ѹ���ǿ�ѡ�ģ�����������ѹ����ѹ�������ݳ��ȵ����Ӳ��ܳ���1024�ֽڡ�
            3) �Լ���Ϣ��֤
               ��ѹ�������ϼ�����Ϣ��֤MAC
            4) ���ܴ����
               ��ѹ�����ݼ�MAC���м��ܣ�
            5) ����SSL��¼ͷ
               �������͡����汾���ΰ汾��ѹ������
        SSL��¼Э��Ľṹ
            1. ��������(8λ):
               1) �ı������ʽЭ��(change_cipher_spec): 20
               2) ����Э��(alert):                      21
               3) ����Э��(handshake):                  22
               4) Ӧ������Э��(application_data):       23
            2. ��Ҫ�汾(8λ):
               ʹ�õ�SSL��Ҫ�汾��Ŀǰ��SSL�汾��SSL v3����������ֶε�ֵֻ��3���ֵ
            3. ��Ҫ�汾(8λ):
               ʹ�õ�SSL��Ҫ�汾������SSL v3.0��ֵΪ0��
            4. ���ݰ�����(16λ):
               1) �������ݰ�: 
                  ����ֶα�ʾ���������������ֽ�Ϊ��λ�ĳ���
               2) ѹ�����ݰ�
                  ����ֶα�ʾ����ѹ���������ֽ�Ϊ��λ�ĳ��� 
               3) �������ݰ�
                  ����ֶα�ʾ���Ǽ����������ֽ�Ϊ��λ�ĳ���
            5. ��¼���� 
            6. MAC��0��16��20λ��
    SSL����Э��
        Э���ʽ
            1.  ����(Type)(1�ֽ�):
                ���ֶ�ָ��ʹ�õ�SSL����Э�鱨������
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
            2.  ����(Length)(3�ֽ�):
                ���ֽ�Ϊ��λ�ı��ĳ��ȡ�
            3.  ����(Content)(��1�ֽ�):
                ��Ӧ�������͵ĵ�ʵ�����ݡ�����
                1) hello_request: ��
                2) client_hello:  
                    2.1) �汾(ProtocolVersion)
                         ����ͻ��˿���֧�ֵ�SSL��߰汾��
                         2.1.1) ���汾: 3
                         2.1.2) �ΰ汾: 0
                    2.2) �����(Random)
                         �ͻ��˲�����һ��������������Կ(master key)��32�ֽڵ������
                         (����Կ�ɿͻ��˺ͷ���˵��������ͬ����)
                        2.2.1) uint32 gmt_unix_time;
                        2.2.2) opaque random_bytes[28];
                    2.3) �ỰID: �ỰID�ĳ��� & �ỰID������
                    2.4) ������(�����׼�): 
                        һ���ͻ��˿���֧�ֵ������׼��б�2�ֽڱ�ʾ��
                        ����б�����ʹ������˳�����У�ÿ�������׼���ָ����
                        "��Կ�����㷨"��"�����㷨"��"��֤�㷨"��"���ܷ�ʽ"
                        ע��
                            ��Կ�����㷨ʹ��Deffie-Hellman��Կ�����㷨��
                            ����RSA����Կ��������һ��ʵ����Fortezza chip�ϵ���Կ����
                            �����㷨����DES��RC4��RC2��3DES��
                            ��֤�㷨����MD5��SHA-1
                            ���ܷ�ʽ��Ϊ��ʽ���ܡ��������
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
                    2.5) ѹ��������
                3) server_hello: 
                    3.1) �汾(ProtocolVersion)
                         ��������"����"�����֧�ֵ�SSL�汾��
                         3.1.1) ���汾: 3
                         3.1.2) �ΰ汾: 0
                    3.2) �����(Random)
                         ����˲�����һ��������������Կ(master key)��32�ֽڵ������
                         (����Կ�ɿͻ��˺ͷ���˵��������ͬ����)
                         3.2.1) uint32 gmt_unix_time;
                         3.2.2) opaque random_bytes[28];
                    3.3) �ỰID: opaque SessionID<0..32>;
                    3.4) ������(�����׼�): 
                         �������˲��ɵ����ڱ���ͨѶ�ĵļ����׼�
                    3.5) ѹ������:
                         �������˲��ɵ����ڱ���ͨѶ�ĵ�ѹ������
                         ����������server_hello���Ƿ���˶Կͻ��˵ĵĻ�Ӧ����ʾ����ĳ������
                4) certificate: 
                   SSL���������Լ���"����˹�Կ֤��(ע�⣬�ǹ�Կ����)"���͸�SSL�ͻ���  
                   ASN.1Cert certificate_list<1..2^24-1>;
                5) server_key_exchange:   
                    1) RSA
                        ִ��RSA��ԿЭ�̹���
                        1.1) RSA����(ServerRSAParams)
                            1.1.1) opaque RSA_modulus<1..2^16-1>;
                            1.1.2) opaque RSA_exponent<1..2^16-1>;
                        1.2) ǩ������(Signature)
                            1.2.1) anonymous: null
                            1.2.2) rsa
                              ���� 1.2.2.1) opaque md5_hash[16];
                              ���� 1.2.2.2) opaque sha_hash[20];
                            1.2.3) dsa
                                   1.2.3.1) opaque sha_hash[20];
                    2) diffie_hellman
                        ִ��DH��ԿЭ�̹���
                        2.1) DH����(ServerDHParams)
                            2.1.1) opaque DH_p<1..2^16-1>;
                            2.1.2) opaque DH_g<1..2^16-1>;
                            2.1.3) opaque DH_Ys<1..2^16-1>;
                        2.2) ǩ������(Signature)
                            2.2.1) anonymous: null
                            2.2.2) rsa
                                2.2.2.1) opaque md5_hash[16];
                                2.2.2.2) opaque sha_hash[20];
                            2.2.3) dsa
                                2.2.3.1) opaque sha_hash[20];
                    3) fortezza_kea
                        ִ��fortezza_kea��ԿЭ�̹���
                        3.1) opaque r_s [128]
                6) certificate_request:   
                    6.1) ֤������(CertificateType)
                        6.1.1) RSA_sign
                        6.1.2) DSS_sign
                        6.1.3) RSA_fixed_DH
                        6.1.4) DSS_fixed_DH
                        6.1.5) RSA_ephemeral_DH
                        6.1.6) DSS_ephemeral_DH  
                        6.1.7) FORTEZZA_MISSI
                    6.2) Ψһ����(DistinguishedName)
                    certificate_authorities<3..2^16-1>;
                7) server_done: 
                   ���������Ƿ���server_hello_done���ģ�ָʾ��������hello�׶ν���
                   struct { } ServerHelloDone;
                8) certificate_verify:  
                    ǩ������(Signature)
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
                        
ֻ��֤��������SSL���ֹ���
    1. Client Hello
        SSL�ͻ���ͨ��Client Hello��Ϣ��SSL����˷���:
        1) ֧�ֵ�SSL�汾
        2) �ͻ������ɵ�һ��������������Կ(master key)��32�ֽڵ������(����Կ�ɿͻ��˺ͷ���˵��������ͬ����)
        3) �ỰID
        3) �����׼�
            3.1) �����㷨
            3.2) ��Կ�����㷨
            3.3) MAC�㷨
            3.4) ���ܷ�ʽ(��������)
        4) ѹ���㷨(���֧��ѹ���Ļ�)
    2. Server Hello
        SSL������ȷ������ͨ�Ų��õ�SSL�汾�ͼ����׼�����ͨ��Server Hello��Ϣ֪ͨ��SSL�ͻ��ˡ�
        ���SSL����������SSL�ͻ������Ժ��ͨ�������ñ��λỰ����SSL��������Ϊ���λỰ����ỰID��
        ��ͨ��Server Hello��Ϣ���͸�SSL�ͻ��ˡ�
        1) ����˲��ɵı���ͨѶ��SSL�汾
        2) ��������ɵ�һ��������������Կ(master key)��32�ֽڵ������(����Կ�ɿͻ��˺ͷ���˵��������ͬ����)
        3) �ỰID
        3) ����˲��ɵ����ڱ���ͨѶ�ļ����׼�(�ӿͻ��˷��͵ļ����׼��б���ѡ����һ��)
            3.1) �����㷨
            3.2) ��Կ�����㷨
            3.3) MAC�㷨
            3.4) ���ܷ�ʽ(��������)
        4) ѹ���㷨(���֧��ѹ���Ļ�)
    3. Certificate
        SSL��������"Я���Լ���Կ��Ϣ������֤��"�͵���CA�����������ͻ���ͨ��Certificate��Ϣ���͸�SSL�ͻ���(������Կ�ļ������͹�ȥ)��
        �ͻ���ʹ�������Կ�����������:
            1) �ͻ��˿���ʹ�øù�Կ����֤����˵���ݣ���Ϊֻ�з�����ж�Ӧ��˽Կ�ܽ������Ĺ�Կ���ܵ�����
            2) ���ڶ�"premaster secret"���м��ܣ����"premaster secret"�����ÿͻ��˺ͷ�������ɵ�Ramdom����������ɵģ�
               �ͻ����÷���˵Ĺ�Կ��������˼��ܺ��͸������
    4. Server Key Exchange
        ��Կ�����׶�(��ѡ����)��֮����˵�ǿ�ѡ���裬����Ϊֻ�������г������������Żᷢ��
        1) Э�̲�����RSA���ܣ����Ƿ���˵�֤��û���ṩRSA��Կ
        2) Э�̲�����DH���ܣ����Ƿ���˵�֤��û���ṩDH����
        3) Э�̲�����fortezza_kea���ܣ����Ƿ���˵�֤��û���ṩ����
        �ܽ���˵��"Server Key Exchange"��������Ƕ���һ��"Certificate"��һ�����䣬Ϊ��������SSL���ֹ�������������
    5. Server Hello Done
        SSL����������Server Hello Done��Ϣ��֪ͨSSL�ͻ��˰汾�ͼ����׼�Э�̽��� 
    6. Client Key Exchange
        SSL�ͻ�����֤SSL��������֤��Ϸ�������֤���еĹ�Կ����SSL�ͻ���������ɵ�"premaster secret"
        (ͨ��֮ǰ�ͻ��ˡ�����˷ֱ����ɵ���������ɵ�)��
        ��ͨ��Client Key Exchange��Ϣ���͸�SSL��������
        ע�⣬��һ����ɺ󣬿ͻ��˺ͷ���˶��Ѿ�������"����Կ"(֮���������Ԥ������Կ������Ϊ��û��Ͷ��ʹ��)��
        ���"����Կ"������֮���SSLͨ�����ݵļ���
    7. Change Cipher Spec
        SSL�ͻ��˷���Change Cipher Spec��Ϣ��֪ͨSSL�������������Ľ�����Э�̺õ�"����Կ"�ͼ����׼����м��ܺ�MAC���㡣
    8. Finished
        SSL�ͻ��˼����ѽ�����������Ϣ(��Change Cipher Spec��Ϣ�������ѽ�������Ϣ)��Hashֵ��
        ����Э�̺õ���Կ�ͼ����׼�����Hashֵ(���㲢���MACֵ�����ܵ�)����ͨ��Finished��Ϣ���͸�SSL��������
        SSL����������ͬ���ķ��������ѽ�����������Ϣ��Hashֵ������Finished��Ϣ�Ľ��ܽ���Ƚϣ�
        ���������ͬ����MACֵ��֤�ɹ�����֤����Կ�ͼ����׼�Э�̳ɹ���
    9. Change Cipher Spec
        ͬ���أ�SSL����������Change Cipher Spec��Ϣ��֪ͨSSL�ͻ��˺������Ľ�����Э�̺õ���Կ�ͼ����׼����м��ܺ�MAC���㡣
    10. Finished
        SSL�����������ѽ�����������Ϣ��Hashֵ������Э�̺õ���Կ�ͼ����׼�����Hashֵ(���㲢���MACֵ�����ܵ�)��
        ��ͨ��Finished��Ϣ���͸�SSL�ͻ��ˡ�SSL�ͻ�������ͬ���ķ���������
        ������������Ϣ��Hashֵ������Finished��Ϣ�Ľ��ܽ���Ƚϣ����������ͬ����MACֵ��֤�ɹ�����֤����Կ�ͼ����׼�Э�̳ɹ���
        SSL�ͻ��˽��յ�SSL���������͵�Finished��Ϣ��������ܳɹ���������ж�SSL������������֤���ӵ���ߣ�
        ��SSL�����������֤�ɹ�����Ϊֻ��ӵ��˽Կ��SSL���������ܴ�Client Key Exchange��Ϣ�н��ܵõ�premaster secret��
        �Ӷ���ӵ�ʵ����SSL�ͻ��˶�SSL�������������֤��
