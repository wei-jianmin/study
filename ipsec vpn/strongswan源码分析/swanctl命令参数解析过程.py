file://command�еĽṹ�����.h

main:
library_init(NULL, "swanctl"))
lib->plugins->load(lib->plugins,lib->settings->get_str(lib->settings, "swanctl.load", PLUGINS))
lib->processor->set_threads(lib->processor, 4);	  
//�������вΣ�file://strongswan��Ҫ���̼����ݽṹ.py
command_dispatch
    command_register
        ע��֧�� h/help �������
    build_opts
        ����cmds�ļ�ȫ�ֱ�������ʼ��command_opts��command_optstring
        Ϊ getopt_long ��׼��
    getopt_long
        linux����жϲ�����ָ�������б��е���һ��
    build_opts
        ���� cmds[active].options
    getopt_long
        ��ȡ������
    call_command(cmd = &cmds[i]);
        vici_conn_t *conn = vici_connect(uri);
            //libvici.c
            stream_t *stream = lib->streams->connect(private_stream_manager_t *this = lib->streams, 
                                                     char* uri = uri ?: VICI_DEFAULT_URI);  //uri = "unix:///var/run/charon.vici"
                for stream_entry_t *entry in this->streams
                    if entry->prefix ��uri��ǰ׺һ�� //"unix://"��"tcp://"��
                        stream_t *stream = entry->create(uri);
                            stream_create_unix(char* uri)
                                int fd = socket(AF_UNIX, SOCK_STREAM, 0);
                                int len = stream_parse_uri_unix(uri, &addr);
                                connect(fd, (struct sockaddr*)&addr, len) 
                                return stream_create_from_fd(fd);
                                    private_stream_t *this ��ʼ��
                                    this.fd = fd
                                    return this->public
                        return stream
            ��ʼ�� vici_conn_t *conn
                conn.stream = stream
            stream->on_read(private_stream_t *this = stream, 
                             stream_cb_t cb = on_read/*�ص�����*/, 
                             void *data = conn);
                //stream.c
                lib->watcher->remove(private_watcher_t *this = lib->watcher, int fd = this->fd);  
                    //����private_watcher_t���� file://watcher.c | file://watcher�еĽṹ�����.h
                    while(1)
                        foreach entry_t *entry in this->fds  //��ʱthis->fds���ǿյ�
                            if this->stateΪWATCHER_QUEUED��WATCHER_RUNNING �� entry->in_callback
                                ���жϱ��Ϊ�棬�ж�ѭ��
                            remove_entry(entry);
                        ����жϱ��Ϊ�棬�ж�ѭ��
                        this->condvar->wait(this->condvar, this->mutex);
                this->read_cb = cb;
                this->read_data = data;
                add_watcher(private_stream_t *this);
                    watcher_event_t events = 0;
                    if(this->read_cb)    events ���� WATCHER_READ  ���
                    if (this->write_cb)  events ���� WATCHER_WRITE ���               
                    lib->watcher->add(  private_watcher_t *this=lib->watcher, 
                                        int fd = this->fd,
                                        watcher_event_t events,
                                        watcher_cb_t cb=watch/*�ص�����*/, 
                                        void*data = this);
                        entry_t *entry ��ʼ��
                            entry�м�¼��fd/events/cb/data�Ȳ���
                        add_entry(this, entry);
                        if (this->state == WATCHER_STOPPED) ��
                            this->state = WATCHER_QUEUED;
                            job_t* job = callback_job_create_with_prio( callback_job_cb_t cb = (void*)watch/*�ص�����*/,
                                                                        void *data = this, 
                                                                        callback_job_cleanup_t cleanup = NULL,
                                                                        callback_job_cancel_t cancel = return_false, 
                                                                        job_priority_t prio = JOB_PRIO_CRITICAL
                                                                       )
                                private_callback_job_t* this ��ʼ��
                                    .callback = cb,
                                    .data = data,
                                    .cleanup = cleanup,
                                    .cancel = cancel,
                                    .prio = prio,
                                return this.public
                            ib->processor->queue_job(job)
                                       
                                       
            return conn
        cmd->call(conn)
            int load_all(vici_conn_t *conn) //load_all.c,��Ϊ�������ĵ���--load-all�����Զ�Ӧ���cmd���
                �ж�--load-all�������ѡ��������ͨ��-f��ѡ��ָ�������ļ�λ�ã�ͨ��-h��ȡ����������û�д���ѡ��
                settings_t *cfg = load_swanctl_conf(file);  fileĬ��Ϊ /etc/swanctl/swanctl.conf
                bool clear = FALSE, noprompt = FALSE;
                command_format_options_t format = COMMAND_FORMAT_NONE;
                load_creds_cfg(conn, format, cfg, bool clear, bool noprompt);  //Load all credentials from configuration file
                    load_ctx_t ctx ��ʼ��,conn��format��noprompt��cfg �Ȳ���������¼��ctx�У�ctx�ṹ�Σ�file://load_creds.c
                    if(clear)  clear_creds(conn, format)
                        vici_req_t *req = vici_begin("clear-creds")
                                vici_req_t *req ��ʼ��  //�Σ�file://libvici.h
                                req.name = name
                                req.b = vici_builder_create()  // b ��ʾmessage builder
                                    private_vici_builder_t* this ��ʼ��  //�Σ�file://vici_builder.c
                                    ���� this->public
                                return req
                         vici_res_t *res = vici_submit(req, conn);
                    get_creds(&ctx);    
                        vici_req_t *req = vici_begin("get-keys")  //��ǰ���Ѿ�չ����
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
                                    private_vici_message_t *this ��ʼ��
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
                                        private_vici_message_t *this = ��ʼ��
                                        data��cleanup�ֱ��¼��.encoding��.cleanup��Ա��
                                        return this.public
                                    conn->queue = chunk_empty;
                            conn->wait = WAIT_IDLE;
                            conn->stream->on_read(conn->stream, on_read, conn);
                                on_read(private_stream_t *this,stream_cb_t cb, void *data)  //stream.c
                                    lib->watcher->remove(this->fd);  //wacher.c
                                        while(1)
                                            foreach entry_t *entry in this->fds
                                                if this->stateΪWATCHER_QUEUED��WATCHER_RUNNING �� entry->in_callback
                                                    ���жϱ��Ϊ�棬�ж�ѭ��
                                                remove_entry(entry);
                                            ����жϱ��Ϊ�棬�ж�ѭ��
                                            this->condvar->wait(this->condvar, this->mutex);
                                    this->read_cb = cb;
                                    this->read_data = data;
                                    add_watcher(private_stream_t *this);  //stream.c��ǰ���Ѿ�չ����
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