iptables��Ĭ���Ǻ��������ƣ���û�м��غ�������ģ����ǿ��Է��е�

iptables [-t Table] COMMAND [Chain] [RuleNum] CRETIRIA -j ACTION
       ���壺
       ip6tables [-t table] {-A|-C|-D} chain rule-specification
       iptables [-t table] {-A|-C|-D} chain rule-specification
       iptables [-t table] -I chain [rulenum] rule-specification
       iptables [-t table] -R chain rulenum rule-specification
       iptables [-t table] -D chain rulenum
       iptables [-t table] -S [chain [rulenum]]
       iptables [-t table] {-F|-L|-Z} [chain [rulenum]] [options...]
       iptables [-t table] -N chain
       iptables [-t table] -X [chain]
       iptables [-t table] -P chain target
       iptables [-t table] -E old-chain-name new-chain-name
       rule-specification = [matches...] [target]
       match = -m matchname [per-match-options]
       target = -j targetname [per-target-options]

���ɣ�       
    iptables 'in' Table Add/Del/.. 'at' Chain [RuleNum] 'on' CRETIRIA 'do' -j ACTION
    �� ['��'] '��ɾ�Ĳ�' [����ض�'��'] [�е�'�ڼ���'] '����ƥ��' �Ľ�� '���С���������'

ע��[Chain] [RuleNum] �����ﲢ���Ǳ�ʾ��ѡ��
    ����ָ��ĳЩ COMMNAD ��ѡ������һЩ COMMAND ��ѡ���ѡ
    
-t��        ָ����Ҫά���ķ���ǽ����� filter��nat��mangle��raw��
            �ڲ�ʹ�� -t ʱ��Ĭ��ʹ�� filter ��

-m/--match: ָ��ʹ��ƥ������

COMMAND��   ���������Թ���Ĺ���
            -A	    ׷�ӷ���ǽ����
            -C      ������ǽ����
            -D	    ɾ������ǽ����
            -F	    ��շ���ǽ����
            -I	    �������ǽ����
            -L	    �г�����ǽ����
            -R	    �滻����ǽ����
            -S      ��ӡ����ǽ����
            -Z	    ��շ���ǽ���ݱ�ͳ����Ϣ
            -P	    ������Ĭ�Ϲ���
            -n      ��ʾ���� IP ��ַ���з��飬
                    �������������ʾ�ٶȽ���ӿ졣
            -v      ��ʾ�����ϸ��Ϣ������ͨ���ù�������ݰ�������
                    ���ֽ����Լ���Ӧ������ӿڡ�
                    
Chain��     ָ���ڵ㣨�������������������������Щ������Щ������������Щ������� 
            PREROUTING      ƥ�䩦      ��nat��mangle��raw����
            INPUT           ƥ�䩦filter��   ��mangle��   ����
            FORWARD         ƥ�䩦filter��   ��mangle��   ����
            OUTPUT          ƥ�䩦filter��nat��mangle��raw����
            POSTROUTING     ƥ�䩦      ��nat��mangle��raw����
                                ���������������ة������ة������������ة�������
                                
CRETIRIA��  ƥ�����
            [!]-p	        ƥ��Э�飬! ��ʾȡ��
            [!]-s	        ƥ��Դ��ַ
            [!]-d	        ƥ��Ŀ���ַ
            [!]-i	        ƥ����վ�����ӿ�
            [!]-o	        ƥ���վ�����ӿ�
            [!]--sport	    ƥ��Դ�˿�
            [!]--dport	    ƥ��Ŀ��˿�
            [!]--src-range	ƥ��Դ��ַ��Χ
            [!]--dst-range	ƥ��Ŀ���ַ��Χ
            [!]--limit	    �������ݱ�����
            [!]--mac-source	ƥ��ԴMAC��ַ
            [!]--sports	    ƥ��Դ�˿�
            [!]--dports	    ƥ��Ŀ��˿�
            [!]--stste	    ƥ��״̬��INVALID��ESTABLISHED��NEW��RELATED)
            [!]--string	    ƥ��Ӧ�ò��ִ�
            [!]--icmp-type  ƥ��ICMP����
    ע�� �������Щ������������ʱ���� -m ����ʹ�� ������ man ������û������
            https://blog.csdn.net/weixin_48190891/article/details/107815698
            ��˿�ƥ��:  -m multiport --sports Դ�˿��б�
            IP��Χƥ��:  -m iprange --src-range IP��Χ
            MAC��ַƥ��: -m mac --mac-source MAC��ַ
            ״̬ƥ��:    -m state --state ����״̬
            
