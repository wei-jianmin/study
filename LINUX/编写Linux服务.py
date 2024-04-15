<catalog s0/s4/s8 catalog_line_prefix=+>
+Linux注册服务的两种方式
    一种是init.d的形式，一种systemd的形式
    1. /etc/init.d，对应的服务管理命令为 ： service 服务名 start
    2. systemd 对应的服务管理命令为 : systemctl start 服务名
       脚本位于/etc/systemd/system，下面对应的大都为一些.services文件
       
    对于第1中方式，Linux在chkconfig时，会使用一个perl脚本(/sbin/insserv)来检查脚本格式是否规范

    红帽6的启动过程为 ： 开机自检BIOS -> MBR引导 -> GRUB菜单 -> 加载内核 -> init进程初始化
    红帽7的启动过程为 ： 开机自检BIOS -> MBR引导 -> GRUB2菜单 -> 加载内核 -> systemd进程初始化

    +systemd是对传统sysvinit的改进
        systemd 被设计用来改进 sysvinit 的缺点，它和ubuntu的upstart是竞争对手，预计会取代它们
        systemd的目标是：尽可能启动更少进程；尽可能将更多进程并行启动。
        systemd尽可能减少对shell脚本的依赖。
        传统sysvinit使用inittab来决定运行哪些shell脚本，大量使用shell脚本被认为是效率低下无法并行的原因

    +init和Systemd的区别
        init： 
            一是启动时间长，init是串行启动，只有前一个进程启动完，才会启动下一个进程
            二是启动脚本复杂，Init进程只是执行启动脚本，不管其他事情，脚本需要自己处理各种情况，这往往使得脚本变得很长
            由Linux内核加载运行，位于 /sbin/init   ,是系统中第一个进程，PID永远为1
        systemd：
            按需启动服务，减少系统资源消耗。
            尽可能并行启动进程，减少系统启动等待时间
            由Linx内核加载运行，位于 /usr/lib/systemd/systemd  ，是系统中第一个进程，PID永远为1
            测试Ubuntu16/Ubuntu20/UOS，发现第一启动进程都是/sbin/init，但也能搜索到systemd进程
            测试centos，测试发现第一启动进程是systemd
    
    +systemd 为什么会有那么大的争议
        https://www.zhihu.com/question/25873473
            代码质量不高, 频繁变更设计和接口。systemd的新功能，最好都等几个版本再用
            不考虑向后兼容
            。。。
        
    +Rhel6 vs Rhel7 管理服务
        Rhel6 用 service 和 chkconfig 来管理服务，它是 SystemV 架构下的一个工具。
        Rhel7 是用 systemctl  来管理服务，它融合了之前的 service 和 chkconfig 的功能于一体（Ubuntu16下也有该工具）
        动作                  Rhel6 旧指令                          Rhel7新指令
        启动某服务            service  httpd   start                systemctl  start   httpd
        停止某服务            service  httpd   stop                 systemctl  stop   httpd
        使服务开机自启动      chkconfig  --level   5  httpd   on    systemctl  enable  httpd
        使服务开机不自启动    chkconfig  --level   5  httpd   off   systemctl  disable  httpd
        重启某服务            service  httpd   restart              systemctl  restart  httpd
        检查服务状态          service  httpd  status                systemctl  status  httpd
        显示所有已启动的服务  chkconfig  --list                     systemctl  list-unit-files | grep enabled
        加入自定义服务        chkconfig  --add  test                systemctl  load  test
        删除某服务            chkconfig  --del  httpd               停掉应用，删除其配置文件
        查询服务是否开机自启  chkconfig  --list | grep httpd        systemctl  is-enabled   httpd
        查看启动失败的服务    无                                    systemctl  --failed

        如果我们想让该程序开机启动，我们可以执行命令 systemctl enable 服务名
        这个命令相当于在 /etc/systemd/system/multi-user.target.wants 目录添加一个软链接，
        指向 /usr/lib/systemd/system 目录下的 httpd.service 文件。
        这是因为开机时，Systemd只执行 /etc/systemd/system/multi-user.target.wants 目录里面的配置文件

        systemd的一些常用命令：
        列出所有可用单元 ：  systemctl list-unit-files
        列出所有运行的单元： systemctl list-unit-files | grep enabled 
        列出所有可用服务：   systemctl list-unit-files  --type=service
        列出所有运行的服务： systemctl list-unit-files  --type=service | grep enabled 
        屏蔽httpd服务：      systemctl mask httpd

