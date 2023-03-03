processor_t  �Σ�file://processor�еĽṹ�����.h
    processor�У����� jobs ����job_t���ͣ���threads ����worker_thread_t���ͣ�
    
job_t �ṹ����
    struct job_t {
        job_status_t status;   // job��״̬���ɴ�����/���ȳ���ר���޸�
        // processingʹ�ø÷���ִ��һ��job��job��һ���Եģ�ִ�����ᱻ����
        job_requeue_t (*execute) (job_t *this);
        // ȡ��һ��job���÷�����ѡ
        // It allows potentially blocking jobs to be canceled during shutdown.
        // If no special action is to be taken simply return FALSE then the thread
        // executing the job will be canceled.  If TRUE is returned the job is
        // expected to return from execute() itself (i.e. the thread won't be
        // canceled explicitly and can still be joined later).
        // Jobs that return FALSE have to make sure they provide the appropriate
        // cancellation points.
        // �������ĳ�����ҵ����ʵ�ִ˷���
        // �����ڵ��� execute() ֮ǰ���ô˷���
        bool (*cancel)(job_t *this);       
        job_priority_t (*get_priority)(job_t *this);  // ��ȡjob�����ȼ�
        void (*destroy)(job_t *this);  // ����һ��job����jobִ�к��ȡ��ʱ����
    };
    
    enum job_status_t {
        JOB_STATUS_QUEUED = 0,   //���ڶ������ˣ���ûִ��
        JOB_STATUS_EXECUTING,    //ִ����
        JOB_STATUS_CANCELED,     //��ȡ����
        JOB_STATUS_DONE,         //�ɹ�ִ������
    };
    
    struct private_callback_job_t {
        callback_job_t public;           //callback_job_t�ڲ�ֻ��job_tһ����Ա
        callback_job_cb_t callback;      //����ָ��
        void *data;                      //����callback������
        callback_job_cleanup_t cleanup;  //�����ͷ�(�̲߳�����)���ݵĺ���
        callback_job_cancel_t cancel;    //ȡ��һ��jobʱ���øú���
        job_priority_t prio;             //job�����ȼ�
    };
    
��ʱ�����job����������˵����Ĭ�����ȼ�Ϊ JOB_PRIO_MEDIUM�� # callback_job_create_with_prio
    charon->initialize  
        #��ʼ��������������
        scheduler_create �ص���schedule JOB_PRIO_CRITICAL
    charon->initialize
        lib->plugins->load��load_plugins
            load_plugin
                create_plugin
                    constructor //����ṩ�ĺ���
                        kernel_libipsec_plugin_create
                            #kernel_ipsec�������ʱ��ʼ��
                            libipsec_init
                                ipsec_event_relay_create  �ص���handle_events 
                                ipsec_processor_create   �ص���process_inbound��process_outbound
            load_features
                load_provided
                    load_dependencies
                        ...
                            #������Լ���/ע��
                            plugin_feature_load
                                 reg->arg.cb.f
                                    #�շ���
                                    daemon.c : sender_receiver_cb
                                        receiver_create
                                            receiver_create �ص���receive_packets JOB_PRIO_CRITICAL
                                        sender_create
                                            sender_create �ص���send_packets JOB_PRIO_CRITICAL
                                    #kernel_net
                                    kernel_net.c �� kernel_net_register
                                        add_net_interface
                                            kernel_netlink_net_create
                                                lib->watcher->add  
                                                    add (watcher.c)
                                                        �ص� ��watch  JOB_PRIO_CRITICAL
                                    #kernel_ipsec
                                    kernel_libipsec_plugin.c : create_router
                                        kernel_libipsec_router_create  �ص��� handle_plain
        start_action_job_create �ص��� start_action_job.c : _execute
            
job����ӵ����Ķ�
    lib->processor->queue_job((job_t*)callback_job_create(...));
    �ɼ�job��processorά����
        
