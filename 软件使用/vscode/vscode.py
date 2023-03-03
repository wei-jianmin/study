.vscode文件夹
    存放工作区特定文件，如tasks.json 用于 Task Runner，launch.json 用于调试器

文件结构
    vscode提供三级文件结构,从工作区到文件夹到单个文件:
    文件夹是vscode配置的最小工作单元,vscode无法为单个文件提供配置。
    在不同的工作区中我们可以选择启用/禁用不同的拓展插件以节省内存
     
快捷键
    ctrl+,       ：设置面板
    ctrl+`       ：显示/隐藏终端面板
    ctrl+shift+` ：新建终端面板
    ctrl+shift+p（或F1）：命令面板
    ctrl+shift+e ：文件资源管理器面板（explorer）
    ctrl+shift+f ：跨文件搜索面板（find）
    ctrl+shift+g ：代码仓库管理面板（git）
    ctrl+shift+d ：启动和调试面板（debug）
    ctrl+shift+x ：管理扩展面板（extend）
    ctrl+shift+m ：错误和警告底部面板（message）
    你可以选择左下角的设置图标，选择弹出菜单中的“键盘快捷方式”菜单项，然后即可设置快捷键了
    你可以在插件管理器中搜索keymap，选择安装一个key映射插件，然后就可以使用预定义的快捷键

代码编辑快捷键
        ctrl+/：触发注释
        ctrl+f，弹出搜索窗口后，点击搜索窗口左侧的展开箭头，即变为替换窗口（ctrl+h）
    函数编辑：
        ctrl+空格：弹出代码补全建立列表
        ctrl+shift+space：函数参数预览
        ctrl+k,ctrl+f：选中内容智能格式化
        alt+shift+f：整个文档代码智能格式化
        F2：变量或函数名，智能重命名  
    光标与选中：
        ctrl+u：光标跳转到上次位置
        ctrl配合方向键，可以以词为单位进行移动
        ctrl+shift+\ ：跳转到匹配的括号
        alt+↑/↓ ：将光标所在行或选中行上下移动
        用鼠标单击编辑界面前面的行号，可选中改行，在行号上拖动，可选中多行        
    行操作：
        ctrl+x : 剪切行
        ctrl+shift+enter ：当前行上面添加空行
        ctrl+enter：当前行下面添加空行
        alt+shift+↑/↓ ：将光标所在行或选中行，向上或向下复制出一份        
    命令面板：
        选中多个单词，在命令面板中输入“大写”或“小写”，会有将单词转为大写/小写的命令
        使用命令面板，输入关键字：括号，使用命令“选择括号所有内容”，可选中光标所在的括号片段
    多光标编辑
        alt+鼠标点击
            按下alt，鼠标在不同位置点击，就会在这些位置都出现光标
            然后输入或修改等操作，在这些光标位置同时生效
        alt+鼠标多次选中
            同上的，配合alt间，可以用鼠标选中多个区段
        shift+alt+鼠标拖动：
            类似'alt+鼠标多次选中'的效果，区别是鼠标可以多行选中
        ctrl+d：多光标模式下，将每个光标所在的单词批量选中
        alt+shift+i ：选中多行后，按下此快捷键，则在每个被选中行后面创建一个光标
                          可以借助这个特性，批量添加/删除续行符  
    代码浏览
        当鼠标点击函数名或变量时，按住ctrl键，可跳转到定义位置
        ctrl+tab：标签页面切换
        * ctrl+p：快速打开指定文件
        * ctrl+g：跳转到行
        * ctrl+t：在所有文件中搜索符号
        * ctrl+shift+o：列出当前文件中的所有符号对象（宏、变量和函数）
        F12：在函数声明和实现之间跳转 ？
        [? shift + ] F12 ：查看函数引用
        ctrl+f 搜索，enter/shift+enter : 在搜索到的匹配项之间向下/向上跳转
        前进/后退
            linux：ctrl + alt + ‘-’、ctrl + shift + ‘-’
            windows: alt + ←、alt + →
               
