openssl�汾��0.9.8e
file://openssl.chm
opensslԴ����
    opensslԴ������Ҫ��eay�⡢ssl�⡢����Դ�롢����Դ���Լ�����Դ����ɡ�
    eay���ǻ����Ŀ⺯�����ṩ�˺ܶ๦�ܡ�Դ�������cryptoĿ¼�¡������������ݣ�
    1��  asn.1 DER�������(crypto/asn1Ŀ¼)���������˻���asn1����ı�����Լ�����֤������
         ����֤�顢CRL�����б��Լ�PKCS8��������ı���뺯������Щ������Ҫͨ������ʵ�֡�
    2��  ����IO(BIO,crypto/bioĿ¼)����Ŀ¼�µĺ����Ը�������������г��󣬰����ļ����ڴ桢��׼���������socket��SSLЭ��ȡ�
    3��  ��������(crypto/bnĿ¼)����Ŀ¼�µ��ļ�ʵ���˸��ִ������㡣��Щ����������Ҫ���ڷǶԳ��㷨����Կ�����Լ����ּӽ��ܲ�����
         ���⻹Ϊ�û��ṩ�˴������������������ڴ������֮����໥ת����
    4��  �ַ��������(crypto/bufferĿ¼)��
    5��  �����ļ���ȡ(crypto/confĿ¼)��openssl��Ҫ�������ļ�Ϊopenssl.cnf����Ŀ¼�µĺ���ʵ���˶����ָ�ʽ�����ļ��Ķ�ȡ������
    6��  DSO(��̬�������,crypto/dsoĿ¼)����Ŀ¼�µ��ļ���Ҫ�����˸���ƽ̨�Ķ�̬����غ�����Ϊ�û��ṩͳһ�ӿڡ�
    7��  Ӳ������(crypto/engineĿ¼)��Ӳ������ӿڡ��û����Ҫд�Լ���Ӳ�����棬����ʵ�������涨�Ľӿڡ�
    8��  ������(crypto/errĿ¼)����������ִ���ʱ��openssl���Զ�ջ����ʽ��ʾ��������
         ��Ŀ¼��ֻ�л����Ĵ�����ӿڣ�����ĵĴ�����Ϣ�ɸ���ģ���ṩ������ģ��ר�����ڴ�������ļ�һ��Ϊ*_err..c�ļ���
    9��  �Գ��㷨���ǶԳ��㷨��ժҪ�㷨��װ(crypto/evpĿ¼)��
    10�� HMAC(crypto/hmacĿ¼)��ʵ���˻��ڶԳ��㷨��MAC��
    11�� hash��(crypto/lhashĿ¼)��ʵ����ɢ�б����ݽṹ��openssl�кܶ����ݽṹ������ɢ�б�����ŵġ�
         ����������Ϣ��ssl session��asn.1������Ϣ�ȡ�
    12�� ����֤��������֤(crypto/ocspĿ¼)��ʵ����ocspЭ��ı�����Լ�֤����Ч�Լ���ȹ��ܡ�
    13�� PEM�ļ���ʽ����(crypto/pem)���������ɺͶ�ȡ����PEM��ʽ�ļ�������������Կ������֤����������֤�顢PKCS7��Ϣ��PKCS8��Ϣ�ȡ�
    14�� pkcs7��Ϣ�﷨(crypto/pkcs7Ŀ¼)����Ҫʵ���˹���ͽ���PKCS7��Ϣ��
    15�� pkcs12����֤���ʽ(crypto/pckcs12Ŀ¼)����Ҫʵ����pkcs12֤��Ĺ���ͽ�����
    16�� ����(crypto/pqueueĿ¼)��ʵ���˶������ݽṹ����Ҫ����DTLS��
    17�� �����(crypto/randĿ¼)��ʵ����α��������ɣ�֧���û��Զ�����������ɡ�
    18�� ��ջ(crypto/stackĿ¼)��ʵ���˶�ջ���ݽṹ��
    19�� �߳�֧��(crypto/threads)��openssl֧�ֶ��̣߳������û�����ʵ����ؽӿڡ�
    20�� �ı����ݿ�(crypto/txt_dbĿ¼)��
    21�� x509����֤��(crypto/x509Ŀ¼��crypto/x509v3)����������֤�����롢����֤���CRL�Ĺ��졢������ǩ����֤�ȹ����ˣ�
    22�� �Գ��㷨(crypto/aes��crypto/bf��crypto/cast��ccrypto/omp��crypto/des��Ŀ¼)��
    23�� �ǶԳ��㷨(crypto/dh��crypto/dsa��crypto/ec��crypto/ecdh)��
    24�� ժҪ�㷨(crypto/md2��crypto/md4��crypto/md5��crypto/sha)�Լ���Կ����/��֤�㷨(crypto/dh ��crypto/krb5)��

������ ��ջ
   ���ݽṹ
        typedef struct stack_st
        {
               int num;
               char **data;
               int sorted;
               int num_alloc;
               int (*comp)(const char * const *, const char * const *);
        } STACK;
        �����������£�
        num:       ��ջ�д�����ݵĸ�����
        data:      ���ڴ�����ݵ�ַ��ÿ�����ݵ�ַ�����data[0]��data[num-1]�С�
        sorted:    ��ջ�Ƿ����������������ֵΪ1������Ϊ0����ջ����һ��������ģ�
                   ֻ�е��û�������sk_sort��������ֵ��Ϊ1��
        comp:      ��ջ�ڴ�����ݵıȽϺ�����ַ���˺�����������Ͳ��Ҳ�����
                   ���û�����һ���¶�ջʱ������ָ��compΪ�û�ʵ�ֵ�һ���ȽϺ�����
                   �򵱶�ջ�Ѿ�����ʱͨ������sk_set_cmp_func����������ָ���ȽϺ�����
        ע�⣬
            �û�����Ҫ���õײ�Ķ�ջ����(sk_sort��sk_set_cmp_func��)��
            ���ǵ�����ͨ����ʵ�ֵĸ���������
    �������������֣�
        openssl��ջʵ��Դ��λ��crypto/stackĿ¼��
        1) sk_set_cmp_func
            �˺����������ö�ջ������ݵıȽϺ��������ڶ�ջ��֪���û���ŵ���ʲô���ݣ�
            ���ԣ��ȽϺ����������û��Լ�ʵ�֡�
        2) sk_find
            �������ݵ�ַ���������ڶ�ջ�е�λ�á�����ջ�����˱ȽϺ���ʱ�������ȶԶ�ջ��������
            Ȼ��ͨ�����ַ����в��ҡ������ջû�����ñȽϺ�������ֻ�Ǽ򵥵ıȽ����ݵ�ַ������.
        3��sk_sort
            �������Զ�ջ�������������ȸ���sorted���ж��Ƿ��Ѿ�����
            ���δ����������˱�׼C����qsort���п�������
        4��sk_pop_free
            �����������ͷŶ�ջ�ڴ�ŵ������Լ���ջ��������Ҫһ�����û�ָ������Ծ������ݵ��ͷź�����
            ����û�������sk_free��������ֻ���ͷŶ�ջ�������õ��ڴ棬�������ͷ������ڴ档
            
������ ��ϣ��
    ���ݽṹ
        ��Դ����crypto/lhashĿ¼�£����ݽṹ��lhash.h�ж������£�
        typedef struct lhash_node_st
        {
            void *data;
            struct lhash_node_st *next;
            #ifndef OPENSSL_NO_HASH_COMP
            unsigned long hash;
            #endif
        } LHASH_NODE;
        ���ṹ��һ�����������У�data���ڴ�����ݵ�ַ��nextΪ��һ�����ݵ�ַ��hashΪ���ݹ�ϣ����ֵ��
        typedef struct lhash_st
        {
            LHASH_NODE **b;  //ͷָ������飬ÿ��ͷָ��ָ��һ�����������Ԫ�ط�������Ľṹ
            LHASH_COMP_FN_TYPE comp;    //comp���ڴ�����ݱȽϺ�����ַ
            LHASH_HASH_FN_TYPE hash;    //hash���ڴ�ż����ϣֵ�����ĵ�ַ
            unsigned int num_nodes;     //num_nodesΪ�������
            unsigned int num_alloc_nodes;   //num_alloc_nodesΪb����ռ�Ĵ�С
            unsigned int p;
            unsigned int pmax;
            unsigned long up_load; /* load times 256 */
            unsigned long down_load; /* load times 256 */
            unsigned long num_items;
            unsigned long num_expands;
            unsigned long num_expand_reallocs;
            unsigned long num_contracts;
            unsigned long num_contract_reallocs;
            unsigned long num_hash_calls;
            unsigned long num_comp_calls;
            unsigned long num_insert;
            unsigned long num_replace;
            unsigned long num_delete;
            unsigned long num_no_delete;
            unsigned long num_retrieve;
            unsigned long num_retrieve_miss;
            unsigned long num_hash_comps;
            int error;
        } LHASH;
    ����˵��
        1)  LHASH *lh_new(LHASH_HASH_FN_TYPE h, LHASH_COMP_FN_TYPE c)
            ���ܣ����ɹ�ϣ��
            Դ�ļ���lhash.c
            ˵���� �������hΪ��ϣ������cΪ�ȽϺ������������������ǻص�������
                   ��Ϊ��ϣ�����ڴ����������ݽṹ����ϣ���š���ѯ��ɾ���Ȳ�������Ҫ�Ƚ����ݺͽ��й�ϣ���㣬
                   ����ϣ��֪���û�������ν��бȽϣ�Ҳ��֪���û����ݽṹ����Ҫ����Щ�ؼ������ɢ�����㡣
                   ���ԣ��û������ṩ�������ص�������
        2)  void *lh_delete(LHASH *lh, const void *data)
            Դ�ļ���lhash.c
            ���ܣ�ɾ��ɢ�б��е�һ������
            ˵����dataΪ���ݽṹָ�롣
        3)  void lh_doall(LHASH *lh, LHASH_DOALL_FN_TYPE func)
            Դ�ļ���lhash.c
            ���ܣ������ϣ���е���������
            ˵����funcΪ�ⲿ�ṩ�Ļص��������������������д洢�ڹ�ϣ���е����ݣ�ÿ�����ݱ�func����
        4)  void lh_doall_arg(LHASH *lh, LHASH_DOALL_ARG_FN_TYPE func, void *arg)
            Դ�ļ���lhash.c
            ���ܣ������ϣ������������
            ˵�����˲���������lh_doall ������funcΪ�ⲿ�ṩ�Ļص�������argΪ���ݸ�func�����Ĳ�����
                  �������������д洢�ڹ�ϣ���е����ݣ�ÿ�����ݱ�func����
        5)  void lh_free(LHASH *lh)
            Դ�ļ���lhash.c
            ���ܣ��ͷŹ�ϣ��
        6�� void *lh_insert(LHASH *lh, void *data)
            Դ�ļ���lhash.c
            ���ܣ�����ϣ����������ݡ�
            ˵����dataΪ��Ҫ������ݽṹ��ָ���ַ��
        7�� void *lh_retrieve(LHASH *lh, const void *data)
            Դ�ļ���lhash.c
            ���ܣ���ѯ���ݡ�
            ˵�����ӹ�ϣ���в�ѯ���ݣ�dataΪ���ݽṹ��ַ�������ݽṹ�б����ṩ�ؼ���
                  (��Щ�ؼ����Ӧ���û��ṩ�Ĺ�ϣ�����ͱȽϺ���)�Թ���ѯ��
                  �����ѯ�ɹ����������ݽṹ�ĵ�ַ�����򷵻�NULL��
                  ����SSL�����з���˲�ѯ��ǰ�洢��SESSIONʱ������Ҫ�ṩ���йؼ��ļ��
                  SSL_SESSION *ret=NULL,data;
                  data.ssl_version=s->version;
                  data.session_id_length=len;
                  memcpy(data.session_id,session_id,len);
                 ret=(SSL_SESSION *)lh_retrieve(s->ctx->sessions,&data);
        8�� void lh_node_stats_bio(const LHASH *lh, BIO *out)
            Դ�ļ���lh_stats.c
            ���ܣ�����ϣ����ÿ�������µ�����״̬�����BIO�С�
        9��  void lh_node_stats(const LHASH *lh, FILE *fp)
            Դ�ļ���lh_stats.c
            ���ܣ�����ϣ����ÿ�����������ݵ����������FILE�С�
            ˵�����˺���������lh_node_stats_bio������
        10��void lh_node_usage_stats_bio(const LHASH *lh, BIO *out)
            Դ�ļ���lh_stats.c
            ���ܣ�����ϣ���ʹ��״̬�����BIO�С�
        11��void lh_node_usage_stats(const LHASH *lh, FILE *fp)
            Դ�ļ���lh_stats.c
            ���ܣ�����ϣ���ʹ��״̬�����FILE��
            ˵�����˺���������lh_node_usage_stats_bio����
        12��unsigned long lh_num_items(const LHASH *lh)
            Դ�ļ���lhash.c
            ���ܣ���ȡ��ϣ����Ԫ�صĸ�����
        13��void lh_stats_bio(const LHASH *lh, BIO *out)
            Դ�ļ���lh_stats.c
            ���ܣ������ϣ��ͳ����Ϣ��BIO��
        14��void lh_stats(const LHASH *lh, FILE *fp)
            Դ�ļ���lh_stats.c
            ���ܣ���ӡ��ϣ���ͳ����Ϣ���˺���������lh_stats_bio��
        15��unsigned long lh_strhash(const char *c)
            Դ�ļ���lhash.c
            ���ܣ������ı��ַ�������ϣֵ
            
������ �ڴ����
    ���
        openssl�ṩ�����õ��ڴ����/�ͷź�����
        ����û���ȫ����openssl���ڴ������ͷź��������Է�����ҵ��ڴ�й¶�㡣
        openssl�����ڴ�ʱ�������ڲ�ά��һ���ڴ�����ϣ�����ڴ���Ѿ����䵫δ�ͷŵ��ڴ���Ϣ��
        ���û������ڴ����ʱ���ڹ�ϣ������Ӵ�����Ϣ���ڴ��ͷ�ʱɾ������Ϣ��
        ���û�ͨ��openssl���������ڴ�й¶��ʱ��ֻ���ѯ�ù�ϣ���ɡ�
        �û�ͨ��openssl�ص��������ܴ�����Щй¶���ڴ档
        openssl���û����õ��ڴ����Ⱥ�����Ҫ��crypto/mem.c��ʵ��
        �����õķ��亯����crypto/mem_dbg.c��ʵ�֡�
        Ĭ�������mem.c�еĺ�������mem_dbg.c�е�ʵ�֡�
        ����û�ʵ�����Լ����ڴ���亯���Լ������ڴ�й¶�ĺ�����
        ����ͨ������CRYPTO_set_mem_functions������CRYPTO_set_mem_debug_functions���������á�
    �ڴ����ݽṹ
        ������crypto/mem_dbg.c��
        typedef struct app_mem_info_st
        {     
            unsigned long thread;
            const char *file;
            int line;
            const char *info;
            struct app_mem_info_st *next; /* tail of thread��s stack */
            int references;
        } APP_INFO;
        typedef struct mem_st
        {
            void *addr;
            int num;
            const char *file;
            int line;
            unsigned long thread;
            unsigned long order;
            time_t time;
            APP_INFO *app_info;
        } MEM;
        �������壺
            addr�������ڴ�ĵ�ַ��
            num�������ڴ�Ĵ�С��
            file�������ڴ���ļ���
            line�������ڴ���кš�
            thread�������ڴ���߳�ID��
            order���ڼ����ڴ���䡣
            time���ڴ����ʱ�䡣
            app_info:���ڴ���û�Ӧ����Ϣ��Ϊһ���������������ļ����к��Լ��߳�ID����Ϣ��
            references�������ô�����
    ��Ҫ����
        1) CRYPTO_mem_ctrl
            ��������Ҫ���ڿ����ڴ����ʱ���Ƿ��¼�ڴ���Ϣ��
            �������¼�ڴ���Ϣ�������ܲ����ڴ�й¶��
            �����ڴ��¼����CRYPTO_mem_ctrl(CRYPTO_MEM_CHECK_ON)��
            �ر��ڴ��¼����CRYPTO_mem_ctrl(CRYPTO_MEM_CHECK_OFF)��
            һ��CRYPTO_mem_ctrl(CRYPTO_MEM_CHECK_ON)�����ã�
            ֱ���û�����CRYPTO_mem_ctrl(CRYPTO_MEM_CHECK_OFF)ǰ��
            �û����е�opessl�ڴ���䶼�ᱻ��¼��
        2) CRYPTO_is_mem_check_on
            ��ѯ�ڴ��¼����Ƿ�����
        3��CRYPTO_dbg_malloc
            ���������ڷ����ڴ�ռ䣬����ڴ��¼��ǿ��������¼�û�������ڴ档
            ����Ҫ��¼�ڴ���Ϣʱ���ú�������Ҳ��Ҫ�����ڴ�����ϣ��
            Ϊ�˷�ֹ�ݹ���������������ڴ��¼��Ϣǰ������ʱ�ر��ڴ��¼��ǣ���������ٷſ���
        4��CRYPTO_dbg_free
            �ͷ��ڴ棬����ڴ��¼��ǿ���������Ҫɾ����ϣ���ж�Ӧ�ļ�¼��
        5��CRYPTO_mem_leaks
            ���ڴ�й¶�����BIO�С�
        6��CRYPTO_mem_leaks_fp
            ���ڴ�й¶�����FILE��(�ļ����߱�׼���)���ú���������CRYPTO_mem_leaks��
        7��CRYPTO_mem_leaks_cb
            �����ڴ�й¶���������Ϊ�û��Լ�ʵ�ֵĴ����ڴ�й¶�ĺ�����ַ��
            �ú���ֻ��Ҫ����һ���ڴ�й¶��opensslͨ��lh_doall_arg�����û��������������м�¼(й¶���ڴ�)��
            
