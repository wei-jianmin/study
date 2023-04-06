����ļ���
    file://add_option����.py
    file://openvpn_help.txt
wmain
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
    openvpn_main
        struct context c;
        init_static  #&<��init_static�ķ���>
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
                        mydata_index = SSL_get_ex_new_index(0, "struct session *", NULL, NULL, NULL);
                    crypto_init_lib
                        �ڲ�û��ִ���κδ���
            prng_init
                crypto.c�еķ�����prng : pseudorandom number generator
        do.while(c.sig->signal_received == SIGHUP)
            pre_init_signal_catch
                sig.c�еķ�����windows�£��ú���ִ��Ϊ�գ�linux�������źŴ�����
            context_clear_all_except_first_time
                ��ʼ�� context c
            CLEAR(siginfo_static)��c.sig = &siginfo_static;  
                siginfo_staticΪsig.h�е�ȫ�ֱ���
                struct signal_info
                {
                    volatile int signal_received;
                    volatile int source;
                    const char *signal_text;
                } siginfo_static;
            gc_init(&c.gc)
                �Σ�file://�������ջ���.txt
            c.es = env_set_create(NULL)
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
            init_management  &<init_management>
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
            init_options(&c.options, true); //��ʼ��ѡ��ΪĬ��״̬ &<��init_options�ķ���>
                struct options options;  //��¼�����к������ļ�
            parse_argv(&c.options, argc, argv, msglevel=M_USAGE=45056,    //&<��parse_argv�ķ���>
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
            net_ctx_init(&c, &c.net_ctx);  //��ʵ�֣�����0
                networking.h�еĺ���
            init_verb_mute(&c, IVM_LEVEL_1);//��ʼ����־�������ϸ�̶�
            init_options_dev(&c.options);
                if (!options->dev && options->dev_node)  //dev��������ƣ������ļ���ָ���� dev tun
                    ���������--dev-node�������û������--dev��ʱ������������
                    ���� options->dev_node ��ֵ��basename������ options->dev
            print_openssl_info(&c.options)
                ���� c.options �е������� show_ciphers��show_digests��show_engines��show_tls_ciphers��show_curves
                ������ʾ��ͬ����Ϣ�����ݵ�ǰ�����ã�����ʲôҲû�У�
            do_genkey(&c.options)
                if (options->mlock && options->genkey)
                    �ֱ��� mlock �� genkey ��������ƣ����ݵ�ǰ���ã��������߾�Ϊfalse
                ��������д��룬���ǻ��� genkey ����Ϊ��ģ�
                ���ݵ�ǰ���ã���Щ�������ִ�У���������false
            ������溯��ִ�гɹ��������˳�
            do_persist_tuntap(&c.options, &c.net_ctx)
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
            options_postprocess(&c.options);  //��ѡ��ĺ��� &<��options_postprocess�ķ���>
                options_postprocess_mutate(options);  //�������ñ䶯
                    helper_client_server(o);
                        ��Ϊ�ͻ���/�����ʱ����������������Ƿ���ȷ��������������������д���
                        �����
                            if(dev == DEV_TYPE_TUN)  //���ݵ�ǰ���ã�dev==DEV_TYPE_TUN
                                //��زο���file://openvpn��������.py
                                if (topology == TOP_NET30 || topology == TOP_P2P) //���ݵ�ǰ���ã�topology==TOP_NET30
                                    helper_add_route(o->server_network, o->server_netmask, o)
                                    push_option(o, print_opt_route(o->server_network + 1, 0, &o->gc), M_USAGE);
                                        ���ݲ����������ַ�������֯Ϊ push_entry �ṹ������ o->push_list ��
                                        push "route 10.8.0.1"
                                push_option(o, print_opt_topology(topology, &o->gc), M_USAGE);
                                    push "topology net30"
                            else if (dev == DEV_TYPE_TAP)    
                        �ͻ���
                            o->pull = true;   //���ƴӷ������ȡ������
                            o->tls_client = true;
                    helper_keepalive(o);  //���� keepalive ������
                        ���� o->ping_rec_timeout_action��o->ping_send_timeout��o->ping_rec_timeout
                        ��� o->mode == MODE_SERVER
                            push "ping 10"
                            push "ping-restart 60"
                    helper_tcp_nodelay(o);  // ���� tcp-nodelay ������
                        ��� o->server_flags ���� SF_TCP_NODELAY_HELPER �����ݵ�ǰ���ã��������������server_flags==0��
                            o->sockflags |= SF_TCP_NODELAY;
                            if (o->mode == MODE_SERVER)
                                push "socket-flags TCP_NODELAY"
                                    TCP_NODELAYѡ�������������Ƿ���Nagle�㷨��
                                    ���㷨��Ϊ����߽����Ĺ���������Ч��
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
                    options_postprocess_mutate_invariant(o);  //mutate : ʹ�任��ʹ�ı�
                        ��������� _WIN32
                            if (options->mode == MODE_SERVER)
                                options->tuntap_options.tap_sleep = 10;
                                options->route_delay_defined = false;
                    if (o->ncp_enabled)  //true ,  NCP: �������Э�� Network Control Protocol
                        ncpЭ����
                            ���磬���һ���û�Ҫ���Ž���·���������û��Ļ���һ�㲻֪��Ҫʹ���ĸ�IP��ַ��
                            ��˱���ͨ��NCP/IPCPЭ�̴�·�������һ����ַ
                        o->ncp_ciphers = mutate_ncp_cipher_list(o->ncp_ciphers, &o->gc);
                            ���˵�libcrypto���в�֧�ֵ��㷨��������ֿⲻ֧�ֵ��㷨�ͷ��ؿգ�
                        ��� o->ncp_ciphers Ϊ�գ���ʾ���ڲ�֧�ֵ� ciphers ��  ciphers���ܳ��ȳ���127�ֽ�
                    if (o->remote_list && !o->connection_list)
                    else if (!o->remote_list && !o->connection_list)    
                        struct connection_entry *ace = alloc_connection_entry(o, M_USAGE);
                            struct connection_list *l = alloc_connection_list_if_undef(options);
                                if (options->connection_list == null)
                                    ���� struct connection_list �ṹ���ŵ� options->connection_list �У����� options->connection_list
                            struct connection_entry *e = ���� struct connection_entry
                            �� e �ŵ� l->array[] ��
                            ���� e
                        *ace = o->ce  // o->ce ���ڳ�ʼ����ʱ��Σ�������õ�
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
                    if (o->tls_server)
                         if (o->dh_file == "none")  //true
                            o->dh_file = NULL
                    if (o->http_proxy_override)  //false
                        options_postprocess_http_proxy_override(o);
                     pre_pull_save(o);
                        if (o->pull)  //false
                            ...
                options_postprocess_verify(options);
                    if (o->connection_list)
                        for i in o->connection_list->len  //len=1
                            options_postprocess_verify_ce(o, o->connection_list->array[i]);
                                ��� options->dev �Ƿ�Ϊ�ǿ� ��="tun"��
                                ���ce�ӳ�Ա��option�ӳ�Ա�ȣ�����÷����ԣ�������ʾ��Ϣ
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
            show_settings(&c.options);
                �������õĵ�����Ϣ�Ǽǣ�������ʾ������Ϣ
            show_windows_version(M_INFO);
                �������õĵ�����Ϣ�Ǽǣ�������ʾWindows�汾��Ϣ
            show_library_versions(M_INFO);
                �������õĵ�����Ϣ�Ǽǣ�������ʾssl��汾��Ϣ
            pre_setup(const struct options *options)
                ��������� _WIN32          
                    win32_signal_open(&win32_signal,
                                      int force=WSO_FORCE_CONSOLE,
                                      const char *exit_event_name=NULL,
                                      bool exit_event_initial_state=false);
                        �������ÿ���̨ģʽ����ֹ����
                        �������ĳ���ʧ���ˣ�������һ������
                        ���ÿ���̨��Ϣ�����Ӻ���Ϊ��win_ctrl_handler������ctrl+c��break�¼�
                    ���Ϊ����̨�����ÿ���̨����
            do_test_crypto(struct options *o= &c.options)
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
            ��� (c.options.management_flags & MF_QUERY_PASSWORDS),
                �����ͨ������ӿڻ�����룬���ѯ���룬���ݵ�ǰ���ã�����ִ������
                init_query_passwords(&c);
                    if (c->options.key_pass_file)  //����������
                        pem_password_setup(c->options.key_pass_file);
                    if (c->options.auth_user_pass_file)   //����������
                        auth_user_pass_setup(c->options.auth_user_pass_file, &c->options.sc_info);
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
            open_management(&c)   //&<��open_management�ķ���>
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
            if (c.options.management_flags & MF_QUERY_PASSWORDS)  //��������˭
                //�����Ҫ����ͨ����������ѯ����
                init_query_passwords(&c);
            setenv_settings(c.es, &c.options)  //��ĳЩѡ������Ϊ��������
            context_init_1(&c)  //&<��main��context_init_1�ķ���>
                context_clear_1(c);
                    CLEAR(c->c1);
                packet_id_persist_init(p=&c->c1.pid_persist);
                    ��p�ĳ�Ա��ʼ��Ϊ��
                init_connection_list(c);
                    if (c->options.remote_random)  //����������
                        len = c->options.connection_list->len
                        foreach i  < len  //���ܣ����� l->array
                            j = rand() % len
                            if (i!=j)
                                l->array[i] �� l->array[j] ���ཻ��
                save_ncp_options(c);
                    c->c1.ciphername = c->options.ciphername;
                    c->c1.authname = c->options.authname;
                    c->c1.keysize = c->options.keysize;
                if (c->first_time) //true
                    pkcs11_initialize(protected_auth=true, nPINCachePeriod=c->options.pkcs11_pin_cache_period=-1);
                    foreach c->options.pkcs11_providers[i]  //������Ϊ�գ�����������
                        pkcs11_addProvider(...)
            do.while(c.sig->signal_received == SIGHUP)
            do.while(c.sig->signal_received == SIGHUP)
                switch(c.options.mode)  // = 1
                     case MODE_POINT_TO_POINT:
                        tunnel_point_to_point(&c);
                     case MODE_SERVER:
                        tunnel_server(top=&c);
                            if (proto_is_udp(top->options.ce.proto))
                                tunnel_server_udp(top);
                            else
                                tunnel_server_tcp(top);  //@tunnel_server_tcp
                c.first_time = false;   //����Χ�ڵĵ�һ�ε���

===========================================================================================================
 
// Top level event loop for single-threaded operation.                        
void tunnel_server_tcp(struct context *top) //&<��main�е�tunnel_server_tcp�ķ���>
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

//&<��init_instance�ķ���>
//��ʼ��һ�����ʵ��
void init_instance(struct context *c, const struct env_set *env, const unsigned int flags)    //&init_instance     
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
file://openvpn��context�ṹ.c+

&<�ļ���֪ʶ��>
file://֪ʶ��.txt

'''�ͻ�ģʽ�µ�vpn���¼�ѭ����ֻ��һ��vnp����Ǽ����'''
&<��tunnel_point_to_point�ķ���>
tunnel_point_to_point  //�ͻ���ģʽ��ѭ��
    '''���c->c2'''
    context_clear_2(c)
    '''���ö˵���ģʽ'''
    c->mode = CM_P2P;
    '''��ʼ�����ʵ��������֮ǰ��֮����źż���'''
    init_instance_handle_signals(c, c->es, CC_HARD_USR1_TO_HUP);
        pre_init_signal_catch
            window��ʲôҲûִ��
        init_instance  //Initialize a tunnel instance.
            '''��c->c2.es �̳� env'''
            do_inherit_env(c, env);
            if (c->mode == CM_P2P)   //true
                init_management_callback_p2p
                    if (management)  //����������
            if (c->mode == CM_P2P || c->mode == CM_TOP)  //true
                do_startup_pause(c);
                    if (!c->first_time)
                        socket_restart_pause(c);
                    else
                        do_hold(0);   //�״�ִ������
                            if (management)  //����������
            if (c->options.resolve_in_advance)   //����������
                do_preresolve(c);
            '''ӳ�䵱ǰ������Ŀ'''
            next_connection_entry(c);
                c->options.ce = *c->options.connection_list->array[0]
                update_options_ce_post(&c->options);
            init_verb_mute(c, IVM_LEVEL_2);
                ���� c->c2.log_rw ������
            '''���ô����ӳ٣���Ӧ��һ�����Ĵ���������Ϊ0'''
            set_check_status_error_delay(P2P_ERROR_DELAY_MS);  //0
            '''����fast io'''
            do_setup_fast_io(c);
            '''����tls����ʱ������SIGUSR1�ź�'''
            do_signal_on_tls_errors(c);
                c->c2.tls_exit_signal = SIGUSR1;
            '''��--statusָ�����ļ�'''
            do_open_status_output(c);
            '''��--ifconfig-pool-persistָ�����ļ�'''
            do_open_ifconfig_pool_persist(c);
            '''����occ״̬'''
            c->c2.occ_op = -1
            '''��ʼ��event�¼���(���ڵȴ�io)'''
            do_event_set_init
            '''��ʼ��http��socks������level2�����������ڣ�'''
            init_proxy(c);
                �������ã���ʼ��c->c1.http_proxy��c->c1.socks_proxy
            '''Ϊc->c2.link_socket�������'''
            do_link_socket_new(c);
            '''��ʼ����Ƭ����'''
            if (options->ce.fragmen) //0
                c->c2.fragment = fragment_init(&c->c2.frame)
            '''��ʼ�����ܲ�'''
            do_init_crypto(struct context *c, const unsigned int flags)
                do_init_crypto_tls(c, flags);
                    init_crypto_pre
                        '''�����ʲôҲûִ��'''
                    '''��ʼ���������'''
                    do_init_crypto_tls_c1
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
                            '''��ʼ�� tls-auth/crypt/crypt-v2 ���õ�key'''
                            do_init_tls_wrap_key(c);    /* initialize tls-auth/crypt/crypt-v2 key */
                                ���� c->c1.ks �µ�ֵ /* tunnel session keys */
                            '''��ʼ��auth-token����Կ������'''
                            do_init_auth_token_key
                                ���auth_token_generate������Ϊ��  //false
                                    auth_token_init_secret
                                        ���������ļ���auth_token_secret_file���� c->c1.ks.auth_token_key
                            '''����c->c1.ks.key_type.cipher���ж�ʹ�ó�Ψһ��ʶ��(64λ)���Ƕ�Ψһ��ʶ��(32Ϊ)'''
                            packet_id_long_form = cipher_kt_mode_ofb_cfb(c->c1.ks.key_type.cipher);  
                            ....
                            struct tls_options to;
                            to.*** = ***
                            '''��ʼ��openvpn����tls-mode����'''
                            c->c2.tls_multi = tls_multi_init(&to);
            '''��ʼ��ѹ����'''
            ���options->comp�е�ѹ���㷨����  //false
                c->c2.comp_context = comp_init(&options->comp);
            '''��ʼ��MTU��ر���'''
            do_init_frame(c);
                ����ѹ��������--tun-mtu-extra�����socket�������ֽڶ���
                �����أ��������� c->c2.frame.extra_frame ��ֵ
            '''��ʼ��TLS MTU��ر���'''
            do_init_frame_tls(c);
                do_init_finalize_tls_frame(c)
                    '''��tls_multi�Ľ��ܣ�
                       ʹ����TLS��vpn�������һ��tls_multi����
                       �ö����д������п���ͨ��������ͨ���İ�ȫ����
                       �ýṹ���԰������(����ͬʱ���ڻ״̬��)tls_context����
                       �Ӷ������ڻỰ����Э��ʱ���жϵ�ת��
                       ÿ��tls_context��ʾһ������ͨ��
                       �����Կ�Խkey_state�ṹ�еĶ������ͨ���ĻỰ��ȫ����
                       �Σ�<file://openvpn��context�ṹ.c+>'''
                    tls_multi_init_finalize(multi=c->c2.tls_multi, frame=&c->c2.frame)
                        '''��ʼ������ͨ����֡����'''
                        tls_init_control_channel_frame_parameters(data_channel_frame = frame, 
                                                                  frame = &multi->opt.frame)
                            frame->extra_frame�Ѿ�����ʼ������
                            frame->link_mtu �� frame->extra_link �̳� data_channel_frame �е�ֵ
                            frame->extra_frame ���Ӵ�С
                            frame->link_mtu_dynamic ����ֵ
                        '''��ʼ������Լ�untrusted��sessions
                           ��ʼ��tls_session�ṹ���������
                           ����һ������ĻỰid��
                           ��ʼ��tls_session.key[KS_PRIMARY]������'''
                        tls_session_init(multi, session = &multi->session[TM_ACTIVE=0])
                        tls_session_init(multi, session = &multi->session[TM_UNTRUSTED=1]
                            session->optָ��multi->opt
                            session->session_id�������ֵ
                            '''��ʼ������ͨ���������֤����'''
                            session->tls_wrap = session->opt->tls_wrap;
                            '''Ϊ--tls-auth��ʼ����id�ز�����'''
                            packet_id_init
                                ���� session->tls_wrap.opt.packet_id
                            '''��ʼ����tls_session������key_state�ṹ
                               ���������ýṹ��SSL-BIO
                               ���ö���key_state.stateΪS_INITIAL
                               ����tls_session���ڲ�״̬��Ϊsession ID��key ID���ú��ʵ�ֵ
                               ����ʼ����һЩ�еĽṹ������·��ɿ���
                               '''
                            key_state_init(tls_session* session, key_state* ks=&session->key[KS_PRIMARY])
                                '''����tls����--����ͨ��BIO��д�ڴ��е�ciphertext'''
                                key_state_ssl_init(key_state_ssl *ks_ssl = &ks->ks_ssl, 
                                                   tls_root_ctx *ssl_ctx = &session->opt->ssl_ctx, 
                                                   bool is_server = session->opt->server,
                                                   tls_session *session)
                                    CLEAR(*ks_ssl);
                                    '''��sessionָ����ssl���󣬴Ӷ�������֤�ص��з�����'''
                                    SSL_set_ex_data(ks_ssl->ssl, mydata_index, session);
                                    '''BIO_f_ssl() returns the SSL BIO method'''
                                    ks_ssl->ssl_bio = BIO_new(BIO_f_ssl())  //ssl bio,���ڶ�д��ͨ�ļ�
                                    ks_ssl->ct_in = BIO_new(BIO_s_mem())    //�ڴ�bio������д�����ı�
                                    ks_ssl->ct_out = BIO_new(BIO_s_mem())   //�ڴ�bio�����ڶ������ı�
                                    '''����ssl������client״̬��
                                       ��Ӧ�ģ�SSL_set_accept_state����ssl�����ڷ�����״̬'''
                                    SSL_set_connect_state(ks_ssl->ssl);
                                    '''����ssl���������������д'''
                                    SSL_set_bio(ks_ssl->ssl, ks_ssl->ct_in, ks_ssl->ct_out);
                                    '''BIO_set_ssl(b,ssl,c)����b�ڲ���SSLָ��ָ��ssl
                                       ��ʹ�ùرձ��c'''
                                    BIO_set_ssl(ks_ssl->ssl_bio, ks_ssl->ssl, BIO_NOCLOSE);
                                '''���ÿ���ͨ���ĳ�ʼ��ģʽ'''
                                ���� ks->initial_opcode��session->initial_opcode��ks->state��ks->key_id
                                '''allocate key source material object'''
                                ��ʼ�� ks->send_reliable��ks->rec_reliable��ks->rec_ack
                                '''����buffer'''
                                ��ʼ�� ks->plaintext_read_buf��ks->plaintext_write_buf��
                                       ks->ack_write_buf��ks->send_reliable��ks->rec_reliable
            '''��ʼ��������buffers'''
            do_init_buffers(c);
                c->c2.buffers = init_context_buffers(&c->c2.frame);
                    struct context_buffers *b;
                    Ϊb�ĸ���Ա������Ӧ�Ľṹ����Сc->c2.frame��buf size��
                    return b
            '''ʹ����֪��frame��С����ʼ���ڲ��ķ�Ƭ������fragmentation capability��'''
            if(options->ce.fragment)  //false
                do_init_fragment
            '''��ʼ����̬MTU����'''
            frame_init_mssfix(&c->c2.frame, &c->options);
                if (options->ce.mssfix)
                    '''��̬����tun��MTU'''
                    frame_set_mtu_dynamic(frame, options->ce.mssfix, SET_MTU_UPPER_BOUND);
            '''��tcp/udp socket'''
            do_init_socket_1(c, link_socket_mode=LS_MODE_DEFAULT=0);
                '''link_socket��ʼ���׶�1'''
                link_socket_init_phase1(sock=c->c2.link_socket, ......)
                    ���ݲ���������ֵ������sock�ĸ���Ա
                    if (sock->bind_local)  //false
                        resolve_bind_local(sock, sock->info.af);
                    resolve_remote(sock, 1, NULL, NULL); 
                        '''���δ���壬����remote��ַ'''
                        if (!sock->info.lsa->remote_list)  //����
                            if (sock->remote_host)  //"192.168.4.143"
                                struct addrinfo *ai;
                                ������
                                '''�ɹ�����0��ʧ�ܷ���-1����ͬgetaddrinfo'''
                                state = get_cached_dns_entry( ock->dns_cache,
                                                              sock->remote_host,
                                                              sock->remote_port,
                                                              sock->info.af,
                                                              flags, &ai);
                                if(state != 0)  //����
                                    '''ת��ipv4��ipv6�Գƻ�������Ϊ struct addrinfo
                                       ���ʧ�ܣ����ڲ���ָ����n�������'''
                                    status = openvpn_getaddrinfo(flags, sock->remote_host, sock->remote_port,
                                                                 retry, signal_received, sock->info.af, &ai);
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
            '''��ʼ��tun/tap�豸���󣬴��豸��ifconfig��ִ��up�ű����ȵ�'''
            //options->pull Ϊ�棬����������, ��helper_client_server�б�����Ϊ��
            if ( options->up_delayΪ�� �� options->pullΪ�� �� 
                 (c->mode == CM_P2P �� c->mode == CM_TOP) )  
                c->c2.did_open_tun = do_open_tun(c);
            c->c2.frame_initial = c->c2.frame;
            '''��ȡ���غ�Զ��ѡ��������ַ���'''
            do_compute_occ_strings
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
                c->c2.options_string_local = options_string(&c->options, &c->c2.frame, 
                                                            c->c1.tuntap, &c->net_ctx,
                                                            false, &gc);
                    struct buffer out = alooc_buf(255)
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
                        init_key_type(&kt, o->ciphername, o->authname, o->keysize, true, false);
                        out += "cipher AES-256-CBC,auth SHA1,keysize 256"
                    '''SSLѡ��'''
                    out += "tls-auth,key-method 2,tls-client"
                c->c2.options_string_remote= options_string(&c->options, &c->c2.frame, 
                                                            c->c1.tuntap, &c->net_ctx,
                                                                    true, &gc);
                    out = "V4,dev-type tun,link-mtu 1557,tun-mtu 1500,\
                           proto UDPv4,keydir 0, cipher AES-256-CBC,auth SHA1,\
                           keysize 256,tls-auth,key-method 2,tls-server"
                if (c->c2.tls_multi)  //����
                    '''���ñ��غ�Զ��ѡ������ַ�����������֤���غ�Զ��ѡ��ϵļ�����'''
                    tls_multi_init_set_options(c->c2.tls_multi,
                                               c->c2.options_string_local,
                                               c->c2.options_string_remote);
                        multi->opt.local_options = local;
                        multi->opt.remote_options = remote;
            '''��ʼ������ٶ�����'''
            if (c->mode == CM_P2P)  //����
                do_init_traffic_shaper
                    '''��ʼ������shaper���༴�����������'''
                    if (c->options.shaper)  //������
            '''ֻ����һ�εĳ�ʼ����������������һ���ػ�����
               ÿ������ʵ��ֻ����һ��
               Ϊ���ܵ� UID/GID �����������ã�����ʱ��Ҫ������
               �����Ҫ�������ػ�����'''
            do_init_first_time
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
            '''��ʼ�����'''
            open_plugins(c, false, OPENVPN_PLUGIN_INIT_POST_DAEMON);
                if (c->plugins && c->plugins_owned)   //������
            '''��ʼ������ʱ�䶨ʱ��
               ��ʼ����������ѯ��ʱ��ʱ��
               �˼�ʱ������ http/socks �������ã������Ҫ������֮ǰ��������'''
            do_init_server_poll_timeout(c);
                update_time();
                if (c->options.ce.connect_timeout) //120
                    c->c2.server_poll_interval->defined = true
                    c->c2.server_poll_interval->n = max(c->options.ce.connect_timeout,0)
                    c->c2.server_poll_interval->last = now
            '''���TCP/UDP socket�����ղ���'''
            do_init_socket_2(c);
                link_socket_init_phase2(sock=c->c2.link_socket, frame=&c->c2.frame, sig_info=c->sig);
                    '''��ʼ��buffers'''
                    socket_frame_init(frame, sock);
                        �����Windows
                            ��ʼ���ص��˿� sock->reads��sock->writes
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
                    '''����ͨ��inetd����xinetd������'''
                    if (sock->inetd)  // 0
                        ...
                    else
                        '''�ڶ��δ���/����socket�Ļ���'''
                        resolve_remote(sock, 2, &remote_dynamic,  &sig_info->signal_received);
                            '''���Զ�̵�ַ���⣨���û���壩'''
                            if (!sock->info.lsa->remote_list)  //������
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
                            create_socket(sock, sock->info.lsa->current_remote);
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
                                    if (sock->bind_local)   //false
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
                    phase2_set_socket_flags(sock);
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
               ���ܱ� --client --pull �� --up-delay �Ƴ�'''
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
                do_init_timers(c, bool deferred = false);
                    ��ʼ���ǻ�Ծ��ʱ
                    ��ʼ��ping�շ���ʱ
                    if(!deferred)
                        ��ʼ���������Ӽ�ʱ
                        ��ʼ��occ��ʱ��
                        ��ʼ����id����ʱ����ʱ��
                        ��ʼ��tmp_int�Ż������������������¼�ѭ���е���tls_multi_process�Ĵ���
            '''��ʼ�����'''
            if (c->mode == CM_P2P || c->mode == CM_TOP)
                open_plugins(c, false, OPENVPN_PLUGIN_INIT_POST_UID_CHANGE);
                    if (c->plugins && c->plugins_owned)  //������
                        ������
            if (child)  //������
                pf_init_context(c);
        post_init_signal_catch  
    '''���¼�ѭ��'''
    while(true)
        perf_push(PERF_EVENT_LOOP);  //��ʵ��
        '''����ʱ����tls��'''
        pre_select(c);
            '''���ֶ�ʱ��'''
            check_coarse_timers(c);
                '''�ֶ�ʱ������Ϊ1s'''
                process_coarse_timers(c);
           
===========================================================================================================     
                
�������ݽṹ
    multi_instance *mi->context.c2.es
    multi_instance *mi->context.c2.tls_multi.es
    session->opt->es
    tls_multi *multi->opt.es        
    
    #&<multi_context>
    #�洢openvpn�ķ���״̬�Ľṹ��ֻ�ڷ����ʹ�ã��洢����vpn����ͽ��̼���״̬
    struct multi_context multi
    {
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
    }
    
    #&<multi_instance>
    #������ģʽ�£����ڴ洢һ��vpn�����״̬�Ľṹ
    struct multi_instance
    {
        #��vpn���ʵ����ʲôʱ�򴴽���
        time_t created;
        #server/tcpģʽ�£�Ҫ���������ݵĶ���
        struct mbuf_set *tcp_link_out_deferred;
        struct context context;  #�洢��vpn�����״̬
        ������
    }
    
    #&<context>
    #�ýṹ������һ��vpn��������ڴ洢һ�������״̬��Ϣ
    #��Ҳ����һЩ���̼�������ݣ���������ѡ��
    struct context
    {
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
    }
    
    #&<context_1>
    #�ýṹ������״̬����SIGUSR1�����źŵ�Ӱ�죬������SIGHUP�����źŶ�����
    struct context_1
    {
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
    }
    
    #&<context_2>
    #�洢����SIGHUP��SIGUSR1�źŵ��µġ�������������״̬��Ϣ
    struct context_2
    {
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
    }
    
    #&<tls_multi>
    #���� TLS ����������еĻ VPN �����һ��tls_multi����
    #���д洢���п���ͨ��������ͨ����ȫ����״̬��
    #�˽ṹ���԰������������ͬʱ���ڻ״̬��tls_context����
    #�������ڻỰ����Э���ڼ�������жϵ�ת����
    #ÿ��tls_context����һ������ͨ���Ự��
    #�ûỰ���Կ�Խ�洢��key_state�ṹ�еĶ������ͨ����ȫ�����Ự��
    struct tls_multi
    {
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
    }
    
    #&<key_state>
    #�洢������ͨ����tls״̬������ͨ��������״̬��
    #�������ˡ����Ų�ṹ��--���ڿ���ͨ������Ϣ[����]
    struct key_state
    {
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
    }
    
    #&<tls_session>
    #�洢һ���Ự�İ�ȫ������Ϣ���Ự���������
    #�ýṹ��Ӧһ��vpn�Ķ˵��˵Ŀ���ͨ��session
    struct tls_session
    {
        struct tls_options *opt;  #����ѡ���������Ϣ
        struct session_id session_id;
        int key_id; #���Ը���renegotiations
        ������
    }
    
    
    &<�ṹ����ʹ�����׷��>
    main�е� context c; 
        ����������
        ������
        ������־
        ���������ϵͳ
        ���𻷾�����
    
    tunnel_server_udp_single_threaded�е� context c ��ָ��main�е� context c��
        ����context_2
            ��context_2��es�̳�main��context�Ļ�������
            ����context_2��link_socket
        ����sig�ź�
        ����context_1
        ����������
    
    tunnel_server_udp_single_threaded�е� multi_context multi;
        ����context top����ʼ��multi
        �̳�context top����������һЩֵ�����޸�
            mode��ΪCM_TOP_CLONE����ֹclose_instance�رո������Դ�����
            first_time = false
            c0 = null
            c2.tls_multi = null
            c1.xxx_owned = false
            c2.xxx_owned = false
            ...
        
        
tunnel_server����ѭ��  #&<tunnel_server����ѭ��>
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
                    
tuntap��link�ֱ�����γ�ʼ����                    
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