状态机数据结构
    &<OSSL_STATEM>
    //用于状态机的结构体,该结构是SSL结构体的成员
    struct ossl_statem_st {         
        MSG_FLOW_STATE state;
        WRITE_STATE write_state;
        WORK_STATE write_state_work;
        READ_STATE read_state;
        WORK_STATE read_state_work;
        OSSL_HANDSHAKE_STATE hand_state;
        int in_init;
        int read_state_first_init;
        /* true when we are actually in SSL_accept() or SSL_connect() */
        int in_handshake;
        /* Should we skip the CertificateVerify message? */
        unsigned int no_cert_verify;
        int use_timer;
    };
    typedef struct ossl_statem_st OSSL_STATEM
    &<MSG_FLOW_STATE>
    typedef enum {
        /* No handshake in progress */
        MSG_FLOW_UNINITED,
        /* A permanent error with this connection */
        MSG_FLOW_ERROR,
        /* We are about to renegotiate */
        MSG_FLOW_RENEGOTIATE,
        /* We are reading messages */
        MSG_FLOW_READING,
        /* We are writing messages */
        MSG_FLOW_WRITING,
        /* Handshake has finished */
        MSG_FLOW_FINISHED
    } MSG_FLOW_STATE;
    
    &<READ_STATE>
    typedef enum {
        READ_STATE_HEADER,
        READ_STATE_BODY,
        READ_STATE_POST_PROCESS
    } READ_STATE;
    
    &<WRITE_STATE>
    typedef enum {
        WRITE_STATE_TRANSITION,
        WRITE_STATE_PRE_WORK,
        WRITE_STATE_SEND,
        WRITE_STATE_POST_WORK
    } WRITE_STATE;
    &<WORK_STATE>
    typedef enum {
        /* Something went wrong */
        WORK_ERROR,
        /* We're done working and there shouldn't be anything else to do after */
        WORK_FINISHED_STOP,
        /* We're done working move onto the next thing */
        WORK_FINISHED_CONTINUE,
        /* We're working on phase A */
        WORK_MORE_A,
        /* We're working on phase B */
        WORK_MORE_B
    } WORK_STATE;
    &<OSSL_HANDSHAKE_STATE>
    typedef enum {
        TLS_ST_BEFORE,
        TLS_ST_OK,
        DTLS_ST_CR_HELLO_VERIFY_REQUEST,
        TLS_ST_CR_SRVR_HELLO,
        TLS_ST_CR_CERT,
        TLS_ST_CR_CERT_STATUS,
        TLS_ST_CR_KEY_EXCH,
        TLS_ST_CR_CERT_REQ,
        TLS_ST_CR_SRVR_DONE,
        TLS_ST_CR_SESSION_TICKET,
        TLS_ST_CR_CHANGE,
        TLS_ST_CR_FINISHED,
        TLS_ST_CW_CLNT_HELLO,
        TLS_ST_CW_CERT,
        TLS_ST_CW_KEY_EXCH,
        TLS_ST_CW_CERT_VRFY,
        TLS_ST_CW_CHANGE,
        TLS_ST_CW_NEXT_PROTO,
        TLS_ST_CW_FINISHED,
        TLS_ST_SW_HELLO_REQ,
        TLS_ST_SR_CLNT_HELLO,
        DTLS_ST_SW_HELLO_VERIFY_REQUEST,
        TLS_ST_SW_SRVR_HELLO,
        TLS_ST_SW_CERT,
        TLS_ST_SW_KEY_EXCH,
        TLS_ST_SW_CERT_REQ,
        TLS_ST_SW_SRVR_DONE,
        TLS_ST_SR_CERT,
        TLS_ST_SR_KEY_EXCH,
        TLS_ST_SR_CERT_VRFY,
        TLS_ST_SR_NEXT_PROTO,
        TLS_ST_SR_CHANGE,
        TLS_ST_SR_FINISHED,
        TLS_ST_SW_SESSION_TICKET,
        TLS_ST_SW_CERT_STATUS,
        TLS_ST_SW_CHANGE,
        TLS_ST_SW_FINISHED
    } OSSL_HANDSHAKE_STATE;
记录层数据结构
    &<RECORD_LAYER>
    typedef struct record_layer_st {
        /* The parent SSL structure */
        SSL *s;
        /*
         * Read as many input bytes as possible (for
         * non-blocking reads)
         */
        int read_ahead;
        /* where we are when reading */
        int rstate;
        /* How many pipelines can be used to read data */
        unsigned int numrpipes;
        /* How many pipelines can be used to write data */
        unsigned int numwpipes;
        /* read IO goes into here */
        SSL3_BUFFER rbuf;
        /* write IO goes into here */
        SSL3_BUFFER wbuf[SSL_MAX_PIPELINES=32];
        /* each decoded record goes in here */
        SSL3_RECORD rrec[SSL_MAX_PIPELINES];
        /* used internally to point at a raw packet */
        unsigned char *packet;
        unsigned int packet_length;
        /* number of bytes sent so far */
        unsigned int wnum;
        /*
         * storage for Alert/Handshake protocol data received but not yet
         * processed by ssl3_read_bytes:
         */
        unsigned char alert_fragment[2];
        unsigned int alert_fragment_len;
        unsigned char handshake_fragment[4];
        unsigned int handshake_fragment_len;
        /* The number of consecutive empty records we have received */
        unsigned int empty_record_count;
        /* partial write - check the numbers match */
        /* number bytes written */
        int wpend_tot;
        int wpend_type;
        /* number of bytes submitted */
        int wpend_ret;
        const unsigned char *wpend_buf;
        unsigned char read_sequence[SEQ_NUM_SIZE];
        unsigned char write_sequence[SEQ_NUM_SIZE];
        /* Set to true if this is the first record in a connection */
        unsigned int is_first_record;
        /* Count of the number of consecutive warning alerts received */
        unsigned int alert_count;
        DTLS_RECORD_LAYER *d;
    } RECORD_LAYER;
    &<SSL3_BUFFER>
    typedef struct ssl3_buffer_st {
        /* at least SSL3_RT_MAX_PACKET_SIZE bytes, see ssl3_setup_buffers() */
        unsigned char *buf;
        /* default buffer size (or 0 if no default set) */
        size_t default_len;
        /* buffer size */
        size_t len;
        /* where to 'copy from' */
        int offset;
        /* how many bytes left */
        int left;
    } SSL3_BUFFER;
状态机
SSL_do_handshake(SSL *s)
{
    s->statem.in_init!=0 &&
    s->statem.hand_state == TLS_ST_BEFORE &&
    s->statem.state == MSG_FLOW_UNINITED
        s->handshake_func(SSL *=s)
            state_machine(SSL *=s, int server=1)
                RAND_add(&Time, sizeof(Time), 0)  //设置随机种子