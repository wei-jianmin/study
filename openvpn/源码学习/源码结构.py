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
    openvpn_main
        struct context c;
        init_static
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
        init_options(&c.options, true); //初始化选项为默认状态
            struct options options;  //记录命令行和配置文件
        parse_argv(&c.options, argc, argv, msglevel=M_USAGE=45056, 
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
        options_postprocess(&c.options);  //对选项的后处理
            options_postprocess_mutate(options);  //处理配置变动
                helper_client_server(o);
                    作为客户端/服务端时，检查配置项配置是否正确，并根据已有配置项进行处理
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
                    设置控制台模式，支持
                    if (。。)  //false
                        打开控制台失败，表明是一个服务
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
            如果不通过管理接口获得密码，则查询密码，跟上当前配置，满足执行条件
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
            open_management(&c)
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
            context_init_1(&c)
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
                c.first_time = false;   //程序范围内的第一次迭代
 
===========================================================================================================
 
// Top level event loop for single-threaded operation.                        
void tunnel_server_tcp(struct context *top) //&tunnel_server_tcp
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
            
file://openvpn的context结构.c+

file://知识点.txt
