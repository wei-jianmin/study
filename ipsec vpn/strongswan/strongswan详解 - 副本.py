����ĵ����ϣ�
file://../ipsec�ٶȰٿ�.txt
file://../ip-xfrm.man.txt
file://../IPSec֮IKEv2Э�����.py
file://../ipsecЭ��.py
file://../ipsec�ٶȰٿ�.txt
file://../IPsec��ص�һЩ��������.txt
file://../ipsec���.txt
file://../Linux Netlink����.py
file://../PF_KEYЭ��.txt
file://../pppЭ��.txt
file://../xfrm.txt
file://../ͼ��Linux��������͹���.pdf
file://../·�ɱ�.txt
file://../����ǽ��������.py

https://blog.imkasen.com/strongswan-config.html
strongSwan���
    strongSwan����һ�������Ŀ�Դ IPsec VPN ���������
    ���������� Linux��Windows �� Mac OS X �ϣ�
    ���⣬�������ݻ��� Android �� iOS �Ĳ�Ʒ��֧�ֵ� IPsec ���ܡ�
    Ҫע����ǣ�strongSwan ������ VPN �ϵ����ݽ��м��ܣ�
    ���������� strongSwan �ĵײ����ϵͳ������ Linux�����м��ܡ�
    strongSwan ����ʹ��������Կ������internet key exchange, IKE��Э��
    ����ͬ��Э�����ڶԳƼ��ܵ���Կ��
    strongSwan ֧�� IKEv1 �� IKEv2��
    strongSwan ��һ���� pluto �ķ�����ʵ���� IKEv1��
    �� IKEv2 ����һ���� charon �ķ����ṩ��
Linux IPsec ֧��
    1998�꿪ʼ�� KAME ��Ŀ�ǵ�һ��Ŭ��ʵ�� IPv4 �� IPv6 ����� IPsec Э��ջ����Ŀ��
    ����Ŀ��ʵʩ��Ϊ�� BSD UNIX ϵͳ�����ܿ����Ϊ Linux �ں˵Ĳ�����
    ��Լ��ͬһʱ�䣬John Gilmore������ FreeS/WAN ��Ŀ��ּ�ڽ� IPsec ���� Linux��
    ��Ҳ��Ҫ�� Linux �ں˴򲹶���FreeS/WAN ��������Ϊ Kernel IP Security��KLIPS����
    �������������(KAME �� KLIPS)������Ҫ�򲹶�
    ���������û��ռ����е� IKE �������ں˿ռ�Ķ�Ӧ�������ͨ�ţ�
    �԰�װ������Կ�����ø��ּ��ܲ�����
    IETF �� RFC 2367 �ж����� PF_KEYv2����Ϊ��׼ API��
    �����û��ռ�����ڲ���ϵͳ�ں������� IPsec��
    KAME �� KLIPS ��ʹ���� PF_KEYv2��
    Ϊÿ���ں˰汾ά�� KAME �� KLIPS �Ĳ����Ǻ�����ս�Եģ�
    ��˾����� Linux 2.6 �ں�ϵ���а� KAME ��ΪĬ�ϵ� IPsec Э��ջ��
    2.6 �ں��µ� KAME ʵ�ֱ���Ϊ NETKEY��
    Ȼ����2.6 �ں˵��ص����޸���Э��ջ������һ����������һ������ NETLINK ��Э�顣
    �� PF_KEYv2 ��ͬ��NETLINK ��һ��ͨ�õ�Э�飬
    �������û��ռ�ʵ�����ں˵ĸ������ֽ�����Ϣ��
    ���磬RT_NETLINK ��һ�� NETLINK ��չ���������ö�̬·�ɽ������ں��а�װ��ɾ��·�ɡ�
    ͬ����XFRM_NETLINK 9 ���� IKE �������û����̹����ں���ά���� IPsec ��ȫ�������ݿ�
    ��Security Association Database, SAD���Ͱ�ȫ�������ݿ⣨Security Policy Database, SPD����
����·��
    strongSwan ʹ����һ�ֽ�������·�ɵ����繦�ܡ����� SPD �� IPsec ʹ�õİ�ȫ���Բ�ͬ��
    ������ IP ·���ǻ��� IP ͷ�е�Ŀ�� IP ��ַ�ֶΡ�
    ���� IP ת����������Ϊ����ǰ���ض�Ŀ�ĵص����ݰ�ѡ����ͬ��·����
    ��������������ǿ�ȡ�ġ�
    ����·�ɵ�һ�����ڰ�����֧�ֲ�ͬ�ͻ����Ĳ�ͬ QoS ����
    ���ƿͻ�Ϊ��ø��������͵��ӳٷ�������ѣ�����ͭ�ͻ���Ϊ�����˵ľ�������������
    Ϊ��Щ�ͻ�ѡ��·��ʱ���������⣬����Ҫ��Դ IP ��ַ��Ŀ�ĵ�ַ��Ϊ IP ·�ɹ��̵�һ���֡�
    Linux ����·�ɵ�ʵ����Ҫ���·�ɱ��һ��·�ɲ������ݿ⣨RPDB����
    �����ͨ���������������г� RPDB �еĲ��ԣ�ip rule show
    ���Ӧ����ʾ���������ݣ�
        0:     from all lookup local 
        220:   from all lookup 220 
        32766: from all lookup main 
        32767: from all lookup default
    Ҫ�ڱ����г����õ�·�ɣ����磬local����ʹ���������
    ip route list table local
    ���Ӧ���������ģ�
        broadcast 127.0.0.0 dev lo proto kernel scope link src 127.0.0.1
        local 127.0.0.0/8 dev lo proto kernel scope host src 127.0.0.1
        local 127.0.0.1 dev lo proto kernel scope host src 127.0.0.1
        broadcast 127.255.255.255 dev lo proto kernel scope link src 127.0.0.1
        broadcast 192.168.3.0 dev br0 proto kernel scope link src 192.168.3.229
        local 192.168.3.229 dev br0 proto kernel scope host src 192.168.3.229
        broadcast 192.168.3.255 dev br0 proto kernel scope link src 192.168.3.229
        broadcast 192.168.122.0 dev virbr0 proto kernel scope link src 192.168.122.1
        local 192.168.122.1 dev virbr0 proto kernel scope host src 192.168.122.1
        broadcast 192.168.122.255 dev virbr0 proto kernel scope link src 192.168.122.1
    ���õĹ����������ȼ���0����������ȼ���32767������ɨ�裬
    һ�� RPDB ����ƥ�䣬�ͻ�ʹ��ָ���ı���������һ��
    ���·�ɹ����޷��ӹ�����ָʾ��·�ɱ��������ݰ�����һ����
    ��������� RPDB �е���һ������
    from �ؼ��ֱ�ʾ��Դ IP ��ַ��ѡ�����
    ������Ҳʹ���� all �����Ա�ʾ�������ݰ�����ƥ��
    Ĭ������£�strongSwan �����һ�����ȼ�Ϊ 220 �Ĳ��Թ���
    �� Ubuntu Linux ����ʱ����������������local��id 255����main��254����default��253��
    ����·�ɱ�������غ͹㲥��ַ�ĸ����ȼ�����·�ɡ�
    ������ǹ��ں��ڲ�ʹ�õģ���Ӧ�ô��û��ռ��޸ġ�
    ��·�ɱ�����û��ָ����ʱʹ�õ���ͨ��
    Ĭ�ϱ�ͨ���ǿյģ���û��������ƥ��ʱʹ�á�
   
https://blog.csdn.net/wq897387/article/details/123446862
strongswan����Ŀ¼����
    https://docs.strongswan.org/docs/5.9/plugins/plugins.html
        �����ǹٷ��Ķ�ÿ������Ĺ���˵��
��Ŀ¼
    �ļ���	����
    conf	�����ļ�
    doc	    RFC��׼�ĵ�
    init	��ʼ����Ϣ
    src	    Դ�����ļ�
    scripts	�ű���Ϣ
    testing	���Գ���
srcĿ¼
    Component	    Description
    aikgen	        Utility to generate an Attestation Identity Key bound to a TPM 1.2
    charon	        IKE ��Կ�ػ�����
    charon-cmd	    ������ IKE �ͻ���
    charon-nm	    NetworkManager D-BUS ����ĺ��
    charon-svc	    Windows IKE ����
    charon-systemd	һ�� IKE �ػ����̣������� charon����ר��������� systemd
    charon-tkm	    �ɿ�����Կ������ (TKM) ֧�ֵ� charon ����
    checksum	    �����ѹ�����ִ���ļ��Ϳ��У��͵�ʵ�ó���
    conftest	    һ���Բ��Թ���
    frontends/android	������ Android �� VPN �ͻ���
    frontends/gnome	NetworkManager plugin
    frontends/osx	���ڱ��� macOS Ӧ�ó���� charon-xpc �����ػ�����
    ipsec	        �Դ�ͳ�� ipsec �����й��ߵİ�װ�������������
    libcharon	    ����charon�ػ����̵Ĵ󲿷ִ���Ͳ��
    libfast	        ʹ�� ClearSilver �� FastCGI �������� Web Ӧ�ó�������������
    libimcv	        ���������Բ����ռ��� (IMC), �����Բ�����֤�� (IMVs) �����ǹ���Ŀ����
    libipsec	    kernel-libipsec �� Android VPN �ͻ���Ӧ�ó���ʹ�õ��û��� IPsec ʵ��
    libpts	        �������� TPM ��ƽ̨���η��� (PTS) �� SWID ��ǩ����Ĵ���
    libpttls	    ʵ�� PT-TLS Э��
    libradius	    RADIUS Э��ʵ�֣������� eap-radius �� tnc-pdp �����ʹ�ã�
    libsimaka	    ������� EAP-SIM/AKA �������Ĵ���
    libstrongswan	�����ػ����̺�ʵ�ó���ʹ�õĻ������ܵ� strongSwan ��
    libtls	        eap-tls��eap-ttls��eap-peap ���������ʹ�õ� TLS ʵ��
    libtnccs	    ʵ�� IF-TNCCS �ӿ�
    libtncif	    ʵ�� IF-IMC/IF-IMV �ӿ�
    manager	        һ�������Ļ��� libfast �� charon ͼ�ι���Ӧ�ó���
    medsrv	        ���� libfast ���н������ʵ�����ǰ��
    pki	            ��Կ������ʩʵ�ó���
    pool	        ���ڹ��� attr-sql ����ṩ�����Ժ� IP ��ַ�ص�ʵ�ó���
    pt-tls-client	Integrity measurement�������Բ����� client using the PT-TLS protocol
    scepclient	    ʹ�� SCEP Э��ע��֤���ʵ�ó���
    sec-updater	    ʵ�ó�����ȡ�й� Linux �洢��İ�ȫ���ºͷ�����ֲ����Ϣ
    starter	        ��ȡ ipsec.conf �����Ƽ���ػ����� charon �Ĵ�ͳ�ػ�����
    stroke	        ͨ�� stroke Э����� charon �Ĵ�ͳ������ʵ�ó���
    swanctl	        ͨ�� vici �ӿڽ���ͨ�ŵ����úͿ���ʵ�ó���
    sw-collector	�� apt ��ʷ��־����ȡ�й��������װ�����»�ɾ���¼�����Ϣ��ʵ�ó���
    tpm_extendpcr	Tool that extends a digest into a TPM PCR
    _updown	        Default script called by the updown plugin on tunnel up/down events
    xfrmi	        ���� XFRM �ӿ�
src/libstrongswanĿ¼
    �ļ�	                                ����
    backtrace.c backtrace.h	                ����
    chunk.c chunk.h	                        ��
    debug.c debug.h	                        ����
    integrity_checker.c integrity_checker.h	�����Լ��
    lexparser.c lexparser.h	                ��
    printf_hook/	                        ��
    utils/ utils.c utils.h	                ��
    compat/	                                ������
    enum.c enum.h	                        ö��
    optionsfrom.c optionsfrom.h	            ����
    process.c process.h	                    ����
    capabilities.c capabilities.h	        ����
    cpu_feature.c cpu_feature.h	            CPU����
    leak_detective.c leak_detective.h	    �������
    identification.c identification.h	    ʶ��
    parser_helper.c parser_helper.h	        ��������
    test.c test.h	                        ����
   
https://blog.csdn.net/weixin_30472035/article/details/96492625   
ipsec.conf��stroke���ʹ�õ������ļ�����������ike proposal��ike peer��ipsec proposal������   
ע��ipsec.conf��������ļ���strongswan�����汾����������ˣ��������ʹ��swanctl.conf
   
https://blog.csdn.net/lz619719265/article/details/91041359
ipsec.conf��������Ľ���   
   
https://docs.strongswan.org/docs/5.9/config/IKEv2.html
strongswan �����ļ�����Ӧ��ʾ��   
   
https://wiki.strongswan.org/projects/strongswan/wiki/Fromipsecconf
�� ipsec.conf Ǩ�Ƶ� swanctl.conf
    Noel Kuntzeд��һ��python�ű������ڽ�ipsec.conf�����swanctl.conf��
    ��ipsec.conf��ipsec.secrets�е�ÿһ�������swanctl.conf�еĶԵ�ת����
    �����Ӧ��ϵ����ο�ԭ����
ע��ipsec.conf��������ļ���strongswan�����汾����������ˣ��������ʹ��swanctl.conf
   
https://www.cnblogs.com/hugetong/p/11143357.html
charon���̳�ʼ���׶ε�����ͼ
Լ����
    ʵ�ߴ�������ͼ��
    ���ߴ������ջ����ͷ����������϶��¡�
    �����Ǹ����ߣ����Լ����
ͼ��file://../imgs/strongswan����ͼ.png
ͼ��file://../imgs/netlinkģ�����ͼ.png
ͼ��file://../imgs/��Task���ں�xfrmģ��ĵ��ù�ϵͼ.png
˵����
    ��ͼ��kernel-netlink pluginΪ��������strongswan 5.7.1����Ҫ����ܹ���
    ��ͼ�����ּܹ��Ĳ��ֲ��棬����չʾȫòΪĿ�ġ�

https://www.cnblogs.com/hugetong/p/11143366.html
strongswan SA������һ��
1 ����
    ������Ҫ�����������Ľ�Ҫ�����ĺ��ĸ��
    ������SA��SP��ע�⣬�ⲻ��һƪ����Ҫ����֪ʶ�����¡�
    ������Ϊ���ʺ��Ķ����������ݵĵ�ǰ���ǣ����Ѿ��߱���һ���������֪ʶ��
    a. ʲô��VPN��
    b. ʲô��IPsec������IKE��ESP��strongswan����ʲô�ȡ�
    c. һ���linuxʹ�÷����ͳ������
    1.1 ʲô��SAD��SPD
        SAD��Security Association Database����д��
        SPD��Security Policy Database����д��
        SAD�������洢SA�����ݿ⡣SPD�������洢SP�����ݿ⡣
    1.2 ʲô��SPI
        SPI��Security Parameter Index����д������һ�����֣����ȣ�����
        ��ʹ����SAD��SPD����Ϊ������һ���֡�����IKEЭ�̵�����ͻ������ѡ���UUID����
        0-255�Ǳ�������ֵ����ֹ��SPI��ʹ�á�
    1.3 ʲô��SA
        SA��Security Association����д��
        SA��һ���㷨���㷨����������key���ļ��ϣ�������ɵ�����������������ܺ���֤����
        ͨ��SPI�����ݰ���Ŀ�ĵ�ַ����Ψһ���ҵ�һ��SA��
        ���������ԣ�
            �����㷨
                ����
                key
            ��֤�㷨
                ����
                key
            SPI
            Ŀ�ĵ�ַ
    1.4 ʲô��SP
        SP��Security Policy����д��
        SP��һ�����򣬾���һ������flow���Ƿ���Ҫ��IPsec����
        SP�Ĵ��������ַ�ʽ��
            ����
            ������
            ����
        ��Ҫ��IPsec����������ᱻָ��һ��template��
        һ��template�������Ϊָ��һ��SA��template�����������ԣ�
            Э��
                AH��ESP��
            ģʽ
                transport��tunnelģʽ��
            pattern
                ԴIP��Ŀ��IP�ԡ�
                NAT��PORT�ԡ�
            SP��һ���������ԣ�ȡֵ�ֱ�Ϊ��
                out
                in
                fwd
    1.5 �ܽ�
        ������IPsec��������ת�߼��У�SP�������What todo��SA�������How todo��
2 ������
    �򵥵�˵�����ı���ͨ��IPsec VPN�豸���ESP����ȥ�Ĺ����ǣ�
        ����·�ɡ�
        ����policy�����Ƿ���Ҫ��ESP
        ����SA�����ܷ�װ��
        ���ܷ�װ��İ��ٲ�·�ɡ�
    IPsec����ͨ��IPsec VPN�豸��ɷǼ��ܰ�����ȥ�Ĺ��̣�
        ����·�ɡ�
        ����policy�����Ƿ���ҪҪ��ESP
        ����SA�����ܽ��װ��
        ���ܽ��װ��İ��ٲ�·�ɡ�
    ͼ��file://../imgs/�����������ͼ.png
