几种常见的Shell
    常见的 Shell 有 sh、bash、csh、tcsh、ash、dash等。
        sh 是 UNIX 上的标准 shell，很多 UNIX 版本都配有 sh。sh 是第一个流行的 Shell。
        csh 这个 shell 的语法有点类似C语言，所以才得名为 C shell ，简称为 csh。
        tcsh 是 csh 的增强版，加入了命令补全功能，提供了更加强大的语法支持。
        ash 是一个简单的轻量级的 Shell，占用资源少，适合运行于低内存环境，但与bash完全兼容。
        bash 由 GNU 组织开发，保持了对 sh shell 的兼容性，是各种 Linux 发行版默认配置的 shell。
        dash 鉴于 bash 过于复杂，有人把bash从NetBSD移植到Linux并更名为dash(debian almquist shell)，
            并以获得更快的脚本执行速度。它比 Bash 小，只需要较少的磁盘空间，但是它的对话性功能也较少。
    查看 Shell
        Shell 是一个程序，一般都是放在/bin或者/user/bin目录下，
        当前 Linux 系统可用的 Shell 都记录在/etc/shells文件中。
        /etc/shells是一个纯文本文件，你可以在图形界面下打开它，也可以使用 cat 命令查看它。
        在现代的 Linux 上，sh 已经被 bash 代替，/bin/sh往往是指向/bin/bash的符号链接。
        如果你希望查看当前 Linux 的默认 Shell，那么可以输出 SHELL 环境变量：echo $SHELL
    本文讲的是bash的用法
Shell 通过PS1和PS2两个环境变量来控制提示符格式
    PS1 控制最外层命令行的提示符格式。
    PS2 控制第二层命令行的提示符格式。
        一些未完成的命令，如 ' echo "aa ' ,此时回车后，因为echo命令还没遇到第二个 ' " '作为结束标记，
        所以之后的每一行都是以 > 开头（这是PS2的默认值)，直到遇到第二个”，echo结束输入。
    设置语法请参阅相关教程
    #! /bin/bash
    第一行的'#!' 是一个约定的标记，它告诉系统这个脚本需要什么解释器来执行，即使用哪一种Shell
    经测试，可以不设置第一行，但如果设置了，就要把shell的路径写对，否则会报错误。
执行sh
    1. 通过 ./test.sh 执行，
        注意，一定要写成./test.sh，而不是test.sh。运行其它二进制的程序也一样。
        直接写test.sh，linux系统会去PATH里寻找有没有叫test.sh的，
        而只有/bin, /sbin, /usr/bin，/usr/sbin等在PATH里，你的当前目录通常不在PATH里，
        所以写成test.sh是会找不到命令的，要用./test.sh告诉系统说，就在当前目录找。
        通过这种方式运行bash脚本，第一行一定要写对，好让系统查找到正确的解释器。
    2. 作为解释器参数
        这种运行方式是，直接运行解释器，其参数就是shell脚本的文件名，如：
        /bin/sh test.sh
        /bin/php test.php
        这种方式运行的脚本，不需要在第一行指定解释器信息，写了也没用。
