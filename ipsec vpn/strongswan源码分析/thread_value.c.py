thread_value_t *thread_value_create(thread_cleanup_t destructor)
    private_thread_value_t *this;
    this��ʼ��
        this.public.set = _set
        this.public.get = _get
        this.public.destroy = _destroy
        this.destructor = destructor
    pthread_key_create
        file://�ֲ߳̾��洢.txt
            
        