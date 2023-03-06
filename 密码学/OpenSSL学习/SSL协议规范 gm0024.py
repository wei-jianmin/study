file://D:\workspace\projects\baseroot\base\depts\jc1\private\zhouping
         \学习笔记\密码行业规范\已整理\GMT 0024-2014 SSL VPN 技术规范.PDF
         
从证书请求协议的结构来看，
该协议区别于rfc5246(tslv2)，
与rfc4346(tlsv1)或rfc8446(tslv3)一致
    
握手协议：
    总的数据结构
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
    从握手协议发送的数据结构可见：
        前4个字节 = 1字节标记类型 + 3字节标记body长度
        后面n字节的body部分是个枚举类型
        所以该数据结构根据类型的不同，又可具体化为10种结构
        在双方握手时，就是以上面的数据结构为发送单位
    双方握手时交互发送的 Handshake
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
        注：
            前面带*的，表可选或依赖上下文，不是每次都发送
                ServerKeyExchange
                    这一步只有在选择了某些密钥交换算法例如DH算法的时候才需要
                CertificateRequest
                Certificate
                CertificateVerify
                    如果是单向认证，这三部分是不需要的
            用[]括起来的，标识不属于握手协议消息
            ChangeCipherSpec由密码变更协议定义
    HelloRequest
        数据结构
            struct { } HelloRequest;  //&<HelloRequest>
    ClientHello
        数据结构 
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
                对于变长类型，前2字节标识长度
    ServerHello
        数据结构
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
        数据结构
            struct {  //&<Certificate>
                bytes<3> length;
                ASN.1Cert certificate_list<0..2^24-1>;
            } Certificate;
            struct {
                bytes<3> length;
                x509 certdata;
            } ASN.1Cert;
    ServerKeyExchange
        数据结构
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
        数据结构
            struct {  //&<CertificateRequest>
                ClientCertificateType certificate_types<1..2^8-1>;
                DistinguishedName certificate_authorities<0..2^16-1>;
            } CertificateRequest;
            enum {    //&<ClientCertificateType>
                rsa_sign(1), dss_sign(2), rsa_fixed_dh(3), dss_fixed_dh(4),
                rsa_ephemeral_dh_RESERVED(5), dss_ephemeral_dh_RESERVED(6),
                fortezza_dms_RESERVED(20), (255)
            } ClientCertificateType;
            opaque DistinguishedName<1..2^16-1>;  //&<DistinguishedName> opaque:不透明的
    ServerHelloDone
        数据结构
            struct { } ServerHelloDone;  //&<ServerHelloDone>
    ClientKeyExchange
        数据结构
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
        数据结构
            struct {  //&<CertificateVerify>
                digitally-signed struct {
                   opaque handshake_messages[handshake_messages_length];
                }
            } CertificateVerify;
    Finished
        数据结构
            struct {  //&<Finished>
                opaque verify_data[verify_data_length];
            } Finished;
    
    
    
相关参考：
    SSL通信过程的官方规范是 RFC5246，其中文翻译参看如下贴：
    https://blog.csdn.net/PiPiQ_Blog/article/details/117910810
    