3 ���linux kernel�е�sa����͹���
    3.1 �ṩ���û���sa�ӿ�
        ���kernel sa���û�չʾ����̬�����԰����������linux kernel����ipsec sa�Ľ�ģ�ͳ���
        ��������VPN��Ʒ��saģ������н��ṩ������
        3.1.1 ʹ��racoon����sa
            setkey add 192.168.0.1 192.168.1.2 esp 0x10001
                        -m tunnel
                        -E des-cbc 0x3ffe05014819ffff
                        -A hmac-md5 "authentication!!"
            ��������Ϣ���Ժ����׿��������������ĺ��壬
            ����-E��������㷨������key��-A������֤�㷨������key��0x10001Ϊspi
        3.1.2 ʹ��racoon����policy(�й�racoon���Σ�https://blog.csdn.net/zhangyang0402/article/details/5730123��
            setkey spdadd 10.0.11.41/32[21] 10.0.11.33/32[any] any
                          -P out ipsec esp/tunnel/192.168.0.1-192.168.1.2/require
            ��һ�д�����Ԫ�飬any����Э�顣
            �ڶ��д���policy�ľ�������������action��template
        3.1.3 �ܽ�
            ͨ����������С�ڵ�����������Ӧ���Ѿ������׵��ܽ��������һ��SA��һ��policy����Ҫ�ṩ�����������Ϣ�ˡ�
            ���߽��ڱ��µ���󣬶�sa��policy�����������б�����Ϣ����һ��ͳһ���ܽᡣ
            ���⣬ͨ�����ĵ��﷨������Ӧ���ܹ����֣�policy��sa֮���match������
            ����Ҫһ���Ը��ӵ�ƥ���߼���ʵ�ֵģ�����������һ���򵥵�ƥ���ϵ��
    3.2 netlink��SA�ӿ�
        strongswan��Ŀǰʹ�����ַ�ʽ���ں˽���ipsec�����ý�����
        �ֱ�Ϊnetlink��pfkey��<file://../Linux Netlink����.py> <file://../PF_KEYЭ��.txt>
        ��ٷ��ĵ�������netlink��strongswanĬ�����õģ����stable�Ľӿڷ�ʽ��
        �������й���Ҳ����netlink��ʽΪ������չ���ģ��ּ򵥽�������
        3.2.1 ʲô��netlink
            netlink�Ǹ�����socket��ʽ���ں����û�̬IPC����
            Why and How to Use Netlink Socket: https://www.linuxjournal.com/article/7356
        3.2.2 �ӿڷ�ʽ
            ��netlink��ʽ����ipsec�ķ���
            netlink��һ���÷�
                ��ʼ��socket
                    �볣���socket�÷���ͬ��ֻ�Ǵ��������netlink��������в���
                �·�������Ϣ��kernel
                    ʹ��socket�ı�׼send��write�ӿڽ��ض���ʽ�Ĳ����·���kernel
                    ������ʽ����
                        struct nlmsghdr
                        {
                          __u32 nlmsg_len;   /* Length of message */
                          __u16 nlmsg_type;  /* Message type*/
                          __u16 nlmsg_flags; /* Additional flags */
                          __u32 nlmsg_seq;   /* Sequence number */
                          __u32 nlmsg_pid;   /* Sending process PID */
                        };
                    ��������ṹ���Ǵ��������ͷ�������������ͷ��֮����ڴ��������Ĳ�����ֵ��
                    ���Ľ���������nlmsg_type��ֵ��ȷ�������Ľ�β��nlmsg_len����ֵ������
                ���sa
                    ���sa��ʱ��nlmsghdr����Ĳ���Ϊ�ṹ��
                    struct xfrm_usersa_info
                    nlmsg_type��ֵΪ��XFRM_MSG_NEWSA
                    �ⲿ�����ݶ�����ϵͳ�ļ� /usr/include/linux/xfrm.h
                    ����ṹ���ߣ�����Ҫ׷���㷨���ֵ���Ϣ������
                    struct xfrm_algo
                    struct xfrm_algo_auth
                ���policy
                    ���policy��ʱ��nlmsghdr����Ĳ���Ϊ�ṹ��
                    struct xfrm_userpolicy_info
                    nlmsg_type��ֵΪ��XFRM_MSG_NEWPOLICY
                    �ⲿ�����ݶ�����ϵͳ�ļ� /usr/include/linux/xfrm.h
    3.3 xfrm��SA�ӿ�
        3.3.1 ʲô��xfrm
            xfrm(transform)��һ��IP��ת����ܡ���Ҫʵ�����������ֹ��ܣ�
                IPsec protocol suite
                IP Payload Compression Protocol
                Mobile IPv6
        3.3.2 �ں˴���
            linux/net/xfrm/
            ��Ҫ����
                Xfrm_lookup()            xfrm lookup(SPD and SAD) method
                Xfrm_input()             xfrm processing for an ingress packet
                Xfrm_output()            xfrm processing for an egress packet
                Xfrm4_rcv()              IPv4 specific Rx method
                Xfrm6_rcv()              IPv6 specific Rx method
                Esp_input()              ESP processing for an ingress packet
                Esp_output()             ESP processing for an egress packet
                Ah_output()              AH processing for an ingress packet
                Ah_input()               ESP processing for an egress packet
                xfrm_policy_alloc()      allocates an SPD object
                Xfrm_policy_destroy()    frees an SPD object
                xfrm_policy_lookup       SPD lookup
                xfrm_policy_byid()       SPD lookup based on id
                Xfrm_policy_insert()     Add an entry to SPD
                Xfrm_Policy_delete()     remove an entry from SPD
                Xfrm_bundle_create()     creates a xfrm bundle
                Xfrm_policy_delete()     releases the resources of a policy object
                Xfrm_state_add()         add an entry to SAD
                Xfrm_state_delete()      free and SAD object
                Xfrm_state_alloc()       allocate an SAD object
                xfrm_state_lookup_byaddr()     src address based SAD lookup
                xfrm_state_find()        SAD look up based on dst
                xfrm_state_lookup()      SAD lookup based on spi
        3.3.3 API
            api�ļ�  include/uapi/linux/xfrm.h ����
        3.3.4 sa�Ĵ������
            struct xfrm_usersa_info {
                    struct xfrm_selector            sel; // ���������Σ�ΪɶҪ�������
                    struct xfrm_id                  id; // Ŀ��ip��spi��Э��ah/esp
                    xfrm_address_t                  saddr; // Դip
                    struct xfrm_lifetime_cfg        lft;
                    struct xfrm_lifetime_cur        curlft;
                    struct xfrm_stats               stats;
                    __u32                           seq;
                    __u32                           reqid;
                    __u16                           family;
                    __u8                            mode; // transport / tunnel
                    __u8                            replay_window;
                    __u8                            flags;
            };  
            �㷨������׷����SA�ṹ��֮����ڴ�飬���ݲ�ͬ�����;�����ͬ�Ľṹ��ʾ����
            struct xfrm_algo {
                    char            alg_name[64];
                    unsigned int    alg_key_len;    /* in bits */
                    char            alg_key[0];
            };
            struct xfrm_algo_auth {
                    char            alg_name[64];
                    unsigned int    alg_key_len;    /* in bits */
                    unsigned int    alg_trunc_len;  /* in bits */
                    char            alg_key[0];
            };
        3.3.5 policy�Ĵ������
            struct xfrm_userpolicy_info {
                    struct xfrm_selector            sel; //���Σ�ip��port��Э��
                    struct xfrm_lifetime_cfg        lft;
                    struct xfrm_lifetime_cur        curlft;
                    __u32                           priority; //
                    __u32                           index;
                    __u8                            dir;  //����in out fwd
                    __u8                            action; // allow, block
                    __u8                            flags;
                    __u8                            share;
            };
    4 xfrm��ʵ��
        4.1 ���ڴ洢sa���ڲ����ݽṹ
            struct xfrm_state  �Σ�file://xfrm.txt
        4.2 ���ڴ洢sp���ڲ����ݽṹ
            struct xfrm_policy �Σ�file://xfrm.txt
        4.3 �ؼ�����
            xfrm_lookup()
            xfrm_output()
            xfrm4_policy_check() // ��ipv4�б����á�
    5 strongswan�е�sa
        5.1 ����
            ��IKEЭ��ĽǶ��ϣ�������SA��һ����IKE_SA��һ����CHILD_SA��
            �������۵�sa����ָ��ͼ�е�CHILD_SA��
                  +---------------------------------+       +----------------------------+
                  |          Credentials            |       |          Backends          |
                  +---------------------------------+       +----------------------------+

                   +------------+    +-----------+          +------+            +----------+
                   |  receiver  |    |           |          |      |  +------+  | CHILD_SA |
                   +----+-------+    | Scheduler |          | IKE- |  | IKE- |--+----------+
                        |            |           |          | SA   |--| SA   |  | CHILD_SA |
                   +-------+--+      +-----------+          |      |  +------+  +----------+
                <->|  socket  |            |                | Man- |
                   +-------+--+      +-----------+          | ager |  +------+  +----------+
                        |            |           |          |      |  | IKE- |--| CHILD_SA |
                   +----+-------+    | Processor |----------|      |--| SA   |  +----------+
                   |   sender   |    |           |          |      |  +------+
                   +------------+    +-----------+          +------+

                  +---------------------------------+       +----------------------------+
                  |               Bus               |       |      Kernel Interface      |
                  +---------------------------------+       +----------------------------+
                         |                    |                           |
                  +-------------+     +-------------+                     V
                  | File-Logger |     |  Sys-Logger |                  //////
                  +-------------+     +-------------+
            ��ƪ���£�ͨƪ���۵�SAָ�Ķ��������CHILD_SA��
            CHILD_SA��strongswan�Ŀ�����Ҫ�������������֡�
                IKEЭ�̹��̡�
                    CHILD_SA��IKEЭ�̹����е��������⣺IKEЭ�̹���ͨ��CHILD_SA�������������
                    IKEЭ�̹��̽�����IKE-SA Manager��CHILD_SA����strongswan��ܡ�
                IPsec����������̡�
                    CHILD_SA��IKEЭ�̹����е����루��⣺IKEЭ�̹���ͨ��CHILD_SA�������������
                    strongswan��ܽ�CHILD_SA����libcharon plugin
                    ���ض���plugin��kernelͨ�ţ�
                    ��kernel�����IPsec tunnel�Ľ������̡�
                IPsec��ת�����̡�
                    �ⲿ�ֺ�strongswan�Ŀ��û���˹�ϵ�����ں���ɡ�
            5.1.1 strongswan�е�plugin
                ��һС���ᵽ��plugin������������plugin��
                ������plugins��һ����libstrongswan��plugin��һ����libcharon��plugin��
                libstrongswan��plugin��Ҫ�ṩ���ܣ���֤�����ݿ���صĹ��ܡ�
                libcharon��plugin��Ҫ�ṩ��specific needs��������
                ���ǽ�����Ҫ���۵���sa�·���ص�plugin����libcharon��һ������ǰ�����
                    kernel-libipsec
                        �û�̬��ת��ƽ�棬Ŀǰ�����ڸ�ʵ���Խ׶Ρ�ת������û��kernel��
                        ��Ҫ�������㲻��ʹ��kernelת���ĳ�����
                    kernel-netlink
                        ʹ��netlink�ӿ���linux kernel��xfrmģ�齻����Ŀǰ����ȶ�ʹ�ý׶Σ�Ĭ����ѡ��
                    kernel-pfkey
                        ʹ��pkkey�ӿ���linux kernel��xfrmģ����н�������ʵ���Խ׶Ρ�
                    kernel-iph
                        windows����ϵͳ�Ľӿڡ�
                    kernel-wfp
                        windows����ϵͳ�Ľӿڡ�
                ���ģ�ֻ����kernel-netlink��plugin
        5.2 ��������
            5.2.1 ����
                strongswan��������ʽ�ж��֡����Ժ͸��ֲ�ͬ��ϵͳ�Խӣ�����systemd��networkmanager�ȡ�
                    starter
                        ipsec����ʹ�õ��ػ����̡���ipsec start����ͻ�����������̡�
                    charon-nm
                        networkmanager��plugin��ʲô��nm��plugin��
                    charon-systemd
                        ����systemd��daemon styleʵ�ֵ�һ�����̡���systemd������
                    charon-svc
                        windows�ķ���
                ����������ʽ������Ŀ�Ķ�����������Ŀ�Ķ�������charon���̡����ԣ����������������ǣ�
                ֱ������ charon ����
                ��Ȼ�����ַ�ʽû��daemon�ػ������ǹ���������
            5.2.2 ���Է���
                ����һС��������charon���̿���ֱ�����С����Ե��Ե�ʱ��ֱ��ʹ��gdb����charon�Ϳ�����
                # gdb `which charon`
            5.2.3 starter����������
                ipsecʵ�ó�������ˡ�������ƺͼ��IPsec����/��֤ϵͳ�ġ�����ʵ�ó����е��κ�һ����
                ��ָ���Ĳ�����ѡ������ָ�����������ֱ�ӵ�����һ����
                ���ںܴ�̶���������������������ܳ��ֵ����Ƴ�ͻ��ͬʱҲ����һЩ���еķ���
                �����������ipsecΪ�����õ������ṩ�˺��ʵĻ���������
                ipsec start �Ĺ����ǵ���starter����starter�ֽ���ipsec.conf������IKE�ػ�����charon
                starter������������ͨ��ipsec�ű�ִ��start����(ipsec start)��������������strongswan����
                �ű�λ�ã�strongswan-5.7.1/src/ipsec/_ipsec
                ipsec�ű�����start�����󣬻�ִ��������������ػ�����starter
                ${IPSEC_DIR}/starter --daemon charon
                starter���̵�Դ��λ�ã�strongswan-5.7.1/src/starter/starter.c
                starter����Ҫ����������charon���̣��������ػ���
                    �� daemon�ĳ�ʼ�������ض��������signal��Ӧ�ȡ�
                    �� ����charon
                    �� ����ipsec.conf�е�����
            5.2.4 systemd����������
                systemd��������������ʹ��systemd��service���ýű�
                Ȼ������systemd��charon�ػ����̣�charon-systemd���̣�
                ���ͨ���ػ���������charon����
                systemd�ű�λ�ã�
                strongswan-5.7.1/init/systemd-swanctl/strongswan-swanctl.service.in
                service�ű�����������ִ����������
                1. ����charon-systemd���̡�
                2. ִ��swanctl --load-all --noprompt����
                charon-systemd����
                    Դ��λ�ã�strongswan-5.7.1/src/charon-systemd/charon-systemd.c
                    charon-systemd������charon���̵���һ����ڡ�
                    charon-systemd���̲����������µĽ��̣�
                    charon-systemed���̾��Ǵ���ҵ��������̣���systemd�����ػ���
                    ���ԣ�charon-systemdֻ��main�����е�����������charon��ͬ��
                    �����߼���charon������ȫ��ͬ
        5.3 ���ù���
                ���й����У���SA��ص�����������Ҫ����add_sa��add_policy�����ط�
                ��charon�����յ�һ��message��ʱ�򣬻���job����ʽ�ַ���standby��ҵ���߳̽��д���
                ���ͨ��kernel�������kernel_interface�ӿ��е�add_sa��add_policy����������
                �ӿڻ���ݾ���ע���plugin���ø�plugin����Ӧ��add_as, add_policy����
                ���磬netlink��plugin���ڸ�plugin�������������У�
                ��ͨ��netlink�Ľӿ����յ����ں˵�xfrm�ӿ����sa��policy���·��͸��µȲ���
        5.4 strongswan�е����ݽṹ
                sa���ݽṹ
                    �������ļ� kernel_ipsec.h �У���id��data�����ṹ��ͬ���
                    struct kernel_ipsec_sa_id_t {
                            /** Source address */
                            host_t *src;
                            /** Destination address */
                            host_t *dst;
                            /** SPI */
                            uint32_t spi;
                            /** Protocol (ESP/AH) */
                            uint8_t proto;
                            /** Optional mark */
                            mark_t mark;
                    }; 
                    //Data required to add an SA to the kernel
                    struct kernel_ipsec_add_sa_t {
                            /** Reqid */
                            uint32_t reqid;
                            /** Mode (tunnel, transport...) */
                            ipsec_mode_t mode;
                            /** List of source traffic selectors */
                            linked_list_t *src_ts;
                            /** List of destination traffic selectors */
                            linked_list_t *dst_ts;
                            /** Network interface restricting policy */
                            char *interface;
                            /** Lifetime configuration */
                            lifetime_cfg_t *lifetime;
                            /** Encryption algorithm */
                            uint16_t enc_alg;
                            /** Encryption key */
                            chunk_t enc_key;
                            /** Integrity protection algorithm */
                            uint16_t int_alg;
                            /** Integrity protection key */
                            chunk_t int_key;
                            /** Anti-replay window size */
                            uint32_t replay_window;
                            /** Traffic Flow Confidentiality padding */
                            uint32_t tfc;
                            /** IPComp transform */
                            uint16_t ipcomp;
                            /** CPI for IPComp */
                            uint16_t cpi;
                            /** TRUE to enable UDP encapsulation for NAT traversal */
                            bool encap;
                            /** no (disabled), yes (enabled), auto (enabled if supported) */
                            hw_offload_t hw_offload;
                            /** Mark the SA should apply to packets after processing */
                            mark_t mark;
                            /** TRUE to use Extended Sequence Numbers */
                            bool esn;
                            /** TRUE to copy the DF bit to the outer IPv4 header in tunnel mode */
                            bool copy_df;
                            /** TRUE to copy the ECN header field to/from the outer header */
                            bool copy_ecn;
                            /** Whether to copy the DSCP header field to/from the outer header */
                            dscp_copy_t copy_dscp;
                            /** TRUE if initiator of the exchange creating the SA */
                            bool initiator;
                            /** TRUE if this is an inbound SA */
                            bool inbound;
                            /** TRUE if an SPI has already been allocated for this SA */
                            bool update;
                    }; 
                policy���ݽṹ
                    �������ļ� kernel_ipsec.h �� ipsec_types.h ��
                    struct kernel_ipsec_policy_id_t {
                            /** Direction of traffic */
                            policy_dir_t dir;
                            /** Source traffic selector */
                            traffic_selector_t *src_ts;
                            /** Destination traffic selector */
                            traffic_selector_t *dst_ts;
                            /** Optional mark */
                            mark_t mark; 
                            /** Network interface restricting policy */
                            char *interface;
                    };
                    // Data required to add/delete a policy to/from the kernel
                    struct kernel_ipsec_manage_policy_t {
                            /** Type of policy */
                            policy_type_t type;
                            /** Priority class */
                            policy_priority_t prio;
                            /** Manually-set priority (automatic if set to 0) */
                            uint32_t manual_prio;
                            /** Source address of the SA(s) tied to this policy */
                            host_t *src;
                            /** Destination address of the SA(s) tied to this policy */
                            host_t *dst;
                            /** Details about the SA(s) tied to this policy */
                            ipsec_sa_cfg_t *sa;
                    };
                    struct ipsec_sa_cfg_t {
                        /** mode of SA (tunnel, transport) */
                        ipsec_mode_t mode;
                        /** unique ID */
                        uint32_t reqid;
                        /** number of policies of the same kind (in/out/fwd) attached to SA */
                        uint32_t policy_count;
                        /** details about ESP/AH */
                        struct {
                            /** TRUE if this protocol is used */
                            bool use;
                            /** SPI for ESP/AH */
                            uint32_t spi;
                        } esp, ah;
                        /** details about IPComp */
                        struct {
                            /** the IPComp transform used */
                            uint16_t transform;
                            /** CPI for IPComp */
                            uint16_t cpi;
                        } ipcomp;
                    }; 
        5.5 charon����
            charon�������������ɹ�������16�����߳�ִ�в�ͬ��job
            ����charon�е��������Χ����task��job�������ĸ������
            ͼ��file://imgs/charon��������ͼ.png
    6 sa�ĳ���ģ��
        sa
            Ŀ�ĵ�ַ��dip���� spi Ψһȷ��һ��sa��Ŀ
            ����	    ȡֵ	        ˵��
            id		
            spi		                    Э�̹��̴�������
            mode	    transport/tunnel	
            protocol	esp/ah/ipcom	����Э��ķ�ʽ
            sip		                    ��һ�������sip��dip�����ģ�������sa
            dip		
            life		                ����ʱ��
            enc_alg		
            enc_key		
            integrity_alg		        ��������֤
            integrity_key		
            nat		                    �Ƿ���nat
        policy
            ����	ȡֵ	        ˵��
            id		
            action	drop/pass/ipsec	���д˲��Ժ����Ϊ
            priority		        ���ȼ�
            dir	    in/out/fwd	    ����
            s_ts		            source traffic selector
            d_ts		            destination traffic selector
        traffic selector
            ts������Ԫ�飬ipʹ��������������һ���Ρ�portҲ������
            ����	        ˵��
            source ip	
            sip_prefixlen	
            dest ip	
            dip_prefixlen	
            sport	
            sport_mask	
            dport	
            dport_mask	
            protocol	
    7 ����
        7.1 policy��·�ɵĹ�ϵ
            ���ҵĲ�����������ɾ���˲���·��֮�󣬹���������Ŀǰ�������Ϊʲô��
            ·����policy֮��Ĺ�ϵ���Լ�·�ɺ�policy���ں˰�ת�������е��߼���ϵ��
            ����Ҫ��һ���ĵ��С�
            
https://www.cnblogs.com/hugetong/p/11143369.html
strongwan sa����(��)  rekey/reauth ���Ʒ���