使用情景：
    替代vs进行调式，一般在客户电脑上进行调试时，使用windgb，然后将pdf及特定的源码文件放到客户电脑上，即可进行调试
注意事项：
    windbg分64位版和32位版，分别用户调试相应版本的进程，不要弄错了
工具集：
    windgb系统的说，是多个调试工具集，包括：cdb,ntsd,kd,windgb
    cdb：   command debugger        ：命令行式的调试工具，有点类似于linux下的gdb
    ntsd:   NT system debugger      : 跟cdb几乎一致，区别只是启动的时候，NTSD会创建一个新的文本窗口，而CDB继承原有的命令行窗口
    kd:     kernal debugger         : 可用户调试内核模式程序和驱动程序，或者监控系统本身的行为
    windgb: windows debugger        : WinDbg可以看作图形界面的 CDB/NTSD + KD。
调试器支持的环境变量：
    _NT_DEBUGGER_EXTENSION_PATH     指定搜索dll的路径的，多个目录用分号分割
    _NT_EXECUTABLE_IMAGE_PATH       指定搜索二进制可执行文件的路径，多个目录用分号分割
    _NT_SOURCE_PATH                 指定源码搜索路径，多个目录用分号分割
    _NT_SYMBOL_PATH                 符号文件目录树的根目录，多个目录用分号分割
    _NT_ALT_SYMBOL_PATH             指定符号文件搜索路径，优先于_NT_SYMBOL_PATH，这对于保存私有版本的符号文件很有用
    _NT_SYMBOL_PROXY                符号文件服务器
    _NT_EXPR_EVAL = {masm | c++}    指定默认使用的求值表达式，默认masm
使用tools.ini配置文件
    cbd或ntsd启动时会查找该文件，并搜索其内的[NTSD]节
    环境变量INIT,指向包含tools.ini的目录
    一般没啥用，相关参考：http://www.dbgtech.net/windbghelp/index.html
