processor_t  参：file://processor中的结构与变量.h
    processor中，含有 jobs 链表（job_t类型）、threads 链表（worker_thread_t类型）
    
job_t 结构介绍
    struct job_t {
        job_status_t status;   // job的状态，由处理器/调度程序专门修改
        // processing使用该方法执行一个job，job是一次性的，执行完后会被销毁
        job_requeue_t (*execute) (job_t *this);
        // 取消一个job，该方法可选
        // It allows potentially blocking jobs to be canceled during shutdown.
        // If no special action is to be taken simply return FALSE then the thread
        // executing the job will be canceled.  If TRUE is returned the job is
        // expected to return from execute() itself (i.e. the thread won't be
        // canceled explicitly and can still be joined later).
        // Jobs that return FALSE have to make sure they provide the appropriate
        // cancellation points.
        // 不阻塞的常规作业不得实现此方法
        // 可以在调用 execute() 之前调用此方法
        bool (*cancel)(job_t *this);       
        job_priority_t (*get_priority)(job_t *this);  // 获取job的优先级
        void (*destroy)(job_t *this);  // 销毁一个job，当job执行后或取消时调用
    };
    
    enum job_status_t {
        JOB_STATUS_QUEUED = 0,   //放在队列中了，还没执行
        JOB_STATUS_EXECUTING,    //执行中
        JOB_STATUS_CANCELED,     //被取消了
        JOB_STATUS_DONE,         //成功执行完了
    };
    
    struct private_callback_job_t {
        callback_job_t public;           //callback_job_t内部只有job_t一个成员
        callback_job_cb_t callback;      //函数指针
        void *data;                      //传给callback的数据
        callback_job_cleanup_t cleanup;  //用于释放(线程产生的)数据的函数
        callback_job_cancel_t cancel;    //取消一个job时调用该函数
        job_priority_t prio;             //job的优先级
    };
    
何时会添加job（如无特殊说明，默认优先级为 JOB_PRIO_MEDIUM） # callback_job_create_with_prio
    charon->initialize  
        #初始化：调度器创建
        scheduler_create 回调：schedule JOB_PRIO_CRITICAL
    charon->initialize
        lib->plugins->load，load_plugins
            load_plugin
                create_plugin
                    constructor //插件提供的函数
                        kernel_libipsec_plugin_create
                            #kernel_ipsec插件创建时初始化
                            libipsec_init
                                ipsec_event_relay_create  回调：handle_events 
                                ipsec_processor_create   回调：process_inbound、process_outbound
            load_features
                load_provided
                    load_dependencies
                        ...
                            #插件特性加载/注册
                            plugin_feature_load
                                 reg->arg.cb.f
                                    #收发器
                                    daemon.c : sender_receiver_cb
                                        receiver_create
                                            receiver_create 回调：receive_packets JOB_PRIO_CRITICAL
                                        sender_create
                                            sender_create 回调：send_packets JOB_PRIO_CRITICAL
                                    #kernel_net
                                    kernel_net.c ： kernel_net_register
                                        add_net_interface
                                            kernel_netlink_net_create
                                                lib->watcher->add  
                                                    add (watcher.c)
                                                        回调 ：watch  JOB_PRIO_CRITICAL
                                    #kernel_ipsec
                                    kernel_libipsec_plugin.c : create_router
                                        kernel_libipsec_router_create  回调： handle_plain
        start_action_job_create 回调： start_action_job.c : _execute
            
job被添加到了哪儿
    lib->processor->queue_job((job_t*)callback_job_create(...));
    可见job是processor维护的
        
