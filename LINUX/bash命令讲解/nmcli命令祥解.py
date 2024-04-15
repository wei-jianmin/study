参：https://www.cnblogs.com/liuhedong/p/10695969.html

nmcli : network manager command line interface
nmcli命令是redhat7或者centos7之后的命令，
nmcui 是 mncli 的可视化版
该命令可以完成网卡上所有的配置工作，并且可以写入配置文件，永久生效
nmcli实用工具是由NetworkManager包提供 ： yum install -y NetworkManager
关于NetworkManager
    NetworkManager由一个管理系统网络连接、
    并且将其状态通过D-BUS进行报告的后台服务，
    以及一个允许用户管理网络连接的客户端程序
    #D-BUS是一个提供简单的应用程序互相通讯的途径的自由软件项目，
    #它是做为freedesktoporg项目的一部分来开发的。
    NetworkManager有自己的CLI工具：nmcli。
    使用nmcli用户可以查询网络连接的状态，也可以用来管理
语法：  nmcli [OPTIONS...] OBJECTS [COMMAND] [ARGUMENTS...] 
        OBJECTS = {help | general | networking | radio | connection | device | agent | monitor} 
        OPTIONS
            -t	简洁输出，会将多余的空格删除，
            -p	人性化输出，输出很漂亮
            -n	优化输出，有两个选项tabular(不推荐)和multiline(默认)
            -c	颜色开关，控制颜色输出(默认启用)
            -f	过滤字段，all为过滤所有字段，common打印出可过滤的字段
            -g	过滤字段，适用于脚本，以:分隔
            -w	超时时间
        OBJECTS
            general 常规选项
                命令格式：nmcli general {status|hostname|permissions|logging}
                命令描述：使用此命令可以显示网络管理器状态和权限，
                          你可以获取和更改系统主机名，以及网络管理器日志记录级别和域。
                status 
                    显示网络管理器的整体状态
                hostname 
                    获取主机名或该更主机名，在没有给定参数的情况下，打印配置的主机名，
                    当指定了参数，它将被移交给NetworkManager，以设置为新的系统主机名
                permissions
                    显示当前用户对网络管理器可允许的操作权限。 
                    如启用和禁用网络、更改WI-FI和WWAN状态、修改连接等
                loggin
                    获取和更改网络管理器日志记录级别和域，
                    没有任何参数当前日志记录级别和域显示。
                    为了更改日志记录状态, 请提供级别和域参数,
                    有关可用级别和域值,参阅NetworkManager.conf
            networking 网络控制
                命令格式：nmcli networking {on|off|connectivity}
                命令描述：查询网络管理器网络状态，开启和关闭网络
                选项：
                    on: 禁用所有接口
                    off: 开启所有接口
                    connectivity: 获取网络状态，
                        可选参数checl告诉网络管理器重新检查连接性，
                        否则显示最近已知的状态。而无需重新检查。
                        可能的状态如下所示:
                            none: 主机为连接到任何网络
                            portal: 无法到达完整的互联网
                            limited: 主机已连接到网络，但无法访问互联网
                            full: 主机连接到网络，并具有完全访问
                            unknown: 无法找到连接状态    
            radio 无线限传输控制
                命令格式：nmcli radio {all|wifi|wwan}
                显示无线开关状态，或启用和禁用开关
            monitor 活动监视器
                活动监视器（ACTIVITY MONITOR）
                观察网络管理器活动。监视连接的变化状态、设备或连接配置文件。
            connection 连接管理
                命令格式：nmcli connection {show|up|down|modify|add|
                                            edit|clone|delete|monitor|
                                            reload|load|import|export}
                这是主要使用的一个功能。
                show
                    1. 列出活动的连接，或进行排序（+-为升降序）
                        # 查看所有连接状态
                        [root@www ~]# nmcli connection show
                        # 等同于nmcli connection show --order +active
                        [root@www ~]# nmcli connection show --active
                        # 以活动的连接进行排序
                        [root@www ~]# nmcli connection show --order +active
                        # 将所有连接以名称排序
                        [root@www ~]# nmcli connection show --order +name
                        # 将所有连接以类型排序(倒序)
                        [root@www ~]# nmcli connection show --order -type
                    2. 查看指定连接的详细信息
                        [root@www ~]# nmcli connection show eth0
                up
                    激活连接，提供连接名称或uuid进行激活，
                    若未提供，则可以使用ifname指定设备名进行激活
                    # 以连接名进行激活
                    [root@www ~]# nmcli connection up eth0
                    # 以uuid进行激活
                    [root@www ~]# nmcli connection up 5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03
                    # 以设备接口名进行激活
                    [root@www ~]# nmcli connection up ifname eth0
                down
                    停用连接，提供连接名或uuid进行停用，
                    若未提供，则可以使用ifname指定设备名进行激活
                    # 以连接名进行激活
                    [root@www ~]# nmcli connection down eth0
                    # 以uuid进行激活
                    [root@www ~]# nmcli connection down 5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03
                    # 以设备接口名进行激活
                    [root@www ~]# nmcli connection down ifname eth0
                modify
                    这些属性可以用nmcli connection show eth0进行获取，
                    然后可以修改、添加或删除属性，若要设置属性，只需指定属性名称后跟值，
                    空值将删除属性值，同一属性添加多个值使用+。同一属性删除指定值用-加索引
                    添加多个ip:
                        # 添加三个
                        [root@www ~]# nmcli connection modify eth0 +ipv4.addresses 192.168.100.102/24
                        [root@www ~]# nmcli connection modify eth0 +ipv4.addresses 192.168.100.103/24
                        [root@www ~]# nmcli connection modify eth0 +ipv4.addresses 192.168.100.104/24
                        # 查看
                        [root@www ~]# nmcli -f IP4 connection show eth0
                        IP4.ADDRESS[1]:                         192.168.100.101/24
                        IP4.GATEWAY:                            192.168.100.100
                        IP4.DNS[1]:                             8.8.8.8
                        # 启用配置
                        [root@www ~]# nmcli connection up eth0
                        Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/18)
                        # 再次查看
                        [root@www ~]# nmcli -f IP4 connection show eth0
                        IP4.ADDRESS[1]:                         192.168.100.101/24
                        IP4.ADDRESS[2]:                         192.168.100.102/24
                        IP4.ADDRESS[3]:                         192.168.100.103/24
                        IP4.ADDRESS[4]:                         192.168.100.104/24
                        IP4.GATEWAY:                            192.168.100.100
                        IP4.DNS[1]:                             8.8.8.8
                    删除指定ip
                        [root@www ~]# nmcli -f IP4 connection show eth0
                        IP4.ADDRESS[1]:                         192.168.100.101/24
                        IP4.ADDRESS[2]:                         192.168.100.102/24
                        IP4.ADDRESS[3]:                         192.168.100.103/24
                        IP4.ADDRESS[4]:                         192.168.100.104/24
                        IP4.GATEWAY:                            192.168.100.100
                        IP4.DNS[1]:                             8.8.8.8
                        # 删除索当前索引为2的地址
                        [root@www ~]# nmcli connection modify eth0 -ipv4.addresses 2
                        # 查看
                        [root@www ~]# nmcli -f IP4 connection show eth0
                        IP4.ADDRESS[1]:                         192.168.100.101/24
                        IP4.ADDRESS[2]:                         192.168.100.102/24
                        IP4.ADDRESS[3]:                         192.168.100.103/24
                        IP4.ADDRESS[4]:                         192.168.100.104/24
                        IP4.GATEWAY:                            192.168.100.100
                        IP4.DNS[1]:                             8.8.8.8
                        # 再次激活
                        [root@www ~]# nmcli connection up eth0
                        Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/19)
                        # 查看
                        [root@www ~]# nmcli -f IP4 connection show eth0
                        IP4.ADDRESS[1]:                         192.168.100.101/24
                        IP4.ADDRESS[2]:                         192.168.100.102/24
                        IP4.GATEWAY:                            192.168.100.100
                        IP4.DNS[1]:                             8.8.8.8
                add
                    这是创建一个新的连接，需要指定新创建连接的属性，语法与modify相同
                    [root@www ~]# nmcli con add con-name eth1 type ethernet  autoconnect yes ifname eth0
                    # con-name     连接名称
                    # type              连接类型
                    # autoconnect 是否自动连接
                    # ifname          连接到的设备名称
                    更多的类型或方法可以使用nmcli connection add help查看
                clone
                    克隆连接，克隆一个存在的连接，除了连接名称和uuid是新生成的，其他都是一样的
                    [root@www ~]# nmcli connection clone eth0 eth0_1
                delete
                    删除连接，这将删除一个连接
                    [root@www ~]# nmcli connection delete eth0_1
                load
                    从磁盘加载/重新加载一个或多个连接文件，
                    例如你手动创建了一个/etc/sysconfig/network-scripts/ifcfg-ethx连接文件，
                    你可以将其加载到网络管理器，以便管理
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
                    监视连接配置文件活动。每当指定的连接更改时, 此命令都会打印一行。
                    要监视的连接由其名称、UUID 或 D 总线路径标识。
                    如果 ID 不明确, 则可以使用关键字 id、uuid 或路径。
                    有关 ID 指定关键字的说明, 请参阅上面的连接显示。
                    监视所有连接配置文件, 以防指定无。
                    当所有监视的连接消失时, 该命令将终止。
                    如果要监视连接创建, 请考虑使用带有 nmcli 监视器命令的全局监视器
                    [root@www ~]# nmcli connection monitor eth0
            device 设备管理
                命令格式：nmcli device {status|show|set|connect|
                                        reapply|modify|disconnect|
                                        delete|monitor|wifi|lldp}
                显示和管理设备接口。
                该选项有很多功能，例如连接wifi，创建热点，扫描无线，邻近发现等，
                下面仅列出常用选项。详细功能可使用nmcli device help查看。
                status
                    打印设备状态，如果没有将命令指定给nmcli device，则这是默认操作
                    [root@www ~]# nmcli device status
                    DEVICE  TYPE      STATE      CONNECTION 
                    eth0    ethernet  connected  eth0       
                    lo      loopback  unmanaged  --         
                    [root@www ~]# nmcli device
                    DEVICE  TYPE      STATE      CONNECTION 
                    eth0    ethernet  connected  eth0       
                    lo      loopback  unmanaged  --
                show
                    显示所有设备接口的详细信息
                    # 不指定设备接口名称，则显示所有接口的信息
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
                    设置设备属性
                    [root@www ~]# nmcli device set ifname eth0 autoconnect yes
                connect
                    连接设备。提供一个设备接口，网络管理器将尝试找到一个合适的连接, 将被激活。
                    它还将考虑未设置为自动连接的连接。(默认超时为90s)
                    [root@www ~]# nmcli dev connect eth0
                    Device 'eth0' successfully activated with '5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03'.
                reapply
                    使用上次应用后对当前活动连接所做的更改来更新设备。
                    [root@www ~]# nmcli device reapply eth0
                    Connection successfully reapplied to device 'eth0'.
                modify
                    修改设备上处于活动的设备，但该修改只是临时的，并不会写入文件。
                    （语法与 nmcli connection modify 相同）
                    [root@www ~]# nmcli device modify eth0 +ipv4.addresses 192.168.100.103/24
                    Connection successfully reapplied to device 'eth0'.
                    [root@www ~]# nmcli dev show eth0
                    [root@www ~]# nmcli device modify eth0 -ipv4.addresses 1
                    Connection successfully reapplied to device 'eth0'.
                disconnect
                    断开当前连接的设备，防止自动连接。但注意，断开意味着设备停止！但可用 connect 进行连接
                    [root@www ~]# nmcli device disconnect eth0
                delete
                    删除设备，该命令从系统中删除接口。
                    请注意, 这仅适用于诸如bonds, bridges, teams等软件设备。
                    命令无法删除硬件设备 (如以太网)。超时时间为10秒
                    [root@www ~]# nmcli device delete bonds
                monitor
                    监视设备活动。每当指定的设备更改状态时, 此命令都会打印一行。
                    监视所有设备以防未指定接口。当所有指定的设备消失时, 监视器将终止。
                    如果要监视设备添加, 请考虑使用带有 nmcli 监视器命令的全局监视器。
                    [root@www ~]# nmcli device monitor eth0
        nmcli 返回状态码
            mcli 如果成功退出状态值为0，如果发生错误则返回大于0的值
            0: 成功-指示操作已成功
            1: 位置或指定的错误
            2: 无效的用户输入，错误的nmcli调用
            3: 超时了（请参阅 --wait 选项）
            4: 连接激活失败
            5: 连接停用失败
            6: 断开设备失败
            7: 连接删除失败
            8: 网络管理器没有运行
            10: 连接、设备或接入点不存在
            65: 当使用 --complete-args 选项，文件名应遵循。
            
参：https://blog.csdn.net/qq_40907977/article/details/88380855            
mcli命令给我们带来了太多的方便，关于nmcli的总结如下
    通过敲命令更改IP地址、DNS、网关等信息，最终影响的都是/etc/sysconfig/network-scripts/ifcfg-ens32配置文件
    关于【nmcli connection reload】命令，只要更改过关于网络的配置文件，都需要做重载操作才能激活网卡。
    激活网卡的命令有三个【nmcli connection up ens32】、【nmcli device reapplyens32】、【nmcli device connect ens32】，
    三个命令作用一样，看个人喜好即可。
    关于DNS,在ifcfg.ens32中配置，但是生效的地方在/etc/resolve.conf，如果删除该文件中的DNS信息，则网络连接会失败。
