<catelob s0>
语法
       ps [options]
简述
       ps 用以显示活动进程的信息
       如果想获得即时更新的信息，请使用top命令
       
       该版本的ps，支持如下几种命令选项标准
       1   UNIX options, 可以成组使用，但必须以-为前缀
       2   BSD options, 可以成组使用，且禁止带-
       3   GNU long options, 以--为前缀
       上面几种不同的选项格式可以自由混合，但可能出现冲突：
       这表现在不同的标准可能对同一个控制项，有不同的解释，
       如 ps -a a， 前一个 -a 按UNIX标准解释，后一个 a 按BSD标准解释
      
       注意，ps -aux 不同于 ps aux，POSIX 和 UNIX 标准要求 "ps -aux"打印
       用户x所拥有的全部进程，同时打印所有符合 -a 的进程， 如果不存在
       名为 x 的用户，则 ps -aux 将被理解为 ps aux，并给出警告，
       这是为了兼容旧的脚本，但这是脆弱的，不要总指望这种方式一定会正确执行.
       默认的，ps 选择哪些euid（effect user id）与当前用户匹配的进程，
       以及与当前终端项关联的进程。
       
       它显示进程ID（pid=PID），与进程相关的终端（tname=TTY），
       以[DD-]hh:mm:ss格式显示的累计CPU时间（time=TIME），
       以及可执行文件的名称（ucmd=CMD）。
       默认情况下，输出是不排序的。
       
       使用 BSD 标准的选项，将会添加进程的state栏，并显示命令的启动参数（而
       不是仅显示程序名），你可以使用 PS_FORMAT 选项覆盖这种行为。 BSD标准的
       选项也会改变进程的选择集，包含其它终端（被你拥有的）的（相关联的）进程
       或者也可以这样说：除了被其它用户所拥有的进程，以及不在终端上的进程之外
       的所有进程的集合。
       
       除下文所述外，过程选择选项是加法的。 
       默认选择被丢弃，然后所选择的过程被添加到要显示的过程集合中。 
       因此，如果一个过程符合任何给定的选择标准，它将被显示出来
举例
       使用 UNIX 标准，查看系统上的所有进程
          ps -e
          ps -ef
          ps -eF
          ps -ely
          
       使用BSD标准，查看系统上的所有进程
          ps ax
          ps axu
       显示进程树
          ps -ejH
          ps axjf
       获取线程信息
          ps -eLf
          ps axms
       获取安全信息
          ps -eo euser,ruser,suser,fuser,f,comm,label
          ps axZ
          ps -eM
       查看所有以root角色运行的进程
          ps -U root -u root u
       
       以用户定义的格式，查看所有进程
          ps -eo pid,tid,class,rtprio,ni,pri,psr,pcpu,stat,wchan:14,comm
          ps axo stat,euid,ruid,tty,tpgid,sess,pgrp,ppid,pid,pcpu,comm
          ps -Ao pid,tt,user,fname,tmout,f,wchan
       仅查看所有syslogd的进程的id
       Print only the process IDs of syslogd:
          ps -C syslogd -o pid=
       仅打印id为42的进程的名字
          ps -q 42 -o comm=
简单进程选择
       BSD 风格
       a      BSD风格默认只显示你自己的进程，选项a可以取消这种限制
              另一种 的描述是，该选项会使ps列出所有具有终端（tty）的进程。
              或者与 x 选项一起使用时，列出所有的进程。
       x      BSD风格默认只显示具有终端（与终端关联）的进程，选项x可取消这种限制
              另一种描述是，该选择的使ps列出所有当前用户的进程
              或者与 a 选项一起使用时，列出所有的进程。
       g      该选项已过时，不推荐使用
       T      选择所有与当前终端关联的进程.  等同于不带任何参数的 t 选项
       r      将选择限制为仅运行的进程
       
       UNIX风格
       -A     等同于 -e.
       -e     选择所有进程
       -d     所有进程，除了 session leaders.
              session的特点
              session的主要特点是当session的leader退出后，
              session中的所有其它进程将会收到SIGHUP信号，其默认行为是终止进程，
              即session的leader退出后，session中的其它进程也会退出。
              如果session和tty关联的话，它们之间只能一一对应，
              一个tty只能属于一个session，一个session只能打开一个tty。
              当然session也可以不和任何tty关联。
       -a     显示所有进程，除了 session leaders 和与终端不关联的进程
       -N     等同于 --deselect.
       
       GNU风格
       --deselect
              显示所有进程，除了满足描述的进程