ACTION��    ��������
            ACCEPT	    �������ݰ�ͨ��
            DROP	    �������ݰ�
            REJECT	    �ܾ����ݰ�ͨ��
            LOG	        �����ݰ���Ϣ��¼ syslog Ի־
            DNAT	    Ŀ���ַת��������PREROUTING��
            SNAT	    Դ��ַת��������POSTROUTING��
            MASQUERADE	��ַ��ƭ��Դ��ַ�Զ�ת��������POSTROUTING��
            REDIRECT	�ض���(ͨ���ı�Ŀ��IP�Ͷ˿�,ʵ�ֶ˿�ӳ��)

iptables-save �� iptables-restore
    iptables�������ļ� /etc/sysconfig/iptables
    iptables-save [-c] [-t table]
        ����-c�������Ǳ�������ֽڼ�������ֵ��
        �����ʹ��������������ǽ�󲻶�ʧ�԰����ֽڵ�ͳ�ơ�
        ��-c������iptables-save����ʹ��������ǽ�����ж�ͳ�Ƽ��������Ϊ���ܡ�
        �������Ĭ���ǲ�ʹ�õġ�
        ����-tָ��Ҫ����ı�Ĭ���Ǳ������еı�
    iptables-save > /etc/sysconfig/iptables
    iptables-save�ǽ�����׷�ӵ�һ���ļ�����Ҫ�����iptables-restore����
    iptables-restore����װ����iptables-save����Ĺ��򼯡�
    ���ҵ��ǣ���ֻ�ܴӱ�׼����������룬�����ܴ��ļ�����
    iptables-restore [-c] [-n]
    ����-cҪ��װ������ֽڼ�������
    �������iptables-save�����˼�����������������װ�룬�ͱ��������������
    ������һ�ֽϳ�����ʽ��--counters��
    ����-n����iptables-restore��Ҫ�������еı����ڵĹ���
    Ĭ���������������Ѵ�Ĺ���
    ��������ĳ���ʽ��--noflush��
    
++++++++++++++++++++++++++++++  ����  ++++++++++++++++++++++++++++++++++++

ʹ�� iptables ����ת��
    #�ر�selinux
    setenforce 0
    #����ת��
    /etc/sysctl.conf �е� net.ipv4.ip_forward=1
    sysctl -p
    #�ھ��� FORWARD �ڵ�ʱ����Ҫ�� filter ��֮���˵�
    iptables -P FORWARD ACCEPT
    #�ѽ������ӵģ�����ת��
    iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
    iptables -t nat -A POSTROUTING -j MASQUERADE
    #���� 11.53.96.13:7777 �ķ��ʣ�ת���� 11.0.34.204:8888
    iptables -t nat -A PREROUTING -d 11.53.96.13 -p tcp --dport 7777 
             -j DNAT --to-destination 11.0.34.204:8888
    iptables -t nat -A PREROUTING -d 192.168.2.72 -p udp --dport 10022 
             -j DNAT --to-destination 192.168.70.2:22
 
iptablesʵ�ֶ˿�ӳ�䣨���غ�Զ�̶˿�ӳ�䣩
    #����<ʹ�� iptables ����ת��>���ᵽ��������˵һ��
    1. ��Ҫ�ȿ���linux������ת������
       vim /etc/sysctl.conf����net.ipv4.ip_forward=0����Ϊnet.ipv4.ip_forward=1
       sysctl -p  //ʹ����ת��������Ч
    2. ����iptables��ʹ֮ʵ��natӳ�书��
       ����������60.208.23.14��1234�˿�ת����192.168.3.44:8000�˿ڡ�
       iptables -t nat -A PREROUTING -d 60.208.23.14 -p tcp --dport 1234 
                -j DNAT --to-destination 192.168.3.44:8000
       ��192.168.3.44 8000�˿ڽ����ݷ��ظ��ͻ���ʱ����Դip��Ϊ60.208.23.14
       iptables -t nat -A POSTROUTING -d 192.168.3.44 -p tcp --dport 8000 
                -j SNAT --to 60.208.23.14
            
++++++++++++++++++++++++++++++++  �������  +++++++++++++++++++++++++++++++++

