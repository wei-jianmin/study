openssl版本：0.9.8e
file://openssl.chm
openssl源代码
    openssl源代码主要由eay库、ssl库、工具源码、范例源码以及测试源码组成。
    eay库是基础的库函数，提供了很多功能。源代码放在crypto目录下。包括如下内容：
    1）  asn.1 DER编码解码(crypto/asn1目录)，它包含了基本asn1对象的编解码以及数字证书请求、
         数字证书、CRL撤销列表以及PKCS8等最基本的编解码函数。这些函数主要通过宏来实现。
    2）  抽象IO(BIO,crypto/bio目录)，本目录下的函数对各种输入输出进行抽象，包括文件、内存、标准输入输出、socket和SSL协议等。
    3）  大数运算(crypto/bn目录)，本目录下的文件实现了各种大数运算。这些大数运算主要用于非对称算法中密钥生成以及各种加解密操作。
         另外还为用户提供了大量辅助函数，比如内存与大数之间的相互转换。
    4）  字符缓存操作(crypto/buffer目录)。
    5）  配置文件读取(crypto/conf目录)，openssl主要的配置文件为openssl.cnf。本目录下的函数实现了对这种格式配置文件的读取操作。
    6）  DSO(动态共享对象,crypto/dso目录)，本目录下的文件主要抽象了各种平台的动态库加载函数，为用户提供统一接口。
    7）  硬件引擎(crypto/engine目录)，硬件引擎接口。用户如果要写自己的硬件引擎，必须实现它所规定的接口。
    8）  错误处理(crypto/err目录)，当程序出现错误时，openssl能以堆栈的形式显示各个错误。
         本目录下只有基本的错误处理接口，具体的的错误信息由各个模块提供。各个模块专门用于错误处理的文件一般为*_err..c文件。
    9）  对称算法、非对称算法及摘要算法封装(crypto/evp目录)。
    10） HMAC(crypto/hmac目录)，实现了基于对称算法的MAC。
    11） hash表(crypto/lhash目录)，实现了散列表数据结构。openssl中很多数据结构都是以散列表来存放的。
         比如配置信息、ssl session和asn.1对象信息等。
    12） 数字证书在线认证(crypto/ocsp目录)，实现了ocsp协议的编解码以及证书有效性计算等功能。
    13） PEM文件格式处理(crypto/pem)，用于生成和读取各种PEM格式文件，包括各种密钥、数字证书请求、数字证书、PKCS7消息和PKCS8消息等。
    14） pkcs7消息语法(crypto/pkcs7目录)，主要实现了构造和解析PKCS7消息；
    15） pkcs12个人证书格式(crypto/pckcs12目录)，主要实现了pkcs12证书的构造和解析。
    16） 队列(crypto/pqueue目录)，实现了队列数据结构，主要用于DTLS。
    17） 随机数(crypto/rand目录)，实现了伪随机数生成，支持用户自定义随机数生成。
    18） 堆栈(crypto/stack目录)，实现了堆栈数据结构。
    19） 线程支持(crypto/threads)，openssl支持多线程，但是用户必须实现相关接口。
    20） 文本数据库(crypto/txt_db目录)。
    21） x509数字证书(crypto/x509目录和crypto/x509v3)，包括数字证书申请、数字证书和CRL的构造、解析和签名验证等功能了；
    22） 对称算法(crypto/aes、crypto/bf、crypto/cast、ccrypto/omp和crypto/des等目录)。
    23） 非对称算法(crypto/dh、crypto/dsa、crypto/ec和crypto/ecdh)。
    24） 摘要算法(crypto/md2、crypto/md4、crypto/md5和crypto/sha)以及密钥交换/认证算法(crypto/dh 和crypto/krb5)。

第三章 堆栈
   数据结构
        typedef struct stack_st
        {
               int num;
               char **data;
               int sorted;
               int num_alloc;
               int (*comp)(const char * const *, const char * const *);
        } STACK;
        各项意义如下：
        num:       堆栈中存放数据的个数。
        data:      用于存放数据地址，每个数据地址存放在data[0]到data[num-1]中。
        sorted:    堆栈是否已排序，如果排序则值为1，否则为0，堆栈数据一般是无序的，
                   只有当用户调用了sk_sort操作，其值才为1。
        comp:      堆栈内存放数据的比较函数地址，此函数用于排序和查找操作；
                   当用户生成一个新堆栈时，可以指定comp为用户实现的一个比较函数；
                   或当堆栈已经存在时通过调用sk_set_cmp_func函数来重新指定比较函数。
        注意，
            用户不需要调用底层的堆栈函数(sk_sort、sk_set_cmp_func等)，
            而是调用他通过宏实现的各个函数。
    操作函数（部分）
        openssl堆栈实现源码位于crypto/stack目录下
        1) sk_set_cmp_func
            此函数用于设置堆栈存放数据的比较函数。由于堆栈不知道用户存放的是什么数据，
            所以，比较函数必须由用户自己实现。
        2) sk_find
            根据数据地址来查找它在堆栈中的位置。当堆栈设置了比较函数时，它首先对堆栈进行排序，
            然后通过二分法进行查找。如果堆栈没有设置比较函数，它只是简单的比较数据地址来查找.
        3）sk_sort
            本函数对堆栈数据排序。它首先根据sorted来判断是否已经排序，
            如果未排序则调用了标准C函数qsort进行快速排序。
        4）sk_pop_free
            本函数用于释放堆栈内存放的数据以及堆栈本身，它需要一个由用户指定的针对具体数据的释放函数。
            如果用户仅调用sk_free函数，则只会释放堆栈本身所用的内存，而不会释放数据内存。
            
第四章 哈希表
    数据结构
        其源码在crypto/lhash目录下，数据结构在lhash.h中定义如下：
        typedef struct lhash_node_st
        {
            void *data;
            struct lhash_node_st *next;
            #ifndef OPENSSL_NO_HASH_COMP
            unsigned long hash;
            #endif
        } LHASH_NODE;
        本结构是一个单链表。其中，data用于存放数据地址，next为下一个数据地址，hash为数据哈希计算值。
        typedef struct lhash_st
        {
            LHASH_NODE **b;  //头指针的数组，每个头指针指向一条链表，链表的元素符合上面的结构
            LHASH_COMP_FN_TYPE comp;    //comp用于存放数据比较函数地址
            LHASH_HASH_FN_TYPE hash;    //hash用于存放计算哈希值函数的地址
            unsigned int num_nodes;     //num_nodes为链表个数
            unsigned int num_alloc_nodes;   //num_alloc_nodes为b分配空间的大小
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
    函数说明
        1)  LHASH *lh_new(LHASH_HASH_FN_TYPE h, LHASH_COMP_FN_TYPE c)
            功能：生成哈希表
            源文件：lhash.c
            说明： 输入参数h为哈希函数，c为比较函数。这两个函数都是回调函数。
                   因为哈希表用于存放任意的数据结构，哈希表存放、查询、删除等操作都需要比较数据和进行哈希运算，
                   而哈希表不知道用户数据如何进行比较，也不知道用户数据结构中需要对哪些关键项进行散列运算。
                   所以，用户必须提供这两个回调函数。
        2)  void *lh_delete(LHASH *lh, const void *data)
            源文件：lhash.c
            功能：删除散列表中的一个数据
            说明：data为数据结构指针。
        3)  void lh_doall(LHASH *lh, LHASH_DOALL_FN_TYPE func)
            源文件：lhash.c
            功能：处理哈希表中的所有数据
            说明：func为外部提供的回调函数，本函数遍历所有存储在哈希表中的数据，每个数据被func处理。
        4)  void lh_doall_arg(LHASH *lh, LHASH_DOALL_ARG_FN_TYPE func, void *arg)
            源文件：lhash.c
            功能：处理哈希表中所有数据
            说明：此参数类似于lh_doall 函数，func为外部提供的回调函数，arg为传递给func函数的参数。
                  本函数遍历所有存储在哈希表中的数据，每个数据被func处理。
        5)  void lh_free(LHASH *lh)
            源文件：lhash.c
            功能：释放哈希表。
        6） void *lh_insert(LHASH *lh, void *data)
            源文件：lhash.c
            功能：往哈希表中添加数据。
            说明：data为需要添加数据结构的指针地址。
        7） void *lh_retrieve(LHASH *lh, const void *data)
            源文件：lhash.c
            功能：查询数据。
            说明：从哈希表中查询数据，data为数据结构地址，此数据结构中必须提供关键项
                  (这些关键项对应于用户提供的哈希函数和比较函数)以供查询，
                  如果查询成功，返回数据结构的地址，否则返回NULL。
                  比如SSL握手中服务端查询以前存储的SESSION时，它需要提供其中关键的几项：
                  SSL_SESSION *ret=NULL,data;
                  data.ssl_version=s->version;
                  data.session_id_length=len;
                  memcpy(data.session_id,session_id,len);
                 ret=(SSL_SESSION *)lh_retrieve(s->ctx->sessions,&data);
        8） void lh_node_stats_bio(const LHASH *lh, BIO *out)
            源文件：lh_stats.c
            功能：将哈希表中每个链表下的数据状态输出到BIO中。
        9）  void lh_node_stats(const LHASH *lh, FILE *fp)
            源文件：lh_stats.c
            功能：将哈希表中每个链表下数据到个数输出到FILE中。
            说明：此函数调用了lh_node_stats_bio函数。
        10）void lh_node_usage_stats_bio(const LHASH *lh, BIO *out)
            源文件：lh_stats.c
            功能：将哈希表的使用状态输出到BIO中。
        11）void lh_node_usage_stats(const LHASH *lh, FILE *fp)
            源文件：lh_stats.c
            功能：将哈希表的使用状态输出到FILE中
            说明：此函数调用了lh_node_usage_stats_bio函数
        12）unsigned long lh_num_items(const LHASH *lh)
            源文件：lhash.c
            功能：获取哈希表中元素的个数。
        13）void lh_stats_bio(const LHASH *lh, BIO *out)
            源文件：lh_stats.c
            功能：输出哈希表统计信息到BIO中
        14）void lh_stats(const LHASH *lh, FILE *fp)
            源文件：lh_stats.c
            功能：打印哈希表的统计信息，此函数调用了lh_stats_bio。
        15）unsigned long lh_strhash(const char *c)
            源文件：lhash.c
            功能：计算文本字符串到哈希值
            
第五章 内存分配
    简介
        openssl提供了内置的内存分配/释放函数。
        如果用户完全调用openssl的内存分配和释放函数，可以方便的找到内存泄露点。
        openssl分配内存时，在其内部维护一个内存分配哈希表，用于存放已经分配但未释放的内存信息。
        当用户申请内存分配时，在哈希表中添加此项信息，内存释放时删除该信息。
        当用户通过openssl函数查找内存泄露点时，只需查询该哈希表即可。
        用户通过openssl回调函数还能处理那些泄露的内存。
        openssl供用户调用的内存分配等函数主要在crypto/mem.c中实现
        其内置的分配函数在crypto/mem_dbg.c中实现。
        默认情况下mem.c中的函数调用mem_dbg.c中的实现。
        如果用户实现了自己的内存分配函数以及查找内存泄露的函数，
        可以通过调用CRYPTO_set_mem_functions函数和CRYPTO_set_mem_debug_functions函数来设置。
    内存数据结构
        定义在crypto/mem_dbg.c中
        typedef struct app_mem_info_st
        {     
            unsigned long thread;
            const char *file;
            int line;
            const char *info;
            struct app_mem_info_st *next; /* tail of thread‘s stack */
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
        各项意义：
            addr：分配内存的地址。
            num：分配内存的大小。
            file：分配内存的文件。
            line：分配内存的行号。
            thread：分配内存的线程ID。
            order：第几次内存分配。
            time：内存分配时间。
            app_info:用于存放用户应用信息，为一个链表，里面存放了文件、行号以及线程ID等信息。
            references：被引用次数。
    主要函数
        1) CRYPTO_mem_ctrl
            本函数主要用于控制内存分配时，是否记录内存信息。
            如果不记录内存信息，将不能查找内存泄露。
            开启内存记录调用CRYPTO_mem_ctrl(CRYPTO_MEM_CHECK_ON)，
            关闭内存记录调用CRYPTO_mem_ctrl(CRYPTO_MEM_CHECK_OFF)。
            一旦CRYPTO_mem_ctrl(CRYPTO_MEM_CHECK_ON)被调用，
            直到用户调用CRYPTO_mem_ctrl(CRYPTO_MEM_CHECK_OFF)前，
            用户所有的opessl内存分配都会被记录。
        2) CRYPTO_is_mem_check_on
            查询内存记录标记是否开启。
        3）CRYPTO_dbg_malloc
            本函数用于分配内存空间，如果内存记录标记开启，则记录用户申请的内存。
            当需要记录内存信息时，该函数本身也需要申请内存插入哈希表，
            为了防止递归申请错误，它申请内存记录信息前必须暂时关闭内存记录标记，申请完毕再放开。
        4）CRYPTO_dbg_free
            释放内存，如果内存记录标记开启，还需要删除哈希表中对应的记录。
        5）CRYPTO_mem_leaks
            将内存泄露输出到BIO中。
        6）CRYPTO_mem_leaks_fp
            将内存泄露输出到FILE中(文件或者标准输出)，该函数调用了CRYPTO_mem_leaks。
        7）CRYPTO_mem_leaks_cb
            处理内存泄露，输入参数为用户自己实现的处理内存泄露的函数地址。
            该函数只需要处理一个内存泄露，openssl通过lh_doall_arg调用用户函数来处理所有记录(泄露的内存)。
            