关于即时调试：
    程序发生内存访问异常、除0这样的错误时，会发生异常中断
    另外程序也可能产生断点中断，
    断点可以由调试器插入代码中，也可以通过对类似DbgBreakPoint这样的函数调用产生。
    在汇编语言中，断点一般由int 3指令产生。
    windows会按下面的优先顺序处理程序错误：
    1. 如果出错进程已经附加上了用户模式调试器，所有错误都会使得目标中断到调试器
    2. 如果程序有自己的异常捕获(如try...catch)，异常处理程序会被尝试用于处理错误。
    3. 如果上述条件不满足，则激活一个调试工具。
    任何程序都可以将自己设置为在这种情况下使用的工具。被选定的程序称为即时调试器。
    也称为just-in-time 调试器或者JIT调试器。
    如果即时调试器是标准的用户模式调试器(如CDB、WinDbg或者Microsoft Visual Studio)，
    该调试器会被启动起来并且中断应用程序。
    如果即时调试器是用于创建dump文件的工具(如Dr. Watson)，
    将会创建一个内存转储(dump)文件，并且应用程序将被终止。
    Dr. Watson的说明：
        这是windows默认的即时调试器。
        当Dr. Watson被触发激活时，会弹出一个消息框
        这个窗口提供选项来发送错误报告给Microsoft。
        如果选择不发送(Don't send)，一个dump文件会被创建并保存到磁盘中。
        如果选择发送错误报告，dump文件会被创建并保存，同时将通过网络发送给Microsoft。
    一些调试程序可以将自己设置为windows的默认即时调试器：
        要将即时调试器修改为WinDbg，运行windbg -I
        要将即时调试器修改为CDB，运行cdb -iae 或 cdb -iaec KeyString
            使用-iaec参数时， 
            KeyString 指定要添加到用于启动即时调试器的命令行之后的字符串。
            如果KeyString包含空格，必须用引号括起来。
            该命令如果成功不会有消息显示，但是失败会有提示。
        要将即时调试器修改为NTSD，运行ntsd –iae或 ntsd -iaec KeyString。
            使用-iaec开关时， KeyString 相关说明同上
        要将即时调试器恢复成Dr. Watson，运行drwtsn32 –i。
    只有系统管理员可以修改即时调试设置。
    如果安装了即时调试器，用户模式应用程序可以通过调用DebugBreak 函数来主动中断到调试器中。
启动调试：
    附加到进程
        cdb:
            cdb -p 进程id
            cdb -pn 进程名
            如果CDB是静止的(非调试状态)或者已经在调试一个或多个进程，可以使用.attach命令。
        windgb:
            windbg -p ProcessID （通过命令方式使用windbg）
            windbg -pn ProcessName  （通过命令方式使用windbg）
            当WinDbg在静止模式时，windgb菜单/Attach to a Process（快捷键F6）
            如果调试器已经打开，可以在调试器命令窗口使用 
            .attach (Attach to Process)命令来附加到运行中的进程
            如果WinDbg是静止的，则不能使用.attach命令。
            如果.attach 命令成功，调试器会在下一次执行命令的时候附加到指定进程
    创建新进程
        cdb
            cdb [-o] ProgramName [Arguments] 
            如果CDB在静止状态或者已经在调试一个或多个进程，可以使用.create 命令
        windgb
            windbg [-o] ProgramName [Arguments]  （命令行方式）
            当WinDbg在静止模式时，可以在File菜单中点击Open Executable或者按下CTRL+E来启动新进程。
                如果想为用户模式程序使用任何命令行参数，
                可以在Arguments 文本框中输入。
                如果要修改掉默认的运行目录，在Start directory 中输入。
                如果希望WinDbg附加到子进程，选上Debug child processes also选择框。
                选择完成后，点击Open。
        如果调试器已经激活，可以通过调试器命令窗口中输入.create (Create Process)命令来创建新进程。
        .create不能在WinDbg静止时使用。
        如果.create命令成功，调试器会在下一次执行命令的时候创建指定进程。
    分析dump文件
        windgb
            windbg -y SymbolPath -i ImagePath -z DumpFileName
            如果WinDbg已经在运行并且处于静止模式，可以通过File/Open Crash Dump菜单命令(CTRL+D)来打开dump文件  
                当Open Crash Dump 对话框出现后，
                在File name 文本框输入dump文件的全路径和名字，
                或使用对话框来选择合适的路径和文件名。
                选定需要的文件后，点击Open。
            可以在调试器已经运行之后使用.opendump (Open Dump File)命令后跟g (Go)命令来打开dump文件   
        cdb
            cdb -y SymbolPath -i ImagePath -z DumpFileName 
            也可以在调试器运行之后通过.opendump (Open Dump File)命令后跟g (Go)命令来打开dump文件
            可以同时调试多个dump文件。
                通过在命令行中包含多个-z 开关(每个后跟一个不同的文件名)，
                或者使用.opendump 将更多的dump文件作为调试目标  
        附注：vs调试dump文件 
            vs调试dump文件时，如果dump文件是本机产生的，
            则vs会自动找到相应的exe和pdb文件，
            而如果是别的机器上产生的，
            则需要把dump文件和可执行文件、pdb文件放到同一个目录下
调试器命令行使用：
    进行用户模式调试时，调试命令窗口的提示符如下例中一样。
    2:005>    //2是当前进程号，005是当前线程号。
    可以使用上下键查找历史命令
    可以使用tab键自动补全，tab补全支持通配符识别，
        如fo*!ba, 查找所有名字以"fo"开头的模块中所有以"ba"开头的符号
        如!*prcb 并按下TAB来完成所有包含"prcb"的扩展命令。
        tab补全规则：
            当使用TAB自动完成时，如果文本片断以点号(.)开始，文本将会以点命令来匹配
            如果以感叹号(!)开始，则以扩展命令来匹配。
            如果没有显式指定模块名，则用本地符号和模块来补完。
            如果给出了模块或者模块的模板，则会按所有匹配的符号来补完。
    可以右键点击调试器命令窗口来自动将剪贴板中的内容粘贴到命令中。
    命令的最大长度为4096个字符
    在CDB和KD中，按下ENTER会自动重复上一条命令
    在WinDbg中，可以在选项面板中启用或禁用这个特性。
    要想中断调试，在CDB和KD中使用CTRL+C，在WinDbg中，使用Debug | Break或按下CTRL+BREAK。
    使用.cls (Clear Screen) 命令清空调试器命令窗口的所有文本。该命令清除所有命令的历史记录。
表达式语法    
    很多命令和扩展命令都接受表达式作为参数。
    调试器在执行命令之前先计算这些表达式的值。
    调试器能够识别两种表达式类型：MASM表达式和C++表达式。
    如果没有特别指出，本帮助文档示例中使用的是Microsoft宏汇编(MASM)表达式。
    在MSAM表达式中，所有符号都被当作地址对待(如全局变量，本地变量，函数，段，模块等)。
    C++表达式和真实的C++代码中一样，符号被当作适当的数据类型。
    可以使用下面的方法之一来选择默认的表达式类型：
        在调试器启动之前使用_NT_EXPR_EVAL 环境变量。
        调试器启动时，使用-ee {masm|c++} 命令行选项。
        调试器启动之后，使用.expr (Choose Expression Evaluator)命令来显示或修改表达式类型。
    ?? (Evaluate C++ Expression)命令总是使用C++ 表达式形式。
    Watch 窗口始终使用C++表达式。
    Locals 窗口始终使用C++ 表达式。
    有些扩展命令始终使用MASM表达式(而有一些扩展命令只允许使用数字参数)。
    @@(the other expression),双at号可以嵌套。每层@@号都将表达式类型改为另一种。
别名
    别名其实就和c++中的宏一样，执行前会被替换为相应的字符串
    别名由别名(alias name)和别名等价字符串(alias equivalent)组成  
    调试器支持以下三种别名：
        可以设置和自定义别名(user-named aliases)。
        设置固定别名，他们必须名为$u0, $u1, ..., $u9。
        调试器设置的自动别名(automatic aliases)。
    自定义别名
        别名和等价字符串都是大小写敏感的。   
        使用as (Set Alias)或 aS (Set Alias)命令来定义或修改自定义别名。
            as Name EquivalentLine 
            aS Name EquivalentPhrase 
            aS Name "EquivalentPhrase" 
            as /e Name EnvironmentVariable 
            as /ma Name Address 
            as /mu Name Address 
            as /msa Name Address 
            as /msu Name Address 
            as /x Name Expression 
            aS /f Name File 
            as /c Name CommandString 
            Name    指定别名的名字。该名字可以是不包含空格、ENTER键
                    并且不以"al"、 "as"、 "aS"或"ad"开头的任何文本字符串。
                    Name 是区分大小写的。
            /e      设置别名的值为EnvironmentVariable 指定的环境变量。
            EnvironmentVariable 指定用来获得别名的值的环境变量。
                    使用调试器的环境变量而不是目标的。
                    果从命令提示符窗口启动调试器，环境变量和该窗口使用的一样。
            /ma     将别名的等价值设置为从地址Address 开始的null结尾的ASCII字符串。
            /mu     将别名的等价值设置为从地址Address 开始的null结尾的Unicode字符串。
            /msa    将别名的等价值设置为从地址Address 开始的null结尾的ANSI_STRING结构。
            /msu    将别名的等价值设置为从地址Address 开始的null结尾的UNICODE_STRING结构。
            Address 指定用来决定别名的等价值的虚拟内存位置。
            /x      设置别名的等价值为Expression 的64位值。
            Expression  指定用来求值的表达式。
                    求出的值作为别名的等价值。该语法的更多信息，查看数值表达式语法。
            /f      设置别名的等价值为File 文件的内容。/f 开关只能和aS一起使用，不能和as一起。
            File    指定内容作为别名等价值的文件。
                    File可以包含空格，但是不能将 File用引号括起来。
                    如果指定了非法的文件，会得到一个"Out of memory"的错误信息。
            /c      设置别名的等价值是CommandString 指定的命令的输出。
                    如果命令输出中包含回车符，别名的等价值中也会包含回车，
                    并且每条命令输出的末尾也会包含回车符(即使只指定了一条命令)。
            CommandString   指定输出作为别名等价值的命令。
                    该字符串可以包含任意多个以分号分隔的命令。
            注释
                如果不使用任何命令参数，as 命令将行的结束符作为别名等价值。
                可以用一个分号来结束aS命令。这在需要将所有命令放在单行中的脚本文件中有用。
                如果使用了/e、/ma、/mu、/msa、/msu或/x开关，as 和aS 命令都会在遇到分号时结束。
                如果Name已经作为别名的名字定义了，则该别名被重定义。
                可以使用as 或aS 命令来创建或修改任何自定义别名。
                但是不能使用该命令来控制预定义别名 ($u0 到$u9)。
                可以使用/ma、/mu、/msa、/msu、/f和/c开关来创建包含回车符的别名。
                但是，不能使用包含回车符的别名来执行一个多命令序列，而必须使用分号。
        使用ad (Delete Alias)命令删除别名。
            ad [/q] Name 
            ad * 
            /q  指定使用安静模式。这种模式隐藏当Name指定的别名不存在时显示的错误信息。
            Name   指定要删除的别名的名字。
                如果指定星号(*)，所有别名都会被删除(即使存在名字为"*"的别名)。
            可以使用ad 来删除任何自定义别名。但是不能用它来删除预定义别名($u0 到$u9)。
        列举当前所有自定义别明，使用al (List Aliases)命令。
    使用r (Registers)命令为固定别明指定等价字符串。
        定义固定别名时，必须在字母"u"之前插入点号(.)。
        等号(=)之后的文本是等价字符串。
        等价字符串可以包含空格或分号，但是头部和尾部的空格被忽略掉。
        不能用引号将等价字符串括起来(除非希望替代结果中包含引号)。
        默认情况下，如果没有定义固定别名，他们是空字符串。
    自动别名
        调试器预设了下面一些自动别名，包括：
        $ntnsym、$ntwsym、$ntsym、$CurrentDumpFile
        $CurrentDumpPath、$CurrentDumpArchiveFile、$CurrentDumpArchivePath
    使用别名
        自定义别名和其他字符之间必须使用空白字符隔开才能被识别。
        别名的第一个字符之前和最末一个字符之后必须是空格、分号或者引号。
        也可以使用${ }符号来展开和其他文本连在一起的自定义别名
            Text ${Alias} Text 
            Text ${/d:Alias} Text 
            Text ${/f:Alias} Text 
            Text ${/n:Alias} Text 
            Text ${/v:Alias} Text 
            /d  根据别名当前是否已经定义计算出1或者0。
                如果别名已经定义，${/d:Alias} (译注：原文这里是 ${/v:Alias})被替换为 1；
                如果别名没有定义，${/d:Alias} (译注：原文这里是 ${/v:Alias})被替换为 0。
            /f  如果别名当前已定义则等同于计算别名。
                如果别名已经定义，${/f:Alias} 被替换为等价的别名；
                如果别名没有定义，${/f:Alias}被替换为空字符串。
            /n  如果别名当前已定义则计算别名的名称。
                如果别名已经定义，${/n:Alias}被替换为别名名称；
                如果别名没有定义，${/n:Alias}保留它字面上的值不替换。
            /v  禁止对任何别名求值。
                不论别名是否已经定义，${/v:Alias} 总是保持它字面上的值。
            使用 ${ } 记号的一个优点是，如果和其它字符紧挨着也会对别名求值。
            没有这个记号，调试器只对那些和其它关键字隔开的别名求值。
常用命令：
    .attach PID     附加进程
    .detach PID     分离进程
    g               相当于F5
    t               trace，进入，相当于F11
    p               相当于F10
    gu              go up，跳出，相当于SHIFT+F11
    q / qq          结束调试、并终止被调试的进程
    .restart        重启被调试的应用
    vercommand      显示被调试程序的路径
    .cls            清屏
    .time           显示时间信息（可以测试语句执行速度）
    .echo  STRING   输出字符串
快捷键：
    F7 / CTRL+F10   : run to cursor
    SHIFT + F5      : stop debugging
    CTRL+BREAK / CTRL+C  :  中断执行
    CTRL + SHIFT + F5 :  restart ( .restart)
    F5  : Go (g)
    SHIFT + F11  :  step out (gu : go up)
    F10   : step over (p)
    F11 / F8  : step into (t : trace)
    进入调试状态时，直接回车可重复执行上一条命令；
    按上下方向键可以浏览和选择以前输入过的命令
    神奇的Tab键，进行命令补全；
    ESC清除当前命令输入框中的文本
    可使用Ctrl + Break来终止一个长时间未完成的命令
MASM语法：
    数字表示 ： 
        n (Set Number Base)命令可以用来将进制设置为16、10或8。
        所有未加前缀的数字都会按这个进制来解释
        默认的进制数可以用0x(16进制)、0n(10进制)、0t(8进制)或0y(2进制)前缀覆盖掉
        0x：16进制；  以h结尾的数字，也可以表示16进制数，如4ah
        0n：10进制；
        0t：8进制
        0y：2进制
        如果只有前缀，后面没有跟数，此时表示0，所以0,0x0,0x,0n,0t,0y等，都表示0
    符号：
        在MASM表达式中，所有的符号都解释为地址。
        根据符号指向的数据的不同，
        可能是全局变量，本地变量，函数，段，模块或其他可识别标志的地址。
        如果符号不明确，可以在它前面加上模块名和感叹号(!)。
        如果符号名可能被当作16进制数字，可以加上模块名和感叹号，或者只加上感叹号。
        如果要指定局部变量的符号，可以省略模块名，并在符号前加上美元符号和感叹号( $! )。
    运算符：
        MASM运算符都是基于byte的，C++运算符由C++类型决定(包括指针的转换)。
    调试器命令程序是由调试器命令和如.if、.for和.while这样的流程控制符组成的小程序
    流程控制符：
        即使只有一条命令，所有条件执行和循环也必须用大括号括起来。
        所有条件都必须是一个表达式。不能使用命令作为条件。
        反的大括号(})之前的最后一条命令不需要用分号结束。
        .if
            .if (Condition) { Commands } 
            .if (Condition) { Commands } .else { Commands } 
            .if (Condition) { Commands } .elsif (Condition) { Commands } 
            .if (Condition) { Commands } .elsif (Condition) { Commands } .else { Commands } 
            Condition   指定一个条件。如果求值为0，则作为假；否则为真。
                        把Condition用圆括号括起来是可选的。
                        Condition必须是一个表达式而不是调试器命令。
            Commands    指定用于条件执行的一条或多条命令。
                        该命令块必须用大括号括起来，即使只有一条命令。
                        多条命令需要用分号分隔，
                        反的大括号前面的最后一条指令后面必须(?)要跟分号。
        .foreach 
            跟批处理的for类似：分析InCommands的输出,并将该输出中各个值依次作为OutCommands的输入。
            .foreach [Options] ( Variable  { InCommands } ) { OutCommands } 
            .foreach [Options] /s ( Variable  "InString" ) { OutCommands } 
            .foreach [Options] /f ( Variable  "InFile" ) { OutCommands } 
            Options 可以是下面选项的任意组合：
                /pS InitialSkipNumber 使得开头的一些符号被跳过。
                    InitialSkipNumber 指定不传递给OutCommands 的输出关键字的数量。
                /ps SkipNumber  每次执行命令时都会跳过一些符号。
                    每次将符号传递给OutCommands 之后，SkipNumber 个数的符号都会被忽略。
                foreach /pS 2 /ps 4 /f ( place "g:\myfile.txt") { dds place }
                    过myfile.txt 文件中的前两个标记，并将第三个传递给dds
                    每传递了一个标记之后，都会跳过后续的四个标记
            Variable 指定一个变量名。
                     该变量用来保存InCommands 字符串中的每次输出，
                     因此传递给OutCommands 的参数中可以通过名字引用Variable 。
                     可以使用任何字母数字的字符串，
                     但是并不建议使用可以当作有效的16进制数字或调试器命令的字符串。
                     如果Variable 使用的名字碰巧和已存在的全局变量、局部变量或别名相同，
                     它们的值不会受.foreach 命令的影响。
            InCommands  指定要解析输出的一个或多个命令；
                        结果会传递给OutCommands 。InCommands 的输出不会显示出来。
            InString  和/s 一起使用。指定一个要解析的字符串；结果会传递给OutCommands。
            InFile    和/f 一起使用。指定要解析的文本文件；结果会传递给OutCommands 。
                      文件名InFile 必须用引号括起来。
            OutCommands 指定每条标记(token)要执行的一个或多个命令。
                        任何时候Variable 都会被替换为当前标记。
            注意 当Variable出现在OutCommands 中时，必须前后带有空格。
            如果有其它任何文本相邻 — 即使是一个圆括号 — 就不会被当前标记替换，
            除非使用${ }  (Alias Interpreter)关键字。
            当InCommands 的输出、InString 字符串或InFile 被解析时，
            任何数量的空格、tab符或回车都将会被当作单个分隔符。
            文本被分隔成的小片段被用来替换OutCommands 中的Variable 。
        .for
            .for (InitialCommand ; Condition ; IncrementCommands) { Commands } 
             Condition 是可选的。Condition 必须是一个表达式，而不是一个调试器命令
             IncrementCommands 指定一条或多条命令，在单次循环结束时执行。
               如果想要执行多条增量命令，需要用分号把它们隔开，不需要用花括号括住。
               如： .for (r eax=0; @eax < 7; reax=eax+1; rebx=ebx+1) { .... }
             Commands 多个命令间用分号隔开，结束花括号前的最后一条命令不需要带分号。
             如果在增量命令中就可以做完所有工作，
             你完全可以忽略 Commands 部分，简单的使用一对花括号就行。
        .while
            .while (Condition) { Commands } 
        .do
            .do { Commands } (Condition)
        .break
            .break 关键字的行为和 C 语言中 break 关键字一样。
        .continue
            .continue 关键字的行为和 C 语言中的 continue 关键字一样。
        .catch
            .catch 关键字通常用来避免错误发生时程序被中止。
            Commands ; .catch { Commands } ; Commands 
            .catch 关键字后面跟由大括号括住的一条或多条命令。
            如果 .catch 块中某条命令发生错误，则显示错误消息，
            忽略该块中剩下的命令，从大括号后面的第一条命令恢复执行。
            如果没有使用 .catch，一个错误将会中止整个调试器命令程序的执行。
            你可以使用.leave从一个 .catch 块中跳出来。.
        .printf
            和C语言中的printf类似。
            .printf "FormatString" [Arguments ...] 
            FormatString
                指定printf中的格式化字符串。一般来说，转义字符和C中完全一样。
                对于浮点转义字符，如果没有使用l 修饰符，64位参数会被当作32位浮点数。
                支持下面这些转义字符：
                %p	    ULONG64	目标的虚拟地址空间中的指针	
                        输出结果：指针的值
                %N	    DWORD_PTR (32位或64位，由主控机的架构决定。)	目标的虚拟地址空间中的指针	
                        输出结果：指针的值。(和标准C的%p字符一样。)
                %I	    ULONG64	任何64位值	
                        输出结果：指定的值。如果大于0xFFFFFFFF作为64位地址显示，否则作为32位地址显示。
                %ma	    ULONG64	目标虚拟地址空间中以NULL结尾的ASCII字符串地址。	
                        输出结果：指定的字符串。
                %mu	    ULONG64	目标虚拟地址空间中以NULL结尾的Unicode字符串地址。	
                        输出结果：指定的字符串。
                %msa	ULONG64	目标虚拟地址空间中的ANSI_STRING结构地址。	
                        输出结果：指定的字符串。
                %msu	ULONG64	目标虚拟地址空间中的UNICODE_STRING结构地址。	
                        输出结果：指定的字符串。
                %y	    ULONG64	目标虚拟地址空间中的调试器符号的地址。	
                        输出结果：包含指定符号的名字的字符串(和偏移量(displacement)，如果有的话)。
                %ly	    ULONG64	目标虚拟地址空间中的调试器符号的地址。	
                        输出结果：包含指定符号的名字的字符串(和偏移量(displacement)，如果有的话)，和任何可用的源码行信息。
    语句块：
        可以用大括号( { } )将大的命令块中的声明块括起来
        输入每个块的时候，块中的所有别名都会被解析。
        如果改变了命令块中别名的值，则只在本块及子块中有效。
        不能用一对大括号来创建块。必须在{之前加上流程控制符。
        如果要创建只用来展开别名的块，应该在 { 之前使用.block标记。
    调试器命令程序可以使用自定义别名和固定别名作为它的本地变量。
    如果要使用数值或类型变量，可以使用$tn 伪寄存器。
    使用注释：
        使用双美元符号 ($$  (Comment Specifier))来为调试器命令程序添加注释。
        如果要在其它命令后创建一条注释，必须在$$之前添加一个分号
        $$ 关键字使得后面的文本被忽略掉，直到行末或者碰到分号。
        如果命令开头带星号( * )字符，则行中剩下的部分被当成注释，即使中间有分号
使用外壳命令：
    任何Windows 调试器中都可以使用.shell (Command Shell)命令。
    该命令可以从调试器直接执行应用程序或者Microsoft MS-DOS命令。
    如果在进行远程调试，则这些外壳命令在服务端上运行
    .noshell (Prohibit Shell Commands) 命令或-noshell 命令行选项可以禁用所有外壳命令
    即使开始了一个新的调试会话，调试器运行时命外壳令还是被禁用。
伪寄存器：
    许多寄存器的名字取决于处理器的架构, 
    因此对于那些偶尔使用调试器的用户来说很难记住所有平台上的寄存器名字. 
    为了克服这个问题, 调试器的开发团队引入了各种伪寄存器(Pseudo-Register), 
    由调试器将这些伪寄存器对应到不同的硬件架构上
    调试器支持许多具有特定值的伪寄存器
    所有伪寄存器都以一个美元标记（$）打头。
    如果你使用 MASM 语法，你可以在 $ 标记前加一个 at 标记（@）。
    这告诉调试器紧接着的记号是一个寄存器或者伪寄存器，不是一个符号。
    如果省略 @ 标记，调试器反映会慢一点，因为它要搜索整个符号表。
    如果有一个实际的符号和伪寄存器名字相同，则 @ 标记是必须的。
    如果你使用 C++ 表达式语法，则 @ 标记始终是必须的。
    r (Registers)命令是一个例外。
        r (Registers)命令介绍
            用户模式 
                [~Thread] r[M Mask|F|X|?] [ Register[:[Num]Type] [= [Value]] ] 
                r.
            内核模式
                [Processor] r[M Mask|F|X|?] [ Register[:[Num]Type] [= [Value]] ] 
                r.
            Processor  指定要读取寄存器的处理器。默认值为0。
                如果指定了Processor，则不能包含Register 参数 — 所有寄存器都会被显示出来。
                该语法的更多信息，查看多多处理器语法。
                只能在内核模式下指定处理器。
            Thread  指定要读取寄存器的线程。如果没有指定线程，则读取当前线程。
                该语法的更多信息，查看线程语法。
                仅能在用户模式下指定线程。
            M Mask  指定调试器显示寄存器时使用的掩码(mask)。
                "M"必须是大写字母。Mask 是一个对寄存器显示进行一些设置的位的集合。
                每一位的意义由处理器和模式决定(查看下面注释中的表格获取更多信息)。
                如果省略掉M，则使用默认的掩码。
                可以使用Rm (Register Mask)命令来设置或显示默认掩码。
            F  显示浮点数寄存器。"F"必须是大写字母。该选项和M 0x4效果一样。
            X  显示SSE MMX寄存器。"X"必须是大写字母。该选项相当于M 0x40。
            ?  (仅在指派伪寄存器时) 使得伪寄存器获得类型信息。可以使用任何类型。
                r? 语法的更多信息，查看调试器命令程序示例。
            Register  指定要显示或修改的寄存器、标志位、伪寄存器或预定义别名。
                该参数前面不能加上at符号(@)。语法的更多信息，查看寄存器语法。
            Num  指定要显示的成员个数。
                如果省略该参数并且包含Type，则显示完整的寄存器长度。
            Type  指定每个寄存器成员要显示的数据格式。
                Type 只能和64位或128位向量寄存器(vector register)一起使用。
                类型	显示格式
                ib	    Signed byte
                ub	    Unsigned byte
                iw	    Signed word
                uw	    Unsigned word
                id	    Signed DWORD
                ud	    Unsigned DWORD
                iq	    Signed quad-word
                uq	    Unsigned quad-word
                f	    32位浮点数
                d	    64位浮点数
            Value  指定要指派给寄存器的值。该语法的更多信息，查看数值表达式语法。
            . 显示当前指令所使用到的寄存器。如果不使用寄存器，则不会有输出。
        它的第一个参数总是被解释为寄存器或者伪寄存器；
        @ 标记不是必须的，有也是允许的。
        如果有第二个参数，会根据缺省的表达式语法来解释。
        所以，如果缺省的表达式语法是 C++，
        你应该采用下面的命令把 $t2 伪寄存器的值复制给 $t1 伪寄存器。
        0:000> r $t1 = @$t2
    自动伪寄存器
        自动伪寄存器被调试器设置为特定的有用值
        $ea	        最后一条被执行指令的有效地址（effective address）。
                    如果这条指令没有一个有效地址，将显示"Bad register error"。
                    如果这条指令有两个有效地址，则显示第一个地址。
        $ea2	    最后一条被执行指令的第二个有效地址，
                    如果这条指令没有两个有效地址，将显示"Bad register error"。
        $exp	    最后一个被求值的表达式。
        $ra	        当前堆栈的返回地址。
                    这个在执行命令中特别有用。
                    例如，g @$ra 将一直执行到返回地址处
                    （虽然，对于“步出(stepping out)”当前函数gu (Go Up)是一个更加准备有效的方法）。
        $ip	        指令指针寄存器：
                    x86     处理器：和 eip 相同
                    Itanium 处理器：涉及 iip（请看表后的注解）
                    x64处理器：和rip相同
        $eventip	当前事件发生时的指令指针，通常和 $ip 匹配，
                    除非你切换了线程或者手动改变了指令指针的值。
        $previp	    前一个事件发生时的指令指针。（中断进入调试器算做一个事件。）
        $relip	    和当前事件相关的指令指针，当你正在跟踪分支指令时，这个是分支来源指针。
        $scopeip	当前局部上下文(也称为作用域)的指令指针。
        $exentry	当前进程的第一个可执行的入口点地址。
        $retreg	    主要的返回值寄存器：
                    x86 处理器：和 eax 相同
                    Itanium 处理器：和 ret0 相同
                    x64 处理器：和 rax 相同
        $retreg64	主要的返回值寄存器，以64位格式。
                    x86处理器：和edx:eax 相同
        $csp	    当前调用堆栈指针，是一个通常表示调用堆栈深度的寄存器。
                    x86 处理器：和 esp 相同
                    Itanium 处理器：和 bsp 相同
                    x64 处理器：和 rsp 相同
        $p	        最后一条 d* (Display Memory)命令打印的值。
        $proc	    当前进程的地址（换句话说，就是 EPROCESS 块的地址）。
        $thread	    当前线程的地址（换句话说，就是 ETHREAD 块的地址）。
        $peb	    当前进程的进程环境块（PEB）的地址。
        $teb	    当前线程的线程环境块（TEB）的地址。
        $tpid	    当前线程所在进程的进程 ID（PID）。
        $tid	    当前线程的线程 ID。
        $bpNumber	对应断点的地址。例如，$bp3（或者 $bp03）引用断点 ID 为 3 的断点。
                    Number 总是一个十进制数，如果没有哪个断点的 ID 为 Number，则 $bpNumber 求值为 0
        $frame	    当前帧索引，这个和.frame (Set Local Context) 命令常用的 frame number 相同。
        $dbgtime	当前时间，根据调试器运行的计算机。
        $callret	被.call (Call Function)命令调用的或者被.fnret /s命令使用的最后函数得到的返回值，
                    $callret 的数据类型就是返回值的数据类型。
        $lastclrex	仅托管代码调试： 最近一次遇到的公共语言运行时(CLR)异常对象的地址。
        $ptrsize	指针大小。在内核模式下，指目标计算机上的指针大小。
        $pagesize	一个内存页的大小（也就是占用的字节数目），在内核模式下，指目标计算机上的页大小。
        注意：在某些调试情景下这些伪寄存器有一部分是不可用的
        你可以用 r 命令改变 $ip 的值，它会自动修改对应的寄存器值。
            当恢复执行时，会恢复到新的指令指针地址处执行。
            这是唯一一个可以手动修改的自动变化伪寄存器。
         MASM 语法中，$ip 伪寄存器也可以用单个点号（.）表示。
            这个点号前面不需要跟一个 @ 标记，不能做为 r 命令的第一个参数。
            在 C++ 表达式中不允许使用该语法。
        除了自动别名可以使用别名相关的记号如 ${ }，而伪寄存器不能使用之外，自动伪寄存器与自动别名相似。
    自定义伪寄存器
        自定义伪寄存器是能够被调试器操作码（operator）读写的整型变量。
        有二十个自定义伪寄存器：$t0, $t1, ..., $t19。
        它们是可以通过调试器读写的变量。能用来保存任意整数值。做为循环变量时非常有用。
        要赋值给伪寄存器，使用r (Registers)命令：
            0:000> r $t0 = 7
            0:000> r $t1 = 128*poi(MyVar)
        和所有伪寄存器一样，自定义伪寄存器可以在任意表达式中使用：
            0:000> bp $t3 
            0:000> bp @$t4 
            0:000> ?? @$t1 + 4*@$t2 
使用日志文件：
    调试器可以为调试会话记录日志文件。
    这些日志包括调试器命令窗口中所有内容，包含输入的命令和调试器的输出。
    用下面的方法之一来打开新的日志文件或覆盖掉旧的日志文件
        (仅CDB 和KD) 启动调试器之前，设置_NT_DEBUG_LOG_FILE_OPEN 环境变量。
        (仅WinDbg)使用Edit | Open/Close Log File菜单命令。
        启动调试器时，使用-logo 命令行选项。
        使用.logopen (Open Log File) 命令。
            如果指定了/t选项，则会在指定的文件名后面加上日期和时间。
            如果指定/u选项，日志文件会用Unicode记录而不是ASCII。
    使用下面的方法之一来将命令窗口文本添加到日志文件末尾：
        (仅CDB 和KD) 启动调试器之前，设置_NT_DEBUG_LOG_FILE_APPEND 环境变量。
        仅WinDbg) 使用Edit | Open/Close Log File菜单命令，然后选择Append。
        启动调试器时，使用-loga 命令行选项。
        使用.logappend (Append Log File)命令。
            如果添加到Unicode日志文件，必须使用/u选项。
    使用下面方法之一来关闭打开的日志文件：
        使用 .logclose (Close Log File)命令。
        (仅WinDbg) 使用 Edit | Open/Close Log File菜单命令
    用下面的方法之一检查日志文件状态：
        使用.logfile (Display Log File Status) 命令。
        (仅WinDbg) 打开 Edit | Open/Close Log File菜单并查看是否日志文件被列出
设置路径和加载文件
    可执行映像路径
        模块一般指二进制可执行文件，但说模块名时，通常不包含可执行文件的后缀名
        大多数情况下调试器都知道可执行文件的位置，所以不需要指定该路径。
        但是，有时候这个路径是需要的。如调试非本机的dump文件时。
        调试器的可执行映像路径由多个由分号分割的目录路径组成。
        调试器会递归搜索可执行映像路径。即调试器会搜索路径列表中的目录的所有子目录。
        可以通过如下方法之一来设置可执行映像路径：
            1.启动调试器之前，使用_NT_EXECUTABLE_IMAGE_PATH 环境变量设置路径。
            2.启动调试器时，使用-i 命令行选项设置路径。
            3.用 .exepath命令显示、设置、修改或添加路径。
                .exepath[+] [Directory [; ...]] 
                + 指示调试器将新的目录添加到可执行文件搜索路径末尾 (而不是替换该路径)。
                Directory  指定要加入搜索路径的一个或多个目录。
                如果不指定Directory，则显示当前搜索路径。
                可以使用分号分隔多个目录。
            4.(仅WinDbg) 使用File | Image File Path命令或按下CTRL+I来显示、设置、修改或添加路径。
    符号路径
        符号路径指定符号文件所在的目录。
        一些编译器(例如VS)将符号文件和二进制文件放到同一个目录中
        如果本机调试，调试器能自动找到符号文件，其他情况则需设置符号路径
        调试器的符号路径由多个由分号分割的目录路径组成
        路径查找规则：
            例如设置查找路径=C:/tmp，则调试器会找：
            C:/tmp/symbols/dll; C:/tmp/dll; C:/tmp; 这三个地方
            由于符号文件有时间戳，所以不用担心调试器会找错
        延迟符号加载
            调试器默认延迟符号加载，当用到时才加载；
            当符号路径改变时，所以已加载的符号会重新加载;
            可以在CDB和KD中使用-s 命令行选项关闭延迟符号加载
            可以使用ld (Load Symbols) 命令强制加载符号
                ld ModuleName [/f FileName]
                ModuleName  指定要加载符号的模块名。
                    ModuleName 可以包含各种通配符和修饰符。
                /f FileName 改变选择用来匹配的名称。
                    默认情况下使用模块名来匹配，
                    但是当使用/f时，使用文件名来匹配而不是模块名。
                    FileName 可以包含各种通配符合修饰符。
            也可以使用.reload (Reload Module)和/f选项强制加载符号
                .reload [Options] [Module [= Address [, Size [, Timestamp] ] ] ] 
                Options
                    /d      重新加载调试器模块列表中的所有模块。
                            (省略所有参数时，这是用户模式调试下的默认行为。)
                    /f      强制调试器立即加载符号。
                            该参数会覆盖延迟符号加载。更多信息，查看下面的注释节。
                    /i      忽略.pdb文件版本不匹配的情况。
                            (如果没有包含该参数，调试器不会加载不匹配的符号文件。) 
                            使用 /i时，即使没有明确指定，也会使用/f。
                    /l      列出模块但是不重加载它们的符号。
                            (内核模式下，使用该参数的输出和!drivers 扩展命令一样。)
                    /n      仅重加载内核符号。该参数不会重加载任何用户模式符号。
                            (只能在内核模式调试时使用该选项。)
                    /o      强制覆盖符号服务器的下游存储(downstream store)中的缓存文件。
                            使用该标志时，还需要包含/f。默认情况下，下游存储中的文件永远不会被覆盖。
                            由于符号服务器对每个版本的二进制文件的符号使用不同的名字，
                            除非确认下游存储被破坏了，否则不需要使用该选项。
                    /s      重新加载系统的模块映像列表中所有模块。
                            (省略所有参数时，在内核模式下这是默认行为。) 
                            如果在用户模式调试时使用名字来单独加载某个系统模块，则必须包含/s。
                    /u      卸载指定模块和它的所有符号。
                            调试器卸载任何名字匹配Module 的模块，不管它的全路径是什么。
                            映像名也会被搜索。更多信息，查看下面的注释节。
                    /unl    基于已卸载模块列表中的映像信息重新加载符号。
                    /user   仅重加载用户模式符号。(只能在内核模式调试时使用该选项。)
                    /v      打开详细显示。
                    /w      将Module 当作一个字面上的字符串。这样可以避免调试器展开通配符。
                Module  指定主控机要重加载符号的目标机上的映像名。
                    Module 需要包含文件的名字和扩展名。
                    如果没有使用/w 选项，Module 可以包含各种通配符和修饰符。
                    如果省略Module，.reload 命令的行为由使用的Options 决定。
                Address 指定模块的基地址。
                    一般来说只有在映像头被破坏或者页换出时才需要该地址。
                Size    指定模块映像的大小。
                    很多情况下，调试器会知道模块的正确大小。
                    当调试器不知道正确大小时，就需要指定Size。
                    该大小可以是实际的模块大小或者更大的数字，但是不能更小。
                    一般来说，只有在映像头被破坏或者页换出时才需要该大小。
                Timestamp  指定模块映像的时间戳。
                    很多情况下，调试器会知道模块的正确时间戳。
                    当调试器不知道正确的时间戳时，就需要指定Timestamp
                    一般来说，只有在映像头被破坏或者页换出时才需要指定。
                -?  显示这个命令的简短帮助文本。
    源码路径
        如果调试本机程序，可以不指定源码路径
        如果使用WinDbg作为调试器，每个调试客户端都有它自己的本地源码路径。
        调试器的源码路径由多个由分号分割的目录路径组成
        设置源码路径
            启动调试器之前，通过_NT_SOURCE_PATH 环境变量设置源码路径。
            启动调试器时，使用-srcpath命令行选项设置源码路径。
            用 .srcpath(Set Source Path)命令显示、设置、修改或添加源码路径。
                .srcpath[+] [Directory [; ...]] 
                +  指定要添加(而不是替代)到当前的源文件搜索路径后面的目录。
                Directory   指定要放入搜索路径中的一个或多个目录。
                如果没有指定Directory，则显示当前路径。可以用分号分隔多个目录。
            (仅WinDbg) 使用File | Source File Path命令或按下CTRL+P
                来显示、设置、修改或添加源码路径或本地源码路径。
        直接打开或关闭源码文件
            使用lsf (Load or Unload Source File)命令来打开或关闭源码文件。
            (仅WinDbg) 使用.open (Open Source File) 命令来打开源码文件
            仅WinDbg) 用File | Open Source File命令或按下CTRL+O来打开源码文件。
                也可以使用工具栏上的Open source file (Ctrl+O) 按钮
                当使用File | Open Source File (或者使用相同功能的快捷菜单和按钮) 
                来打开源码文件时，该文件的路径会自动添加到源码路径中。
            (仅WinDbg) 使用File | Recent Files命令来打开WinDbg最近打开过的4个文件之一。
            (仅WinDbg) 用File | Close Current Window命令或点击源码窗口角上的Close按钮来关闭一个源码文件。
    使用符号服务器 略
    使用源码服务器 略