======================================================================  

+旧的服务方式

    +服务是如何自启动的：
        参：https://www.jianshu.com/p/5af068656d4b

        1. 服务脚本都是放在 /etc/init.d 目录下的

        2. 这些脚本是如何被自动执行的？
           在 /etc下，有 rc0~6.d、rcS.d目录
           在这些目录下有超链接，指向 /etc/init 下的脚本文件
           脚本文件的命名方式： "K/S 2位的数字 自定义名字"
           K : kill , 自动调用指向的脚本，并携带 stop 参数
           S ：start ，自动调用指向的脚本，并携带 start 参数
           自动执行时，先按名字顺序，执行所有的 K 开头的脚本
           再按名字顺序，执行所有的 S 开头的脚本
           
        3. rc0~6.d、rcS.d目录的区别
           /etc/rcS.d/ #开机后需要自动启动的一些基本服务
           /etc/rc0.d/ #运行模式0下需要启动的服务
           /etc/rc1.d/ #运行模式1下需要启动的服务
           /etc/rc2.d/ #运行模式2下需要启动的服务
           /etc/rc3.d/ #运行模式3下需要启动的服务
           /etc/rc4.d/ #运行模式4下需要启动的服务
           /etc/rc5.d/ #运行模式5下需要启动的服务
           /etc/rc6.d/ #运行模式6下需要启动的服务

        4. /etc/rc.local  
           这是个脚本文件，在系统初始化级别的脚本运行之后再执行
   
    ======================================================================  

    +/etc/init 目录下的脚本格式样例：

       #! /bin/bash
       ### BEGIN INIT INFO
       #
       # Provides:	 location_server
       # Required-Start:	$local_fs  $remote_fs
       # Required-Stop:	$local_fs  $remote_fs
       # Default-Start: 	2 3 4 5
       # Default-Stop: 	0 1 6
       # Short-Description:	initscript
       # Description: 	This file should be used to construct scripts to be placed in /etc/init.d.
       #
       ### END INIT INFO
     
       case "$1" in
          start)
            ;;
          restart)
            ;;
          stop)
            ;;
          status)
            ;;
          reload)
            ;;
          force-reload)
            ;;
          *)
            ;;
       esac        
       
       注： 
          ### BEGIN INIT INFO 段必须存在，否则会在注册服务时报错
          注册服务时，会参照这部分的信息，创建相关文件
          Required-Start 指明在服务被启动前，哪些服务应该被提前准备好
          系统启动时，根据这些依赖，组织各服务的启动顺序
          $local_fs表明本地文件系统应该被准备好
          Required-Stop则指明应该在哪些服务(停止)之前停止
          Default-Start、Default-Stop则影响在/etc/rc0~6.d哪些目录下创建什么链接

    ======================================================================

    +LSB初始化脚本
        上面的 ### BEGIN INIT INFO 段，就是LSB初始化脚本
        Debian 在 2015 年停止了对 LSB 的支持
        符合 LSB 标准的初始化脚本需要：
            至少提供以下操作：启动、停止、重新启动、强制重新加载和状态
            返回正确的退出状态代码。
            文档运行时依赖项
            [可选]使用 Init.d 函数记录消息：log_success_msg、log_failure_msg和log_warning_msg
        支持的关键字
            Provides
                指定该服务的名称，其它服务脚本如果依赖本服务，则以此名称为依据
            Required-Start
                指明需要在此服务之前，准备好的服务
            Required-Stop
                指明需要在此服务关掉之前，先关掉的服务，一般与Required-Start部分指定的服务一致
            Should-Start
                如果这些服务存在，则应在本服务脚本之前开启，但这些服务不存在，也不影响当前服务的开启
            Should-Stop
                同上，如果这些服务存在，则应该先于本服务关闭
            Default-Start
                影响在 /etc/rc0~6.d 哪些目录下创建 S 开头的链接
            Default-Stop
                影响在 /etc/rc0~6.d 哪些目录下创建 K 开头的链接
            Short-Description
                对脚本的简单描述，只能占一行
            Description
                对脚本行为的详细描述，可占多行，每个续行应该以 # 开头,且 # 后面跟两个空格或一个tab
            X-Interactive: true
                表明该初始化脚本可以与用户交互（如需要用户输入），这确保了脚本有使用tty的能力
        一些基本服务的名字
            $local_fs 所有挂载的本地文件系统
            $network  基础网络服务
            $named 域名转换，如DNS、NIS+或LDAP
            $portmap ?SunRPC/ONCRPC端口映射服务
            $remote_fs  所有挂载的远程文件系统
            $syslog  系统日志
            $time 系统时间必须设置好
            $all  先启动那些在Required-Start部分没有指定$all的服务

    ====================================================================== 

    +将脚本注册成服务
        RedHat系的操作系统自带 chkconfig 工具，可以将上面的脚本注册成服务
            使用方法参：https://www.runoob.com/linux/linux-comm-chkconfig.html
                这是Red Hat公司遵循GPL规则所开发的程序，
                它可查询操作系统在每一个执行等级中会执行哪些系统服务，其中包括各类常驻服务。
                chkconfig [--add][--del][--list][系统服务] 或 
                chkconfig [--level <等级代号>][系统服务][on/off/reset]
                --add     增加所指定的系统服务，让 chkconfig 指令得以管理它，并同时在系统启动的叙述文件内增加相关数据。
                --del     删除所指定的系统服务，不再由 chkconfig 指令管理，并同时在系统启动的叙述文件内删除相关数据。
                --level<等级代号>     指定读系统服务要在哪一个执行等级中开启或关毕。
            使用方法参：https://www.cnblogs.com/tianyiwuying/p/7519632.html
        Debian系的操作系统与之对应的是 update-rc.d
            参：https://blog.csdn.net/weixin_34041003/article/details/93055408
            添加删除服务
                添加： sudo update-rc.d 服务名 defaults
                删除： sudo update-rc.d -f 服务名 remove
            注册服务后，会在如下位置自动创建相关文件：
                /etc/init.d/ (原有)
                /etc/rc0~6.d/ (是指向/etc/init.d下相应文件的链接)
                /run/systemd/generator.late/graphical.target.wants/
                /run/systemd/generator.late/multi-user.target.wants/
                /run/systemd/generator.late/
                上面三个generator.late目录下创建的.service文件内容一样
                。service文件也是调用/etc/init.d下的相应脚本，并传入start/stop参数
        Debian下也可以装chkconfig工具
            参：https://blog.csdn.net/wildwolf_001/article/details/115250102
        
    ======================================================================

    +调用/停用服务   
        历史版本中的linux对服务的操作是通过service来完成的。
        若创建用户自定义的服务，则需要较为复杂的操作。
        目前linux新的发行版已经内置了systemctl来操作服务
        man service 可以发现，其实就是去 /ect/init.d 下找相应脚本进行调用
        经测试，服务需注册后，才能通过service调用
        
