https://mp.weixin.qq.com/s?__biz=MjM5Njg5NDgwNA==&mid=2247484058&idx=1&sn=a2621bc27c74b313528eefbc81ee8c0f
图解Linux网络包接收过程 （微信公众号：开发内功修炼/内功修炼/网络篇/1）

一 Linux网络收包总览
    在TCP/IP网络分层模型里，整个协议栈被分成了物理层、链路层、网络层，传输层和应用层。
    物理层对应的是网卡和网线，应用层对应的是我们常见的Nginx，FTP等等各种应用。
    Linux实现的是链路层、网络层和传输层这三层
    在Linux内核实现中，链路层协议靠网卡驱动来实现，内核协议栈来实现网络层和传输层。
    内核对更上层的应用层提供socket接口来供用户进程访问。
    我们用Linux的视角来看到的TCP/IP网络分层模型应该是下面这个样子的。
    file://imgs/Linux视角的网络协议栈.png
    在Linux的源代码中，网络设备驱动对应的逻辑位于driver/net/ethernet, 
    其中intel系列网卡的驱动在driver/net/ethernet/intel目录下。
    协议栈模块代码位于kernel和net目录。
    内核和网络设备驱动是通过中断的方式来处理的。
    当设备上有数据到达的时候，会给CPU的相关引脚上触发一个电压变化，以通知CPU来处理数据。
    对于网络模块来说，由于处理过程比较复杂和耗时，如果在中断函数中完成所有的处理，
    将会导致中断处理函数（优先级过高）将过度占据CPU，将导致CPU无法响应其它设备，例如鼠标和键盘的消息。
    因此Linux中断处理函数是分上半部和下半部的。
    上半部是只进行最简单的工作，快速处理然后释放CPU，接着CPU就可以允许其它中断进来。
    剩下将绝大部分的工作都放到下半部中，可以慢慢从容处理。
    2.4以后的内核版本采用的下半部实现方式是软中断，由ksoftirqd内核线程全权处理。
    和硬中断不同的是，硬中断是通过给CPU物理引脚施加电压变化，
    而软中断是通过给内存中的一个变量的二进制值以通知软中断处理程序。
    file://imgs/Linux内核网络收包总览.png
    当网卡上收到数据以后，Linux中第一个工作的模块是网络驱动。# 硬中断，cpu完成DMA的初始化
    网络驱动会以DMA的方式把网卡上收到的帧写到内存里。再向CPU发起一个中断，以通知CPU有数据到达。
    第二，当CPU收到中断请求后，会去调用网络驱动注册的中断处理函数。
    网卡的中断处理函数并不做过多工作，发出软中断请求，然后尽快释放CPU。
    ksoftirqd(kernal soft interupt request deamon)检测到有软中断请求到达，
    调用poll开始轮询收包，收到后交由各级协议栈处理。
    对于UDP包来说，会被放到用户socket的接收队列中。
