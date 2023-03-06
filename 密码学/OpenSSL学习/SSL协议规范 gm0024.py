file://D:\workspace\projects\baseroot\base\depts\jc1\private\zhouping
         \ѧϰ�ʼ�\������ҵ�淶\������\GMT 0024-2014 SSL VPN �����淶.PDF
         
��֤������Э��Ľṹ������
��Э��������rfc5246(tslv2)��
��rfc4346(tlsv1)��rfc8446(tslv3)һ��
    
����Э�飺
    �ܵ����ݽṹ
        struct Handshake{
          HandshakeType msg_type;    /* @HandshakeType */
          uint24 length;             /* bytes in message */
          select (HandshakeType) {
              case hello_request:       HelloRequest;
              case client_hello:        ClientHello;
              case server_hello:        ServerHello;
              case certificate:         Certificate;
              case server_key_exchange: ServerKeyExchange;
              case certificate_request: CertificateRequest;
              case server_hello_done:   ServerHelloDone;
              case certificate_verify:  CertificateVerify;
              case client_key_exchange: ClientKeyExchange;
              case finished:            Finished;
          } body;
        };
        enum HandshakeType{   //&<HandshakeType>
          hello_request(0), client_hello(1), server_hello(2),
          certificate(11), server_key_exchange (12),
          certificate_request(13), server_hello_done(14),
          certificate_verify(15), client_key_exchange(16),
          finished(20), (255)
        };
    ������Э�鷢�͵����ݽṹ�ɼ���
        ǰ4���ֽ� = 1�ֽڱ������ + 3�ֽڱ��body����
        ����n�ֽڵ�body�����Ǹ�ö������
        ���Ը����ݽṹ�������͵Ĳ�ͬ���ֿɾ��廯Ϊ10�ֽṹ
        ��˫������ʱ����������������ݽṹΪ���͵�λ
    ˫������ʱ�������͵� Handshake
        Client                                             Server
        =========================================================
        ClientHello            -------->
        ---------------------------------------------------------
                               <--------              ServerHello
                               <--------             *Certificate
                               <--------       *ServerKeyExchange
                               <--------      *CertificateRequest
                               <--------          ServerHelloDone
        ---------------------------------------------------------                       
        *Certificate           -------->
        ClientKeyExchange      -------->
        *CertificateVerify     -------->
        [ChangeCipherSpec]     -------->
        Finished               -------->
        ---------------------------------------------------------
                               <--------       [ChangeCipherSpec]
                               <--------                 Finished
        ---------------------------------------------------------
        Application Data       <------->         Application Data
        =========================================================
        ע��
            ǰ���*�ģ����ѡ�����������ģ�����ÿ�ζ�����
                ServerKeyExchange
                    ��һ��ֻ����ѡ����ĳЩ��Կ�����㷨����DH�㷨��ʱ�����Ҫ
                CertificateRequest
                Certificate
                CertificateVerify
                    ����ǵ�����֤�����������ǲ���Ҫ��
            ��[]�������ģ���ʶ����������Э����Ϣ
            ChangeCipherSpec��������Э�鶨��
    HelloRequest
        ���ݽṹ
            struct { } HelloRequest;  //&<HelloRequest>
    ClientHello
        ���ݽṹ 
            struct {  //&<ClientHello>
                ProtocolVersion client_version;
                Random random;
                SessionID session_id;
                CipherSuite cipher_suites<2..2^16-2>;
                CompressionMethod compression_methods<1..2^8-1>;
                select (extensions_present) {
                  case false:
                      struct {};
                  case true:
                      Extension extensions<0..2^16-1>;
                };
            } ClientHello;
            struct { //&<ProtocolVersion>
               uint8 major;
               uint8 minor;
            } ProtocolVersion;
            struct {  //&<Random>
               uint32 gmt_unix_time;
               opaque random_bytes[28];
            } Random;
            opaque SessionID<0..32>;  //&SessionID>
            uint8 CipherSuite[2];  //&<CipherSuite>
            enum { null(0), (255) } CompressionMethod;  //&<CompressionMethod>
            struct {  //&<Extension>
                ExtensionType extension_type;
                opaque extension_data<0..2^16-1>;
            } Extension;
            enum {   //&<ExtensionType>
                signature_algorithms(13), (65535)
            } ExtensionType;
            opaque //&<opaque>
                ���ڱ䳤���ͣ�ǰ2�ֽڱ�ʶ����
    ServerHello
        ���ݽṹ
            struct {  //&<ServerHello>
                ProtocolVersion server_version;
                Random random;
                SessionID session_id;
                CipherSuite cipher_suite;
                CompressionMethod compression_method;
                select (extensions_present) {
                  case false:
                      struct {};
                  case true:
                      Extension extensions<0..2^16-1>;
                };
            } ServerHello;
    Certificate
        ���ݽṹ
            struct {  //&<Certificate>
                bytes<3> length;
                ASN.1Cert certificate_list<0..2^24-1>;
            } Certificate;
            struct {
                bytes<3> length;
                x509 certdata;
            } ASN.1Cert;
    ServerKeyExchange
        ���ݽṹ
            struct {  //&<ServerKeyExchange>
                select (KeyExchangeAlgorithm) {
                    case ECDHE:
                        ...
                    case ECC:
                        ...
                    case IBSDH:
                        ...
                    case IBC:
                        ...
                    case RSA:
                        ...
                };
            } ServerKeyExchange;
    CertificateRequest
        ���ݽṹ
            struct {  //&<CertificateRequest>
                ClientCertificateType certificate_types<1..2^8-1>;
                DistinguishedName certificate_authorities<0..2^16-1>;
            } CertificateRequest;
            enum {    //&<ClientCertificateType>
                rsa_sign(1), dss_sign(2), rsa_fixed_dh(3), dss_fixed_dh(4),
                rsa_ephemeral_dh_RESERVED(5), dss_ephemeral_dh_RESERVED(6),
                fortezza_dms_RESERVED(20), (255)
            } ClientCertificateType;
            opaque DistinguishedName<1..2^16-1>;  //&<DistinguishedName> opaque:��͸����
    ServerHelloDone
        ���ݽṹ
            struct { } ServerHelloDone;  //&<ServerHelloDone>
    ClientKeyExchange
        ���ݽṹ
            struct {  //&<ClientKeyExchange>
                select (KeyExchangeAlgorithm) {
                    case rsa: 
                        EncryptedPreMasterSecret;
                    case dhe_dss:
                    case dhe_rsa:
                    case dh_dss:
                    case dh_rsa:
                    case dh_anon: 
                        ClientDiffieHellmanPublic;
                } exchange_keys;
            } ClientKeyExchange;
            struct {  //&<EncryptedPreMasterSecret>
                public-key-encrypted PreMasterSecret pre_master_secret;
            } EncryptedPreMasterSecret;
            struct {   //&<ClientDiffieHellmanPublic>
                select (PublicValueEncoding) {  //&<dh_public>
                    case implicit: 
                        struct { };
                    case explicit: 
                        opaque dh_Yc<1..2^16-1>;
                } dh_public;
            } ClientDiffieHellmanPublic;
    CertificateVerify
        ���ݽṹ
            struct {  //&<CertificateVerify>
                digitally-signed struct {
                   opaque handshake_messages[handshake_messages_length];
                }
            } CertificateVerify;
    Finished
        ���ݽṹ
            struct {  //&<Finished>
                opaque verify_data[verify_data_length];
            } Finished;
    
    
    
��زο���
    SSLͨ�Ź��̵Ĺٷ��淶�� RFC5246�������ķ���ο���������
    https://blog.csdn.net/PiPiQ_Blog/article/details/117910810
    