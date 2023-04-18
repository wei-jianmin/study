RUN_ONCE
    ������
        RUN_ONCE(&err_string_init, do_err_strings_init)
    �궨�壺
        ��define RUN_ONCE(once, init) \
            CRYPTO_THREAD_run_once(once, init����_ossl_) ? init��_ossl_ret_ : 0
        enum CRYPTO_ONCE { ONCE_UNINITED, ONCE_ININIT, ONCE_DONE }
        CRYPTO_THREAD_run_once(CRYPTO_ONCE *once, void (*init)(void)) {
            if *once == 2�� return
            if *once == 0,  old=*once, *once = 1
            if old == 0
                init()
                *once = 2
    do_err_strings_init �Σ�@�����ʼ��
        
&<�����ʼ��>                
    DEFINE_RUN_ONCE_STATIC(do_err_strings_init) չ����
        int do_err_strings_init(void);                     
        int do_err_strings_init_ossl_ret_ = 0;            
        void do_err_strings_init_ossl_(void)              
        {                                           
            do_err_strings_init_ossl_ret_ = do_err_strings_init();              
        }          
    int do_err_strings_init(void)
    {
        OPENSSL_init_crypto(0, NULL); �Σ�@crypto��ʼ��
        err_string_lock = CRYPTO_THREAD_lock_new();
        return err_string_lock != NULL;
    }
    
&<crypto��ʼ��>    
    OPENSSL_init_crypto(uint64_t opts=0, 
                        const OPENSSL_INIT_SETTINGS *settings=NULL)
    {
        if (!base_inited && !RUN_ONCE(&base, ossl_init_base))
            return 0;
        if (opts & xxx) ...
        return 1;   //�ɹ�����1���м��������0
    }
    int ossl_init_base()
    {
        //TlsAlloc��ϵͳapi����ȡ�ֲ߳̾��洢������
        global DWORD threadstopkey = TlsAlloc(); 
        global void* init_lock = CRYPTO_THREAD_lock_new()
        OPENSSL_cpuid_setup()  //��ʵ��
        //�ж��Ƿ��ܳɹ���ȡ������
        BOOL ret = GetModuleHandleEx( GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS
                                      | GET_MODULE_HANDLE_EX_FLAG_PIN,
                                      (void *)&base_inited, &handle)
        return (ret == TRUE) ? 1 : 0                              
    }
���ش�����Ϣ
    ERR_load_strings(int lib, ERR_STRING_DATA *str)
        ERR_load_ERR_strings()
        err_load_strings(lib, str)
    ERR_load_ERR_strings
        err_load_strings(0, ERR_str_libraries);
        err_load_strings(0, ERR_str_reasons);
        err_load_strings(ERR_LIB_SYS=2, ERR_str_functs);
        err_load_strings(ERR_LIB_SYS=2, SYS_str_reasons);
    void err_load_strings(int lib, ERR_STRING_DATA *str)    
        ���� str ���飬ֱ�� str->error == 0
        if lib != 0 , str->error != ERR_PACK(lib, 0, 0);
        �� str ���뵽ȫ�ֹ�ϣ�� int_error_hash ��