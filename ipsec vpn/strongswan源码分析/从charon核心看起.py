前言：
    之前采用顺序看代码的方法，现改为由核心向外扩散的看代码方法
    对应到strongswan，就是先看核心代码：ike是如何建立的
    然后再看与之相关的必要知识点

相关参考：
    file://../strongswan/strongswan建立连接打印出的日志.txt

为了便于跟踪，原来strongswan会默认创建16个线程来处理任务，现在改为使用2个线程
修改方法：/etc/strongswan.conf : charon 下添加 threads = 2
    
关于日志打印级别，从 charon.c 第 339 行可知，默认设为了  LEVEL_CTRL   
可通过命令行参数的方式设置打印日志级别，方法：
--debug-dmn|mgr|ike|chd|job|cfg|knl|net|asn|enc|tnc|imc|imv|pts|tls|esp|lib <level>
<level> :
	/** absolutely silent */
	LEVEL_SILENT = -1,
	/** most important auditing logs */
	LEVEL_AUDIT =   0,
	/** control flow */
	LEVEL_CTRL =    1,
	/** diagnose problems */
	LEVEL_DIAG =    2,
	/** raw binary blobs */
	LEVEL_RAW =     3,
	/** including sensitive data (private keys) */
	LEVEL_PRIVATE = 4,
此次调试使用的参数    ：
    "--debug-dmn=4","--debug-mgr=4","--debug-ike=4","--debug-chd=4","--debug-job=4","--debug-cfg=4",
    "--debug-knl=4","--debug-net=4","--debug-asn=4","--debug-enc=4","--debug-tnc=4","--debug-imc=4",
    "--debug-imv=4","--debug-pts=4","--debug-tls=4","--debug-esp=4","--debug-lib=4"
    如果直接命令行启动charon，参数传递：
        --debug-dmn=4 --debug-mgr=4 --debug-ike=4 --debug-chd=4 --debug-job=4 --debug-cfg=4
        --debug-knl=4 --debug-net=4 --debug-asn=4 --debug-enc=4 --debug-tnc=4 --debug-imc=4
        --debug-imv=4 --debug-pts=4 --debug-tls=4 --debug-esp=4 --debug-lib=4
    
vm2执行swanctl --load-all
会进到 callback_job_create_with_prio
    调用堆栈：
        0  callback_job_create_with_prio (cb=0x7ffff7ba01f3 <notify_async>, ...) at processing/jobs/callback_job.c:101
        1  0x00007ffff7ba0440 in notify (this=0x610ce0, entry=0x6567e0, event=WATCHER_READ) at processing/watcher.c:267
        2  0x00007ffff7ba0b0b in watch (this=0x610ce0) at processing/watcher.c:449
        3  0x00007ffff7b9e2b9 in execute (this=0x64df10) at processing/jobs/callback_job.c:77
        4  0x00007ffff7b9e828 in process_job (this=0x610410, worker=0x65f370) at processing/processor.c:235
        5  0x00007ffff7b9eb2a in process_jobs (worker=0x65f370) at processing/processor.c:321
        6  0x00007ffff7bb6dfc in thread_main (this=0x65f3a0) at threading/thread.c:331
        7  0x00007ffff7372ea5 in start_thread () from /lib64/libpthread.so.0
        8  0x00007ffff6e97b0d in clone () from /lib64/libc.so.6
    首先关注的是调用堆栈中的 watch 函数
        watch   //libvici.c Dispatching function    猜测应该是vici插件初始化时创建的循环任务
            遍历 vici（private_watcher_t） 的 fds（entry_t） 成员
                监视等待(poll) 该 fd
                    当可读时， notify(this, entry, WATCHER_READ);
                    当可写时， notify(this, entry, WATCHER_WRITE);
                    notify将"文件可读"这一事件打包成任务(回调 notify_async )，添加到任务队列中 （private_watcher_t *this->jobs）
                如果 this->jobs 不为空，则
                    移除并交给processor执行该job : lib->processor->execute_job(lib->processor, job);
                        job添加到 private_processor_t *this->jobs 任务队列中，或（没有空闲线程时）直接执行该job
                            调用执行 notify_async
    其它空闲线程（包括本线程）会处理该任务，
        进入到 notify_async ： watcher.c
            data->keep = data->cb(data->data, data->fd, data->event);
                watch ：stream_service.c
                    async_data_t *data——>fd = accept(data->fd,NULL,NULL)
                    添加任务给processor，回调 accept_async : stream_service.c
    其他空闲线程（包括本线程）会进到 accept_async 函数 （响应连接请求）
        调用堆栈：
            0  _cb_on_accept (this=0x6569d0, stream=0x7fffc80009f0) at vici_socket.c:573  //添加读任务，记录该连接
            1  0x00007ffff7b99350 in accept_async (data=0x7fffc8000940) at networking/streams/stream_service.c:189
            2  0x00007ffff7b9e2b9 in execute (this=0x7fffc8000970) at processing/jobs/callback_job.c:77
            3  0x00007ffff7b9e828 in process_job (this=0x610410, worker=0x65df20) at processing/processor.c:235
            4  0x00007ffff7b9eb2a in process_jobs (worker=0x65df20) at processing/processor.c:321
            5  0x00007ffff7bb6dfc in thread_main (this=0x65df50) at threading/thread.c:331
            6  0x00007ffff7372ea5 in start_thread () from /lib64/libpthread.so.0
            7  0x00007ffff6e97b0d in clone () from /lib64/libc.so.6
        
