route ���鿴·�ɱ�
    file://D:/workspace/projects/baseroot/base/depts/jc1/private/weijianmin/ѧϰ�ʼ�/����/·�ɱ�.txt

=========================================================    

����·��  
    ���ԣ�file://D:/workspace/projects/baseroot/base/depts/jc1/private/weijianmin/ѧϰ�ʼ�/ipsec vpn/strongswan/strongswan���.py
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
        
========================================================= 

ʹ��ipsec��������sa
    ���ԣ�file://D:/workspace/projects/baseroot/base/depts/jc1/private/weijianmin/ѧϰ�ʼ�/ipsec vpn/strongswan/strongswan���.py    
    1 ʹ��racoon����sa
        setkey add 192.168.0.1 192.168.1.2 esp 0x10001
                    -m tunnel
                    -E des-cbc 0x3ffe05014819ffff
                    -A hmac-md5 "authentication!!"
        ��������Ϣ���Ժ����׿��������������ĺ��壬
        ����-E��������㷨������key��-A������֤�㷨������key��0x10001Ϊspi
    2 ʹ��racoon����policy(�й�racoon���Σ�https://blog.csdn.net/ai58203/article/details/101469199��
        setkey spdadd 10.0.11.41/32[21] 10.0.11.33/32[any] any
                      -P out ipsec esp/tunnel/192.168.0.1-192.168.1.2/require
        ��һ�д�����Ԫ�飬any����Э�顣
        �ڶ��д���policy�ľ�������������action��template   

========================================================= 

����xfrm
       file://D:/workspace/projects/baseroot/base/depts/jc1/private/weijianmin/ѧϰ�ʼ�/ipsec vpn/IP XFRM����ʾ��.txt 
       
=========================================================

strongswan ����֤�飺
    pki --gen --type ed25519 --outform pem > strongswanKey.pem

    pki --self --ca --lifetime 3652 --in strongswanKey.pem \
               --dn "C=CH, O=strongSwan, CN=strongSwan Root CA" \
               --outform pem > strongswanCert.pem
     
    pki --print --in strongswanCert.pem

    pki --gen --type ed25519 --outform pem > moonKey.pem

    pki --req --type priv --in moonKey.pem \
              --dn "C=CH, O=strongswan, CN=moon.strongswan.org" \
              --san moon.strongswan.org --outform pem > moonReq.pem
              
    pki --issue --cacert strongswanCert.pem --cakey strongswanKey.pem \
                --type pkcs10 --in moonReq.pem --serial 01 --lifetime 1826 \
                --outform pem > moonCert.pem          
               
    pki --gen --type ed25519 --outform pem > sunKey.pem

    pki --req --type priv --in sunKey.pem \
              --dn "C=CH, O=strongswan, CN=sun.strongswan.org" \
              --san sun.strongswan.org --outform pem > sunReq.pem
              
    pki --issue --cacert strongswanCert.pem --cakey strongswanKey.pem \
                --type pkcs10 --in sunReq.pem --serial 01 --lifetime 1826 \
                --outform pem > sunCert.pem
            
=========================================================

�鿴·������  traceroute  ip

=========================================================

swanctl֤�����λ�ü���������
    /etc/swanctl/x509ca/strongswanCert.pem
    /etc/swanctl/x509/sunCert.pem
    /etc/swanctl/private/sunKey.pem
    swanctl --load-creds        
    swanctl --load-conns

=========================================================

arp -a �鿴���������arp��ͨ���������ж���������Щip��ռ��

=========================================================

ip xfrm state �鿴SA    // wireshark����esp��ʱ����ʹ�ø������г�������
ip xfrm state flush ���SA���ݿ�

==========================================================

ipsec-tool ����
    libipsec��PF_KEYʵ�ֿ�
        Ϊʵ��racoon��Setkeyģ�����ں˽�������ʹ��PF_KEYv2�׽���
    setkey����������SAD����ȫ�������ݿ⣩��SPD����ȫ�������ݿ⣩
    racoon��IKE�ػ����������Զ�����IPsec����
        һ����Կ�����ػ����̣�ʵ���û��е�IKE��ԿЭ��ģ�飬
        ��Ҫ�����Զ���ʽ����ͨ�ŶԶ���Ӧģ���SAЭ��
    racoonctl������racoon��shell����
    
==============================================================

����·�� 
     strongSwan ʹ����"����·��"��һ���繦��
     Linux ����·�ɵ�ʵ����Ҫ���·�ɱ��һ��·�ɲ������ݿ⣨RPDB��
     ip rule help
        ip rule { add | del } SELECTOR ACTION
        ip rule { flush | save | restore }
        ip rule [ list [ SELECTOR ]]
        SELECTOR := [ not ] [ from PREFIX ] [ to PREFIX ] [ tos TOS ] [ fwmark FWMARK[/MASK] ]
                    [ iif STRING ] [ oif STRING ] [ pref NUMBER ] [ l3mdev ]
                    [ uidrange NUMBER-NUMBER ]
        ACTION := [ table TABLE_ID ]
                  [ nat ADDRESS ]
                  [ realms [SRCREALM/]DSTREALM ]
                  [ goto NUMBER ]
                  SUPPRESSOR
        SUPPRESSOR := [ suppress_prefixlength NUMBER ]
                      [ suppress_ifgroup DEVGROUP ]
        TABLE_ID := [ local | main | default | NUMBER ]
     ip rule show���г� RPDB �еĲ���
        ����
        0:     from all lookup local 
        220:   from all lookup 220 
        32766: from all lookup main 
        32767: from all lookup default
     ip route list table local���г�local���п��õ�·��
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

==============================================================        
        
file://ip route ��  ip rule.py        

==============================================================

