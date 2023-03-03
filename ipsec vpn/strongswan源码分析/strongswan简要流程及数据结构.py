��������ͼ�Σ�file://../imgs/strongswan����ͼ.png
charon.c��main <<file://charon�еĽṹ�����.h>>
    library_init(NULL, "charon")  <<file://library�еĽṹ�����.h>> <<file://library.c.py>> //��strongswanĿ¼��
        private_library_t *this;
        printf_hook_t *pfh;
        ��ʼ��this
        global library_t *lib = &this->public;
        threads_init    <<file://thread�еĽṹ�����.h>>  //�������߳����ݽṹ
        utils_init      <<file://utils�еĽṹ�����.h>>   //�����ͻ���
            atomics_init   <<file://atomics�еĽṹ�����.h>>
            strerror_init  <<file://strerror�еĽṹ�����.h>>
        arrays_init     <<file://array�еĽṹ�����.h>>
        backtrace_init  <<file://backtrace�еĽṹ�����.h>>
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
        pfh = printf_hook_create();  <<file://printf_hook_glibc�еĽṹ�����.h>>
        this->public.printf_hook = pfh;
        pfh->add_handler(...)           //��ӡ���ӹ�����ӡ����
            ��2����������char����������3���������亯��ָ��
            ������-'A' ��Ϊ���������printf_hooks�����У���<=57��
            ʹ��register_printf_functionע��ú���
                Ŀ����ʵ��֧�������� printf("%B",bit_string); �����Ĺ���
            �²���ʵ����printf֧������ռλ��
                %b  ��ӡmem��Ϣ
                %B  ��ӡchunk��Ϣ
                %H  ��ӡhost��Ϣ
                %N  ��ӡenum��Ϣ
                %T  ��ӡtime��Ϣ
                %V  ��ӡtime_delta��Ϣ
                %Y  ��ӡidentification��Ϣ
                %R  ��ӡtraffic_selector��Ϣ
                %P  ��ӡproposal��Ϣ
        this->objects = hashtable_create(hash,equals, 4);  <<file://hashtable�еĽṹ�����.h>>
            ��1������ʱ�����ϣ��������2������ʱ�ж���Ⱥ�����
            ���ݵ�3���������ҵ�һ�����ڸò����ġ���С�ġ�����2^n����
            ���������2^n������ 2^n * sizeof(pair_t*)����� table �ṹ���Ա
        this->public.settings = settings_create(NULL);    <<file://settings�еĽṹ�����.h>>  
            private_settings_t *this = settings_create_base();
            load_files(this, NULL, FALSE);
            return &this->public;
        lib->settings->add_fallback(lib->settings, "charon", "libstrongswan");    //��charon�ڵ�������ã����ýڵ���Ϊlibstrongswan�����ã�
            ���"charon"�ڵ�
            �ڽڵ�������ߣ�references���У�����"libstrongswan"�����ã�
        # resolve hosts by DNS name
        this->public.hosts = host_resolver_create();        <<file://host_resolver�еĽṹ�����.h>>
            �ԷǱ��ļ��б�����Ӱ�죺��
        # Proposal keywords registry
        this->public.proposal = proposal_keywords_create(); <<file://proposal_keywords�еĽṹ�����.h>>
            �ԷǱ��ļ��б�����Ӱ�죺��
        # POSIX capability dropping
        this->public.caps = capabilities_create();          <<file://capabilities�еĽṹ�����.h>>
            �ԷǱ��ļ��б�����Ӱ�죺��
        # crypto algorithm registry and factory
        this->public.crypto = crypto_factory_create();      <<file://crypto_factory�еĽṹ�����.h>>
            �ԷǱ��ļ��б�����Ӱ�죺��
        # credential constructor registry and factory
        this->public.creds = credential_factory_create();   <<file://credential_factory�еĽṹ�����.h>> ??
            �ԷǱ��ļ��б�����Ӱ�죺��
        # Manager for the credential set backends
        this->public.credmgr = credential_manager_create(); <<file://credential_manager�еĽṹ�����.h>> ??   
            �ԷǱ��ļ��б�����Ӱ�죺��
        # Credential encoding registry and factory
        this->public.encoding = cred_encoding_create();     <<file://cred_encoding�еĽṹ�����.h>>   
            �ԷǱ��ļ��б�����Ӱ�죺��
        # URL fetching facility
        this->public.fetcher = fetcher_manager_create();    <<file://fetcher_manager�еĽṹ�����.h>>
            �ԷǱ��ļ��б�����Ӱ�죺��
        # Manager for DNS resolvers
        this->public.resolver = resolver_manager_create();  <<file://resolver_manager�еĽṹ�����.h>>
            �ԷǱ��ļ��б�����Ӱ�죺��
        # database construction factory
        this->public.db = database_factory_create();        <<file://database_factory�еĽṹ�����.h>>
            �ԷǱ��ļ��б�����Ӱ�죺��
        # process jobs using a thread pool  //processor�Ǹ����������������������߳�
        # ���˸ý���ģ�ͣ�ֻҪ��job�Ӹ��������ˣ�����ŵ������в��Զ������߳̽��д���
        # ��ȻҲ������ֱ��ִ��ĳjob����������У�����ʽ��
        this->public.processor = processor_create();        <<file://processor�еĽṹ�����.h>>  
            �ԷǱ��ļ��б�����Ӱ�죺��
        # schedule jobs�����������������ά��һ��event���У����Զ�����processorִ����Щ��ʱ����
        # �õ�������ʼ����ʱ�򣬾Ͱ�һ��schedule�����ύ��processor�ˣ����Լ��ȹ���������
        this->public.scheduler = scheduler_create();        <<file://scheduler�еĽṹ�����.h>>
            �ԷǱ��ļ��б�����Ӱ�죺lib->processor->queue_job
        # File descriptor monitoring�� �ļ���������ע��socketҲ���ļ���
        this->public.watcher = watcher_create();            <<file://watcher�еĽṹ�����.h>>
            �ԷǱ��ļ��б�����Ӱ�죺��
        # Streams and Services
        this->public.streams = stream_manager_create();     <<file://stream_manager�еĽṹ�����.h>>
            �ԷǱ��ļ��б�����Ӱ�죺��
        # plugin loading facility �� �ȳ�ʼ�����������
        this->public.plugins = plugin_loader_create();      <<file://plugin_loader�еĽṹ�����.h>>
            �ԷǱ��ļ��б�����Ӱ�죺��
            this��ʼ����
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
        # ��������ʼ��
        diffie_hellman_init
    libcharon_init() <<file://daemon�еĽṹ�����.h>>  //��libcharonĿ¼��
        private_daemon_t *this;
        this = daemon_create()   #����ɼ�libcharon����Ϊһ���ػ���������ڵģ����ṩ logger��bus��eap��xauth�ȹ���
            ���� private_daemon_t ���ڴ�
            ����ֵ
                # �������ü���
                this.ref = 1
                # The signaling bus. �ź����ߣ�������ģʽ��
                this.public.bus = bus_create();                         <<file://bus�еĽṹ�����.h>>
                    �ԷǱ��ļ��б�����Ӱ�죺lib->credmgr->set_hook
                    ��bus�ϵ�alerts��������֤�����Ӻ���hook_creds���Ӷ���ʶ��bus�ϵ������֤��ص�alerts��
                    bus��ע�����������ߣ����Լ����Լ�����Ȥ���¼�
                    ������bus�ϵķ���ʱ�������ڲ������ε��ø������ߵ���Ӧ����
                    ע��ע��ļ����߿�����һ���Եģ�������ִ�й�����֮�󣬾ͻ�Ӽ����߶����б��Ƴ���
                    ������ע����ǣ�bus�ϵ�log������Щ�ر�������ʹ�ü����߶��У�����ʹ���Լ���loger����
                # A list of installed loggers (as logger_entry_t*)
                this.loggers = linked_list_create();                    <<file://linked_list�еĽṹ�����.h>>
                    �ԷǱ��ļ��б�����Ӱ�죺��
                this.mutex = mutex_create()
                # Kernel interface to communicate with kernel���������ں˵�ͨ�ţ���SA�Ͳ��Թ����ӿں�IP��ַ����
                this->public.kernel = kernel_interface_create();        <<file://kernel_interface�еĽṹ�����.h>>
                    �ԷǱ��ļ��б�����Ӱ�죺��
                # Manager for IKE configuration attributes
                this->public.attributes = attribute_manager_create();   <<file://attribute_manager�еĽṹ�����.h>>
                    �ԷǱ��ļ��б�����Ӱ�죺��
                # Controller to control the daemon
                this->public.controller = controller_create();          <<file://controller�еĽṹ�����.h>>
                    �ԷǱ��ļ��б�����Ӱ�죺��
                    �ṩ�˼򵥵�API�������ֲ�����ʺͿ����ػ����̣����磺��ʼ��IKE_SA�ȣ�,
                    �൱��Ϊdaemon�ṩ��һ������Ĳ������
                # EAP manager to maintain registered EAP methods
                this->public.eap = eap_manager_create();                <<file://eap_manager�еĽṹ�����.h>>
                    �ԷǱ��ļ��б�����Ӱ�죺��
                # XAuth manager to maintain registered XAuth methods
                this->public.xauth = xauth_manager_create();            <<file://xauth_manager�еĽṹ�����.h>>
                    �ԷǱ��ļ��б�����Ӱ�죺��
                    �Σ� file://../strongswan/xauth.txt
                # Manager for the different configuration backends. Ϊ��֧��vici��stroke��uci�ȵȲ�ͬ���ն�
                this->public.backends = backend_manager_create();       <<file://backend_manager�еĽṹ�����.h>>
                    �ԷǱ��ļ��б�����Ӱ�죺��
                    ������ע��vici���նˣ�����backends�Ķ����õ���ط���ʱ���ڲ�ʹ��ע����ն˽��������Ĳ���
                    ע����ն�ʵ����backend_t�ӿڣ�
                    ע��swanctl	��ͨ�� vici �ӿڽ���ͨ�ŵ����úͿ���ʵ�ó���vici ����ṩ�˶๦�� IKE ���ƽӿ�
                # Socket manager instance��socket��������������ע��socketʵ���࣬��ͨ������ʵ����ʵ�ְ����շ�
                this->public.socket = socket_manager_create();          <<file://socket_manager�еĽṹ�����.h>>
                    �ԷǱ��ļ��б�����Ӱ�죺��
                # Manager for triggering policies, called traps
                this->public.traps = trap_manager_create();             <<file://trap_manager�еĽṹ�����.h>>
                    �ԷǱ��ļ��б�����Ӱ�죺charon->bus->add_listener
                # Manager for shunt PASS|DROP policies
                this->public.shunts = shunt_manager_create();           <<file://shunt_manager�еĽṹ�����.h>>
                    �ԷǱ��ļ��б�����Ӱ�죺��
                # Manager for IKE redirect providers
                this->public.redirect = redirect_manager_create();      <<file://redirect_manager�еĽṹ�����.h>>
                    �ԷǱ��ļ��б�����Ӱ�죺��
                # Handler for kernel events�������ʹ����ں��¼�
                this->kernel_handler = kernel_handler_create();         <<file://kernel_handler�еĽṹ�����.h>>
                    �ԷǱ��ļ��б�����Ӱ�죺charon->kernel->add_listener
                ... 
                global daemon_t *charon = this->public
                    charon�ļ�ȫ�ֱ���ָ�� public
            ����this
            ����С�᣺
                ���⣺
                    �ṩ���ߣ�ͨ���������߽ӿڣ������Ӧ����
                    �ṩ������壬�Ӷ��ṩ�˼򵥵�API�������ֲ�����ʺͿ����ػ�����
                �ڲ���
                    �������ں˵�ͨ��
                    �������ݰ����շ�
                    �������ݰ��ķ�װ
                    ֧��xauth��ʽ�����֤
                    ����IKE��������
                    ������
        srandom
        dbg_old = dbg;  //����ָ�����
        dbg = dbg_bus;
    ��ʼ���ֲ����� level_t levels[DBG_MAX] ֵΪ LEVEL_CTRL
        ����loglevel
        	LEVEL_SILENT = -1,  // absolutely silent 
            LEVEL_AUDIT   = 0,  // most important auditing logs */
            LEVEL_CTRL    = 1,  // control flow
            LEVEL_DIAG    = 2,  // diagnose problems 
            LEVEL_RAW     = 3,  // raw binary blobs 
            LEVEL_PRIVATE = 4,  // including sensitive data (private keys) 
    �������������֧�ֵ��������������
        use-syslog��debug-dmn��debug-mgr��debug-ike��debug-chd��debug-job
        debug-cfg��debug-dnl��debug-net��debug-asn��debug-enc��debug-tnc
        debugimc��debug-imv��debug-pts��debug-tls��debug-esp��debug-lib
        ������Щ���������˵�1���⣬�����Ķ���Ҫ������ֵ(��opt=value)
        ����ֵ���ھֲ����� level_t levels[DBG_MAX] ��Ӧλ��
    lookup_uid_gid ��user id��group id��
        �������� charon.user��Ĭ��ΪNULL���� charon.group��Ĭ��ΪNULL��
        ���������Ϊ�գ������ lib->caps->resolve_uid / lib->caps->resolve_gid
        ������ú�������ֵΪʧ�ܣ��򱾺�������ʧ�ܣ�������main�����˳�
        ע��lib->caps �� library_init �б���ֵ
    ���� level_t levels[DBG_MAX] ������־����
        Ӱ�� private_daemon_t �ĳ�Ա���� this->levels �� this->to_stderr
    charon->load_loggers    //��deamon.bus֧����log����
        ���������ļ���Ĭ�ϴ��� sys_logger �� file_logger����¼��private_daemon_t��logger��Ա�У���Ϊ�����ô����������
        charon->bus->add_logger(sys_logger->logger)
        charon->bus->add_logger(file_logger->logger)
    uname(&utsname) 
    charon->initialize   file://charon��ʼ��ʱ���ص�Ĭ�ϲ��.txt
        ���� plugin_feature_t features[]   //file://plugin_feature_t.py        
        <�� file://../imgs/strongswan������ƽṹ��ϵ2.png> 
        <�Σ�file://plugin_feature_t.py> 
        <�Σ�file://../imgs/plugin_loader��plugins��ֵ.png>
        lib->plugins->add_static_features(...)  
            plugin_t *plugin = static_features_create(...)
                this = new static_features_t;
                ����ָ���Ա��ʼ��
                this.name = ��������������
                this.features = clone ����������features
                return this.public  //static_features_t.public is typeof plugin_t
            entry = new plugin_entry_t
                entry.plugin = plugin
                entry.features =  linked_list_create()
            lib->plugins->plugsin->insert_last(entry)
            lib->plugins->register_features(entry)
                ���� entry.plugin �е� features
                    ����� FEATURE_PROVIDE
                        ��� lib->plugins->features ���Ƿ��Ѵ��ڸ�feature
                            ���������
                                registered = new registered_feature_t
                                    registered.feature = feature
                                    registered.plugins = linked_list_create()
                                lib->plugins->features->put(registered)
                                provided = new provided_feature_t
                                    provided.entry = entry
                                    provided.feature = feature
                                    provided.reg = reg  //reg ��ע��feature��Ĭ��Ϊ��
                                    provided.dependencies = count - i
                                registered->plugins->insert_last��provided��
                                entry->features->insert_last��provide��
                    ����� FEATURE_REGISTER �� FEATURE_CALLBACK
                        �� feature ���浽 reg
                    ������϶�����
                        ��������
        lib->plugins->load(plugins)
           �Σ�<file://plugin_loader����.py> <file://plugin_feature�еĽṹ�����.h>
           &pluginsֵ
           plugins = '''aes des rc2 sha2 sha1 md5 mgf1 random nonce x509 revocation 
                        constraints pubkey pkcs1 pkcs7 pkcs8 pkcs12 pgp dnskey sshkey 
                        pem openssl fips-prf gmp curve25519 xcbc cmac hmac attr 
                        kernel-netlink resolve socket-default stroke vici updown 
                        eap-identity eap-md5 eap-mschapv2 eap-dynamic eap-radius 
                        eap-tls eap-ttls eap-peap eap-tnc xauth-generic xauth-eap 
                        tnc-tnccs counters'''
        lib->processor->queue_job(job=start_action_job_create())
            ����job=start_action_job_create:
                ��������ʼ�� private_start_action_job_t������public����
                    private_start_action_job_t *this;
                    this.public.job_interface = {
                                .execute = _execute,
                                .get_priority = _get_priority,
                                .destroy = _destroy
                                }   
            this->jobs[job->get_priority]->insert_last(job)
            this->job_added->signal(this->job_added); //������������
                �ڲ�����pthread_cond_signal()  //���Ǹ�pthread.h���ṩ��ϵͳ����
                    pthread_cond_signal�����������Ƿ���һ���źŸ�����һ�����ڴ��������ȴ�״̬���߳�,
                    ʹ����������״̬,����ִ��.
                    pthread_cond_wait() ����������ǰ�̣߳�
                    �ȴ�����߳�ʹ��pthread_cond_signal()��pthread_cond_broadcast����������
    check_pidfile
    !lib->caps->drop
    �����źŴ�����  ��ӦSIGSEGV��SIGILL��SIGBUS�źţ�������ֻ�е�ǰ�̣߳����̣߳���������Щ�ź�
    charon->start(charon)
        lib->processor->set_threads(count)  //���ÿ����߳�����count�������ļ���ȡ��Ĭ��Ϊ16
            ���뵽processor.c�ļ���
                this->desired_threads = count;
                for 0 : count
                    worker = new worker_thread_t
                        worker.processor = this
                        worker.thread = thread_create(process_jobs,worker)
                    this->threads->insert_last(worker)
                    this->total_threads++;
                this->job_added->broadcast  //�㲥�������job�� job_addedΪcondvar_t*���� 
        run_scripts(verb="start")
             lib->settings->create_key_value_enumerator("charon.verb-scripts")  //����ö�������Ĭ��Ϊ��
             ��ö����Ϊ��ʱ������Ĵ���û�б�ִ��
    run()
        �����߳�����SIGINT��SIGHUP��SIGTERM�������ź�
        �����ȴ������ź�
            ������յ��ź�SIGHUP�������źţ���
            ������յ��ź�SIGINT���ж��źţ���
            ������յ��ź�SIGTERM����ֹ�źţ���
            