第七章 抽象IO
    简介
        openssl对于io类型的抽象封装，包括：
        内存、文件、日志、标准输入输出、socket（TCP/UDP）、加/解密、摘要和ssl通道等
        BIO通过回调函数为用户隐藏了底层实现细节
        Bio中的数据能从一个BIO传送到另外一个BIO或者是应用程序
    数据结构：
        在crypto/bio.h中定义如下
        1）BIO_METHOD
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
            该结构定义了IO操作的各种回调函数，
            根据需要，具体的bio类型必须实现其中的一种或多种回调函数，
            各项意义如下：
                type：   具体BIO类型；
                name：   具体BIO的名字；
                bwrite： 具体BIO写操作回调函数；
                bread：  具体BIO读操作回调函数；
                bputs：  具体BIO中写入字符串回调函数；
                bgets：  具体BIO中读取字符串函数；
                ctrl：   具体BIO的控制回调函数；
                create： 生成具体BIO回调函数；
                destroy：销毁具体BIO回调函数；
                callback_ctrl：具体BIO控制回调函数，与ctrl回调函数不一样，
                               该函数可由调用者（而不是实现者）来实现，
                               然后通过BIO_set_callback等函数来设置。
        2）BIO
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
            }；
            主要项含义：
                init：
                    具体句柄初始化标记，初始化后为1。
                    比如文件BIO中，通过BIO_set_fp关联一个文件指针时，该标记则置1；
                    socket BIO中，通过BIO_set_fd关联一个链接时，设置该标记为1。
                shutdown：
                    BIO关闭标记，当该值不为0时，释放资源；该值可以通过控制函数来设置。
                flags：
                    有些BIO实现需要它来控制各个函数的行为。
                    比如文件BIO默认该值为BIO_FLAGS_UPLINK，
                    这时文件读操作调用UP_fread函数而不是调用fread函数。
                retry_reason：
                    重试原因，主要用在socket和ssl BIO 的异步阻塞。
                    比如socket bio中，遇到WSAEWOULDBLOCK错误时，openssl告诉用户的操作需要重试。
                num：
                    该值因具体BIO而异，比如socket BIO中num用来存放链接字。
                ptr：
                    指针，具体bio有不同含义。
                    比如文件BIO中它用来存放文件句柄；
                    mem bio中它用来存放内存地址；
                    connect bio中它用来存放BIO_CONNECT数据，
                    accept bio中它用来存放BIO_ACCEPT数据。
                next_bio：
                    下一个BIO地址，BIO数据可以从一个BIO传送到另一个BIO，
                    该值指明了下一个BIO的地址。
                references：
                    被引用数量。
                num_read：
                    BIO中已读取的字节数。
                num_write：
                    BIO中已写入的字节数。
                ex_data：
                    用于存放额外数据。
    相关函数
        BIO各个函数定义在crypto/bio.h中。所有的函数都由BIO_METHOD中的回调函数来实现。
        函数主要分为几类：
            1）具体BIO相关函数
               比如：BIO_new_file（生成新文件）和BIO_get_fd（设置网络链接）等。
            2）通用抽象函数
               比如BIO_read和BIO_write等。
        另外，有很多函数是由宏定义通过控制函数BIO_ctrl实现，
        比如BIO_set_nbio、BIO_get_fd和BIO_eof等等。
    示例
        加解密
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
            //===========解密==============
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
            
第九章 随机数
    概述
        openssl生成随机数的源码位于crypto/rand目录下
        rand.h定义了许多与随机数生成相关的函数
        openssl通过使用摘要算法来生成随机数，可用的摘要算法有：sha1、md5、mdc2和md2。
        具体采用那种摘要算法在crypto/rand_lcl.h中由宏来控制。
        Openssl维护一个内部随机状态数据(md_rand.c中定义的全局变量state和md)，
        通过对这些内部数据计算摘要来生成随机数
    数据结构
        Openssl随机数相关的数据结构如下，定义在rand.h中：
        struct rand_meth_st
        {
            void (*seed)(const void *buf, int num);
            int (*bytes)(unsigned char *buf, int num);
            void (*cleanup)(void);
            void (*add)(const void *buf, int num, double entropy);
            int (*pseudorand)(unsigned char *buf, int num);
            int (*status)(void);
        };    
        本结构主要定义了各种回调函数，如果用户需要实现自己的随机数生成函数，他需要实现本结构中的各个函数。
        Openssl给出了一个默认的基于摘要的rand_meth实现(crypto/md_rand.c)。
        各项意义如下：
            seed：种子函数，为了让openssl内部维护的随机数据更加无序，可使用本函数。
                buf为用户输入的随机数地址，num为其字节数。
                Openssl将用户提供的buf中的随机内容与其内部随机数据进行摘要计算，更新其内部随机数据。
                本函数无输出；
            bytes：生成随机数，openssl根据内部维护的随机数状态来生成结果。
                buf用于存放生成的随机数。num为输入参数，用来指明生成随机数的字节长度；
            cleanup：清除函数，本函数将内部维护的随机数据清除；
            add：与seed类似，也是为了让openssl内部随机数据更加无序，
                其中entropy(信息熵)可以看作用户本次加入的随机数的个数。
                Openssl默认的随机数熵为32字节，在rand_lcl.h中由ENTROPY_NEEDED定义。
                Openssl给出随机数之前，用户提供的所有的随机种子数之和必须达到32字节。
                在openssl实现的md_rand中，即使用户不调用种子函数来直接生成随机数，
                openssl也会调用RAND_poll函数来完成该操作。
            pseudorand：本函数与bytes类似也是来生成随机数。
            status：查看熵值是否达到预定值，openssl中为32字节，如果达到则返回1，否则返回0。
                在openssl实现的md_rand中该函数会调用RAND_poll函数来使熵值合格。 
                如果本函数返回0，则说明此时用户不应生成随机数，需要调用seed和add函数来添加熵值。
    主要函数
        1)  int RAND_load_file(const char *file, long bytes)
            本函数将file指定的随机数文件中的数据读取bytes字节(如果bytes大于1024，则读取1024字节)，
            调用RAND_add进行计算，生成内部随机数。
        2)  RAND_write_file
            写随机数到文件，该文件可用被之后的RAND_load_file调用来完成PRNG的初始化。
        3)  const char *RAND_file_name(char *file,size_t num)
            获取随机数文件名，如果随机数文件长度小于num则返回空，否则返回文件名。
        4)  RAND_poll
            用于计算内部随机数，各个平台有各自的实现。
        5)  RAND_screen/RAND_event
            Windows特有函数，用来计算内部随机数，他们调用了RAND_seed。
        6)  RAND_seed/RAND_add
            用来计算内部随机数。
        7)  RAND_bytes/RAND_pseudo_bytes
            用来计算随机数。
        8)  RAND_cleanup
            清除内部随机数。
        9)  RAND_set_rand_method
            用来设置rand_meth，当用户实现了自己的随机数生成函数时(实现rand_meth中的回调函数)，
            调用该方法来替换openssl 所提供的随机数功能。
        10) RAND_status
            用来查看内部随机数熵值是否已达到预定值，如果未达到，则不应该生成随机数。
        11) RAND_bytes
            生成指定数量的随机字节（使用一个密码安全伪随机数）并存储在buf参数中
        
第十一章 大数
    数据结构
        crypto/bn.h中定义了大数的表示方式，如下：
        struct bignum_st
        {
            BN_ULONG *d;
            int top;    
            int dmax;
            int neg;
            int flags;
        };
        各项意义如下：
        d：    BN_ULONG(因系统而异，win32下为4个字节)，数组指针首地址，大数就存放在这里面，不过是倒放的。
               比如，用户要存放的大数为12345678000（通过BN_bin2bn放入），
               则d的内容如下：0x30 0x30 0x30 0x38 0x37 0x36 0x35 0x34 0x33 0x32 0x31；
        top：  用来指明大数占多少个BN_ULONG空间，上例中top为3。
        dmax： d数组的大小。
        neg：  是否为负数，如果为1，则是负数，为0，则为正数。
        flags：用于存放一些标记，比如flags含有BN_FLG_STATIC_DATA时，表明d的内存是静态分配的；
               含有BN_FLG_MALLOCED时，d的内存是动态分配的。
    函数
        1） BN_rand/BN_pseudo_rand
            生成一个随机的大数。
        2） BN_rand_range/BN_pseudo_rand_range
            生成随机数，但是给出了随机数的范围。
        3） BN_dup
            大数复制。
        4)  BN_generate_prime
            生成素数。
        5)  int BN_add_word(BIGNUM *a, BN_ULONG w)
            给大数a加上w，如果成功，返回1。
        6)  BIGNUM *BN_bin2bn(const unsigned char *s, int len, BIGNUM *ret)
            将内存中的数据转换为大数，为内存地址，len为数据长度，ret为返回值。
        7)  int BN_bn2bin(const BIGNUM *a, unsigned char *to)
            将大数转换为内存形式。输入参数为大数a，to为输出缓冲区地址，缓冲区需要预先分配，返回值为缓冲区的长度。
        8)  char *BN_bn2dec(const BIGNUM *a) 
            将大数转换成整数字符串。返回值中存放整数字符串，它由内部分配空间，用户必须在外部用OPENSSL_free函数释放该空间。
        9）char *BN_bn2hex(const BIGNUM *a)
            将大数转换为十六进制字符串。返回值为生成的十六进制字符串，外部需要用OPENSSL_free函数释放
        10) BN_cmp
            比较两个大数。
        11）BIGNUM *BN_mod_inverse(BIGNUM *in,  const BIGNUM *a, const BIGNUM *n, BN_CTX *ctx)
            计算ax=1(mod n)。          
        12）BN_zero()、BN_one()、BN_set_word() 
            设置值为0、1、或指定值
            
第十二章 BASE64编解码
    主要函数
        1）  编码函数
        EVP_EncodeInit         编码前初始化上下文。
        EVP_EncodeUpdate       进行BASE64编码，本函数可多次调用。
        EVP_EncodeFinal        进行BASE64编码，并输出结果。
        EVP_EncodeBlock        进行BASE64编码。
        2）  解码函数
        EVP_DecodeInit         解码前初始化上下文。
        EVP_DecodeUpdate       BASE64解码，本函数可多次调用。
        EVP_DecodeFinal        BASE64解码，并输出结果。
        EVP_DecodeBlock        BASE64解码，可单独调用。
    