上面(charon启动时)添加的各种job的介绍  
    ipsec_event_relay.c : handle_events
        功能：
            Dequeue events and relay them to listeners
            从该文件名及函数介绍可知，
            该函数相当于 private_ipsec_event_relay_t 的成员方法
            从维护的queue不断的取出 ipsec_event_t *event，
            然后调用listeners记录的监听者的expire方法，
            将event中的数据告诉给每一个监听者
        代码分析：
            该函数的传入参数是：private_ipsec_event_relay_t *this
            ipsec_event_t *event = this->queue->dequeue();  //为空时等待
            foreach ipsec_event_listener_t *current in this->listeners
                if event->type == IPSEC_EVENT_EXPIRE
                    current->expire(...)
            return JOB_REQUEUE_DIRECT;  //下次无需调度，直接再次调用
    ipsec_processor.c : process_inbound              
        参数：
            传入的是 private_ipsec_processor_t*this
        功能
            inbound的翻译是"入境"
            rocess_inbound的功能：Processes inbound packets
            所以猜测process_inbound是对接收的esp数据包进行处理
        代码分析
            process_inbound相当于private_ipsec_processor_t的成员方法
            从inbound_queue中取出esp_packet_t *packet，为空时等待
            packet->parse_header()得到uint32_t spi
            ipsec->sas->checkout_by_spi()得到ipsec_sa_t *sa，ipsec是ipsec.c中记录的对象
            sa为空，说明收到的packet不属于installed SA过程，return JOB_REQUEUE_DIRECT
            sa->is_inbound(),如果失败，说明该sa不是inbound的，return JOB_REQUEUE_DIRECT
            packet->decrypt() ，对packet进行解码
            ip_packet_t *ip_packet = packet->get_payload(), 得到解码后的ip包
            sa->update_usestats(),记录数据包的加密/解密以更新使用统计信息
            uint32_t reqid = sa->get_reqid()
            ipsec->sas->checkin(sa), 每次检出sa后，记得检入回去
            uint8_t next_header = packet->get_next_header()
            如果next_header为IPPROTO_IPIP或IPPROTO_IPV6
                ipsec_policy_t *policy = ipsec->policies->find_by_packet(ip_packet, TRUE, reqid)
                如果能找到该policy
                    deliver_inbound(packet);
                        该函数的功能是：Deliver an inbound IP packet to the registered listener
                        翻译为：将入站 IP 数据包传递给注册的侦听器
                        代码：
                            如果inbound.cb不为空(register_inbound注册的，默认为空)
                            //在 kernel_libipsec_router.c:kernel_libipsec_router_create()中，调用了register_inbound
                                inbound.cb(this->inbound.data, packet->extract_payload(packet));
                            否则丢弃该包
            如果不是上述协议，则不处理
            返回 JOB_REQUEUE_DIRECT
    ipsec_processor.c : process_outbound                
        参数：
            传入的是 private_ipsec_processor_t*this
        功能
            outbound的翻译是"出境"
            rocess_inbound的功能：Processes outbound packets
            所以猜测process_outbound是对发出的esp数据包进行处理
        代码分析        
            process_outbound相当于private_ipsec_processor_t的成员方法
            从outbound_queue中取出ip_packet_t *packet，为空时等待
            ipsec_policy_t *policy = ipsec->policies->find_by_packet()
            如果policy为空，说明没有匹配的 outbound IPsec policy，return JOB_REQUEUE_DIRECT
            ipsec_sa_t *sa = ipsec->sas->checkout_by_reqid(policy->get_reqid(policy))
            如果sa为空，丢弃该包(建立好ca后才能发esp包)，return JOB_REQUEUE_DIRECT
            host_t* src = sa->get_source()
            host_t* dst = sa->get_destination()
            esp_packet_t *esp_packet = esp_packet_create_from_payload(src,dst,packet)
            esp_packet->encrypt() ,对esp包加密，加密失败return JOB_REQUEUE_DIRECT
            sa->update_usestats(),记录数据包的加密/解密以更新使用统计信息
            send_outbound(esp_packet)
                功能：Send an ESP packet using the registered outbound callback
                翻译：使用注册的出站回调发送 ESP 数据包
                代码分析
                    如果outbound.cb不为空(register_outbound注册的,默认为空)
                    //在 kernel_libipsec_router.c:kernel_libipsec_router_create()中，调用了register_out  bound
                        outbound.cb(packet)
                    否则丢弃该包
            return JOB_REQUEUE_DIRECT   
    scheduler.c : schedule  参：file://scheduler中的结构与变量.h
        功能：
            检查维护的event队列中，各event的时间，
            时间到了，lib->processor->queue_job(event->job)
        代码分析：
            获取当前时间(&now)
            event = peek_event
                如果this->event_count大于0，返回 this->heap[1] ，否则返回 NULL
            如果能取到event
                如果当前 now >= event->time
                    remove_event
                        移除并返回 this->heap[1]，然后根据时间关系，重新整理堆结构
                    lib->processor->queue_job(event->job)
                    return JOB_REQUEUE_DIRECT  //表明直接再次执行该任务
                如果 now < event->time
                    提示下一个事件多长时间后开始
                this->condvar->timed_wait_abs(event->time)  //条件变量都到某时间后有效    
            否则
                this->condvar->wait()    //条件变量一直等待，直到被触发
            return JOB_REQUEUE_DIRECT  //表明直接再次执行该任务
    receiver.c : receive_packets
        chunk_t marker = chunk_from_chars(0x00, 0x00, 0x00, 0x00)
            struct chunk_t {
                u_char *ptr;  //指向的数据
                size_t len;   //指向的数据的长度
            }
            chunk_from_chars是个宏，上面代码宏替换后的效果是：
            marker = { (u_char[]){0x00, 0x00, 0x00, 0x00}, 
                        sizeof((u_char[]){0x00, 0x00, 0x00, 0x00}/*=4*/)
                     }
            这里的marker.ptr指向一个常量数据块
        packet_t *packet = charon->socket->receive();  //使用注册的socket接收一个数据包
        如果接收失败，返回 JOB_REQUEUE_FAIR  //fair:公平的，表明插入到jobs队列的尾部重新排队
        chunk_t data = packet->get_data()
        如果 data.len<marker.len，  return JOB_REQUEUE_DIRECT   //无需排队，直接重新执行
        host_t* dst = packet->get_destination()
        host_t* src = packet->get_source()
        bool b1 = charon->kernel->all_interfaces_usable()
             return !this->ifaces_filter 
             //如果ifaces_filter为空，说明无过滤器，返回真，所有接口可用
        bool b2 = charon->kernel->get_interface(dst,NULL)
            bool get_interface(host_t *host, char **name)  //kernel_interface.c
                if(this->net == NULL) return NULL
                return this->net->get_interface(host,name)  ??
                这部分的介绍参：file://kernel_interface.py
        if( b1==false && b2==false)  //有的接口不可用，且host相应的网卡不可用
            return JOB_REQUEUE_DIRECT
        if( dst的port 和 src的port 都不是 IKEV2_UDP_PORT/*500*/ )  //500表明是natd的包
            如果 data 的开始部分和 marker 一致，则跳过(移除) marker 部分（前面4字节）
            否则，说明该packet 可能是个esp packet
                this->esp_cb.cb（packet）
                    参：file://reciever.c
                    在 kernel_libipsec_router.c:kernel_libipsec_router_create()中，
                    调用了add_esp_cb
                return JOB_REQUEUE_DIRECT;
        //能走到这里，说明是natd的包
        message = message_create_from_packet(packet);
        status_t s = message->parse_header()
        如果 s ！= SUCESS
            charon->bus->alert(ALERT_PARSE_ERROR_HEADER,message)
            return JOB_REQUEUE_DIRECT;
        switch (message->get_major_version())  //检查 IKE 是 IKEV1 还是 IKEV2
            是 IKEV2
                如果 message->get_exchange_type == IKE_SA_INIT 并且 message是个request（还可能是reply）
                    send_notify(message, IKEV1_MAJOR_VERSION, INFORMATIONAL_V1,INVALID_MAJOR_VERSION, chunk_empty)
                 supported = FALSE;   
            是 KIEV1
                如果 message->get_exchange_type 是 ID_PROT 或 AGGRESSIVE
                    send_notify(message, IKEV2_MAJOR_VERSION, INFORMATIONAL,INVALID_MAJOR_VERSION, chunk_empty);
                supported = FALSE;   
            都不是
                supported = FALSE;
        如果 supported == FALSE   //不支持的协议版本
            return JOB_REQUEUE_DIRECT;
        如果 message 是个 request，且 message->get_exchange_type() == IKE_SA_INIT
            ike_sa_id_t *id = message->get_ike_sa_id()
    sender.c : send_packets
        输入参数：private_sender_t *this，参：file://sender.c
        相当于 private_sender_t 的成员函数
        如果 list 的count为0，则等待 got 条件变量
        当list不同空时
        packet_t *packet = list->remove_first()
        触发 sent 条件变量
        charon->socket->send(packet);  //参：file://socket_manager.c
        return JOB_REQUEUE_DIRECT;
    watcher.c : watch    
        相当于 private_watcher_t 的成员函数
        参：file://watcher中的结构与变量.h | file://watcher.c
        功能：派发函数
        代码分析：
            //有个state枚举类型成员，有三种状态：停止、在排队、在执行
            判断如果注册的FDs（文件描述符）为0
                设，state = WATCHER_STOPPED
                返回 JOB_REQUEUE_NONE  //不再入队
                通常这种情况不会发生，因为在将该job入队前，都会先为其添加FD
            如果state当前为在排队状态，先将其设置为在执行状态
            使用poll，监视notify[0]管道及各 FDs ，poll设置为无限等待
                //参：file://poll用法.txt
                监视notify时，监视的是POLLIN/*有数据可读*/事件
                监视各FDs时，fd是从FDs中取的，FD是event结构，
                里面不但记录了fd，还有要监视的事件等等
                然后把这些描述符、事件，组成个struct pollfd*数组
                然后用poll方法监视
            当poll监视到事件了
                如果监视到了notify有数据了
                    将notify[0]中的数据读完（不不留）
                    return JOB_REQUEUE_DIRECT;
                    因为该notify[0]的作用，
                    即使FDs没监视到也会返回，
                    之后job重新入队
                不是notify[0]有数据了，则说明FDs有读写事件了
                for entry in FDs
                    如果有 entry->in_callback
                        说明该文件句柄正在回调其相应的函数
                        此时无需再做后续处理，可以终止for循环了
                    看该entry的fd对应的pfd(pool fds)的revents（记录了该fd实际发生的事件）
                    如果该revents有事件
                        如果是WATCHER_EXCEPT，说明文件描述符有错误发生
                            notify(this, entry, WATCHER_EXCEPT);
                        如果包含WATCHER_READ，说明有数据可读
                            notify(this, entry, WATCHER_READ);
                        如果包含WATCHER_WRITE，说明有数据可写（写不会阻塞）
                            notify(this, entry, WATCHER_WRITE);
                        //notify中会 in_callback++
                如果jobs成员的数量不为0（上一步的notify会添加job）
                    调用lib->processor->execute_job，执行各jobs
                    execute_job是使用一个空闲线程直接执行该job
                    如果没有空闲线程，就使用调用者线程执行该job
        watch方法中引用到的notify方法
            功能：创建一个job，调用notify_async，添加到自己的jobs中
            void notify(private_watcher_t *this, entry_t *entry,
                        watcher_event_t event)
                创建并初始化 notify_data_t* data
                data中记录 entry->fd,entry->cb,entry->data,evnet等
                this->jobs->insert_last(
                    callback_job_create_with_prio(notify_async,data,notify_end))
                notify_end是在notify_async完成之后进行的，
                完成的功能是 entry->in_callback--,
                并当 entry->enents（记录了该fd产生了哪些事件）为空时，
                从 FDs中移除该 entry，
    start_action_job.c : _execute
        函数说明：
            This job handles all child configurations stored in an
            backend according to their start_action field (restart, route).
            翻译： 处理start_action下的相关子配置
            该函数返回JOB_REQUEUE_NONE，表明该任务只会执行一次
        代码分析：
            枚举所有 peer configs  //参：file://peer_cfg.h
                枚举各 child cfg
                    child_cfg->get_start_action
                        如果是 ACTION_RESTART：
                            charon->controller->initiate(...)
                        如果是 ACTION_ROUTE：
                            mode = child_cfg->get_mode()
                            如果 mode 为 MODE_PASS 或 MODE_DROP
                                charon->shunts->install(...)
            return JOB_REQUEUE_NONE;

