�Σ�https://www.cnblogs.com/liuhedong/p/10695969.html

nmcli : network manager command line interface
nmcli������redhat7����centos7֮������
nmcui �� mncli �Ŀ��ӻ���
���������������������е����ù��������ҿ���д�������ļ���������Ч
nmcliʵ�ù�������NetworkManager���ṩ �� yum install -y NetworkManager
����NetworkManager
    NetworkManager��һ������ϵͳ�������ӡ�
    ���ҽ���״̬ͨ��D-BUS���б���ĺ�̨����
    �Լ�һ�������û������������ӵĿͻ��˳���
    #D-BUS��һ���ṩ�򵥵�Ӧ�ó�����ͨѶ��;�������������Ŀ��
    #������Ϊfreedesktoporg��Ŀ��һ�����������ġ�
    NetworkManager���Լ���CLI���ߣ�nmcli��
    ʹ��nmcli�û����Բ�ѯ�������ӵ�״̬��Ҳ������������
�﷨��  nmcli [OPTIONS...] OBJECTS [COMMAND] [ARGUMENTS...] 
        OBJECTS = {help | general | networking | radio | connection | device | agent | monitor} 
        OPTIONS
            -t	���������Ὣ����Ŀո�ɾ����
            -p	���Ի�����������Ư��
            -n	�Ż������������ѡ��tabular(���Ƽ�)��multiline(Ĭ��)
            -c	��ɫ���أ�������ɫ���(Ĭ������)
            -f	�����ֶΣ�allΪ���������ֶΣ�common��ӡ���ɹ��˵��ֶ�
            -g	�����ֶΣ������ڽű�����:�ָ�
            -w	��ʱʱ��
        OBJECTS
            general ����ѡ��
                �����ʽ��nmcli general {status|hostname|permissions|logging}
                ����������ʹ�ô����������ʾ���������״̬��Ȩ�ޣ�
                          ����Ի�ȡ�͸���ϵͳ���������Լ������������־��¼�������
                status 
                    ��ʾ���������������״̬
                hostname 
                    ��ȡ��������ø�����������û�и�������������£���ӡ���õ���������
                    ��ָ���˲������������ƽ���NetworkManager��������Ϊ�µ�ϵͳ������
                permissions
                    ��ʾ��ǰ�û������������������Ĳ���Ȩ�ޡ� 
                    �����úͽ������硢����WI-FI��WWAN״̬���޸����ӵ�
                loggin
                    ��ȡ�͸��������������־��¼�������
                    û���κβ�����ǰ��־��¼���������ʾ��
                    Ϊ�˸�����־��¼״̬, ���ṩ����������,
                    �йؿ��ü������ֵ,����NetworkManager.conf
            networking �������
                �����ʽ��nmcli networking {on|off|connectivity}
                ������������ѯ�������������״̬�������͹ر�����
                ѡ�
                    on: �������нӿ�
                    off: �������нӿ�
                    connectivity: ��ȡ����״̬��
                        ��ѡ����checl����������������¼�������ԣ�
                        ������ʾ�����֪��״̬�����������¼�顣
                        ���ܵ�״̬������ʾ:
                            none: ����Ϊ���ӵ��κ�����
                            portal: �޷����������Ļ�����
                            limited: ���������ӵ����磬���޷����ʻ�����
                            full: �������ӵ����磬��������ȫ����
                            unknown: �޷��ҵ�����״̬    
            radio �����޴������
                �����ʽ��nmcli radio {all|wifi|wwan}
                ��ʾ���߿���״̬�������úͽ��ÿ���
            monitor �������
                ���������ACTIVITY MONITOR��
                �۲��������������������ӵı仯״̬���豸�����������ļ���
            connection ���ӹ���
                �����ʽ��nmcli connection {show|up|down|modify|add|
                                            edit|clone|delete|monitor|
                                            reload|load|import|export}
                ������Ҫʹ�õ�һ�����ܡ�
                show
                    1. �г�������ӣ����������+-Ϊ������
                        # �鿴��������״̬
                        [root@www ~]# nmcli connection show
                        # ��ͬ��nmcli connection show --order +active
                        [root@www ~]# nmcli connection show --active
                        # �Ի�����ӽ�������
                        [root@www ~]# nmcli connection show --order +active
                        # ��������������������
                        [root@www ~]# nmcli connection show --order +name
                        # ��������������������(����)
                        [root@www ~]# nmcli connection show --order -type
                    2. �鿴ָ�����ӵ���ϸ��Ϣ
                        [root@www ~]# nmcli connection show eth0
                up
                    �������ӣ��ṩ�������ƻ�uuid���м��
                    ��δ�ṩ�������ʹ��ifnameָ���豸�����м���
                    # �����������м���
                    [root@www ~]# nmcli connection up eth0
                    # ��uuid���м���
                    [root@www ~]# nmcli connection up 5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03
                    # ���豸�ӿ������м���
                    [root@www ~]# nmcli connection up ifname eth0
                down
                    ͣ�����ӣ��ṩ��������uuid����ͣ�ã�
                    ��δ�ṩ�������ʹ��ifnameָ���豸�����м���
                    # �����������м���
                    [root@www ~]# nmcli connection down eth0
                    # ��uuid���м���
                    [root@www ~]# nmcli connection down 5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03
                    # ���豸�ӿ������м���
                    [root@www ~]# nmcli connection down ifname eth0
                modify
                    ��Щ���Կ�����nmcli connection show eth0���л�ȡ��
                    Ȼ������޸ġ���ӻ�ɾ�����ԣ���Ҫ�������ԣ�ֻ��ָ���������ƺ��ֵ��
                    ��ֵ��ɾ������ֵ��ͬһ������Ӷ��ֵʹ��+��ͬһ����ɾ��ָ��ֵ��-������
                    ��Ӷ��ip:
                        # �������
                        [root@www ~]# nmcli connection modify eth0 +ipv4.addresses 192.168.100.102/24
                        [root@www ~]# nmcli connection modify eth0 +ipv4.addresses 192.168.100.103/24
                        [root@www ~]# nmcli connection modify eth0 +ipv4.addresses 192.168.100.104/24
                        # �鿴
                        [root@www ~]# nmcli -f IP4 connection show eth0
                        IP4.ADDRESS[1]:                         192.168.100.101/24
                        IP4.GATEWAY:                            192.168.100.100
                        IP4.DNS[1]:                             8.8.8.8
                        # ��������
                        [root@www ~]# nmcli connection up eth0
                        Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/18)
                        # �ٴβ鿴
                        [root@www ~]# nmcli -f IP4 connection show eth0
                        IP4.ADDRESS[1]:                         192.168.100.101/24
                        IP4.ADDRESS[2]:                         192.168.100.102/24
                        IP4.ADDRESS[3]:                         192.168.100.103/24
                        IP4.ADDRESS[4]:                         192.168.100.104/24
                        IP4.GATEWAY:                            192.168.100.100
                        IP4.DNS[1]:                             8.8.8.8
                    ɾ��ָ��ip
                        [root@www ~]# nmcli -f IP4 connection show eth0
                        IP4.ADDRESS[1]:                         192.168.100.101/24
                        IP4.ADDRESS[2]:                         192.168.100.102/24
                        IP4.ADDRESS[3]:                         192.168.100.103/24
                        IP4.ADDRESS[4]:                         192.168.100.104/24
                        IP4.GATEWAY:                            192.168.100.100
                        IP4.DNS[1]:                             8.8.8.8
                        # ɾ������ǰ����Ϊ2�ĵ�ַ
                        [root@www ~]# nmcli connection modify eth0 -ipv4.addresses 2
                        # �鿴
                        [root@www ~]# nmcli -f IP4 connection show eth0
                        IP4.ADDRESS[1]:                         192.168.100.101/24
                        IP4.ADDRESS[2]:                         192.168.100.102/24
                        IP4.ADDRESS[3]:                         192.168.100.103/24
                        IP4.ADDRESS[4]:                         192.168.100.104/24
                        IP4.GATEWAY:                            192.168.100.100
                        IP4.DNS[1]:                             8.8.8.8
                        # �ٴμ���
                        [root@www ~]# nmcli connection up eth0
                        Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/19)
                        # �鿴
                        [root@www ~]# nmcli -f IP4 connection show eth0
                        IP4.ADDRESS[1]:                         192.168.100.101/24
                        IP4.ADDRESS[2]:                         192.168.100.102/24
                        IP4.GATEWAY:                            192.168.100.100
                        IP4.DNS[1]:                             8.8.8.8
                add
                    ���Ǵ���һ���µ����ӣ���Ҫָ���´������ӵ����ԣ��﷨��modify��ͬ
                    [root@www ~]# nmcli con add con-name eth1 type ethernet  autoconnect yes ifname eth0
                    # con-name     ��������
                    # type              ��������
                    # autoconnect �Ƿ��Զ�����
                    # ifname          ���ӵ����豸����
                    ��������ͻ򷽷�����ʹ��nmcli connection add help�鿴
                clone
                    ��¡���ӣ���¡һ�����ڵ����ӣ������������ƺ�uuid�������ɵģ���������һ����
                    [root@www ~]# nmcli connection clone eth0 eth0_1
                delete
                    ɾ�����ӣ��⽫ɾ��һ������
                    [root@www ~]# nmcli connection delete eth0_1
                load
                    �Ӵ��̼���/���¼���һ�����������ļ���
                    �������ֶ�������һ��/etc/sysconfig/network-scripts/ifcfg-ethx�����ļ���
                    ����Խ�����ص�������������Ա����
                    [root@www ~]# echo -e "TYPE=Ethernet\nNAME=ethx" > /etc/sysconfig/network-scripts/ifcfg-ethx
                    [root@www ~]# nmcli connection show
                    NAME  UUID                                  TYPE            DEVICE 
                    eth0  5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03  802-3-ethernet  eth0 
                    [root@www ~]# nmcli connection load /etc/sysconfig/network-scripts/ifcfg-ethx 
                    [root@www ~]# nmcli connection show
                    NAME  UUID                                  TYPE            DEVICE 
                    eth0  5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03  802-3-ethernet  eth0   
                    ethx  d45d97fb-8530-60e2-2d15-d92c0df8b0fc  802-3-ethernet  --
                monitor
                    �������������ļ����ÿ��ָ�������Ӹ���ʱ, ��������ӡһ�С�
                    Ҫ���ӵ������������ơ�UUID �� D ����·����ʶ��
                    ��� ID ����ȷ, �����ʹ�ùؼ��� id��uuid ��·����
                    �й� ID ָ���ؼ��ֵ�˵��, ����������������ʾ��
                    �����������������ļ�, �Է�ָ���ޡ�
                    �����м��ӵ�������ʧʱ, �������ֹ��
                    ���Ҫ�������Ӵ���, �뿼��ʹ�ô��� nmcli �����������ȫ�ּ�����
                    [root@www ~]# nmcli connection monitor eth0
            device �豸����
                �����ʽ��nmcli device {status|show|set|connect|
                                        reapply|modify|disconnect|
                                        delete|monitor|wifi|lldp}
                ��ʾ�͹����豸�ӿڡ�
                ��ѡ���кܶ๦�ܣ���������wifi�������ȵ㣬ɨ�����ߣ��ڽ����ֵȣ�
                ������г�����ѡ���ϸ���ܿ�ʹ��nmcli device help�鿴��
                status
                    ��ӡ�豸״̬�����û�н�����ָ����nmcli device��������Ĭ�ϲ���
                    [root@www ~]# nmcli device status
                    DEVICE  TYPE      STATE      CONNECTION 
                    eth0    ethernet  connected  eth0       
                    lo      loopback  unmanaged  --         
                    [root@www ~]# nmcli device
                    DEVICE  TYPE      STATE      CONNECTION 
                    eth0    ethernet  connected  eth0       
                    lo      loopback  unmanaged  --
                show
                    ��ʾ�����豸�ӿڵ���ϸ��Ϣ
                    # ��ָ���豸�ӿ����ƣ�����ʾ���нӿڵ���Ϣ
                    [root@www ~]# nmcli device show eth0
                    GENERAL.DEVICE:                         eth0
                    GENERAL.TYPE:                           ethernet
                    GENERAL.HWADDR:                         00:0C:29:99:9A:A1
                    GENERAL.MTU:                            1500
                    GENERAL.STATE:                          100 (connected)
                    GENERAL.CONNECTION:                     eth0
                    GENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/9
                    WIRED-PROPERTIES.CARRIER:               on
                    IP4.ADDRESS[1]:                         192.168.100.101/24
                    IP4.ADDRESS[2]:                         192.168.100.102/24
                    IP4.GATEWAY:                            192.168.100.100
                    IP4.DNS[1]:                             8.8.8.8
                set
                    �����豸����
                    [root@www ~]# nmcli device set ifname eth0 autoconnect yes
                connect
                    �����豸���ṩһ���豸�ӿڣ�����������������ҵ�һ�����ʵ�����, �������
                    ����������δ����Ϊ�Զ����ӵ����ӡ�(Ĭ�ϳ�ʱΪ90s)
                    [root@www ~]# nmcli dev connect eth0
                    Device 'eth0' successfully activated with '5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03'.
                reapply
                    ʹ���ϴ�Ӧ�ú�Ե�ǰ����������ĸ����������豸��
                    [root@www ~]# nmcli device reapply eth0
                    Connection successfully reapplied to device 'eth0'.
                modify
                    �޸��豸�ϴ��ڻ���豸�������޸�ֻ����ʱ�ģ�������д���ļ���
                    ���﷨�� nmcli connection modify ��ͬ��
                    [root@www ~]# nmcli device modify eth0 +ipv4.addresses 192.168.100.103/24
                    Connection successfully reapplied to device 'eth0'.
                    [root@www ~]# nmcli dev show eth0
                    [root@www ~]# nmcli device modify eth0 -ipv4.addresses 1
                    Connection successfully reapplied to device 'eth0'.
                disconnect
                    �Ͽ���ǰ���ӵ��豸����ֹ�Զ����ӡ���ע�⣬�Ͽ���ζ���豸ֹͣ�������� connect ��������
                    [root@www ~]# nmcli device disconnect eth0
                delete
                    ɾ���豸���������ϵͳ��ɾ���ӿڡ�
                    ��ע��, �������������bonds, bridges, teams������豸��
                    �����޷�ɾ��Ӳ���豸 (����̫��)����ʱʱ��Ϊ10��
                    [root@www ~]# nmcli device delete bonds
                monitor
                    �����豸���ÿ��ָ�����豸����״̬ʱ, ��������ӡһ�С�
                    ���������豸�Է�δָ���ӿڡ�������ָ�����豸��ʧʱ, ����������ֹ��
                    ���Ҫ�����豸���, �뿼��ʹ�ô��� nmcli �����������ȫ�ּ�������
                    [root@www ~]# nmcli device monitor eth0
        nmcli ����״̬��
            mcli ����ɹ��˳�״ֵ̬Ϊ0��������������򷵻ش���0��ֵ
            0: �ɹ�-ָʾ�����ѳɹ�
            1: λ�û�ָ���Ĵ���
            2: ��Ч���û����룬�����nmcli����
            3: ��ʱ�ˣ������ --wait ѡ�
            4: ���Ӽ���ʧ��
            5: ����ͣ��ʧ��
            6: �Ͽ��豸ʧ��
            7: ����ɾ��ʧ��
            8: ���������û������
            10: ���ӡ��豸�����㲻����
            65: ��ʹ�� --complete-args ѡ��ļ���Ӧ��ѭ��
            
�Σ�https://blog.csdn.net/qq_40907977/article/details/88380855            
mcli��������Ǵ�����̫��ķ��㣬����nmcli���ܽ�����
    ͨ�����������IP��ַ��DNS�����ص���Ϣ������Ӱ��Ķ���/etc/sysconfig/network-scripts/ifcfg-ens32�����ļ�
    ���ڡ�nmcli connection reload�����ֻҪ���Ĺ���������������ļ�������Ҫ�����ز������ܼ���������
    ����������������������nmcli connection up ens32������nmcli device reapplyens32������nmcli device connect ens32����
    ������������һ����������ϲ�ü��ɡ�
    ����DNS,��ifcfg.ens32�����ã�������Ч�ĵط���/etc/resolve.conf�����ɾ�����ļ��е�DNS��Ϣ�����������ӻ�ʧ�ܡ�
