相关文件：
    file://add_option函数.py
    file://openvpn_help.txt
wmain
    /*
     * 该函数包含两个外层循环，其结构如下
     *     每个进程一次的初始化
     *     外层循环（启动时或SIGHUP后执行） //file://SIGHUP信号.py
     *         level 1 初始化
     *         内层循环（启动时或SIGUSR1后执行） //file://SIGUSR1信号.py
     *             基于客户端模式/服务端模式，调用事件循环函数
     *                 tunnel_point_to_point()  //点对点模式
     *                 tunnel_server()   //客户端-服务器模式
     *         level 1 清理
     *     每进程一次的清理
     */
    //&<对openvpn_main的分析>
    openvpn_main
        struct context c;
        init_static  #&<对init_static的分析>
            srandom设置随机数种子
            error_reset
                error.c中的方法，初始化文件变量
            reset_check_status
                 error.c中的方法，初始化文件变量
            init_win32
                win32.c中的方法，wsa初始化、初始化全局变量 win32_signal、window_title
            update_time
                otime.h中的方法，获取时间，存给局部变量 timeval tv;
            init_ssl_lib
                ssl.c中的方法
                    tls_init_lib
                        mydata_index = SSL_get_ex_new_index(0, "struct session *", NULL, NULL, NULL);
                    crypto_init_lib
                        内部没有执行任何代码
            prng_init
                crypto.c中的方法，prng : pseudorandom number generator
        do.while(c.sig->signal_received == SIGHUP)
            pre_init_signal_catch
                sig.c中的方法，windows下，该函数执行为空，linux下设置信号处理函数
            context_clear_all_except_first_time
                初始化 context c
            CLEAR(siginfo_static)，c.sig = &siginfo_static;  
                siginfo_static为sig.h中的全局变量
                struct signal_info
                {
                    volatile int signal_received;
                    volatile int source;
                    const char *signal_text;
                } siginfo_static;
            gc_init(&c.gc)
                参：file://垃圾回收机制.txt
            c.es = env_set_create(NULL)
                创建 struct env_set {
                    struct gc_arena *gc;
                    struct env_item *list;
                };
                struct env_item {
                    char *string;
                    struct env_item *next;
                };
                list链表占用的内存，通过gc管理并释放
            Windows下，set_win_sys_path_via_env(c.es)
                获取 "SystemRoot" 环境变量的值，存给 c.es
            init_management  &<init_management>
                init.c中的方法
                    management = management_init();  management 为全局变量
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
            init_options(&c.options, true); //初始化选项为默认状态 &<对init_options的分析>
                struct options options;  //记录命令行和配置文件
            parse_argv(&c.options, argc, argv, msglevel=M_USAGE=45056,    //&<对parse_argv的分析>
                       permission_mask=OPT_P_DEFAULT, option_types_found=NULL, es=c.es);
                判断如果argc小于1，显示提示信息，程序退出
                如果有2个参数（第一个参数是程序本身），且第二个参数是 --，给出错误提示
                提取选项命令（--之后的字符），如果不是以--开头，报错
                将选项命令记录到p[0]
                获取选项参数（直到碰到--开头的字符串），记录到p[1]..p[15]，每个命令最多支持16个参数
                add_option(options, p, is_inline=false, char* file=NULL, line=0, level=0,
                           msglevel, permission_mask, option_types_found, es);
                    具体参：file://options.py
                    #该函数的作用就是根据参数p，将配置信息存到options中
                    如果file为空，file="[CMD-LINE]"，line=1
                    如果p[0] 为 "help"
                        显示帮助信息，程序退出
                    如果p[0] 为 "version"
                        显示版本信息，程序退出
                    如果p[0] 为 "config"
                        options->config = p[1]
                        read_config_file(options, char* file = p[1], level, char* top_file=file, 
                                         int top_line=line, msglevel, permission_mask, option_types_found, es);
                             level++;
                             FILE* fp = fopen(file,"r");
                             while 读取一行到 line 字符数组
                                char *p[MAX_PARMS+1];
                                parse_line(line, p, SIZE(p)-1, file, line_num, msglevel, &options->gc)
                                    该函数的作用就是读取每一行配置，然后把读到的结果放到输出参数p中
                                add_option(options, p, lines_inline, file, line_num, level,
                                           msglevel, permission_mask, option_types_found, es);    
                    如果p[0] 为 "show-gateway"
                        显示默认网关，程序退出
                    如果p[0] 为 "echo" 或 "parameter"
                        打印命令参数信息到日志输出
                    如果p[0] 为 "management"
                        后跟三个参数，分别记录到
                        options->management_addr、
                        options->management_port、
                        options->management_user_pass
                        第三个参数为可选项
                    如果p[0] 为 "management-client-user"
                        后跟一个参数，记录到options->management_client_user
                    如果p[0] 为 "management-client-group"
                        后跟一个参数，记录到options->management_client_group
                    如果p[0] 为 "management-query-passwords"
                        后面不跟参数，影响 options->management_flags （MF_QUERY_PASSWORDS）
                    如果p[0] 为 "management-query-remote"
                    如果p[0] 为 "management-query-proxy"
                    如果p[0] 为 "management-hold"
                    如果p[0] 为 "management-signal"
                    如果p[0] 为 "management-forget-disconnect"
                    如果p[0] 为 "management-up-down"
                    如果p[0] 为 "management-client"
                    如果p[0] 为 "management-external-key"
                    如果p[0] 为 "management-external-cert"
                    如果p[0] 为 "management-client-auth"
                    如果p[0] 为 "management-client-pf"
                    如果p[0] 为 "management-log-cache"
                    如果p[0] 为 "plugin"
                    如果p[0] 为 "mode"
                    如果p[0] 为 "dev"
                    如果p[0] 为 "dev-type"
                    如果p[0] 为 "windows-driver"
                    如果p[0] 为 "dev-node"
                    如果p[0] 为 "lladdr"
                    如果p[0] 为 "topology"
                    如果p[0] 为 "tun-ipv6"
                    如果p[0] 为 "ifconfig"
                    如果p[0] 为 "ifconfig-ipv6"
                    如果p[0] 为 "ifconfig-noexec"
                    如果p[0] 为 "ifconfig-nowarn"
                    如果p[0] 为 "local"
                    如果p[0] 为 "remote-random"
                    如果p[0] 为 "connection"
                    如果p[0] 为 "ignore-unknown-option"
                    如果p[0] 为 "ignore-unknown-option"
                    如果p[0] 为 "remote"
                    如果p[0] 为 "resolv-retry"
                    如果p[0] 为 "preresolve"
                    如果p[0] 为 "connect-retry"
                    如果p[0] 为 "connect-timeout"
                    如果p[0] 为 "connect-retry-max"
                    如果p[0] 为 "ipchange"
                    如果p[0] 为 "float"
                    如果p[0] 为 "gremlin"
                    如果p[0] 为 "chroot"
                    如果p[0] 为 "cd"
                    如果p[0] 为 "setcon"
                    如果p[0] 为 "writepid"
                    如果p[0] 为 "up"
                    如果p[0] 为 "down"
                    如果p[0] 为 "down-pre"
                    如果p[0] 为 "up-delay"
                    如果p[0] 为 "up-restart"
                    如果p[0] 为 "syslog"
                    如果p[0] 为 "daemon"
                    如果p[0] 为 "inetd"
                    如果p[0] 为 "log"
                    如果p[0] 为 "suppress-timestamps"
                    如果p[0] 为 "machine-readable-output"
                    如果p[0] 为 "log-append"
                    如果p[0] 为 "memstats"
                    如果p[0] 为 "mlock"
                    如果p[0] 为 "multihome"
                    如果p[0] 为 "verb"
                    如果p[0] 为 "mute"
                    如果p[0] 为 "errors-to-stderr"
                    如果p[0] 为 "status"
                    如果p[0] 为 "status-version"
                    如果p[0] 为 "remap-usr1"
                    如果p[0] 为 "link-mtu"
                    如果p[0] 为 "tun-mtu"
                    如果p[0] 为 "tun-mtu-extra"
                    如果p[0] 为 "mtu-dynamic"
                    如果p[0] 为 "fragment"
                    如果p[0] 为 "mtu-disc"
                    如果p[0] 为 "mtu-test"
                    如果p[0] 为 "nice"
                    如果p[0] 为 "rcvbuf"
                    如果p[0] 为 "sndbuf"
                    如果p[0] 为 "mark"
                    如果p[0] 为 "socket-flags"
                    如果p[0] 为 "bind-dev"
                    如果p[0] 为 "txqueuelen"
                    如果p[0] 为 "shaper"
                    如果p[0] 为 "port"
                    如果p[0] 为 "lport"
                    如果p[0] 为 "rport"
                    如果p[0] 为 "bind"
                    如果p[0] 为 "nobind"
                    如果p[0] 为 "fast-io"
                    如果p[0] 为 "inactive"
                    如果p[0] 为 "proto"
                    如果p[0] 为 "proto-force"
                    如果p[0] 为 "http-proxy"
                    如果p[0] 为 "http-proxy-user-pass"
                    如果p[0] 为 "http-proxy-retry"
                    如果p[0] 为 "http-proxy-timeout"
                    如果p[0] 为 "http-proxy-option"
                    如果p[0] 为 "socks-proxy"
                    如果p[0] 为 "keepalive"
                    如果p[0] 为 "ping"
                    如果p[0] 为 "ping-exit"
                    如果p[0] 为 "ping-restart"
                    如果p[0] 为 "ping-timer-rem"
                    如果p[0] 为 "explicit-exit-notify"
                    如果p[0] 为 "persist-tun"
                    如果p[0] 为 "persist-key"
                    如果p[0] 为 "persist-local-ip"
                    如果p[0] 为 "persist-remote-ip"
                    如果p[0] 为 "client-nat"
                    如果p[0] 为 "route"
                    如果p[0] 为 "route-ipv6"
                    如果p[0] 为 "max-routes"
                    如果p[0] 为 "route-gateway"
                    如果p[0] 为 "route-ipv6-gateway"
                    如果p[0] 为 "route-metric"
                    如果p[0] 为 "route-delay"
                    如果p[0] 为 "route-up"
                    如果p[0] 为 "route-pre-down"
                    如果p[0] 为 "route-noexec"
                    如果p[0] 为 "route-nopull"
                    如果p[0] 为 "pull-filter"
                    如果p[0] 为 "allow-pull-fqdn"
                    如果p[0] 为 "redirect-gateway"
                    如果p[0] 为 "redirect-gateway"
                    如果p[0] 为 "block-ipv6"
                    如果p[0] 为 "remote-random-hostname"
                    如果p[0] 为 "setenv"
                    如果p[0] 为 "setenv-safe"
                    如果p[0] 为 "script-security"
                    如果p[0] 为 "mssfix"
                    如果p[0] 为 "disable-occ"
                    如果p[0] 为 "server"
                    如果p[0] 为 "server-ipv6"
                    如果p[0] 为 "server-bridge"
                    如果p[0] 为 "server-bridge"
                    如果p[0] 为 "server-bridge"
                    如果p[0] 为 "push"
                    如果p[0] 为 "push-reset"
                    如果p[0] 为 "push-remove"
                    如果p[0] 为 "ifconfig-pool"
                    如果p[0] 为 "ifconfig-pool-persist"
                    如果p[0] 为 "ifconfig-ipv6-pool"
                    如果p[0] 为 "hash-size"
                    如果p[0] 为 "connect-freq"
                    如果p[0] 为 "max-clients"
                    如果p[0] 为 "max-routes-per-client"
                    如果p[0] 为 "client-cert-not-required"
                    如果p[0] 为 "verify-client-cert"
                    如果p[0] 为 "username-as-common-name"
                    如果p[0] 为 "auth-user-pass-optional"
                    如果p[0] 为 "opt-verify"
                    如果p[0] 为 "auth-user-pass-verify"
                    如果p[0] 为 "auth-gen-token"
                    如果p[0] 为 "auth-gen-token-secret"
                    如果p[0] 为 "client-connect"
                    如果p[0] 为 "client-disconnect"
                    如果p[0] 为 "learn-address"
                    如果p[0] 为 "tmp-dir"
                    如果p[0] 为 "client-config-dir"
                    如果p[0] 为 "ccd-exclusive"
                    如果p[0] 为 "bcast-buffers"
                    如果p[0] 为 "tcp-queue-limit"
                    如果p[0] 为 "port-share"
                    如果p[0] 为 "client-to-client"
                    如果p[0] 为 "duplicate-cn"
                    如果p[0] 为 "iroute"
                    如果p[0] 为 "iroute-ipv6"
                    如果p[0] 为 "ifconfig-push"
                    如果p[0] 为 "ifconfig-push-constraint"
                    如果p[0] 为 "ifconfig-ipv6-push"
                    如果p[0] 为 "disable"
                    如果p[0] 为 "tcp-nodelay"
                    如果p[0] 为 "stale-routes-check"
                    如果p[0] 为 "client"
                    如果p[0] 为 "pull"
                    如果p[0] 为 "push-continuation"
                    如果p[0] 为 "auth-user-pass"
                    如果p[0] 为 "auth-retry"
                    如果p[0] 为 "static-challenge"
                    如果p[0] 为 "msg-channel"
                    如果p[0] 为 "win-sys"
                    如果p[0] 为 "route-method"
                    如果p[0] 为 "ip-win32"
                    如果p[0] 为 "dhcp-option"
                    如果p[0] 为 "show-adapters"
                    如果p[0] 为 "show-net"
                    如果p[0] 为 "show-net-up"
                    如果p[0] 为 "tap-sleep"
                    如果p[0] 为 "dhcp-renew"
                    如果p[0] 为 "dhcp-pre-release"
                    如果p[0] 为 "dhcp-release"
                    如果p[0] 为 "dhcp-internal"
                    如果p[0] 为 "register-dns"
                    如果p[0] 为 "block-outside-dns"
                    如果p[0] 为 "rdns-internal"
                    如果p[0] 为 "show-valid-subnets"
                    如果p[0] 为 "pause-exit"
                    如果p[0] 为 "service"
                    如果p[0] 为 "allow-nonadmin"
                    如果p[0] 为 "user"
                    如果p[0] 为 "group"
                    如果p[0] 为 "user"
                    如果p[0] 为 "group"
                    如果p[0] 为 "dhcp-option"
                    如果p[0] 为 "route-method"
                    如果p[0] 为 "passtos"
                    如果p[0] 为 "allow-compression"
                    如果p[0] 为 "comp-lzo"
                    如果p[0] 为 "comp-noadapt"
                    如果p[0] 为 "compress"
                    如果p[0] 为 "show-ciphers"
                    如果p[0] 为 "show-digests"
                    如果p[0] 为 "show-engines"
                    如果p[0] 为 "key-direction"
                    如果p[0] 为 "secret"
                    如果p[0] 为 "genkey"
                    如果p[0] 为 "auth"
                    如果p[0] 为 "cipher"
                    如果p[0] 为 "data-ciphers-fallback"
                    如果p[0] 为 "data-ciphers"
                    如果p[0] 为 "ncp-ciphers"
                    如果p[0] 为 "ncp-disable"
                    如果p[0] 为 "prng"
                    如果p[0] 为 "no-replay"
                    如果p[0] 为 "replay-window"
                    如果p[0] 为 "mute-replay-warnings"
                    如果p[0] 为 "replay-persist"
                    如果p[0] 为 "test-crypto"
                    如果p[0] 为 "engine"
                    如果p[0] 为 "keysize"
                    如果p[0] 为 "use-prediction-resistance"
                    如果p[0] 为 "show-tls"
                    如果p[0] 为 "show-curves"
                    如果p[0] 为 "ecdh-curve"
                    如果p[0] 为 "tls-server"
                    如果p[0] 为 "tls-client"
                    如果p[0] 为 "ca"
                    如果p[0] 为 "capath"
                    如果p[0] 为 "dh"
                    如果p[0] 为 "cert"
                    如果p[0] 为 "enc-cert"
                    如果p[0] 为 "cert-bak"
                    如果p[0] 为 "enc-cert-bak"
                    如果p[0] 为 "extra-certs"
                    如果p[0] 为 "verify-hash"
                    如果p[0] 为 "cryptoapicert"
                    如果p[0] 为 "key"
                    如果p[0] 为 "enc-key"
                    如果p[0] 为 "key-bak"
                    如果p[0] 为 "enc-key-bak"
                    如果p[0] 为 "tls-version-min"
                    如果p[0] 为 "tls-version-max"
                    如果p[0] 为 "pkcs12"
                    如果p[0] 为 "askpass"
                    如果p[0] 为 "auth-nocache"
                    如果p[0] 为 "auth-token"
                    如果p[0] 为 "auth-token-user"
                    如果p[0] 为 "single-session"
                    如果p[0] 为 "push-peer-info"
                    如果p[0] 为 "tls-exit"
                    如果p[0] 为 "tls-cipher"
                    如果p[0] 为 "tls-cert-profile"
                    如果p[0] 为 "tls-ciphersuites"
                    如果p[0] 为 "tls-groups"
                    如果p[0] 为 "crl-verify"
                    如果p[0] 为 "tls-verify"
                    如果p[0] 为 "tls-export-cert"
                    如果p[0] 为 "compat-names"
                    如果p[0] 为 "no-name-remapping"
                    如果p[0] 为 "verify-x509-name"
                    如果p[0] 为 "ns-cert-type"
                    如果p[0] 为 "remote-cert-ku"
                    如果p[0] 为 "remote-cert-eku"
                    如果p[0] 为 "remote-cert-tls"
                    如果p[0] 为 "tls-timeout"
                    如果p[0] 为 "reneg-bytes"
                    如果p[0] 为 "reneg-pkts"
                    如果p[0] 为 "reneg-sec"
                    如果p[0] 为 "hand-window"
                    如果p[0] 为 "tran-window"
                    如果p[0] 为 "tls-auth"
                    如果p[0] 为 "tls-crypt"
                    如果p[0] 为 "tls-crypt-v2"
                    如果p[0] 为 "tls-crypt-v2-verify"
                    如果p[0] 为 "x509-track"
                    如果p[0] 为 "x509-username-field"
                    如果p[0] 为 "show-pkcs11-ids"
                    如果p[0] 为 "pkcs11-providers"
                    如果p[0] 为 "pkcs11-protected-authentication"
                    如果p[0] 为 "pkcs11-private-mode"
                    如果p[0] 为 "pkcs11-cert-private"
                    如果p[0] 为 "pkcs11-pin-cache"
                    如果p[0] 为 "pkcs11-id"
                    如果p[0] 为 "pkcs11-id-management"
                    如果p[0] 为 "rmtun"
                    如果p[0] 为 "mktun"
                    如果p[0] 为 "peer-id"
                    如果p[0] 为 "keying-material-exporter"
                    如果p[0] 为 "allow-recursive-routing"
                    如果p[0] 为 "vlan-tagging"
                    如果p[0] 为 "vlan-accept"
                    如果p[0] 为 "vlan-pvid"
            如果定义了 ENABLE_PLUGIN
                init_verb_mute  //设置详细程度和静音级别  
                    set_check_status(D_LINK_ERRORS, D_READ_WRITE);
                    set_debug_level(c->options.verbosity, SDL_CONSTRAIN);
                    set_mute_cutoff(c->options.mute);
                    这三个都是error.c中的函数
                    c->c2.log_rw = (check_debug_level(D_LOG_RW) && !check_debug_level(D_LOG_RW + 1));
                    控制是否把收发的包打印出来，这里不打印
                init_plugins(&c);
                    如果 c->option.plugins_list 不为空（由plugin配置项控制，这里为空，所以没有执行）
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
                        。。。略（调试时不满足条件，所以没有执行）
            net_ctx_init(&c, &c.net_ctx);  //空实现，返回0
                networking.h中的函数
            init_verb_mute(&c, IVM_LEVEL_1);//初始化日志级别的详细程度
            init_options_dev(&c.options);
                if (!options->dev && options->dev_node)  //dev配置项控制，配置文件中指定了 dev tun
                    如果设置了--dev-node配置项，而没有设置--dev项时，该条件满足
                    根据 options->dev_node 的值的basename，设置 options->dev
            print_openssl_info(&c.options)
                根据 c.options 中的配置项 show_ciphers、show_digests、show_engines、show_tls_ciphers、show_curves
                控制显示不同的信息（根据当前的配置，这里什么也没有）
            do_genkey(&c.options)
                if (options->mlock && options->genkey)
                    分别由 mlock 和 genkey 配置项控制，根据当前配置，这里两者均为false
                后面的所有代码，都是基于 genkey 配置为真的，
                根据当前配置，这些代码均不执行，函数返回false
            如果上面函数执行成功，程序退出
            do_persist_tuntap(&c.options, &c.net_ctx)
                if (options->persist_config) //根据当前配置，为false
                    如果定义了 ENABLE_FEATURE_TUN_PERSIST  //当前没有定义
                        tuncfg(...)
                            tun.c中的函数
                        set_lladdr(...)
                            lladdr.c中的函数
                        return true;
                    否则
                        输出错误提示，return false
            如果上面函数执行成功，程序退出
            options_postprocess(&c.options);  //对选项的后处理 &<对options_postprocess的分析>
                options_postprocess_mutate(options);  //处理配置变动
                    helper_client_server(o);
                        作为客户端/服务端时，检查配置项配置是否正确，并根据已有配置项进行处理
                        服务端
                            if(dev == DEV_TYPE_TUN)  //根据当前配置，dev==DEV_TYPE_TUN
                                //相关参考：file://openvpn网络拓扑.py
                                if (topology == TOP_NET30 || topology == TOP_P2P) //根据当前配置，topology==TOP_NET30
                                    helper_add_route(o->server_network, o->server_netmask, o)
                                    push_option(o, print_opt_route(o->server_network + 1, 0, &o->gc), M_USAGE);
                                        根据参数传来的字符串，组织为 push_entry 结构，放入 o->push_list 中
                                        push "route 10.8.0.1"
                                push_option(o, print_opt_topology(topology, &o->gc), M_USAGE);
                                    push "topology net30"
                            else if (dev == DEV_TYPE_TAP)    
                        客户端
                            o->pull = true;   //控制从服务端拉取配置项
                            o->tls_client = true;
                    helper_keepalive(o);  //处理 keepalive 配置项
                        设置 o->ping_rec_timeout_action、o->ping_send_timeout、o->ping_rec_timeout
                        如果 o->mode == MODE_SERVER
                            push "ping 10"
                            push "ping-restart 60"
                    helper_tcp_nodelay(o);  // 处理 tcp-nodelay 配置项
                        如果 o->server_flags 包含 SF_TCP_NODELAY_HELPER （根据当前配置，不满足该条件，server_flags==0）
                            o->sockflags |= SF_TCP_NODELAY;
                            if (o->mode == MODE_SERVER)
                                push "socket-flags TCP_NODELAY"
                                    TCP_NODELAY选项是用来控制是否开启Nagle算法，
                                    该算法是为了提高较慢的广域网传输效率
                    options_postprocess_cipher(o);
                        if (!o->pull && !(o->mode == MODE_SERVER))  //o->pull:控制从对端接收配置选项，根据当前配置，该值为false
                            当为非SERVER时，才会执行该条件下面的语句
                            o->ncp_enabled = false
                            if (!o->ciphername) o->ciphername = "BF-CBC";
                            return
                        if (!o->ciphername)  //根据当前配置，ciphername="SMS4-CBC"
                            不执行
                        else if (!o->enable_ncp_fallback && !tls_item_in_cipher_list(o->ciphername, o->ncp_ciphers))  //满足
                            o->enable_ncp_fallback = true;
                            将 ciphername="SMS4-CBC" 添加到 o->ncp_ciphers 中
                    options_postprocess_mutate_invariant(o);  //mutate : 使变换，使改变
                        如果定义了 _WIN32
                            if (options->mode == MODE_SERVER)
                                options->tuntap_options.tap_sleep = 10;
                                options->route_delay_defined = false;
                    if (o->ncp_enabled)  //true ,  NCP: 网络控制协议 Network Control Protocol
                        ncp协议简介
                            例如，如果一个用户要拨号进入路由器，该用户的机器一般不知道要使用哪个IP地址，
                            因此必须通过NCP/IPCP协商从路由器获得一个地址
                        o->ncp_ciphers = mutate_ncp_cipher_list(o->ncp_ciphers, &o->gc);
                            过滤掉libcrypto库中不支持的算法（如果发现库不支持的算法就返回空）
                        如果 o->ncp_ciphers 为空，提示存在不支持的 ciphers 或  ciphers的总长度超过127字节
                    if (o->remote_list && !o->connection_list)
                    else if (!o->remote_list && !o->connection_list)    
                        struct connection_entry *ace = alloc_connection_entry(o, M_USAGE);
                            struct connection_list *l = alloc_connection_list_if_undef(options);
                                if (options->connection_list == null)
                                    申请 struct connection_list 结构，放到 options->connection_list 中，返回 options->connection_list
                            struct connection_entry *e = 申请 struct connection_entry
                            将 e 放到 l->array[] 中
                            返回 e
                        *ace = o->ce  // o->ce 是在初始化的时候危机感设置的
                    for i in o->connection_list->len
                        options_postprocess_mutate_ce(o, o->connection_list->array[i]);
                            if (o->server_defined || o->server_bridge_defined || o->server_bridge_proxy_dhcp) // server_defined为true
                                if (ce->proto == PROTO_TCP)  
                                    ce->proto = PROTO_TCP_SERVER;
                            。。。 （设ce的设置/修改一些成员值）
                            if (o->persist_key)
                                connection_entry_preload_key(&ce->tls_auth_file, &ce->tls_auth_file_inline, &o->gc);
                                connection_entry_preload_key(&ce->tls_crypt_file, &ce->tls_crypt_file_inline, &o->gc);
                                connection_entry_preload_key(&ce->tls_crypt_v2_file, &ce->tls_crypt_v2_file_inline, &o->gc);
                                    #connection_entry_preload_key(const char **key_file, bool *key_inline,struct gc_arena *gc)
                                    if (key_file && *key_file && !(*key_inline))
                                        条件不满足（*key_file为空），不执行
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
                                检查 options->dev 是否为非空 （="tun"）
                                检查ce子成员、option子成员等，如果用法不对，给出提示信息
                options_postprocess_filechecks(options);
                    check_file_access_inline(bool is_inline, const int type, const char *file, const int mode, const char *opt)
                        if (is_inline)  return false;
                        return check_file_access(type, file, mode, opt);
                            if file==null ,return false
                            if type & CHKACC_ACPTSTDIN 且 file=="stdin", return false
                            if (type & CHKACC_DIRPATH)  //检查文件夹
                                提取父目录，检查是否具有mode指定的权限，没有则返回true（表明有错）
                            if (type & CHKACC_FILE )
                                检查file是否有指定的权限，没有则返回true
                            if (type & CHKACC_FILEXSTWR)
                                检查文件是否存在且具有些权限，存在但没有写权限，返回true
                            if (type & CHKACC_PRIVATE)  //检查私有文件是否会被组的其它成员或其他组成员访问
                                检查是否能获取文件信息，失败（如文件不存在），则返回true
                    check_file_access_chroot(const char *chroot, const int type, const char *file, const int mode, const char *opt)
                        if file==null ,return false
                        if (chroot)  // If chroot is set, look for the file/directory inside the chroot
                            给 file 前面添加上 file
                        return check_file_access(type, file, mode, opt);
                    总结：
                        该函数检查 options下的 dh_file、ca_path、extra_certs_file、pkcs12_file、chroot_dir、
                        tls_auth_file、tls_crypt_file、tls_crypt_v2_file、shared_secret_file。。。是否具有指定的权限
            show_settings(&c.options);
                根据配置的调试信息登记，控制显示配置信息
            show_windows_version(M_INFO);
                根据配置的调试信息登记，控制显示Windows版本信息
            show_library_versions(M_INFO);
                根据配置的调试信息登记，控制显示ssl库版本信息
            pre_setup(const struct options *options)
                如果定义了 _WIN32          
                    win32_signal_open(&win32_signal,
                                      int force=WSO_FORCE_CONSOLE,
                                      const char *exit_event_name=NULL,
                                      bool exit_event_initial_state=false);
                        尝试设置控制台模式，禁止输入
                        如果上面的尝试失败了，表明是一个服务
                        设置控制台消息处理钩子函数为：win_ctrl_handler，处理ctrl+c或break事件
                    如果为控制台，设置控制台标题
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
                程序退出
            检查 (c.options.management_flags & MF_QUERY_PASSWORDS),
                如果不通过管理接口获得密码，则查询密码，根据当前配置，满足执行条件
                init_query_passwords(&c);
                    if (c->options.key_pass_file)  //条件不满足
                        pem_password_setup(c->options.key_pass_file);
                    if (c->options.auth_user_pass_file)   //条件不满足
                        auth_user_pass_setup(c->options.auth_user_pass_file, &c->options.sc_info);
            if (c.first_time)  //true
                c.did_we_daemonize = possibly_become_daemon(&c.options)  //检查我们应该成为守护进程吗？
                    if (options->daemon)  //条件不满足
                        。。。
                    else
                        return false
                write_pid_file(const char *filename=c.options.writepid,    //Write our PID to a file
                               const char *chroot_dir=c.options.chroot_dir);
                    if(filename)  //条件不满足
                        获取pid，写到 filename 文件中
                    if (!chroot_dir)  //条件不满足
                        saved_pid_file_name = strdup(filename)  //saved_pid_file_name为文件全局变量
            open_management(&c)   //&<对open_management的分析>
                if (management)   //management 为文件全局变量，init_management在前面已经执行过
                    if (c->options.management_addr)  //条件不满足
                        。。。
                    else
                        close_management();
                            if (management)
                                management_close(management);
                                    man_output_list_push_finalize(man)
                                        management_connected(man)
                                            检查 man->connection.state == MS_CC_WAIT_READ
                                            或   man->connection.state == MS_CC_WAIT_WRITE
                                        如果上一步返回为真  // 条件不满足
                                            man_update_io_state(man);
                                            if (!man->persist.standalone_disabled)
                                                int signal_received = 0;
                                                man_output_standalone(man, &signal_received);
                                    man_connection_close(man)
                                        struct man_connection *mc = &man->connection;
                                        if (mc->es)  //条件不满足
                                            event_free(mc->es);
                                        如果定义了 _WIN32
                                            net_event_win32_close(ne=&mc->ne32);
                                                if (ne->handle->read != null)  //条件不满足
                                                    close_net_event_win32(&ne->handle, ne->sd, 0);
                                                net_event_win32_init(ne);
                                                    CLEAR(*ne)
                                                    ne->sd = SOCKET_UNDEFINED;
                                        if( mc->sd_top != SOCKET_UNDEFINED )  //条件不满足
                                            man_close_socket(man, mc->sd_top);
                                        if( mc->sd_cli != SOCKET_UNDEFINED ) //条件不满足
                                            man_close_socket(man, mc->sd_cli);
                                        if (mc->in)  //条件不满足
                                            command_line_free(mc->in);
                                        if (mc->out)  //条件不满足
                                            buffer_list_free(mc->out);
                                        in_extra_reset(mc=&man->connection, mode=IER_RESET);
                                            if(mc)  //条件满足
                                                 if (mode != IER_NEW)   //条件满足
                                                    mc->in_extra_cmd = IEC_UNDEF;
                                                    mc->in_extra_cid = 0;
                                                    mc->in_extra_kid = 0;
                                                 if (mc->in_extra)  //条件不满足
                                                    buffer_list_free(mc->in_extra);
                                                    mc->in_extra = NULL;
                                                if (mode == IER_NEW)    //条件不满足
                                                    mc->in_extra = buffer_list_new(0);
                                        buffer_list_free(mc->ext_key_input);
                                        man_connection_clear(mc);
                                    man_settings_close(ms=&man->settings)
                                        free(ms->write_peer_info_file);
                                        CLEAR(*ms);
                                    man_persist_close(mp=&man->persist);
                                        if (mp->log)  //条件满足
                                            msg_set_virtual_output(NULL);
                                                x_msg_virtual_output = NULL  //x_msg_virtual_output为error.c中的全局变量
                                            log_history_close(mp->log);  //释放相关内存
                                        if (mp->echo)
                                            log_history_close(mp->echo);  //释放相关内存
                                        if (mp->state)
                                            log_history_close(mp->state);  //释放相关内存
                                        CLEAR(*mp);
                                    free(man);
                                management = NULL;
                return true
            if (c.options.management_flags & MF_QUERY_PASSWORDS)  //条件不满谁
                //如果需要，则通过管理界面查询密码
                init_query_passwords(&c);
            setenv_settings(c.es, &c.options)  //将某些选项设置为环境变量
            context_init_1(&c)  //&<对main中context_init_1的分析>
                context_clear_1(c);
                    CLEAR(c->c1);
                packet_id_persist_init(p=&c->c1.pid_persist);
                    将p的成员初始化为空
                init_connection_list(c);
                    if (c->options.remote_random)  //条件不满足
                        len = c->options.connection_list->len
                        foreach i  < len  //功能：乱序 l->array
                            j = rand() % len
                            if (i!=j)
                                l->array[i] 和 l->array[j] 互相交换
                save_ncp_options(c);
                    c->c1.ciphername = c->options.ciphername;
                    c->c1.authname = c->options.authname;
                    c->c1.keysize = c->options.keysize;
                if (c->first_time) //true
                    pkcs11_initialize(protected_auth=true, nPINCachePeriod=c->options.pkcs11_pin_cache_period=-1);
                    foreach c->options.pkcs11_providers[i]  //该数组为空，条件不满足
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
                c.first_time = false;   //程序范围内的第一次迭代

===========================================================================================================
 
// Top level event loop for single-threaded operation.                        
void tunnel_server_tcp(struct context *top) //&<对main中的tunnel_server_tcp的分析>
    top->mode = CM_TOP
    context_clear_2(top);
         CLEAR(c->c2);
    init_instance_handle_signals(top, top->es, CC_HARD_USR1_TO_HUP);  //initialize top-tunnel instance
        pre_init_signal_catch();
            如果没定义 _WIN32
                设置信号处理函数
        init_instance(c, env, flags);  //@init_instance
        post_init_signal_catch();
        if(c->sig->signal_received)
            remap_signal(c);
            uninit_management_callback();
            
===========================================================================================================

//&<对init_instance的分析>
//初始化一个隧道实例
void init_instance(struct context *c, const struct env_set *env, const unsigned int flags)    //&init_instance     
    gc_init(&c->c2.gc);
    if (env) //满足
        c->c2.es->list 中添加新的 struct env_item，记录遍历的 env->list->string  
            env->list->string 中包含的列表
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
    if (c->mode == CM_P2P)  //不满足，c->mode 为 CM_TOP
        init_management_callback_p2p(c);
    if (c->mode == CM_P2P || c->mode == CM_TOP)  //满足
        do_startup_pause(c);
            if (!c->first_time) //不满足
                socket_restart_pause(c);
            else
                do_hold(holdtime=0);
                    if (management)  //不满足
                        management_hold(management, holdtime)  //阻塞直到管理暂停被释放
        if( c->sig->signal_received )  //不满足
            goto sig
    if (c->options.resolve_in_advance)  //不满足
        do_preresolve(c);
        if( c->sig->signal_received )  //不满足
            goto sig
    next_connection_entry(c);
        ...(没有执行，略）
        update_options_ce_post(&c->options)
            ...(没有执行，略）
    if (c->options.ce.proto == PROTO_TCP_SERVER)  //满足
        if (c->mode == CM_TOP)  //满足
            link_socket_mode = LS_MODE_TCP_LISTEN;
        else if (c->mode == CM_CHILD_TCP){
            link_socket_mode = LS_MODE_TCP_ACCEPT_FROM;
    if (c->first_time && options->mlock)  //不满足
        platform_mlockall(true);
    if (auth_retry_get() == AR_INTERACT)   //不满足
        init_query_passwords(c);
     init_verb_mute(c, IVM_LEVEL_2);
        if (flags & IVM_LEVEL_1)
            /* 设置详细程度和静音级别 */
            set_check_status(D_LINK_ERRORS, D_READ_WRITE);
            set_debug_level(c->options.verbosity, SDL_CONSTRAIN);
            set_mute_cutoff(c->options.mute);
        if (flags & IVM_LEVEL_2) /* 特殊的 D_LOG_RW 模式 */
            c->c2.log_rw = (check_debug_level(D_LOG_RW) && !check_debug_level(D_LOG_RW + 1));
    if (c->mode == CM_P2P)  //不满足
        set_check_status_error_delay(P2P_ERROR_DELAY_MS);
    if (c->mode == CM_P2P || c->mode == CM_TOP)  //满足， 警告不一致的选项 
        do_option_warnings(c);  //检查 c->options 相关项，给出警告信息
    if (c->mode == CM_P2P || c->mode == CM_TOP)  //满足
        open_plugins(c, false, OPENVPN_PLUGIN_INIT_PRE_DAEMON);
            if (c->plugins && c->plugins_owned)  //不满足
                。。。。。。
    if (c->mode == CM_P2P || c->mode == CM_TOP)
        do_setup_fast_io(c);
            设置快速io，只有如下条件都满足，才可用
                平台不是Windows
                --proto udp 已启用
                --shaper 被禁用
            if (c->options.fast_io)  //不满足
    do_signal_on_tls_errors(c);  //我们应该在 TLS 错误上发出信号吗？
        if (c->options.tls_exit) //不满足
             c->c2.tls_exit_signal = SIGTERM;
         else
             c->c2.tls_exit_signal = SIGUSR1;
    if (c->mode == CM_P2P || c->mode == CM_TOP)   //满足
        do_open_status_output(c);  //打开和关闭 --status 文件
            if (!c->c1.status_output)  //满足
                 c->c1.status_output = status_open(filename=c->options.status_file,
                                                   refresh_freq=c->options.status_file_update_freq,
                                                   msglevel=-1, vout=NULL, flags=STATUS_OUTPUT_WRITE);
                    if (filename || msglevel >= 0 || vout)  //不满足
                        。。。
                    else
                        return NULL
                c->c1.status_output_owned = true;
    if (c->mode == CM_TOP)  //满足
        do_open_ifconfig_pool_persist(c);   //处理 ifconfig-pool 持久化对象
            if (!c->c1.ifconfig_pool_persist && c->options.ifconfig_pool_persist_filename)  //满足
                 c->c1.ifconfig_pool_persist = ifconfig_pool_persist_init(
                                                     filename=c->options.ifconfig_pool_persist_filename,
                                                     refresh_freq=c->options.ifconfig_pool_persist_refresh_freq);
                    struct ifconfig_pool_persist *ret;
                    if (refresh_freq > 0)  //满足
                        ret->fixed = false;
                        ret->file = status_open(filename="ipp.txt", refresh_freq=600, msglevel=-1,  //"ipp.txt"是配置文件中写的
                                                vout=NULL, flags=STATUS_OUTPUT_READ|STATUS_OUTPUT_WRITE);
                             if (filename || msglevel >= 0 || vout)  //条件满足
                                struct status_output *so = NULL;
                                so->flags = flags
                                so->msglevel = msglevel;
                                so->vout = vout;
                                so->fd = platform_open(filename, O_CREAT | O_RDWR, S_IRUSR | S_IWUSR);
                                so->filename = filename
                                set_cloexec(int fd=so->fd)
                                    set_cloexec_action(fd)
                                        如果没定义 _WIN32
                                            fcntl(fd, F_SETFD, FD_CLOEXEC)
                                if (so->flags & STATUS_OUTPUT_READ)  //满足
                                    so->read_buf = alloc_buf(512);
                                so->et->defined = true
                                et->n = refresh_freq
                                et->last = 0
                    return ret
                 c->c1.ifconfig_pool_persist_owned = true;
    if (c->mode == CM_P2P || child)  //不满足
        c->c2.occ_op = occ_reset_op();
    if (c->mode == CM_P2P)  //不满足
        do_event_set_init(c, SHAPER_DEFINED(&c->options));
    else if (c->mode == CM_CHILD_TCP)   //不满足
        do_event_set_init(c, false);
    init_proxy(c);  //在作用域级别 2 初始化 HTTP 或 SOCKS 代理对象
        init_proxy_dowork(c);
            uninit_proxy_dowork(c);
                里面的代码没有执行到
            if (c->options.ce.http_proxy_options)   //不满足
                c->c1.http_proxy = http_proxy_new(c->options.ce.http_proxy_options);
                if (c->c1.http_proxy)  //代理http
                    c->c1.http_proxy_owned = true;
            if (!did_http && c->options.ce.socks_proxy_server)  //不满足 
                c->c1.socks_proxy = socks_proxy_new(c->options.ce.socks_proxy_server,
                                                    c->options.ce.socks_proxy_port,
                                                    c->options.ce.socks_proxy_authfile);
                if (c->c1.socks_proxy)  //代理socket
                    c->c1.socks_proxy_owned = true;
    if (c->mode == CM_P2P || c->mode == CM_TOP || c->mode == CM_CHILD_TCP)  //满足，分配我们的套接字对象
        do_link_socket_new(c);
            c->c2.link_socket = link_socket_new();
                创建一个 struct link_socket 结构
            c->c2.link_socket_owned = true;
    if (options->ce.fragment && (c->mode == CM_P2P || child))   //不满足，初始化内部碎片对象
    初始化加密层
        unsigned int crypto_flags = 0;
        if (c->mode == CM_TOP)  //满足
            crypto_flags = CF_INIT_TLS_AUTH_STANDALONE;
        else if (c->mode == CM_P2P)
            crypto_flags = CF_LOAD_PERSISTED_PACKET_ID | CF_INIT_TLS_MULTI;
        else if (child)
            crypto_flags = CF_INIT_TLS_MULTI;
        do_init_crypto(c, crypto_flags);
            if (c->options.shared_secret_file)
                do_init_crypto_static(c, flags);
            else if (c->options.tls_server || c->options.tls_client)  //满足
                do_init_crypto_tls(c, flags);
                    init_crypto_pre(c, flags);
                        if (c->options.engine)  //不满足
                            。。。
                        if (flags & CF_LOAD_PERSISTED_PACKET_ID)  //不满足
                            。。。
                    do_init_crypto_tls_c1(c);   // 初始化持久化组件
                        if( c->c1.ks.ssl_ctx->ctx == null ) //满足，tls_ctx_initialised
                            init_ssl(options, new_ctx=&(c->c1.ks.ssl_ctx),   //初始化ssl tcx，所有文件都是pem格式
                                     bool in_chroot=c->c0 && c->c0->uid_gid_chroot_set);
                                if (options->tls_server)   //满足
                                    tls_ctx_server_new(ctx=new_ctx);
                                        ctx->ctx = SSL_CTX_new(SSLv23_server_method());
                                    if (options->dh_file)   //不满足
                                        tls_ctx_load_dh_params(new_ctx, options->dh_file,
                                                               options->dh_file_inline);
                                else
                                    tls_ctx_client_new(new_ctx);
                                tls_ctx_set_cert_profile(new_ctx, options->tls_cert_profile);  
                                    //看到这里，ssl.c:622, 2023年2月22日
                                    if (profile) 打印提示信息
                                tls_ctx_restrict_ciphers(new_ctx, options->cipher_list);
                                tls_ctx_restrict_ciphers_tls13(new_ctx, options->cipher_list_tls13);
            else
                do_init_crypto_none(c);
        if (IS_SIG(c) && !child)
            goto sig;
       
&<文件：openvpn的context结构>       
file://openvpn的context结构.c+

&<文件：知识点>
file://知识点.txt

'''客户模式下的vpn主事件循环，只有一个vnp隧道是激活的'''
&<对tunnel_point_to_point的分析>
tunnel_point_to_point  //客户端模式主循环
    '''清空c->c2'''
    context_clear_2(c)
    '''设置端到端模式'''
    c->mode = CM_P2P;
    '''初始化隧道实例，处理之前和之后的信号集合'''
    init_instance_handle_signals(c, c->es, CC_HARD_USR1_TO_HUP);
        pre_init_signal_catch
            window下什么也没执行
        init_instance  //Initialize a tunnel instance.
            '''让c->c2.es 继承 env'''
            do_inherit_env(c, env);
            if (c->mode == CM_P2P)   //true
                init_management_callback_p2p
                    if (management)  //条件不满足
            if (c->mode == CM_P2P || c->mode == CM_TOP)  //true
                do_startup_pause(c);
                    if (!c->first_time)
                        socket_restart_pause(c);
                    else
                        do_hold(0);   //首次执行这里
                            if (management)  //条件不满足
            if (c->options.resolve_in_advance)   //条件不满足
                do_preresolve(c);
            '''映射当前连接条目'''
            next_connection_entry(c);
                c->options.ce = *c->options.connection_list->array[0]
                update_options_ce_post(&c->options);
            init_verb_mute(c, IVM_LEVEL_2);
                设置 c->c2.log_rw 布尔项
            '''设置错误延迟，以应对一连串的错误，这里设为0'''
            set_check_status_error_delay(P2P_ERROR_DELAY_MS);  //0
            '''启动fast io'''
            do_setup_fast_io(c);
            '''设置tls错误时，产生SIGUSR1信号'''
            do_signal_on_tls_errors(c);
                c->c2.tls_exit_signal = SIGUSR1;
            '''打开--status指定的文件'''
            do_open_status_output(c);
            '''打开--ifconfig-pool-persist指定的文件'''
            do_open_ifconfig_pool_persist(c);
            '''重置occ状态'''
            c->c2.occ_op = -1
            '''初始化event事件，(用于等待io)'''
            do_event_set_init
            '''初始化http和socks代理（在level2的生命周期内）'''
            init_proxy(c);
                根据配置，初始化c->c1.http_proxy和c->c1.socks_proxy
            '''为c->c2.link_socket申请对象'''
            do_link_socket_new(c);
            '''初始化分片对象'''
            if (options->ce.fragmen) //0
                c->c2.fragment = fragment_init(&c->c2.frame)
            '''初始化加密层'''
            do_init_crypto(struct context *c, const unsigned int flags)
                do_init_crypto_tls(c, flags);
                    init_crypto_pre
                        '''这底下什么也没执行'''
                    '''初始化永久组件'''
                    do_init_crypto_tls_c1
                        如果&c->c1.ks.ssl_ctx没有初始化过
                            '''Initialize the OpenSSL library’s global SSL context'''
                            init_ssl(options, new_ctx = &(c->c1.ks.ssl_ctx), c->c0 && c->c0->uid_gid_chroot_set)
                                tls_ctx_client_new(new_ctx);
                                tls_ctx_set_cert_profile(new_ctx, options->tls_cert_profile);
                                tls_ctx_restrict_ciphers(new_ctx, options->cipher_list);
                                tls_ctx_set_options(new_ctx, options->ssl_flags)
                                tls_ctx_load_cert_file(new_ctx, options->cert_file, options->cert_file_inline);
                                tls_ctx_load_priv_file(new_ctx, options->priv_key_file, options->priv_key_file_inline)
                                tls_ctx_load_ca(new_ctx, options->ca_file, options->ca_file_inline, 
                                                options->ca_path, options->tls_server);
                            '''获得加密和哈希算法'''
                            init_key_type(kt=&c->c1.ks.key_type, options->ciphername, options->authname, 
                                          options->keysize, true, warn);
                                kt->cipher = cipher_kt_get(ciphername);  //AES-256-CBC
                                    return cipher = EVP_get_cipherbyname(ciphername);
                                kt->digest = md_kt_get(authname);    //SHA1
                                    return md = EVP_get_digestbyname(digest);
                            '''使用配置项指定的摘要算法初始化伪随机函数'''
                            prng_init(options->prng_hash, options->prng_nonce_secret_len);
                                prng_reset_nonce(void)
                                    rand_bytes(nonce_data, size)
                            '''初始化 tls-auth/crypt/crypt-v2 所用的key'''
                            do_init_tls_wrap_key(c);    /* initialize tls-auth/crypt/crypt-v2 key */
                                设置 c->c1.ks 下的值 /* tunnel session keys */
                            '''初始化auth-token的密钥上下文'''
                            do_init_auth_token_key
                                如果auth_token_generate配置项为真  //false
                                    auth_token_init_secret
                                        根据配置文件的auth_token_secret_file设置 c->c1.ks.auth_token_key
                            '''根据c->c1.ks.key_type.cipher，判断使用长唯一标识符(64位)还是短唯一标识符(32为)'''
                            packet_id_long_form = cipher_kt_mode_ofb_cfb(c->c1.ks.key_type.cipher);  
                            ....
                            struct tls_options to;
                            to.*** = ***
                            '''初始化openvpn的主tls-mode对象'''
                            c->c2.tls_multi = tls_multi_init(&to);
            '''初始化压缩库'''
            如果options->comp中的压缩算法存在  //false
                c->c2.comp_context = comp_init(&options->comp);
            '''初始化MTU相关变量'''
            do_init_frame(c);
                根据压缩、代理、--tun-mtu-extra配置项、socket参数、字节对齐
                等因素，设置增加 c->c2.frame.extra_frame 的值
            '''初始化TLS MTU相关变量'''
            do_init_frame_tls(c);
                do_init_finalize_tls_frame(c)
                    '''对tls_multi的介绍：
                       使用了TLS的vpn隧道，有一个tls_multi对象
                       该对象中存了所有控制通道和数据通道的安全参数
                       该结构可以包含多个(可能同时处于活动状态的)tls_context对象
                       从而允许在会话重新协商时无中断的转换
                       每个tls_context表示一个控制通道
                       它可以跨越key_state结构中的多个数据通道的会话安全参数
                       参：<file://openvpn的context结构.c+>'''
                    tls_multi_init_finalize(multi=c->c2.tls_multi, frame=&c->c2.frame)
                        '''初始化控制通道的帧参数'''
                        tls_init_control_channel_frame_parameters(data_channel_frame = frame, 
                                                                  frame = &multi->opt.frame)
                            frame->extra_frame已经被初始化过了
                            frame->link_mtu 和 frame->extra_link 继承 data_channel_frame 中的值
                            frame->extra_frame 增加大小
                            frame->link_mtu_dynamic 设置值
                        '''初始化活动的以及untrusted的sessions
                           初始化tls_session结构，这包括：
                           生成一个随机的会话id，
                           初始化tls_session.key[KS_PRIMARY]数组项'''
                        tls_session_init(multi, session = &multi->session[TM_ACTIVE=0])
                        tls_session_init(multi, session = &multi->session[TM_UNTRUSTED=1]
                            session->opt指向multi->opt
                            session->session_id设置随机值
                            '''初始化控制通道的身份认证参数'''
                            session->tls_wrap = session->opt->tls_wrap;
                            '''为--tls-auth初始化包id重播窗口'''
                            packet_id_init
                                设置 session->tls_wrap.opt.packet_id
                            '''初始化与tls_session关联的key_state结构
                               函数启动该结构的SSL-BIO
                               设置对象key_state.state为S_INITIAL
                               基于tls_session的内部状态，为session ID和key ID设置合适的值
                               还初始化了一些列的结构用于链路层可靠性
                               '''
                            key_state_init(tls_session* session, key_state* ks=&session->key[KS_PRIMARY])
                                '''创建tls对象--用于通过BIO读写内存中的ciphertext'''
                                key_state_ssl_init(key_state_ssl *ks_ssl = &ks->ks_ssl, 
                                                   tls_root_ctx *ssl_ctx = &session->opt->ssl_ctx, 
                                                   bool is_server = session->opt->server,
                                                   tls_session *session)
                                    CLEAR(*ks_ssl);
                                    '''把session指针存给ssl对象，从而能在验证回调中访问它'''
                                    SSL_set_ex_data(ks_ssl->ssl, mydata_index, session);
                                    '''BIO_f_ssl() returns the SSL BIO method'''
                                    ks_ssl->ssl_bio = BIO_new(BIO_f_ssl())  //ssl bio,用于读写普通文件
                                    ks_ssl->ct_in = BIO_new(BIO_s_mem())    //内存bio，用于写加密文本
                                    ks_ssl->ct_out = BIO_new(BIO_s_mem())   //内存bio，用于读加密文本
                                    '''设置ssl工作在client状态，
                                       对应的，SSL_set_accept_state设置ssl工作在服务器状态'''
                                    SSL_set_connect_state(ks_ssl->ssl);
                                    '''设置ssl从哪里读，往哪里写'''
                                    SSL_set_bio(ks_ssl->ssl, ks_ssl->ct_in, ks_ssl->ct_out);
                                    '''BIO_set_ssl(b,ssl,c)设置b内部的SSL指针指向ssl
                                       并使用关闭标记c'''
                                    BIO_set_ssl(ks_ssl->ssl_bio, ks_ssl->ssl, BIO_NOCLOSE);
                                '''设置控制通道的初始化模式'''
                                设置 ks->initial_opcode、session->initial_opcode、ks->state、ks->key_id
                                '''allocate key source material object'''
                                初始化 ks->send_reliable、ks->rec_reliable、ks->rec_ack
                                '''申请buffer'''
                                初始化 ks->plaintext_read_buf、ks->plaintext_write_buf、
                                       ks->ack_write_buf、ks->send_reliable、ks->rec_reliable
            '''初始化工作区buffers'''
            do_init_buffers(c);
                c->c2.buffers = init_context_buffers(&c->c2.frame);
                    struct context_buffers *b;
                    为b的各成员申请相应的结构（大小c->c2.frame的buf size）
                    return b
            '''使用已知的frame大小，初始化内部的分片能力（fragmentation capability）'''
            if(options->ce.fragment)  //false
                do_init_fragment
            '''初始化动态MTU变量'''
            frame_init_mssfix(&c->c2.frame, &c->options);
                if (options->ce.mssfix)
                    '''动态设置tun的MTU'''
                    frame_set_mtu_dynamic(frame, options->ce.mssfix, SET_MTU_UPPER_BOUND);
            '''绑定tcp/udp socket'''
            do_init_socket_1(c, link_socket_mode=LS_MODE_DEFAULT=0);
                '''link_socket初始化阶段1'''
                link_socket_init_phase1(sock=c->c2.link_socket, ......)
                    根据参数传来的值，设置sock的各成员
                    if (sock->bind_local)  //false
                        resolve_bind_local(sock, sock->info.af);
                    resolve_remote(sock, 1, NULL, NULL); 
                        '''如果未定义，则解决remote地址'''
                        if (!sock->info.lsa->remote_list)  //满足
                            if (sock->remote_host)  //"192.168.4.143"
                                struct addrinfo *ai;
                                。。。
                                '''成功返回0，失败返回-1，如同getaddrinfo'''
                                state = get_cached_dns_entry( ock->dns_cache,
                                                              sock->remote_host,
                                                              sock->remote_port,
                                                              sock->info.af,
                                                              flags, &ai);
                                if(state != 0)  //满足
                                    '''转换ipv4或ipv6对称或主机名为 struct addrinfo
                                       如果失败，会在参数指定的n秒后重试'''
                                    status = openvpn_getaddrinfo(flags, sock->remote_host, sock->remote_port,
                                                                 retry, signal_received, sock->info.af, &ai);
                                if(status == 0) //满足
                                    sock->info.lsa->remote_list = ai;
                                    sock->info.lsa->current_remote = ai;
                        '''我们需要复用之前有效的remote address吗？'''
                        如果 &sock->info.lsa->actual 定义了  //不满足
                            ...
                        esel
                            清空 sock->info.lsa->actual
                            if (sock->info.lsa->current_remote)  //满足
                                set_actual_address(&sock->info.lsa->actual,
                                                   sock->info.lsa->current_remote);
                                    actual->dest.addr.in4 = *(ai->ai_addr)
            '''初始化tun/tap设备对象，打开设备，ifconfig，执行up脚本，等等'''
            //options->pull 为真，条件不满足, 在helper_client_server中被设置为真
            if ( options->up_delay为假 且 options->pull为假 且 
                 (c->mode == CM_P2P 或 c->mode == CM_TOP) )  
                c->c2.did_open_tun = do_open_tun(c);
            c->c2.frame_initial = c->c2.frame;
            '''获取本地和远程选项兼容性字符串'''
            do_compute_occ_strings
                '''建立选项字符串来代表数据通道加密选项，该字符串两端必须一致
                   keysize单独被read_key()检查
                   下面的选项在两端之间必须匹配：
                   tun选项：
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
                   密码选项：
                    * --cipher
                    * --auth
                    * --keysize
                    * --secret
                    * --no-replay
                   SSL选项：
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
                    '''隧道选项'''
                    out += "dev-type tun"
                    '''link-mut表示是否有个固定的cipher(p2p)
                       或有个适用于旧的非tcp客户端的fallback cipher
                       但不发送它将导致告警，所以还是发送它'''
                    out += "link-mtu 1557"
                    out += "tun-mtu 1500"
                    out += "proto UDPv4"
                    '''尝试获取ifconfig参数给options字符串，如果tt没定义，创建个临时的'''
                    if (!tt)  //满足
                        tt = init_tun(o->dev,...)
                             struct tuntap *tt = 申请内存结构
                             tt->type = 2  //"tun"
                             tt->topology = 1
                             if (ifconfig_local_parm && ifconfig_remote_netmask_parm) //不满足
                                。。。
                             if (ifconfig_ipv6_local_parm && ifconfig_ipv6_remote_parm)   //不满足
                             if (es)  //不满足
                                。。。
                             return tt
                        bool tt_local = true
                    if (tt && p2p_nopull)  //不满足
                        。。。
                    if(tt_local)
                        free tt;
                        tt = NULL;
                    '''key方向'''
                    out += "keydir 1"
                    '''密码选项'''
                    如果是tls客户端或tls服务端  //条件满足
                        struct key_type kt
                        init_key_type(&kt, o->ciphername, o->authname, o->keysize, true, false);
                        out += "cipher AES-256-CBC,auth SHA1,keysize 256"
                    '''SSL选项'''
                    out += "tls-auth,key-method 2,tls-client"
                c->c2.options_string_remote= options_string(&c->options, &c->c2.frame, 
                                                            c->c1.tuntap, &c->net_ctx,
                                                                    true, &gc);
                    out = "V4,dev-type tun,link-mtu 1557,tun-mtu 1500,\
                           proto UDPv4,keydir 0, cipher AES-256-CBC,auth SHA1,\
                           keysize 256,tls-auth,key-method 2,tls-server"
                if (c->c2.tls_multi)  //满足
                    '''设置本地和远端选项兼容字符串，用于验证本地和远端选项集合的兼容性'''
                    tls_multi_init_set_options(c->c2.tls_multi,
                                               c->c2.options_string_local,
                                               c->c2.options_string_remote);
                        multi->opt.local_options = local;
                        multi->opt.remote_options = remote;
            '''初始化输出速度限制'''
            if (c->mode == CM_P2P)  //满足
                do_init_traffic_shaper
                    '''初始化流量shaper，亦即传输带宽限制'''
                    if (c->options.shaper)  //不满足
            '''只进行一次的初始化，可能在这里变成一个守护程序
               每个程序实例只进行一次
               为可能的 UID/GID 降级进行设置，但暂时不要这样做
               如果需要，则变成守护程序'''
            do_init_first_time
                为 c->c0 申请空间
                '''获取/设置进程的GID'''
                platform_group_get(c->options.groupname, &c0->platform_state_group)
                    清空第二个参数
                    if(第一个参数不为空)   //不满足
                    else
                        return false
                '''获取/设置进程的UID'''
                platform_user_get(c->options.username, &c0->platform_state_user)
                    清空第二个参数
                    if(第一个参数不为空)   //不满足
                    else
                        return false
                c0->uid_gid_specified = false
                '''如果有 --daemo 选项，则执行推迟的chdir'''
                if (c->did_we_daemonize && c->options.cd_dir == NULL)  //不满足
                    platform_chdir("/");  //内部执行平台相关的chdir命令
                '''我们应该改变调度优先级吗？'''
                platform_nice(c->options.nice=0);
            '''初始化插件'''
            open_plugins(c, false, OPENVPN_PLUGIN_INIT_POST_DAEMON);
                if (c->plugins && c->plugins_owned)   //不满足
            '''初始化连接时间定时器
               初始化服务器轮询超时计时器
               此计时器用于 http/socks 代理设置，因此需要在设置之前进行设置'''
            do_init_server_poll_timeout(c);
                update_time();
                if (c->options.ce.connect_timeout) //120
                    c->c2.server_poll_interval->defined = true
                    c->c2.server_poll_interval->n = max(c->options.ce.connect_timeout,0)
                    c->c2.server_poll_interval->last = now
            '''完成TCP/UDP socket的最终操作'''
            do_init_socket_2(c);
                link_socket_init_phase2(sock=c->c2.link_socket, frame=&c->c2.frame, sig_info=c->sig);
                    '''初始化buffers'''
                    socket_frame_init(frame, sock);
                        如果是Windows
                            初始化重叠端口 sock->reads、sock->writes
                        bool b=link_socket_connection_oriented(sock)
                            if(sock)   //满足
                                '''看是否是面向连接的'''
                                link_socket_proto_connection_oriented(sock->info.proto);
                                    return !proto_is_udp(proto)
                            else
                                return false
                        if(b)  //不满足
                            stream_buf_init
                    '''传递要连接/接受的远程名称，以便他们可以测试动态 IP 地址更改'''
                    if (sock->resolve_retry_seconds)  //=100000000
                        remote_dynamic = sock->remote_host;   //"192.168.4.143"
                    '''我们通过inetd还是xinetd启动？'''
                    if (sock->inetd)  // 0
                        ...
                    else
                        '''第二次创建/处理socket的机会'''
                        resolve_remote(sock, 2, &remote_dynamic,  &sig_info->signal_received);
                            '''解决远程地址问题（如果没定义）'''
                            if (!sock->info.lsa->remote_list)  //不满足
                                。。。
                            '''我们应该重用之前活动的远程地址吗'''
                            if (link_socket_actual_defined(&sock->info.lsa->actual))  //满足
                                打印信息，表明使用 192.168.4.143:1194
                                if(remote_dynamic)  //满足
                                    *remote_dynamic = NULL
                            else
                                ...
                        '''如果发现了一个有效的远端，则使用它的地址创建socket'''
                        if (sock->info.lsa->current_remote)     //满足
                            create_socket(sock, sock->info.lsa->current_remote);
                                如果是udp类型
                                    sock->sd = create_socket_udp(addr, sock->sockflags);
                                        socket_descriptor_t sd;
                                        sd = socket(addrinfo->ai_family, addrinfo->ai_socktype, addrinfo->ai_protocol)
                                        sock->sockflags |= SF_GETADDRINFO_DGRAM;
                                        '''假定‘socks代理’的控制socket和数据socket 是用的相同的ip族'''
                                        if (sock->socks_proxy)  //不满足
                                            struct addrinfo addrinfo_tmp = *addr;
                                            addrinfo_tmp.ai_socktype = SOCK_STREAM;
                                            addrinfo_tmp.ai_protocol = IPPROTO_TCP;
                                            sock->ctrl_sd = create_socket_tcp(&addrinfo_tmp);
                                如果是tcp类型
                                    ...
                                '''基于--sndbuf和--rcvbuf配置项，设置socket buffer，否则不设置(默认大小65536)'''
                                socket_set_buffers(sock->sd, &sock->socket_buffer_sizes)
                                '''绑定本地地址/端口'''
                                bind_local(sock, addr->ai_family); 
                                    if (sock->bind_local)   //false
                                        if (sock->socks_proxy && sock->info.proto == PROTO_UDP)
                                            socket_bind(sock->ctrl_sd, sock->info.lsa->bind_local,
                                                        ai_family, "SOCKS", false);
                                        else
                                            socket_bind(sock->sd, sock->info.lsa->bind_local,
                                                        ai_family, "TCP/UDP", sock->info.bind_ipv6_only);
                        '''如果socet到现在还没有被创建'''
                        if (sock->sd == SOCKET_UNDEFINED)
                            '''如果我们没有 --remote 且我们仍没得出要用的协议族
                               我们将使用绑定的第一个'''
                            if (sock->bind_local  && !sock->remote_host && 
                                sock->info.lsa->bind_local)
                                ....
                        '''socket还没定义，给出警告并中止连接'''
                        if (sock->sd == SOCKET_UNDEFINED)  //不满足
                            msg(...)
                            goto done
                        if (sig_info->signal_received)  //不满足
                            goto done
                        if (sock->info.proto == PROTO_TCP_SERVER)   //不满足
                            phase2_tcp_server(sock, remote_dynamic, &sig_info->signal_received);
                        else if (sock->info.proto == PROTO_TCP_CLIENT)  //不满足
                            phase2_tcp_client(sock, sig_info);
                        else if (sock->info.proto == PROTO_UDP && sock->socks_proxy)    //不满足
                            phase2_socks_client(sock, sig_info);
                    phase2_set_socket_flags(sock);
                        根据 sock->sockflags 设置 sock->sd
                        设置 sock->sd 为非阻塞的
                        在套接字上设置路径 MTU 发现选项
                            if(mut_type >=0)   //-1 ,不满足
                                switch (proto_af)  // 0
                                    case AF_INET:  // 2
                                        setsockopt(sd, IPPROTO_IP, IP_MTU_DISCOVER,...)
                                    case AF_INET6: // 23
                                        setsockopt(sd, IPPROTO_IPV6, IPV6_MTU_DISCOVER, ...)
            '''真正的进行UID/GID的降级，如果需要，则chroot
               可能被 --client --pull 或 --up-delay 推迟'''
            do_uid_gid_chroot(c, bool no_delay=c->c2.did_open_tun)
                if (c0 && !c0->uid_gid_chroot_set)  //满足
                    if (c->options.chroot_dir)  //NULL，不满足
                        if (no_delay)
                            platform_chroot(c->options.chroot_dir);
                    '''设置用户和/或组，如果我们想要setuid/setgid'''
                    if (c0->uid_gid_specified)
                        if (no_delay)
                            platform_group_set(&c0->platform_state_group);
                            platform_user_set(&c0->platform_state_user);
            '''初始化各种定时器'''
            if (c->mode == CM_P2P || child)
                do_init_timers(c, bool deferred = false);
                    初始化非活跃计时
                    初始化ping收发计时
                    if(!deferred)
                        初始化建立连接计时
                        初始化occ定时器
                        初始化包id持续时长定时器
                        初始化tmp_int优化，以限制我们在主事件循环中调用tls_multi_process的次数
            '''初始化插件'''
            if (c->mode == CM_P2P || c->mode == CM_TOP)
                open_plugins(c, false, OPENVPN_PLUGIN_INIT_POST_UID_CHANGE);
                    if (c->plugins && c->plugins_owned)  //不满足
                        。。。
            if (child)  //不满足
                pf_init_context(c);
        post_init_signal_catch  
    '''主事件循环'''
    while(true)
        perf_push(PERF_EVENT_LOOP);  //空实现
        '''处理定时器、tls等'''
        pre_select(c);
            '''检查粗定时器'''
            check_coarse_timers(c);
                '''粗定时器精度为1s'''
                process_coarse_timers(c);
           
===========================================================================================================     
                
部分数据结构
    multi_instance *mi->context.c2.es
    multi_instance *mi->context.c2.tls_multi.es
    session->opt->es
    tls_multi *multi->opt.es        
    
    #&<multi_context>
    #存储openvpn的服务状态的结构，只在服务端使用，存储所有vpn隧道和进程级的状态
    struct multi_context multi
    {
        #MC_UNDEF(0)、MC_SINGLE_THREADED（1）、MC_MULTI_THREADED_MASTER（2）
        #MC_MULTI_THREADED_WORKER（4）、MC_MULTI_THREADED_SCHEDULER（8）
        int thread_mode;
        #multi_instance对象的数组，成员可通过peer-id作为下标进行索引，分别对应一个连接
        struct multi_instance **instances;
        #在vpn隧道实例之前传送数据通道包的buffer的集合
        struct mbuf_set *mbuf;   #广播/组播缓冲区列表
        #OpenVPN 的特定状态--使用 TCP 作为外部传输时，分别对应一个连接
        struct multi_tcp *mtcp;
        #当前认证过的客户端的数量
        int n_clients;
        #存储了进程级的配置信息
        struct context top;
        #调度器，用于基于时间的唤醒事件
        struct schedule *schedule;  #schedule的主要成员是时间和优先级
        #最多支持多少个连接
        int max_clients;
        #已认证通过的连接数
        int n_clients;
        。。。
    }
    
    #&<multi_instance>
    #服务器模式下，用于存储一个vpn隧道的状态的结构
    struct multi_instance
    {
        #该vpn隧道实例是什么时候创建的
        time_t created;
        #server/tcp模式下，要发出的数据的队列
        struct mbuf_set *tcp_link_out_deferred;
        struct context context;  #存储该vpn隧道的状态
        。。。
    }
    
    #&<context>
    #该结构代表了一个vpn隧道，用于存储一个隧道的状态信息
    #但也包含一些进程级别的数据，像如配置选项
    struct context
    {
        #标记main主循环的第一次迭代
        bool first_time;
        #从命令行或配置文件中获取的选项
        struct options options; 
        #标记context在openvpn进程中的角色，
        #可以是CM_P2P（0,客户端）、CM_TOP（1,服务端）、CM_TOP_CLONE（2,线程下克隆的CM_TOP）
        #CM_CHILD_UDP（3,CM_TOP的子context）、CM_CHILD_TCP（4,CM_TOP的子context）
        int mode;   
        #存放环境变量
        struct env_set *es; 
        #网络api透明的context
        openvpn_net_ctx_t net_ctx;
        #不同作用域子context结构
        struct context_0 *c0;       
        struct context_1 c1;        
        struct context_2 c2;       
        。。。
    }
    
    #&<context_1>
    #该结构包含的状态不受SIGUSR1重启信号的影响，但会因SIGHUP重启信号而重置
    struct context_1
    {
        #本地和远端的地址
        struct link_socket_addr link_socket_addr;
        #隧道的会话密钥
        struct key_schedule ks;
        #预解析或缓存的主机名
        struct cached_dns_entry *dns_cache;
        #tun/tap虚拟网络接口对象
        struct tuntap *tuntap; 
        #是否随着当前context的清理而销毁
        bool tuntap_owned;  
        #路由信息列表，参--route命令选项
        struct route_list *route_list;
        #http代理对象
        struct http_proxy_info *http_proxy;
        #socks代理对象
        struct socks_proxy_info *socks_proxy;
        #认证用的用户名密码
        struct user_pass *auth_user_pass;
        #配置文件中的数据通道身份验证
        const char *authname;
    }
    
    #&<context_2>
    #存储了因SIGHUP或SIGUSR1信号导致的“重启”以来的状态信息
    struct context_2
    {
        #用于与远端建立tcp/udp连接的socket（link_socket是Windows和linux下socket的透明实现）
        struct link_socket *link_socket;   
        #远端的ip地址
        struct link_socket_actual *to_link_addr;
        #过来的数据包的地址
        struct link_socket_actual from; 
        #活动的MUT帧参数
        struct frame frame; 
        #tls模式密码对象，存储vpn隧道的tls状态信息,注意tls_multi对象只会创建一个，而不是一个列表
        struct tls_multi *tls_multi;
        #两端必须匹配的选项字符串
        char *options_string_local;
        char *options_string_remote;
        #用于处理包的buffer
        struct context_buffers *buffers;
        #下面的三个buffer并不实际分配内存，而是指向上面的 buffers
        struct buffer buf;
        struct buffer to_tun;
        struct buffer to_link;
        #在读link或tun时等待多久
        struct timeval timeval;
        #粗精度定时器的下次唤醒时间
        time_t coarse_timer_wakeup
        #要传给脚本的环境变量
        struct env_set *es;
        bool es_owned;
        。。。
    }
    
    #&<tls_multi>
    #启用 TLS 的情况下运行的活动 VPN 隧道有一个tls_multi对象，
    #其中存储所有控制通道和数据通道安全参数状态。
    #此结构可以包含多个（可能同时处于活动状态）tls_context对象，
    #以允许在会话重新协商期间进行无中断的转换。
    #每个tls_context代表一个控制通道会话，
    #该会话可以跨越存储在key_state结构中的多个数据通道安全参数会话。
    struct tls_multi
    {
         #常量选项和配置信息
        struct tls_options opt;
        #该列表将会被数据通道扫描
        #KEY_SCAN_SIZE=3，第一个是"active key", 
        #第二个是与"active key"的 session_id 关联的 lame_duck 或停用的key
        #第三个适用于分离的lame_duck会话，
        #这种情况只发生在重新协商活动钥匙失败，但lame_duck钥匙仍然有效的情况下。
        struct key_state *key_scan[KEY_SCAN_SIZE];  #指向对应session的key成员
        #拥有3(TM_SIZE)个tls_session对象：
        #第一个(TM_ACTIVE)是当前的，tls认证过的
        #第二个(TM_UNTRUSTED)拥有处理新客户端的连接请求，如果认证成功，则篡夺当前session
        #第三个(TM_LAME_DUCK)是一个仓库：主session因为错误而重置，而Lame duck keys还没过期
        #    Lame duck keys用于保持在保持key被重新协商时，数据通道连接的持续性
        struct tls_session session[TM_SIZE];
        #当前已经协商的会话的数量
        int n_sessions; 
        #从对端的控制通道上接收的多行通用信息字符串
        char *peer_info;
        。。。
    }
    
    #&<key_state>
    #存储量控制通道的tls状态和数据通道的密码状态，
    #还包含了“可信层结构”--用于控制通道的消息[传输]
    struct key_state
    {
        #从客户端发送的身份验证令牌的状态
        int state;
        #key_state的id，继承自tls_session
        int key_id;
        #包含ssl对象和控制通道的BIO对象
        struct key_state_ssl ks_ssl;
        #对端的随机的会话id
        struct session_id session_id_remote; 
        #持有一个发出的包的副本，知道收到ACK回复
        struct reliable *send_reliable; 
        #对端的ip地址
        struct link_socket_actual remote_addr;
        #数据通道的密码选项
        struct crypto_options crypto_options
        #在我们传递给 TLS 之前对传入的密文数据包进行排序
        struct reliable *rec_reliable; 
        #缓存我们要回复给发送者的所有包id
        struct reliable_ack *rec_ack
        #什么时候state变为S_ACTIVE的
        time_t established;         
        #在这个时间之前还没完成密钥协商，则认为超时
        time_t must_negotiate;   
        #该对象将在这个时间时销毁
        time_t must_die;         
        。。。
    }
    
    #&<tls_session>
    #存储一个会话的安全参数信息（会话属于隧道）
    #该结构对应一个vpn的端到端的控制通道session
    struct tls_session
    {
        struct tls_options *opt;  #常量选项和配置信息
        struct session_id session_id;
        int key_id; #用以跟踪renegotiations
        。。。
    }
    
    
    &<结构变量使用情况追踪>
    main中的 context c; 
        负责配置项
        负责插件
        负责日志
        负责管理子系统
        负责环境变量
    
    tunnel_server_udp_single_threaded中的 context c （指向main中的 context c）
        负责context_2
            让context_2的es继承main中context的环境变量
            负责context_2的link_socket
        负责sig信号
        负责context_1
        负责配置项
    
    tunnel_server_udp_single_threaded中的 multi_context multi;
        根据context top，初始化multi
        继承context top，并对其中一些值进行修改
            mode改为CM_TOP_CLONE（防止close_instance关闭父类的资源句柄）
            first_time = false
            c0 = null
            c2.tls_multi = null
            c1.xxx_owned = false
            c2.xxx_owned = false
            ...
        
        
tunnel_server的内循环  #&<tunnel_server的内循环>
    tunnel_server_udp_single_threaded(context *top)
        multi_context multi;
        '初始化顶层context的c2'
        top->mode = CM_TOP;
        context_clear_2(top)
        '初始化一个隧道实例，'
        '如果是linux，还设置在初始化隧道实例过程中的信号捕获函数'
        '隧道实例初始化前，设置只捕获SIGINT和SIGTERM信号'
        '隧道实例初始化完成后，增加捕获SIGNHUP、SIGUSR1、SIGUSR2'
        init_instance_handle_signals(top, top->es, CC_HARD_USR1_TO_HUP);
            '''
            让top.c2.es继承top.es
            如果使用了management，则在这里暂停一个设置时长，等待客户连接
            根据top.options.connection_list，设置top.options.ce 
            初始化插件
            让top.c1.status_output维护管理--status文件
            让top.c1.ifconfig_pool_persist维护管理 ifconfig-pool 持久化对象
            创建并设置top.c1.http_proxy
            创建并设置top.c1.socks_proxy
            创建top.c2.link_socket
            创建并设置top.c2.fragment（根据top.c2.frame）
            创建并设置top.c1.ks.ssl_ctx   //全局 SSL context
            创建并设置top.c1.ks.key_type  //标记用哪种cipher、HMAC摘要和key长度
            修改top.c2.frame.extra_frame的值
            创建并设置top.c2.tls_multi或top.c2.tls_auth_standalone
            初始设置top.c2.link_socket
            创建并设置top.c1.tuntap
            创建top.c1.route_list（路由表）
            初始化top.c1.route_list
            设置top.c1.tuntap.hand（即打开tap/tun设备），并配置tun/tap设备的ip等
            如果配置了management，等待客户连接，否则sleep(n=10)秒
            配置top.c1.tuntap（tun/tap设备）的mtu等   
            运行up_script脚本（根据参数设置top.c2.es环境变量，并将之转为字符串传给脚本）
            可能基于选项为top.c1.tuntap添加路由和/或调用route_script路由脚本
            设置top.c2.server_poll_interval（该定时器用于http/socks代理设置）
            再次设置c->c2.link_socket（包括创建tcp/udp连接或服务--绑定本地）
            '''
        multi_init
            '''
            multi.thread_mode=MC_SINGLE_THREADED
            创建 multi.hash、multi.vhash、multi.iter、multi.cid_hash、multi.schedule
            创建 multi.mbuf  //分配广播/组播缓冲区列表（254个）
            创建 multi.ifconfig_pool  //分配一个ifconfig池，252个
            设置 multi.ifconfig_pool  //从 t->c1.ifconfig_pool_persist 文件中加载池数据
            创建 multi.route_helper
            创建 multi.reaper
            设置 multi.local , 根据 top.c1.tuntap->local
            设置 multi.max_clients = topo.options.max_clients = 1024
            创建 multi.instances ， 1024个
            创建 multi.mtcp ，只在tcp模式，， 1024 个
            '''
         multi_top_init   
            '''
            multi.top 继承 top，并对其中一些值进行修改:
            multi.top.mode改为CM_TOP_CLONE（防止close_instance关闭父类的资源句柄）
            multi.top.first_time = false
            multi.top.c0 = null
            multi.top.c2.tls_multi = null
            multi.top.c1.xxx_owned = false
            multi.top.c2.xxx_owned = false
            创建 multi.top.c2.buffers  // 根据 top.c2.frame
                ...
            '''
        。。。
        while(true)
            multi_get_timeout
                '''
                从multi.schedule中找到最早苏醒的instance，记录在multi.earliest_wakeup上
                并将醒来时间与当前时间的差值（如果大于10秒，则设为10秒）存给multi.top.c2.timeval，
                该值控制着我们在link/tun上等多久
                如果从从multi.schedule中获取失败，则multi.top.c2.timeval设置为10s（REAP_MAX_WAKEUP）
                '''
            io_wait
                p2mp_iow_flags(multi)
                '''
                设置flags
                    flags = IOW_WAIT_SIGNAL
                    如果 multi.mbuf 不为空 ，flags |= IOW_MBUF, 否则 flags |= IOW_READ
                    检查 multi.top.c1.tuntap 是否为 WINDOWS_DRIVER_WINTUN， 是：
                        检查设备的 ring 是否为空，是：
                            去掉 flags 中的 IOW_READ_TUN
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
                    如果 flags 包含 IOW_TO_LINK 。。。
                    如果 flags 不包含 IOW_FRAG 或 multi.top.c2.fragment->outgoing.len 为 0，
                        如果 flags 包含 IOW_READ_TUN （满足）， int tuntap |= EVENT_READ
                    如果 flags 包含 IOW_TO_TUN ， tuntap |= EVENT_WRITE ，否则，若 flags 包含 IOW_READ_LINK , 则 int socket |= EVENT_READ 
                    如果 flags 包含 IOW_MBUF， socket |= EVENT_WRITE
                    如果 flags 包含 IOW_READ_TUN_FORCE， tuntap |= EVENT_READ
                    '''
                    socket_set
                    '''
                    根据socket的值，设置 multi.top.c2.link_socket，
                        如果 socket 包含 EVENT_READ （如果是面向连接的，还要再做些读操作的前置工作）
                            如果 sock->reads.iostate  == IOSTATE_INITIAL（0） 。。。
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
                        启动异步读tun/tap设备，设置读到的内容放在 multi.top.c1.tuntap.reads.buf
                        如果函数返回失败，错误原因是：ERROR_IO_PENDING（重叠 I/O 操作在进行中），
                        则设置 multi.top.c1.tuntap.reads.iostate = IOSTATE_QUEUED
                    '''
                    (this)
                    '''
                    如果没在 multi.top.sig.signal_received 上产生信号
                        如果 flags 不包含 IOW_CHECK_RESIDUAL
                            event_wait
                                等待 (we_set*)multi.top.c2.event_set)->events
                                如果某个 event 被触发了，则 out 输出参数记录 ((we_set*)multi.top.c2.event_set)->esr[?].arg 
                                int status = 返回触发的事件个数
                                如果 status > 0  , 设置 multi.top.c2.event_set_status 的相应位
                                如果 status = 0 , 设置 multi.top.c2.event_set_status = ES_TIMEOUT
                    '''
            MULTI_CHECK_SIG(&multi);
                '''
                检查信号，判断是否应该中断循环
                '''
            multi_process_per_second_timers
                '''
                处理每秒定时器
                    将 multi.ifconfig_pool 池写入 multi.top.c1.ifconfig_pool_persist 文件
                    。。。
                '''
            if (multi.top.c2.event_set_status == ES_TIMEOUT)
                multi_process_timeout 
            else
                multi_process_io_udp
                    '''
                    根据 multi.top.c2.event_set_status ：
                    处理 MANAGEMENT_READ|MANAGEMENT_WRITE 事件
                    处理 SOCKET_READ 事件
                    处理 SOCKET_WRITE 事件
                    处理 TUN_READ 事件
                        read_incoming_tun
                            等待完成端口，看是否读完了
                            multi.top.c2.buf = multi.c1.tuntap.reads.buf
                            multi.top.c1.tuntap.reads.iostate = IOSTATE_INITIAL
                        multi.top.sig.signal_received 没有收到信号（为0）
                            multi_process_incoming_tun
                                如果 multi.top.c2.buf 不为空
                                    解析 multi.top.c2.buf 上的原始数据包，获取源地址和目标地址
                                    如果目标地址是多播或广播， 。。。
                                    否则，。。。
                    处理 TUN_WRITE 事件
                    '''
                    
tuntap和link分别是如何初始化的                    
    c.c2.link_socket的初始化
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
                                        将其它参数存给c->c2.link_socket的相应项
                                        if (sock->bind_local)
                                            resolve_bind_local(sock, sock->info.af);
                                                if (!sock->info.lsa->bind_local)
                                                    status = get_cached_dns_entry(sock->dns_cache,
                                                                                  sock->local_host,
                                                                                  sock->local_port,
                                                                                  af,
                                                                                  flags,
                                                                                  &sock->info.lsa->bind_local);
                                                        遍历 sock->dns_cache ，
                                                            如果某一项的相关成员能与后四个参数匹配上
                                                            则把该项的ai成员存给最后一个参数，并返回0
                                                            否则，返回-1
                                                    如果 status 不为 0
                                                        status = openvpn_getaddrinfo(flags, 
                                                                                     sock->local_host=0.0.0.0, 
                                                                                     sock->local_port=1194, 
                                                                                     0,
                                                                                     NULL, 
                                                                                     af, 
                                                                                     &sock->info.lsa->bind_local);
                                                            调用 getaddrinfo，根据参数，获得 addrinfo 结构，存给最后一个参数
                                do_init_socket_2(c)
                                    link_socket_init_phase2
                                        socket_frame_init
                                            为socket的read/write完成端口的overlapped.hEvent创建事件对象
                                            并设置sock->rw_handle的read/write成员分别指向这两个事件对象
                                            为socket的read/write完成端口的buf_init申请内存
                                            如果sock是面向连接的
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
                                                        通过 setsockopt 设置 sock->sd 的读写缓冲区大小
                                                    bind_local(sock, addr->ai_family)
                                                        if (sock->bind_local)
                                                            socket_bind(sock->sd, 
                                                                        sock->info.lsa->bind_local,
                                                                        ai_family,
                                                                        "TCP/UDP", 
                                                                        sock->info.bind_ipv6_only);