������ ����IO
    ���
        openssl����io���͵ĳ����װ��������
        �ڴ桢�ļ�����־����׼���������socket��TCP/UDP������/���ܡ�ժҪ��sslͨ����
        BIOͨ���ص�����Ϊ�û������˵ײ�ʵ��ϸ��
        Bio�е������ܴ�һ��BIO���͵�����һ��BIO������Ӧ�ó���
    ���ݽṹ��
        ��crypto/bio.h�ж�������
        1��BIO_METHOD
            typedef struct bio_method_st
            {
                 int type;
                 const char *name;
                 int (*bwrite)(BIO *, const char *, int);
                 int (*bread)(BIO *, char *, int);
                 int (*bputs)(BIO *, const char *);
                 int (*bgets)(BIO *, char *, int);
                 long (*ctrl)(BIO *, int, long, void *);
                 int (*create)(BIO *);
                 int (*destroy)(BIO *);
                long (*callback_ctrl)(BIO *, int, bio_info_cb *);
            } BIO_METHOD;
            �ýṹ������IO�����ĸ��ֻص�������
            ������Ҫ�������bio���ͱ���ʵ�����е�һ�ֻ���ֻص�������
            �����������£�
                type��   ����BIO���ͣ�
                name��   ����BIO�����֣�
                bwrite�� ����BIOд�����ص�������
                bread��  ����BIO�������ص�������
                bputs��  ����BIO��д���ַ����ص�������
                bgets��  ����BIO�ж�ȡ�ַ���������
                ctrl��   ����BIO�Ŀ��ƻص�������
                create�� ���ɾ���BIO�ص�������
                destroy�����پ���BIO�ص�������
                callback_ctrl������BIO���ƻص���������ctrl�ص�������һ����
                               �ú������ɵ����ߣ�������ʵ���ߣ���ʵ�֣�
                               Ȼ��ͨ��BIO_set_callback�Ⱥ��������á�
        2��BIO
            truct bio_st
            {
                BIO_METHOD *method;
                /* bio, mode, argp, argi, argl, ret */
                long (*callback)(struct bio_st *,int,const char *,int, long,long);
                char *cb_arg; /* first argument for the callback */
                int init;
                int shutdown;
                int flags;  /* extra storage */
                int retry_reason;
                int num;
                void *ptr;
                struct bio_st *next_bio;  /* used by filter BIOs */
                struct bio_st *prev_bio;/* used by filter BIOs */
                int references;
                nsigned long num_read;
                unsigned long num_write;
                CRYPTO_EX_DATA ex_data;
            }��
            ��Ҫ��壺
                init��
                    ��������ʼ����ǣ���ʼ����Ϊ1��
                    �����ļ�BIO�У�ͨ��BIO_set_fp����һ���ļ�ָ��ʱ���ñ������1��
                    socket BIO�У�ͨ��BIO_set_fd����һ������ʱ�����øñ��Ϊ1��
                shutdown��
                    BIO�رձ�ǣ�����ֵ��Ϊ0ʱ���ͷ���Դ����ֵ����ͨ�����ƺ��������á�
                flags��
                    ��ЩBIOʵ����Ҫ�������Ƹ�����������Ϊ��
                    �����ļ�BIOĬ�ϸ�ֵΪBIO_FLAGS_UPLINK��
                    ��ʱ�ļ�����������UP_fread���������ǵ���fread������
                retry_reason��
                    ����ԭ����Ҫ����socket��ssl BIO ���첽������
                    ����socket bio�У�����WSAEWOULDBLOCK����ʱ��openssl�����û��Ĳ�����Ҫ���ԡ�
                num��
                    ��ֵ�����BIO���죬����socket BIO��num������������֡�
                ptr��
                    ָ�룬����bio�в�ͬ���塣
                    �����ļ�BIO������������ļ������
                    mem bio������������ڴ��ַ��
                    connect bio�����������BIO_CONNECT���ݣ�
                    accept bio�����������BIO_ACCEPT���ݡ�
                next_bio��
                    ��һ��BIO��ַ��BIO���ݿ��Դ�һ��BIO���͵���һ��BIO��
                    ��ֵָ������һ��BIO�ĵ�ַ��
                references��
                    ������������
                num_read��
                    BIO���Ѷ�ȡ���ֽ�����
                num_write��
                    BIO����д����ֽ�����
                ex_data��
                    ���ڴ�Ŷ������ݡ�
    ��غ���
        BIO��������������crypto/bio.h�С����еĺ�������BIO_METHOD�еĻص�������ʵ�֡�
        ������Ҫ��Ϊ���ࣺ
            1������BIO��غ���
               ���磺BIO_new_file���������ļ�����BIO_get_fd�������������ӣ��ȡ�
            2��ͨ�ó�����
               ����BIO_read��BIO_write�ȡ�
        ���⣬�кܶຯ�����ɺ궨��ͨ�����ƺ���BIO_ctrlʵ�֣�
        ����BIO_set_nbio��BIO_get_fd��BIO_eof�ȵȡ�
    ʾ��
        �ӽ���
            const BIO_METHOD* bm1 = BIO_f_cipher();
            BIO *bc=BIO_new(bm1);
            const EVP_CIPHER*c=EVP_des_ecb();
            unsigned char key[8],iv[8];
            for(int i=0;i<8;i++)
            {
                iv[i]=key[i]=i+1;
            }
            BIO_set_cipher(bc,c,key,iv,1);
            const BIO_METHOD* bm2 = BIO_s_null();
            BIO *b= BIO_new(bm2);
            b = BIO_push(bc,b);
            int len = BIO_write(b,"openssl",7);
            char tmp[100];
            len = BIO_read(b,tmp,1024);
            BIO_free(b);
            //===========����==============
            c = EVP_des_ecb();
            bm1 = BIO_f_cipher();
            BIO* bdec=BIO_new(bm1);
            BIO_set_cipher(bdec,c,key,iv,0);
            b = BIO_new(bm2);
            b = BIO_push(bdec,b);
            len = BIO_write(b,tmp,len);
            len = BIO_read(b,tmp,100);
            BIO_free(b);
        SSL
            
�ھ��� �����
    ����
        openssl�����������Դ��λ��crypto/randĿ¼��
        rand.h����������������������صĺ���
        opensslͨ��ʹ��ժҪ�㷨����������������õ�ժҪ�㷨�У�sha1��md5��mdc2��md2��
        �����������ժҪ�㷨��crypto/rand_lcl.h���ɺ������ơ�
        Opensslά��һ���ڲ����״̬����(md_rand.c�ж����ȫ�ֱ���state��md)��
        ͨ������Щ�ڲ����ݼ���ժҪ�����������
    ���ݽṹ
        Openssl�������ص����ݽṹ���£�������rand.h�У�
        struct rand_meth_st
        {
            void (*seed)(const void *buf, int num);
            int (*bytes)(unsigned char *buf, int num);
            void (*cleanup)(void);
            void (*add)(const void *buf, int num, double entropy);
            int (*pseudorand)(unsigned char *buf, int num);
            int (*status)(void);
        };    
        ���ṹ��Ҫ�����˸��ֻص�����������û���Ҫʵ���Լ�����������ɺ���������Ҫʵ�ֱ��ṹ�еĸ���������
        Openssl������һ��Ĭ�ϵĻ���ժҪ��rand_methʵ��(crypto/md_rand.c)��
        �����������£�
            seed�����Ӻ�����Ϊ����openssl�ڲ�ά����������ݸ������򣬿�ʹ�ñ�������
                bufΪ�û�������������ַ��numΪ���ֽ�����
                Openssl���û��ṩ��buf�е�������������ڲ�������ݽ���ժҪ���㣬�������ڲ�������ݡ�
                �������������
            bytes�������������openssl�����ڲ�ά���������״̬�����ɽ����
                buf���ڴ�����ɵ��������numΪ�������������ָ��������������ֽڳ��ȣ�
            cleanup��������������������ڲ�ά����������������
            add����seed���ƣ�Ҳ��Ϊ����openssl�ڲ�������ݸ�������
                ����entropy(��Ϣ��)���Կ����û����μ����������ĸ�����
                OpensslĬ�ϵ��������Ϊ32�ֽڣ���rand_lcl.h����ENTROPY_NEEDED���塣
                Openssl���������֮ǰ���û��ṩ�����е����������֮�ͱ���ﵽ32�ֽڡ�
                ��opensslʵ�ֵ�md_rand�У���ʹ�û����������Ӻ�����ֱ�������������
                opensslҲ�����RAND_poll��������ɸò�����
            pseudorand����������bytes����Ҳ���������������
            status���鿴��ֵ�Ƿ�ﵽԤ��ֵ��openssl��Ϊ32�ֽڣ�����ﵽ�򷵻�1�����򷵻�0��
                ��opensslʵ�ֵ�md_rand�иú��������RAND_poll������ʹ��ֵ�ϸ� 
                �������������0����˵����ʱ�û���Ӧ�������������Ҫ����seed��add�����������ֵ��
    ��Ҫ����
        1)  int RAND_load_file(const char *file, long bytes)
            ��������fileָ����������ļ��е����ݶ�ȡbytes�ֽ�(���bytes����1024�����ȡ1024�ֽ�)��
            ����RAND_add���м��㣬�����ڲ��������
        2)  RAND_write_file
            д��������ļ������ļ����ñ�֮���RAND_load_file���������PRNG�ĳ�ʼ����
        3)  const char *RAND_file_name(char *file,size_t num)
            ��ȡ������ļ��������������ļ�����С��num�򷵻ؿգ����򷵻��ļ�����
        4)  RAND_poll
            ���ڼ����ڲ������������ƽ̨�и��Ե�ʵ�֡�
        5)  RAND_screen/RAND_event
            Windows���к��������������ڲ�����������ǵ�����RAND_seed��
        6)  RAND_seed/RAND_add
            ���������ڲ��������
        7)  RAND_bytes/RAND_pseudo_bytes
            ���������������
        8)  RAND_cleanup
            ����ڲ��������
        9)  RAND_set_rand_method
            ��������rand_meth�����û�ʵ�����Լ�����������ɺ���ʱ(ʵ��rand_meth�еĻص�����)��
            ���ø÷������滻openssl ���ṩ����������ܡ�
        10) RAND_status
            �����鿴�ڲ��������ֵ�Ƿ��ѴﵽԤ��ֵ�����δ�ﵽ����Ӧ�������������
        11) RAND_bytes
            ����ָ������������ֽڣ�ʹ��һ�����밲ȫα����������洢��buf������
        
��ʮһ�� ����
    ���ݽṹ
        crypto/bn.h�ж����˴����ı�ʾ��ʽ�����£�
        struct bignum_st
        {
            BN_ULONG *d;
            int top;    
            int dmax;
            int neg;
            int flags;
        };
        �����������£�
        d��    BN_ULONG(��ϵͳ���죬win32��Ϊ4���ֽ�)������ָ���׵�ַ�������ʹ���������棬�����ǵ��ŵġ�
               ���磬�û�Ҫ��ŵĴ���Ϊ12345678000��ͨ��BN_bin2bn���룩��
               ��d���������£�0x30 0x30 0x30 0x38 0x37 0x36 0x35 0x34 0x33 0x32 0x31��
        top��  ����ָ������ռ���ٸ�BN_ULONG�ռ䣬������topΪ3��
        dmax�� d����Ĵ�С��
        neg��  �Ƿ�Ϊ���������Ϊ1�����Ǹ�����Ϊ0����Ϊ������
        flags�����ڴ��һЩ��ǣ�����flags����BN_FLG_STATIC_DATAʱ������d���ڴ��Ǿ�̬����ģ�
               ����BN_FLG_MALLOCEDʱ��d���ڴ��Ƕ�̬����ġ�
    ����
        1�� BN_rand/BN_pseudo_rand
            ����һ������Ĵ�����
        2�� BN_rand_range/BN_pseudo_rand_range
            ��������������Ǹ�����������ķ�Χ��
        3�� BN_dup
            �������ơ�
        4)  BN_generate_prime
            ����������
        5)  int BN_add_word(BIGNUM *a, BN_ULONG w)
            ������a����w������ɹ�������1��
        6)  BIGNUM *BN_bin2bn(const unsigned char *s, int len, BIGNUM *ret)
            ���ڴ��е�����ת��Ϊ������Ϊ�ڴ��ַ��lenΪ���ݳ��ȣ�retΪ����ֵ��
        7)  int BN_bn2bin(const BIGNUM *a, unsigned char *to)
            ������ת��Ϊ�ڴ���ʽ���������Ϊ����a��toΪ�����������ַ����������ҪԤ�ȷ��䣬����ֵΪ�������ĳ��ȡ�
        8)  char *BN_bn2dec(const BIGNUM *a) 
            ������ת���������ַ���������ֵ�д�������ַ����������ڲ�����ռ䣬�û��������ⲿ��OPENSSL_free�����ͷŸÿռ䡣
        9��char *BN_bn2hex(const BIGNUM *a)
            ������ת��Ϊʮ�������ַ���������ֵΪ���ɵ�ʮ�������ַ������ⲿ��Ҫ��OPENSSL_free�����ͷ�
        10) BN_cmp
            �Ƚ�����������
        11��BIGNUM *BN_mod_inverse(BIGNUM *in,  const BIGNUM *a, const BIGNUM *n, BN_CTX *ctx)
            ����ax=1(mod n)��          
        12��BN_zero()��BN_one()��BN_set_word() 
            ����ֵΪ0��1����ָ��ֵ
            
��ʮ���� BASE64�����
    ��Ҫ����
        1��  ���뺯��
        EVP_EncodeInit         ����ǰ��ʼ�������ġ�
        EVP_EncodeUpdate       ����BASE64���룬�������ɶ�ε��á�
        EVP_EncodeFinal        ����BASE64���룬����������
        EVP_EncodeBlock        ����BASE64���롣
        2��  ���뺯��
        EVP_DecodeInit         ����ǰ��ʼ�������ġ�
        EVP_DecodeUpdate       BASE64���룬�������ɶ�ε��á�
        EVP_DecodeFinal        BASE64���룬����������
        EVP_DecodeBlock        BASE64���룬�ɵ������á�
    
