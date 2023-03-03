�Σ�https://blog.csdn.net/yuweiping5247/article/details/81386658
�Σ�https://blog.csdn.net/swartz_lubel/article/details/76423470
����rcf��
    rcfԴ�����кܶ��ļ���������hpp�ļ�
    ����rcfʱ��ֻҪ����һ�� RCF.hpp ����
�������������⣺
    rcf�ڲ�ʹ����boost
rcfʵ�ֵĹ��ܣ� 
    ��������ñ����෽��һ�������÷����������ķ���
rcf����˾�����
    #include <iostream>
    #include <RCF/RCF.hpp>
        
    //���������ڿͻ���Զ�̵��õ���
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
    
    //��PrintService��rcf����
    RCF_BEGIN(I_PrintService, "I_PrintService")  //RCF�ӿڶ��壬��������25����Ա����
        RCF_METHOD_V1(void, Print, const std::string &) //RCF_METHOD_ͨ��ǰ׺��V��ʾ����ֵvoid�� //1��ʾһ������
        RCF_METHOD_R1(std::string, echo, const std::string &) //R��return����ʾ�з���ֵ����void��
    RCF_END(I_PrintService)  //��Щ�����ն���Ϊ RcfClient<type>��
    
    //������
    int main(int argc, char **argv)
    {
        try
        {
            RCF::RcfInit rcfInit;  //��ʼ��RCF
            RCF::RcfServer server(RCF::TcpEndpoint("192.168.241.129", 500001)); 
            //����RCFԶ�̷����趨IP�Ͷ˿�,�������� RCF::TcpEndpoint(50001)
            //����ΪRCF::UdpEndpoint(50001)������ʹ��udpЭ��
            
            PrintService printService;
            server.bind<I_PrintService>(printService);  //�������
            
            server.start();  //�������񣬿�ʼ����������������ǰ�߳�
            std::cin.get();  //��ǰ�̲߳����˳�������ǰ�����󶨵��������ͷ���
            //�� server.startInThisThread();
        }
        catch(const RCF::Exception &e)
        {
            std::cout << "Error: " << e.getErrorMessage() << std::endl;
        }
        return 0;
    }    
rcf�ͻ��˾�����    
    #include <iostream>
    #include <RCF/RCF.hpp>
    
    //Զ�����rcf����
    RCF_BEGIN(I_PrintService, "I_PrintService")  //RCF�ӿ�
        RCF_METHOD_V1(void, Print, const std::string &)
        RCF_METHOD_R1(std::string, echo, const std::string &)
    RCF_END(I_PrintService)
     
    //������
    int main(int argc, char **argv)
    {
        try
        {
            RCF::RcfInit rcfInit;  //��ʼ��RCF
            RcfClient<I_PrintService> client(RCF::TcpEndpoint("192.168.241.129", 500001)); //�����ͻ��˲�����

            //����Զ����ķ���
            client.Print("Hello World");   
            //RCF::Twoway(����ʱ��Ĭ��ʹ�øò���)�ͻ��˴�������еĲ�����һ����־������RCF����˫��ͻ��˵���;
            //�ͻ��˷������󣬵ȴ���Ӧ������ڿ����õĳ���ʱ����û���յ���������׳��쳣��
            //��һ��ѡ����ʹ��RCF::Oneway; �������󣬵���������������Ӧ���ͻ��˴�����ý�����������Ȩ���ظ��û���
            std::string s = client.echo(RCF::Twoway, "what's up");
            std::cout << s << std::endl;
        }
        catch(const RCF::Exception & e)
        {
            std::cout << "Error: " << e.getErrorMessage() << std::endl;
        }
     
        return 0;
    }
rcf����˰󶨶���
    �󶨶���ķ�ʽ�ж��֣�
        ֱ�Ӱ󶨶���
            Echo echo;
            server.bind<I_Echo>(echo);
        �� std::auto_ptr<>...
            std::auto_ptr<Echo> echoAutoPtr(new Echo());
            server.bind<I_Echo>(echoAutoPtr);
        �� boost::shared_ptr<>...
            boost::shared_ptr<Echo> echoPtr(new Echo());
            server.bind<I_Echo>(echoPtr);
        �� boost::weak_ptr<>...
            boost::weak_ptr<Echo> echoWeakPtr(echoPtr);
            server.bind<I_Echo>(echoWeakPtr);
    ����ͬʱ�󶨶������Ϊÿ������ָ����ͬ�����֣�
        RcfServer server(endpoint);
        // �󶨶���1
        Echo echo1;
        server.bind<I_Echo>(echo1, "Echo1");
        // �󶨶���2
        Echo echo2;
        server.bind<I_Echo>(echo2, "Echo2");
        server.start();
        //�ͻ���ʹ��ʱ��
        RcfClient<I_Echo> echoClient(endpoint);
        echoClient.getClientStub().setServerBindingName("Echo1"); //ָ��ʹ��"Echo1"����
        std::cout << echoClient.echo("aaa");
        echoClient.getClientStub().setServerBindingName("Echo2"); //ָ��ʹ��"Echo2"����
        std::cout << echoClient.echo("bbb");
