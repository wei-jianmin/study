https://juejin.cn/post/6844903737165791240

--topology t  ： 2.1版本新增参数，指定网络拓扑
    可选参数为net30，p2p以及subnet
    net30拓扑结构主要用于p2p网络，   //参：file://p2p网络.py
        该种网络假设server和client均存在于一个p2p链路之上，
        因此各需要配置一个p2p网关，
        每对连接要用去4个IP地址，
        client和server均占有一个30位的子网掩码的网络，
        （这也正是30的含义）每端余下4个IP地址，
        并且一个子网中全0号IP表示子网本身，全1号IP表示广播地址，
        于是仅留下两个IP地址可用，
        net30虽然用于p2p链路，
        在以太网这种广播网络中也是可以使用的，该模式十分浪费IP地址；
    p2p拓扑用在一种半p2p的网络中，
        server将分配且只分配一个IP地址给client端，
        如此一来client端就可以和server端直接建立联系，
        而不必再通过一个p2p网关了，
        而server端仍然保留p2p网关，类似net30模式；
    subnet拓扑则是完全实现了虚拟网络从p2p模式向广播型网络的过渡，
        server端和client端均使用且只使用一个IP地址，
        如此一来server和所有的client构成一个可以基于
        广播链路的虚拟局域网（注意不是VLAN），
        大量节省了IP地址并且降低了配置的难度。
        
注意：net30->p2p->subnet的演进过程有两层含义，
    第一层含义代表了OpenVPN本身的版本升级，
    在2.0之前OpenVPN是不支持multi-clients的，
    也就是说所有的p2p模式以及c/s模式均是一对一的连接，
    因此虚拟网卡的配置很简单，直接配置上对端的ip地址即可，
    但是到了2.0及之后，OpenVPN的一个server可以对应多个客户端了，
    按照前面的思路，只需要将client虚拟网卡的地址p2p地配置成server的虚拟网卡地址即可，
    可是对于Windows这样却不行，
    于是就引出了第二层含义，为了兼容Tap-WIN32驱动，
    Tap-WIN32驱动不支持在“点对多点/多点对多点”的链路上创建p2p连接，
    于是不得不用net30的方式来“模拟”出一条p2p的链路