通过列表选择进程
       这些选项接受一个参数，参数为空格或逗号分隔的一个列表
       她它们可以被多次使用，如：ps -p "1 2" -p 3,4
       
       BSD风格
       123    等同于 --pid 123.
       p pidlist
              使用进程id选择.  等同于 -p 和 --pid.
       q pidlist
              通过进程id选择 (快速模式).  等同于 -q 和 --quick-pid.
       t ttylist
              通过终端选择.  类似于 -t 和 --tty, 但也能使用一个空的ttylist
              来表示使用ps命令关联的那个，但这时建议使用选项T，它更简洁
       U userlist
              根据有效的用户ID (EUID)或名称选择
              这会选择那些effective user name or ID在userlist中的进程
              effective user ID描述的是the user whose file access
              permissions are used by the process，等同于 -u 和 --user
              参：geteuid(2)
              
       UNIX风格
       -123   等同于 --pid 123.              
       -C cmdlist
              通过command name选择. 选择的进程，其可执行程序名在cmdlist中
       -G grplist
              通过real group ID (RGID)或名字选择
              选择的进程，其 real group name or ID 在 grplist 中，参 getgid(2)
       -g grplist
              通过 session 或 effective group name 选择
              当列表完全是数字时（如会话），这个ps将按会话选择。 
              只有当某些组的名字也被指定时，组的ID数字才会起作用。 
              参见-s和-group选项。
       -p pidlist
              通过PID选择，这将选择进程ID号出现在pidlist中的进程。 
              等同于 p and --pid.
       -q pidlist
              按PID选择（快速模式）。 这将选择进程ID号出现在pidlist中的进程。 
              使用该选项，ps只读取pid列表中列出的pid的必要信息，而不应用额外的过滤规则。
              pids的顺序没有被排序，并被保留下来。
              在这种模式下，不允许有额外的选择选项、排序和森林类型列表。 
              与q和--quick-pid相同。
       -s sesslist
              通过会话ID选择。 这将选择具有在sesslist中指定的会话ID的进程。          
       -t ttylist
              按tty选择。 这将选择与ttylist中给出的终端相关的进程。 
              终端（ttys，或文本输出的屏幕）可以用几种形式指定： /dev/ttyS1, ttyS1, S1.  
              可以用一个普通的"-"来选择没有连接到任何终端的进程。
       -U userlist
              按真实用户ID（RUID）或名称选择。
              它选择那些真实用户名或ID在用户列表中的进程。 
              真实用户ID标识了创建该进程的用户，见getuid(2)。
       -u userlist
              按有效用户ID（EUID）或名称选择。 
              这将选择其有效用户名或ID在userlist中的进程。
              有效用户ID描述了进程所使用的文件访问权限的用户（见geteuid(2)）。 
              与U和--user相同。
       GNU风格
       --Group grplist
              通过真实组ID（RGID）或名称选择。 与-G相同。
       --group grplist
              通过有效组ID（EGID）或名称选择。 
              这将选择其有效组名或ID在grplist中的进程。
              有效组ID描述了进程所使用的文件访问权限的组（见getegid(2)）。 
              -g选项通常是--group的替代方案。
       --pid pidlist
              按进程ID选择。 与-p和p相同。
       --ppid pidlist
              按父进程ID选择。 这将选择pidlist中父进程ID的进程。 
              也就是说，它选择的是pidlist中所列进程的子进程。
       --quick-pid pidlist
              按进程ID选择（快速模式）。 与-q和q相同。
       --sid sesslist
              通过会话ID选择。 与-s相同。
       --tty ttylist
              按终端选择。 与-t和t相同。
       --User userlist
              通过真实的用户ID（RUID）或名字选择。 与-U相同。
       --user userlist
              通过有效的用户ID（EUID）或名称选择。 与-u和U相同
输出格式控制 
       这些选项是用来选择ps显示的信息的。 输出结果可能因人而异。
       
       UNIX风格
       -c     Show different scheduler information for the -l option.
              为-l选项显示不同的调度器信息
       -f     Do full-format listing. 
              这个选项可以和许多其他UNIX风格的选项结合起来，增加额外的列。 
              它还会使命令参数被打印出来。 
              当与-L一起使用时，NLWP（线程数）和LWP（线程ID）列将被添加。 
              参见c选项、格式关键字args和格式关键字comm。
       -j     Jobs format.
       -o format
              用户定义的格式。
              格式是一个空白分隔或逗号分隔的列表形式的单一参数，
              它提供了一种指定单个输出列的方法。 
              认可的关键字在下面的STANDARD FORMAT SPECIFIERS部分有描述。
              列头可以根据需要进行重命名（ps -o pid,ruser=RealUser -o comm=Command）。 
              如果所有列的标题都是空的（ps -o pid= -o comm=），那么标题行将不会被输出。
              列的宽度将根据需要增加宽的标题；
              这可以用来扩大列的宽度，
              如WCHAN（ps -o pid,wchan=WIDE- WCHAN-COLUMN -o comm）。 
              也提供了明确的宽度控制（ps opid, wchan:42,cmd）。 
              ps -o pid=X, comm=Y的行为因人而异；
              输出可能是一列名为 "X,comm=Y "或两列名为 "X "和 "Y"。 
              在有疑问的时候使用多个-o选项。 
              使用PS_FORMAT环境变量来指定所需的默认值；
              DefSysV和DefBSD是宏，可以用来选择默认的UNIX或BSD列。
       -O format
              类似于-o，但预装了一些默认的列。 
              与-o pid,format,state,tname,time,command
              或-o pid,format,tname,time,cmd相同，见 -o。
       -y     不显示标志；显示rss以代替addr。 这个选项只能和-l一起使用。
       -F     额外的完整格式。 参见-f选项，-F暗示了该选项。
       -j     作业格式。
       -l     长格式。 -y选项通常与此有关。
       -M     增加一列安全数据。 与Z相同（用于SELinux）。
              
       BSD风格
       j      BSD job control format. BSD作业控制格式。
       l      Display BSD long format. 显示BSD长格式。
       O format
              是预装的o（overloaded）。
              BSD的O选项可以像-O（用户定义的输出格式，预设一些常用字段）一样，
              也可以用来指定排序顺序。 
              启发式方法被用来确定这个选项的行为。 
              为了确保获得所需的行为（排序或格式化），
              请以其他方式指定该选项（例如，用-O或-排序）。 
              当作为一个格式化选项使用时，它与-O相同，具有BSD个性。
       o format
              指定用户定义的格式。 与-o和--format相同。
       s      显示信号格式。
       u      显示面向用户的格式。
       v      显示虚拟内存格式。
       X      Register format.
       Z      增加一列安全数据。 与-M（用于SELinux）相同。
              
       GNU风格
       --format format
              用户定义的格式。 与-o和o相同。
       --context
              显示安全上下文格式（用于SELinux）。