代码片段（即代码模板） 
    配置代码片段
        首先，我们打开命令面板，搜索“配置用户代码片段”并且执行。
        这时候我们会看到一个列表，让我们选择语言。
        选择语言后，会出现代码片段配置文件(json，带示例)
        代码片段示例：
            "Print to console": {  //代码片段名称
                    "prefix": "log",  //代码片段快捷键，必选
                    "body": [  //代码片段内容，必选
                        "console.log('$1');", //每个json节点对应一行
                        "$2"
                        ],
                    "description": "Log output to console"  //代码片段描述，可选
                }
    使用代码片段
        当在代码编辑窗口中输入log，则上述代码片段就会出现在候选列表中
        按tab，即可将该条目插入到当前位置
        插入代码段后，代码片段中的 $1,$2等，为显示为|，代表插入位置（占位符），
        按tab键，可定位到下个插入位置（shift+tab：上个插入位置）
    占位符带默认值
        上面的$1，$2等占位符，可以带默认值，如：${1:label}
        这样，"label"字样就会出现在$1插入位置，并呈现为选中状态，
        按下tab键，代表使用该值，并将光标定位到下一插入位置
    多光标
        上面的$1、$2等，可以多次出现在一个代码片段中，
        这样插入代码片段的时候，就会呈现为多光标状态，
        当修改一处，其它同值的占位符也相应修改
        如：
            "insert for": {  //代码片段名称
                    "prefix": "for",  //代码片段快捷键，必选
                    "body": [  //代码片段内容，必选
                        "for(int ${1:i}=0; ${1:i}<$2; ${1:i}++)", 
                        "{",
                        "   $3",
                        "}"
                        ],
                    "description": "insert for template"  //代码片段描述，可选
                }
    预设变量
        我们想在代码片段里的某个位置使用剪切板的内容，
        那么我们在那个位置写上 $CLIPBOARD 就好了，
        如果我们希望插入代码片段后自己可以修改这个值，
        也可以将它放在一个 Tab Stop 里面，语法则是 ${1:$CLIPBOARD}
        vs code 支持的预设变量有：
            TM_SELECTED_TEXT
            TM_CURRENT_LINE
            TM_CURRENT_WORD
            TM_LINE_INDEX   (从0开始)
            TM_LINE_NUMBERR (从1开始)
            TM_FILENAME
            TM_FILENAME_BASE
            TM_DIRECTORY
            TM_FILEPATH
            CLIPBOARD
            CURRENT_YEAR
            CURRENT_YEAR_SHORT (只显示两位)
            CURRENT_MONTH (两位)
            CURRENT_MONTH_NAME (如"July")
            CURRENT_MONTH_NAME_SHORT (如"Jul")
            CURRENT_DATE
            CURRENT_DAY_NAME (如"Monday")
            CURRENT_DAY_NAME_SHORT (如"Mon")
            CURRENT_HOUR  (24小时制)
            CURRENT_MINUTE
            CURRENT_SECOND
        
代码折叠
    vscode 支持 region，用法
    // region xxx
    ...
    // endregion
    快捷键：
        Ctrl + K，Ctrl + 0 ： 折叠全部
        Ctrl + K，Ctrl + J ： 展开全部
        Ctrl + Shift + 左方括号 ：折叠当前层
        Ctrl + Shift + 右方括号 ：展开当前层
        Ctrl + K、Ctrl + 左方括号 ：折叠光标处所有层
        Ctrl + K、Ctrl + 右方括号 ：展开光标处所有层
        
通过命令行启动code
    -d <file> <file>: 文件比较   
    不带控制参数
        code 命令后加上文件或者文件夹的地址，
        这样VS Code 就会在一个新窗口中打开这个文件或文件夹
    -r --reuse-window ：在已存在的窗口中打开文件或文件夹
        如果你希望使用已经打开的窗口来打开文件，    
        可以在 code 命令后添加参数 -r来进行窗口的复用
    打开管道数据
        VS Code 命令行除了支持打开磁盘上的文件以外，也接受来自管道中的数据
        如： ls -l | code -r -   // - 代表管道数据
    
