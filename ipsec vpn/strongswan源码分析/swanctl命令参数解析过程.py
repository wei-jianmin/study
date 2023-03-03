file://command中的结构与变量.h

main:
library_init(NULL, "swanctl"))
lib->plugins->load(lib->plugins,lib->settings->get_str(lib->settings, "swanctl.load", PLUGINS))
lib->processor->set_threads(lib->processor, 4);	  
//上面三行参：file://strongswan简要流程及数据结构.py
command_dispatch
    command_register
        注册支持 h/help 命令参数
    build_opts
        根据cmds文件全局变量，初始化command_opts、command_optstring
        为 getopt_long 做准备
    getopt_long
        linux命令，判断参数是指定参数列表中的哪一个
    build_opts
        遍历 cmds[active].options
    getopt_long
        获取子命令
    call_command(cmd = &cmds[i]);
        vici_conn_t *conn = vici_connect(uri);
            //libvici.c
            stream_t *stream = lib->streams->connect(private_stream_manager_t *this = lib->streams, 
                                                     char* uri = uri ?: VICI_DEFAULT_URI);  //uri = "unix:///var/run/charon.vici"
                for stream_entry_t *entry in this->streams
                    if entry->prefix 与uri的前缀一致 //"unix://"、"tcp://"等
                        stream_t *stream = entry->create(uri);
                            stream_create_unix(char* uri)
                                int fd = socket(AF_UNIX, SOCK_STREAM, 0);
                                int len = stream_parse_uri_unix(uri, &addr);
                                connect(fd, (struct sockaddr*)&addr, len) 
                                return stream_create_from_fd(fd);
                                    private_stream_t *this 初始化
                                    this.fd = fd
                                    return this->public
                        return stream
            初始化 vici_conn_t *conn
                conn.stream = stream
            stream->on_read(private_stream_t *this = stream, 
                             stream_cb_t cb = on_read/*回调函数*/, 
                             void *data = conn);
                //stream.c
                lib->watcher->remove(private_watcher_t *this = lib->watcher, int fd = this->fd);  
                    //关于private_watcher_t，参 file://watcher.c | file://watcher中的结构与变量.h
                    while(1)
                        foreach entry_t *entry in this->fds  //此时this->fds还是空的
                            if this->state为WATCHER_QUEUED或WATCHER_RUNNING 且 entry->in_callback
                                设中断标记为真，中断循环
                            remove_entry(entry);
                        如果中断标记为真，中断循环
                        this->condvar->wait(this->condvar, this->mutex);
                this->read_cb = cb;
                this->read_data = data;
                add_watcher(private_stream_t *this);
                    watcher_event_t events = 0;
                    if(this->read_cb)    events 增加 WATCHER_READ  标记
                    if (this->write_cb)  events 增加 WATCHER_WRITE 标记               
                    lib->watcher->add(  private_watcher_t *this=lib->watcher, 
                                        int fd = this->fd,
                                        watcher_event_t events,
                                        watcher_cb_t cb=watch/*回调函数*/, 
                                        void*data = this);
                        entry_t *entry 初始化
                            entry中记录了fd/events/cb/data等参数
                        add_entry(this, entry);
                        if (this->state == WATCHER_STOPPED) √
                            this->state = WATCHER_QUEUED;
                            job_t* job = callback_job_create_with_prio( callback_job_cb_t cb = (void*)watch/*回调函数*/,
                                                                        void *data = this, 
                                                                        callback_job_cleanup_t cleanup = NULL,
                                                                        callback_job_cancel_t cancel = return_false, 
                                                                        job_priority_t prio = JOB_PRIO_CRITICAL
                                                                       )
                                private_callback_job_t* this 初始化
                                    .callback = cb,
                                    .data = data,
                                    .cleanup = cleanup,
                                    .cancel = cancel,
                                    .prio = prio,
                                return this.public
                            ib->processor->queue_job(job)
                                       
                                       
            return conn
        cmd->call(conn)
            int load_all(vici_conn_t *conn) //load_all.c,因为参数传的的是--load-all，所以对应这个cmd相对
                判断--load-all后面的子选项，例如可以通过-f子选项指定配置文件位置，通过-h获取帮助，这里没有传子选项
                settings_t *cfg = load_swanctl_conf(file);  file默认为 /etc/swanctl/swanctl.conf
                bool clear = FALSE, noprompt = FALSE;
                command_format_options_t format = COMMAND_FORMAT_NONE;
                load_creds_cfg(conn, format, cfg, bool clear, bool noprompt);  //Load all credentials from configuration file
                    load_ctx_t ctx 初始化,conn、format、noprompt、cfg 等参数均被记录在ctx中，ctx结构参：file://load_creds.c
                    if(clear)  clear_creds(conn, format)
                        vici_req_t *req = vici_begin("clear-creds")
                                vici_req_t *req 初始化  //参：file://libvici.h
                                req.name = name
                                req.b = vici_builder_create()  // b 表示message builder
                                    private_vici_builder_t* this 初始化  //参：file://vici_builder.c
                                    返回 this->public
                                return req
                         vici_res_t *res = vici_submit(req, conn);
                    get_creds(&ctx);    
                        vici_req_t *req = vici_begin("get-keys")  //在前面已经展开过
                        vici_res_t *res = vici_submit(vici_req_t *req, ctx->conn);
                            vici_message_t *message = req->b->finalize(private_vici_builder_t *this = req->b)
                                chunk_t data = this->writer->extract_buf(this->writer)
                                    chunk_t ret = get_buf(private_bio_writer_t *this);
                                        chunk_create(this->buf.ptr, this->used)
                                            return chunk_t{ptr, len};  //ptr=null,len=0
                                vici_message_t *product = vici_message_create_from_data(data, TRUE)  //vici_builder.c
                                    extract_buf(private_bio_writer_t *this)
                                        this->buf = chunk_empty;
                                        this->used = 0;
                                        return ret;
                                    private_vici_message_t *this 初始化
                                    return this->public;
                                return product
                            uint8_t op = VICI_CMD_REQUEST
                            uint8_t namelen = strlen(req->name);
                            chunk_t data = message->get_encoding(message);
                                return this->encoding   //null
                            onn->stream->write_all(conn->stream, &len, sizeof(len)) 
                                write_all(private_stream_t *this, void *buf, size_t len)
                                write_(this, buf, len, TRUE);   
                                    send(this->fd, buf, len, 0)
                            conn->stream->write_all(conn->stream, &op, sizeof(op)) 
                            conn->stream->write_all(conn->stream, &namelen, sizeof(namelen)) 
                            conn->stream->write_all(conn->stream, req->name, namelen) 
                            conn->stream->write_all(conn->stream, data.ptr, data.len))
                            while (conn->wait == WAIT_IDLE)
                                conn->cond->wait(conn->cond, conn->mutex);
                            switch (conn->wait)
                                case WAIT_SUCCESS:
                                    message = vici_message_create_from_data(chunk_t data=conn->queue,  bool cleanup=TRUE);
                                        private_vici_message_t *this = 初始化
                                        data和cleanup分别记录在.encoding和.cleanup成员中
                                        return this.public
                                    conn->queue = chunk_empty;
                            conn->wait = WAIT_IDLE;
                            conn->stream->on_read(conn->stream, on_read, conn);
                                on_read(private_stream_t *this,stream_cb_t cb, void *data)  //stream.c
                                    lib->watcher->remove(this->fd);  //wacher.c
                                        while(1)
                                            foreach entry_t *entry in this->fds
                                                if this->state为WATCHER_QUEUED或WATCHER_RUNNING 且 entry->in_callback
                                                    设中断标记为真，中断循环
                                                remove_entry(entry);
                                            如果中断标记为真，中断循环
                                            this->condvar->wait(this->condvar, this->mutex);
                                    this->read_cb = cb;
                                    this->read_data = data;
                                    add_watcher(private_stream_t *this);  //stream.c，前面已经展开过
                        vici_parse_cb(res, NULL, NULL, get_id, ctx->keys);  
                        vici_req_t *req = vici_begin("get-shared")
                        vici_res_t *res = vici_submit(req, ctx->conn);
                        vici_parse_cb(res, NULL, NULL, get_id, ctx->shared);
                    load_certs(&ctx, "x509",     SWANCTL_X509DIR);
                    load_certs(&ctx, "x509ca",   SWANCTL_X509CADIR);
                    load_certs(&ctx, "x509ocsp", SWANCTL_X509OCSPDIR);
                    load_certs(&ctx, "x509aa",   SWANCTL_X509AADIR);
                    load_certs(&ctx, "x509ac",   SWANCTL_X509ACDIR);
                    load_certs(&ctx, "x509crl",  SWANCTL_X509CRLDIR);
                    load_certs(&ctx, "pubkey",   SWANCTL_PUBKEYDIR);
                    load_keys(&ctx, "private", SWANCTL_PRIVATEDIR);
                    load_keys(&ctx, "rsa",     SWANCTL_RSADIR);
                    load_keys(&ctx, "ecdsa",   SWANCTL_ECDSADIR);
                    load_keys(&ctx, "bliss",   SWANCTL_BLISSDIR);
                    load_keys(&ctx, "pkcs8",   SWANCTL_PKCS8DIR);
                    ......
                load_authorities_cfg(conn, format, cfg);
                load_pools_cfg(conn, format, cfg);
                load_conns_cfg(conn, format, cfg);
        vici_disconnect(conn)