输出修饰语 
       GNU风格
       --cols n 
              设置屏幕宽度。
       --columns n 
              设置屏幕宽度。
       --cumulative 
              包括一些死亡的子进程数据（作为与父进程的总和）。
       --forest 
              ASCII艺术进程树。
       --headers 
              重复打印标题行，每页输出一个。
       --lines n 
              设置屏幕高度。
       --no-headers 
              完全不打印标题行。 --no-heading是这个选项的一个别名。
       --rows n 
              设置屏幕高度。
       --sort spec 
              指定排序的顺序。 排序的语法是 
              [+|-]key[,[+|-]key[,...]].  从STANDARD FORMAT SPECIFIERS部分选择一个多字母键。 
              "+"是可选的，因为默认的方向是数字或词法的递增顺序。 
              与k相同。例如：ps jax --sort=uid,-ppid, +pid 
       --width n 
              设置屏幕宽度。
       UNIX风格
       -H 显示进程的层次结构（森林）。
       -w 宽幅输出。 使用该选项两次，可以获得无限的宽度。
       BSD风格
       c 显示真正的命令名称。 这是从可执行文件的名称得出的，而不是从argv值得出的。 
         因此不显示命令参数和对其进行的任何修改。这个选项有效地将args格式关键字变成了comm格式关键字；
         它对-f格式选项和各种BSD风格的格式选项很有用，它们通常都显示命令参数。 
         参见-f选项，格式关键字args和格式关键字comm。
       e 显示命令后的环境。
       f ASCII艺术进程的层次结构（森林）。
       h No header. (或者，在BSD个性中每个屏幕有一个头)。h选项是有问题的。 
         标准的BSD ps使用这个选项在每页输出上打印一个页眉，但是老的Linux ps使用这个选项完全禁用页眉。 
         这个版本的ps沿用了Linux的做法，即不打印页眉，除非选择了BSD个性，
         在这种情况下，它会在每一页的输出上打印一个页眉。 
         不管当前的个性是什么，
         你可以使用长选项--headers和--no-headers来分别启用每页打印页眉或完全禁用页眉。
       k spec 指定排序顺序。 排序的语法是 
         [+|-]key[,[+|-]key[,...]].  从STANDARD FORMAT SPECIFIERS部分选择一个多字母键。 
         "+"是可选的，因为默认方向是数字或词法的增加。 与--排序相同。
         例子： 
         ps jaxkuid,-ppid,+pid 
         ps axk comm o comm,args 
         ps kstart_time -ef 
       n WCHAN和USER的数字输出（包括所有类型的UID和GID）。
       O order 
         排序顺序（重载）。 
         BSD的O选项可以像-O（用户定义的输出格式，预先定义了一些常见的字段）一样，
         也可以用来指定排序顺序。 启发式方法被用来确定这个选项的行为。 
         为了确保获得所需的行为（排序或格式化），以其他方式指定该选项（例如，用-O或-sort）。
         对于排序，过时的BSD O选项语法是 
         O[+|-]k1[,[+|-]k2[,...]].  
         它根据下面OBSOLETE SORT KEYS部分描述的单字母短键k1,k2,...序列所指定的多级排序来排列进程列表。 
         目前 "+"是可选的，只是在一个键上重复默认的方向，
         但可能有助于区分O排序和O格式。 "-"只在它前面的键上反转方向。
       S 将一些信息，如CPU的使用，从死的子进程汇总到它们的父进程中。 
         这对于检查一个父进程反复分叉短命的子进程进行工作的系统很有用。
       w 宽幅输出。 使用该选项两次可获得无限宽度。
