https://blog.csdn.net/w17691058648x/article/details/100087113

�����������ָ�����������ͨ����װ�Լ����װ�����ڹ����Ͻ���һ������ͨ����ʹ������ͨ�������ݱ��Ľ��д���

��������Ƚϣ�
---------------------------------------------------------------------------------------------------------------------��
���Э��    ������Χ          ʹ�ó���                �û������֤                        ���ܺ���֤                 ��
---------------------------------------------------------------------------------------------------------------------��
GRE         IP�㼰��������    Intranet VPN            ��֧��                              ֧�ּ򵥵Ĺؼ�����֤��У�� ��
---------------------------------------------------------------------------------------------------------------------��
L2TP        IP�㼰��������    Access VPN/ExtranetVPN  ֧�ֻ���PPP��CHAP��PAP��EAP��֤     ��֧��                     ��
---------------------------------------------------------------------------------------------------------------------��
IP sec      IP�㼰��������    Intranet VPN/           ֧���빲����Կ��֤����֤��          ֧��                       ��
                              Access VPN/Extranet VPN ֧��IKEv2��EAP��֤                                             ��
---------------------------------------------------------------------------------------------------------------------��
Sangfor VPN IP�㼰��������    Intranet VPN/           ֧�ֶ��������֤                    ֧��                       ��
                              Extranet VPN                                                                           ��
---------------------------------------------------------------------------------------------------------------------��
SSL VPN     Ӧ�ò��ض�����    Access VPN              ֧�ֶ��������֤                    ֧��                       ��
---------------------------------------------------------------------------------------------------------------------��

��IPsec����һ��IP��֮ǰ�������Ƚ�����ȫ������SA��
IPSec�İ�ȫ��������ͨ���ֹ����õķ�ʽ���������ǵ������нڵ�϶�ʱ���ֹ����ý��ǳ����ѣ��������Ա�֤��ȫ�ԡ�
��ʱ�Ϳ���ʹ��IKE�� Internet Key Exchange���Զ����а�ȫ������������Կ�����Ĺ��̡� 
Internet��Կ������ IKE�������ڶ�̬����SA������IPSec��SA����Э��

IKE���Զ����а�ȫ������������Կ�����Ĺ���
��;��
IKEΪIPsecЭ��������Կ����AH/ESP�ӽ��ܺ���֤ʹ�á�
��IPSecͨ��˫��֮�䣬 ��̬�ؽ�����ȫ������ SA�� SecurityAssociation������SA���й����ά��

IKE�Ĺ�������
��һ�׶Σ��˴˼佨����һ����ͨ�������֤�Ͱ�ȫ������ͨ�����˽׶εĽ���������һ��ISAKMP��ȫ����

--------------------------------------------------------------------------------------------------

http://www.unixwiz.net/techtips/iguide-ipsec.html

ipsec�����úܸ��ӣ�һ��ԭ���ǣ�
    Psec�ṩ���ǻ��ƣ������ǲ��ԣ������Ƕ������������ļ����㷨��ĳ�������֤���ܣ�
    �����ṩ��һ����ܣ�����ʵ���ṩ�����κ�˫����ͬ��Ķ�����
    
ip���ݰ���Я����Э�����ͣ����֣�
    Protocol code	Protocol Description
    1	            ICMP �� Internet Control Message Protocol
    2	            IGMP �� Internet Group Management Protocol
    4	            IP within IP (a kind of encapsulation)
    6	            TCP �� Transmission Control Protocol
    17	            UDP �� User Datagram Protocol
    41	            IPv6 �� next-generation TCP/IP
    47	            GRE �� Generic Router Encapsulation (used by PPTP)
    50	            IPsec: ESP �� Encapsulating Security Payload
    51	            IPsec: AH �� Authentication Header

AH��ESP���������֤�Ĺ��ܣ����ǽ���HMAC�ṩ�ģ��������ipsec��ʱ����Ҫָ��hamcҪ�õ���ֵ��

ipsec����������ʱ�������������������͵ģ�
    ͼ��file://imgs/IPSec-VPN����.gif
    
ʹ��ESP����AH ��    
    ���� AH �������ַת������ľ����ԣ���ʵ���в������ã���֧��NAT��
    
