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
    openvpn_main
        struct context c;
        init_static
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
        init_options(&c.options, true); //��ʼ��ѡ��ΪĬ��״̬
            struct options options;  //��¼�����к������ļ�
        parse_argv(&c.options, argc, argv, msglevel=M_USAGE=45056, 
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
        options_postprocess(&c.options);  //��ѡ��ĺ���
            options_postprocess_mutate(options);  //�������ñ䶯
                helper_client_server(o);
                    ��Ϊ�ͻ���/�����ʱ����������������Ƿ���ȷ��������������������д���
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
                    ���ÿ���̨ģʽ��֧��
                    if (����)  //false
                        �򿪿���̨ʧ�ܣ�������һ������
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
            �����ͨ������ӿڻ�����룬���ѯ���룬���ϵ�ǰ���ã�����ִ������
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
            open_management(&c)
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
            context_init_1(&c)
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
            do  
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
void tunnel_server_tcp(struct context *top) //&tunnel_server_tcp
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
            
file://openvpn��context�ṹ.c+

file://֪ʶ��.txt