����(charon����ʱ)��ӵĸ���job�Ľ���  
    ipsec_event_relay.c : handle_events
        ���ܣ�
            Dequeue events and relay them to listeners
            �Ӹ��ļ������������ܿ�֪��
            �ú����൱�� private_ipsec_event_relay_t �ĳ�Ա����
            ��ά����queue���ϵ�ȡ�� ipsec_event_t *event��
            Ȼ�����listeners��¼�ļ����ߵ�expire������
            ��event�е����ݸ��߸�ÿһ��������
        ���������
            �ú����Ĵ�������ǣ�private_ipsec_event_relay_t *this
            ipsec_event_t *event = this->queue->dequeue();  //Ϊ��ʱ�ȴ�
            foreach ipsec_event_listener_t *current in this->listeners
                if event->type == IPSEC_EVENT_EXPIRE
                    current->expire(...)
            return JOB_REQUEUE_DIRECT;  //�´�������ȣ�ֱ���ٴε���
    ipsec_processor.c : process_inbound              
        ������
            ������� private_ipsec_processor_t*this
        ����
            inbound�ķ�����"�뾳"
            rocess_inbound�Ĺ��ܣ�Processes inbound packets
            ���Բ²�process_inbound�ǶԽ��յ�esp���ݰ����д���
        �������
            process_inbound�൱��private_ipsec_processor_t�ĳ�Ա����
            ��inbound_queue��ȡ��esp_packet_t *packet��Ϊ��ʱ�ȴ�
            packet->parse_header()�õ�uint32_t spi
            ipsec->sas->checkout_by_spi()�õ�ipsec_sa_t *sa��ipsec��ipsec.c�м�¼�Ķ���
            saΪ�գ�˵���յ���packet������installed SA���̣�return JOB_REQUEUE_DIRECT
            sa->is_inbound(),���ʧ�ܣ�˵����sa����inbound�ģ�return JOB_REQUEUE_DIRECT
            packet->decrypt() ����packet���н���
            ip_packet_t *ip_packet = packet->get_payload(), �õ�������ip��
            sa->update_usestats(),��¼���ݰ��ļ���/�����Ը���ʹ��ͳ����Ϣ
            uint32_t reqid = sa->get_reqid()
            ipsec->sas->checkin(sa), ÿ�μ��sa�󣬼ǵü����ȥ
            uint8_t next_header = packet->get_next_header()
            ���next_headerΪIPPROTO_IPIP��IPPROTO_IPV6
                ipsec_policy_t *policy = ipsec->policies->find_by_packet(ip_packet, TRUE, reqid)
                ������ҵ���policy
                    deliver_inbound(packet);
                        �ú����Ĺ����ǣ�Deliver an inbound IP packet to the registered listener
                        ����Ϊ������վ IP ���ݰ����ݸ�ע���������
                        ���룺
                            ���inbound.cb��Ϊ��(register_inboundע��ģ�Ĭ��Ϊ��)
                            //�� kernel_libipsec_router.c:kernel_libipsec_router_create()�У�������register_inbound
                                inbound.cb(this->inbound.data, packet->extract_payload(packet));
                            �������ð�
            �����������Э�飬�򲻴���
            ���� JOB_REQUEUE_DIRECT
    ipsec_processor.c : process_outbound                
        ������
            ������� private_ipsec_processor_t*this
        ����
            outbound�ķ�����"����"
            rocess_inbound�Ĺ��ܣ�Processes outbound packets
            ���Բ²�process_outbound�ǶԷ�����esp���ݰ����д���
        �������        
            process_outbound�൱��private_ipsec_processor_t�ĳ�Ա����
            ��outbound_queue��ȡ��ip_packet_t *packet��Ϊ��ʱ�ȴ�
            ipsec_policy_t *policy = ipsec->policies->find_by_packet()
            ���policyΪ�գ�˵��û��ƥ��� outbound IPsec policy��return JOB_REQUEUE_DIRECT
            ipsec_sa_t *sa = ipsec->sas->checkout_by_reqid(policy->get_reqid(policy))
            ���saΪ�գ������ð�(������ca����ܷ�esp��)��return JOB_REQUEUE_DIRECT
            host_t* src = sa->get_source()
            host_t* dst = sa->get_destination()
            esp_packet_t *esp_packet = esp_packet_create_from_payload(src,dst,packet)
            esp_packet->encrypt() ,��esp�����ܣ�����ʧ��return JOB_REQUEUE_DIRECT
            sa->update_usestats(),��¼���ݰ��ļ���/�����Ը���ʹ��ͳ����Ϣ
            send_outbound(esp_packet)
                ���ܣ�Send an ESP packet using the registered outbound callback
                ���룺ʹ��ע��ĳ�վ�ص����� ESP ���ݰ�
                �������
                    ���outbound.cb��Ϊ��(register_outboundע���,Ĭ��Ϊ��)
                    //�� kernel_libipsec_router.c:kernel_libipsec_router_create()�У�������register_out  bound
                        outbound.cb(packet)
                    �������ð�
            return JOB_REQUEUE_DIRECT   
    scheduler.c : schedule  �Σ�file://scheduler�еĽṹ�����.h
        ���ܣ�
            ���ά����event�����У���event��ʱ�䣬
            ʱ�䵽�ˣ�lib->processor->queue_job(event->job)
        ���������
            ��ȡ��ǰʱ��(&now)
            event = peek_event
                ���this->event_count����0������ this->heap[1] �����򷵻� NULL
            �����ȡ��event
                �����ǰ now >= event->time
                    remove_event
                        �Ƴ������� this->heap[1]��Ȼ�����ʱ���ϵ����������ѽṹ
                    lib->processor->queue_job(event->job)
                    return JOB_REQUEUE_DIRECT  //����ֱ���ٴ�ִ�и�����
                ��� now < event->time
                    ��ʾ��һ���¼��೤ʱ���ʼ
                this->condvar->timed_wait_abs(event->time)  //������������ĳʱ�����Ч    
            ����
                this->condvar->wait()    //��������һֱ�ȴ���ֱ��������
            return JOB_REQUEUE_DIRECT  //����ֱ���ٴ�ִ�и�����
    receiver.c : receive_packets
        chunk_t marker = chunk_from_chars(0x00, 0x00, 0x00, 0x00)
            struct chunk_t {
                u_char *ptr;  //ָ�������
                size_t len;   //ָ������ݵĳ���
            }
            chunk_from_chars�Ǹ��꣬���������滻���Ч���ǣ�
            marker = { (u_char[]){0x00, 0x00, 0x00, 0x00}, 
                        sizeof((u_char[]){0x00, 0x00, 0x00, 0x00}/*=4*/)
                     }
            �����marker.ptrָ��һ���������ݿ�
        packet_t *packet = charon->socket->receive();  //ʹ��ע���socket����һ�����ݰ�
        �������ʧ�ܣ����� JOB_REQUEUE_FAIR  //fair:��ƽ�ģ��������뵽jobs���е�β�������Ŷ�
        chunk_t data = packet->get_data()
        ��� data.len<marker.len��  return JOB_REQUEUE_DIRECT   //�����Ŷӣ�ֱ������ִ��
        host_t* dst = packet->get_destination()
        host_t* src = packet->get_source()
        bool b1 = charon->kernel->all_interfaces_usable()
             return !this->ifaces_filter 
             //���ifaces_filterΪ�գ�˵���޹������������棬���нӿڿ���
        bool b2 = charon->kernel->get_interface(dst,NULL)
            bool get_interface(host_t *host, char **name)  //kernel_interface.c
                if(this->net == NULL) return NULL
                return this->net->get_interface(host,name)  ??
                �ⲿ�ֵĽ��ܲΣ�file://kernel_interface.py
        if( b1==false && b2==false)  //�еĽӿڲ����ã���host��Ӧ������������
            return JOB_REQUEUE_DIRECT
        if( dst��port �� src��port ������ IKEV2_UDP_PORT/*500*/ )  //500������natd�İ�
            ��� data �Ŀ�ʼ���ֺ� marker һ�£�������(�Ƴ�) marker ���֣�ǰ��4�ֽڣ�
            ����˵����packet �����Ǹ�esp packet
                this->esp_cb.cb��packet��
                    �Σ�file://reciever.c
                    �� kernel_libipsec_router.c:kernel_libipsec_router_create()�У�
                    ������add_esp_cb
                return JOB_REQUEUE_DIRECT;
        //���ߵ����˵����natd�İ�
        message = message_create_from_packet(packet);
        status_t s = message->parse_header()
        ��� s ��= SUCESS
            charon->bus->alert(ALERT_PARSE_ERROR_HEADER,message)
            return JOB_REQUEUE_DIRECT;
        switch (message->get_major_version())  //��� IKE �� IKEV1 ���� IKEV2
            �� IKEV2
                ��� message->get_exchange_type == IKE_SA_INIT ���� message�Ǹ�request����������reply��
                    send_notify(message, IKEV1_MAJOR_VERSION, INFORMATIONAL_V1,INVALID_MAJOR_VERSION, chunk_empty)
                 supported = FALSE;   
            �� KIEV1
                ��� message->get_exchange_type �� ID_PROT �� AGGRESSIVE
                    send_notify(message, IKEV2_MAJOR_VERSION, INFORMATIONAL,INVALID_MAJOR_VERSION, chunk_empty);
                supported = FALSE;   
            ������
                supported = FALSE;
        ��� supported == FALSE   //��֧�ֵ�Э��汾
            return JOB_REQUEUE_DIRECT;
        ��� message �Ǹ� request���� message->get_exchange_type() == IKE_SA_INIT
            ike_sa_id_t *id = message->get_ike_sa_id()
    sender.c : send_packets
        ���������private_sender_t *this���Σ�file://sender.c
        �൱�� private_sender_t �ĳ�Ա����
        ��� list ��countΪ0����ȴ� got ��������
        ��list��ͬ��ʱ
        packet_t *packet = list->remove_first()
        ���� sent ��������
        charon->socket->send(packet);  //�Σ�file://socket_manager.c
        return JOB_REQUEUE_DIRECT;
    watcher.c : watch    
        �൱�� private_watcher_t �ĳ�Ա����
        �Σ�file://watcher�еĽṹ�����.h | file://watcher.c
        ���ܣ��ɷ�����
        ���������
            //�и�stateö�����ͳ�Ա��������״̬��ֹͣ�����Ŷӡ���ִ��
            �ж����ע���FDs���ļ���������Ϊ0
                �裬state = WATCHER_STOPPED
                ���� JOB_REQUEUE_NONE  //�������
                ͨ������������ᷢ������Ϊ�ڽ���job���ǰ��������Ϊ�����FD
            ���state��ǰΪ���Ŷ�״̬���Ƚ�������Ϊ��ִ��״̬
            ʹ��poll������notify[0]�ܵ����� FDs ��poll����Ϊ���޵ȴ�
                //�Σ�file://poll�÷�.txt
                ����notifyʱ�����ӵ���POLLIN/*�����ݿɶ�*/�¼�
                ���Ӹ�FDsʱ��fd�Ǵ�FDs��ȡ�ģ�FD��event�ṹ��
                ���治����¼��fd������Ҫ���ӵ��¼��ȵ�
                Ȼ�����Щ���������¼�����ɸ�struct pollfd*����
                Ȼ����poll��������
            ��poll���ӵ��¼���
                ������ӵ���notify��������
                    ��notify[0]�е����ݶ��꣨��������
                    return JOB_REQUEUE_DIRECT;
                    ��Ϊ��notify[0]�����ã�
                    ��ʹFDsû���ӵ�Ҳ�᷵�أ�
                    ֮��job�������
                ����notify[0]�������ˣ���˵��FDs�ж�д�¼���
                for entry in FDs
                    ����� entry->in_callback
                        ˵�����ļ�������ڻص�����Ӧ�ĺ���
                        ��ʱ����������������������ֹforѭ����
                    ����entry��fd��Ӧ��pfd(pool fds)��revents����¼�˸�fdʵ�ʷ������¼���
                    �����revents���¼�
                        �����WATCHER_EXCEPT��˵���ļ��������д�����
                            notify(this, entry, WATCHER_EXCEPT);
                        �������WATCHER_READ��˵�������ݿɶ�
                            notify(this, entry, WATCHER_READ);
                        �������WATCHER_WRITE��˵�������ݿ�д��д����������
                            notify(this, entry, WATCHER_WRITE);
                        //notify�л� in_callback++
                ���jobs��Ա��������Ϊ0����һ����notify�����job��
                    ����lib->processor->execute_job��ִ�и�jobs
                    execute_job��ʹ��һ�������߳�ֱ��ִ�и�job
                    ���û�п����̣߳���ʹ�õ������߳�ִ�и�job
        watch���������õ���notify����
            ���ܣ�����һ��job������notify_async����ӵ��Լ���jobs��
            void notify(private_watcher_t *this, entry_t *entry,
                        watcher_event_t event)
                ��������ʼ�� notify_data_t* data
                data�м�¼ entry->fd,entry->cb,entry->data,evnet��
                this->jobs->insert_last(
                    callback_job_create_with_prio(notify_async,data,notify_end))
                notify_end����notify_async���֮����еģ�
                ��ɵĹ����� entry->in_callback--,
                ���� entry->enents����¼�˸�fd��������Щ�¼���Ϊ��ʱ��
                �� FDs���Ƴ��� entry��
    start_action_job.c : _execute
        ����˵����
            This job handles all child configurations stored in an
            backend according to their start_action field (restart, route).
            ���룺 ����start_action�µ����������
            �ú�������JOB_REQUEUE_NONE������������ֻ��ִ��һ��
        ���������
            ö������ peer configs  //�Σ�file://peer_cfg.h
                ö�ٸ� child cfg
                    child_cfg->get_start_action
                        ����� ACTION_RESTART��
                            charon->controller->initiate(...)
                        ����� ACTION_ROUTE��
                            mode = child_cfg->get_mode()
                            ��� mode Ϊ MODE_PASS �� MODE_DROP
                                charon->shunts->install(...)
            return JOB_REQUEUE_NONE;