配置：
    通过设置面板进行的设置（工作区），会记录在 .vscode/settings.josn 中
    而对用户的配置，则相当于全局配置
    
任务：
    很多时候,像在使用linux系统的时候,我们会自定义一些小脚本来方便的实现一些功能,
    vscode就使用tasks来支持快捷实现一些方便的功能
    有些拓展插件会有封装好的task可以直接执行,我们也可以自定义各种各样的task,
    例如实现“编译当前文件”,“删除多余文件”等等操作。
    tasks比直接定义.bat文件更方便之处在于vscode提供了诸多快捷访问特定路径的方式,
    tasks.json中定义的任务仅能在当前文件夹(包含该文件夹的工作区)中使用。
    task.json用以描述任务
    与该文件相关的菜单是：终端（因为任务可看做是一系列终端命令的集合）
    当没有这个文件时，选择终端/配置任务（或配置默认生成任务），可创建出这个文件
    任务包括编译、打包、测试、部署等， 
    在命令面板中输入 tasks

调试
    调试使用的配置文件是launch.json
    通过运行菜单/添加配置，可创建出该文件
    应该先在命令面板(F1)，填入关键字"c/c++ edit"，选择c/c++：编辑配置(UI)
    经过这一步操作会，会在.vscode下创建出c_cpp_properties.json文件
    有了该文件后，再执行运行菜单/添加配置，才会有(多出)c/c++的调试配置项
    不同于task，调试不是可以"通过一系列脚本命令的集合，实现一个功能"
    launch.json, 这其中的内容主要是用来对调试提供支持
    按f5可以选择模板并生成文件(针对不同语言的拓展插件会提供不同的模板)
    调试时有些功能是gdb有的，但vscode不支持，如跳过执行某几行代码等
    此时可在调试控制台面板的底部，可以执行gdb命令
    不过需要在要执行的gdb命令之前加上 -exec，如 -exec bt、-exec l 等
    在调试多线程时，因为线程调度的关系，程序可以一会儿运行在a线程中，
    一会儿运行在b线程中，可以在程序运行到a线程时，执行 
    -exec set scheduler-locking on，这样，代码便一直在a线程中（b线程得不到调度）
    如果一个线程因为等待而挂起，这时候再执行-exec set scheduler-locking off
    会提示：Unable to perform this action because the process is running
    解决办法就是先暂停该线程，然后在执行上述命令，之后再继续运行该线程

