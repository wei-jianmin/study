https://cloud.tencent.com/developer/article/1883049?from=15425
    Linuxʵ�ֵ�����·�㡢�����ʹ����������
        ��Linux�ں�ʵ���У���·��Э�鿿����������ʵ�֣��ں�Э��ջ��ʵ�������ʹ����
        �ں˶Ը��ϲ��Ӧ�ò��ṩsocket�ӿ������û����̷���
        ��·�㣺��0��1���з��飬��������֡��ȷ�������������ַ����������;
        ����㣺����IP��ַ��ȷ���������ڵ�����λ�ã���ͨ��IP����MACѰַ�����������ݰ�����·��ת���������ĸ�������;
        ����㣺����˿ڣ�ȷ��������Ӧ�ó������ݣ��������ݰ�������Ӧ��Ӧ�ó���;
        Ӧ�ò㣺�������ݸ�ʽ�������ն�Ӧ�ĸ�ʽ������ݡ�
    Linux �����հ�ʱ���жϴ�������
        �жϵ�ʱ��Խ��Խ�ã�����ſ�����������������ȥ��Ӧ�´��ж��������е��ȹ�����
        ���ڴˣ����ǽ��жϷֳ������������֣��ϰ벿�־�������˵���жϲ��֣�
        ��Ҫ���ټ�ʱ��Ӧ��ͬʱ��ҪԽ�����Խ�á�
        ���°벿�־������һЩ�����ƺ�ִ�еĹ�����
        ���������հ���˵�������յ����ݰ���֪ͨ�ں����ݰ����ˣ�
        �жϴ������ݰ������ڴ���Щ���Ǽ�����Ҫ��ɵĹ������ŵ��ϰ벿��ɡ�
        �������������ݰ��Ĺ�������Էŵ��°벿ȥִ�С�
        ���жϾ����°벿ʹ�õ�һ�ֻ��ƣ���ͨ�����ģ��Ӳ���жϵĴ�����̣�
        ���Ǻ�Ӳ��û�й�ϵ��������ͨ������ﵽһ���첽����ķ�ʽ��
        �����°벿�Ĵ�����ƻ�����tasklet���������еȡ�
        ����������ĳ��ϲ�ͬ��ѡ��ͬ�Ļ��ƣ������հ�һ��ʹ�����жϡ�
        Linux�ж�ע����ȻӦ�ð���������Ӳ�жϣ�����������ж���������
    ��⣺
        ����������һ����Ҫ�������ע�Ტʵ����������Ӳ�жϴ�����
        ��ͬ����������������ע�ᵽ�ں��У�linux�ں�ά��һ�����������б�
        ��������ʱ������·�ɱ��ҵ�������Ϣ���ٸ���������Ϣ���ҵ���Ӧ����������

https://zhuanlan.zhihu.com/p/373060740        
ͼ��Linux��������͹���.pdf
    send ϵͳ����ʵ��
        sendϵͳ����λ��Դ�� net/socket.c��
        �����ϵͳ������ڲ���ʵ����ʹ�õ��� sendto ϵͳ���á�
        ��������������Ȼ���̣�����ʵ��Ҫֻ���������򵥵�����
            1. ����fd���ں��а������� socket �ҳ�����
               ������������¼�Ÿ���Э��ջ�ĺ�����ַ
            2. ����һ�� struct msghdr ���󣬰��û���������ݣ�
               ���� buffer��ַ�����ݳ���ɶ�ģ�ͳͳ��װ��ȥ.
        ʣ�µ�����ͽ�����һ�㣬Э��ջ��ĺ��� inet_sendmsg ��
        inet_sendmsg �����ĵ�ַ��ͨ�� socket �ں˶������ ops ��Ա�ҵ���
        sock_sendmsg(sock, &msghdr, len)
            __sock_sendmsg
                __sock_sendmsg_nosec
                    sock->ops->sendmsg(iocb, sock, msg, size)
                        inet_sendmsg
    ����㴦��
        �ڽ��뵽Э��ջ inet_sendmsg �Ժ��ں˽��Ż��ҵ� socket �ϵľ���Э�鷢�ͺ���
        #ʹ������Э�����ڴ���socket��ʱ��ָ���ģ����ʵ���Զ���Э�飬��socket���¼�ľ����Զ���Э�麯����ָ��
        ���� TCP Э����˵���Ǿ��� tcp_sendmsg��ͬ��Ҳ��ͨ�� socket �ں˶����ҵ��ģ�
        ����������У��ں˻�����һ���ں�̬�� skb �ڴ棬���û������͵����ݿ�����ȥ��
        ע�����ʱ��һ����������ʼ���ͣ����û�дﵽ���������Ļ��ܿ�����ε���ֱ�Ӿͷ����ˡ�
        tcp_sendmsg
            //��ȡ���Ͷ���
            skb = tcp_write_queue_tail(sk);
                return skb_peek_tail(&sk->sk_write_queue);
            ������
            if (skbû���㹻�Ĵ洢�ռ�)
                //���� skb������ӵ����Ͷ��е�β��
                skb = sk_stream_alloc_skb(sk, select_size(sk, sg), sk->sk_allocation);
                //�� skb �ҵ�socket�ķ��Ͷ�����
                skb_entail(sk, skb);
            // skb �����㹻�Ŀռ�
            if (skb_availroom(skb) > 0) {
                //�����û��ռ�����ݵ��ں˿ռ䣬ͬʱ����У���
                //from���û��ռ�����ݵ�ַ 
                skb_add_data_nocache(sk, skb, from, copy);
            } 
            ������
            //�����ж�
            if (forced_push(tp)) {
                tcp_mark_push(tp, skb);
                __tcp_push_pending_frames(sk, mss_now, TCP_NAGLE_PUSH);
            } else if (skb == tcp_send_head(sk))
                tcp_push_one(sk, mss_now);  
            }
        ���� socket ���� tcp_write_queue_tail ����ⷢ�͵�ǰ��
        ����������ڻ�ȡ socket ���Ͷ����е����һ�� skb
        skb �� struct sk_buff ����ļ�ƣ��û��ķ��Ͷ��о��Ǹö�����ɵ�һ������
        �����ں�ʲôʱ�������� skb ���ͳ�ȥ���� tcp_sendmsg �л����һЩ�ж�
        ֻ������ forced_push(tp) ���� skb == tcp_send_head(sk) ������ʱ���ں˲Ż����������������ݰ���
        ���� forced_push(tp) �жϵ���δ���͵����������Ƿ��Ѿ�������󴰿ڵ�һ���ˡ�
        ������������Ļ�����ε��û�Ҫ���͵�����ֻ�ǿ������ں˾��������ˣ�
    ����㷢��
        ���������ں˷��������Ѿ������ˣ�������������һ��ʵ�ʵķ��͹��̡� 
        ������С�ں����У���������������������ʱ��
        ���۵��õ��� __tcp_push_pending_frames ���� tcp_push_one 
        ���ն�ʵ�ʻ�ִ�е� tcp_write_xmit
        ��������ֱ�Ӵ� tcp_write_xmit ����������������˴�����ӵ�����ơ�����������صĹ�����
        ���㴰��Ҫ���ʱ������һ�� TCP ͷȻ�� skb �������͵��������д���
        <file://imgs/1.jpg>
    ����㷢�ʹ���
        Linux �ں������ķ��͵�ʵ��λ�� net/ipv4/ip_output.c ����ļ���
        �������õ��� ip_queue_xmit Ҳ������
        �����������Ҫ����·������ҡ�IP ͷ���á�netfilter ���ˡ�skb �з֣����� MTU �Ļ����ȼ����
        <file://imgs/2.jpg>
        ��������Щ������ύ�����²���ھ���ϵͳ������
        ���������������ں��� ip_queue_xmit ��Դ�룺
        int ip_queue_xmit(struct sk_buff *skb, struct flowi *fl)
        {
            //��� socket ���Ƿ��л����·�ɱ�
            rt = (struct rtable *)__sk_dst_check(sk, 0);
            if (rt == NULL) {
                //û�л�����չ������·��� �����浽 socket ��
                rt = ip_route_output_ports(...);
                sk_setup_caps(sk, &rt->dst);
            }
            //Ϊ skb ����·�ɱ����淢��ʱ��ʹ���ĸ���������skb�Ϳ�����
            skb_dst_set_noref(skb, &rt->dst);
            //���� IP header
            iph = ip_hdr(skb);
            iph->protocol = sk->sk_protocol;
            iph->ttl      = ip_select_ttl(inet, &rt->dst);
            iph->frag_off = ...;
            //����
            ip_local_out(skb);
                //ִ�� netfilter ����
                err = __ip_local_out(skb);
                //��ʼ��������
                if (likely(err == 1))
                    err = dst_output(skb);
        }
        ��·�ɱ��У����Բ鵽ĳ��Ŀ������Ӧ��ͨ���ĸ� Iface�����������ĸ� Gateway�����أ����ͳ�ȥ��
        #���ص�ַ��������·��Ŀ��mac��ַ
        ���ҳ����Ժ󻺴浽 socket �ϣ��´��ٷ������ݾͲ��ò���
        ��ip_local_out => __ip_local_out => nf_hook ��ִ�� netfilter ����
        �����ʹ�� iptables ������һЩ������ô���ｫ����Ƿ����й���
        ����ֻ�ĺͷ����йصĹ��� dst_output
        //file: include/net/dst.h
        static inline int dst_output(struct sk_buff *skb)
        {
            return skb_dst(skb)->output(skb);
        }
        �˺����ҵ������ skb ��·�ɱ�dst ��Ŀ�� ��Ȼ�����·�ɱ�� output ������
        ������һ������ָ�룬ָ����� ip_output ����
        �� ip_output �н���һЩ�򵥵ģ�ͳ�ƹ������ٴ�ִ�� netfilter ���ˡ�
        ����ͨ��֮��ص� ip_finish_output��
        //file: net/ipv4/ip_output.c
        static int ip_finish_output(struct sk_buff *skb)
        {
            //���� mtu �Ļ���Ҫ���з�Ƭ�ˣ�ʵ�� MTU ��Сȷ������ MTU ���֣���̫��֡Ϊ 1500 �ֽ�
            if (skb->len > ip_skb_dst_mtu(skb) && !skb_is_gso(skb))
                return ip_fragment(skb, ip_finish_output2);
            else
                return ip_finish_output2(skb);
        }
        //file: net/ipv4/ip_output.c
        static inline int ip_finish_output2(struct sk_buff *skb)
        {
            //������һ�� IP ��ַ�����ھ���Ҳ����ʹ���һ��
            nexthop = (__force u32) rt_nexthop(rt, ip_hdr(skb)->daddr);  
            neigh = __ipv4_neigh_lookup_noref(dev, nexthop);
            if (unlikely(!neigh))
                neigh = __neigh_create(&arp_tbl, &nexthop, dev, false);

            //�������²㴫��
            int res = dst_neigh_output(dst, neigh, skb);
        }
        ip_finish_output2�е��õĺ����Ĺ��ܣ�����һ�ڽ���
    �ھ���ϵͳ
        �ھ���ϵͳ��λ��������������·���м��һ��ϵͳ����������Ϊ������ṩһ����װ��
        ������㲻�ع����²�ĵ�ַ��Ϣ�����²����������͵��ĸ� MAC ��ַ
        ����ھ���ϵͳ����λ��Э��ջ net/ipv4/ Ŀ¼�ڣ�����λ�� net/core/neighbour.c��
        ��Ϊ�����Ƕ��� IPv4 ���� IPv6 ������Ҫʹ�ø�ģ��
        ���ھ���ϵͳ����Ҫ�ǲ��һ��ߴ����ھ���ڴ����ھ����ʱ���п��ܻᷢ��ʵ�ʵ� arp ����
        Ȼ���װһ�� MAC ͷ�������͹����ٴ��ݵ����²�������豸��ϵͳ��
        <file://imgs/3.jpg>
        ��һ���У�ip_finish_output2������__ipv4_neigh_lookup_noref��
        ������ arp �����н��в��ң���ڶ��������������·����һ�� IP ��Ϣ
        ���֪ʶ�ɲο� <file://·�ɱ�.txt>
        ������Ҳ���������� __neigh_create ����һ���ھ�
        �����ھ����Ժ󣬴�ʱ��Ȼ�����߱����� IP ���ĵ���������ΪĿ�� MAC ��ַ��δ��ȡ
        dst_neigh_output(struct dst_entry *dst, struct neighbour *n, struct sk_buff *skb)
            ...
            return n->output(n, skb);
                neigh_resolve_output
                    //ע�⣺������ܻᴥ�� arp ����
                    if (!neigh_event_send(neigh, skb))
                        //neigh->ha �� MAC ��ַ
                        dev_hard_header(skb, dev, ntohs(skb->protocol), neigh->ha, NULL, skb->len);
                        //����
                        dev_queue_xmit(skb);
        ����ȡ��Ӳ�� MAC ��ַ�Ժ󣬾Ϳ��Է�װ skb �� MAC ͷ�ˡ�
        ������ dev_queue_xmit �� skb ���ݸ� Linux �����豸��ϵͳ��
    �����豸��ϵͳ &�����豸��ϵͳ
        �����豸��ϵͳ�ɿ����Ƕ������ķ�װ�����ϲ㲻�ù�ע���ĸ��������ĸ����������������շ�
        �ھ���ϵͳͨ�� dev_queue_xmit ���뵽"�����豸��ϵͳ"����    
        int dev_queue_xmit(struct sk_buff *skb)
        {
            //ѡ���Ͷ���
            txq = netdev_pick_tx(dev, skb);
            //��ȡ��˶��й������Ŷӹ���
            q = rcu_dereference_bh(txq->qdisc);
            //����ж��У������__dev_xmit_skb ������������
            if (q->enqueue) {
                rc = __dev_xmit_skb(skb, q, dev, txq);
                    //���
                    q->enqueue(skb, q)
                    //��ʼ����
                    __qdisc_run(q);
                goto out;
            }
            //û�ж��е��ǻػ��豸������豸
            ......
        }
        �������ж�����Ͷ��еģ����������ڵ�������
        ��dev_queue_xmit�У������netdev_pick_tx��ѡ��һ�����н��з���   
        Ȼ���ȡ��˶��й����� qdisc 
            tcȫ��Ϊtraffic control����iproute2���п����ں��������Ĺ���
            qdiscʵ����queueing discipline(����)����д�����ǿ��Խ��俴��һ������һ������Ķ���
            �� linux ��ͨ�� tc ������Կ��� qdisc ���ͣ�#tc qdisc
        ��__dev_xmit_skb�У��ȵ��� q->enqueue �� skb ��ӵ������Ȼ����� __qdisc_run ��ʼ����
        ��__qdisc_run�У�ʹ�� while ѭ�����ϵشӶ�����ȡ�� skb ������������������������