线程显示
       H 显示线程，就像它们是进程一样。
       m 在进程之后显示线程。
       -L 显示线程，可能带有LWP和NLWP列。
       -m 在进程之后显示线程。
       -T 显示线程，可能带有SPID列。       
其他信息
       L 列出所有的格式指定器。
       V 打印procps-ng的版本。
       -V 打印 procps-ng 的版本。
       --help section
              打印一个帮助信息。 节的参数可以是
              简单、列表、输出、线程、杂项或全部。 该参数可以是
              简称为下划线字母之一，如：s|l|o|t|m|a。
       --info 打印调试信息。
       --version
              打印 procps-ng 的版本。
NOTES
        这个ps通过读取/proc中的虚拟文件来工作。 
        这个ps不需要setuid kmem，也不需要有任何权限来运行。 
        不要给这个ps任何特殊的权限。
       目前，CPU的使用率是以一个进程在整个生命周期内运行的时间百分比来表示的。 
       这并不理想，而且也不符合ps其他方面所符合的标准。
       CPU的使用率不可能精确到100%。
       SIZE和RSS字段没有计算进程的某些部分，
       包括页表、内核堆栈、线程信息结构和任务结构。 
       这通常是至少20KiB的内存，总是驻留的。 
       SIZE是进程的虚拟大小（代码+数据+堆栈）。
       标记为<defunct>的进程是死的进程（所谓的 "僵尸"），
       因为它们的父进程没有正确地销毁它们而保留下来。
       如果父进程退出，这些进程将被init(8)销毁。
       如果用户名的长度大于显示列的长度，用户名将被截断。
       参见-o和-O格式化选项来定制长度。
       不推荐使用ps -aux这样的命令选项，因为它混淆了两种不同的标准。
       根据POSIX和UNIX的标准，
       上述命令要求显示所有带有TTY的进程（通常是用户正在运行的命令），
       加上一个名为 "x "的用户所拥有的所有进程。 
       如果这个用户不存在，那么ps会认为你真正的意思是 "ps aux"。
&<进程标志>
       这些值的总和显示在 "F "列中，它是由flags输出指定器提供的： 
        1 fork了，但没有执行 
        4 使用了超级用户的权限         
&<进程状态代码>
       下面是s、stat和状态输出指定器（标头 "STAT "或 "S"）将显示的不同数值，以描述进程的状态： 
               D 不间断的睡眠(通常是IO) 
               I 空闲的内核线程 
               R 正在运行或可运行(在运行队列中) 
               S 可中断的睡眠（等待事件的完成） 
               T 被工作控制信号停止 
               t 在跟踪过程中被调试器停止 
               W 分页（从2.6.xx内核开始无效） X 死亡（永远不应该被看到） 
               Z 失效的（"僵尸"）进程，被终止但没有被其父方收割 
       对于BSD格式和使用stat关键字时，可以显示额外的字符： 
               < 高优先级（对其他用户不友好） 
               N 低优先级 (对其他用户好) 
               L 将页面锁定在内存中（用于实时和自定义 IO） s 是一个会话领导者 
               l 是多线程的（使用CLONE_THREAD，就像NPTL的pthreads那样）。
               + 是在前台进程组中             
废弃的排序键 
       这些键被BSD的O选项使用（当它被用于排序时）。
       GNU --sort 选项不使用这些键，
       而是使用下面STANDARD FORMAT SPECIFIERS章节中描述的指定器。 
       注意，排序时使用的值是ps使用的内部值，
       而不是在某些输出格式字段中使用的 "熟 "值
       （例如，在tty上排序将按设备号排序，而不是根据显示的终端名称）。 
       如果你想对熟化的值进行排序，请将ps的输出结果输入sort(1)命令。
       
       KEY  LONG        DESCRIPTION
       c    cmd         可执行文件的简单名称
       C    pcpu        cpu利用率
       f    flags       长格式的F字段的标志
       g    pgrp        进程组ID
       G    tpgid       控制tty进程组的ID
       J    cutime      累积用户时间
       J    cstime      累积系统时间
       k    utime       用户时间
       m    min_flt     小型页面故障的数量
       M    maj_flt     主要页面故障的数量
       n    cmin_flt    累积的次要页面故障
       N    cmaj_flt    累积的主要页面故障
       o    session     session ID
       p    pid         进程ID
       P    ppid        父进程ID
       r    rss         驻留集大小
       R    resident    区驻留页
       s    size        内存大小，以千字节为单位
       S    share       共享页的数量
       t    tty         控制tty的设备号
       T    start_time  进程开始的时间
       U    uid         用户ID号
       u    user        用户名称
       v    vsize       虚拟机总大小（KiB
       y    priority    内核调度优先级