变量
    变量的类型
        脚本语言在定义变量时通常不需要指明类型，直接赋值就可以，Shell 变量也遵循这个规则。
        在 Bash shell 中，每一个变量的值都是字符串，无论你给变量赋值时有没有使用引号，值都会以字符串的形式存储。
        这意味着，Bash shell 在默认情况下不会区分变量类型，即使你将整数和小数赋值给变量，它们也会被视为字符串.
        当然，如果有必要，你也可以使用 declare 关键字显式定义变量的类型，但在一般情况下没有这个需求.
    变量赋值
        variable=value
        variable='value'
        variable="value"
        注意，赋值号的周围不能有空格
        单引号和双引号的区别
            以单引号' '包围变量的值时，单引号里面是什么就输出什么，即使内容中有变量和命令（命令需要反引起来）
            也会把它们原样输出。这种方式比较适合定义显示纯字符串的情况，即不希望解析变量、命令等的场景。
            以双引号" "包围变量的值时，输出时会先解析里面的变量和命令，而不是把双引号中的变量名和命令原样输出。
            这种方式比较适合字符串中附带有变量和命令并且想将其解析后再输出的变量定义。
            #!/bin/bash
            url="http://c.biancheng.net"
            website1='C语言中文网：${url}'
            website2="C语言中文网：${url}"
            echo $website1
            echo $website2
            运行结果：
            C语言中文网：${url}
            C语言中文网：http://c.biancheng.net
        将命令的结果赋值给变量
            Shell 也支持将命令的执行结果赋值给变量，常见的有以下两种方式：
            variable=`command`
            variable=$(command)    //与反引号效果一致，但容易和单引号区分，所以推荐这种样式
    使用变量
        用一个定义过的变量，只要在变量名前面加美元符号$即可
        echo $author
        echo ${author}
        变量名外面的花括号{ }是可选的，加不加都行，加花括号是为了帮助解释器识别变量的边界
        skill="Java"
        echo "I am good at ${skill}Script"
    修改变量的值
        已定义的变量，可以被重新赋值
        第二次对变量赋值时不能在变量名前加$，只有在使用变量时才能加$
    只读变量 
        使用 readonly 命令可以将变量定义为只读变量，只读变量的值不能被改变。
        myUrl="http://see.xidian.edu.cn/cpp/shell/"
        readonly myUrl
        myUrl="http://see.xidian.edu.cn/cpp/danpianji/"   //报错
    局部变量
        使用 local 命令可以定义局部变量，在函数中定义的变量，默认是全局可见的。
    删除变量
        使用 unset 命令可以删除变量。语法：
        unset variable_name
        变量被删除后不能再次使用；unset 命令不能删除只读变量。
    特殊变量
        $ 表示当前Shell进程的ID，即pid， echo $$ 显示当前进城id
        变量	含义
        $0	当前脚本的文件名
        $n	传递给脚本或函数的参数。n 是一个数字，表示第几个参数。例如，第一个参数是$1。
        $#	传递给脚本或函数的参数个数。
        $*	传递给脚本或函数的所有参数。
        $@	传递给脚本或函数的所有参数。$@被双引号(" ")包含时，与 $* 稍有不同，下面将会讲到。
        $?	上个命令的退出状态，或函数的返回值。
        $$	当前Shell进程ID。对于 Shell 脚本，就是这些脚本所在的进程ID。
        $* 和 $@ 的区别
            被双引号(" ")包含时，"$*" 会将所有的参数作为一个整体，以"$1 $2 … $n"的形式输出所有参数；
            "$@" 和没被双引号包含的$*/$@效果一样，会将各个参数分开，以"$1" "$2" … "$n" 的形式输出所有参数。