����ʱ������ʲôʱ����õ� watcher.c:add_entry
    ���壺�ú���������watcher��������ЩFDs
    kernel_netlink_ipsec_create
        fd = socket_xfrm_events = socket(AF_NETLINK, SOCK_RAW, NETLINK_XFRM);
        event = WATCHER_READ
        cb = receive_events
        data = this
    kernel_netlink_net_create
        fd = socket_events = socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE);
        event = WATCHER_READ
        cb = receive_events
        data = this
    stroke_socket_create
        stream_service_t* service = lib->streams->create_service("unix://", 10);  //10Ϊ������Ӹ���
            stream_service_create_unix
                fd = socket(AF_UNIX, SOCK_STREAM, 0);
        stream_service.c : on_accept(service)    
            fd = service->fd
            event = WATCHER_READ
            cb = stream_service.c : watch
            data = this
    vici_socket_create
        stream_service_t* service = lib->streams->create_service("unix:///var/run/charon.vici",3)
        stream_service.c : on_accept(service)    
            fd = service->fd
            event = WATCHER_READ
            cb = stream_service.c : watch
            data = this
            
JOB_REQUEUE_FAIR���job
    android_service.c : handle_plain
    receiver.c : receive_packets
    ha_ctl.c : dispatch_fifo 
        ha high-availability,�߿����ԡ��߳����
    kernel_libipsec_router.c : handle_plain
    smp.c : process
    smp.c : dispatch
    uci_control.c : receive
    