启动时，都在什么时候调用的 watcher.c:add_entry
    意义：该函数决定了watcher都监视哪些FDs
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
        stream_service_t* service = lib->streams->create_service("unix://", 10);  //10为最大连接个数
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
            
JOB_REQUEUE_FAIR类的job
    android_service.c : handle_plain
    receiver.c : receive_packets
    ha_ctl.c : dispatch_fifo 
        ha high-availability,高可用性、冗长设计
    kernel_libipsec_router.c : handle_plain
    smp.c : process
    smp.c : dispatch
    uci_control.c : receive
    
JOB_REQUEUE_DIRECT类的job
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
    
JOB_RESCHEDULE类的job
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
        private_processor_t *processor;  //指向的进程
        thread_t *thread;                //(对应的)实际的线程（为每个worker创建了一个线程，函数：process_jobs）
        job_t *job;                      //当前线程正执行的job
        job_priority_t priority;         //当前job的优先级
    }
    
process_jobs    
    while desired_threads >= total_threads     //当现存的线程数超过需要的线程数时，循环结束
        如果 get_job(worker) 成功，执行 process_job(worker);
        否则，等待 job_added 条件变量，该条件变量表明添加了新的job了
    total_threads --
    thread_terminated->signal  //表明该线程结束了

get_job(worker)
    int idle = this->total_threads -  this->working_threads[0~JOB_PRIO_MAX]
    for 高优先级 to 低优先级
        this->jobs[本优先级]->remove_first，存给 worker->job，
        上一步成功，则worker->priority = 当前优先级，并返回真，否则继续下次循环
    返回失败
        
