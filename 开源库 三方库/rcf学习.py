参：https://blog.csdn.net/yuweiping5247/article/details/81386658
参：https://blog.csdn.net/swartz_lubel/article/details/76423470
引用rcf：
    rcf源码下有很多文件，但都是hpp文件
    引用rcf时，只要包含一个 RCF.hpp 即可
依赖其它三方库：
    rcf内部使用了boost
rcf实现的功能： 
    可以像调用本地类方法一样，调用服务端所绑定类的方法
rcf服务端举例：
    #include <iostream>
    #include <RCF/RCF.hpp>
        
    //这是期望在客户端远程调用的类
    class PrintService
    {
    public:
        void Print(const std::string & s)
        {
            std::cout << "I_PrintService service: " << s << std::endl;
        }
        std::string echo(const std::string &s)
        {
            return s;
        }
    };
    
    //对PrintService的rcf描述
    RCF_BEGIN(I_PrintService, "I_PrintService")  //RCF接口定义，最多可以由25个成员方法
        RCF_METHOD_V1(void, Print, const std::string &) //RCF_METHOD_通用前缀，V表示返回值void， //1表示一个参数
        RCF_METHOD_R1(std::string, echo, const std::string &) //R（return）表示有返回值（非void）
    RCF_END(I_PrintService)  //这些宏最终定义为 RcfClient<type>类
    
    //主程序
    int main(int argc, char **argv)
    {
        try
        {
            RCF::RcfInit rcfInit;  //初始化RCF
            RCF::RcfServer server(RCF::TcpEndpoint("192.168.241.129", 500001)); 
            //建立RCF远程服务，设定IP和端口,还可以是 RCF::TcpEndpoint(50001)
            //还可为RCF::UdpEndpoint(50001)，表明使用udp协议
            
            PrintService printService;
            server.bind<I_PrintService>(printService);  //绑定类对象
            
            server.start();  //启动服务，开始监听，不会阻塞当前线程
            std::cin.get();  //当前线程不能退出，否则前面所绑定的类对象就释放了
            //或 server.startInThisThread();
        }
        catch(const RCF::Exception &e)
        {
            std::cout << "Error: " << e.getErrorMessage() << std::endl;
        }
        return 0;
    }    
rcf客户端举例：    
    #include <iostream>
    #include <RCF/RCF.hpp>
    
    //远程类的rcf描述
    RCF_BEGIN(I_PrintService, "I_PrintService")  //RCF接口
        RCF_METHOD_V1(void, Print, const std::string &)
        RCF_METHOD_R1(std::string, echo, const std::string &)
    RCF_END(I_PrintService)
     
    //主程序
    int main(int argc, char **argv)
    {
        try
        {
            RCF::RcfInit rcfInit;  //初始化RCF
            RcfClient<I_PrintService> client(RCF::TcpEndpoint("192.168.241.129", 500001)); //创建客户端并连接

            //调用远程类的方法
            client.Print("Hello World");   
            //RCF::Twoway(不加时，默认使用该参数)客户端存根调用中的参数是一个标志，告诉RCF进行双向客户端调用;
            //客户端发送请求，等待响应，如果在可配置的持续时间内没有收到请求，则会抛出异常。
            //另一个选择是使用RCF::Oneway; 发送请求，但服务器不发送响应，客户端存根调用将立即将控制权返回给用户。
            std::string s = client.echo(RCF::Twoway, "what's up");
            std::cout << s << std::endl;
        }
        catch(const RCF::Exception & e)
        {
            std::cout << "Error: " << e.getErrorMessage() << std::endl;
        }
     
        return 0;
    }