任务配置示例讲解1
    https://geek-docs.com/vscode/vscode-tutorials/
        vscode-task-system-configuration-grouping-and-result-display.html
    {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "test shell",
                "type": "shell",  //使用哪个脚本工具
                "command": "./scripts/test.sh",
                "windows": {
                    "command": ".\\scripts\\test.cmd"
                    },
                "group": "test",
                "presentation": {  //任务运行时的呈现效果
                    "reveal": "always",
                    "panel": "new"
                    },
                "options": {
                    "cwd": "",
                    "env": {},
                    "shell": {
                        "executable": "bash"
                        }
                    }
            }
        ]
    }
    在上面的任务里，我们能够看到 “label”“type”“command” 这几个熟悉的属性，
    它们的意思是，在 shell 下运行 ./scripts/test.sh 这个脚本
    type:使用哪种工具执行，取值受限于 VS Code 或者插件所支持的脚本工具
    当type取值为shell时，任务在集成终端中执行，否则，就是以相应进程执行
    type取值还可以为process，表明以进程方式执行
    vscode也支持对配置文件的自动补全
        比如当我们删除type的值，然后重新输入""后，可以自动列出type的可选值
    command:当type值为shell时使用，代表在shell中执行哪个命令或命令脚本，
            当type取值为process时，代表可执行程序的地址路径
            我们还可以将command放到"windows"/"linux"节点下，代表适用于哪个平台
    args:当我们想给上面的command传递参数时，可直接写在command中，也可使用args
         该属性的值为数组类型，args里的每个值都会传递给command
    不过又多了三个属性 “group” “presentation” 和 “options”，它们分别是干什么的呢
    “group” 属性就是分组，我们可以通过这个属性指定这个任务被包含在哪一种分组当中。
    关于分组，我们有三种选择：“build” 编译生成、“test”测试和 “none”
    在这个例子里，我们把它设置为了 “test”。
    那么，当我们在命令面板里搜索 “运行测试任务” (Run Test Task) 时，
    只有这个任务会被显示出来
    如果我们把这个分组 group 改为 “build”，
    那么在我们执行 “运行生成任务” （Run Build Task）时，则同样能够看到它
    分组的意思很好理解，但是你可能感觉还是不够意思，
    因为虽然有专门的命令去执行生成任务，或者测试任务，
    但是它们还是调出了一个列表让我们进行选择，多此一举，有没有办法一键运行
    当然没问题，我们只需将分组 “group” 的值改成下面这样即可。
    “isDefault” 代表着这条任务是不是这个分组中的默认任务，“kind” 则是代表分组
    "group": {
        "isDefault": true,
        "kind": "test"
       },
    当把“group”改成以上的值后，再当我们执行 “运行测试任务” (Run Test Task) 命令时，
    我们会发现这条测试任务被直接执行了
    而 “运行生成任务” 就更方便了，这个命令已经绑定了一组快捷键。
    我们只需按下 Cmd + Shift + B，就可以自动运行默认的那个生成任务了（build task）
    接下里的两个属性：presentation 是用于控制任务运行的时候，
    是否要自动调出运行的界面，让我们看到结果，
    或者是否要新创建一个窗口执行任务；
    而 options 则是用于控制任务执行时候的几个配置，
    比如控制任务脚本运行的文件夹地址 cwd，控制环境变量 env，
    或者控制任务脚本运行的时候使用哪个 shell 环境。
    
代码调试
    vscode支持代码调试的原理
        VS Code 是把调试功能的最终实现交给插件来完成的。
        VS Code 提供了一套通用的图形界面和交互方式，
        比如怎么创建断点、如何添加条件断点、如何查看当前调试状态下参数的值，等等
        而对于插件作者而言，
        他们需要完成的是如何把真正的调试工作跟 VS Code 的界面和交互结合起来，
        为此 VS Code 为插件作者提供了一套统一的接口，
        叫做Debug Adapter Protocol（DAP）。
        当用户在界面上完成一系列调试相关的操作时，
        VS Code 则通过 DAP 唤起调试插件，由插件完成最终的操作。
        讲到这里，你可能想到了，如果你在使用的语言已经有一个命令行的调试工具，
        那你也可以通过写一个调试插件，
        把这个命令行的调试器通过 DAP 连接到 VS Code 中，
        然后就能够借助 VS Code 这套 UI 来进行图形化的调试
        当然，尽管我们在编辑器中提供了各种调试的界面和功能，
        但这并不意味着每一个调试插件把它们全都实现了。
        这可能是因为插件还没有足够成熟，也有可能是受限于底层的调试器。
    c++的调试
        安装插件：gdb debugger - beyond
    launch.json
        支持ctrl+space智能提示
        type : 调试器的类型，它决定了vscode使用哪个插件来调试代码
        request：如何启动调试器
            如果我们的代码已经运行起来了，
            则可以将它的值设为 attach，
            那么我们则是使用调试器来调试这个已有的代码进程；
            而如果它的值是 launch，
            则意味着我们会使用调试器直接启动代码并且调试
        name：这个配置的名字
        program：告诉调试器调试哪个可执行文件，该值支持预定义变量
            如：${workspaceFolder} 是代表当前工作区文件夹地址
        stopOnEntry当调试器启动后，是否在第一行代码处暂停代码的执行。
            这个属性非常方便，如果没有设置断点而代码执行非常快的话，
            我们就会像文章的最开头那样，代码调试一闪而过，
            而没有办法在代码执行的过程中暂停了。
            而设置了 stopOnEntry 后，代码会自动在第一行停下来，
            然后我们就可以继续我们的代码调试了。
        args 可以通过 args 来把参数传给将要被调试的代码。
        env 环境变量。大部分调试器都使用它来控制调试进程的特殊环境变量。
        cwd 控制调试程序的工作目录。
        port 是调试时使用的端口
        miDebuggerPath gdb 的路径
        miDebuggerServerAddress 服务器的地址和端口(远程调试用)
        
