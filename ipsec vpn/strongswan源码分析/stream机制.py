stream_manager_create
    private_stream_manager_t �ṹ�к��� linked_list_t<stream_entry_t> *streams; �� linked_list_t<service_entry_t> *services;
    private_stream_manager_t �Ĵ��������� library_init �� �� this->public.streams = stream_manager_create();
    �� stream_manager_create �У������� private_stream_manager_t ��
    ������� "tcp��//"��"unix://" �Ŀͻ��˺ͷ���˹��캯����װ�ṹ���ֱ���ӵ� streams �� services ��Ա��
     
connect(char* uri)
    ����uri��ǰ׺("tcp��//"��"unix://")���ҵ���Ӧ�� stream_entry_t���������еļ�¼�ĺ���ָ��(create)�����ػ�õ�stream_t*����ֵ
    ע��
        ���� unix://��int fd = socket(AF_UNIX, SOCK_STREAM, 0);   connect(fd,uri)      
        ���� tcp://, int fd = socket(addr.sa.sa_family, SOCK_STREAM, 0);   connect(fd,uri)      