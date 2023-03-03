https://zhuanlan.zhihu.com/p/85431412

һ��ʲô��Netlinkͨ�Ż���
    Netlink��linux�ṩ�������ں˺��û�̬����֮���ͨ�ŷ�ʽ
    ����ע����ȻNetlink��Ҫ�����û��ռ���ں˿ռ��ͨ�ţ�����Ҳ�������û��ռ����������ͨ�š�
    ֻ�ǽ��̼�ͨ���������ܶ෽ʽ��һ�㲻��Netlink��������Ҫ�õ�Netlink�Ĺ㲥����ʱ��
    ��ôNetlink��ʲô�����أ�
    һ����˵�û��ռ���ں˿ռ��ͨ�ŷ�ʽ�����֣�/proc��ioctl��Netlink��
    ��ǰ���ֶ��ǵ���ģ�����Netlink����ʵ��˫��ͨ�š�
    NetlinkЭ�����BSD socket��AF_NETLINK��ַ��(address family)��
    ʹ��32λ�Ķ˿ں�Ѱַ(��ǰ����PID)��
    ÿ��NetlinkЭ��(��������ߣ�man�ֲ������֮Ϊnetlink family)��
    ͨ����һ����һ���ں˷���/����������
    ��NETLINK_ROUTE���ڻ�ȡ������·������·��Ϣ��
    NETLINK_KOBJECT_UEVENT�����ں����û��ռ��udev���̷���֪ͨ�ȡ�
    netlink���������ص�
        �� ֧��ȫ˫�����첽ͨ��(��Ȼͬ��Ҳ֧��)
        �� �û��ռ��ʹ�ñ�׼��BSD socket�ӿ�
          (��netlink��û�����ε�Э����Ĺ�����������̣��Ƽ�ʹ��libnl�ȵ�������)
        �� ���ں˿ռ�ʹ��ר�õ��ں�API�ӿ�
        �� ֧�ֶಥ(���֧�֡����ߡ�ʽͨ�ţ���ʵ����Ϣ����)
        �� ���ں˶˿����ڽ������������ж�������
    
