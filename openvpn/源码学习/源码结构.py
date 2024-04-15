<catalog s0/s4/s8/s12/s16/s20/s24/s28/s32 catalog_line_prefix=+>
+相关文件：
    file://add_option函数.py
    file://openvpn_help.txt
    file://openvpn的context结构.c+
    file://../知识点.txt
    file://openvpn中ssl的初始化过程.c
    file://ovpnlog--分析1/文件分析.png
    file://ovpnlog--分析1/_抓包分析.txt
    file://ovpnlog/_抓包分析.txt
    file://ovpn协商对称加密密钥.txt
    file://ovpn源码分析-服务端.py
+wmain  
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
    +openvpn_main
        struct context c; 
        /'''init_static简介
         设置随机种子，初始化error相关变量，wsa初始化，初始化信号量
         初始化时间，调用ssl库为程序的数据注册新索引，初始化伪随机数
         '''
        +init_static  #&<对init_static的分析>
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
                        '''CRYPTO_get_ex_new_index(int class_index,
                            long argl, void *argp,
                            CRYPTO_EX_new *new_func,
                            CRYPTO_EX_dup *dup_func,
                            CRYPTO_EX_free *free_func);
                            #define SSL_get_ex_new_index(l, p, newf, dupf, freef) 
                             CRYPTO_get_ex_new_index(CRYPTO_EX_INDEX_SSL, l, p, newf, dupf, freef)
                            CRYPTO_get_ex_new_index 操作特定结构的exdata, argp是当前的exdata项
                            SSL_get_ex_new_index 用于为特定于应用程序的数据注册新索引
                        '''
                        mydata_index = SSL_get_ex_new_index(0, "struct session *", NULL, NULL, NULL);
                    crypto_init_lib
                        内部没有执行任何代码
            prng_init
                crypto.c中的方法，prng : pseudorandom number generator
        /'''SIGHUP引发的循环，一般 ip-fail, tun-abort 会引发这种中断'''
        +do.while(c.sig->signal_received == SIGHUP)
            /'''windows下，该函数执行为空，linux下设置信号处理函数'''
            pre_init_signal_catch
                sig.c文件中的方法，windows下，该函数执行为空，linux下设置信号处理函数
            /'''初始化 context c'''
            context_clear_all_except_first_time
                初始化 context c
            /'''初始化信号信息对象（除了first_time成员）   &<ovpn中的信号对象>
                c.sig是整个context（包括其子结构）中唯一的一个用于记录信号的成员
                它指向的siginfo_static是个文件级的静态变量（sig.c文件中）
                类似的，还有一个win32_signal，是用于记录控制台键盘事件的
                其它还能记录信号的，可能就是win32的重叠端口结构了（overlapped_io）及其关联句柄了
                这样的结构变量有：
                context_2.(link_socket/accept_from).(reads/writes)  <-> context_2.(link_socket/accept_from).rw_handle
                context_1.tuntap.reads/writes <-> context_1.tuntap.rw_handle
                注：context_2中有个 event_set 成员，用做记录等待多个 event 对象
                '''
            CLEAR(siginfo_static)，c.sig = &siginfo_static;  
                siginfo_static为sig.h中的全局变量
                struct signal_info
                {
                    volatile int signal_received;
                    volatile int source;
                    const char *signal_text;
                } siginfo_static;
            /'''垃圾回收机制初始化'''
            +gc_init(&c.gc)
                参：file://垃圾回收机制.txt
            /'''初始化环境变量集合'''
            +c.es = env_set_create(NULL)
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
            /'''初始化用户连接管理器'''
            +init_management  &<init_management>
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
            /'''初始化配置信息，给一些配置项赋初始值'''
            +init_options(&c.options, true); //初始化选项为默认状态 &<对init_options的分析>
                struct options options;  //记录命令行和配置文件
            /'''解析配置参数'''
            +parse_argv(&c.options, argc, argv, msglevel=M_USAGE=45056,    //&<对parse_argv的分析>
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
            /'''插件支持'''
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
            /'''空实现，返回0'''
            net_ctx_init(&c, &c.net_ctx);  
                networking.h中的函数
            /'''初始化日志级别的详细程度'''
            +init_verb_mute(&c, IVM_LEVEL_1);   &<init_verb_mute:1>
            /'''设置 options->dev '''
            +init_options_dev(&c.options);
                if (!options->dev && options->dev_node)  //dev配置项控制，配置文件中指定了 dev tun
                    如果设置了--dev-node配置项，而没有设置--dev项时，该条件满足
                    根据 options->dev_node 的值的basename，设置 options->dev
            /'''打印ssl相关信息'''
            +print_openssl_info(&c.options)
                根据 c.options 中的配置项 show_ciphers、show_digests、show_engines、show_tls_ciphers、show_curves
                控制显示不同的信息（根据当前的配置，这里什么也没有）
            /'''openvpn 创建密钥工具'''
            +do_genkey(&c.options)
                if (options->mlock && options->genkey)
                    分别由 mlock 和 genkey 配置项控制，根据当前配置，这里两者均为false
                后面的所有代码，都是基于 genkey 配置为真的，
                根据当前配置，这些代码均不执行，函数返回false
            如果上面函数执行成功，程序退出
            /'''tuntap工具'''
            +do_persist_tuntap(&c.options, &c.net_ctx)
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
            +options_postprocess(&c.options);  //对选项的后处理 &<对options_postprocess的分析>
                /'''主要设置了 routes、push_list、ncp_ciphers、connection_list 等成员'''
                options_postprocess_mutate(options);  //处理配置变动
                    #helper_xxx : 对复合命令进行展开处理
                    /''' 客户端/服务端 路由相关设置
                     当为服务端，且拓扑为 TOP_NET30 或 TOP_P2P，（todo)
                     当为客户端，设置 o->pull = true; o->pull = true;
                     '''
                    helper_client_server(o);
                        作为客户端/服务端时，检查配置项配置是否正确，并根据已有配置项进行处理
                        服务端
                            if(dev == DEV_TYPE_TUN)  //根据当前配置，dev==DEV_TYPE_TUN
                                //相关参考：file://openvpn网络拓扑.py
                                if (topology == TOP_NET30 || topology == TOP_P2P) //根据当前配置，topology==TOP_NET30
                                    helper_add_route(o->server_network, o->server_netmask, o)
                                        add_route_to_option_list（o->routes,network,netmask,0,0)
                                        ' route_option_list *routes;
                                    push_option(o, print_opt_route(o->server_network + 1, 0, &o->gc), M_USAGE);
                                        根据参数传来的字符串，组织为 push_entry 结构，放入 o->push_list 中
                                        push "route 10.8.0.1"
                                push_option(o, print_opt_topology(topology, &o->gc), M_USAGE);
                                    push "topology net30"
                            else if (dev == DEV_TYPE_TAP)    
                        客户端
                            o->pull = true;   //控制从服务端拉取配置项
                            o->tls_client = true;
                    /'''服务端时，push ping时间间隔'''
                    helper_keepalive(o);  //处理 keepalive 配置项
                        设置 o->ping_rec_timeout_action、o->ping_send_timeout、o->ping_rec_timeout
                        如果 o->mode == MODE_SERVER
                            push "ping 10"
                            push "ping-restart 60"
                    /'''当为服务端，且包含 SF_TCP_NODELAY_HELPER 配置时（当前不满足）提高传输效率'''
                    helper_tcp_nodelay(o);  // 处理 tcp-nodelay 配置项
                        如果 o->server_flags 包含 SF_TCP_NODELAY_HELPER （根据当前配置，不满足该条件，server_flags==0）
                            o->sockflags |= SF_TCP_NODELAY;
                            if (o->mode == MODE_SERVER)
                                push "socket-flags TCP_NODELAY"
                                    TCP_NODELAY选项是用来控制是否开启Nagle算法，
                                    该算法是为了提高较慢的广域网传输效率
                    /'''将 ciphername="SMS4-CBC" 添加到 o->ncp_ciphers 中; o->enable_ncp_fallback = true;'''
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
                    /'''win系统，且为 server 时，options->tuntap_options.tap_sleep = 10; options->route_delay_defined = false;'''
                    options_postprocess_mutate_invariant(o);  //mutate : 使变换，使改变， invariant：不变的
                        如果定义了 _WIN32
                            if (options->mode == MODE_SERVER)
                                options->tuntap_options.tap_sleep = 10;
                                options->route_delay_defined = false;
                    /'''o->ncp_ciphers 过滤掉libcrypto库不支持的算法 '''
                    if (o->ncp_enabled)  //true ,  NCP: 网络控制协议 Network Control Protocol
                        ncp协议简介
                            例如，如果一个用户要拨号进入路由器，该用户的机器一般不知道要使用哪个IP地址，
                            因此必须通过NCP/IPCP协商从路由器获得一个地址
                        o->ncp_ciphers = mutate_ncp_cipher_list(o->ncp_ciphers, &o->gc);
                            过滤掉libcrypto库中不支持的算法（如果发现库不支持的算法就返回空）
                        如果 o->ncp_ciphers 为空，提示存在不支持的 ciphers 或  ciphers的总长度超过127字节
                    /'''将remote_list转为connection_list'''
                    if (o->remote_list && !o->connection_list) //客户端时满足
                    else if (!o->remote_list && !o->connection_list)  
                        struct connection_entry *ace = alloc_connection_entry(o, M_USAGE);
                            struct connection_list *l = alloc_connection_list_if_undef(options);
                                if (options->connection_list == null)
                                    申请 struct connection_list 结构，放到 options->connection_list 中，返回 options->connection_list
                            struct connection_entry *e = 申请 struct connection_entry
                            将 e 放到 l->array[] 中
                            返回 e
                        *ace = o->ce  // o->ce 是在初始化的时候危机感设置的
                    /'''遍历connection_list，根据现有信息，修改/设置一些成员值；
                        if(o->persist_key) 预加载 tls_auth_file、tls_crypt_file、tls_crypt_v2_file'''
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
                    /'''设置o->dh_file = NULL'''
                    if (o->tls_server)
                         if (o->dh_file == "none")  //true
                            o->dh_file = NULL
                    /'''没执行'''
                    if (o->http_proxy_override)  //false
                        options_postprocess_http_proxy_override(o);
                     /'''没执行'''
                     pre_pull_save(o);
                        if (o->pull)  //false
                            ...
                /'''检验配置项'''
                options_postprocess_verify(options);
                    if (o->connection_list)
                        for i in o->connection_list->len  //len=1
                            options_postprocess_verify_ce(o, o->connection_list->array[i]);
                                检查 options->dev 是否为非空 （="tun"）
                                检查ce子成员、option子成员等，如果用法不对，给出提示信息
                /'''检验配置项'''
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
            /'''显示配置信息'''
            +show_settings(&c.options);
                根据配置的调试信息登记，控制显示配置信息
            /'''显示Windows版本信息'''
            +show_windows_version(M_INFO);
                根据配置的调试信息登记，控制显示Windows版本信息
            /'''显示ssl库版本信息'''
            +show_library_versions(M_INFO);
                根据配置的调试信息登记，控制显示ssl库版本信息
            /'''windows下，对控制台进行设置，监视控制台键盘事件'''
            +pre_setup(const struct options *options)
                如果定义了 _WIN32          
                    win32_signal_open(&win32_signal,
                                      int force=WSO_FORCE_CONSOLE,
                                      const char *exit_event_name=NULL,
                                      bool exit_event_initial_state=false);
                        尝试设置控制台模式，禁止输入
                        如果上面的尝试失败了，表明是一个服务
                        设置控制台消息处理钩子函数为：win_ctrl_handler，处理ctrl+c或break事件
                    如果为控制台，设置控制台标题
            /'''在加密子系统上做环回测试'''
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
                程序退出
            /'''如果配置使用连接管理器，则通过连接管理器获取用户名密码，否则，立即获取用户名密码'''
            检查 (c.options.management_flags & MF_QUERY_PASSWORDS),
                如果不通过管理接口获得密码，则查询密码，根据当前配置，满足执行条件
                init_query_passwords(&c);
                    if (c->options.key_pass_file)  //条件不满足
                        pem_password_setup(c->options.key_pass_file);
                    if (c->options.auth_user_pass_file)   //条件不满足
                        auth_user_pass_setup(c->options.auth_user_pass_file, &c->options.sc_info);
            /'''是第一个循环时，将进程id写入本地文件'''
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
            /'''打开连接管理子系统'''
            +open_management(&c)   //&<对open_management的分析>
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
            /'''等待连接管理密码'''
            if (c.options.management_flags & MF_QUERY_PASSWORDS)  //条件不满谁
                //如果需要，则通过管理界面查询密码
                init_query_passwords(&c);
            /'''将某些选项设置为环境变量'''
            +setenv_settings(c.es, &c.options) 
            /'''主要是清空 c->c1，设置 c->c1 的 ciphername、authname、authname， pkcs11初始化，乱序 c->options.connection_list'''
            +context_init_1(&c)  //&<对main中context_init_1的分析>
                /'''清空 context 的 c1 '''
                context_clear_1(c);
                    CLEAR(c->c1);
                /''' c->c1->fd = -1 '''
                packet_id_persist_init(p=&c->c1.pid_persist);
                    将p的成员初始化为空
                /'''如果配置了 remote_random，则打乱 connection_list 的顺序'''
                init_connection_list(c);
                    if (c->options.remote_random)  //条件不满足
                        len = c->options.connection_list->len
                        foreach i  < len  //功能：乱序 l->array
                            j = rand() % len
                            if (i!=j)
                                l->array[i] 和 l->array[j] 互相交换
                /'''将 c->options 的 ciphername、authname、authname ，存给 c->c1 '''
                save_ncp_options(c);
                    c->c1.ciphername = c->options.ciphername;
                    c->c1.authname = c->options.authname;
                    c->c1.keysize = c->options.keysize;
                /'''pkcs11（密码设备接口，主要是应用于智能卡和HSM）初始化'''
                if (c->first_time) //true
                    pkcs11_initialize(protected_auth=true, nPINCachePeriod=c->options.pkcs11_pin_cache_period=-1);
                    foreach c->options.pkcs11_providers[i]  //该数组为空，条件不满足
                        pkcs11_addProvider(...)
            /'''因SIGUSR1引发的循环，一般网络通信故障会引发这种信号'''
            +do.while(c.sig->signal_received == SIGUSR1)
                /'''客户端/服务端隧道通信：tunnel_point_to_point 或 tunnel_server_udp 内部都是个循环，正常不会退出'''
                +switch(c.options.mode)  // = 1
                     /'''处理客户端的通信过程，该函数内有个循环'''
                     +case MODE_POINT_TO_POINT:
                        tunnel_point_to_point(&c);   //参：@对tunnel_point_to_point的分析
                     /'''处理服务端的通信过程，该函数内有个循环'''
                     +case MODE_SERVER:
                        tunnel_server(top=&c);
                            if (proto_is_udp(top->options.ce.proto))
                                tunnel_server_udp(top);
                            else
                                tunnel_server_tcp(top);  //@tunnel_server_tcp
                +c.first_time = false;   //程序范围内的第一次迭代
                /'''如果隧道通信是因为收到信号而退出，则打印信号内容'''
                +if(c->sig->signal_received)
                    print_signal(c.sig, NULL, M_INFO);
                /'''将重启信号传递给管理子系统（重启连接管理子系统）'''
                +signal_restart_status(c.sig);
===========================================================================================================
 