rcf服务端绑定对象：
    绑定对象的方式有多种：
        直接绑定对象
            Echo echo;
            server.bind<I_Echo>(echo);
        绑定 std::auto_ptr<>...
            std::auto_ptr<Echo> echoAutoPtr(new Echo());
            server.bind<I_Echo>(echoAutoPtr);
        绑定 boost::shared_ptr<>...
            boost::shared_ptr<Echo> echoPtr(new Echo());
            server.bind<I_Echo>(echoPtr);
        绑定 boost::weak_ptr<>...
            boost::weak_ptr<Echo> echoWeakPtr(echoPtr);
            server.bind<I_Echo>(echoWeakPtr);
    可以同时绑定多个对象（为每个对象指定不同的名字）
        RcfServer server(endpoint);
        // 绑定对象1
        Echo echo1;
        server.bind<I_Echo>(echo1, "Echo1");
        // 绑定对象2
        Echo echo2;
        server.bind<I_Echo>(echo2, "Echo2");
        server.start();
        //客户端使用时：
        RcfClient<I_Echo> echoClient(endpoint);
        echoClient.getClientStub().setServerBindingName("Echo1"); //指定使用"Echo1"对象
        std::cout << echoClient.echo("aaa");
        echoClient.getClientStub().setServerBindingName("Echo2"); //指定使用"Echo2"对象
        std::cout << echoClient.echo("bbb");
远程调用类中，函数的返回值与参数限制
    函数的参数类型可以为指针或引用，但不能是对指针的引用
    返回值类型不允许为指针或引用，要返回指针时，可返回智能指针对象，如std::auto_ptr<>或boost::shared_ptr<>
    通常自定义类是不能作为函数参数的，但也有解决办法，就是让你的自定义类支持序列化
    让自定义类支持序列化的方法：
        class MyClass
        {
            int myInteger;
            std::string myString;
            std::map<
                std::string,
                std::map<int,std::vector<int> > > myMap;
        };
        //
        template<typename Archive>
        void serialize(Archive &ar, MyClass &x)
        {
            ar & x.myInteger & x.myString & x.myMap;
        }
rcf接口支持继承或多重继承  
    //接口1
    RCF_BEGIN(I_A, "I_A")
        RCF_METHOD_V0(void, func1)
    RCF_END(I_Base)
    //接口2
    RCF_BEGIN(I_B, "I_B")
        RCF_METHOD_V0(void, func2)
    RCF_END(I_Base)
    // 单继承
    RCF_BEGIN_INHERITED(I_C, "I_C", I_A)
        RCF_METHOD_V0(void, func3)
    RCF_END(I_Base)
    // 多继承
    RCF_BEGIN_INHERITED_2(I_D, "I_D", I_A, I_B)
        RCF_METHOD_V0(void, func4)
    RCF_END(I_Base)
过滤器
    rcf支持指定"过滤器"，来对传输的消息进行加解密或压缩解压
    例如可以使用ssl过滤器来加密通信数据，使用zlib过滤器来压缩通信数据
    在服务器 - 客户端会话上安装加解密过滤器（传输过滤器）的过程由客户端发起
    客户端查询服务器以确定服务器是否支持给定的过滤器。
    如果服务器执行，则过滤器安装在传输的两端，并且通信恢复。
    ClientStub::requestTransportFilters()
    而压缩解压过滤器，不需要客户端提前跟服务端商定，
    ClientStub::setMessageFilters()
    编码消息将以描述已使用哪些过滤器的数据为前缀，从而允许服务器对消息进行解码
    如果服务器无法识别过滤器，则会将异常传回客户端。
    RCF自带的几个过滤器：
        两个用于压缩，基于Zlib，两个用于基于OpenSSL和Schannel的 SSL加密，
        以及两个基于Windows的Kerberos和NTLM协议过滤器。
        这些过滤器也可以相互链接以创建过滤器序列
    使用举例：
        参：https://blog.csdn.net/swartz_lubel/article/details/76423470
