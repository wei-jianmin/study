https://cloud.tencent.com/developer/article/1883049?from=15425
    Linux实现的是链路层、网络层和传输层这三层
        在Linux内核实现中，链路层协议靠网卡驱动来实现，内核协议栈来实现网络层和传输层
        内核对更上层的应用层提供socket接口来供用户进程访问
        链路层：对0和1进行分组，定义数据帧，确认主机的物理地址，传输数据;
        网络层：定义IP地址，确认主机所在的网络位置，并通过IP进行MAC寻址，对外网数据包进行路由转发（发到哪个网卡）;
        传输层：定义端口，确认主机上应用程序的身份，并将数据包交给对应的应用程序;
        应用层：定义数据格式，并按照对应的格式解读数据。
    Linux 网卡收包时的中断处理问题
        中断的时间越短越好，尽快放开处理器，让它可以去响应下次中断甚至进行调度工作。
        基于此，我们将中断分成了上下两部分，上半部分就是上面说的中断部分，
        需要快速及时响应，同时需要越快结束越好。
        而下半部分就是完成一些可以推后执行的工作。
        对于网卡收包来说，网卡收到数据包，通知内核数据包到了，
        中断处理将数据包存入内存这些都是急切需要完成的工作，放到上半部完成。
        而解析处理数据包的工作则可以放到下半部去执行。
        软中断就是下半部使用的一种机制，它通过软件模仿硬件中断的处理过程，
        但是和硬件没有关系，单纯的通过软件达到一种异步处理的方式。
        其它下半部的处理机制还包括tasklet，工作队列等。
        依据所处理的场合不同，选择不同的机制，网卡收包一般使用软中断。
        Linux中断注册显然应该包括网卡的硬中断，包处理的软中断两个步骤
    理解：
        网卡驱动的一项主要任务就是注册并实现网卡的软硬中断处理函数
        不同的网卡驱动都可以注册到内核中，linux内核维护一个网卡驱动列表，
        发送数据时，根据路由表找到网卡信息，再根据网卡信息，找到对应的网卡驱动

