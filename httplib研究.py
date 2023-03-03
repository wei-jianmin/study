c++11��make_shared��������û��make_unique����������Դ˺��������˷�װ���Ա���ʹ��new�ؼ���

����ci����������֧�������ַ������Դ�Сд���бȽ�

class Client 
    ʹ�����ģʽ����������������ǵ��õ� std::unique_ptr<ClientImpl> cli_; ����ط���
    ֻ��һ�����캯�����Լ���ʵ�֣�����Ըú������з�����
    1. ������ "^(?:([a-z]+)://)?([^:/?#]+)(?::(\d+))?"���жϴ����� scheme_host_port
       �������http��ͷ�� �׳��쳣�� ����
       ��ȡ��host��port����
       �����Ƿ���https��Ϊcli_��ֵ SSLClient�����������CPPHTTPLIB_OPENSSL_SUPPORT���� ClientImpl
       SSLClient��ClientImpl����Ҫ�ֱ�ָ��host��port��[client_cert_path]��[client_key_path]������       
class ClientImpl
    ��Ա������
        ���������ĳ�Ա�����Ƚ϶�
        ��¼����������Ϣ���У�
            host_��port_��host_and_port_��client_cert_path_��client_key_path_��
        ���Ӻ����У�
            socket_
        ���ӿ����У�
            socket_should_be_closed_when_request_is_done_=false��
            keep_alive_��tcp_nodelay_��decompress_��compress_��
        ������Ա�У�
            logger_��socket_mutex_��request_mutex_
        ������
            socket_requests_are_from_thread_��interface_��proxy_host_��
            socket_requests_in_flight_=0 ��
    ���캯����ֻ�𵽽�������¼Ϊ��Ա����������
    Post������Ҫ����������ʵ�֣�
        Result ClientImpl::Post(const char *path, const Headers &headers,
                               const char *body, size_t content_length,const char *content_type) 
        {
            return send_with_content_provider("POST", path, headers, body, content_length,
                                              nullptr, nullptr, content_type);
        }
        Result ClientImpl::Post(const char *path, const Headers &headers,
                                const MultipartFormDataItems &items, const std::string &boundary)
        { ... }
        �����ַ�ʽ�ĸ���ʵ����һ��������(-MARK)����������ֻ������һ��
            send_with_content_providerҲ��ClientImpl�����س�Ա����
            �ڲ�����Request�����Response���󣬽�������������Ϊ����������send����
            Request��װ��Ҫ���͵�������Ϣ���������������method��path��headers��body����Ϣ������¼��������
            Response�Ǹ��ն�����Ϊsend���������
                send��ClientImpl�ĳ�Ա����
                bool ClientImpl::send(const Request &req, Response &res, Error &error);
                ClientImpl�и� socket_should_be_closed_when_request_is_done_ �Ĳ����ͳ�Ա������
                ���socket��������ɺ��Ƿ��Զ��رգ�������Ϊ��
                ���socket_�Ǵ򿪵ģ���2�����ϵ���send����ʱ��
                    ������
                �� create_and_connect_socket(socket_,error);  ������ʧ�ܣ��ͷ���false
                ���socket_requests_in_flight_���׽�����ʹ���б�ǣ�> 1
                ��ȷ����¼�� socket_requests_are_from_thread_ == std::this_thread::get_id()
                socket_requests_in_flight_ += 1
                socket_requests_are_from_thread_ = std::this_thread::get_id();
                �� process_socket - handle_request
                    process_socket����SocketStream���󣬼�¼sock, read_timeout_sec_, read_timeout_usec_,
                    write_timeout_sec_, write_timeout_usec_�Ȳ���(����sock,�����������ǳ���)
                    ��SocketStream���󴫸� handle_request(strm, req, res, !keep_alive_, error)
                        ȷ��req.path��Ϊ�գ����򷵻�false
                        ��鲻��ssl && proxy_host_��Ϊ�� && proxy_port_ != -1
                            ... ��ʹ�ô���������
                        �������process_request
                            write_request(strm, req, close_connection, error)
                            read_response_line(strm, req, res) �� detail::read_headers(strm, res.headers)
                            ע��SocketStream��װ��read��write��is_readable��is_writable��socket�ȷ���
                                ʵ���˶Թ�����socket�Ķ���д
                            ���req��response_handler_�� ���� req.response_handler_(res)
                socket_requests_in_flight_ -= 1;
                �� socket_requests_in_flight_ Ϊ 0 ʱ��socket_requests_are_from_thread_ = std::thread::id();
                ��� socket_should_be_closed_when_request_is_done_==true �� keep_alive_==false �� ��һ��ִ�г���
                ��shutdown(socket,SD_BOTH)��closesocket