// Top level event loop for single-threaded operation.                        
+&<对main中的tunnel_server_tcp的分析>
.void tunnel_server_tcp(struct context *top) 
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
+&<对init_instance的分析>
//初始化一个隧道实例
/void init_instance(struct context *c, const struct env_set *env, const unsigned int flags)    //&init_instance     
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
                    '''
                       完成全局用的c1.ks.ssl_ctx的初始化
                       完成对称加密用的c1.ks.key_type的初始化
                       完成伪随机数的初始化
                       完成使用认证传输数据（tls-auth）时用的c1.ks.tls_auth_key_type的初始化
                       完成使用tls握手加密（tls-crypt）时用的c1.ks.tls_wrap_key的初始化
                       '''
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
+file://openvpn的context结构.c+

&<文件：知识点>
file://知识点.txt

'''客户模式下的vpn主事件循环，只有一个vnp隧道是激活的'''
&<对tunnel_point_to_point的分析>
+tunnel_point_to_point  //客户端模式主循环
    '''清空c->c2'''
    context_clear_2(c)
    '''设置端到端模式'''
    c->mode = CM_P2P;
    '''初始化隧道实例，处理之前和之后的信号集合'''
    +init_instance_handle_signals(c, c->es, CC_HARD_USR1_TO_HUP);
        +pre_init_signal_catch
            window下什么也没执行
        '''初始化隧道实例简介：
            让c->c2.es 继承 env
            为连接管理子系统（如果启用了）设置回调函数
            计划性暂停
            果配置为交互模式（当前不是），则再次查询用户名密码
            预先对域名进行解析（条件不满足）
            c->options.ce = c->options.connection_list[++i]
            警告不一致的选项
            初始化插件
            设置tls错误时，是产生SIGUSR1信号（√），还是产生SIGTERM信号
            打开--status指定的文件
            打开--ifconfig-pool-persist指定的文件
            重置occ（OpenVPN Configuration Control）状态
            初始化event事件，(用于等待io)
            初始化http和socks代理（在level2的生命周期内）
            为c->c2.link_socket申请对象
            初始化分片对象（没执行）
            初始化压缩库，没执行
            初始化加密层，主要涉及 c->c1.ks.ssl_ctx、c->c1.ks.key_type、c->c2.tls_multi
            初始化压缩库，没执行
            初始化MTU相关变量
            初始化工作区c->c2.buffers
            初始化tcp/udp socket ： 主要是设置 c->c2.link_socket 的各成员值
            初始化tun/tap设备对象（没有执行），打开设备，ifconfig，执行up脚本，等等
            根据本地和远程通道相关选项，转为字符串描述，并设置给 c->c2.tls_multi->opt
            初始化输出速度限制，没有执行
            打开插件 OPENVPN_PLUGIN_INIT_POST_DAEMON，没有执行
            设置初始连接时间定时器
            完成TCP/UDP socket的最终操作
            初始化各种定时器
            打开插件 OPENVPN_PLUGIN_INIT_POST_UID_CHANGE，没有执行
            '''
        +init_instance  //Initialize a tunnel instance.
            '''让c->c2.es 继承 env'''
            +do_inherit_env(c, env);
            '''为连接管理子系统（如果启用了）设置回调函数'''
            if (c->mode == CM_P2P)   //true
                init_management_callback_p2p
                    if (management)  //条件不满足
            '''计划性暂停：如果是首次循环，则只在启用了连接管理器时才暂停，等待客户端连接，
               否则（不是第一次循环），则除了有连接管理器会暂停外，
               没有配置连接管理器时，也会暂停一段时间（才开启下次的连接）
               '''
            if (c->mode == CM_P2P || c->mode == CM_TOP)  //true
                do_startup_pause(c);
                    if (!c->first_time)
                        '''如连接服务端失败，SIGUSR1信号导致的‘重启’，等待一段时间后再尝试连接'''
                        socket_restart_pause(c);
                            客户端等待5秒， 如果在所有的 connection_list 上都尝试过4遍了（这是第5遍了），还没建立上连接，
                            则在增加等待时长，每次增加的时长为： sec <<= min(连接失败次数-4,15)
                            sec = min(sec,c->options.ce.connect_retry_seconds_max)  = 300
                            如果启用了连接管理子系统，则该子系统保持（知道连接者发送release ）
                            否则， sleep（sec）
                    else
                        do_hold(0);   //首次执行这里
                            if (management)  //条件不满足
            '''预先对域名进行解析（条件不满足）'''
            if (c->options.resolve_in_advance)   //条件不满足
                do_preresolve(c);
            '''c->options.ce = c->options.connection_list[++i], c->options.unsuccessful_attempts++ '''
            +next_connection_entry(c);
                if(c->c1.link_socket_addr.current_remote && 该链表的下一个不为空)
                    让 c->c1.link_socket_addr.current_remote 指向链表的下一个
                else 
                    if ( persist_remote_ip 为假） #即不使用固定的远端地址
                        clear_remote_addrlist(&c->c1.link_socket_addr, !c->options.resolve_in_advance);
                    else
                        c->c1.link_socket_addr.current_remote = c->c1.link_socket_addr.remote_list;
                    c->options.unsuccessful_attempts++;
                c->options.ce = *c->options.connection_list->array[i++]
                '''如果有最大连接次数限制，则在达到限制次数后，退出程序'''
                if (c->options.connect_retry_max > 0)
                    如果在所有可用的远程地址上分别尝试过 connect_retry_max 次后还没成功，则发送 M_FATAL 信号（exit(1)）
                '''重置ping时间'''
                update_options_ce_post(&c->options);
            '''如果配置为交互模式（当前不是），则再次查询用户名密码
               这意味着，如果配置为交互模式，则如果本次连接服务端失败，
               下次连接服务端前，也会索要密码
               '''
            if (auth_retry_get() == AR_INTERACT)
                init_query_passwords(c);
            '''设置 c->c2.log_rw 布尔项'''
            +init_verb_mute(c, IVM_LEVEL_2);  
                在最外层的SIGHUP循环中也设置过，不过用的是 IVM_LEVEL_1, 
                参 @init_verb_mute:1
                设置 c->c2.log_rw 布尔项
            '''客户端：设置错误延迟（以应对极短的时间内出现一连串的错误），这里设为0'''
            set_check_status_error_delay(P2P_ERROR_DELAY_MS);  //0
                x_cs_err_delay_ms = P2P_ERROR_DELAY_MS = 0（ms）
            '''警告不一致的选项'''
            do_option_warnings(c);
            '''初始化插件（如果配置了使用插件）'''
            open_plugins(c, false, OPENVPN_PLUGIN_INIT_PRE_DAEMON);
            '''启动fast io'''
            do_setup_fast_io(c);
            '''设置tls错误时，是产生SIGUSR1信号（√），还是产生SIGTERM信号'''
            do_signal_on_tls_errors(c);
                c->c2.tls_exit_signal = SIGUSR1;
            '''打开--status指定的文件'''
            do_open_status_output(c);
            '''打开--ifconfig-pool-persist指定的文件'''
            do_open_ifconfig_pool_persist(c);
            '''重置occ（OpenVPN Configuration Control）状态'''
            c->c2.occ_op = -1
            '''初始化event事件，(用于等待io)'''
            do_event_set_init
            '''初始化http和socks代理（在level2的生命周期内）'''
            init_proxy(c);
                根据配置，初始化c->c1.http_proxy和c->c1.socks_proxy
            '''为c->c2.link_socket申请对象'''
            +do_link_socket_new(c);
            '''初始化分片对象（没执行）'''
            if (options->ce.fragmen) //0
                c->c2.fragment = fragment_init(&c->c2.frame)
            '''初始化加密层，主要涉及 c->c1.ks.ssl_ctx、c->c1.ks.key_type、c->c2.tls_multi '''
            +do_init_crypto(struct context *c, const unsigned int flags)
                如果是 CM_TOP 模式（当前），flags = CF_LOAD_PERSISTED_PACKET_ID | CF_INIT_TLS_MULTI
                '''初始化 c->c1 中的ssl环境、加密算法、哈希算法， 初始化 c->c2.tls_multi ：
                   初始化 c->c1.ks.ssl_ctx，包括设置tls配置项，设置密码算法，加载证书，加载私钥文件
                   为 c->c1.ks.key_type 设置加密和哈希算法
                   c->c2.tls_multi = tls_multi_init(&to)  //tls_options to;
                   '''
                +do_init_crypto_tls(c, flags);
                    '''条件不满足，没执行'''
                    +init_crypto_pre
                        '''加载硬件引擎（vpn配置使用硬件引擎时才执行）'''
                        if (c->options.engine)  //为空，不满足
                            crypto_init_lib_engine(c->options.engine);
                        '''从文件中加载持久记录的 packet_id (time and id) （仅一次）, 并设置 state 为真'''
                        if (c->options.packet_id_file)  //为空，不满足
                            packet_id_persist_load(&c->c1.pid_persist, c->options.packet_id_file);
                    '''初始化永久组件:
                       初始化 c->c1.ks.ssl_ctx，包括设置tls配置项，设置密码算法，加载证书，加载私钥文件
                       为 c->c1.ks.key_type 设置加密和哈希算法（ks为 key_schedule 结构变量，记录密钥策略信息）
                       为伪随机数重置nonce(文件全局变量 nonce_data）的初始值为随机值 
                       '''
                    +do_init_crypto_tls_c1
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
                            '''初始化 tls-auth/crypt/crypt-v2 所用的key，没执行'''
                            do_init_tls_wrap_key(c);    /* initialize tls-auth/crypt/crypt-v2 key */
                                if (options->ce.tls_auth_file)  //为空
                                if (options->ce.tls_crypt_file)  //为空
                                if (options->ce.tls_crypt_v2_file)  //为空
                                上面三个条件下，都是设置 c->c1.ks 下的相关值 /* tunnel session keys */
                            '''初始化auth-token的密钥上下文，没执行'''
                            do_init_auth_token_key
                                如果auth_token_generate配置项为真  //false
                                    auth_token_init_secret
                                        根据配置文件的auth_token_secret_file设置 c->c1.ks.auth_token_key
                    '''根据c->c1.ks.key_type.cipher，判断使用长唯一标识符(64位)还是短唯一标识符(32为)'''
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
                        to.renegotiate_seconds = options->renegotiate_seconds - ...;  #默认renegotiate_seconds=3600
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
                        if (flags & CF_INIT_TLS_MULTI)  //满足
                            c->c2.tls_multi = tls_multi_init(&to);
                                struct tls_multi *ret;
                                ret = new tls_multi
                                ret->opt = *to;
                                '''TM_ACTIVE=0 TM_UNTRUSTED=1 TM_LAME_DUCK=2, TM：tls multi'''
                                '''通常一个活动的vpn会话会持有3个tls_session对象；
                                   一个tls认证过的会话，第二个用于处理来自新客户的连接请求，
                                   如果成功通过验证，该客户将取代当前会话，
                                   第三个用作 "跛脚 "钥匙的储存库，以备主会话因错误而重置，
                                   而 "跛脚 "钥匙在过期前仍有剩余时间。 
                                   跛脚钥匙用于保持数据通道连接的连续性，同时正在协商一个新的钥匙
                                   基本上，每隔一段时间，OpenVPN就会重新生成会话密钥并重新协商连接。
                                   跛脚鸭钥匙不过是传出的密钥（正在协商的密钥）。
                                   "lame duck" key是用美国总统的通称来命名的，
                                   指的是在选举中失败或任期届满，但在继任者上台前还有几周任期的总统，
                                   其目的是实现从旧政权到新政权的平稳政治过渡。
                                   OpenVPN定期重新协商一个新密钥，在此过程中，
                                   旧的、过期的密钥被标记为“跛脚鸭”密钥，以允许新旧密钥之间平滑重叠，
                                   以便无缝地过渡到新密钥，没有隧道流量延迟或丢失。
                                   因此，“杀死的跛脚鸭钥匙”是完全无害的，并不意味着重启已经发生
                                   '''
                                '''KS_PRIMARY=0 KS_LAME_DUCK=1, KS=key state'''
                                ret->key_scan[0] = &ret->session[TM_ACTIVE].key[KS_PRIMARY];
                                ret->key_scan[1] = &ret->session[TM_ACTIVE].key[KS_LAME_DUCK];
                                ret->key_scan[2] = &ret->session[TM_LAME_DUCK].key[KS_LAME_DUCK];
                                ret->use_peer_id = false;
                                return ret;
                     if (flags & CF_INIT_TLS_AUTH_STANDALONE)   //不满足
                        c->c2.tls_auth_standalone = tls_auth_standalone_init(&to, &c->c2.gc);
            '''初始化压缩库，没执行'''
            如果options->comp中的压缩算法存在  //false
                c->c2.comp_context = comp_init(&options->comp);
            '''初始化MTU相关变量，主要是设置 c->c2.frame.extra_frame 的值，
               上面 do_init_crypto 也修改了该值，c->c2.frame 是数据通道用的'''
            do_init_frame(c);
                根据压缩、代理、--tun-mtu-extra配置项、socket参数、字节对齐
                等因素，设置增加 c->c2.frame.extra_frame 的值
            '''初始化TLS MTU相关变量：c->c2.frame、c->c2.multi->session[]（重点）：'''
            +do_init_frame_tls(c);  //file://do_init_frame_tls.png
                +do_init_finalize_tls_frame(c)
                    '''对tls_multi的介绍：
                       使用了TLS的vpn隧道，有一个tls_multi对象
                       该对象中存了所有控制通道和数据通道的安全参数
                       该结构可以包含多个(可能同时处于活动状态的)tls_context对象
                       从而允许在会话重新协商时无中断的转换
                       每个tls_context表示一个控制通道
                       它可以跨越key_state结构中的多个数据通道的会话安全参数
                       参：<file://openvpn的context结构.c+>'''
                    +tls_multi_init_finalize(multi=c->c2.tls_multi, frame=&c->c2.frame)
                        '''根据数据通道的帧参数（c->c2.frame）初始化控制通道的帧参数（c->c2.multi->opt.frame）'''
                        +tls_init_control_channel_frame_parameters(data_channel_frame = c->c2.frame, 
                                                                  frame = &c->c2.multi->opt.frame)
                            frame->link_mtu 和 frame->extra_link 继承 data_channel_frame 中的值
                            设置 frame->extra_frame，增加大小
                            frame->link_mtu_dynamic 设置值
                        '''初始化 c->c2.multi->session[] : @tls_session
                           c->c2.multi->session[]->opt = multi->opt
                           c->c2.multi->session[]->session_id = 随机值
                           c->c2.multi->session[]->initial_opcode = 
                           c->c2.multi->session[]->tls_wrap = multi->opt->tls_wrap
                           c->c2.multi->session[]->tls_wrap.opt.packet_id->rec 各成员初始化 :
                               注：session->tls_wrap.opt 是 crypto_options 结构，用于记录通信用的安全参数
                               crypto_options.packet_id 是 packet_id 结构，用于记录发送(send)的包的id，时间
                               和接收的包(rec)的id、时间、naee、seq_backtrack、time_backtrack等等
                           c->c2.multi->session[]->key[KS_PRIMARY] 个成员初始化 :
                               c->c2.multi->session[]->key[KS_PRIMARY]->ks_ssl （key_state_ssl结构）各成员初始化
                                   为各成员创建出相应结构
                                   设置 ssl 成员为接收状态（服务端）或连接状态（客户端）
                                   将 ct_in 和 ct_in 设置给 ssl， 设置 ssl_bio 关联 ssl
                                   struct key_state_ssl 
                                        SSL *ssl;                   /* SSL object -- new obj created for each new key */
                                        BIO *ssl_bio;               /* read/write plaintext from here */
                                        BIO *ct_in;                 /* write ciphertext to here */
                                        BIO *ct_out;                /* read ciphertext from here */
                               c->c2.multi->session[]->key[KS_PRIMARY] 的其它成员设置值或申请相应结构 :
                                   ks->initial_opcode、session->initial_opcode、ks->state、ks->key_id
                                   ks->send_reliable、ks->rec_reliable、ks->rec_ack
                                   ks->plaintext_read_buf、ks->plaintext_write_buf
                                   ks->ack_write_buf、ks->send_reliable、ks->rec_reliable
                                   ks->crypto_options.packet_id->rec
                           '''
                        +tls_session_init(multi = c->c2.multi, session = &c->c2.multi->session[TM_ACTIVE=0])
                        +tls_session_init(multi = c->c2.multi, session = &c->c2.multi->session[TM_UNTRUSTED=1]
                            '''c->c2.multi->session[]->opt指向外层multi->opt'''
                            c->c2.multi->session[]->opt指向外层multi->opt
                            '''c->c2.multi->session[]->session_id设置随机值'''
                            c->c2.multi->session[]->session_id设置随机值
                            '''设置c->c2.multi->session[]->initial_opcode'''
                            if (session->opt->server)
                                session->initial_opcode = 
                            else
                                session->initial_opcode = 
                            '''初始化控制通道的身份认证参数，tls_wrap管理用于（控制通道）身份认证的包的上下文'''
                            session->tls_wrap = multi->opt->tls_wrap;
                            session->tls_wrap.work = alloc_buf(session->opt->frame)
                            '''根据multi->opt，设置 c->c2.multi->session[]->tls_wrap.opt.packet_id->rec(接收的包) 的各成员值
                               注：session->tls_wrap.opt 是 crypto_options 结构，用于记录通信用的安全参数
                               crypto_options.packet_id 是 packet_id 结构，用于记录发送(send)的包的id，时间
                               和接收的包(rec)的id、时间、naee、seq_backtrack、time_backtrack等等'''
                            +packet_id_init
                                session->tls_wrap.opt.packet_id->rec.name = "TLS_WRAP"
                                session->tls_wrap.opt.packet_id->rec.unit = session->key_id
                                if(session->opt->replay_window)
                                    session->tls_wrap.opt.packet_id->rec.seq_list =
                                                                alloc(sizeof(seq_list) * multi->opt->replay_window)
                                    session->tls_wrap.opt.packet_id->rec.seq_backtrack = multi->opt->replay_window;
                                    session->tls_wrap.opt.packet_id->rec.time_backtrack = multi->opt->replay_time
                            '''c->c2.multi->session[]->key[KS_PRIMARY] （@key_state 结构）中各成员的初始化 ：
                               c->c2.multi->session[]->key[KS_PRIMARY]->ks_ssl （key_state_ssl结构）各成员初始化
                                   为各成员创建出相应结构
                                   设置 ssl 成员为接收状态（服务端）或连接状态（客户端）
                                   将 ct_in 和 ct_in 设置给 ssl， 设置 ssl_bio 关联 ssl
                                   注 : struct key_state_ssl 
                                            SSL *ssl;                   /* SSL object -- new obj created for each new key */
                                            BIO *ssl_bio;               /* read/write plaintext from here */
                                            BIO *ct_in;                 /* write ciphertext to here */
                                            BIO *ct_out;                /* read ciphertext from here */
                               c->c2.multi->session[]->key[KS_PRIMARY] 的其它成员设置值或申请相应结构 :
                                   ks->initial_opcode、session->initial_opcode、ks->state、ks->key_id
                                   ks->send_reliable、ks->rec_reliable、ks->rec_ack
                                   ks->plaintext_read_buf、ks->plaintext_write_buf
                                   ks->ack_write_buf、ks->send_reliable、ks->rec_reliable
                                   ks->crypto_options.packet_id->rec
                               '''
                            +key_state_init(tls_session* session, key_state* ks=&session->key[KS_PRIMARY])  &<key_state_init>
                                '''创建tls对象--用于通过BIO读写内存中的ciphertext'''
                                key_state_ssl_init(key_state_ssl *ks_ssl = &session->key[KS_PRIMARY]->ks_ssl, 
                                                   tls_root_ctx *ssl_ctx = &session->opt->ssl_ctx, 
                                                   bool is_server = session->opt->server,
                                                   tls_session *session)
                                    ks_ssl = c->c2.multi->session[]->key[KS_PRIMARY]->ks_ssl
                                    ssl_ctx = c->c2.multi->session[]->opt->ssl_ctx
                                    CLEAR(*ks_ssl);
                                    ks_ssl->ssl = SSL_new(ssl_ctx->ctx)
                                    '''把session指针存给ssl对象，从而能在验证回调中访问它'''
                                    SSL_set_ex_data(ks_ssl->ssl, mydata_index, session);
                                        ks_ssl->ssl->ex_data[mydata_index] = session
                                    '''BIO_f_ssl() returns the SSL BIO method'''
                                    ks_ssl->ssl_bio = BIO_new(BIO_f_ssl())  //ssl bio,用于读写普通文件
                                    ks_ssl->ct_in = BIO_new(BIO_s_mem())    //内存bio，用于写加密文本
                                    ks_ssl->ct_out = BIO_new(BIO_s_mem())   //内存bio，用于读加密文本
                                    '''设置ssl工作在client状态，
                                       对应的，SSL_set_accept_state设置ssl工作在服务器状态'''
                                    SSL_set_connect_state(ks_ssl->ssl);
                                    '''设置ssl从哪里读，往哪里写
                                       当OpenSSL需要从远程侧获取数据时，使用第一个，
                                       而当OpenSSL需要将数据发送到远程侧时，则使用第二个数据
                                       '''
                                    SSL_set_bio(ks_ssl->ssl, ks_ssl->ct_in, ks_ssl->ct_out);
                                    '''BIO_set_ssl(b,ssl,c)设置b内部的SSL指针指向ssl
                                       并使用关闭标记c'''
                                    BIO_set_ssl(ks_ssl->ssl_bio, ks_ssl->ssl, BIO_NOCLOSE);
                                '''设置控制通道的初始化模式''' 
                                设置 ks->initial_opcode、session->initial_opcode、ks->state、ks->key_id
                                '''allocate key source material object'''
                                初始化 ks->send_reliable、ks->rec_reliable、ks->rec_ack
                                '''申请buffer并初始化'''
                                初始化 ks->plaintext_read_buf、ks->plaintext_write_buf、
                                       ks->ack_write_buf、ks->send_reliable、ks->rec_reliable
                                if (session->opt->replay)  //真
                                    packet_id_init
                                        ks->crypto_options.packet_id->rec.name = "SSL"
                                        ks->crypto_options.packet_id->rec.unit = ks->key_id
                                        ks->crypto_options.packet_id->rec.seq_backtrack = multi->opt->replay_window
                                        ks->crypto_options.packet_id->rec.time_backtrack = multi->opt->replay_time
            '''初始化工作区c->c2.buffers'''
            +do_init_buffers(c);
                c->c2.buffers = init_context_buffers(&c->c2.frame);
                    struct context_buffers *b;
                    为b的各成员申请相应的结构 :
                        b = new context_buffers;
                        b->read_link_buf  = alloc_buf(BUF_SIZE(frame));
                        b->read_tun_buf   = alloc_buf(BUF_SIZE(frame));
                        b->aux_buf        = alloc_buf(BUF_SIZE(frame));
                        b->encrypt_buf    = alloc_buf(BUF_SIZE(frame));
                        b->decrypt_buf    = alloc_buf(BUF_SIZE(frame));
                        b->compress_buf   = alloc_buf(BUF_SIZE(frame));
                        b->decompress_buf = alloc_buf(BUF_SIZE(frame));
                    return b
            '''使用已知的frame大小，初始化内部的分片能力（fragmentation capability）'''
            if(options->ce.fragment)  //false
                do_init_fragment
            '''初始化动态MTU变量(max trans unit)'''
            +frame_init_mssfix(&c->c2.frame, &c->options);
                if (options->ce.mssfix)
                    '''动态设置tun的MTU'''
                    frame_set_mtu_dynamic(frame, options->ce.mssfix=1450, SET_MTU_UPPER_BOUND);
            '''初始化tcp/udp socket ： 主要是设置 c->c2.link_socket 的各成员值'''
            +do_init_socket_1(c, link_socket_mode=LS_MODE_DEFAULT=0); //file://do_init_socket_1.png 
                '''link_socket初始化阶段1 ： 主要是设置 c->c2.link_socket 的各成员值'''
                +link_socket_init_phase1(sock=c->c2.link_socket, ......)
                    根据参数传来的值，设置sock的各成员 :
                            mode,           //标记作为服务端监听本机、监听网络，还是作为客户端连接
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
                    '''获取远端的 addrinfo, 存给 sock->info.lsa->remote_list 和 sock->info.lsa->current_remote'''
                    +resolve_remote(sock, 1, NULL, NULL); 
                        '''如果未定义，则解决remote地址 :
                           struct addrinfo *ai = getaddrinfo(...)
                           sock->info.lsa->remote_list = ai;
                           sock->info.lsa->current_remote = ai;
                           '''
                        if (!sock->info.lsa->remote_list)  //满足
                            if (sock->remote_host)  //"192.168.4.143"
                                struct addrinfo *ai;
                                。。。
                                '''成功返回0，失败返回-1，如同getaddrinfo'''
                                state = get_cached_dns_entry( sock->dns_cache,
                                                              sock->remote_host,
                                                              sock->remote_port,
                                                              sock->info.af,
                                                              flags, &ai);
                                    遍历 sock->dns_cache，如果能找到与参数 2,3,4 匹配的条目，
                                    则将该条目的 addrinfo 成员赋值给最后一个参数 ai
                                    失败返回 -1
                                if(state != 0)  //满足
                                    '''转换ipv4或ipv6地址或主机名为 struct addrinfo
                                       如果失败，会在参数指定的n秒后重试'''
                                    status = openvpn_getaddrinfo(flags, sock->remote_host, sock->remote_port,
                                                                 retry, signal_received, sock->info.af, &ai);
                                        内部调用了 getaddrinfo 方法
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
            '''初始化tun/tap设备对象（没有执行），打开设备，ifconfig，执行up脚本，等等'''
            #options->pull 为真，条件不满足, 在 helper_client_server 中被设置为真
            if ( options->up_delay为假 且 options->pull为假 且 
                 (c->mode == CM_P2P 或 c->mode == CM_TOP) )  
                c->c2.did_open_tun = do_open_tun(c);
            c->c2.frame_initial = c->c2.frame;
            '''根据本地和远程通道相关选项，转为字符串描述，并设置给
               c->c2.tls_multi->opt.local_options = c->c2.options_string_local = options_string() 和
               c->c2.tls_multi->opt.remote_options = c->c2.options_string_remote = options_string()
               '''
            +do_compute_occ_strings
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
                c->c2.options_string_local = options_string(o=&c->options, frame=&c->c2.frame, 
                                                            tt=c->c1.tuntap, ctx=&c->net_ctx,
                                                            remote=false, gc=&gc);
                    struct buffer out = alloc_buf(255)
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
                        init_key_type(kt=&kt, ciphername=o->ciphername, authname=o->authname, 
                                      keysize=o->keysize, tls_mode=true, warn=false);
                            kt->cipher = cipher_kt_get(ciphername);
                            kt->cipher_length = cipher_kt_key_size(kt->cipher);
                            kt->digest = md_kt_get(authname);
                            kt->hmac_length = md_kt_size(kt->digest);
                        out += "cipher AES-256-CBC,auth SHA1,keysize 256"
                    '''SSL选项'''
                    out += "tls-auth,key-method 2,tls-client"
                    return out
                c->c2.options_string_remote= options_string(&c->options, &c->c2.frame, 
                                                            c->c1.tuntap, &c->net_ctx,
                                                                    true, &gc);
                    out = "V4,dev-type tun,link-mtu 1557,tun-mtu 1500,\
                           proto UDPv4,keydir 0, cipher AES-256-CBC,auth SHA1,\
                           keysize 256,tls-auth,key-method 2,tls-server"
                if (c->c2.tls_multi)  //满足
                    '''设置本地和远端选项兼容字符串，用于验证本地和远端选项集合的兼容性'''
                    tls_multi_init_set_options(multi=c->c2.tls_multi,
                                               local=c->c2.options_string_local,
                                               remote=c->c2.options_string_remote);
                        multi->opt.local_options = local;
                        multi->opt.remote_options = remote;
            '''初始化输出速度限制，没有执行'''
            if (c->mode == CM_P2P)  //满足
                do_init_traffic_shaper
                    '''初始化流量shaper，亦即传输带宽限制'''
                    if (c->options.shaper)  //不满足
            '''只进行一次的初始化，可能在这里变成一个守护程序
               每个程序实例只进行一次
               为可能的 UID/GID 降级进行设置，但暂时不要这样做
               如果需要，则变成守护程序
               '''
            do_init_first_time   #客户端跟踪结果 ： 该函数里面啥也没干
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
            '''初始化插件，没有执行'''
            open_plugins(c, false, OPENVPN_PLUGIN_INIT_POST_DAEMON);
                if (c->plugins && c->plugins_owned)   //不满足
            '''设置初始连接时间定时器
               初始化服务器轮询超时计时器
               该定时器用于统计一切，直到收到来自服务端或http代理的第一个包
               此计时器在 http/socks 代理启动时使用了，因此需要在这之前进行设置'''
            +do_init_server_poll_timeout(c);
                update_time();  #更新当前时间
                '''
                   server_poll_interval : 
                   Timer for everything up to the first packet from 
                   the *OpenVPN* server socks, http proxy, and tcp packets do not count
                   用于所有的定时器，直到收到来自服务端或http代理的第一个包
                   但 tcp 包不计入在内
                   '''
                if (c->options.ce.connect_timeout) //120
                    c->c2.server_poll_interval->defined = true
                    c->c2.server_poll_interval->n = max(c->options.ce.connect_timeout,0)
                    c->c2.server_poll_interval->last = now
            '''完成TCP/UDP socket的最终操作 ：
               完成sock套接字的创建，如果是服务端，还绑定相应网卡
               '''
            +do_init_socket_2(c);
                +link_socket_init_phase2(sock=c->c2.link_socket, frame=&c->c2.frame, sig_info=c->sig);
                    const char *remote_dynamic = NULL;
                    '''初始化重叠端口: sock->reads、sock->writes'''
                    +socket_frame_init(frame, sock);   &<socket_frame_init>
                        如果是Windows
                            初始化重叠端口 sock->reads、sock->writes
                        '''udp时，该条件不满足'''
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
                    '''我们通过inetd还是xinetd启动？
                       file://inetd和xinetd.py
                       '''
                    if (sock->inetd)  // 0
                        ...
                    else  '''完成sock套接字的创建，如果是服务端，还绑定相应网卡'''
                        '''第二次创建/处理socket的机会（没有执行）
                           根据客户端跟踪结果来看，因为 do_init_socket_1 中已经设置过相应值了
                           所以本次执行基本没做啥事，就是把 remote_dynamic 参数置为 NULL 了
                           '''
                        +resolve_remote(sock, 2, &remote_dynamic,  &sig_info->signal_received);
                            '''解决远程地址问题（如果没定义）'''
                            if (!sock->info.lsa->remote_list)  //不满足，在 do_init_socket_1 中已经设置过了
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
                            '''完成 socket 套接字对象的创建, 如果是服务端，还会绑定相应网卡'''
                            +create_socket(sock, sock->info.lsa->current_remote);
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
                                    if (sock->bind_local)   //false，因为客户端要绑定远端服务器，而不是监听本地网卡
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
                    '''根据 sock->sockflags，设置socket套接字对象的特性'''
                    +phase2_set_socket_flags(sock);
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
               可能被 --client --pull 或 --up-delay 推迟
               客户端跟踪结果 ： 该函数啥也没干
               '''
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
                update_time()  #更新当前时间
                do_init_timers(c, bool deferred = false);
                    '''初始化非活跃计时 ：c->c2.inactivity_interval'''
                    if (c->options.inactivity_timeout)  //=0
                    '''初始化ping发送计时 ：c->c2.ping_send_interval'''
                    if (c->options.ping_send_timeout)   //=0
                    '''初始化ping接收计时 ：c->c2.ping_rec_interval'''
                    if (c->options.ping_rec_timeout)   //=120
                    if(!deferred)  //满足条件
                        初始化建立连接计时 : c->c2.wait_for_connect
                        初始化occ定时器（不满足条件）
                        初始化包id持久定时器（不满足）
                        初始化tmp_int优化，以限制我们在主事件循环中调用tls_multi_process的次数
            '''初始化插件'''
            if (c->mode == CM_P2P || c->mode == CM_TOP)
                open_plugins(c, false, OPENVPN_PLUGIN_INIT_POST_UID_CHANGE);
                    if (c->plugins && c->plugins_owned)  //不满足
                        。。。
            if (child)  //不满足
                pf_init_context(c);
        +post_init_signal_catch  
    '''主事件循环'''
    +while(true)
        '''空实现'''
        +perf_push(PERF_EVENT_LOOP); 
        '''处理定时器、tls等'''
        +pre_select(c);   &<pre_select>
            '''检查粗定时器完成如下定时任务：
               packed-id 存文件
               status 存文件
               检查连接是否建立
               检查是否需要添加路由
               检查c->sig上是否有信号
               检查规定时间内是否收到 ping
               检查是否收到服务端的第一个包
               检查是否到达预定的退出时间了
               检查是否该发送 OCC_REQUEST 消息了
               检查是否该发送 MTU 负载测试了
               检查是否该ping远端了'''
            +check_coarse_timers(c);   &<check_coarse_timers>
                '''coarse_timer_wakeup定时器还没到时，更新该定时器，函数返回'''
                if (now < c->c2.coarse_timer_wakeup)
                    context_reschedule_sec(c, c->c2.coarse_timer_wakeup - now);
                    return
                c->c2.coarse_timer_wakeup = now + 7天
                '''完成如下定时任务：
                   packed-id 存文件
                   status 存文件
                   检查连接是否建立
                   检查是否需要添加路由
                   检查c->sig上是否有信号
                   检查规定时间内是否收到 ping
                   检查是否收到服务端的第一个包
                   检查是否到达预定的退出时间了
                   检查是否该发送 OCC_REQUEST 消息了
                   检查是否该发送 MTU 负载测试了
                   检查是否该ping远端了
                   '''
                process_coarse_timers(c);  &<process_coarse_timers>
                    '''该函数检查第一个参数et（定时器）是否已到时,
                       如果定时器已经到时或超时，则只在第三个参数小于0时，才开启定时器et的下一轮定时，并将剩余时间设置为定时器声明周期
                       如果第二个参数不为空，根据第三个参数是否小于0，设置第二个参数的值：
                       是：剩余时间(可能<0)小于第二个参数的值时，将剩余到时时间存给第二个参数
                       否：第三个参数小于第二个参数的值时，将第三个参数的值存给第二个参数
                       之后在第三个参数小于0，且定时器还没到时时，函数才返回真
                       另一种表述：
                       不使用第三个参数时（传-1）
                           定时器已到时，重置定时器和剩余到时时间，返回真
                           如果第二个参数不为空，还把剩余时间存给第二个参数
                       使用第三个参数时（要求>=0），则只有第二个参数不为空，才有意义
                           定时器已到时，parma2 > param3 ? param2=param3 : (0)
                           定时器没到时，param2 > 剩余时间 ? param2=剩余时间 : (0)
                       另一种表述：
                       当定时器没到达时，计算苏醒时间 wakeup，且 wakeup < tv? tv=wakeup, 返回假
                       当定时器达到时，
                           et_const_retry < 0
                               更新定时器的触发事件 et->last = now，
                               如果该定时器的定时间隔 et->n < tv,  tv = et->n
                               返回真
                           else          //此时不会更新定时器事件
                               如果 et_const_retry < tv, tv = et_const_retry
                               返回假
                       '''
                    &<event_timeout_trigger>
                    event_timeout_trigger(  struct event_timeout *et,
                                            struct timeval *tv,
                                            const int et_const_retry)
                        if(et->defined == false) return false
                        bool ret = false
                        '''et->last是开始时间，et->n是定时时长'''
                        检查et是否已到时，
                            是：
                                if et_const_retry<0  //et_const_retry通常传来的值为-1
                                    et->last = now
                                    ret = true
                                else
                                    wakeup = et_const_retry;
                        如果tv不为空             
                            如果 tv->tv_sec > et->n
                                tv->tv_sec = et->n
                                tv->tv_usec = 0
                        return ret
                    '如果指定了 --replay-persist，则每60秒，将 packed-id 存到文件
                    '如果c->c1.status_output不为空，则定时的写 status 文件
                    '''如果c->c2.wait_for_connect到达，则检查是否建立好连接了
                       注意，这一步之后，会把 c->c2.coarse_timer_wakeup 改为 1
                       '''
                    if (event_timeout_trigger(c->c2.wait_for_connect '=1'，c->c2.timeval，-1))
                        check_connection_established(c);
                    '''检查是否应该发送一个 push_request (对应选项--pull，此处没有配置)'''
                    if (event_timeout_trigger(c->c2.push_request_interval，c->c2.timeval，-1))  
                        check_push_request(c);
                    '''检查是否需要添加路由（对应--route选项，此处没有配置）'''
                    if (event_timeout_trigger(c->c2.route_wakeup，c->c2.timeval，-1))
                        check_add_routes(c);
                    '如果配置了--inactive选项，则检查是否该因失活而退出程序
                    '''如果检测的信号，说明上面哪一步产生错误信号了，则函数退出'''
                    if (c->sig->signal_received) return
                    '''实现如果规定时间内没有收到 ping 则重启'''
                    check_ping_restart(c);
                        if(event_timeout_trigger(c->c2.ping_rec_interval '=120'，c->c2.timeval，-1))
                            trigger_ping_timeout_signal(c);
                    if (c->sig->signal_received) return
                    '''检查规定时间内，是否连服务器的第一个包都还没收到'''
                    if (c->options.ce.connect_timeout '=120' &&
                        event_timeout_trigger(c->c2.server_poll_interval，c->c2.timeval，-1))
                        check_server_poll_timeout(c);
                            if (!tls_initial_packet_received(c->c2.tls_multi))
                                register_signal(c, SIGUSR1, "server_poll");
                    if (c->sig->signal_received) return
                    '''检查是否到达预定的退出时间了'''
                    if (event_timeout_trigger(c->c2.scheduled_exit，c->c2.timeval，-1))
                        check_scheduled_exit(c);
                    if (c->sig->signal_received) return
                    '''根据配置检查是否该发送 OCC_REQUEST 消息了（没配置）'''
                    check_send_occ_req(c);
                        event_timeout_trigger(c->c2.occ_interval，c->c2.timeval，-1)
                            check_send_occ_req_dowork(c);
                    '''根据配置，检查是否该发送 MTU 负载测试了（没配置）'''
                    check_send_occ_load_test(c);
                        event_timeout_trigger(c->c2.occ_mtu_load_test_interval，c->c2.timeval，-1)
                            check_send_occ_load_test_dowork(c)
                    '''根据配置，检查是否该ping远端了（没配置）'''
                    check_ping_send(c)
                        event_timeout_trigger(c->c2.ping_send_interval，c->c2.timeval，-1)
                            check_ping_send_dowork(c);
                设置c->c2.coarse_timer_wakeup为c->c2.timeval的时间（1秒后）
            '''如果粗定时器有信号产生，则函数退出'''
            if (c->sig->signal_received) return
            '''可信层（reliable）数据处理，关键函数是tls_process'''
            +if (c->c2.tls_multi) 
                +check_tls(c);
                    +if( interval_test(&c->c2.tmp_int) )  #起到控制调用tls_multi_process频率的作用
                        '''被顶层循环调用，主要决定是否应该为 active 或 untrusted sessions 调用 tls_process'''
                        +int ret = tls_multi_process(   &<tls_multi_process>
                                            multi               = c->c2.tls_multi,
                                            to_link             = c->c2.to_link,
                                            to_link_addr        = c->c2.to_link_addr,
                                            to_link_socket_info = c->c2.link_socket->info,
                                            wakeup              = &(interval_t wakeup=7天) );
                            +for (int i = 0; i < TM_SIZE; ++i)  #TM_SIZE=3
                                struct tls_session *session = &multi->session[i];
                                struct key_state *ks = &session->key[KS_PRIMARY];
                                struct key_state *ks_lame = &session->key[KS_LAME_DUCK];
                                int active = TLSMP_INACTIVE;
                                '''只有 TM_ACTIVE=0 的session，且其 ks 的状态为 S_INITIAL 时才执行'''
                                if (i == TM_ACTIVE && ks->state == S_INITIAL)
                                    ks->remote_addr = to_link_socket_info->lsa->actual
                                if (ks->state >= S_INITIAL)
                                    struct link_socket_actual *tla = NULL;
                                    '''可信层（reliable）数据处理'''
                                    if (tls_process(multi, session, to_link, &tla, to_link_socket_info, wakeup))  @tls_process
                                        active = TLSMP_ACTIVE;
                                    if(tla)
                                       c->c2.to_link_addr = multi->to_link_addr 
                                                          = *tla; 
                                                          = multi->session[].key[0].remote_addr
                                    '''如果上面的tls_process过程中出了错误，则这里会判断出来'''
                                    if (ks->state == S_ERROR)
                                        。。。
                            '''获取认证状态：
                               遍历multi->key_scan，看有没有状态为>=S_GOT_KEY/S_SENT_KEY的
                               如果有，则检查其有没有认证过？
                               如果认证过了，则返回 TLS_AUTHENTICATION_SUCCEEDED（认证成功）
                               否则，如果有有状态为S_GOT_KEY/S_SENT_KEY的，但没认证过的，返回 TLS_AUTHENTICATION_FAILED
                               否则，返回 TLS_AUTHENTICATION_DEFERRED （认证推迟）
                               '''
                            int tls_auth_state = tls_authentication_status(multi, TLS_MULTI_AUTH_STATUS_INTERVAL);
                            '''检查session->key[KS_LAME_DUCK]，
                               如果其state >= S_INITIAL，
                                   如果其must_die时间超过当前时间，返回真
                                   否则，返回假，wakeup更新为‘到期时间-当前时间’
                               否则，返回假'''
                            if (lame_duck_must_die(&multi->session[TM_LAME_DUCK], wakeup))
                                ...
                            '''如果 TM_UNTRUSTED 的session的KS_PRIMARY key的状态为>= S_GOT_KEY/S_SENT_KEY 的,
                               将之转为 active 的session'''
                            if (DECRYPT_KEY_ENABLED(multi, &multi->session[TM_UNTRUSTED].key[KS_PRIMARY]))
                                move_session(multi, TM_ACTIVE, TM_UNTRUSTED, true);
                            ...
                        if(ret == TLSMP_ACTIVE)
                            interval_action(&c->c2.tmp_int);
                                c->c2.tmp_int->last_action = now
                        '''如果tls_multi_process返回了错误，则触发错误事件'''
                        else if(ret == TLSMP_KILL)
                            register_signal(c, SIGTERM, "auth-control-exit");
                        c->c2.tmp_int->future_trigger = now + wakeup
                    '''根据c->c2.tmp_int的成员值，得到较早的wakeup时间：
                       min(last_test_true+refresh-now, wakeup)
                       min(future_trigger,wakeup)'''
                    interval_schedule_wakeup(&c->c2.tmp_int, &wakeup);
                        min(c->c2.tmp_int
                    if (wakeup) //真
                        c->c2.timeval.tv_sec = min(wakeup,c->c2.timeval.tv_sec)
            +check_tls_errors(c);
            '''如果tls有错误产生，则函数退出'''
            if (c->sig->signal_received) return
            '''如果控制通道上有收到控制信息了，则处理它
               tls_test_payload_len会在multi->session[TM_ACTIVE].key[KS_PRIMARY].state >= S_ACTIVE(6) 时
               返回 ks->plaintext_read_buf（读到的文本内容） 的长度， 否则，返回0
               '''
            +if (tls_test_payload_len(c->c2.tls_multi) > 0)
                +check_incoming_control_channel(c);
            '''检查是否应该发送occ信息
               如果 c->c2.occ_op >= 0 且当前 c->c2.to_link 上没有数据要发送
               '''
            +check_send_occ_msg(c);
                if (c->c2.occ_op >= 0)  #当前为-1，后面可能会修改该值
                    如果 c->c2.to_link 的长度为0 
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
        '''从 c->c2.link_socket(或c->c1.tuntap，不满足)上读，并等待监测读写事件'''
        +io_wait(c, flags);
            +io_wait_dowork(c, flags);
                static int socket_shift = 0;   #depends on SOCKET_READ and SOCKET_WRITE 
                static int tun_shift = 2;      #depends on TUN_READ and TUN_WRITE 
                static int err_shift = 4;      #depends on ES_ERROR 
                uint socket = 0
                uint tuntap = 0
                struct event_set_return esr[4];
                +event_reset(c->c2.event_set);
                '''把win32_signal.in记录到c->c2.event_set中：
                   把c->c2.event_set强转为 we_set 结构，然后设置其成员值：
                   HANDLE* events[n_events] = win32_signal.in.read
                   event_set_return* esr[n_events].rwflags = EVENT_READ 
                   event_set_return* esr[n_events].arg = &err_shift
                   n_events++
                   '''
                +如果flags包含 IOW_WAIT_SIGNAL  #IOW是 io wait 的意思
                    '''把win32_signal.in记录到c->c2.event_set中，
                       err_shift表明如果在win32_signal.in上收到信号，
                       将设置 c->c2.event_set_status 为 ES_ERROR
                       '''
                    +wait_signal(c->c2.event_set, arg=(void *)&err_shift);  &<wait_signal>
                        +if(HANDLE_DEFINED(win32_signal.in.read))  #win32_signal在客户端用于获取控制台键盘输入
                            event_ctl(c->c2.event_set,&win32_signal.in,EVENT_READ,arg) #win32_signal.in是 @rw_handle 结构
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
                                如果上句失败，会产生 D_EVENT_ERRORS 事件
                '''如果有传出数据等待发送，设置局部变量socket的值'''
                if (flags & IOW_TO_LINK)   #满足
                    socket |= EVENT_WRITE;
                '''如果不满足（包含 IOW_FRAG 且 c->c2.fragment 不为空）'''
                else if (!((flags & IOW_FRAG) && TO_LINK_FRAG(c)))   #上句满足，则该句不判断     
                    if (flags & IOW_READ_TUN)  #满足
                        tuntap |= EVENT_READ;
                if (flags & IOW_TO_TUN)   #不满足
                    tuntap |= EVENT_WRITE;
                else if (flags & IOW_READ_LINK)  #满足
                    socket |= EVENT_READ;
                if (flags & IOW_MBUF)    #不满足
                    socket |= EVENT_WRITE;
                if (flags & IOW_READ_TUN_FORCE)  #不满足
                    tuntap |= EVENT_READ;
                if (tuntap_is_wintun(c->c1.tuntap))  #不满足
                    。。。
                '''从c->c2.link_socket上测试读，数据存在 c->c2.link_socket.reads.buf 中，
                   根据读取结果，设置 c->c2.link_socket.reads 的成员值：
                       overlapped.hEvent、status、overlapped.hEvent
                   如果不是 persistent==rwflags，则把 c2.link_socket->rw_handle 记到 c2.event_set 中
                   '''
                +socket_set(s=c->c2.link_socket, es=c->c2.event_set, rwflags=socket, 
                           arg=(void *)&socket_shift, uint*persistent=NULL);
                    +if( rwflags & EVENT_READ)
                        +socket_recv_queue(sock=s, 0);
                            if (sock->reads.io_state == IOSTATE_INITIAL)  #sock->reads是overlapped_io结构
                                调用WSARecvFrom，从socket读，结果存给 sock->reads.buf
                                如果能立即读到内容
                                    sock->reads.io_state = IOSTATE_IMMEDIATE_RETURN;
                                    SetEvent(sock->reads.overlapped.hEvent)
                                    sock->reads.status = 0
                                否则，
                                    如果返回值为：WSA_IO_PENDING  #说明有数据等待读
                                        sock->reads.io_state = IOSTATE_QUEUED;
                                        sock->reads.status = WSA_IO_PENDING;
                                    否则  #没有数据等待读
                                        sock->reads.io_state = IOSTATE_IMMEDIATE_RETURN;
                                        sock->reads.status = WSAGetLastError();
                            return sock->reads.io_state
                    if (!persistent || *persistent != rwflags) 
                        '''把c->c2.event_set强转为 we_set 结构，然后设置其成员值：
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
                    if (tuntap_defined(tt))  #不满足
                '''如果没发生错误，就等待事件集c->c2.event_set，并将等待结果设置给c->c2.event_set_status'''
                +if (!c->sig->signal_received)  #如果c->sig->signal_received有信号，通常是出错信号
                    '''等待 (we_set*)multi.top.c2.event_set)->events
                       如果某个 event 被触发了，则将之记录到out中
                       返回触发的事件个数
                       如果 status > 0  , 设置 multi.top.c2.event_set_status 的相应位
                       如果 status = 0 , 设置 multi.top.c2.event_set_status = ES_TIMEOUT
                       '''
                    +status = event_wait(c->c2.event_set, &c->c2.timeval, esr, SIZE(esr));
                    =we_wait(struct event_set *es, const struct timeval *tv, struct event_set_return *out, int outlen)
                        dword status = WSAWaitForMultipleEvents((we_set*)es->n_events,(we_set*)es->events,FALSE,0,FALSE)
                        如果status>=WSA_WAIT_EVENT_0
                            调用 WaitForSingleObject((we_set*)es->events[i])，检查那个事件触发了
                                将之记录到out参数中
                            返回触发的事件个数
                        如果没有事件触发
                            如果参数tv（120）>0
                                等待，直到有事件触发或超时
                            如果有事件触发了
                                将之记录到out中，返回1
                            如果超时了
                                返回0
                            其它情况
                                返回 -1
                    '''根据事件等待结果esr，设置c->c2.event_set_status'''
                    if(status > 0) #status=3，status>0 表明有事件等到了
                        c->c2.event_set_status = 0;
                        for (i = 0; i < status; ++i)
                            event_set_return *e = &esr[i]
                            c->c2.event_set_status |= ( e->rwflags&3 << e->arg )
                            参：file://openvpn的context结构.c+@io_wait可能返回的事件值
                    else if (status == 0)
                        c->c2.event_set_status = ES_TIMEOUT;
                '''如果这个条件满足，说明在 c->sig 上收到信号了，这一般表明出错了'''
                if (c->c2.event_set_status & ES_ERROR)
                    get_signal(&c->sig->signal_received);
                        *sig = win32_signal_get(&win32_signal);
                            先检查如果 siginfo_static 上收到信号了， 则返回 siginfo_static 的错误码
                            否则检查参数 win32_signal 上的信号值（通常表明有键盘事件了）
        '''检查c->sig'''
        P2P_CHECK_SIG();
            if(c->sig->signal_received)
                '''如果c->sig->signal_received收到的信号为SIGUSR1，可将之映射为c->options.remap_sigusr1'''
                remap_signal(c);
                    if (c->sig->signal_received == SIGUSR1 && c->options.remap_sigusr1)
                        c->sig->signal_received = c->options.remap_sigusr1;
                '''处理SIGUSR1或SIGHUP信号:
                   如果上行条件满足，且定义了 c->c2.explicit_exit_notification_interval（event_timeout结构）
                       如果 c->sig->source == SIG_SOURCE_HARD 为真，清空c->sig，返回真，
                       否则设置c->sig为SIGTERM，返回假
                   否则返回假
                   '''
                int brk = process_signal(c);
                    if( c->sig->signal_received==SIGUSR1或SIGHUP 且 
                        c->c2.explicit_exit_notification_interval->defined为真 )
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
            '''连接管理器上收到信号'''
            +if (status & (MANAGEMENT_READ|MANAGEMENT_WRITE))
                。。。
            '''先看socket上是否收到可写信号'''
            +if (status & SOCKET_WRITE)
                '''将c->c2.to_link上的数据发送的目的地址'''
                +process_outgoing_link(c);
                    +如果c->c2.to_link上有数据要写
                        +确保c->c2.to_link_addr（远端地址）有效
                        '''如果使用了流量校正，让shaper知道我们写了多少字节'''
                        if (c->options.shaper) #不满足
                            。。。
                        '''重置ping的计时时间'''
                        if (c->options.ping_send_timeout)
                            event_timeout_reset(&c->c2.ping_send_interval);
                        +'''设置socket的TOS(服务类型)'''
                        link_socket_set_tos(ls=c->c2.link_socket);
                            if (ls && ls->ptos_defined) #ptos_defined为假
                                setsockopt(ls->sd, IPPROTO_IP, IP_TOS, ls->ptos, sizeof(ls->ptos));
                        +'跟踪(打印或记录日志或不执行)发送的包
                        int size_delta=0
                        socks_preprocess_outgoing_link(c, &to_addr, &size_delta);  #内部没有执行
                            if (c->c2.link_socket->socks_proxy)  #不满足
                                if(c->c2.link_socket->info.proto == PROTO_UDP)  #满足
                                    。。。
                        '''将c->c2.to_link上的数据发送的目的地址'''
                        +size = link_socket_write(c->c2.link_socket,&c->c2.to_link,c->c2.to_link_addr);
                            if (proto_is_udp(sock->info.proto))  #满足
                                return link_socket_write_udp(sock=c->c2.link_socket, buf=c->c2.to_link, to=c->c2.to_link_addr);
                                    '''如果重叠端口的状态为排队或立即返回（不是IOSTATE_INITIAL），检查重叠端口发送结果，如果出错，则报错'''
                                    如果 sock->writes->iostate 为 IOSTATE_QUEUED(1) 或 IOSTATE_IMMEDIATE_RETURN(2)  #为0，不满足
                                        '''看重叠端口处理完了没有，成功处理完，返回收发的数据长度，还在收发或者出错，都返回-1
                                           如果buf参数不为空，还会在成功处理完成的情况下，把重叠端口上的数据存给buf（适用于读）
                                           另外，收发完成（不管是成功还是失败）了，还会把重叠端口的事件恢复为未触发状态
                                           如果第三个参数from不为空，则还会把重叠端口上记录的ip地址存给from参数
                                           具体：
                                               传入的参数io，为重叠端口，
                                               如果该重叠端口的状态为 IOSTATE_INITIAL，说明该重叠端口没有监控socket上数据的收发
                                                   通常这种情况不应该出现，因为我们知道前面我们是用重叠端口监视了socket的，
                                                   那出现这种情况，怀疑是不是参数错了，不管为什么会出现这种情况，我们只是把返回值设为-1
                                               如果该重叠端口的状态为 IOSTATE_IMMEDIATE_RETURN，说明该重叠端口已经完成收发了（但不代表没出错）
                                                   设置重叠端口的状态为 IOSTATE_INITIAL，同时消除重叠端口的事件触发状态
                                                   如果是因为出错而返回，则设置返回值为-1
                                                   如果是成功返回的，设置返回值为读到的字节数，若参数buf不为空，则把重叠端口中记录的数据存给buf
                                               如果该重叠端口的状态为 IOSTATE_QUEUED，说明该重叠端口还没完成收发，还在进行中
                                                   此时，再检查该重叠端口，看其完成收发了没有
                                                       如果完成了（也可能是出错了），设置重叠端口的状态为 IOSTATE_INITIAL，同时消除重叠端口的事件触发状态
                                                           如果成功，设置返回值为读到的字节数，若参数buf不为空，则把重叠端口中记录的数据存给buf
                                                           如果失败了，则设置返回值为-1
                                                       如果没完成，则什么也不做（返回值默认为-1）
                                           '''
                                        socket_finalize(s=sock->sd, io=&sock->writes, buf=NULL, from=NULL);  &<socket_finalize>
                                            '''上次的发送结果为IOSTATE_QUEUED（排队的）'''
                                            if （sock->writes->iostate == IOSTATE_QUEUED）
                                                BOOL status = WSAGetOverlappedResult(s=sock->sd, io=sock->writes->overlapped, ...)
                                                if (status) #成功表示重叠端口操作已经成功完成，失败表没有完成或出错了
                                                    if(buf) *buf = io->buf;
                                                    io->iostate = IOSTATE_INITIAL;
                                                    ResetEvent(io->overlapped.hEvent)
                                                else
                                                    if (WSAGetLastError() != WSA_IO_INCOMPLETE)  #不是重叠端口还没完成的情况，即出错了
                                                        io->iostate = IOSTATE_INITIAL;
                                                        ResetEvent(io->overlapped.hEvent)
                                                        msg(D_WIN32_IO | M_ERRNO, "WIN32 I/O: Socket Completion error");
                                            '''上次的发送结果为IOSTATE_IMMEDIATE_RETURN（立即成功返回了）'''
                                            if （sock->writes->iostate == IOSTATE_IMMEDIATE_RETURN
                                                io->iostate = IOSTATE_INITIAL;
                                                ResetEvent(io->overlapped.hEvent)
                                                '''上次发送结果不为0'''
                                                if (io->status)
                                                    msg(D_WIN32_IO | M_ERRNO, "WIN32 I/O: Socket Completion non-queued error");
                                                else  #上次发送结果为成功
                                                    ret = io->size;
                                            if (from) #不满足
                                                。。。
                                    '''将c->c2.to_link的内容发送到目的地址，设置sock->writes.overlapped.hEvent'''
                                    socket_send_queue(sock=c->c2.link_socket, buf=c->c2.to_link, to=c->c2.to_link_addr);
                                        if (sock->writes.iostate == IOSTATE_INITIAL)  #满足
                                            #sock->writes.buf 在 @socket_frame_init 函数中完成的初始设置,buf_init.offset=548, buf_init.len=1640
                                            sock->writes.buf = sock->writes.buf_init;
                                            sock->writes.buf.len = 0;
                                            '''将参数buf的内容，放到sock->writes.buf上'''
                                            buf_copy(&sock->writes.buf, buf)  #这句执行完后，buf_init.offset=548, buf_init.len=14
                                            '''将sock->writes.buf上的有效数据存给wsabuf'''
                                            WSABUF wsabuf[1];
                                            wsabuf[0].buf = BPTR(&sock->writes.buf);
                                            wsabuf[0].len = BLEN(&sock->writes.buf);
                                            '''将wsabuf上的数据发送出去，如果立即发送成功了，返回0，否则返回其他值'''
                                            status = sock->writes.status = WSASendTo(...)
                                            if (0==status)  #满足
                                                sock->writes.iostate = IOSTATE_IMMEDIATE_RETURN;
                                            else
                                                if( WSA_IO_PENDING == WSAGetLastError()) #重叠端口成功初始化了，稍后将指示完成
                                                    sock->writes.iostate = IOSTATE_QUEUED;
                                                else  #说明发送错误
                                                    ASSERT(SetEvent(sock->writes.overlapped.hEvent));
                                                    sock->writes.iostate = IOSTATE_IMMEDIATE_RETURN;
                                        return sock->writes.iostate;
                                    return 发送的数据长度，或小于0的值，表示错误
                            else if (proto_is_tcp(sock->info.proto))
                                return link_socket_write_tcp(sock, buf, to);
                        link_socket_write_post_size_adjust(&size, size_delta, &c->c2.to_link);  #内部没有执行
                            if(size_delta>0) #不满足
                                if(size>0)
                                    size -= size_delta
                                    buf_advance(buf, size_delta)
                                    *size = 0
                        if (size > 0)  #表明发送成功，size是发送的字节数
                            '''累计已发送字节数'''
                            c->c2.link_write_bytes += size;
                            link_write_bytes_global += size
                            if (management)  #不满足
                                ...
                            '''实际发送的数据长度，与想发送的数据长度不一致，报错'''
                            if (size != BLEN(&c->c2.to_link))
                                msg(D_LINK_ERRORS, ...)
                        if (c->c2.buf.len > 0) #0，不满足
                            。。。
                        if(size < 0)  #不满足
                            。。。
                    buf_reset(&c->c2.to_link);
            '''再看tuntap上是否收到可写信号'''
            +else if (status & TUN_WRITE)
                。。。
            '''再看socket上是否收到可读信号'''
            +else if (status & SOCKET_READ)
                '''尝试把重叠端口上的数据存给c->c2.buffers->read_link_buf，并让c->c2.buf指向该buffer'''
                +read_incoming_link(c);
                    c->c2.buf = c->c2.buffers->read_link_buf;   #c2.buffers专门用于包处理的Buffers
                    buf_init(&c->c2.buf,FRAME_HEADROOM_ADJ(..))
                    status = link_socket_read(c->c2.link_socket, &c->c2.buf, &c->c2.from);
                        if (proto_is_udp(sock->info.proto))
                            int res = link_socket_read_udp_win32(sock, buf, from);
                                return socket_finalize(sock->sd, &sock->reads, buf, from);
                                    @socket_finalize
                        else if (proto_is_tcp(sock->info.proto))
                            ...
                    '''这句只是用来显示错误信息的'''
                    check_status(status, "read", c->c2.link_socket, NULL); &<check_status>
                    '''这句只是在使用socket代理的情况下才工作'''
                    socks_postprocess_incoming_link(c);
                +if ( ! c->sig->signal_received ) #如果没有出错
                    +process_incoming_link(c);
                        link_socket_info *lsi = c->c2.link_socket_info;
                        +process_incoming_link_part1(c, lsi, false);
                            @process_incoming_link_part1
                        +process_incoming_link_part2(c, lsi, orig_buf);
                            @process_incoming_link_part2
            '''最后看tuntap上是否收到可读信号'''
            +else if (status & TUN_READ)
                。。。
        '''检查c->sig'''
        P2P_CHECK_SIG();         
'''该函数是主事件循环中，处理TLS事项的主要函数，
   当该函数返回 non-error，它将设置wakeup参数为希望下次被调用的时间
   如果我们把一个包存给了 to_link 参数，将返回成功
   to_link 是我们希望发给对端的包数据
   '''
&<tls_process>            
+bool tls_process(  #可信层（reliable）数据处理
                 struct tls_multi *multi,                        = c->c2.tls_multi,
                 struct tls_session *session,                    = multi->session[]
                 struct buffer *to_link,                         = c->c2.to_link,
                 struct link_socket_actual **to_link_addr,       = tla,
                 struct link_socket_info *to_link_socket_info,   = c->c2.link_socket->info
                 interval_t *wakeup)                             = = &(interval_t wakeup=7天)
    struct key_state *ks = &session->key[KS_PRIMARY];      /* primary key */
    struct key_state *ks_lame = &session->key[KS_LAME_DUCK]; /* retiring key */
    bool active = false;
    bool state_change = true;
    '检查是否我们应该触发一个软重启 --  因为需要更换新密钥
    '''重新协商主密钥的几秒后，关闭 lame duck key transition_window
       lame_duck_must_die 函数内，会检查 session->key[KS_LAME_DUCK]->must_die 是否到时
       '''
    +if (lame_duck_must_die(session, wakeup))
        key_state_free(ks_lame, true);
        msg("TLS: tls_process: killed expiring key");
    +while(state_change)
        update_time();
        state_change = false;
        if (ks->state == S_INITIAL)
            '''send_reliable 是个 reliable 结构，里面最多可存放RELIABLE_CAPACITY=8个 reliable_entry 结构，
               实际只用了4个，每个reliable_entry可记录一个数据包（包括有效标记、包id、包数据、操作码、时间等）
               一个 reliable 结构（可信层的数据结构）则代表了vpn的一个方向上的控制通道
               reliable 中有个 hold 标记， 用以控制在 reliable_schedule_now 调用前，不会发送
               reliable_get_buf_output_sequenced 则是定位到包id最小的 reliable_entry 成员，
               并返回其buf（reliable_entry中记录包数据的buffer结构）
               返回前，会设置 buf 的 len=0 和 offset=ks->send_reliable->offset=44
               '''
            +struct buffer *buf = reliable_get_buf_output_sequenced(ks->send_reliable)
            +if(buf)
                ks->must_negotiate = now + session->opt->handshake_window=60s;
                ks->auth_deferred_expire = now + auth_deferred_expire_window(session->opt)=60s;
                '''找到与传入的buf参数对应的那个 reliable_entry，设置其内容：
                   设置其有效标记为真，设置其操作码为7（P_CONTROL_HARD_RESET_CLIENT_V2）
                   设置其包id（0），设置其偏移为 44-4=40，设置其buf内容存入包id'''
                +reliable_mark_active_outgoing(ks->send_reliable, buf, ks->initial_opcode);
                ks->state = S_PRE_START;
                state_change = true;
        '''如果 ks->state 还没 S_ACTIVE，则检查当前时间，是否到达 ks->must_negotiate 的时间了，是，则说明协商超时了'''
        +if (now >= ks->must_negotiate && ks->state < S_ACTIVE) goto error
        '''FULL_SYNC是个宏函数，检查是否 ks->send_reliable 和 ks->rec_ack 都为空,
           一般在发送完后，收到服务端回复之前，会满足该条件'''
        +if (ks->state == S_PRE_START && FULL_SYNC)    
            ks->state = S_START;
            state_change = true;
            if (session->opt->crl_file && 
                session->opt->ssl_flags 不包含 SSLF_CRL_VERIFY_DIR)
                。。。
            '''新的连接，清除旧的X509环境变量'''
            tls_x509_clear_env(session->opt->es);
        '''如果已经发送了key（服务端）或获得了key（客户端）'''
        +if (ks->state == S_GOT_KEY && is_client || ks->state == S_SENT_KEY && is_server)
            ...
        '''to_link=c->c2.to_link，reliable_can_send会检查send_reliable中的保持标记是否为假，且其中有没有有效的包
           当在reliable中准备好了要发包，但还没将之转码存储到c->c2.to_link前，该条件通常是满足的
           '''
        +if (!to_link->len && reliable_can_send(ks->send_reliable))
            int opcode;
            '''找到包id最小的那个reliable_entry,记为best，设置 best->next_try = now+best->timeout(2)
               best->timeout *= 2; 参数 opcode = best->opcode; 返回 best->buf'''
            +buf = reliable_send(ks->send_reliable, &opcode);
            +buffer b = *buf  # b 与 buf 共享 uint8_t *data，其它值则各自拥有
            '''把 ks->rec_ack 的信息prepend到 b 中，并根据需要处理b中的数据内容，以支持认证或加密：
               把 ks->rec_ack 的信息prepend到 b 中
               如果session->tls_wrap.mode为'认证'或'无'标记
                   把session->session_id（8字节） prepend到b中
                   把ovpn头prepend到b中
               如果session->tls_wrap.mode为'认证'标记
                   。。。。
               如果session->tls_wrap.mode为'加密'标记
                   。。。。
               '''
            &<write_control_auth>
            +write_control_auth(session,ks,buf=b,to_link_addr, opcode, max_ack=CONTROL_SEND_ACK_MAX=4, prepend_ack=true) 
                '''把 ack=ks->rec_ack 的信息存入到 b 中：
                   将 ack->len 的值=0（1字节）写入到 b 中（头插法）
                   如果 ack->len > 0，
                       则还把 ack->packet_id[]、 ks->session_id_remote、依次写入到b中
                       还会修改 ack->packet_id[] 的值
                   '''
                reliable_ack_write(ks->rec_ack, buf, &ks->session_id_remote, max_ack, prepend_ack)
                '''把session->session_id(随机值)prepend到b中，把ovpn头（ks->key_id | opcode）prepend到b中'''
                if (session->tls_wrap.mode == TLS_WRAP_AUTH 或 TLS_WRAP_NONE)
                    session_id_write_prepend(&session->session_id, buf)
                if (session->tls_wrap.mode == TLS_WRAP_AUTH)
                    。。。
                else if (session->tls_wrap.mode == TLS_WRAP_CRYPT)
                    。。。
                *to_link_addr = ks->remote_addr
            '''把b交给udp层'''
            +*to_link = b;  
            active = true;
            state_change = true;
            +break;
        '''从接收信任层中获取有效的包，返回其包数据指针
           在客户端收到服务端的第一个连接响应包时，会执行这里
           '''
        buf = reliable_get_buf_sequenced(ks->rec_reliable);
        if(buf)
            int status = 1
            if (buf->len)
                '''把数据写给 ks->ks_ssl->ct_in (ssl)'''
                status = key_state_write_ciphertext(&ks->ks_ssl, buf);
                    ret=bio_write(ks_ssl->ct_in, BPTR(buf), BLEN(buf), "tls_write_ciphertext");
                    '如果成功，成功时清空buf
                    return ret
            if(status == 1)
                '''将该buf对应的rec_reliable中的包设置为非活动的，
                   同时 rec_reliable 中的 packet_id 值增1
                   '''
                reliable_mark_deleted(ks->rec_reliable, buf, true);
                state_change = true;
        '''让buf指向文本缓存区(尝试从ssl上读取数据）'''
        buf = &ks->plaintext_read_buf;
        if (!buf->len)  #如果文件缓存区为空，符合
            buf_init(buf, 0)
            int status = key_state_read_plaintext(&ks->ks_ssl, buf, TLS_CHANNEL_BUF_SIZE);
                '''从ks_ssl->ssl_bio上读取数据'''
                return bio_read(ks_ssl->ssl_bio, buf, maxlen, "tls_read_plaintext");
                    int ret = 0;
                    if (buf->len > 0)
                        int len = buf_forward_capacity(buf);  #buf从 buf->offset+buf->len 开始之后的容量
                        i = BIO_read(bio, BPTR(buf), len);
                        if(i < 0)  #读取失败
                            if (BIO_should_retry(bio)) #下次再试？
                                (0)
                            else
                                crypto_msg(D_TLS_ERRORS, "TLS_ERROR: BIO read %s error", desc);
                                ret = -1;
                        else if(i == 0)  #无数据可读
                            buf->len = 0;
                        else  #读到数据了
                            buf->len = i;
                            ret = 1;
                    return ret
            if(status == 1) #读到数据了
                state_change = true;
                *wakeup = 0;
        '''让buf指向文本写缓冲区，为了发送Key'''
        buf = &ks->plaintext_write_buf;
        if (!buf->len && ( (ks->state == S_START && !session->opt->server)
                           || (ks->state == S_GOT_KEY && session->opt->server) ) )
            '''将key数据、对端信息，用户名密码，OCC等，写到tsl控制通道中（纯文本）'''
            bool b = key_method_2_write(buf, multi, session)
                'buf中写一个 uint32 的 0
                'buf中写 uint8 的 KEY_METHOD_2(2)
                '''buf中写入密钥材料（一个随机数）'''
                key_source2_randomize_write(k2=ks->key_src, buf, session->opt->server)
                    key_source *k = &k2->client / &k2->server;
                    clear(*k)
                    if (!server)
                        '''out中产生随机数，并写入到buf中'''
                        random_bytes_to_buf(buf, out=k->pre_master, sizeof k->pre_master)
                    random_bytes_to_buf(buf, k->random1, sizeof k->random1)
                    random_bytes_to_buf(buf, k->random2, sizeof k->random2)
                '''session->opt->local_options = 
                       V4,dev-type tun,link-mtu 1553,tun-mtu 1500,proto UDPv4,
                       cipher BF-CBC,auth SM3,keysize 128,key-method 2,tls-client
                   '''
                write_string(buf, session->opt->local_options, TLS_OPTIONS_LEN)
                if (auth_user_pass_enabled || #auth_user_pass_enabled为全局变量，根据配置，为真
                    (auth_token.token_defined && auth_token.defined))
                    user_pass *up = &auth_user_pass;
                    '''maxlen<0时，表不限长度'''
                    write_string(buf, str = up->username, maxlen=-1)
                        len = strlen(str) + 1
                        buf_write_u16(buf, len)
                        buf_write(buf, str, len)
                    write_string(buf, up->password, maxlen=-1)
                    if (!session->opt->pull)  #客户端时，pull值为真
                        purge_user_pass(&auth_user_pass, false);
                else
                    write_empty_string(buf) #表示没有用户名
                    write_empty_string(buf) #表示没有密码
                push_peer_info(buf, session)
                    if (session->opt->push_peer_info_detail > 0) #满足
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
                '''如果我们是TLS server，则产生tunnel keys ：
                   如果我们是一个允许NCP的p2mp服务器，
                   第一个密钥的生成会被推迟到连接脚本完成和NCP选项可以被处理之后。
                   因为这总是发生在连接脚本选项可用之后，
                   CAS_SUCCEEDED状态与NCP选项被处理相同，我们没有额外的NCP完成状态。
                   '''
                if (session->opt->server && 
                    (session->opt->mode != MODE_SERVER || 
                     multi->multi_state == CAS_SUCCEEDED) )
                    if (ks->authenticated > KS_AUTH_FALSE)
                        tls_session_generate_data_channel_keys(session)
            state_change = true;
            ks->state = S_SENT_KEY;
        '''让buf重新指向文本缓存区(为了读取Key）'''
        buf = &ks->plaintext_read_buf;
        if (buf->len && ( (ks->state == S_SENT_KEY && !session->opt->server)
                          || (ks->state == S_START && session->opt->server) ) )
            。。。
        '''让buf重新指向文本写缓冲区，为了将要输出的文本写到tls上'''
        buf = &ks->plaintext_write_buf;
        if (buf->len)
            '''客户端的第一个Client Hello包，就是从这里产生的'''
            key_state_write_plaintext(&ks->ks_ssl, buf);
        '''将要输出的数据放到可信层上'''
        if (ks->state >= S_START)
            //在send_reliable中寻找一个空闲的reliable_entry，取出其buf
            buf = reliable_get_buf_output_sequenced(ks->send_reliable);
                int status = key_state_read_ciphertext(&ks->ks_ssl, buf, PAYLOAD_SIZE_DYNAMIC(&multi->opt.frame));
                    '''ks_ssl->ct_out 为 key_state_ssl 结构，成员值有：
                       SSL *ssl;     /* SSL object -- new obj created for each new key */
                       BIO *ssl_bio; /* read/write plaintext from here */
                       BIO *ct_in;   /* write ciphertext to here */
                       BIO *ct_out;  /* read ciphertext from here */
                       之前的代码有有过对这些成员变量的初始化设置
                       这里是从tls层读取加密的数据（读到的为tls解密后的）
                       '''
                    return bio_read(ks_ssl->ct_out, buf, maxlen, "tls_read_ciphertext");
                if (status == 1)  #从ssl层读到数据了
                    '''从send_reliable->array[]中找到与buf对应的那个 reliable_entry，记为 e
                       e->packet_id = rel->packet_id++;
                       buf_write_prepend(buf, e->packet_id)
                       e->active = true;
                       e->opcode = P_CONTROL_V1;
                       e->next_try = 0;
                       e->timeout = rel->initial_timeout;
                       '''
                    reliable_mark_active_outgoing(ks->send_reliable, buf, opcode=P_CONTROL_V1)
                        从 
                    state_change = true;
        +。。。
    '''如果to_link中没有要发送的数据，且 ks->rec_ack 不为空（收到了响应包）'''
    +if (!to_link->len && !reliable_ack_empty(ks->rec_ack))
        buffer buf = ks->ack_write_buf;
        buf_init(&buf，...)
        '''产生回应包
           注：客户端发送了 P_ACK_V1 包后（携带密钥材料），服务端就会发送 ssl 层的 Client Hello
           然后客户端回应 Server Hello，从而相互之间建立起ssl连接
           '''
        write_control_auth(session, ks, &buf, to_link_addr, opcode=P_ACK_V1,
                           max_ack=RELIABLE_ACK_SIZE, prepend_ack=false);
            @write_control_auth
        *to_link = buf;
        active = true;
    '''计算得到wakeup时间'''
    +if (ks->state >= S_INITIAL)
        '''ks->send_reliable中找到最早的打算发送的reliable_entry，将其时间存给wakeup'''
        compute_earliest_wakeup(wakeup,reliable_send_timeout(ks->send_reliable))
        '''如果wakeup的值大于ks->must_negotiate的时间，则设为ks->must_negotiate指定的时间'''
        compute_earliest_wakeup(wakeup, ks->must_negotiate - now);
        '''如果已经建立起连接，wakeup与重新协商时间（renegotiate_seconds）做对比，wakeup=其中较早者'''
        if (ks->established && session->opt->renegotiate_seconds)
            。。。
        如果 wakeup 的值 <=0 ，wakeup = 1， active = true;
    +return active;
    error:  return false;
+&<ovpn控制协议操作码>
    #packet opcode (high 5 bits) and key-id (low 3 bits) are combined in one byte 
    ＃define P_KEY_ID_MASK                  0x07
    ＃define P_OPCODE_SHIFT                 3
    #packet opcodes -- the V1 is intended to allow protocol changes in the future 
    ＃define P_CONTROL_HARD_RESET_CLIENT_V1 1     /* initial key from client, forget previous state */
    ＃define P_CONTROL_HARD_RESET_SERVER_V1 2     /* initial key from server, forget previous state */
    ＃define P_CONTROL_SOFT_RESET_V1        3     /* new key, graceful transition from old to new key */
    ＃define P_CONTROL_V1                   4     /* control channel packet (usually TLS ciphertext) */
    ＃define P_ACK_V1                       5     /* acknowledgement for packets received */
    ＃define P_DATA_V1                      6     /* data channel packet */
    ＃define P_DATA_V2                      9     /* data channel packet with peer-id */
    #indicates key_method >= 2 
    ＃define P_CONTROL_HARD_RESET_CLIENT_V2 7     /* initial key from client, forget previous state */
    ＃define P_CONTROL_HARD_RESET_SERVER_V2 8     /* initial key from server, forget previous state */
    #indicates key_method >= 2 and client-specific tls-crypt key
    ＃define P_CONTROL_HARD_RESET_CLIENT_V3 10    /* initial key from client, forget previous state */
    #define the range of legal opcodes, Since no longer support key-method 1, consider the v1 op codes invalid 
    ＃define P_FIRST_OPCODE                 3
    ＃define P_LAST_OPCODE                  10

            
===========================================================================================================     
                
+部分数据结构
    multi_instance *mi->context.c2.es
    multi_instance *mi->context.c2.tls_multi.es
    session->opt->es
    tls_multi *multi->opt.es        
    
    +&<multi_context>
    #存储openvpn的服务状态的结构，只在服务端使用，存储所有vpn隧道和进程级的状态
    struct multi_context multi
    /{
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
    /}
    
    +&<multi_instance>
    #服务器模式下，用于存储一个vpn隧道的状态的结构
    struct multi_instance
    /{
        #该vpn隧道实例是什么时候创建的
        time_t created;
        #server/tcp模式下，要发出的数据的队列
        struct mbuf_set *tcp_link_out_deferred;
        struct context context;  #存储该vpn隧道的状态
        。。。
    /}
    
    +&<context>
    #该结构代表了一个vpn隧道，用于存储一个隧道的状态信息
    #但也包含一些进程级别的数据，像如配置选项
    struct context
    /{
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
    /}
    
    +&<context_1>
    #该结构包含的状态不受SIGUSR1重启信号的影响，但会因SIGHUP重启信号而重置
    struct context_1
    /{
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
    /}
    
    +&<context_2>
    #存储了因SIGHUP或SIGUSR1信号导致的“重启”以来的状态信息
    struct context_2
    /{
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
    /}
        
    +&<tls_multi>
    #启用 TLS 的情况下运行的活动 VPN 隧道有一个tls_multi对象，
    #其中存储所有控制通道和数据通道安全参数状态。
    #此结构可以包含多个（可能同时处于活动状态）tls_context对象，
    #以允许在会话重新协商期间进行无中断的转换。
    #每个tls_context代表一个控制通道会话，
    #该会话可以跨越存储在key_state结构中的多个数据通道安全参数会话。
    struct tls_multi
    /{
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
    /}
    
    +&<key_state>
    #存储量控制通道的tls状态和数据通道的密码状态，
    #还包含了“可信层结构”--用于控制通道的消息[传输]
    struct key_state
    /{
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
    /}
    
    +&<tls_session>
    #存储一个会话的安全参数信息（会话属于隧道）
    #该结构对应一个vpn的端到端的控制通道session
    struct tls_session
    /{
        struct tls_options *opt;  #常量选项和配置信息
        struct session_id session_id;  #随机数
        ''' during hard reset used to control burst retransmit '''
        bool burst;
        ''' authenticate control packets '''
        struct tls_wrap_ctx tls_wrap;
        int initial_opcode;         ''' our initial P_ opcode '''
        ''' The current active key id, used to keep track of renegotiations.
            key_id increments with each soft reset to KEY_ID_MASK then recycles back
            to 1.  This way you know that if key_id is 0, it is the first key.
        '''
        int key_id; #用以跟踪renegotiations
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
    
    '''记录密钥策略结果信息
       该结构成员的初始化，主要在do_init_crypto_tls::do_init_crypto_tls_c1中完成
       '''
    +&<key_schedule>
    {
        '''记录我们用什么cipher（特指对称加密算法）、HMAC算法、密钥大小'''
        struct key_type key_type;  #这个是对称加密用的数据结构
        '''预共享的静态密钥，从文件中读取'''
        struct key_ctx_bi static_key;
        '''全局用的 SSL context'''
        struct tls_root_ctx ssl_ctx;
        '''下面这些用于对 TLS 控制通道数据的包装（可选），
           对应--tls-auth/--tls-crypt
           与之关联的数据结构是 :
           tls_options.tls_wrap
           tls_auth_standalone.tls_wrap (服务端）
           tls_multi.opt.tls_wrap
           注：
               key_type中包含cipher_kt_t、md_kt_t等成员结构
               而key_ctx中包含cipher_ctx_t、hmac_ctx_t等成员结构
               他们的关系是，cipher_ctx_t中除了包含cipher_kt_t，
               还包含加密用的其它相关参数，能真正完成数据的加密
           '''
        struct key_type tls_auth_key_type;  #这个是使用认证层时，用到的数据结构
        struct key_ctx_bi tls_wrap_key;   #这个是使用认证层时，用到的数据结构
        struct key_ctx tls_crypt_v2_server_key;
        struct buffer tls_crypt_v2_wkc;            ''' Wrapped client key'''
        struct key_ctx auth_token_key;
    };
    
    '''用于记录键盘事件的结构'''
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
    
    
+&<结构变量使用情况追踪>
    +main中的 context c; 
        负责配置项
        负责插件
        负责日志
        负责管理子系统
        负责环境变量
    
    +tunnel_server_udp_single_threaded中的 context c （指向main中的 context c）
        负责context_2
            让context_2的es继承main中context的环境变量
            负责context_2的link_socket
        负责sig信号
        负责context_1
        负责配置项
    
    +tunnel_server_udp_single_threaded中的 multi_context multi;
        根据context top，初始化multi
        继承context top，并对其中一些值进行修改
            mode改为CM_TOP_CLONE（防止close_instance关闭父类的资源句柄）
            first_time = false
            c0 = null
            c2.tls_multi = null
            c1.xxx_owned = false
            c2.xxx_owned = false
            ...
        
        
+tunnel_server的内循环  #&<tunnel_server的内循环>
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
                    
+tuntap和link分别是如何初始化的                    
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

+&<常用宏定义>
    +Tunnel types
        ＃define DEV_TYPE_UNDEF 0
        ＃define DEV_TYPE_NULL  1
        ＃define DEV_TYPE_TUN   2    /* point-to-point IP tunnel */
        ＃define DEV_TYPE_TAP   3    /* ethernet (802.3) tunnel */
    +TUN的组网方式
        ＃define TOP_UNDEF   0
        ＃define TOP_NET30   1
        ＃define TOP_P2P     2
        ＃define TOP_SUBNET  3
    +enum proto_num 
        PROTO_NONE,     /* catch for uninitialized */
        PROTO_UDP,
        PROTO_TCP,
        PROTO_TCP_SERVER,
        PROTO_TCP_CLIENT,
        PROTO_N
    +context modes
        ＃define CM_P2P            0  /* standalone point-to-point session or client */
        ＃define CM_TOP            1  /* top level of a multi-client or point-to-multipoint server */
        ＃define CM_TOP_CLONE      2  /* clone of a CM_TOP context for one thread */
        ＃define CM_CHILD_UDP      3  /* child context of a CM_TOP or CM_THREAD */
        ＃define CM_CHILD_TCP      4  /* child context of a CM_TOP or CM_THREAD */

+&<:tls_multi>
'''共1个tls_multi下面有TM_SIZE=3个tls_session，每个tls_session下面又有KS_SIZE=2个key_state'''
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
            ＃ifdef USE_COMP
            struct compress_options comp_options;
            ＃endif
            ''' configuration file SSL-related boolean and low-permutation options '''
            ＃define SSLF_CLIENT_CERT_NOT_REQUIRED (1<<0)
            ＃define SSLF_CLIENT_CERT_OPTIONAL     (1<<1)
            ＃define SSLF_USERNAME_AS_COMMON_NAME  (1<<2)
            ＃define SSLF_AUTH_USER_PASS_OPTIONAL  (1<<3)
            ＃define SSLF_OPT_VERIFY               (1<<4)
            ＃define SSLF_CRL_VERIFY_DIR           (1<<5)
            ＃define SSLF_TLS_VERSION_MIN_SHIFT    6
            ＃define SSLF_TLS_VERSION_MIN_MASK     0xF  ''' (uses bit positions 6 to 9) '''
            ＃define SSLF_TLS_VERSION_MAX_SHIFT    10
            ＃define SSLF_TLS_VERSION_MAX_MASK     0xF  ''' (uses bit positions 10 to 13) '''
            ＃define SSLF_TLS_DEBUG_ENABLED        (1<<14)
            unsigned int ssl_flags;
            ＃ifdef MANAGEMENT_DEF_AUTH
            struct man_def_auth_context *mda_context;
            ＃endif
            const struct x509_track *x509_track;
            ＃ifdef ENABLE_MANAGEMENT
            const struct static_challenge_info *sci;
            ＃endif
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
                ＃define CO_PACKET_ID_LONG_FORM  (1<<0)
                '''< Bit-flag indicating whether to use
                    OpenVPN's long packet ID format. '''
                ＃define CO_IGNORE_PACKET_ID     (1<<1)
                '''< Bit-flag indicating whether to ignore
                     the packet ID of a received packet.
                     This flag is used during processing
                     of the first packet received from a
                     client. '''
                ＃define CO_MUTE_REPLAY_WARNINGS (1<<2)
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
            ＃ifdef MANAGEMENT_DEF_AUTH
            unsigned int mda_key_id;
            unsigned int mda_status;
            ＃endif
            ＃ifdef PLUGIN_DEF_AUTH
            unsigned int auth_control_status;
            time_t acf_last_mod;
            char *auth_control_file;
            ＃endif
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
        ＃define  AUTH_TOKEN_HMAC_OK              (1<<0)
        '''< Auth-token sent from client has valid hmac '''
        ＃define  AUTH_TOKEN_EXPIRED              (1<<1)
        '''< Auth-token sent from client has expired '''
        ＃define  AUTH_TOKEN_VALID_EMPTYUSER      (1<<2)
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
            ＃ifdef ENABLE_PF
            uint32_t common_name_hashval;
            ＃endif
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
    struct crypto_options *opt = NULL;   &<opt参数定义位置>
    +if (c->c2.buf.len > 0)  #如果读到了数据
        '''记录读到的数据长度'''
        c->c2.original_recv_size = c->c2.buf.len;
        c->c2.link_read_bytes += c->c2.buf.len;
        link_read_bytes_global += c->c2.buf.len;
        '确保收到的包的地址，与c->c2.link_socket_info是一致的
        +if (c->c2.tls_multi)
            '''如果tls_pre_decrypt返回true，意味着收到的包是良好的tls控制通道的包
               如果是这样，则TLS代码将处理该包，并设置buf.len为0，从而后面的步骤不会再处理它了
               如果该包是个数据通道的包，则tls_pre_decrypt会加载正确的加密密钥，并返回假;
               当在TLS模式时，这是第一个看到（处理）收到的包的函数
               如果是数据包，我们设置选项e，从而使得我们的调用者可以解密它
               我们也把对应的解密key给到我们的调用者
               如果是个控制包，我们认证它并处理它
               可能会创建一个新的tls会话（如果他表示的是一个新会话的第一个包）
               对应控制包，我们会把它的buf清零，从而使我们的调用者在我们返回后忽略该包
               注意，ovpn只允许同时有一个活动的会话，所以一个新的会话（一旦认证过）将总是篡夺一个旧的会话
               如果是个认证通过的控制通道的包，返回真，否则返回假
               '''
            '''主要完成的工作（下面只列出了对控制包的处理情况）：
               找到对应的session，设置 session->untrusted_addr = 远端地址
               ks = session->key[KS_PRIMARY]
               ks->session_id_remote = sid（传来的包的会话id）; 
               ks->remote_addr = 远端地址
               ks->send_reliable中相应的包设置为非活动的
               ks->rec_reliable中找到一个可用的的 reliable_entry
                   e = rel->array[]
                   e->active = true;  
                   e->packed_id = pid;  
                   e->opcode= opcode;
                   e->next_try = e->timeout = 0
               如果使用了 -tls-auth 或 --tls-crypt 配置项时，
               还会完成包的验证/解密处理
               '''
            +bool b = tls_pre_decrypt(...)   &<tls_pre_decrypt>  file://ovpn源码分析-服务端.py@tls_pre_decrypt
                uint8_t pkt_firstbyte = *BPTR(buf);
                int op = pkt_firstbyte >> P_OPCODE_SHIFT;  #ovpn包头的高5位是操作码
                +'''是数据包'''
                if ((op == P_DATA_V1) || (op == P_DATA_V2))
                    handle_data_channel_packet(multi, from, buf, opt, floated, ad_start);  @opt参数定义位置
                        for (int i = 0; i < KEY_SCAN_SIZE; ++i)
                            '''注意，key_scan（key_state*结构）是指向不同session的key子成员的'''
                            struct key_state *ks = multi->key_scan[i];
                            '''该if条件是本地vpn实例和其远端，两者之间TSL状态的基本测试
                               如果测试失败，它告诉我们，我们从一个来源获得了一个数据包，
                               该数据包声称参考了先前协商的TLS会话，但本地OpenVPN实例没有关于这种协商的记忆。
                               这几乎总是发生在UDP会话中，当连接的被动端被重启而主动端没有重启时
                               （被动端是服务器，只监听连接，主动端是客户端，发起连接）
                               '''
                            if ( ks->state>=S_GOT_KEY/S_SEND_KEY     && 
                                 key_id == ks->key_id                && 
                                 ks->authenticated == KS_AUTH_TRUE   && 
                                 (floated || link_socket_actual_match(from, &ks->remote_addr) ) ) 
                                '''与远端之间的key还没初始化，丢弃该包'''
                                if (!ks->crypto_options.key_ctx_bi.initialized)
                                    goto done
                                *opt = &ks->crypto_options;   #opt是函数传来的参数，crypto_options **类型  @opt参数定义位置
                                ++ks->n_packets;
                                ks->n_bytes += buf->len;
                                return
                    return false;
                +'''是控制包'''
                int key_id = pkt_firstbyte & P_KEY_ID_MASK;  #ovpn包头的低3位是keyid
                +'''验证包的操作码是否在有效范围'''
                if (op < P_FIRST_OPCODE || op > P_LAST_OPCODE)
                    goto error;  #不在有效范围（不能识别的包操作码）
                +'''如果发来的是通知重置的包，则核实其是否来自正确的对端
                   检查包的控制码，如果是要求重新初始化key（要求忘记之前的状态），则重置c->c2.frame'''
                if (op == P_CONTROL_HARD_RESET_CLIENT_V2 ||    &<is_hard_reset_method2>
                    op == P_CONTROL_HARD_RESET_SERVER_V2 || 
                    op == P_CONTROL_HARD_RESET_CLIENT_V3)   
                    '''确保是对应的服务端或客户端发起的重置'''
                    if (((op == P_CONTROL_HARD_RESET_CLIENT_V2  ||
                          op == P_CONTROL_HARD_RESET_CLIENT_V3) && !multi->opt.server) ||
                          ((op == P_CONTROL_HARD_RESET_SERVER_V2) && multi->opt.server))
                        '''说明该通知重置的包是来自客户端的，但自己才是客户端
                           或该通知重置的包是来自服务端的，但自己才是服务端
                           这显然是不正常的包'''
                        goto error 
                '''开始包的认证'''
                +'从包中获取到会话id（sid，随机值）
                +'''从multi->session[]中找到与sid一致的那个session'''
                for (i = 0; i < TM_SIZE; ++i)  #TM_SIZE: tls_multi（下session）的个数（3个）
                    tls_session *session = &multi->session[i];
                    key_state *ks = &session->key[KS_PRIMARY];
                    if (session_id_equal(&ks->session_id_remote, &sid))  #获取到的会话id，与记录的远端会话id比较
                        if (i == TM_LAME_DUCK)  #匹配了，但这个是与TM_LAME_DUCK的那个session匹配的 
                            goto error
                        break
                '''i == TM_SIZE 通常表明上一步没有找到与包中记录的会话id匹配的那个session
                   如果是这样的情况，且包的操作码是要求重置的情况
                   此时认为这是（新）会话的第一个包
                   注：客户端开始建立连接的时候，服务端回复的第一个包就是 P_CONTROL_HARD_RESET_SERVER_V2 的
                   '''
                +'''检测是不是使用TM_ACTIVE建立一个新的会话'''
                if (i == TM_SIZE && is_hard_reset_method2(op))     @is_hard_reset_method2
                    tls_session *session = &multi->session[TM_ACTIVE];
                    key_state *ks = &session->key[KS_PRIMARY];
                    '''如果还没设置记录远端的会话id（还没建立过任何连接）'''
                    if (!session_id_defined(&ks->session_id_remote))
                        do_burst = true;
                        new_link = true;  #这是个布尔值，标识是新连接
                        i = TM_ACTIVE;  #直接使用 TM_ACTIVE 的session
                        session->untrusted_addr = *from;  #TM_ACTIVE的session中记录远端地址
                '''这里i == TM_SIZE，说明之前已经建立过连接，
                   但那个连接对应的session中记录的sid与收到的包的sid不一致（sid是个随机数）
                   is_hard_reset_method2验证是否是要求重置的包
                   '''
                +'''检测是不是使用TM_UNTRUSTED建立一个新的会话'''
                +if (i == TM_SIZE && is_hard_reset_method2(op))  
                    +'''选择在TM_UNTRUSTED的session上建立连接'''
                    tls_session *session = &multi->session[TM_UNTRUSTED];
                    +'''读取控制通道的认证记录 &<read_control_auth>'''
                    bool b = read_control_auth(buf, ctx=&session->tls_wrap, from,opt=session->opt)
                        uint8_t opcode = *(BPTR(buf)) >> P_OPCODE_SHIFT;
                        if (opcode == P_CONTROL_HARD_RESET_CLIENT_V3)  #是客户端发起的重置包
                            bool b = tls_crypt_v2_extract_client_key(buf, ctx, opt)
                            '''无法从对端提取出tls-crypt-v2的客户端密钥'''
                            if(!b) goto cleanup
                            。。。
                        '''&<控制层安全>：
                           使用--tls-auth file选项，可以给控制层加一层HMAC，
                           对于验证HAMC失败的包，直接丢弃，从而使ovpn免于DDOS攻击
                           该选项如果要用，应该放在服务端的配置文件中
                           类似的，--tls-crypt key可以给tls控制通道添加额外的一层加密
                           这可以起到隐藏tls证书的作用，也可以放置DOS攻击
                           这里的这个ctx变量，是tls_wrap_ctx类型的，
                           而这个结构，就是用于给tls控制层HMAC或加密用的，
                           当然，如果没有使用 -tls-auth 或 --tls-crypt 时（当前配置就是这样），
                           这个变量就没啥用了，此时 ctx->mode 为 TLS_WRAP_NONE
                           '''
                        if (ctx->mode == TLS_WRAP_AUTH)
                            。。。
                        else if (ctx->mode == TLS_WRAP_CRYPT)
                            。。。
                        else if (ctx->tls_crypt_v2_server_key.cipher)
                            。。。
                        +if (ctx->mode == TLS_WRAP_NONE || ctx->mode == TLS_WRAP_AUTH) 
                            +'''将buffer的指针跳过ovpn头（1字节）和会话id（8字节）'''
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
                    +'''不是新连接，但当前远端的地址与ks（成功建立连接）中记录的远端地址不一致
                       攻击的包？
                       '''
                    if (!new_link && !link_socket_actual_match(&ks->remote_addr, from))  goto error
                    +'''P_CONTROL_SOFT_RESET_V1 得体的要求重新更换新的key的控制包(远端要求重新协商密钥)
                       DECRYPT_KEY_ENABLED 展开为：ks->state >= S_GOT_KEY/S_SEND_KEY
                       满足该if条件，说明之前已经协商好key了，现在服务端要求重新更换key
                       '''
                    if (op == P_CONTROL_SOFT_RESET_V1 && DECRYPT_KEY_ENABLED(multi, ks))
                        。。。
                    else
                        if (op == P_CONTROL_SOFT_RESET_V1) do_burst = true;
                        +'''将buf的指针跳过ovpn头（1字节）和会话id（8字节）'''
                        bool b = read_control_auth(buf, &session->tls_wrap, from, session->opt) @read_control_auth
                        if(!b) goto error
                tls_session *session = &multi->session[i];
                key_state *ks = &session->key[KS_PRIMARY];
                '确保session->session_id不为空
                +'''如果是新连接，key_state记录下远端的会话id和地址'''
                if (new_link)
                    ks->session_id_remote = sid;   
                    ks->remote_addr = *from;
                    ++multi->n_sessions;
                +else 
                    +'''key_state中记录的远端地址，与发来包的远端地址不一致，错误'''
                    if (!link_socket_actual_match(&ks->remote_addr, from))  goto error;
                +'''是否应该对发送缓冲区中所有未确认的数据包进行重传?
                   这会提高了第2个对端上线后，初始密钥协商的启动效率。'''
                if (do_burst && !session->burst)
                    '''遍历可信层的每个reliable_entry（包）
                       如果该包是 active 的，则将其 next_try 设置为 now，
                       将其超时时间设置为可信层的 initial_timeout（初始超时时间）
                       '''
                    reliable_schedule_now(ks->send_reliable);
                    session->burst = true;
                '''key_id是包头的第3位记录的'''
                if (ks->key_id != key_id)  goto error  
                struct reliable_ack send_ack;
                +'''从回复的包中读packid部分（位于ovpn头和sid之后，最多支持8个packid）
                   和紧跟其后的RemoteSessionID部分
                   '''
                bool b = reliable_ack_read(ack=&send_ack, buf, sid=&session->session_id)
                    uint8_t count;
                    buf_read(buf, &count, sizeof(count)
                if(!b)  goto error
                +'''遍历send_reliable，如果哪个包的id与send_ack中记录的某个包id一致了
                   说明该包有回应了，则将该包的 active 设置为 false
                   具体：
                   遍历send_ack中记录的packed_id[]
                   内部再遍历 reliable 可信层的 array[] (发送可信层最多支持4个包）
                   如果可信层取到的array（包）是active的，且其包id 与 packed_id[i] 一致，
                   说着发送的这个包，有相应的回复了，则将之 active 设置为假
                   '''
                reliable_send_purge(ks->send_reliable, &send_ack);
                +'''reliable_can_get检查rec_reliable中有没有空闲的，可用于接收数据的buffer'''
                if (op != P_ACK_V1 && reliable_can_get(ks->rec_reliable))   
                    '''从buf中读（包末尾--初次连接的第一个回复包）Message Package-ID'''
                    bool b=reliable_ack_read_packet_id(buf, &id)
                    if(b)
                        '''确保接收的包的id，不会死锁接收buffer
                           因为包的id是uint32表示的，它有个最大表示范围
                           这里的判断就是应对包的id马上就要到其最大表示范围的情况
                           '''
                        b = reliable_wont_break_sequentiality(ks->rec_reliable, id)
                            return reliable_pid_in_range2(test=id, base=rel->packet_id, extent=rel->size)
                                   #注：param1, param2 都是 uint32 类型
                                   if ( UINT32_MAX_VAL - base > extend )    #当base的值还没接近其表示上限时
                                        if (test < base + extent)
                                            return true;
                                   else                                     #当base的值接近其表示上限时
                                        if ((test+0x80000000u) < (base+0x80000000u) + extent)
                                            return true;
                                   return false;
                        if(b)
                            '''确定接收的包不是一个(已接收过的)历史的重放包'''
                            b = reliable_not_replay(rel=ks->rec_reliable, id)
                                '''如果 id < rel->packet_id'''
                                b=reliable_pid_min(id, rel->packet_id)
                                if(b)  return false
                                遍历 rel->array[]
                                    如果存在某个 reliable_entry 是 active 的，
                                    且其 packet_id == id;  
                                    return false
                                return true    
                            if(b)
                                '''在接收信任层中抓取一个可用的 reliable_entry'''
                                struct buffer *in = reliable_get_buf(ks->rec_reliable);
                                    遍历 rel->array[]， 如果某个 reliable_entry 的 active 为假，
                                    将该 reliable_entry 初始化(buf_init)，并返回其 buf
                                '''将buf（收到的包）拷贝给接收信任层的那个 reliable_entry'''
                                buf_copy(in, buf)
                                '''将操作类型 op 、包id（两个都是从buf中分析出来的）等存给接收信任层的那个 reliable_entry'''
                                reliable_mark_active_incoming(ret=ks->rec_reliable, buf=in, pid=id, op)
                                    遍历 rel->array[] ,找到与参数 buf 匹配的那个 reliable_entry, 记为 e
                                    e->active = true;  e->packed_id = pid;  e->opcode= opcode;
                                    e->next_try = e->timeout = 0
                            reliable_ack_acknowledge_packet_id(ack=ks->rec_ack, pid=id);
                                '''检查 pid 是否已经记录在 ack 中了
                                   ack 是 key_state 中的 reliable_ack 结构，用以记录packedid，最多支持记8个
                                   '''
                                bool b = reliable_ack_packet_id_present(ack, pid)
                                if(!b)   #没记录
                                    if(ack->len < RELIABLE_ACK_SIZE(8) )  #还没满
                                        ack->packet_id[ack->len++] = pid;
                                        return true
                                    return false                  
            if(b)
                '''检查包的控制码，如果是要求重新初始化key（要求忘记之前的状态），则重置c->c2.frame'''
                uint8_t op = *BPTR(&c->c2.buf) >> P_OPCODE_SHIFT;
                if (op == P_CONTROL_HARD_RESET_CLIENT_V2 || 
                    op == P_CONTROL_HARD_RESET_SERVER_V2 || 
                    op == P_CONTROL_HARD_RESET_CLIENT_V3)
                    c->c2.frame = c->c2.frame_initial;
                c->c2.tmp_int->last_action = now;
                '''重置ping计时'''
                if (c->options.ping_rec_timeout)
                    event_timeout_reset(&c->c2.ping_rec_interval);
        else
            opt = &c->c2.crypto_options;
        '''验证和解密传入的数据包'''
        bool decrypt_status = openvpn_decrypt(buf=&c->c2.buf, work=c->c2.buffers->decrypt_buf,
                                              opt=crypto_options, frame=&c->c2.frame, ad_start);
            if(buf->len>0 && crypto_options!=NULL)  #控制包时，crypto_options为NULL
                key_ctx *ctx = &opt->key_ctx_bi.decrypt;
                cipher_kt_t * tmp = cipher_ctx_get_cipher_kt(ctx->cipher)
                '''如果 EVP_CIPHER_nid(cipher) 为
                   NID_aes_128_gcm 或 
                   NID_aes_192_gcm 或 
                   ID_aes_256_gcm 或 
                   NID_chacha20_poly1305
                   返回真，否则返回假
                   '''
                bool b= cipher_kt_mode_aead(tmp)
                if(b)
                    '''aead加密： &<aead加密>
                       Authenticated Encryption with Associated Data (AEAD) 
                       是一种同时具备保密性，完整性和可认证性的加密形式。
                       单纯的对称加密算法，其解密步骤是无法确认密钥是否正确的。
                       也就是说，加密后的数据可以用任何密钥执行解密运算，
                       得到一组疑似原始数据，而不知道密钥是否是正确的，
                       也不知道解密出来的原始数据是否正确。
                       因此，需要在单纯的加密算法之上，
                       加上一层验证手段，来确认解密步骤是否正确。
                       AEAD则是在一个算法在内部同时实现加密和认证
                       '''
                    return openvpn_decrypt_aead(buf, work, opt, frame, ad_start);
                else
                    '''解开（验证、解密和检查重放保护）CBC、OFB或CFB模式的数据通道包。
                       将buf->len设置为0，解密错误时返回false。
                       成功时，buf被设置为指向明文，返回true。
                       '''
                    return openvpn_decrypt_v1(buf, work, opt, frame);
            else
                return true
        '''解密错误在 TCP 模式下是致命的，注册 SIGUSR1 信号'''
        if (false==decrypt_status && link_socket_connection_oriented(c->c2.link_socket))
            register_signal(c, SIGUSR1, "decryption-error"); 

&<process_incoming_link_part2>
+process_incoming_link_part2(c, lsi, orig_buf);   
    lsi = c->c2.link_socket_info
    orig_buf = c->c2.buf.data
    '''满足条件时，如果有必要，会解压该包
       如果是ping包或occ包，会做一定的处理，
       把 buf 的数据存给 c->c2.to_tun 和
       c->c2.buffers->read_link_buf->data
       '''
    if (c->c2.buf.len > 0)  
        '''解压传入的数据包'''
        if (c->c2.comp_context)
            (*c->c2.comp_context->alg.decompress)(&c->c2.buf, c->c2.buffers->decompress_buf, ...);
        '''根据配置，不满足'''
        if (c->c2.tls_multi == NULL && c->c2.buf.len > 0) 
            link_socket_set_outgoing_addr(lsi, &c->c2.from, NULL, c->c2.es);
        '重置数据包接收定时器
        '''如果是ping包，则设置buf.len=0，后面不再处理该包'''
        if (is_ping_msg(&c->c2.buf))
            c->c2.buf.len = 0; #后面不再处理该包
        '''如果收到的是个occ包'''
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
                    if (c->options.occ && c->c2.tls_multi != NULL #根据配置，不满足
                        && c->c2.options_string_remote)
                        。。。
                    event_timeout_clear(&c->c2.occ_interval);
                case OCC_MTU_REPLY:
                    c->c2.max_recv_size_remote = buf_read_u16(&c->c2.buf);
                    c->c2.max_send_size_remote = buf_read_u16(&c->c2.buf);
                    if (c->options.mtu_test  #根据配置，不满足
                        && c->c2.max_recv_size_remote > 0
                        && c->c2.max_send_size_remote > 0)
                        。。。
                    event_timeout_clear(&c->c2.occ_mtu_load_test_interval);
                case OCC_EXIT:
                    c->sig->signal_received = SIGTERM;
                    c->sig->signal_text = "remote-exit";
        '''如果 orig_buf 是指向 c->c2.buf->data 且区别于 c->c2.buffers->read_link_buf->data
           则将 c->c2.buf 存给 c->c2.buffers->read_link_buf，并让 c->c2.to_tun 指向 read_link_buf
           否则，让 c->c2.to_tun 指向 c->c2.buf
           '''
        buffer_turnover(uint8* orig_buf, buffer* dest_stub=&c->c2.to_tun, buffer* src_stub=&c->c2.buf, 
                        buffer* storage=&c->c2.buffers->read_link_buf);
            if (orig_buf == src_stub->data && src_stub->data != storage->data)
                '''src_stub 存给 src_stub'''
                buf_assign(storage, src_stub);
                *dest_stub = *storage;
            else
                *dest_stub = *src_stub;
        '''如果tuntap还没定义，设置 c->c2.to_tun.len = 0，否则会导致死锁'''
        if (!tuntap_defined(c->c1.tuntap))
            c->c2.to_tun.len = 0;
    else
        buf_reset(&c->c2.to_tun);