JOB_REQUEUE_DIRECT���job
    android_service.c : handle_plain
    receiver.c : receive_packets
    sender.c : send_packets
    ha_ctl.c : dispatch_fifo
    ha_dispatcher.c : dispatch
    ha_segments.c : watchdog
    kernel_libipsec_router.c : handle_plain
    smp.c : dispatch
    vici_logger.c : raise_events
    ipsec_event_relay.c : handle_events
    ipsec_processor.c : process_inbound
    ipsec_processor.c : process_outbound
    pkcs11_manager.c : dispatch_slot_events
    scheduler.c : schedule
    watcher.c : watch
    
JOB_RESCHEDULE���job
    android_dns_proxy.c : handle_timeout
    ha_segments.c : send_status
    ha_segments.c : autobalance
    systime_fix_plugin.c : check_systime
    tnc_ifmap_renew_session_job.c : execute
    inactivity_job.c : execute
    initiate_mediation_job.c : initiate
    rekey_ike_sa_job.c : execute
    ipsec_sa_mgr.c : sa_expired
    
worker        
    struct worker_thread_t {
        private_processor_t *processor;  //ָ��Ľ���
        thread_t *thread;                //(��Ӧ��)ʵ�ʵ��̣߳�Ϊÿ��worker������һ���̣߳�������process_jobs��
        job_t *job;                      //��ǰ�߳���ִ�е�job
        job_priority_t priority;         //��ǰjob�����ȼ�
    }
    
