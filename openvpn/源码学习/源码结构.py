<catalog s0/s4/s8/s12/s16/s20/s24/s28/s32 catalog_line_prefix=+>
+����ļ���
    file://add_option����.py
    file://openvpn_help.txt
    file://openvpn��context�ṹ.c+
    file://../֪ʶ��.txt
    file://openvpn��ssl�ĳ�ʼ������.c
    file://ovpnlog--����1/�ļ�����.png
    file://ovpnlog--����1/_ץ������.txt
    file://ovpnlog/_ץ������.txt
    file://ovpnЭ�̶ԳƼ�����Կ.txt
    file://ovpnԴ�����-�����.py
+wmain  
    /*
     * �ú��������������ѭ������ṹ����
     *     ÿ������һ�εĳ�ʼ��
     *     ���ѭ��������ʱ��SIGHUP��ִ�У� //file://SIGHUP�ź�.py
     *         level 1 ��ʼ��
     *         �ڲ�ѭ��������ʱ��SIGUSR1��ִ�У� //file://SIGUSR1�ź�.py
     *             ���ڿͻ���ģʽ/�����ģʽ�������¼�ѭ������
     *                 tunnel_point_to_point()  //��Ե�ģʽ
     *                 tunnel_server()   //�ͻ���-������ģʽ
     *         level 1 ����
     *     ÿ����һ�ε�����
     */
    //&<��openvpn_main�ķ���>
    +openvpn_main
        struct context c; 
        /'''init_static���
         ����������ӣ���ʼ��error��ر�����wsa��ʼ������ʼ���ź���
         ��ʼ��ʱ�䣬����ssl��Ϊ���������ע������������ʼ��α�����
         '''
        +init_static  #&<��init_static�ķ���>
            srandom�������������
            error_reset
                error.c�еķ�������ʼ���ļ�����
            reset_check_status
                 error.c�еķ�������ʼ���ļ�����
            init_win32
                win32.c�еķ�����wsa��ʼ������ʼ��ȫ�ֱ��� win32_signal��window_title
            update_time
                otime.h�еķ�������ȡʱ�䣬����ֲ����� timeval tv;
            init_ssl_lib
                ssl.c�еķ���
                    tls_init_lib
                        '''CRYPTO_get_ex_new_index(int class_index,
                            long argl, void *argp,
                            CRYPTO_EX_new *new_func,
                            CRYPTO_EX_dup *dup_func,
                            CRYPTO_EX_free *free_func);
                            #define SSL_get_ex_new_index(l, p, newf, dupf, freef) 
                             CRYPTO_get_ex_new_index(CRYPTO_EX_INDEX_SSL, l, p, newf, dupf, freef)
                            CRYPTO_get_ex_new_index �����ض��ṹ��exdata, argp�ǵ�ǰ��exdata��
                            SSL_get_ex_new_index ����Ϊ�ض���Ӧ�ó��������ע��������
                        '''
                        mydata_index = SSL_get_ex_new_index(0, "struct session *", NULL, NULL, NULL);
                    crypto_init_lib
                        �ڲ�û��ִ���κδ���
            prng_init
                crypto.c�еķ�����prng : pseudorandom number generator
        /'''SIGHUP������ѭ����һ�� ip-fail, tun-abort �����������ж�'''
        +do.while(c.sig->signal_received == SIGHUP)
            /'''windows�£��ú���ִ��Ϊ�գ�linux�������źŴ�����'''
            pre_init_signal_catch
                sig.c�ļ��еķ�����windows�£��ú���ִ��Ϊ�գ�linux�������źŴ�����
            /'''��ʼ�� context c'''
            context_clear_all_except_first_time
                ��ʼ�� context c
            /'''��ʼ���ź���Ϣ���󣨳���first_time��Ա��   &<ovpn�е��źŶ���>
                c.sig������context���������ӽṹ����Ψһ��һ�����ڼ�¼�źŵĳ�Ա
                ��ָ���siginfo_static�Ǹ��ļ����ľ�̬������sig.c�ļ��У�
                ���Ƶģ�����һ��win32_signal�������ڼ�¼����̨�����¼���
                �������ܼ�¼�źŵģ����ܾ���win32���ص��˿ڽṹ�ˣ�overlapped_io��������������
                �����Ľṹ�����У�
                context_2.(link_socket/accept_from).(reads/writes)  <-> context_2.(link_socket/accept_from).rw_handle
                context_1.tuntap.reads/writes <-> context_1.tuntap.rw_handle
                ע��context_2���и� event_set ��Ա��������¼�ȴ���� event ����
                '''
            CLEAR(siginfo_static)��c.sig = &siginfo_static;  
                siginfo_staticΪsig.h�е�ȫ�ֱ���
                struct signal_info
                {
                    volatile int signal_received;
                    volatile int source;
                    const char *signal_text;
                } siginfo_static;
            /'''�������ջ��Ƴ�ʼ��'''
            +gc_init(&c.gc)
                �Σ�file://�������ջ���.txt
            /'''��ʼ��������������'''
            +c.es = env_set_create(NULL)
                ���� struct env_set {
                    struct gc_arena *gc;
                    struct env_item *list;
                };
                struct env_item {
                    char *string;
                    struct env_item *next;
                };
                list����ռ�õ��ڴ棬ͨ��gc�����ͷ�
            Windows�£�set_win_sys_path_via_env(c.es)
                ��ȡ "SystemRoot" ����������ֵ����� c.es
            /'''��ʼ���û����ӹ�����'''
            +init_management  &<init_management>
                init.c�еķ���
                    management = management_init();  management Ϊȫ�ֱ���
                        struct management *man;
                            struct management
                            {
                                struct man_persist persist;
                                struct man_settings settings;
                                struct man_connection connection;
                            };
                            Management object, split into three components:
                            struct man_persist  : Data elements which are persistent across
                                                  man_connection open and close.
                            struct man_settings : management parameters.
                            struct man_connection : created on socket binding and listen,
                                                    deleted on socket unbind, may handle 
                                                    multiple sequential client connections.
            /'''��ʼ��������Ϣ����һЩ�������ʼֵ'''
            +init_options(&c.options, true); //��ʼ��ѡ��ΪĬ��״̬ &<��init_options�ķ���>
                struct options options;  //��¼�����к������ļ�
            /'''�������ò���'''
            +parse_argv(&c.options, argc, argv, msglevel=M_USAGE=45056,    //&<��parse_argv�ķ���>
                       permission_mask=OPT_P_DEFAULT, option_types_found=NULL, es=c.es);
                �ж����argcС��1����ʾ��ʾ��Ϣ�������˳�
                �����2����������һ�������ǳ��������ҵڶ��������� --������������ʾ
                ��ȡѡ�����--֮����ַ��������������--��ͷ������
                ��ѡ�������¼��p[0]
                ��ȡѡ�������ֱ������--��ͷ���ַ���������¼��p[1]..p[15]��ÿ���������֧��16������
                add_option(options, p, is_inline=false, char* file=NULL, line=0, level=0,
                           msglevel, permission_mask, option_types_found, es);
                    ����Σ�file://options.py
                    #�ú��������þ��Ǹ��ݲ���p����������Ϣ�浽options��
                    ���fileΪ�գ�file="[CMD-LINE]"��line=1
                    ���p[0] Ϊ "help"
                        ��ʾ������Ϣ�������˳�
                    ���p[0] Ϊ "version"
                        ��ʾ�汾��Ϣ�������˳�
                    ���p[0] Ϊ "config"
                        options->config = p[1]
                        read_config_file(options, char* file = p[1], level, char* top_file=file, 
                                         int top_line=line, msglevel, permission_mask, option_types_found, es);
                             level++;
                             FILE* fp = fopen(file,"r");
                             while ��ȡһ�е� line �ַ�����
                                char *p[MAX_PARMS+1];
                                parse_line(line, p, SIZE(p)-1, file, line_num, msglevel, &options->gc)
                                    �ú��������þ��Ƕ�ȡÿһ�����ã�Ȼ��Ѷ����Ľ���ŵ��������p��
                                add_option(options, p, lines_inline, file, line_num, level,
                                           msglevel, permission_mask, option_types_found, es);    
                    ���p[0] Ϊ "show-gateway"
                        ��ʾĬ�����أ������˳�
                    ���p[0] Ϊ "echo" �� "parameter"
                        ��ӡ���������Ϣ����־���
                    ���p[0] Ϊ "management"
                        ��������������ֱ��¼��
                        options->management_addr��
                        options->management_port��
                        options->management_user_pass
                        ����������Ϊ��ѡ��
                    ���p[0] Ϊ "management-client-user"
                        ���һ����������¼��options->management_client_user
                    ���p[0] Ϊ "management-client-group"
                        ���һ����������¼��options->management_client_group
                    ���p[0] Ϊ "management-query-passwords"
                        ���治��������Ӱ�� options->management_flags ��MF_QUERY_PASSWORDS��
                    ���p[0] Ϊ "management-query-remote"
                    ���p[0] Ϊ "management-query-proxy"
                    ���p[0] Ϊ "management-hold"
                    ���p[0] Ϊ "management-signal"
                    ���p[0] Ϊ "management-forget-disconnect"
                    ���p[0] Ϊ "management-up-down"
                    ���p[0] Ϊ "management-client"
                    ���p[0] Ϊ "management-external-key"
                    ���p[0] Ϊ "management-external-cert"
                    ���p[0] Ϊ "management-client-auth"
                    ���p[0] Ϊ "management-client-pf"
                    ���p[0] Ϊ "management-log-cache"
                    ���p[0] Ϊ "plugin"
                    ���p[0] Ϊ "mode"
                    ���p[0] Ϊ "dev"
                    ���p[0] Ϊ "dev-type"
                    ���p[0] Ϊ "windows-driver"
                    ���p[0] Ϊ "dev-node"
                    ���p[0] Ϊ "lladdr"
                    ���p[0] Ϊ "topology"
                    ���p[0] Ϊ "tun-ipv6"
                    ���p[0] Ϊ "ifconfig"
                    ���p[0] Ϊ "ifconfig-ipv6"
                    ���p[0] Ϊ "ifconfig-noexec"
                    ���p[0] Ϊ "ifconfig-nowarn"
                    ���p[0] Ϊ "local"
                    ���p[0] Ϊ "remote-random"
                    ���p[0] Ϊ "connection"
                    ���p[0] Ϊ "ignore-unknown-option"
                    ���p[0] Ϊ "ignore-unknown-option"
                    ���p[0] Ϊ "remote"
                    ���p[0] Ϊ "resolv-retry"
                    ���p[0] Ϊ "preresolve"
                    ���p[0] Ϊ "connect-retry"
                    ���p[0] Ϊ "connect-timeout"
                    ���p[0] Ϊ "connect-retry-max"
                    ���p[0] Ϊ "ipchange"
                    ���p[0] Ϊ "float"
                    ���p[0] Ϊ "gremlin"
                    ���p[0] Ϊ "chroot"
                    ���p[0] Ϊ "cd"
                    ���p[0] Ϊ "setcon"
                    ���p[0] Ϊ "writepid"
                    ���p[0] Ϊ "up"
                    ���p[0] Ϊ "down"
                    ���p[0] Ϊ "down-pre"
                    ���p[0] Ϊ "up-delay"
                    ���p[0] Ϊ "up-restart"
                    ���p[0] Ϊ "syslog"
                    ���p[0] Ϊ "daemon"
                    ���p[0] Ϊ "inetd"
                    ���p[0] Ϊ "log"
                    ���p[0] Ϊ "suppress-timestamps"
                    ���p[0] Ϊ "machine-readable-output"
                    ���p[0] Ϊ "log-append"
                    ���p[0] Ϊ "memstats"
                    ���p[0] Ϊ "mlock"
                    ���p[0] Ϊ "multihome"
                    ���p[0] Ϊ "verb"
                    ���p[0] Ϊ "mute"
                    ���p[0] Ϊ "errors-to-stderr"
                    ���p[0] Ϊ "status"
                    ���p[0] Ϊ "status-version"
                    ���p[0] Ϊ "remap-usr1"
                    ���p[0] Ϊ "link-mtu"
                    ���p[0] Ϊ "tun-mtu"
                    ���p[0] Ϊ "tun-mtu-extra"
                    ���p[0] Ϊ "mtu-dynamic"
                    ���p[0] Ϊ "fragment"
                    ���p[0] Ϊ "mtu-disc"
                    ���p[0] Ϊ "mtu-test"
                    ���p[0] Ϊ "nice"
                    ���p[0] Ϊ "rcvbuf"
                    ���p[0] Ϊ "sndbuf"
                    ���p[0] Ϊ "mark"
                    ���p[0] Ϊ "socket-flags"
                    ���p[0] Ϊ "bind-dev"
                    ���p[0] Ϊ "txqueuelen"
                    ���p[0] Ϊ "shaper"
                    ���p[0] Ϊ "port"
                    ���p[0] Ϊ "lport"
                    ���p[0] Ϊ "rport"
                    ���p[0] Ϊ "bind"
                    ���p[0] Ϊ "nobind"
                    ���p[0] Ϊ "fast-io"
                    ���p[0] Ϊ "inactive"
                    ���p[0] Ϊ "proto"
                    ���p[0] Ϊ "proto-force"
                    ���p[0] Ϊ "http-proxy"
                    ���p[0] Ϊ "http-proxy-user-pass"
                    ���p[0] Ϊ "http-proxy-retry"
                    ���p[0] Ϊ "http-proxy-timeout"
                    ���p[0] Ϊ "http-proxy-option"
                    ���p[0] Ϊ "socks-proxy"
                    ���p[0] Ϊ "keepalive"
                    ���p[0] Ϊ "ping"
                    ���p[0] Ϊ "ping-exit"
                    ���p[0] Ϊ "ping-restart"
                    ���p[0] Ϊ "ping-timer-rem"
                    ���p[0] Ϊ "explicit-exit-notify"
                    ���p[0] Ϊ "persist-tun"
                    ���p[0] Ϊ "persist-key"
                    ���p[0] Ϊ "persist-local-ip"
                    ���p[0] Ϊ "persist-remote-ip"
                    ���p[0] Ϊ "client-nat"
                    ���p[0] Ϊ "route"
                    ���p[0] Ϊ "route-ipv6"
                    ���p[0] Ϊ "max-routes"
                    ���p[0] Ϊ "route-gateway"
                    ���p[0] Ϊ "route-ipv6-gateway"
                    ���p[0] Ϊ "route-metric"
                    ���p[0] Ϊ "route-delay"
                    ���p[0] Ϊ "route-up"
                    ���p[0] Ϊ "route-pre-down"
                    ���p[0] Ϊ "route-noexec"
                    ���p[0] Ϊ "route-nopull"
                    ���p[0] Ϊ "pull-filter"
                    ���p[0] Ϊ "allow-pull-fqdn"
                    ���p[0] Ϊ "redirect-gateway"
                    ���p[0] Ϊ "redirect-gateway"
                    ���p[0] Ϊ "block-ipv6"
                    ���p[0] Ϊ "remote-random-hostname"
                    ���p[0] Ϊ "setenv"
                    ���p[0] Ϊ "setenv-safe"
                    ���p[0] Ϊ "script-security"
                    ���p[0] Ϊ "mssfix"
                    ���p[0] Ϊ "disable-occ"
                    ���p[0] Ϊ "server"
                    ���p[0] Ϊ "server-ipv6"
                    ���p[0] Ϊ "server-bridge"
                    ���p[0] Ϊ "server-bridge"
                    ���p[0] Ϊ "server-bridge"
                    ���p[0] Ϊ "push"
                    ���p[0] Ϊ "push-reset"
                    ���p[0] Ϊ "push-remove"
                    ���p[0] Ϊ "ifconfig-pool"
                    ���p[0] Ϊ "ifconfig-pool-persist"
                    ���p[0] Ϊ "ifconfig-ipv6-pool"
                    ���p[0] Ϊ "hash-size"
                    ���p[0] Ϊ "connect-freq"
                    ���p[0] Ϊ "max-clients"
                    ���p[0] Ϊ "max-routes-per-client"
                    ���p[0] Ϊ "client-cert-not-required"
                    ���p[0] Ϊ "verify-client-cert"
                    ���p[0] Ϊ "username-as-common-name"
                    ���p[0] Ϊ "auth-user-pass-optional"
                    ���p[0] Ϊ "opt-verify"
                    ���p[0] Ϊ "auth-user-pass-verify"
                    ���p[0] Ϊ "auth-gen-token"
                    ���p[0] Ϊ "auth-gen-token-secret"
                    ���p[0] Ϊ "client-connect"
                    ���p[0] Ϊ "client-disconnect"
                    ���p[0] Ϊ "learn-address"
                    ���p[0] Ϊ "tmp-dir"
                    ���p[0] Ϊ "client-config-dir"
                    ���p[0] Ϊ "ccd-exclusive"
                    ���p[0] Ϊ "bcast-buffers"
                    ���p[0] Ϊ "tcp-queue-limit"
                    ���p[0] Ϊ "port-share"
                    ���p[0] Ϊ "client-to-client"
                    ���p[0] Ϊ "duplicate-cn"
                    ���p[0] Ϊ "iroute"
                    ���p[0] Ϊ "iroute-ipv6"
                    ���p[0] Ϊ "ifconfig-push"
                    ���p[0] Ϊ "ifconfig-push-constraint"
                    ���p[0] Ϊ "ifconfig-ipv6-push"
                    ���p[0] Ϊ "disable"
                    ���p[0] Ϊ "tcp-nodelay"
                    ���p[0] Ϊ "stale-routes-check"
                    ���p[0] Ϊ "client"
                    ���p[0] Ϊ "pull"
                    ���p[0] Ϊ "push-continuation"
                    ���p[0] Ϊ "auth-user-pass"
                    ���p[0] Ϊ "auth-retry"
                    ���p[0] Ϊ "static-challenge"
                    ���p[0] Ϊ "msg-channel"
                    ���p[0] Ϊ "win-sys"
                    ���p[0] Ϊ "route-method"
                    ���p[0] Ϊ "ip-win32"
                    ���p[0] Ϊ "dhcp-option"
                    ���p[0] Ϊ "show-adapters"
                    ���p[0] Ϊ "show-net"
                    ���p[0] Ϊ "show-net-up"
                    ���p[0] Ϊ "tap-sleep"
                    ���p[0] Ϊ "dhcp-renew"
                    ���p[0] Ϊ "dhcp-pre-release"
                    ���p[0] Ϊ "dhcp-release"
                    ���p[0] Ϊ "dhcp-internal"
                    ���p[0] Ϊ "register-dns"
                    ���p[0] Ϊ "block-outside-dns"
                    ���p[0] Ϊ "rdns-internal"
                    ���p[0] Ϊ "show-valid-subnets"
                    ���p[0] Ϊ "pause-exit"
                    ���p[0] Ϊ "service"
                    ���p[0] Ϊ "allow-nonadmin"
                    ���p[0] Ϊ "user"
                    ���p[0] Ϊ "group"
                    ���p[0] Ϊ "user"
                    ���p[0] Ϊ "group"
                    ���p[0] Ϊ "dhcp-option"
                    ���p[0] Ϊ "route-method"
                    ���p[0] Ϊ "passtos"
                    ���p[0] Ϊ "allow-compression"
                    ���p[0] Ϊ "comp-lzo"
                    ���p[0] Ϊ "comp-noadapt"
                    ���p[0] Ϊ "compress"
                    ���p[0] Ϊ "show-ciphers"
                    ���p[0] Ϊ "show-digests"
                    ���p[0] Ϊ "show-engines"
                    ���p[0] Ϊ "key-direction"
                    ���p[0] Ϊ "secret"
                    ���p[0] Ϊ "genkey"
                    ���p[0] Ϊ "auth"
                    ���p[0] Ϊ "cipher"
                    ���p[0] Ϊ "data-ciphers-fallback"
                    ���p[0] Ϊ "data-ciphers"
                    ���p[0] Ϊ "ncp-ciphers"
                    ���p[0] Ϊ "ncp-disable"
                    ���p[0] Ϊ "prng"
                    ���p[0] Ϊ "no-replay"
                    ���p[0] Ϊ "replay-window"
                    ���p[0] Ϊ "mute-replay-warnings"
                    ���p[0] Ϊ "replay-persist"
                    ���p[0] Ϊ "test-crypto"
                    ���p[0] Ϊ "engine"
                    ���p[0] Ϊ "keysize"
                    ���p[0] Ϊ "use-prediction-resistance"
                    ���p[0] Ϊ "show-tls"
                    ���p[0] Ϊ "show-curves"
                    ���p[0] Ϊ "ecdh-curve"
                    ���p[0] Ϊ "tls-server"
                    ���p[0] Ϊ "tls-client"
                    ���p[0] Ϊ "ca"
                    ���p[0] Ϊ "capath"
                    ���p[0] Ϊ "dh"
                    ���p[0] Ϊ "cert"
                    ���p[0] Ϊ "enc-cert"
                    ���p[0] Ϊ "cert-bak"
                    ���p[0] Ϊ "enc-cert-bak"
                    ���p[0] Ϊ "extra-certs"
                    ���p[0] Ϊ "verify-hash"
                    ���p[0] Ϊ "cryptoapicert"
                    ���p[0] Ϊ "key"
                    ���p[0] Ϊ "enc-key"
                    ���p[0] Ϊ "key-bak"
                    ���p[0] Ϊ "enc-key-bak"
                    ���p[0] Ϊ "tls-version-min"
                    ���p[0] Ϊ "tls-version-max"
                    ���p[0] Ϊ "pkcs12"
                    ���p[0] Ϊ "askpass"
                    ���p[0] Ϊ "auth-nocache"
                    ���p[0] Ϊ "auth-token"
                    ���p[0] Ϊ "auth-token-user"
                    ���p[0] Ϊ "single-session"
                    ���p[0] Ϊ "push-peer-info"
                    ���p[0] Ϊ "tls-exit"
                    ���p[0] Ϊ "tls-cipher"
                    ���p[0] Ϊ "tls-cert-profile"
                    ���p[0] Ϊ "tls-ciphersuites"
                    ���p[0] Ϊ "tls-groups"
                    ���p[0] Ϊ "crl-verify"
                    ���p[0] Ϊ "tls-verify"
                    ���p[0] Ϊ "tls-export-cert"
                    ���p[0] Ϊ "compat-names"
                    ���p[0] Ϊ "no-name-remapping"
                    ���p[0] Ϊ "verify-x509-name"
                    ���p[0] Ϊ "ns-cert-type"
                    ���p[0] Ϊ "remote-cert-ku"
                    ���p[0] Ϊ "remote-cert-eku"
                    ���p[0] Ϊ "remote-cert-tls"
                    ���p[0] Ϊ "tls-timeout"
                    ���p[0] Ϊ "reneg-bytes"
                    ���p[0] Ϊ "reneg-pkts"
                    ���p[0] Ϊ "reneg-sec"
                    ���p[0] Ϊ "hand-window"
                    ���p[0] Ϊ "tran-window"
                    ���p[0] Ϊ "tls-auth"
                    ���p[0] Ϊ "tls-crypt"
                    ���p[0] Ϊ "tls-crypt-v2"
                    ���p[0] Ϊ "tls-crypt-v2-verify"
                    ���p[0] Ϊ "x509-track"
                    ���p[0] Ϊ "x509-username-field"
                    ���p[0] Ϊ "show-pkcs11-ids"
                    ���p[0] Ϊ "pkcs11-providers"
                    ���p[0] Ϊ "pkcs11-protected-authentication"
                    ���p[0] Ϊ "pkcs11-private-mode"
                    ���p[0] Ϊ "pkcs11-cert-private"
                    ���p[0] Ϊ "pkcs11-pin-cache"
                    ���p[0] Ϊ "pkcs11-id"
                    ���p[0] Ϊ "pkcs11-id-management"
                    ���p[0] Ϊ "rmtun"
                    ���p[0] Ϊ "mktun"
                    ���p[0] Ϊ "peer-id"
                    ���p[0] Ϊ "keying-material-exporter"
                    ���p[0] Ϊ "allow-recursive-routing"
                    ���p[0] Ϊ "vlan-tagging"
                    ���p[0] Ϊ "vlan-accept"
                    ���p[0] Ϊ "vlan-pvid"
            /'''���֧��'''
            ��������� ENABLE_PLUGIN
                init_verb_mute  //������ϸ�̶Ⱥ;�������  
                    set_check_status(D_LINK_ERRORS, D_READ_WRITE);
                    set_debug_level(c->options.verbosity, SDL_CONSTRAIN);
                    set_mute_cutoff(c->options.mute);
                    ����������error.c�еĺ���
                    c->c2.log_rw = (check_debug_level(D_LOG_RW) && !check_debug_level(D_LOG_RW + 1));
                    �����Ƿ���շ��İ���ӡ���������ﲻ��ӡ
                init_plugins(&c);
                    ��� c->option.plugins_list ��Ϊ�գ���plugin��������ƣ�����Ϊ�գ�����û��ִ�У�
                        c->plugins = plugin_list_init(c->options.plugin_list);
                            struct plugin_list
                            {
                                struct plugin_per_client per_client;
                                struct plugin_common *common;
                                bool common_owned;
                            };
                            struct plugin_common
                            {
                                int n;
                                struct plugin plugins[MAX_PLUGINS];
                            };
                            struct plugin {
                                bool initialized;
                                const char *so_pathname;
                                unsigned int plugin_type_mask;
                                int requested_initialization_point;
                                #ifndef _WIN32
                                void *handle;
                                #else
                                HMODULE module;
                                #endif
                                openvpn_plugin_open_v1 open1;
                                openvpn_plugin_open_v2 open2;
                                openvpn_plugin_open_v3 open3;
                                openvpn_plugin_func_v1 func1;
                                openvpn_plugin_func_v2 func2;
                                openvpn_plugin_func_v3 func3;
                                openvpn_plugin_close_v1 close;
                                openvpn_plugin_abort_v1 abort;
                                openvpn_plugin_client_constructor_v1 client_constructor;
                                openvpn_plugin_client_destructor_v1 client_destructor;
                                openvpn_plugin_min_version_required_v1 min_version_required;
                                openvpn_plugin_select_initialization_point_v1 initialization_point;
                                openvpn_plugin_handle_t plugin_handle;
                            };
                        c->plugins_owned = true;
                open_plugins(&c, bool import_options=true, int init_point=OPENVPN_PLUGIN_INIT_PRE_CONFIG_PARSE);
                    if (c->plugins && c->plugins_owned)
                        �������ԣ�����ʱ����������������û��ִ�У�
            /'''��ʵ�֣�����0'''
            net_ctx_init(&c, &c.net_ctx);  
                networking.h�еĺ���
            /'''��ʼ����־�������ϸ�̶�'''
            +init_verb_mute(&c, IVM_LEVEL_1);   &<init_verb_mute:1>
            /'''���� options->dev '''
            +init_options_dev(&c.options);
                if (!options->dev && options->dev_node)  //dev��������ƣ������ļ���ָ���� dev tun
                    ���������--dev-node�������û������--dev��ʱ������������
                    ���� options->dev_node ��ֵ��basename������ options->dev
            /'''��ӡssl�����Ϣ'''
            +print_openssl_info(&c.options)
                ���� c.options �е������� show_ciphers��show_digests��show_engines��show_tls_ciphers��show_curves
                ������ʾ��ͬ����Ϣ�����ݵ�ǰ�����ã�����ʲôҲû�У�
            /'''openvpn ������Կ����'''
            +do_genkey(&c.options)
                if (options->mlock && options->genkey)
                    �ֱ��� mlock �� genkey ��������ƣ����ݵ�ǰ���ã��������߾�Ϊfalse
                ��������д��룬���ǻ��� genkey ����Ϊ��ģ�
                ���ݵ�ǰ���ã���Щ�������ִ�У���������false
            ������溯��ִ�гɹ��������˳�
            /'''tuntap����'''
            +do_persist_tuntap(&c.options, &c.net_ctx)
                if (options->persist_config) //���ݵ�ǰ���ã�Ϊfalse
                    ��������� ENABLE_FEATURE_TUN_PERSIST  //��ǰû�ж���
                        tuncfg(...)
                            tun.c�еĺ���
                        set_lladdr(...)
                            lladdr.c�еĺ���
                        return true;
                    ����
                        ���������ʾ��return false
            ������溯��ִ�гɹ��������˳�
            +options_postprocess(&c.options);  //��ѡ��ĺ��� &<��options_postprocess�ķ���>
                /'''��Ҫ������ routes��push_list��ncp_ciphers��connection_list �ȳ�Ա'''
                options_postprocess_mutate(options);  //�������ñ䶯
                    #helper_xxx : �Ը����������չ������
                    /''' �ͻ���/����� ·���������
                     ��Ϊ����ˣ�������Ϊ TOP_NET30 �� TOP_P2P����todo)
                     ��Ϊ�ͻ��ˣ����� o->pull = true; o->pull = true;
                     '''
                    helper_client_server(o);
                        ��Ϊ�ͻ���/�����ʱ����������������Ƿ���ȷ��������������������д���
                        �����
                            if(dev == DEV_TYPE_TUN)  //���ݵ�ǰ���ã�dev==DEV_TYPE_TUN
                                //��زο���file://openvpn��������.py
                                if (topology == TOP_NET30 || topology == TOP_P2P) //���ݵ�ǰ���ã�topology==TOP_NET30
                                    helper_add_route(o->server_network, o->server_netmask, o)
                                        add_route_to_option_list��o->routes,network,netmask,0,0)
                                        ' route_option_list *routes;
                                    push_option(o, print_opt_route(o->server_network + 1, 0, &o->gc), M_USAGE);
                                        ���ݲ����������ַ�������֯Ϊ push_entry �ṹ������ o->push_list ��
                                        push "route 10.8.0.1"
                                push_option(o, print_opt_topology(topology, &o->gc), M_USAGE);
                                    push "topology net30"
                            else if (dev == DEV_TYPE_TAP)    
                        �ͻ���
                            o->pull = true;   //���ƴӷ������ȡ������
                            o->tls_client = true;
                    /'''�����ʱ��push pingʱ����'''
                    helper_keepalive(o);  //���� keepalive ������
                        ���� o->ping_rec_timeout_action��o->ping_send_timeout��o->ping_rec_timeout
                        ��� o->mode == MODE_SERVER
                            push "ping 10"
                            push "ping-restart 60"
                    /'''��Ϊ����ˣ��Ұ��� SF_TCP_NODELAY_HELPER ����ʱ����ǰ�����㣩��ߴ���Ч��'''
                    helper_tcp_nodelay(o);  // ���� tcp-nodelay ������
                        ��� o->server_flags ���� SF_TCP_NODELAY_HELPER �����ݵ�ǰ���ã��������������server_flags==0��
                            o->sockflags |= SF_TCP_NODELAY;
                            if (o->mode == MODE_SERVER)
                                push "socket-flags TCP_NODELAY"
                                    TCP_NODELAYѡ�������������Ƿ���Nagle�㷨��
                                    ���㷨��Ϊ����߽����Ĺ���������Ч��
                    /'''�� ciphername="SMS4-CBC" ��ӵ� o->ncp_ciphers ��; o->enable_ncp_fallback = true;'''
                    options_postprocess_cipher(o);
                        if (!o->pull && !(o->mode == MODE_SERVER))  //o->pull:���ƴӶԶ˽�������ѡ����ݵ�ǰ���ã���ֵΪfalse
                            ��Ϊ��SERVERʱ���Ż�ִ�и�������������
                            o->ncp_enabled = false
                            if (!o->ciphername) o->ciphername = "BF-CBC";
                            return
                        if (!o->ciphername)  //���ݵ�ǰ���ã�ciphername="SMS4-CBC"
                            ��ִ��
                        else if (!o->enable_ncp_fallback && !tls_item_in_cipher_list(o->ciphername, o->ncp_ciphers))  //����
                            o->enable_ncp_fallback = true;
                            �� ciphername="SMS4-CBC" ��ӵ� o->ncp_ciphers ��
                    /'''winϵͳ����Ϊ server ʱ��options->tuntap_options.tap_sleep = 10; options->route_delay_defined = false;'''
                    options_postprocess_mutate_invariant(o);  //mutate : ʹ�任��ʹ�ı䣬 invariant�������
                        ��������� _WIN32
                            if (options->mode == MODE_SERVER)
                                options->tuntap_options.tap_sleep = 10;
                                options->route_delay_defined = false;
                    /'''o->ncp_ciphers ���˵�libcrypto�ⲻ֧�ֵ��㷨 '''
                    if (o->ncp_enabled)  //true ,  NCP: �������Э�� Network Control Protocol
                        ncpЭ����
                            ���磬���һ���û�Ҫ���Ž���·���������û��Ļ���һ�㲻֪��Ҫʹ���ĸ�IP��ַ��
                            ��˱���ͨ��NCP/IPCPЭ�̴�·�������һ����ַ
                        o->ncp_ciphers = mutate_ncp_cipher_list(o->ncp_ciphers, &o->gc);
                            ���˵�libcrypto���в�֧�ֵ��㷨��������ֿⲻ֧�ֵ��㷨�ͷ��ؿգ�
                        ��� o->ncp_ciphers Ϊ�գ���ʾ���ڲ�֧�ֵ� ciphers ��  ciphers���ܳ��ȳ���127�ֽ�
                    /'''��remote_listתΪconnection_list'''
                    if (o->remote_list && !o->connection_list) //�ͻ���ʱ����
                    else if (!o->remote_list && !o->connection_list)  
                        struct connection_entry *ace = alloc_connection_entry(o, M_USAGE);
                            struct connection_list *l = alloc_connection_list_if_undef(options);
                                if (options->connection_list == null)
                                    ���� struct connection_list �ṹ���ŵ� options->connection_list �У����� options->connection_list
                            struct connection_entry *e = ���� struct connection_entry
                            �� e �ŵ� l->array[] ��
                            ���� e
                        *ace = o->ce  // o->ce ���ڳ�ʼ����ʱ��Σ�������õ�
                    /'''����connection_list������������Ϣ���޸�/����һЩ��Աֵ��
                        if(o->persist_key) Ԥ���� tls_auth_file��tls_crypt_file��tls_crypt_v2_file'''
                    for i in o->connection_list->len
                        options_postprocess_mutate_ce(o, o->connection_list->array[i]);
                            if (o->server_defined || o->server_bridge_defined || o->server_bridge_proxy_dhcp) // server_definedΪtrue
                                if (ce->proto == PROTO_TCP)  
                                    ce->proto = PROTO_TCP_SERVER;
                            ������ ����ce������/�޸�һЩ��Աֵ��
                            if (o->persist_key)
                                connection_entry_preload_key(&ce->tls_auth_file, &ce->tls_auth_file_inline, &o->gc);
                                connection_entry_preload_key(&ce->tls_crypt_file, &ce->tls_crypt_file_inline, &o->gc);
                                connection_entry_preload_key(&ce->tls_crypt_v2_file, &ce->tls_crypt_v2_file_inline, &o->gc);
                                    #connection_entry_preload_key(const char **key_file, bool *key_inline,struct gc_arena *gc)
                                    if (key_file && *key_file && !(*key_inline))
                                        ���������㣨*key_fileΪ�գ�����ִ��
                    /'''����o->dh_file = NULL'''
                    if (o->tls_server)
                         if (o->dh_file == "none")  //true
                            o->dh_file = NULL
                    /'''ûִ��'''
                    if (o->http_proxy_override)  //false
                        options_postprocess_http_proxy_override(o);
                     /'''ûִ��'''
                     pre_pull_save(o);
                        if (o->pull)  //false
                            ...
                /'''����������'''
                options_postprocess_verify(options);
                    if (o->connection_list)
                        for i in o->connection_list->len  //len=1
                            options_postprocess_verify_ce(o, o->connection_list->array[i]);
                                ��� options->dev �Ƿ�Ϊ�ǿ� ��="tun"��
                                ���ce�ӳ�Ա��option�ӳ�Ա�ȣ�����÷����ԣ�������ʾ��Ϣ
                /'''����������'''
                options_postprocess_filechecks(options);
                    check_file_access_inline(bool is_inline, const int type, const char *file, const int mode, const char *opt)
                        if (is_inline)  return false;
                        return check_file_access(type, file, mode, opt);
                            if file==null ,return false
                            if type & CHKACC_ACPTSTDIN �� file=="stdin", return false
                            if (type & CHKACC_DIRPATH)  //����ļ���
                                ��ȡ��Ŀ¼������Ƿ����modeָ����Ȩ�ޣ�û���򷵻�true�������д�
                            if (type & CHKACC_FILE )
                                ���file�Ƿ���ָ����Ȩ�ޣ�û���򷵻�true
                            if (type & CHKACC_FILEXSTWR)
                                ����ļ��Ƿ�����Ҿ���ЩȨ�ޣ����ڵ�û��дȨ�ޣ�����true
                            if (type & CHKACC_PRIVATE)  //���˽���ļ��Ƿ�ᱻ���������Ա���������Ա����
                                ����Ƿ��ܻ�ȡ�ļ���Ϣ��ʧ�ܣ����ļ������ڣ����򷵻�true
                    check_file_access_chroot(const char *chroot, const int type, const char *file, const int mode, const char *opt)
                        if file==null ,return false
                        if (chroot)  // If chroot is set, look for the file/directory inside the chroot
                            �� file ǰ������� file
                        return check_file_access(type, file, mode, opt);
                    �ܽ᣺
                        �ú������ options�µ� dh_file��ca_path��extra_certs_file��pkcs12_file��chroot_dir��
                        tls_auth_file��tls_crypt_file��tls_crypt_v2_file��shared_secret_file�������Ƿ����ָ����Ȩ��
            /'''��ʾ������Ϣ'''
            +show_settings(&c.options);
                �������õĵ�����Ϣ�Ǽǣ�������ʾ������Ϣ
            /'''��ʾWindows�汾��Ϣ'''
            +show_windows_version(M_INFO);
                �������õĵ�����Ϣ�Ǽǣ�������ʾWindows�汾��Ϣ
            /'''��ʾssl��汾��Ϣ'''
            +show_library_versions(M_INFO);
                �������õĵ�����Ϣ�Ǽǣ�������ʾssl��汾��Ϣ
            /'''windows�£��Կ���̨�������ã����ӿ���̨�����¼�'''
            +pre_setup(const struct options *options)
                ��������� _WIN32          
                    win32_signal_open(&win32_signal,
                                      int force=WSO_FORCE_CONSOLE,
                                      const char *exit_event_name=NULL,
                                      bool exit_event_initial_state=false);
                        �������ÿ���̨ģʽ����ֹ����
                        �������ĳ���ʧ���ˣ�������һ������
                        ���ÿ���̨��Ϣ�����Ӻ���Ϊ��win_ctrl_handler������ctrl+c��break�¼�
                    ���Ϊ����̨�����ÿ���̨����
            /'''�ڼ�����ϵͳ�������ز���'''
            +do_test_crypto(struct options *o= &c.options)
                 if (o->test_crypto)  // false
                    struct context c;
                    c.options = *o;
                    test_crypto_thread((void *) &c);
                        init_verb_mute(c, IVM_LEVEL_1);
                        context_init_1(c);
                        next_connection_entry(c);
                        do_init_crypto_static(c, 0);
                        frame_finalize_options(c, options);
                        test_crypto(&c->c2.crypto_options, &c->c2.frame);
                        key_schedule_free(&c->c1.ks, true);
                        packet_id_free(&c->c2.crypto_options.packet_id);
                �����˳�
            /'''�������ʹ�����ӹ���������ͨ�����ӹ�������ȡ�û������룬����������ȡ�û�������'''
            ��� (c.options.management_flags & MF_QUERY_PASSWORDS),
                �����ͨ������ӿڻ�����룬���ѯ���룬���ݵ�ǰ���ã�����ִ������
                init_query_passwords(&c);
                    if (c->options.key_pass_file)  //����������
                        pem_password_setup(c->options.key_pass_file);
                    if (c->options.auth_user_pass_file)   //����������
                        auth_user_pass_setup(c->options.auth_user_pass_file, &c->options.sc_info);
            /'''�ǵ�һ��ѭ��ʱ��������idд�뱾���ļ�'''
            if (c.first_time)  //true
                c.did_we_daemonize = possibly_become_daemon(&c.options)  //�������Ӧ�ó�Ϊ�ػ�������
                    if (options->daemon)  //����������
                        ������
                    else
                        return false
                write_pid_file(const char *filename=c.options.writepid,    //Write our PID to a file
                               const char *chroot_dir=c.options.chroot_dir);
                    if(filename)  //����������
                        ��ȡpid��д�� filename �ļ���
                    if (!chroot_dir)  //����������
                        saved_pid_file_name = strdup(filename)  //saved_pid_file_nameΪ�ļ�ȫ�ֱ���
            /'''�����ӹ�����ϵͳ'''
            +open_management(&c)   //&<��open_management�ķ���>
                if (management)   //management Ϊ�ļ�ȫ�ֱ�����init_management��ǰ���Ѿ�ִ�й�
                    if (c->options.management_addr)  //����������
                        ������
                    else
                        close_management();
                            if (management)
                                management_close(management);
                                    man_output_list_push_finalize(man)
                                        management_connected(man)
                                            ��� man->connection.state == MS_CC_WAIT_READ
                                            ��   man->connection.state == MS_CC_WAIT_WRITE
                                        �����һ������Ϊ��  // ����������
                                            man_update_io_state(man);
                                            if (!man->persist.standalone_disabled)
                                                int signal_received = 0;
                                                man_output_standalone(man, &signal_received);
                                    man_connection_close(man)
                                        struct man_connection *mc = &man->connection;
                                        if (mc->es)  //����������
                                            event_free(mc->es);
                                        ��������� _WIN32
                                            net_event_win32_close(ne=&mc->ne32);
                                                if (ne->handle->read != null)  //����������
                                                    close_net_event_win32(&ne->handle, ne->sd, 0);
                                                net_event_win32_init(ne);
                                                    CLEAR(*ne)
                                                    ne->sd = SOCKET_UNDEFINED;
                                        if( mc->sd_top != SOCKET_UNDEFINED )  //����������
                                            man_close_socket(man, mc->sd_top);
                                        if( mc->sd_cli != SOCKET_UNDEFINED ) //����������
                                            man_close_socket(man, mc->sd_cli);
                                        if (mc->in)  //����������
                                            command_line_free(mc->in);
                                        if (mc->out)  //����������
                                            buffer_list_free(mc->out);
                                        in_extra_reset(mc=&man->connection, mode=IER_RESET);
                                            if(mc)  //��������
                                                 if (mode != IER_NEW)   //��������
                                                    mc->in_extra_cmd = IEC_UNDEF;
                                                    mc->in_extra_cid = 0;
                                                    mc->in_extra_kid = 0;
                                                 if (mc->in_extra)  //����������
                                                    buffer_list_free(mc->in_extra);
                                                    mc->in_extra = NULL;
                                                if (mode == IER_NEW)    //����������
                                                    mc->in_extra = buffer_list_new(0);
                                        buffer_list_free(mc->ext_key_input);
                                        man_connection_clear(mc);
                                    man_settings_close(ms=&man->settings)
                                        free(ms->write_peer_info_file);
                                        CLEAR(*ms);
                                    man_persist_close(mp=&man->persist);
                                        if (mp->log)  //��������
                                            msg_set_virtual_output(NULL);
                                                x_msg_virtual_output = NULL  //x_msg_virtual_outputΪerror.c�е�ȫ�ֱ���
                                            log_history_close(mp->log);  //�ͷ�����ڴ�
                                        if (mp->echo)
                                            log_history_close(mp->echo);  //�ͷ�����ڴ�
                                        if (mp->state)
                                            log_history_close(mp->state);  //�ͷ�����ڴ�
                                        CLEAR(*mp);
                                    free(man);
                                management = NULL;
                return true
            /'''�ȴ����ӹ�������'''
            if (c.options.management_flags & MF_QUERY_PASSWORDS)  //��������˭
                //�����Ҫ����ͨ����������ѯ����
                init_query_passwords(&c);
            /'''��ĳЩѡ������Ϊ��������'''
            +setenv_settings(c.es, &c.options) 
            /'''��Ҫ����� c->c1������ c->c1 �� ciphername��authname��authname�� pkcs11��ʼ�������� c->options.connection_list'''
            +context_init_1(&c)  //&<��main��context_init_1�ķ���>
                /'''��� context �� c1 '''
                context_clear_1(c);
                    CLEAR(c->c1);
                /''' c->c1->fd = -1 '''
                packet_id_persist_init(p=&c->c1.pid_persist);
                    ��p�ĳ�Ա��ʼ��Ϊ��
                /'''��������� remote_random������� connection_list ��˳��'''
                init_connection_list(c);
                    if (c->options.remote_random)  //����������
                        len = c->options.connection_list->len
                        foreach i  < len  //���ܣ����� l->array
                            j = rand() % len
                            if (i!=j)
                                l->array[i] �� l->array[j] ���ཻ��
                /'''�� c->options �� ciphername��authname��authname ����� c->c1 '''
                save_ncp_options(c);
                    c->c1.ciphername = c->options.ciphername;
                    c->c1.authname = c->options.authname;
                    c->c1.keysize = c->options.keysize;
                /'''pkcs11�������豸�ӿڣ���Ҫ��Ӧ�������ܿ���HSM����ʼ��'''
                if (c->first_time) //true
                    pkcs11_initialize(protected_auth=true, nPINCachePeriod=c->options.pkcs11_pin_cache_period=-1);
                    foreach c->options.pkcs11_providers[i]  //������Ϊ�գ�����������
                        pkcs11_addProvider(...)
            /'''��SIGUSR1������ѭ����һ������ͨ�Ź��ϻ����������ź�'''
            +do.while(c.sig->signal_received == SIGUSR1)
                /'''�ͻ���/��������ͨ�ţ�tunnel_point_to_point �� tunnel_server_udp �ڲ����Ǹ�ѭ�������������˳�'''
                +switch(c.options.mode)  // = 1
                     /'''����ͻ��˵�ͨ�Ź��̣��ú������и�ѭ��'''
                     +case MODE_POINT_TO_POINT:
                        tunnel_point_to_point(&c);   //�Σ�@��tunnel_point_to_point�ķ���
                     /'''�������˵�ͨ�Ź��̣��ú������и�ѭ��'''
                     +case MODE_SERVER:
                        tunnel_server(top=&c);
                            if (proto_is_udp(top->options.ce.proto))
                                tunnel_server_udp(top);
                            else
                                tunnel_server_tcp(top);  //@tunnel_server_tcp
                +c.first_time = false;   //����Χ�ڵĵ�һ�ε���
                /'''������ͨ������Ϊ�յ��źŶ��˳������ӡ�ź�����'''
                +if(c->sig->signal_received)
                    print_signal(c.sig, NULL, M_INFO);
                /'''�������źŴ��ݸ�������ϵͳ���������ӹ�����ϵͳ��'''
                +signal_restart_status(c.sig);