第十三章 asn1
    ASN.1(Abstract Syntax Notation One，X.208)，是一套灵活的标记语言，它允许定义多种数据类型，
    从integer、bit string 一类的简单类型，到结构化类型，如set 和sequence，
    并且可以使用这些类型构建复杂类型。
    DER编码是ANS.1定义的将对象描述数据编码成八位串值的编码规则，
    它给出了对ANS.1值（对象的类型和值）的唯一编码规则。
    1) 简单类型
        BIT STRING          任意0、1位串；
        IA5String           任意IA5(ASCII)字符串；
        INTEGER             任意一个整数；
        NULL                空值；
        OBJECT IDENTIFIER   一个对象标识号（一串整数），标识算法或属性类型等对象；
        OCTET STRING        8位串；
        PrintableString     任意可打印字符串；
        T61String           任意T.61（8位）字符串；
        UTCTime             一个“协同世界时”或“格林威治标准时（G.M.T）”。
    2) 结构类型
        结构类型由组件组成，ANS.1定义了四种结构类型：
        SEQUENCE            一个或多个类型的有序排列；
        SEQUENCE OF         一个给定类型的0个或多个有序排列；
        SET                 一个或多个类型的无序集合；
        SET OF              一个给定类型的0个或多个无序集合。
    3) 带标记类型
        在一个应用内部区分类型的有效方法是使用标记，
        标记也同样用于区分一个结构类型内部不同的组件。
        例如SET或SEQUENCE类型可选项通常使用上下文标记以避免混淆。
        有两种标记类型的方法：隐式和显式。
        隐式标记类型是将其它类型的标记改变，得到新的类型。
        隐式标记的关键字是IMPLICIT。
        显式标记类型是将其它类型加上一个外部标记，得到新的类型。
        显式标记的关键字是EXPLICIT。
        为了进行编码，隐式标记类型除了标记不同以外，可以视为与其基础类型相同。
        显式标记类型可以视为只有一个组件的结构类型。
    4) 其它类型
        类型和值用符号::=表示，符号左边的是名字，右边是类型和值。
        名字又可以用于定义其它的类型和值。
        除了CHOICE类型、ANY类型以外，所有ANS.1类型都有一个标记，
        标记由一个类和一个非负的标记码组成，
        当且仅当标记码相同时，ANS.1类型是相同的。
        也就是说，影响其抽象意义的不是ANS.1类型的名字，而是其标记。
        通用标记在X.208中定义，并给出相应的通用标记码。
        其它的标记类型分别在很多地方定义，可以通过隐式和显式标记获得。
    下表列出了一些通用类型及其标记：
        类型                        标记码（十六进制）
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
    当采用Openssl的ASN.1库编码一个asn.1定义的结构的时候，需要采用如下步骤：
        1) 用 ASN.1语法定义内部数据结构，并声明函数；
            所谓内部数据结构，指的是Openssl中用基本的数据类型，
            按照ASN.1语法定义的其他的数据结构，这种数据结构可以方便的用于编解码。
            以x509v4中的证书有效期为例，证书有效期定义如下：
            AttCertValidityPeriod  ::= SEQUENCE 
            {
                notBeforeTime  GeneralizedTime,
                notAfterTime   GeneralizedTime
            }
            
            所以我们可以定义相应的内部数据结构，如下：
            typedef    struct      X509V4_VALID_st
            {
                ASN1_GENERALIZEDTIME *notBefore;
                ASN1_GENERALIZEDTIME *notAfter;
            }X509V4_VALID;
            DECLARE_ASN1_FUNCTIONS(X509V4_VALID)
            
            其中最后一行用于定义四个函数：
            X509V4_VALID  *X509V4_VALID_new(void);
            void          *X509V4_VALID_free(X509V4_VALID *a);
            X509V4_VALID  *d2i_ASN1_INTEGER(X509V4_VALID **a,unsigned char **in,long len);
            int           i2d_ X509V4_VALID (X509V4_VALID *a,unsigned char **out);
        2) 实现内部数据结构的四个基本函数
            实现内部数据结构的基本函数，是通过一系列的宏来实现的。
            定义的模式如下，以属性证书有效期为例，如下：
            /* X509V4_VALID */
            ASN1_SEQUENCE(X509V4_VALID) = 
            {
                ASN1_SIMPLE(X509V4_VALID, notBefore, ASN1_GENERALIZEDTIME),
                ASN1_SIMPLE(X509V4_VALID, notAfter, ASN1_GENERALIZEDTIME)
            } ASN1_SEQUENCE_END(X509V4_VALID)
            IMPLEMENT_ASN1_FUNCTIONS(X509V4_VALID)
            这样通过宏就实现了一个asn.1定义结构的最基本的四个函数。
    Openssl的ASN.1宏
        1)   DECLARE_ASN1_FUNCTIONS
             用于声明一个内部数据结构的四个基本函数，一般可以在头文件中定义。
        2)   IMPLEMENT_ASN1_FUNCTIONS
             用于实现一个数据结构的四个基本函数。
        3）  ASN1_SEQUENCE
             用于SEQUENCE，表明下面的编码是一个SEQUENCE。
        4)   ASN1_CHOICE
             表明下面的编码是选择其中一项，为CHOICE类型。
        5）  ASN1_SIMPLE
             用于简单类型或结构类型，并且是必须项。
        6)   ASN1_EXP
             用于显示标记，表明asn.1语法中，本项是显示标记。
        7)   ASN1_IMP
             用于隐示标记，表明asn.1语法中，本项是隐示类型。
        8)   ASN1_OPT
             用于可选项，表明asn.1语法中，本项是可选的。
        9)   ASN1_EXP_OPT
             用于显示标记，表明asn.1语法中，本项是显示类型，并且是可选的；
        10)  ASN1_IMP_OPT
             用于隐示标记，表明asn.1语法中，本项是隐示类型，并且是可选的。
        11） ASN1_IMP_SEQUENCE_OF_OPT
             用于隐示标记，表明asn.1语法中，本项是一个SEQUENCE序列，为隐示类型，并且是可选的。
        12)  ASN1_SEQUENCE_END
             用于SEQUENCE结束。
        13)  ASN1_CHOICE_END
             用于结束CHOICE类型。
    openssl源码探索
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
 
第十四章 错误处理
    数据结构
        openssl中，通过unsigned long类型来存放错误信息。
        它包含三部分内容：库代码、函数代码以及错误原因代码。
        其中，库代码在crypto/err.h中定义，函数代码以及错误原因代码由各个功能模块定义
        这三部分分别占用不同的bit位
        #define ERR_GET_LIB(l)       (int)((((unsigned long)l)>>24L)&0xffL)
        #define ERR_GET_FUNC(l)      (int)((((unsigned long)l)>>12L)&0xfffL)
        #define ERR_GET_REASON(l)    (int)((l)&0xfffL)
        库的个数不能大于255（0xff），函数个数和错误原因不能大于4095（0xfff）。
        主要数据结构有两个，定义在crypto/err/err.h中，如下：
        1）ERR_STRING_DATA
            typedef struct ERR_string_data_st
            {
                unsigned long error;
                const char *string;
            } ERR_STRING_DATA;
            该数据结构的内容由各个功能模块来设置。
            其中，error用来存放错误信息（由库代码、函数代码以及错误原因代码计算得来），
            string用来存放文本信息，可以是函数名也可以是错误原因。
            以crypto/bio_err.c为例，它定义了两个全局表，分别用来存放函数信息和错误信息：
            #define ERR_FUNC(func) ERR_PACK(ERR_LIB_BIO,func,0)
            #define ERR_REASON(reason) ERR_PACK(ERR_LIB_BIO,0,reason)
            static ERR_STRING_DATA BIO_str_functs[]=
            {
                {ERR_FUNC(BIO_F_ACPT_STATE),  "ACPT_STATE"},
                ……
            }
            static ERR_STRING_DATA BIO_str_reasons[]=
            {
                {ERR_REASON(BIO_R_ACCEPT_ERROR)          ,"accept error"},
                {ERR_REASON(BIO_R_BAD_FOPEN_MODE)        ,"bad fopen mode"},
                ……
            }
            这两个表通过 ERR_load_BIO_strings 函数来添加到错误信息哈希表中去。
            为了便于查找，所有模块的错误信息存放在一个全局哈希表中，在crypto/err.c中实现。
        2）ERR_STATE
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
            该结构用于存放和获取错误信息。
            由于可能会有多层函数调用(错误堆栈)，这些信息都是一个数组。
            每个数组代表了一层函数的错误信息。
            各项意义如下：
                pid：          当前线程id。
                err_buffer[i]：第i层错误码，包含库、函数以及错误原因信息。
                err_data[i]：  存放第i层操作信息。
                err_data_flags[i]：存放err_data[i]相关的标记；比如为ERR_TXT_MALLOCED时，
                                    表名err_data[i]中的数据是动态分配内存的，
                                    需要释放；为ERR_TXT_STRING表名err_data[i]中的数据是一个字符串，可以用来打印。
                err_file[i]：第i层错误的文件名。
                err_line[i]：第i层错误的行号。
                top和bottom：用于指明ERR_STATE的使用状态。
                             top对应于最后一个错误（错误堆栈的最上层），
                             bottom对应第一个错误（错误堆栈的最底层）。
        当用户需要扩展openssl的模块时，可以仿照其他已有模块来实现自己的错误处理。
    主要函数
        1)  ERR_add_error_data
            在本层错误的err_data元素中添加说明信息。
            该函数一般由各个模块调用，比如可以用它说明什么操作导致了错误。
        2） ERR_clear_error
            清除所有的错误信息。如果不清楚所有错误信息，可能会有其他无关错误遗留在ERR_STATE表中。
        3） ERR_error_string/ ERR_error_string_n
            根据错误码获取具体的错误信息，包括出错的库、出错的函数以及错误原因。
        4)  ERR_free_strings
            释放错误信息哈希表；通常在最后调用。
        5)  ERR_func_error_string
            根据错误号，获取出错的函数信息。
        6） ERR_get_err_state_table
            获取存放错误的哈希表。
        7） ERR_get_error
            获取第一个错误号。
        8)  ERR_get_error_line
            根据错误号，获取错误的行号。
        9)  ERR_get_error_line_data
            根据错误号，获取出错信息。
        10) ERR_get_implementation
            获取错误处理函数，与哈希表操作相关。
        11）ERR_get_state
            获取ERR_STATE表。
        12）ERR_lib_error_string
            根据错误号，获取是哪个库出错。
        13）ERR_load_strings
            加载错误信息，由各个模块调用。
        14）ERR_load_ASN1_strings
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
            各个模块实现的，加载各自错误信息。
        15）ERR_peek_error
            获取第一个错误号。
        16）ERR_peek_error_line
            获取第一个错误的出错行。
        17）ERR_peek_error_line_data
            获取第一个错误的行数和错误信息。
        18）ERR_peek_last_error
            获取最后一个错误号。
        19）ERR_peek_last_error_line
            获取最后一个错误的行号。
        20）ERR_peek_last_error_line_data
            获取最后一个错误的行号和错误信息。
        21）ERR_print_errors
            将错误信息输出到bio中。
        22）ERR_print_errors_cb
            根据用户设置的回调函数来打印错误信息。
        23）ERR_print_errors_fp
            将错误打印到FILE中。
        24)  ERR_put_error
            将错误信息存放到ERR_STATE 表中top指定的错误堆栈(最后的错误)。
        25)  ERR_reason_error_string
            根据错误号得到错误原因。
        26)  ERR_remove_state
            删除线程相关的错误信息。
        27)  ERR_set_error_data
            将错误信息存放到ERR_STATE 表中top指定的错误堆栈(最后的错误)。
        28)  ERR_unload_strings
            从错误哈希表中删除相关信息。
 
第十五章 摘要与hmac
    函数说明
        1)  XXX_Init
            XXX为具体的摘要算法名称，该函数初始化上下问，用于多数据摘要。
        2)  XXX_Update
            XXX为具体的摘要算法名称，进行摘要计算，该函数可运行多次，对多个数据摘要。
        3)  XXX_Final
            XXX为具体的摘要算法名称，进行摘要计算，该函数与1)和2）一起用。
        4)  XXX
            对一个数据进行摘要。该函数由上述1）2）和3）实现，只是XXX_Update只调用一次
            
第十六章 数据压缩
    数据结构
        COMP_METHOD（压缩算法）
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
            各项意义如下：
                type：压缩算法的nid；
                name：压缩算法的名字；
                init：初始化函数；
                finish：结束操作；
                commpress：具体的压缩算法，本函数必须实现；
                expand：具体的解压算法，本函数必须实现；
                ctrl和callback_ctrl：控制函数与回调控制函数，用于内部控制。
        comp_ctx（存放压缩/解压中的上下文数据）
            struct comp_ctx_st
            {
                COMP_METHOD *meth;
                unsigned long compress_in;
                unsigned long compress_out;
                unsigned long expand_in;
                unsigned long expand_out;
                CRYPTO_EX_DATA     ex_data;
            };
            各项意义如下：
                meth：COMP_METHOD结构，一个comp_ctx通过它指明了一种具体的压缩算法；
                compress_in：被压缩数据总字节数；
                compress_out：压缩数据(结果)总字节数；
                expand_in：被解压数据总字节数；
                expand_out：解压数据（结果）总字节数；
                ex_data：供用户使用的扩展数据，用于存放用户自定义的信息。
    函数说明
        1)  COMP_rle
            返回openssl实现的空压缩算法，返回值为一个COMP_METHOD。
        2)  COMP_zlib
            返回基于zlib库的COMP_METHOD。
        3） COMP_CTX_new
            初始化上下文，输入参数为COMP_METHOD。
        4） COMP_compress_block
            压缩计算。
        5） COMP_expand_block
            解压计算。
            