======================================================================

+新的服务方式

    +service脚本编写格式（/lib/systemd/system）
        参：https://www.jianshu.com/p/92208194d700
        参：https://www.cnblogs.com/mafeng/p/10316351.html
        参：https://www.cnblogs.com/virgosnail/p/12675880.html
        参：https://blog.csdn.net/weixin_57400332/article/details/123627742

        脚本分为3个部分：[Unit] [Service] [Install]
        Unit  此区块信息用于描述当前服务的简单描述
            Description：服务描述信息；
            Documentation：文档相关信息；
            下面四个选项只涉及启动顺序，不涉及依赖关系；
            After：定义sshd服务应该在哪些服务之后启动；
            Before：定义sshd服务应该在哪些服务之前启动；
            Requires：表示强依赖关系，如果sshd服务启动失败或异常退出，则Requires配置的服务也必须退出；
            Wants：表示若依赖关系，如果sshd服务启动失败或异常退出，不影响Wants配置的服务；
        Service   此区块定义如何启动当前服务
            Service是脚本的关键部分
            Type=forking : 后台运行模式
            PIDFile=/xxx/xxx.xxx : 存放PID文件的位置
            ExecStart=/bin/echo xxx : 这是服务运行的具体执行命令
            ExecReload=/bin/echo xxx ： 这是服务重启的执行命令
            EexcStop=/bin/echo xxx : 这是服务停止的执行命令
            一些节点的介绍：
                Type：
                    在Service段中，启动方式使用Type指定。具体可以参考man systemd.service。
                    Type有如下几种可选项：simple、forking、oneshot、dbus、notify、idel
                    simple
                        这是默认的Type，当Type和BusName配置都没有设置，指定了ExecStart设置后，simple就是默认的Type设置。
                        simple使用ExecStart创建的进程作为服务的主进程。在此设置下systemd会立即启动服务，
                        如果该服务要启动其他服务（simple不会forking），
                        它们的通讯渠道应当在守护进程启动之前被安装好（e.g. sockets,通过sockets激活）。
                    forking
                        如果使用了这个Type，则ExecStart的脚本启动后会调用fork()函数创建一个进程作为其启动的一部分。
                        当一切初始化完毕后，父进程会退出。子进程会继续作为主进程执行。
                        这是传统UNIX主进程的行为。如果这个设置被指定，
                        建议同时设置PIDFile选项来指定pid文件的路径，以便systemd能够识别主进程。
                    oneshot
                        onesh的行为十分类似simple，但是，在systemd启动之前，进程就会退出。
                        这是一次性的行为。可能还需要设置RemainAfterExit=yes，以便systemd认为j进程退出后仍然处于激活状态。
                    dbus
                        这个设置也和simple很相似，该配置期待或设置一个name值，通过设置BusName=设置name即可。
                    notify
                        同样地，与simple相似的配置。顾名思义，该设置会在守护进程启动的时候发送推送消息(通过sd_notify(3))给systemd
                Type：
                    Type=simple  说明：
                        在有些情况下 systemctl start *** 这条命令即使执行成功，服务也没有运行，原因在于此条配置，
                        simple为默认值（必须写，不写默认值为oneshot），在你指定ExecStart=所配置的进程视为主进程，
                        因为服务管理器将在创建主服务进程之后和执行服务的二进制文件之前立即启动后续单元。
                        请注意，这意味着即使无法成功调用服务的二进制文件(例如，因为选定的User=不存在，或者服务二进制文件丢失)，
                        简单服务的systemctl start命令行也将报告成功。
                    Type=exec   说明：
                        exec类型类似于simple，但是服务管理器会考虑在主服务二进制文件执行后立即启动该单元。
                        这意味着如果二进制文件丢失或者选定的User=不存在，systemctl start 将报错
                    Type=forking  说明：
                        如果设置为forking，则会将execut=所配置的进程将调用fork（）作为其启动的一部分，
                        这意味着启动完成后父进程退出，子进程作为主服务进程运行，当父进程退出时，服务管理器默认该单元已经启动，
                        通常搭配PIDFlie=选项，以便systemd能够可靠的识别服务的主要进程
                    Type=oneshot  说明
                        如果没有指定Type=或ExecStart=的话，Type=oneshot是默认的。
                        请注意，如果使用此选项而没有RemainAfterExit=服务将永远不会进入“活动”单元状态，
                        而是直接从“激活”转换到“停用”或“死亡”，因为没有配置应连续运行的进程。
                    Type=notify  说明：
                        notify的行为类似于exec但是，当服务完成启动时，预计会通过sd_notify(3)或等效的调用发送通知消息。
                        发送此通知消息后，systemd将继续启动后续装置。
                        如果使用此选项，NotifyAccess=(见下文)应设置为打开对systemd提供的通知套接字的访问。
                        如果NotifyAccess=缺失或设置为none，它将被强制设置为main。
                    Type参数选择官方建议：
                        通常建议尽可能对长时间运行的服务使用Type=simple，因为这是最简单、最快的选项。
                        但是，由于这种服务类型不会传播服务启动失败，
                        并且不允许在服务初始化完成后对其他单元进行排序
                        (例如，如果客户端需要通过某种形式的IPC连接到服务，并且IPC通道仅由服务本身建立，
                        而不是通过套接字或总线激活或类似方式提前建立)，
                        这在许多情况下可能是不够的。
                        如果是这样，notify或dbus(后者仅在服务提供D-Bus接口的情况下)是首选选项，
                        因为它们允许服务程序代码精确地安排何时考虑服务成功启动以及何时继续后续单元。
                        notify服务类型需要服务代码库中的显式支持(因为sd_notify()或等效的API需要由服务在适当的时间调用)——如果不支持，
                        那么分叉是一种替代方法:它支持传统的UNIX服务启动协议。
                        最后，对于足以确保服务二进制文件被调用的情况，以及服务二进制文件本身不执行或很少执行初始化
                        (并且其初始化不太可能失败)的情况，exec可能是一个选项。
                        请注意，使用简单以外的任何类型都可能会延迟启动过程，因为服务管理器需要等待服务初始化完成。
                        因此，建议不要不必要地使用简单类型以外的任何类型。
                        (还要注意，对于长时间运行的服务，通常不建议使用idle或oneshot。)
                ExitType=
                    ExitType=main  说明：
                        如果设置为main(默认值)，服务管理器将认为该单元在主进程(根据类型=)退出时已停止。因此，它不能与Type=oneshot一起使用。
                    ExitType=cgroup  说明：
                        如果设置为cgroup，只要cgroup中至少有一个进程没有退出，该服务将被视为正在运行。
                    官方使用建议：
                        当服务具有已知的分叉模型并且可以可靠地确定主进程时，通常建议使用ExitType=main。
                        ExitType= cgroup是指分叉模型事先未知且可能没有特定主进程的应用程序。
                        它非常适合临时或自动生成的服务，例如桌面环境中的图形应用程序。
                RemainAfterExit=
                    RemainAfterExit=yes/no  说明：
                        接受一个布尔值，该值指定服务是否应被视为活动的，即使它的所有进程都已退出。默认为no。
                    GuessMainPID=
                        接受一个布尔值，该值指定如果不能可靠地确定服务的主PID，systemd是否应该尝试猜测它。
                        除非设置了类型=分叉并且未设置PIDFile=否则忽略此选项，因为对于其他类型或显式配置的PIDFile，主PID file总是已知的。
                        如果一个守护进程包含多个进程，猜测算法可能会得出不正确的结论。
                        如果无法确定主PID，服务的故障检测和自动重启将无法可靠工作。默认为是。
                    PIDFile=
                        后面通常跟一个文件路径，如果不指定绝对路径，则默认相对路径为/run/，通常与Type=forking一起使用；
                        服务管理器不会写入此处配置的文件，但如果文件仍然存在，它会在服务关闭后删除该文件。
                    官方建议：
                        请注意，在现代项目中应该避免PID文件。在可能的情况下，使用Type=notify或Type=simple，
                        这不需要使用PID文件来确定服务的主要进程，并避免不必要的分叉。
                ExecStart=
                    启动此服务时执行的带有参数的命令。根据下面描述的规则，该值被分成零个或多个命令行(参见下面的“命令行”部分)。
                     除非Type=是oneshot，否则只能给出一个命令。当使用Type=oneshot时，可以指定零个或多个命令。
                     可以通过在同一个指令中提供多个命令行来指定命令，或者，可以多次指定该指令以获得相同的效果。
                     如果将空字符串分配给此选项，将重置要启动的命令列表，以前分配的此选项将无效。
                     如果没有指定ExecStart=则服务必须有RemainAfterExit = yes和至少一个ExecStop= line集。
                     (同时缺少ExecStart=和ExecStop=的服务无效。) 
                     对于每个指定的命令，第一个参数必须是可执行文件的绝对路径或不带任何斜杠的简单文件名。
                     可选地，该文件名可以以许多特殊字符作为前缀:
                ExecStartPre=, ExecStartPost=
                    分别在ExecStart=中的命令之前或之后执行的附加命令。
                    语法与ExecStart=相同，只是允许多个命令行，并且命令是一个接一个地串行执行的
                    如果这些命令中的任何一个(不以“-”为前缀)失败，其余的命令将不会执行，该单元将被视为失败。
                    ExecStart=命令仅在所有没有前缀“-”的ExecStartPre=命令成功退出后运行。
                     ExecStartPost =只有在成功调用了ExecStart=中指定的命令后，才运行命令，
                     这由Type=(即，对于Type=simple或Type=idle，进程已经启动，对于Type=oneshot，
                     最后一个ExecStart=进程成功退出，对于Type=forking，初始进程成功退出，
                     “READY=1”被发送给Type=notify，或者对于Type=dbus，BusName=已被采用)。 
                     请注意，ExecStartPre=可能不用于启动长时间运行的进程。
                     所有由通过ExecStartPre=调用的进程分叉的进程将在下一个服务进程运行之前被终止。 
                     请注意，如果在服务完全启动之前，在ExecStartPre =、ExecStart=、或ExecStartPost =中指定的
                     任何命令失败(并且没有以“-”作为前缀，请参见上文)或超时，
                     则继续执行在ExecStopPost =中指定的命令，跳过在ExecStop=中指定的命令。 
                     请注意，ExecStartPost =的执行是为了考虑Before=/After=排序约束。
                ExecReload=
                    ExecReload=kill -HUP $MAINPID
                        重加载使用，最好为一条命令
                ExecStop=
                    可选参数，不写也行；
                    请注意，ExecStop=中指定的命令仅在服务首次成功启动时执行。
                    如果服务从未启动过，或者启动失败，
                    例如，因为ExecStart=、ExecStartPre =或ExecStartPost =中指定的任何命令失败(并且没有前缀“-”，见上文)或超时，
                    则不会调用它们。当服务无法正确启动并再次关闭时，使用ExecStopPost =调用命令。
                    还要注意，如果服务成功启动，即使服务中的进程自行终止或被终止，停止操作也始终会执行。
                    停止命令必须准备好处理这种情况。如果systemd知道在调用停止命令时主进程已经退出，
                    那么$MAINPID将被取消设置。 服务重启请求被实现为停止操作，然后是启动操作。
                    这意味着在服务重新启动操作过程中会执行ExecStop=和ExecStopPost =命令。 
                    建议将此设置用于与请求干净终止的服务通信的命令。对于事后清理步骤，请使用ExecStopPost =来代替。
                RestartSec=
                    配置重新启动服务之前的睡眠时间(如重新启动=所配置的)。
                    采用以秒为单位的无单位值，或时间跨度值，如“5min 20s”。默认为100ms。
                TimeoutStartSec=
                    配置等待启动的时间。如果守护程序服务没有在配置的时间内发出启动完成的信号，该服务将被视为失败，并将再次关闭。
                RuntimeMaxSec=
                    配置服务运行的最长时间。如果使用了这种方法，并且服务已激活超过指定时间，它将被终止并进入故障状态。
                    请注意，此设置对Type=oneshot服务没有任何影响，因为它们会在激活完成后立即终止。
                Restart=
                    配置当服务进程退出、终止或达到超时时是否应重新启动服务。
                    如果设置为on-success，则只有在服务进程干净退出时才会重新启动。
                    选项列表：参file://编写Linux服务_图1.png
                RemainAfterExit：默认值no
                    默认值为no，这个设置采用booleean值，可以是0、no、off、1、yes、on等值。
                    它表明服务是否应当被视为激活的，即便当它所有的进程都退出了。
                    简言之，这个设置用于告诉systemd服务是否应当是被视为激活状态，而不管进程是否退出。
                    当为true时，即便服务退出，systemd依然将这个服务视为激活状态，反之则服务停止。
                GuessMainPID
                    采用boolean值指定systemd在无法确切的查明服务的时候是否需要猜测服务的main pid。
                    除非Type=forking被采用并且PIDFile没有被设置，否则这个选项会被忽略。
                    因为当设置为Type的其他选项，或者显示的指定了PID文件后，systemd总是能够知道main pid。
                PIDFile
                    采用一个绝对路径的文件名指定守护进程的PID文件。当Type=forking被设置的时候，建议采取这个设置。
                    当服务启动后，systemd会读取守护进程的主进程id。systemd不会对该文件写入数据。
                BusName
                    使用一个D-Bus的总线名称,作为该服务的可访问名称。当Type=dbus的时候，该设置被强制使用。
                BusPolicy
                    如果该选项被指定，一个自定义的kdbus终结点将会被创建，并且会被指定为默认的dbus节点安装到服务上。
                    这样的自定义终结点自身持有一个策略规则集合。这些规则将会在总线范围内被强制指定。该选项只有在kdbus被激活时有效。
                ExecStart
                    当服务启动的时候（systemctl start youservice.service），会执行这个选项的值，这个值一般是“ExecStart=指令 参数”的形式。
                    当Type=oneshot的时候，只有一个指令可以并且必须给出。原因是oneshot只会被执行一次。
                ExecStartPre、ExecStartPost
                    顾名思义，这两个设置的意义在于ExecStart被执行之前和之后被执行。
                ExecReload
                    服务重启时执行。
                ExecStop
                    服务停止时执行。
                ExecStopPost
                    服务停止后执行。
            节点分类介绍
                3.2.1 启动类型
                    type 字段定义启动类型　
                    simple：默认值，ExecStart字段启动的进程为主进程，如果启动脚本中 以 nohup & 形式启动进程时，此时启动脚本后会自动 kill 当前服务；
                        forking：ExecStart字段将以fork()方式启动，此时父进程将会退出，子进程将成为主进程；
                        oneshot：类似于simple，但只执行一次，Systemd 会等它执行完，才启动其他服务，表明这个服务只要运行一次就行；
                        dbus：类似于simple，但会等待 D-Bus 信号后启动
                        notify：类似于simple，启动结束后会发出通知信号，然后 Systemd 再启动其他服务
                        idle：类似于simple，但是要等到其他任务都执行完，才会启动该服务。一种使用场合是为让该服务的输出，不与其他服务的输出相混合
                3.2.2 启动，停止，重启命令
                        EnvironmentFile：环境参数配置文件，文件内部配置参数形式为key=value键值对，可以在service文件中以$key的形式引用配置项；
                        ExecStart：启动服务时执行的命令；
                        ExecReload：重启服务时执行的命令；
                        ExecStop：停止服务时执行的命令；
                        ExecStartPre：启动服务之前执行的命令；
                        ExecStartPost：启动服务之后执行的命令；
                        ExecStopPost：停止服务之后执行的命令；
                3.2.3 停止模式
                        KillMode 表示停止服务时的方式
                        control-group：默认值，当前控制组里面的所有子进程，都会被杀掉
                        process：只杀主进程
                        mixed：主进程将收到 SIGTERM 信号，子进程收到 SIGKILL 信号
                        none：没有进程会被杀掉，只是执行服务的 stop 命令
                3.2.4 PrivateTmp
                        该字段用于设置服务是否使用私有的 tmp目录；
                        该目录在 /tmp目录下，目录名格式如下：
                        /tmp/systemd-private-66ae5e5313ba4417b83b427fddb36e47-xxx.service-s65dIw/
                        服务启动时创建一个目录，服务停止时删除临时目录；
                        启用该属性后，写临时文件时可能会写到这个目录下，需要注意一下
                        php-fpm临时文件路径问题（Sytemd PrivateTmp的坑）
                        Systemd Unit文件中PrivateTmp字段详解-Jason.Zhi
        Install
            定义如何安装配置文件；
            WantedBy：表示服务所在的服务组；
            WantedBy=multi-user.target 表示服务属于 multi-user.target 用户组；
            multi-user.target 组里的所有服务都将开机启动；
            执行 systemctl enable sshd.service 时
            将把 sshd.service 文件的一个符号链接保存到 /etc/systemd/system 目录下的 
            multi-user.target.wants 子目录中；
        
    ======================================================================  

    +service脚本样例：
        [Unit]
        Description=tzvirtd-Cloud cryptographic server management
        After=network-online.target
        Wants=network-online.target

        [Service]
        User=root
        Group=root
        LimitNOFILE=65536
        Type=simple
        ExecStart=/usr/dong/tzvirtd/tzvirtd/OutPut/bin/Debug/tzvirtd.bin
        ExecStop=/bin/kill -s TERM ${MAINPID}
        ExecReload=
        Restart=always
        TimeoutStopSec=120

        [Install]
        WantedBy=multi-user.target

    +最简化的service模板
        [Unit]
        Description=simulator
        [Service]
        Type=simple
        ExecStart=/home/chenfan/simulator/start.sh
        ExecStop=/home/chenfan/simulator/stop.sh
        [Install]
        WantedBy=multi-user.target
    
    +Demo
        [Unit]
        Description=Esign Service
        After=network.target
        [Service]
        Type=forking
        User=root
        ExecStart=/usr/local/bin/esign-startup.sh
        Restart=on-failure
        [Install]
        WantedBy=default.target

        esign-startup.sh 内容：
        #!/bin/bash
        JAR_PATH=/usr/local/app/esign/esign.war
        LOG_PATH=/usr/local/app/esign/start.log
        nohup java -Xms2048M -Xmx8192M -XX:MetaspaceSize=256M -XX:MaxMetaspaceSize=512M  
                   -jar $JAR_PATH > $LOG_PATH 2>&1 &
    ======================================================================    

    +各种systemd目录的介绍
        /etc/systemd  
        /run/systemd 
        /lib/systemd
            /system   ： 很多系统服务都在这个目录下
            /network
            /system-generators
            /system-preset
            /system-shutdown
        /usr/lib/systemd
            /user
            /network
            /scripts
            /catalog
            /user-generators
        /var/lib/systemd
        /bin/systemd
        /usr/shared/systemd
        关系：
            ● /etc/systemd vs  /usr/lib/systemd
            Systemd 默认从目录/etc/systemd/system/读取配置文件
            里面存放的大部分文件都是符号链接，指向目录/usr/lib/systemd/system
            systemctl enable 命令用于在上面两个目录之间，建立符号链接关系
            ● /lib/systemd/system  vs  /usr/lib/systemd/system
            两者指向的是同一目录（在银河飞腾下不是）
            ● /etc/systemd/system  vs  /run/systemd/system  vs  /lib/systemd/system
            参：https://www.cnblogs.com/TonvyLeeBlogs/articles/13762400.html
            而unit的文件位置一般主要有三个目录:
            ┌────────────────────────┬─────────────────────────────┐
            │Path                    │ Description                 │
            ├────────────────────────┼─────────────────────────────┤
            │/etc/systemd/system     │ Local configuration         │
            ├────────────────────────┼─────────────────────────────┤
            │/run/systemd/system     │ Runtime units               │
            ├────────────────────────┼─────────────────────────────┤
            │/lib/systemd/system     │ Units of installed packages │
            └────────────────────────┴─────────────────────────────┘
            这三个目录的配置文件优先级依次从高到低，如果同一选项三个地方都配置了，优先级高的会覆盖优先级低的
            系统安装时，默认会将unit文件放在/lib/systemd/system目录。
            如果我们想要修改系统默认的配置，比如nginx.service，一般有两种方法：
            1. 在/etc/systemd/system目录下创建nginx.service文件，里面写上我们自己的配置。
            2. 在/etc/systemd/system下面创建nginx.service.d目录，
               在这个目录里面新建任何以.conf结尾的文件，然后写入我们自己的配置。推荐这种做法。
            /run/systemd/system这个目录一般是进程在运行时动态创建unit文件的目录，一般很少修改
            
======================================================================    

+界面程序的崩溃自启
    尝试的，但不可行的方法：
        通过服务，无论是直接启动WebsignServer，还是通过keepalive启动WebsignServer，都不行
        原因可能是桌面环境没准备好
        另外，在 /etc/profile 或 /etc/rc.local 中启动keepalive的方法也不行
        从报错提示看，也是无法跟桌面环境进行连接
    可行的方法
        1. 写一个keepalive程序
            原理就是 ps -a | grep 程序名 ; if [ $? -eq 0 ]; then 执行目标程序 fi
        2. 写一个 /ect/xdg/autostart/*.desktop 文件
            内容为
            [Desktop Entry]
            Exec=（自己的应用程序绝对路径）
            Type=Application
            
            上面方法在麒麟飞腾下测试可用（可能需要.destkop文件有执行权限），也有说法
            1. 进入 cd /home/xxx/.config（xxx为用户名）
            2. 新建autostart文件夹（这个自己新建）
            3. 进入到autostart文件夹
            4. 新建一个后缀为desktop的文件