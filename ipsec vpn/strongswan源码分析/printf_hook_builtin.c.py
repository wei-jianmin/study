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

            ��ʼ�� handler
                handler �����ڴ�
                handler.hook = hook

            ���λ�ȡ�ɱ����
                �����ȡ�Ĳ����� PRINTF_HOOK_ARGTYPE_END�������ѭ��
                �����ȡ�Ĳ���ͳ�Ƴ��� handler->argtypes��������3�����򱨴�
                handler->argtypes[i] = ��ȡ�Ŀɱ����ֵ
            handler->numargs = ��ȡ�Ŀɱ��������
            free(hooks->put(hooks, (void*)(uintptr_t)spec, handler));
        }    
    this.public.destroy = _destroy
    hooks = hashtable_create(hashtable_hash_ptr, hashtable_equals_ptr, 8);
        file://hashtable.c.py
    return &this->public
    
static hashtable_t *hooks;
    
	