vm2执行ipsec up h2h:
输出： 11[CFG] received stroke: initiate 'h2h'    
根据日志输出内容，在相应代码处打断点，
调用堆栈：
    0  stroke_initiate (this=0x64f220, msg=0x7fffac000a80, out=0x7fffac000d20) at stroke_socket.c:248
    1  0x00007ffff2197d69 in on_accept (this=0x64f220, stream=0x7fffac0009f0) at stroke_socket.c:664
    2  0x00007ffff7b99350 in accept_async (data=0x7fffac000940) at networking/streams/stream_service.c:189
    3  0x00007ffff7b9e2b9 in execute (this=0x7fffac000970) at processing/jobs/callback_job.c:77
    4  0x00007ffff7b9e828 in process_job (this=0x610410, worker=0x65caf0) at processing/processor.c:235
    5  0x00007ffff7b9eb2a in process_jobs (worker=0x65caf0) at processing/processor.c:321
    6  0x00007ffff7bb6dfc in thread_main (this=0x65cb20) at threading/thread.c:331
    7  0x00007ffff7372ea5 in start_thread () from /lib64/libpthread.so.0
    8  0x00007ffff6e97b0d in clone () from /lib64/libc.so.6

process_job
    worker->job->execute(worker->job);
        job->callback(job->data)
            accept_async(async_data_t *data)    #Async processing of accepted connection
                stream_t *stream = stream_create_from_fd(data->fd);
                thread_cleanup_push(reduce_running, data);
                thread_cleanup_push((void*)stream->destroy, stream);
                bool b = data->cb(data->data, stream);
                     bool on_accept(private_stroke_socket_t *this, stream_t *stream)
                        从 stream 中读取 stroke_msg_t *msg
                        switch (msg->type)
                            case STR_INITIATE
                            case STR_ROUTE
                            case STR_TERMINATE
                            case STR_REKEY
                            case STR_STATUS
                            case STR_ADD_CONN
                            case STR_DEL_CONN
                            case STR_ADD_CA
                            case STR_DEL_CA
                            case STR_CONFIG
                            case STR_USER_CREDS
                            case ......
                thread_cleanup_pop(!b);
                thread_cleanup_pop(TRUE);

关于 accept_async
    该job是 stream_service.c : watch 函数中添加的
    
