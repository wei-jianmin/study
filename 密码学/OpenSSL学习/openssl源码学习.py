RUN_ONCE
    举例：
        RUN_ONCE(&err_string_init, do_err_strings_init)
    宏定义：
        ＃define RUN_ONCE(once, init) \
            CRYPTO_THREAD_run_once(once, init＃＃_ossl_) ? init＃_ossl_ret_ : 0
        enum CRYPTO_ONCE { ONCE_UNINITED, ONCE_ININIT, ONCE_DONE }
        CRYPTO_THREAD_run_once(CRYPTO_ONCE *once, void (*init)(void)) {
            if *once == 2， return
            if *once == 0,  old=*once, *once = 1
            if old == 0
                init()
                *once = 2
    do_err_strings_init 参：@错误初始化
        
&<错误初始化>                
    DEFINE_RUN_ONCE_STATIC(do_err_strings_init) 展开：
        int do_err_strings_init(void);                     
        int do_err_strings_init_ossl_ret_ = 0;            
        void do_err_strings_init_ossl_(void)              
        {                                           
            do_err_strings_init_ossl_ret_ = do_err_strings_init();              
        }          
    int do_err_strings_init(void)
    {
        OPENSSL_init_crypto(0, NULL); 参：@crypto初始化
        err_string_lock = CRYPTO_THREAD_lock_new();
        return err_string_lock != NULL;
    }
    
&<crypto初始化>    
    OPENSSL_init_crypto(uint64_t opts=0, 
                        const OPENSSL_INIT_SETTINGS *settings=NULL)
    {
        if (!base_inited && !RUN_ONCE(&base, ossl_init_base))
            return 0;
        if (opts & xxx) ...
        return 1;   //成功返回1，中间出错，返回0
    }
    int ossl_init_base()
    {
        //TlsAlloc是系统api，获取线程局部存储的索引
        global DWORD threadstopkey = TlsAlloc(); 
        global void* init_lock = CRYPTO_THREAD_lock_new()
        OPENSSL_cpuid_setup()  //空实现
        //判断是否能成功获取自身句柄
        BOOL ret = GetModuleHandleEx( GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS
                                      | GET_MODULE_HANDLE_EX_FLAG_PIN,
                                      (void *)&base_inited, &handle)
        return (ret == TRUE) ? 1 : 0                              
    }
加载错误信息
    ERR_load_strings(int lib, ERR_STRING_DATA *str)
        ERR_load_ERR_strings()
        err_load_strings(lib, str)
    ERR_load_ERR_strings
        err_load_strings(0, ERR_str_libraries);
        err_load_strings(0, ERR_str_reasons);
        err_load_strings(ERR_LIB_SYS=2, ERR_str_functs);
        err_load_strings(ERR_LIB_SYS=2, SYS_str_reasons);
    void err_load_strings(int lib, ERR_STRING_DATA *str)    
        遍历 str 数组，直到 str->error == 0
        if lib != 0 , str->error != ERR_PACK(lib, 0, 0);
        将 str 插入到全局哈希表 int_error_hash 中