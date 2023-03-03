file://imgs/数据包收发过程的调用逻辑图.jpg
    从图中可以看到，*ip_rcv*函数为网络层向下层开放的入口，数据包通过该函数进入网络层进行处理，
    该函数主要对上传到网络层的数据包进行前期合法性检查，通过后交由 Netfilter 的钩子节点；
    绿色方框内的IP_PRE_ROUTING为 Netfilter 框架的 Hook 点，
    该节点会根据预设的规则对数据包进行判决并根据判决结果做相关的处理，比如执行 NAT 转换；
    IP_PRE_ROUTING节点处理完成后，数据包将交由*ip_rcv_finish*处理，
    该函数根据路由判决结果，决定数据包是交由本机上层应用处理，还是需要进行转发；
    如果是交由本机处理，则会交由*ip_local_deliver*走本地上交流程；
    如果需要转发，则交由*ip_forward*函数走转发流程；
    在数据包上交本地的流程中，IP_LOCAL_INPUT节点用于监控和检查上交到本地上层应用的数据包，
    该节点是 Linux 防火墙的重要生效节点之一；
    在数据包转发流程中，Netfilter 框架的IP_FORWARD节点会对转发数据包进行检查过滤；
    而对于本机上层发出的数据包，网络层通过注册到上层的*ip_local_out*函数接收数据处理，
    处理 OK 进一步交由IP_LOCAL_OUT节点检测；
    对于即将发往下层的数据包，需要经过IP_POST_ROUTING节点处理；网络层处理结束，
    通过*dev_queue_xmit*函数将数据包交由 Linux 内核中虚拟网络设备做进一步处理，
    从这里数据包即离开网络层进入到下一层；
    相关参考：
        file://imgs/四表五链的关系图.png
        file://imgs/接收 IPsec 数据包（传输模式）流程图.jpg   
        file://imgs/发送 IPsec 数据包（传输模式）流程图.jpg
        file://imgs/xfrm_lookup流程图.jpg
        file://imgs/数据包发送过程.png
        file://imgs/网络协议栈处理.png
        file://imgs/网络包的流动图.png
        file://图解Linux网络包接收过程.py
        file://imgs/数据包收发过程.png