AIX FORMAT DESCRIPTORS
       这个ps支持AIX格式描述符，其工作原理有点像printf(1)和printf(3)的格式化代码。
       例如，正常的默认输出可以这样产生：ps -eo "%p %y %x %c"。 
       NORMAL代码将在下一节描述。
       CODE   NORMAL   HEADER
       %C     pcpu     %CPU
       %G     group    GROUP
       %P     ppid     PPID
       %U     user     USER
       %a     args     COMMAND
       %c     comm     COMMAND
       %g     rgroup   RGROUP
       %n     nice     NI
       %p     pid      PID
       %r     pgid     PGID
       %t     etime    ELAPSED
       %u     ruser    RUSER
       %x     time     TIME
       %y     tty      TTY
       %z     vsz      VSZ
标准格式指定器
       这里有不同的关键字，可以用来控制输出格式（例如，用选项-o），
       或者用GNU风格的-sort选项对所选进程进行排序。
       例如：ps -eo pid,user,args --sort user 
       这个版本的ps试图识别其他ps实现中使用的大部分关键字。
       以下用户定义的格式指定符可能包含空格：
       args, cmd, comm, command, fname, ucmd, ucomm, lstart, bsdstart, start。
       有些关键字可能无法进行排序。
       
       CODE        HEADER    DESCRIPTION
       %cpu        %CPU      进程的cpu利用率为 "##.#"格式。
                             目前，它是用CPU时间除以进程运行的时间（cputime/realtime比率），以百分比表示。 
                             除非你很幸运，否则它不会加到100%。 (别名pcpu)。
       %mem        %MEM      进程的常驻集大小与机器上的物理内存的比率，以百分比表示。 (alias pmem). 
       args        COMMAND   COMMAND命令，其所有参数为一个字符串。对参数的修改可能会被显示出来。 
                             这一栏的输出可能包含空格。 
                             一个标记为<defunct>的进程是部分死亡的，等待被它的父进程完全销毁。 
                             有时，进程的参数将不可用；当这种情况发生时，ps将在括号中打印可执行文件的名称。 
                             (别名cmd，command)。 另见comm格式关键字、-f选项和c选项。
                             最后指定时，这一栏将延伸到显示器的边缘。 
                             如果ps不能确定显示宽度，如输出被重定向（管道）到一个文件或另一个命令时，
                             输出宽度是未定义的（可能是80，无限，由TERM变量决定，等等）。 
                             在这种情况下，可以使用COLUMNS环境变量或-cols选项来精确确定宽度。 
                             w或-w选项也可用于调整宽度。
       blocked     BLOCKED   被封锁的信号的屏蔽，见signal(7)。
                             根据字段的宽度，会显示16进制格式的32或64位掩码。(别名sig_block, sigmask)。
       bsdstart    START     命令开始的时间。 如果进程开始的时间少于24小时，
                             输出格式为 "HH:MM"，否则为 "Mmm:SS"（其中Mmm为月份的三个字母）。 
                             参见lstart, start, start_time, 和stime。
       bsdtime     TIME      累积的cpu时间，用户+系统。 显示格式通常是 "MMM:SS"，
                             但如果进程使用了超过999分钟的cpu时间，可以向右移动。
       c           C         处理器利用率。目前，这是在进程的生命周期内使用百分比的整数值。 (见%cpu)。
       caught      CAUGHT    捕获信号的掩码，见 signal(7)。根据字段的宽度，
                             显示16进制格式的32或64位掩码。(别名sig_catch, sigcatch)。
       cgname      CGNAME    显示进程所属的控制组的名称。
       cgroup      CGROUP    显示该进程所属的控制组。                             
       class       CLS       进程的调度类。 (别名policy, cls)。 字段的可能值是：
                                      -   not reported
                                      TS  SCHED_OTHER
                                      FF  SCHED_FIFO
                                      RR  SCHED_RR
                                      B   SCHED_BATCH
                                      ISO SCHED_ISO
                                      IDL SCHED_IDLE
                                      DLN SCHED_DEADLINE
                                      ?   unknown value
       cls         CLS       进程的调度类。 (别名policy, cls)。 字段的可能值是：
                                      -   not reported
                                      TS  SCHED_OTHER
                                      FF  SCHED_FIFO
                                      RR  SCHED_RR
                                      B   SCHED_BATCH
                                      ISO SCHED_ISO
                                      IDL SCHED_IDLE
                                      DLN SCHED_DEADLINE
                                      ?   unknown value
       cmd         CMD       see args.  (alias args, command).
       comm        COMMAND   命令名称（只有可执行的名称）。对命令名的修改不会被显示。 
                             一个标记为<defunct>的进程是部分死亡的，等待被其父代完全销毁。 
                             这一栏的输出可能包含空格。 (别名 ucmd, ucomm)。 
                             也请参见args格式关键字、-f选项和c选项。当最后指定时，
                             这一列将延伸到显示器的边缘。 
                             如果ps不能确定显示的宽度，如输出被重定向（管道）到一个文件或另一个命令时，
                             输出的宽度是未定义的（可能是80，无限，由TERM变量决定，等等）。 
                             在这种情况下，可以使用COLUMNS环境变量或-cols选项来精确确定宽度。 
                             也可以用w或-w选项来调整宽度。
       command     COMMAND   See args.  (alias args, command).
       cp          CP        per-mill (tenths of a percent) CPU usage.  (see
                             %cpu).
       cputime     TIME      cumulative CPU time, "[DD-]hh:mm:ss" format.
                             (alias time).
       cputimes    TIME      cumulative CPU time in seconds (alias times).
       drs         DRS       数据常驻集大小，即用于可执行代码以外的物理内存的数量。
       egid        EGID      进程的有效组ID号，是一个 十进制的整数。 (别名gid)。
       egroup      EGROUP    进程的有效组ID。 这将是文本的组ID，
                             如果可以获得并且字段宽度允许的话，或者是十进制的表示。 (别名group)。
       eip         EIP       instruction pointer.
       esp         ESP       stack pointer.
       etime       ELAPSED   elapsed time since the process was started, in
                             the form [[DD-]hh:]mm:ss.
       etimes      ELAPSED   elapsed time since the process was started, in
                             seconds.
       euid        EUID      effective user ID (alias uid).
       euser       EUSER     有效的用户名。 如果可以获得，并且字段宽度允许，
                             这将是文本的用户ID，否则就是十进制表示。 
                             可以使用n选项来强制使用十进制表示法。 (别名uname, user)。
       f           F         flags associated with the process, see the
                             PROCESS FLAGS section.  (alias flag, flags). @进程标志
       fgid        FGID      filesystem access group ID.  (alias fsgid).
       fgroup      FGROUP    文件系统访问组ID。 
                             这将是文本组ID，如果它可以被获得并且字段宽度允许的话，
                             或者是一个十进制的代表。 (alias fsgroup)。
       flag        F         see f.  (alias f, flags).
       flags       F         see f.  (alias f, flag).
       fname       COMMAND   first 8 bytes of the base name of the process's
                             executable file.  The output in this column may
                             contain spaces.
       fuid        FUID      filesystem access user ID.  (alias fsuid).
       fuser       FUSER     filesystem access user ID.  This will be the
                             textual user ID, if it can be obtained and the
                             field width permits, or a decimal representation
                             otherwise.
       gid         GID       see egid.  (alias egid).
       group       GROUP     see egroup.  (alias egroup).
       ignored     IGNORED   mask of the ignored signals, see signal(7).
                             According to the width of the field, a 32 or 64
                             bits mask in hexadecimal format is displayed.
                             (alias sig_ignore, sigignore).
       ipcns       IPCNS     Unique inode number describing the namespace the
                             process belongs to. See namespaces(7).
       label       LABEL     security label, most commonly used for SELinux
                             context data.  This is for the Mandatory Access
                             Control ("MAC") found on high-security systems.
       lstart      STARTED   time the command started.  See also
                             bsdstart, start, start_time, and stime.
       lsession    SESSION   displays the login session identifier of a
                             process, if systemd support has been included.
       luid        LUID      displays Login ID associated with a process.
       lwp         LWP       light weight process (thread) ID of the
                             dispatchable entity (alias spid, tid).  See tid
                             for additional information.
       lxc         LXC       The name of the lxc container within which a task
                             is running.  If a process is not running inside a
                             container, a dash ('-') will be shown.
       machine     MACHINE   displays the machine name for processes assigned
                             to VM or container, if systemd support has been
                             included.
       maj_flt     MAJFLT    The number of major page faults that have
                             occurred with this process.
       min_flt     MINFLT    The number of minor page faults that have
                             occurred with this process.
       mntns       MNTNS     Unique inode number describing the namespace the
                             process belongs to. See namespaces(7).
       netns       NETNS     Unique inode number describing the namespace the
                             process belongs to. See namespaces(7).
       ni          NI        nice value. This ranges from 19 (nicest) to -20
                             (not nice to others), see nice(1).  (alias nice).
       nice        NI        see ni.(alias ni).
       nlwp        NLWP      number of lwps (threads) in the process.  (alias
                             thcount).
       numa        NUMA      The node assocated with the most recently used
                             processor.  A -1 means that NUMA information is
                             unavailable.
       nwchan      WCHAN     address of the kernel function where the process
                             is sleeping (use wchan if you want the kernel
                             function name).  Running tasks will display a
                             dash ('-') in this column.
       ouid        OWNER     displays the Unix user identifier of the owner of
                             the session of a process, if systemd support has
                             been included.
       pcpu        %CPU      see %cpu.  (alias %cpu).
       pending     PENDING   mask of the pending signals. See signal(7).
                             Signals pending on the process are distinct from
                             signals pending on individual threads.  Use the m
                             option or the -m option to see both.  According
                             to the width of the field, a 32 or 64 bits mask
                             in hexadecimal format is displayed.  (alias sig).
       pgid        PGID      process group ID or, equivalently, the process ID
                             of the process group leader.  (alias pgrp).
       pgrp        PGRP      see pgid.  (alias pgid).
       pid         PID       a number representing the process ID (alias
                             tgid).
       pidns       PIDNS     Unique inode number describing the namespace the
                             process belongs to. See namespaces(7).
       pmem        %MEM      see %mem.  (alias %mem).
       policy      POL       scheduling class of the process.  (alias
                             class, cls).  Possible values are:
                                      -   not reported
                                      TS  SCHED_OTHER
                                      FF  SCHED_FIFO
                                      RR  SCHED_RR
                                      B   SCHED_BATCH
                                      ISO SCHED_ISO
                                      IDL SCHED_IDLE
                                      DLN SCHED_DEADLINE
                                      ?   unknown value
       ppid        PPID      parent process ID.
       pri         PRI       priority of the process.  Higher number means
                             lower priority.
       psr         PSR       processor that process is currently assigned to.
       rgid        RGID      real group ID.
       rgroup      RGROUP    real group name.  This will be the textual group
                             ID, if it can be obtained and the field width
                             permits, or a decimal representation otherwise.
       rss         RSS       驻留集大小，一个任务所使用的非交换的物理内存
                            （单位：KiloBytes）。 (alias rssize, rsz)。
       rssize      RSS       see rss.  (alias rss, rsz).
       rsz         RSZ       see rss.  (alias rss, rssize).
       rtprio      RTPRIO    realtime priority.
       ruid        RUID      real user ID.
       ruser       RUSER     real user ID.  This will be the textual user ID,
                             if it can be obtained and the field width
                             permits, or a decimal representation otherwise.
       s           S         简单状态显示 (一个字符).   @进程状态代码
                             See stat if you want additional
                             information displayed.  (alias state).
       sched       SCH       scheduling policy of the process.  The policies
                             SCHED_OTHER (SCHED_NORMAL), SCHED_FIFO, SCHED_RR,
                             SCHED_BATCH, SCHED_ISO, SCHED_IDLE and
                             SCHED_DEADLINE are respectively displayed as 0,
                             1, 2, 3, 4, 5 and 6.
       seat        SEAT      displays the identifier associated with all
                             hardware devices assigned to a specific
                             workplace, if systemd support has been included.
       sess        SESS      session ID or, equivalently, the process ID of
                             the session leader.  (alias session, sid).
       sgi_p       P         processor that the process is currently executing
                             on.  Displays "*" if the process is not currently
                             running or runnable.
       sgid        SGID      saved group ID.  (alias svgid).
       sgroup      SGROUP    saved group name.  This will be the textual group
                             ID, if it can be obtained and the field width
                             permits, or a decimal representation otherwise.
       sid         SID       see sess.  (alias sess, session).
       sig         PENDING   see pending.  (alias pending, sig_pend).
       sigcatch    CAUGHT    see caught.  (alias caught, sig_catch).
       sigignore   IGNORED   see ignored.  (alias ignored, sig_ignore).
       sigmask     BLOCKED   see blocked.  (alias blocked, sig_block).
       size        SIZE      approximate amount of swap space that would be
                             required if the process were to dirty all
                             writable pages and then be swapped out.  This
                             number is very rough!
       slice       SLICE     displays the slice unit which a process belongs
                             to, if systemd support has been included.
       spid        SPID      see lwp.  (alias lwp, tid).
       stackp      STACKP    address of the bottom (start) of stack for the
                             process.
       start       STARTED   time the command started.  If the process was
                             started less than 24 hours ago, the output format
                             is "HH:MM:SS", else it is "  Mmm dd" (where Mmm
                             is a three-letter month name).  See also
                             lstart, bsdstart, start_time, and stime.
       start_time  START     starting time or date of the process.  Only the
                             year will be displayed if the process was not
                             started the same year ps was invoked, or "MmmDD"
                             if it was not started the same day, or "HH:MM"
                             otherwise.  See also bsdstart, start, lstart,
                             and stime.
       stat        STAT      多字符过程状态。 关于不同数值的含义，
                             请参见PROCESS STATE CODES部分。 
                             如果你只想显示第一个字符，也请参见s和state。
       state       S         see s. (alias s).
       suid        SUID      saved user ID.  (alias svuid).
       supgid      SUPGID    group ids of supplementary groups, if any.  See
                             getgroups(2).
       supgrp      SUPGRP    group names of supplementary groups, if any.  See
                             getgroups(2).
       suser       SUSER     saved user name.  This will be the textual user
                             ID, if it can be obtained and the field width
                             permits, or a decimal representation otherwise.
                             (alias svuser).
       svgid       SVGID     see sgid.  (alias sgid).
       svuid       SVUID     see suid.  (alias suid).
       sz          SZ        size in physical pages of the core image of the
                             process.  This includes text, data, and stack
                             space.  Device mappings are currently excluded;
                             this is subject to change.  See vsz and rss.
       tgid        TGID      a number representing the thread group to which a
                             task belongs (alias pid).  It is the process ID
                             of the thread group leader.
       thcount     THCNT     see nlwp.  (alias nlwp).  number of kernel
                             threads owned by the process.
       tid         TID       the unique number representing a dispatchable
                             entity (alias lwp, spid).  This value may also
                             appear as: a process ID (pid); a process group ID
                             (pgrp); a session ID for the session leader
                             (sid); a thread group ID for the thread group
                             leader (tgid); and a tty process group ID for the
                             process group leader (tpgid).
       time        TIME      cumulative CPU time, "[DD-]HH:MM:SS" format.
                             (alias cputime).
       times       TIME      cumulative CPU time in seconds (alias cputimes).
       tname       TTY       controlling tty (terminal).  (alias tt, tty).
       tpgid       TPGID     ID of the foreground process group on the tty
                             (terminal) that the process is connected to, or
                             -1 if the process is not connected to a tty.
       trs         TRS       text resident set size, the amount of physical
                             memory devoted to executable code.
       tt          TT        controlling tty (terminal).  (alias tname, tty).
       tty         TT        controlling tty (terminal).  (alias tname, tt).
       ucmd        CMD       see comm.  (alias comm, ucomm).
       ucomm       COMMAND   see comm.  (alias comm, ucmd).
       uid         UID       see euid.  (alias euid).
       uname       USER      see euser.  (alias euser, user).
       unit        UNIT      displays unit which a process belongs to, if
                             systemd support has been included.
       user        USER      see euser.  (alias euser, uname).
       userns      USERNS    Unique inode number describing the namespace the
                             process belongs to. See namespaces(7).
       utsns       UTSNS     Unique inode number describing the namespace the
                             process belongs to. See namespaces(7).
       uunit       UUNIT     displays user unit which a process belongs to, if
                             systemd support has been included.
       vsize       VSZ       see vsz.  (alias vsz).
       vsz         VSZ       virtual memory size of the process in KiB
                             (1024-byte units).  Device mappings are currently
                             excluded; this is subject to change.  (alias
                             vsize).
       wchan       WCHAN     进程正在休眠的内核函数的名称，
                             如果进程正在运行，则为"-"；
                             如果进程是多线程的，ps不显示线程，则为 "*"。