��ʮ���� asn1
    ASN.1(Abstract Syntax Notation One��X.208)����һ�����ı�����ԣ�������������������ͣ�
    ��integer��bit string һ��ļ����ͣ����ṹ�����ͣ���set ��sequence��
    ���ҿ���ʹ����Щ���͹����������͡�
    DER������ANS.1����Ľ������������ݱ���ɰ�λ��ֵ�ı������
    �������˶�ANS.1ֵ����������ͺ�ֵ����Ψһ�������
    1) ������
        BIT STRING          ����0��1λ����
        IA5String           ����IA5(ASCII)�ַ�����
        INTEGER             ����һ��������
        NULL                ��ֵ��
        OBJECT IDENTIFIER   һ�������ʶ�ţ�һ������������ʶ�㷨���������͵ȶ���
        OCTET STRING        8λ����
        PrintableString     ����ɴ�ӡ�ַ�����
        T61String           ����T.61��8λ���ַ�����
        UTCTime             һ����Эͬ����ʱ���򡰸������α�׼ʱ��G.M.T������
    2) �ṹ����
        �ṹ�����������ɣ�ANS.1���������ֽṹ���ͣ�
        SEQUENCE            һ���������͵��������У�
        SEQUENCE OF         һ���������͵�0�������������У�
        SET                 һ���������͵����򼯺ϣ�
        SET OF              һ���������͵�0���������򼯺ϡ�
    3) ���������
        ��һ��Ӧ���ڲ��������͵���Ч������ʹ�ñ�ǣ�
        ���Ҳͬ����������һ���ṹ�����ڲ���ͬ�������
        ����SET��SEQUENCE���Ϳ�ѡ��ͨ��ʹ�������ı���Ա��������
        �����ֱ�����͵ķ�������ʽ����ʽ��
        ��ʽ��������ǽ��������͵ı�Ǹı䣬�õ��µ����͡�
        ��ʽ��ǵĹؼ�����IMPLICIT��
        ��ʽ��������ǽ��������ͼ���һ���ⲿ��ǣ��õ��µ����͡�
        ��ʽ��ǵĹؼ�����EXPLICIT��
        Ϊ�˽��б��룬��ʽ������ͳ��˱�ǲ�ͬ���⣬������Ϊ�������������ͬ��
        ��ʽ������Ϳ�����Ϊֻ��һ������Ľṹ���͡�
    4) ��������
        ���ͺ�ֵ�÷���::=��ʾ��������ߵ������֣��ұ������ͺ�ֵ��
        �����ֿ������ڶ������������ͺ�ֵ��
        ����CHOICE���͡�ANY�������⣬����ANS.1���Ͷ���һ����ǣ�
        �����һ�����һ���Ǹ��ı������ɣ�
        ���ҽ����������ͬʱ��ANS.1��������ͬ�ġ�
        Ҳ����˵��Ӱ�����������Ĳ���ANS.1���͵����֣��������ǡ�
        ͨ�ñ����X.208�ж��壬��������Ӧ��ͨ�ñ���롣
        �����ı�����ͷֱ��ںܶ�ط����壬����ͨ����ʽ����ʽ��ǻ�á�
    �±��г���һЩͨ�����ͼ����ǣ�
        ����                        ����루ʮ�����ƣ�
        INTEGER                             02
        BIT STRING                          03
        OCTET STRING                        04
        NULL                                05
        OBJECT IDENTIFIER                   06
        SEQUENCE and SEQUENCEOF             10
        SET and SET OF                      11
        PrintableString                     13
        T61String                           14
        IA5String                           16
        UTCTime                             17
    ������Openssl��ASN.1�����һ��asn.1����Ľṹ��ʱ����Ҫ�������²��裺
        1) �� ASN.1�﷨�����ڲ����ݽṹ��������������
            ��ν�ڲ����ݽṹ��ָ����Openssl���û������������ͣ�
            ����ASN.1�﷨��������������ݽṹ���������ݽṹ���Է�������ڱ���롣
            ��x509v4�е�֤����Ч��Ϊ����֤����Ч�ڶ������£�
            AttCertValidityPeriod  ::= SEQUENCE 
            {
                notBeforeTime  GeneralizedTime,
                notAfterTime   GeneralizedTime
            }
            
            �������ǿ��Զ�����Ӧ���ڲ����ݽṹ�����£�
            typedef    struct      X509V4_VALID_st
            {
                ASN1_GENERALIZEDTIME *notBefore;
                ASN1_GENERALIZEDTIME *notAfter;
            }X509V4_VALID;
            DECLARE_ASN1_FUNCTIONS(X509V4_VALID)
            
            �������һ�����ڶ����ĸ�������
            X509V4_VALID  *X509V4_VALID_new(void);
            void          *X509V4_VALID_free(X509V4_VALID *a);
            X509V4_VALID  *d2i_ASN1_INTEGER(X509V4_VALID **a,unsigned char **in,long len);
            int           i2d_ X509V4_VALID (X509V4_VALID *a,unsigned char **out);
        2) ʵ���ڲ����ݽṹ���ĸ���������
            ʵ���ڲ����ݽṹ�Ļ�����������ͨ��һϵ�еĺ���ʵ�ֵġ�
            �����ģʽ���£�������֤����Ч��Ϊ�������£�
            /* X509V4_VALID */
            ASN1_SEQUENCE(X509V4_VALID) = 
            {
                ASN1_SIMPLE(X509V4_VALID, notBefore, ASN1_GENERALIZEDTIME),
                ASN1_SIMPLE(X509V4_VALID, notAfter, ASN1_GENERALIZEDTIME)
            } ASN1_SEQUENCE_END(X509V4_VALID)
            IMPLEMENT_ASN1_FUNCTIONS(X509V4_VALID)
            ����ͨ�����ʵ����һ��asn.1����ṹ����������ĸ�������
    Openssl��ASN.1��
        1)   DECLARE_ASN1_FUNCTIONS
             ��������һ���ڲ����ݽṹ���ĸ�����������һ�������ͷ�ļ��ж��塣
        2)   IMPLEMENT_ASN1_FUNCTIONS
             ����ʵ��һ�����ݽṹ���ĸ�����������
        3��  ASN1_SEQUENCE
             ����SEQUENCE����������ı�����һ��SEQUENCE��
        4)   ASN1_CHOICE
             ��������ı�����ѡ������һ�ΪCHOICE���͡�
        5��  ASN1_SIMPLE
             ���ڼ����ͻ�ṹ���ͣ������Ǳ����
        6)   ASN1_EXP
             ������ʾ��ǣ�����asn.1�﷨�У���������ʾ��ǡ�
        7)   ASN1_IMP
             ������ʾ��ǣ�����asn.1�﷨�У���������ʾ���͡�
        8)   ASN1_OPT
             ���ڿ�ѡ�����asn.1�﷨�У������ǿ�ѡ�ġ�
        9)   ASN1_EXP_OPT
             ������ʾ��ǣ�����asn.1�﷨�У���������ʾ���ͣ������ǿ�ѡ�ģ�
        10)  ASN1_IMP_OPT
             ������ʾ��ǣ�����asn.1�﷨�У���������ʾ���ͣ������ǿ�ѡ�ġ�
        11�� ASN1_IMP_SEQUENCE_OF_OPT
             ������ʾ��ǣ�����asn.1�﷨�У�������һ��SEQUENCE���У�Ϊ��ʾ���ͣ������ǿ�ѡ�ġ�
        12)  ASN1_SEQUENCE_END
             ����SEQUENCE������
        13)  ASN1_CHOICE_END
             ���ڽ���CHOICE���͡�
    opensslԴ��̽��
        '''
        ' This is the ASN1 template structure that defines a wrapper round the
        ' actual type. It determines the actual position of the field in the value
        ' structure, various flags such as OPTIONAL and the field name.
        '''
        struct ASN1_TEMPLATE_st {
            unsigned long flags;        # Various flags 
            long tag;                   # tag, not used if no tagging 
            unsigned long offset;       # Offset of this field in structure 
            'ifndef NO_ASN1_FIELD_NAMES
            const char *field_name;     # Field name 
            'endif
            ASN1_ITEM_EXP *item;        # Relevant ASN1_ITEM or ASN1_ADB 
        };
        typedef const ASN1_ITEM *ASN1_ITEM_EXP (void);
        ''' This is the actual ASN1 item itself '''
        struct ASN1_ITEM_st {
            char itype;                 # The item type, primitive, SEQUENCE, CHOICE or extern 
            long utype;                 # underlying type 
            const ASN1_TEMPLATE *templates; # If SEQUENCE or CHOICE this contains the contents 
            long tcount;                # Number of templates if SEQUENCE or CHOICE 
            const void *funcs;          # functions that handle this type 
            long size;                  # Structure size (usually) 
            'ifndef NO_ASN1_FIELD_NAMES
            const char *sname;          # Structure name 
            'endif
        };
        
        define ASN1_SIMPLE(stname, field, type)               ASN1_EX_TYPE(flags=0,tag=0, stname, field, type)
        define ASN1_OPT(stname, field, type)                  ASN1_EX_TYPE(ASN1_TFLG_OPTIONAL, tag=0, stname, field, type)
        define ASN1_IMP(stname, field, type, tag)             ASN1_EX_TYPE(ASN1_TFLG_IMPLICIT, tag, stname, field, type)
        define ASN1_IMP_OPT(stname, field, type, tag)         ASN1_EX_TYPE(ASN1_TFLG_IMPLICIT | ASN1_TFLG_OPTIONAL, tag, stname, field, type)
        define ASN1_SEQUENCE_OF(stname, field, type)          ASN1_EX_TYPE(ASN1_TFLG_SEQUENCE_OF, tag=0, stname, field, type)    
        define ASN1_EX_TYPE(flags, tag, stname, field, type)  { (flags), (tag), offsetof(stname, field), '#field', ASN1_ITEM_ref(type) }  
                                           
        template flags (ASN1_TFLG_xxx)
            ''' Field is optional '''
            define ASN1_TFLG_OPTIONAL      (0x1) = 1
            ''' Field is a SET OF '''
            define ASN1_TFLG_SET_OF        (0x1 << 1) = 2
            ''' Field is a SEQUENCE OF '''
            define ASN1_TFLG_SEQUENCE_OF   (0x2 << 1) = 4
            '''
            ' Special case: this refers to a SET OF that will be sorted into DER order
            ' when encoded *and* the corresponding STACK will be modified to match the
            ' new order.
            '''
            define ASN1_TFLG_SET_ORDER     (0x3 << 1) = 6
            ''' Mask for SET OF or SEQUENCE OF '''
            define ASN1_TFLG_SK_MASK       (0x3 << 1) = 6
            '''
            ' These flags mean the tag should be taken from the tag field. If EXPLICIT
            ' then the underlying type is used for the inner tag.
            '''
            ''' IMPLICIT tagging '''
            define ASN1_TFLG_IMPTAG        (0x1 << 3) = 8
            ''' EXPLICIT tagging, inner tag from underlying type '''
            define ASN1_TFLG_EXPTAG        (0x2 << 3) = 16
            define ASN1_TFLG_TAG_MASK      (0x3 << 3) = 24
            ''' context specific IMPLICIT '''
            define ASN1_TFLG_IMPLICIT      ASN1_TFLG_IMPTAG|ASN1_TFLG_CONTEXT = 136
            ''' context specific EXPLICIT '''
            define ASN1_TFLG_EXPLICIT      ASN1_TFLG_EXPTAG|ASN1_TFLG_CONTEXT = 144
            '''
            ' If tagging is in force these determine the type of tag to use. Otherwise
            ' the tag is determined by the underlying type. These values reflect the
            ' actual octet format.
            '''
            ''' Universal tag '''
            define ASN1_TFLG_UNIVERSAL     (0x0<<6) = 0
            ''' Application tag '''
            define ASN1_TFLG_APPLICATION   (0x1<<6) = 64
            ''' Context specific tag '''
            define ASN1_TFLG_CONTEXT       (0x2<<6) = 128
            ''' Private tag '''
            define ASN1_TFLG_PRIVATE       (0x3<<6) = 192
            define ASN1_TFLG_TAG_CLASS     (0x3<<6) = 192
            '''
            ' These are for ANY DEFINED BY type. In this case the 'item' field points to
            ' an ASN1_ADB structure which contains a table of values to decode the
            ' relevant type
            '''
            define ASN1_TFLG_ADB_MASK      (0x3<<8) = 768
            define ASN1_TFLG_ADB_OID       (0x1<<8) = 256
            define ASN1_TFLG_ADB_INT       (0x1<<9) = 512
            '''
            ' This flag means a parent structure is passed instead of the field: this is
            ' useful is a SEQUENCE is being combined with a CHOICE for example. Since
            ' this means the structure and item name will differ we need to use the
            ' ASN1_CHOICE_END_name() macro for example.
            '''
            define ASN1_TFLG_COMBINE       (0x1<<10) = 1024
            '''
            ' This flag when present in a SEQUENCE OF, SET OF or EXPLICIT causes
            ' indefinite length constructed encoding to be used if required.
            '''
            define ASN1_TFLG_NDEF          (0x1<<11) = 2048
 
��ʮ���� ������
    ���ݽṹ
        openssl�У�ͨ��unsigned long��������Ŵ�����Ϣ��
        ���������������ݣ�����롢���������Լ�����ԭ����롣
        ���У��������crypto/err.h�ж��壬���������Լ�����ԭ������ɸ�������ģ�鶨��
        �������ֱַ�ռ�ò�ͬ��bitλ
        #define ERR_GET_LIB(l)       (int)((((unsigned long)l)>>24L)&0xffL)
        #define ERR_GET_FUNC(l)      (int)((((unsigned long)l)>>12L)&0xfffL)
        #define ERR_GET_REASON(l)    (int)((l)&0xfffL)
        ��ĸ������ܴ���255��0xff�������������ʹ���ԭ���ܴ���4095��0xfff����
        ��Ҫ���ݽṹ��������������crypto/err/err.h�У����£�
        1��ERR_STRING_DATA
            typedef struct ERR_string_data_st
            {
                unsigned long error;
                const char *string;
            } ERR_STRING_DATA;
            �����ݽṹ�������ɸ�������ģ�������á�
            ���У�error������Ŵ�����Ϣ���ɿ���롢���������Լ�����ԭ���������������
            string��������ı���Ϣ�������Ǻ�����Ҳ�����Ǵ���ԭ��
            ��crypto/bio_err.cΪ����������������ȫ�ֱ��ֱ�������ź�����Ϣ�ʹ�����Ϣ��
            #define ERR_FUNC(func) ERR_PACK(ERR_LIB_BIO,func,0)
            #define ERR_REASON(reason) ERR_PACK(ERR_LIB_BIO,0,reason)
            static ERR_STRING_DATA BIO_str_functs[]=
            {
                {ERR_FUNC(BIO_F_ACPT_STATE),  "ACPT_STATE"},
                ����
            }
            static ERR_STRING_DATA BIO_str_reasons[]=
            {
                {ERR_REASON(BIO_R_ACCEPT_ERROR)          ,"accept error"},
                {ERR_REASON(BIO_R_BAD_FOPEN_MODE)        ,"bad fopen mode"},
                ����
            }
            ��������ͨ�� ERR_load_BIO_strings ��������ӵ�������Ϣ��ϣ����ȥ��
            Ϊ�˱��ڲ��ң�����ģ��Ĵ�����Ϣ�����һ��ȫ�ֹ�ϣ���У���crypto/err.c��ʵ�֡�
        2��ERR_STATE
            typedef struct err_state_st
            {
                unsigned long pid;
                int err_flags[ERR_NUM_ERRORS];
                unsigned long err_buffer[ERR_NUM_ERRORS];
                char *err_data[ERR_NUM_ERRORS];
                int err_data_flags[ERR_NUM_ERRORS];
                const char *err_file[ERR_NUM_ERRORS];
                int err_line[ERR_NUM_ERRORS];
                int top,bottom;
            } ERR_STATE;
            �ýṹ���ڴ�źͻ�ȡ������Ϣ��
            ���ڿ��ܻ��ж�㺯������(�����ջ)����Щ��Ϣ����һ�����顣
            ÿ�����������һ�㺯���Ĵ�����Ϣ��
            �����������£�
                pid��          ��ǰ�߳�id��
                err_buffer[i]����i������룬�����⡢�����Լ�����ԭ����Ϣ��
                err_data[i]��  ��ŵ�i�������Ϣ��
                err_data_flags[i]�����err_data[i]��صı�ǣ�����ΪERR_TXT_MALLOCEDʱ��
                                    ����err_data[i]�е������Ƕ�̬�����ڴ�ģ�
                                    ��Ҫ�ͷţ�ΪERR_TXT_STRING����err_data[i]�е�������һ���ַ���������������ӡ��
                err_file[i]����i�������ļ�����
                err_line[i]����i�������кš�
                top��bottom������ָ��ERR_STATE��ʹ��״̬��
                             top��Ӧ�����һ�����󣨴����ջ�����ϲ㣩��
                             bottom��Ӧ��һ�����󣨴����ջ����ײ㣩��
        ���û���Ҫ��չopenssl��ģ��ʱ�����Է�����������ģ����ʵ���Լ��Ĵ�����
    ��Ҫ����
        1)  ERR_add_error_data
            �ڱ�������err_dataԪ�������˵����Ϣ��
            �ú���һ���ɸ���ģ����ã������������˵��ʲô���������˴���
        2�� ERR_clear_error
            ������еĴ�����Ϣ�������������д�����Ϣ�����ܻ��������޹ش���������ERR_STATE���С�
        3�� ERR_error_string/ ERR_error_string_n
            ���ݴ������ȡ����Ĵ�����Ϣ����������Ŀ⡢����ĺ����Լ�����ԭ��
        4)  ERR_free_strings
            �ͷŴ�����Ϣ��ϣ��ͨ���������á�
        5)  ERR_func_error_string
            ���ݴ���ţ���ȡ����ĺ�����Ϣ��
        6�� ERR_get_err_state_table
            ��ȡ��Ŵ���Ĺ�ϣ��
        7�� ERR_get_error
            ��ȡ��һ������š�
        8)  ERR_get_error_line
            ���ݴ���ţ���ȡ������кš�
        9)  ERR_get_error_line_data
            ���ݴ���ţ���ȡ������Ϣ��
        10) ERR_get_implementation
            ��ȡ�������������ϣ�������ء�
        11��ERR_get_state
            ��ȡERR_STATE��
        12��ERR_lib_error_string
            ���ݴ���ţ���ȡ���ĸ������
        13��ERR_load_strings
            ���ش�����Ϣ���ɸ���ģ����á�
        14��ERR_load_ASN1_strings
            ERR_load_BIO_strings
            ERR_load_BN_strings
            ERR_load_BUF_strings
            ERR_load_COMP_strings
            ERR_load_CONF_strings
            ERR_load_CRYPTO_strings
            ERR_load_crypto_strings
            ERR_load_DH_strings
            ERR_load_DSA_strings
            ERR_load_DSO_strings
            ERR_load_EC_strings
            ERR_load_ENGINE_strings
            ERR_load_ERR_strings
            ERR_load_EVP_strings
            ERR_load_OBJ_strings
            ERR_load_OCSP_strings
            ERR_load_PEM_strings
            ERR_load_PKCS12_strings
            ERR_load_PKCS7_strings
            ERR_load_RAND_strings
            ERR_load_RSA_strings
            ERR_load_UI_strings
            ERR_load_X509_strings
            ERR_load_X509V3_strings
            ����ģ��ʵ�ֵģ����ظ��Դ�����Ϣ��
        15��ERR_peek_error
            ��ȡ��һ������š�
        16��ERR_peek_error_line
            ��ȡ��һ������ĳ����С�
        17��ERR_peek_error_line_data
            ��ȡ��һ������������ʹ�����Ϣ��
        18��ERR_peek_last_error
            ��ȡ���һ������š�
        19��ERR_peek_last_error_line
            ��ȡ���һ��������кš�
        20��ERR_peek_last_error_line_data
            ��ȡ���һ��������кźʹ�����Ϣ��
        21��ERR_print_errors
            ��������Ϣ�����bio�С�
        22��ERR_print_errors_cb
            �����û����õĻص���������ӡ������Ϣ��
        23��ERR_print_errors_fp
            �������ӡ��FILE�С�
        24)  ERR_put_error
            ��������Ϣ��ŵ�ERR_STATE ����topָ���Ĵ����ջ(���Ĵ���)��
        25)  ERR_reason_error_string
            ���ݴ���ŵõ�����ԭ��
        26)  ERR_remove_state
            ɾ���߳���صĴ�����Ϣ��
        27)  ERR_set_error_data
            ��������Ϣ��ŵ�ERR_STATE ����topָ���Ĵ����ջ(���Ĵ���)��
        28)  ERR_unload_strings
            �Ӵ����ϣ����ɾ�������Ϣ��
 
��ʮ���� ժҪ��hmac
    ����˵��
        1)  XXX_Init
            XXXΪ�����ժҪ�㷨���ƣ��ú�����ʼ�������ʣ����ڶ�����ժҪ��
        2)  XXX_Update
            XXXΪ�����ժҪ�㷨���ƣ�����ժҪ���㣬�ú��������ж�Σ��Զ������ժҪ��
        3)  XXX_Final
            XXXΪ�����ժҪ�㷨���ƣ�����ժҪ���㣬�ú�����1)��2��һ���á�
        4)  XXX
            ��һ�����ݽ���ժҪ���ú���������1��2����3��ʵ�֣�ֻ��XXX_Updateֻ����һ��
            
��ʮ���� ����ѹ��
    ���ݽṹ
        COMP_METHOD��ѹ���㷨��
            typedef struct comp_method_st
            {
                int type;
                const char *name;
                int (*init)(COMP_CTX *ctx);
                void (*finish)(COMP_CTX *ctx);
                int (*compress)(COMP_CTX *ctx,unsigned char *out, unsigned int olen,                
                                unsigned char *in, unsigned int ilen);
                int (*expand)(COMP_CTX *ctx,unsigned char *out, unsigned int olen,                      
                              unsigned char *in, unsigned int ilen);
                long (*ctrl)(void);
                long (*callback_ctrl)(void);
            } COMP_METHOD;
            �����������£�
                type��ѹ���㷨��nid��
                name��ѹ���㷨�����֣�
                init����ʼ��������
                finish������������
                commpress�������ѹ���㷨������������ʵ�֣�
                expand������Ľ�ѹ�㷨������������ʵ�֣�
                ctrl��callback_ctrl�����ƺ�����ص����ƺ����������ڲ����ơ�
        comp_ctx�����ѹ��/��ѹ�е����������ݣ�
            struct comp_ctx_st
            {
                COMP_METHOD *meth;
                unsigned long compress_in;
                unsigned long compress_out;
                unsigned long expand_in;
                unsigned long expand_out;
                CRYPTO_EX_DATA     ex_data;
            };
            �����������£�
                meth��COMP_METHOD�ṹ��һ��comp_ctxͨ����ָ����һ�־����ѹ���㷨��
                compress_in����ѹ���������ֽ�����
                compress_out��ѹ������(���)���ֽ�����
                expand_in������ѹ�������ֽ�����
                expand_out����ѹ���ݣ���������ֽ�����
                ex_data�����û�ʹ�õ���չ���ݣ����ڴ���û��Զ������Ϣ��
    ����˵��
        1)  COMP_rle
            ����opensslʵ�ֵĿ�ѹ���㷨������ֵΪһ��COMP_METHOD��
        2)  COMP_zlib
            ���ػ���zlib���COMP_METHOD��
        3�� COMP_CTX_new
            ��ʼ�������ģ��������ΪCOMP_METHOD��
        4�� COMP_compress_block
            ѹ�����㡣
        5�� COMP_expand_block
            ��ѹ���㡣
            
