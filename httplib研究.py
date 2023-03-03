c++11有make_shared方法，但没有make_unique方法，这里对此函数进行了封装，以避免使用new关键字

构造ci函数对象，以支持两个字符串忽略大小写进行比较

class Client 
    使用组合模式，绝大多数函数都是调用的 std::unique_ptr<ClientImpl> cli_; 的相关方法
    只有一个构造函数有自己的实现，下面对该函数进行分析：
    1. 用正则 "^(?:([a-z]+)://)?([^:/?#]+)(?::(\d+))?"，判断传来的 scheme_host_port
       如果不以http开头， 抛出异常， 返回
       提取出host或port部分
       根据是否是https，为cli_赋值 SSLClient（如果定义了CPPHTTPLIB_OPENSSL_SUPPORT）或 ClientImpl
       SSLClient或ClientImpl都需要分别指定host、port、[client_cert_path]、[client_key_path]参数。       
class ClientImpl
    成员变量：
        这个类里面的成员变量比较多
        记录基础连接信息的有：
            host_、port_、host_and_port_、client_cert_path_、client_key_path_等
        连接核心有：
            socket_
        连接控制有：
            socket_should_be_closed_when_request_is_done_=false、
            keep_alive_、tcp_nodelay_、decompress_、compress_等
        辅助成员有：
            logger_、socket_mutex_、request_mutex_
        其它：
            socket_requests_are_from_thread_、interface_、proxy_host_、
            socket_requests_in_flight_=0 等
    构造函数：只起到将参数记录为成员变量的作用
    Post方法主要有两种重载实现：
        Result ClientImpl::Post(const char *path, const Headers &headers,
                               const char *body, size_t content_length,const char *content_type) 
        {
            return send_with_content_provider("POST", path, headers, body, content_length,
                                              nullptr, nullptr, content_type);
        }
        Result ClientImpl::Post(const char *path, const Headers &headers,
                                const MultipartFormDataItems &items, const std::string &boundary)
        { ... }
        这两种方式的根本实现有一定相似性(-MARK)，这里我们只分析第一种
            send_with_content_provider也是ClientImpl的重载成员方法
            内部创建Request对象和Response对象，将这两个对象作为参数，调用send方法
            Request封装了要发送的请求信息，像如参数传来的method、path、headers、body等信息，都记录在这里面
            Response是个空对象，作为send的输出参数
                send是ClientImpl的成员方法
                bool ClientImpl::send(const Request &req, Response &res, Error &error);
                ClientImpl有个 socket_should_be_closed_when_request_is_done_ 的布尔型成员变量，
                标记socket在请求完成后是否自动关闭，这里设为否
                如果socket_是打开的（第2次以上调用send方法时）
                    。。。
                ● create_and_connect_socket(socket_,error);  如果这句失败，就返回false
                如果socket_requests_in_flight_（套接字在使用中标记）> 1
                则确保记录的 socket_requests_are_from_thread_ == std::this_thread::get_id()
                socket_requests_in_flight_ += 1
                socket_requests_are_from_thread_ = std::this_thread::get_id();
                ● process_socket - handle_request
                    process_socket创建SocketStream对象，记录sock, read_timeout_sec_, read_timeout_usec_,
                    write_timeout_sec_, write_timeout_usec_等参数(除了sock,其它参数都是常量)
                    将SocketStream对象传给 handle_request(strm, req, res, !keep_alive_, error)
                        确保req.path不为空，否则返回false
                        检查不是ssl && proxy_host_不为空 && proxy_port_ != -1
                            ... （使用代理的情况）
                        否则调用process_request
                            write_request(strm, req, close_connection, error)
                            read_response_line(strm, req, res) 或 detail::read_headers(strm, res.headers)
                            注：SocketStream封装了read、write、is_readable、is_writable、socket等方法
                                实现了对关联的socket的读和写
                            如果req有response_handler_， 调用 req.response_handler_(res)
                socket_requests_in_flight_ -= 1;
                当 socket_requests_in_flight_ 为 0 时，socket_requests_are_from_thread_ = std::thread::id();
                如果 socket_should_be_closed_when_request_is_done_==true 或 keep_alive_==false 或 上一步执行出错
                则shutdown(socket,SD_BOTH)和closesocket