二 Linux启动
    2.1 创建ksoftirqd内核线程
        ksoftirqd内核进程数量不是1个，而是N个，其中N等于你的机器的核数。
        系统初始化的时候在kernel/smpboot.c中调用了smpboot_register_percpu_thread， 
        该函数进一步会执行到spawn_ksoftirqd（位于kernel/softirq.c）来创建出softirqd进程。
        当ksoftirqd被创建出来以后，它就会进入自己的线程循环函数ksoftirqd_should_run和run_ksoftirqd了。
        不停地判断有没有软中断需要被处理。这里需要注意的一点是，软中断不仅仅只有网络软中断，还有其它类型。
    2.2 网络子系统初始化
        linux内核通过调用subsys_initcall来初始化各个子系统，
        在源代码目录里你可以grep出许多对这个函数的调用。
        这里我们要说的是网络子系统的初始化，会执行到net_dev_init函数。
        static int __init net_dev_init(void){
            ......
            for_each_possible_cpu(i) {
                struct softnet_data *sd = &per_cpu(softnet_data, i);
                memset(sd, 0, sizeof(*sd));
                skb_queue_head_init(&sd->input_pkt_queue);
                skb_queue_head_init(&sd->process_queue);
                sd->completion_queue = NULL;
                INIT_LIST_HEAD(&sd->poll_list);
                ......
            }
            ......
            open_softirq(NET_TX_SOFTIRQ, net_tx_action);
            open_softirq(NET_RX_SOFTIRQ, net_rx_action);
        }
        subsys_initcall(net_dev_init);
        在这个函数里，会为每个CPU都申请一个softnet_data数据结构，
        在这个数据结构里的 poll_list 是等待驱动程序将其poll函数注册进来，
        稍后网卡驱动初始化的时候我们可以看到这一过程。
        另外open_softirq为每一种软中断都注册一个处理函数
        继续跟踪open_softirq后发现这个注册的方式是记录在softirq_vec变量里的。
        后面ksoftirqd线程收到软中断的时候，也会使用这个变量来找到每一种软中断对应的处理函数。
    2.3 协议栈注册
        内核实现了网络层的ip协议，也实现了传输层的tcp协议和udp协议。
        这些协议对应的实现函数分别是ip_rcv(),tcp_v4_rcv()和udp_rcv()
        Linux内核中的fs_initcall和subsys_initcall类似，也是初始化模块的入口。
        fs_initcall调用inet_init后开始网络协议栈注册。
        通过inet_init，将这些函数注册到了inet_protos和ptype_base数据结构中了。
        这里我们需要记住inet_protos记录着udp，tcp的处理函数地址，
        ptype_base存储着ip_rcv()函数的处理地址。
        后面我们会看到软中断中会通过ptype_base找到ip_rcv函数地址，
        进而将ip包正确地送到ip_rcv()中执行
        在ip_rcv中将会通过inet_protos找到tcp或者udp的处理函数，
        再而把包转发给udp_rcv()或tcp_v4_rcv()函数。
        扩展一下，如果看一下ip_rcv和udp_rcv等函数的代码能看到很多协议的处理过程。
        例如，ip_rcv中会处理netfilter和iptable过滤，
        如果你有很多或者很复杂的 netfilter 或 iptables 规则，
        这些规则都是在软中断的上下文中执行的，会加大网络延迟。
        再例如，udp_rcv中会判断socket接收队列是否满了。
    2.4 网卡驱动初始化
        每一个驱动程序（不仅仅只是网卡驱动）会使用 module_init 向内核注册一个初始化函数，
        当驱动被加载时，内核会调用这个函数。
        static struct pci_driver igb_driver = {
            .name     = igb_driver_name,
            .id_table = igb_pci_tbl,
            .probe    = igb_probe,
            .remove   = igb_remove,
            ......
        };
        static int __init igb_init_module(void){
            ......
            int ret = pci_register_driver(&igb_driver);  //pci_register_driver为内核函数
            return ret;
        }
        module_init(igb_init_module);
        驱动的pci_register_driver调用完成后，Linux内核就知道了该驱动的相关信息，
        比如igb网卡驱动的igb_driver_name和igb_probe函数地址等等。
        当网卡设备被识别以后，内核会调用其驱动的probe方法（igb_probe）。
        驱动probe方法执行的目的就是让设备ready(包括DMA初始化、注册ethtool函数、
        注册net_device_ops、netdev等变量、NAPI初始化、注册poll函数)
        file://imgs/网卡驱动初始化.png
        从图中第5步中我们看到，网卡驱动实现了ethtool所需要的接口，也在这里注册完成函数地址的注册。
        当 ethtool 发起一个系统调用之后，内核会找到对应操作的回调函数。
        注：ethtool 是用于查询及设置网卡参数的命令
        这个命令之所以能查看网卡收发包统计、能修改网卡自适应模式、能调整RX 队列的数量和大小，
        是因为ethtool命令最终调用到了网卡驱动的相应方法，而不是ethtool本身有这个超能力。
        第6步注册的igb_netdev_ops中包含的是igb_open等函数，该函数在网卡被启动的时候会被调用。
        第7步中，在igb_probe初始化过程中，还调用到了igb_alloc_q_vector。
        他注册了一个NAPI机制所必须的poll函数，对于igb网卡驱动来说，这个函数就是igb_poll。
        static int igb_alloc_q_vector(struct igb_adapter *adapter, int v_count, int v_idx,
                                      int txr_count, int txr_idx, int rxr_count, int rxr_idx)
        {
            ......
            /* initialize NAPI */
            netif_napi_add(adapter->netdev, &q_vector->napi,igb_poll, 64);
        }
        注：NAPI机制
            随着网络带宽的发展，网速越来越快，之前的中断收包模式已经无法适应目前千兆，万兆的带宽了。
            如果每个数据包大小等于MTU大小1460字节。当驱动以千兆网速收包时，CPU将每秒被中断91829次。
            在以MTU收包的情况下都会出现每秒被中断10万次的情况。
            过多的中断会引起一个问题，CPU一直陷入硬中断而没有时间来处理别的事情了。
            为了解决这个问题，内核在2.6中引入了NAPI机制。
            NAPI就是混合中断和轮询的方式来收包，当有中断来了，驱动关闭中断，通知内核收包，
            内核软中断轮询当前网卡，在规定时间尽可能多的收包。时间用尽或者没有数据可收，
            内核再次开启中断，准备下一次收包。
            netif_napi_add：驱动初始时向内核注册软软中断处理回调poll函数
            __napi_schedule：网卡硬件中断用来触发软中断
            napi_poll：软中断处理函数net_rx_action用来回调上面驱动初始化时
                       通过netif_napi_add注册的回调收包poll函数
            napi_gro_receive：poll函数用来将网卡上的数据包发给协议栈处理。
            到这，NAPI机制下的收包处理流程就很清晰了。
            IRQ->__napi_schedule->进入软中断->net_rx_action->napi_poll->驱动注册的poll->napi_gro_receive。
    2.5 启动网卡
        当上面的初始化都完成以后，就可以启动网卡了
        前面网卡驱动初始化时，我们提到了驱动向内核注册了 structure net_device_ops 变量，
        它包含着网卡启用、发包、设置mac 地址等回调函数（函数指针）。
        当启用一个网卡时（例如，通过 ifconfig eth0 up），net_device_ops 中的 igb_open方法会被调用。
        它通常会做以下事情： file://imgs/启动网卡.png
        当做好以上准备工作以后，就可以开门迎客（数据包）了！