https://zhuanlan.zhihu.com/p/373060740        
图解Linux网络包发送过程.pdf
    send 系统调用实现
        send系统调用位于源码 net/socket.c中
        在这个系统调用里，内部其实真正使用的是 sendto 系统调用。
        整个调用链条虽然不短，但其实主要只干了两件简单的事情
            1. 根据fd在内核中把真正的 socket 找出来，
               在这个对象里记录着各种协议栈的函数地址
            2. 构造一个 struct msghdr 对象，把用户传入的数据，
               比如 buffer地址、数据长度啥的，统统都装进去.
        剩下的事情就交给下一层，协议栈里的函数 inet_sendmsg 了
        inet_sendmsg 函数的地址是通过 socket 内核对象里的 ops 成员找到的
        sock_sendmsg(sock, &msghdr, len)
            __sock_sendmsg
                __sock_sendmsg_nosec
                    sock->ops->sendmsg(iocb, sock, msg, size)
                        inet_sendmsg
    传输层处理
        在进入到协议栈 inet_sendmsg 以后，内核接着会找到 socket 上的具体协议发送函数
        #使用哪种协议是在创建socket的时候指定的，如果实现自定义协议，则socket里记录的就是自定义协议函数的指针
        对于 TCP 协议来说，那就是 tcp_sendmsg（同样也是通过 socket 内核对象找到的）
        在这个函数中，内核会申请一个内核态的 skb 内存，将用户待发送的数据拷贝进去。
        注意这个时候不一定会真正开始发送，如果没有达到发送条件的话很可能这次调用直接就返回了。
        tcp_sendmsg
            //获取发送队列
            skb = tcp_write_queue_tail(sk);
                return skb_peek_tail(&sk->sk_write_queue);
            。。。
            if (skb没有足够的存储空间)
                //申请 skb，并添加到发送队列的尾部
                skb = sk_stream_alloc_skb(sk, select_size(sk, sg), sk->sk_allocation);
                //把 skb 挂到socket的发送队列上
                skb_entail(sk, skb);
            // skb 中有足够的空间
            if (skb_availroom(skb) > 0) {
                //拷贝用户空间的数据到内核空间，同时计算校验和
                //from是用户空间的数据地址 
                skb_add_data_nocache(sk, skb, from, copy);
            } 
            。。。
            //发送判断
            if (forced_push(tp)) {
                tcp_mark_push(tp, skb);
                __tcp_push_pending_frames(sk, mss_now, TCP_NAGLE_PUSH);
            } else if (skb == tcp_send_head(sk))
                tcp_push_one(sk, mss_now);  
            }
        理解对 socket 调用 tcp_write_queue_tail 是理解发送的前提
        这个函数是在获取 socket 发送队列中的最后一个 skb
        skb 是 struct sk_buff 对象的简称，用户的发送队列就是该对象组成的一个链表
        至于内核什么时候真正把 skb 发送出去。在 tcp_sendmsg 中会进行一些判断
        只有满足 forced_push(tp) 或者 skb == tcp_send_head(sk) 成立的时候，内核才会真正启动发送数据包。
        其中 forced_push(tp) 判断的是未发送的数据数据是否已经超过最大窗口的一半了。
        条件都不满足的话，这次的用户要发送的数据只是拷贝到内核就算完事了！
    传输层发送
        假设现在内核发送条件已经满足了，我们再来跟踪一下实际的发送过程。 
        对于上小节函数中，当满足真正发送条件的时候，
        无论调用的是 __tcp_push_pending_frames 还是 tcp_push_one 
        最终都实际会执行到 tcp_write_xmit
        所以我们直接从 tcp_write_xmit 看起，这个函数处理了传输层的拥塞控制、滑动窗口相关的工作。
        满足窗口要求的时候，设置一下 TCP 头然后将 skb 传到更低的网络层进行处理
        <file://imgs/1.jpg>
    网络层发送处理
        Linux 内核网络层的发送的实现位于 net/ipv4/ip_output.c 这个文件。
        传输层调用到的 ip_queue_xmit 也在这里
        在网络层里主要处理路由项查找、IP 头设置、netfilter 过滤、skb 切分（大于 MTU 的话）等几项工作
        <file://imgs/2.jpg>
        处理完这些工作后会交给更下层的邻居子系统来处理
        我们来看网络层入口函数 ip_queue_xmit 的源码：
        int ip_queue_xmit(struct sk_buff *skb, struct flowi *fl)
        {
            //检查 socket 中是否有缓存的路由表
            rt = (struct rtable *)__sk_dst_check(sk, 0);
            if (rt == NULL) {
                //没有缓存则展开查找路由项， 并缓存到 socket 中
                rt = ip_route_output_ports(...);
                sk_setup_caps(sk, &rt->dst);
            }
            //为 skb 设置路由表，后面发送时，使用哪个网卡，查skb就可以了
            skb_dst_set_noref(skb, &rt->dst);
            //设置 IP header
            iph = ip_hdr(skb);
            iph->protocol = sk->sk_protocol;
            iph->ttl      = ip_select_ttl(inet, &rt->dst);
            iph->frag_off = ...;
            //发送
            ip_local_out(skb);
                //执行 netfilter 过滤
                err = __ip_local_out(skb);
                //开始发送数据
                if (likely(err == 1))
                    err = dst_output(skb);
        }
        在路由表中，可以查到某个目的网络应该通过哪个 Iface（网卡），哪个 Gateway（网关）发送出去。
        #网关地址决定了链路层目的mac地址
        查找出来以后缓存到 socket 上，下次再发送数据就不用查了
        在ip_local_out => __ip_local_out => nf_hook 会执行 netfilter 过滤
        如果你使用 iptables 配置了一些规则，那么这里将检测是否命中规则。
        继续只聊和发送有关的过程 dst_output
        //file: include/net/dst.h
        static inline int dst_output(struct sk_buff *skb)
        {
            return skb_dst(skb)->output(skb);
        }
        此函数找到到这个 skb 的路由表（dst 条目） ，然后调用路由表的 output 方法。
        这又是一个函数指针，指向的是 ip_output 方法
        在 ip_output 中进行一些简单的，统计工作，再次执行 netfilter 过滤。
        过滤通过之后回调 ip_finish_output。
        //file: net/ipv4/ip_output.c
        static int ip_finish_output(struct sk_buff *skb)
        {
            //大于 mtu 的话就要进行分片了，实际 MTU 大小确定依赖 MTU 发现，以太网帧为 1500 字节
            if (skb->len > ip_skb_dst_mtu(skb) && !skb_is_gso(skb))
                return ip_fragment(skb, ip_finish_output2);
            else
                return ip_finish_output2(skb);
        }
        //file: net/ipv4/ip_output.c
        static inline int ip_finish_output2(struct sk_buff *skb)
        {
            //根据下一跳 IP 地址查找邻居项，找不到就创建一个
            nexthop = (__force u32) rt_nexthop(rt, ip_hdr(skb)->daddr);  
            neigh = __ipv4_neigh_lookup_noref(dev, nexthop);
            if (unlikely(!neigh))
                neigh = __neigh_create(&arp_tbl, &nexthop, dev, false);

            //继续向下层传递
            int res = dst_neigh_output(dst, neigh, skb);
        }
        ip_finish_output2中调用的函数的功能，在下一节介绍
    邻居子系统
        邻居子系统是位于网络层和数据链路层中间的一个系统，其作用是为网络层提供一个封装，
        让网络层不必关心下层的地址信息，让下层来决定发送到哪个 MAC 地址
        这个邻居子系统并不位于协议栈 net/ipv4/ 目录内，而是位于 net/core/neighbour.c。
        因为无论是对于 IPv4 还是 IPv6 ，都需要使用该模块
        在邻居子系统里主要是查找或者创建邻居项，在创造邻居项的时候，有可能会发出实际的 arp 请求。
        然后封装一下 MAC 头，将发送过程再传递到更下层的网络设备子系统。
        <file://imgs/3.jpg>
        上一节中，ip_finish_output2调用了__ipv4_neigh_lookup_noref，
        它是在 arp 缓存中进行查找，其第二个参数传入的是路由下一跳 IP 信息
        相关知识可参考 <file://路由表.txt>
        如果查找不到，则调用 __neigh_create 创建一个邻居
        有了邻居项以后，此时仍然还不具备发送 IP 报文的能力，因为目的 MAC 地址还未获取
        dst_neigh_output(struct dst_entry *dst, struct neighbour *n, struct sk_buff *skb)
            ...
            return n->output(n, skb);
                neigh_resolve_output
                    //注意：这里可能会触发 arp 请求
                    if (!neigh_event_send(neigh, skb))
                        //neigh->ha 是 MAC 地址
                        dev_hard_header(skb, dev, ntohs(skb->protocol), neigh->ha, NULL, skb->len);
                        //发送
                        dev_queue_xmit(skb);
        当获取到硬件 MAC 地址以后，就可以封装 skb 的 MAC 头了。
        最后调用 dev_queue_xmit 将 skb 传递给 Linux 网络设备子系统。
    网络设备子系统 &网络设备子系统
        网络设备子系统可看做是对网卡的封装，让上层不用关注用哪个网卡、哪个驱动来进行数据收发
        邻居子系统通过 dev_queue_xmit 进入到"网络设备子系统"中来    
        int dev_queue_xmit(struct sk_buff *skb)
        {
            //选择发送队列
            txq = netdev_pick_tx(dev, skb);
            //获取与此队列关联的排队规则
            q = rcu_dereference_bh(txq->qdisc);
            //如果有队列，则调用__dev_xmit_skb 继续处理数据
            if (q->enqueue) {
                rc = __dev_xmit_skb(skb, q, dev, txq);
                    //入队
                    q->enqueue(skb, q)
                    //开始发送
                    __qdisc_run(q);
                goto out;
            }
            //没有队列的是回环设备和隧道设备
            ......
        }
        网卡是有多个发送队列的（尤其是现在的网卡）
        在dev_queue_xmit中，会调用netdev_pick_tx，选择一个队列进行发送   
        然后获取与此队列关联的 qdisc 
            tc全称为traffic control，是iproute2包中控制内核中流量的工具
            qdisc实际是queueing discipline(纪律)的缩写，我们可以将其看作一个具有一定规则的队列
            在 linux 上通过 tc 命令可以看到 qdisc 类型：#tc qdisc
        在__dev_xmit_skb中，先调用 q->enqueue 把 skb 添加到队列里。然后调用 __qdisc_run 开始发送
        在__qdisc_run中，使用 while 循环不断地从队列中取出 skb 并调用驱动程序来发送数据