process_jobs    
    while desired_threads >= total_threads     //���ִ���߳���������Ҫ���߳���ʱ��ѭ������
        ��� get_job(worker) �ɹ���ִ�� process_job(worker);
        ���򣬵ȴ� job_added ������������������������������µ�job��
    total_threads --
    thread_terminated->signal  //�������߳̽�����

get_job(worker)
    int idle = this->total_threads -  this->working_threads[0~JOB_PRIO_MAX]
    for �����ȼ� to �����ȼ�
        this->jobs[�����ȼ�]->remove_first����� worker->job��
        ��һ���ɹ�����worker->priority = ��ǰ���ȼ����������棬��������´�ѭ��
    ����ʧ��
        
process_job(worker)
    working_threads[worker->priority��¼�����ȼ�] ++
    worker->job->status = JOB_STATUS_EXECUTING  //����job����ִ��
    private_thread_t->cleanup_handlers�в���(��¼) cleanup���� = restart
    worker->job->execute
    private_thread_t->cleanup_handlers�е����������cleanup�����������ø�cleanup����
    working_threads[worker->priority��¼�����ȼ�] --
    ע��
    ����û��ע job_requeue_t requeue = worker->job->execute �ķ���ֵ
    ��ʵ��process_job�������滹�д��룬����ʡ����
    ʡ�ԵĴ�����ɵĹ��ܾ��Ǹ��� requeue���жϸ�job���ٴ�ִ��һ�顢
    �����ٴβ��뵽jobs���е�ĩβ�����߱� lib->scheduler->schedule_job �ȵ���
    ��� requeue.type == JOB_REQUEUE_TYPE_NONE �� worker->job->status == JOB_STATUS_CANCELED��
    �������ٸ�job
    
ʲôʱ��ἤ�� job_added ��������   
    process_job ��ĳ������»� signal
    queue_job �л� signal
    execute_job �л� signal
    set_threads �л� broadcast
    cancel �л� broadcast
    
start_action_job_create��execute������
    �������ȴ���һ��ipsec���õĵ�����
    ��������ÿ�����ã��������õĵ�ǰ״ִ̬����Ӧ�Ĳ���
        ACTION_RESTART
            ִ�����ó�ʼ�� charon->controller->initiate(...)
        ACTION_ROUTE
            MODE_PASS/MODE_DROPģʽ��ִ��charon->shunts->install(...)
            MODE_TRANSPORT/MODE_TUNNELģʽ��ִ��charon->traps->install(...)
    Ĭ�������£��ú���ʲôҲû����