执行 ipsec up h2h  后：
    job 的创建：
    stroke_socket.c : on_accept
        stroke_socket.c : stroke_initiate
            (private_stroke_socket_t*) this->control->initiate(msg, out);
                stroke_control.c : initiate
                    stroke_control.c : charon_initiate
                        charon->controller->initiate(...)
                            controller.c : initiate
                                controller.c : wait_for_listener
                                    charon->bus->add_listener(job->listener)
                                    lib->processor->queue_job(job->public)
    stroke_socket.c : stroke_initiate
        peer_cfg_t *peer_cfg = charon->backends->get_peer_cfg_by_name("h2h")
        if(peer_cfg)  //如果配置文件正确，通常应该是有该peer_cfg的
            child_cfg_t *child_cfg = get_child_from_peer(peer_cfg, "h2h")
                //有个叫"child-h2h"的child_cfg，与"h2h"不同名，所以返回值为空
            if (child_cfg == NULL)
                enumerator = peer_cfg->create_child_cfg_enumerator(peer_cfg);
                while (enumerator->enumerate(enumerator, &child_cfg))  //有一个"child_h2h"的
                {
                    empty = FALSE;  //标记不为空
                    charon_initiate(this, peer_cfg, child_cfg, msg, out);  //见下文
                }
                如果 empty 为真 //表明peer_cfg中没有chhild-cfg
                    输出日志：no child config named h2h
                return
            else
                return
        else
            ...  这里不关注，不会走到这里
    stroke_socket.c : charon_initiate  #被 stroke_initiate 调用
        if (msg->output_verbosity < 0) //消息输出的详细程度 from -1=silent to 4=private 在执行ipsec时指定
            charon->controller->initiate(charon->controller, peer_cfg, child_cfg,NULL, NULL, 0, FALSE);
        else  // msg->output_verbosity = 1
            ...  
            虽然调试时走了这一块代码，但其实就是多了些日志输出的东西，实际功能跟上面一样
    controller.c : initiate  #被 charon_initiate 调用
        interface_job_t * job 创建并初始化
        调用 initiate_execute 执行该job
    controller.c : initiate_execute #被 initiate 调用，这块代码实现关键功能
        ike_sa_t *ike_sa = charon->ike_sa_manager->checkout_by_config(peer_cfg)
        interface_listener_t *listener = &job->listener
        listener->ike_sa = ike_sa
        if (ike_sa->get_peer_cfg(ike_sa) == NULL) 
            ike_sa->set_peer_cfg(ike_sa, peer_cfg);
        //刚创建出来的 ike_sa 即为 IKE_CREATED 状态，但listener->options.limits为空
        if (listener->options.limits && ike_sa->get_state(ike_sa) == IKE_CREATED)
            。。。
        ike_sa->initiate(listener->child_cfg, 0, NULL, NULL)
        charon->ike_sa_manager->checkin(ike_sa);    //检入sa
    ike_sa_manager.c : checkout_by_config(private_ike_sa_manager_t *this,peer_cfg_t *peer_cfg)  #被 initiate_execute 调用
        private_enumerator_t *enumerator0
        INIT(enumerator0,
            .enumerator = {
                .enumerate = enumerator_enumerate_default,
                .venumerate = _enumerate,
                .destroy = _enumerator_destroy,
            },
            .manager = this,
        );
        enumerator_t *enumerator = enumerator0->enumerator
        entry_t *entry;
        u_int segment;
        while (enumerator->venumerate( &entry, &segment))
            <=> while enumerate(private_enumerator_t *this,&entry, &segment)
            。。。参照segment_count，查ike_sa_table
            这块代码返回为FALSE
        if (!ike_sa)
            ike_sa = checkout_new(this, peer_cfg->get_ike_version(peer_cfg), TRUE);
        charon->bus->set_sa(charon->bus, ike_sa);  //Set a thread-specific value
        return ike_sa
    ike_sa_manager.c : checkout_new(ike_version_t version=IKEV2, bool initiator=TRUE)  #被 checkout_by_config 调用
        uint64_t spi = get_spi(this); //Get a random SPI for new IKE_SAs
        //Creates an ike_sa_id_t object.
        ike_sa_id_t *ike_sa_id = ike_sa_id_create(IKEV2, spi, 0, TRUE)  
        //Creates an ike_sa_t object with a specific ID and IKE version.
        ike_sa = ike_sa_create(ike_sa_id, initiator, version); 
        return ike_sa
    ike_sa.c : initiate  #被 initiate_execute 调用
        if (this->state == IKE_CREATED)
            resolve_hosts(this);
                功能：
                    根据配置的ip，创建了ike_sa的my_host和other_host
                int family = ike_cfg_get_family(TRUE);
                    int family = AF_UNSPEC
                    for str in this->my_hosts
                        host_t *host = host_create_from_string(str, 0)
                            host_t *host_create_from_string_and_family(
                                        char *string = 192.168.3.108,  //本机ip 
                                        int family = 0,  //AF_UNSPEC
                                        uint16_t port = 0)
                                struct sockaddr_in addr
                                addr.sin_addr = inet_pton(string)
                                addr.sin_port = htons(port)
                                addr.sin_family = AF_INET
                                host_t *host_create_from_sockaddr(addr)
                                    private_host_t *this = 创建该对象
                                    将参数addr存给this->address4
                                    update_sa_len(this)
                                    return this->public
                        if (family == AF_UNSPEC)
                                family = host->get_family()
                    return family
                host_t *host = this->ike_cfg->resolve_other(family)
                    ike_cfg.c : resolve(this->other_hosts,family=2,port=500) //500是默认配置
                        for str in hosts  //str = 192.168.3.166
                            host_t *host = host_create_from_dns(str, family, port);
                            if(host) break;
                        return host
                if(host->is_anyaddr()==false || this->other_host->is_anyaddr())
                    this->other_host = host
                family = this->other_host->get_family() = 2
                host = this->ike_cfg->resolve_me(family);
                    ike_cfg.c : resolve(this->my_hosts,family=2,port=500)
                my_host = host
            if(this->other_host->is_anyaddr())  //根据上面的resolve_hosts，可知为假
                ...    
            //Enable/disable a condition flag for this IKE_SA
            set_condition(this, COND_ORIGINAL_INITIATOR, TRUE);
            this->task_manager->queue_ike()
                queue_task(this, (task_t*)ike_vendor_create(this->ike_sa, TRUE));
                    queue_task_delayed(this, task, 0);
                        queued_task_t* queued = 创建并初始化
                        array_insert(this->queued_tasks, ARRAY_TAIL, queued);
                queue_task(this, (task_t*)ike_init_create(this->ike_sa, TRUE, NULL));
                queue_task(this, (task_t*)ike_natd_create(this->ike_sa, TRUE));
                queue_task(this, (task_t*)ike_cert_pre_create(this->ike_sa, TRUE));
                queue_task(this, (task_t*)ike_auth_create(this->ike_sa, TRUE));
                queue_task(this, (task_t*)ike_cert_post_create(this->ike_sa, TRUE));
                queue_task(this, (task_t*)ike_config_create(this->ike_sa, TRUE));
                queue_task(this, (task_t*)ike_auth_lifetime_create(this->ike_sa, TRUE));
                if (peer_cfg->use_mobike(peer_cfg))  //调试时，条件为假
                    queue_task(this, (task_t*)ike_mobike_create(this->ike_sa, TRUE));
        if(child_cfg)  //controller.c : initiate创建job时，将child_cfg存给了listener的child_cfg成员
            this->task_manager->queue_child(this->task_manager, 
                                            child_cfg, reqid, tsi, tsr);
                child_create_t *task = child_create_create(this->ike_sa, cfg, FALSE, tsi, tsr)
                    创建并初始化 private_child_create_t 对象，并返回其 public
                queue_task(this, &task->task);
        return this->task_manager->initiate(this->task_manager)
            switch(this->ike_sa->get_state())
                case IKE_CREATED:
                    activate_task(this, TASK_IKE_VENDOR);
                        遍历 this->queued_tasks, 找到type与参数一致的task
                        从queued_tasks中移出，放到active_tasks的尾部
                    if (activate_task(this, TASK_IKE_INIT))
                        activate_task(this, TASK_IKE_NATD);
                        activate_task(this, TASK_IKE_CERT_PRE);
                        activate_task(this, TASK_IKE_AUTH);
                        activate_task(this, TASK_IKE_CERT_POST);
                        activate_task(this, TASK_IKE_CONFIG);
                        activate_task(this, TASK_CHILD_CREATE);
                        activate_task(this, TASK_IKE_AUTH_LIFETIME);
                        activate_task(this, TASK_IKE_MOBIKE);
                case IKE_ESTABLISHED:
                    ...
                case IKE_REKEYING:
                case IKE_REKEYED:
                    activate_task(this, TASK_IKE_DELETE)
            host_t *me = this->ike_sa->get_my_host()
            host_t *other = this->ike_sa->get_other_host()
            message_t *message = message_create(IKEV2_MAJOR_VERSION, IKEV2_MINOR_VERSION)
                packet_t *packet = packet_create()
                    return packet_create_from_data(NULL, NULL, chunk_empty);
                        private_packet_t *this 创建并初始化
                        返回 this->public
            message_t *this = message_create_from_packet(packet);
            message->set_message_id(message, this->initiating.mid=0);
            message->set_source(message, me->clone(me));
            message->set_destination(message, other->clone(other));
            message->set_exchange_type(message, exchange=IKE_SA_INIT);    
            for task in this->active_tasks
                task->build(task, message)
                    功能：
                        Build a request or response message for this task.
                        不同的task，调用不同的build方法
                        ike_vendor.c : build
                            遍历 vids (静态常量结构体数组)
                                依据vids[i]，从配置文件中查看是否需要 send vendor id
                                是
                                   vid = vendor_id_payload_create_data(
                                            PLV2_VENDOR_ID ,get_vid_data(vids[i]) )
                            //实际没有一个需要发送vnedor id 的，所以该函数相当于什么也没干
                        ike_init.c : buid_i
                            ike_cfg_t *ike_cfg = this->ike_sa->get_ike_cfg()
                            this->ike_sa->set_state(IKE_CONNECTING)
                            if(!this->dh)  //条件满足
                                if (this->old_sa && lib->settings->get_bool(lib->settings,
                                        "%s.prefer_previous_dh_group", TRUE, lib->ns)) //不满足
                                    。。。
                                else
                                    //在ike_sa->set_peer_cfg时，完成的 ike_cfg的赋值
                                    this->dh_group = ike_cfg->get_dh_group(ike_cfg); 
                                        for proposal in this->proposals /*提案*/
                                            if proposal->get_algorithm(proposal, DIFFIE_HELLMAN_GROUP, &dh_group, NULL)
                                                break
                                    this->dh = this->keymat->keymat.create_dh(this->dh_group)
                                        for entry in this->dhs
                从 active_tasks 中移除该task