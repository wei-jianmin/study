https://blog.csdn.net/qq_38265137/article/details/89423809

ipsecʹ�� AH �� ESP �Ա��Ľ��з�װ
    AHֻ��������֤��û�м��ܵĹ��ܣ���ESPͬʱ���м��ܺ���֤�Ĺ��ܣ�
    AH��ESP���Ե���ʹ��Ҳ�������ʹ��
    
�д���ģʽ�����ģʽ���֣�
    ���ģʽ
        �����ģʽ�£�AHͷ��ESPͷ��ӵ�ԭʼIPͷ֮ǰ��Ȼ��������һ���µı���ͷ�ŵ�AHͷ��ESPͷ֮ǰ
        ͼ��file://imgs/ipsec vpn���ģʽ��װ����.png
    ����ģʽ
        �ڴ���ģʽ�У�AHͷ��ESPͷ���뵽IPͷ�봫���Э��ͷ֮�䣺
        ͼ��file://imgs/ipsec vpn����ģʽ��װ����.png
        ����ģʽ���ı䱨��ͷ�������Դ��Ŀ�ĵ�ַ��������ͨ��˫����Դ��Ŀ�ĵ�ַ��
        ͨ��˫��ֻ�ܱ����Լ���������Ϣ�����ܱ���һ���������Ϣ��
        ���Ը�ģʽֻ��������̨����֮��ͨ��
        
�ھ���nat�豸ʱ����Ҫ�����ڲ���ip_portת��Ϊ�����ip_port
����AHЭ�飬���������ĵ�ȫ��������ipͷ���������� AH ��װ�ı��Ĳ�֧��nat��Խ
����ESPЭ�飬�������е�����Ҳ�޷�����nat��Խ���޷�����natת������
    ESP��װ�ı��ģ���ʼ��ipͷ������ת��Ϊ�����ip
    ��ipͷ������Ĳ���tcpͷ������espͷ��
    espͷ�������ģ�file://imgs/espͷ.png
    �ɼ�espͷ�ǲ����˿ںŵģ�
    ����ģʽ�£�espͷ���������tcpͷ�����ģʽ����ip-tcpͷ��
    �����Ͽ����滻��tcpͷ�Ķ˿ںţ����Ǹ�tcpͷ�Ǽ��ܵģ�
    ���������޷��滻��tcpͷ�еĶ˿ں�
    
nat��Խ�Ľ���취��nat-t��    
    ��ESP����ģʽ����nat��Խʱ���������⣬�����޷�����portת��
    �Դˣ���ESPЭ�����һ�����޸ģ�
    ��esp���з�װʱ�������������ipʱ����ipͷ��������˿ں�
    ���������൱�ڽ�esp��װΪudp�����ˣ�������ԭ����ip�����ˣ�
    ������nat�豸���ܶԸñ��ĵ�ip���˿ڽ�������ת����
    ͬʱ�¸�esp��Ϊ����֤ipͷ�Ͷ˿ڣ�������֤��һ��Ҳû����
    ������������nat��Խ��
    ���Է������ַ�ʽ�����ʺ���esp����ģʽ����ͬ���ʺ���esp���ģʽ
    ���ּ������� NAT-T ������ͼ��file://imgs/esp nat��Խ.png
    
�ؼ�NAT-T��3�����⣺
    IPSEC�������֪���Լ��Ƿ���Ҫ֧��NAT-T��
        ����˫���Ƿ�֧��NAT-T������һ�����ж�peers֮���Ƿ���NAT���ڣ�
        ����������IKEv1�ĵ�һ�׶���ɣ�
        NAT-T����̽��ʹ��IKEv1��һ�׶�1-2����������ʵ�֣�
        ˫�����ཻ��NAT-T��Vendor ID����ʾ�����Ƿ�֧��NAT-T��
    IPSEC��������ж�����NAT���豸��
        Ϊ�˾���Peers֮���Ƿ���NAT���ڣ�Peer�ᷢ��һ��hash����
        ��ԴĿIP�Ͷ˿ڵĹ�ϣ�������˫�������hash�ͽ��ܵ�hashֵƥ�䣬
        ��ôPeers֮���û��NAT���ڣ��Ͳ���ESP��װ����
        ���hashֵ��ͬ����ôPeers����Ҫʹ��NAT-T������װ��ԽNAT��
        hash����Ҳ����NAT-D���أ�
        ����ģʽ�е�3-4�������ͣ���Ұ��ģʽ��2-3�����з��͡�
        IKEV1ͨ��3-4������NAT-D�������ж�
        ͨ��ԴIPԴ�˿�, Ŀ��IP Ŀ�Ķ˿���HASHֵ
        ���HASHֵ��ͬ��˵��û�о���NAT�����HASHֵ���ȣ�˵��������NAT
    ʲôʱ�����UDP�Ķ˿ڣ�
        ���ȷ���˾���nat������IKEV1��ͨ��5 6��ʱ������ UDP 4500�˿� 
        
��IKEv1/IKEv2��NAT��ԽЭ�̹��̣���μ�ԭ������

--------------------------------------------------------------------------------------
https://blog.csdn.net/ddv_9527/article/details/5679469
    NAT-T��Ƽ򵥣�����Ҫ�Ķ����е��豸����Э�飬ֻ��Ҫ�߽��豸֧�ּ��ɡ�
    ��������Ļ���˼·����IPSec��װ�õ����ݰ����ٽ���һ��UDP�����ݷ�װ��
    �������������ݰ�����NAT����ʱ�����޸ĵ�ֻ��������IP/UDP���ݣ�
    �������ڲ�������IPSec ����û�н��иĶ���
    ��Ŀ���������ٰ�����IP/UDP��װȥ�����Ϳ��Ի��������IPSec���ݰ���
    NAT-T��ʵ������ʱ����һ����̽��ͨ��˫���Ƿ�֧��NAT-T��
    ����Ҫͨ��IKEЭ��ʱ�˴˷��͵ĵ�һ�����ݰ����жϡ�
    ���ж�˫����֧��NAT-T�󣬽��뵽�ڶ���NAT�豸�ķ��֣�
    ��ȥ�������Ϸ�����·�м��Ƿ����NAT�豸��
    ͨ���ж�ͨ��˫����IP��ַ���߶˿��Ƿ����˸ı����֪��
    �������Ϸ�����·�д���NAT�豸��
    ͨ��˫��NAT-T��ʼЭ�������õ����ݰ���װ��ʽ���������Э�̹��̡�

--------------------------------------------------------------------------------------
ip xfrm ����nat��Խ
    ��nat��Խʱ������
        ����A��
        ip xfrm state add src 192.168.4.127 dst 192.168.3.171 proto esp spi 0x00000301 mode tunnel auth md5 0x96358c90783bbfa3d7b196ceabe0536b enc des3_ede 0xf6ddb555acfd9d77b03ea3843f2653255afe8eb5573965df
        ip xfrm state add src 192.168.3.171 dst 192.168.4.127 proto esp spi 0x00000302 mode tunnel auth md5 0x99358c90783bbfa3d7b196ceabe0536b enc des3_ede 0xffddb555acfd9d77b03ea3843f2653255afe8eb5573965df
        ip xfrm policy add src 192.168.4.127 dst 192.168.3.171 dir out ptype main tmpl src 192.168.4.127 dst 192.168.3.171 proto esp mode tunnel
        ip xfrm policy add src 192.168.3.171 dst 192.168.4.127 dir in ptype main tmpl src 192.168.3.171 dst 192.168.4.127 proto esp mode tunnel
        ����B��
        ip xfrm state add src 192.168.4.127 dst 192.168.3.171 proto esp spi 0x00000301 mode tunnel auth md5 0x96358c90783bbfa3d7b196ceabe0536b enc des3_ede 0xf6ddb555acfd9d77b03ea3843f2653255afe8eb5573965df
        ip xfrm state add src 192.168.3.171 dst 192.168.4.127 proto esp spi 0x00000302 mode tunnel auth md5 0x99358c90783bbfa3d7b196ceabe0536b enc des3_ede 0xffddb555acfd9d77b03ea3843f2653255afe8eb5573965df
        ip xfrm policy add src 192.168.4.127 dst 192.168.3.171 dir in ptype main tmpl src 192.168.4.127 dst 192.168.3.171 proto esp mode tunnel
        ip xfrm policy add src 192.168.3.171 dst 192.168.4.127 dir out ptype main tmpl src 192.168.3.171 dst 192.168.4.127 proto esp mode tunnel
    ��nat��Խʱ������
        ��ɾ��֮ǰ���õ�ipsec sa��
            ip xfrm state deleteall
            ip xfrm policy����nat��Խʱ������һ��
        ����A��
        ip xfrm state add src 192.168.4.127 dst 192.168.3.171 proto esp spi 0x00000301 mode tunnel auth sha1 0x96358c90783bbfa3d7b196ceabe0536b enc aes 0xf6ddb555acfd9d77b03ea3843f2653255afe8eb5573965df encap espinudp 4500 4500 0.0.0.0
        ip xfrm state add src 192.168.3.171 dst 192.168.4.127 proto esp spi 0x00000302 mode tunnel auth sha1 0x99358c90783bbfa3d7b196ceabe0536b enc aes 0xffddb555acfd9d77b03ea3843f2653255afe8eb5573965df encap espinudp 4500 4500 0.0.0.0
        ip xfrm policy add src 192.168.4.127 dst 192.168.3.171 dir out ptype main tmpl src 192.168.4.127 dst 192.168.3.171 proto esp mode tunnel
        ip xfrm policy add src 192.168.3.171 dst 192.168.4.127 dir in ptype main tmpl src 192.168.3.171 dst 192.168.4.127 proto esp mode tunnel
        ����B��
        ip xfrm state add src 192.168.4.127 dst 192.168.3.171 proto esp spi 0x00000301 mode tunnel auth sha1 0x96358c90783bbfa3d7b196ceabe0536b enc aes 0xf6ddb555acfd9d77b03ea3843f2653255afe8eb5573965df encap espinudp 4500 4500 0.0.0.0
        ip xfrm state add src 192.168.3.171 dst 192.168.4.127 proto esp spi 0x00000302 mode tunnel auth sha1 0x99358c90783bbfa3d7b196ceabe0536b enc aes 0xffddb555acfd9d77b03ea3843f2653255afe8eb5573965df encap espinudp 4500 4500 0.0.0.0
        ip xfrm policy add src 192.168.4.127 dst 192.168.3.171 dir in ptype main tmpl src 192.168.4.127 dst 192.168.3.171 proto esp mode tunnel
        ip xfrm policy add src 192.168.3.171 dst 192.168.4.127 dir out ptype main tmpl src 192.168.3.171 dst 192.168.4.127 proto esp mode tunnel