class SSLClient
    SSLClient�̳���ClientImpl
    ���еĳ�Ա������
        SSL_CTX *ctx_;
        std::mutex ctx_mutex_;
        std::string ca_cert_file_path_;
        std::string ca_cert_dir_path_;
        ��
    ���캯��
        ctx_ = SSL_CTX_new(SSLv23_client_method());
        ����ctx_
    ������    

����Openssl��HTTPSͨ��c++ʵ��
    �Σ�https://www.cnblogs.com/bwar/p/9879893.html
    https���ͣ� http���ݣ�����ssl���ܺ���ͨ��tcp����
    https���ܣ� tcp���յ��������Ǽ��ܵģ���ssl���ܺ󣬵õ��ɶ���http
    Openssl��ص�API
        �ȳ�ʼ��Openssl
            �ڽ���SSL����֮ǰ��ҪΪClient��Server�ֱ�ָ���������Ӳ��õ�Э�鼰��汾��
            Ŀǰ�ܹ�ʹ�õ�Э��汾����SSLv2��SSLv3��SSLv2/v3��TLSv1.0
            �����磺
            OPENSSL_config(NULL);
            SSL_library_init();         // ��ʼ��SSL�㷨�⺯��( ����Ҫ�õ����㷨 )��
                                        // ����SSL����֮ǰ������ô˺���
            SSL_load_error_strings();   // ������Ϣ�ĳ�ʼ��
            OpenSSL_add_all_algorithms();
        ����CTX
            CTX��SSL�Ự��������������ʱʹ�ò�ͬ��Э�飬��CTXҲ��һ��
            //�ͻ��ˡ�����˶���Ҫ����
            SSL_CTX_new();                       //����SSL�Ự����
            //������֤�Է�֤��������������
            SSL_CTX_set_verify();                //ָ��֤����֤��ʽ
            SSL_CTX_load_verify_location();      //ΪSSL�Ự�������ر�Ӧ�������ε�CA֤���б�
            //���м���֤��������������
            int SSL_CTX_use_certificate_file();      //ΪSSL�Ự���ر�Ӧ�õ�֤��
            int SSL_CTX_use_certificate_chain_file();//ΪSSL�Ự���ر�Ӧ�õ�֤��������֤����
            int SSL_CTX_use_PrivateKey_file();       //ΪSSL�Ự���ر�Ӧ�õ�˽Կ
            int SSL_CTX_check_private_key();         //��֤�����ص�˽Կ��֤���Ƿ���ƥ�� 
        ����SSL�׽���
            �ڴ���SSL�׽���֮ǰҪ�ȴ���Socket�׽��֣�����TCP���ӣ�����˻�Ҫ���bind��listen
            SSL *SSl_new(SSL_CTX *ctx);          //����һ��SSL�׽���
            int SSL_set_fd(SSL *ssl, int fd);     //�Զ�дģʽ�����׽���
            int SSL_set_rfd(SSL *ssl, int fd);    //��ֻ��ģʽ�����׽���
            int SSL_set_wfd(SSL *ssl, int fd);    //��ֻдģʽ�����׽���
        ���SSL����
            int SSL_connect(SSL *ssl);   //�ͻ���
            int SSL_accept(SSL *ssl);    //�����
            ���ֹ������֮��Clientͨ����Ҫ��Server����֤����Ϣ���Ա��Server���м���
            ��ʵ�ֻ��õ�������������
            X509 *SSL_get_peer_certificate(SSL *ssl);  //��SSL�׽����л�ȡ�Է���֤����Ϣ
            X509_NAME *X509_get_subject_name(X509 *a); //�õ�֤�������ߵ�����
        ���ݴ���
            int SSL_read(SSL *ssl,void *buf,int num);            //��SSL�׽��ֶ�ȡ����
            int SSL_write(SSL *ssl,const void *buf,int num);     //��SSL�׽���д������
        �Ự����
            int SSL_shutdown(SSL *ssl);       //�ر�SSL�׽���
            void SSl_free(SSL *ssl);          //�ͷ�SSL�׽���
            void SSL_CTX_free(SSL_CTX *ctx);  //�ͷ�SSL�Ự����
    Nebula���
        Nebula��һ��C++���Կ������¼������͵�TCPЭ��ֲ�ʽ�����ܣ�
        ֧�ְ���proto3��http��https��websocket����Ӧ�ò�ͨ��Э��
    