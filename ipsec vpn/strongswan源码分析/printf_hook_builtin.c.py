printf_hook_t *printf_hook_create()
    private_printf_hook_t *this;
    this.public.add_handler = _add_handler
        static void add_handler(    union {
                                        printf_hook_t *_public; 
                                        private_printf_hook_t *this;
                                    } __attribute__((transparent_union)),
                                    char spec, 
                                    printf_hook_function_t hook, 
                                    ...
                               ); 
        static typeof(add_handler) *_add_handler = (typeof(add_handler)*)add_handler; 
        static void add_handler(private_printf_hook_t *this,char spec, printf_hook_function_t hook, ...)
        {
            printf_hook_handler_t *handler;
            printf_hook_argtype_t argtype;

            初始化 handler
                handler 分配内存
                handler.hook = hook

            依次获取可变参数
                如果获取的参数是 PRINTF_HOOK_ARGTYPE_END，则结束循环
                如果获取的参数统计超过 handler->argtypes的容量（3），则报错
                handler->argtypes[i] = 获取的可变参数值
            handler->numargs = 获取的可变参数个数
            free(hooks->put(hooks, (void*)(uintptr_t)spec, handler));
        }    
    this.public.destroy = _destroy
    hooks = hashtable_create(hashtable_hash_ptr, hashtable_equals_ptr, 8);
        file://hashtable.c.py
    return &this->public
    
static hashtable_t *hooks;
    
	