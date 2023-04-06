--config file
    如果只有配置文件选项，没有其它选项，则可以省略前面的--config
    双引号字符（“”）可用于将包含空格的单个参数括起来
    第一行如果是'#'或';'，则可表注释
    openvpn2.0之后，反斜杠有特殊意义，所以：
    用\\表示一个普通的反斜杠，
    用\"表示使用普通的引号，
    用\[space]表示一个普通的空格（而不是参数分隔符）
    
------------------隧道相关的参数-------------------
--mode m
    设置vpn的模式，默认'p2p'
    2.0之后的版本增加支持'server'，用以实现支持多客户端的服务器
--local host
    本地域名或ip，如果指定了，openvpn将会只绑定该地址，否则绑定所有网卡
--remote host [port]
    远端域名或ip。在客户端可使用多个 --remote 选项指定冗余，
    每个代表一个不同的vpn服务器，当连接失败是，就尝试下一个
    注意，由于udp是非面向连接的，所以用--ping和--ping-restart选项定义连接失败
    注意下面这种情况：如果指定了多个--remote，且用--user或/和--group选项
    控制放弃管理员权限，而你的客户端程序又不是运行在Windows系统上，
    则如果客户端需要切换到另一个不同的vpn服务器上，那个服务器又发来了
    不同的tun/tap或路由配置，则客户端则可能因缺少权限到导致错误退出
    如果没指定--remote，则vpn将监听所有ip地址的包，
    但除非通过所有身份验证测试，否则不会对这些数据包采取行动
    这种身份验证要求对所有潜在的对等方都有约束力，
    即使是来自已知和假定可信IP地址的对等方（在UDP数据包上伪造源IP地址非常容易）
    在tcp模式下，--remote将作为一个过滤器，拒绝所有与host不匹配域名的连接
    如果域名是个用于解析多个ip地址的DNS名字，
    则将随机选择一个，从而提供一种基本的负载平衡和故障切换功能。
--remote-random    
    当有多个--remote选项时，将列表的顺序随机化（否则默认按顺序），以实现简单的负载均衡
--proto p    
    使用协议p与远端host通信，p可以是udp/tcp-client/tcp-server，默认udp
    如果是tcp，则一端指定tcp-server，另一端指定tcp-client
    tcp-server将会无限期的等待，而tcp-client将尝试连接，
    如果失败，则5秒后（可通过--connect-retry选项控制）继续尝试
    tcp客户端和服务端的任何一方重置了连接，则另一个发出SIGUSR1信号
    OpenVPN旨在通过UDP优化运行，在无法使用UDP时，可改用TCP
    比起upd，tcp在拥挤的或不可信的网络上不够高效和健壮
    然后在特定情形下，tcp有其优势，像如隧道传输非IP或应用程序级UDP协议，
    或者不具有内置可靠性层的隧道传输协议。
--connect-retry n    
    连接失败后，等待多少秒后重试，默认5秒
--http-proxy server port [authfile] [auth-method]
--http-proxy-retry
--http-proxy-timeout n
--http-proxy-option type [parm]
--socks-proxy server [port]
--socks-proxy-retry
--resolv-retry n
    如果n秒内解析--remote的域名还不成功，则认定失败
    可以设置n为"infinite"(默认)，使之一直尝试
--float
    允许对端变动其ip和/或端口，像如因为DHCP（如果没有--remote选项，则默认使用该功能）
    如果--float和--remote搭配使用，则允许一个vpn会话在开始时连到到一个已知的地址，
    而如果从新地址上来的包通过了所有的认证，则新的地址将接管该会话
    如果对端拥有一个动态地址（像如拨号连接或DHCP客户端），则将是有用的
    本质上，--float 告诉vpn允许接收任何地址上发来的通过认证的包，
    而不只是从--remote来的包
--ipchange cmd
    当远端ip地址在初次认证后或改变后，执行shell命令cmd
    执行方式为：cmd ip_address port_number
    不要在--mode server时使用该命令（使用--client-connect替代）
    注意cmd可以使多有多个参数的shell命令，所有vpn生成的参数将被传送给cmd
    例如你运行在一个动态ip地址的环境，你可以使用该脚传来的对端的地址本来编辑/etc/host文件
    类似的，如果我们的ip因为dhcp而改变了，我们应配置我们的ip变动脚本（参dhcpcd(8)的man帮助）
    来发送一个 SIGHUP or SIGUSR1 信号给vpn。
    然后OpenVPN将在其新的IP地址上与最近经过身份验证的对等方重新建立连接
--port port
    客户端/服务端端口号，2.0版本后默认1194（之前版本默认5000）
--lport port
    本地端口号
--rport port
    远端端口号
--nobind
    不要绑定到本地地址和端口
    ip堆栈将使用一个动态端口用以接收包
    由于动态端口的值不能被对等端口提前知道，
    因此此选项只适用于将使用 --remote 选项启动连接的对等端口。
--dev tunX | tapX | null
    两端应该一致，不能混用
    tun封装ip，tap封装ethernet 802.3
--dev-type device-type
    应该是tun或tap。
    该选项只在--dev选项指定的tun/tap设备不是以tun或tap开头时使用
--tun-ipv6
--dev-node node
--ifconfig l rn
    显式设置设备节点，而不是使用/dev/net/tun、/dev/tun、/dev/tap等。
    如果OpenVPN无法根据名称确定节点是tun还是tap设备，
    则还应指定-dev type tun或-dev type tap。
    在Windows系统上，选择tap-Win32适配器，
    该适配器在“网络连接控制面板”中命名为node，
    或用大括号括起来的适配器的原始GUID。
    Windows下的--show adapters选项也可用于枚举所有可用的TAP-Win32适配器，
    并将显示网络连接控制面板名称和每个TAP-Win33适配器的GUID。
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

------------------服务端相关的参数-------------------