SA �� SPI
    �� IPsec ���ݱ���AH �� ESP������ӿ�ʱ���ӿ����֪��Ҫʹ����������������㷨�Ͳ��ԣ���
    �κ����������Խ���������ڽ��еĶԻ���ÿ���Ի�����һ�鲻ͬ����Կ���㷨�����ұ����ܹ�ָ�����ִ���
    ���ɰ�ȫ���� ��SA��ָ����SA �������ض������ļ��ϣ�ÿ����������һ��������ȫ������
    �����ݱ�����ʱ����ʹ�����������ڰ�ȫ�������ݿ� ��SADB�� �в�����ȷ�� SA:
        ������� IP ��ַ + IPsec Э�飨ESP �� AH�� + ��ȫ��������
    ��ȫ�����ǵ���ģ����˫�����ӣ����������������Ҫ����
    SADB�б����˴�����Ϣ������ֻ�ܴ������е�һЩ��
        AH�������֤�㷨
        AH�������֤����
        ESP�������㷨
        ESP��������Կ
        ESP�������֤��������/��
        �����Կ��������
        ·������
        IP ɸѡ����
    
��Կ����    
    ���û�������֤�ͼ��ܵļ��ܹ��ܣ�IPsec�����������ô�
    IKE ʹ�� ISAKMP����������ȫЭ����Կ����Э�飩��Ϊ��ܣ�֧�ֽ��������˼��ݵİ�ȫЭ�ᡣ
    ֧�ֶ�����Կ����Э�鱾������Oakley��ʹ����㷺��Э�顣
    ���ǽ�ע�⵽ IPsec ��Կ����ͨ��ͨ���˿� 500/udp ����
    
===============================================================================================
    
https://apprize.best/linux/kernel/11.html 
IPsec�ѳ�Ϊ�����ϴ����IP����ר�����磨VPN�������ı�׼��������ζ�ţ�Ҳ�л��ڲ�ͬ������VPN��
���簲ȫ�׽��ֲ㣨SSL����pptp��ͨ��GREЭ���������PPP���ӣ�   

�����ȼ�Ҫ���� IPsec �е� Internet ��Կ���� ��IKE�� 
�û��ռ��ػ�����ͼ��ܡ���Щ����ͨ�������ں������ջ��һ���֣����� IPsec ������أ�
��Ҫ��Щ������ܸ��õ��˽��ں� IPsec ��ϵͳ��
���������ҽ����� XFRM ��ܣ��ÿ���� IPsec �û��ռ䲿�ֺ� IPsec �ں����֮������úͼ��ӽӿڣ�
�������� IPsec ���ݰ��� Tx �� Rx ·���еı�����
�ڱ��µ��������һС�ڽ��� IPsec �е� NAT ����������һ����Ҫ����Ȥ�Ĺ���

IKE ����������Կ������
    �����еĿ�Դ�û��ռ�Linux IPsec���������
    Openswan����libreswan����Openswan�ֲ��������strongSwan��racoon��ipsec-tools����
    Racoon��Kame��Ŀ��һ���֣�����Ŀּ��ΪBSD�ı����ṩ��ѵ�IPv6��IPsecЭ��ջʵ�֡�
    Openswan �� strongSwan ʵ���ṩ��һ�� IKE �ػ�����
    ��Openswan �е� pluto �� strongSwan �е� charon��
    ��ʹ�� UDP �˿� 500��Դ��Ŀ�꣩�����ͺͽ��� IKE ��Ϣ
    ���߶�ʹ��XFRM Netlink�ӿ���Linux�ں˵ı���IPsec��ջ����ͨ�š�
    strongSwan��Ŀ��RFC 5996��Internet Key Exchange Protocol Version 2��IKEv2������Ψһ�����Ŀ�Դʵ�֣�
    ��Openswan��Ŀ��ʵ��һ��С��ǿ���Ӽ�
    
    �������� Openswan �� strongSwan 5.x ��ʹ�� IKEv1 Aggressive Mode
    ������ strongSwan��Ӧ��ʽ������������������£�charon �ػ���������Ƹ���Ϊ weakSwan��;
    ����ѡ���Ϊ�ǲ���ȫ��
    
    IKEv2 Э�鲻���ֽ׶� 1 �ͽ׶� 2�����ǽ���һ��CHILD_SA��ΪIKE_AUTH��Ϣ������һ���֡�
    CHILD_SA_CREATE��Ϣ���������ڽ�������CHILD_SAs������������ IKE �� IPsec SA ����Կ��
    
