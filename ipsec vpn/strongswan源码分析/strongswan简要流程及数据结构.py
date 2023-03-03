整体流程图参：file://../imgs/strongswan流程图.png
charon.c：main <<file://charon中的结构与变量.h>>
    library_init(NULL, "charon")  <<file://library中的结构与变量.h>> <<file://library.c.py>> //在strongswan目录下
        private_library_t *this;
        printf_hook_t *pfh;
        初始化this
        global library_t *lib = &this->public;
        threads_init    <<file://thread中的结构与变量.h>>  //定义了线程数据结构
        utils_init      <<file://utils中的结构与变量.h>>   //条件和互斥
            atomics_init   <<file://atomics中的结构与变量.h>>
            strerror_init  <<file://strerror中的结构与变量.h>>
        arrays_init     <<file://array中的结构与变量.h>>
        backtrace_init  <<file://backtrace中的结构与变量.h>>
            '#ifdef HAVE_DBGHELP
            	SymSetOptions(SYMOPT_LOAD_LINES);
                SymInitialize(GetCurrentProcess(), NULL, TRUE);
                dbghelp_mutex = mutex_create(MUTEX_TYPE_DEFAULT);
            '#elif defined(HAVE_DLADDR) || defined(HAVE_BFD_H)
                bfd_init();
                bfds = hashtable_create((hashtable_hash_t)bfd_hash,
                                        (hashtable_equals_t)bfd_equals, 8);
                bfd_mutex = mutex_create(MUTEX_TYPE_DEFAULT);
            '#else
            '#endif
        pfh = printf_hook_create();  <<file://printf_hook_glibc中的结构与变量.h>>
        this->public.printf_hook = pfh;
        pfh->add_handler(...)           //打印钩子关联打印方法
            第2个参数传入char描述符，第3个参数传输函数指针
            描述符-'A' 作为索引存放在printf_hooks数组中（需<=57）
            使用register_printf_function注册该函数
                目的是实现支持类似于 printf("%B",bit_string); 这样的功能
            猜测是实现让printf支持如下占位符
                %b  打印mem信息
                %B  打印chunk信息
                %H  打印host信息
                %N  打印enum信息
                %T  打印time信息
                %V  打印time_delta信息
                %Y  打印identification信息
                %R  打印traffic_selector信息
                %P  打印proposal信息
        this->objects = hashtable_create(hash,equals, 4);  <<file://hashtable中的结构与变量.h>>
            第1个参数时计算哈希函数，第2个参数时判断相等函数，
            根据第3个参数，找到一个大于该参数的、最小的、符合2^n的数
            并根据这个2^n，申请 2^n * sizeof(pair_t*)，存给 table 结构体成员
        this->public.settings = settings_create(NULL);    <<file://settings中的结构与变量.h>>  
            private_settings_t *this = settings_create_base();
            load_files(this, NULL, FALSE);
            return &this->public;
        lib->settings->add_fallback(lib->settings, "charon", "libstrongswan");    //给charon节点添加引用，引用节点名为libstrongswan（永久）
            获得"charon"节点
            在节点的引用者（references）中，加入"libstrongswan"（永久）
        # resolve hosts by DNS name
        this->public.hosts = host_resolver_create();        <<file://host_resolver中的结构与变量.h>>
            对非本文件中变量的影响：无
        # Proposal keywords registry
        this->public.proposal = proposal_keywords_create(); <<file://proposal_keywords中的结构与变量.h>>
            对非本文件中变量的影响：无
        # POSIX capability dropping
        this->public.caps = capabilities_create();          <<file://capabilities中的结构与变量.h>>
            对非本文件中变量的影响：无
        # crypto algorithm registry and factory
        this->public.crypto = crypto_factory_create();      <<file://crypto_factory中的结构与变量.h>>
            对非本文件中变量的影响：无
        # credential constructor registry and factory
        this->public.creds = credential_factory_create();   <<file://credential_factory中的结构与变量.h>> ??
            对非本文件中变量的影响：无
        # Manager for the credential set backends
        this->public.credmgr = credential_manager_create(); <<file://credential_manager中的结构与变量.h>> ??   
            对非本文件中变量的影响：无
        # Credential encoding registry and factory
        this->public.encoding = cred_encoding_create();     <<file://cred_encoding中的结构与变量.h>>   
            对非本文件中变量的影响：无
        # URL fetching facility
        this->public.fetcher = fetcher_manager_create();    <<file://fetcher_manager中的结构与变量.h>>
            对非本文件中变量的影响：无
        # Manager for DNS resolvers
        this->public.resolver = resolver_manager_create();  <<file://resolver_manager中的结构与变量.h>>
            对非本文件中变量的影响：无
        # database construction factory
        this->public.db = database_factory_create();        <<file://database_factory中的结构与变量.h>>
            对非本文件中变量的影响：无
        # process jobs using a thread pool  //processor是个处理器，它管理多个工作线程
        # 有了该进程模型，只要把job扔给它就行了，它会放到队列中并自动调用线程进行处理，
        # 当然也可让它直接执行某job而不放入队列（阻塞式）
        this->public.processor = processor_create();        <<file://processor中的结构与变量.h>>  
            对非本文件中变量的影响：无
        # schedule jobs，任务调度器，它会维护一个event队列，并自动调用processor执行这些定时任务
        # 该调度器初始化的时候，就把一个schedule任务提交给processor了（让自己先工作起来）
        this->public.scheduler = scheduler_create();        <<file://scheduler中的结构与变量.h>>
            对非本文件中变量的影响：lib->processor->queue_job
        # File descriptor monitoring， 文件监视器（注意socket也是文件）
        this->public.watcher = watcher_create();            <<file://watcher中的结构与变量.h>>
            对非本文件中变量的影响：无
        # Streams and Services
        this->public.streams = stream_manager_create();     <<file://stream_manager中的结构与变量.h>>
            对非本文件中变量的影响：无
        # plugin loading facility ， 先初始化插件管理器
        this->public.plugins = plugin_loader_create();      <<file://plugin_loader中的结构与变量.h>>
            对非本文件中变量的影响：无
            this初始化：
                .public = {
                    .add_static_features = _add_static_features,
                    .load = _load_plugins,
                    .add_path = _add_path,
                    .reload = _reload,
                    .unload = _unload,
                    .create_plugin_enumerator = _create_plugin_enumerator,
                    .has_feature = _has_feature,
                    .loaded_plugins = _loaded_plugins,
                    .status = _status,
                    .destroy = _destroy
                },
                .plugins = linked_list_create(),
                .loaded = linked_list_create(),
                .features = hashtable_create(
                                    (hashtable_hash_t)registered_feature_hash,
                                    (hashtable_equals_t)registered_feature_equals, 64)
        # 黎赫运算初始化
        diffie_hellman_init
    libcharon_init() <<file://daemon中的结构域变量.h>>  //在libcharon目录下
        private_daemon_t *this;
        this = daemon_create()   #这里可见libcharon是作为一个守护服务而存在的，它提供 logger、bus、eap、xauth等功能
            创建 private_daemon_t 堆内存
            赋初值
                # 对象引用计数
                this.ref = 1
                # The signaling bus. 信号总线（监听者模式）
                this.public.bus = bus_create();                         <<file://bus中的结构与变量.h>>
                    对非本文件中变量的影响：lib->credmgr->set_hook
                    对bus上的alerts添加身份认证管理钩子函数hook_creds（从而能识别bus上的身份认证相关的alerts）
                    bus上注册了许多监听者，各自监听自己感兴趣的事件
                    当调用bus上的方法时，方法内部会依次调用各监听者的相应方法
                    注：注册的监听者可以是一次性的，当它被执行过依次之后，就会从监听者队列中被移除掉
                    另外需注意的是，bus上的log方法有些特别，它不是使用监听者队列，而是使用自己的loger队列
                # A list of installed loggers (as logger_entry_t*)
                this.loggers = linked_list_create();                    <<file://linked_list中的结构与变量.h>>
                    对非本文件中变量的影响：无
                this.mutex = mutex_create()
                # Kernel interface to communicate with kernel，处理与内核的通信，如SA和策略管理，接口和IP地址管理
                this->public.kernel = kernel_interface_create();        <<file://kernel_interface中的结构与变量.h>>
                    对非本文件中变量的影响：无
                # Manager for IKE configuration attributes
                this->public.attributes = attribute_manager_create();   <<file://attribute_manager中的结构与变量.h>>
                    对非本文件中变量的影响：无
                # Controller to control the daemon
                this->public.controller = controller_create();          <<file://controller中的结构与变量.h>>
                    对非本文件中变量的影响：无
                    提供了简单的API，供各种插件访问和控制守护进程（例如：初始化IKE_SA等）,
                    相当于为daemon提供了一个对外的操作面板
                # EAP manager to maintain registered EAP methods
                this->public.eap = eap_manager_create();                <<file://eap_manager中的结构与变量.h>>
                    对非本文件中变量的影响：无
                # XAuth manager to maintain registered XAuth methods
                this->public.xauth = xauth_manager_create();            <<file://xauth_manager中的结构与变量.h>>
                    对非本文件中变量的影响：无
                    参： file://../strongswan/xauth.txt
                # Manager for the different configuration backends. 为了支持vici、stroke、uci等等不同的终端
                this->public.backends = backend_manager_create();       <<file://backend_manager中的结构与变量.h>>
                    对非本文件中变量的影响：无
                    可向里注册vici等终端，调用backends的读配置的相关方法时，内部使用注册的终端进行真正的操作
                    注册的终端实现了backend_t接口，
                    注：swanctl	是通过 vici 接口进行通信的配置和控制实用程序，vici 插件提供了多功能 IKE 控制接口
                # Socket manager instance，socket管理器，可向里注册socket实现类，并通过调用实现类实现包的收发
                this->public.socket = socket_manager_create();          <<file://socket_manager中的结构与变量.h>>
                    对非本文件中变量的影响：无
                # Manager for triggering policies, called traps
                this->public.traps = trap_manager_create();             <<file://trap_manager中的结构与变量.h>>
                    对非本文件中变量的影响：charon->bus->add_listener
                # Manager for shunt PASS|DROP policies
                this->public.shunts = shunt_manager_create();           <<file://shunt_manager中的结构与变量.h>>
                    对非本文件中变量的影响：无
                # Manager for IKE redirect providers
                this->public.redirect = redirect_manager_create();      <<file://redirect_manager中的结构与变量.h>>
                    对非本文件中变量的影响：无
                # Handler for kernel events，监听和处理内核事件
                this->kernel_handler = kernel_handler_create();         <<file://kernel_handler中的结构与变量.h>>
                    对非本文件中变量的影响：charon->kernel->add_listener
                ... 
                global daemon_t *charon = this->public
                    charon文件全局变量指向 public
            返回this
            功能小结：
                对外：
                    提供总线，通过调用总线接口，完成相应处理
                    提供控制面板，从而提供了简单的API，供各种插件访问和控制守护进程
                内部：
                    管理与内核的通信
                    管理数据包的收发
                    管理数据包的封装
                    支持xauth方式身份认证
                    管理IKE配置属性
                    。。。
        srandom
        dbg_old = dbg;  //函数指针变量
        dbg = dbg_bus;
    初始化局部变量 level_t levels[DBG_MAX] 值为 LEVEL_CTRL
        设置loglevel
        	LEVEL_SILENT = -1,  // absolutely silent 
            LEVEL_AUDIT   = 0,  // most important auditing logs */
            LEVEL_CTRL    = 1,  // control flow
            LEVEL_DIAG    = 2,  // diagnose problems 
            LEVEL_RAW     = 3,  // raw binary blobs 
            LEVEL_PRIVATE = 4,  // including sensitive data (private keys) 
    处理输入参数，支持的输入参数包括：
        use-syslog、debug-dmn、debug-mgr、debug-ike、debug-chd、debug-job
        debug-cfg、debug-dnl、debug-net、debug-asn、debug-enc、debug-tnc
        debugimc、debug-imv、debug-pts、debug-tls、debug-esp、debug-lib
        上面这些参数，除了第1个外，其它的都需要跟参数值(即opt=value)
        参数值放在局部变量 level_t levels[DBG_MAX] 对应位置
    lookup_uid_gid （user id、group id）
        读配置项 charon.user（默认为NULL）和 charon.group（默认为NULL）
        如果读到不为空，则调用 lib->caps->resolve_uid / lib->caps->resolve_gid
        如果调用函数返回值为失败，则本函数返回失败，并导致main函数退出
        注：lib->caps 在 library_init 中被赋值
    根据 level_t levels[DBG_MAX] 设置日志级别
        影响 private_daemon_t 的成员变量 this->levels 和 this->to_stderr
    charon->load_loggers    //让deamon.bus支持了log方法
        根据配置文件，默认创建 sys_logger 和 file_logger，记录在private_daemon_t的logger成员中，并为其设置错误输出级别
        charon->bus->add_logger(sys_logger->logger)
        charon->bus->add_logger(file_logger->logger)
    uname(&utsname) 
    charon->initialize   file://charon初始化时加载的默认插件.txt
        创建 plugin_feature_t features[]   //file://plugin_feature_t.py        
        <参 file://../imgs/strongswan插件机制结构关系2.png> 
        <参：file://plugin_feature_t.py> 
        <参：file://../imgs/plugin_loader的plugins赋值.png>
        lib->plugins->add_static_features(...)  
            plugin_t *plugin = static_features_create(...)
                this = new static_features_t;
                函数指针成员初始化
                this.name = 参数传来的名字
                this.features = clone 参数传来的features
                return this.public  //static_features_t.public is typeof plugin_t
            entry = new plugin_entry_t
                entry.plugin = plugin
                entry.features =  linked_list_create()
            lib->plugins->plugsin->insert_last(entry)
            lib->plugins->register_features(entry)
                遍历 entry.plugin 中的 features
                    如果是 FEATURE_PROVIDE
                        检查 lib->plugins->features 中是否已存在该feature
                            如果不存在
                                registered = new registered_feature_t
                                    registered.feature = feature
                                    registered.plugins = linked_list_create()
                                lib->plugins->features->put(registered)
                                provided = new provided_feature_t
                                    provided.entry = entry
                                    provided.feature = feature
                                    provided.reg = reg  //reg 是注册feature，默认为空
                                    provided.dependencies = count - i
                                registered->plugins->insert_last（provided）
                                entry->features->insert_last（provide）
                    如果是 FEATURE_REGISTER 或 FEATURE_CALLBACK
                        将 feature 缓存到 reg
                    如果以上都不是
                        结束遍历
        lib->plugins->load(plugins)
           参：<file://plugin_loader分析.py> <file://plugin_feature中的结构与变量.h>
           &plugins值
           plugins = '''aes des rc2 sha2 sha1 md5 mgf1 random nonce x509 revocation 
                        constraints pubkey pkcs1 pkcs7 pkcs8 pkcs12 pgp dnskey sshkey 
                        pem openssl fips-prf gmp curve25519 xcbc cmac hmac attr 
                        kernel-netlink resolve socket-default stroke vici updown 
                        eap-identity eap-md5 eap-mschapv2 eap-dynamic eap-radius 
                        eap-tls eap-ttls eap-peap eap-tnc xauth-generic xauth-eap 
                        tnc-tnccs counters'''
        lib->processor->queue_job(job=start_action_job_create())
            参数job=start_action_job_create:
                创建并初始化 private_start_action_job_t，返回public部分
                    private_start_action_job_t *this;
                    this.public.job_interface = {
                                .execute = _execute,
                                .get_priority = _get_priority,
                                .destroy = _destroy
                                }   
            this->jobs[job->get_priority]->insert_last(job)
            this->job_added->signal(this->job_added); //触发条件变量
                内部调用pthread_cond_signal()  //这是个pthread.h中提供的系统函数
                    pthread_cond_signal函数的作用是发送一个信号给另外一个正在处于阻塞等待状态的线程,
                    使其脱离阻塞状态,继续执行.
                    pthread_cond_wait() 用于阻塞当前线程，
                    等待别的线程使用pthread_cond_signal()或pthread_cond_broadcast来唤醒它。
    check_pidfile
    !lib->caps->drop
    设置信号处理函数  响应SIGSEGV、SIGILL、SIGBUS信号，并设置只有当前线程（主线程）来处理这些信号
    charon->start(charon)
        lib->processor->set_threads(count)  //设置开启线程数，count从配置文件获取，默认为16
            进入到processor.c文件中
                this->desired_threads = count;
                for 0 : count
                    worker = new worker_thread_t
                        worker.processor = this
                        worker.thread = thread_create(process_jobs,worker)
                    this->threads->insert_last(worker)
                    this->total_threads++;
                this->job_added->broadcast  //广播表明添加job， job_added为condvar_t*类型 
        run_scripts(verb="start")
             lib->settings->create_key_value_enumerator("charon.verb-scripts")  //用以枚举配置项，默认为空
             当枚举器为空时，后面的代码没有被执行
    run()
        设置线程阻塞SIGINT、SIGHUP、SIGTERM这三个信号
        阻塞等待上述信号
            如果接收到信号SIGHUP（挂起信号）：
            如果接收到信号SIGINT（中断信号）：
            如果接收到信号SIGTERM（终止信号）：
            
processor.c : process_jobs线程            
    参：file://关于processor、worker、job等.py
    
start_action_job_create的execute函数：
    参：file://关于processor、worker、job等.py
    
charon框架综述
https://peiyake.com/wiki/strongswan/index.html#charon%E6%A1%86%E6%9E%B6
    charon的工作机制：
    IKE_SA Manager从后端Backends获取配置信息，并根据配置信息初始化IKE_SA。
    IKE_SA的初始化包括：
        构建IKE_SA实例，交付给处理器（Processor）、调度器（Scheduler），
        根据IKE协议执行报文构建发送（sender）或者接收（receiver）报文并解析。
        IKE_SA协商成功后，创建对应的CHILD_SA，
        同时调用内核接口（Kernel Interface）将相关信息下发到内核，
        隧道建立成功后，根据配置转入状态监控（Rekey等）。
        以上所有过程对各个阶段的事件交付总线（Bus），由总线确定事件的流向。
        总之，charon的核心任务是管理IPSec的SA，所以业务逻辑核心是IKE_SA Manager，
        其它的模块都是为其服务的。    