�����û�̬���ݽṹ
    ���ȿ�һ�¼�����Ҫ�����ݽṹ�Ĺ�ϵ
    1.struct msghdr
        msghdr����ṹ��socket����оͻ��õ���������Netlinkר�еģ����ﲻ�ڹ���˵����
        ֻ˵��һ����θ����������ṹ�Ĺ��ܡ�
        ����֪��socket��Ϣ�ķ��ͺͽ��պ���һ�����⼸�ԣ�
        recv��send��readv��writev��recvfrom��sendto����Ȼ����recvmsg��sendmsg��
        ǰ�����Ժ������и����ص㹦�ܣ�
        ��recvmsg��sendmsg����Ҫ����ǰ�����Ե����й��ܣ���Ȼ�����Լ��������;��
        msghdr��ǰ������Ա����Ϊ������recvfrom��sendto�Ĺ��ܣ�
        �м�������Աmsg_iov��msg_iovlen����Ϊ������readv��writev�Ĺ��ܣ�
        ������msg_flags����Ϊ������recv��send��flag�Ĺ��ܣ�
        ʣ�µ�msg_control��msg_controllen��������recvmsg��sendmsg���еĹ��ܡ�
    2.struct sockaddr_ln
        struct sockaddr_lnΪNetlink�ĵ�ַ��
        ������ͨ��socket����е�sockaddr_in����һ�������ǵĽṹ�Ա����£�
        struct sockaddr_nl����ϸ������������£�
            struct sockaddr_nl
            {
                sa_family_t nl_family; /*���ֶ�����ΪAF_NETLINK */
                unsigned short nl_pad; /* Ŀǰδ�õ������Ϊ0*/
                __u32 nl_pid; /* process pid */
                __u32 nl_groups; /* multicast groups mask */
            };
            (1) nl_pid��
                ��Netlink�淶�PIDȫ����Port-ID(32bits)��
                ����Ҫ����������Ψһ�ı�ʶһ������netlink��socketͨ����
                ͨ�������nl_pid������Ϊ��ǰ���̵Ľ��̺š�
                ǰ������Ҳ˵����Netlink��������ʵ���û�-�ں˿ռ��ͨ��
                ����ʹ��ʵ�û��ռ���������֮�䣬���ں˿ռ���������֮���ͨ�š�
                ������Ϊ0ʱһ��ָ�ںˡ�
            (2) nl_groups��
                ����û��ռ�Ľ���ϣ������ĳ���ಥ�飬�����ִ��bind()ϵͳ���á�
                ���ֶ�ָ���˵�����ϣ������Ķಥ��ŵ�����
                (ע�ⲻ����ţ��������ǻ���ϸ��������ֶ�)��
                ������ֶ�Ϊ0���ʾ�����߲�ϣ�������κζಥ�顣
                ����ÿ��������NetlinkЭ�����Э�飬
                ����֧��32���ಥ��(��Ϊnl_groups�ĳ���Ϊ32����)��
                ÿ���ಥ����һ����������ʾ��
    3.struct nlmsghdr
        Netlink�ı�������Ϣͷ����Ϣ�幹�ɣ�struct nlmsghdr��Ϊ��Ϣͷ��
        ��Ϣͷ�������ļ���ɽṹ��nlmsghdr��ʾ��
        struct nlmsghdr
        {
            __u32 nlmsg_len; /* Length of message including header */
            __u16 nlmsg_type; /* Message content */
            __u16 nlmsg_flags; /* Additional flags */
            __u32 nlmsg_seq; /* Sequence number */
            __u32 nlmsg_pid; /* Sending process PID */
        };
        ��Ϣͷ�и���Ա���ԵĽ��ͼ�˵����
        (1) nlmsg_len��������Ϣ�ĳ��ȣ����ֽڼ��㡣������Netlink��Ϣͷ����
        (2) nlmsg_type����Ϣ�����ͣ��������ݻ��ǿ�����Ϣ��
            Ŀǰ(�ں˰汾2.6.21)Netlink��֧���������͵Ŀ�����Ϣ�����£�
            a) NLMSG_NOOP-����Ϣ��ʲôҲ������
            b) NLMSG_ERROR-ָ������Ϣ�а���һ������
            c) NLMSG_DONE-����ں�ͨ��Netlink���з����˶����Ϣ��
               ��ô���е����һ����Ϣ������ΪNLMSG_DONE��
               ����������Ϣ��nlmsg_flags���Զ�������NLM_F_MULTIλ��Ч��
            d) NLMSG_OVERRUN-��ʱû�õ���
        (3) nlmsg_flags����������Ϣ�ϵĶ���˵����Ϣ���������ᵽ��NLM_F_MULTI��
        
�����û��ռ�Netlink socket API
    1.����socket
        int socket(int domain, int type, int protocol)
        domainָ����ַ��,��AF_NETLINK;
        �׽�������ΪSOCK_RAW��SOCK_DGRAM,��Ϊnetlink��һ���������ݱ��ķ���;
        protocolѡ����׽���ʹ������netlink������
        �����Ǽ���Ԥ�����Э������:
            NETLINK_ROUTE,
            NETLINK_FIREWALL,
            NETLINK_APRD,
            NETLINK_ROUTE6_FW��
        ���Էǳ����׵�����Լ���netlinkЭ�顣
        Ϊÿһ��Э�����������Զ���32���ಥ�顣
        ÿһ���ಥ����һ��bitmask����ʾ,1<<i(0<=i<= 31),����һ����̺��ں˽���Эͬ���һ������ʱ�ǳ�����
        ���Ͷಥnetlink��Ϣ���Լ���ϵͳ���õ�����,ͬʱ��������ά���ಥ���Ա��Ϣ�ĸ�����
    2.��ַ��bind()
        bind(fd, (struct sockaddr*)&, nladdr, sizeof(nladdr));
    3.����netlink��Ϣ
        Ϊ�˷���һ��netlink��Ϣ���ں˻����������û��ռ����,
        ����һ��struct sockaddr_nl nladdr��Ҫ��ΪĿ�ĵ�ַ,
        ���ʹ��sendmsg()����һ��UDP����һ���ġ�
        �������Ϣ�Ƿ������ں˵�,��ônl_pid��nl_groups����Ϊ0.
        �����Ϣ�Ƿ��͸���һ�����̵ĵ�����Ϣ,nl_pid������һ�����̵�pidֵ��nl_groupsΪ�㡣
        �����Ϣ�Ƿ��͸�һ�������ಥ��Ķಥ��Ϣ,���е�Ŀ�Ķಥ�����bitmask����or�����Ӷ��γ�nl_groups��
        sendmsg(fd, &, msg, 0);
    4.����netlink��Ϣ
        һ�����ճ���������һ���㹻����ڴ����ڱ���netlink��Ϣͷ����Ϣ���ء�
        Ȼ�������struct msghdr msg,��ʹ�ñ�׼��recvmsg()����������netlink��Ϣ��
        ����Ϣ����ȷ�Ľ���֮��,nlhӦ��ָ��ոս��յ���netlink��Ϣ��ͷ��
        nladdrӦ�ð���������Ϣ��Ŀ�ĵ�ַ,���а�������Ϣ�����ߵ�pid�Ͷಥ�顣
        ͬʱ,��NLMSG_DATA(nlh),������netlink.h��,����һ��ָ��netlink��Ϣ���ص�ָ�롣
        ����close(fd)�ر�fd����������ʶ��socket��
        recvmsg(fd, &, msg, 0);
        