第十七章 rsa
    简介
        RSA算法是一个广泛使用的公钥算法。其密钥包括公钥和私钥。
        它能用于数字签名、身份认证以及密钥交换。
    RSA密钥信息主要包括：
        n：   模数
        e：   公钥指数
        d：   私钥指数
        p：   最初的大素数
        q：   最初的大素数
        dmp1：e*dmp1 = 1 (mod (p-1))
        dmq1：e*dmq1 = 1 (mod (q-1))
        iqmp：q*iqmp = 1 (mod p )
        参：file://RSA原理.txt
    openssl的RSA实现源码如下：
        1）rsa.h
           定义RSA数据结构以及RSA_METHOD，定义了RSA的各种函数。
        2) rsa_asn1.c
           实现了RSA密钥的DER编码和解码，包括公钥和私钥。
        3）rsa_chk.c
           RSA密钥检查。
        4）rsa_eay.c
           Openssl实现的一种RSA_METHOD，作为其默认的一种RSA计算实现方式。
           此文件未实现rsa_sign、rsa_verify和rsa_keygen回调函数。
        5）rsa_err.c
           RSA错误处理。
        6）rsa_gen.c
           RSA密钥生成，如果RSA_METHOD中的rsa_keygen回调函数不为空，则调用它，否则调用其内部实现。
        7）rsa_lib.c
           主要实现了RSA运算的四个函数(公钥/私钥，加密/解密)，它们都调用了RSA_METHOD中相应都回调函数。
        8）rsa_none.c
           实现了一种填充和去填充。
        9）rsa_null.c
           实现了一种空的RSA_METHOD。
        10) rsa_oaep.c
           实现了oaep填充与去填充。
        11）rsa_pk1.c
           实现了pkcs1填充与去填充。
        12）rsa_sign.c
           实现了RSA的签名和验签。
        13）rsa_ssl.c
           实现了ssl填充。
        14）rsa_x931.c
           实现了一种填充和去填充。
    RSA签名与验证过程
        RSA签名过程如下：
            1) 对用户数据进行摘要；
            2）构造X509_SIG结构并DER编码，其中包括了摘要算法以及摘要结果。
            3）对2）的结果进行填充，填满RSA密钥长度字节数。
               比如1024位RSA密钥必须填满128字节。具体的填充方式由用户指定。
            4）对3）的结果用RSA私钥加密。
            注 RSA_eay_private_encrypt函数实现了3）和4）过程。
        RSA验签过程是上述过程的逆过程，如下：
            1) 对数据用RSA公钥解密，得到签名过程中2）的结果。
            2) 去除1）结果的填充。
            3) 从2）的结果中得到摘要算法，以及摘要结果。
            4) 将原数据根据3）中得到摘要算法进行摘要计算。
            5）比较4）与签名过程中1）的结果。
            注 RSA_eay_public_decrypt实现了1）和2）过程。
    数据结构
        RSA_METHOD
            struct rsa_meth_st
            {
                const char      *name;
                int (*rsa_pub_enc)(int flen,const unsigned char *from,unsigned char *to,RSA *rsa,int padding);
                int (*rsa_pub_dec)(int flen,const unsigned char *from,unsigned char *to,RSA *rsa,int padding);
                int (*rsa_priv_enc)(int flen,const unsigned char *from,unsigned char *to,RSA *rsa,int padding);
                int (*rsa_priv_dec)(int flen,const unsigned char *from,unsigned char *to,RSA *rsa,int padding);
                /* 其他函数 */
                int (*rsa_sign)(int type,const unsigned char *m, unsigned int m_length,unsigned char *sigret,
                                unsigned int *siglen, const RSA *rsa);
                int (*rsa_verify)(int dtype,const unsigned char *m, unsigned int m_length,unsigned char *sigbuf, 
                                  unsigned int siglen, const RSA *rsa);
                int (*rsa_keygen)(RSA *rsa, int bits, BIGNUM *e, BN_GENCB *cb);
            };
            主要项说明：
                name：RSA_METHOD名称；
                rsa_pub_enc： 公钥加密函数，padding为其填充方式，输入数据不能太长，否则无法填充；
                rsa_pub_dec： 公钥解密函数，padding为其去除填充的方式，输入数据长度为RSA密钥长度的字节数；
                rsa_priv_enc：私钥加密函数，padding为其填充方式，输入数据长度不能太长，否则无法填充；
                rsa_priv_dec：私钥解密函数，padding为其去除填充的方式，输入数据长度为RSA密钥长度的字节数；
                rsa_sign：    签名函数；
                rsa_verify：  验签函数；
                rsa_keygen：  RSA密钥对生成函数。
            用户可实现自己的RSA_METHOD来替换openssl提供的默认方法。
        RSA
            RSA数据结构中包含了公/私钥信息（如果仅有n和e，则表明是公钥），定义如下：
            struct rsa_st
            {
                /* 其他 */
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
                /* 其他数据项 */
            };
            各项意义：
                meth：RSA_METHOD结构，指明了本RSA密钥的各种运算函数地址；
                engine：硬件引擎；
                n，e，d，p，q，dmp1，dmq1，iqmp：RSA密钥的各个值；
                ex_data：扩展数据结构，用于存放用户数据；
                references：RSA结构引用数。
    主要函数
        1） RSA_check_key
            检查RSA密钥。
        2） RSA_new
            生成一个RSA密钥结构，并采用默认的rsa_pkcs1_eay_meth RSA_METHOD方法。
        3） RSA_free
            释放RSA结构。
        4)  RSA *RSA_generate_key(int bits, unsigned long e_value,
            void (*callback)(int,int,void *), void *cb_arg)
            生成RSA密钥，bits是模数比特数，e_value是公钥指数e，callback回调函数由用户实现，
            用于干预密钥生成过程中的一些运算，可为空。
        5） RSA_get_default_method
            获取默认的RSA_METHOD，为rsa_pkcs1_eay_meth。
        6） RSA_get_ex_data
            获取扩展数据。
        7） RSA_get_method
            获取RSA结构的RSA_METHOD。
        8） RSA_padding_add_none
            RSA_padding_add_PKCS1_OAEP
            RSA_padding_add_PKCS1_type_1（私钥加密的填充）
            RSA_padding_add_PKCS1_type_2（公钥加密的填充）
            RSA_padding_add_SSLv23
            各种填充方式函数。
        9） RSA_padding_check_none
            RSA_padding_check_PKCS1_OAEP
            RSA_padding_check_PKCS1_type_1
            RSA_padding_check_PKCS1_type_2
            RSA_padding_check_SSLv23
            RSA_PKCS1_SSLeay
            各种去除填充函数。
        10）int RSA_print(BIO *bp, const RSA *x, int off)
            将RSA信息输出到BIO中，off为输出信息在BIO中的偏移量，
            比如是屏幕BIO，则表示打印信息的位置离左边屏幕边缘的距离。
        11）int DSA_print_fp(FILE *fp, const DSA *x, int off)
            将RSA信息输出到FILE中，off为输出偏移量。
        12）RSA_public_decrypt
            RSA公钥解密。
        13）RSA_public_encrypt
            RSA公钥加密。
        14）RSA_set_default_method/ RSA_set_method
            设置RSA结构中的method，当用户实现了一个RSA_METHOD时，
            调用此函数来设置，使RSA运算采用用户的方法。
        15）RSA_set_ex_data
            设置扩展数据。
        16）RSA_sign
            RSA签名。
        17）RSA_sign_ASN1_OCTET_STRING
            另外一种RSA签名，不涉及摘要算法，它将输入数据作为ASN1_OCTET_STRING
            进行DER编码，然后直接调用RSA_private_encrypt进行计算。
        18）RSA_size
            获取RSA密钥长度字节数。
        19）RSA_up_ref
            给RSA密钥增加一个引用。
        20）RSA_verify
            RSA验证。
        21）RSA_verify_ASN1_OCTET_STRING
            另一种RSA验证，不涉及摘要算法，与RSA_sign_ASN1_OCTET_STRING对应。
        22）RSAPrivateKey_asn1_meth
            获取RSA私钥的ASN1_METHOD，包括i2d、d2i、new和free函数地址。
        23）RSAPrivateKey_dup
            复制RSA私钥。
        24）RSAPublicKey_dup
            复制RSA公钥。
                
第十八章 DSA
    简介
        DSA算法是一种公钥算法，DSA安全性基于离散对数问题
        DSA 只能用于数字签名，而无法用于加密（某些扩展可以支持加密）
        与RSA相比，DSA的签名生成速度更快，但验证速度较慢
        file://RSA、DSA、ECDSA、EdDSA 和 Ed25519 的区别.py
        因为DSA已经不推荐使用，所以这里略过，具体参看chm文件
        
第十九章 DH
    简介
        它实质是一个通信双方进行密钥协商的协议：
            两个实体中的任何一个使用自己的私钥和另一实体的公钥，得到一个对称密钥，
            这一对称密钥其它实体都计算不出来
        DH算法的安全性基于有限域上计算离散对数的困难性。
        离散对数的研究现状表明：所使用的DH密钥至少需要1024位，才能保证有足够的中、长期安全。
        DH算法不能抵御中间人攻击，中间人可以伪造假的X和Y分别发送给双方来获取他们的秘密密钥，
        所以需要保证X和Y的来源合法性。
    数据结构
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
            DH_METHOD指明了一个DH密钥所有的计算方法函数。
            用户可以实现自己的DH_METHOD来替换openssl提供默认方法。
            各项意义如下：
                name：           DH_METHOD方法名称。
                generate_key：   生成DH公私钥的函数。
                compute_key：    根据对方公钥和己方DH密钥来生成共享密钥的函数。
                bn_mod_exp：     大数模运算函数，如果用户实现了它，生成DH密钥时，
                                 将采用用户实现的该回调函数。用于干预DH密钥生成。
                init：           初始化函数。
                finish：         结束函数。
                flags：          用于记录标记。
                app_data：       用于存放应用数据。
                generate_params：生成DH密钥参数的回调函数，生成的密钥参数是可以公开的。
        DH
            struct dh_st
            {
                /* 其他 */
                BIGNUM *p;
                BIGNUM *g;
                long length;      /* optional */
                BIGNUM *pub_key;
                BIGNUM *priv_key; 
                int references;
                CRYPTO_EX_DATA ex_data;
                const DH_METHOD *meth;
                ENGINE *engine;
                /* 其他 */
            };
            解释：
                p、g、length：DH密钥参数；
                pub_key：    DH公钥；
                priv_key：   DH私钥；
                references： 引用；
                ex_data：    扩展数据；
                meth：       DH_METHOD，本DH密钥的各种计算方法，明确指明了DH的各种运算方式；
                engine：     硬件引擎。
    主要函数
        1） DH_new
            生成DH数据结构，其DH_METHOD采用openssl默认提供的。
        2） DH_free
            释放DH数据结构。
        3） DH_generate_parameters
            生成DH密钥参数。
        4） DH_generate_key
            生成DH公私钥。
        5） DH_compute_key
            计算共享密钥，用于数据交换。
        6） DH_check
            检查DH密钥。
        7） DH_get_default_method
            获取默认的DH_METHOD，该方法是可以由用户设置的。
        8） DH_get_ex_data
            获取DH结构中的扩展数据。
        9)  DH_new_method
            生成DH数据结构。
        10）DH_OpenSSL
            获取openssl提供的DH_METHOD。
        11）DH_set_default_method
            设置默认的DH_METHOD方法，当用户实现了自己的DH_METHOD时，可调用本函数来设置，控制DH各种计算。
        12）DH_set_ex_data
            获取扩展数据。
        13）DH_set_method
            替换已有的DH_METHOD。
        14）DH_size
            获取DH密钥长度的字节数。
        15) DH_up_ref
            增加DH结构的一个引用。
        16）DHparams_print
            将DH密钥参数输出到bio中。
        17) DHparams_print_fp
            将DH密钥参数输出到FILE中。

第二十章 ECC
    简介
        椭圆曲线(ECC)算法是一种公钥算法，它比流行的RSA算法有很多优点：
        1）安全性能更高 ， 如160位ECC与1024位RSA、DSA有相同的安全强度。
        2）计算量小，处理速度快， 在私钥的处理速度上（解密和签名），ECC比RSA、DSA快得多。
        3）存储空间占用小  ECC的密钥尺寸和系统参数与RSA、DSA相比要小得多， 所以占用的存储空间小得多。
        4）带宽要求低。
    openssl的ECC实现
        Openssl实现了ECC算法。
        ECC算法系列包括三部分：
            ECC算法(crypto/ec)、
            椭圆曲线数字签名算法ECDSA (crypto/ecdsa)
            椭圆曲线密钥交换算法ECDH(crypto/dh)
        密钥数据结构
            主要是公钥和私钥数据结构。
            椭圆曲线密钥数据结构如下，定义在crypto/ec_lcl.h中，对用户是透明的。
            struct ec_key_st
            {
                int         version;
                EC_GROUP    *group;
                EC_POINT    *pub_key;
                BIGNUM      *priv_key;
                /* 其他项 */
            }
        密钥生成
            对照公钥和私钥的表示方法，非对称算法不同有各自的密钥生成过程。
            椭圆曲线的密钥生成实现在crytpo/ec/ec_key.c中。
            Openssl中，椭圆曲线密钥生成时，首先用户需要选取一种椭圆曲线
            (openssl的crypto/ec_curve.c中内置实现了67种，调用EC_get_builtin_curves获取该列表)，
            然后根据选择的椭圆曲线计算密钥生成参数group，最后根据密钥参数group来生公私钥。
        签名值数据结构
            非对称算法不同，签名的结果表示也不一样。
            与DSA签名值一样，ECDSA的签名结果表示为两项。
            ECDSA的签名结果数据结构定义在crypto/ecdsa/ecdsa.h中，如下：
            typedef struct ECDSA_SIG_st
            {
                BIGNUM *r;
                BIGNUM *s;
            } ECDSA_SIG;
        签名与验签
            对照签名结果，研究其是如何生成的。
            crypto/ecdsa/ecs_sign.c实现了签名算法，
            crypto/ecdsa/ecs_vrf.c实现了验签。
        密钥交换
            研究其密钥交换是如何进行的；
            crypto/ecdh/ech_ossl.c实现了密钥交换算法。
        主要函数
            1） EC_get_builtin_curves
                获取椭圆曲线列表。
            2） EC_GROUP_new_by_curve_name
                根据指定的椭圆曲线来生成密钥参数。
            3） EC_KEY_generate_key
                根据密钥参数生成ECC公私钥。
            4） EC_KEY_check_key
                检查ECC密钥。
            5） ECDSA_size
                获取ECC密钥大小字节数。
            6） ECDSA_sign
                签名，返回1表示成功。
            7） ECDSA_verify
                验签，返回1表示合法。
            8） EC_KEY_get0_public_key
                获取公钥。
            9） EC_KEY_get0_private_key
                获取私钥。
            10）ECDH_compute_key
                生成共享密钥
                