XFRM ���
    �ÿ����Դ��USAGI��Ŀ��ּ���ṩ������������IPv6��IPsecЭ��ջ
    XFRM ������ʩ������Э���壬����ζ�� IPv4 �� IPv6 ����һ��ͨ�ò��֣�λ�� net/xfrm �¡�
    IPv4 �� IPv6 �����Լ��� ESP��AH �� IPCOMP ʵ�֡�
    ���磬IPv4 ESP ģ���� net/ipv4/esp4.c��IPv6 ESP ģ���� net/ipv6/esp6.c��
    ���������ռ�
        XFRM ���֧�����������ռ䣬����һ���������������⻯��ʽ��
        ��ʹ�������̻�һ������ܹ�ӵ���Լ��������ջ
        ÿ�����������ռ䣨�ṹ����ʵ����������һ����Ϊ xfrm �ĳ�Ա������netns_xfrm�ṹ��һ��ʵ����
        struct netns_xfrm {
            struct hlist_head *state_bydst;
            struct hlist_head *state_bysrc;
            struct hlist_head *state_byspi;
            . . .
            unsigned int state_num;
            . . .
            struct work_struct state_gc_work;
            . . .
            u32 sysctl_aevent_etime;
            u32 sysctl_aevent_rseqth;
            int sysctl_larval_drop;
            u32 sysctl_acq_expires;
            };
    XFRM ��ʼ��
        �� IPv4 �У�XFRM ��ʼ����ͨ���� net/ipv4/route.c �е� 
        ip_rt_init���� �������� xfrm_init���� ������ xfrm4_init���� ��������ɵ�
        �û��ռ���ں�֮���ͨ����ͨ������NETLINK_XFRM���������׽��ֲ����ͺͽ�������������Ϣ����ɵ�
        netlink NETLINK_XFRM�ں��׽�����ͨ�����·��������ģ�
        static int __net_init xfrm_user_net_init��struct net *net��
        {
            struct sock *nlsk;
            struct netlink_kernel_cfg cfg = {
                .groups = XFRMNLGRP_MAX��
                .input = xfrm_netlink_rcv��
                };
            nlsk = netlink_kernel_create��net�� NETLINK_XFRM�� &cfg��;
            ...
            return 0;
        }
        ���û��ռ䷢�͵���Ϣ
        �������ڴ����°�ȫ���Ե�XFRM_MSG_NEWPOLICY�����ڴ����°�ȫ������XFRM_MSG_NEWSA��
        ��xfrm_netlink_rcv����������net/xfrm/xfrm_user.c������
        �÷����ֵ���thexfrm_user_rcv_msg��������
        
        XFRM ���Ժ� XFRM ״̬�� XFRM ��ܵĻ������ݽṹ��
        �����Ժ�״̬���ں˽ṹ���ɼ���Ŀ¼�µ������ļ���
        xfrm_policy�ṹ����Ҫ��Ա��
            �� refcnt: 
                The XFRM policy reference counter; initialized to 1 in the xfrm_policy_alloc( ) method, 
                incremented by the xfrm_pol_hold() method, and decremented by the xfrm_pol_put() method.
            �� timer: 
                Per-policy timer; the timer callback is set to be xfrm_policy_timer() in the xfrm_policy_alloc() method. 
                The xfrm_policy_timer() method handles policy expiration: it is responsible for deleting a policy 
                when it is expired by calling thexfrm_policy_delete() method, 
                and sending an event (XFRM_MSG_POLEXPIRE) to all registered Key Managers 
                by calling the km_policy_expired() method.
            �� lft: 
                The XFRM policy lifetime (xfrm_lifetime_cfg object).
                 Every XFRM policy has a lifetime, which is a time interval (expressed as a time or byte count).
                You can set XFRM policy lifetime values with the ip command and the limit parameter��for example:
                ip xfrm policy add src 172.16.2.0/24 dst 172.16.1.0/24 limit byte-soft 6000 ...
            �� sets 
                the soft_byte_limit of the XFRM policy lifetime (lft) to be 6000; see man 8 ip xfrm.
                You can display the lifetime (lft) of an XFRM policy by inspecting the lifetime configuration entry 
                when running ip -stat xfrm policy show.
            �� curlft: 
                The XFRM policy current lifetime, which reflects the current status of the policy in context of lifetime. 
                The curlft is an xfrm_lifetime_cur object. It consists of four members
                 (all of them are fields of 64 bits, unsigned):
            �� bytes: 
                The number of bytes which were processed by the IPsec subsystem, 
                incremented in the Tx path by the xfrm_output_one() method and in the Rx path by the xfrm_input() method.
            �� packets: 
                The number of packets that were processed by the IPsec subsystem, 
                incremented in the Tx path by the xfrm_output_one() method, 
                and in the Rx path by the xfrm_input() method.
            �� add_time
                The timestamp of adding the policy, initialized when adding a policy, 
                in the xfrm_policy_insert() method and in the xfrm_sk_policy_insert() method.
            �� use_time: 
                The timestamp of last access to the policy. The use_time timestamp is updated,
                 for example, in the xfrm_lookup() method or in the __xfrm_policy_check() method. 
                 Initialized to 0 when adding the XFRM policy, in thexfrm_policy_insert() method 
                 and in the xfrm_sk_policy_insert() method.
                image Note You can display the current lifetime (curlft) object of an XFRM policy 
                by inspecting the lifetime current entry when running ip -stat xfrm policy show.
            �� polq: 
                A queue to hold packets that are sent while there are still no XFRM states associated with the policy. 
                As a default, such packets are discarded by calling the make_blackhole() method. 
                When setting the xfrm_larval_drop sysctl entry to 0 (/proc/sys/net/core/xfrm_larval_drop), 
                these packets are kept in a queue (polq.hold_queue) of SKBs; 
                up to 100 packets (XFRM_MAX_QUEUE_LEN) can be kept in this queue. 
                This is done by creating a dummy XFRM bundle, 
                by thexfrm_create_dummy_bundle() method (see more in the ��XFRM lookup�� section later in this chapter). 
                By default, the xfrm_larval_drop sysctl entry is set to 1 
                (see the __xfrm_sysctl_init() method in net/xfrm/xfrm_sysctl.c).
            �� type: 
                Usually the type is XFRM_POLICY_TYPE_MAIN (0). 
                When the kernel has support for subpolicy (CONFIG_XFRM_SUB_POLICY is set), 
                two policies can be applied to the same packet, and you can use the XFRM_POLICY_TYPE_SUB (1) type. 
                Policy that lives a shorter time in kernel should be a subpolicy. 
                This feature is usually needed only for developers/debugging and for mobile IPv6, 
                because you might apply one policy for IPsec and one for mobile IPv6. 
                The IPsec policy is usually the main policy with a longer lifetime than the mobile IPv6 (sub) policy.
            �� action: 
                Can have one of these two values:
            �� XFRM_POLICY_ALLOW (0): 
                Permit the traffic.
            �� XFRM_POLICY_BLOCK(1): 
                Disallow the traffic (for example, when using type=reject or type=drop in /etc/ipsec.conf).
            �� xfrm_nr: 
                Number of templates associated with the policy��can be up to six templates (XFRM_MAX_DEPTH). 
                The xfrm_tmpl structure is an intermediate structure between the XFRM state and the XFRM policy. 
                It is initialized in the copy_templates()method, net/xfrm/xfrm_user.c.
            �� family: 
                IPv4 or IPv6.
            �� security: 
                A security context (xfrm_sec_ctx object) that allows the XFRM subsystem to restrict the sockets 
                that can send or receive packets via Security Associations (XFRM states). 
                For more details, see http://lwn.net/Articles/156604/.
            �� xfrm_vec: An array of XFRM templates (xfrm_tmpl objects).
                The kernel stores the IPsec Security Policies in the Security Policy Database (SPD). 
                Management of the SPD is done by sending messages from a userspace socket. For example:
            �� Adding 
                an XFRM policy (XFRM_MSG_NEWPOLICY) is handled by the xfrm_add_policy() method.
            �� Deleting 
                an XFRM policy (XFRM_MSG_DELPOLICY) is handled by the xfrm_get_policy() method.
            �� Displaying 
                the SPD (XFRM_MSG_GETPOLICY) is handled by the xfrm_dump_policy() method.
            �� Flushing 
                the SPD (XFRM_MSG_FLUSHPOLICY) is handled by the xfrm_flush_policy() method.
        xfrm_state�ṹ����Ҫ��Ա��
            �� refcnt: 
                A reference counter, incremented by the xfrm_state_hold() method and decremented 
                by the __xfrm_state_put() method or by the xfrm_state_put() method 
                (the latter also releases the XFRM state by calling the__xfrm_state_destroy() method 
                when the reference counter reaches 0).
            �� id: 
                The id (xfrm_id object) consists of three fields, which uniquely define it: 
                destination address, spi, and security protocol (AH, ESP, or IPCOMP).
            �� props: 
                The properties of the XFRM state. For example:
            �� mode: 
                Can be one of five modes (for example, XFRM_MODE_TRANSPORT for transport mode 
                or XFRM_MODE_TUNNEL for tunnel mode; see include/uapi/linux/xfrm.h).
            �� flag: 
                For example, XFRM_STATE_ICMP. These flags are available in include/uapi/linux/xfrm.h. 
                These flags can be set from userspace, 
                for example, with the ip command and the flag option: ip xfrm add state flag icmp ...
            �� family: 
                IPv4 of IPv6.
            �� saddr: 
                The source address of the XFRM state.
            �� lft: 
                The XFRM state lifetime (xfrm_lifetime_cfg object).
            �� stats: 
                An xfrm_stats object, representing XFRM state statistics. 
                You can display the XFRM state statistics by ip �Cstat xfrm show.
        �ں˽� IPsec ��ȫ�����洢�ڰ�ȫ�������ݿ� ��SAD�� �С�
        xfrm_state����洢��netns_xfrm��ǰ�����۵� XFRM �����ռ䣩��������ϣ���У�
        state_bydst��state_bysrc��state_byspi��
        ��Щ��ļ��ֱ��� xfrm_dst_hash������xfrm_src_hash���� �� xfrm_spi_hash���� ��������
        ���xfrm_state����ʱ���Ὣ����뵽��������ϣ���С�
        ��� spi ��ֵΪ 0��ֵ 0 ͨ�������� spi �� �Һܿ�ͻ��ᵽ������ 0 ʱ����
        �� xfrm_state ���󲻻���ӵ�state_byspi��ϣ����
        ֵΪ 0 �� spi �����ڻ�ȡ״̬��
            �ں�����Կ���������ͻ�ȡ��Ϣ��
            ������������ƥ�䣬��״̬��δ����������� spi 0 ����ʱ��ȡ״̬��
            ֻҪ��ȡ״̬���ڣ��ں˾Ͳ�����ķ��ͽ�һ���Ļ�ȡ;
            ���״̬�õ��������˻�ȡ״̬���滻Ϊʵ��״̬��
        SAD �еĲ��ҿ���ͨ�����·�ʽ��ɣ�
            ��xfrm_state_lookup���� ��������state_byspi��ϣ���С�
            ��xfrm_state_lookup_byaddr���� ��������state_bysrc��ϣ���С�
            ��xfrm_state_find���� ��������state_bydst��ϣ���С�

ESP ʵʩ ��IPv4��   
    �� RFC 4303 ��ָ���� ESP Э��;��֧�ּ��ܺ������֤��
    ��Ȼ����֧�ֽ����ܺͽ������֤ģʽ��
    ����ͨ������ܺ������֤һ��ʹ�ã���Ϊ������ȫ��
    ͼ��file://imgs/���� IPsec ���ݰ�������ģʽ������ͼ.jpg
    ע�⣺ ��ͼ������һ�� IPv4 ESP ���ݰ���
    ���� IPv4 AH ���ݰ������� ah_input���� ���������� esp_input�� �� ����;
    ͬ�������� IPv4 IPCOMP ���ݰ��������� ipcomp_input���� ����
    ������ esp_input�� �� ����
    ͼ��xfrm_state_lookup���� ������ SAD ��ִ�в��ҡ�
    �������ʧ�ܣ���ᶪ�����ݰ���
    ������ֲ������У��������Ӧ IPsec Э�������ص�����
    ͼ��file://imgs/���� IPsec ���ݰ�������ģʽ������ͼ.jpg
    ��ͼ�е�xfrm_lookup()��ʽ��һ�ַǳ����ӵķ���
    ͼ��file://imgs/xfrm_lookup����ͼ.jpg
    
�� IPsec �� NAT ����
    Ϊ�˽��NATת�����⣬������ IPsec �� NAT ������׼
    �����ߣ��� RFC 3948 ����ʽ��Ϊ��IPsec ESP ���ݰ��� UDP ��װ������
    UDP ��װ����Ӧ���� IPv4 ���ݰ��Լ� IPv6 ���ݰ���
    NAT ������������������� IPsec ����;
    �ͻ��˵��ͻ�������Ӧ�ó���ͨ����Ҫ��Щ������
    �ر��Ƕ��ڶԵȺ� Internet Э������ ��VoIP�� Ӧ�ó���
    ��Ӧ���������ᵽ��strongSwanʵ����IKEv2�н���չ����
    ��http://tools.ietf.org/html/draft-brunner-ikev2-mediation-00����
    ������λ��NAT·�������������VPN�˵�(ʹ����һ�ֻ���)����ֱ�ӵĶԵ�IPSec�����
    NAT ������ι�����
        ���ȣ����ס��NAT-T �ǽ����� ESP �������������� AH �����ý��������
        ��һ��������NAT-T�������ֶ�����һ��ʹ�ã���ֻ����IKEv1��IKEv2һ��ʹ�á�
        ������Ϊ NAT-T �뽻�� IKEv1/IKEv2 ��Ϣ�йء�
        ���ȣ�����������û��ռ��ػ����� ��pluto�� ��Ҫʹ�� NAT �������ܣ�
        ��ΪĬ������²��ἤ��ù��ܡ�
        �������� Openswan ��ͨ���� /etc/ipsec.conf �е����Ӳ�������� 
        nat_traversal=yes ��ִ�д˲�����
        ��λ�� NAT ����Ŀͻ��˲�����Ӵ���Ŀ��Ӱ�졣
        �� strongSwan �У�IKEv2 charon �ػ�����ʼ��֧�� NAT ���������Ҵ˹����޷�ͣ�á�
        �� IKE����ģʽ���ĵ�һ�׶Σ���������Եȷ��Ƿ�֧�� NAT-T��
        �� IKEv1 �У����Ե���֧�� NAT-T ʱ��
        ����һ�� ISAKAMP ��ͷ��Ա����Ӧ�� ID�����֪���Ƿ�֧�� NAT-T��
        ��IKEv2�У�NAT-T�Ǳ�׼��һ���֣�����������
        ��������������������ͨ������ NAT-D ������Ϣ
        ��������� IPsec �Ե���֮���·�����Ƿ����һ������ NAT �豸
        ���ͬʱ�����������NAT-T ��ͨ���� IP ��ͷ�� ESP ��ͷ֮����� UDP ��ͷ
        ������ԭʼ IPsec ��������ݰ���
        UDP ��ͷ�е�Դ�˿ں�Ŀ��˿ھ�Ϊ 4500��
        ���⣬NAT-T ÿ 20 �뷢��һ�α��ֻ״̬����Ϣ���Ա� NAT ������ӳ�䡣
        ���ֻ״̬����ϢҲ�� UDP �˿� 4500 �Ϸ��ͣ�
        ��ͨ�������ݺ�ֵ����һ���ֽڣ�0xFF������ʶ��
        �������ݰ����� IPsec �Ե���ʱ����ͨ�� NAT ��
        �ں˻���� UDP ��ͷ������ ESP ��Ч���ء�
        
        