字符串处理
    ${var}	        变量本来的值
    ${var:-word}	    如果变量 var 为空或已被删除(unset)，那么返回 word，但不改变 var 的值。
    ${var:=word}	    如果变量 var 为空或已被删除(unset)，那么返回 word，并将 var 的值设置为 word。
    ${var:?message}	如果变量 var 为空或已被删除(unset)，那么将消息 message 送到标准错误输出。
    ${var:+word}	    如果变量 var 被定义，那么返回 word，但不改变 var 的值。
    ${#var}          获取字符串长度
    ${var:1:4}       提取子字符串（第2~5个字符），第一个字符从0算起，4表示截取长度，不带表示一直到结尾
    ${var:1}         提取子字符串（第2个字符到结尾），第一个字符从0算起
    拼接字符串         两个字符串直接拼接即可， 如echo "abc""def" 或 "abc"$var
    查找子字符串       可以expr实现，如 expr index 和 expr substr等
    更多知识，参见后面的"各种括号详解/单大括号"一节
运算符
    数学运算
        原生bash不支持简单的数学运算，但是可以通过其他命令来实现，例如 awk 和 expr，expr 最常用。
        可以使用 expr --help 查看使用帮助， 这里提几个注意事项：
        1. 运算符前后要带空格  ；  2. 乘号运算符前面要带转义控制符\  3.不支持小数运算
        举例： val=`expr $a \* $b`  ； val=`expr $b / $a`
    比较运算
        运算符	说明	                                         举例
        -eq	检测两个数是否相等，相等返回 true。	            [ $a -eq $b ] 返回 true。
        -ne	检测两个数是否相等，不相等返回 true。	            [ $a -ne $b ] 返回 true。
        -gt	检测左边的数是否大于右边的，如果是，则返回 true。    [ $a -gt $b ] 返回 false。
        -lt	检测左边的数是否小于右边的，如果是，则返回 true。	[ $a -lt $b ] 返回 true。
        -ge	检测左边的数是否大等于右边的，如果是，则返回 true。	[ $a -ge $b ] 返回 false。
        -le	检测左边的数是否小于等于右边的，如果是，则返回 true。	[ $a -le $b ] 返回 true。
        ==	相等。可用于数字或字符串的比较，相同则返回 true。	[ $a == $b ] 返回 false。
        !=	不相等。可用于数字或字符串的比较，不相同则返回 true。	[ $a != $b ] 返回 true。
        \>  大于，可用于数字或字符串的比较                     [ $a \< $b ] 
        \<  小于，可用于数字或字符串的比较                     [ $a \> $b ] 
        注意： 运算符前后要用空格隔开，没有特别说明的，则只支持数字比较，不支持字符串比较
    逻辑运算
        运算符	说明	                                         举例
        !	非运算，表达式为 true 则返回 false，否则返回 true。	[ ! false ] 返回 true。
        -o	或运算，有一个表达式为 true 则返回 true。	        [ $a -lt 20 -o $b -gt 100 ] 返回 true。
        -a	与运算，两个表达式都为 true 才返回 true。	        [ $a -lt 20 -a $b -gt 100 ] 返回 false。
    字符串运算
        运算符	说明	                                         举例
        =	检测两个字符串是否相等，相等返回 true。	         [ $a = $b ] 返回 false。
        !=	检测两个字符串是否相等，不相等返回 true。	         [ $a != $b ] 返回 true。
        =~  检测包含子字符串                                    [[ $filepath =~ "." ]]
        -z	检测字符串长度是否为0，为0返回 true。	             [ -z $a ] 返回 false。
        -n	检测字符串长度是否为0，不为0返回 true。	         [ -z $a ] 返回 true。
        str	检测字符串是否为非空，非空返回 true。	             [ $a ] 返回 true。
    文件测试
        操作符	说明	                                         举例
        -b file	检测文件是否是块设备文件。	                 [ -b $file ] 返回 false。
        -c file	检测文件是否是字符设备文件。	                 [ -b $file ] 返回 false。
        -d file	检测文件是否是目录。	                     [ -d $file ] 返回 false。
        -g file	检测文件是否设置了 SGID 位。	                 [ -g $file ] 返回 false。
        -p file	检测文件是否是具名管道。	                     [ -p $file ] 返回 false。
        -u file	检测文件是否设置了 SUID 位。	                 [ -u $file ] 返回 false。
        -r file	检测文件是否可读。	                         [ -r $file ] 返回 true。
        -w file	检测文件是否可写。	                         [ -w $file ] 返回 true。
        -x file	检测文件是否可执行。	                     [ -x $file ] 返回 true。
        -e file	检测文件（包括目录）是否存在。	             [ -e $file ] 返回 true。    
        -s file	检测文件是否为空（文件大小是否大于0）。	         [ -s $file ] 返回 true。
        -k file	检测文件是否设置了粘着位(Sticky Bit)。	     [ -k $file ] 返回 false。
        -f file	检测文件是否是普通文件（不包括目录和设备文件）。  [ -f $file ] 返回 true。
注释
    h里没有多行注释，只能每一行加一个#号
    遇到大段的代码需要临时注释起来，可以把这一段要注释的代码用一对花括号括起来，
    定义成一个函数，没有地方调用这个函数，这块代码就不会执行，达到了和注释一样的效果
数组
    定义
        在Shell中，用括号来表示数组，数组元素用“空白”符号分割开。定义数组的一般形式为：
        array_name=(value_1 ... value_n)
        例如：array_name=(value0 value1 value2 value3)
        也可以单独定义数组的各个分量：
        array_name[0]=value0
        array_name[1]=value1
        array_name[5]=value2
        可以不使用连续的下标，而且下标的范围没有限制。
    使用
        读取时，直接 $arr[0]是不行的，需要${arr[0]}
        echo ${arr[@]} 或 echo ${arr[*]} 可以打印整个数组
        ${#arr[*]} 或 ${#arr[@]} 获取数组的元素个数
输出命令
    echo 选项 字符串
        选项
        -n  不输出尾随的换行符
        -e  启用反斜杠的转义功能
        -E  禁用反斜杠的转义功能（默认)
    printf
        echo的增强版，它是c语言printf的有限变形，并在语法上有些不同
        printf  format-string  [arguments...]
        与C语言中printf的不同：
            控制字符串可以有引号，也可以不加，单双引号均可
            参数多于格式控制符(%)时，format-string 可以循环重用，直到将所有参数都转换
            arguments 使用空格分隔，不用逗号
            不支持%e/%E/%f/%g/%G等控制符（需要时，可用awk完成)
        例： printf "%s %s %s\n" a b c d e f g h
            a b c
            d e f
            g h
