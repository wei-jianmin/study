stream_manager_create
    private_stream_manager_t 结构中含有 linked_list_t<stream_entry_t> *streams; 和 linked_list_t<service_entry_t> *services;
    private_stream_manager_t 的创建发生在 library_init 中 ： this->public.streams = stream_manager_create();
    在 stream_manager_create 中，创建了 private_stream_manager_t 后，
    又添加了 "tcp：//"、"unix://" 的客户端和服务端构造函数包装结构，分别添加到 streams 和 services 成员中
     
connect(char* uri)
    根据uri的前缀("tcp：//"、"unix://")，找到相应的 stream_entry_t，调用其中的记录的函数指针(create)，返回获得的stream_t*返回值
    注：
        对于 unix://，int fd = socket(AF_UNIX, SOCK_STREAM, 0);   connect(fd,uri)      
        对于 tcp://, int fd = socket(addr.sa.sa_family, SOCK_STREAM, 0);   connect(fd,uri)      