c_cpp_properties.json
    在命令面板中输入关键词:c/c++，选择c/c++编辑配置(ui)
    在这里进行基础的c++编译器的相关设置后，
    即可创建出 c_cpp_properties.json 文件
        
json中支持的变量    
    $ {workspaceFolder} - 在VS Code中打开的文件夹的路径
    $ {workspaceFolderBasename} - VS代码中打开的文件夹的名称，没有任何斜杠（/）
    $ {file} - 当前打开的文件
    $ {relativeFile} - 当前打开的文件相对于workspaceFolder
    $ {fileBasename} - 当前打开文件的基本名称
    $ {relativeFileDirname} - folder
    $ {fileBasenameNoExtension} - 当前打开文件的基本名称，没有文件扩展名
    $ {fileDirname} - 当前打开文件的目录名
    $ {fileExtname} - 当前打开文件的扩展名
    $ {cwd} - 任务运行器在启动时的当前工作目录
    $ {lineNumber} - 活动文件中当前选定的行号
    $ {selectedText} - 活动文件中当前选定的文本
    $ {execPath} - location of Code.exe
    当预定义变量满足不了使用需求时，
    可以在 VSCode 中设置自定义变量，并通过 ${config:Name} 的方式调用
    自定义变量可以在 settings.json 中配置，即 VSCode 的 setting 文件
    
launch.json介绍（调试配置文件）
    {
        "version": "0.2.0", //版本信息
        "configurations": [
            {
            },
            {
                // 配置名称，将会在启动配置的下拉菜单中显示
                "name": "C++ Launch (GDB)",
                // 配置类型，这里只能为cppdbg
                "type": "cppdbg",
                // 请求配置类型，可以为launch（启动）或attach（附加）
                "request": "launch",
                // 调试器启动类型，这里只能为Local
                "launchOptionType": "Local",
                // 生成目标架构，一般为x86或x64,
                // 可以为x86, arm, arm64, mips, x64, amd64, x86_64               
                "targetArchitecture": "x86", 
                // 将要进行调试的程序的路径               
                "program": "${workspaceRoot}",
                // 程序调试时传递给程序的命令行参数，一般设为空即可 
                "args": [], 
                // 指定连接的调试器，可以为gdb或lldb。但目前lldb在windows下没有预编译好的版本。
                "MIMode": "gdb",
                // miDebugger的路径，注意这里要与MinGw的路径对应 
                "miDebuggerPath":"D:\\mingw\\bin\\gdb.exe",
                // 设为true时程序将暂停在程序入口处，一般设置为false                                
                "stopAtEntry": false,
                // 调试程序时的工作目录，一般为${workspaceRoot}即代码所在目录                       
                "cwd": "${workspaceRoot}",
                // （环境变量？）
                "environment": [],
                // 调试时是否显示控制台窗口，一般设置为true显示控制台                
                "externalConsole": true,
                // 如果不设为neverOpen，调试时会跳到“调试控制台”选项卡，你应该不需要对gdb手动输命令吧？
                "internalConsoleOptions": "neverOpen",
                // 用处未知，模板如此，猜测是调试插件（如cppdbg）的启动控制参数 
                "setupCommands": [ 
                    {
                        "description": "Enable pretty-printing for gdb",
                        "text": "-enable-pretty-printing",
                        "ignoreFailures": false
                    }
                ],
                // 调试会话开始前执行的任务，一般为编译程序。与tasks.json的label相对应
                "preLaunchTask": "g++"
            }    
        ]
    }    
    