调试器操作
    常规
        控制目标的运行与停止
            当调试器连接到内核模式的目标时，
                调试器会继续让目标运行（除非使用了-b命令行选项）
            当调试器启动或连接到一个用户模式目标时，
                会立即中断目标的执行，除非使用-g 命令行选项
            运行中的目标
                当目标正在运行时，大多数调试操作都不可用。
                如果要停止运行中的目标，可以输入中断(Break)命令
                该命令使得调试器中断到目标中，
                调试器停止目标，并获得所有控制权，应用程序可能不会立即中断下来
                    例如，如果所有线程当前正在执行系统代码，或者在等待操作，
                    中断会延迟到控制返回应用程序代码时发生。
                如果运行中的目标发生异常、特定事件发生、遇到断点或程序正常关闭，
                目标会中断到调试器。
            控制程序的执行：
                使用运行(Go)命令使得程序开始运行。
                一次单步执行一条指令，使用单步进入或单步步过命令。
                结束当前函数的执行并在返回时中断，
                    使用执行到返回(Step Out)或 or 跟踪和监视(Trace and Watch)命令。
                    Step Out命令继续程序执行直到当前函数结束。
                    Trace and Watch 继续执行直到当前函数结束，并显示函数调用的摘要信息。
                如果有异常发生，可以使用处理异常并运行(Go with Exception Handled)
                和不处理异常并运行(Go with Exception Not Handled)命令来恢复执行和控制异常状态。
                (仅WinDbg) 如果在反汇编窗口(Disassembly window)或 源码窗口(Source window )选中一行，
                    然后使用运行到光标(Run to Cursor)命令，程序会一直运行直到遇到选中那一行。
                (仅User Mode) 关闭目标程序并重新开始运行它，可以使用重新开始(Restart)命令。
                    该命令只能用于调试器创建的进程。进程重起之后，会立即中断到调试器。
                (仅WinDbg) 使用停止调试(Stop Debugging)命令关闭目标程序并清空调试器。
                    该命令使得可以开始调试另一个目标。
            命令窗体
                无                                      Debug | Stop Debugging	        SHIFT + F5	        停止所有的调试并关闭目标。
                无                                      Debug | Run to Cursor	        F7 或 CTRL + F10	(仅WinDbg)?运行到光标位置。
                g (Go)	                                Debug | Go	                    F5	                目标自由执行。
                (仅CDB/KD)?CTRL+C	                    Debug | Break	                CTRL + BREAK	    停止执行，调试器中断目标。
                .restart (Restart Target Application)	Debug | Restart	                CTRL + SHIFT + F5	(仅User mode)?重起目标程序。
                gu (Go Up)	                            Debug | Step Out	            SHIFT + F11	        目标运行到当前函数执行完成。
                p (Step)	                            Debug | Step Over	            F10	                目标执行一条指令。
                                                                                                            如果该指令是函数调用，则这个调用被当作一步执行。
                t (Trace)	                            Debug | Step Into	            F11 或 F8	        目标执行一条指令。
                                                                                                            如果该指令是一条call，调试器跟踪到这个call中。
                gh (Go with Exception Handled)	        Debug | Go Handled Exception	和g (Go)相同，但是当前异常被当作已处理。
                gn (Go with Exception Not Handled)	    Debug | Go Unhandled Exception	和g (Go)相同，但是当前异常被当作未处理。
                gc (Go from Conditional Breakpoint)		在一次条件断点之后恢复执行。
                pt (Step to Next Return)			    目标执行，直到遇到return指令。
                wt (Trace and Watch Data)			    目标执行，直到指定的函数执行完成。
                pct (Step to Next Call or Return)		目标继续执行，直到遇到一个call指令或者return指令。
                ta (Trace to Address)			        目标执行直到指定地址。本函数和被调用函数中的每一步都会显示出来。
                tb (Trace to Next Branch)			    (除内核模式之外的所有模式，仅在基于x86的系统上)?目标运行到下一条分支指令。
                tc (Trace to Next Call)			        目标运行到下一条call指令。
                                                        如果当前指令是call，该命令会跟踪进去直到遇到另一条call。
                tt (Trace to Next Return)			    目标运行直到遇到return指令。
                                                        如果当前指令是一条return，则跟踪进入直到另外一条return。
                ph (Step to Next Branching Instruction)	目标执行，直到到达任何一种分支指令，
                                                        包括条件和非条件分支、call调用、函数返回和系统调用。
                pc (Step to Next Call)			        目标运行直到遇到下一个call指令。
                                                        如果当前指令是call，则这个call会被完成并执行到下一个call。
                pa (Step to Address)			        目标运行直到到达指定的地址。
                                                        该函数中执行的每一步都会显示出来(但是不显示被调用的函数中的内容。)
                tct (Trace to Next Call or Return)		目标运行到下一条call指令或return指令。
                                                        如果当前指令是call或return，命令会跟踪进去知道遇到另一个call或return。
                th (Trace to Next Branching Instruction)目标执行直到遇到任意类型的分支指令，包括条件和非条件跳转、call、return和系统调用。
                                                        如果当前指令是分支指令，该命令跟踪进入直到遇到下一个分支指令。
        使用断点
            可以通过指定虚拟地址、模块和函数偏移或源码文件和行号来设置断点(当在源码模式中时)。
            如果在某个例程上设置断点并且没有使用偏移，则当运行到这个例程上时就会触发断点。
            如果在用户模式下调试多于一个进程，每个进程都有它自己的断点集合。
            要查看或修改某个进程的断点，必须将该进程设置为当前进程。
            管理断点：
                bl (Breakpoint List)命令列出当前存在的断点和他们的状态。
                bp (Set Breakpoint) 命令设置新断点。
                bu (Set Unresolved Breakpoint) 命令设置新断点。
                bm (Set Symbol Breakpoint) 在匹配指定格式的符号上设置断点。
                ba (Break on Access) 命令设置数据断点。这种断点在指定内存被访问时触发。
                    (可以在写入、读取、执行或发生内核I/O时触发，但不是所有处理器都支持所有的内存访问断点)
                bc (Breakpoint Clear) 命令移除一个或多个断点。
                bd (Breakpoint Disable) 命令暂时禁用一个或多个断点。
                be (Breakpoint Enable) 命令重新启用一个或多个断点。
                br (Breakpoint Renumber) 命令修改一个已存在的断点的ID。
                bs (Update Breakpoint Command) 命令用于更改已存在的断点所关联的命令。
                bsc (Update Conditional Breakpoint) 命令用于更改已存在的断点的触发条件。
                (仅WinDbg) 反汇编窗口(Disassembly window) 和 源码窗口(Source windows) 会将设置了断点的行高亮。
                    已启用的断点为红色，禁用的断点为黄色，如果当前程序计数器(EIP)位置是断点位置则显示为紫色。
                (仅WinDbg) Edit | Breakpoints 命令或ALT+F9快捷键打开Breakpoints对话框。
                    该对话框会列出所有断点，所以可以用它来禁用、启用、删除已存在的断点或设置新断点。
                (仅WinDbg) 如果光标在反汇编窗口或源码窗口中，可以按下F9
                    或点击工具栏上的Insert or remove 按钮 () 来在光标所在行上设置断点。
                    如果在当前窗口不是反汇编窗口或源码窗口时按下快捷键或点击上述按钮，
                    则和使用Edit | Breakpoints具有相同效果。
            每个断点都有一个关联的10进制数字称为断点ID。该数字在各种命令中用于指定断点。
            断点类型简介
                BU 和 BP
                    如果一个断点是设置在某个还未加载的函数名上，则称为延迟、虚拟或未定断点。
                    未定断点没有被关联到任何具体被加载的模块上。
                    每当一个新的模块被加载时，会检查该函数名。如果这个函数出现，调试器计算虚拟断点的实际位置并启用它。
                    使用bu设置的断点自动被认为是未定断点。如果断点在一个已加载模块中，则会启用并正常生效。
                    但是，如果模块之后被卸载并重新加载，这个断点不会消失。
                    而使用bp设置的断点会立即绑定到某个地址。
                    bp和bu断点有以下三个主要的不同点：
                        1. bp 断点的位置总是被转换成地址。
                        如果某个模块改变了，并且bp设置的地址位置改变，断点还是在原来的位置。
                        而bu断点仍然和使用的符号值关联(一般是符号加上偏移)，
                        它会一直跟踪符号的地址，即使这个地址已经改变。
                        2. 如果bp的断点地址在某个已加载模块中找到，并且该模块之后被卸载，则该断点会从断点列表中移除。
                        而bu断点经过反复的卸载和加载仍然存在。
                        3. 用bp设置的断点不会保存到WinDbg 工作空间(workspaces)中，而使用bu设置的断点会保存。
                        当在WinDbg 反汇编窗口或源码窗口中使用鼠标设置断点时，调试器创建的是bu断点。
                初始断点
                    当调试器启动一个新的目标程序时，
                    初始断点在主映像和所有静态加载的DLL被加载、DLL初始化例程被调用之前自动触发。
                    调试器附加到一个已存在的用户模式程序时，初始断点立即触发
                    -g 命令行选项使得WinDbg或CDB跳过初始断点。在这时可以自动执行命令。
                    如果想启动新调试目标并在实际的程序即将开始执行的时候中断下来，就不要使用-g选项。
                    当调试器激活之后，在main或winmai函数上设置断点并使用g (Go) 命令。
                    之后所有初始化过程都会运行并且程序在main函数即将执行时停止。
            断点的地址：
                断点支持几种地址语法，包括虚拟地址、函数偏移和源码行号。
                例如，可以使用下面的方法之一来设置断点：
                0:000> bp 0040108c
                0:000> bp main+5c
                0:000> bp `source.c:31`
                关于这些语法的更多信息，查看数值表达式语法， 源代码行语法
                源代码行语法：
                    源文件行数值可以做为 MASM 表达式的一部分使用。
                    它们计算出对应源码行的可执行代码偏移值。
                    注解 源代码行数值不能做为 C++ 表达式的一部分使用。
                    源文件和行数表达式需要用重音符号（`）括住。完整的源码行号的格式如下：
                    `[[Module!]Filename][:LineNumber]`
                    如果你有多个文件同名，Filename 应该包含完整的路径和文件名。路径使用编译时的路径。
                    如果你仅提供文件名或者一部分路径，而且有多个匹配项，调试器将使用第一个找到的匹配项。
                    如果省略Filename，调试器假定使用对应当前程序计数器（program counter）对应的源文件。
                    不管当前的缺省基数是多少，除非带有 0x 前缀，否则 LineNumber 将被读作十进制数值。
                    如果省略 LineNumber，表达式将被计算为对应源文件的起始可执行地址。
                    在 CDB 中不会计算源码行表达式，除非使用了.lines (Toggle Source Line Support)命令
                    或者调试器带有-lines 命令行选项启动
            方法的断点
                如果要在MyClass类的MyMethod方法上设置断点，可以使用两种不同语法：
                用MASM表达式语法，可以用双冒号或者双下划线来指定一个方法。
                0:000> bp MyClass::MyMethod 
                0:000> bp MyClass__MyMethod 
                用C++表达式语法，必须用双冒号指定方法。
                0:000> bp @@( MyClass::MyMethod ) 
            复杂文本的断点
                @!""语法用于在MASM求值器中进行转义，使得符号解析支持任意文本。
                必须以@!"开始并以引号(")结束。
                如果不使用该语法，则在MASM表达式的符号名中不能使用空格、大于小于号(<, >)和其他特殊字符。
                该语法只能用于名字，不能用于参数。
                模板和重载是符号中需要这种引号的主要原因。
                举例：
                   bu @!"ExecutableName!std::pair<
                            unsigned int,
                            std::basic_string<
                                unsigned short,
                                std::char_traits<unsigned short>,
                                std::allocator<unsigned short> 
                            > 
                        >::operator="
                   ExecutableName 是一个可执行文件的名字。
                   注释连续的两个简括要，应该用空格隔开
            断点的数量
                在内核模式下，最多可以使用32个断点。在用户模式下，可以使用任意数量的断点。
                数据断点的数量由目标处理器架构决定
            断点伪寄存器    
                如果在某个表达式中想引用某个断点的地址，
                可以使用一个$bpNumber 语法的伪寄存器，Number是断点ID。
            可动态变化的断点
                使用下面的语法来表明表达式需要被解释成断点。
                b?[Expression]
                这个语法中，必须使用中括号，Expression是任何想要被当作断点ID的值为整数的数值表达式。
                b?[@$t0]  //断点会根据自定义伪寄存器的值的不同而变化
            断点命令
                所谓断点命令，就是可以设置在断点触发时，自动执行的语句
                方法就是在设置断点的命令后面跟上命令字符串，如：
                bu MyFunction+0x47 ".dump c:\mydump.dmp; g" 
            条件断点
                条件断点其实就是断点命令的特殊使用
                当断点触发时，在断点命令中，判断是否符合条件，如果不符合，就继续执行
                判断是否满足条件，可以使用 j命令，也可以使用.if命令，如
                bp Address "j (Condition) 'OptionalCommands'; 'gc' "
                bp Address ".if (Condition) {OptionalCommands} .else {gc}"
        读写内存
            显示内存数据
                d{a|b|c|d|D|f|p|q|u|w|W} [Options] [Range] 
                    da  ASCII 字符。每行最多48个字符
                    db  字节值和ASCII字符。
                        每个显示行都包含该行第一个字节的地址，后面跟16进制字节值。
                        这些字节值后面会紧跟它们对应的ASCII值
                    dw  WORD值(2字节)。
                    dW  WORD值(2字节)和ASCII字符。
                    dc  双字值(4字节)和ASCII字符
                    dd  双字值(4字节)
                    dq  四字值(Quad-word values) (8 bytes)。
                    df  单精度浮点数(4字节)
                    dD  双精度浮点数(8字节)
                    dp  指针大小的值。该命令根据目标机的处理器是32位还是64位的，分别等于dd 或dq。
                    du  Unicode字符 。
                dy{b|d} [Options] [Range] 
                    dyb 二进制值和字节的值
                    dyd 二进制值和双字值(4字节)。
                d [Options] [Range] 
                    d   等价于最近一次d*命令，如果之前没有使用过d*命令，和db的效果相同。
                [Options]
                    /c Width 指定要显示的列的数量。如果省略掉，默认的列数由显示类型决定。
                    /p       (仅内核模式) 使用物理内存地址进行显示。
                             Range 指定的范围将被当作物理地址而不是虚拟内存。
                    /p[c]    (仅内核模式) 除了读取高速缓冲存储器(cached memory)中的内存之外，
                             和/p一样。必须包含c两边的中括号。
                    /p[uc]   (仅内核模式) 除了读取非缓存的内存(uncached memory)之外和/p一样。
                             必须包含uc两边的中括号。
                    /p[wc]   (仅内核模式) 除了会读取写聚合内存(write-combined memory)之外，
                             和/p一样。必须包含wc两边的中括号。
                如果尝试显示一个非法地址，它的内容会显示为问号(?)
            修改内存数据
                e{b|d|D|f|p|q|w} Address [Values] 
                    eb  字节值。
                    ew  字值(2字节)。
                    ed  双字值(4字节)。
                    eq  4字值(8字节)。
                    ef  单精度浮点数(4字节)。
                    eD  双精度浮点数(8字节)。
                    ep  指针大小的值。
                        该命令根据目标机的处理器架构是32位还是64位，可能分别等于ed 或eq。
                e{a|u|za|zu} Address "String" 
                    ea  ASCII 字符串(不以NULL结尾)。
                    eu  Unicode字符串(非NULL结尾)。
                    eza NULL结尾的ASCII字符串。
                    ezu NULL结尾的Unicode字符串。
                e Address [Values] 
                    e   等价于最近一次e*命令
                        如果上一次的e*命令是ea、eza、eu或ezu，
                        则最后一个参数是String并且不能省略。
                Address 指定要改写数据的开始位置。
                        调试器替换Address 和之后的每个内存位置，直到所有的Values 都被使用到。
                Values  指定要写入内存的一个或多个值。多个数字值之间需要使用空格分隔。
                        如果不指定任何值，则显示指定位置的值，并提示输入数据。
                String  指定要写入内存的字符串。
                        ea 和eza 命令会把它作为ASCII字符串写入内存； 
                        eu 和ezu 命令会把它作为Unicode字符串写入内存。
                        eza 和ezu 命令会写入结尾的NULL字符；
                        ea 和eu 命令不会。
                        String 必须用引号括起来。
                数字值会以当前基数(16、10,或者8)进行解析。
                使用n (Set Number Base)命令来改变默认基数。
                默认基数可以通过指定0x(16进制)、0n (10进制)、0t (8进制)或0y (2进制)前缀来覆盖。
            使用内存窗口来显示或修改内存（仅windgb）
            其它访问内存的命令
                以使用? (Evaluate Expression)命令来显示和任何符号关联的地址。
        查看调用堆栈
            k  该命令显示栈帧的基指针、返回地址和函数名。
               如果有源码行号信息，k命令还会显示源码模块和行号。
            kb 显示堆栈，并且显示传递给函数的前三个参数。
            kp 和kb命令一样显示堆栈，并且显示传递给函数的完整参数列表。
            kv 和kb一样显示堆栈，并且再显示帧指针省略信息(FPO)。
               在基于x86的处理器上，该命令还显示调用约定的信息。
               在基于Itanium的处理器上，该命令显示非易失性寄存器。
            kd 显示原始堆栈信息，不按照任何格式。
            可以调用堆栈窗口(Calls window)显示调用堆栈信息(仅WinDbg)  
        结束调试会话
            退出 CDB
                q  可以使用q (Quit)命令退出CDB。该命令同时关闭被调试的程序。
                qd (Quit and Detach) 命令停止CDB对目标程序的附加，
                   退出调试器，并让目标程序继续运行(Windows XP或更高)
                如果调试器停止了响应，可以通过按下CTRL+B再按下ENTER来退出。
                   这种方法是退出的后备机制。它强制性的结束调试器，
                   类似从任务管理器结束进程或关闭窗口。 
            退出 KD
                q  保存日志文件、结束调试会话并退出调试器。目标机会保持锁定。
                按下CTRL+B之后按ENTER 来强制结束调试器。
                   如果要目标机在退出调试器之后继续运行，必须使用这种方法。
                   由于CTRL+B不删除断点，所以应该像下面一样使用。
                   kd>  bc *
                   kd>  g
                   kd>  <CTRL+B> <ENTER>
            退出WinDbg 
                可以通过在File菜单点击Exit或按下ALT+F4退出WinDbg。
                要停止用户模式调试会话将调试器返回到静止状态，并关闭目标程序:
                    .kill (Kill Process) 命令
                    q (Quit)命令 -- 当没用-pd选项启动调试器时
                    SHIFT+F5快捷键
                    菜单Debug | Stop Debugging命令
                    工具栏上的Stop debugging (Shift+F5) 按钮
                要停止用户模式调试会话，将调试器返回到静止模式，并让目标程序重新运行起来：   
                    .detach 命令。
                        .detach [ /h | /n ]
                        /h  所有未处理的调试事件都会标记为已处理并继续运行。这是默认值。
                        /n  所有未处理的调试事件都不会标记为已处理并继续运行。
                    菜单Debug | Detach Debuggee 命令
                    qd (Quit and Detach)命令。
                    q (Quit)命令 -- 当使用了-pd选项启动调试器时
    用户模式
        显示进程和线程信息
            | (Process Status)   显示进程信息
                管道(|)命令显示指定进程或当前正在调试的所有进程的信息。
                语法   ：   | Process 、 | s
                Process 指定要显示的进程。如果省略掉该参输，则显示所有进程。
                | s 显示当前进程信息
            ~ (Thread Status)    显示线程信息
                语法    ：   ~ Thread   、 ~ s
                Thread  指定要显示的线程。如果省略该参数，则显示所有线程。
                ~ s 显示当前线程的信息
            (仅WinDbg) 进程和线程窗口
        设置当前进程、线程
            |s (Set Current Process) 命令
                |Process s    Process指定要显示或设置的进程。
            ~s (Set Current Thread) 命令
            (仅WinDbg) 进程和线程窗口
        冻结和挂起线程
            挂起线程
                挂起线程的相关知识：
                    每个线程都有一个关联的挂起计数(suspend count)。
                    如果这个数字是大于等于1，则系统不会运行该线程。
                    如果计数小于等于0，系统会在适当的时机运行该线程。
                    一般来说，每个线程的挂起计数都是0。
                    当调试器附加到进程时，会将它的所有线程的挂起计数加1。
                    如果调试器停止对进程的附加，会将所有挂起计数减1。
                    当调试器执行进程时，会临时将所有的挂起计数减少1。
                ~Thread n  命令将指定线程的挂起计数加1。
                ~Thread m  命令将指定线程的挂起计数减1。
                附加说明：
                    一般用这些命令来将指定线程的挂起计数从1加到2。
                    当调试器执行或停止附加进程时，该线程由于挂起计数为1，
                    即使进程中其他线程都开始执行，该线程仍然保持挂起。
            冻结线程
                冻结相关知识
                    该行为和以某些方式挂起线程类似。
                    但是，"冻结"仅仅是一种调试器设置。
                    Windows系统不会知道该线程有任何不同点。
                    默认情况下，所有线程都是非冻结的。
                    当调试器运行进程时，被冻结的线程不会运行。
                    但是，当调试器停止对该进程的附加时，所有线程都会变为非冻结状态
                ~Thread f  命令冻结指定线程。
                ~Thread u  命令解冻指定线程
                附加说明
                    在任何情况下，当调试器中断目标时，该进程中的所有线程永远不会被执行。
                    线程的挂起计数仅在调试器运行进程或者停止进程附加时有效。
                    冻结状态仅在调试器运行进程时有效。
    内核模式  略
    使用调试器扩展命令
        加载扩展dll
            _NT_DEBUGGER_EXTENSION_PATH 环境变量
                (启动调试器之前)使用_NT_DEBUGGER_EXTENSION_PATH 环境变量
                来设置扩展DLL的默认路径。可以是用分号分割的许多目录路径。
            使用.load (Load Extension DLL) 命令加载一个新的DLL。
                .load DLLName 
                !DLLName.load 
                DLLName为完整路径名
            .unload (Unload Extension DLL)命令卸载一个DLL。
                .unload DLLName 
                !DLLName.unload 
                DLLName为完整路径名
            .unloadall  命令卸载所有调试器扩展。
            (仅CDB，启动调试器之前) 用 tools.ini 文件设置默认的扩展DLL。
            (启动调试器之前) 用 -a 命令行选项设置默认扩展DLL。
            用.extpath (Set Extension Path) 命令设置扩展DLL 搜索路径。
                .extpath[+] [Directory [; ...]] 
                +   指示调试器应该把新的目路添加到扩展DLL搜索路径末尾 (而不是替换该路径)。
                Directory  指定一个或多个要添加的搜索路径。
                    如果不指定Directory，则显示当前搜索路径。可以用分号分隔多个目录。
            .setdll (Set Default Extension DLL)命令设置默认扩展DLL。
                .setdll DLLName 
                !DLLName.setdll 
            .chain 显示所有已加载的调试器扩展模块，以他们的默认搜索顺序。
        使用扩展命令
            ![module.]extension [arguments]
            module 名字不能包含.dll扩展名。
            如果module 包含完整路径，默认的字符串尺寸限制为255。
            如果模块还没有被加载，调试器会使用LoadLibrary(module)调用来加载它。
            调试器加载了扩展库之后，会调用GetProcAddress 函数来定位扩展模块中的命令名。
            扩展命令名是大小写敏感的，并且必须和出现在扩展模块的.def 中的名字完全相同。
            如果找到了命令地址，则会调用该命令。
            搜索顺序
                如果没有指定模块名，调试器会在已加载的扩展模块中搜索。
                搜索顺序如下：
                1. 能在所有操作系统和两种调试模式中使用的扩展模块：dbghelp.dll 、winext\ext.dll。
                2. 在所有模式下可以使用，但是和特定操作系统相关的扩展模块。
                   在Windows XP和之后版本的Windows中为winxp\exts.dll。
                   Windows 2000种没有对应的模块。
                3. 可以在所有操作系统中使用，但是和调试模式相关的扩展模块。
                   内核模式下为winext\kext.dll。用户模式下为winext\uext.dll。
                4. 既和操作系统相关又和调试模式相关的扩展模块。
    远程调试  略
符号文件讲解
崩溃转储文件讲解
windbg命令分为标准命令，元命令和扩展命令。
     标准命令提供最基本的调试功能，不区分大小写。如：bp  g  dt  dv  k等
     元命令提供标准命令没有提供的功能，也内建在调试引擎中，以.开头。如.sympath  .reload等
     扩展命令用于扩展某一方面的调试功能，实现在动态加载的扩展模块中，以!开头。如!analyze等
 
  