条件测试
    test命令，简写为[]，可以进行数值、字符串、文件三方面的检测，
    通常和if一起使用，且大部分的if语句都以来test
    如果使用[]时，注意中括号与表达式之间要用空格分隔
    测试表达式的相关语法，参看前面的“运算符”一节
    举例： 
    if test -e ./bash   // 或 if [ -e ./bash ]
    then
        echo "the file already exist"
    else
        echo "the file does not exist"
    fi
流程控制
    if then elif then else fi
        if [ expression ]
        then 
            ...
        elif [ expression ]
        then
            ...
        else
            ...
        fi
        如果写成一行，则应把上面的每个换行符替换成分号，
    case in esac
        case 值 in        //不要忘记关键字in，值的类型可为数字或字符串
        匹配1)            //末尾是右括号)，而不是冒号:
            。。。        //可以与模式1)写在同一行，且无需分号隔开
            ;;           //两个连续分号，对应break
        匹配2)
            。。。
            ;;
        *)               //*）对应 default
            。。。
            ;;
        esac
        举例：
        echo 'Input a number between 1 to 4'
        echo 'Your number is:\c'
        read aNum
        case $aNum in
            1)  echo 'You select 1'
            ;;
            2)  echo 'You select 2'
            ;;
            3)  echo 'You select 3'
            ;;
            4)  echo 'You select 4'
            ;;
            *)  echo 'You do not select a number between 1 to 4'
            ;;
        esac
    for in do done
        for 变量 in 列表
        do
            command1
            command2
            ...
            commandN
        done
        列表是一组值（数字、字符串等）组成的序列，每个值通过空白分隔。
        每循环一次，就将列表中的下一个值赋给变量
        举例： 显示主目录下，以.bash开头的文件
        for FILE in $HOME/.bash*
        do
           echo $FILE
        done
    while do done
        while command
        do
           Statement(s) to be executed if command is true
        done
        举例：循环计数
        COUNTER=0
        while [ $COUNTER -lt 5 ]
        do
            COUNTER='expr $COUNTER+1'
            echo $COUNTER
        done
        举例：循环读，直到用户按ctrl+D结束
        while read aa
        do
            。。。
        done
    until do done
        until command
        do
           Statement(s) to be executed until command is true
        done
        until 循环执行一系列命令直至条件为 true 时停止。until 循环与 while 循环在处理方式上刚好相反。
        command 一般为条件表达式，如果返回值为 false，则继续执行循环体内的语句，否则跳出循环。
    break / continue
函数
    声明
        Shell 函数的定义格式如下：
        function_name () {
            list of commands
            [ return value ]
        }
        如果你愿意，也可以在函数名前加上关键字 function：
        function function_name () {
            list of commands
            [ return value ]
        }
        Shell 函数返回值只能是整数，一般用来表示函数执行成功与否，0表示成功，其他值表示失败。
        如果 return 其他数据，比如一个字符串，往往会得到错误提示：“numeric argument required”。
        如果需要得到字符串形式的函数处理结果，在函数内部声明的变量，在函数外部可以直接使用。
    使用
        调用函数时，就像调用内置命令一行，直接给出函数名即可，不需要加括号，
        如果有参数，则可通过空格隔开的方式，将参数传给函数
        函数内部使用 $n $*等获取参数信息，具体参看 "变量/特殊变量"一节
        使用 $? 得到函数返回值
        如果你希望直接从终端调用函数，可以将函数定义在主目录下的 .profile 文件，
        这样每次登录后，在命令提示符后面输入函数名字就可以立即调用。
重定向
    一般情况下，每个 Unix/Linux 命令运行时都会打开三个文件：
        标准输入文件(stdin)：stdin的文件描述符为0，Unix程序默认从stdin读取数据。
        标准输出文件(stdout)：stdout 的文件描述符为1，Unix程序默认向stdout输出数据。
        标准错误文件(stderr)：stderr的文件描述符为2，Unix程序会向stderr流中写入错误信息。
    默认情况下，command > file 将 stdout 重定向到 file，command < file 将stdin 重定向到 file。
    如果希望 stderr 重定向到 file，可以这样写：$command 2 > file 或 $command 2 >> file
    如果希望对 stdin 和 stdout 都重定向，可以这样写：$command < file1 >file2
    如果希望将 stdout 和 stderr 合并后重定向到 file，可以这样写：$command > file 2>&1
    注意，2>&这三个字符必须连在一块，中间不能有空格，而&1中间是可以有空格的。
    如果希望执行某个命令，但又不希望在屏幕上显示输出结果，那么可以将输出重定向到 /dev/null。
    如果希望屏蔽 stdout 和 stderr，可以这样写：command > /dev/null 2>&1
文件包含
    如果脚本需要包含其它脚本文件，可用 . filename 或 source file 进行包含，两者效果相同   