launch.json示例：    
    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "cctest",
                "type": "cppdbg",
                "request": "launch",
                "program": "${workspaceFolder}/bin/cctest",
                "args": ["-a","--all"],
                "stopAtEntry": false,
                "cwd": "${workspaceFolder}",
                "environment": [],
                "externalConsole": true,
                "MIMode": "gdb",
                "miDebuggerPath": "D:/wecode_build_tools/mingw/bin/gdb.exe",
                "preLaunchTask": "Build",
                "setupCommands": [
                    {
                        "description": "Enable pretty-printing for gdb",
                        "text": "-enable-pretty-printing",
                        "ignoreFailures": true
                    }
                ]
            },
            {
                "name": "test_cctest",
                "type": "cppdbg",
                "request": "launch",
                "program": "${workspaceFolder}/bin/test_cctest",
                "args": [],
                "stopAtEntry": false,
                "cwd": "${workspaceFolder}",
                "environment": [],
                "externalConsole": true,
                "MIMode": "gdb",
                "miDebuggerPath": "D:/wecode_build_tools/mingw/bin/gdb.exe",
                "preLaunchTask": "Build",
                "setupCommands": [
                    {
                        "description": "Enable pretty-printing for gdb",
                        "text": "-enable-pretty-printing",
                        "ignoreFailures": true
                    }
                ]
            }
        ]
    }

task.json介绍
    {
        "version": "2.0.0",
        //每次执行都启动一个新的控制台
        "presentation": {
            "reveal": "always",
            "panel": "new",
            "echo": true
        },
        //设置环境变量
        "options": {
            "env": {
                "LINUX_SRC_HOME": "/home/user/system/packages/services/Car/evs",
                "LOCAL_SRC_HOME": "${workspaceRoot}"
            }
        },
        "type": "shell",
        "problemMatcher": {
            "owner": "vs_code",
            "fileLocation": [
                "relative",
                "${workspaceRoot}"
            ],
            "pattern": {
                "regexp": ".*(app/.*|project/.*):(\\d+):(\\d+):\\s+(warning|error):\\s+(.*)$",
                "file": 1,
                "line": 2,
                "column": 3,
                "severity": 4,
                "message": 5
            }
        },
        //任务列表
        "tasks": [
            {
                "label": "01.[同步代码]本地代码->Linux远程服务器",
                "command": "${workspaceRoot}\\.vscode\\sync_code.cmd",
                "args": [
                    "native",
                    "False"
                ],
                "identifier": "CodeSync",
                "taskClassify": "同步代码"
            },
            
            {
                "label": "02.[同步代码并获取修改文件列表]本地代码-->Linux远程服务器",
                "command": "${workspaceRoot}\\.vscode\\sync_code.cmd",
                "args": [
                    "native",
                    "True"
                ],
                "identifier": "CodeSyncDiff",
                "taskClassify": "同步代码"
            },	
            
            {
                "label": "03.[编译IT]在Linux远程服务器上编译IT工程",
                "dependsOn": "CodeSync",
                "command": "${workspaceRoot}\\.vscode\\build_obj.cmd",
                "args": [
                    "test",
                    "DTCenter.out",
                    "it_cfg",
                    "Debug",
                    "-j8",
                    "cache"
                ],
                "taskClassify": "编译IT工程"
            },
            {
                "label": "04.[同步+编译+IT]在Linux远程服务器上构建IT工程并运行",
                "dependsOn": "CodeSync",
                "command": "${workspaceRoot}\\.vscode\\build_and_run_IT.cmd ratmng.nrom.cfgslave",
                "taskClassify": "同步+编译+IT工程"
            },     
            {
                "label": "05.[静态检查]代码静态检查",
                "dependsOn": "CodeSyncDiff",
                "command": "${workspaceRoot}\\.vscode\\inc_build_flint.cmd",
                "taskClassify": "flint"
            },
            {
                "label": "06.[增量构建] 代码增量compile",
                "dependsOn": "CodeSyncDiff",
                "command": "${workspaceRoot}\\.vscode\\inc_build_compile.cmd",
                "taskClassify": "增量编译"
            }
        ]
    }    
    