��ʮ���� rsa
    ���
        RSA�㷨��һ���㷺ʹ�õĹ�Կ�㷨������Կ������Կ��˽Կ��
        ������������ǩ���������֤�Լ���Կ������
    RSA��Կ��Ϣ��Ҫ������
        n��   ģ��
        e��   ��Կָ��
        d��   ˽Կָ��
        p��   ����Ĵ�����
        q��   ����Ĵ�����
        dmp1��e*dmp1 = 1 (mod (p-1))
        dmq1��e*dmq1 = 1 (mod (q-1))
        iqmp��q*iqmp = 1 (mod p )
        �Σ�file://RSAԭ��.txt
    openssl��RSAʵ��Դ�����£�
        1��rsa.h
           ����RSA���ݽṹ�Լ�RSA_METHOD��������RSA�ĸ��ֺ�����
        2) rsa_asn1.c
           ʵ����RSA��Կ��DER����ͽ��룬������Կ��˽Կ��
        3��rsa_chk.c
           RSA��Կ��顣
        4��rsa_eay.c
           Opensslʵ�ֵ�һ��RSA_METHOD����Ϊ��Ĭ�ϵ�һ��RSA����ʵ�ַ�ʽ��
           ���ļ�δʵ��rsa_sign��rsa_verify��rsa_keygen�ص�������
        5��rsa_err.c
           RSA������
        6��rsa_gen.c
           RSA��Կ���ɣ����RSA_METHOD�е�rsa_keygen�ص�������Ϊ�գ��������������������ڲ�ʵ�֡�
        7��rsa_lib.c
           ��Ҫʵ����RSA������ĸ�����(��Կ/˽Կ������/����)�����Ƕ�������RSA_METHOD����Ӧ���ص�������
        8��rsa_none.c
           ʵ����һ������ȥ��䡣
        9��rsa_null.c
           ʵ����һ�ֿյ�RSA_METHOD��
        10) rsa_oaep.c
           ʵ����oaep�����ȥ��䡣
        11��rsa_pk1.c
           ʵ����pkcs1�����ȥ��䡣
        12��rsa_sign.c
           ʵ����RSA��ǩ������ǩ��
        13��rsa_ssl.c
           ʵ����ssl��䡣
        14��rsa_x931.c
           ʵ����һ������ȥ��䡣
    RSAǩ������֤����
        RSAǩ���������£�
            1) ���û����ݽ���ժҪ��
            2������X509_SIG�ṹ��DER���룬���а�����ժҪ�㷨�Լ�ժҪ�����
            3����2���Ľ��������䣬����RSA��Կ�����ֽ�����
               ����1024λRSA��Կ��������128�ֽڡ��������䷽ʽ���û�ָ����
            4����3���Ľ����RSA˽Կ���ܡ�
            ע RSA_eay_private_encrypt����ʵ����3����4�����̡�
        RSA��ǩ�������������̵�����̣����£�
            1) ��������RSA��Կ���ܣ��õ�ǩ��������2���Ľ����
            2) ȥ��1���������䡣
            3) ��2���Ľ���еõ�ժҪ�㷨���Լ�ժҪ�����
            4) ��ԭ���ݸ���3���еõ�ժҪ�㷨����ժҪ���㡣
            5���Ƚ�4����ǩ��������1���Ľ����
            ע RSA_eay_public_decryptʵ����1����2�����̡�
    ���ݽṹ
        RSA_METHOD
            struct rsa_meth_st
            {
                const char      *name;
                int (*rsa_pub_enc)(int flen,const unsigned char *from,unsigned char *to,RSA *rsa,int padding);
                int (*rsa_pub_dec)(int flen,const unsigned char *from,unsigned char *to,RSA *rsa,int padding);
                int (*rsa_priv_enc)(int flen,const unsigned char *from,unsigned char *to,RSA *rsa,int padding);
                int (*rsa_priv_dec)(int flen,const unsigned char *from,unsigned char *to,RSA *rsa,int padding);
                /* �������� */
                int (*rsa_sign)(int type,const unsigned char *m, unsigned int m_length,unsigned char *sigret,
                                unsigned int *siglen, const RSA *rsa);
                int (*rsa_verify)(int dtype,const unsigned char *m, unsigned int m_length,unsigned char *sigbuf, 
                                  unsigned int siglen, const RSA *rsa);
                int (*rsa_keygen)(RSA *rsa, int bits, BIGNUM *e, BN_GENCB *cb);
            };
            ��Ҫ��˵����
                name��RSA_METHOD���ƣ�
                rsa_pub_enc�� ��Կ���ܺ�����paddingΪ����䷽ʽ���������ݲ���̫���������޷���䣻
                rsa_pub_dec�� ��Կ���ܺ�����paddingΪ��ȥ�����ķ�ʽ���������ݳ���ΪRSA��Կ���ȵ��ֽ�����
                rsa_priv_enc��˽Կ���ܺ�����paddingΪ����䷽ʽ���������ݳ��Ȳ���̫���������޷���䣻
                rsa_priv_dec��˽Կ���ܺ�����paddingΪ��ȥ�����ķ�ʽ���������ݳ���ΪRSA��Կ���ȵ��ֽ�����
                rsa_sign��    ǩ��������
                rsa_verify��  ��ǩ������
                rsa_keygen��  RSA��Կ�����ɺ�����
            �û���ʵ���Լ���RSA_METHOD���滻openssl�ṩ��Ĭ�Ϸ�����
        RSA
            RSA���ݽṹ�а����˹�/˽Կ��Ϣ���������n��e��������ǹ�Կ�����������£�
            struct rsa_st
            {
                /* ���� */
                const RSA_METHOD *meth;
                ENGINE *engine;
                BIGNUM *n;
                BIGNUM *e;
                BIGNUM *d;
                BIGNUM *p;
                BIGNUM *q;
                BIGNUM *dmp1;
                BIGNUM *dmq1;
                BIGNUM *iqmp;
                CRYPTO_EX_DATA ex_data;
                int references;
                /* ���������� */
            };
            �������壺
                meth��RSA_METHOD�ṹ��ָ���˱�RSA��Կ�ĸ������㺯����ַ��
                engine��Ӳ�����棻
                n��e��d��p��q��dmp1��dmq1��iqmp��RSA��Կ�ĸ���ֵ��
                ex_data����չ���ݽṹ�����ڴ���û����ݣ�
                references��RSA�ṹ��������
    ��Ҫ����
        1�� RSA_check_key
            ���RSA��Կ��
        2�� RSA_new
            ����һ��RSA��Կ�ṹ��������Ĭ�ϵ�rsa_pkcs1_eay_meth RSA_METHOD������
        3�� RSA_free
            �ͷ�RSA�ṹ��
        4)  RSA *RSA_generate_key(int bits, unsigned long e_value,
            void (*callback)(int,int,void *), void *cb_arg)
            ����RSA��Կ��bits��ģ����������e_value�ǹ�Կָ��e��callback�ص��������û�ʵ�֣�
            ���ڸ�Ԥ��Կ���ɹ����е�һЩ���㣬��Ϊ�ա�
        5�� RSA_get_default_method
            ��ȡĬ�ϵ�RSA_METHOD��Ϊrsa_pkcs1_eay_meth��
        6�� RSA_get_ex_data
            ��ȡ��չ���ݡ�
        7�� RSA_get_method
            ��ȡRSA�ṹ��RSA_METHOD��
        8�� RSA_padding_add_none
            RSA_padding_add_PKCS1_OAEP
            RSA_padding_add_PKCS1_type_1��˽Կ���ܵ���䣩
            RSA_padding_add_PKCS1_type_2����Կ���ܵ���䣩
            RSA_padding_add_SSLv23
            ������䷽ʽ������
        9�� RSA_padding_check_none
            RSA_padding_check_PKCS1_OAEP
            RSA_padding_check_PKCS1_type_1
            RSA_padding_check_PKCS1_type_2
            RSA_padding_check_SSLv23
            RSA_PKCS1_SSLeay
            ����ȥ����亯����
        10��int RSA_print(BIO *bp, const RSA *x, int off)
            ��RSA��Ϣ�����BIO�У�offΪ�����Ϣ��BIO�е�ƫ������
            ��������ĻBIO�����ʾ��ӡ��Ϣ��λ���������Ļ��Ե�ľ��롣
        11��int DSA_print_fp(FILE *fp, const DSA *x, int off)
            ��RSA��Ϣ�����FILE�У�offΪ���ƫ������
        12��RSA_public_decrypt
            RSA��Կ���ܡ�
        13��RSA_public_encrypt
            RSA��Կ���ܡ�
        14��RSA_set_default_method/ RSA_set_method
            ����RSA�ṹ�е�method�����û�ʵ����һ��RSA_METHODʱ��
            ���ô˺��������ã�ʹRSA��������û��ķ�����
        15��RSA_set_ex_data
            ������չ���ݡ�
        16��RSA_sign
            RSAǩ����
        17��RSA_sign_ASN1_OCTET_STRING
            ����һ��RSAǩ�������漰ժҪ�㷨����������������ΪASN1_OCTET_STRING
            ����DER���룬Ȼ��ֱ�ӵ���RSA_private_encrypt���м��㡣
        18��RSA_size
            ��ȡRSA��Կ�����ֽ�����
        19��RSA_up_ref
            ��RSA��Կ����һ�����á�
        20��RSA_verify
            RSA��֤��
        21��RSA_verify_ASN1_OCTET_STRING
            ��һ��RSA��֤�����漰ժҪ�㷨����RSA_sign_ASN1_OCTET_STRING��Ӧ��
        22��RSAPrivateKey_asn1_meth
            ��ȡRSA˽Կ��ASN1_METHOD������i2d��d2i��new��free������ַ��
        23��RSAPrivateKey_dup
            ����RSA˽Կ��
        24��RSAPublicKey_dup
            ����RSA��Կ��
                
��ʮ���� DSA
    ���
        DSA�㷨��һ�ֹ�Կ�㷨��DSA��ȫ�Ի�����ɢ��������
        DSA ֻ����������ǩ�������޷����ڼ��ܣ�ĳЩ��չ����֧�ּ��ܣ�
        ��RSA��ȣ�DSA��ǩ�������ٶȸ��죬����֤�ٶȽ���
        file://RSA��DSA��ECDSA��EdDSA �� Ed25519 ������.py
        ��ΪDSA�Ѿ����Ƽ�ʹ�ã����������Թ�������ο�chm�ļ�
        
��ʮ���� DH
    ���
        ��ʵ����һ��ͨ��˫��������ԿЭ�̵�Э�飺
            ����ʵ���е��κ�һ��ʹ���Լ���˽Կ����һʵ��Ĺ�Կ���õ�һ���Գ���Կ��
            ��һ�Գ���Կ����ʵ�嶼���㲻����
        DH�㷨�İ�ȫ�Ի����������ϼ�����ɢ�����������ԡ�
        ��ɢ�������о���״��������ʹ�õ�DH��Կ������Ҫ1024λ�����ܱ�֤���㹻���С����ڰ�ȫ��
        DH�㷨���ܵ����м��˹������м��˿���α��ٵ�X��Y�ֱ��͸�˫������ȡ���ǵ�������Կ��
        ������Ҫ��֤X��Y����Դ�Ϸ��ԡ�
    ���ݽṹ
        DH_METHOD
            struct dh_method
            {
                const char *name;
                int (*generate_key)(DH *dh);
                int (*compute_key)(unsigned char *key,const BIGNUM *pub_key,DH *dh);
                int (*bn_mod_exp)(const DH *dh, BIGNUM *r, const BIGNUM *a,
                                  const BIGNUM *p, const BIGNUM *m, BN_CTX *ctx,
                                  BN_MONT_CTX *m_ctx);
                int (*init)(DH *dh);
                int (*finish)(DH *dh);
                int flags;
                char *app_data;
                int (*generate_params)(DH *dh, int prime_len, int generator, BN_GENCB *cb);
            };
            DH_METHODָ����һ��DH��Կ���еļ��㷽��������
            �û�����ʵ���Լ���DH_METHOD���滻openssl�ṩĬ�Ϸ�����
            �����������£�
                name��           DH_METHOD�������ơ�
                generate_key��   ����DH��˽Կ�ĺ�����
                compute_key��    ���ݶԷ���Կ�ͼ���DH��Կ�����ɹ�����Կ�ĺ�����
                bn_mod_exp��     ����ģ���㺯��������û�ʵ������������DH��Կʱ��
                                 �������û�ʵ�ֵĸûص����������ڸ�ԤDH��Կ���ɡ�
                init��           ��ʼ��������
                finish��         ����������
                flags��          ���ڼ�¼��ǡ�
                app_data��       ���ڴ��Ӧ�����ݡ�
                generate_params������DH��Կ�����Ļص����������ɵ���Կ�����ǿ��Թ����ġ�
        DH
            struct dh_st
            {
                /* ���� */
                BIGNUM *p;
                BIGNUM *g;
                long length;      /* optional */
                BIGNUM *pub_key;
                BIGNUM *priv_key; 
                int references;
                CRYPTO_EX_DATA ex_data;
                const DH_METHOD *meth;
                ENGINE *engine;
                /* ���� */
            };
            ���ͣ�
                p��g��length��DH��Կ������
                pub_key��    DH��Կ��
                priv_key��   DH˽Կ��
                references�� ���ã�
                ex_data��    ��չ���ݣ�
                meth��       DH_METHOD����DH��Կ�ĸ��ּ��㷽������ȷָ����DH�ĸ������㷽ʽ��
                engine��     Ӳ�����档
    ��Ҫ����
        1�� DH_new
            ����DH���ݽṹ����DH_METHOD����opensslĬ���ṩ�ġ�
        2�� DH_free
            �ͷ�DH���ݽṹ��
        3�� DH_generate_parameters
            ����DH��Կ������
        4�� DH_generate_key
            ����DH��˽Կ��
        5�� DH_compute_key
            ���㹲����Կ���������ݽ�����
        6�� DH_check
            ���DH��Կ��
        7�� DH_get_default_method
            ��ȡĬ�ϵ�DH_METHOD���÷����ǿ������û����õġ�
        8�� DH_get_ex_data
            ��ȡDH�ṹ�е���չ���ݡ�
        9)  DH_new_method
            ����DH���ݽṹ��
        10��DH_OpenSSL
            ��ȡopenssl�ṩ��DH_METHOD��
        11��DH_set_default_method
            ����Ĭ�ϵ�DH_METHOD���������û�ʵ�����Լ���DH_METHODʱ���ɵ��ñ����������ã�����DH���ּ��㡣
        12��DH_set_ex_data
            ��ȡ��չ���ݡ�
        13��DH_set_method
            �滻���е�DH_METHOD��
        14��DH_size
            ��ȡDH��Կ���ȵ��ֽ�����
        15) DH_up_ref
            ����DH�ṹ��һ�����á�
        16��DHparams_print
            ��DH��Կ���������bio�С�
        17) DHparams_print_fp
            ��DH��Կ���������FILE�С�

�ڶ�ʮ�� ECC
    ���
        ��Բ����(ECC)�㷨��һ�ֹ�Կ�㷨���������е�RSA�㷨�кܶ��ŵ㣺
        1����ȫ���ܸ��� �� ��160λECC��1024λRSA��DSA����ͬ�İ�ȫǿ�ȡ�
        2��������С�������ٶȿ죬 ��˽Կ�Ĵ����ٶ��ϣ����ܺ�ǩ������ECC��RSA��DSA��öࡣ
        3���洢�ռ�ռ��С  ECC����Կ�ߴ��ϵͳ������RSA��DSA���ҪС�ö࣬ ����ռ�õĴ洢�ռ�С�öࡣ
        4������Ҫ��͡�
    openssl��ECCʵ��
        Opensslʵ����ECC�㷨��
        ECC�㷨ϵ�а��������֣�
            ECC�㷨(crypto/ec)��
            ��Բ��������ǩ���㷨ECDSA (crypto/ecdsa)
            ��Բ������Կ�����㷨ECDH(crypto/dh)
        ��Կ���ݽṹ
            ��Ҫ�ǹ�Կ��˽Կ���ݽṹ��
            ��Բ������Կ���ݽṹ���£�������crypto/ec_lcl.h�У����û���͸���ġ�
            struct ec_key_st
            {
                int         version;
                EC_GROUP    *group;
                EC_POINT    *pub_key;
                BIGNUM      *priv_key;
                /* ������ */
            }
        ��Կ����
            ���չ�Կ��˽Կ�ı�ʾ�������ǶԳ��㷨��ͬ�и��Ե���Կ���ɹ��̡�
            ��Բ���ߵ���Կ����ʵ����crytpo/ec/ec_key.c�С�
            Openssl�У���Բ������Կ����ʱ�������û���Ҫѡȡһ����Բ����
            (openssl��crypto/ec_curve.c������ʵ����67�֣�����EC_get_builtin_curves��ȡ���б�)��
            Ȼ�����ѡ�����Բ���߼�����Կ���ɲ���group����������Կ����group������˽Կ��
        ǩ��ֵ���ݽṹ
            �ǶԳ��㷨��ͬ��ǩ���Ľ����ʾҲ��һ����
            ��DSAǩ��ֵһ����ECDSA��ǩ�������ʾΪ���
            ECDSA��ǩ��������ݽṹ������crypto/ecdsa/ecdsa.h�У����£�
            typedef struct ECDSA_SIG_st
            {
                BIGNUM *r;
                BIGNUM *s;
            } ECDSA_SIG;
        ǩ������ǩ
            ����ǩ��������о�����������ɵġ�
            crypto/ecdsa/ecs_sign.cʵ����ǩ���㷨��
            crypto/ecdsa/ecs_vrf.cʵ������ǩ��
        ��Կ����
            �о�����Կ��������ν��еģ�
            crypto/ecdh/ech_ossl.cʵ������Կ�����㷨��
        ��Ҫ����
            1�� EC_get_builtin_curves
                ��ȡ��Բ�����б�
            2�� EC_GROUP_new_by_curve_name
                ����ָ������Բ������������Կ������
            3�� EC_KEY_generate_key
                ������Կ��������ECC��˽Կ��
            4�� EC_KEY_check_key
                ���ECC��Կ��
            5�� ECDSA_size
                ��ȡECC��Կ��С�ֽ�����
            6�� ECDSA_sign
                ǩ��������1��ʾ�ɹ���
            7�� ECDSA_verify
                ��ǩ������1��ʾ�Ϸ���
            8�� EC_KEY_get0_public_key
                ��ȡ��Կ��
            9�� EC_KEY_get0_private_key
                ��ȡ˽Կ��
            10��ECDH_compute_key
                ���ɹ�����Կ
                
