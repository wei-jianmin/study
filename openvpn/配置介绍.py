--config file
    ���ֻ�������ļ�ѡ�û������ѡ������ʡ��ǰ���--config
    ˫�����ַ��������������ڽ������ո�ĵ�������������
    ��һ�������'#'��';'����ɱ�ע��
    openvpn2.0֮�󣬷�б�����������壬���ԣ�
    ��\\��ʾһ����ͨ�ķ�б�ܣ�
    ��\"��ʾʹ����ͨ�����ţ�
    ��\[space]��ʾһ����ͨ�Ŀո񣨶����ǲ����ָ�����
    
------------------�����صĲ���-------------------
--mode m
    ����vpn��ģʽ��Ĭ��'p2p'
    2.0֮��İ汾����֧��'server'������ʵ��֧�ֶ�ͻ��˵ķ�����
--local host
    ����������ip�����ָ���ˣ�openvpn����ֻ�󶨸õ�ַ���������������
--remote host [port]
    Զ��������ip���ڿͻ��˿�ʹ�ö�� --remote ѡ��ָ�����࣬
    ÿ������һ����ͬ��vpn��������������ʧ���ǣ��ͳ�����һ��
    ע�⣬����udp�Ƿ��������ӵģ�������--ping��--ping-restartѡ�������ʧ��
    ע������������������ָ���˶��--remote������--user��/��--groupѡ��
    ���Ʒ�������ԱȨ�ޣ�����Ŀͻ��˳����ֲ���������Windowsϵͳ�ϣ�
    ������ͻ�����Ҫ�л�����һ����ͬ��vpn�������ϣ��Ǹ��������ַ�����
    ��ͬ��tun/tap��·�����ã���ͻ����������ȱ��Ȩ�޵����´����˳�
    ���ûָ��--remote����vpn����������ip��ַ�İ���
    ������ͨ�����������֤���ԣ����򲻻����Щ���ݰ���ȡ�ж�
    ���������֤Ҫ�������Ǳ�ڵĶԵȷ�����Լ������
    ��ʹ��������֪�ͼٶ�����IP��ַ�ĶԵȷ�����UDP���ݰ���α��ԴIP��ַ�ǳ����ף�
    ��tcpģʽ�£�--remote����Ϊһ�����������ܾ�������host��ƥ������������
    ��������Ǹ����ڽ������ip��ַ��DNS���֣�
    �����ѡ��һ�����Ӷ��ṩһ�ֻ����ĸ���ƽ��͹����л����ܡ�
--remote-random    
    ���ж��--remoteѡ��ʱ�����б��˳�������������Ĭ�ϰ�˳�򣩣���ʵ�ּ򵥵ĸ��ؾ���
--proto p    
    ʹ��Э��p��Զ��hostͨ�ţ�p������udp/tcp-client/tcp-server��Ĭ��udp
    �����tcp����һ��ָ��tcp-server����һ��ָ��tcp-client
    tcp-server���������ڵĵȴ�����tcp-client���������ӣ�
    ���ʧ�ܣ���5��󣨿�ͨ��--connect-retryѡ����ƣ���������
    tcp�ͻ��˺ͷ���˵��κ�һ�����������ӣ�����һ������SIGUSR1�ź�
    OpenVPNּ��ͨ��UDP�Ż����У����޷�ʹ��UDPʱ���ɸ���TCP
    ����upd��tcp��ӵ���Ļ򲻿��ŵ������ϲ�����Ч�ͽ�׳
    Ȼ�����ض������£�tcp�������ƣ�������������IP��Ӧ�ó���UDPЭ�飬
    ���߲��������ÿɿ��Բ���������Э�顣
--connect-retry n    
    ����ʧ�ܺ󣬵ȴ�����������ԣ�Ĭ��5��
--http-proxy server port [authfile] [auth-method]
--http-proxy-retry
--http-proxy-timeout n
--http-proxy-option type [parm]
--socks-proxy server [port]
--socks-proxy-retry
--resolv-retry n
    ���n���ڽ���--remote�����������ɹ������϶�ʧ��
    ��������nΪ"infinite"(Ĭ��)��ʹ֮һֱ����
--float
    ����Զ˱䶯��ip��/��˿ڣ�������ΪDHCP�����û��--remoteѡ���Ĭ��ʹ�øù��ܣ�
    ���--float��--remote����ʹ�ã�������һ��vpn�Ự�ڿ�ʼʱ������һ����֪�ĵ�ַ��
    ��������µ�ַ�����İ�ͨ�������е���֤�����µĵ�ַ���ӹܸûỰ
    ����Զ�ӵ��һ����̬��ַ�����粦�����ӻ�DHCP�ͻ��ˣ����������õ�
    �����ϣ�--float ����vpn��������κε�ַ�Ϸ�����ͨ����֤�İ���
    ����ֻ�Ǵ�--remote���İ�
--ipchange cmd
    ��Զ��ip��ַ�ڳ�����֤���ı��ִ��shell����cmd
    ִ�з�ʽΪ��cmd ip_address port_number
    ��Ҫ��--mode serverʱʹ�ø����ʹ��--client-connect�����
    ע��cmd����ʹ���ж��������shell�������vpn���ɵĲ����������͸�cmd
    ������������һ����̬ip��ַ�Ļ����������ʹ�øýŴ����ĶԶ˵ĵ�ַ�����༭/etc/host�ļ�
    ���Ƶģ�������ǵ�ip��Ϊdhcp���ı��ˣ�����Ӧ�������ǵ�ip�䶯�ű�����dhcpcd(8)��man������
    ������һ�� SIGHUP or SIGUSR1 �źŸ�vpn��
    Ȼ��OpenVPN�������µ�IP��ַ����������������֤�ĶԵȷ����½�������
--port port
    �ͻ���/����˶˿ںţ�2.0�汾��Ĭ��1194��֮ǰ�汾Ĭ��5000��
--lport port
    ���ض˿ں�
--rport port
    Զ�˶˿ں�
--nobind
    ��Ҫ�󶨵����ص�ַ�Ͷ˿�
    ip��ջ��ʹ��һ����̬�˿����Խ��հ�
    ���ڶ�̬�˿ڵ�ֵ���ܱ��Եȶ˿���ǰ֪����
    ��˴�ѡ��ֻ�����ڽ�ʹ�� --remote ѡ���������ӵĶԵȶ˿ڡ�
--dev tunX | tapX | null
    ����Ӧ��һ�£����ܻ���
    tun��װip��tap��װethernet 802.3
--dev-type device-type
    Ӧ����tun��tap��
    ��ѡ��ֻ��--devѡ��ָ����tun/tap�豸������tun��tap��ͷʱʹ��
--tun-ipv6
--dev-node node
--ifconfig l rn
    ��ʽ�����豸�ڵ㣬������ʹ��/dev/net/tun��/dev/tun��/dev/tap�ȡ�
    ���OpenVPN�޷���������ȷ���ڵ���tun����tap�豸��
    ��Ӧָ��-dev type tun��-dev type tap��
    ��Windowsϵͳ�ϣ�ѡ��tap-Win32��������
    ���������ڡ��������ӿ�����塱������Ϊnode��
    ���ô���������������������ԭʼGUID��
    Windows�µ�--show adaptersѡ��Ҳ������ö�����п��õ�TAP-Win32��������
    ������ʾ�������ӿ���������ƺ�ÿ��TAP-Win33��������GUID��
--ifconfig-noexec
--ifconfig-nowarn
--route network/IP [netmask] [gateway] [metric]
--route-gateway gw
--route-delay [n] [w]
--route-up cmd
--route-noexec
--redirect-gateway [local] [def1]
--link-mtu n
--tun-mtu n
--tun-mtu-extra n
--mtu-disc type
--mtu-test
--fragment max
--mssfix max
--sndbuf size
--rcvbuf size
--txqueuelen n
--shaper n
--inactive n
--ping n
--ping-exit n
--ping-restart n
--keepalive n m
--ping-timer-rem
--persist-tun
--persist-key
--persist-local-ip
--persist-remote-ip
--mlock
--up cmd
--up-delay
--down cmd
--down-pre
--up-restart
--setenv name value
--disable-occ
--user user
--group group
--cd dir
--chroot dir
--daemon [progname]
--syslog [progname]
--passtos
--inetd [wait|nowait] [progname]
--log file
--log-append file
--suppress-timestamps
--writepid file
--nice n
--fast-io
--echo [parms...]
--remap-usr1 signal
--verb n
--status file [n]
--status-version [n]
--mute n
--comp-lzo
--comp-noadapt
--management IP port [pw-file]
--management-query-passwords
--management-hold
--management-log-cache n
--plugin module-pathname [init-string]

------------------�������صĲ���-------------------