使用Makefile编译    
    默认生成的task使用g++编译
        {
            "version": "2.0.0",
            "tasks": [
                {
                    "type": "cppbuild",
                    "label": "C/C++: cpp.exe 生成活动文件",
                    "command": "C:\\Qt\\Qt5.9.0\\Tools\\mingw530_32\\bin\\cpp.exe",
                    "args": [
                        "-fdiagnostics-color=always",
                        "-g",
                        "${file}",
                        "-o",
                        "${fileDirname}\\${fileBasenameNoExtension}.exe"
                    ],
                    "options": {
                        "cwd": "${fileDirname}"  //当前工作路径
                    },
                    "problemMatcher": [
                        "$gcc"
                    ],
                    "group": {
                        "kind": "build",
                        "isDefault": true
                    },
                    "detail": "编译器: C:\\Qt\\Qt5.9.0\\Tools\\mingw530_32\\bin\\cpp.exe"
                }
            ]
        }
    需要修改为使用make：
        {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "build", 
                    "command": "make",  //在shell中执行make命令（找Makefile文件）
                    "type": "shell",
                    "group": {
                        "kind": "build",  //任务分组
                        "isDefault": true
                    }
                },
                {
                    "label": "clean",
                    "command": "make", // 在shell中使用命令，如需加参数，可再添加args属性
                    "args": [
                        "clean"
                    ],
                    "type": "shell",
                    "group": {
                        "kind": "build",
                        "isDefault": true
                    }
                }
            ]
        }

vscode常见文件解决        
    编辑窗口中文乱码：
        设置（ctrl+,）,输入：file:auto
        启用 Files:Auto Guess Encoding
    安装go插件失败
        go env -w GO111MODULE=on
        go env -w GOPROXY=https://goproxy.io,direct
    编译时提示“中断将被重用，按任意键关闭”
        c/c++ 这个插件的bug导致的
        在tasks.json中输入presentation(在设置面板中找不到)，
        其值会只能填充，修改"panel"值为"new"
        
插件介绍
    codelldb
        lldb vs gdb
            两个都是调试用的Debugger，只是LLDB是比较高级的版本，
            或者在调试开发iOS应用时比较好用
            xcode（苹果系统的编译器）之前集成gdb，后改为用lldb
    code runner
        无需繁杂的配置，快速方便的运行代码片段或代码文件
        缺点：不支持断点调试、不支持多文件编译
        支持多种语言，包括但不限于c、c++、java、js、Python、go、
        Perl、bat、lua、c#
        配置：Run Code configuration
        安装该插件后，在编辑区右键，会多出Run Code菜单项
    gdb debugger
        
vscode个性化配置
    预览窗口
        打开和关闭方法：查看/Minimap
        或设置：editor.minimap
    高亮选中行
        设置：editor.renderLineHighlight: "all"
    显示空格与制表符
        设置：editor.renderWhitespace: all
    显示隐藏缩进指示线
        设置：editor.renderIndentGuides
    关闭信任模式
        设置：关键词“信任”，security.workspace.trust
        取消前面的对勾，再添加文件夹时，就不会弹出信任提示窗口了
    禁用非活动区着色（即无效代码自动置灰，该功能默认开启）
        设置，关键字 “dim inactive regions”
    禁用文件标签彩色显示
        设置：workbench>editor>decorations:colors，
        取消前面的对勾，这样可以保证只有当前打开的文件标签是高亮的
        