第二十一章 evp
    Openssl EVP(high-level cryptographic functions[1])提供了丰富的密码学中的各种函数
    Openssl中实现了各种摘要算法、对称算法以及签名/验签算法。
    EVP函数将这些具体的算法进行了封装。
    EVP主要封装了如下功能函数：
        1） 实现了base64编解码BIO；
        2） 实现了加解密BIO；
        3） 实现了摘要BIO；
        4） 实现了reliable BIO；
        5） 封装了摘要算法；
        6） 封装了对称加解密算法；
        7） 封装了非对称密钥的加密(公钥)、解密(私钥)、签名与验证以及辅助函数；
        7） 基于口令的加密(PBE)；
        8） 对称密钥处理；
        9） 数字信封：数字信封用对方的公钥加密对称密钥，数据则用此对称密钥加密。
            发送给对方时，同时发送对称密钥密文和数据密文。
            接收方首先用自己的私钥解密密钥密文，得到对称密钥，然后用它解密数据。
        10）其他辅助函数。
    数据结构
        EVP数据结构定义在crypto/evp.h中
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
            该结构用来存放非对称密钥信息，可以是RSA、DSA、DH或ECC密钥。
            其中， ptr 用来存放密钥结构地址，attributes堆栈用来存放密钥属性。
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
            该结构用来存放摘要算法信息、非对称算法类型以及各种计算函数。
            主要各项意义如下：
                type：     摘要类型，一般是摘要算法NID；
                pkey_type：公钥类型，一般是签名算法NID；
                md_size：  摘要值大小，为字节数；
                flags：    用于设置标记；
                init：     摘要算法初始化函数；
                update：   多次摘要函数；
                final：    摘要完结函数；
                copy：     摘要上下文结构复制函数；
                cleanup：  清除摘要上下文函数；
                sign：     签名函数，其中key为非对称密钥结构地址；
                verify：   摘要函数，其中key为非对称密钥结构地址。
            openssl对于各种摘要算法实现了上述结构，各个源码位于cypto/evp目录下，文件名以m_开头。
            Openssl通过这些结构来封装了各个摘要相关的运算。
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
            该结构用来存放对称加密相关的信息以及算法。主要各项意义如下：
                nid：        对称算法nid；
                block_size： 对称算法每次加解密的字节数；
                key_len：    对称算法的密钥长度字节数；
                iv_len：     对称算法的填充长度；
                flags：      用于标记；
                init：       加密初始化函数，用来初始化ctx，key为对称密钥值，iv为初始化向量，
                             enc用于指明是要加密还是解密，这些信息存放在ctx中；
                do_cipher：  对称运算函数，用于加密或解密；
                cleanup：    清除上下文函数；
                set_asn1_parameters：设置上下文参数函数；
                get_asn1_parameters：获取上下文参数函数；
                ctrl：       控制函数；
                app_data：   用于存放应用数据。
            openssl对于各种对称算法实现了上述结构，各个源码位于cypto/evp目录下，文件名以e_开头。
            Openssl通过这些结构来封装了对称算法相关的运算。
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
                /* 其他 */
                unsigned char final[EVP_MAX_BLOCK_LENGTH];
            } ;
            对称算法上下文结构，此结构主要用来维护加解密状态，存放中间以及最后结果。
            因为加密或解密时，当数据很多时，可能会用到Update函数，
            并且每次加密或解密的输入数据长度任意的，并不一定是对称算法block_size的整数倍，
            所以需要用该结构来存放中间未加密的数据。
            主要项意义如下：
                cipher：       指明对称算法；
                engine：       硬件引擎；
                encrypt：      是加密还是解密；非0为加密，0为解密；
                buf和buf_len： 指明还有多少数据未进行运算；
                oiv：          原始初始化向量；
                iv：           当前的初始化向量；
                final：        存放最终结果，一般与Final函数对应。
    源码结构
        evp源码位于crypto/evp目录，可以分为如下几类：
        1)  全局函数
            主要包括c_all.c、c_allc.c、c_alld.c以及names.c。
            他们加载openssl支持的所有的对称算法和摘要算法，放入到哈希表中。
            实现了OpenSSL_add_all_digests、OpenSSL_add_all_ciphers以及
            OpenSSL_add_all_algorithms(调用了前两个函数)函数。
            在进行计算时，用户也可以单独加载摘要函数（EVP_add_digest）和对称计算函数（EVP_add_cipher）。
        2)  BIO扩充
            包括bio_b64.c、bio_enc.c、bio_md.c和bio_ok.c，各自实现了BIO_METHOD方法，
            分别用于base64编解码、对称加解密以及摘要。
        3)  摘要算法EVP封装
            由digest.c实现，实现过程中调用了对应摘要算法的回调函数。
            各个摘要算法提供了自己的EVP_MD静态结构，对应源码为m_xxx.c。
        4） 对称算法EVP封装
            由evp_enc.c实现，实现过程调用了具体对称算法函数，实现了Update操作。
            各种对称算法都提供了一个EVP_CIPHER静态结构，对应源码为e_xxx.c。
            需要注意的是，e_xxx.c中不提供完整的加解密运算，它只提供基本的对于一个block_size数据的计算，
            完整的计算由evp_enc.c来实现。当用户想添加一个自己的对称算法时，可以参考e_xxx.c的实现方式。
            一般用户至少需要实现如下功能：
            ?  构造一个新的静态的EVP_CIPHER结构；
            ?  实现EVP_CIPHER结构中的init函数，该函数用于设置iv，
               设置加解密标记、以及根据外送密钥生成自己的内部密钥；
            ?  实现do_cipher函数，该函数仅对block_size字节的数据进行对称运算；
            ?  实现cleanup函数，该函数主要用于清除内存中的密钥信息。
        5)  非对称算法EVP封装
            主要是以p_开头的文件。其中，p_enc.c封装了公钥加密；p_dec.c封装了私钥解密；p_lib.c实现一些辅助函数；
            p_sign.c封装了签名函数；p_verify.c封装了验签函数；p_seal.c封装了数字信封；p_open.c封装了解数字信封。
        6） 基于口令的加密
            包括p5_crpt2.c、p5_crpt.c和evp_pbe.c。
    摘要函数
        '典型的'摘要函数主要有：
        1）  EVP_md5 
             返回md5的EVP_MD。
        2)   EVP_sha1
             返回sha1的EVP_MD。
        3)   EVP_sha256
             返回sha256的EVP_MD。
        4）  EVP_DigestInit
             摘要初使化函数，需要有EVP_MD作为输入参数。
        5）  EVP_DigestUpdate和EVP_DigestInit_ex
             摘要Update函数，用于进行多次摘要。
        6）  EVP_DigestFinal和EVP_DigestFinal_ex
             摘要Final函数，用户得到最终结果。
        7）  EVP_Digest
             对一个数据进行摘要，它依次调用了上述三个函数。
    对称加解密函数
        '典型的'加解密函数主要有：
        1）  EVP_CIPHER_CTX_init
             初始化对称计算上下文。
        2）  EVP_CIPHER_CTX_cleanup
             清除对称算法上下文数据，它调用用户提供的销毁函数销清除存中的内部密钥以及其他数据。
        3）  EVP_des_ede3_ecb
             返回一个EVP_CIPHER；
        4)   EVP_EncryptInit和EVP_EncryptInit_ex
             加密初始化函数，本函数调用具体算法的init回调函数，
             将外送密钥key转换为内部密钥形式，将初始化向量iv拷贝到ctx结构中。
        5）  EVP_EncryptUpdate
             加密函数，用于多次计算，它调用了具体算法的do_cipher回调函数。
        6）  EVP_EncryptFinal和EVP_EncryptFinal_ex
             获取加密结果，函数可能涉及填充，它调用了具体算法的do_cipher回调函数。
        7）  EVP_DecryptInit和EVP_DecryptInit_ex
             解密初始化函数。
        8）  EVP_DecryptUpdate
             解密函数，用于多次计算，它调用了具体算法的do_cipher回调函数。
        9）  EVP_DecryptFinal和EVP_DecryptFinal_ex
             获取解密结果，函数可能涉及去填充，它调用了具体算法的do_cipher回调函数。
        10） EVP_BytesToKey
             计算密钥函数，它根据算法类型、摘要算法、salt以及输入数据计算出一个对称密钥和初始化向量iv。
        11） PKCS5_PBE_keyivgen和PKCS5_v2_PBE_keyivgen
             实现了PKCS5基于口令生成密钥和初始化向量的算法。
        12） PKCS5_PBE_add
             加载所有openssl实现的基于口令生成密钥的算法。
        13） EVP_PBE_alg_add
             添加一个PBE算法。
    非对称函数
        '典型的'非对称函数有：
        1）  EVP_PKEY_encrypt
             公钥加密。
        2)   EVP_PKEY_decrypt
             私钥解密。
        3)   EVP_PKEY_assign
             设置EVP_PKEY中具体的密钥结构，使它代表该密钥。
        4)   EVP_PKEY_assign_RSA/ EVP_PKEY_set1_RSA
             设置EVP_PKEY中的RSA密钥结构，使它代表该RSA密钥。
        5)   EVP_PKEY_get1_RSA
             获取EVP_PKEY的RSA密钥结构。
        6)   EVP_SignFinal
             签名操作，输入参数必须有私钥(EVP_PKEY)。
        7)   EVP_VerifyFinal
             验证签名，输入参数必须有公钥(EVP_PKEY)。
        8)   int EVP_OpenInit(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *type,
                              const unsigned char *ek, int ekl, 
                              const unsigned char *iv,EVP_PKEY *priv)
             解数字信封初始化操作，type为对称加密算法，ek为密钥密文，
             ekl为密钥密文长度，iv为填充值，priv为用户私钥。
        9)   EVP_OpenUpdate
             做解密运算。
        10)  EVP_OpenFinal
             做解密运算，解开数字信封。
        11)  int EVP_SealInit(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *type, 
                              unsigned char **ek,int *ekl, unsigned char *iv, 
                              EVP_PKEY **pubk, int npubk)
             type为对称算法，ek数组用来存放多个公钥对密钥加密的结果，
             ekl用于存放ek数组中每个密钥密文的长度，iv为填充值，pubk数组用来存放多个公钥，
             npubk为公钥个数，本函数用多个公钥分别加密密钥，并做加密初始化。
        12） EVP_SealUpdate
             做加密运算。
        13） EVP_SealFinal
             做加密运算，制作数字信封。
     BASE64编解码函数
        1)   EVP_EncodeInit
             BASE64编码初始化。
        2)   EVP_EncodeUpdate
             BASE64编码，可多次调用。
        3)   EVP_EncodeFinal
             BASE64编码，并获取最终结果。
        4)   EVP_DecodeInit
             BASE64解码初始化。
        5)   EVP_DecodeUpdate
             输入数据长度不能大于80字节。BASE64解码可多次调用，注意，本函数的输入数据不能太长。
        6)   EVP_DecodeFinal
             BASE64解码，并获取最终结果。
        7）  EVP_EncodeBlock
             BASE64编码函数，本函数可单独调用。
        8）  EVP_DecodeBlock
             BASE64解码，本函数可单独调用，对输入数据长度无要求。
     其他函数
        1）  EVP_add_cipher
             将对称算法加入到全局变量，以供调用。
        2）  EVP_add_digest
             将摘要算法加入到全局变量中，以供调用。
        -------------------------------------------------------------------------     
        3)   EVP_CIPHER_CTX_ctrl
             对称算法控制函数，它调用了用户实现的ctrl回调函数。
        4)   EVP_CIPHER_CTX_set_key_length
             当对称算法密钥长度为可变长时，设置对称算法的密钥长度。
        5)   EVP_CIPHER_CTX_set_padding
             设置对称算法的填充，对称算法有时候会涉及填充。
             加密分组长度大于一时，用户输入数据不是加密分组的整数倍时，会涉及到填充。
             填充在最后一个分组来完成，openssl分组填充时，如果有n个填充，则将最后一个分组用n来填满。
        6)   EVP_CIPHER_get_asn1_iv
             获取原始iv，存放在ASN1_TYPE结构中。
        7)   EVP_CIPHER_param_to_asn1
             设置对称算法参数，参数存放在ASN1_TYPE类型中，
             它调用用户实现的回调函数set_asn1_parameters来实现。
        8)   EVP_CIPHER_type
             获取对称算法的类型。
        9）  EVP_CipherInit/EVP_CipherInit_ex
             对称算法计算(加/解密)初始化函数，_ex函数多了硬件enginge参数，
             EVP_EncryptInit和EVP_DecryptInit函数也调用本函数。
        10)  EVP_CipherUpdate
             对称计算（加/解密）函数，它调用了EVP_EncryptUpdate和EVP_DecryptUpdate函数。
        11） EVP_CipherFinal/EVP_CipherFinal_ex
             对称计算(加/解)函数，调用了EVP_EncryptFinal（_ex）和EVP_DecryptFinal(_ex）；
             本函数主要用来处理最后加密分组，可能会有对称计算。
        -------------------------------------------------------------------------     
        12） EVP_cleanup
             清除加载的各种算法，包括对称算法、摘要算法以及PBE算法，并清除这些算法相关的哈希表的内容。
        -------------------------------------------------------------------------     
        13)  EVP_get_cipherbyname
             根据字串名字来获取一种对称算法(EVP_CIPHER)，本函数查询对称算法哈希表。
        14)  EVP_get_digestbyname
             根据字串获取摘要算法(EVP_MD)，本函数查询摘要算法哈希表。
        -------------------------------------------------------------------------     
        15)  EVP_get_pw_prompt
             获取口令提示信息字符串.
        -------------------------------------------------------------------------     
        16） int EVP_PBE_CipherInit(ASN1_OBJECT *pbe_obj, const char *pass, int passlen,
                                    ASN1_TYPE *param, EVP_CIPHER_CTX *ctx, int en_de)
             PBE初始化函数。本函数用口令生成对称算法的密钥和初始化向量，并作加/解密初始化操作。
             本函数再加上后续的EVP_CipherUpdate以及EVP_CipherFinal_ex构成一个完整的加密过程
             （可参考crypto/p12_decr.c的PKCS12_pbe_crypt函数）.
        17)  EVP_PBE_cleanup
             删除所有的PBE信息，释放全局堆栈中的信息.
        -------------------------------------------------------------------------     
        18） EVP_PKEY *EVP_PKCS82PKEY(PKCS8_PRIV_KEY_INFO *p8)
             将PKCS8_PRIV_KEY_INFO(x509.h中定义)中保存的私钥转换为EVP_PKEY结构。
        19)  EVP_PKEY2PKCS8/EVP_PKEY2PKCS8_broken
             将EVP_PKEY结构中的私钥转换为PKCS8_PRIV_KEY_INFO数据结构存储。
        20)  EVP_PKEY_bits
             非对称密钥大小，为比特数。
        21)  EVP_PKEY_cmp_parameters
             比较非对称密钥的密钥参数，用于DSA和ECC密钥。
        22） EVP_PKEY_copy_parameters
             拷贝非对称密钥的密钥参数，用于DSA和ECC密钥。
        23） EVP_PKEY_free
             释放非对称密钥数据结构。
        24)  EVP_PKEY_get1_DH/EVP_PKEY_set1_DH
             获取/设置EVP_PKEY中的DH密钥。
        25)  EVP_PKEY_get1_DSA/EVP_PKEY_set1_DSA
             获取/设置EVP_PKEY中的DSA密钥。
        26） EVP_PKEY_get1_RSA/EVP_PKEY_set1_RSA
             获取/设置EVP_PKEY中结构中的RSA结构密钥。
        27)  EVP_PKEY_missing_parameters
             检查非对称密钥参数是否齐全，用于DSA和ECC密钥。
        28)  EVP_PKEY_new
             生成一个EVP_PKEY结构。
        29)  EVP_PKEY_size
             获取非对称密钥的字节大小。
        30)  EVP_PKEY_type
             获取EVP_PKEY中表示的非对称密钥的类型。
        31)  int EVP_read_pw_string(char *buf,int length,const char *prompt,int verify)
             获取用户输入的口令；buf用来存放用户输入的口令，length为buf长度，
             prompt为提示给用户的信息，如果为空，它采用内置的提示信息，verify为0时，
             不要求验证用户输入的口令，否则回要求用户输入两遍。返回0表示成功。
        32)  EVP_set_pw_prompt
             设置内置的提示信息，用于需要用户输入口令的场合。
    对称加密过程
       对称加密过程如下：    
        1）  EVP_EncryptInit：
             设置buf_len为0，表明临时缓冲区buf没有数据。
        2）  EVP_EncryptUpdate：
             ctx结构中的buf缓冲区用于存放上次EVP_EncryptUpdate遗留下来的未加密的数据，buf_len指明其长度。
             如果buf_len为0，加密的时候先加密输入数据的整数倍，将余下的数据拷贝到buf缓冲区。
             如果buf_len不为0，先加密buf里面的数据和输入数据的一部分（凑足一个分组的长度），
             然后用上面的方法加密，输出结果是加过密的数据。
        3）  EVP_EncryptFinal
             加密ctx的buf中余下的数据，如果长度不够一个分组（分组长度不为1），则填充，然后再加密，输出结果。
             总之，加密大块数据（比如一个大的文件，多出调用EVP_EncryptUpdate）
             的结果等效于将所有的数据一次性读入内存进行加密的结果。
             加密和解密时每次计算的数据块的大小不影响其运算结果。
     编程示例
        略
            
第二十二章 PEM
    它是openssl默认采用的信息存放方式
    Openssl生成PEM格式文件的大致过程如下：
        1)    将各种数据DER编码；
        2)    将1）中的数据进行加密处理（如果需要）；
        3)    根据类型以及是否加密，构造PEM头；
        4)    将2）中的数据进行BASE64编码，放入PEM文件。
    openssl的PEM实现
        Openssl的PEM模块实现位于crypto/pem目录下，并且还依赖于openssl的ASN1模块
        Openssl支持的PEM类型(在crypto/pem/pem.h中定义)如下：
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
    PEM函数
        1)  PEM_write_XXXX/PEM_write_bio_XXXX
            将XXXX代表的信息类型写入到文件/bio中。
        2)  PEM_read_XXXX/PEM_read_bio_XXXX
            从文件/bio中读取PEM的XXXX代表类型的信息。
            XXXX可用代表的有：
                SSL_SESSION、X509、X509_REQ、X509_AUX、X509_CRL、RSAPrivateKey、
                RSAPublicKey、DSAPrivateKey、PrivateKey、PKCS7、DHparams、
                NETSCAPE_CERT_SEQUENCE、PKCS8PrivateKey、DSAPrivateKey、
                DSA_PUBKEY、DSAparams、ECPKParameters、ECPrivateKey、EC_PUBKEY等。
        3)  PEM_ASN1_read/PEM_ASN1_read_bio
            比较底层的PEM读取函数，2）中的函数都调用了这两个函数。
        4)  PEM_ASN1_write/PEM_ASN1_write_bio
            比较底层的PEM读取函数，1)中的函数都调用了这两个函数。
        5） PEM_read_bio
            读取PEM文件的各个部分，包括文件类型、头信息以及消息体(base64解码后的结果）。
        6） PEM_get_EVP_CIPHER_INFO
            根据头信息获取对称算法，并加载初始化向量iv。
        7)  PEM_do_header
            根据对称算法，解密数据。
        8)  PEM_bytes_read_bio
            获取PEM数据，得到的结果为一个DER编码的明文数据，该函数先后调用了5)、6）和7）函数。
        Openssl各个类型的PEM处理函数主要是write和read函数。
        write函数用于生成PEM格式的文件，而read函数主要用于读取PEM格式的文件。
    
第二十三章 引擎
    Openssl硬件引擎(Engine）能够使用户比较容易地将自己的硬件加入到openssl中去，替换其提供的软件算法。
    一个Engine提供了密码计算中各种计算方法的集合，它用于控制openssl的各种密码计算。
    Engine支持的原理
        Openssl中的许多数据结构不仅包含数据本身，还包含各种操作，并且这些操作是可替换的。
        Openssl中这些结构集合一般叫做XXX_METHOD，有DSO_METHOD、DSA_METHOD、EC_METHOD、
        ECDH_METHOD、ECDSA_METHOD、DH_METHOD、RAND_METHOD、 RSA_METHOD、EVP_CIPHER和EVP_MD等。
        以RSA结构为例(crypto/rsa/rsa.h)，RSA结构不仅包含了大数n、e、d和p等等数据项目，
        还包含一个RSA_METHOD回调函数集合。该方法给出了RSA各种运算函数。
        对于各种数据类型，要进行计算必须至少有一个可用的方法(XXX_METHOD)。
        因此，openssl对各种类型都提供了默认的计算方法(软算法)。
        如果用户实现了自己的XXX_METHOD，那么就能替换openssl提供的方法，各种计算由用户自己控制。
        硬件Engine就是这种原理。
        根据需要，一个硬件Engine可实现自己的RAND_METHOD、RSA_METHOD、EVP_CIPHER、
        DSA_METHOD、DH_METHOD、ECDH_METHOD和EVP_MD等，来替换对应软算法的METHOD。
    Engine数据结构
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
            /* 其他项 */
            int struct_ref;
            CRYPTO_EX_DATA ex_data;
            struct engine_st *prev;
            struct engine_st *next;
        };
        本结构包含大量的运算集合函数(包括各种METHOD)供用户来实现。各项意义如下：
            id：         Engine标识；
            name：       Engine的名字；
            rsa_meth：   RSA方法集合；
            dsa_meth：   DSA方法集合；
            dh_meth：    DH方法集合；
            ecdh_meth：  ECDH方法结合；
            ecdsa_meth： ECDSA方法集合；
            rand_meth：  随机数方法集合；
            store_meth： 存储方法集合；
            ciphers：    对称算法选取函数。硬件一般会支持多种对称算法，该回调函数用来从
                         用户实现的多个对称算法中根据某种条件(一般是算法nid)来选择其中的一种；
            digests：    摘要算法选取函数。该回调函数用来从用户实现的多个摘要算法中
                         根据某种条件(一般是算法nid)来选择其中的一种；
            destroy：    销毁引擎函数；
            init：       初始化引擎函数；
            finish：     完成回调函数；
            ctrl：       控制函数；
            load_privkey：加载私钥函数；
            load_pubkey：加载公钥函数；
            struct_ref： 引用计数
            ex_data：    扩展数据结构，可用来存放用户数据；
            prev/next：  用于构建Engine链表，openssl中的硬件Engine可能不止一个。
            上述这些函数，用户根据应用的需求来实现其中的一种或多种。
    openssl 的Engine源码
        Openssl的Engine源码分为四类：
        1） 核心实现
            在crypto/engine目录下，是其核心实现。
            当同时有多个硬件Engine时，openssl分别为cipher对称算法(tb_cipher.c)、
            dh算法(tb_dh.c)、digest摘要算法(tb_digest.c)、dsa算法(tb_dsa.c)、
            ecdh算法(tb_ecdh.c)、ecdsa算法(tb_ecdsa.c)、rand随机数算法(tb_rand.c)、
            rsa算法(tb_rsa.c)和存储方式(tb_store.c)维护一个哈希表。
            所有用户实现的硬件Engine都注册在这些全局的哈希表中。
            同时，用户使用的时候，能够指定各种算法默认的硬件Engine。
        2） 内置硬件Engine
            源码位于engines目录，实现了一些硬件Engine。
        3)  范例
            源码位于demos/engines目录下，供用户学习参考。
        4） 分散于其他各个运算模块用于支持Engine
            各个运算模块都支持Engine，当提供了Engine时，将会采用Engine中的算法。
    Engine函数(包括定义、实现、使用各方面)
        主要函数如下：
        1)  ENGINE_add
            将Engine加入全局到链表中。
        2)  ENGINE_by_id
            根据id来获取Engine。
        3） ENGINE_cleanup
            清除所有Engine数据。
        4） const EVP_CIPHER *ENGINE_get_cipher(ENGINE *e, int nid)
            根据指定的硬件Engine以及对称算法的nid，获取Engine实现的对应的     EVP_CIPHER，用于对称计算。
        5） ENGINE_get_cipher_engine
            根据对称算法nid来获取Engine。
        6） ENGINE_get_ciphers/ENGINE_set_ciphers
            获取/设置指定Engine的对称算法选取函数地址，该函数用于从Engine中选择一种对称算法。
        7)  ENGINE_get_ctrl_function
            获取Engine的控制函数地址。
        8） const DH_METHOD *ENGINE_get_DH(const ENGINE *e)
            获取Engine的DH_METHOD。
        9） const EVP_MD *ENGINE_get_digest(ENGINE *e, int nid)
            根据Engine和摘要算法nid来获取Engine中实现的摘要方法EVP_MD。
        10) ENGINE *ENGINE_get_digest_engine(int nid)
            根据摘要算法nid来获取Engine。
        11）ENGINE_get_digests/ENGINE_set_digests
            获取/设置指定Engine的摘要算法选取函数地址，该函数用于从Engine中选择一种摘要算法。
        12) const DSA_METHOD *ENGINE_get_DSA(const ENGINE *e)
            获取Engine的DSA方法。
        13) int ENGINE_register_XXX(ENGINE *e)
            注册函数，将某一个Engine添加到对应方法的哈希表中。
        14) void ENGINE_unregister_XXX(ENGINE *e)
            将某一个Engine从对应的哈希表中删除。
        15) void ENGINE_register_all_XXX(void)
            将所有的Engine注册到对应方法的哈希表中。
        16）ENGINE_set_default_XXXX
            设置某Engine为对应XXXX方法的默认Engine。
        17) ENGINE_get_default_XXXX
            获取XXXX方法的默认Engine。
        18）ENGINE_load_XXXX
            加载某种Engine。
        19) ENGINE_get_RAND/ENGINE_set_RAND
            获取/设置Engine的随机数方法。
        20) ENGINE_get_RSA/ENGINE_set_RSA
            获取/设置Engine的RSA方法。
        21) ENGINE_get_first/ENGINE_get_next/ENGINE_get_prev/ENGINE_get_last
            Engine链表操作函数。
        22）ENGINE_set_name/ENGINE_get_name
            设置/获取Engine名字。
        23）ENGINE_set_id/ENGINE_get_id
            设置/获取Engine的id。
        24) int ENGINE_set_default(ENGINE *e, unsigned int flags)
            根据flags将e设置为各种方法的默认Engine。
        25) ENGINE_set_XXX_function
            设置Engine中XXX对应的函数。
        26) ENGINE_get_XXX_function
            获取Engine中XXX对应的函数。
        27) ENGINE_ctrl
            Engine控制函数。
        28) ENGINE_get_ex_data/ENGINE_set_ex_data
            获取/设置Engine的扩展数据。
        29）ENGINE_init/ENGINE_finish
            Engine初始化/结束。
        30）ENGINE_up_ref
            给Engine增加一个引用。
        31）ENGINE_new/ENGINE_free
            生成/释放一个Engine数据结构。
        32）ENGINE_register_complete
            将给定的Engine，对于每个方法都注册一遍。
        33）ENGINE_register_all_complete
            将所有的Engine，对于每个方法都注册一遍。
    实现Engine示例
        以下的示例演示了采用Engine机制，来改变openssl的各种运算行为。
        实现的Engine方法有：随机数方法、对称算法、摘要算法以及RSA运算算法。
        其中，RSA计算中，密钥ID存放在Engine的扩展数据结构中。
        file://Openssl引擎示例.c
    引擎编写
        https://blog.csdn.net/cqwei1987/article/details/107423111
        OpenSSL引擎分为两类：动态引擎，Version => 0.9.7、静态引擎，0.9.7 <= Version < 1.1.0
        以下介绍以动态Engine为例
        1. AES引擎
            Openssl定义好的主接口
            1. AES引擎
                Openssl定义好的主接口
                IMPLEMENT_DYNAMIC_BIND_FN(bind)
                IMPLEMENT_DYNAMIC_CHECK_FN()
                只需自定义bind函数即可，而bind函数的定义如下所示：
                Static int bind(ENGINE *e)
                {
                    available();                            //自定义函数，用于一些硬件实现时检查硬件是否支持，可选
                    ENGINE_set_id(e,id);                    //设置ENGINE的唯一性ID
                    ENGINE_set_name(e,name);                //设置ENGINE可识别名字
                    ENGINE_set_init_function(e,init_func);  //加解密算法的初始化工作，内容可为空
                    ENGINE_set_cipher(e,cipher_func);       //加解密算法的真实实现
                }
                可以发现其中最为重要的是cipher_func函数，其定义如下所示：
                static int cipher_func(ENGINE *e, const EVP_CIPHER **cipher, const int **nids, int nid){}
                其中，EVP_CIPHER的定义如下图所示，do_cipher 函数是算法过程的真正实现过程。
                file://imgs/EVP_CIPHER的定义.png
                测试方法：
                openssl enc -aes-128-ecb -nopad -in plain -out cipher -e 
                            -K 0123456789ABCDEFFEDCBA9876543210 -engine `pwd`/SM4.so
    编写 OpenSSL Engine
        https://blog.csdn.net/enlaihe/article/details/110474705
        除了国际算法，实际应用中可能有国密算法的需求，
        例如部分应用中需要使用国密套件SM2-WITH-SMS4-SM3进行TLS连接。
        本文将使用GmSSL完成引擎的实现。
        本文的示例代码可参考 gmssl_engine
        OpenSSL提供了引擎相关Demo，编写引擎时首先通过ENGINE_set_xxx接口完成引擎相关信息及接口的配置：
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
        通过IMPLEMENT_DYNAMIC_BIND_FN宏定义完成引擎的注册：
        IMPLEMENT_DYNAMIC_BIND_FN(bind_gmssl_engine)
        IMPLEMENT_DYNAMIC_CHECK_FN()
        这样只需要实现引擎中注册的相关接口即可，
        例如前面通过 ENGINE_set_pkey_meths 接口设置的 gmssl_engine_pkey 接口。
        以Pkey接口为例，通过 EVP_PKEY_meth_set_xxx 接口完成PKEY方法的注册。
        这里也可以通过PKEY的子方法完成注册，
        例如ECC相关的EC_KEY_METHOD，OpenSSL speed速度测试中直接调用字方法完成，
        这样的好处是可以使用speed工具完成性能测试，
        但PKEY接口更加通用，将公钥算法全部包含在内，
        目前GmSSL支持的公钥算法相关NID如下：
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
        OpenSSL还支持异步模式，引擎中需要增加ASYNC_xxx相关接口完成挂起以及唤醒操作，
        在异步模式过程中，首先通过ASYNC_start_job接口创建异步Job，
        引擎相关加速接口中将任务卸载到硬件后通过ASYNC_get_wait_ctx接口得到当前异步job，
        并通过ASYNC_WAIT_CTX_get_fd接口得到异步句柄，通过读取异步句柄的方式将任务挂起，
        当硬件计算完成后通过回调函数将任务唤醒继续执行，该过程和将人物挂起的流程类似，
        通过写异步句柄的方式将人物唤醒。由于示例代码中没有使用硬件设备，
        异步模式没有进行添加，但在实际应用中确非常重要。
    利用ENGINE替换OPENSSL中的加解密算法
        https://blog.csdn.net/bytxl/article/details/39498769
        一：ENGINE的目的：
            如果要使用Engine（假设你已经加载上该Engine了），那么首先要Load该Engine(比如ENGINE_load_XXXX)，
            然后选择要使用的算法或者使用支持的所有加密算法（有相关函数）。
            这样你的应用程序在调用加解密算法时，它就会指向你加载的动态库里的加解密算法，
            而不是原先的OPENSSL的libeay32.dll库里的加解密算法。
        二：ENGINE原理：
            使用你自己编译的加解密动态库里的函数的指针或硬件接口指针来替换OPENSSL中默认的加解密函数
        三：ENGINE操作流程：
            例如替换RSA：
            1 声明你要替换的函数名称和其它内部使用的函数
            2 声明RSA_Method结构，要替换的函数就提供函数名，不提换就是NULL了，还有其它的类型也要填上；
            3 利用Engine_init等一系列函数初始化ENGINE库（其实上就是在初始化加解密算法），
              主要是绑定特定的函数指针（自定义）和结构或初始化硬件设备等等操作；
              Engine_finish也是一样，做一些清理工作；
            4 实现真正的接口，包括RSA密钥结构的转换，如果是不能取出的私钥，
              要保存硬件设备提供的指针（通常是HANDLE）等等操作。然后调用硬件的加密解密函数。
        四：程序实例：（实现ENGINE）
        
