���ܣ� ip����������ʾ�����Linux������·�ɡ������豸������·�ɺ����
�﷨�� ip [OPTIONS] OBJECT COMMAND
    OBJECT := { link | address | addrlabel | route | rule | neigh | ntable |
                tunnel | tuntap | maddress | mroute | mrule | monitor | xfrm |
                netns | l2tp | tcp_metrics | token }
    OPTIONS := { -V[ersion] | -h[uman-readable] | -s[tatistics] | -d[etails] |
                 -r[esolve] | -iec | -f[amily] {inet|inet6|ipx|dnet|link} |
                 -4 | -6 | -I | -D | -B | -0 | -rc[vbuf] [size] | -o[neline] |
                 -l[oops] { maximum-addr-flush-attempts } | -t[imestamp] | 
                 -ts[hort] | -n[etns] name | -a[ll] }
�������
    OPTIONS ��һЩ�޸�ip��Ϊ���߸ı��������ѡ�
    ���е�ѡ�����-�ַ���ͷ����Ϊ������������ʽ:
        -V�� -Version��ӡip�İ汾���˳�
        -h�� ����ɶ����
        -s�� -stats �Cstatistics������������Ϣ��������ѡ��������λ����ϣ��������Ϣ����Ϊ�꾡
        -d�� ��������ϸ����Ϣ
        -l�� ָ��"IP��ַˢ��"�߼������Ե����ѭ������Ĭ��Ϊ10
        -f�� -family ��ָ��Ҫʹ�õ�Э���壬Э�������һ��inet��inet6��bridge, ipx, dnet or link
        -4�� �� -family inet�ļ�д
        -6�� �� -family inet6�ļ�д
        -0�� �� -family link �ļ�д
        -I�� ��-family ipx�ļ�д
        -o�� -oneline �����������"\"�ַ��滻���з�
        -n�� -netns��������IP��ָ��������ռ�netns
        -r�� -resolve ʹ��ϵͳ���ƽ�������ӡDNS���ƶ�����������ַ
        -t�� ʹ�ü�����ѡ��ʱ��ʾ��ǰʱ��
        -a�� -all�����ж���ִ��ָ���������ȡ���������Ƿ�֧�����ѡ��
        -rc��-rcvbuf (size) ����Netlink�׽��ֽ��ջ������Ĵ�С���ã�Ĭ��Ϊ1MB
    OBJECT ����Ҫ������߻�ȡ��Ϣ�Ķ���
        link �����豸
        address һ���豸��Э�飨IP����IPV6����ַ
        neighbour ARP����NDISC��������Ŀ
        route ·�ɱ���Ŀ
        rule ·�ɲ������ݿ��еĹ���
        maddress �ಥ��ַ
        mroute �ಥ·�ɻ�������Ŀ
        monitor ���������Ϣ
        mrule �鲥·�ɲ������ݿ��еĹ���
        tunnel IP�ϵ�ͨ��
        l2tp �����̫��(L2TPV3)
        netns  - manage network namespaces
        ntable - manage the neighbor cache's operation
        tcp_metrics/tcpmetrics - manage TCP Metrics
        token  - manage tokenized interface identifiers
        tunnel - tunnel over IP.
        tuntap - manage TUN/TAP devices
        xfrm   - manage IPSec policies
        ע�⣺���еĶ����������Լ�д�����磺address���Լ�дΪaddr��������a
ͨ��man��ȡ����
    man ip ֻ�Ǽ�Ҫ�г�����֧�ֵĲ�������Ҫ����øò���������֧�ֵľ�������
    ��ʹ��man���������´�����
    ip-address, ip-addrlabel, ip-l2tp, ip-link, ip-maddress, ip-monitor, 
    ip-mroute, ip-neighbour, ip-netns, ip-ntable, ip-route, ip-rule, 
    ip-tcp_metrics, ip-token, ip-tunnel, ip-xfrm
    Ҳ����ʹ�� ip OBJECT help,��ȡָ������ļ�Ҫ����
������
    ����IP��ַ
        ��ʽ�� ip addr add ADDRESS/MASK dev DEVICE
        root@centos7 ~]# ip addr add 192.1.1.1/24 dev ens33
    ɾ��IP��ַ
        [root@centos7 ~]# ip addr del 192.1.1.1/24 dev ens34
    �鿴������Ϣ
        [root@centos7 ~]# ip address show
    ���·�ɱ�
        ��ʽ��ip rouite add TARGET via GW
        TARGETΪĿ�������������GWΪ���ػ���һ����
        [root@centos7 ~]# ip route add 172.16.0.0/16 via 192.168.29.1
    ɾ��·�ɱ�
        [root@centos7 ~]# ip route del 172.16.0.0/16
    ��ʾ·�ɱ�
        ��ʽ��ip route show|list
        [root@centos7 ~]# ip route list
    ���·�ɱ�
        ��ʽ��ip route flush [dev IFACE] [via PREFIX]
        [root@centos7 ~]# ip route flush dev ens33
    �������
        ��ʽ��ip route add default via GW dev IFACE
        [root@centos7 ~]# ip route add default via 192.168.29.1
    ��ʾ�����豸������״̬
        [root@centos7 ~]# ip link list
    ��ʾ�ھӱ�
        [root@centos7 ~]# ip neigh 
    �鿴������Ϣ
        [root@centos7 ~]# ip -s link list 
    ����MTU
        [root@centos7 ~]# ip link set ens33 mtu 1400
    �ر������豸
        [root@centos7 ~]# ip link set ens38 down
        [root@centos7 ~]# ip link show ens38
    ���������豸
        [root@centos7 ~]# ip link set ens38 up
        [root@centos7 ~]# ip link show ens38