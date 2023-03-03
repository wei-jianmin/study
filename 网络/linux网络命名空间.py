相关参考： file://veth设备.txt

 Linux 网络命名空间
    在 Linux 上通过 veth 我们可以创建出许多的虚拟设备。
    通过 Bridge 模拟以太网交换机的方式可以让这些网络设备之间进行通信。
    不过虚拟化中还有很重要的一步，那就是隔离。
    借用 Docker 的概念来说，那就是不能让 A 容器用到 B 容器的设备，甚至连看一眼都不可以。
    只有这样才能保证不同的容器之间复用硬件资源的同时，还不会影响其它容器的正常运行。
    在 Linux 上实现隔离的技术手段就是 namespace
    通过 namespace 可以隔离容器的进程 PID、文件系统挂载点、主机名等多种资源。
    不过我们今天重点要介绍的是网络 namespace，简称 netns。
    它可以为不同的命名空间从逻辑上提供独立的网络协议栈，
    具体包括网络设备、路由表、arp表、iptables、以及套接字（socket）等。
    使得不同的网络空间就都好像运行在独立的网络中一样。
    在这个空间里，网络设备、路由表、arp表、iptables都是独立的，
    不会和母机上的冲突，也不会和其它空间里的产生干扰。
    而且还可以通过 veth 来和其它空间下的网络进行通信。
    file://imgs/网络命令空间.png
    
    内核中 namespace 的定义
        在内核中，很多组件都是和 namespace 有关系的
        在 Linux 中，很多我们平常熟悉的概念都是归属到某一个特定的网络 namespace 中的，
        比如进程、网卡设备、socket 等等。
        Linux 中每个进程（线程）都是用 task_struct 来表示的。
        每个 task_struct 都要关联到一个 namespace 对象 nsproxy，
        而 nsproxy 又包含了 netns。
        对于网卡设备和 socket 来说，通过自己的成员来直接表明自己的归属。
        file://linux命令空间关系图.png
        拿网络设备来举例，只有归属到当前 netns 下的才能够通过 ifconfig 看到，否则是不可见的。
        struct nsproxy {
             struct uts_namespace *uts_ns; // 主机名
             struct ipc_namespace *ipc_ns; // IPC
             struct mnt_namespace *mnt_ns; // 文件系统挂载点
             struct pid_namespace *pid_ns; // 进程标号
             struct net       *net_ns;  // 网络协议栈
            };
        命名空间的核心数据结构是上面的这个 struct nsproxy
        所有类型的 namespace（包括 pid、文件系统挂载点、网络栈等等）都是在这里定义的。
        所有的网络设备刚创建出来都是在宿主机默认网络空间下的。
        可以通过ip link set 设备名 netns 网络空间名将设备移动到另外一个空间里去。
        例如当 veth 1 移动到 net1 下的时候，该设备在宿主机下“消失”了，在 net1 下就能看到了。
        还有我们经常用的 socket，也是归属在某一个网络命名空间下的
        struct net {
             //每个 net 中都有一个回环设备
             struct net_device       *loopback_dev;          /* The loopback */
             //路由表、netfilter都在这里
             struct netns_ipv4 ipv4;
             ......
             unsigned int  proc_inum;
            }
        file://imgs/网络命令空间2.png
        可见每个 net 下都包含了自己的路由表、iptable 以及内核参数配置等等。
        网络 netspace 中最核心的数据结构是 struct netns_ipv4 ipv4
        在这个数据结构里，定义了每一个网络空间专属的路由表、ipfilter 以及各种内核参数。
        struct netns_ipv4 {
             //路由表 
             struct fib_table *fib_local;
             struct fib_table *fib_main;
             struct fib_table *fib_default;
             //ip表
             struct xt_table  *iptable_filter;
             struct xt_table  *iptable_raw;
             struct xt_table  *arptable_filter;
             //内核参数
             long sysctl_tcp_mem[3];
             ...
            }
        Linux 上存在一个默认的网络命名空间，Linux 中的 1 号进程初始使用该默认空间(init_net)。
        Linux 上其它所有进程都是由 1 号进程派生出来的，
        在派生 clone 的时候如果没有额外特别指定，所有的进程都将共享这个默认网络空间。
        file://imgs/默认网络命名空间.png
        在一个设备刚刚创建出来的时候，它是属于默认网络命名空间 init_net 的，包括 veth 设备
        
        当考虑到网络命名空间的时候，网络包的收发又是怎么样的呢？
            socket 与网络命名空间
                其实每个 socket 都是归属于某一个网络命名空间的
                到底归属那个 netns，这是由创建这个 socket 的进程所属的 netns 来决定
                当在某个进程里创建 socket 的时候，
                内核就会把当前进程的 nsproxy->net_ns 找出来，
                并把它赋值给 socket 上的网络命名空间成员 skc_net。
                在默认下，我们创建的 socket 都属于默认的网络命名空间 init_net
                file://imgs/socket的网络命名空间.png
                我们就以网络包发送过程中的路由功能为例，
                来看一下网络在传输的时候是如何使用到 netns 的。
                其它收发过程中的各个步骤也都是类似的。
                大致的原理就是 socket 上记录了其归属的网络命名空间。
                需要查找路由表之前先找到该命名空间，再找到命名空间里的路由表，
                然后再开始执行查找。这样，各个命名空间中的路由过程就都隔离开了。
                具体可参看：
                    file://../ipsec vpn/图解Linux网络包发送过程.pdf
                    file://../ipsec vpn/图解Linux网络包发送过程.py
    结论
        Linux 的网络 namespace 实现了独立协议栈的隔离。
        这个说法其实不是很准确，内核网络代码只有一套，并没有隔离。
        它是通过为不同空间创建不同的 struct net 对象。
        每个 struct net 中都有独立的路由表、iptable 等数据结构。
        每个设备、每个 socket 上也都有指针指明自己归属那个 netns。
        通过这种方法从逻辑上看起来好像是真的有多个协议栈一样。
        file://imgs/一台物理上创建多个逻辑上的协议栈.jpg
        在上图中，Docker1 和 Docker2 都可以分别拥有自己独立的网卡设备，
        配置自己的路由规则、iptable。从而使得他们的网络功能不会相互影响。

        