第三十一章 SSL实现
    概述
        SSL协议最先由netscape公司提出，包括sslv2和sslv3两个版本
        当前形成标准的为tls协议（rfc2246规范）和DTLS协议（rfc4347，用于支持UDP协议）。
        sslv3和tls协议大致一样，只是有一些细微的差别。实际应用中，用的最多的为sslv3。
        SSL协议能够保证通信双方的信道安全。
        它能提供数据加密、身份认证以及消息完整性保护，另外SSL协议还支持数据压缩。
        SSL协议通过客户端和服务端握手来协商各种算法和密钥。
    openssl对ssl协议的实现
        SSL协议源码位于ssl目录下。它实现了sslv2、sslv3、TLS以及DTLS（Datagram TLS，基于UDP的TLS实现）
        ssl实现中，对于每个协议，都有客户端实现(XXX_clnt.c)、服务端实现(XXX_srvr.c)、
        加密实现(XXX_enc.c)、记录协议实现(XXX_pkt.c)、METHOD方法(XXX_meth.c)、
        客户端服务端都用到的握手方法实现(XXX_both.c)，以及对外提供的函数实现(XXX_lib.c)，
    搭建ssl测试环境
        略
    数据结构
        ssl的主要数据结构定义在ssl.h中。
        主要的数据结构有SSL_CTX、SSL和SSL_SESSION。
        SSL_CTX 数据结构主要用于SSL握手前的环境准备，设置CA文件和目录、
        设置SSL握手中的证书文件和私钥、设置协议版本以及其他一些SSL握手时的选项。
        SSL 数据结构主要用于SSL握手以及传送应用数据。
        SSL_SESSION中保存了主密钥、session id、读写加解密钥、读写MAC密钥等信息。
        SSL_CTX中缓存了所有SSL_SESSION信息，SSL中包含SSL_CTX。
        一般SSL_CTX的初始化在程序最开始调用，然后再生成SSL数据结构。
        由于SSL_CTX中缓存了所有的SESSION，新生成的SSL结构又包含SSL_CTX数据，
        所以通过SSL数据结构能查找以前用过的SESSION id，实现SESSION重用。
        另外，SSL_METHOD中是个包含了一系列ssl函数指针的结构体
        SSL_CIPHER用于维护密码算法的相关信息
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
    加密套件
        一个加密套件指明了SSL握手阶段和通信阶段所应该采用的各种算法。
        这些算法包括：认证算法、密钥交换算法、对称算法和摘要算法等。
        在握手初始化的时候，双方都会导入各自所认可的多种加密套件。
        在握手阶段，由服务端选择其中的一种加密套件。
        OpenSSL的ciphers命令可以列出所有的加密套件
        openssl的加密套件在s3_lib.c的ssl3_ciphers数组中定义
        比如有：
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
            其中1表示是合法的加密套件；
            SSL3_TXT_RSA_RC4_128_SHA为加密套件的名字，
            SSL3_CK_RSA_RC4_128_SHA为加密套件ID，
            SSL_kRSA|SSL_aRSA|SSL_RC4|SSL_SHA1|SSL_SSLV3表明了各种算法，
            其中密钥交换采用RSA算法（SSL_kRSA），
            认证采用RSA算法（SSL_aRSA），
            对称加密算法采用RC4算法(SSL_RC4)，
            摘要采用SHA1，
            采用SSL协议第三版本，
            SSL_NOT_EXP|SSL_MEDIUM表明算法的强度。
        在客户端和服务器端建立安全连接之前，双方都必须指定适合自己的加密套件。
        加密套件的选择可以通过组合的字符串来控制。
        字符串的形式举例：ALL:!ADH:RC4+RSA:+SSLv2:@STRENGTH。
        Openssl定义了4中选择符号：“＋”，“－”，“！”，“@”。
        其中，“＋”表示取并集；“－”表示临时删除一个算法；“！”表示永久删除一个算法；“@“表示了排序方法。
        多个描述之间可以用“：” 或 “，” 或 “ ” 或 “；”来分开。
        选择加密套件的时候按照从左到的顺序构成双向链表，存放与内存中
        上例表示的意思是：
            首先选择所有的加密套件（不包含eNULL，即空对称加密算法），
            然后在得到的双向链表之中去掉身份验证采用DH的加密套件；
            将包含RC4算法且包含RSA算法的加密套件放在双向链表的尾部；
            再将支持SSLV2的加密套件放在尾部；
            最后得到的结果按照安全强度进行排序。
        SSL建立链接之前，客户端和服务器端用openssl函数来设置自己支持的加密套件。主要的函数有：
        int SSL_set_cipher_list(SSL *s,const char *str)；
        int SSL_CTX_set_cipher_list(SSL_CTX *ctx, const char *str)；
        如果服务端只设置了一种加密套件，那么客户端要么接受要么返回错误。
        加密套件的选择是由服务端做出的。
    秘钥信息
        ssl中的密钥相关信息包括：预主密钥、主密钥、读解密密钥及其iv、写加密密钥及其iv、读MAC密钥、写MAC密钥。
        1)  预主密钥
            预主密钥是主密钥的计算来源。它由客户端生成，采用服务端的公钥加密发送给服务端。
            以sslv3为例，预主密钥的生成在源代码 s3_clnt.c 的 ssl3_send_client_key_exchange 函数中，
            有源码如下：
                tmp_buf[0] = s->client_version>>8;
                tmp_buf[1] = s->client_version&0xff;
                if (RAND_bytes(&(tmp_buf[2]),sizeof tmp_buf-2) <= 0)
                    goto err;
                s->session->master_key_length = sizeof tmp_buf;
                ……
                n=RSA_public_encrypt(sizeof tmp_buf,tmp_buf,p,rsa,RSA_PKCS1_PADDING);
                此处，tmp_buf中存放的就是预主密钥。
        2)  主密钥
            主密钥分别由客户端和服务端根据预主密钥、客户端随机数和服务端随机数来生成，他们的主密钥是相同的。
            主密钥用于生成各种密钥信息，它存放在SESSION数据结构中。由于协议版本不同，生成方式也不同。
            sslv3的源代码中，它通过ssl3_generate_master_secret函数生成，
            tlsv1中它通过tls1_generate_master_secret函数来生成。
        3)  对称密钥和MAC密钥
            对称密钥（包括IV）和读写MAC密钥通过主密钥、客户端随机数和服务端随机数来生成。
            sslv3源代码中，它们在ssl3_generate_key_block中生成，在ssl3_change_cipher_state中分配。
    SESSION
        当客户端和服务端在握手中新建了session，
        服务端生成一个session ID，通过哈希表缓存SESSION信息，并通过server hello消息发送给客户端。
        此ID是一个随机数，SSL v2版本时长度为16字节，SSLv3和TLSv1长度为32字节。
        此ID与安全无关，但是在服务端必须是唯一的。
        当需要session重用时，客户端发送包含session id的clientHello消息（无sesion重用时，此值为空）给服务端，
        服务端可用根据此ID来查询缓存。
        session重用可以免去诸多SSL握手交互，特别是客户端的公钥加密和服务端的私钥解密所带来的性能开销。
        session的默认超时时间为60*5+4秒，5分钟。
        session相关函数有：
            1) int SSL_has_matching_session_id(const SSL *ssl, const unsigned char *  id,unsigned int id_len)
                SSL中查询session id，id和 id_len为输入的要查询的session id，
                查询哈希表ssl->ctx->sessions，如果匹配，返回1，否则返回0。
            2）int ssl_get_new_session(SSL *s, int session)
                生成ssl用的session，此函数可用被服务端或客户端调用，
                当服务端调用时，传入参数session为1，生成新的session；
                当客户端调用时，传入参数session为0，只是简单的将session id的长度设为0。
            3) int ssl_get_prev_session(SSL *s, unsigned char *session_id, int len)
                获取以前用过的session id，用于服务端session重用，
                本函数由服务端调用，session_id为输入senssion ID首地址，len为其长度，
                如果返回1，表明要session重用；返回0，表示没有找到；返回-1表示错误。
            4) int SSL_set_session(SSL *s, SSL_SESSION *session)
                设置session，本函数用于客户端，用于设置session信息；
                如果输入参数session为空值，它将置空s->session；
                如果不为空，它将输入信息作为session信息。
            5) void SSL_CTX_flush_sessions(SSL_CTX *s, long t)
                清除超时的SESSION，输入参数t指定一个时间，
                如果t=0,则清除所有SESSION，一般用time(NULL)取当前时间。
                此函数调用了哈希表函数lh_doall_arg来处理每一个SESSION数据。
            6) int ssl_clear_bad_session(SSL *s)
                清除无效SESSION。
    多线程支持
        编写openssl多线程程序时，需要设置两个回调函数：
        CRYPTO_set_id_callback((unsigned long (*)())pthreads_thread_id);
            用于记录当前正在执行线程的id
            函数实现不应直接填充id参数，而应该
        CRYPTO_set_locking_callback((void (*)())pthreads_locking_callback);
            用于完成对共享数据结构的锁操作
            该函数必须有能力处理CRYPTO_num_locks()个互斥锁
        对于多线程程序的写法，读者可以参考crypto/threads/mttest.c
    函数
        1） SSL_accept
            对应于socket函数accept，该函数在服务端调用，用来进行SSL握手。
        2） int SSL_add_client_CA(SSL *ssl,X509 *x)
            添加客户端CA名。
        3） const char *SSL_alert_desc_string_long(int value)
            根据错误号得到错误原因。
        4） SSL_check_private_key
            检查SSL结构中的私钥。
        5） SSL_CIPHER_description
            获取SSL加密套件描述。
        6） SSL_CIPHER_get_bits
            获取加密套件中对称算法的加密长度。
        7） SSL_CIPHER_get_name
            得到加密套件的名字。
        8） SSL_CIPHER_get_version
            根据加密套件获取SSL协议版本。
        9） SSL_clear
            清除SSL结构。
        10) SSL_connect
            对应于socket函数connect，该函数在客户端调用，用来进行SSL握手。
        11) SSL_CTX_add_client_CA
            给SSL_CTX添加客户端CA。
        12) int SSL_CTX_add_session(SSL_CTX *ctx, SSL_SESSION *c)
            往SSL_CTX添加session。
        13) SSL_CTX_check_private_key
            检查私钥。
        14) SSL_CTX_free
            释放SSL_CTX空间。
        15) long SSL_CTX_get_timeout(const SSL_CTX *s)
            获取超时时间。
        16) SSL_CTX_get_verify_callback
            获取证书验证回调函数。
        17) SSL_CTX_get_verify_depth
            获取证书验证深度。
        18）SSL_CTX_get_verify_mode
            获取验证方式，这些值在ssl.h中定义如下：
            #define SSL_VERIFY_NONE                 0x00
            #define SSL_VERIFY_PEER                 0x01
            #define SSL_VERIFY_FAIL_IF_NO_PEER_CERT 0x02
            #define SSL_VERIFY_CLIENT_ONCE          0x04
        19）SSL_get_current_cipher
            获取当前的加密套件。
        20）SSL_get_fd
            获取链接句柄。
        21）SSL_get_peer_certificate
            获取对方证书。
        22）XXX_client/server_method
            获取各个版本的客户端和服务端的SSL方法。
        23）SSL_read
            读取数据。
        24) SSL_write
            发送数据。
        25）SSL_set_fd
            设置SSL的链接句柄。
        26）SSL_get_current_compression
            获取当前的压缩算法的COMP_METHOD。
        27）SSL_get_current_expansion
            获取当前的解压算法的COMP_METHOD。
        28）SSL_COMP_get_name
            获取压缩/解压算法的名称。
        29）SSL_CTX_set/get_ex_data
            设置/读取用户扩展数据。
        30）SSL_dup
            复制函数。
        31）SSL_get_default_timeout
            获取默认超时时间。
        32）SSL_do_handshake
            进行ssl握手。
    示例
        file://ssl_server.cpp | file://ssl_client.cpp
        