各种括号详解
    单小括号
        1. 命令组
            括号中的命令将会新开一个子shell顺序执行，所以括号中的变量不能够被脚本余下的部分使用。
            括号中多个命令之间用分号隔开，最后一个命令可以没有分号，各命令和括号之间不必有空格。
        2. $()，命令替换，等同于反引号
        3. 初始化数组，如 arr=(a b c)
    双小括号
        1. $((exp))
            只要exp符号c语言的运算规则，都可用在$((exp))中，甚至是三目运算符。
            如a=$((3+4))，b=$(( 5 + 6 ))，都是可以的，只要=两边没有空格就行
        2. ((exp))
            与前面带$相比，这种方式也可以执行算数运算，只是没法将运算结果返回而已。
            如a的值原来为7, 执行 ((a++))后，a的值会变为8,((a=13)后，a的值变为13。
        3. for((i=0;i<5;i++)) , 效果等同于 for i in `seq 0 4` 或 for i in {0..4}
    单中括号
        1. 一般配合if使用，和test效果相同
           此时，[是个命令，所以后面必须有空格，该命令要求最后一个参数必须是]
        2. 作为数组的下标
        3. 出现在正则表达式中，用以描述一个匹配的字符范围
    双中括号
        1. 和[]用作条件判断类似，但比[]更为通用，
            如<、>、&&、||等操作符能直接出现在[[]]中，但在[]中则会报错
            如 if [[ $a != 1 && $a != 2 ]],如果不适用双括号, 
            则为if [ $a -ne 1] && [ $a != 2 ]或者if [ $a -ne 1 -a $a != 2 ],
            bash把双中括号中的表达式看作一个单独的元素，并返回一个退出状态码。
    单大括号 
        1. ${} 用以标识变量
        2. {,} 和 {..} 用以表示一个集合列表
            如 ls {a,b}.txt  显示 a.txt b.txt
            ls a_{1..3}.txt 显示 a_1.txt a_2.txt a_3.txt
            ls {ex[1-3],ex4}.txt 显示 ex1.txt ex2.txt ex3.txt ex4.txt
        3. 表示代码块，实际是创建了一个匿名函数，与小括号不同的，它不会新开一个shell
        4. 字符串处理（返回修改后结果)
            4.1 字符串为空或非空时，替换为指定字符串，返回结果，不改变原变量
                ${var:-string},${var:+string},${var:=string},${var:?string} ，实现字符串替换
                详见"字符串处理"一节
            4.2. 模式匹配删除 (删除开头或结尾的字符，返回结果，不改变原变量)
                模式匹配记忆方法：
                    # 是去掉左边(在键盘上#在$之左边)，% 是去掉右边(在键盘上%在$之右边)
                    单一的 # 或 % 是最小匹配，## 或 %% 是最大匹配
                例：
                    dir=`pwd`
                    dir2=${dir%/*}  获取上级目录
                ${var%pattern},${var%%pattern},${var#pattern},${var##pattern}
                这四种模式中都不会改变variable的值，
                其中，只有在pattern中使用了*匹配符号时，%和%%，#和##才有区别。
                结构中的pattern支持通配符 *、？和[..]、[!..]
                    *表示零个或多个任意字符，
                    ?表示仅与一个任意字符匹配，
                    [...]表示匹配中括号里面的字符，
                    [!...]表示不匹配中括号里面的字符。
            4.3. 字符串提取和替换（返回结果，不改变原变量)
                ${var:num} 类似于substr
                    shell在var中提取第num个字符到末尾的所有字符。
                    若num为正数，从左边0处开始； 若num为负数，从右边开始提取字串；
                    如num为负数，则必须使用在冒号后面加空格或一个数字或整个num加上括号，
                    如${var: -2}、${var:1-3}或${var:(-2)}。
                ${var:num1:num2}，类似于substr,num1是位置，num2是长度
                ${var/pattern/pattern}，将var字符串的第一个匹配的pattern替换为另一个pattern
                ${var//pattern/pattern}，将var字符串中的所有能匹配的pattern替换为另一个pattern
通配符：
    *       ： 匹配多个 
    ？      ： 匹配一个
    []     ： 匹配范围内的单个字符
        [A-z] : 表示 A~Z,a~z 中的任意一个字符
        [Az]  : 表示 A或z
    [!]    ： 匹配范围外的单个字符，匹配指定的字符集合之外的字符
    [^]    ： 效果同[!]
test和[]和[[]]的对比
    参：https://segmentfault.com/a/1190000022265453