class SSLClient
    SSLClient继承了ClientImpl
    特有的成员变量：
        SSL_CTX *ctx_;
        std::mutex ctx_mutex_;
        std::string ca_cert_file_path_;
        std::string ca_cert_dir_path_;
        等
    构造函数
        ctx_ = SSL_CTX_new(SSLv23_client_method());
        设置ctx_
    。。。    

基于Openssl的HTTPS通信c++实现
    参：https://www.cnblogs.com/bwar/p/9879893.html
    https发送： http数据，经过ssl加密后，在通过tcp发送
    https接受： tcp接收到的数据是加密的，经ssl解密后，得到可读的http
    Openssl相关的API
        先初始化Openssl
            在建立SSL连接之前，要为Client和Server分别指定本次连接采用的协议及其版本，
            目前能够使用的协议版本包括SSLv2、SSLv3、SSLv2/v3和TLSv1.0
            代码如：
            OPENSSL_config(NULL);
            SSL_library_init();         // 初始化SSL算法库函数( 加载要用到的算法 )，
                                        // 调用SSL函数之前必须调用此函数
            SSL_load_error_strings();   // 错误信息的初始化
            OpenSSL_add_all_algorithms();
        创建CTX
            CTX是SSL会话环境，建立连接时使用不同的协议，其CTX也不一样
            //客户端、服务端都需要调用
            SSL_CTX_new();                       //申请SSL会话环境
            //若有验证对方证书的需求，则需调用
            SSL_CTX_set_verify();                //指定证书验证方式
            SSL_CTX_load_verify_location();      //为SSL会话环境加载本应用所信任的CA证书列表
            //若有加载证书的需求，则需调用
            int SSL_CTX_use_certificate_file();      //为SSL会话加载本应用的证书
            int SSL_CTX_use_certificate_chain_file();//为SSL会话加载本应用的证书所属的证书链
            int SSL_CTX_use_PrivateKey_file();       //为SSL会话加载本应用的私钥
            int SSL_CTX_check_private_key();         //验证所加载的私钥和证书是否相匹配 
        创建SSL套接字
            在创建SSL套接字之前要先创建Socket套接字，建立TCP连接，服务端还要完成bind、listen
            SSL *SSl_new(SSL_CTX *ctx);          //创建一个SSL套接字
            int SSL_set_fd(SSL *ssl, int fd);     //以读写模式绑定流套接字
            int SSL_set_rfd(SSL *ssl, int fd);    //以只读模式绑定流套接字
            int SSL_set_wfd(SSL *ssl, int fd);    //以只写模式绑定流套接字
        完成SSL握手
            int SSL_connect(SSL *ssl);   //客户端
            int SSL_accept(SSL *ssl);    //服务端
            握手过程完成之后，Client通常会要求Server发送证书信息，以便对Server进行鉴别。
            其实现会用到以下两个函数
            X509 *SSL_get_peer_certificate(SSL *ssl);  //从SSL套接字中获取对方的证书信息
            X509_NAME *X509_get_subject_name(X509 *a); //得到证书所用者的名字
        数据传输
            int SSL_read(SSL *ssl,void *buf,int num);            //从SSL套接字读取数据
            int SSL_write(SSL *ssl,const void *buf,int num);     //向SSL套接字写入数据
        会话结束
            int SSL_shutdown(SSL *ssl);       //关闭SSL套接字
            void SSl_free(SSL *ssl);          //释放SSL套接字
            void SSL_CTX_free(SSL_CTX *ctx);  //释放SSL会话环境
    Nebula框架
        Nebula是一个C++语言开发的事件驱动型的TCP协议分布式网络框架，
        支持包括proto3、http、https、websocket多种应用层通信协议
    