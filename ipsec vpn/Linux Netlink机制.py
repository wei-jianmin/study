https://zhuanlan.zhihu.com/p/85431412

一：什么是Netlink通信机制
    Netlink是linux提供的用于内核和用户态进程之间的通信方式
    但是注意虽然Netlink主要用于用户空间和内核空间的通信，但是也能用于用户空间的两个进程通信。
    只是进程间通信有其他很多方式，一般不用Netlink。除非需要用到Netlink的广播特性时。
    那么Netlink有什么优势呢？
    一般来说用户空间和内核空间的通信方式有三种：/proc、ioctl、Netlink。
    而前两种都是单向的，但是Netlink可以实现双工通信。
    Netlink协议基于BSD socket和AF_NETLINK地址簇(address family)，
    使用32位的端口号寻址(以前称作PID)，
    每个Netlink协议(或称作总线，man手册中则称之为netlink family)，
    通常与一个或一组内核服务/组件相关联，
    如NETLINK_ROUTE用于获取和设置路由与链路信息、
    NETLINK_KOBJECT_UEVENT用于内核向用户空间的udev进程发送通知等。
    netlink具有以下特点
        ① 支持全双工、异步通信(当然同步也支持)
        ② 用户空间可使用标准的BSD socket接口
          (但netlink并没有屏蔽掉协议包的构造与解析过程，推荐使用libnl等第三方库)
        ③ 在内核空间使用专用的内核API接口
        ④ 支持多播(因此支持“总线”式通信，可实现消息订阅)
        ⑤ 在内核端可用于进程上下文与中断上下文
    
二：用户态数据结构
    首先看一下几个重要的数据结构的关系
    1.struct msghdr
        msghdr这个结构在socket编程中就会用到，并不算Netlink专有的，这里不在过多说明。
        只说明一下如何更好理解这个结构的功能。
        我们知道socket消息的发送和接收函数一般有这几对：
        recv／send、readv／writev、recvfrom／sendto。当然还有recvmsg／sendmsg，
        前面三对函数各有各的特点功能，
        而recvmsg／sendmsg就是要囊括前面三对的所有功能，当然还有自己特殊的用途。
        msghdr的前两个成员就是为了满足recvfrom／sendto的功能，
        中间两个成员msg_iov和msg_iovlen则是为了满足readv／writev的功能，
        而最后的msg_flags则是为了满足recv／send中flag的功能，
        剩下的msg_control和msg_controllen则是满足recvmsg／sendmsg特有的功能。
    2.struct sockaddr_ln
        struct sockaddr_ln为Netlink的地址，
        和我们通常socket编程中的sockaddr_in作用一样，他们的结构对比如下：
        struct sockaddr_nl的详细定义和描述如下：
            struct sockaddr_nl
            {
                sa_family_t nl_family; /*该字段总是为AF_NETLINK */
                unsigned short nl_pad; /* 目前未用到，填充为0*/
                __u32 nl_pid; /* process pid */
                __u32 nl_groups; /* multicast groups mask */
            };
            (1) nl_pid：
                在Netlink规范里，PID全称是Port-ID(32bits)，
                其主要作用是用于唯一的标识一个基于netlink的socket通道。
                通常情况下nl_pid都设置为当前进程的进程号。
                前面我们也说过，Netlink不仅可以实现用户-内核空间的通信
                还可使现实用户空间两个进程之间，或内核空间两个进程之间的通信。
                该属性为0时一般指内核。
            (2) nl_groups：
                如果用户空间的进程希望加入某个多播组，则必须执行bind()系统调用。
                该字段指明了调用者希望加入的多播组号的掩码
                (注意不是组号，后面我们会详细讲解这个字段)。
                如果该字段为0则表示调用者不希望加入任何多播组。
                对于每个隶属于Netlink协议域的协议，
                最多可支持32个多播组(因为nl_groups的长度为32比特)，
                每个多播组用一个比特来表示。
    3.struct nlmsghdr
        Netlink的报文由消息头和消息体构成，struct nlmsghdr即为消息头。
        消息头定义在文件里，由结构体nlmsghdr表示：
        struct nlmsghdr
        {
            __u32 nlmsg_len; /* Length of message including header */
            __u16 nlmsg_type; /* Message content */
            __u16 nlmsg_flags; /* Additional flags */
            __u32 nlmsg_seq; /* Sequence number */
            __u32 nlmsg_pid; /* Sending process PID */
        };
        消息头中各成员属性的解释及说明：
        (1) nlmsg_len：整个消息的长度，按字节计算。包括了Netlink消息头本身。
        (2) nlmsg_type：消息的类型，即是数据还是控制消息。
            目前(内核版本2.6.21)Netlink仅支持四种类型的控制消息，如下：
            a) NLMSG_NOOP-空消息，什么也不做；
            b) NLMSG_ERROR-指明该消息中包含一个错误；
            c) NLMSG_DONE-如果内核通过Netlink队列返回了多个消息，
               那么队列的最后一条消息的类型为NLMSG_DONE，
               其余所有消息的nlmsg_flags属性都被设置NLM_F_MULTI位有效。
            d) NLMSG_OVERRUN-暂时没用到。
        (3) nlmsg_flags：附加在消息上的额外说明信息，如上面提到的NLM_F_MULTI。
        