Զ�̵������У������ķ���ֵ���������
    �����Ĳ������Ϳ���Ϊָ������ã��������Ƕ�ָ�������
    ����ֵ���Ͳ�����Ϊָ������ã�Ҫ����ָ��ʱ���ɷ�������ָ�������std::auto_ptr<>��boost::shared_ptr<>
    ͨ���Զ������ǲ�����Ϊ���������ģ���Ҳ�н���취������������Զ�����֧�����л�
    ���Զ�����֧�����л��ķ�����
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
rcf�ӿ�֧�ּ̳л���ؼ̳�  
    //�ӿ�1
    RCF_BEGIN(I_A, "I_A")
        RCF_METHOD_V0(void, func1)
    RCF_END(I_Base)
    //�ӿ�2
    RCF_BEGIN(I_B, "I_B")
        RCF_METHOD_V0(void, func2)
    RCF_END(I_Base)
    // ���̳�
    RCF_BEGIN_INHERITED(I_C, "I_C", I_A)
        RCF_METHOD_V0(void, func3)
    RCF_END(I_Base)
    // ��̳�
    RCF_BEGIN_INHERITED_2(I_D, "I_D", I_A, I_B)
        RCF_METHOD_V0(void, func4)
    RCF_END(I_Base)
������
    rcf֧��ָ��"������"�����Դ������Ϣ���мӽ��ܻ�ѹ����ѹ
    �������ʹ��ssl������������ͨ�����ݣ�ʹ��zlib��������ѹ��ͨ������
    �ڷ����� - �ͻ��˻Ự�ϰ�װ�ӽ��ܹ�������������������Ĺ����ɿͻ��˷���
    �ͻ��˲�ѯ��������ȷ���������Ƿ�֧�ָ����Ĺ�������
    ���������ִ�У����������װ�ڴ�������ˣ�����ͨ�Żָ���
    ClientStub::requestTransportFilters()
    ��ѹ����ѹ������������Ҫ�ͻ�����ǰ��������̶���
    ClientStub::setMessageFilters()
    ������Ϣ����������ʹ����Щ������������Ϊǰ׺���Ӷ��������������Ϣ���н���
    ����������޷�ʶ�����������Ὣ�쳣���ؿͻ��ˡ�
    RCF�Դ��ļ�����������
        ��������ѹ��������Zlib���������ڻ���OpenSSL��Schannel�� SSL���ܣ�
        �Լ���������Windows��Kerberos��NTLMЭ���������
        ��Щ������Ҳ�����໥�����Դ�������������
    ʹ�þ�����
        �Σ�https://blog.csdn.net/swartz_lubel/article/details/76423470
��rcf��̬����Զ�̶���
    RcfServer���������û������е���ĵ���ʵ��������Զ�̿ͻ���
    ��û���ÿͻ����ڷ������϶�̬�Ĵ�������
    Ҫ��ﵽ��Ŀ�ģ������÷����ʹ�� ObjectFactoryService
    Ȼ��ͻ��˾Ϳ���ʹ�� ClientStub::createRemoteObject() ��
    �÷���˶�̬�Ĵ���Զ�̶�����
    ���õ��ķ���˶�̬�����Ķ�����ͷ����⣬
    ��û�л�Ŀͻ��˻Ự�������ڿ����õĳ���ʱ����δ�����ʺ�
    ����˶�̬�����Ķ��󽫱����գ��ͷţ���
    ������
        ����ˣ�
            //�������̬����10������û�����ӣ�20s�󣬶����ͷ�
            RCF::ObjectFactoryServicePtr ofsPtr(new RCF::ObjectFactoryService(10, 20) );
            //ָ��Ҫ��̬�����Ķ�������
            ofsPtr->bind<I_Echo, Echo>();

            RCF::RcfServer server(endpoint);
            server.addService(ofsPtr);  //ָ����̬��������Ĺ�����
            server.start();
        �ͻ��ˣ�
            RcfClient<I_Echo> client1(endpoint);
            bool ok = client1.getClientStub().createRemoteObject();  
            //��̬��������󣬲���ʹ�ö��󷽷�

            RcfClient<I_Echo> client2(endpoint);
            client2.getClientStub().setToken( client1.getClientStub().getToken() );
            //client2��ʹ����client1��ͬ�Ķ���
            //ͨ��ObjectFactoryService�����Ķ�������session��ʶ�ģ��൱�ڶ�������֣�
            //�����Ķ���ʱ���Ա������ͻ���ʹ�õģ�
            //ֻҪͨ�� client1.getClientStub().getToken()����ȡsession��ʶ����
            
            RcfClient<I_Echo> client3(endpoint);
            bool ok = client3.getClientStub().createRemoteSessionObject();
            //����ר����client3��Զ�̶���
rcf����ѡ��
    RCF_USE_BOOST_THREADS������Boost.Thread����л�����߳����ɹ��ܡ����û�ж��壬RCF��ʹ���Լ����ڲ��߳̿⡣
    RCF_USE_BOOST_ASIO������Boost.Asio����⡣�ڷ�Windowsƽ̨����Ҫ�������˴��롣
    RCF_USE_ZLIB������֧��Zlibѹ����
    RCF_USE_OPENSSL������֧��OpenSSL���ܡ�
    RCF_USE_BOOST_SERIALIZATION������֧��Boost.Serialization�⡣
    RCF_USE_SF_SERIALIZATION������֧��RCF���������л���ܡ�
        ����Ȳ�����RCF_USE_BOOST_SERIALIZATIONҲ��RCF_USE_SF_SERIALIZATION�����Զ����塣
    RCF_NO_AUTO_INIT_DEINIT������RCF���Զ���ʼ��/ȥ��ʼ����ʩ��
        ������壬�û���������ȷ�ص���RCF::init()��RCF::deinit()���ʵ���ʱ�䡣
        �ر�أ�����RCF����ΪDLL�Ա�������ʼ��ʱ�����Ǳ�Ҫ�ġ�
    ���е��������������Boost.Threads��Boost.Serialization��Zlib��OpenSSL�����ǿ�ѡ��
����˵��ÿͻ���    
    ����ĳЩ�ڷ���˺�ʱ�ĺ������첽�������б�Ҫ�ģ�
    �÷�������з��أ�Ȼ������ݴ�������ٵ��ÿͻ��˵ķ����������ݷ��ظ��ͻ���
    Ϊ���÷�����ܷ��������ÿͻ��ˣ��Ķ��󷽷���
    �����ÿͻ���Ҳ��һ�� RcfServer��Ȼ����� RcfServer::createCallbackConnection()
    �ѿͻ��˵ķ�����Ϣ���߸�����ˣ�
    ��������ڻص������У�����ͨ�Ŀͻ�����������¼�ͻ����ṩ��Զ����
    
    �ͻ��˴���ʾ����
        //�ͻ���֧�ֻص�
        RCF::RcfServer callbackServer(( RCF::TcpEndpoint() ));
        HelloWorldImpl helloWorld;  //���ڱ�����˵��õ���
        callbackServer.bind<I_HelloWorld>(helloWorld);
        callbackServer.start();
        //�ͻ������ӷ����
        RcfClient<I_HelloWorld> client( RCF::TcpEndpoint(50001) );
        RCF::createCallbackConnection(client, callbackServer);
    ����˴��룺
        void onCallbackConnectionCreated(RCF::RcfSessionPtr sessionPtr,
                                         RCF::ClientTransportAutoPtr transportAutoPtr)
        {
            //����ͨ�Ŀͻ����������������ͻ��˵����ӣ�����¼�ͻ����ṩ��Զ����
            typedef boost::shared_ptr< RcfClient<I_HelloWorld> > HelloWorldPtr;
            HelloWorldPtr helloWorldPtr( new RcfClient<I_HelloWorld>(transportAutoPtr) );
            RCF::Lock lock(gCallbackClientsMutex);
            gCallbackClients.push_back( helloWorldPtr );
        }
        int main()
        {
            RCF::RcfInitDeinit rcfInit;
            RCF::RcfServer server( RCF::TcpEndpoint(50001) );
            server.setOnCallbackConnectionCreated(  //ָ����Ӧ�ͻ��˻ص��ĺ���
                    boost::bind(&onCallbackConnectionCreated, _1, _2) );
            server.start();

            for (std::size_t i=0; i<clients.size(); ++i)
            {
                HelloWorldPtr clientPtr = clients[i];
                clientPtr->Print("Hello World");
            }:qvim :q
            return 0;
        }