�ڶ�ʮһ�� evp
    Openssl EVP(high-level cryptographic functions[1])�ṩ�˷ḻ������ѧ�еĸ��ֺ���
    Openssl��ʵ���˸���ժҪ�㷨���Գ��㷨�Լ�ǩ��/��ǩ�㷨��
    EVP��������Щ������㷨�����˷�װ��
    EVP��Ҫ��װ�����¹��ܺ�����
        1�� ʵ����base64�����BIO��
        2�� ʵ���˼ӽ���BIO��
        3�� ʵ����ժҪBIO��
        4�� ʵ����reliable BIO��
        5�� ��װ��ժҪ�㷨��
        6�� ��װ�˶ԳƼӽ����㷨��
        7�� ��װ�˷ǶԳ���Կ�ļ���(��Կ)������(˽Կ)��ǩ������֤�Լ�����������
        7�� ���ڿ���ļ���(PBE)��
        8�� �Գ���Կ����
        9�� �����ŷ⣺�����ŷ��öԷ��Ĺ�Կ���ܶԳ���Կ���������ô˶Գ���Կ���ܡ�
            ���͸��Է�ʱ��ͬʱ���ͶԳ���Կ���ĺ��������ġ�
            ���շ��������Լ���˽Կ������Կ���ģ��õ��Գ���Կ��Ȼ�������������ݡ�
        10����������������
    ���ݽṹ
        EVP���ݽṹ������crypto/evp.h��
        EVP_PKEY
            struct evp_pkey_st
            {
                int references;
                union      
                {
                     char *ptr;
                     'ifndef OPENSSL_NO_RSA
                     struct rsa_st *rsa;  /* RSA */
                     'endif
                     'ifndef OPENSSL_NO_DSA
                     struct dsa_st *dsa;/* DSA */
                     'endif
                     'ifndef OPENSSL_NO_DH
                     struct dh_st *dh;    /* DH */
                     'endif
                     'ifndef OPENSSL_NO_EC
                     struct ec_key_st *ec;     /* ECC */
                     'endif
                } pkey;
                STACK_OF(X509_ATTRIBUTE) *attributes; /* [ 0 ] */
            };
            �ýṹ������ŷǶԳ���Կ��Ϣ��������RSA��DSA��DH��ECC��Կ��
            ���У� ptr ���������Կ�ṹ��ַ��attributes��ջ���������Կ���ԡ�
        EVP_MD
            struct env_md_st
            {
                int type;
                int pkey_type;
                int md_size;
                unsigned long flags;
                int (*init)(EVP_MD_CTX *ctx);
                int (*update)(EVP_MD_CTX *ctx,const void *data,size_t count);
                int (*final)(EVP_MD_CTX *ctx,unsigned char *md);
                int (*copy)(EVP_MD_CTX *to,const EVP_MD_CTX *from);
                int (*cleanup)(EVP_MD_CTX *ctx);
                int (*sign)(int type, const unsigned char *m, unsigned int m_length,
                            unsigned char *sigret, unsigned int *siglen, void *key);
                int (*verify)(int type, const unsigned char *m, unsigned int m_length,
                              const unsigned char *sigbuf, unsigned int siglen, void *key);
                int required_pkey_type[5];
                int block_size;
                int ctx_size;  # how big does the ctx->md_data need to be 
            } ;
            �ýṹ�������ժҪ�㷨��Ϣ���ǶԳ��㷨�����Լ����ּ��㺯����
            ��Ҫ�����������£�
                type��     ժҪ���ͣ�һ����ժҪ�㷨NID��
                pkey_type����Կ���ͣ�һ����ǩ���㷨NID��
                md_size��  ժҪֵ��С��Ϊ�ֽ�����
                flags��    �������ñ�ǣ�
                init��     ժҪ�㷨��ʼ��������
                update��   ���ժҪ������
                final��    ժҪ��ắ����
                copy��     ժҪ�����Ľṹ���ƺ�����
                cleanup��  ���ժҪ�����ĺ�����
                sign��     ǩ������������keyΪ�ǶԳ���Կ�ṹ��ַ��
                verify��   ժҪ����������keyΪ�ǶԳ���Կ�ṹ��ַ��
            openssl���ڸ���ժҪ�㷨ʵ���������ṹ������Դ��λ��cypto/evpĿ¼�£��ļ�����m_��ͷ��
            Opensslͨ����Щ�ṹ����װ�˸���ժҪ��ص����㡣
        EVP_CIPHER
            struct evp_cipher_st
            {
                int nid;
                int block_size;
                int key_len;     
                int iv_len;
                unsigned long flags;
                int (*init)(EVP_CIPHER_CTX *ctx, const unsigned char *key,
                  const unsigned char *iv, int enc);
                int (*do_cipher)(EVP_CIPHER_CTX *ctx, unsigned char *out,
                      const unsigned char *in, unsigned int inl);
                int (*cleanup)(EVP_CIPHER_CTX *); /* cleanup ctx */
                int ctx_size;
                int (*set_asn1_parameters)(EVP_CIPHER_CTX *, ASN1_TYPE *);
                int (*get_asn1_parameters)(EVP_CIPHER_CTX *, ASN1_TYPE *);
                int (*ctrl)(EVP_CIPHER_CTX *, int type, int arg, void *ptr);
                void *app_data;
            } ;
            �ýṹ������ŶԳƼ�����ص���Ϣ�Լ��㷨����Ҫ�����������£�
                nid��        �Գ��㷨nid��
                block_size�� �Գ��㷨ÿ�μӽ��ܵ��ֽ�����
                key_len��    �Գ��㷨����Կ�����ֽ�����
                iv_len��     �Գ��㷨����䳤�ȣ�
                flags��      ���ڱ�ǣ�
                init��       ���ܳ�ʼ��������������ʼ��ctx��keyΪ�Գ���Կֵ��ivΪ��ʼ��������
                             enc����ָ����Ҫ���ܻ��ǽ��ܣ���Щ��Ϣ�����ctx�У�
                do_cipher��  �Գ����㺯�������ڼ��ܻ���ܣ�
                cleanup��    ��������ĺ�����
                set_asn1_parameters�����������Ĳ���������
                get_asn1_parameters����ȡ�����Ĳ���������
                ctrl��       ���ƺ�����
                app_data��   ���ڴ��Ӧ�����ݡ�
            openssl���ڸ��ֶԳ��㷨ʵ���������ṹ������Դ��λ��cypto/evpĿ¼�£��ļ�����e_��ͷ��
            Opensslͨ����Щ�ṹ����װ�˶Գ��㷨��ص����㡣
        EVP_CIPHER_CTX
            struct evp_cipher_ctx_st
            {
                const EVP_CIPHER *cipher;
                ENGINE *engine;   
                int encrypt;     
                int buf_len;
                unsigned char  oiv[EVP_MAX_IV_LENGTH];
                unsigned char  iv[EVP_MAX_IV_LENGTH];     
                unsigned char        buf[EVP_MAX_BLOCK_LENGTH];
                /* ���� */
                unsigned char final[EVP_MAX_BLOCK_LENGTH];
            } ;
            �Գ��㷨�����Ľṹ���˽ṹ��Ҫ����ά���ӽ���״̬������м��Լ��������
            ��Ϊ���ܻ����ʱ�������ݺܶ�ʱ�����ܻ��õ�Update������
            ����ÿ�μ��ܻ���ܵ��������ݳ�������ģ�����һ���ǶԳ��㷨block_size����������
            ������Ҫ�øýṹ������м�δ���ܵ����ݡ�
            ��Ҫ���������£�
                cipher��       ָ���Գ��㷨��
                engine��       Ӳ�����棻
                encrypt��      �Ǽ��ܻ��ǽ��ܣ���0Ϊ���ܣ�0Ϊ���ܣ�
                buf��buf_len�� ָ�����ж�������δ�������㣻
                oiv��          ԭʼ��ʼ��������
                iv��           ��ǰ�ĳ�ʼ��������
                final��        ������ս����һ����Final������Ӧ��
    Դ��ṹ
        evpԴ��λ��crypto/evpĿ¼�����Է�Ϊ���¼��ࣺ
        1)  ȫ�ֺ���
            ��Ҫ����c_all.c��c_allc.c��c_alld.c�Լ�names.c��
            ���Ǽ���openssl֧�ֵ����еĶԳ��㷨��ժҪ�㷨�����뵽��ϣ���С�
            ʵ����OpenSSL_add_all_digests��OpenSSL_add_all_ciphers�Լ�
            OpenSSL_add_all_algorithms(������ǰ��������)������
            �ڽ��м���ʱ���û�Ҳ���Ե�������ժҪ������EVP_add_digest���ͶԳƼ��㺯����EVP_add_cipher����
        2)  BIO����
            ����bio_b64.c��bio_enc.c��bio_md.c��bio_ok.c������ʵ����BIO_METHOD������
            �ֱ�����base64����롢�ԳƼӽ����Լ�ժҪ��
        3)  ժҪ�㷨EVP��װ
            ��digest.cʵ�֣�ʵ�ֹ����е����˶�ӦժҪ�㷨�Ļص�������
            ����ժҪ�㷨�ṩ���Լ���EVP_MD��̬�ṹ����ӦԴ��Ϊm_xxx.c��
        4�� �Գ��㷨EVP��װ
            ��evp_enc.cʵ�֣�ʵ�ֹ��̵����˾���Գ��㷨������ʵ����Update������
            ���ֶԳ��㷨���ṩ��һ��EVP_CIPHER��̬�ṹ����ӦԴ��Ϊe_xxx.c��
            ��Ҫע����ǣ�e_xxx.c�в��ṩ�����ļӽ������㣬��ֻ�ṩ�����Ķ���һ��block_size���ݵļ��㣬
            �����ļ�����evp_enc.c��ʵ�֡����û������һ���Լ��ĶԳ��㷨ʱ�����Բο�e_xxx.c��ʵ�ַ�ʽ��
            һ���û�������Ҫʵ�����¹��ܣ�
            ?  ����һ���µľ�̬��EVP_CIPHER�ṹ��
            ?  ʵ��EVP_CIPHER�ṹ�е�init�������ú�����������iv��
               ���üӽ��ܱ�ǡ��Լ�����������Կ�����Լ����ڲ���Կ��
            ?  ʵ��do_cipher�������ú�������block_size�ֽڵ����ݽ��жԳ����㣻
            ?  ʵ��cleanup�������ú�����Ҫ��������ڴ��е���Կ��Ϣ��
        5)  �ǶԳ��㷨EVP��װ
            ��Ҫ����p_��ͷ���ļ������У�p_enc.c��װ�˹�Կ���ܣ�p_dec.c��װ��˽Կ���ܣ�p_lib.cʵ��һЩ����������
            p_sign.c��װ��ǩ��������p_verify.c��װ����ǩ������p_seal.c��װ�������ŷ⣻p_open.c��װ�˽������ŷ⡣
        6�� ���ڿ���ļ���
            ����p5_crpt2.c��p5_crpt.c��evp_pbe.c��
    ժҪ����
        '���͵�'ժҪ������Ҫ�У�
        1��  EVP_md5 
             ����md5��EVP_MD��
        2)   EVP_sha1
             ����sha1��EVP_MD��
        3)   EVP_sha256
             ����sha256��EVP_MD��
        4��  EVP_DigestInit
             ժҪ��ʹ����������Ҫ��EVP_MD��Ϊ���������
        5��  EVP_DigestUpdate��EVP_DigestInit_ex
             ժҪUpdate���������ڽ��ж��ժҪ��
        6��  EVP_DigestFinal��EVP_DigestFinal_ex
             ժҪFinal�������û��õ����ս����
        7��  EVP_Digest
             ��һ�����ݽ���ժҪ�������ε�������������������
    �ԳƼӽ��ܺ���
        '���͵�'�ӽ��ܺ�����Ҫ�У�
        1��  EVP_CIPHER_CTX_init
             ��ʼ���ԳƼ��������ġ�
        2��  EVP_CIPHER_CTX_cleanup
             ����Գ��㷨���������ݣ��������û��ṩ�����ٺ�����������е��ڲ���Կ�Լ��������ݡ�
        3��  EVP_des_ede3_ecb
             ����һ��EVP_CIPHER��
        4)   EVP_EncryptInit��EVP_EncryptInit_ex
             ���ܳ�ʼ�����������������þ����㷨��init�ص�������
             ��������Կkeyת��Ϊ�ڲ���Կ��ʽ������ʼ������iv������ctx�ṹ�С�
        5��  EVP_EncryptUpdate
             ���ܺ��������ڶ�μ��㣬�������˾����㷨��do_cipher�ص�������
        6��  EVP_EncryptFinal��EVP_EncryptFinal_ex
             ��ȡ���ܽ�������������漰��䣬�������˾����㷨��do_cipher�ص�������
        7��  EVP_DecryptInit��EVP_DecryptInit_ex
             ���ܳ�ʼ��������
        8��  EVP_DecryptUpdate
             ���ܺ��������ڶ�μ��㣬�������˾����㷨��do_cipher�ص�������
        9��  EVP_DecryptFinal��EVP_DecryptFinal_ex
             ��ȡ���ܽ�������������漰ȥ��䣬�������˾����㷨��do_cipher�ص�������
        10�� EVP_BytesToKey
             ������Կ�������������㷨���͡�ժҪ�㷨��salt�Լ��������ݼ����һ���Գ���Կ�ͳ�ʼ������iv��
        11�� PKCS5_PBE_keyivgen��PKCS5_v2_PBE_keyivgen
             ʵ����PKCS5���ڿ���������Կ�ͳ�ʼ���������㷨��
        12�� PKCS5_PBE_add
             ��������opensslʵ�ֵĻ��ڿ���������Կ���㷨��
        13�� EVP_PBE_alg_add
             ���һ��PBE�㷨��
    �ǶԳƺ���
        '���͵�'�ǶԳƺ����У�
        1��  EVP_PKEY_encrypt
             ��Կ���ܡ�
        2)   EVP_PKEY_decrypt
             ˽Կ���ܡ�
        3)   EVP_PKEY_assign
             ����EVP_PKEY�о������Կ�ṹ��ʹ���������Կ��
        4)   EVP_PKEY_assign_RSA/ EVP_PKEY_set1_RSA
             ����EVP_PKEY�е�RSA��Կ�ṹ��ʹ�������RSA��Կ��
        5)   EVP_PKEY_get1_RSA
             ��ȡEVP_PKEY��RSA��Կ�ṹ��
        6)   EVP_SignFinal
             ǩ���������������������˽Կ(EVP_PKEY)��
        7)   EVP_VerifyFinal
             ��֤ǩ����������������й�Կ(EVP_PKEY)��
        8)   int EVP_OpenInit(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *type,
                              const unsigned char *ek, int ekl, 
                              const unsigned char *iv,EVP_PKEY *priv)
             �������ŷ��ʼ��������typeΪ�ԳƼ����㷨��ekΪ��Կ���ģ�
             eklΪ��Կ���ĳ��ȣ�ivΪ���ֵ��privΪ�û�˽Կ��
        9)   EVP_OpenUpdate
             ���������㡣
        10)  EVP_OpenFinal
             ���������㣬�⿪�����ŷ⡣
        11)  int EVP_SealInit(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *type, 
                              unsigned char **ek,int *ekl, unsigned char *iv, 
                              EVP_PKEY **pubk, int npubk)
             typeΪ�Գ��㷨��ek����������Ŷ����Կ����Կ���ܵĽ����
             ekl���ڴ��ek������ÿ����Կ���ĵĳ��ȣ�ivΪ���ֵ��pubk����������Ŷ����Կ��
             npubkΪ��Կ�������������ö����Կ�ֱ������Կ���������ܳ�ʼ����
        12�� EVP_SealUpdate
             ���������㡣
        13�� EVP_SealFinal
             ���������㣬���������ŷ⡣
     BASE64����뺯��
        1)   EVP_EncodeInit
             BASE64�����ʼ����
        2)   EVP_EncodeUpdate
             BASE64���룬�ɶ�ε��á�
        3)   EVP_EncodeFinal
             BASE64���룬����ȡ���ս����
        4)   EVP_DecodeInit
             BASE64�����ʼ����
        5)   EVP_DecodeUpdate
             �������ݳ��Ȳ��ܴ���80�ֽڡ�BASE64����ɶ�ε��ã�ע�⣬���������������ݲ���̫����
        6)   EVP_DecodeFinal
             BASE64���룬����ȡ���ս����
        7��  EVP_EncodeBlock
             BASE64���뺯�����������ɵ������á�
        8��  EVP_DecodeBlock
             BASE64���룬�������ɵ������ã����������ݳ�����Ҫ��
     ��������
        1��  EVP_add_cipher
             ���Գ��㷨���뵽ȫ�ֱ������Թ����á�
        2��  EVP_add_digest
             ��ժҪ�㷨���뵽ȫ�ֱ����У��Թ����á�
        -------------------------------------------------------------------------     
        3)   EVP_CIPHER_CTX_ctrl
             �Գ��㷨���ƺ��������������û�ʵ�ֵ�ctrl�ص�������
        4)   EVP_CIPHER_CTX_set_key_length
             ���Գ��㷨��Կ����Ϊ�ɱ䳤ʱ�����öԳ��㷨����Կ���ȡ�
        5)   EVP_CIPHER_CTX_set_padding
             ���öԳ��㷨����䣬�Գ��㷨��ʱ����漰��䡣
             ���ܷ��鳤�ȴ���һʱ���û��������ݲ��Ǽ��ܷ����������ʱ�����漰����䡣
             ��������һ����������ɣ�openssl�������ʱ�������n����䣬�����һ��������n��������
        6)   EVP_CIPHER_get_asn1_iv
             ��ȡԭʼiv�������ASN1_TYPE�ṹ�С�
        7)   EVP_CIPHER_param_to_asn1
             ���öԳ��㷨���������������ASN1_TYPE�����У�
             �������û�ʵ�ֵĻص�����set_asn1_parameters��ʵ�֡�
        8)   EVP_CIPHER_type
             ��ȡ�Գ��㷨�����͡�
        9��  EVP_CipherInit/EVP_CipherInit_ex
             �Գ��㷨����(��/����)��ʼ��������_ex��������Ӳ��enginge������
             EVP_EncryptInit��EVP_DecryptInit����Ҳ���ñ�������
        10)  EVP_CipherUpdate
             �ԳƼ��㣨��/���ܣ���������������EVP_EncryptUpdate��EVP_DecryptUpdate������
        11�� EVP_CipherFinal/EVP_CipherFinal_ex
             �ԳƼ���(��/��)������������EVP_EncryptFinal��_ex����EVP_DecryptFinal(_ex����
             ��������Ҫ�������������ܷ��飬���ܻ��жԳƼ��㡣
        -------------------------------------------------------------------------     
        12�� EVP_cleanup
             ������صĸ����㷨�������Գ��㷨��ժҪ�㷨�Լ�PBE�㷨���������Щ�㷨��صĹ�ϣ������ݡ�
        -------------------------------------------------------------------------     
        13)  EVP_get_cipherbyname
             �����ִ���������ȡһ�ֶԳ��㷨(EVP_CIPHER)����������ѯ�Գ��㷨��ϣ��
        14)  EVP_get_digestbyname
             �����ִ���ȡժҪ�㷨(EVP_MD)����������ѯժҪ�㷨��ϣ��
        -------------------------------------------------------------------------     
        15)  EVP_get_pw_prompt
             ��ȡ������ʾ��Ϣ�ַ���.
        -------------------------------------------------------------------------     
        16�� int EVP_PBE_CipherInit(ASN1_OBJECT *pbe_obj, const char *pass, int passlen,
                                    ASN1_TYPE *param, EVP_CIPHER_CTX *ctx, int en_de)
             PBE��ʼ���������������ÿ������ɶԳ��㷨����Կ�ͳ�ʼ��������������/���ܳ�ʼ��������
             �������ټ��Ϻ�����EVP_CipherUpdate�Լ�EVP_CipherFinal_ex����һ�������ļ��ܹ���
             ���ɲο�crypto/p12_decr.c��PKCS12_pbe_crypt������.
        17)  EVP_PBE_cleanup
             ɾ�����е�PBE��Ϣ���ͷ�ȫ�ֶ�ջ�е���Ϣ.
        -------------------------------------------------------------------------     
        18�� EVP_PKEY *EVP_PKCS82PKEY(PKCS8_PRIV_KEY_INFO *p8)
             ��PKCS8_PRIV_KEY_INFO(x509.h�ж���)�б����˽Կת��ΪEVP_PKEY�ṹ��
        19)  EVP_PKEY2PKCS8/EVP_PKEY2PKCS8_broken
             ��EVP_PKEY�ṹ�е�˽Կת��ΪPKCS8_PRIV_KEY_INFO���ݽṹ�洢��
        20)  EVP_PKEY_bits
             �ǶԳ���Կ��С��Ϊ��������
        21)  EVP_PKEY_cmp_parameters
             �ȽϷǶԳ���Կ����Կ����������DSA��ECC��Կ��
        22�� EVP_PKEY_copy_parameters
             �����ǶԳ���Կ����Կ����������DSA��ECC��Կ��
        23�� EVP_PKEY_free
             �ͷŷǶԳ���Կ���ݽṹ��
        24)  EVP_PKEY_get1_DH/EVP_PKEY_set1_DH
             ��ȡ/����EVP_PKEY�е�DH��Կ��
        25)  EVP_PKEY_get1_DSA/EVP_PKEY_set1_DSA
             ��ȡ/����EVP_PKEY�е�DSA��Կ��
        26�� EVP_PKEY_get1_RSA/EVP_PKEY_set1_RSA
             ��ȡ/����EVP_PKEY�нṹ�е�RSA�ṹ��Կ��
        27)  EVP_PKEY_missing_parameters
             ���ǶԳ���Կ�����Ƿ���ȫ������DSA��ECC��Կ��
        28)  EVP_PKEY_new
             ����һ��EVP_PKEY�ṹ��
        29)  EVP_PKEY_size
             ��ȡ�ǶԳ���Կ���ֽڴ�С��
        30)  EVP_PKEY_type
             ��ȡEVP_PKEY�б�ʾ�ķǶԳ���Կ�����͡�
        31)  int EVP_read_pw_string(char *buf,int length,const char *prompt,int verify)
             ��ȡ�û�����Ŀ��buf��������û�����Ŀ��lengthΪbuf���ȣ�
             promptΪ��ʾ���û�����Ϣ�����Ϊ�գ����������õ���ʾ��Ϣ��verifyΪ0ʱ��
             ��Ҫ����֤�û�����Ŀ�������Ҫ���û��������顣����0��ʾ�ɹ���
        32)  EVP_set_pw_prompt
             �������õ���ʾ��Ϣ��������Ҫ�û��������ĳ��ϡ�
    �ԳƼ��ܹ���
       �ԳƼ��ܹ������£�    
        1��  EVP_EncryptInit��
             ����buf_lenΪ0��������ʱ������bufû�����ݡ�
        2��  EVP_EncryptUpdate��
             ctx�ṹ�е�buf���������ڴ���ϴ�EVP_EncryptUpdate����������δ���ܵ����ݣ�buf_lenָ���䳤�ȡ�
             ���buf_lenΪ0�����ܵ�ʱ���ȼ����������ݵ��������������µ����ݿ�����buf��������
             ���buf_len��Ϊ0���ȼ���buf��������ݺ��������ݵ�һ���֣�����һ������ĳ��ȣ���
             Ȼ��������ķ������ܣ��������Ǽӹ��ܵ����ݡ�
        3��  EVP_EncryptFinal
             ����ctx��buf�����µ����ݣ�������Ȳ���һ�����飨���鳤�Ȳ�Ϊ1��������䣬Ȼ���ټ��ܣ���������
             ��֮�����ܴ�����ݣ�����һ������ļ����������EVP_EncryptUpdate��
             �Ľ����Ч�ڽ����е�����һ���Զ����ڴ���м��ܵĽ����
             ���ܺͽ���ʱÿ�μ�������ݿ�Ĵ�С��Ӱ������������
     ���ʾ��
        ��
            