第三十二章 OpenSSL命令
    asn1parse   是一种用来诊断ASN.1结构的工具，也能用于从ASN1.1数据中提取数据
    dgst        用于数据摘要
    gendh       此命令用于生成DH参数。
    passwd      生成各种口令密文
    rand        生成随机数   
    genrsa      生成RSA密钥
    req         主要用于生成和处理PKCS#10证书请求
    x509        是一个多用途的证书工具。它可以显示证书信息、转换证书格式、签名证书请求以及改变证书的信任设置等。
    version     印版本以及openssl其他各种信息
    speed       用于测试库的性能
    sess_id     SSL/TLS协议的session处理工具。
    s_server    openssl提供的一个SSL服务程序。使用此程序前，需要生成各种证书; 
                本命令可以用来测试ssl客户端，比如各种浏览器的https协议支持
    s_client    一个SSL/TLS客户端程序，与s_server对应，
                它不仅能与s_server进行通信，也能与任何使用ssl协议的其他服务程序进行通信。
    rsa         用于处理RSA密钥、格式转换和打印信息
    pkcs7       用于处理DER或者PEM格式的pkcs#7文件
    dsaparam    用于生成和操作dsa参数
    gendsa      根据DSA密钥参数生成DSA密钥，dsa密钥参数可用dsaparam命令生成
    enc         对称加解密工具，还可以进行base64编码转换
    ciphers     显示支持的加密套件
    CA          是一个小型CA系统。它能签发证书请求和生成CRL。它维护一个已签发证书状态的文本数据库。
    verify      证书验证工具
    rsatul      本指令能够使用RSA算法签名，验证身份， 加密/解密数据
    crl         用于处里PME或DER格式的CRL文件
    crl2pkcs7   根据CRL或证书来生成pkcs#7消息
    errstr      用于查询错误代码
    ocsp        在线证书状态工具
    pkcs12      pkcs12文件工具，能生成和分析pkcs12文件
    pkcs8       pkcs8格式的私钥转换工具。
    s_time      SSL/TLS性能测试工具，用于测试SSL/TSL服务
    dhparam和dh ？
    ecparam     椭圆曲线密钥参数生成及操作
    ec          椭圆曲线密钥处理工具
    dsa         处理DSA密钥、格式转换和打印信息
    nseq        用于多个证书与netscape证书序列间相互转化
    prime       检查一个数是否为素数
    smime       用于处理S/MIME邮件，它能加密、解密、签名和验证S/MIME消息
    注：这里只给出了各命令的简介，具体使用参chm文件
        
OpenSSL各版本区别        
    OpenSSL版本	官方支持情况
    0.9.8 系列	不再支持
    1.0.0 系列	不再支持
    1.0.1 系列	不再支持
    1.0.2 系列	将被支持到 2019 年 12 月 31 日
    1.1.0 系列	只做安全修复，到 2019 年 9 月 11 日停止支持
    1.1.1 系列	将被支持到 2023 年 9 月 11 日
    对比：
        1） 1.0.1 与 1.0.2 这两个系列之间变化相对较小，大部分函数接口可通用
        2） 1.0.x 与 1.1.1 这两个系列之间变化比较大，很多在 1.0.x 系列中提供的函数接口
            到 1.1.1 系列中已被删去或被转变为内部接口，不再对外提供；
        3） 截至 2019 年 5月，在 1.1.1 系列中包含 pre1 至 pre9 共 9 个预览版、1.1.1 正式版，
            1.1.1a 至 1.1.1c 三个延伸版，总共有 13 个版本。
            1.1.1 系列是从 2018 年 2 月开始发布的，其内容一直在做调整，
            预览版、正式版、延伸版之间有一定差异。
    下面举例说明一些不同版本之间的差异：
        a） 1.0.2d vs. 1.1.1
            在 1.0.2d 版本中可以调用到一些与 ASN.1 编码有关的底层函数，
            例如：M_i2d_ASN1_OCTET_STRING( )，M_ASN1_BIT_STRING_free( ) 等。
            在 1.1.1 系列中，这些以 M_ 开头的 ASN.1 编码函数都被删去了。
        b） 1.1.1-pre6 vs. 1.1.1
            在 1.1.1-pre6 版中，sm2.h 文件所在的路径是 include/openssl。
            在 1.1.1 版中，sm2.h 文件所在的目录是 include/internal 。
            在 1.1.1-pre6 版的 sm2.h 中，SM2 签名和验签函数的声明如下：
               int SM2_sign(int type, const unsigned char *dgst, int dgstlen,
                            unsigned char *sig, unsigned int *siglen, EC_KEY *eckey);
               int SM2_verify(int type, const unsigned char *dgst, int dgstlen,
                              const unsigned char *sig, int siglen, EC_KEY *eckey);
            在 1.1.1 版的 sm2.h 中，SM2 签名和验签函数的声明如下：
                int sm2_sign(const unsigned char *dgst, int dgstlen,
                             unsigned char *sig, unsigned int *siglen, EC_KEY *eckey);
                int sm2_verify(const unsigned char *dgst, int dgstlen,
                               const unsigned char *sig, int siglen, EC_KEY *eckey);
            在 1.1.1-pre6 版的 sm2.h 中，SM2加密和解密函数定义如下：
                int SM2_encrypt(const EC_KEY *key,
                                const EVP_MD *digest,
                                const uint8_t *msg,
                                size_t msg_len,
                                uint8_t *ciphertext_buf, size_t *ciphertext_len);
                int SM2_decrypt(const EC_KEY *key,
                                const EVP_MD *digest,
                                const uint8_t *ciphertext,
                                size_t ciphertext_len, uint8_t *ptext_buf, size_t *ptext_len);
            在 1.1.1 版的 sm2.h 中，SM2加密和解密函数定义如下：           
                int sm2_encrypt(const EC_KEY *key,
                                const EVP_MD *digest,
                                const uint8_t *msg,
                                size_t msg_len,
                                uint8_t *ciphertext_buf, size_t *ciphertext_len);
                int sm2_decrypt(const EC_KEY *key,
                                const EVP_MD *digest,
                                const uint8_t *ciphertext,
                                size_t ciphertext_len, uint8_t *ptext_buf, size_t *ptext_len);
            通过对比可以看出：在 1.1.1 版的 SM2 签名和验签函数中，删掉了一个名为 type 的参数，
            函数名与 1.1.1-pre6 中的对应函数名在大小写拼写上有差别；
            1.1.1 版的 SM2 加密和解密函数，与 1.1.1-pre6 版中的对应函数相比，
            其函数名在大小写拼写上有差别。
        c） 在 1.1.1 版与 1.1.1c 版之间也有差别，
            例如在 1.1.1 版 ecdh_kdf.c 中实现了一个名为 ECDH_KDF_X9_62( ) 的函数，
            在 1.1.1c 版 ecdh_kdf.c 中，新增了对一个名为 ecdh_KDF_X9_63( ) 函数的实现，
            对它的声明放在 internal/ec_int.h 中。
            ECDH_KDF_X9_62( ) 依然存在，但它的实现过程如下：
            int ECDH_KDF_X9_62(unsigned char *out, size_t outlen,
                               const unsigned char *Z, size_t Zlen,
                               const unsigned char *sinfo, size_t sinfolen,
                               const EVP_MD *md)
            {
                return ecdh_KDF_X9_63(out, outlen, Z, Zlen, sinfo, sinfolen, md);
            }
            可以看出 ECDH_KDF_X9_62( ) 与 ecdh_KDF_X9_63( ) 这两个函数实现的功能是完全相同的，
            在 1.1.1c 版中将在以前版本里对函数 ECDH_KDF_X9_62( ) 的调用，
            都改为对新增函数 ecdh_KDF_X9_63( ) 的调用。
    我们在使用 OpenSSL 时，一定要留心不同版本之间的差异，
    这种差异可能给已有的应用程序带来不兼容的问题。
    在编程时应尽量选择近期发布的 OpenSSL 系列中的稳定版本。
    
    OpenSSL 1.1.1 新特性: 全面支持国密SM2/SM3/SM4加密算法
        https://blog.csdn.net/bruce135lee/article/details/81811403
        
openssl编程注意事项
    定义 EVP_CIPHER_CTX ctx; 报错
        原因： 
            typedef struct evp_cipher_ctx_st EVP_CIPHER_CTX; 
            没有 evp_cipher_ctx_st 结构的定义
        测试：
            在自定义lib中
                定义结构体 struct aaa;
                定义函数  struct aaa* geta(); void seta(struct aaa* pa);
            在主程序中定义 typedef struct aaa AAA;
            并在main中声明 AAA aaa; 同样报错，报错原因与上面的一致
            改为用 AAA *a; a = geta(); seta(a); 成功
            改为用 struct aaa *a; a = geta(); seta(a); 同样成功
         原理：
            c/c++支持使用typedef将外部未知结构重命名，
            但不可以将外部未知结构定义为实例，而只能定义为指针，
            这有点类似于只用class A声明的类，可以定义指针，不能定义实例一样
            
        
                           