===========================================================================================================
 
// Top level event loop for single-threaded operation.                        
+&<��main�е�tunnel_server_tcp�ķ���>
.void tunnel_server_tcp(struct context *top) 
    top->mode = CM_TOP
    context_clear_2(top);
         CLEAR(c->c2);
    init_instance_handle_signals(top, top->es, CC_HARD_USR1_TO_HUP);  //initialize top-tunnel instance
        pre_init_signal_catch();
            ���û���� _WIN32
                �����źŴ�����
        init_instance(c, env, flags);  //@init_instance
        post_init_signal_catch();
        if(c->sig->signal_received)
            remap_signal(c);
            uninit_management_callback();
            
===========================================================================================================
+&<��init_instance�ķ���>
//��ʼ��һ�����ʵ��
/void init_instance(struct context *c, const struct env_set *env, const unsigned int flags)    //&init_instance     
    gc_init(&c->c2.gc);
    if (env) //����
        c->c2.es->list ������µ� struct env_item����¼������ env->list->string  
            env->list->string �а������б�
            remote_port_1=1194
            local_port_1=1194
            proto_1=tcp-server
            daemon_pid=18016
            daemon_start_time=1677048399
            daemon_log_redirect=1
            daemon=0
            verb=3
            config=D:/Program Files/OpenVPN/config/server_ok.ovpn
            SystemRoot=C:\\Windows
    c->sig->signal_received = 0;
    c->sig->signal_text = NULL;
    c->sig->source = SIG_SOURCE_SOFT;
    if (c->mode == CM_P2P)  //�����㣬c->mode Ϊ CM_TOP
        init_management_callback_p2p(c);
    if (c->mode == CM_P2P || c->mode == CM_TOP)  //����
        do_startup_pause(c);
            if (!c->first_time) //������
                socket_restart_pause(c);
            else
                do_hold(holdtime=0);
                    if (management)  //������
                        management_hold(management, holdtime)  //����ֱ��������ͣ���ͷ�
        if( c->sig->signal_received )  //������
            goto sig
    if (c->options.resolve_in_advance)  //������
        do_preresolve(c);
        if( c->sig->signal_received )  //������
            goto sig
    next_connection_entry(c);
        ...(û��ִ�У��ԣ�
        update_options_ce_post(&c->options)
            ...(û��ִ�У��ԣ�
    if (c->options.ce.proto == PROTO_TCP_SERVER)  //����
        if (c->mode == CM_TOP)  //����
            link_socket_mode = LS_MODE_TCP_LISTEN;
        else if (c->mode == CM_CHILD_TCP){
            link_socket_mode = LS_MODE_TCP_ACCEPT_FROM;
    if (c->first_time && options->mlock)  //������
        platform_mlockall(true);
    if (auth_retry_get() == AR_INTERACT)   //������
        init_query_passwords(c);
     init_verb_mute(c, IVM_LEVEL_2);
        if (flags & IVM_LEVEL_1)
            /* ������ϸ�̶Ⱥ;������� */
            set_check_status(D_LINK_ERRORS, D_READ_WRITE);
            set_debug_level(c->options.verbosity, SDL_CONSTRAIN);
            set_mute_cutoff(c->options.mute);
        if (flags & IVM_LEVEL_2) /* ����� D_LOG_RW ģʽ */
            c->c2.log_rw = (check_debug_level(D_LOG_RW) && !check_debug_level(D_LOG_RW + 1));
    if (c->mode == CM_P2P)  //������
        set_check_status_error_delay(P2P_ERROR_DELAY_MS);
    if (c->mode == CM_P2P || c->mode == CM_TOP)  //���㣬 ���治һ�µ�ѡ�� 
        do_option_warnings(c);  //��� c->options ��������������Ϣ
    if (c->mode == CM_P2P || c->mode == CM_TOP)  //����
        open_plugins(c, false, OPENVPN_PLUGIN_INIT_PRE_DAEMON);
            if (c->plugins && c->plugins_owned)  //������
                ������������
    if (c->mode == CM_P2P || c->mode == CM_TOP)
        do_setup_fast_io(c);
            ���ÿ���io��ֻ���������������㣬�ſ���
                ƽ̨����Windows
                --proto udp ������
                --shaper ������
            if (c->options.fast_io)  //������
    do_signal_on_tls_errors(c);  //����Ӧ���� TLS �����Ϸ����ź���
        if (c->options.tls_exit) //������
             c->c2.tls_exit_signal = SIGTERM;
         else
             c->c2.tls_exit_signal = SIGUSR1;
    if (c->mode == CM_P2P || c->mode == CM_TOP)   //����
        do_open_status_output(c);  //�򿪺͹ر� --status �ļ�
            if (!c->c1.status_output)  //����
                 c->c1.status_output = status_open(filename=c->options.status_file,
                                                   refresh_freq=c->options.status_file_update_freq,
                                                   msglevel=-1, vout=NULL, flags=STATUS_OUTPUT_WRITE);
                    if (filename || msglevel >= 0 || vout)  //������
                        ������
                    else
                        return NULL
                c->c1.status_output_owned = true;
    if (c->mode == CM_TOP)  //����
        do_open_ifconfig_pool_persist(c);   //���� ifconfig-pool �־û�����
            if (!c->c1.ifconfig_pool_persist && c->options.ifconfig_pool_persist_filename)  //����
                 c->c1.ifconfig_pool_persist = ifconfig_pool_persist_init(
                                                     filename=c->options.ifconfig_pool_persist_filename,
                                                     refresh_freq=c->options.ifconfig_pool_persist_refresh_freq);
                    struct ifconfig_pool_persist *ret;
                    if (refresh_freq > 0)  //����
                        ret->fixed = false;
                        ret->file = status_open(filename="ipp.txt", refresh_freq=600, msglevel=-1,  //"ipp.txt"�������ļ���д��
                                                vout=NULL, flags=STATUS_OUTPUT_READ|STATUS_OUTPUT_WRITE);
                             if (filename || msglevel >= 0 || vout)  //��������
                                struct status_output *so = NULL;
                                so->flags = flags
                                so->msglevel = msglevel;
                                so->vout = vout;
                                so->fd = platform_open(filename, O_CREAT | O_RDWR, S_IRUSR | S_IWUSR);
                                so->filename = filename
                                set_cloexec(int fd=so->fd)
                                    set_cloexec_action(fd)
                                        ���û���� _WIN32
                                            fcntl(fd, F_SETFD, FD_CLOEXEC)
                                if (so->flags & STATUS_OUTPUT_READ)  //����
                                    so->read_buf = alloc_buf(512);
                                so->et->defined = true
                                et->n = refresh_freq
                                et->last = 0
                    return ret
                 c->c1.ifconfig_pool_persist_owned = true;
    if (c->mode == CM_P2P || child)  //������
        c->c2.occ_op = occ_reset_op();
    if (c->mode == CM_P2P)  //������
        do_event_set_init(c, SHAPER_DEFINED(&c->options));
    else if (c->mode == CM_CHILD_TCP)   //������
        do_event_set_init(c, false);
    init_proxy(c);  //�������򼶱� 2 ��ʼ�� HTTP �� SOCKS �������
        init_proxy_dowork(c);
            uninit_proxy_dowork(c);
                ����Ĵ���û��ִ�е�
            if (c->options.ce.http_proxy_options)   //������
                c->c1.http_proxy = http_proxy_new(c->options.ce.http_proxy_options);
                if (c->c1.http_proxy)  //����http
                    c->c1.http_proxy_owned = true;
            if (!did_http && c->options.ce.socks_proxy_server)  //������ 
                c->c1.socks_proxy = socks_proxy_new(c->options.ce.socks_proxy_server,
                                                    c->options.ce.socks_proxy_port,
                                                    c->options.ce.socks_proxy_authfile);
                if (c->c1.socks_proxy)  //����socket
                    c->c1.socks_proxy_owned = true;
    if (c->mode == CM_P2P || c->mode == CM_TOP || c->mode == CM_CHILD_TCP)  //���㣬�������ǵ��׽��ֶ���
        do_link_socket_new(c);
            c->c2.link_socket = link_socket_new();
                ����һ�� struct link_socket �ṹ
            c->c2.link_socket_owned = true;
    if (options->ce.fragment && (c->mode == CM_P2P || child))   //�����㣬��ʼ���ڲ���Ƭ����
    ��ʼ�����ܲ�
        unsigned int crypto_flags = 0;
        if (c->mode == CM_TOP)  //����
            crypto_flags = CF_INIT_TLS_AUTH_STANDALONE;
        else if (c->mode == CM_P2P)
            crypto_flags = CF_LOAD_PERSISTED_PACKET_ID | CF_INIT_TLS_MULTI;
        else if (child)
            crypto_flags = CF_INIT_TLS_MULTI;
        do_init_crypto(c, crypto_flags);
            if (c->options.shared_secret_file)
                do_init_crypto_static(c, flags);
            else if (c->options.tls_server || c->options.tls_client)  //����
                do_init_crypto_tls(c, flags);
                    init_crypto_pre(c, flags);
                        if (c->options.engine)  //������
                            ������
                        if (flags & CF_LOAD_PERSISTED_PACKET_ID)  //������
                            ������
                    '''
                       ���ȫ���õ�c1.ks.ssl_ctx�ĳ�ʼ��
                       ��ɶԳƼ����õ�c1.ks.key_type�ĳ�ʼ��
                       ���α������ĳ�ʼ��
                       ���ʹ����֤�������ݣ�tls-auth��ʱ�õ�c1.ks.tls_auth_key_type�ĳ�ʼ��
                       ���ʹ��tls���ּ��ܣ�tls-crypt��ʱ�õ�c1.ks.tls_wrap_key�ĳ�ʼ��
                       '''
                    do_init_crypto_tls_c1(c);   // ��ʼ���־û����
                        if( c->c1.ks.ssl_ctx->ctx == null ) //���㣬tls_ctx_initialised
                            init_ssl(options, new_ctx=&(c->c1.ks.ssl_ctx),   //��ʼ��ssl tcx�������ļ�����pem��ʽ
                                     bool in_chroot=c->c0 && c->c0->uid_gid_chroot_set);
                                if (options->tls_server)   //����
                                    tls_ctx_server_new(ctx=new_ctx);
                                        ctx->ctx = SSL_CTX_new(SSLv23_server_method());
                                    if (options->dh_file)   //������
                                        tls_ctx_load_dh_params(new_ctx, options->dh_file,
                                                               options->dh_file_inline);
                                else
                                    tls_ctx_client_new(new_ctx);
                                tls_ctx_set_cert_profile(new_ctx, options->tls_cert_profile);  
                                    //�������ssl.c:622, 2023��2��22��
                                    if (profile) ��ӡ��ʾ��Ϣ
                                tls_ctx_restrict_ciphers(new_ctx, options->cipher_list);
                                tls_ctx_restrict_ciphers_tls13(new_ctx, options->cipher_list_tls13);
            else
                do_init_crypto_none(c);
        if (IS_SIG(c) && !child)
            goto sig;
       
&<�ļ���openvpn��context�ṹ>       
+file://openvpn��context�ṹ.c+

&<�ļ���֪ʶ��>
file://֪ʶ��.txt

'''�ͻ�ģʽ�µ�vpn���¼�ѭ����ֻ��һ��vnp����Ǽ����'''
&<��tunnel_point_to_point�ķ���>
+tunnel_point_to_point  //�ͻ���ģʽ��ѭ��
    '''���c->c2'''
    context_clear_2(c)
    '''���ö˵���ģʽ'''
    c->mode = CM_P2P;
    '''��ʼ�����ʵ��������֮ǰ��֮����źż���'''
    +init_instance_handle_signals(c, c->es, CC_HARD_USR1_TO_HUP);
        +pre_init_signal_catch
            window��ʲôҲûִ��
        '''��ʼ�����ʵ����飺
            ��c->c2.es �̳� env
            Ϊ���ӹ�����ϵͳ����������ˣ����ûص�����
            �ƻ�����ͣ
            ������Ϊ����ģʽ����ǰ���ǣ������ٴβ�ѯ�û�������
            Ԥ�ȶ��������н��������������㣩
            c->options.ce = c->options.connection_list[++i]
            ���治һ�µ�ѡ��
            ��ʼ�����
            ����tls����ʱ���ǲ���SIGUSR1�źţ��̣������ǲ���SIGTERM�ź�
            ��--statusָ�����ļ�
            ��--ifconfig-pool-persistָ�����ļ�
            ����occ��OpenVPN Configuration Control��״̬
            ��ʼ��event�¼���(���ڵȴ�io)
            ��ʼ��http��socks������level2�����������ڣ�
            Ϊc->c2.link_socket�������
            ��ʼ����Ƭ����ûִ�У�
            ��ʼ��ѹ���⣬ûִ��
            ��ʼ�����ܲ㣬��Ҫ�漰 c->c1.ks.ssl_ctx��c->c1.ks.key_type��c->c2.tls_multi
            ��ʼ��ѹ���⣬ûִ��
            ��ʼ��MTU��ر���
            ��ʼ��������c->c2.buffers
            ��ʼ��tcp/udp socket �� ��Ҫ������ c->c2.link_socket �ĸ���Աֵ
            ��ʼ��tun/tap�豸����û��ִ�У������豸��ifconfig��ִ��up�ű����ȵ�
            ���ݱ��غ�Զ��ͨ�����ѡ�תΪ�ַ��������������ø� c->c2.tls_multi->opt
            ��ʼ������ٶ����ƣ�û��ִ��
            �򿪲�� OPENVPN_PLUGIN_INIT_POST_DAEMON��û��ִ��
            ���ó�ʼ����ʱ�䶨ʱ��
            ���TCP/UDP socket�����ղ���
            ��ʼ�����ֶ�ʱ��
            �򿪲�� OPENVPN_PLUGIN_INIT_POST_UID_CHANGE��û��ִ��
            '''
        +init_instance  //Initialize a tunnel instance.
            '''��c->c2.es �̳� env'''
            +do_inherit_env(c, env);
            '''Ϊ���ӹ�����ϵͳ����������ˣ����ûص�����'''
            if (c->mode == CM_P2P)   //true
                init_management_callback_p2p
                    if (management)  //����������
            '''�ƻ�����ͣ��������״�ѭ������ֻ�����������ӹ�����ʱ����ͣ���ȴ��ͻ������ӣ�
               ���򣨲��ǵ�һ��ѭ����������������ӹ���������ͣ�⣬
               û���������ӹ�����ʱ��Ҳ����ͣһ��ʱ�䣨�ſ����´ε����ӣ�
               '''
            if (c->mode == CM_P2P || c->mode == CM_TOP)  //true
                do_startup_pause(c);
                    if (!c->first_time)
                        '''�����ӷ����ʧ�ܣ�SIGUSR1�źŵ��µġ����������ȴ�һ��ʱ����ٳ�������'''
                        socket_restart_pause(c);
                            �ͻ��˵ȴ�5�룬 ��������е� connection_list �϶����Թ�4���ˣ����ǵ�5���ˣ�����û���������ӣ�
                            �������ӵȴ�ʱ����ÿ�����ӵ�ʱ��Ϊ�� sec <<= min(����ʧ�ܴ���-4,15)
                            sec = min(sec,c->options.ce.connect_retry_seconds_max)  = 300
                            ������������ӹ�����ϵͳ�������ϵͳ���֣�֪�������߷���release ��
                            ���� sleep��sec��
                    else
                        do_hold(0);   //�״�ִ������
                            if (management)  //����������
            '''Ԥ�ȶ��������н��������������㣩'''
            if (c->options.resolve_in_advance)   //����������
                do_preresolve(c);
            '''c->options.ce = c->options.connection_list[++i], c->options.unsuccessful_attempts++ '''
            +next_connection_entry(c);
                if(c->c1.link_socket_addr.current_remote && ���������һ����Ϊ��)
                    �� c->c1.link_socket_addr.current_remote ָ���������һ��
                else 
                    if ( persist_remote_ip Ϊ�٣� #����ʹ�ù̶���Զ�˵�ַ
                        clear_remote_addrlist(&c->c1.link_socket_addr, !c->options.resolve_in_advance);
                    else
                        c->c1.link_socket_addr.current_remote = c->c1.link_socket_addr.remote_list;
                    c->options.unsuccessful_attempts++;
                c->options.ce = *c->options.connection_list->array[i++]
                '''�����������Ӵ������ƣ����ڴﵽ���ƴ������˳�����'''
                if (c->options.connect_retry_max > 0)
                    ��������п��õ�Զ�̵�ַ�Ϸֱ��Թ� connect_retry_max �κ�û�ɹ������� M_FATAL �źţ�exit(1)��
                '''����pingʱ��'''
                update_options_ce_post(&c->options);
            '''�������Ϊ����ģʽ����ǰ���ǣ������ٴβ�ѯ�û�������
               ����ζ�ţ��������Ϊ����ģʽ��������������ӷ����ʧ�ܣ�
               �´����ӷ����ǰ��Ҳ����Ҫ����
               '''
            if (auth_retry_get() == AR_INTERACT)
                init_query_passwords(c);
            '''���� c->c2.log_rw ������'''
            +init_verb_mute(c, IVM_LEVEL_2);  
                ��������SIGHUPѭ����Ҳ���ù��������õ��� IVM_LEVEL_1, 
                �� @init_verb_mute:1
                ���� c->c2.log_rw ������
            '''�ͻ��ˣ����ô����ӳ٣���Ӧ�Լ��̵�ʱ���ڳ���һ�����Ĵ��󣩣�������Ϊ0'''
            set_check_status_error_delay(P2P_ERROR_DELAY_MS);  //0
                x_cs_err_delay_ms = P2P_ERROR_DELAY_MS = 0��ms��
            '''���治һ�µ�ѡ��'''
            do_option_warnings(c);
            '''��ʼ����������������ʹ�ò����'''
            open_plugins(c, false, OPENVPN_PLUGIN_INIT_PRE_DAEMON);
            '''����fast io'''
            do_setup_fast_io(c);
            '''����tls����ʱ���ǲ���SIGUSR1�źţ��̣������ǲ���SIGTERM�ź�'''
            do_signal_on_tls_errors(c);
                c->c2.tls_exit_signal = SIGUSR1;
            '''��--statusָ�����ļ�'''
            do_open_status_output(c);
            '''��--ifconfig-pool-persistָ�����ļ�'''
            do_open_ifconfig_pool_persist(c);
            '''����occ��OpenVPN Configuration Control��״̬'''
            c->c2.occ_op = -1
            '''��ʼ��event�¼���(���ڵȴ�io)'''
            do_event_set_init
            '''��ʼ��http��socks������level2�����������ڣ�'''
            init_proxy(c);
                �������ã���ʼ��c->c1.http_proxy��c->c1.socks_proxy
            '''Ϊc->c2.link_socket�������'''
            +do_link_socket_new(c);
            '''��ʼ����Ƭ����ûִ�У�'''
            if (options->ce.fragmen) //0
                c->c2.fragment = fragment_init(&c->c2.frame)
            '''��ʼ�����ܲ㣬��Ҫ�漰 c->c1.ks.ssl_ctx��c->c1.ks.key_type��c->c2.tls_multi '''
            +do_init_crypto(struct context *c, const unsigned int flags)
                ����� CM_TOP ģʽ����ǰ����flags = CF_LOAD_PERSISTED_PACKET_ID | CF_INIT_TLS_MULTI
                '''��ʼ�� c->c1 �е�ssl�����������㷨����ϣ�㷨�� ��ʼ�� c->c2.tls_multi ��
                   ��ʼ�� c->c1.ks.ssl_ctx����������tls��������������㷨������֤�飬����˽Կ�ļ�
                   Ϊ c->c1.ks.key_type ���ü��ܺ͹�ϣ�㷨
                   c->c2.tls_multi = tls_multi_init(&to)  //tls_options to;
                   '''
                +do_init_crypto_tls(c, flags);
                    '''���������㣬ûִ��'''
                    +init_crypto_pre
                        '''����Ӳ�����棨vpn����ʹ��Ӳ������ʱ��ִ�У�'''
                        if (c->options.engine)  //Ϊ�գ�������
                            crypto_init_lib_engine(c->options.engine);
                        '''���ļ��м��س־ü�¼�� packet_id (time and id) ����һ�Σ�, ������ state Ϊ��'''
                        if (c->options.packet_id_file)  //Ϊ�գ�������
                            packet_id_persist_load(&c->c1.pid_persist, c->options.packet_id_file);
                    '''��ʼ���������:
                       ��ʼ�� c->c1.ks.ssl_ctx����������tls��������������㷨������֤�飬����˽Կ�ļ�
                       Ϊ c->c1.ks.key_type ���ü��ܺ͹�ϣ�㷨��ksΪ key_schedule �ṹ��������¼��Կ������Ϣ��
                       Ϊα���������nonce(�ļ�ȫ�ֱ��� nonce_data���ĳ�ʼֵΪ���ֵ 
                       '''
                    +do_init_crypto_tls_c1
                        ���&c->c1.ks.ssl_ctxû�г�ʼ����
                            '''Initialize the OpenSSL library��s global SSL context'''
                            init_ssl(options, new_ctx = &(c->c1.ks.ssl_ctx), c->c0 && c->c0->uid_gid_chroot_set)
                                tls_ctx_client_new(new_ctx);
                                tls_ctx_set_cert_profile(new_ctx, options->tls_cert_profile);
                                tls_ctx_restrict_ciphers(new_ctx, options->cipher_list);
                                tls_ctx_set_options(new_ctx, options->ssl_flags)
                                tls_ctx_load_cert_file(new_ctx, options->cert_file, options->cert_file_inline);
                                tls_ctx_load_priv_file(new_ctx, options->priv_key_file, options->priv_key_file_inline)
                                tls_ctx_load_ca(new_ctx, options->ca_file, options->ca_file_inline, 
                                                options->ca_path, options->tls_server);
                            '''��ü��ܺ͹�ϣ�㷨'''
                            init_key_type(kt=&c->c1.ks.key_type, options->ciphername, options->authname, 
                                          options->keysize, true, warn);
                                kt->cipher = cipher_kt_get(ciphername);  //AES-256-CBC
                                    return cipher = EVP_get_cipherbyname(ciphername);
                                kt->digest = md_kt_get(authname);    //SHA1
                                    return md = EVP_get_digestbyname(digest);
                            '''ʹ��������ָ����ժҪ�㷨��ʼ��α�������'''
                            prng_init(options->prng_hash, options->prng_nonce_secret_len);
                                prng_reset_nonce(void)
                                    rand_bytes(nonce_data, size)
                            '''��ʼ�� tls-auth/crypt/crypt-v2 ���õ�key��ûִ��'''
                            do_init_tls_wrap_key(c);    /* initialize tls-auth/crypt/crypt-v2 key */
                                if (options->ce.tls_auth_file)  //Ϊ��
                                if (options->ce.tls_crypt_file)  //Ϊ��
                                if (options->ce.tls_crypt_v2_file)  //Ϊ��
                                �������������£��������� c->c1.ks �µ����ֵ /* tunnel session keys */
                            '''��ʼ��auth-token����Կ�����ģ�ûִ��'''
                            do_init_auth_token_key
                                ���auth_token_generate������Ϊ��  //false
                                    auth_token_init_secret
                                        ���������ļ���auth_token_secret_file���� c->c1.ks.auth_token_key
                    '''����c->c1.ks.key_type.cipher���ж�ʹ�ó�Ψһ��ʶ��(64λ)���Ƕ�Ψһ��ʶ��(32Ϊ)'''
                    packet_id_long_form = cipher_kt_mode_ofb_cfb(c->c1.ks.key_type.cipher);  
                    ....
                    struct tls_options to;
                    to.*** = ***
                        to.crypto_flags &= ~(CO_PACKET_ID_LONG_FORM);
                        to.ssl_ctx = c->c1.ks.ssl_ctx;
                        to.key_type = c->c1.ks.key_type;
                        to.server = options->tls_server;
                        to.replay = options->replay;
                        to.replay_window = options->replay_window;
                        to.replay_time = options->replay_time;
                        to.tcp_mode = link_socket_proto_connection_oriented(options->ce.proto);
                        to.config_ciphername = c->c1.ciphername;
                        to.config_ncp_ciphers = options->ncp_ciphers;
                        to.ncp_enabled = options->ncp_enabled;
                        to.transition_window = options->transition_window;
                        to.handshake_window = options->handshake_window;
                        to.packet_timeout = options->tls_timeout;
                        to.renegotiate_bytes = options->renegotiate_bytes;
                        to.renegotiate_packets = options->renegotiate_packets;
                        to.renegotiate_seconds = options->renegotiate_seconds - ...;  #Ĭ��renegotiate_seconds=3600
                        to.single_session = options->single_session;
                        to.mode = options->mode;
                        to.pull = options->pull;
                        to.push_peer_info_detail = 1;
                        to.disable_occ = !options->occ;
                        to.verify_command = options->tls_verify;
                        to.verify_export_cert = options->tls_export_cert;
                        to.verify_x509_type = (options->verify_x509_type & 0xff);
                        to.verify_x509_name = options->verify_x509_name;
                        to.crl_file = options->crl_file;
                        to.crl_file_inline = options->crl_file_inline;
                        to.ssl_flags = options->ssl_flags;
                        to.ns_cert_type = options->ns_cert_type;
                        memmove(to.remote_cert_ku, options->remote_cert_ku, sizeof(to.remote_cert_ku));
                        to.remote_cert_eku = options->remote_cert_eku;
                        to.verify_hash = options->verify_hash;
                        to.verify_hash_algo = options->verify_hash_algo;
                        to.x509_username_field = X509_USERNAME_FIELD_DEFAULT;
                        to.es = c->c2.es;
                        to.net_ctx = &c->net_ctx;
                        to.gremlin = c->options.gremlin;
                        to.plugins = c->plugins;
                        to.mda_context = &c->c2.mda_context;
                        to.auth_user_pass_verify_script = options->auth_user_pass_verify_script;
                        to.auth_user_pass_verify_script_via_file = options->auth_user_pass_verify_script_via_file;
                        to.tmp_dir = options->tmp_dir;
                        to.client_config_dir_exclusive = options->client_config_dir;
                        to.auth_user_pass_file = options->auth_user_pass_file;
                        to.auth_token_generate = options->auth_token_generate;
                        to.auth_token_lifetime = options->auth_token_lifetime;
                        to.auth_token_call_auth = options->auth_token_call_auth;
                        to.auth_token_key = c->c1.ks.auth_token_key;
                        to.x509_track = options->x509_track;
                        ...
                        '''c->c2.tls_multi = tls_multi_init(&to);'''
                        if (flags & CF_INIT_TLS_MULTI)  //����
                            c->c2.tls_multi = tls_multi_init(&to);
                                struct tls_multi *ret;
                                ret = new tls_multi
                                ret->opt = *to;
                                '''TM_ACTIVE=0 TM_UNTRUSTED=1 TM_LAME_DUCK=2, TM��tls multi'''
                                '''ͨ��һ�����vpn�Ự�����3��tls_session����
                                   һ��tls��֤���ĻỰ���ڶ������ڴ��������¿ͻ�����������
                                   ����ɹ�ͨ����֤���ÿͻ���ȡ����ǰ�Ự��
                                   ���������� "�˽� "Կ�׵Ĵ���⣬�Ա����Ự���������ã�
                                   �� "�˽� "Կ���ڹ���ǰ����ʣ��ʱ�䡣 
                                   �˽�Կ�����ڱ�������ͨ�����ӵ������ԣ�ͬʱ����Э��һ���µ�Կ��
                                   �����ϣ�ÿ��һ��ʱ�䣬OpenVPN�ͻ��������ɻỰ��Կ������Э�����ӡ�
                                   �˽�ѼԿ�ײ����Ǵ�������Կ������Э�̵���Կ����
                                   "lame duck" key����������ͳ��ͨ���������ģ�
                                   ָ������ѡ����ʧ�ܻ����ڽ��������ڼ�������̨ǰ���м������ڵ���ͳ��
                                   ��Ŀ����ʵ�ִӾ���Ȩ������Ȩ��ƽ�����ι��ɡ�
                                   OpenVPN��������Э��һ������Կ���ڴ˹����У�
                                   �ɵġ����ڵ���Կ�����Ϊ���˽�Ѽ����Կ���������¾���Կ֮��ƽ���ص���
                                   �Ա��޷�ع��ɵ�����Կ��û����������ӳٻ�ʧ��
                                   ��ˣ���ɱ�����˽�ѼԿ�ס�����ȫ�޺��ģ�������ζ�������Ѿ�����
                                   '''
                                '''KS_PRIMARY=0 KS_LAME_DUCK=1, KS=key state'''
                                ret->key_scan[0] = &ret->session[TM_ACTIVE].key[KS_PRIMARY];
                                ret->key_scan[1] = &ret->session[TM_ACTIVE].key[KS_LAME_DUCK];
                                ret->key_scan[2] = &ret->session[TM_LAME_DUCK].key[KS_LAME_DUCK];
                                ret->use_peer_id = false;
                                return ret;
                     if (flags & CF_INIT_TLS_AUTH_STANDALONE)   //������
                        c->c2.tls_auth_standalone = tls_auth_standalone_init(&to, &c->c2.gc);
            '''��ʼ��ѹ���⣬ûִ��'''
            ���options->comp�е�ѹ���㷨����  //false
                c->c2.comp_context = comp_init(&options->comp);
            '''��ʼ��MTU��ر�������Ҫ������ c->c2.frame.extra_frame ��ֵ��
               ���� do_init_crypto Ҳ�޸��˸�ֵ��c->c2.frame ������ͨ���õ�'''
            do_init_frame(c);
                ����ѹ��������--tun-mtu-extra�����socket�������ֽڶ���
                �����أ��������� c->c2.frame.extra_frame ��ֵ
            '''��ʼ��TLS MTU��ر�����c->c2.frame��c->c2.multi->session[]���ص㣩��'''
            +do_init_frame_tls(c);  //file://do_init_frame_tls.png
                +do_init_finalize_tls_frame(c)
                    '''��tls_multi�Ľ��ܣ�
                       ʹ����TLS��vpn�������һ��tls_multi����
                       �ö����д������п���ͨ��������ͨ���İ�ȫ����
                       �ýṹ���԰������(����ͬʱ���ڻ״̬��)tls_context����
                       �Ӷ������ڻỰ����Э��ʱ���жϵ�ת��
                       ÿ��tls_context��ʾһ������ͨ��
                       �����Կ�Խkey_state�ṹ�еĶ������ͨ���ĻỰ��ȫ����
                       �Σ�<file://openvpn��context�ṹ.c+>'''
                    +tls_multi_init_finalize(multi=c->c2.tls_multi, frame=&c->c2.frame)
                        '''��������ͨ����֡������c->c2.frame����ʼ������ͨ����֡������c->c2.multi->opt.frame��'''
                        +tls_init_control_channel_frame_parameters(data_channel_frame = c->c2.frame, 
                                                                  frame = &c->c2.multi->opt.frame)
                            frame->link_mtu �� frame->extra_link �̳� data_channel_frame �е�ֵ
                            ���� frame->extra_frame�����Ӵ�С
                            frame->link_mtu_dynamic ����ֵ
                        '''��ʼ�� c->c2.multi->session[] : @tls_session
                           c->c2.multi->session[]->opt = multi->opt
                           c->c2.multi->session[]->session_id = ���ֵ
                           c->c2.multi->session[]->initial_opcode = 
                           c->c2.multi->session[]->tls_wrap = multi->opt->tls_wrap
                           c->c2.multi->session[]->tls_wrap.opt.packet_id->rec ����Ա��ʼ�� :
                               ע��session->tls_wrap.opt �� crypto_options �ṹ�����ڼ�¼ͨ���õİ�ȫ����
                               crypto_options.packet_id �� packet_id �ṹ�����ڼ�¼����(send)�İ���id��ʱ��
                               �ͽ��յİ�(rec)��id��ʱ�䡢naee��seq_backtrack��time_backtrack�ȵ�
                           c->c2.multi->session[]->key[KS_PRIMARY] ����Ա��ʼ�� :
                               c->c2.multi->session[]->key[KS_PRIMARY]->ks_ssl ��key_state_ssl�ṹ������Ա��ʼ��
                                   Ϊ����Ա��������Ӧ�ṹ
                                   ���� ssl ��ԱΪ����״̬������ˣ�������״̬���ͻ��ˣ�
                                   �� ct_in �� ct_in ���ø� ssl�� ���� ssl_bio ���� ssl
                                   struct key_state_ssl 
                                        SSL *ssl;                   /* SSL object -- new obj created for each new key */
                                        BIO *ssl_bio;               /* read/write plaintext from here */
                                        BIO *ct_in;                 /* write ciphertext to here */
                                        BIO *ct_out;                /* read ciphertext from here */
                               c->c2.multi->session[]->key[KS_PRIMARY] ��������Ա����ֵ��������Ӧ�ṹ :
                                   ks->initial_opcode��session->initial_opcode��ks->state��ks->key_id
                                   ks->send_reliable��ks->rec_reliable��ks->rec_ack
                                   ks->plaintext_read_buf��ks->plaintext_write_buf
                                   ks->ack_write_buf��ks->send_reliable��ks->rec_reliable
                                   ks->crypto_options.packet_id->rec
                           '''
                        +tls_session_init(multi = c->c2.multi, session = &c->c2.multi->session[TM_ACTIVE=0])
                        +tls_session_init(multi = c->c2.multi, session = &c->c2.multi->session[TM_UNTRUSTED=1]
                            '''c->c2.multi->session[]->optָ�����multi->opt'''
                            c->c2.multi->session[]->optָ�����multi->opt
                            '''c->c2.multi->session[]->session_id�������ֵ'''
                            c->c2.multi->session[]->session_id�������ֵ
                            '''����c->c2.multi->session[]->initial_opcode'''
                            if (session->opt->server)
                                session->initial_opcode = 
                            else
                                session->initial_opcode = 
                            '''��ʼ������ͨ���������֤������tls_wrap�������ڣ�����ͨ���������֤�İ���������'''
                            session->tls_wrap = multi->opt->tls_wrap;
                            session->tls_wrap.work = alloc_buf(session->opt->frame)
                            '''����multi->opt������ c->c2.multi->session[]->tls_wrap.opt.packet_id->rec(���յİ�) �ĸ���Աֵ
                               ע��session->tls_wrap.opt �� crypto_options �ṹ�����ڼ�¼ͨ���õİ�ȫ����
                               crypto_options.packet_id �� packet_id �ṹ�����ڼ�¼����(send)�İ���id��ʱ��
                               �ͽ��յİ�(rec)��id��ʱ�䡢naee��seq_backtrack��time_backtrack�ȵ�'''
                            +packet_id_init
                                session->tls_wrap.opt.packet_id->rec.name = "TLS_WRAP"
                                session->tls_wrap.opt.packet_id->rec.unit = session->key_id
                                if(session->opt->replay_window)
                                    session->tls_wrap.opt.packet_id->rec.seq_list =
                                                                alloc(sizeof(seq_list) * multi->opt->replay_window)
                                    session->tls_wrap.opt.packet_id->rec.seq_backtrack = multi->opt->replay_window;
                                    session->tls_wrap.opt.packet_id->rec.time_backtrack = multi->opt->replay_time
                            '''c->c2.multi->session[]->key[KS_PRIMARY] ��@key_state �ṹ���и���Ա�ĳ�ʼ�� ��
                               c->c2.multi->session[]->key[KS_PRIMARY]->ks_ssl ��key_state_ssl�ṹ������Ա��ʼ��
                                   Ϊ����Ա��������Ӧ�ṹ
                                   ���� ssl ��ԱΪ����״̬������ˣ�������״̬���ͻ��ˣ�
                                   �� ct_in �� ct_in ���ø� ssl�� ���� ssl_bio ���� ssl
                                   ע : struct key_state_ssl 
                                            SSL *ssl;                   /* SSL object -- new obj created for each new key */
                                            BIO *ssl_bio;               /* read/write plaintext from here */
                                            BIO *ct_in;                 /* write ciphertext to here */
                                            BIO *ct_out;                /* read ciphertext from here */
                               c->c2.multi->session[]->key[KS_PRIMARY] ��������Ա����ֵ��������Ӧ�ṹ :
                                   ks->initial_opcode��session->initial_opcode��ks->state��ks->key_id
                                   ks->send_reliable��ks->rec_reliable��ks->rec_ack
                                   ks->plaintext_read_buf��ks->plaintext_write_buf
                                   ks->ack_write_buf��ks->send_reliable��ks->rec_reliable
                                   ks->crypto_options.packet_id->rec
                               '''
                            +key_state_init(tls_session* session, key_state* ks=&session->key[KS_PRIMARY])  &<key_state_init>
                                '''����tls����--����ͨ��BIO��д�ڴ��е�ciphertext'''
                                key_state_ssl_init(key_state_ssl *ks_ssl = &session->key[KS_PRIMARY]->ks_ssl, 
                                                   tls_root_ctx *ssl_ctx = &session->opt->ssl_ctx, 
                                                   bool is_server = session->opt->server,
                                                   tls_session *session)
                                    ks_ssl = c->c2.multi->session[]->key[KS_PRIMARY]->ks_ssl
                                    ssl_ctx = c->c2.multi->session[]->opt->ssl_ctx
                                    CLEAR(*ks_ssl);
                                    ks_ssl->ssl = SSL_new(ssl_ctx->ctx)
                                    '''��sessionָ����ssl���󣬴Ӷ�������֤�ص��з�����'''
                                    SSL_set_ex_data(ks_ssl->ssl, mydata_index, session);
                                        ks_ssl->ssl->ex_data[mydata_index] = session
                                    '''BIO_f_ssl() returns the SSL BIO method'''
                                    ks_ssl->ssl_bio = BIO_new(BIO_f_ssl())  //ssl bio,���ڶ�д��ͨ�ļ�
                                    ks_ssl->ct_in = BIO_new(BIO_s_mem())    //�ڴ�bio������д�����ı�
                                    ks_ssl->ct_out = BIO_new(BIO_s_mem())   //�ڴ�bio�����ڶ������ı�
                                    '''����ssl������client״̬��
                                       ��Ӧ�ģ�SSL_set_accept_state����ssl�����ڷ�����״̬'''
                                    SSL_set_connect_state(ks_ssl->ssl);
                                    '''����ssl���������������д
                                       ��OpenSSL��Ҫ��Զ�̲��ȡ����ʱ��ʹ�õ�һ����
                                       ����OpenSSL��Ҫ�����ݷ��͵�Զ�̲�ʱ����ʹ�õڶ�������
                                       '''
                                    SSL_set_bio(ks_ssl->ssl, ks_ssl->ct_in, ks_ssl->ct_out);
                                    '''BIO_set_ssl(b,ssl,c)����b�ڲ���SSLָ��ָ��ssl
                                       ��ʹ�ùرձ��c'''
                                    BIO_set_ssl(ks_ssl->ssl_bio, ks_ssl->ssl, BIO_NOCLOSE);
                                '''���ÿ���ͨ���ĳ�ʼ��ģʽ''' 
                                ���� ks->initial_opcode��session->initial_opcode��ks->state��ks->key_id
                                '''allocate key source material object'''
                                ��ʼ�� ks->send_reliable��ks->rec_reliable��ks->rec_ack
                                '''����buffer����ʼ��'''
                                ��ʼ�� ks->plaintext_read_buf��ks->plaintext_write_buf��
                                       ks->ack_write_buf��ks->send_reliable��ks->rec_reliable
                                if (session->opt->replay)  //��
                                    packet_id_init
                                        ks->crypto_options.packet_id->rec.name = "SSL"
                                        ks->crypto_options.packet_id->rec.unit = ks->key_id
                                        ks->crypto_options.packet_id->rec.seq_backtrack = multi->opt->replay_window
                                        ks->crypto_options.packet_id->rec.time_backtrack = multi->opt->replay_time
            '''��ʼ��������c->c2.buffers'''
            +do_init_buffers(c);
                c->c2.buffers = init_context_buffers(&c->c2.frame);
                    struct context_buffers *b;
                    Ϊb�ĸ���Ա������Ӧ�Ľṹ :
                        b = new context_buffers;
                        b->read_link_buf  = alloc_buf(BUF_SIZE(frame));
                        b->read_tun_buf   = alloc_buf(BUF_SIZE(frame));
                        b->aux_buf        = alloc_buf(BUF_SIZE(frame));
                        b->encrypt_buf    = alloc_buf(BUF_SIZE(frame));
                        b->decrypt_buf    = alloc_buf(BUF_SIZE(frame));
                        b->compress_buf   = alloc_buf(BUF_SIZE(frame));
                        b->decompress_buf = alloc_buf(BUF_SIZE(frame));
                    return b
            '''ʹ����֪��frame��С����ʼ���ڲ��ķ�Ƭ������fragmentation capability��'''
            if(options->ce.fragment)  //false
                do_init_fragment
            '''��ʼ����̬MTU����(max trans unit)'''
            +frame_init_mssfix(&c->c2.frame, &c->options);
                if (options->ce.mssfix)
                    '''��̬����tun��MTU'''
                    frame_set_mtu_dynamic(frame, options->ce.mssfix=1450, SET_MTU_UPPER_BOUND);
            '''��ʼ��tcp/udp socket �� ��Ҫ������ c->c2.link_socket �ĸ���Աֵ'''
            +do_init_socket_1(c, link_socket_mode=LS_MODE_DEFAULT=0); //file://do_init_socket_1.png 
                '''link_socket��ʼ���׶�1 �� ��Ҫ������ c->c2.link_socket �ĸ���Աֵ'''
                +link_socket_init_phase1(sock=c->c2.link_socket, ......)
                    ���ݲ���������ֵ������sock�ĸ���Ա :
                            mode,           //�����Ϊ����˼����������������磬������Ϊ�ͻ�������
                            c->plugins,
                            c->options.ce.af,
                            c->options.ce.proto,
                            c->options.ce.local,
                            c->options.ce.remote,
                            c->options.ce.bind_local,
                            c->options.ce.local_port,
                            c->options.ce.remote_port,
                            c->options.ce.remote_float,
                            c->options.ce.bind_ipv6_only,
                            c->options.ce.mtu_discover_type,
                            c->options.mark,
                            c->options.inetd,
                            c->options.rcvbuf,
                            c->options.sndbuf,
                            c->options.gremlin,
                            c->options.ipchange,
                            c->options.bind_dev,
                            c->options.resolve_retry_seconds,
                            c->c2.accept_from,
                            c->c2.server_poll_interval,
                            c->c1.dns_cache,
                            c->c1.http_proxy,
                            c->c1.socks_proxy,
                            c->c1.link_socket_addr
                    if (sock->bind_local)  //false
                        resolve_bind_local(sock, sock->info.af);
                    '''��ȡԶ�˵� addrinfo, ��� sock->info.lsa->remote_list �� sock->info.lsa->current_remote'''
                    +resolve_remote(sock, 1, NULL, NULL); 
                        '''���δ���壬����remote��ַ :
                           struct addrinfo *ai = getaddrinfo(...)
                           sock->info.lsa->remote_list = ai;
                           sock->info.lsa->current_remote = ai;
                           '''
                        if (!sock->info.lsa->remote_list)  //����
                            if (sock->remote_host)  //"192.168.4.143"
                                struct addrinfo *ai;
                                ������
                                '''�ɹ�����0��ʧ�ܷ���-1����ͬgetaddrinfo'''
                                state = get_cached_dns_entry( sock->dns_cache,
                                                              sock->remote_host,
                                                              sock->remote_port,
                                                              sock->info.af,
                                                              flags, &ai);
                                    ���� sock->dns_cache��������ҵ������ 2,3,4 ƥ�����Ŀ��
                                    �򽫸���Ŀ�� addrinfo ��Ա��ֵ�����һ������ ai
                                    ʧ�ܷ��� -1
                                if(state != 0)  //����
                                    '''ת��ipv4��ipv6��ַ��������Ϊ struct addrinfo
                                       ���ʧ�ܣ����ڲ���ָ����n�������'''
                                    status = openvpn_getaddrinfo(flags, sock->remote_host, sock->remote_port,
                                                                 retry, signal_received, sock->info.af, &ai);
                                        �ڲ������� getaddrinfo ����
                                if(status == 0) //����
                                    sock->info.lsa->remote_list = ai;
                                    sock->info.lsa->current_remote = ai;
                        '''������Ҫ����֮ǰ��Ч��remote address��'''
                        ��� &sock->info.lsa->actual ������  //������
                            ...
                        esel
                            ��� sock->info.lsa->actual
                            if (sock->info.lsa->current_remote)  //����
                                set_actual_address(&sock->info.lsa->actual,
                                                   sock->info.lsa->current_remote);
                                    actual->dest.addr.in4 = *(ai->ai_addr)
            '''��ʼ��tun/tap�豸����û��ִ�У������豸��ifconfig��ִ��up�ű����ȵ�'''
            #options->pull Ϊ�棬����������, �� helper_client_server �б�����Ϊ��
            if ( options->up_delayΪ�� �� options->pullΪ�� �� 
                 (c->mode == CM_P2P �� c->mode == CM_TOP) )  
                c->c2.did_open_tun = do_open_tun(c);
            c->c2.frame_initial = c->c2.frame;
            '''���ݱ��غ�Զ��ͨ�����ѡ�תΪ�ַ��������������ø�
               c->c2.tls_multi->opt.local_options = c->c2.options_string_local = options_string() ��
               c->c2.tls_multi->opt.remote_options = c->c2.options_string_remote = options_string()
               '''
            +do_compute_occ_strings
                '''����ѡ���ַ�������������ͨ������ѡ����ַ������˱���һ��
                   keysize������read_key()���
                   �����ѡ��������֮�����ƥ�䣺
                   tunѡ�
                    * --dev tun|tap [unit number need not match]
                    * --dev-type tun|tap
                    * --link-mtu
                    * --udp-mtu
                    * --tun-mtu
                    * --proto udp
                    * --proto tcp-client [matched with --proto tcp-server
                                          on the other end of the connection]
                    * --proto tcp-server [matched with --proto tcp-client on
                                          the other end of the connection]
                    * --tun-ipv6
                    * --ifconfig x y [matched with --ifconfig y x on
                                      the other end of the connection]
                    * --comp-lzo
                    * --compress alg
                    * --fragment
                   ����ѡ�
                    * --cipher
                    * --auth
                    * --keysize
                    * --secret
                    * --no-replay
                   SSLѡ�
                    * --tls-auth
                    * --tls-client [matched with --tls-server on
                                    the other end of the connection]
                    * --tls-server [matched with --tls-client on
                                    the other end of the connection] '''
                char * options_string(const struct options *o, const struct frame *frame,
                                      struct tuntap *tt, openvpn_net_ctx_t *ctx,
                                      bool remote, struct gc_arena *gc)
                c->c2.options_string_local = options_string(o=&c->options, frame=&c->c2.frame, 
                                                            tt=c->c1.tuntap, ctx=&c->net_ctx,
                                                            remote=false, gc=&gc);
                    struct buffer out = alloc_buf(255)
                    out += "V4"
                    '''���ѡ��'''
                    out += "dev-type tun"
                    '''link-mut��ʾ�Ƿ��и��̶���cipher(p2p)
                       ���и������ھɵķ�tcp�ͻ��˵�fallback cipher
                       ���������������¸澯�����Ի��Ƿ�����'''
                    out += "link-mtu 1557"
                    out += "tun-mtu 1500"
                    out += "proto UDPv4"
                    '''���Ի�ȡifconfig������options�ַ��������ttû���壬��������ʱ��'''
                    if (!tt)  //����
                        tt = init_tun(o->dev,...)
                             struct tuntap *tt = �����ڴ�ṹ
                             tt->type = 2  //"tun"
                             tt->topology = 1
                             if (ifconfig_local_parm && ifconfig_remote_netmask_parm) //������
                                ������
                             if (ifconfig_ipv6_local_parm && ifconfig_ipv6_remote_parm)   //������
                             if (es)  //������
                                ������
                             return tt
                        bool tt_local = true
                    if (tt && p2p_nopull)  //������
                        ������
                    if(tt_local)
                        free tt;
                        tt = NULL;
                    '''key����'''
                    out += "keydir 1"
                    '''����ѡ��'''
                    �����tls�ͻ��˻�tls�����  //��������
                        struct key_type kt
                        init_key_type(kt=&kt, ciphername=o->ciphername, authname=o->authname, 
                                      keysize=o->keysize, tls_mode=true, warn=false);
                            kt->cipher = cipher_kt_get(ciphername);
                            kt->cipher_length = cipher_kt_key_size(kt->cipher);
                            kt->digest = md_kt_get(authname);
                            kt->hmac_length = md_kt_size(kt->digest);
                        out += "cipher AES-256-CBC,auth SHA1,keysize 256"
                    '''SSLѡ��'''
                    out += "tls-auth,key-method 2,tls-client"
                    return out
                c->c2.options_string_remote= options_string(&c->options, &c->c2.frame, 
                                                            c->c1.tuntap, &c->net_ctx,
                                                                    true, &gc);
                    out = "V4,dev-type tun,link-mtu 1557,tun-mtu 1500,\
                           proto UDPv4,keydir 0, cipher AES-256-CBC,auth SHA1,\
                           keysize 256,tls-auth,key-method 2,tls-server"
                if (c->c2.tls_multi)  //����
                    '''���ñ��غ�Զ��ѡ������ַ�����������֤���غ�Զ��ѡ��ϵļ�����'''
                    tls_multi_init_set_options(multi=c->c2.tls_multi,
                                               local=c->c2.options_string_local,
                                               remote=c->c2.options_string_remote);
                        multi->opt.local_options = local;
                        multi->opt.remote_options = remote;
            '''��ʼ������ٶ����ƣ�û��ִ��'''
            if (c->mode == CM_P2P)  //����
                do_init_traffic_shaper
                    '''��ʼ������shaper���༴�����������'''
                    if (c->options.shaper)  //������
            '''ֻ����һ�εĳ�ʼ����������������һ���ػ�����
               ÿ������ʵ��ֻ����һ��
               Ϊ���ܵ� UID/GID �����������ã�����ʱ��Ҫ������
               �����Ҫ�������ػ�����
               '''
            do_init_first_time   #�ͻ��˸��ٽ�� �� �ú�������ɶҲû��
                Ϊ c->c0 ����ռ�
                '''��ȡ/���ý��̵�GID'''
                platform_group_get(c->options.groupname, &c0->platform_state_group)
                    ��յڶ�������
                    if(��һ��������Ϊ��)   //������
                    else
                        return false
                '''��ȡ/���ý��̵�UID'''
                platform_user_get(c->options.username, &c0->platform_state_user)
                    ��յڶ�������
                    if(��һ��������Ϊ��)   //������
                    else
                        return false
                c0->uid_gid_specified = false
                '''����� --daemo ѡ���ִ���Ƴٵ�chdir'''
                if (c->did_we_daemonize && c->options.cd_dir == NULL)  //������
                    platform_chdir("/");  //�ڲ�ִ��ƽ̨��ص�chdir����
                '''����Ӧ�øı�������ȼ���'''
                platform_nice(c->options.nice=0);
            '''��ʼ�������û��ִ��'''
            open_plugins(c, false, OPENVPN_PLUGIN_INIT_POST_DAEMON);
                if (c->plugins && c->plugins_owned)   //������
            '''���ó�ʼ����ʱ�䶨ʱ��
               ��ʼ����������ѯ��ʱ��ʱ��
               �ö�ʱ������ͳ��һ�У�ֱ���յ����Է���˻�http����ĵ�һ����
               �˼�ʱ���� http/socks ��������ʱʹ���ˣ������Ҫ����֮ǰ��������'''
            +do_init_server_poll_timeout(c);
                update_time();  #���µ�ǰʱ��
                '''
                   server_poll_interval : 
                   Timer for everything up to the first packet from 
                   the *OpenVPN* server socks, http proxy, and tcp packets do not count
                   �������еĶ�ʱ����ֱ���յ����Է���˻�http����ĵ�һ����
                   �� tcp ������������
                   '''
                if (c->options.ce.connect_timeout) //120
                    c->c2.server_poll_interval->defined = true
                    c->c2.server_poll_interval->n = max(c->options.ce.connect_timeout,0)
                    c->c2.server_poll_interval->last = now
            '''���TCP/UDP socket�����ղ��� ��
               ���sock�׽��ֵĴ���������Ƿ���ˣ�������Ӧ����
               '''
            +do_init_socket_2(c);
                +link_socket_init_phase2(sock=c->c2.link_socket, frame=&c->c2.frame, sig_info=c->sig);
                    const char *remote_dynamic = NULL;
                    '''��ʼ���ص��˿�: sock->reads��sock->writes'''
                    +socket_frame_init(frame, sock);   &<socket_frame_init>
                        �����Windows
                            ��ʼ���ص��˿� sock->reads��sock->writes
                        '''udpʱ��������������'''
                        bool b=link_socket_connection_oriented(sock)
                            if(sock)   //����
                                '''���Ƿ����������ӵ�'''
                                link_socket_proto_connection_oriented(sock->info.proto);
                                    return !proto_is_udp(proto)
                            else
                                return false
                        if(b)  //������
                            stream_buf_init
                    '''����Ҫ����/���ܵ�Զ�����ƣ��Ա����ǿ��Բ��Զ�̬ IP ��ַ����'''
                    if (sock->resolve_retry_seconds)  //=100000000
                        remote_dynamic = sock->remote_host;   //"192.168.4.143"
                    '''����ͨ��inetd����xinetd������
                       file://inetd��xinetd.py
                       '''
                    if (sock->inetd)  // 0
                        ...
                    else  '''���sock�׽��ֵĴ���������Ƿ���ˣ�������Ӧ����'''
                        '''�ڶ��δ���/����socket�Ļ��ᣨû��ִ�У�
                           ���ݿͻ��˸��ٽ����������Ϊ do_init_socket_1 ���Ѿ����ù���Ӧֵ��
                           ���Ա���ִ�л���û��ɶ�£����ǰ� remote_dynamic ������Ϊ NULL ��
                           '''
                        +resolve_remote(sock, 2, &remote_dynamic,  &sig_info->signal_received);
                            '''���Զ�̵�ַ���⣨���û���壩'''
                            if (!sock->info.lsa->remote_list)  //�����㣬�� do_init_socket_1 ���Ѿ����ù���
                                ������
                            '''����Ӧ������֮ǰ���Զ�̵�ַ��'''
                            if (link_socket_actual_defined(&sock->info.lsa->actual))  //����
                                ��ӡ��Ϣ������ʹ�� 192.168.4.143:1194
                                if(remote_dynamic)  //����
                                    *remote_dynamic = NULL
                            else
                                ...
                        '''���������һ����Ч��Զ�ˣ���ʹ�����ĵ�ַ����socket'''
                        if (sock->info.lsa->current_remote)     //����
                            '''��� socket �׽��ֶ���Ĵ���, ����Ƿ���ˣ��������Ӧ����'''
                            +create_socket(sock, sock->info.lsa->current_remote);
                                �����udp����
                                    sock->sd = create_socket_udp(addr, sock->sockflags);
                                        socket_descriptor_t sd;
                                        sd = socket(addrinfo->ai_family, addrinfo->ai_socktype, addrinfo->ai_protocol)
                                        sock->sockflags |= SF_GETADDRINFO_DGRAM;
                                        '''�ٶ���socks�����Ŀ���socket������socket ���õ���ͬ��ip��'''
                                        if (sock->socks_proxy)  //������
                                            struct addrinfo addrinfo_tmp = *addr;
                                            addrinfo_tmp.ai_socktype = SOCK_STREAM;
                                            addrinfo_tmp.ai_protocol = IPPROTO_TCP;
                                            sock->ctrl_sd = create_socket_tcp(&addrinfo_tmp);
                                �����tcp����
                                    ...
                                '''����--sndbuf��--rcvbuf���������socket buffer����������(Ĭ�ϴ�С65536)'''
                                socket_set_buffers(sock->sd, &sock->socket_buffer_sizes)
                                '''�󶨱��ص�ַ/�˿�'''
                                bind_local(sock, addr->ai_family);  
                                    if (sock->bind_local)   //false����Ϊ�ͻ���Ҫ��Զ�˷������������Ǽ�����������
                                        if (sock->socks_proxy && sock->info.proto == PROTO_UDP)
                                            socket_bind(sock->ctrl_sd, sock->info.lsa->bind_local,
                                                        ai_family, "SOCKS", false);
                                        else
                                            socket_bind(sock->sd, sock->info.lsa->bind_local,
                                                        ai_family, "TCP/UDP", sock->info.bind_ipv6_only);
                        '''���socet�����ڻ�û�б�����'''
                        if (sock->sd == SOCKET_UNDEFINED)
                            '''�������û�� --remote ��������û�ó�Ҫ�õ�Э����
                               ���ǽ�ʹ�ð󶨵ĵ�һ��'''
                            if (sock->bind_local  && !sock->remote_host && 
                                sock->info.lsa->bind_local)
                                ....
                        '''socket��û���壬�������沢��ֹ����'''
                        if (sock->sd == SOCKET_UNDEFINED)  //������
                            msg(...)
                            goto done
                        if (sig_info->signal_received)  //������
                            goto done
                        if (sock->info.proto == PROTO_TCP_SERVER)   //������
                            phase2_tcp_server(sock, remote_dynamic, &sig_info->signal_received);
                        else if (sock->info.proto == PROTO_TCP_CLIENT)  //������
                            phase2_tcp_client(sock, sig_info);
                        else if (sock->info.proto == PROTO_UDP && sock->socks_proxy)    //������
                            phase2_socks_client(sock, sig_info);
                    '''���� sock->sockflags������socket�׽��ֶ��������'''
                    +phase2_set_socket_flags(sock);
                        ���� sock->sockflags ���� sock->sd
                        ���� sock->sd Ϊ��������
                        ���׽���������·�� MTU ����ѡ��
                            if(mut_type >=0)   //-1 ,������
                                switch (proto_af)  // 0
                                    case AF_INET:  // 2
                                        setsockopt(sd, IPPROTO_IP, IP_MTU_DISCOVER,...)
                                    case AF_INET6: // 23
                                        setsockopt(sd, IPPROTO_IPV6, IPV6_MTU_DISCOVER, ...)
            '''�����Ľ���UID/GID�Ľ����������Ҫ����chroot
               ���ܱ� --client --pull �� --up-delay �Ƴ�
               �ͻ��˸��ٽ�� �� �ú���ɶҲû��
               '''
            do_uid_gid_chroot(c, bool no_delay=c->c2.did_open_tun)
                if (c0 && !c0->uid_gid_chroot_set)  //����
                    if (c->options.chroot_dir)  //NULL��������
                        if (no_delay)
                            platform_chroot(c->options.chroot_dir);
                    '''�����û���/���飬���������Ҫsetuid/setgid'''
                    if (c0->uid_gid_specified)
                        if (no_delay)
                            platform_group_set(&c0->platform_state_group);
                            platform_user_set(&c0->platform_state_user);
            '''��ʼ�����ֶ�ʱ��'''
            if (c->mode == CM_P2P || child)
                update_time()  #���µ�ǰʱ��
                do_init_timers(c, bool deferred = false);
                    '''��ʼ���ǻ�Ծ��ʱ ��c->c2.inactivity_interval'''
                    if (c->options.inactivity_timeout)  //=0
                    '''��ʼ��ping���ͼ�ʱ ��c->c2.ping_send_interval'''
                    if (c->options.ping_send_timeout)   //=0
                    '''��ʼ��ping���ռ�ʱ ��c->c2.ping_rec_interval'''
                    if (c->options.ping_rec_timeout)   //=120
                    if(!deferred)  //��������
                        ��ʼ���������Ӽ�ʱ : c->c2.wait_for_connect
                        ��ʼ��occ��ʱ����������������
                        ��ʼ����id�־ö�ʱ���������㣩
                        ��ʼ��tmp_int�Ż������������������¼�ѭ���е���tls_multi_process�Ĵ���
            '''��ʼ�����'''
            if (c->mode == CM_P2P || c->mode == CM_TOP)
                open_plugins(c, false, OPENVPN_PLUGIN_INIT_POST_UID_CHANGE);
                    if (c->plugins && c->plugins_owned)  //������
                        ������
            if (child)  //������
                pf_init_context(c);
        +post_init_signal_catch  
    '''���¼�ѭ��'''
    +while(true)
        '''��ʵ��'''
        +perf_push(PERF_EVENT_LOOP); 
        '''����ʱ����tls��'''
        +pre_select(c);   &<pre_select>
            '''���ֶ�ʱ��������¶�ʱ����
               packed-id ���ļ�
               status ���ļ�
               ��������Ƿ���
               ����Ƿ���Ҫ���·��
               ���c->sig���Ƿ����ź�
               ���涨ʱ�����Ƿ��յ� ping
               ����Ƿ��յ�����˵ĵ�һ����
               ����Ƿ񵽴�Ԥ�����˳�ʱ����
               ����Ƿ�÷��� OCC_REQUEST ��Ϣ��
               ����Ƿ�÷��� MTU ���ز�����
               ����Ƿ��pingԶ����'''
            +check_coarse_timers(c);   &<check_coarse_timers>
                '''coarse_timer_wakeup��ʱ����û��ʱ�����¸ö�ʱ������������'''
                if (now < c->c2.coarse_timer_wakeup)
                    context_reschedule_sec(c, c->c2.coarse_timer_wakeup - now);
                    return
                c->c2.coarse_timer_wakeup = now + 7��
                '''������¶�ʱ����
                   packed-id ���ļ�
                   status ���ļ�
                   ��������Ƿ���
                   ����Ƿ���Ҫ���·��
                   ���c->sig���Ƿ����ź�
                   ���涨ʱ�����Ƿ��յ� ping
                   ����Ƿ��յ�����˵ĵ�һ����
                   ����Ƿ񵽴�Ԥ�����˳�ʱ����
                   ����Ƿ�÷��� OCC_REQUEST ��Ϣ��
                   ����Ƿ�÷��� MTU ���ز�����
                   ����Ƿ��pingԶ����
                   '''
                process_coarse_timers(c);  &<process_coarse_timers>
                    '''�ú�������һ������et����ʱ�����Ƿ��ѵ�ʱ,
                       �����ʱ���Ѿ���ʱ��ʱ����ֻ�ڵ���������С��0ʱ���ſ�����ʱ��et����һ�ֶ�ʱ������ʣ��ʱ������Ϊ��ʱ����������
                       ����ڶ���������Ϊ�գ����ݵ����������Ƿ�С��0�����õڶ���������ֵ��
                       �ǣ�ʣ��ʱ��(����<0)С�ڵڶ���������ֵʱ����ʣ�ൽʱʱ�����ڶ�������
                       �񣺵���������С�ڵڶ���������ֵʱ����������������ֵ����ڶ�������
                       ֮���ڵ���������С��0���Ҷ�ʱ����û��ʱʱ�������ŷ�����
                       ��һ�ֱ�����
                       ��ʹ�õ���������ʱ����-1��
                           ��ʱ���ѵ�ʱ�����ö�ʱ����ʣ�ൽʱʱ�䣬������
                           ����ڶ���������Ϊ�գ�����ʣ��ʱ�����ڶ�������
                       ʹ�õ���������ʱ��Ҫ��>=0������ֻ�еڶ���������Ϊ�գ���������
                           ��ʱ���ѵ�ʱ��parma2 > param3 ? param2=param3 : (0)
                           ��ʱ��û��ʱ��param2 > ʣ��ʱ�� ? param2=ʣ��ʱ�� : (0)
                       ��һ�ֱ�����
                       ����ʱ��û����ʱ����������ʱ�� wakeup���� wakeup < tv? tv=wakeup, ���ؼ�
                       ����ʱ���ﵽʱ��
                           et_const_retry < 0
                               ���¶�ʱ���Ĵ����¼� et->last = now��
                               ����ö�ʱ���Ķ�ʱ��� et->n < tv,  tv = et->n
                               ������
                           else          //��ʱ������¶�ʱ���¼�
                               ��� et_const_retry < tv, tv = et_const_retry
                               ���ؼ�
                       '''
                    &<event_timeout_trigger>
                    event_timeout_trigger(  struct event_timeout *et,
                                            struct timeval *tv,
                                            const int et_const_retry)
                        if(et->defined == false) return false
                        bool ret = false
                        '''et->last�ǿ�ʼʱ�䣬et->n�Ƕ�ʱʱ��'''
                        ���et�Ƿ��ѵ�ʱ��
                            �ǣ�
                                if et_const_retry<0  //et_const_retryͨ��������ֵΪ-1
                                    et->last = now
                                    ret = true
                                else
                                    wakeup = et_const_retry;
                        ���tv��Ϊ��             
                            ��� tv->tv_sec > et->n
                                tv->tv_sec = et->n
                                tv->tv_usec = 0
                        return ret
                    '���ָ���� --replay-persist����ÿ60�룬�� packed-id �浽�ļ�
                    '���c->c1.status_output��Ϊ�գ���ʱ��д status �ļ�
                    '''���c->c2.wait_for_connect��������Ƿ�����������
                       ע�⣬��һ��֮�󣬻�� c->c2.coarse_timer_wakeup ��Ϊ 1
                       '''
                    if (event_timeout_trigger(c->c2.wait_for_connect '=1'��c->c2.timeval��-1))
                        check_connection_established(c);
                    '''����Ƿ�Ӧ�÷���һ�� push_request (��Ӧѡ��--pull���˴�û������)'''
                    if (event_timeout_trigger(c->c2.push_request_interval��c->c2.timeval��-1))  
                        check_push_request(c);
                    '''����Ƿ���Ҫ���·�ɣ���Ӧ--routeѡ��˴�û�����ã�'''
                    if (event_timeout_trigger(c->c2.route_wakeup��c->c2.timeval��-1))
                        check_add_routes(c);
                    '���������--inactiveѡ������Ƿ����ʧ����˳�����
                    '''��������źţ�˵��������һ�����������ź��ˣ������˳�'''
                    if (c->sig->signal_received) return
                    '''ʵ������涨ʱ����û���յ� ping ������'''
                    check_ping_restart(c);
                        if(event_timeout_trigger(c->c2.ping_rec_interval '=120'��c->c2.timeval��-1))
                            trigger_ping_timeout_signal(c);
                    if (c->sig->signal_received) return
                    '''���涨ʱ���ڣ��Ƿ����������ĵ�һ��������û�յ�'''
                    if (c->options.ce.connect_timeout '=120' &&
                        event_timeout_trigger(c->c2.server_poll_interval��c->c2.timeval��-1))
                        check_server_poll_timeout(c);
                            if (!tls_initial_packet_received(c->c2.tls_multi))
                                register_signal(c, SIGUSR1, "server_poll");
                    if (c->sig->signal_received) return
                    '''����Ƿ񵽴�Ԥ�����˳�ʱ����'''
                    if (event_timeout_trigger(c->c2.scheduled_exit��c->c2.timeval��-1))
                        check_scheduled_exit(c);
                    if (c->sig->signal_received) return
                    '''�������ü���Ƿ�÷��� OCC_REQUEST ��Ϣ�ˣ�û���ã�'''
                    check_send_occ_req(c);
                        event_timeout_trigger(c->c2.occ_interval��c->c2.timeval��-1)
                            check_send_occ_req_dowork(c);
                    '''�������ã�����Ƿ�÷��� MTU ���ز����ˣ�û���ã�'''
                    check_send_occ_load_test(c);
                        event_timeout_trigger(c->c2.occ_mtu_load_test_interval��c->c2.timeval��-1)
                            check_send_occ_load_test_dowork(c)
                    '''�������ã�����Ƿ��pingԶ���ˣ�û���ã�'''
                    check_ping_send(c)
                        event_timeout_trigger(c->c2.ping_send_interval��c->c2.timeval��-1)
                            check_ping_send_dowork(c);
                ����c->c2.coarse_timer_wakeupΪc->c2.timeval��ʱ�䣨1���
            '''����ֶ�ʱ�����źŲ����������˳�'''
            if (c->sig->signal_received) return
            '''���Ų㣨reliable�����ݴ����ؼ�������tls_process'''
            +if (c->c2.tls_multi) 
                +check_tls(c);
                    +if( interval_test(&c->c2.tmp_int) )  #�𵽿��Ƶ���tls_multi_processƵ�ʵ�����
                        '''������ѭ�����ã���Ҫ�����Ƿ�Ӧ��Ϊ active �� untrusted sessions ���� tls_process'''
                        +int ret = tls_multi_process(   &<tls_multi_process>
                                            multi               = c->c2.tls_multi,
                                            to_link             = c->c2.to_link,
                                            to_link_addr        = c->c2.to_link_addr,
                                            to_link_socket_info = c->c2.link_socket->info,
                                            wakeup              = &(interval_t wakeup=7��) );
                            +for (int i = 0; i < TM_SIZE; ++i)  #TM_SIZE=3
                                struct tls_session *session = &multi->session[i];
                                struct key_state *ks = &session->key[KS_PRIMARY];
                                struct key_state *ks_lame = &session->key[KS_LAME_DUCK];
                                int active = TLSMP_INACTIVE;
                                '''ֻ�� TM_ACTIVE=0 ��session������ ks ��״̬Ϊ S_INITIAL ʱ��ִ��'''
                                if (i == TM_ACTIVE && ks->state == S_INITIAL)
                                    ks->remote_addr = to_link_socket_info->lsa->actual
                                if (ks->state >= S_INITIAL)
                                    struct link_socket_actual *tla = NULL;
                                    '''���Ų㣨reliable�����ݴ���'''
                                    if (tls_process(multi, session, to_link, &tla, to_link_socket_info, wakeup))  @tls_process
                                        active = TLSMP_ACTIVE;
                                    if(tla)
                                       c->c2.to_link_addr = multi->to_link_addr 
                                                          = *tla; 
                                                          = multi->session[].key[0].remote_addr
                                    '''��������tls_process�����г��˴�����������жϳ���'''
                                    if (ks->state == S_ERROR)
                                        ������
                            '''��ȡ��֤״̬��
                               ����multi->key_scan������û��״̬Ϊ>=S_GOT_KEY/S_SENT_KEY��
                               ����У���������û����֤����
                               �����֤���ˣ��򷵻� TLS_AUTHENTICATION_SUCCEEDED����֤�ɹ���
                               �����������״̬ΪS_GOT_KEY/S_SENT_KEY�ģ���û��֤���ģ����� TLS_AUTHENTICATION_FAILED
                               ���򣬷��� TLS_AUTHENTICATION_DEFERRED ����֤�Ƴ٣�
                               '''
                            int tls_auth_state = tls_authentication_status(multi, TLS_MULTI_AUTH_STATUS_INTERVAL);
                            '''���session->key[KS_LAME_DUCK]��
                               �����state >= S_INITIAL��
                                   �����must_dieʱ�䳬����ǰʱ�䣬������
                                   ���򣬷��ؼ٣�wakeup����Ϊ������ʱ��-��ǰʱ�䡯
                               ���򣬷��ؼ�'''
                            if (lame_duck_must_die(&multi->session[TM_LAME_DUCK], wakeup))
                                ...
                            '''��� TM_UNTRUSTED ��session��KS_PRIMARY key��״̬Ϊ>= S_GOT_KEY/S_SENT_KEY ��,
                               ��֮תΪ active ��session'''
                            if (DECRYPT_KEY_ENABLED(multi, &multi->session[TM_UNTRUSTED].key[KS_PRIMARY]))
                                move_session(multi, TM_ACTIVE, TM_UNTRUSTED, true);
                            ...
                        if(ret == TLSMP_ACTIVE)
                            interval_action(&c->c2.tmp_int);
                                c->c2.tmp_int->last_action = now
                        '''���tls_multi_process�����˴����򴥷������¼�'''
                        else if(ret == TLSMP_KILL)
                            register_signal(c, SIGTERM, "auth-control-exit");
                        c->c2.tmp_int->future_trigger = now + wakeup
                    '''����c->c2.tmp_int�ĳ�Աֵ���õ������wakeupʱ�䣺
                       min(last_test_true+refresh-now, wakeup)
                       min(future_trigger,wakeup)'''
                    interval_schedule_wakeup(&c->c2.tmp_int, &wakeup);
                        min(c->c2.tmp_int
                    if (wakeup) //��
                        c->c2.timeval.tv_sec = min(wakeup,c->c2.timeval.tv_sec)
            +check_tls_errors(c);
            '''���tls�д�������������˳�'''
            if (c->sig->signal_received) return
            '''�������ͨ�������յ�������Ϣ�ˣ�������
               tls_test_payload_len����multi->session[TM_ACTIVE].key[KS_PRIMARY].state >= S_ACTIVE(6) ʱ
               ���� ks->plaintext_read_buf���������ı����ݣ� �ĳ��ȣ� ���򣬷���0
               '''
            +if (tls_test_payload_len(c->c2.tls_multi) > 0)
                +check_incoming_control_channel(c);
            '''����Ƿ�Ӧ�÷���occ��Ϣ
               ��� c->c2.occ_op >= 0 �ҵ�ǰ c->c2.to_link ��û������Ҫ����
               '''
            +check_send_occ_msg(c);
                if (c->c2.occ_op >= 0)  #��ǰΪ-1��������ܻ��޸ĸ�ֵ
                    ��� c->c2.to_link �ĳ���Ϊ0 
                        check_send_occ_msg_dowork(c);
                    else
                        c->c2.timeval = 0
        +uint flags = IOW_READ_TUN (1<<2) | 
                     IOW_READ_LINK (1<<3) |
                     IOW_SHAPER  (1<<4) |
                     IOW_CHECK_RESIDUAL (1<<5) |
                     IOW_FRAG  (1<<6) |
                     IOW_WAIT_SIGNAL  (1<<9)
        if (c->c2.to_link.len>0)  flags |= IOW_TO_LINK  (1<<1) ;
        '''�� c->c2.link_socket(��c->c1.tuntap��������)�϶������ȴ�����д�¼�'''
        +io_wait(c, flags);
            +io_wait_dowork(c, flags);
                static int socket_shift = 0;   #depends on SOCKET_READ and SOCKET_WRITE 
                static int tun_shift = 2;      #depends on TUN_READ and TUN_WRITE 
                static int err_shift = 4;      #depends on ES_ERROR 
                uint socket = 0
                uint tuntap = 0
                struct event_set_return esr[4];
                +event_reset(c->c2.event_set);
                '''��win32_signal.in��¼��c->c2.event_set�У�
                   ��c->c2.event_setǿתΪ we_set �ṹ��Ȼ���������Աֵ��
                   HANDLE* events[n_events] = win32_signal.in.read
                   event_set_return* esr[n_events].rwflags = EVENT_READ 
                   event_set_return* esr[n_events].arg = &err_shift
                   n_events++
                   '''
                +���flags���� IOW_WAIT_SIGNAL  #IOW�� io wait ����˼
                    '''��win32_signal.in��¼��c->c2.event_set�У�
                       err_shift���������win32_signal.in���յ��źţ�
                       ������ c->c2.event_set_status Ϊ ES_ERROR
                       '''
                    +wait_signal(c->c2.event_set, arg=(void *)&err_shift);  &<wait_signal>
                        +if(HANDLE_DEFINED(win32_signal.in.read))  #win32_signal�ڿͻ������ڻ�ȡ����̨��������
                            event_ctl(c->c2.event_set,&win32_signal.in,EVENT_READ,arg) #win32_signal.in�� @rw_handle �ṹ
                            ->we_ctl(es,event,rwflags,arg)  &<we_ctl> &<event_ctl>
                                we_append_event(es, event, rwflags, arg)
                                    if (rwflags & EVENT_WRITE)
                                        if(es->n_events < es->capacity)
                                            we_set_event(wes, wes->n_events, event, EVENT_WRITE, arg);
                                                (we_set*)es->events[i] = event->read;
                                                wes->esr[i].rwflags = rwflags;
                                                wes->esr[i].arg = arg;
                                    if (rwflags & EVENT_READ)
                                        if(es->n_events < es->capacity)
                                            we_set_event(wes, wes->n_events, event, EVENT_READ, arg);
                                                (we_set*)es->events[i] = event->read;
                                                wes->esr[i].rwflags = rwflags;
                                                wes->esr[i].arg = arg;
                                ����Ͼ�ʧ�ܣ������ D_EVENT_ERRORS �¼�
                '''����д������ݵȴ����ͣ����þֲ�����socket��ֵ'''
                if (flags & IOW_TO_LINK)   #����
                    socket |= EVENT_WRITE;
                '''��������㣨���� IOW_FRAG �� c->c2.fragment ��Ϊ�գ�'''
                else if (!((flags & IOW_FRAG) && TO_LINK_FRAG(c)))   #�Ͼ����㣬��þ䲻�ж�     
                    if (flags & IOW_READ_TUN)  #����
                        tuntap |= EVENT_READ;
                if (flags & IOW_TO_TUN)   #������
                    tuntap |= EVENT_WRITE;
                else if (flags & IOW_READ_LINK)  #����
                    socket |= EVENT_READ;
                if (flags & IOW_MBUF)    #������
                    socket |= EVENT_WRITE;
                if (flags & IOW_READ_TUN_FORCE)  #������
                    tuntap |= EVENT_READ;
                if (tuntap_is_wintun(c->c1.tuntap))  #������
                    ������
                '''��c->c2.link_socket�ϲ��Զ������ݴ��� c->c2.link_socket.reads.buf �У�
                   ���ݶ�ȡ��������� c->c2.link_socket.reads �ĳ�Աֵ��
                       overlapped.hEvent��status��overlapped.hEvent
                   ������� persistent==rwflags����� c2.link_socket->rw_handle �ǵ� c2.event_set ��
                   '''
                +socket_set(s=c->c2.link_socket, es=c->c2.event_set, rwflags=socket, 
                           arg=(void *)&socket_shift, uint*persistent=NULL);
                    +if( rwflags & EVENT_READ)
                        +socket_recv_queue(sock=s, 0);
                            if (sock->reads.io_state == IOSTATE_INITIAL)  #sock->reads��overlapped_io�ṹ
                                ����WSARecvFrom����socket���������� sock->reads.buf
                                �����������������
                                    sock->reads.io_state = IOSTATE_IMMEDIATE_RETURN;
                                    SetEvent(sock->reads.overlapped.hEvent)
                                    sock->reads.status = 0
                                ����
                                    �������ֵΪ��WSA_IO_PENDING  #˵�������ݵȴ���
                                        sock->reads.io_state = IOSTATE_QUEUED;
                                        sock->reads.status = WSA_IO_PENDING;
                                    ����  #û�����ݵȴ���
                                        sock->reads.io_state = IOSTATE_IMMEDIATE_RETURN;
                                        sock->reads.status = WSAGetLastError();
                            return sock->reads.io_state
                    if (!persistent || *persistent != rwflags) 
                        '''��c->c2.event_setǿתΪ we_set �ṹ��Ȼ���������Աֵ��
                           HANDLE* events[n_events] = s->rw_handle->write
                           event_set_return* esr[n_events].rwflags = EVENT_WRITE 
                           event_set_return* esr[n_events].arg = &socket_shift
                           n_events++
                           HANDLE* events[n_events] = s->rw_handle->read
                           event_set_return* esr[n_events].rwflags = EVENT_READ 
                           event_set_return* esr[n_events].arg = &socket_shift
                           n_events++
                           '''
                        event_ctl(es, s->rw_handle, rwflags, arg);
                            we_ctl(struct event_set *es, event_t event, unsigned int rwflags, void *arg)
                                @we_ctl
                    s->rwflags_debug = rwflags;
                    return rwflags;
                +tun_set(c->c1.tuntap, c->c2.event_set, tuntap, (void *)&tun_shift, NULL);
                    if (tuntap_defined(tt))  #������
                '''���û�������󣬾͵ȴ��¼���c->c2.event_set�������ȴ�������ø�c->c2.event_set_status'''
                +if (!c->sig->signal_received)  #���c->sig->signal_received���źţ�ͨ���ǳ����ź�
                    '''�ȴ� (we_set*)multi.top.c2.event_set)->events
                       ���ĳ�� event �������ˣ���֮��¼��out��
                       ���ش������¼�����
                       ��� status > 0  , ���� multi.top.c2.event_set_status ����Ӧλ
                       ��� status = 0 , ���� multi.top.c2.event_set_status = ES_TIMEOUT
                       '''
                    +status = event_wait(c->c2.event_set, &c->c2.timeval, esr, SIZE(esr));
                    =we_wait(struct event_set *es, const struct timeval *tv, struct event_set_return *out, int outlen)
                        dword status = WSAWaitForMultipleEvents((we_set*)es->n_events,(we_set*)es->events,FALSE,0,FALSE)
                        ���status>=WSA_WAIT_EVENT_0
                            ���� WaitForSingleObject((we_set*)es->events[i])������Ǹ��¼�������
                                ��֮��¼��out������
                            ���ش������¼�����
                        ���û���¼�����
                            �������tv��120��>0
                                �ȴ���ֱ�����¼�������ʱ
                            ������¼�������
                                ��֮��¼��out�У�����1
                            �����ʱ��
                                ����0
                            �������
                                ���� -1
                    '''�����¼��ȴ����esr������c->c2.event_set_status'''
                    if(status > 0) #status=3��status>0 �������¼��ȵ���
                        c->c2.event_set_status = 0;
                        for (i = 0; i < status; ++i)
                            event_set_return *e = &esr[i]
                            c->c2.event_set_status |= ( e->rwflags&3 << e->arg )
                            �Σ�file://openvpn��context�ṹ.c+@io_wait���ܷ��ص��¼�ֵ
                    else if (status == 0)
                        c->c2.event_set_status = ES_TIMEOUT;
                '''�������������㣬˵���� c->sig ���յ��ź��ˣ���һ�����������'''
                if (c->c2.event_set_status & ES_ERROR)
                    get_signal(&c->sig->signal_received);
                        *sig = win32_signal_get(&win32_signal);
                            �ȼ����� siginfo_static ���յ��ź��ˣ� �򷵻� siginfo_static �Ĵ�����
                            ��������� win32_signal �ϵ��ź�ֵ��ͨ�������м����¼��ˣ�
        '''���c->sig'''
        P2P_CHECK_SIG();
            if(c->sig->signal_received)
                '''���c->sig->signal_received�յ����ź�ΪSIGUSR1���ɽ�֮ӳ��Ϊc->options.remap_sigusr1'''
                remap_signal(c);
                    if (c->sig->signal_received == SIGUSR1 && c->options.remap_sigusr1)
                        c->sig->signal_received = c->options.remap_sigusr1;
                '''����SIGUSR1��SIGHUP�ź�:
                   ��������������㣬�Ҷ����� c->c2.explicit_exit_notification_interval��event_timeout�ṹ��
                       ��� c->sig->source == SIG_SOURCE_HARD Ϊ�棬���c->sig�������棬
                       ��������c->sigΪSIGTERM�����ؼ�
                   ���򷵻ؼ�
                   '''
                int brk = process_signal(c);
                    if( c->sig->signal_received==SIGUSR1��SIGHUP �� 
                        c->c2.explicit_exit_notification_interval->definedΪ�� )
                        if( c->sig->source == SIG_SOURCE_HARD )
                            signal_reset(si=c->sig);
                                si->signal_received = 0;
                                si->signal_text = NULL;
                                si->source = SIG_SOURCE_SOFT;
                            return true
                        else
                            register_signal(c, SIGTERM, "exit-with-notification");
                                c->sig->signal_received = SIGTERM;
                                c->sig->signal_text = "exit-with-notification";
                            return false
                    return false
                perf_pop();
                if(brk)
                    break;
                else
                    continue;
        +process_io(c)
            uint status = c->c2.event_set_status;
            '''���ӹ��������յ��ź�'''
            +if (status & (MANAGEMENT_READ|MANAGEMENT_WRITE))
                ������
            '''�ȿ�socket���Ƿ��յ���д�ź�'''
            +if (status & SOCKET_WRITE)
                '''��c->c2.to_link�ϵ����ݷ��͵�Ŀ�ĵ�ַ'''
                +process_outgoing_link(c);
                    +���c->c2.to_link��������Ҫд
                        +ȷ��c->c2.to_link_addr��Զ�˵�ַ����Ч
                        '''���ʹ��������У������shaper֪������д�˶����ֽ�'''
                        if (c->options.shaper) #������
                            ������
                        '''����ping�ļ�ʱʱ��'''
                        if (c->options.ping_send_timeout)
                            event_timeout_reset(&c->c2.ping_send_interval);
                        +'''����socket��TOS(��������)'''
                        link_socket_set_tos(ls=c->c2.link_socket);
                            if (ls && ls->ptos_defined) #ptos_definedΪ��
                                setsockopt(ls->sd, IPPROTO_IP, IP_TOS, ls->ptos, sizeof(ls->ptos));
                        +'����(��ӡ���¼��־��ִ��)���͵İ�
                        int size_delta=0
                        socks_preprocess_outgoing_link(c, &to_addr, &size_delta);  #�ڲ�û��ִ��
                            if (c->c2.link_socket->socks_proxy)  #������
                                if(c->c2.link_socket->info.proto == PROTO_UDP)  #����
                                    ������
                        '''��c->c2.to_link�ϵ����ݷ��͵�Ŀ�ĵ�ַ'''
                        +size = link_socket_write(c->c2.link_socket,&c->c2.to_link,c->c2.to_link_addr);
                            if (proto_is_udp(sock->info.proto))  #����
                                return link_socket_write_udp(sock=c->c2.link_socket, buf=c->c2.to_link, to=c->c2.to_link_addr);
                                    '''����ص��˿ڵ�״̬Ϊ�Ŷӻ��������أ�����IOSTATE_INITIAL��������ص��˿ڷ��ͽ������������򱨴�'''
                                    ��� sock->writes->iostate Ϊ IOSTATE_QUEUED(1) �� IOSTATE_IMMEDIATE_RETURN(2)  #Ϊ0��������
                                        '''���ص��˿ڴ�������û�У��ɹ������꣬�����շ������ݳ��ȣ������շ����߳���������-1
                                           ���buf������Ϊ�գ������ڳɹ�������ɵ�����£����ص��˿��ϵ����ݴ��buf�������ڶ���
                                           ���⣬�շ���ɣ������ǳɹ�����ʧ�ܣ��ˣ�������ص��˿ڵ��¼��ָ�Ϊδ����״̬
                                           �������������from��Ϊ�գ��򻹻���ص��˿��ϼ�¼��ip��ַ���from����
                                           ���壺
                                               ����Ĳ���io��Ϊ�ص��˿ڣ�
                                               ������ص��˿ڵ�״̬Ϊ IOSTATE_INITIAL��˵�����ص��˿�û�м��socket�����ݵ��շ�
                                                   ͨ�����������Ӧ�ó��֣���Ϊ����֪��ǰ�����������ص��˿ڼ�����socket�ģ�
                                                   �ǳ�����������������ǲ��ǲ������ˣ�����Ϊʲô������������������ֻ�ǰѷ���ֵ��Ϊ-1
                                               ������ص��˿ڵ�״̬Ϊ IOSTATE_IMMEDIATE_RETURN��˵�����ص��˿��Ѿ�����շ��ˣ���������û����
                                                   �����ص��˿ڵ�״̬Ϊ IOSTATE_INITIAL��ͬʱ�����ص��˿ڵ��¼�����״̬
                                                   �������Ϊ��������أ������÷���ֵΪ-1
                                                   ����ǳɹ����صģ����÷���ֵΪ�������ֽ�����������buf��Ϊ�գ�����ص��˿��м�¼�����ݴ��buf
                                               ������ص��˿ڵ�״̬Ϊ IOSTATE_QUEUED��˵�����ص��˿ڻ�û����շ������ڽ�����
                                                   ��ʱ���ټ����ص��˿ڣ���������շ���û��
                                                       �������ˣ�Ҳ�����ǳ����ˣ��������ص��˿ڵ�״̬Ϊ IOSTATE_INITIAL��ͬʱ�����ص��˿ڵ��¼�����״̬
                                                           ����ɹ������÷���ֵΪ�������ֽ�����������buf��Ϊ�գ�����ص��˿��м�¼�����ݴ��buf
                                                           ���ʧ���ˣ������÷���ֵΪ-1
                                                       ���û��ɣ���ʲôҲ����������ֵĬ��Ϊ-1��
                                           '''
                                        socket_finalize(s=sock->sd, io=&sock->writes, buf=NULL, from=NULL);  &<socket_finalize>
                                            '''�ϴεķ��ͽ��ΪIOSTATE_QUEUED���Ŷӵģ�'''
                                            if ��sock->writes->iostate == IOSTATE_QUEUED��
                                                BOOL status = WSAGetOverlappedResult(s=sock->sd, io=sock->writes->overlapped, ...)
                                                if (status) #�ɹ���ʾ�ص��˿ڲ����Ѿ��ɹ���ɣ�ʧ�ܱ�û����ɻ������
                                                    if(buf) *buf = io->buf;
                                                    io->iostate = IOSTATE_INITIAL;
                                                    ResetEvent(io->overlapped.hEvent)
                                                else
                                                    if (WSAGetLastError() != WSA_IO_INCOMPLETE)  #�����ص��˿ڻ�û��ɵ��������������
                                                        io->iostate = IOSTATE_INITIAL;
                                                        ResetEvent(io->overlapped.hEvent)
                                                        msg(D_WIN32_IO | M_ERRNO, "WIN32 I/O: Socket Completion error");
                                            '''�ϴεķ��ͽ��ΪIOSTATE_IMMEDIATE_RETURN�������ɹ������ˣ�'''
                                            if ��sock->writes->iostate == IOSTATE_IMMEDIATE_RETURN
                                                io->iostate = IOSTATE_INITIAL;
                                                ResetEvent(io->overlapped.hEvent)
                                                '''�ϴη��ͽ����Ϊ0'''
                                                if (io->status)
                                                    msg(D_WIN32_IO | M_ERRNO, "WIN32 I/O: Socket Completion non-queued error");
                                                else  #�ϴη��ͽ��Ϊ�ɹ�
                                                    ret = io->size;
                                            if (from) #������
                                                ������
                                    '''��c->c2.to_link�����ݷ��͵�Ŀ�ĵ�ַ������sock->writes.overlapped.hEvent'''
                                    socket_send_queue(sock=c->c2.link_socket, buf=c->c2.to_link, to=c->c2.to_link_addr);
                                        if (sock->writes.iostate == IOSTATE_INITIAL)  #����
                                            #sock->writes.buf �� @socket_frame_init ��������ɵĳ�ʼ����,buf_init.offset=548, buf_init.len=1640
                                            sock->writes.buf = sock->writes.buf_init;
                                            sock->writes.buf.len = 0;
                                            '''������buf�����ݣ��ŵ�sock->writes.buf��'''
                                            buf_copy(&sock->writes.buf, buf)  #���ִ�����buf_init.offset=548, buf_init.len=14
                                            '''��sock->writes.buf�ϵ���Ч���ݴ��wsabuf'''
                                            WSABUF wsabuf[1];
                                            wsabuf[0].buf = BPTR(&sock->writes.buf);
                                            wsabuf[0].len = BLEN(&sock->writes.buf);
                                            '''��wsabuf�ϵ����ݷ��ͳ�ȥ������������ͳɹ��ˣ�����0�����򷵻�����ֵ'''
                                            status = sock->writes.status = WSASendTo(...)
                                            if (0==status)  #����
                                                sock->writes.iostate = IOSTATE_IMMEDIATE_RETURN;
                                            else
                                                if( WSA_IO_PENDING == WSAGetLastError()) #�ص��˿ڳɹ���ʼ���ˣ��Ժ�ָʾ���
                                                    sock->writes.iostate = IOSTATE_QUEUED;
                                                else  #˵�����ʹ���
                                                    ASSERT(SetEvent(sock->writes.overlapped.hEvent));
                                                    sock->writes.iostate = IOSTATE_IMMEDIATE_RETURN;
                                        return sock->writes.iostate;
                                    return ���͵����ݳ��ȣ���С��0��ֵ����ʾ����
                            else if (proto_is_tcp(sock->info.proto))
                                return link_socket_write_tcp(sock, buf, to);
                        link_socket_write_post_size_adjust(&size, size_delta, &c->c2.to_link);  #�ڲ�û��ִ��
                            if(size_delta>0) #������
                                if(size>0)
                                    size -= size_delta
                                    buf_advance(buf, size_delta)
                                    *size = 0
                        if (size > 0)  #�������ͳɹ���size�Ƿ��͵��ֽ���
                            '''�ۼ��ѷ����ֽ���'''
                            c->c2.link_write_bytes += size;
                            link_write_bytes_global += size
                            if (management)  #������
                                ...
                            '''ʵ�ʷ��͵����ݳ��ȣ����뷢�͵����ݳ��Ȳ�һ�£�����'''
                            if (size != BLEN(&c->c2.to_link))
                                msg(D_LINK_ERRORS, ...)
                        if (c->c2.buf.len > 0) #0��������
                            ������
                        if(size < 0)  #������
                            ������
                    buf_reset(&c->c2.to_link);
            '''�ٿ�tuntap���Ƿ��յ���д�ź�'''
            +else if (status & TUN_WRITE)
                ������
            '''�ٿ�socket���Ƿ��յ��ɶ��ź�'''
            +else if (status & SOCKET_READ)
                '''���԰��ص��˿��ϵ����ݴ��c->c2.buffers->read_link_buf������c->c2.bufָ���buffer'''
                +read_incoming_link(c);
                    c->c2.buf = c->c2.buffers->read_link_buf;   #c2.buffersר�����ڰ������Buffers
                    buf_init(&c->c2.buf,FRAME_HEADROOM_ADJ(..))
                    status = link_socket_read(c->c2.link_socket, &c->c2.buf, &c->c2.from);
                        if (proto_is_udp(sock->info.proto))
                            int res = link_socket_read_udp_win32(sock, buf, from);
                                return socket_finalize(sock->sd, &sock->reads, buf, from);
                                    @socket_finalize
                        else if (proto_is_tcp(sock->info.proto))
                            ...
                    '''���ֻ��������ʾ������Ϣ��'''
                    check_status(status, "read", c->c2.link_socket, NULL); &<check_status>
                    '''���ֻ����ʹ��socket���������²Ź���'''
                    socks_postprocess_incoming_link(c);
                +if ( ! c->sig->signal_received ) #���û�г���
                    +process_incoming_link(c);
                        link_socket_info *lsi = c->c2.link_socket_info;
                        +process_incoming_link_part1(c, lsi, false);
                            @process_incoming_link_part1
                        +process_incoming_link_part2(c, lsi, orig_buf);
                            @process_incoming_link_part2
            '''���tuntap���Ƿ��յ��ɶ��ź�'''
            +else if (status & TUN_READ)
                ������
        '''���c->sig'''
        P2P_CHECK_SIG();         
'''�ú��������¼�ѭ���У�����TLS�������Ҫ������
   ���ú������� non-error����������wakeup����Ϊϣ���´α����õ�ʱ��
   ������ǰ�һ��������� to_link �����������سɹ�
   to_link ������ϣ�������Զ˵İ�����
   '''
&<tls_process>            
+bool tls_process(  #���Ų㣨reliable�����ݴ���
                 struct tls_multi *multi,                        = c->c2.tls_multi,
                 struct tls_session *session,                    = multi->session[]
                 struct buffer *to_link,                         = c->c2.to_link,
                 struct link_socket_actual **to_link_addr,       = tla,
                 struct link_socket_info *to_link_socket_info,   = c->c2.link_socket->info
                 interval_t *wakeup)                             = = &(interval_t wakeup=7��)
    struct key_state *ks = &session->key[KS_PRIMARY];      /* primary key */
    struct key_state *ks_lame = &session->key[KS_LAME_DUCK]; /* retiring key */
    bool active = false;
    bool state_change = true;
    '����Ƿ�����Ӧ�ô���һ�������� --  ��Ϊ��Ҫ��������Կ
    '''����Э������Կ�ļ���󣬹ر� lame duck key transition_window
       lame_duck_must_die �����ڣ����� session->key[KS_LAME_DUCK]->must_die �Ƿ�ʱ
       '''
    +if (lame_duck_must_die(session, wakeup))
        key_state_free(ks_lame, true);
        msg("TLS: tls_process: killed expiring key");
    +while(state_change)
        update_time();
        state_change = false;
        if (ks->state == S_INITIAL)
            '''send_reliable �Ǹ� reliable �ṹ���������ɴ��RELIABLE_CAPACITY=8�� reliable_entry �ṹ��
               ʵ��ֻ����4����ÿ��reliable_entry�ɼ�¼һ�����ݰ���������Ч��ǡ���id�������ݡ������롢ʱ��ȣ�
               һ�� reliable �ṹ�����Ų�����ݽṹ���������vpn��һ�������ϵĿ���ͨ��
               reliable ���и� hold ��ǣ� ���Կ����� reliable_schedule_now ����ǰ�����ᷢ��
               reliable_get_buf_output_sequenced ���Ƕ�λ����id��С�� reliable_entry ��Ա��
               ��������buf��reliable_entry�м�¼�����ݵ�buffer�ṹ��
               ����ǰ�������� buf �� len=0 �� offset=ks->send_reliable->offset=44
               '''
            +struct buffer *buf = reliable_get_buf_output_sequenced(ks->send_reliable)
            +if(buf)
                ks->must_negotiate = now + session->opt->handshake_window=60s;
                ks->auth_deferred_expire = now + auth_deferred_expire_window(session->opt)=60s;
                '''�ҵ��봫���buf������Ӧ���Ǹ� reliable_entry�����������ݣ�
                   ��������Ч���Ϊ�棬�����������Ϊ7��P_CONTROL_HARD_RESET_CLIENT_V2��
                   �������id��0����������ƫ��Ϊ 44-4=40��������buf���ݴ����id'''
                +reliable_mark_active_outgoing(ks->send_reliable, buf, ks->initial_opcode);
                ks->state = S_PRE_START;
                state_change = true;
        '''��� ks->state ��û S_ACTIVE�����鵱ǰʱ�䣬�Ƿ񵽴� ks->must_negotiate ��ʱ���ˣ��ǣ���˵��Э�̳�ʱ��'''
        +if (now >= ks->must_negotiate && ks->state < S_ACTIVE) goto error
        '''FULL_SYNC�Ǹ��꺯��������Ƿ� ks->send_reliable �� ks->rec_ack ��Ϊ��,
           һ���ڷ�������յ�����˻ظ�֮ǰ�������������'''
        +if (ks->state == S_PRE_START && FULL_SYNC)    
            ks->state = S_START;
            state_change = true;
            if (session->opt->crl_file && 
                session->opt->ssl_flags ������ SSLF_CRL_VERIFY_DIR)
                ������
            '''�µ����ӣ�����ɵ�X509��������'''
            tls_x509_clear_env(session->opt->es);
        '''����Ѿ�������key������ˣ�������key���ͻ��ˣ�'''
        +if (ks->state == S_GOT_KEY && is_client || ks->state == S_SENT_KEY && is_server)
            ...
        '''to_link=c->c2.to_link��reliable_can_send����send_reliable�еı��ֱ���Ƿ�Ϊ�٣���������û����Ч�İ�
           ����reliable��׼������Ҫ����������û��֮ת��洢��c->c2.to_linkǰ��������ͨ���������
           '''
        +if (!to_link->len && reliable_can_send(ks->send_reliable))
            int opcode;
            '''�ҵ���id��С���Ǹ�reliable_entry,��Ϊbest������ best->next_try = now+best->timeout(2)
               best->timeout *= 2; ���� opcode = best->opcode; ���� best->buf'''
            +buf = reliable_send(ks->send_reliable, &opcode);
            +buffer b = *buf  # b �� buf ���� uint8_t *data������ֵ�����ӵ��
            '''�� ks->rec_ack ����Ϣprepend�� b �У���������Ҫ����b�е��������ݣ���֧����֤����ܣ�
               �� ks->rec_ack ����Ϣprepend�� b ��
               ���session->tls_wrap.modeΪ'��֤'��'��'���
                   ��session->session_id��8�ֽڣ� prepend��b��
                   ��ovpnͷprepend��b��
               ���session->tls_wrap.modeΪ'��֤'���
                   ��������
               ���session->tls_wrap.modeΪ'����'���
                   ��������
               '''
            &<write_control_auth>
            +write_control_auth(session,ks,buf=b,to_link_addr, opcode, max_ack=CONTROL_SEND_ACK_MAX=4, prepend_ack=true) 
                '''�� ack=ks->rec_ack ����Ϣ���뵽 b �У�
                   �� ack->len ��ֵ=0��1�ֽڣ�д�뵽 b �У�ͷ�巨��
                   ��� ack->len > 0��
                       �򻹰� ack->packet_id[]�� ks->session_id_remote������д�뵽b��
                       �����޸� ack->packet_id[] ��ֵ
                   '''
                reliable_ack_write(ks->rec_ack, buf, &ks->session_id_remote, max_ack, prepend_ack)
                '''��session->session_id(���ֵ)prepend��b�У���ovpnͷ��ks->key_id | opcode��prepend��b��'''
                if (session->tls_wrap.mode == TLS_WRAP_AUTH �� TLS_WRAP_NONE)
                    session_id_write_prepend(&session->session_id, buf)
                if (session->tls_wrap.mode == TLS_WRAP_AUTH)
                    ������
                else if (session->tls_wrap.mode == TLS_WRAP_CRYPT)
                    ������
                *to_link_addr = ks->remote_addr
            '''��b����udp��'''
            +*to_link = b;  
            active = true;
            state_change = true;
            +break;
        '''�ӽ������β��л�ȡ��Ч�İ��������������ָ��
           �ڿͻ����յ�����˵ĵ�һ��������Ӧ��ʱ����ִ������
           '''
        buf = reliable_get_buf_sequenced(ks->rec_reliable);
        if(buf)
            int status = 1
            if (buf->len)
                '''������д�� ks->ks_ssl->ct_in (ssl)'''
                status = key_state_write_ciphertext(&ks->ks_ssl, buf);
                    ret=bio_write(ks_ssl->ct_in, BPTR(buf), BLEN(buf), "tls_write_ciphertext");
                    '����ɹ����ɹ�ʱ���buf
                    return ret
            if(status == 1)
                '''����buf��Ӧ��rec_reliable�еİ�����Ϊ�ǻ�ģ�
                   ͬʱ rec_reliable �е� packet_id ֵ��1
                   '''
                reliable_mark_deleted(ks->rec_reliable, buf, true);
                state_change = true;
        '''��bufָ���ı�������(���Դ�ssl�϶�ȡ���ݣ�'''
        buf = &ks->plaintext_read_buf;
        if (!buf->len)  #����ļ�������Ϊ�գ�����
            buf_init(buf, 0)
            int status = key_state_read_plaintext(&ks->ks_ssl, buf, TLS_CHANNEL_BUF_SIZE);
                '''��ks_ssl->ssl_bio�϶�ȡ����'''
                return bio_read(ks_ssl->ssl_bio, buf, maxlen, "tls_read_plaintext");
                    int ret = 0;
                    if (buf->len > 0)
                        int len = buf_forward_capacity(buf);  #buf�� buf->offset+buf->len ��ʼ֮�������
                        i = BIO_read(bio, BPTR(buf), len);
                        if(i < 0)  #��ȡʧ��
                            if (BIO_should_retry(bio)) #�´����ԣ�
                                (0)
                            else
                                crypto_msg(D_TLS_ERRORS, "TLS_ERROR: BIO read %s error", desc);
                                ret = -1;
                        else if(i == 0)  #�����ݿɶ�
                            buf->len = 0;
                        else  #����������
                            buf->len = i;
                            ret = 1;
                    return ret
            if(status == 1) #����������
                state_change = true;
                *wakeup = 0;
        '''��bufָ���ı�д��������Ϊ�˷���Key'''
        buf = &ks->plaintext_write_buf;
        if (!buf->len && ( (ks->state == S_START && !session->opt->server)
                           || (ks->state == S_GOT_KEY && session->opt->server) ) )
            '''��key���ݡ��Զ���Ϣ���û������룬OCC�ȣ�д��tsl����ͨ���У����ı���'''
            bool b = key_method_2_write(buf, multi, session)
                'buf��дһ�� uint32 �� 0
                'buf��д uint8 �� KEY_METHOD_2(2)
                '''buf��д����Կ���ϣ�һ���������'''
                key_source2_randomize_write(k2=ks->key_src, buf, session->opt->server)
                    key_source *k = &k2->client / &k2->server;
                    clear(*k)
                    if (!server)
                        '''out�в������������д�뵽buf��'''
                        random_bytes_to_buf(buf, out=k->pre_master, sizeof k->pre_master)
                    random_bytes_to_buf(buf, k->random1, sizeof k->random1)
                    random_bytes_to_buf(buf, k->random2, sizeof k->random2)
                '''session->opt->local_options = 
                       V4,dev-type tun,link-mtu 1553,tun-mtu 1500,proto UDPv4,
                       cipher BF-CBC,auth SM3,keysize 128,key-method 2,tls-client
                   '''
                write_string(buf, session->opt->local_options, TLS_OPTIONS_LEN)
                if (auth_user_pass_enabled || #auth_user_pass_enabledΪȫ�ֱ������������ã�Ϊ��
                    (auth_token.token_defined && auth_token.defined))
                    user_pass *up = &auth_user_pass;
                    '''maxlen<0ʱ�����޳���'''
                    write_string(buf, str = up->username, maxlen=-1)
                        len = strlen(str) + 1
                        buf_write_u16(buf, len)
                        buf_write(buf, str, len)
                    write_string(buf, up->password, maxlen=-1)
                    if (!session->opt->pull)  #�ͻ���ʱ��pullֵΪ��
                        purge_user_pass(&auth_user_pass, false);
                else
                    write_empty_string(buf) #��ʾû���û���
                    write_empty_string(buf) #��ʾû������
                push_peer_info(buf, session)
                    if (session->opt->push_peer_info_detail > 0) #����
                        "IV_VER=PACKAGE_VERSION\n" => buf
                        "IV_PLAT=win\n" => buf
                        "IV_PROTO=IV_PROTO_DATA_V2 | IV_PROTO_REQUEST_PUSH\n" => buf
                        "IV_CIPHERS=$(session->opt->config_ncp_ciphers)\n" => buf
                        if (!(opt->flags & COMP_F_ADVERTISE_STUBS_ONLY))
                            "IV_LZ4=1\n" => buf
                            "IV_LZ4v2=1\n" => buf
                            "IV_LZO=1\n" => buf
                            "IV_COMP_STUB=1\n" => buf
                            "IV_COMP_STUBv2=1\n" => buf
                            "IV_TCPNL=1\n" => buf
                        ... => buf
                    else
                        write_empty_string(buf)   #no peer info 
                '''���������TLS server�������tunnel keys ��
                   ���������һ������NCP��p2mp��������
                   ��һ����Կ�����ɻᱻ�Ƴٵ����ӽű���ɺ�NCPѡ����Ա�����֮��
                   ��Ϊ�����Ƿ��������ӽű�ѡ�����֮��
                   CAS_SUCCEEDED״̬��NCPѡ�������ͬ������û�ж����NCP���״̬��
                   '''
                if (session->opt->server && 
                    (session->opt->mode != MODE_SERVER || 
                     multi->multi_state == CAS_SUCCEEDED) )
                    if (ks->authenticated > KS_AUTH_FALSE)
                        tls_session_generate_data_channel_keys(session)
            state_change = true;
            ks->state = S_SENT_KEY;
        '''��buf����ָ���ı�������(Ϊ�˶�ȡKey��'''
        buf = &ks->plaintext_read_buf;
        if (buf->len && ( (ks->state == S_SENT_KEY && !session->opt->server)
                          || (ks->state == S_START && session->opt->server) ) )
            ������
        '''��buf����ָ���ı�д��������Ϊ�˽�Ҫ������ı�д��tls��'''
        buf = &ks->plaintext_write_buf;
        if (buf->len)
            '''�ͻ��˵ĵ�һ��Client Hello�������Ǵ����������'''
            key_state_write_plaintext(&ks->ks_ssl, buf);
        '''��Ҫ��������ݷŵ����Ų���'''
        if (ks->state >= S_START)
            //��send_reliable��Ѱ��һ�����е�reliable_entry��ȡ����buf
            buf = reliable_get_buf_output_sequenced(ks->send_reliable);
                int status = key_state_read_ciphertext(&ks->ks_ssl, buf, PAYLOAD_SIZE_DYNAMIC(&multi->opt.frame));
                    '''ks_ssl->ct_out Ϊ key_state_ssl �ṹ����Աֵ�У�
                       SSL *ssl;     /* SSL object -- new obj created for each new key */
                       BIO *ssl_bio; /* read/write plaintext from here */
                       BIO *ct_in;   /* write ciphertext to here */
                       BIO *ct_out;  /* read ciphertext from here */
                       ֮ǰ�Ĵ������й�����Щ��Ա�����ĳ�ʼ������
                       �����Ǵ�tls���ȡ���ܵ����ݣ�������Ϊtls���ܺ�ģ�
                       '''
                    return bio_read(ks_ssl->ct_out, buf, maxlen, "tls_read_ciphertext");
                if (status == 1)  #��ssl�����������
                    '''��send_reliable->array[]���ҵ���buf��Ӧ���Ǹ� reliable_entry����Ϊ e
                       e->packet_id = rel->packet_id++;
                       buf_write_prepend(buf, e->packet_id)
                       e->active = true;
                       e->opcode = P_CONTROL_V1;
                       e->next_try = 0;
                       e->timeout = rel->initial_timeout;
                       '''
                    reliable_mark_active_outgoing(ks->send_reliable, buf, opcode=P_CONTROL_V1)
                        �� 
                    state_change = true;
        +������
    '''���to_link��û��Ҫ���͵����ݣ��� ks->rec_ack ��Ϊ�գ��յ�����Ӧ����'''
    +if (!to_link->len && !reliable_ack_empty(ks->rec_ack))
        buffer buf = ks->ack_write_buf;
        buf_init(&buf��...)
        '''������Ӧ��
           ע���ͻ��˷����� P_ACK_V1 ����Я����Կ���ϣ�������˾ͻᷢ�� ssl ��� Client Hello
           Ȼ��ͻ��˻�Ӧ Server Hello���Ӷ��໥֮�佨����ssl����
           '''
        write_control_auth(session, ks, &buf, to_link_addr, opcode=P_ACK_V1,
                           max_ack=RELIABLE_ACK_SIZE, prepend_ack=false);
            @write_control_auth
        *to_link = buf;
        active = true;
    '''����õ�wakeupʱ��'''
    +if (ks->state >= S_INITIAL)
        '''ks->send_reliable���ҵ�����Ĵ��㷢�͵�reliable_entry������ʱ����wakeup'''
        compute_earliest_wakeup(wakeup,reliable_send_timeout(ks->send_reliable))
        '''���wakeup��ֵ����ks->must_negotiate��ʱ�䣬����Ϊks->must_negotiateָ����ʱ��'''
        compute_earliest_wakeup(wakeup, ks->must_negotiate - now);
        '''����Ѿ����������ӣ�wakeup������Э��ʱ�䣨renegotiate_seconds�����Աȣ�wakeup=���н�����'''
        if (ks->established && session->opt->renegotiate_seconds)
            ������
        ��� wakeup ��ֵ <=0 ��wakeup = 1�� active = true;
    +return active;
    error:  return false;
+&<ovpn����Э�������>
    #packet opcode (high 5 bits) and key-id (low 3 bits) are combined in one byte 
    ��define P_KEY_ID_MASK                  0x07
    ��define P_OPCODE_SHIFT                 3
    #packet opcodes -- the V1 is intended to allow protocol changes in the future 
    ��define P_CONTROL_HARD_RESET_CLIENT_V1 1     /* initial key from client, forget previous state */
    ��define P_CONTROL_HARD_RESET_SERVER_V1 2     /* initial key from server, forget previous state */
    ��define P_CONTROL_SOFT_RESET_V1        3     /* new key, graceful transition from old to new key */
    ��define P_CONTROL_V1                   4     /* control channel packet (usually TLS ciphertext) */
    ��define P_ACK_V1                       5     /* acknowledgement for packets received */
    ��define P_DATA_V1                      6     /* data channel packet */
    ��define P_DATA_V2                      9     /* data channel packet with peer-id */
    #indicates key_method >= 2 
    ��define P_CONTROL_HARD_RESET_CLIENT_V2 7     /* initial key from client, forget previous state */
    ��define P_CONTROL_HARD_RESET_SERVER_V2 8     /* initial key from server, forget previous state */
    #indicates key_method >= 2 and client-specific tls-crypt key
    ��define P_CONTROL_HARD_RESET_CLIENT_V3 10    /* initial key from client, forget previous state */
    #define the range of legal opcodes, Since no longer support key-method 1, consider the v1 op codes invalid 
    ��define P_FIRST_OPCODE                 3
    ��define P_LAST_OPCODE                  10

            
===========================================================================================================     
                
+�������ݽṹ
    multi_instance *mi->context.c2.es
    multi_instance *mi->context.c2.tls_multi.es
    session->opt->es
    tls_multi *multi->opt.es        
    
    +&<multi_context>
    #�洢openvpn�ķ���״̬�Ľṹ��ֻ�ڷ����ʹ�ã��洢����vpn����ͽ��̼���״̬
    struct multi_context multi
    /{
        #MC_UNDEF(0)��MC_SINGLE_THREADED��1����MC_MULTI_THREADED_MASTER��2��
        #MC_MULTI_THREADED_WORKER��4����MC_MULTI_THREADED_SCHEDULER��8��
        int thread_mode;
        #multi_instance��������飬��Ա��ͨ��peer-id��Ϊ�±�����������ֱ��Ӧһ������
        struct multi_instance **instances;
        #��vpn���ʵ��֮ǰ��������ͨ������buffer�ļ���
        struct mbuf_set *mbuf;   #�㲥/�鲥�������б�
        #OpenVPN ���ض�״̬--ʹ�� TCP ��Ϊ�ⲿ����ʱ���ֱ��Ӧһ������
        struct multi_tcp *mtcp;
        #��ǰ��֤���Ŀͻ��˵�����
        int n_clients;
        #�洢�˽��̼���������Ϣ
        struct context top;
        #�����������ڻ���ʱ��Ļ����¼�
        struct schedule *schedule;  #schedule����Ҫ��Ա��ʱ������ȼ�
        #���֧�ֶ��ٸ�����
        int max_clients;
        #����֤ͨ����������
        int n_clients;
        ������
    /}
    
    +&<multi_instance>
    #������ģʽ�£����ڴ洢һ��vpn�����״̬�Ľṹ
    struct multi_instance
    /{
        #��vpn���ʵ����ʲôʱ�򴴽���
        time_t created;
        #server/tcpģʽ�£�Ҫ���������ݵĶ���
        struct mbuf_set *tcp_link_out_deferred;
        struct context context;  #�洢��vpn�����״̬
        ������
    /}
    
    +&<context>
    #�ýṹ������һ��vpn��������ڴ洢һ�������״̬��Ϣ
    #��Ҳ����һЩ���̼�������ݣ���������ѡ��
    struct context
    /{
        #���main��ѭ���ĵ�һ�ε���
        bool first_time;
        #�������л������ļ��л�ȡ��ѡ��
        struct options options; 
        #���context��openvpn�����еĽ�ɫ��
        #������CM_P2P��0,�ͻ��ˣ���CM_TOP��1,����ˣ���CM_TOP_CLONE��2,�߳��¿�¡��CM_TOP��
        #CM_CHILD_UDP��3,CM_TOP����context����CM_CHILD_TCP��4,CM_TOP����context��
        int mode;   
        #��Ż�������
        struct env_set *es; 
        #����api͸����context
        openvpn_net_ctx_t net_ctx;
        #��ͬ��������context�ṹ
        struct context_0 *c0;       
        struct context_1 c1;        
        struct context_2 c2;       
        ������
    /}
    
    +&<context_1>
    #�ýṹ������״̬����SIGUSR1�����źŵ�Ӱ�죬������SIGHUP�����źŶ�����
    struct context_1
    /{
        #���غ�Զ�˵ĵ�ַ
        struct link_socket_addr link_socket_addr;
        #����ĻỰ��Կ
        struct key_schedule ks;
        #Ԥ�����򻺴��������
        struct cached_dns_entry *dns_cache;
        #tun/tap��������ӿڶ���
        struct tuntap *tuntap; 
        #�Ƿ����ŵ�ǰcontext�����������
        bool tuntap_owned;  
        #·����Ϣ�б���--route����ѡ��
        struct route_list *route_list;
        #http�������
        struct http_proxy_info *http_proxy;
        #socks�������
        struct socks_proxy_info *socks_proxy;
        #��֤�õ��û�������
        struct user_pass *auth_user_pass;
        #�����ļ��е�����ͨ�������֤
        const char *authname;
    /}
    
    +&<context_2>
    #�洢����SIGHUP��SIGUSR1�źŵ��µġ�������������״̬��Ϣ
    struct context_2
    /{
        #������Զ�˽���tcp/udp���ӵ�socket��link_socket��Windows��linux��socket��͸��ʵ�֣�
        struct link_socket *link_socket;   
        #Զ�˵�ip��ַ
        struct link_socket_actual *to_link_addr;
        #���������ݰ��ĵ�ַ
        struct link_socket_actual from; 
        #���MUT֡����
        struct frame frame; 
        #tlsģʽ������󣬴洢vpn�����tls״̬��Ϣ,ע��tls_multi����ֻ�ᴴ��һ����������һ���б�
        struct tls_multi *tls_multi;
        #���˱���ƥ���ѡ���ַ���
        char *options_string_local;
        char *options_string_remote;
        #���ڴ������buffer
        struct context_buffers *buffers;
        #���������buffer����ʵ�ʷ����ڴ棬����ָ������� buffers
        struct buffer buf;
        struct buffer to_tun;
        struct buffer to_link;
        #�ڶ�link��tunʱ�ȴ����
        struct timeval timeval;
        #�־��ȶ�ʱ�����´λ���ʱ��
        time_t coarse_timer_wakeup
        #Ҫ�����ű��Ļ�������
        struct env_set *es;
        bool es_owned;
        ������
    /}
        
    +&<tls_multi>
    #���� TLS ����������еĻ VPN �����һ��tls_multi����
    #���д洢���п���ͨ��������ͨ����ȫ����״̬��
    #�˽ṹ���԰������������ͬʱ���ڻ״̬��tls_context����
    #�������ڻỰ����Э���ڼ�������жϵ�ת����
    #ÿ��tls_context����һ������ͨ���Ự��
    #�ûỰ���Կ�Խ�洢��key_state�ṹ�еĶ������ͨ����ȫ�����Ự��
    struct tls_multi
    /{
         #����ѡ���������Ϣ
        struct tls_options opt;
        #���б��ᱻ����ͨ��ɨ��
        #KEY_SCAN_SIZE=3����һ����"active key", 
        #�ڶ�������"active key"�� session_id ������ lame_duck ��ͣ�õ�key
        #�����������ڷ����lame_duck�Ự��
        #�������ֻ����������Э�̻Կ��ʧ�ܣ���lame_duckԿ����Ȼ��Ч������¡�
        struct key_state *key_scan[KEY_SCAN_SIZE];  #ָ���Ӧsession��key��Ա
        #ӵ��3(TM_SIZE)��tls_session����
        #��һ��(TM_ACTIVE)�ǵ�ǰ�ģ�tls��֤����
        #�ڶ���(TM_UNTRUSTED)ӵ�д����¿ͻ��˵��������������֤�ɹ�����۶ᵱǰsession
        #������(TM_LAME_DUCK)��һ���ֿ⣺��session��Ϊ��������ã���Lame duck keys��û����
        #    Lame duck keys���ڱ����ڱ���key������Э��ʱ������ͨ�����ӵĳ�����
        struct tls_session session[TM_SIZE];
        #��ǰ�Ѿ�Э�̵ĻỰ������
        int n_sessions; 
        #�ӶԶ˵Ŀ���ͨ���Ͻ��յĶ���ͨ����Ϣ�ַ���
        char *peer_info;
        ������
    /}
    
    +&<key_state>
    #�洢������ͨ����tls״̬������ͨ��������״̬��
    #�������ˡ����Ų�ṹ��--���ڿ���ͨ������Ϣ[����]
    struct key_state
    /{
        #�ӿͻ��˷��͵������֤���Ƶ�״̬
        int state;
        #key_state��id���̳���tls_session
        int key_id;
        #����ssl����Ϳ���ͨ����BIO����
        struct key_state_ssl ks_ssl;
        #�Զ˵�����ĻỰid
        struct session_id session_id_remote; 
        #����һ�������İ��ĸ�����֪���յ�ACK�ظ�
        struct reliable *send_reliable; 
        #�Զ˵�ip��ַ
        struct link_socket_actual remote_addr;
        #����ͨ��������ѡ��
        struct crypto_options crypto_options
        #�����Ǵ��ݸ� TLS ֮ǰ�Դ�����������ݰ���������
        struct reliable *rec_reliable; 
        #��������Ҫ�ظ��������ߵ����а�id
        struct reliable_ack *rec_ack
        #ʲôʱ��state��ΪS_ACTIVE��
        time_t established;         
        #�����ʱ��֮ǰ��û�����ԿЭ�̣�����Ϊ��ʱ
        time_t must_negotiate;   
        #�ö��������ʱ��ʱ����
        time_t must_die;         
        ������
    /}
    
    +&<tls_session>
    #�洢һ���Ự�İ�ȫ������Ϣ���Ự���������
    #�ýṹ��Ӧһ��vpn�Ķ˵��˵Ŀ���ͨ��session
    struct tls_session
    /{
        struct tls_options *opt;  #����ѡ���������Ϣ
        struct session_id session_id;  #�����
        ''' during hard reset used to control burst retransmit '''
        bool burst;
        ''' authenticate control packets '''
        struct tls_wrap_ctx tls_wrap;
        int initial_opcode;         ''' our initial P_ opcode '''
        ''' The current active key id, used to keep track of renegotiations.
            key_id increments with each soft reset to KEY_ID_MASK then recycles back
            to 1.  This way you know that if key_id is 0, it is the first key.
        '''
        int key_id; #���Ը���renegotiations
        int limit_next;             ''' used for traffic shaping on the control channel '''
        int verify_maxlevel;
        char *common_name;
        struct cert_hash_set *cert_hash_set;
        uint32_t common_name_hashval;
        bool verified;              ''' true if peer certificate was verified against CA '''
        ''' not-yet-authenticated incoming client '''
        struct link_socket_actual untrusted_addr;
        struct key_state key[KS_SIZE];    //@key_state  @:key_state
    /}
    
    '''��¼��Կ���Խ����Ϣ
       �ýṹ��Ա�ĳ�ʼ������Ҫ��do_init_crypto_tls::do_init_crypto_tls_c1�����
       '''
    +&<key_schedule>
    {
        '''��¼������ʲôcipher����ָ�ԳƼ����㷨����HMAC�㷨����Կ��С'''
        struct key_type key_type;  #����ǶԳƼ����õ����ݽṹ
        '''Ԥ����ľ�̬��Կ�����ļ��ж�ȡ'''
        struct key_ctx_bi static_key;
        '''ȫ���õ� SSL context'''
        struct tls_root_ctx ssl_ctx;
        '''������Щ���ڶ� TLS ����ͨ�����ݵİ�װ����ѡ����
           ��Ӧ--tls-auth/--tls-crypt
           ��֮���������ݽṹ�� :
           tls_options.tls_wrap
           tls_auth_standalone.tls_wrap (����ˣ�
           tls_multi.opt.tls_wrap
           ע��
               key_type�а���cipher_kt_t��md_kt_t�ȳ�Ա�ṹ
               ��key_ctx�а���cipher_ctx_t��hmac_ctx_t�ȳ�Ա�ṹ
               ���ǵĹ�ϵ�ǣ�cipher_ctx_t�г��˰���cipher_kt_t��
               �����������õ�������ز�����������������ݵļ���
           '''
        struct key_type tls_auth_key_type;  #�����ʹ����֤��ʱ���õ������ݽṹ
        struct key_ctx_bi tls_wrap_key;   #�����ʹ����֤��ʱ���õ������ݽṹ
        struct key_ctx tls_crypt_v2_server_key;
        struct buffer tls_crypt_v2_wkc;            ''' Wrapped client key'''
        struct key_ctx auth_token_key;
    };
    
    '''���ڼ�¼�����¼��Ľṹ'''
    +&<win32_signal>
    {
        #define WSO_MODE_UNDEF   0
        #define WSO_MODE_SERVICE 1
        #define WSO_MODE_CONSOLE 2
        int mode;
        struct rw_handle in;
        DWORD console_mode_save;
        bool console_mode_save_defined;
    };
    
    +&<rw_handle>
    {
        HANDLE read;
        HANDLE write;
    };
    
    
+&<�ṹ����ʹ�����׷��>
    +main�е� context c; 
        ����������
        ������
        ������־
        ���������ϵͳ
        ���𻷾�����
    
    +tunnel_server_udp_single_threaded�е� context c ��ָ��main�е� context c��
        ����context_2
            ��context_2��es�̳�main��context�Ļ�������
            ����context_2��link_socket
        ����sig�ź�
        ����context_1
        ����������
    
    +tunnel_server_udp_single_threaded�е� multi_context multi;
        ����context top����ʼ��multi
        �̳�context top����������һЩֵ�����޸�
            mode��ΪCM_TOP_CLONE����ֹclose_instance�رո������Դ�����
            first_time = false
            c0 = null
            c2.tls_multi = null
            c1.xxx_owned = false
            c2.xxx_owned = false
            ...
        
        
+tunnel_server����ѭ��  #&<tunnel_server����ѭ��>
    tunnel_server_udp_single_threaded(context *top)
        multi_context multi;
        '��ʼ������context��c2'
        top->mode = CM_TOP;
        context_clear_2(top)
        '��ʼ��һ�����ʵ����'
        '�����linux���������ڳ�ʼ�����ʵ�������е��źŲ�����'
        '���ʵ����ʼ��ǰ������ֻ����SIGINT��SIGTERM�ź�'
        '���ʵ����ʼ����ɺ����Ӳ���SIGNHUP��SIGUSR1��SIGUSR2'
        init_instance_handle_signals(top, top->es, CC_HARD_USR1_TO_HUP);
            '''
            ��top.c2.es�̳�top.es
            ���ʹ����management������������ͣһ������ʱ�����ȴ��ͻ�����
            ����top.options.connection_list������top.options.ce 
            ��ʼ�����
            ��top.c1.status_outputά������--status�ļ�
            ��top.c1.ifconfig_pool_persistά������ ifconfig-pool �־û�����
            ����������top.c1.http_proxy
            ����������top.c1.socks_proxy
            ����top.c2.link_socket
            ����������top.c2.fragment������top.c2.frame��
            ����������top.c1.ks.ssl_ctx   //ȫ�� SSL context
            ����������top.c1.ks.key_type  //���������cipher��HMACժҪ��key����
            �޸�top.c2.frame.extra_frame��ֵ
            ����������top.c2.tls_multi��top.c2.tls_auth_standalone
            ��ʼ����top.c2.link_socket
            ����������top.c1.tuntap
            ����top.c1.route_list��·�ɱ�
            ��ʼ��top.c1.route_list
            ����top.c1.tuntap.hand������tap/tun�豸����������tun/tap�豸��ip��
            ���������management���ȴ��ͻ����ӣ�����sleep(n=10)��
            ����top.c1.tuntap��tun/tap�豸����mtu��   
            ����up_script�ű������ݲ�������top.c2.es��������������֮תΪ�ַ��������ű���
            ���ܻ���ѡ��Ϊtop.c1.tuntap���·�ɺ�/�����route_script·�ɽű�
            ����top.c2.server_poll_interval���ö�ʱ������http/socks�������ã�
            �ٴ�����c->c2.link_socket����������tcp/udp���ӻ����--�󶨱��أ�
            '''
        multi_init
            '''
            multi.thread_mode=MC_SINGLE_THREADED
            ���� multi.hash��multi.vhash��multi.iter��multi.cid_hash��multi.schedule
            ���� multi.mbuf  //����㲥/�鲥�������б�254����
            ���� multi.ifconfig_pool  //����һ��ifconfig�أ�252��
            ���� multi.ifconfig_pool  //�� t->c1.ifconfig_pool_persist �ļ��м��س�����
            ���� multi.route_helper
            ���� multi.reaper
            ���� multi.local , ���� top.c1.tuntap->local
            ���� multi.max_clients = topo.options.max_clients = 1024
            ���� multi.instances �� 1024��
            ���� multi.mtcp ��ֻ��tcpģʽ���� 1024 ��
            '''
         multi_top_init   
            '''
            multi.top �̳� top����������һЩֵ�����޸�:
            multi.top.mode��ΪCM_TOP_CLONE����ֹclose_instance�رո������Դ�����
            multi.top.first_time = false
            multi.top.c0 = null
            multi.top.c2.tls_multi = null
            multi.top.c1.xxx_owned = false
            multi.top.c2.xxx_owned = false
            ���� multi.top.c2.buffers  // ���� top.c2.frame
                ...
            '''
        ������
        while(true)
            multi_get_timeout
                '''
                ��multi.schedule���ҵ��������ѵ�instance����¼��multi.earliest_wakeup��
                ��������ʱ���뵱ǰʱ��Ĳ�ֵ���������10�룬����Ϊ10�룩���multi.top.c2.timeval��
                ��ֵ������������link/tun�ϵȶ��
                ����Ӵ�multi.schedule�л�ȡʧ�ܣ���multi.top.c2.timeval����Ϊ10s��REAP_MAX_WAKEUP��
                '''
            io_wait
                p2mp_iow_flags(multi)
                '''
                ����flags
                    flags = IOW_WAIT_SIGNAL
                    ��� multi.mbuf ��Ϊ�� ��flags |= IOW_MBUF, ���� flags |= IOW_READ
                    ��� multi.top.c1.tuntap �Ƿ�Ϊ WINDOWS_DRIVER_WINTUN�� �ǣ�
                        ����豸�� ring �Ƿ�Ϊ�գ��ǣ�
                            ȥ�� flags �е� IOW_READ_TUN
                '''
                io_wait_dowork
                    event_reset
                    '''
                    ((we_set*)multi.top.c2.event_set)->n_event = 0
                    '''
                    wait_signal
                    '''
                    ((we_set*)multi.top.c2.event_set)->events[n_event] = &win32_signal.in->read
                    ((we_set*)multi.top.c2.event_set)->esr[n_events].rwflags = EVENT_READ
                    ((we_set*)multi.top.c2.event_set)->esr[n_events].arg = (void *)&err_shift=4
                    '''
                    (this)
                    '''
                    ��� flags ���� IOW_TO_LINK ������
                    ��� flags ������ IOW_FRAG �� multi.top.c2.fragment->outgoing.len Ϊ 0��
                        ��� flags ���� IOW_READ_TUN �����㣩�� int tuntap |= EVENT_READ
                    ��� flags ���� IOW_TO_TUN �� tuntap |= EVENT_WRITE �������� flags ���� IOW_READ_LINK , �� int socket |= EVENT_READ 
                    ��� flags ���� IOW_MBUF�� socket |= EVENT_WRITE
                    ��� flags ���� IOW_READ_TUN_FORCE�� tuntap |= EVENT_READ
                    '''
                    socket_set
                    '''
                    ����socket��ֵ������ multi.top.c2.link_socket��
                        ��� socket ���� EVENT_READ ��������������ӵģ���Ҫ����Щ��������ǰ�ù�����
                            ��� sock->reads.iostate  == IOSTATE_INITIAL��0�� ������
                            (we_set*)multi.top.c2.event_set)->events[n_event] = multi.top.c2.link_socket.rw_handle.read
                            ((we_set*)multi.top.c2.event_set)->esr[n_events].rwflags = EVENT_READ
                            ((we_set*)multi.top.c2.event_set)->esr[n_events].arg = (void *)&socket_shift=0
                    '''
                    tun_set
                    '''
                    (we_set*)multi.top.c2.event_set)->events[n_event] = multi.top.c1.tuntap.rw_handle.read
                    ((we_set*)multi.top.c2.event_set)->esr[n_events].rwflags = EVENT_READ
                    ((we_set*)multi.top.c2.event_set)->esr[n_events].arg = (void *)&tun_shift=2
                    if (multi.top.c1.tuntap.reads.iostate == IOSTATE_INITIAL)
                        �����첽��tun/tap�豸�����ö��������ݷ��� multi.top.c1.tuntap.reads.buf
                        �����������ʧ�ܣ�����ԭ���ǣ�ERROR_IO_PENDING���ص� I/O �����ڽ����У���
                        ������ multi.top.c1.tuntap.reads.iostate = IOSTATE_QUEUED
                    '''
                    (this)
                    '''
                    ���û�� multi.top.sig.signal_received �ϲ����ź�
                        ��� flags ������ IOW_CHECK_RESIDUAL
                            event_wait
                                �ȴ� (we_set*)multi.top.c2.event_set)->events
                                ���ĳ�� event �������ˣ��� out ���������¼ ((we_set*)multi.top.c2.event_set)->esr[?].arg 
                                int status = ���ش������¼�����
                                ��� status > 0  , ���� multi.top.c2.event_set_status ����Ӧλ
                                ��� status = 0 , ���� multi.top.c2.event_set_status = ES_TIMEOUT
                    '''
            MULTI_CHECK_SIG(&multi);
                '''
                ����źţ��ж��Ƿ�Ӧ���ж�ѭ��
                '''
            multi_process_per_second_timers
                '''
                ����ÿ�붨ʱ��
                    �� multi.ifconfig_pool ��д�� multi.top.c1.ifconfig_pool_persist �ļ�
                    ������
                '''
            if (multi.top.c2.event_set_status == ES_TIMEOUT)
                multi_process_timeout 
            else
                multi_process_io_udp
                    '''
                    ���� multi.top.c2.event_set_status ��
                    ���� MANAGEMENT_READ|MANAGEMENT_WRITE �¼�
                    ���� SOCKET_READ �¼�
                    ���� SOCKET_WRITE �¼�
                    ���� TUN_READ �¼�
                        read_incoming_tun
                            �ȴ���ɶ˿ڣ����Ƿ������
                            multi.top.c2.buf = multi.c1.tuntap.reads.buf
                            multi.top.c1.tuntap.reads.iostate = IOSTATE_INITIAL
                        multi.top.sig.signal_received û���յ��źţ�Ϊ0��
                            multi_process_incoming_tun
                                ��� multi.top.c2.buf ��Ϊ��
                                    ���� multi.top.c2.buf �ϵ�ԭʼ���ݰ�����ȡԴ��ַ��Ŀ���ַ
                                    ���Ŀ���ַ�Ƕಥ��㲥�� ������
                                    ���򣬡�����
                    ���� TUN_WRITE �¼�
                    '''
                    
+tuntap��link�ֱ�����γ�ʼ����                    
    c.c2.link_socket�ĳ�ʼ��
        openvpn_main
            tunnet_server
                tunnel_server_udp
                    tunnel_server_udp_single_threaded
                        init_instance_handle_signals
                            init_instance
                                do_link_socket_new(c)
                                    c.c2.link_socket = link_socket_new()
                                do_init_socket_1(c,link_socket_mode)
                                    link_socket_init_phase1(
                                                c->c2.link_socket,
                                                c->options.ce.local,
                                                c->options.ce.local_port,
                                                c->options.ce.remote,
                                                c->options.ce.remote_port,
                                                c->c1.dns_cache,
                                                c->options.ce.proto,
                                                c->options.ce.af,
                                                c->options.ce.bind_ipv6_only,
                                                mode,
                                                c->c2.accept_from,
                                                c->c1.http_proxy,
                                                c->c1.socks_proxy,
                                                #ifdef ENABLE_DEBUG
                                                c->options.gremlin,
                                                #endif
                                                c->options.ce.bind_local,
                                                c->options.ce.remote_float,
                                                c->options.inetd,
                                                &c->c1.link_socket_addr,
                                                c->options.ipchange,
                                                c->plugins,
                                                c->options.resolve_retry_seconds,
                                                c->options.ce.mtu_discover_type,
                                                c->options.rcvbuf,
                                                c->options.sndbuf,
                                                c->options.mark,
                                                c->options.bind_dev,
                                                &c->c2.server_poll_interval,
                                                sockflags);
                                        �������������c->c2.link_socket����Ӧ��
                                        if (sock->bind_local)
                                            resolve_bind_local(sock, sock->info.af);
                                                if (!sock->info.lsa->bind_local)
                                                    status = get_cached_dns_entry(sock->dns_cache,
                                                                                  sock->local_host,
                                                                                  sock->local_port,
                                                                                  af,
                                                                                  flags,
                                                                                  &sock->info.lsa->bind_local);
                                                        ���� sock->dns_cache ��
                                                            ���ĳһ�����س�Ա������ĸ�����ƥ����
                                                            ��Ѹ����ai��Ա������һ��������������0
                                                            ���򣬷���-1
                                                    ��� status ��Ϊ 0
                                                        status = openvpn_getaddrinfo(flags, 
                                                                                     sock->local_host=0.0.0.0, 
                                                                                     sock->local_port=1194, 
                                                                                     0,
                                                                                     NULL, 
                                                                                     af, 
                                                                                     &sock->info.lsa->bind_local);
                                                            ���� getaddrinfo�����ݲ�������� addrinfo �ṹ��������һ������
                                do_init_socket_2(c)
                                    link_socket_init_phase2
                                        socket_frame_init
                                            Ϊsocket��read/write��ɶ˿ڵ�overlapped.hEvent�����¼�����
                                            ������sock->rw_handle��read/write��Ա�ֱ�ָ���������¼�����
                                            Ϊsocket��read/write��ɶ˿ڵ�buf_init�����ڴ�
                                            ���sock���������ӵ�
                                                stream_buf_init(sock->stream_buf,
                                                                &sock->reads.buf_init,
                                                                sock->sockflags,
                                                                sock->info.proto);
                                        if (sock->sd == SOCKET_UNDEFINED)
                                            if (sock->bind_local  && !sock->remote_host && sock->info.lsa->bind_local)
                                                create_socket(sock, sock->info.lsa->bind_local);
                                                    if (addr->ai_protocol == IPPROTO_UDP || addr->ai_socktype == SOCK_DGRAM)
                                                        sock->sd = create_socket_udp(addr, sock->sockflags);
                                                        if (sock->socks_proxy)
                                                            sock->ctrl_sd = create_socket_tcp(&addrinfo_tmp);
                                                    socket_set_buffers(sock->sd, &sock->socket_buffer_sizes);
                                                        ͨ�� setsockopt ���� sock->sd �Ķ�д��������С
                                                    bind_local(sock, addr->ai_family)
                                                        if (sock->bind_local)
                                                            socket_bind(sock->sd, 
                                                                        sock->info.lsa->bind_local,
                                                                        ai_family,
                                                                        "TCP/UDP", 
                                                                        sock->info.bind_ipv6_only);

+&<���ú궨��>
    +Tunnel types
        ��define DEV_TYPE_UNDEF 0
        ��define DEV_TYPE_NULL  1
        ��define DEV_TYPE_TUN   2    /* point-to-point IP tunnel */
        ��define DEV_TYPE_TAP   3    /* ethernet (802.3) tunnel */
    +TUN��������ʽ
        ��define TOP_UNDEF   0
        ��define TOP_NET30   1
        ��define TOP_P2P     2
        ��define TOP_SUBNET  3
    +enum proto_num 
        PROTO_NONE,     /* catch for uninitialized */
        PROTO_UDP,
        PROTO_TCP,
        PROTO_TCP_SERVER,
        PROTO_TCP_CLIENT,
        PROTO_N
    +context modes
        ��define CM_P2P            0  /* standalone point-to-point session or client */
        ��define CM_TOP            1  /* top level of a multi-client or point-to-multipoint server */
        ��define CM_TOP_CLONE      2  /* clone of a CM_TOP context for one thread */
        ��define CM_CHILD_UDP      3  /* child context of a CM_TOP or CM_THREAD */
        ��define CM_CHILD_TCP      4  /* child context of a CM_TOP or CM_THREAD */

+&<:tls_multi>
'''��1��tls_multi������TM_SIZE=3��tls_session��ÿ��tls_session��������KS_SIZE=2��key_state'''
/struct tls_multi
        struct tls_options opt;  &<:tls_options>
            ''' our master TLS context from which all SSL objects derived '''
            struct tls_root_ctx ssl_ctx;
            ''' data channel cipher, hmac, and key lengths '''
            struct key_type key_type;
            ''' true if we are a TLS server, client otherwise '''
            bool server;
            ''' if true, don't xmit until first packet from peer is received '''
            bool xmit_hold;
            ''' local and remote options strings
                that must match between client and server '''
            const char *local_options;
            const char *remote_options;
            ''' from command line '''
            bool replay;
            bool single_session;
            bool disable_occ;
            int mode;
            bool pull;
            int push_peer_info_detail;
            int transition_window;
            int handshake_window;
            interval_t packet_timeout;
            int renegotiate_bytes;
            int renegotiate_packets;
            interval_t renegotiate_seconds;
            ''' cert verification parms '''
            const char *verify_command;
            const char *verify_export_cert;
            int verify_x509_type;
            const char *verify_x509_name;
            const char *crl_file;
            bool crl_file_inline;
            int ns_cert_type;
            unsigned remote_cert_ku[MAX_PARMS];
            const char *remote_cert_eku;
            uint8_t *verify_hash;
            hash_algo_type verify_hash_algo;
            char *x509_username_field;
            ''' allow openvpn config info to be
                passed over control channel '''
            bool pass_config_info;
            ''' struct crypto_option flags '''
            unsigned int crypto_flags;
            int replay_window;                 ''' --replay-window parm '''
            int replay_time;                   ''' --replay-window parm '''
            bool tcp_mode;
            const char *config_ciphername;
            const char *config_ncp_ciphers;
            bool ncp_enabled;
            bool tls_crypt_v2;
            const char *tls_crypt_v2_verify_script;
            '''   TLS handshake wrapping state '''
            struct tls_wrap_ctx tls_wrap;
            struct frame frame;
            ''' used for username/password authentication '''
            const char *auth_user_pass_verify_script;
            bool auth_user_pass_verify_script_via_file;
            const char *tmp_dir;
            const char *auth_user_pass_file;
            bool auth_token_generate;   '''<Generate auth-tokens on successful
                                            user/pass auth,seet via
                                            options->auth_token_generate. '''
            bool auth_token_call_auth; '''< always call normal authentication '''
            unsigned int auth_token_lifetime;
            struct key_ctx auth_token_key;
            ''' use the client-config-dir as a positive authenticator '''
            const char *client_config_dir_exclusive;
            ''' instance-wide environment variable set '''
            struct env_set *es;
            openvpn_net_ctx_t *net_ctx;
            const struct plugin_list *plugins;
            ''' compression parms '''
            ��ifdef USE_COMP
            struct compress_options comp_options;
            ��endif
            ''' configuration file SSL-related boolean and low-permutation options '''
            ��define SSLF_CLIENT_CERT_NOT_REQUIRED (1<<0)
            ��define SSLF_CLIENT_CERT_OPTIONAL     (1<<1)
            ��define SSLF_USERNAME_AS_COMMON_NAME  (1<<2)
            ��define SSLF_AUTH_USER_PASS_OPTIONAL  (1<<3)
            ��define SSLF_OPT_VERIFY               (1<<4)
            ��define SSLF_CRL_VERIFY_DIR           (1<<5)
            ��define SSLF_TLS_VERSION_MIN_SHIFT    6
            ��define SSLF_TLS_VERSION_MIN_MASK     0xF  ''' (uses bit positions 6 to 9) '''
            ��define SSLF_TLS_VERSION_MAX_SHIFT    10
            ��define SSLF_TLS_VERSION_MAX_MASK     0xF  ''' (uses bit positions 10 to 13) '''
            ��define SSLF_TLS_DEBUG_ENABLED        (1<<14)
            unsigned int ssl_flags;
            ��ifdef MANAGEMENT_DEF_AUTH
            struct man_def_auth_context *mda_context;
            ��endif
            const struct x509_track *x509_track;
            ��ifdef ENABLE_MANAGEMENT
            const struct static_challenge_info *sci;
            ��endif
            ''' --gremlin bits '''
            int gremlin;
            ''' Keying Material Exporter [RFC 5705] parameters '''
            const char *ekm_label;
            size_t ekm_label_size;
            size_t ekm_size;        
        struct key_state *key_scan[KEY_SCAN_SIZE];  &<:key_state>
            int state;
            '''The state of the auth-token sent from the client '''
            int auth_token_state_flags;
            ''' Key id for this key_state,  inherited from struct tls_session.
                @see tls_session::key_id.'''
            int key_id;
            struct key_state_ssl ks_ssl; '''contains SSL object and BIOs for the control channel '''
                SSL *ssl;                   ''' SSL object -- new obj created for each new key '''
                BIO *ssl_bio;                       ''' read/write plaintext from here '''
                BIO *ct_in;                 ''' write ciphertext to here '''
                BIO *ct_out;                        ''' read ciphertext from here '''
            time_t established;         '''when our state went S_ACTIVE '''
            time_t must_negotiate;      '''key negotiation times out if not finished before this time '''
            time_t must_die;            '''this object is destroyed at this time '''
            int initial_opcode;         '''our initial P_ opcode '''
            struct session_id session_id_remote; '''peer's random session ID '''
                uint8_t id[8];
            struct link_socket_actual remote_addr; &<:link_socket_actual> '''peer's IP addr '''
                struct openvpn_sockaddr dest;
                    union {
                        struct sockaddr sa;
                        struct sockaddr_in in4;
                        struct sockaddr_in6 in6;
                    } addr;
            struct crypto_options crypto_options;'''data channel crypto options '''
                struct key_ctx_bi key_ctx_bi;
                '''< OpenSSL cipher and HMAC contexts for
                     both sending and receiving
                     directions. '''
                struct packet_id packet_id; '''< Current packet ID state for both
                                                 sending and receiving directions. '''
                struct packet_id_persist *pid_persist;
                '''< Persistent packet ID state for
                     keeping state between successive
                     OpenVPN process startups. '''
                ��define CO_PACKET_ID_LONG_FORM  (1<<0)
                '''< Bit-flag indicating whether to use
                    OpenVPN's long packet ID format. '''
                ��define CO_IGNORE_PACKET_ID     (1<<1)
                '''< Bit-flag indicating whether to ignore
                     the packet ID of a received packet.
                     This flag is used during processing
                     of the first packet received from a
                     client. '''
                ��define CO_MUTE_REPLAY_WARNINGS (1<<2)
                '''< Bit-flag indicating not to display
                     replay warnings. '''
                unsigned int flags;         '''< Bit-flags determining behavior of
                                                 security operation functions. '''
            struct key_source2 *key_src;       '''source entropy for key expansion '''
                struct key_source client;   '''< Random provided by client. '''
                    uint8_t pre_master[48];     '''< Random used for master secret
                                                     generation, provided only by client
                                                     OpenVPN peer. '''
                    uint8_t random1[32];        '''< Seed used for master secret
                                                     generation, provided by both client
                                                     and server. '''
                    uint8_t random2[32];        '''< Seed used for key expansion, provided
                                                     by both client and server. '''
                struct key_source server;   '''< Random provided by server. '''
            struct buffer plaintext_read_buf;
            struct buffer plaintext_write_buf;
            struct buffer ack_write_buf;
            struct reliable *send_reliable; '''holds a copy of outgoing packets until ACK received '''
            struct reliable *rec_reliable; '''order incoming ciphertext packets before we pass to TLS '''
            struct reliable_ack *rec_ack; '''buffers all packet IDs we want to ACK back to sender '''
            struct buffer_list *paybuf;
            counter_type n_bytes;                '''how many bytes sent/recvd since last key exchange '''
            counter_type n_packets;              '''how many packets sent/recvd since last key exchange '''
            ''' If bad username/password, TLS connection will come up but 'authenticated' will be false.'''
            enum ks_auth_state authenticated;
            time_t auth_deferred_expire;
            ��ifdef MANAGEMENT_DEF_AUTH
            unsigned int mda_key_id;
            unsigned int mda_status;
            ��endif
            ��ifdef PLUGIN_DEF_AUTH
            unsigned int auth_control_status;
            time_t acf_last_mod;
            char *auth_control_file;
            ��endif
        '''<List of key_state objects in the
              order they should be scanned by data
              channel modules. '''
        ''' used by tls_pre_encrypt to communicate the encrypt key
            to tls_post_encrypt()'''
        struct key_state *save_ks;  ''' temporary pointer used between pre/post routines '''
        ''' Used to return outgoing address from tls_multi_process.'''
        struct link_socket_actual to_link_addr;
            struct openvpn_sockaddr dest;
                union {
                    struct sockaddr sa;
                    struct sockaddr_in in4;
                    struct sockaddr_in6 in6;
                } addr;
        int n_sessions;             '''< Number of sessions negotiated thus far. '''
        enum client_connect_status multi_state;
            enum client_connect_status {
                CAS_SUCCEEDED=0,
                CAS_PENDING,
                CAS_PENDING_DEFERRED,
                CAS_PENDING_DEFERRED_PARTIAL,   /**< at least handler succeeded, no result yet*/
                CAS_FAILED,
            };
        ''' Number of errors.'''
        int n_hard_errors; ''' errors due to TLS negotiation failure '''
        int n_soft_errors; ''' errors due to unrecognized or failed-to-authenticate incoming packets '''
        ''' Our locked common name, username, and cert hashes (cannot change during the life of this tls_multi object)'''
        char *locked_cn;
        char *locked_username;
        struct cert_hash_set *locked_cert_hash_set;
        ''' Time of last call to tls_authentication_status '''
        time_t tas_last;
        ''' An error message to send to client on AUTH_FAILED'''
        char *client_reason;
        ''' A multi-line string of general-purpose info received from peer
            over control channel.'''
        char *peer_info;
        char *auth_token;    '''<  If server sends a generated auth-token,
                                   this is the token to use for future
                                   user/pass authentications in this session.
                              '''
        char *auth_token_initial;
        '''< The first auth-token we sent to a client, for clients that do
            not update their auth-token (older OpenVPN3 core versions)'''
        ��define  AUTH_TOKEN_HMAC_OK              (1<<0)
        '''< Auth-token sent from client has valid hmac '''
        ��define  AUTH_TOKEN_EXPIRED              (1<<1)
        '''< Auth-token sent from client has expired '''
        ��define  AUTH_TOKEN_VALID_EMPTYUSER      (1<<2)
        ''' Auth-token is only valid for an empty username
            and not the username actually supplied from the client
            OpenVPN 3 clients sometimes wipes or replaces the username with a
            username hint from their config.'''
        ''' For P_DATA_V2 '''
        uint32_t peer_id;
        bool use_peer_id;
        char *remote_ciphername;    '''< cipher specified in peer's config file '''
        ''' Our session objects.'''
        struct tls_session session[TM_SIZE];
            ''' const options and config info '''
            struct tls_options *opt; @:tls_options
            ''' during hard reset used to control burst retransmit '''
            bool burst;
            ''' authenticate control packets '''
            struct tls_wrap_ctx tls_wrap;
                enum {
                    TLS_WRAP_NONE = 0, '''< No control channel wrapping '''
                    TLS_WRAP_AUTH,  '''< Control channel authentication '''
                    TLS_WRAP_CRYPT, '''< Control channel encryption and authentication '''
                } mode;                     '''< Control channel wrapping mode '''
                struct crypto_options opt;  '''< Crypto state '''  @:crypto_options
                struct buffer work;         '''< Work buffer (only for --tls-crypt) '''
                struct key_ctx tls_crypt_v2_server_key;  '''< Decrypts client keys ''' &<:key_ctx>
                    cipher_ctx_t *cipher;       '''< Generic cipher %context. '''
                        typedef EVP_CIPHER_CTX cipher_ctx_t;
                    hmac_ctx_t *hmac;           '''< Generic HMAC %context. '''
                        typedef HMAC_CTX hmac_ctx_t;
                    uint8_t implicit_iv[OPENVPN_MAX_IV_LENGTH];
                    '''< The implicit part of the IV '''
                    size_t implicit_iv_len;     '''< The length of implicit_iv '''
                const struct buffer *tls_crypt_v2_wkc;   '''< Wrapped client key, sent to server '''
                struct buffer tls_crypt_v2_metadata;     '''< Received from client '''
                bool cleanup_key_ctx;                    '''< opt.key_ctx_bi is owned by
                                                              this context '''
            int initial_opcode;         ''' our initial P_ opcode '''
            struct session_id session_id; ''' our random session ID '''
                uint8_t id[8];
            ''' The current active key id, used to keep track of renegotiations.
                key_id increments with each soft reset to KEY_ID_MASK then recycles back
                to 1.  This way you know that if key_id is 0, it is the first key.
             '''
            int key_id;
            int limit_next;             ''' used for traffic shaping on the control channel '''
            int verify_maxlevel;
            char *common_name;
            struct cert_hash_set *cert_hash_set;
            ��ifdef ENABLE_PF
            uint32_t common_name_hashval;
            ��endif
            bool verified;              ''' true if peer certificate was verified against CA '''
            ''' not-yet-authenticated incoming client '''
            struct link_socket_actual untrusted_addr;  @:link_socket_actual
            struct key_state key[KS_SIZE];  @:key_state
        '''<  Array of tls_session objects
              representing control channel
              sessions with the remote peer. '''        
================================================================================================================================== 

&<process_incoming_link_part1>
+process_incoming_link_part1(c, lsi, false);
    struct crypto_options *opt = NULL;   &<opt��������λ��>
    +if (c->c2.buf.len > 0)  #�������������
        '''��¼���������ݳ���'''
        c->c2.original_recv_size = c->c2.buf.len;
        c->c2.link_read_bytes += c->c2.buf.len;
        link_read_bytes_global += c->c2.buf.len;
        'ȷ���յ��İ��ĵ�ַ����c->c2.link_socket_info��һ�µ�
        +if (c->c2.tls_multi)
            '''���tls_pre_decrypt����true����ζ���յ��İ������õ�tls����ͨ���İ�
               �������������TLS���뽫����ð���������buf.lenΪ0���Ӷ�����Ĳ��費���ٴ�������
               ����ð��Ǹ�����ͨ���İ�����tls_pre_decrypt�������ȷ�ļ�����Կ�������ؼ�;
               ����TLSģʽʱ�����ǵ�һ�������������յ��İ��ĺ���
               ��������ݰ�����������ѡ��e���Ӷ�ʹ�����ǵĵ����߿��Խ�����
               ����Ҳ�Ѷ�Ӧ�Ľ���key�������ǵĵ�����
               ����Ǹ����ư���������֤����������
               ���ܻᴴ��һ���µ�tls�Ự���������ʾ����һ���»Ự�ĵ�һ������
               ��Ӧ���ư������ǻ������buf���㣬�Ӷ�ʹ���ǵĵ����������Ƿ��غ���Ըð�
               ע�⣬ovpnֻ����ͬʱ��һ����ĻỰ������һ���µĻỰ��һ����֤���������Ǵ۶�һ���ɵĻỰ
               ����Ǹ���֤ͨ���Ŀ���ͨ���İ��������棬���򷵻ؼ�
               '''
            '''��Ҫ��ɵĹ���������ֻ�г��˶Կ��ư��Ĵ����������
               �ҵ���Ӧ��session������ session->untrusted_addr = Զ�˵�ַ
               ks = session->key[KS_PRIMARY]
               ks->session_id_remote = sid�������İ��ĻỰid��; 
               ks->remote_addr = Զ�˵�ַ
               ks->send_reliable����Ӧ�İ�����Ϊ�ǻ��
               ks->rec_reliable���ҵ�һ�����õĵ� reliable_entry
                   e = rel->array[]
                   e->active = true;  
                   e->packed_id = pid;  
                   e->opcode= opcode;
                   e->next_try = e->timeout = 0
               ���ʹ���� -tls-auth �� --tls-crypt ������ʱ��
               ������ɰ�����֤/���ܴ���
               '''
            +bool b = tls_pre_decrypt(...)   &<tls_pre_decrypt>  file://ovpnԴ�����-�����.py@tls_pre_decrypt
                uint8_t pkt_firstbyte = *BPTR(buf);
                int op = pkt_firstbyte >> P_OPCODE_SHIFT;  #ovpn��ͷ�ĸ�5λ�ǲ�����
                +'''�����ݰ�'''
                if ((op == P_DATA_V1) || (op == P_DATA_V2))
                    handle_data_channel_packet(multi, from, buf, opt, floated, ad_start);  @opt��������λ��
                        for (int i = 0; i < KEY_SCAN_SIZE; ++i)
                            '''ע�⣬key_scan��key_state*�ṹ����ָ��ͬsession��key�ӳ�Ա��'''
                            struct key_state *ks = multi->key_scan[i];
                            '''��if�����Ǳ���vpnʵ������Զ�ˣ�����֮��TSL״̬�Ļ�������
                               �������ʧ�ܣ����������ǣ����Ǵ�һ����Դ�����һ�����ݰ���
                               �����ݰ����Ʋο�����ǰЭ�̵�TLS�Ự��������OpenVPNʵ��û�й�������Э�̵ļ��䡣
                               �⼸�����Ƿ�����UDP�Ự�У������ӵı����˱�������������û������ʱ
                               ���������Ƿ�������ֻ�������ӣ��������ǿͻ��ˣ��������ӣ�
                               '''
                            if ( ks->state>=S_GOT_KEY/S_SEND_KEY     && 
                                 key_id == ks->key_id                && 
                                 ks->authenticated == KS_AUTH_TRUE   && 
                                 (floated || link_socket_actual_match(from, &ks->remote_addr) ) ) 
                                '''��Զ��֮���key��û��ʼ���������ð�'''
                                if (!ks->crypto_options.key_ctx_bi.initialized)
                                    goto done
                                *opt = &ks->crypto_options;   #opt�Ǻ��������Ĳ�����crypto_options **����  @opt��������λ��
                                ++ks->n_packets;
                                ks->n_bytes += buf->len;
                                return
                    return false;
                +'''�ǿ��ư�'''
                int key_id = pkt_firstbyte & P_KEY_ID_MASK;  #ovpn��ͷ�ĵ�3λ��keyid
                +'''��֤���Ĳ������Ƿ�����Ч��Χ'''
                if (op < P_FIRST_OPCODE || op > P_LAST_OPCODE)
                    goto error;  #������Ч��Χ������ʶ��İ������룩
                +'''�����������֪ͨ���õİ������ʵ���Ƿ�������ȷ�ĶԶ�
                   �����Ŀ����룬�����Ҫ�����³�ʼ��key��Ҫ������֮ǰ��״̬����������c->c2.frame'''
                if (op == P_CONTROL_HARD_RESET_CLIENT_V2 ||    &<is_hard_reset_method2>
                    op == P_CONTROL_HARD_RESET_SERVER_V2 || 
                    op == P_CONTROL_HARD_RESET_CLIENT_V3)   
                    '''ȷ���Ƕ�Ӧ�ķ���˻�ͻ��˷��������'''
                    if (((op == P_CONTROL_HARD_RESET_CLIENT_V2  ||
                          op == P_CONTROL_HARD_RESET_CLIENT_V3) && !multi->opt.server) ||
                          ((op == P_CONTROL_HARD_RESET_SERVER_V2) && multi->opt.server))
                        '''˵����֪ͨ���õİ������Կͻ��˵ģ����Լ����ǿͻ���
                           ���֪ͨ���õİ������Է���˵ģ����Լ����Ƿ����
                           ����Ȼ�ǲ������İ�'''
                        goto error 
                '''��ʼ������֤'''
                +'�Ӱ��л�ȡ���Ựid��sid�����ֵ��
                +'''��multi->session[]���ҵ���sidһ�µ��Ǹ�session'''
                for (i = 0; i < TM_SIZE; ++i)  #TM_SIZE: tls_multi����session���ĸ�����3����
                    tls_session *session = &multi->session[i];
                    key_state *ks = &session->key[KS_PRIMARY];
                    if (session_id_equal(&ks->session_id_remote, &sid))  #��ȡ���ĻỰid�����¼��Զ�˻Ựid�Ƚ�
                        if (i == TM_LAME_DUCK)  #ƥ���ˣ����������TM_LAME_DUCK���Ǹ�sessionƥ��� 
                            goto error
                        break
                '''i == TM_SIZE ͨ��������һ��û���ҵ�����м�¼�ĻỰidƥ����Ǹ�session
                   �����������������Ұ��Ĳ�������Ҫ�����õ����
                   ��ʱ��Ϊ���ǣ��£��Ự�ĵ�һ����
                   ע���ͻ��˿�ʼ�������ӵ�ʱ�򣬷���˻ظ��ĵ�һ�������� P_CONTROL_HARD_RESET_SERVER_V2 ��
                   '''
                +'''����ǲ���ʹ��TM_ACTIVE����һ���µĻỰ'''
                if (i == TM_SIZE && is_hard_reset_method2(op))     @is_hard_reset_method2
                    tls_session *session = &multi->session[TM_ACTIVE];
                    key_state *ks = &session->key[KS_PRIMARY];
                    '''�����û���ü�¼Զ�˵ĻỰid����û�������κ����ӣ�'''
                    if (!session_id_defined(&ks->session_id_remote))
                        do_burst = true;
                        new_link = true;  #���Ǹ�����ֵ����ʶ��������
                        i = TM_ACTIVE;  #ֱ��ʹ�� TM_ACTIVE ��session
                        session->untrusted_addr = *from;  #TM_ACTIVE��session�м�¼Զ�˵�ַ
                '''����i == TM_SIZE��˵��֮ǰ�Ѿ����������ӣ�
                   ���Ǹ����Ӷ�Ӧ��session�м�¼��sid���յ��İ���sid��һ�£�sid�Ǹ��������
                   is_hard_reset_method2��֤�Ƿ���Ҫ�����õİ�
                   '''
                +'''����ǲ���ʹ��TM_UNTRUSTED����һ���µĻỰ'''
                +if (i == TM_SIZE && is_hard_reset_method2(op))  
                    +'''ѡ����TM_UNTRUSTED��session�Ͻ�������'''
                    tls_session *session = &multi->session[TM_UNTRUSTED];
                    +'''��ȡ����ͨ������֤��¼ &<read_control_auth>'''
                    bool b = read_control_auth(buf, ctx=&session->tls_wrap, from,opt=session->opt)
                        uint8_t opcode = *(BPTR(buf)) >> P_OPCODE_SHIFT;
                        if (opcode == P_CONTROL_HARD_RESET_CLIENT_V3)  #�ǿͻ��˷�������ð�
                            bool b = tls_crypt_v2_extract_client_key(buf, ctx, opt)
                            '''�޷��ӶԶ���ȡ��tls-crypt-v2�Ŀͻ�����Կ'''
                            if(!b) goto cleanup
                            ������
                        '''&<���Ʋ㰲ȫ>��
                           ʹ��--tls-auth fileѡ����Ը����Ʋ��һ��HMAC��
                           ������֤HAMCʧ�ܵİ���ֱ�Ӷ������Ӷ�ʹovpn����DDOS����
                           ��ѡ�����Ҫ�ã�Ӧ�÷��ڷ���˵������ļ���
                           ���Ƶģ�--tls-crypt key���Ը�tls����ͨ����Ӷ����һ�����
                           �����������tls֤������ã�Ҳ���Է���DOS����
                           ��������ctx��������tls_wrap_ctx���͵ģ�
                           ������ṹ���������ڸ�tls���Ʋ�HMAC������õģ�
                           ��Ȼ�����û��ʹ�� -tls-auth �� --tls-crypt ʱ����ǰ���þ�����������
                           ���������ûɶ���ˣ���ʱ ctx->mode Ϊ TLS_WRAP_NONE
                           '''
                        if (ctx->mode == TLS_WRAP_AUTH)
                            ������
                        else if (ctx->mode == TLS_WRAP_CRYPT)
                            ������
                        else if (ctx->tls_crypt_v2_server_key.cipher)
                            ������
                        +if (ctx->mode == TLS_WRAP_NONE || ctx->mode == TLS_WRAP_AUTH) 
                            +'''��buffer��ָ������ovpnͷ��1�ֽڣ��ͻỰid��8�ֽڣ�'''
                            buf_advance(buf, SID_SIZE(8) + 1);
                        return true
                    if (!b) goto error
                    new_link = true;
                    i = TM_UNTRUSTED;
                    session->untrusted_addr = *from;
                +else
                    struct tls_session *session = &multi->session[i];
                    struct key_state *ks = &session->key[KS_PRIMARY];
                    if (i != TM_ACTIVE && i != TM_UNTRUSTED) goto error
                    +'''���������ӣ�����ǰԶ�˵ĵ�ַ��ks���ɹ��������ӣ��м�¼��Զ�˵�ַ��һ��
                       �����İ���
                       '''
                    if (!new_link && !link_socket_actual_match(&ks->remote_addr, from))  goto error
                    +'''P_CONTROL_SOFT_RESET_V1 �����Ҫ�����¸����µ�key�Ŀ��ư�(Զ��Ҫ������Э����Կ)
                       DECRYPT_KEY_ENABLED չ��Ϊ��ks->state >= S_GOT_KEY/S_SEND_KEY
                       �����if������˵��֮ǰ�Ѿ�Э�̺�key�ˣ����ڷ����Ҫ�����¸���key
                       '''
                    if (op == P_CONTROL_SOFT_RESET_V1 && DECRYPT_KEY_ENABLED(multi, ks))
                        ������
                    else
                        if (op == P_CONTROL_SOFT_RESET_V1) do_burst = true;
                        +'''��buf��ָ������ovpnͷ��1�ֽڣ��ͻỰid��8�ֽڣ�'''
                        bool b = read_control_auth(buf, &session->tls_wrap, from, session->opt) @read_control_auth
                        if(!b) goto error
                tls_session *session = &multi->session[i];
                key_state *ks = &session->key[KS_PRIMARY];
                'ȷ��session->session_id��Ϊ��
                +'''����������ӣ�key_state��¼��Զ�˵ĻỰid�͵�ַ'''
                if (new_link)
                    ks->session_id_remote = sid;   
                    ks->remote_addr = *from;
                    ++multi->n_sessions;
                +else 
                    +'''key_state�м�¼��Զ�˵�ַ���뷢������Զ�˵�ַ��һ�£�����'''
                    if (!link_socket_actual_match(&ks->remote_addr, from))  goto error;
                +'''�Ƿ�Ӧ�öԷ��ͻ�����������δȷ�ϵ����ݰ������ش�?
                   �������˵�2���Զ����ߺ󣬳�ʼ��ԿЭ�̵�����Ч�ʡ�'''
                if (do_burst && !session->burst)
                    '''�������Ų��ÿ��reliable_entry������
                       ����ð��� active �ģ����� next_try ����Ϊ now��
                       ���䳬ʱʱ������Ϊ���Ų�� initial_timeout����ʼ��ʱʱ�䣩
                       '''
                    reliable_schedule_now(ks->send_reliable);
                    session->burst = true;
                '''key_id�ǰ�ͷ�ĵ�3λ��¼��'''
                if (ks->key_id != key_id)  goto error  
                struct reliable_ack send_ack;
                +'''�ӻظ��İ��ж�packid���֣�λ��ovpnͷ��sid֮�����֧��8��packid��
                   �ͽ�������RemoteSessionID����
                   '''
                bool b = reliable_ack_read(ack=&send_ack, buf, sid=&session->session_id)
                    uint8_t count;
                    buf_read(buf, &count, sizeof(count)
                if(!b)  goto error
                +'''����send_reliable������ĸ�����id��send_ack�м�¼��ĳ����idһ����
                   ˵���ð��л�Ӧ�ˣ��򽫸ð��� active ����Ϊ false
                   ���壺
                   ����send_ack�м�¼��packed_id[]
                   �ڲ��ٱ��� reliable ���Ų�� array[] (���Ϳ��Ų����֧��4������
                   ������Ų�ȡ����array��������active�ģ������id �� packed_id[i] һ�£�
                   ˵�ŷ��͵������������Ӧ�Ļظ��ˣ���֮ active ����Ϊ��
                   '''
                reliable_send_purge(ks->send_reliable, &send_ack);
                +'''reliable_can_get���rec_reliable����û�п��еģ������ڽ������ݵ�buffer'''
                if (op != P_ACK_V1 && reliable_can_get(ks->rec_reliable))   
                    '''��buf�ж�����ĩβ--�������ӵĵ�һ���ظ�����Message Package-ID'''
                    bool b=reliable_ack_read_packet_id(buf, &id)
                    if(b)
                        '''ȷ�����յİ���id��������������buffer
                           ��Ϊ����id��uint32��ʾ�ģ����и�����ʾ��Χ
                           ������жϾ���Ӧ�԰���id���Ͼ�Ҫ��������ʾ��Χ�����
                           '''
                        b = reliable_wont_break_sequentiality(ks->rec_reliable, id)
                            return reliable_pid_in_range2(test=id, base=rel->packet_id, extent=rel->size)
                                   #ע��param1, param2 ���� uint32 ����
                                   if ( UINT32_MAX_VAL - base > extend )    #��base��ֵ��û�ӽ����ʾ����ʱ
                                        if (test < base + extent)
                                            return true;
                                   else                                     #��base��ֵ�ӽ����ʾ����ʱ
                                        if ((test+0x80000000u) < (base+0x80000000u) + extent)
                                            return true;
                                   return false;
                        if(b)
                            '''ȷ�����յİ�����һ��(�ѽ��չ���)��ʷ���طŰ�'''
                            b = reliable_not_replay(rel=ks->rec_reliable, id)
                                '''��� id < rel->packet_id'''
                                b=reliable_pid_min(id, rel->packet_id)
                                if(b)  return false
                                ���� rel->array[]
                                    �������ĳ�� reliable_entry �� active �ģ�
                                    ���� packet_id == id;  
                                    return false
                                return true    
                            if(b)
                                '''�ڽ������β���ץȡһ�����õ� reliable_entry'''
                                struct buffer *in = reliable_get_buf(ks->rec_reliable);
                                    ���� rel->array[]�� ���ĳ�� reliable_entry �� active Ϊ�٣�
                                    ���� reliable_entry ��ʼ��(buf_init)���������� buf
                                '''��buf���յ��İ����������������β���Ǹ� reliable_entry'''
                                buf_copy(in, buf)
                                '''���������� op ����id���������Ǵ�buf�з��������ģ��ȴ���������β���Ǹ� reliable_entry'''
                                reliable_mark_active_incoming(ret=ks->rec_reliable, buf=in, pid=id, op)
                                    ���� rel->array[] ,�ҵ������ buf ƥ����Ǹ� reliable_entry, ��Ϊ e
                                    e->active = true;  e->packed_id = pid;  e->opcode= opcode;
                                    e->next_try = e->timeout = 0
                            reliable_ack_acknowledge_packet_id(ack=ks->rec_ack, pid=id);
                                '''��� pid �Ƿ��Ѿ���¼�� ack ����
                                   ack �� key_state �е� reliable_ack �ṹ�����Լ�¼packedid�����֧�ּ�8��
                                   '''
                                bool b = reliable_ack_packet_id_present(ack, pid)
                                if(!b)   #û��¼
                                    if(ack->len < RELIABLE_ACK_SIZE(8) )  #��û��
                                        ack->packet_id[ack->len++] = pid;
                                        return true
                                    return false                  
            if(b)
                '''�����Ŀ����룬�����Ҫ�����³�ʼ��key��Ҫ������֮ǰ��״̬����������c->c2.frame'''
                uint8_t op = *BPTR(&c->c2.buf) >> P_OPCODE_SHIFT;
                if (op == P_CONTROL_HARD_RESET_CLIENT_V2 || 
                    op == P_CONTROL_HARD_RESET_SERVER_V2 || 
                    op == P_CONTROL_HARD_RESET_CLIENT_V3)
                    c->c2.frame = c->c2.frame_initial;
                c->c2.tmp_int->last_action = now;
                '''����ping��ʱ'''
                if (c->options.ping_rec_timeout)
                    event_timeout_reset(&c->c2.ping_rec_interval);
        else
            opt = &c->c2.crypto_options;
        '''��֤�ͽ��ܴ�������ݰ�'''
        bool decrypt_status = openvpn_decrypt(buf=&c->c2.buf, work=c->c2.buffers->decrypt_buf,
                                              opt=crypto_options, frame=&c->c2.frame, ad_start);
            if(buf->len>0 && crypto_options!=NULL)  #���ư�ʱ��crypto_optionsΪNULL
                key_ctx *ctx = &opt->key_ctx_bi.decrypt;
                cipher_kt_t * tmp = cipher_ctx_get_cipher_kt(ctx->cipher)
                '''��� EVP_CIPHER_nid(cipher) Ϊ
                   NID_aes_128_gcm �� 
                   NID_aes_192_gcm �� 
                   ID_aes_256_gcm �� 
                   NID_chacha20_poly1305
                   �����棬���򷵻ؼ�
                   '''
                bool b= cipher_kt_mode_aead(tmp)
                if(b)
                    '''aead���ܣ� &<aead����>
                       Authenticated Encryption with Associated Data (AEAD) 
                       ��һ��ͬʱ�߱������ԣ������ԺͿ���֤�Եļ�����ʽ��
                       �����ĶԳƼ����㷨������ܲ������޷�ȷ����Կ�Ƿ���ȷ�ġ�
                       Ҳ����˵�����ܺ�����ݿ������κ���Կִ�н������㣬
                       �õ�һ������ԭʼ���ݣ�����֪����Կ�Ƿ�����ȷ�ģ�
                       Ҳ��֪�����ܳ�����ԭʼ�����Ƿ���ȷ��
                       ��ˣ���Ҫ�ڵ����ļ����㷨֮�ϣ�
                       ����һ����֤�ֶΣ���ȷ�Ͻ��ܲ����Ƿ���ȷ��
                       AEAD������һ���㷨���ڲ�ͬʱʵ�ּ��ܺ���֤
                       '''
                    return openvpn_decrypt_aead(buf, work, opt, frame, ad_start);
                else
                    '''�⿪����֤�����ܺͼ���طű�����CBC��OFB��CFBģʽ������ͨ������
                       ��buf->len����Ϊ0�����ܴ���ʱ����false��
                       �ɹ�ʱ��buf������Ϊָ�����ģ�����true��
                       '''
                    return openvpn_decrypt_v1(buf, work, opt, frame);
            else
                return true
        '''���ܴ����� TCP ģʽ���������ģ�ע�� SIGUSR1 �ź�'''
        if (false==decrypt_status && link_socket_connection_oriented(c->c2.link_socket))
            register_signal(c, SIGUSR1, "decryption-error"); 

&<process_incoming_link_part2>
+process_incoming_link_part2(c, lsi, orig_buf);   
    lsi = c->c2.link_socket_info
    orig_buf = c->c2.buf.data
    '''��������ʱ������б�Ҫ�����ѹ�ð�
       �����ping����occ��������һ���Ĵ���
       �� buf �����ݴ�� c->c2.to_tun ��
       c->c2.buffers->read_link_buf->data
       '''
    if (c->c2.buf.len > 0)  
        '''��ѹ��������ݰ�'''
        if (c->c2.comp_context)
            (*c->c2.comp_context->alg.decompress)(&c->c2.buf, c->c2.buffers->decompress_buf, ...);
        '''�������ã�������'''
        if (c->c2.tls_multi == NULL && c->c2.buf.len > 0) 
            link_socket_set_outgoing_addr(lsi, &c->c2.from, NULL, c->c2.es);
        '�������ݰ����ն�ʱ��
        '''�����ping����������buf.len=0�����治�ٴ���ð�'''
        if (is_ping_msg(&c->c2.buf))
            c->c2.buf.len = 0; #���治�ٴ���ð�
        '''����յ����Ǹ�occ��'''
        if (is_occ_msg(&c->c2.buf))
            process_received_occ_msg(c);
                case OCC_REQUEST:
                    c->c2.occ_op = OCC_REPLY;
                case OCC_MTU_REQUEST:
                    c->c2.occ_op = OCC_MTU_REPLY;
                case OCC_MTU_LOAD_REQUEST:
                    c->c2.occ_mtu_load_size = buf_read_u16(&c->c2.buf);
                    if (c->c2.occ_mtu_load_size >= 0)
                        c->c2.occ_op = OCC_MTU_LOAD;
                case OCC_REPLY:
                    if (c->options.occ && c->c2.tls_multi != NULL #�������ã�������
                        && c->c2.options_string_remote)
                        ������
                    event_timeout_clear(&c->c2.occ_interval);
                case OCC_MTU_REPLY:
                    c->c2.max_recv_size_remote = buf_read_u16(&c->c2.buf);
                    c->c2.max_send_size_remote = buf_read_u16(&c->c2.buf);
                    if (c->options.mtu_test  #�������ã�������
                        && c->c2.max_recv_size_remote > 0
                        && c->c2.max_send_size_remote > 0)
                        ������
                    event_timeout_clear(&c->c2.occ_mtu_load_test_interval);
                case OCC_EXIT:
                    c->sig->signal_received = SIGTERM;
                    c->sig->signal_text = "remote-exit";
        '''��� orig_buf ��ָ�� c->c2.buf->data �������� c->c2.buffers->read_link_buf->data
           �� c->c2.buf ��� c->c2.buffers->read_link_buf������ c->c2.to_tun ָ�� read_link_buf
           ������ c->c2.to_tun ָ�� c->c2.buf
           '''
        buffer_turnover(uint8* orig_buf, buffer* dest_stub=&c->c2.to_tun, buffer* src_stub=&c->c2.buf, 
                        buffer* storage=&c->c2.buffers->read_link_buf);
            if (orig_buf == src_stub->data && src_stub->data != storage->data)
                '''src_stub ��� src_stub'''
                buf_assign(storage, src_stub);
                *dest_stub = *storage;
            else
                *dest_stub = *src_stub;
        '''���tuntap��û���壬���� c->c2.to_tun.len = 0������ᵼ������'''
        if (!tuntap_defined(c->c1.tuntap))
            c->c2.to_tun.len = 0;
    else
        buf_reset(&c->c2.to_tun);