�ڶ�ʮ���� PEM
    ����opensslĬ�ϲ��õ���Ϣ��ŷ�ʽ
    Openssl����PEM��ʽ�ļ��Ĵ��¹������£�
        1)    ����������DER���룻
        2)    ��1���е����ݽ��м��ܴ��������Ҫ����
        3)    ���������Լ��Ƿ���ܣ�����PEMͷ��
        4)    ��2���е����ݽ���BASE64���룬����PEM�ļ���
    openssl��PEMʵ��
        Openssl��PEMģ��ʵ��λ��crypto/pemĿ¼�£����һ�������openssl��ASN1ģ��
        Openssl֧�ֵ�PEM����(��crypto/pem/pem.h�ж���)���£�
            "X509 CERTIFICATE"
            "CERTIFICATE"
            "CERTIFICATE PAIR"
            "TRUSTED CERTIFICATE"
            "NEW CERTIFICATE REQUEST"
            "CERTIFICATE REQUEST"
            "X509 CRL"
            "ANY PRIVATE KEY"
            "PUBLIC KEY"
            "RSA PRIVATE KEY"
            "RSA PUBLIC KEY"
            "DSA PRIVATE KEY"
            "DSA PUBLIC KEY"
            "PKCS7"
            "ENCRYPTED PRIVATE KEY"
            "PRIVATE KEY"
            "DH PARAMETERS"
            "SSL SESSION PARAMETERS"
            "DSA PARAMETERS"
            "ECDSA PUBLIC KEY"
            "EC PARAMETERS"
            "EC PRIVATE KEY"
    PEM����
        1)  PEM_write_XXXX/PEM_write_bio_XXXX
            ��XXXX�������Ϣ����д�뵽�ļ�/bio�С�
        2)  PEM_read_XXXX/PEM_read_bio_XXXX
            ���ļ�/bio�ж�ȡPEM��XXXX�������͵���Ϣ��
            XXXX���ô�����У�
                SSL_SESSION��X509��X509_REQ��X509_AUX��X509_CRL��RSAPrivateKey��
                RSAPublicKey��DSAPrivateKey��PrivateKey��PKCS7��DHparams��
                NETSCAPE_CERT_SEQUENCE��PKCS8PrivateKey��DSAPrivateKey��
                DSA_PUBKEY��DSAparams��ECPKParameters��ECPrivateKey��EC_PUBKEY�ȡ�
        3)  PEM_ASN1_read/PEM_ASN1_read_bio
            �Ƚϵײ��PEM��ȡ������2���еĺ�����������������������
        4)  PEM_ASN1_write/PEM_ASN1_write_bio
            �Ƚϵײ��PEM��ȡ������1)�еĺ�����������������������
        5�� PEM_read_bio
            ��ȡPEM�ļ��ĸ������֣������ļ����͡�ͷ��Ϣ�Լ���Ϣ��(base64�����Ľ������
        6�� PEM_get_EVP_CIPHER_INFO
            ����ͷ��Ϣ��ȡ�Գ��㷨�������س�ʼ������iv��
        7)  PEM_do_header
            ���ݶԳ��㷨���������ݡ�
        8)  PEM_bytes_read_bio
            ��ȡPEM���ݣ��õ��Ľ��Ϊһ��DER������������ݣ��ú����Ⱥ������5)��6����7��������
        Openssl�������͵�PEM��������Ҫ��write��read������
        write������������PEM��ʽ���ļ�����read������Ҫ���ڶ�ȡPEM��ʽ���ļ���
    