�ģ��ں˿ռ�Netlink socket API
    1.���� netlink socket
        struct sock *netlink_kernel_create( struct net *net,
                                            int unit,unsigned int groups,
                                            void (*input)(struct sk_buff *skb),
                                            struct mutex *cb_mutex,struct module *module);
        ����˵����
        (1) net����һ���������ֿռ�namespace���ڲ�ͬ�����ֿռ�����������Լ���ת����Ϣ�⣬���Լ���һ��net_device�ȵȡ�
            Ĭ������¶���ʹ�� init_net���ȫ�ֱ�����
        (2) unit����ʾnetlinkЭ�����ͣ���NETLINK_TEST��NETLINK_SELINUX��
        (3) groups���ಥ��ַ��
        (4) input��Ϊ�ں�ģ�鶨���netlink��Ϣ�������������� Ϣ�������netlink socketʱ��
            ��input����ָ��ͻᱻ���ã���ֻ�д˺�������ʱ�������ߵ�sendmsg���ܷ��ء�
        (5) cb_mutex��Ϊ��������ʱ�Ļ����ź�����
        (6) module�� һ��ΪTHIS_MODULE��
    2.���͵�����Ϣ netlink_unicast
        int netlink_unicast(struct sock *ssk, struct sk_buff *skb, u32 pid, int nonblock)
        ����˵����
        (1) ssk��Ϊ���� netlink_kernel_create()���ص�socket��
        (2) skb�������Ϣ������data�ֶ�ָ��Ҫ���͵�netlink��Ϣ�ṹ��
            �� skb�Ŀ��ƿ鱣������Ϣ�ĵ�ַ��Ϣ����NETLINK_CB(skb)�����ڷ������øÿ��ƿ顣
        (3) pid��Ϊ���մ���Ϣ���̵�pid����Ŀ���ַ�����Ŀ��Ϊ����ںˣ�������Ϊ 0��
        (4) nonblock����ʾ�ú����Ƿ�Ϊ�����������Ϊ1���ú�������û�н��ջ��������ʱ�������أ�
            �����Ϊ0���ú�����û�н��ջ�������ö�ʱ˯�ߡ�
    3.���͹㲥��Ϣ netlink_broadcast
        int netlink_broadcast(struct sock *ssk, struct sk_buff *skb, u32 pid, u32 group, gfp_t allocation)
        ǰ������������� netlink_unicast��ͬ������groupΪ������Ϣ�Ķಥ�飬�ò�����ÿһ��λ����һ���ಥ�飬
        ���������͸�����ಥ�飬�ͰѸò�������Ϊ����ಥ����ID��λ�򡣲���allocationΪ�ں��ڴ�������ͣ�һ���ΪGFP_ATOMIC��
        GFP_KERNEL��GFP_ATOMIC����ԭ�ӵ������ģ���������˯�ߣ�����GFP_KERNEL���ڷ�ԭ�������ġ�
    4.�ͷ� netlink socket
        int netlink_broadcast(struct sock *ssk, struct sk_buff *skb, u32 pid, u32 group, gfp_t allocation)        

������
    ��ԭ����