三：用户空间Netlink socket API
    1.创建socket
        int socket(int domain, int type, int protocol)
        domain指代地址族,即AF_NETLINK;
        套接字类型为SOCK_RAW或SOCK_DGRAM,因为netlink是一个面向数据报的服务;
        protocol选择该套接字使用哪种netlink特征。
        以下是几种预定义的协议类型:
            NETLINK_ROUTE,
            NETLINK_FIREWALL,
            NETLINK_APRD,
            NETLINK_ROUTE6_FW。
        可以非常容易的添加自己的netlink协议。
        为每一个协议类型最多可以定义32个多播组。
        每一个多播组用一个bitmask来表示,1<<i(0<=i<= 31),这在一组进程和内核进程协同完成一项任务时非常有用
        发送多播netlink消息可以减少系统调用的数量,同时减少用来维护多播组成员信息的负担。
    2.地址绑定bind()
        bind(fd, (struct sockaddr*)&, nladdr, sizeof(nladdr));
    3.发送netlink消息
        为了发送一条netlink消息到内核或者其他的用户空间进程,
        另外一个struct sockaddr_nl nladdr需要作为目的地址,
        这和使用sendmsg()发送一个UDP包是一样的。
        如果该消息是发送至内核的,那么nl_pid和nl_groups都置为0.
        如果消息是发送给另一个进程的单播消息,nl_pid是另外一个进程的pid值而nl_groups为零。
        如果消息是发送给一个或多个多播组的多播消息,所有的目的多播组必须bitmask必须or起来从而形成nl_groups域。
        sendmsg(fd, &, msg, 0);
    4.接收netlink消息
        一个接收程序必须分配一个足够大的内存用于保存netlink消息头和消息负载。
        然后其填充struct msghdr msg,再使用标准的recvmsg()函数来接收netlink消息。
        当消息被正确的接收之后,nlh应该指向刚刚接收到的netlink消息的头。
        nladdr应该包含接收消息的目的地址,其中包括了消息发送者的pid和多播组。
        同时,宏NLMSG_DATA(nlh),定义在netlink.h中,返回一个指向netlink消息负载的指针。
        调用close(fd)关闭fd描述符所标识的socket。
        recvmsg(fd, &, msg, 0);
        
四：内核空间Netlink socket API
    1.创建 netlink socket
        struct sock *netlink_kernel_create( struct net *net,
                                            int unit,unsigned int groups,
                                            void (*input)(struct sk_buff *skb),
                                            struct mutex *cb_mutex,struct module *module);
        参数说明：
        (1) net：是一个网络名字空间namespace，在不同的名字空间里面可以有自己的转发信息库，有自己的一套net_device等等。
            默认情况下都是使用 init_net这个全局变量。
        (2) unit：表示netlink协议类型，如NETLINK_TEST、NETLINK_SELINUX。
        (3) groups：多播地址。
        (4) input：为内核模块定义的netlink消息处理函数，当有消 息到达这个netlink socket时，
            该input函数指针就会被引用，且只有此函数返回时，调用者的sendmsg才能返回。
        (5) cb_mutex：为访问数据时的互斥信号量。
        (6) module： 一般为THIS_MODULE。
    2.发送单播消息 netlink_unicast
        int netlink_unicast(struct sock *ssk, struct sk_buff *skb, u32 pid, int nonblock)
        参数说明：
        (1) ssk：为函数 netlink_kernel_create()返回的socket。
        (2) skb：存放消息，它的data字段指向要发送的netlink消息结构，
            而 skb的控制块保存了消息的地址信息，宏NETLINK_CB(skb)就用于方便设置该控制块。
        (3) pid：为接收此消息进程的pid，即目标地址，如果目标为组或内核，它设置为 0。
        (4) nonblock：表示该函数是否为非阻塞，如果为1，该函数将在没有接收缓存可利用时立即返回；
            而如果为0，该函数在没有接收缓存可利用定时睡眠。
    3.发送广播消息 netlink_broadcast
        int netlink_broadcast(struct sock *ssk, struct sk_buff *skb, u32 pid, u32 group, gfp_t allocation)
        前面的三个参数与 netlink_unicast相同，参数group为接收消息的多播组，该参数的每一个位代表一个多播组，
        因此如果发送给多个多播组，就把该参数设置为多个多播组组ID的位或。参数allocation为内核内存分配类型，一般地为GFP_ATOMIC或
        GFP_KERNEL，GFP_ATOMIC用于原子的上下文（即不可以睡眠），而GFP_KERNEL用于非原子上下文。
    4.释放 netlink socket
        int netlink_broadcast(struct sock *ssk, struct sk_buff *skb, u32 pid, u32 group, gfp_t allocation)        

范例：
    参原链接