processor.c : process_jobs�߳�            
    �Σ�file://����processor��worker��job��.py
    
start_action_job_create��execute������
    �Σ�file://����processor��worker��job��.py
    
charon�������
https://peiyake.com/wiki/strongswan/index.html#charon%E6%A1%86%E6%9E%B6
    charon�Ĺ������ƣ�
    IKE_SA Manager�Ӻ��Backends��ȡ������Ϣ��������������Ϣ��ʼ��IKE_SA��
    IKE_SA�ĳ�ʼ��������
        ����IKE_SAʵ������������������Processor������������Scheduler����
        ����IKEЭ��ִ�б��Ĺ������ͣ�sender�����߽��գ�receiver�����Ĳ�������
        IKE_SAЭ�̳ɹ��󣬴�����Ӧ��CHILD_SA��
        ͬʱ�����ں˽ӿڣ�Kernel Interface���������Ϣ�·����ںˣ�
        ��������ɹ��󣬸�������ת��״̬��أ�Rekey�ȣ���
        �������й��̶Ը����׶ε��¼��������ߣ�Bus����������ȷ���¼�������
        ��֮��charon�ĺ��������ǹ���IPSec��SA������ҵ���߼�������IKE_SA Manager��
        ������ģ�鶼��Ϊ�����ġ�    