ENVIRONMENT VARIABLES
       The following environment variables could affect ps:
       COLUMNS
          Override default display width.
       LINES
          Override default display height.
       PS_PERSONALITY
          Set to one of posix, old, linux, bsd, sun, digital...  (see section
          PERSONALITY below).
       CMD_ENV
          Set to one of posix, old, linux, bsd, sun, digital...  (see section
          PERSONALITY below).
       I_WANT_A_BROKEN_PS
          Force obsolete command line interpretation.
       LC_TIME
          Date format.
       PS_COLORS
          Not currently supported.
       PS_FORMAT
          Default output format override. You may set this to a format string
          of the type used for the -o option.  The DefSysV and DefBSD values
          are particularly useful.
       POSIXLY_CORRECT
          Don't find excuses to ignore bad "features".
       POSIX2
          When set to "on", acts as POSIXLY_CORRECT.
       UNIX95
          Don't find excuses to ignore bad "features".
       _XPG
          Cancel CMD_ENV=irix non-standard behavior.
       In general, it is a bad idea to set these variables.  The one exception
       is CMD_ENV or PS_PERSONALITY, which could be set to Linux for normal
       systems.  Without that setting, ps follows the useless and bad parts of
       the Unix98 standard.
PERSONALITY
       390        like the OS/390 OpenEdition ps
       aix        like AIX ps
       bsd        like FreeBSD ps (totally non-standard)
       compaq     like Digital Unix ps
       debian     like the old Debian ps
       digital    like Tru64 (was Digital Unix, was OSF/1) ps
       gnu        like the old Debian ps
       hp         like HP-UX ps
       hpux       like HP-UX ps
       irix       like Irix ps
       linux      ***** recommended *****
       old        like the original Linux ps (totally non-standard)
       os390      like OS/390 Open Edition ps
       posix      standard
       s390       like OS/390 Open Edition ps
       sco        like SCO ps
       sgi        like Irix ps
       solaris2   like Solaris 2+ (SunOS 5) ps
       sunos4     like SunOS 4 (Solaris 1) ps (totally non-standard)
       svr4       standard
       sysv       standard
       tru64      like Tru64 (was Digital Unix, was OSF/1) ps
       unix       standard
       unix95     standard
       unix98     standard
SEE ALSO
       pgrep(1), pstree(1), top(1), proc(5).
STANDARDS
       This ps conforms to:
       1   Version 2 of the Single Unix Specification
       2   The Open Group Technical Standard Base Specifications, Issue 6
       3   IEEE Std 1003.1, 2004 Edition
       4   X/Open System Interfaces Extension [UP XSI]
       5   ISO/IEC 9945:2003