������� SNAT �� DNAT
    https://www.frozentux.net/iptables-tutorial/cn/iptables-tutorial-cn-1.1.19.html#MARKTARGET
        6.5.12. SNAT target
            ���target��������Դ�����ַת���ģ�������д����ԴIP��ַ
            �������м������ӹ���һ��Internet ����ʱ�������õ�����
            �����ں����ipת�����ܣ�Ȼ����дһ��SNAT����
            �Ϳ��԰����дӱ��������ȥ�İ���Դ��ַ��ΪInternet���ӵĵ�ַ��
            ������ǲ�����������ֱ��ת���������İ��Ļ���
            Internet�ϵĻ��ӾͲ�֪�����Ķ�����Ӧ���ˣ�
            ��Ϊ�ڱ�����������һ��ʹ�õ���IANA��֯ר��ָ����һ�ε�ַ��
            �����ǲ�����Internet��ʹ�õġ�
            SNAT target�����þ��������дӱ����������İ����������Ǵ�һ̨���ӷ����ģ�
            ��̨����һ����Ƿ���ǽ��
            SNATֻ������nat���POSTROUTING���
            ֻҪ���ӵĵ�һ�����������İ���SNAT�ˣ�
            ��ô������ӵ��������еİ������Զ��ر�SNAT,
            ����������򻹻�Ӧ������ ���������������������ݰ���
    https://blog.csdn.net/oyyy3/article/details/121099277
        һ.SNAT
            1.ԭ��
                ԭ��Դ��ַת�����޸����ݰ��е�ԴIP��ַ #�²⻹�޸���Դ�˿ڵ�ַ
                ���ã�����ʵ�־�������������
                ���õı�����nat���е�POSTROUTING
            2.ת��ǰ������
                ����������������ȷ����IP��ַ���������롢Ĭ�����ص�ַ
                Linux���ؿ���IP·��ת��
                linxu��ϵͳ������û��ת������ ֻ��·�ɷ������� 
                ��ʱ��:
                echo 1 > /proc/sys/net/ipv4/ip_forward
                sysctl -W net.ipv4.ip_forward=1
                ���ô�:
                vim /etc/sysct1.conf
                net.ipv4.ip_forward = 1    #������д�������ļ�   
                sysctl -p                  #��ȡ�޸ĺ�����ã�ʹ֮������Ч
    https://zhuanlan.zhihu.com/p/632713274
        SNAT��ָ�����ݰ����������ͳ�ȥ��ʱ�򣬰����ݰ��е�Դ��ַ�����滻Ϊָ����IP��
        ���������շ�����Ϊ���ݰ�����Դ�Ǳ��滻���Ǹ�IP������
        MASQUERADE���÷������ݵ������ϵ�IP���滻ԴIP��
        ��ˣ�������ЩIP���̶��ĳ��ϣ����粦���������ͨ��dhcp����IP������£��͵���MASQUERADE
        DNAT������ָ���ݰ����������ͳ�ȥ��ʱ���޸����ݰ��е�Ŀ��IP������Ϊ����������A��
        ������Ϊ��������DNAT�������з���A�����ݰ���Ŀ��IPȫ���޸�ΪB����ô����ʵ���Ϸ��ʵ���B
        DNAT����PREROUTING���������еģ�
        ��SNAT�������ݰ����ͳ�ȥ��ʱ��Ž��У��������POSTROUTING���Ͻ��е�
        
REDIRECT �� DNAT ����
    https://www.cnblogs.com/zhangpeiyao/p/14448036.html
    DNAT���Խ������ݰ����͵���������������������Ͷ˿ڣ�
    ��REDIRECT����Խ��յ������ݰ�ת���������������˿ڣ�
    ������������DNAT�Ĳ���һ�㶼�ƶ���ר�ŵ�NAT�������ϣ�
    ��REDIRECT�Ĳ���һ���ƶ���Ŀ�������ϵ�ȻҲ������������DNAT
    https://blog.csdn.net/zhangge3663/article/details/101518356
    redirect����Ա����ģ����������İ�ת��localhost��ĳ���˿ڣ�
    �ʺ���redirect�����DNATЧ�ʸߵ㡣
    ���ⲿ��ַֻ����DNAT�ˡ�
    