process_job(worker)
    working_threads[worker->priority记录的优先级] ++
    worker->job->status = JOB_STATUS_EXECUTING  //表明job正在执行
    private_thread_t->cleanup_handlers中插入(记录) cleanup方法 = restart
    worker->job->execute
    private_thread_t->cleanup_handlers中弹出（清除）cleanup方法，并调用该cleanup方法
    working_threads[worker->priority记录的优先级] --
    注：
    这里没关注 job_requeue_t requeue = worker->job->execute 的返回值
    其实该process_job函数后面还有代码，这里省略了
    省略的代码完成的功能就是根据 requeue，判断该job是再次执行一遍、
    还是再次插入到jobs队列的末尾，或者被 lib->scheduler->schedule_job 等调度
    如果 requeue.type == JOB_REQUEUE_TYPE_NONE 或 worker->job->status == JOB_STATUS_CANCELED，
    还会销毁该job
    
什么时候会激活 job_added 条件变量   
    process_job 中某种情况下会 signal
    queue_job 中会 signal
    execute_job 中会 signal
    set_threads 中会 broadcast
    cancel 中会 broadcast
    
start_action_job_create的execute函数：
    函数首先创建一个ipsec配置的迭代器
    迭代处理每组配置，根据配置的当前状态执行相应的操作
        ACTION_RESTART
            执行配置初始化 charon->controller->initiate(...)
        ACTION_ROUTE
            MODE_PASS/MODE_DROP模式，执行charon->shunts->install(...)
            MODE_TRANSPORT/MODE_TUNNEL模式，执行charon->traps->install(...)
    默认配置下，该函数什么也没有做