资源管理器面板
    在资源管理器面板右上角有...
    点击这个按钮，可控制显示/隐藏哪些卷展栏，
    其中“打开的编辑器”卷展栏可以展示当前打开了哪些文件
    而这个卷展栏可能默认是关闭的
    当你在资源管理器中删除一个文件时，
    默认会弹出一个确认删除窗口，如果不希望弹出该窗口
    可通过：设置：explorer.confirmDelete
    另外，资源管理器中当前选中的文件会随编辑窗口中的文件而改变
    如果不希望使用该特性，可：设置：explorer.autoReveal
    过滤显示文件、文件夹
        设置：关键字 exclude
        **/tmp ：过滤掉所有目录下的tmp文件目录
        **/*.d ：过滤掉所有目录下的.d后缀名的文件
        
多文件夹工作区
    通常默认我们只能在vscode中打开一个文件夹
    通过命令面板，输入关键字“文件夹”，选择“工作区：将文件夹添加到工作区”
    即可添加新的文件夹，此时管理器中会创建一个工作区
    将新添加的文件夹与原有的文件夹放在该工作区中
    此后，你可以直接在该工作区中通过右键菜单添加新的文件夹或删除已有文件夹
    可以看到，默认窗口的工作区是没有名字的（名字显示为：无标题）
    同样通过命令面板，将工作区另存为。。。,之后工作区就有名字了

终端面板
    修改使用的终端
        默认情况下，在 Windows 10 上我们会使用 PowerShell，
        而如果是 Win 10 以下的版本那么默认的 Shell 则会是 Cmd。
        macOS 和 Linux 下 VS Code 会检测你的默认 Shell 是什么
        如果 VS Code 挑选的 Shell 不是你想要的，那么你可以修改
        terminal.integrated.shell.windows、
        terminal.integrated.shell.osx 或者
        terminal.integrated.shell.linux，
        这个设置的值就是你想要使用的 Shell 在系统上的路径
        在设置中搜索关键字：terminal.integrated.shell
        在terminal.integrated.shell.windows项目下，可选择使用git bash作为终端
    设置终端字体
        1. 进到系统字体目录
           whereis fonts
           fonts: /etc/fonts /usr/share/fonts
           cd /usr/share/fonts
        2. git clone https://github.com/abertsch/Menlo-for-Powerline.git
           这在linux命令行中直接运行可能无法访问，可在浏览器中先下载下来
           然后把zip包中的 Menlo for Powerline.ttf 文件拷到字体目录下
        3. 更新字体
           fc-cache -f -v [可指定字体目录，默认当前目录]
        4. 重启vscode，设置终端字体
           设置：integrated:font family
           输入：Menlo for Powerline
           注意：只能在用户或工作区中进行设置，在当前目录下不能设置
    将参数传给终端
        设置：terminal.integrated.shellArgs
    设置终端中可使用哪些环境变量
        设置：terminal.integrated.env
    其他终端设置
        terminal.integrated.cwd 用于控制 Shell 启动时的初始目录
        terminal.integrated.rightClickBehavior 控制鼠标右键点击时的行为
        terminal.integrated.enableBell 可以控制当脚本出错时是否要发出响声
        terminal.integrated.scrollback 设置终端输出缓存行数（默认1000行）
    比linux自带的shell终端更强的地方是
    vscode终端可以支持查找(ctrl+f)，支持ctrl+c,ctrl+v
    在终端中输入文件名（相对路径），ctrl+鼠标点击，可以在编辑窗口中打开该文件
    在资源管理器面板中定位到路径，右键选择在集成终端中打开，
    即可让集成终端跳转到该路径

变量监视窗口
    查看数组内容
        *(数组数据类型(*)[number])数组名
    
好用的插件
    better c++ syntax
    c/c++
    c/c++ extension pack
    c/c++ runner
    c/c++ themes
    chinese
    cmake
    cmake tools
    code runner
    error lens
    gdb debugger
    local history
    partial diff
    path intellisense
    todo tree
    vscode-icons
    （）*bookmarks