client ：

state_machine
    if (st->state == MSG_FLOW_UNINITED)
        st->hand_state = TLS_ST_BEFORE
        s->server=0
        s->init_buf = 申请buf，并扩充到SSL3_RT_MAX_PLAIN_LENGTH=16384长度
        申请记录层读写buffer
        s->init_num = 0
        s->s3->change_cipher_spec = 0
        s->bbio = 申请buf，；类型为 BIO_TYPE_BUFFER，设置大小为1
        s->wbio = 追加 s->bbio
        释放 s->s3->handshake_buffer
        释放 s->s3->handshake_dgst
        s->s3->handshake_buffer = 申请内存读写BIO（BIO_TYPE_MEM）
        s->ctx->stats.sess_connect++ ，变为1
        s->s3->client_random 初始化为0
        s->hit = 0;
        s->s3->tmp.cert_req = 0;
        st->state = MSG_FLOW_WRITING
        s->statem->write_state = WRITE_STATE_TRANSITION
        st->read_state_first_init = 1
    while (st->state != MSG_FLOW_FINISHED)
        if (st->state == MSG_FLOW_READING)
        if (st->state == MSG_FLOW_WRITING)
            ::write_state_machine
    
init_write_state_machine 
    st = s->statem
    while(1)
        switch (st->write_state)   
            case WRITE_STATE_TRANSITION:   //先进这里
                switch (transition(s))  @transition1
                    case WRITE_TRAN_CONTINUE
                        st->write_state = WRITE_STATE_PRE_WORK;
                        st->write_state_work = WORK_MORE_A;
            case WRITE_STATE_PRE_WORK  //第二步进这里
                state = pre_work(s, st->write_state_work) @pre_work1
                st->write_state_work = state
                switch(state)
                    case WORK_FINISHED_CONTINUE:
                        st->write_state = WRITE_STATE_SEND
                construct_message(s) @ossl_statem_client_construct_message
                
                
pre_work(SSL *s, WORK_STATE wst) &<pre_work1>
    st = s->statem
    switch (st->hand_state)
        case TLS_ST_CW_CLNT_HELLO:
            s->shutdown = 0;
            return WORK_FINISHED_CONTINUE

construct_message(SSL *s) &<ossl_statem_client_construct_message>
    switch (st->hand_state)
        case TLS_ST_CW_CLNT_HELLO:
            return tls_construct_client_hello(s);  @tls_construct_client_hello
    
transition &<transition1>           
    switch (st->hand_state)
        case TLS_ST_BEFORE:
            st->hand_state = TLS_ST_CW_CLNT_HELLO;
            return WRITE_TRAN_CONTINUE;
            
tls_construct_client_hello(SSL *s) &<tls_construct_client_hello>
    ssl_set_client_hello_version
        SSL_SESSION *sess = s->session
        s->client_version = s->version;
    ssl_get_new_session
        s->session = SSL_SESSION_new
        设置 s->session 的成员初始值
    ssl_fill_hello_random
        为 s->s3->client_random 设置随机值
    ssl_handshake_start
        