让rcf动态创建远程对象
    RcfServer该类允许用户将已有的类的单个实例公开到远程客户端
    但没法让客户端在服务器上动态的创建对象
    要想达到此目的，可以让服务端使用 ObjectFactoryService
    然后客户端就可以使用 ClientStub::createRemoteObject() ，
    让服务端动态的创建远程对象了
    不用担心服务端动态创建的对象的释放问题，
    当没有活动的客户端会话，并且在可配置的持续时间内未被访问后，
    服务端动态创建的对象将被回收（释放）。
    举例：
        服务端：
            //最多允许动态创建10个对象，没有连接，20s后，对象将释放
            RCF::ObjectFactoryServicePtr ofsPtr(new RCF::ObjectFactoryService(10, 20) );
            //指定要动态创建的对象类型
            ofsPtr->bind<I_Echo, Echo>();

            RCF::RcfServer server(endpoint);
            server.addService(ofsPtr);  //指定动态创建对象的工厂类
            server.start();
        客户端：
            RcfClient<I_Echo> client1(endpoint);
            bool ok = client1.getClientStub().createRemoteObject();  
            //动态创建对象后，才能使用对象方法

            RcfClient<I_Echo> client2(endpoint);
            client2.getClientStub().setToken( client1.getClientStub().getToken() );
            //client2将使用与client1相同的对象
            //通过ObjectFactoryService创建的对象，是有session标识的（相当于对象的名字）
            //这样的对象时可以被其它客户端使用的，
            //只要通过 client1.getClientStub().getToken()，获取session标识即可
            
            RcfClient<I_Echo> client3(endpoint);
            bool ok = client3.getClientStub().createRemoteSessionObject();
            //创建专属于client3的远程对象
rcf编译选项
    RCF_USE_BOOST_THREADS：利用Boost.Thread库进行互斥和线程生成功能。如果没有定义，RCF将使用自己的内部线程库。
    RCF_USE_BOOST_ASIO：利用Boost.Asio网络库。在非Windows平台上需要服务器端代码。
    RCF_USE_ZLIB：编译支持Zlib压缩。
    RCF_USE_OPENSSL：编译支持OpenSSL加密。
    RCF_USE_BOOST_SERIALIZATION：编译支持Boost.Serialization库。
    RCF_USE_SF_SERIALIZATION：编译支持RCF的内置序列化框架。
        如果既不定义RCF_USE_BOOST_SERIALIZATION也不RCF_USE_SF_SERIALIZATION定义自动定义。
    RCF_NO_AUTO_INIT_DEINIT：禁用RCF的自动初始化/去初始化设施。
        如果定义，用户将必须明确地调用RCF::init()并RCF::deinit()在适当的时间。
        特别地，当将RCF编译为DLL以避免过早初始化时，这是必要的。
    所有第三方构建依赖项（Boost.Threads，Boost.Serialization，Zlib，OpenSSL）都是可选的
服务端调用客户端    
    对于某些在服务端耗时的函数，异步调用是有必要的：
    让服务端先行返回，然后等数据处理完后，再调用客户端的方法，把数据返回给客户端
    为了让服务端能反过来调用客户端（的对象方法）
    可以让客户端也起一个 RcfServer，然后调用 RcfServer::createCallbackConnection()
    把客户端的服务信息告诉给服务端，
    服务端则在回调函数中，像普通的客户端那样，记录客户端提供的远程类
    
    客户端代码示例：
        //客户端支持回调
        RCF::RcfServer callbackServer(( RCF::TcpEndpoint() ));
        HelloWorldImpl helloWorld;  //用于被服务端调用的类
        callbackServer.bind<I_HelloWorld>(helloWorld);
        callbackServer.start();
        //客户端连接服务端
        RcfClient<I_HelloWorld> client( RCF::TcpEndpoint(50001) );
        RCF::createCallbackConnection(client, callbackServer);
    服务端代码：
        void onCallbackConnectionCreated(RCF::RcfSessionPtr sessionPtr,
                                         RCF::ClientTransportAutoPtr transportAutoPtr)
        {
            //像普通的客户端那样，建立到客户端的连接，并记录客户端提供的远程类
            typedef boost::shared_ptr< RcfClient<I_HelloWorld> > HelloWorldPtr;
            HelloWorldPtr helloWorldPtr( new RcfClient<I_HelloWorld>(transportAutoPtr) );
            RCF::Lock lock(gCallbackClientsMutex);
            gCallbackClients.push_back( helloWorldPtr );
        }
        int main()
        {
            RCF::RcfInitDeinit rcfInit;
            RCF::RcfServer server( RCF::TcpEndpoint(50001) );
            server.setOnCallbackConnectionCreated(  //指定相应客户端回调的函数
                    boost::bind(&onCallbackConnectionCreated, _1, _2) );
            server.start();

            for (std::size_t i=0; i<clients.size(); ++i)
            {
                HelloWorldPtr clientPtr = clients[i];
                clientPtr->Print("Hello World");
            }:qvim :q
            return 0;
        }