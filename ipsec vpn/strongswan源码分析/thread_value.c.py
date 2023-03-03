thread_value_t *thread_value_create(thread_cleanup_t destructor)
    private_thread_value_t *this;
    this初始化
        this.public.set = _set
        this.public.get = _get
        this.public.destroy = _destroy
        this.destructor = destructor
    pthread_key_create
        file://线程局部存储.txt
            
        