三 迎接数据的到来
    3.1 硬中断处理
        首先当数据帧从网线到达网卡上的时候，第一站是网卡的接收队列。
        网卡在分配给自己的RingBuffer中寻找可用的内存位置，
        找到后DMA引擎会把数据DMA到网卡之前关联的内存里，这个时候CPU都是无感的。
        当DMA操作完成以后，网卡会像CPU发起一个硬中断，通知CPU有数据到达。
        file://imgs/网卡数据硬中断处理过程.png
        注意：当RingBuffer满的时候，新来的数据包将给丢弃。
        ifconfig查看网卡的时候，可以里面有个overruns，表示因为环形队列满被丢弃的包。
        如果发现有丢包，可能需要通过ethtool命令来加大环形队列的长度。
        在启动网卡一节，我们说到了网卡的硬中断注册的处理函数是igb_msix_ring。
        static irqreturn_t igb_msix_ring(int irq, void *data){
            struct igb_q_vector *q_vector = data;
            /* Write the ITR value calculated from the previous interrupt. */
            igb_write_itr(q_vector);
            napi_schedule(&q_vector->napi);
            return IRQ_HANDLED;
        }
        igb_write_itr只是记录一下硬件中断频率（据说目的是在减少对CPU的中断频率时用到）。
        顺着napi_schedule调用一路跟踪下去，__napi_schedule=>____napi_schedule
        static inline void ____napi_schedule(struct softnet_data *sd, struct napi_struct *napi)
        {
            //将 napi->poll_list 添加到 sd->poll_list 中
            list_add_tail(&napi->poll_list, &sd->poll_list);  
            __raise_softirq_irqoff(NET_RX_SOFTIRQ);

        }
        list_add_tail修改了CPU变量softnet_data里的poll_list，
        将驱动napi_struct传过来的poll_list添加了进来
        __raise_softirq_irqoff触发了一个软中断NET_RX_SOFTIRQ， 
        这个所谓的触发过程只是对一个变量进行了一次或运算而已。
        Linux在硬中断里只完成简单必要的工作，剩下的大部分的处理都是转交给软中断的。
        通过上面代码可以看到，硬中断处理过程真的是非常短。
        只是记录了一个寄存器，修改了一下下CPU的poll_list，然后发出个软中断。
        就这么简单，硬中断工作就算是完成了。
    3.2 ksoftirqd内核线程处理软中断
        file://imgs/ksoftirqd内核线程.png
    3.3 网络协议栈处理
        file://imgs/网络协议栈处理.png
    3.4 IP协议层处理        
    3.5 UDP协议层处理
五 总结    
    首先在开始收包之前，Linux要做许多的准备工作：
    1. 创建ksoftirqd线程，为它设置好它自己的线程函数，后面指望着它来处理软中断呢
    2. 协议栈注册，linux要实现许多协议，比如arp，icmp，ip，udp，tcp，
       每一个协议都会将自己的处理函数注册一下，方便包来了迅速找到对应的处理函数
    3. 网卡驱动初始化，每个驱动都有一个初始化函数，内核会让驱动也初始化一下。
       在这个初始化过程中，把自己的DMA准备好，把NAPI的poll函数地址告诉内核
    4. 启动网卡，分配RX，TX队列，注册中断对应的处理函数
    以上是内核准备收包之前的重要工作，当上面都ready之后，就可以打开硬中断，等待数据包的到来了。
    当数据到来了以后，第一个迎接它的是网卡
    1. 网卡将数据帧DMA到内存的RingBuffer中，然后向CPU发起中断通知
    2. CPU响应中断请求，调用网卡启动时注册的中断处理函数
    3. 中断处理函数几乎没干啥，就发起了软中断请求
    4. 内核线程ksoftirqd线程发现有软中断请求到来，先关闭硬中断
    5. ksoftirqd线程开始调用驱动的poll函数收包
    6. poll函数将收到的包送到协议栈注册的ip_rcv函数中
    7. ip_rcv函数再讲包送到udp_rcv函数中（对于tcp包就送到tcp_rcv）
    现在我们可以回到开篇的问题了，我们在用户层看到的简单一行recvfrom,
    Linux内核要替我们做如此之多的工作，才能让我们顺利收到数据。
    这还是简简单单的UDP，如果是TCP，内核要做的工作更多
    理解了整个收包过程以后，我们就能明确知道Linux收一个包的CPU开销了。
    首先第一块是用户进程调用系统调用陷入内核态的开销。
    第二块是CPU响应包的硬中断的CPU开销。
    第三块是ksoftirqd内核线程的软中断上下文花费的