https://www.linuxso.com/linuxxitongguanli/1070.html
IPtables��SNAT��MASQUERADE������
һ��SNAT��DNAT����
    IPtables�п������������������ַת����NAT���������ַת����Ҫ�����֣�SNAT��DNAT��
    
    SNAT��source network address translation����д����Դ��ַĿ��ת����
    ���磬���PC��ʹ��ADSL·��������������ÿ��PC��������������IP��
    PC�������ⲿ�����ʱ��·���������ݰ��ı�ͷ�е�Դ��ַ�滻��·������ip��
    ���ⲿ����ķ�����������վweb�������ӵ����������ʱ��
    ������־��¼��������·������ip��ַ��������pc��������ip��
    ������Ϊ������������յ������ݰ��ı�ͷ��ߵġ�Դ��ַ����
    �Ѿ����滻�ˣ����Խ���SNAT������Դ��ַ�ĵ�ַת����
    ע��ADSL
        ��ͳ�ĵ绰��ϵͳʹ�õ���ͭ�ߵĵ�Ƶ���֣�4kHz����Ƶ�Σ���
        ��ADSL����DMT����ɢ����Ƶ��������
        ��ԭ���绰��·4kHz��1.1MHzƵ�λ��ֳ�256��Ƶ��Ϊ4.3125khz����Ƶ����
        ���У�4khz����Ƶ�������ڴ���POTS����ͳ�绰ҵ�񣩣�
        20KhZ��138KhZ��Ƶ���������������źţ�
        138KhZ��1.1MHZ��Ƶ���������������źš�
        DMT�������Ը�����·�����������ÿ���ŵ��������Ƶı��������Ա��ֵ�������·��
        һ����˵�����ŵ��������Խ���ڸ��ŵ��ϵ��Ƶı�����Խ�࣬
        ���ĳ�����ŵ�����Ⱥܲ����֮���á�
        ADSL�ɴﵽ����640kbps������8Mbps�����ݴ����ʡ�

    DNAT��destination network address translation����д����Ŀ�������ַת����
    ���͵�Ӧ���ǣ��и�web����������������������ip��ǰ���и�����ǽ���ù���ip��
    �������ϵķ�����ʹ�ù���ip�����������վ�������ʵ�ʱ�򣬿ͻ��˷���һ�����ݰ���
    ������ݰ��ı�ͷ��ߣ�Ŀ���ַд���Ƿ���ǽ�Ĺ���ip��
    ����ǽ���������ݰ��ı�ͷ��дһ�Σ���Ŀ���ַ��д��web������������ip��
    Ȼ���ٰ�������ݰ����͵�������web�������ϣ����������ݰ��ʹ�͸�˷���ǽ��
    ���ӹ���ip�����һ����������ַ�ķ����ˣ���DNAT������Ŀ��������ַת����
    
����MASQUERADE����
    MASQUERADE����ַαװ����iptables�����ź�SNAT�����Ч������Ҳ��һЩ����
    ��ʹ��SNAT��ʱ�򣬳���ip�ĵ�ַ��Χ������һ����Ҳ�����Ƕ�������磺
    ���������ʾ������10.8.0.0���ε����ݰ�SNAT��192.168.5.3��ipȻ�󷢳�ȥ��
    iptables -t nat -A POSTROUTING -s 10.8.0.0/255.255.255.0 -o eth0 
             -j SNAT --to-source 192.168.5.3
    ���������ʾ������10.8.0.0���ε����ݰ�SNAT��192.168.5.3/.4/.5�ȼ���ipȻ�󷢳�ȥ
    iptables -t nat -A POSTROUTING -s 10.8.0.0/255.255.255.0 -o eth0 
             -j SNAT --to-source 192.168.5.3-192.168.5.5
    �����SNAT��ʹ�÷�����������NAT��һ����ַ��Ҳ����NAT�ɶ����ַ��
    
    ���ǣ�����SNAT�������Ǽ�����ַ��������ȷ��ָ��ҪSNAT��ip��
    ���統ǰϵͳ�õ���ADSL��̬���ŷ�ʽ����ôÿ�β��ţ�����ip192.168.5.3����ı䣬
    ���Ҹı�ķ��Ⱥܴ󣬲�һ����192.168.5.3��192.168.5.5��Χ�ڵĵ�ַ��
    ���ʱ������������ڵķ�ʽ������iptables�ͻ���������ˣ�
    ��Ϊÿ�β��ź󣬷�������ַ����仯����iptables�����ڵ�ip�ǲ��������Զ��仯�ģ�
    ÿ�ε�ַ�仯�󶼱����ֹ��޸�һ��iptables��
    �ѹ�����ߵĹ̶�ip�ĳ��µ�ip�������Ƿǳ������õġ�

    MASQUERADE����������ֳ�������Ƶģ����������ǣ�
    �ӷ������������ϣ��Զ���ȡ��ǰip��ַ����NAT��
    �����±ߵ����
    iptables -t nat -A POSTROUTING -s 10.8.0.11/255.255.255.255 -o eth0 -j MASQUERADE
    ������õĻ�������ָ��SNAT��Ŀ��ip�ˣ���������eth0�ĳ��ڻ���������Ķ�̬ip��
    MASQUERADE���Զ���ȡeth0���ڵ�ip��ַȻ����SNAT��ȥ��
    ������ʵ���˺ܺõĶ�̬SNAT��ַת����
    
    iptables [-t filter] 