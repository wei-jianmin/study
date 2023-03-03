library_t��file://strongswan lib�ṹ.h

library_init(char *settings=NULL, const char *namespace="charon")
    chunk_hash_seed();  #libstrongswan\utils\chunk.c
        static u_char key[16] = {};  #static��.c�ļ�������ȫ�ֱ���ʱ����ʾ˽��
        �� key �зź������
    private_library_t *this
        struct private_library_t {
            library_t public;
            hashtable_t *objects;
            bool init_failed;
            #ifdef LEAK_DETECTIVE
            FILE *ld_out;
            #endif
            refcount_t ref;
        };    
    ��ʼ��this
        Ϊ this �����ڴ�
        this.public.get = _get
        this.public.set = _set
        this.public.ns = namespace?:"libstrongswan"
        this.public.conf = settings?:STRONGSWAN_CONF����������ֵ?:NULL
        this.ret = 1
    lib = &this->public  #libΪ���ļ��е�ȫ�ֱ���
    threads_init
        file://thread.c.py
    utils_init
    arrays_init
    backtrace_init
    Ϊ this.public.printf_hook ���� printf_hook_t �������һϵ�еĴ�����
        printf_hook_t * pfh = printf_hook_create();
            file://printf_hook_builtin.c.py
        this.public.printf_hook = pfh
        pfh->add_handler('b', mem_printf_hook);
        pfh->add_handler('B', chunk_printf_hook);
        pfh->add_handler('H', host_printf_hook);
        pfh->add_handler('N', enum_printf_hook);
        pfh->add_handler('T', time_printf_hook);
        pfh->add_handler('V', time_delta_printf_hook);
        pfh->add_handler('Y', identification_printf_hook);
        pfh->add_handler('R', traffic_selector_printf_hook);
        pfh->add_handler('P', proposal_printf_hook);
    this->objects = hashtable_create(hash,equals, 4);
    this->public.settings ��ʼ��������conf�����ļ�
        this->public.settings = settings_create(NULL);
            file://settings.c.py
        this->public.settings->load_files(this->public.settings,this->public.conf, FALSE)

void add_fallback(private_settings_t *this, const char *key, const char *fallback, ...)
{
	section_t *section;
	va_list args;
	char buf[512];

	this->lock->write_lock(this->lock);
	va_start(args, fallback);
	section = ensure_section(this, this->top, key, args);
	va_end(args);

	va_start(args, fallback);
	if (section && vsnprintf(buf, sizeof(buf), fallback, args) < sizeof(buf))
	{
		settings_reference_add(section, strdup(buf), TRUE);
	}
	va_end(args);
	this->lock->unlock(this->lock);
}    