�ڶ�ʮ���� ����
    OpensslӲ������(Engine���ܹ�ʹ�û��Ƚ����׵ؽ��Լ���Ӳ�����뵽openssl��ȥ���滻���ṩ������㷨��
    һ��Engine�ṩ����������и��ּ��㷽���ļ��ϣ������ڿ���openssl�ĸ���������㡣
    Engine֧�ֵ�ԭ��
        Openssl�е�������ݽṹ�����������ݱ������������ֲ�����������Щ�����ǿ��滻�ġ�
        Openssl����Щ�ṹ����һ�����XXX_METHOD����DSO_METHOD��DSA_METHOD��EC_METHOD��
        ECDH_METHOD��ECDSA_METHOD��DH_METHOD��RAND_METHOD�� RSA_METHOD��EVP_CIPHER��EVP_MD�ȡ�
        ��RSA�ṹΪ��(crypto/rsa/rsa.h)��RSA�ṹ���������˴���n��e��d��p�ȵ�������Ŀ��
        ������һ��RSA_METHOD�ص��������ϡ��÷���������RSA�������㺯����
        ���ڸ����������ͣ�Ҫ���м������������һ�����õķ���(XXX_METHOD)��
        ��ˣ�openssl�Ը������Ͷ��ṩ��Ĭ�ϵļ��㷽��(���㷨)��
        ����û�ʵ�����Լ���XXX_METHOD����ô�����滻openssl�ṩ�ķ��������ּ������û��Լ����ơ�
        Ӳ��Engine��������ԭ��
        ������Ҫ��һ��Ӳ��Engine��ʵ���Լ���RAND_METHOD��RSA_METHOD��EVP_CIPHER��
        DSA_METHOD��DH_METHOD��ECDH_METHOD��EVP_MD�ȣ����滻��Ӧ���㷨��METHOD��
    Engine���ݽṹ
        struct engine_st
        {
            const char *id;
            const char *name;
            const RSA_METHOD *rsa_meth;
            const DSA_METHOD *dsa_meth;
            const DH_METHOD *dh_meth;
            const ECDH_METHOD *ecdh_meth;
            const ECDSA_METHOD *ecdsa_meth;
            const RAND_METHOD *rand_meth;
            const STORE_METHOD *store_meth;
            ENGINE_CIPHERS_PTR ciphers;
            ENGINE_DIGESTS_PTR digests;
            ENGINE_GEN_INT_FUNC_PTRdestroy;
            ENGINE_GEN_INT_FUNC_PTR init;
            ENGINE_GEN_INT_FUNC_PTR finish;
            ENGINE_CTRL_FUNC_PTR ctrl;
            ENGINE_LOAD_KEY_PTR load_privkey;
            ENGINE_LOAD_KEY_PTR load_pubkey;
            /* ������ */
            int struct_ref;
            CRYPTO_EX_DATA ex_data;
            struct engine_st *prev;
            struct engine_st *next;
        };
        ���ṹ�������������㼯�Ϻ���(��������METHOD)���û���ʵ�֡������������£�
            id��         Engine��ʶ��
            name��       Engine�����֣�
            rsa_meth��   RSA�������ϣ�
            dsa_meth��   DSA�������ϣ�
            dh_meth��    DH�������ϣ�
            ecdh_meth��  ECDH������ϣ�
            ecdsa_meth�� ECDSA�������ϣ�
            rand_meth��  ������������ϣ�
            store_meth�� �洢�������ϣ�
            ciphers��    �Գ��㷨ѡȡ������Ӳ��һ���֧�ֶ��ֶԳ��㷨���ûص�����������
                         �û�ʵ�ֵĶ���Գ��㷨�и���ĳ������(һ�����㷨nid)��ѡ�����е�һ�֣�
            digests��    ժҪ�㷨ѡȡ�������ûص������������û�ʵ�ֵĶ��ժҪ�㷨��
                         ����ĳ������(һ�����㷨nid)��ѡ�����е�һ�֣�
            destroy��    �������溯����
            init��       ��ʼ�����溯����
            finish��     ��ɻص�������
            ctrl��       ���ƺ�����
            load_privkey������˽Կ������
            load_pubkey�����ع�Կ������
            struct_ref�� ���ü���
            ex_data��    ��չ���ݽṹ������������û����ݣ�
            prev/next��  ���ڹ���Engine����openssl�е�Ӳ��Engine���ܲ�ֹһ����
            ������Щ�������û�����Ӧ�õ�������ʵ�����е�һ�ֻ���֡�
    openssl ��EngineԴ��
        Openssl��EngineԴ���Ϊ���ࣺ
        1�� ����ʵ��
            ��crypto/engineĿ¼�£��������ʵ�֡�
            ��ͬʱ�ж��Ӳ��Engineʱ��openssl�ֱ�Ϊcipher�Գ��㷨(tb_cipher.c)��
            dh�㷨(tb_dh.c)��digestժҪ�㷨(tb_digest.c)��dsa�㷨(tb_dsa.c)��
            ecdh�㷨(tb_ecdh.c)��ecdsa�㷨(tb_ecdsa.c)��rand������㷨(tb_rand.c)��
            rsa�㷨(tb_rsa.c)�ʹ洢��ʽ(tb_store.c)ά��һ����ϣ��
            �����û�ʵ�ֵ�Ӳ��Engine��ע������Щȫ�ֵĹ�ϣ���С�
            ͬʱ���û�ʹ�õ�ʱ���ܹ�ָ�������㷨Ĭ�ϵ�Ӳ��Engine��
        2�� ����Ӳ��Engine
            Դ��λ��enginesĿ¼��ʵ����һЩӲ��Engine��
        3)  ����
            Դ��λ��demos/enginesĿ¼�£����û�ѧϰ�ο���
        4�� ��ɢ��������������ģ������֧��Engine
            ��������ģ�鶼֧��Engine�����ṩ��Engineʱ���������Engine�е��㷨��
    Engine����(�������塢ʵ�֡�ʹ�ø�����)
        ��Ҫ�������£�
        1)  ENGINE_add
            ��Engine����ȫ�ֵ������С�
        2)  ENGINE_by_id
            ����id����ȡEngine��
        3�� ENGINE_cleanup
            �������Engine���ݡ�
        4�� const EVP_CIPHER *ENGINE_get_cipher(ENGINE *e, int nid)
            ����ָ����Ӳ��Engine�Լ��Գ��㷨��nid����ȡEngineʵ�ֵĶ�Ӧ��     EVP_CIPHER�����ڶԳƼ��㡣
        5�� ENGINE_get_cipher_engine
            ���ݶԳ��㷨nid����ȡEngine��
        6�� ENGINE_get_ciphers/ENGINE_set_ciphers
            ��ȡ/����ָ��Engine�ĶԳ��㷨ѡȡ������ַ���ú������ڴ�Engine��ѡ��һ�ֶԳ��㷨��
        7)  ENGINE_get_ctrl_function
            ��ȡEngine�Ŀ��ƺ�����ַ��
        8�� const DH_METHOD *ENGINE_get_DH(const ENGINE *e)
            ��ȡEngine��DH_METHOD��
        9�� const EVP_MD *ENGINE_get_digest(ENGINE *e, int nid)
            ����Engine��ժҪ�㷨nid����ȡEngine��ʵ�ֵ�ժҪ����EVP_MD��
        10) ENGINE *ENGINE_get_digest_engine(int nid)
            ����ժҪ�㷨nid����ȡEngine��
        11��ENGINE_get_digests/ENGINE_set_digests
            ��ȡ/����ָ��Engine��ժҪ�㷨ѡȡ������ַ���ú������ڴ�Engine��ѡ��һ��ժҪ�㷨��
        12) const DSA_METHOD *ENGINE_get_DSA(const ENGINE *e)
            ��ȡEngine��DSA������
        13) int ENGINE_register_XXX(ENGINE *e)
            ע�ắ������ĳһ��Engine��ӵ���Ӧ�����Ĺ�ϣ���С�
        14) void ENGINE_unregister_XXX(ENGINE *e)
            ��ĳһ��Engine�Ӷ�Ӧ�Ĺ�ϣ����ɾ����
        15) void ENGINE_register_all_XXX(void)
            �����е�Engineע�ᵽ��Ӧ�����Ĺ�ϣ���С�
        16��ENGINE_set_default_XXXX
            ����ĳEngineΪ��ӦXXXX������Ĭ��Engine��
        17) ENGINE_get_default_XXXX
            ��ȡXXXX������Ĭ��Engine��
        18��ENGINE_load_XXXX
            ����ĳ��Engine��
        19) ENGINE_get_RAND/ENGINE_set_RAND
            ��ȡ/����Engine�������������
        20) ENGINE_get_RSA/ENGINE_set_RSA
            ��ȡ/����Engine��RSA������
        21) ENGINE_get_first/ENGINE_get_next/ENGINE_get_prev/ENGINE_get_last
            Engine�������������
        22��ENGINE_set_name/ENGINE_get_name
            ����/��ȡEngine���֡�
        23��ENGINE_set_id/ENGINE_get_id
            ����/��ȡEngine��id��
        24) int ENGINE_set_default(ENGINE *e, unsigned int flags)
            ����flags��e����Ϊ���ַ�����Ĭ��Engine��
        25) ENGINE_set_XXX_function
            ����Engine��XXX��Ӧ�ĺ�����
        26) ENGINE_get_XXX_function
            ��ȡEngine��XXX��Ӧ�ĺ�����
        27) ENGINE_ctrl
            Engine���ƺ�����
        28) ENGINE_get_ex_data/ENGINE_set_ex_data
            ��ȡ/����Engine����չ���ݡ�
        29��ENGINE_init/ENGINE_finish
            Engine��ʼ��/������
        30��ENGINE_up_ref
            ��Engine����һ�����á�
        31��ENGINE_new/ENGINE_free
            ����/�ͷ�һ��Engine���ݽṹ��
        32��ENGINE_register_complete
            ��������Engine������ÿ��������ע��һ�顣
        33��ENGINE_register_all_complete
            �����е�Engine������ÿ��������ע��һ�顣
    ʵ��Engineʾ��
        ���µ�ʾ����ʾ�˲���Engine���ƣ����ı�openssl�ĸ���������Ϊ��
        ʵ�ֵ�Engine�����У�������������Գ��㷨��ժҪ�㷨�Լ�RSA�����㷨��
        ���У�RSA�����У���ԿID�����Engine����չ���ݽṹ�С�
        file://Openssl����ʾ��.c
    �����д
        https://blog.csdn.net/cqwei1987/article/details/107423111
        OpenSSL�����Ϊ���ࣺ��̬���棬Version => 0.9.7����̬���棬0.9.7 <= Version < 1.1.0
        ���½����Զ�̬EngineΪ��
        1. AES����
            Openssl����õ����ӿ�
            1. AES����
                Openssl����õ����ӿ�
                IMPLEMENT_DYNAMIC_BIND_FN(bind)
                IMPLEMENT_DYNAMIC_CHECK_FN()
                ֻ���Զ���bind�������ɣ���bind�����Ķ���������ʾ��
                Static int bind(ENGINE *e)
                {
                    available();                            //�Զ��庯��������һЩӲ��ʵ��ʱ���Ӳ���Ƿ�֧�֣���ѡ
                    ENGINE_set_id(e,id);                    //����ENGINE��Ψһ��ID
                    ENGINE_set_name(e,name);                //����ENGINE��ʶ������
                    ENGINE_set_init_function(e,init_func);  //�ӽ����㷨�ĳ�ʼ�����������ݿ�Ϊ��
                    ENGINE_set_cipher(e,cipher_func);       //�ӽ����㷨����ʵʵ��
                }
                ���Է���������Ϊ��Ҫ����cipher_func�������䶨��������ʾ��
                static int cipher_func(ENGINE *e, const EVP_CIPHER **cipher, const int **nids, int nid){}
                ���У�EVP_CIPHER�Ķ�������ͼ��ʾ��do_cipher �������㷨���̵�����ʵ�ֹ��̡�
                file://imgs/EVP_CIPHER�Ķ���.png
                ���Է�����
                openssl enc -aes-128-ecb -nopad -in plain -out cipher -e 
                            -K 0123456789ABCDEFFEDCBA9876543210 -engine `pwd`/SM4.so
    ��д OpenSSL Engine
        https://blog.csdn.net/enlaihe/article/details/110474705
        ���˹����㷨��ʵ��Ӧ���п����й����㷨������
        ���粿��Ӧ������Ҫʹ�ù����׼�SM2-WITH-SMS4-SM3����TLS���ӡ�
        ���Ľ�ʹ��GmSSL��������ʵ�֡�
        ���ĵ�ʾ������ɲο� gmssl_engine
        OpenSSL�ṩ���������Demo����д����ʱ����ͨ��ENGINE_set_xxx�ӿ�������������Ϣ���ӿڵ����ã�
        static int bind_gmssl_engine(ENGINE *e, const char *id)
        {
            int ret = 1;
            gmssl_engine_create_ciphers();
            ret &= ENGINE_set_id(e, engine_id);
            ret &= ENGINE_set_name(e, engine_name);
            ret &= ENGINE_set_ciphers(e, gmssl_engine_ciphers);
            ret &= ENGINE_set_pkey_meths(e, gmssl_engine_pkey);
            ret &= ENGINE_set_destroy_function(e, engine_destroy);
            ret &= ENGINE_set_init_function(e, engine_init);
            ret &= ENGINE_set_finish_function(e, engine_finish);
            ret &= ENGINE_set_ctrl_function(e, engine_ctrl);
            ret &= ENGINE_set_cmd_defns(e, cmd_defns);
            _assert(ret != 0, ret);
            return ret;
        }
        ͨ��IMPLEMENT_DYNAMIC_BIND_FN�궨����������ע�᣺
        IMPLEMENT_DYNAMIC_BIND_FN(bind_gmssl_engine)
        IMPLEMENT_DYNAMIC_CHECK_FN()
        ����ֻ��Ҫʵ��������ע�����ؽӿڼ��ɣ�
        ����ǰ��ͨ�� ENGINE_set_pkey_meths �ӿ����õ� gmssl_engine_pkey �ӿڡ�
        ��Pkey�ӿ�Ϊ����ͨ�� EVP_PKEY_meth_set_xxx �ӿ����PKEY������ע�ᡣ
        ����Ҳ����ͨ��PKEY���ӷ������ע�ᣬ
        ����ECC��ص�EC_KEY_METHOD��OpenSSL speed�ٶȲ�����ֱ�ӵ����ַ�����ɣ�
        �����ĺô��ǿ���ʹ��speed����������ܲ��ԣ�
        ��PKEY�ӿڸ���ͨ�ã�����Կ�㷨ȫ���������ڣ�
        ĿǰGmSSL֧�ֵĹ�Կ�㷨���NID���£�
        # define EVP_PKEY_NONE       NID_undef
        # define EVP_PKEY_RSA        NID_rsaEncryption
        # define EVP_PKEY_RSA2       NID_rsa
        # define EVP_PKEY_DSA        NID_dsa
        # define EVP_PKEY_DSA1       NID_dsa_2
        # define EVP_PKEY_DSA2       NID_dsaWithSHA
        # define EVP_PKEY_DSA3       NID_dsaWithSHA1
        # define EVP_PKEY_DSA4       NID_dsaWithSHA1_2
        # define EVP_PKEY_DH         NID_dhKeyAgreement
        # define EVP_PKEY_DHX        NID_dhpublicnumber
        # define EVP_PKEY_EC         NID_X9_62_id_ecPublicKey
        # define EVP_PKEY_HMAC       NID_hmac
        # define EVP_PKEY_CMAC       NID_cmac
        # define EVP_PKEY_TLS1_PRF   NID_tls1_prf
        # define EVP_PKEY_HKDF       NID_hkdf
        # define EVP_PKEY_PAILLIER   NID_paillier
        # define EVP_PKEY_SM9_MASTER NID_id_sm9MasterSecret
        # define EVP_PKEY_SM9        NID_id_sm9PublicKey
        OpenSSL��֧���첽ģʽ����������Ҫ����ASYNC_xxx��ؽӿ���ɹ����Լ����Ѳ�����
        ���첽ģʽ�����У�����ͨ��ASYNC_start_job�ӿڴ����첽Job��
        ������ؼ��ٽӿ��н�����ж�ص�Ӳ����ͨ��ASYNC_get_wait_ctx�ӿڵõ���ǰ�첽job��
        ��ͨ��ASYNC_WAIT_CTX_get_fd�ӿڵõ��첽�����ͨ����ȡ�첽����ķ�ʽ���������
        ��Ӳ��������ɺ�ͨ���ص������������Ѽ���ִ�У��ù��̺ͽ����������������ƣ�
        ͨ��д�첽����ķ�ʽ�����﻽�ѡ�����ʾ��������û��ʹ��Ӳ���豸��
        �첽ģʽû�н�����ӣ�����ʵ��Ӧ����ȷ�ǳ���Ҫ��
    ����ENGINE�滻OPENSSL�еļӽ����㷨
        https://blog.csdn.net/bytxl/article/details/39498769
        һ��ENGINE��Ŀ�ģ�
            ���Ҫʹ��Engine���������Ѿ������ϸ�Engine�ˣ�����ô����ҪLoad��Engine(����ENGINE_load_XXXX)��
            Ȼ��ѡ��Ҫʹ�õ��㷨����ʹ��֧�ֵ����м����㷨������غ�������
            �������Ӧ�ó����ڵ��üӽ����㷨ʱ�����ͻ�ָ������صĶ�̬����ļӽ����㷨��
            ������ԭ�ȵ�OPENSSL��libeay32.dll����ļӽ����㷨��
        ����ENGINEԭ��
            ʹ�����Լ�����ļӽ��ܶ�̬����ĺ�����ָ���Ӳ���ӿ�ָ�����滻OPENSSL��Ĭ�ϵļӽ��ܺ���
        ����ENGINE�������̣�
            �����滻RSA��
            1 ������Ҫ�滻�ĺ������ƺ������ڲ�ʹ�õĺ���
            2 ����RSA_Method�ṹ��Ҫ�滻�ĺ������ṩ�����������ỻ����NULL�ˣ���������������ҲҪ���ϣ�
            3 ����Engine_init��һϵ�к�����ʼ��ENGINE�⣨��ʵ�Ͼ����ڳ�ʼ���ӽ����㷨����
              ��Ҫ�ǰ��ض��ĺ���ָ�루�Զ��壩�ͽṹ���ʼ��Ӳ���豸�ȵȲ�����
              Engine_finishҲ��һ������һЩ��������
            4 ʵ�������Ľӿڣ�����RSA��Կ�ṹ��ת��������ǲ���ȡ����˽Կ��
              Ҫ����Ӳ���豸�ṩ��ָ�루ͨ����HANDLE���ȵȲ�����Ȼ�����Ӳ���ļ��ܽ��ܺ�����
        �ģ�����ʵ������ʵ��ENGINE��
        
����ʮһ�� SSLʵ��
    ����
        SSLЭ��������netscape��˾���������sslv2��sslv3�����汾
        ��ǰ�γɱ�׼��ΪtlsЭ�飨rfc2246�淶����DTLSЭ�飨rfc4347������֧��UDPЭ�飩��
        sslv3��tlsЭ�����һ����ֻ����һЩϸ΢�Ĳ��ʵ��Ӧ���У��õ�����Ϊsslv3��
        SSLЭ���ܹ���֤ͨ��˫�����ŵ���ȫ��
        �����ṩ���ݼ��ܡ������֤�Լ���Ϣ�����Ա���������SSLЭ�黹֧������ѹ����
        SSLЭ��ͨ���ͻ��˺ͷ����������Э�̸����㷨����Կ��
    openssl��sslЭ���ʵ��
        SSLЭ��Դ��λ��sslĿ¼�¡���ʵ����sslv2��sslv3��TLS�Լ�DTLS��Datagram TLS������UDP��TLSʵ�֣�
        sslʵ���У�����ÿ��Э�飬���пͻ���ʵ��(XXX_clnt.c)�������ʵ��(XXX_srvr.c)��
        ����ʵ��(XXX_enc.c)����¼Э��ʵ��(XXX_pkt.c)��METHOD����(XXX_meth.c)��
        �ͻ��˷���˶��õ������ַ���ʵ��(XXX_both.c)���Լ������ṩ�ĺ���ʵ��(XXX_lib.c)��
    �ssl���Ի���
        ��
    ���ݽṹ
        ssl����Ҫ���ݽṹ������ssl.h�С�
        ��Ҫ�����ݽṹ��SSL_CTX��SSL��SSL_SESSION��
        SSL_CTX ���ݽṹ��Ҫ����SSL����ǰ�Ļ���׼��������CA�ļ���Ŀ¼��
        ����SSL�����е�֤���ļ���˽Կ������Э��汾�Լ�����һЩSSL����ʱ��ѡ�
        SSL ���ݽṹ��Ҫ����SSL�����Լ�����Ӧ�����ݡ�
        SSL_SESSION�б���������Կ��session id����д�ӽ���Կ����дMAC��Կ����Ϣ��
        SSL_CTX�л���������SSL_SESSION��Ϣ��SSL�а���SSL_CTX��
        һ��SSL_CTX�ĳ�ʼ���ڳ����ʼ���ã�Ȼ��������SSL���ݽṹ��
        ����SSL_CTX�л��������е�SESSION�������ɵ�SSL�ṹ�ְ���SSL_CTX���ݣ�
        ����ͨ��SSL���ݽṹ�ܲ�����ǰ�ù���SESSION id��ʵ��SESSION���á�
        ���⣬SSL_METHOD���Ǹ�������һϵ��ssl����ָ��Ľṹ��
        SSL_CIPHER����ά�������㷨�������Ϣ
        typedef struct ssl_cipher_st
        {
            int valid;
            const char *name;		/* text name */
            unsigned long id;		/* id, 4 bytes, first is version */
            /* changed in 0.9.9: these four used to be portions of a single value 'algorithms' */
            unsigned long algorithm_mkey;	/* key exchange algorithm */
            unsigned long algorithm_auth;	/* server authentication */
            unsigned long algorithm_enc;	/* symmetric encryption */
            unsigned long algorithm_mac;	/* symmetric authentication */
            unsigned long algorithm_ssl;	/* (major) protocol version */
            unsigned long algo_strength;	/* strength and export flags */
            unsigned long algorithm2;	/* Extra flags */
            int strength_bits;		/* Number of bits really used */
            int alg_bits;			/* Number of bits for algorithm */
        } SSL_CIPHER;
    �����׼�
        һ�������׼�ָ����SSL���ֽ׶κ�ͨ�Ž׶���Ӧ�ò��õĸ����㷨��
        ��Щ�㷨��������֤�㷨����Կ�����㷨���Գ��㷨��ժҪ�㷨�ȡ�
        �����ֳ�ʼ����ʱ��˫�����ᵼ��������ϿɵĶ��ּ����׼���
        �����ֽ׶Σ��ɷ����ѡ�����е�һ�ּ����׼���
        OpenSSL��ciphers��������г����еļ����׼�
        openssl�ļ����׼���s3_lib.c��ssl3_ciphers�����ж���
        �����У�
            {
                1,
                SSL3_TXT_RSA_RC4_128_SHA,
                SSL3_CK_RSA_RC4_128_SHA,
                SSL_kRSA|SSL_aRSA|SSL_RC4  |SSL_SHA1|SSL_SSLV3,
                SSL_NOT_EXP|SSL_MEDIUM,
                0,
                128,
                128,
                SSL_ALL_CIPHERS,
                SSL_ALL_STRENGTHS,
            }
            ����1��ʾ�ǺϷ��ļ����׼���
            SSL3_TXT_RSA_RC4_128_SHAΪ�����׼������֣�
            SSL3_CK_RSA_RC4_128_SHAΪ�����׼�ID��
            SSL_kRSA|SSL_aRSA|SSL_RC4|SSL_SHA1|SSL_SSLV3�����˸����㷨��
            ������Կ��������RSA�㷨��SSL_kRSA����
            ��֤����RSA�㷨��SSL_aRSA����
            �ԳƼ����㷨����RC4�㷨(SSL_RC4)��
            ժҪ����SHA1��
            ����SSLЭ������汾��
            SSL_NOT_EXP|SSL_MEDIUM�����㷨��ǿ�ȡ�
        �ڿͻ��˺ͷ������˽�����ȫ����֮ǰ��˫��������ָ���ʺ��Լ��ļ����׼���
        �����׼���ѡ�����ͨ����ϵ��ַ��������ơ�
        �ַ�������ʽ������ALL:!ADH:RC4+RSA:+SSLv2:@STRENGTH��
        Openssl������4��ѡ����ţ���������������������������@����
        ���У���������ʾȡ��������������ʾ��ʱɾ��һ���㷨����������ʾ����ɾ��һ���㷨����@����ʾ�����򷽷���
        �������֮������á����� �� ������ �� �� �� �� ���������ֿ���
        ѡ������׼���ʱ���մ��󵽵�˳�򹹳�˫������������ڴ���
        ������ʾ����˼�ǣ�
            ����ѡ�����еļ����׼���������eNULL�����նԳƼ����㷨����
            Ȼ���ڵõ���˫������֮��ȥ�������֤����DH�ļ����׼���
            ������RC4�㷨�Ұ���RSA�㷨�ļ����׼�����˫�������β����
            �ٽ�֧��SSLV2�ļ����׼�����β����
            ���õ��Ľ�����հ�ȫǿ�Ƚ�������
        SSL��������֮ǰ���ͻ��˺ͷ���������openssl�����������Լ�֧�ֵļ����׼�����Ҫ�ĺ����У�
        int SSL_set_cipher_list(SSL *s,const char *str)��
        int SSL_CTX_set_cipher_list(SSL_CTX *ctx, const char *str)��
        ��������ֻ������һ�ּ����׼�����ô�ͻ���Ҫô����Ҫô���ش���
        �����׼���ѡ�����ɷ���������ġ�
    ��Կ��Ϣ
        ssl�е���Կ�����Ϣ������Ԥ����Կ������Կ����������Կ����iv��д������Կ����iv����MAC��Կ��дMAC��Կ��
        1)  Ԥ����Կ
            Ԥ����Կ������Կ�ļ�����Դ�����ɿͻ������ɣ����÷���˵Ĺ�Կ���ܷ��͸�����ˡ�
            ��sslv3Ϊ����Ԥ����Կ��������Դ���� s3_clnt.c �� ssl3_send_client_key_exchange �����У�
            ��Դ�����£�
                tmp_buf[0] = s->client_version>>8;
                tmp_buf[1] = s->client_version&0xff;
                if (RAND_bytes(&(tmp_buf[2]),sizeof tmp_buf-2) <= 0)
                    goto err;
                s->session->master_key_length = sizeof tmp_buf;
                ����
                n=RSA_public_encrypt(sizeof tmp_buf,tmp_buf,p,rsa,RSA_PKCS1_PADDING);
                �˴���tmp_buf�д�ŵľ���Ԥ����Կ��
        2)  ����Կ
            ����Կ�ֱ��ɿͻ��˺ͷ���˸���Ԥ����Կ���ͻ���������ͷ��������������ɣ����ǵ�����Կ����ͬ�ġ�
            ����Կ�������ɸ�����Կ��Ϣ���������SESSION���ݽṹ�С�����Э��汾��ͬ�����ɷ�ʽҲ��ͬ��
            sslv3��Դ�����У���ͨ��ssl3_generate_master_secret�������ɣ�
            tlsv1����ͨ��tls1_generate_master_secret���������ɡ�
        3)  �Գ���Կ��MAC��Կ
            �Գ���Կ������IV���Ͷ�дMAC��Կͨ������Կ���ͻ���������ͷ��������������ɡ�
            sslv3Դ�����У�������ssl3_generate_key_block�����ɣ���ssl3_change_cipher_state�з��䡣
    SESSION
        ���ͻ��˺ͷ�������������½���session��
        ���������һ��session ID��ͨ����ϣ����SESSION��Ϣ����ͨ��server hello��Ϣ���͸��ͻ��ˡ�
        ��ID��һ���������SSL v2�汾ʱ����Ϊ16�ֽڣ�SSLv3��TLSv1����Ϊ32�ֽڡ�
        ��ID�밲ȫ�޹أ������ڷ���˱�����Ψһ�ġ�
        ����Ҫsession����ʱ���ͻ��˷��Ͱ���session id��clientHello��Ϣ����sesion����ʱ����ֵΪ�գ�������ˣ�
        ����˿��ø��ݴ�ID����ѯ���档
        session���ÿ�����ȥ���SSL���ֽ������ر��ǿͻ��˵Ĺ�Կ���ܺͷ���˵�˽Կ���������������ܿ�����
        session��Ĭ�ϳ�ʱʱ��Ϊ60*5+4�룬5���ӡ�
        session��غ����У�
            1) int SSL_has_matching_session_id(const SSL *ssl, const unsigned char *  id,unsigned int id_len)
                SSL�в�ѯsession id��id�� id_lenΪ�����Ҫ��ѯ��session id��
                ��ѯ��ϣ��ssl->ctx->sessions�����ƥ�䣬����1�����򷵻�0��
            2��int ssl_get_new_session(SSL *s, int session)
                ����ssl�õ�session���˺������ñ�����˻�ͻ��˵��ã�
                ������˵���ʱ���������sessionΪ1�������µ�session��
                ���ͻ��˵���ʱ���������sessionΪ0��ֻ�Ǽ򵥵Ľ�session id�ĳ�����Ϊ0��
            3) int ssl_get_prev_session(SSL *s, unsigned char *session_id, int len)
                ��ȡ��ǰ�ù���session id�����ڷ����session���ã�
                �������ɷ���˵��ã�session_idΪ����senssion ID�׵�ַ��lenΪ�䳤�ȣ�
                �������1������Ҫsession���ã�����0����ʾû���ҵ�������-1��ʾ����
            4) int SSL_set_session(SSL *s, SSL_SESSION *session)
                ����session�����������ڿͻ��ˣ���������session��Ϣ��
                ����������sessionΪ��ֵ�������ÿ�s->session��
                �����Ϊ�գ�����������Ϣ��Ϊsession��Ϣ��
            5) void SSL_CTX_flush_sessions(SSL_CTX *s, long t)
                �����ʱ��SESSION���������tָ��һ��ʱ�䣬
                ���t=0,���������SESSION��һ����time(NULL)ȡ��ǰʱ�䡣
                �˺��������˹�ϣ����lh_doall_arg������ÿһ��SESSION���ݡ�
            6) int ssl_clear_bad_session(SSL *s)
                �����ЧSESSION��
    ���߳�֧��
        ��дopenssl���̳߳���ʱ����Ҫ���������ص�������
        CRYPTO_set_id_callback((unsigned long (*)())pthreads_thread_id);
            ���ڼ�¼��ǰ����ִ���̵߳�id
            ����ʵ�ֲ�Ӧֱ�����id��������Ӧ��
        CRYPTO_set_locking_callback((void (*)())pthreads_locking_callback);
            ������ɶԹ������ݽṹ��������
            �ú�����������������CRYPTO_num_locks()��������
        ���ڶ��̳߳����д�������߿��Բο�crypto/threads/mttest.c
    ����
        1�� SSL_accept
            ��Ӧ��socket����accept���ú����ڷ���˵��ã���������SSL���֡�
        2�� int SSL_add_client_CA(SSL *ssl,X509 *x)
            ��ӿͻ���CA����
        3�� const char *SSL_alert_desc_string_long(int value)
            ���ݴ���ŵõ�����ԭ��
        4�� SSL_check_private_key
            ���SSL�ṹ�е�˽Կ��
        5�� SSL_CIPHER_description
            ��ȡSSL�����׼�������
        6�� SSL_CIPHER_get_bits
            ��ȡ�����׼��жԳ��㷨�ļ��ܳ��ȡ�
        7�� SSL_CIPHER_get_name
            �õ������׼������֡�
        8�� SSL_CIPHER_get_version
            ���ݼ����׼���ȡSSLЭ��汾��
        9�� SSL_clear
            ���SSL�ṹ��
        10) SSL_connect
            ��Ӧ��socket����connect���ú����ڿͻ��˵��ã���������SSL���֡�
        11) SSL_CTX_add_client_CA
            ��SSL_CTX��ӿͻ���CA��
        12) int SSL_CTX_add_session(SSL_CTX *ctx, SSL_SESSION *c)
            ��SSL_CTX���session��
        13) SSL_CTX_check_private_key
            ���˽Կ��
        14) SSL_CTX_free
            �ͷ�SSL_CTX�ռ䡣
        15) long SSL_CTX_get_timeout(const SSL_CTX *s)
            ��ȡ��ʱʱ�䡣
        16) SSL_CTX_get_verify_callback
            ��ȡ֤����֤�ص�������
        17) SSL_CTX_get_verify_depth
            ��ȡ֤����֤��ȡ�
        18��SSL_CTX_get_verify_mode
            ��ȡ��֤��ʽ����Щֵ��ssl.h�ж������£�
            #define SSL_VERIFY_NONE                 0x00
            #define SSL_VERIFY_PEER                 0x01
            #define SSL_VERIFY_FAIL_IF_NO_PEER_CERT 0x02
            #define SSL_VERIFY_CLIENT_ONCE          0x04
        19��SSL_get_current_cipher
            ��ȡ��ǰ�ļ����׼���
        20��SSL_get_fd
            ��ȡ���Ӿ����
        21��SSL_get_peer_certificate
            ��ȡ�Է�֤�顣
        22��XXX_client/server_method
            ��ȡ�����汾�Ŀͻ��˺ͷ���˵�SSL������
        23��SSL_read
            ��ȡ���ݡ�
        24) SSL_write
            �������ݡ�
        25��SSL_set_fd
            ����SSL�����Ӿ����
        26��SSL_get_current_compression
            ��ȡ��ǰ��ѹ���㷨��COMP_METHOD��
        27��SSL_get_current_expansion
            ��ȡ��ǰ�Ľ�ѹ�㷨��COMP_METHOD��
        28��SSL_COMP_get_name
            ��ȡѹ��/��ѹ�㷨�����ơ�
        29��SSL_CTX_set/get_ex_data
            ����/��ȡ�û���չ���ݡ�
        30��SSL_dup
            ���ƺ�����
        31��SSL_get_default_timeout
            ��ȡĬ�ϳ�ʱʱ�䡣
        32��SSL_do_handshake
            ����ssl���֡�
    ʾ��
        file://ssl_server.cpp | file://ssl_client.cpp
        
����ʮ���� OpenSSL����
    asn1parse   ��һ���������ASN.1�ṹ�Ĺ��ߣ�Ҳ�����ڴ�ASN1.1��������ȡ����
    dgst        ��������ժҪ
    gendh       ��������������DH������
    passwd      ���ɸ��ֿ�������
    rand        ���������   
    genrsa      ����RSA��Կ
    req         ��Ҫ�������ɺʹ���PKCS#10֤������
    x509        ��һ������;��֤�鹤�ߡ���������ʾ֤����Ϣ��ת��֤���ʽ��ǩ��֤�������Լ��ı�֤����������õȡ�
    version     ӡ�汾�Լ�openssl����������Ϣ
    speed       ���ڲ��Կ������
    sess_id     SSL/TLSЭ���session�����ߡ�
    s_server    openssl�ṩ��һ��SSL�������ʹ�ô˳���ǰ����Ҫ���ɸ���֤��; 
                �����������������ssl�ͻ��ˣ���������������httpsЭ��֧��
    s_client    һ��SSL/TLS�ͻ��˳�����s_server��Ӧ��
                ����������s_server����ͨ�ţ�Ҳ�����κ�ʹ��sslЭ�����������������ͨ�š�
    rsa         ���ڴ���RSA��Կ����ʽת���ʹ�ӡ��Ϣ
    pkcs7       ���ڴ���DER����PEM��ʽ��pkcs#7�ļ�
    dsaparam    �������ɺͲ���dsa����
    gendsa      ����DSA��Կ��������DSA��Կ��dsa��Կ��������dsaparam��������
    enc         �ԳƼӽ��ܹ��ߣ������Խ���base64����ת��
    ciphers     ��ʾ֧�ֵļ����׼�
    CA          ��һ��С��CAϵͳ������ǩ��֤�����������CRL����ά��һ����ǩ��֤��״̬���ı����ݿ⡣
    verify      ֤����֤����
    rsatul      ��ָ���ܹ�ʹ��RSA�㷨ǩ������֤��ݣ� ����/��������
    crl         ���ڴ���PME��DER��ʽ��CRL�ļ�
    crl2pkcs7   ����CRL��֤��������pkcs#7��Ϣ
    errstr      ���ڲ�ѯ�������
    ocsp        ����֤��״̬����
    pkcs12      pkcs12�ļ����ߣ������ɺͷ���pkcs12�ļ�
    pkcs8       pkcs8��ʽ��˽Կת�����ߡ�
    s_time      SSL/TLS���ܲ��Թ��ߣ����ڲ���SSL/TSL����
    dhparam��dh ��
    ecparam     ��Բ������Կ�������ɼ�����
    ec          ��Բ������Կ������
    dsa         ����DSA��Կ����ʽת���ʹ�ӡ��Ϣ
    nseq        ���ڶ��֤����netscape֤�����м��໥ת��
    prime       ���һ�����Ƿ�Ϊ����
    smime       ���ڴ���S/MIME�ʼ������ܼ��ܡ����ܡ�ǩ������֤S/MIME��Ϣ
    ע������ֻ�����˸�����ļ�飬����ʹ�ò�chm�ļ�
        
OpenSSL���汾����        
    OpenSSL�汾	�ٷ�֧�����
    0.9.8 ϵ��	����֧��
    1.0.0 ϵ��	����֧��
    1.0.1 ϵ��	����֧��
    1.0.2 ϵ��	����֧�ֵ� 2019 �� 12 �� 31 ��
    1.1.0 ϵ��	ֻ����ȫ�޸����� 2019 �� 9 �� 11 ��ֹ֧ͣ��
    1.1.1 ϵ��	����֧�ֵ� 2023 �� 9 �� 11 ��
    �Աȣ�
        1�� 1.0.1 �� 1.0.2 ������ϵ��֮��仯��Խ�С���󲿷ֺ����ӿڿ�ͨ��
        2�� 1.0.x �� 1.1.1 ������ϵ��֮��仯�Ƚϴ󣬺ܶ��� 1.0.x ϵ�����ṩ�ĺ����ӿ�
            �� 1.1.1 ϵ�����ѱ�ɾȥ��ת��Ϊ�ڲ��ӿڣ����ٶ����ṩ��
        3�� ���� 2019 �� 5�£��� 1.1.1 ϵ���а��� pre1 �� pre9 �� 9 ��Ԥ���桢1.1.1 ��ʽ�棬
            1.1.1a �� 1.1.1c ��������棬�ܹ��� 13 ���汾��
            1.1.1 ϵ���Ǵ� 2018 �� 2 �¿�ʼ�����ģ�������һֱ����������
            Ԥ���桢��ʽ�桢�����֮����һ�����졣
    �������˵��һЩ��ͬ�汾֮��Ĳ��죺
        a�� 1.0.2d vs. 1.1.1
            �� 1.0.2d �汾�п��Ե��õ�һЩ�� ASN.1 �����йصĵײ㺯����
            ���磺M_i2d_ASN1_OCTET_STRING( )��M_ASN1_BIT_STRING_free( ) �ȡ�
            �� 1.1.1 ϵ���У���Щ�� M_ ��ͷ�� ASN.1 ���뺯������ɾȥ�ˡ�
        b�� 1.1.1-pre6 vs. 1.1.1
            �� 1.1.1-pre6 ���У�sm2.h �ļ����ڵ�·���� include/openssl��
            �� 1.1.1 ���У�sm2.h �ļ����ڵ�Ŀ¼�� include/internal ��
            �� 1.1.1-pre6 ��� sm2.h �У�SM2 ǩ������ǩ�������������£�
               int SM2_sign(int type, const unsigned char *dgst, int dgstlen,
                            unsigned char *sig, unsigned int *siglen, EC_KEY *eckey);
               int SM2_verify(int type, const unsigned char *dgst, int dgstlen,
                              const unsigned char *sig, int siglen, EC_KEY *eckey);
            �� 1.1.1 ��� sm2.h �У�SM2 ǩ������ǩ�������������£�
                int sm2_sign(const unsigned char *dgst, int dgstlen,
                             unsigned char *sig, unsigned int *siglen, EC_KEY *eckey);
                int sm2_verify(const unsigned char *dgst, int dgstlen,
                               const unsigned char *sig, int siglen, EC_KEY *eckey);
            �� 1.1.1-pre6 ��� sm2.h �У�SM2���ܺͽ��ܺ����������£�
                int SM2_encrypt(const EC_KEY *key,
                                const EVP_MD *digest,
                                const uint8_t *msg,
                                size_t msg_len,
                                uint8_t *ciphertext_buf, size_t *ciphertext_len);
                int SM2_decrypt(const EC_KEY *key,
                                const EVP_MD *digest,
                                const uint8_t *ciphertext,
                                size_t ciphertext_len, uint8_t *ptext_buf, size_t *ptext_len);
            �� 1.1.1 ��� sm2.h �У�SM2���ܺͽ��ܺ����������£�           
                int sm2_encrypt(const EC_KEY *key,
                                const EVP_MD *digest,
                                const uint8_t *msg,
                                size_t msg_len,
                                uint8_t *ciphertext_buf, size_t *ciphertext_len);
                int sm2_decrypt(const EC_KEY *key,
                                const EVP_MD *digest,
                                const uint8_t *ciphertext,
                                size_t ciphertext_len, uint8_t *ptext_buf, size_t *ptext_len);
            ͨ���Աȿ��Կ������� 1.1.1 ��� SM2 ǩ������ǩ�����У�ɾ����һ����Ϊ type �Ĳ�����
            �������� 1.1.1-pre6 �еĶ�Ӧ�������ڴ�Сдƴд���в��
            1.1.1 ��� SM2 ���ܺͽ��ܺ������� 1.1.1-pre6 ���еĶ�Ӧ������ȣ�
            �亯�����ڴ�Сдƴд���в��
        c�� �� 1.1.1 ���� 1.1.1c ��֮��Ҳ�в��
            ������ 1.1.1 �� ecdh_kdf.c ��ʵ����һ����Ϊ ECDH_KDF_X9_62( ) �ĺ�����
            �� 1.1.1c �� ecdh_kdf.c �У������˶�һ����Ϊ ecdh_KDF_X9_63( ) ������ʵ�֣�
            �������������� internal/ec_int.h �С�
            ECDH_KDF_X9_62( ) ��Ȼ���ڣ�������ʵ�ֹ������£�
            int ECDH_KDF_X9_62(unsigned char *out, size_t outlen,
                               const unsigned char *Z, size_t Zlen,
                               const unsigned char *sinfo, size_t sinfolen,
                               const EVP_MD *md)
            {
                return ecdh_KDF_X9_63(out, outlen, Z, Zlen, sinfo, sinfolen, md);
            }
            ���Կ��� ECDH_KDF_X9_62( ) �� ecdh_KDF_X9_63( ) ����������ʵ�ֵĹ�������ȫ��ͬ�ģ�
            �� 1.1.1c ���н�����ǰ�汾��Ժ��� ECDH_KDF_X9_62( ) �ĵ��ã�
            ����Ϊ���������� ecdh_KDF_X9_63( ) �ĵ��á�
    ������ʹ�� OpenSSL ʱ��һ��Ҫ���Ĳ�ͬ�汾֮��Ĳ��죬
    ���ֲ�����ܸ����е�Ӧ�ó�����������ݵ����⡣
    �ڱ��ʱӦ����ѡ����ڷ����� OpenSSL ϵ���е��ȶ��汾��
    
    OpenSSL 1.1.1 ������: ȫ��֧�ֹ���SM2/SM3/SM4�����㷨
        https://blog.csdn.net/bruce135lee/article/details/81811403
        
openssl���ע������
    ���� EVP_CIPHER_CTX ctx; ����
        ԭ�� 
            typedef struct evp_cipher_ctx_st EVP_CIPHER_CTX; 
            û�� evp_cipher_ctx_st �ṹ�Ķ���
        ���ԣ�
            ���Զ���lib��
                ����ṹ�� struct aaa;
                ���庯��  struct aaa* geta(); void seta(struct aaa* pa);
            ���������ж��� typedef struct aaa AAA;
            ����main������ AAA aaa; ͬ����������ԭ���������һ��
            ��Ϊ�� AAA *a; a = geta(); seta(a); �ɹ�
            ��Ϊ�� struct aaa *a; a = geta(); seta(a); ͬ���ɹ�
         ԭ��
            c/c++֧��ʹ��typedef���ⲿδ֪�ṹ��������
            �������Խ��ⲿδ֪�ṹ����Ϊʵ������ֻ�ܶ���Ϊָ�룬
            ���е�������ֻ��class A�������࣬���Զ���ָ�룬���ܶ���ʵ��һ��
            
        
                           