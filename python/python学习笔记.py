<catalog s0/s4/s8/s12/s16 catalog_line_prefix=.>
.Python3基础语法（菜鸟教程）
    .空行：
        空行与缩进不同，不是python语法的一部分，空行分割只是方便阅读
    .多行语句： 
        需要在行尾用\连接多行，括号中的多行语句无需行换行符
    .多条语句连写：
        可以将多条语句写为一行，每条语句间通过分号分隔
    .import 与 from...import：
        import将整个模块(somemodule)导入，格式为： import somemodule
        从某个模块中导入某个函数,格式为： from somemodule import somefunction
        从某个模块中导入多个函数,格式为： from somemodule import func1, func2, func3
        将某个模块中的全部函数导入，格式为： from somemodule import *
        关于 import 的小结，以 time 模块为例：
            1、将整个模块导入，例如：import time，在引用时格式为：time.sleep(1)。
            2、将整个模块中全部函数导入，例如：from time import *，在引用时格式为：sleep(1)。
            3、将模块中特定函数导入，例如：from time import sleep，在引用时格式为：sleep(1)。
            4、将模块换个别名，例如：import time as abc，在引用时格式为：abc.sleep(1)
    .获取函数的帮助信息：
        可以通过python安装目录下的chm帮助文档获取函数帮助
        在python交互模式中，使用help("函数名")，可以获得该函数的帮助信息
    .变量：
        变量无需声明
        多变量赋值：
            1. a = b = c = 1
            2. a, b, c = 1, 2, "runoob"  #三个值会分别赋给变量a,b,c
    .数学运算：
        /  ：普通除法
        // ：整除
            //得到的结果不一定是整数，这与分子、分母类型有关
            7//2 返回值为 3 ，7.0//2 或 7//2.0 返回值为 3.0
        %  ：取余
        ** ：密乘
        数学表达式语句执行后，会默认将结果赋值给内置的只读变量_（有点类似shell的$?）
    .标准数据类型：
        不可变数据
            Numuber(int,bool,float,complex)、String(str)、Tuple(tuple,元组)
        可变数据
            List(list)、Dictionary(dic)、Set(set)
        说明：
            与c++不同，python中所有的数据类型，其本质都是引用类型
            对于不可变数据类型，就是当修改该变量的值时，该变量会指向一个新的对象
            使用id(变量名)，可得到变量引用的真实对象的内存地址
            使用type(变量名)，会返回表征该变量类型信息的type类变量
                type是个内建类，该对象可以被输出，如 "<class 'int'>"
                type(3) == int;  返回 True
            使用isinstance(变量名, 类型名)，判断一个变量是否为指定类型或其派生类，返回布尔
            使用del，可以删除引用的对象： del var1,var2,....
    .数字类型： 
        bool(True=1,False=0,是int的派生类) int float complex(复数)
        和java一样，对于较小的整数变量([-5,256])，都是引用的预置静态对象：
            a=10;b=10;id(a)==id(b)      # True
            a=1234;b=1234;id(a)==id(b)  # True (优化)
                其实在同一个代码块中，也会有这种优化，即：
                在同一个代码块中创建的两个整数对象中，它们的值相等的话，
                那么这两个对象引用同一个整数对象
                不仅是整数，但凡是不可变的对象(如字符串等)，在同一代码块中，
                只要值相等的对象就不会重复创建，而是直接引用已经存在的对象
            a=1234;
            b=1234;
            id(a)==id(b)  # False
        上述关键字可用于数据类型强转，如
            当字符串内容为浮点型要转换为整型时，无法直接用 int() 转换：
            a='2.1'  # 这是一个字符串
            print(int(a))
            会报错 "invalid literal for int() "。
            需要把字符串先转化成 float 型再转换成 int 型：
            a='2.1'
            print(int(float(a)))
            输出 2。
    .字符串：
        单引号等价于双引号
        单引号和双引号可以嵌套，被嵌套的会被解释成为普通标点符号
        三引号可以指定一个多行字符串，里面可以嵌套单引号/双引号的字符串
        连续的字符串自动拼接
        字符串支持加法和乘法运算，+用于拼接，*表字符串重复
        Python 没有单独的char字符类型，一个字符就是长度为 1 的字符串
        .字符串的截取
            语法格式：变量[头下标:尾下标:步长]
            下标为负数时，表从后面数第几位，尾下标默认为-1，步长默认为1
            步长为负数时，表反向读取
            含头不含尾：头下标处的字符会输出，尾下标处的字符不会输出
            举例：
                str='123456789'
                print(str)                 # 输出字符串
                print(str[0:])             # 输出 123456789 
                print(str[0:-1])           # 输出 12345678   #-1可理解为len(str)-1，即9的位置([8])
                print(str[-1::-1])         # 输出 987654321  
                print(str[9::-1])          # 输出 987654321   
                print(str[9:0:-1])         # 输出 98765432  
                print(str[9:-1:1])         # 输出空
                print(str[-1:0:-1])        # 输出 98765432
                print(str[0])              # 输出字符串第一个字符
                print(str[2:5])            # 输出从第三个开始到第五个的字符
                print(str[2:])             # 输出从第三个开始后的所有字符
                print(str[1:5:2])          # 输出从第二个开始到第五个且每隔一个的字符（步长为2）
                含头不含尾：
                    如 s[0:2], 希望输出的是：'012'，实际输出的是：'12'
                    单独输出 s[9],报错, s[8], 输出 '9'
                    s[0:8], 输出 '12345678',  s[0:9], 输出 '123456789'
        .原生字符串
            r""为原生字符串方式，即让字符串中的\原样输出，而不发生转义
        .b字符串
            b""形式的字符串，里面的字符只能是拉丁字符（不支持中文），
            默认情况下，字符串中的字符是Unicode编码的，
            b字符串中的字符则是采用多字节编码
        .Unicode字符串
            在python2中，字符串默认用8位的ASCII码进行存储，
            在字符串前面加标识符u，可以强制用Unicode编码
            而在python3中，字符串默认用Unicode编码
        .%格式化字符串
            "格式化字符串" % (元组)   #不能用列表
            例： print ("我叫 %s 今年 %d 岁!" % ('小明', 10))
            优点：与后两种格式化字符串方法相比，这种方法能更精确的控制字符串输出格式
        .str.format()方法格式化字符串   （python >= 2.6)
            这种方法有点类似Qt的字符串格式化方法，使用 {索引数字} 作占位符，索引从0开始
            例： print("我叫 {0} 今年 {1} 岁".format('小明',10))
            另外，占位符除了使用索引数字，还可以使用 {参数名} 作占位符
            例： print("我叫 {name} 今年 {age} 岁".format(name="小明",age=10))
            如果使用空占位符 {},也是允许的，此时表明依次使用第1、2、3...个参数
            例： print("我叫 {} 今年 {} 岁".format('小明',10))
            优点：这种方法使用方便，无需关心要输出变量的格式
        .f-string格式化字符串   (python >= 3.6)
            这种方法有点像bash脚本中的${变量名}用法, 在python的f-string中，
            可以直接使用 {变量}、{表达式}、{变量表达式}
            但是需要在字符串前面带f-string字符串标记f
            例： name="小明";age=9; print(f"我叫 {name} 今年 {age+1} 岁")
            优点：与前两种格式化字符串方法相比，这种方法更加简洁直观方便，但它对python的版本要求高
        .字符串部分内建函数
            1	capitalize()
                将字符串的第一个字符转换为大写
            2	center(width, fillchar)
                返回一个指定的宽度 width 居中的字符串，fillchar 为填充的字符，默认为空格。
            3	count(str, beg= 0,end=len(string))
                返回 str 在 string 里面出现的次数，
                如果 beg 或者 end 指定则返回指定范围内 str 出现的次数
            4	bytes.decode(encoding="utf-8", errors="strict")
                Python3 中没有 decode 方法，但我们可以使用 bytes 对象的 decode() 方法
                来解码给定的 bytes 对象，这个 bytes 对象可以由 str.encode() 来编码返回。
            5	encode(encoding='UTF-8',errors='strict')
                以 encoding 指定的编码格式编码字符串，
                如果出错默认报一个ValueError 的异常，除非 errors 指定的是'ignore'或者'replace'
                例：str.encode(encoding='UTF-8',errors='strict')
                encoding -- 要使用的编码，如: UTF-8、GBK。
                errors -- 设置不同错误的处理方案。
                默认为 'strict',意为编码错误引起一个UnicodeError。 
                其他可能得值有 'ignore', 'replace', 'xmlcharrefreplace', 'backslashreplace' 
                以及通过 codecs.register_error() 注册的任何值
            6	endswith(suffix, beg=0, end=len(string))
                检查字符串是否以 obj 结束，如果beg 或者 end 指定则检查指定的范围内
                是否以 obj 结束，如果是，返回 True,否则返回 False.
            7	expandtabs(tabsize=8)
                把字符串 string 中的 tab 符号转为空格，tab 符号默认的空格数是 8 。
            8	find(str, beg=0, end=len(string))
                检测 str 是否包含在字符串中，如果指定范围 beg 和 end ，
                则检查是否包含在指定范围内，如果包含返回开始的索引值，否则返回-1
            9	index(str, beg=0, end=len(string))
                跟find()方法一样，只不过如果str不在字符串中会报一个异常。
            10	isalnum()
                如果字符串至少有一个字符并且所有字符都是汉字、字母或数字，
                则返回 True，否则返回 False
            11	isalpha()
                如果字符串至少有一个字符并且所有字符都是汉字或字母，
                则返回 True, 否则返回 False
            12	isdigit()
                如果字符串只包含数字则返回 True 否则返回 False..
            13	islower()
                如果字符串中包含至少一个区分大小写的字符， #有且全是
                并且所有这些(区分大小写的)字符都是小写，则返回 True，否则返回 False
            14	isnumeric()
                如果字符串中只包含数字字符，则返回 True，否则返回 False
            15	isspace()
                如果字符串中只包含空白，则返回 True，否则返回 False.
            16	istitle()
                如果字符串是标题化的(见 title())则返回 True，否则返回 False
            17	isupper()
                如果字符串中包含至少一个区分大小写的字符， #有且全是
                并且所有这些(区分大小写的)字符都是大写，则返回 True，否则返回 False
            18	join(seq)
                以当前字符串作为分隔符，将 seq 中所有的元素(的字符串表示)合并为一个新的字符串
                例：
                    s1 = "-"
                    s2 = ""
                    seq = ("r", "u", "n", "o", "o", "b") # 字符串序列
                    print (s1.join( seq ))
                    print (s2.join( seq ))
                    以上实例输出结果如下：
                    r-u-n-o-o-b
                    runoob
            19	len(string)
                返回字符串长度
            20	ljust(width[, fillchar])
                返回一个原字符串左对齐,并使用 fillchar 填充至长度 width 的新字符串，
                fillchar 默认为空格。 例：
                str = "Runoob example....wow!!!"
                print (str.ljust(50, '*'))
                以上实例输出结果如下：
                Runoob example....wow!!!**************************      
            21	lower()
                转换字符串中所有大写字符为小写.
            22	lstrip()
                截掉字符串左边的空格或指定字符。
            23	maketrans()
                创建字符映射的转换表，对于接受两个参数的最简单的调用方式，
                第一个参数是字符串，表示需要转换的字符，第二个参数也是字符串表示转换的目标。
                Python3.4 已经没有 string.maketrans() 了，取而代之的是内建函数: 
                bytearray.maketrans()、bytes.maketrans()、str.maketrans()
                例：
                    # 字母 R 替换为 N
                    txt = "Runoob!"
                    mytable = txt.maketrans("R", "N")  #建立映射表
                    print(txt.translate(mytable))      #参照映射表对字符串进行替换处理
                    输出结果： Nunoob!
                    # 使用字符串设置要替换的字符，一一对应
                    intab = "aeiou"
                    outtab = "12345"
                    trantab = str.maketrans(intab, outtab)  #建立映射表
                    str = "this is string example....wow!!!"
                    print (str.translate(trantab))          #参照映射表对字符串进行替换处理
                    输出结果： th3s 3s str3ng 2x1mpl2....w4w!!!
                    txt = "Google Runoob Taobao!"
                    x = "mSa"
                    y = "eJo"
                    z = "odnght"   # 设置删除的字符
                    mytable = txt.maketrans(x, y, z)    #建立映射表
                    print(txt.translate(mytable))       #参照映射表对字符串进行替换处理
                    输出结果： Gle Rub Tobo!
            24	max(str)
                返回字符串 str 中最大的字母。
            25	min(str)
                返回字符串 str 中最小的字母。
            26	replace(old, new [, max])
                把 将字符串中的 old 替换成 new,如果 max 指定，则替换不超过 max 次。
            27	rfind(str, beg=0,end=len(string))
                类似于 find()函数，不过是从右边开始查找.
            28	rindex( str, beg=0, end=len(string))
                类似于 index()，不过是从右边开始.
            29	rjust(width,[, fillchar])
                返回一个原字符串右对齐,并使用fillchar(默认空格）填充至长度 width 的新字符串
            30	rstrip()
                删除字符串末尾的空格或指定字符。
            31	split(str="", num=string.count(str))
                以 str 为分隔符截取字符串，如果 num 有指定值，则仅截取 num+1 个子字符串
                str -- 分隔符，默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等
                num -- 分割次数。默认为 -1, 即分隔所有
                返回分割后的字符串列表（是一个列表结构）
                例：
                    >>> "C:/1/a.txt".split("/",0)
                    ['C:/1/a.txt']
                    >>> "C:/1/a.txt".split("/",1)　　
                    ['C:', '1/a.txt']       #只处理完第 1 个分隔符，后面的分隔符不再处理
                    >>> "C:/1/a.txt".split("/",2)
                    ['C:', '1', 'a.txt']
                    >>> file="C:/dir1/dir2/dir3/aa.txt"
                    >>>file.split("/")[-1] 
                    aa.txt
            32	splitlines([keepends])
                按照行('\r', '\r\n', '\n')分隔，返回一个包含各行作为元素的列表，
                如果参数 keepends 为 False，不包含换行符，如果为 True，则保留换行符。
            33	startswith(substr, beg=0,end=len(string))
                检查字符串是否是以指定子字符串 substr 开头，是则返回 True，
                否则返回 False。如果beg 和 end 指定值，则在指定范围内检查。
            34	strip([chars])
                在字符串上执行 lstrip()和 rstrip()
            35	swapcase()
                将字符串中大写转换为小写，小写转换为大写
            36	title()
                返回"标题化"的字符串,就是说所有单词都是以大写开始，
                其余字母均为小写(见 istitle())
            37	translate(table, deletechars="")
                根据 table 给出的表(包含 256 个字符)转换 string 的字符, 
                要过滤掉的字符放到 deletechars 参数中
            38	upper()
                转换字符串中的小写字母为大写
            39	zfill (width)
                返回长度为 width 的字符串，原字符串右对齐，前面填充0
            40	isdecimal()
                检查字符串是否只包含十进制字符，如果是返回 true，否则返回 false。
    .元组类型：
        元组（tuple）与列表类似，不同之处在于元组的元素不能修改。
        元组写在小括号 () 里，元素之间用逗号隔开
        元组中的元素类型也可以不相同
        虽然tuple的元素不可改变，但它可以包含可变的对象，比如list列表
        跟字符串或列表一样，也支持加法和乘法运算
        可以使用len(元组)，对元组求长度
        易错点注意：
            当赋值仅有一个元素的元组时，要特别注意写法
            tup0 = ('abc')   
            这是错的，此时的括号被认作是优先级运算符，这里的tup0实际是字符串
            tup1 = ('abc',)
            这例的tup1才是真正的元组类型
        举例：
            tup = (1, 2, 3, 4, 5, 6)  #也可写为tup=1,2,3,4,5,6  因为会自动封包
            tup[0] = 11  # 报错，操作非法，不可修改
            tup1 = ()    # 空元组
            tup2 = (20,) # 一个元素，需要在元素后添加逗号，否则会被当作运算符使用
        .索引：
            元组、列表具有同字符串一样的下标索引方式：[起始位置:结束位置:步进量]
            起始位置:结束位置:步进量，这三个都是可省略的
            如: [:]  <==>  [0:-1]
        .作为参数或函数的返回值：
            一般来说，函数的返回值一般为一个。
            而函数返回多个值的时候，通常借助元组的方式返回（也可以是list等）
                return (a,b)  #返回的是元组
                return a,b    #返回的是元组
                return [a,b]  #返回的是列表
            python中的函数还可以接收可变长参数，比如以 "*" 开头的的参数名，
            它会将所有的参数收集到一个元组上
            如：def test(*args):
                    print(type(args)) # 输出：<class 'tuple'>
        .嵌套
            元组中的元素不仅可以是元组（自嵌套），还可以是列表、集合、字典等
            当这些可修改对象作为元组的元素时，所谓的元组元素不可修改，
            指的是该列表/集合/字典元素所引用的位置（指向的对象地址）不可修改，
            但该列表/集合/字典元素所指向的内存对象（中的子元素）仍是可修改的
            例：
                >>> tp=(1,2,['a','b','c'])
                >>> tp[2][0]='x'
                >>> tp
                (1, 2, ['x', 'b', 'c'])
        .元组复制
            tp1=(1,2,3)
            tp2=()          # id(tp2) != id(tp1)
            tp2=tp1         # id(tp2) == id(tp1)
            tp2=tp1[:]      # id(tp2) == id(tp1) ,这是与列表不同的地方
            #tp1[:] 等同于 tp1[0:-1]，实际是返回了一个新元组，只是这个新元祖与之前的一致，
            #而根据元组的特点，如果两个元组一致，则实际引用同一个对象
        .内置函数
            1	len(tuple)
                计算元组元素个数。	
            2	max(tuple)
                返回元组中元素最大值。	
            3	min(tuple)
                返回元组中元素最小值。	
            4	tuple(iterable)
                将可迭代对象转换为元组（有点强制类型转换的意思）。
        .装包与解包
            >>> tp1=1,2,3,4     # 自动装包，等价于 tp1=(1,2,3,4)
            >>> tp1
            (1, 2, 3, 4)
            >>> i1,i2,i3,i4=tp1 # 自动解包，经测试，列表、range等可迭代对象都可以自动解包
            >>> print(f'i1={i1},i2={i2},i3={i3},i4={i4}')
            i1=1,i2=2,i3=3,i4=4
            当函数return的时候，其实只能return一个值，并不能return多个值
            有人会问，我return了多个值也没有报错啊，运行很正常
            那正是因为Python将多个返回值自动装包造成的
            因此当你返回多个变量，而外面只用一个变量去接收，会接收到一个元组
            而当你用多个变量去接，就能对应的接收到每个值，这是因为自动拆包
    .列表类型：
        列表是写在方括号 [] 之间、用逗号分隔开的元素列表
        列表中元素的类型可以不相同，它支持数字，字符串甚至可以包含列表
        列表支持与字符串一样的索引方法：变量[头下标:尾下标:步长]
        列表与字符串一样，也支持加法和乘法运算，进行列表拼接或重复
        支持split、join等成员方法
        .修改列表
            因为列表属于可变数据类型，所以可以对列表的元素重新指定新的值
            如：list = ['Google', 'Runoob', 1997, 2000]
            list[2] = 1996      #修改
            list.append("xxx")  #追加
            del list[0]         #删除
            于是，list 变为 ['Runoob', 1996, 2000, 'xxx']
        .嵌套列表
            >>>a = ['a', 'b', 'c']
            >>> n = [1, 2, 3]
            >>> x = [a, n]
            >>> x
            [['a', 'b', 'c'], [1, 2, 3]]
            >>> x[0]
            ['a', 'b', 'c']
            >>> x[0][1]
            'b'
        .列表复制
            >>> a = [1, 2, 3]
            >>> b = a           # id(a) == id(b)
            >>> c = []          # id(c) != id(a)
            >>> c = a           # id(c) == id(a)
            >>> d = a[:]        # id(d) != id(a)
            >>> e = a.copy()    # id(e) != id(a)
        .列表遍历
            # 正序遍历：
            list01 = ["Googl",'Runoob',1997,2002]
            for item in list01:             #用法1
                print(item)
            for i in range(len(list01)):    #用法2    
                print(list01[i])
            # 反向遍历
            for i in range(len(list01)-1,-1,-1):    
                print(list01[i])
        .部分函数&方法
            1	len(list)  # len 对字符串、元组、列表等都有效
                列表元素个数
            2	max(list)
                返回列表元素最大值
            3	min(list)
                返回列表元素最小值
            4	list(seq)  #强转
                将元组转换为列表，经测试，seq只要是可迭代对象，就可以转换为列表
            1	list.append(obj)
                在列表末尾添加新的对象
                >> l1=[1,2,3]
                >> l1.append([4,5,6])
                >> print(f"l1={l1}")
                [1,2,3,[4,5,6]]
            2	list.count(obj)
                统计某个元素在列表中出现的次数
            3	list.extend(seq)
                在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
                >> l2=[1,2,3]
                >> l2.extend([4,5,6])
                >> print(f"l2={l2}")
                [1,2,3,4,5,6]
            4	list.index(obj)
                从列表中找出某个值第一个匹配项的索引位置
            5	list.insert(index, obj)
                将对象插入列表
            6	list.pop([index=-1])
                移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
            7	list.remove(obj)
                移除列表中某个值的第一个匹配项
            8	list.reverse()
                反向列表中元素
            9	list.sort( key=None, reverse=False)
                对本列表进行排序
            10	list.clear()
                清空列表
            11	list.copy()
                复制列表
    .集合类型：  #集合是一种比列表约束性更强的类型
        可以使用大括号 { } 或者 set() 函数创建集合，
        集合中的元素可以无序，但不可以重复（会自动合并重复，并自动排序），
        另外，元素必需是不可变类型
        要想实现集合的嵌套，可借助frozenset方法
        注意：
            创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典
            set中的元素内部会自动排序，如
            set1={1,2,5,4}  对set1输出的结果为：{1, 2, 4, 5}
        格式：parame = {value01,value02,...} 或 set(value)
        因为会自动排序，所以与字符串、列表、元组不同，集合不支持通过[]进行下标索引
        集合支持 -(差集) |(并集) &(交集) ^(并集-交集) 等运算，他们有相同的运算优先级
        # 因为不支持下标运算，且其元素必须是不可变类型，所以这限制了其使用范围
        # 其更像是为了专门处理 “集合” 这个数学上的数据类型而专门设计的
        使用举例：
            a = set('abracadabra')
            b = set('alacazam')
            print(a - b)     # a 和 b 的差集
            print(a | b)     # a 和 b 的并集
            print(a & b)     # a 和 b 的交集
            print(a ^ b)     # a 和 b 中不同时存在的元素
        .内置方法：
            1.  add(elmnt)	
                为集合添加元素
            2.  clear()	
                移除集合中的所有元素
            3.  copy()	
                拷贝一个集合
            4.  difference(set)	
                返回与set集合的差集
                例：
                    x = {"apple", "banana", "cherry"}
                    y = {"google", "microsoft", "apple"}
                    z = x.difference(y)   
                    z 输出为：{'cherry', 'banana'}， 等价于 z = x - y
            5.  difference_update(set)	    
                移除在set集合中也存在的元素（set集合的差集），
                并更新到原集合中，无输出
                例：set1.difference_update(set2) 
                结果等于 set1 = set1-set2，但两者存在不同，
                前者是在原集合上修改，后者是赋值了一个新集合
            6.  discard(value)	
                删除集合中指定的元素
            7.  intersection()	
                返回集合的交集,等价于运算符&
            8.  intersection_update()
                与intersection_update相比，无返回，而是更新到原集合中            
                与difference_update类似，不过这里交集运算
            9.  isdisjoint(set)	
                判断两个集合是否包含相同的元素，
                如果没有返回 True，否则返回 False。
                disjoint：不相交的
            10. issubset(set)	
                判断当前集合是否为参数集合的子集。
            11. issuperset(set)	
                判断参数集合是否为当前集合的子集（即当前集合是否为参数集合的父集）
            12. pop()	
                删除（内部自动按升序排序后的）第1个元素，返回移除的元素
            13. remove(item)	
                移除指定元素，没有返回值
            14. symmetric_difference()	
                返回两个集合中不重复的元素集合，等价于^运算
            15. symmetric_difference_update()	
                与symmetric_difference相比，无返回，而是更新到当前集合中
                与difference_update类似，不过这里是^运算
            16. union(set1[, set2...])	
                返回当前集合与参数指定集合的并集，等价于 | 运算
            17. update()	#实际是union_update
                与union相比，无返回，而是更新到当前集合中
                与difference_update类似，不过这里是并集运算
        .使用注意事项：
            set1.update( "字符串" ) 与 set1.update( {"字符串"} ) 含义不同
            set1.update( "字符串" ) 是将字符串拆分单个字符后，
            然后再一个个添加到集合中，有重复的会忽略。
            实际这一步暗含了'解包'操作："字符串"可迭代对象被分解为一个个的字符
            >>> from collections import Iterable
            >>> isinstance("asdf", Iterable)
            返回True，证明字符串为可迭代对象
            其他因为字符串可迭代对象导致的、容易出错的地方：
            >>> set1 = set('abc')     #set1为：{'a', 'b', 'c'}，字符串自动解包了
            >>> set1 = set(('abc'))   #set1为：{'a', 'b', 'c'}，还是对字符串解包
            >>> set1 = set(('abc',))  #set1为：{'abc'}，这次是对元组解包
            >>> set1=set({'abc'})     #set1为：{'abc'}，对集合解包
            >>> set1 = ['abc']        #set1为：['abc']
            >>> set1 = ['abc']        #set1为：['abc']
            >>> tup1 = ('abc')        #tup1为：'abc'，可见这里的tup1实为字符串类型
            >>> tup1 = ('abc',)       #tup1为：('asdf',),这时tup1才是真正的元组类型
    .字典类型：
        字典是一种映射类型，字典用 { } 标识，它是一个无序的 键(key) : 值(value) 的集合
        字典跟列表具有可比性：列表中的元素是通过偏移来存储的，字典中的元素是通过键来存取的
        键(key)必须使用不可变类型，且在同一个字典中，键(key)必须是唯一的，但值不必唯一
        一个字典中可以同时存在不同类型的键（只要是不可变类型就行）
        值可以取任何数据类型，但键必须是不可变的，如字符串，数字
        构造函数 dict() 可以直接从键值对序列中构建字典
        .使用举例：
            dic = {}
            dic['one'] = "1 - 菜鸟教程"  #如果没有，就自动添加新的元素
            dic[2]     = "2 - 菜鸟工具"  #key只要是不可变类型即可，字符串、数字、元组，都是不可变类型
            dic[(1,2,3)] = "3 - 菜鸟编程"
            dic2 = {'name': 'runoob','code':1, 'site': 'www.runoob.com'}
            print (dic['one'])       # 输出键为 'one' 的值
            print (dic[2])           # 输出键为 2 的值
            print (dic2)             # 输出完整的字典
            print (dic2.keys())      # 输出所有键（返回值为dict_keys类型)
            print (dic2.values())    # 输出所有值（返回值为dict_values类型)
            print (dic2.items())     # 输出所有键值对（返回值为dict_items类型)
            dic = dict([('Runoob', 1), ('Google', 2), ('Taobao', 3)]) # 将二元元组的列表，强转为字典
                等同于：
                tup1=('Runoob', 1)
                tup2=('Google', 2)
                tup3=('Taobao', 3)
                lst=[tup1,tup2,tup3]    
                dic=dict(lst)        # 从元组列表(强转)构建
            del dic['Runoob']        # 删除字典中的元素（键值对）
            dic.clear()              # 清空
            del dic                  # 删除字典
        .部分内置函数&方法
            1	len(dict)
                计算字典元素个数，即键的总数。	
            2	str(dict)
                输出字典，可以打印的字符串表示。	
            3	type(variable)
                返回输入的变量类型，如果变量是字典就返回字典类型。
            1	dict.clear()
                删除字典内所有元素
            2	dict.copy()
                返回一个字典的浅复制(返回一个新字典对象，但字典中的元素，仍引用的原对象)
            3	dict.fromkeys((seq[, value])
                创建一个新字典，以序列seq中元素做字典的键，
                val为字典所有键对应的初始值,默认为None
            4	dict.get(key, default=None)
                返回指定键的值，如果键不在字典中返回 default 设置的默认值，
                类似于下标运算法，不过可以指定默认值
            5	key in dict
                如果键在字典dict里返回true，否则返回false
            6	dict.items()
                以列表返回一个视图对象dict_items
            7	dict.keys()
                返回一个视图对象dict_keys
            8	dict.setdefault(key, default=None)
                和get()类似, 但如果键不存在，将会添加键，并将值设为default
                返回值为该键对应的值
            9	dict.update(dict2)
                把字典dict2的键/值对更新到dict里
            10	dict.values()
                返回一个视图对象dict_values
            11	pop(key[,default])
                删除字典给定键 key 所对应的值，返回值为被删除的值。
                key值必须给出。 否则，返回default值。
            12	popitem()
                返回并删除字典中的最后一对键和值。
        .使用举例：
            将字典中的键和值互换：
                >>> dic = {'a': 1,'b': 2,'c': 3}
                >>> reverse = {v: k for k, v in dic.items()}  # 推导式
                #每次item赋值给k,v时，会发生解包
            通过 values 取到 key 的方法：
                >>> dic={"a":1,"b":2,"c":3}
                >>> list(dic.keys())[list(dic.values()).index(1)]
                注：
                    list(dic.keys())  将 dic.keys() 强转为 list
                    list(dic.values())  将 dic.values() 强转为 list
                    lst1 = list(dic.keys())
                    lst2 = list(dic.values())
                    idx = lst2.index(1)  # 值 1 对应的索引序号
                    lst1[idx]   #得到 idx 对应的 key 的名字
    .Python数据类型转换：
        int(x [,base])          将x转换为一个整数
        float(x)                将x转换到一个浮点数
        complex(real [,imag])   创建一个复数
        str(x)                  将对象 x 转换为字符串
        repr(x)                 将对象 x 转换为表达式字符串
            repr(object) ：返回一个对象的 string 格式，如：
            >>> s = 'RUNOOB'
            >>> repr(s)
            "'RUNOOB'"
            >>> dict = {'runoob': 'runoob.com', 'google': 'google.com'};
            >>> repr(dict)
            "{'google': 'google.com', 'runoob': 'runoob.com'}"
        eval(str)               用来计算在字符串中的有效Python表达式,并返回一个对象
            语法：eval(expression[, globals[, locals]])
            >>> x = 7
            >>> eval( '3 * x' )
            21
            >>> eval('pow(2,2)')
            4
            >>> eval('2 + 2')
            4
            >>> eval("n + 4")
            11
        tuple(s)                将序列 s 转换为一个元组
        list(s)                 将序列 s 转换为一个列表
        set(s)                  转换为可变集合
        dict(d)                 创建一个字典。d 必须是一个 (key, value)元组序列。
        frozenset(s)            转换为不可变集合
            class frozenset([iterable])
            iterable ：可迭代对象
                可迭代对象指存储了元素的一个容器对象，
                该容器中的元素可以通过__iter__( )方法或__getitem__( )方法访问
                常见的可迭代对象包括：
                a) 集合数据类型，如list、tuple、dict、set、str等；
                b) 生成器(generator)
                可以通过collections模块的Iterable类型判断是否为可迭代的对象：
                >>> from collections import Iterable
                >>> isinstance(变量, Iterable) #返回布尔
            返回新的 frozenset 对象
            如果不提供任何参数，默认会生成空集合
            >>>a = frozenset(range(10))     # 生成一个新的不可变集合
            >>> a
            frozenset([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> b = frozenset('runoob') 
            >>> b
            frozenset(['b', 'r', 'u', 'o', 'n'])   # 创建不可变集合
        chr(x)                  将一个整数转换为一个字符
        ord(x)                  将一个字符转换为它的整数值
        hex(x)                  将一个整数转换为一个十六进制字符串
        oct(x)                  将一个整数转换为一个八进制字符串
    .推导式：
        列表推导式：[表达式 for 变量 in 可迭代对象]  或  [表达式 for 变量 in 可迭代对象 if 条件]
        元组推导式：(表达式 for 变量 in 可迭代对象)  或  (表达式 for 变量 in 可迭代对象 if 条件)
        集合推导式：{表达式 for 变量 in 可迭代对象}  或  {表达式 for 变量 in 可迭代对象 if 条件}
        字典推导式：{表达式:表达式 for 变量 in 可迭代对象}  或
                    {表达式：表达式 for 变量 in 可迭代对象 if 条件}
        条件：
            对变量或变量的表达式进行判断，当该条件表达式为假时，滤除该变量
        常用的可迭代对象：    
            经常简单使用range()方法获得可迭代对象：
            range([start,] stop[, step])
            返回一个由整数元素组成的range对象，该对象像列表一样，可迭代
            start默认为0，step默认为1
        功用：
            列表推导式的用途是简便的创建一个列表对象
            元组推导式的用途是简便的创建一个元组对象
            集合推导式的用途是简便的创建一个集合对象
            字典推导式的用途是简便的创建一个字典对象
        举例：
            写一段代码生成1到100之间的数字的平方的列表，答案是：
            1, 4, 9, 16, ...
            nums = [i*i for i in range(1, 101)]
            类似于：
                nums = []
                for i in range(1, 101): nums.append(i*i)
    .运算符：
        .算术运算符
            +	加        - 两个对象相加	a + b 输出结果 31
            -	减        - 得到负数或是一个数减去另一个数	a - b 输出结果 -11
            *	乘        - 两个数相乘或是返回一个被重复若干次的字符串	a * b 输出结果 210
            /	除        - x 除以 y	b / a 输出结果 2.1
            %	取模      - 返回除法的余数	b % a 输出结果 1
            **	幂        - 返回x的y次幂	a**b 为10的21次方
            //	取整除    - 向下取接近商的整数
        .比较（关系）运算符
            ==	等于      - 比较对象是否相等	(a == b) 返回 False。
                            默认会调用对象的__eq__()成员方法
            !=	不等于    - 比较两个对象是否不相等	(a != b) 返回 True。
            >	大于      - 返回x是否大于y	(a > b) 返回 False。
            <	小于      - 返回x是否小于y。所有比较运算符返回1表示真，返回0表示假。
                            这分别与特殊的变量True和False等价。
                            注意，这些变量名的大写。(a < b) 返回 True。
            >=	大于等于  - 返回x是否大于等于y。	(a >= b) 返回 False。
            <=	小于等于  - 返回x是否小于等于y
        .赋值运算符
            =	简单的赋值运算符	c = a + b 将 a + b 的运算结果赋值为 c
            +=	加法赋值运算符	    c += a 等效于 c = c + a
            -=	减法赋值运算符	    c -= a 等效于 c = c - a
            *=	乘法赋值运算符	    c *= a 等效于 c = c * a
            /=	除法赋值运算符	    c /= a 等效于 c = c / a
            %=	取模赋值运算符	    c %= a 等效于 c = c % a
            **=	幂赋值运算符	    c **= a 等效于 c = c ** a
            //=	取整除赋值运算符	c //= a 等效于 c = c // a
            :=	海象运算符，可在表达式内部为变量赋值（Python3.8 版本新增）
                海象运算符，英文原名叫 Assignment Expressions，
                翻译过来也就是 赋值表达式，不过因为其样子像海象，所以称为海象运算符
                = 运算符没有返回值（这点不用于c/c++），海象运算符有返回值
                所以海象运算符可以在完成赋值后，继续参与运算
                if (n := len(a)) > 10:
                    print(f"List is too long (expected <= 10)")
        .逻辑运算符
            x and y	布尔"与" - 如果 x 为 False，x and y 返回 x 的值，否则返回 y 的计算值。	
            x or y	布尔"或" - 如果 x 是 True，它返回 x 的值，否则它返回 y 的计算值。	
            not x	布尔"非" - 如果 x 为 True，返回 False 。如果 x 为 False，它返回 True。
            例：a=10;b=20;  (a and b) 返回 20，(a or b) 返回 10，(not a) 返回 False
            拓展：print("a") and print("b")   输出 "a"
                  开关语句：
                      a and b or c
                      a 为真时，执行 b，a 为假时，执行 c
                  type(print("a")) 返回对象 <class 'NoneType'> , 
                  该对象用作表达式时，被认定为假（即print()没有返回值，或说返回值为 None，为假）
                  除此之外，空列表、空字典、空元组、空字符串等，用于逻辑表达式时，也会被认定为假
                  进一步测试，如果自定义的函数，没有返回值，则等同于该函数返回了 NoneType 类型
                  常量/关键词 None 即为 NoneType 类型对象，常用其表征 null 对象，函数默认返回 None
                  定义时，函数的参数可以指定默认值为 None
                  在正则表达式中，如果没有匹配到对象，也是返回 None
                  None因为是内置对象，所以是单例的，True、False、小整数等，也都是单例对象
        .位运算符
            &	按位与运算符
            |	按位或运算符
            ^	按位异或运算符
            ~	按位取反运算符
            <<	左移动运算符（非循环）
            >>	右移动运算符（非循环）
        .成员运算符
            in	如果在指定的"序列"中找到值返回 True，否则返回 False。	
            not in	如果在指定的"序列"中没有找到值返回 True，否则返回 False。
            例： 3 in [1,2,3] 返回 True， 4 not in [1,2,3] 返回 True
            参：@序列与可迭代对象
        .身份运算符
            is	是判断两个标识符是不是引用自一个对象， x is y, 类似 id(x) == id(y) 
                如果引用的是同一个对象则返回 True，否则返回 False
            is not	是判断两个标识符是不是引用自不同对象， x is not y ，类似 id(x) != id(y)
                如果引用的不是同一个对象则返回结果 True，否则返回 False。
        .运算符优先级
            **	指数 (最高优先级)
            ~ + -	按位翻转, 一元加号和减号 (最后两个的方法名为 +@ 和 -@)
            * / % //	乘，除，求余数和取整除
            + -	加法减法
            >> <<	右移，左移运算符
            &	位 'AND'
            ^ |	位运算符
            <= < > >=	比较运算符
            == !=	等于运算符
            = %= /= //= -= += *= **=	赋值运算符
            is, is not	身份运算符
            in, not in	成员运算符
            not and or	逻辑运算符
            记忆： 指单基移位比等,赋值is in逻辑 （跟c/c++的有区别）
    .常用数学函数：
        .运算函数：
            abs(x)	        返回数字的绝对值，如abs(-10) 返回 10
            ceil(x)	        返回数字的上入整数，如math.ceil(4.1) 返回 5
            cmp(x, y)       如果 x < y 返回 -1, 如果 x == y 返回 0, 如果 x > y 返回 1。 
                            Python 3 已废弃，使用 (x>y)-(x<y) 替换。
            exp(x)	        返回e的x次幂(ex),如math.exp(1) 返回2.718281828459045
            fabs(x)	        返回数字的绝对值，如math.fabs(-10) 返回10.0
            floor(x)	    返回数字的下舍整数，如math.floor(4.9)返回 4
            log(x)	        如math.log(math.e)返回1.0,math.log(100,10)返回2.0
            log10(x)	    返回以10为基数的x的对数，如math.log10(100)返回 2.0
            max(x1, x2,...)	返回给定参数的最大值，参数可以为序列。
            min(x1, x2,...)	返回给定参数的最小值，参数可以为序列。
            modf(x)	        返回x的整数部分与小数部分，两部分的数值符号与x相同，整数部分以浮点型表示。
            pow(x, y)	    x**y 运算后的值。
            round(x [,n])	返回浮点数 x 的四舍五入值，如给出 n 值，则代表舍入到小数点后的位数。
                            其实准确的说是保留值将保留到离上一位更近的一端。
                            round(10.5)返回10，round(11.5)返回12，
                            规律为'4舍6入5看齐,奇入偶不入'，国标也已经规定使用这种方式取代"四舍五入"
                            从统计学的角度上来讲,如果大量数据无脑的采用四舍五入会造成统计结果偏大。
                            而"奇进偶舍"可以将舍入误差降到最低
            sqrt(x)     	返回数字x的平方根。
        .随机数函数：
            choice(seq)	    从序列的元素中随机挑选一个元素，
                            比如random.choice(range(10))，从0到9中随机挑选一个整数。
            randrange ([start,] stop [,step])	
                            从指定范围内，按指定基数递增的集合中获取一个随机数，基数默认值为 1
            random()	    随机生成下一个实数，它在[0,1)范围内。
            seed([x])	    改变随机数生成器的种子seed。
                            如果你不了解其原理，你不必特别去设定seed，Python会帮你选择seed。
            shuffle(lst)	将序列的所有元素随机排序
            uniform(x, y)	随机生成下一个实数，它在[x,y]范围内。
            rand
        .三角函数：
            acos(x)	        返回x的反余弦弧度值。
            asin(x)	        返回x的反正弦弧度值。
            atan(x)	        返回x的反正切弧度值。
            atan2(y, x)	    返回给定的 X 及 Y 坐标值的反正切值。
            cos(x)	        返回x的弧度的余弦值。
            hypot(x, y)	    返回欧几里德范数 sqrt(x*x + y*y)。
            sin(x)	        返回的x弧度的正弦值。
            tan(x)	        返回x弧度的正切值。
            degrees(x)	    将弧度转换为角度,如degrees(math.pi/2) ， 返回90.0
            radians(x)	    将角度转换为弧度
        附注： 上面绝大多数函数都不是内置函数，需引入特定的模块后才能使用
    .变量的作用域：
        python中变量的作用域及用法，同C语言有很大的差别
        .变量的五种作用域：
            L = Local     #局部作用域
                定义在函数体内的变量，默认都是局部变量
            E = Enclosing #外部嵌套函数作用域
                python函数内部，支持继续定义函数（这是C语言所不具有的）
                如果函数f1内，又定义了函数f2，则f1是f2的外部嵌套函数
            N = nonlocal  只作用于嵌套作用域，而且只是作用在函数里面
            G = global    #全局作用域（即模块作用域）
                global与local、enclosing等不同，他是一个python的内置关键字
                在模块级别定义的变量，自然成为全部变量，无需使用关键字global
                那global什么时候使用呢？现在考虑如下一个问题：
                在函数体内使用变量（为变量赋值）时，如果外层存在同名变量，
                则会自动覆盖外层的同名变量，并形成一个新的局部变量，
                那如果想在函数体内引用/修改外层变量，该怎么办？
                答案就是使用 'global 外层变量名' 
                告诉编译器不要再为该变量产生局部变量了
            B = Built-in  #Python内置作用域
            python引用/查找变量的顺序： L -> E -> G -> B
        注意：
            只有模块，类以及函数(包括lambda)才会引入新的作用域
            if、for、while、try-except等语句块并不形成作用域
            当当前作用域中找不到某个变量时，会自动去外层作用域中继续查找（效率？）
            函数在查找全局作用域的变量时，不仅会查找定义在该函数之前的变量
            还会查找定义在该函数之后的变量
        以下参： https://zhuanlan.zhihu.com/p/103164544
        与C语言的不同：
            1. 不存在语句块作用域，如 if for while等不会产生作用域
            2. 如果本层作用域中不存在某变量，会一级一级向外层作用域查找
               其实这一点跟C语言是一样的
               我们在写Python的时候，发现在函数中可以直接使用函数外定义的变量
               这是因为这些"函数外的变量"。其实相当于C语言中的全局变量
               另外，Python函数内支持嵌套子函数，这是C语言所不具有的功能
               所以在Python中还会涉及内层函数访问外层函数变量的问题（嵌套作用域）
            3. Python中，在函数作用域中，没法做到又访问外部变量，又使用与该外部变量同名的局部变量
               例如，在 C 中，如下代码是可以的：
               int g=3;
               void func()
               {
                  printf("g=%d\n",g);
                  int g=5;
                  printf("g=%d\n",g);
               }
               但在Python中，想达到同样的效果，则代码应写为：
               g=3
               def func():
                  # global g
                  print("g=%d"%g)
                  g=5
                  print("g=%d"%g)
               如果不加 global g 这一句，则调用该函数时会报错，提示变量不能在定义前被引用
               如果加上 global g 这一句，则所有的修改又全是对外部变量的修改，内部不会自动创建同名的局部变量了
               而Python中也没有 local 关键字，所以，目前看来，Python无法达到如上面 C代码 同样的功能
            4. 内层函数访问外层函数变量的问题（嵌套作用域）
               这是Python因为支持函数嵌套，才会面临的情况
               在嵌套函数中，使用 'nonlocal 变量名' 标明：如果该作用域内，使用了与外层同名变量的变量，
               则不是对该变量重新定义赋值，而是使用的'紧邻的'上一层作用域的那个变量，
               如果'紧邻的'上一层没有这个变量，则在向上层找，直到找到这个变量，如果最终找不到这个变量，则会报错
               nonlocal和global是不同的，global是一下子找到全局作用域那一层，而nonlocal则优先只向上找一层
        与C语言的相同点：
            1. 都有函数作用域，在函数作用域可以定义使用与外部作用域同名的变量，而不会影响外部作用域的变量值
               且在函数作用域定义的变量，出了该函数作用域，就不可访问了    
    .流程控制：
        .if-elif-else 
            语法：
            if 表达式1:
                语句
            elif 表达式2:
                语句
            else:
                语句
            表达式部分不必有括号，但表达式最后的冒号是必须的，
            python以此（冒号结尾）判断不是个完整的句子。
            如果 if 语句中的条件过长，可以用接续符 \ 来换行
            \ 后的一行要缩进没有要求，可无序缩进
            下表列出了不同数值类型的 true 和 false 情况：
            类型	False	                True
            布尔	False(与0等价)	        True(与1等价)
            数值	0, 0.0	                非零的数值
            None	None	                非None对象
            字符串	'', ""(空字符串)	    非空字符串
            容器	[],  (),  {},  set()	至少有一个元素的容器对象
        .while-else
            语法：
            while 判断条件：
                执行语句
            else：
                执行语句
            在 Python 中没有 do..while 循环，else部分不是必需的
            else 语句只有在 while 正常循环完的条件下，才会执行
            如果 while 中遇到了 break，就不会执行 else 了
            举例：
                while count < 5 :
                    count++
                    print(count)
                else:
                    print(finish)
        .for-in-else
            语法：
            for 变量 in 序列:
                执行语句
            else:
                执行语句
            注：else部分不是必需的，else语句只有在正常循环完的条件下，才会执行
            提示：因为python支持自动封包/解包，所以for语句中，变量可以为多个
            当想使用for完成固定次数的循环时，可搭配range()函数使用，如：
            for i in range(5):  
            range函数语法：range([start,] stop[, step])
            返回一个由整数元素组成的range对象，该对象像列表一样，可迭代
            start默认为0，step默认为1
        .while/for语句后的else有什么用：
            对于while语句，之后当条件不满足（正常结束循环）时，才会执行else语句部分
            对于for语句，只有在枚举序列完结（正常结束循环）时，才会执行else语句部分
            从上可见，else部分都是在正常循环完成会，才会执行到
            这和直接在while/for句式结束后书写普通语句有什么区别？else是不是很鸡肋？
            其实不然，else语句部分的执行是有条件的：之后在循环正常完结，
            即while条件不满足后，或for枚举完结后，即循环正常结束后，else才会执行，
            如果是因为break语句导致的不正常完结，else部分是不会执行的
            所以我们可以在else部分书写一些只有在循环正常结束后，才允许执行的句子
        .break:
            break 语句可以跳出 for 和 while 的循环体。
            如果你从 for 或 while 循环中终止，任何对应的循环 else 块将不执行
        .continue:
            continue 语句被用来告诉 Python 跳过当前循环块中的剩余语句，然后继续进行下一轮循环
        .pass:
            pass是空语句，不做任何事情，一般用做占位语句，是为了保持程序结构的完整性。
            如想使用一个空循环进行等待，可以用：while True: pass
            或如 if x>1 : pass #需要对x>1的情况进行处理，但具体该怎么做先临时空着，待完成
        .python不支持switch-case句法
            可以用函数字典技术，完成 switch-case 的功能
    .迭代器与生成器：
        迭代器函数iter()：
            iter内建函数语法：iter(object[, sentinel]) 
            返回一个iterator对象
            如果不使用第2个参数时，第一个参数必需是个集合对象，
            且该集合对象要么支持枚举（有__iter()__成员方法），
            要么支持按按序获取（有__getitem(index)__成员方法）
            否则会引发TypeError异常
            而
    .可迭代对象、序列、迭代器、生成器 
        https://blog.csdn.net/qq_23981335/article/details/105110398
        &<序列与可迭代对象>  
        可迭代对象（Iterable）、
        序列（Sequence）、
        迭代器（Iterator）、
        生成器（generator） 
    .序列 &<序列>
        .序列的定义
             .Python 序列（Sequence）是指按特定顺序依次排列的一组数据，
              它们可以占用一块连续的内存，也可以分散到多块内存中。
              Python 中的序列类型包括字符串、列表、元组、字典和集合。
             .列表（list）和元组（tuple）比较相似，都按顺序保存元素，
              所有的元素占用一块连续的内存，每个元素都有自己的索引，
              因此列表和元组的元素都可以通过索引（index）来访问
             .字典（dict）和集合（set）存储的数据都是无序的，
              每份元素占用不同的内存
        .序列支持的操作
            #注：集合和字典不支持索引、切片、相加、相乘操作
            1. 序列索引
                序列中每个元素都有属于自己的编号（索引）。
                从起始元素开始，索引值从 0 开始递增
                还支持索引值是负数，最后一个元素的索引是-1，
                倒数第二个元素的索引是-2，以此类推
            2. 序列切片
                语法格式：sequence[start : end : step]
            3. 序列相乘
                使用数字 n 乘以一个序列会生成新的序列，
                其内容为原来序列被重复 n 次的结果
            4. 检查元素是否包含在序列中
                ython 中可以使用 in 关键字检查某元素是否为序列的成员，
                其语法格式： value in sequence ， value 为要检查的元素值
                not in 和 in 关键字用法相同，功能恰好相反
            5. 和序列相关的内置函数
                Python提供了几个内置函数用于实现与序列相关的一些常用操作
                函数	    功能
                len()	    计算序列的长度，即返回序列中包含多少个元素。
                max()	    找出序列中的最大元素。
                            注意，对序列使用 sum() 函数时，
                            做加和操作的必须都是数字，不能是字符或字符串，
                            否则该函数将抛出异常，
                            因为解释器无法判定是要做连接操作
                            （+ 运算符可以连接两个序列），还是做加和操作。
                min()	    找出序列中的最小元素。
                list()	    将序列转换为列表。
                str()	    将序列转换为字符串。
                sum()	    计算元素和。
                sorted()	对元素进行排序。
                reversed()	反向序列中的元素。
                enumerate()	将序列组合为一个索引序列，多用在 for 循环中。              
        @自定义序列
.Python从菜鸟到高手（第2版）
    源码位置： file://python从菜鸟到高手 代码
    .类和对象
        .成员函数
            每个方法的第1个参数都是self，其实这是必需的。
            这个参数名不一定叫self（可以叫abc或任何其他名字），
            但任意一个方法必须至少指定一个self参数，
            如果方法中包含多个参数，第1个参数将作为self参数使用。
            在调用方法时，这个参数的值不需要自己传递，
            系统会将方法所属的对象传入这个参数。
            在方法内部可以利用这个参数调用对象本身的资源，如属性、方法等。
            也可以为对象添加、设置新的属性、方法等
            注意：类的成员函数不支持重载
            例 : 通过 self 为类增添新的属性、方法：                
                class A:
                    def set_src(self, s):
                        self.src = s
                    def get_src(self):
                        return self.src
                    def aa(self):
                        "调用了该函数后，可以为 A 增添一个新的成员方法"
                        def a1(v):  # 内部方法不带 self 参数，但可以方外部的 self
                            print("val = {}，src = {}".format(v,self.src))
                        self.f_a1 = a1
                a=A()         #创建类对象
                a.set_src("A")
                a.aa()        # 调用过该函数后，a.f_a1() 才可用
                a.f_a1("ab")  # 注1
                a.src = 4567  # 可以通过变量直接访问/添加 src 属性
                a.f_a1(12)
                注1：
                    虽然函数内嵌函数 a1() 在写法上没有 self 参数，
                    但该函数仍然可以被类对象直接调用，
                    说明 self 参数也传给 a1() 函数了，
                    所以可以退出，a1() 函数也接受 self 参数，
                    只是无需像普通成员函数一样，明显的写出来
        .通过类创建对象
            使用类创建对象的方式与调用函数的方式相同
            如 
               class A:
                   ...
               a = A()
        .调用成员方法   &<调用类的成员方法>
            法1. 直接通过对象调用方法，
            法2. 通过类调用方法，并且将相应的对象传入方法的第1个参数。 
            使用 dir(对象) ，可返回一个列表，包好对象的所有（包括"私有"的）成员函数、成员变量（属性）
            使用 hasattr(对象,"成员名")，可查看某个对象是否有字符串描述的，指定的成员方法、成员变量(属性)
            使用 getattr(对象,"成员名","默认值") 与 hasattr() 的前两个参数一致，当没有该成员时，返回默认值
        .类的私有化
            Python类默认情况下，所有的方法都可以被外部访问
            在Python类的方法名前面加双下画线（__）可以让该方法在外部不可访问
            其实这样定义的私有函数，也并不是真正的私有化
            而是编译器在编译类时，遇到这样以__开头的成员方法，
            会将其将其方法名进行修改，修改方法为，
            在这样的"私有"方法名前，自动加上 "_类名" 这样的前缀
            例如 A 类中有个 __func 的私有成员方法，
            编译器会将之修改为 _A__func，
            所以通过类对象，调用__func()方法时，就会提示不存在，
            如果改为调用 _A__func()，就可调用到 A 中私有的 __func() 方法了，
            所以这样的私有，只是通过自动给改名，实现的"伪私有"
            经测试，类的私有成员变量，也有同样的特点
        .类代码块 &<类代码块>
            类代码块，是直接写在类中的（而非类成员方法中的）可执行语句
            类代码块会在类定义的时候执行（而非类对象创建的时候）
            类代码块对写在哪里没有要求，可以在任意函数前面或后面
            类代码块也不必写在一起，一个类中可以有多个类代码块
            相如类中定义的成员变量，因为是可执行语句，所以也算是类代码块
            所以，类中的成员变量，也是在类定义的时候创建的，
            而非类对象创建的时候创建
            探索思考：
                类代码块之所以有这样的特性，是与 Python 中一切对象皆是引用相关的
                它不像 c/c++ 一样，只有当创建类对象时，才在堆栈中申请内存
                而是在程序一开始执行的时候，就会为类创建一个对象
                而之后创建的类变量，都是对一开始创建的类对象的引用
                假设有类 A，可测试 a=A(); b=A(); id(a) 和 id(b) 的值一致
                所以类代码块，看起来像是在类定义的时候就执行，
                其实这种说法是不准确的，其根本原因还是上面说的，
                类在程序一开始执行的时候，创建了一个"基础对象"，
                而类代码块，就是在创建该"基础对象"的时候执行的
        .类的继承
           语法： class 子类(父类1,父类2,...):
           · 判断子类与父类/祖先类之间的继承关系，可以使用issubclass函数，
             该函数接收两个参数：第1个参数是子类，第2个参数是父类/祖先类，返回类型为 bool
           · instance 函数则可检测是一个变量，是否是某个类，或是子类的的实例
           · __bases__ 可以以元组的形式，返回该类的所有父类
             这是类的一个特殊属性，使用该属性时，用"类名.__bases__"，而非"类对象.__bases__"
             注：就跟 __docs__ 是函数的一个特殊属性一样，使用该属性时，用"函数名.__doc__"
           · 多继承时，如果不同父类中有同名的成员，
             写在前面的父类会覆盖写在后面的父类同名的方法
        .构造方法
            构造函数是一种特殊类型的方法(函数)，它在类的实例化对象时被调用
            构造函数的名称是__init__()
            创建对象时，如果需要，构造函数可以接受参数
            当没有构造函数时，Python会自动创建一个不执行任何操作的默认构造函数
            例：
                class ComplexNumber:
                    def __init__(self, r = 0, i = 0):
                        """"初始化方法"""
                        self.real = r 
                        self.imag = i 
                    def getData(self):
                        print("{0}+{1}j".format(self.real, self.imag))
            .调用父类的构造函数
                如果子类继承父类，则子类会覆盖父类中同名的函数，
                这之中当然也包括构造函数
                构造函数对父类构造函数的"覆盖"体现在两方面：
                1. 创建对象是，不会自动调用父类的无参构造函数，只自动调用自己的
                2. 父类的构造函数并不是真的被子类覆盖消失了
                   例：
                        from inspect import getmembers
                        class A:
                            def __init__(self):
                                print("construct A")
                        class B(A):
                            def __func_b(self):   # B 的私有方法
                                print("B private method")
                            def func_b(self):     # B 的共有方法
                                print("B private method")
                        class C(B):
                            def __init__(self):   # "覆盖"继承自 A 的构造方法
                                print("constrcut C")
                            def __func_c(self):   # C 的私有方法
                                print("B private method")
                        a = A()
                        b = B()
                        c = C()
                        print(getmembers(b,inspect.ismethod))
                        print(getmembers(b,inspect.ismethod))
                        print(getmembers(c,inspect.ismethod))
                   输出：
                        construct A
                        construct A  # b 对象使用了 A 的构造方法
                        constrcut C  # c 对象使用了 C 自己的构造方法
                        [   ''' a 对象的函数表 '''
                            (
                                '__init__', 
                                #'__init__' 绑定到 A 对象的 A.__init__ 方法上
                                <bound method A.__init__ of <__main__.A object at 0x0000020326FB8F70>>
                            )
                        ]
                        [   ''' b 对象的函数表 '''
                            (
                                '_B__func_b', 
                                # '_B__func_b' 绑定到 B 对象的私有方法 B.__func_b 上
                                <bound method B.__func_b of <__main__.B object at 0x0000020326FB8DF0>>
                            ), 
                            (
                                '__init__', 
                                #'__init__' 绑定到 B 对象的 A.__init__ 方法上
                                <bound method A.__init__ of <__main__.B object at 0x0000020326FB8DF0>>
                            ), 
                            (
                                'func_b', 
                                # 'func_b' 绑定到 B 对象的公有方法 B.func_b 上
                                <bound method B.func_b of <__main__.B object at 0x0000020326FB8DF0>>
                            )
                        ]
                        [   ''' c 对象的函数表 '''
                            (
                                '_B__func_b', 
                                #继承自父类 B 的方法 _B__func_b
                                <bound method B.__func_b of <__main__.C object at 0x0000020326FC4280>>
                            ), 
                            (
                                '_C__func_c', 
                                #'_C__func_c' 绑定到 C 对象的私有方法 C.__func_c 上
                                <bound method C.__func_c of <__main__.C object at 0x0000020326FC4280>>
                            ), 
                            (
                                '__init__', 
                                #'__init__' 绑定到 C 对象自己的 C.__init__ 方法上
                                <bound method C.__init__ of <__main__.C object at 0x0000020326FC4280>>
                            ), 
                            (
                                'func_b', 
                                #继承自父类 B 的 func_b
                                <bound method B.func_b of <__main__.C object at 0x0000020326FC4280>>
                            )
                        ]
                   通过该例可以说明，Python使用了一种"函数绑定"的机制，
                   像如 B 没有"覆盖"父类 A 的 __init__ 方法，所以 b 对象的 __init__ 绑定到 A.__init__ 上
                   而 C "覆盖"了父类 A 的 __init__ 方法，所以 c 对象的 __init__ 绑定到自己的 C.__init__ 上
                   通过本例还可以看出，类的私有方法也是通过这种"函数绑定"机制实现隐藏的
            .调用父类的构造函数 -- 拓展
                现在我们知道了，如果一个子类没有定义自己的构造方法时，会自动调用父类的构造方法
                而如果一个子类定义了自己的构造方法，就不会自动调用父类的任何构造方法了
                '注意：上面这点需要特别注意，这是不同于C++的地方，这意味着父类的构造函数，通常不会默认调用'
                但其实这里面还有许多疑问没有解决：
                1. 父类的构造方法如果有参数，子类没有构造方法时，会怎样
                2. 多继承时，子类如果没有自己的构造方法时，是如何自动调用父类的构造方法的
                3. 多继承是，子类如果定义了自己的构造方法，该如何继续调用父类的构造方法
                下面将对以上疑问逐条解答：
                1. 这种情况下，子类相当于默认定义了构造方法：
                   def __init__(self,*arg,**args):
                       父类.__init__(self,*arg,**args)
                   所以，即使父类的构造方法有参数，也是可以正确调用到父类的构造方法的
                   所以，这种情况下，构建该子类的对象时，传的参数，应跟父类构造函数所要求的参数一致
                2. 多继承时，写在后面的父类，会被写在前面的父类，同名覆盖成员方法
                   这其中也包括构造函数：当子类没有构造方法时，默认调用最前面父类的构造方法
                   这种情况，其实就跟只有一个父类的情形是相似的
                   注意，这种情况会有一个"缺陷"：
                       就是写在后面的父类，如果其构造函数中，
                       通过 self ，为类添加了新的动态属性，
                       则因为该类的构造方法没有被执行，
                       所以派生子类中，也不会自动创建出这些动态属性
                   总结：子类从多个父类派生，而子类又没有自己的构造函数时，
                   （1）按顺序继承，哪个父类在最前面且它又有自己的构造函数，就继承它的构造函数；
                   （2）如果最前面第一个父类没有构造函数，则继承第2个的构造函数，
                        第2个没有的话，再往后找，以此类推。
                3. 参：@调用类的成员方法 
                   我们总是可以通过"父类名.__init__()"这种方法调用指定父类的构造方法
                   但这种继承时，需要提及一种情形，即菱形继承：
                   C 继承 B1,B2，且 B1,B2 都继承 A，
                   C 通过 "父类名.__init__()" 方法，同时调用了 B1 和 B2 的 __init__ 方法
                   B1,B2 均通过 "父类名.__init__()" 方法， 调用了 A 的 __init__ 方法
                   这时，构建 C 的对象时，可想而知， A 中的构造方法，
                   将因为 B1 和 B2 构造方法的执行，而执行两次
                   那有没有方法，让上述情形中，A 的构造方法，只调用一次呢？
                   解决办法就是使用 super()：   &<super()方法>
                       super() 函数是用于调用父类(超类)的一个方法。
                       语法：super(type[, object-or-type])
                           type -- 当前类名
                           object-or-type -- 一般是 self
                           Python3.x 和 Python2.x 的一个区别是: 
                           Python 3 可以使用直接使用 super().xxx 
                           代替 super(Class, self).xxx
                       super() 的本质
                           事实上，对于你定义的每一个类，
                           Python 会计算出一个方法解析顺序（Method Resolution Order, MRO）列表，
                           它代表了类继承的顺序，
                           我们可以使用下面的方式获得某个类的 MRO 列表：
                           print(类.mro())
                           上面的菱形继承结构，D.mro()的输出：
                           (
                            <class '__main__.C'>, 
                            <class '__main__.B1'>, 
                            <class '__main__.B2'>, 
                            <class '__main__.A'>, 
                            <class 'object'>
                           )
                           总的来说，一个类的 MRO 列表就是合并所有父类的 MRO 列表，并遵循以下三条原则：
                           a. 子类永远在父类前面
                           b. 如果有多个父类，会根据它们在列表中的顺序被检查
                           c. 如果对下一个类存在两个合法的选择，选择第一个父类
                           super() 方法的实现代码：
                           def super(cls, inst):
                               mro = inst.__class__.mro()
                               return mro[mro.index(cls) + 1]
                           上面的代码做了两件事：
                           1. 获取 inst 的 MRO 列表
                           2. 查找 cls 在当前 MRO 列表中的 index, 
                              并返回它的下一个类，即 mro[index + 1]
                           简单来说，super()就是检索 inst 对象对应类的 MRO 列表，
                           然后返回 cls 类的后面的那类
                           inst 参数默认传 self（子类对象比父类对象具有更完成的 MRO 列表）
                           cls 参数通常传自身类，
                           所以此时的 super() 方法过去的是自身类在 MRO 列表中的后面的那个类
                   假设 B1,B2 分别通过 super() 调用了 A 的构造方法，C 没有自己的构造函数，
                   此时，创建 c 对象时，会默认调用 B1 的构造方法，
                   而 B1 构造方法中调用的 super().__init__() 方法，
                   第一个参数 type，传的是 B1，
                   第二个参数 object-or-type，则是 c 对象
                   所以，B1 的 super() 方法，会查找 c 的 MRO 列表，
                   因为该列表中，排在 B1 后面的是 B2，所以 super() 返回的是 B2
                   所以，B1 的构造方法中，就会调用 B2 的构造方法，
                   同理， B2 构造方法中的 super().__init__() 方法，
                   第一个参数 type，传的是 B2，
                   第二个参数 object-or-type，仍是 c 对象
                   所以，B2 中的 super() 方法，也会查找 c 的 MRO 列表，
                   因为该列表中，排在 B2 后面的是 A，所以 super() 返回的是 A
                   所以，B2 的构造方法中，就会调用 A 的构造方法
        .多继承
            如果多个父类中有相同的成员，
            例如，在两个或两个以上父类中有同名的方法，那么会按照父类书写的顺序继承。
            也就是说，写在前面的父类会覆盖写在后面的父类同名的方法。
            在Python类中，不会根据方法参数个数和数据类型进行重载。
        .继承 object 与不继承的区别
            创建一个类 A，不指定父类，然后 print("A: ",A.__mro__)
            输出结果：A:  (<class '__main__.A'>, <class 'object'>)
            可见，A 是默认继承了 object 类的
            注：在 python3 中默认继承 object，在 python2 中，默认不继承
            python3中，继承自 object 的成员：
            '__class__', '__dir__', '__doc__', '__init__', 
            '__delattr__', '__setattr__', '__getattribute__', 
            '__dict__',  '__hash__', '__repr__', '__str__', 
            '__eq__','__ge__', '__gt__', '__le__', '__lt__','__ne__', 
            '__sizeof__','__module__', '__format__', 
            '__new__', '__reduce__', '__reduce_ex__', '__weakref__', 
            '__init_subclass__', '__subclasshook__', 
        .类的特殊成员方法
            .将类变成序列 &<自定义序列>
                参：@序列
                序列的最大特点是，能通过下标[]，获取或设置键值
                自定义序列需要实现如下4个特殊方法
                · __len__(self):         #使用 len() 获取序列的长度时，调用该方法                    
                · __getitem__(self,key): #使用 myseq[key] 获取键值时，调用该方法
                · __setitem__(self,key,value): #使用 myseq[key]=value 设置键值时，调用该方法
                · __delitem__(self,key): #当使用 del 删除序列中键为 key 的键值对时，调用该方法
                如果未定义某个特殊方法，但却执行了对应的操作，就会抛出异常
                除了完全实现上面的4个特殊方法外，我们还可以选择继承内置序列类
                如继承字符串类(str)、列表类(list)、字典类(dict)等，
                然后只实现自己需要的特殊方法即可
        .方法重载
            方法重载需要3个维度：方法名、数据类型和参数个数。
            但Python只有2个维度，那就是参数名和参数个数
            所以Python不支持方法重载，至少在语法层次上不支持
            不过Python有参数注解，也就是说，可以在参数后面跟":参数类型"
            那使用了参数注解，是不是就相当于不足的第3个维度(数据类型)，
            从而使函数达到支持重载呢？
            其实Python的类就相当于一个字典，key是类的成员标识，value就是成员本身
            对类的成员函数来说，函数名就是key，函数体就是value
            Python会从头扫描所有的方法，遇到一个方法，就会将这个方法添加到类维护的字典中
            这就会导致后一个方法会覆盖前一个同名的方法，
            所以MyClass类最后就剩下一个method方法了，也就是最后定义的method方法
            所以，参数注解并不能实现方法的重载
            另外，要注意一点，参数注解也只是一个标注而已，与注释差不多，并不会影响传入参数的值。
            也就是说，将一个参数标注为int，也可以传入其他类型的值，如字符串类型
        .监听属性的读写
            通常会将类的成员变量称为属性
            在创建类实例后，可以通过类实例访问这些属性，也就是读写属性的值
            尽管可以读写属性的值，但无法对读写的过程进行监视
            例如，在读取属性值时无法对属性值进行二次加工，在写属性值时也无法校验属性值是否有效
            在Python语言中可以通过property函数解决这个问题，
            该函数可以将一对方法与一个属性绑定，
            当读写该属性值时，就会调用相应的方法进行处理
            property函数
                该函数会创建一个属性，并通过返回值返回这个属性
                property(getmethod，setmethod，delmethod)
                getmethod: 读属性时要执行的方法
                    只有 self 参数，返回对应属性的值
                setmethod: 写属性时要执行的方法
                    第一个参数是 self，第二个参数用于接收要设置的属性的值，无返回值
                delmethod: 删除属性时要执行的方法
                    只有 self 参数，无返回值
                    删除对象的属性只是调用了通过property函数绑定的回调方法，
                    并没有真正删除对象的属性
            尽管使用property函数可以将3个方法与一个属性绑定，
            在读写属性值和删除属性时，就会调用相应的方法进行处理。
            但是，如果需要监控的属性很多，则这样做就意味着，
            要在类中需要定义大量的getter和setter方法。
            通过重写特殊成员方法 __getattr__、__setattr__和__delattr__
            可以任何一个属性进行读写和删除操作时，都会调用它们中的一个方法进行处理
            ·　__getattr__(self,name)：
                用于监控所有属性的读操作，其中name表示监控的属性名。
            ·　__setattr__(self,name,value)：
                用于监控所有属性的写操作，
                其中name表示监控的属性名，value表示设置的属性值。
            ·　__delattr__(self,name)：
                用于监控所有属性的删除操作，其中name表示监控的属性名。
        .静态方法和类方法
            Python类包含3种方法：实例方法、静态方法和类方法
            .静态方法
                静态方法在调用时根本不需要类的实例（静态方法不需要self参数）
                # 注：并不是说类方法不支持带参数，只是说不需要带 self 参数
                定义静态方法需要使用 @staticmethod 装饰器（decorator）
            .类方法
                类方法的调用方式与静态方法完全一样，
                所不同的是，类方法与实例方法的定义方式相同，都需要一个self参数，
                只不过这个self参数的含义不同。
                #注：self这个参数，也可改叫别的名字，所以类方法的参数名叫 cls 比较合适
                对于实例方法来说，这个self参数就代表当前类的实例，
                可以通过self访问对象中的方法和属性。
                而类方法的self参数表示类的元数据，也就是类本身，
                并不能通过self参数访问对象中的方法和属性，
                而只能通过这个self访问类的静态方法和静态属性。
                #注：和静态方法一样，也可以同时定义多个不同的类方法，
                #类方法也可以在 self 参数后面，再加任意个参数
                定义类方法需要使用 @classmethod 装饰器。
            .举例：
                class MyClass:
                    # 实例方法
                    def instanceMethod(self):
                        pass
                    # 静态方法
                    @staticmethod
                    def staticMethod():
                        pass
                    # 类方法
                    @classmethod
                    def classMethod(self):  # 或 def classMethod(cls):
                        pass
            静态方法和类方法，只能访问直接在类中定义的静态成员变量
            类的静态成员变量，即在 @类代码块 中定义的变量
            对象成员变量，是通过对象直接添加，或通过成员函数的 self 参数添加的成员变量
            类方法一定程度上用于弥补类只能有一个构造函数的缺陷，如：
                class Book(object):
                    def __init__(self, title):
                        self.title = title
                    @classmethod
                    def create(cls, title):
                        book = cls(title=title)
                        return book
                    @staticmethod
                    def create_2(title):
                        book = Book(title=title)
                        return book
                book1 = Book("python")
                book2 = Book.create("python and django")
                print(book1.title)
                print(book2.title)
                注：虽然使用静态方法也能达成类似的功能，如 create_2 方法
                但在 create_2 中访问类的静态方法/静态属性时，都需要使用类名
                而如果类名做了改动，则静态方法中，所以使用类名的地方都需要跟着改动
                所以从这一点上来说，使用类方法更加合适
        .迭代器
            迭代就是循环的意思，也就是对一个集合中的元素进行循环，从而得到每个元素
            对于自定义的类，也可以让其支持迭代，这就是本节要介绍的特殊成员方法__iter__的作用。
            如果在一个类中定义__iter__方法，那么这个类的实例就是一个迭代器。
            __iter__方法需要返回一个迭代器，所以就返回对象本身即可（也就是self）
            当对象每迭代一次时，就会调用迭代器中的另外一个特殊成员方法__next__
            该方法需要返回当前迭代的结果
            当使用 for e in obj : 这样的语句时，就会隐含使用 obj 的迭代方法
            例：
                class A:  #产生奇数
                    def __iter__(self):
                        self.i = 0
                        return self

                    def __next__(self):
                        if self.i == 0 :
                            self.i = 1
                        else :
                            self.i = self.i + 2
                        if self.i > 10 :   # 用于标识迭代的完成
                            raise StopIteration
                        return self.i
                a = A()
                for i in a :
                    print(i)
        .生成器
            如果说迭代器是以类为基础的序列产生器，那么生成器就是以函数为基础的序列产生器
            也就是说，迭代器和生成器都只能一个值一个值地生产。每迭代一次，只能得到一个值
            所不同的是，迭代器需要在类中定义__iter__和__next__方法，
            在使用时需要借助迭代器对象的实例
            而生成器是通过一个函数展现的，可以直接调用，
            所以从某种意义上来说，生成器在使用上更简洁。
            带有 yield 的函数不再是一个普通函数，
            调用这样的函数，会返回一个生成器generator对象
            该生成器对象具有 __iter__ 方法，
            调用该方法，就会将记忆点重置到函数的开始位置（注1）
            #注1 ： 
            #经测，调用 __iter__ 方法，并不会起到重置函数记忆位置的作用
            #__iter__() 里面什么也没做，只是单纯的将 self 返回
            #另外，每次执行生成器函数，都会返回一个新的生成器对象（具有不同的id）
            同时生成器对象具有 __next__ 方法，
            每调用一次 __next__ 方法，就会从生成器函数的上次记忆位置开始执行
            直到遇到 yield 语句，返回 yield 后面的值，并记忆该位置
            由于返回的生成器对象，也有 __iter__ 和 __next__ 方法，
            所以也可以用在 for in 语句中，
            例：
                def func() :
                    for i in range(1,10):
                        yield i
                for i in f :
                     print(i)
        .装饰器
            装饰器是Python中一个非常有趣的特性，
            可以利用Python装饰器对一个函数再次包装
            装饰器是Python提供的一种机制：
                可以指定另一个函数或另外两多个函数，对某个函数的返回值进行"再加工"
                方法是定义函数的上面的行，借助特殊符号 @，指定装饰函数
                例：
                @add_surfix
                @add_prefix
                def get_str(str):
            装饰器本身就是一个普通的Python函数，只是函数的参数需要是函数类型（通常传入被装饰的函数）
            例如上面例子中的 add_surfix 函数：
                def add_prefix(fun):
                    def f(*args,**args2):   # 经测，*args 参数也能接受字典型参数
                        return "prefix : " + fun(*args,**args2)
                    return f
                def add_surfix(fun):
                    def f(*args):   # **args2 参数不知道什么时候会有用，不带该参数也行
                        return "surfix : " + fun(*args)
                    return f
            实际上，写在 get_str 上面的 @add_prefix 这样的写法，是一种语法糖，它等价于：
            get_str = add_prefix(get_str)
            声明的 get_str 函数，其实是声明了一个函数变量（本质是函数对象的引用），指向函数体，
            所有函数对象具有一些共通的特殊内置成员，如 __doc__、__name__ 等
            实际上可以通过运算符 del get_str ，将该 get_str 变量删除，之后就不能使用该函数变量了
            相关参考： file://基础.py@*的用法
    .异常        
        .抛出异常
            使用raise语句可以直接抛出异常
            raise语句可以使用一个类（必须是Exception类或Exception类的子类）或异常对象抛出异常
            如果使用类，系统会自动创建类的实例
            如果直接使用 raise Exception，则抛出的异常信息，
            除了该抛出异常语句所在代码文件和代码行外，没有其他有价值的信息
            Exection类还可接受一个字符串参数，描述异常原因，如：
            raise Exception("这是自己主动抛出的一个异常")
            在Python语句中内置了很多异常类，用来描述特定类型的异常，
            如ArithmeticError表示与数值有关的异常。
            使用内建的异常类是不需要导入任何模块的，
            不过要使用其他模块中的异常类，就需要导入相应的模块了
            一些最重要的内建异常类
                异常类名            描述
                Exception           所有异常的基类
                AttributeError      属性引用或赋值失败时抛出的异常
                OSError             当操作系统无法执行任务时抛出的异常
                IndexError          在使用序列中不存在的索引抛出的异常
                KeyError            在使用映射中不存在的键值时抛出的异常
                NameError           在找不到名字(变量)时抛出的异常
                SyntaxError         在代码为错误形式时触发
                TypeError           在内建操作或函数应用于错误类型的对象时抛出的异常
                ZeroDivisionError   在除法或者取模操作的第2个参数值为0时抛出的异常
                ValueError          在内建操作或者函数应用于正确类型的对象，
                                    但该对象使用了不合适的值时抛出的异常
        .自定义异常类
            最简单的自定义异常类就是一个空的Exception类的子类。
            class MyException(Exception):
                pass
        .捕捉异常
            如果异常未捕捉，系统就会一直将异常传递下去，直到程序由于异常而导致中断
            为了尽可能避免出现这种程序异常中断的情况，需要对"危险"的代码段进行异常捕捉
            try…except语句的基本用法
                try:
                    语句
                except 异常类1 [as e]:             #中括号中的 as e，表示可省略不用
                    当产生"异常类1"对应的异常时，进入到这里
                except (异常类2,异常类3) [as e]:   #捕捉多个异常
                    当产生"异常类2"、"异常类3"对应的异常时，进入到这里
                except:                            #如果想接受异常对象，使用 except Exception as e:
                    产生其它异常时，进入到这里
                else:
                    当try和except之间的代码正常执行后才执行这里，
                finally:
                    不管是正常执行，还是抛出异常，最后都会执行finally子句中的代码，
                    所以应该在finally子句中放置关闭资源的代码，如关闭文件、关闭数据库等。
                注： 
                    except 和 else 和 finally 都不是必须的
                    但当使用 else 时，要去必须有 except 存在
                    try 不能单独使用，后面要么使用 except，要么使用 finally
        .异常、函数与栈跟踪
            如果异常被隐藏得很深，而且又不被处理，这种异常是不太好捕捉的，
            幸亏Python解析器可以利用栈进行跟踪
            Python解析器面板会将异常发生的源头以及其传播的路径都显示出来
        .异常的一种使用情形
            当访问一个类对象的方法或属性时，
            如果该方法或属性不存在，就会产生异常
            当然可以通过 hasattr() 这样的函数，先判断该对象是否有指定的成员
            不过有时大量使用这样的判断语句，会使程序显得繁琐
            此时使用异常捕获，可能更好
    .qt使用python开发
        .PySide2 or PyQt5
            PyQT是由Riverbank Computing Ltd开发维护的。采用了GPL加商业许可两种许可证模式
            这就意味着，如果你的代码使用了PyQT，那么你必须开源你的代码，这是由GPL的传染性决定的。
            要么如果你不想开源你的代码，你就得购买商业许可证。
            是Nokia(QT的开发者)打算和Riverbank Computing谈判，劝说PyQT采用LGPL
            (如果只是将采用该许可证的项目做为Library来link，则不需要开源)
            但是Riverbank不同意该建议，所以，Nokia一气之下，决定开发自己的版本，这就是后来的PySide
            PySide和PySide2的区别只在于一个是支持QT5之前的版本，一个是支持QT5的版本
            其实PyQT5和PySide2大部分的接口都是很类似的。只不过PyQT5对QT5的支持完成的比较早
        .pip
            .简介
                pip 是一个现代的，通用的 Python 包管理工具
                提供了对 Python 包的查找、下载、安装、卸载的功能。
            .windows 安装 pip
                在正式安装pip之前，可在控制台输入以下命令 ： python -m pip --version，
                用于检测当前Windows环境中是否已经安装pip。
                pip 安装方法：下载并执行该脚本 ： https://bootstrap.pypa.io/get-pip.py
            .pip常用命令
                pip --version                    #查看版本
                pip --help                       #获取帮助信息
                pip help 子命令                  #查看某个命令的帮助信息
                pip instal -U pip                #升级pip
                    easy_install --upgrade pip   #也可升级pip
                pip -o                           #查看可升级的包
                pip search 安装包名              #搜索工具包
                pip install 安装包名[==/>=版本]  #安装工具包
                pip install --upgrade 安装包名   #升级工具包
                pip show 安装包名                #显示安装包的信息
                pip show -f 安装包名             #显示安装包的详细信息
                pip uninstall 安装包名           #卸载工具包 
            .更换pip源
                默认的pip源是国外的，下载速度非常慢，可以配置成使用国内的源：
                提供软件源的网址
                    清华大学开源软件镜像站 https://pypi.tuna.tsinghua.edu.cn/simple
                    阿里云开源镜像站 http://mirrors.aliyun.com/pypi/simple
                    豆瓣开源镜像站 http://pypi.douban.com/simple/
                    中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple
                    网易开源镜像站 http://mirrors.163.com/
                    搜狐开源镜像 http://mirrors.sohu.com/
                    浙江大学开源镜像站 http://mirrors.zju.edu.cn/
                    腾讯开源镜像站 http://mirrors.cloud.tencent.com/pypi/simple
                临时使用源：
                    pip instal xxx[==版本号] -i 源URL  [--trusted-host 可信源URL]
                永久使用源：
                    源配置文件内容举例：
                        [global]
                            index-url = http://pypi.douban.com/simple
                        [install]
                            trusted-host=pypi.douban.com
                    通过命令修改源配置文件：
                        换镜像源：
                        pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple 
                        pip安装源的可信问题：
                        pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
                        pip安装源的超时设置：
                        pip config set global.timeout 6000
                    不配置信任源有什么影响
                        像如阿里云，如果没配置信任源，会提示：
                        位于 mirrors.aliyun.com 的存储库不是受信任或安全的主机，因此被忽略。
                        如果此存储库可通过 HTTPS 访问，则建议改用 HTTPS，否则您可以静音此警告，
                        并使用“–trusted-host mirrors.aliyun.com”允许它。
        .使用 pip 安装 PySide2
            pip install pyside2 -i https://pypi.tuna.tsinghua.edu.cn/simple
            注：pyside2 与 phthon3.8 不兼容，可使用 python3.6.8 版本
        .使用 pip 安装 pyQt5
            pip install PyQt5 -i https://pypi.douban.com/simple
            pip install PyQt5 -i https://pypi.tuna.tsinghua.edu.cn/simple
            注：PyQt5不再提供常用Qt工具，
            比如图形界面开发工具Qt Designer、国际化翻译工具Liguist 
            如果开发中使用到这些，必须自行安装Qt工具 : PyQt5-tools
.在 pycharm 中配置使用 pyqt5
    .项目包管理（配置使用pyqt5库）
        菜单/文件/设置/项目/Python解释器，
        可选择使用哪个位置的解释器，还可以对包进行安装、卸载操作
        点右侧的配置按钮，可弹出添加Python解释器的窗口：
        Virtualenv环境：
            在当前工程中拷贝得到一个Python解释器，
            安装、引用的包，位于当前工程目录的特定位置
        系统解释器：
            Python的默认安装位置
            安装、引用的包，位于 pip 系统安装目录中的特定位置
    .添加外部工具（配置使用 qt5 designer）
        菜单/文件/设置/工具/外部工具
        点添加按钮，我们把qt设计器加进来，qt designer 的目录一般在：
        Python安装目录\Lib\site-packages\qt5_applications\Qt\bin
        注：工作目录，我们可以不指定，也可以设置为当前项目目录 "$FileDir$"
        这样，就可以在主菜单栏的工具菜单中，找到我们添加的工具了
        但上面只添加了 qt designer 工具还是不够的，
        这是因为 qt designer 保存的文件是 ui 格式的，
        我们还需要一个工具（uic工具）把 ui 转为 python 文件，
        操作方法跟上面添加 qt designer 工具的过程相似，
        不过选择的工具为 python.exe
        我们可以将这个工具的名字设为 pyuic，
        然后在参数中，设置为： 
        -m PyQt5.uic.pyuic "$FileName$" -o "$FileNameWithoutExtension$.py"
        工具目录还是设为 "$FileDir$"
        可以看出来，这是使用了 pyqt5 提供的一个 python 模块（PyQt5.uic.pyuic）
        通过该模块，将传入的文件 $FileName$ 专为 py 格式的文件
        这样，我们就可以先用 qt disigner 编辑生成 ui 文件，
        该文件可以在 pycharm 的项目面板中看到，
        然后在该 ui 文件上右键，然后选择外部工具\pyuic，
        这样，就可以生成该文件对应的 python 文件了
    .引用生成的 .py 界面文件
        一般使用步骤：
            1. 导入 py 文件
            2. 为界面控件绑定信号槽
            3. 继承使用 Ui_Form 类
        代码举例：
            import sys
            from PyQt5.QtWidgets import QApplication,QWidget
            from Form_untitled import Ui_Form
            class A(QWidget,Ui_Form):
                def __init__(self):
                    super(A,self).__init__()  
                    #也可使用 QWidget(self).__init__()
                    #一定要先调用 QWidget 的构造方法，完成 QWidget 的初始化
                    self.setupUi(self)
            if __name__ == "__main__":
                app = QApplication(sys.argv)
                w = A()
                w.show()
                sys.exit(app.exec_())
    .Qt中 gui 模块和 widgets 模块的区别
        在Qt5下，QWidget系列从QtGui中被剥离出去，成为单独的QtWidget模块
        随着Qt Quick2的引入，QtDeclarative也逐渐和QWidget系列也脱离关系。
        最终：在Qt5下的GUI编程，有两套不同的东西
        QtWidget（使用一个被称为 BackingStore 的东西）
        QtQuick （使用一个被称为 SceneGraph 的东西）
        gui 模块提供了基本的图形系统抽象层,
        包括QPaintDevice、QPainter等类,这些类构成了Qt的绘图基础
        widgets 模块在 gui 模块的基础上,提供了完整的桌面级用户界面控件,
        如按钮、列表、滑块等。这些控件继承自更基础的图形类
        gui 模块是更底层的图形功能,widgets模块依赖于gui模块,提供了高级控件实现。
        如果只需要基本的GUI编程功能,可以只使用gui模块。
        如果要开发完整的桌面程序,需要同时使用gui和widgets。
        gui模块包含的类提供绘图功能,但没有事件、布局等高级功能。
        widgets模块在gui之上扩展了这些高级特性。
        总结来说,gui模块提供基础绘图和渲染功能,
        widgets模块在此基础上实现完整的桌面控件层
        两者可以分开使用,但widgets依赖gui
        依赖于gui的qt程序可以在无界面的终端系统centos上跑吗?
            如果Qt程序依赖gui模块,但没有使用widgets模块的代码,
            是可以在无界面的终端环境如CentOS上运行的
            关键的是该Qt程序不能使用任何QWidget及其子类的GUI控件代码,
            这些控件都依赖于底层的窗口系统支持。
            但使用gui模块提供的核心绘图类是可以的,
            如QPainter、QPixmap、QIcon等。
            这些类不依赖窗口系统,可以在无界面环境下使用,
            实现一些基本的图片处理、图形输出等功能。
            所以如果程序只使用gui模块的纯绘图功能,
            不涉及任何窗口、控件的创建和显示,就可以在终端环境下运行。
            但这需要程序从设计上就考虑到无界面环境,
            不依赖窗口和控件,只基于核心绘图类实现所需功能。
            如果已经使用了窗口、界面控件,要想在无界面环境运行,
            关键的是该Qt程序不能使用任何QWidget及其子类的GUI控件代码,
            这些控件都依赖于底层的窗口系统支持。
            但使用gui模块提供的核心绘图类是可以的,如QPainter、QPixmap、QIcon等。
.python虚拟机原理
    与 C 语言不同，python 没有官方标准，最接近官方标准的文档是所谓的 python 语言参考手册，
    也就是说，python 并不完全由参考手册定义，但我们也不能说它是由 CPython 定义的，
    因为 CPython 的很多实现细节并不属于 python 的一部分，
    比如说，基于引用计数的垃圾回收机制就是一个例子。
    因此，我们或许可以说，python 的定义包括两部分，
    其一是 python 语言参考手册，其二是其主要实现 CPython。
    Python 代码的执行可以大概分成三个阶段： 初始化、编译、解释
        在初始化阶段，
            CPython 会初始化 Python 运行所需的各种数据结构，
            准备内建类型、配置信息，加载内建模块，建立依赖系统，
            并完成很多其它必要的准备工作。
            这个过程很重要，却往往被忽视。
        之后是编译阶段。
            CPython 是一个解释器而不是编译器，
            意思是说，它并不生成机器码。但和其它解释器一样，
            CPython 会在执行前把源代码转换成一种中间形式，
            这个转换过程其实和编译器做的事情是一样的：
            解析源码，建立 AST（Abstract Syntax Tree 抽象语法树），
            根据 AST 生成字节码，并对字节码做一些可能的优化。
            python文件在被import运行的时候会在同目录下编译一个pyc的文件（为了下次快速加载），
            这个文件可以和py文件一样使用，但无法阅读和修改；
            有很多在线工具支持将pyc文件反编译为py文件
        CPython 的核心是一个执行字节码的虚拟机
.python反编译攻防
    通过 Pyinstaller 打包的 python 程序，可以通过 pyinstxtractor.py 
    (下载地址：https://github.com/extremecoders-re/pyinstxtractor)
    解包,并得到 .pyc 文件， .pyc 文件就像 java 中的 .class 文件类似，
    是交由虚拟机执行的字节码文件，其特点就是容易被反编译，
    有甚多在线工具，可以将 .pyc 文件反编译成 python 源码
    防止反编译的思路大概有两种，
    一种是不将 .pyc 文件打包，而是将 .pyd 文件打包
        因为 .pyd 文件无法被解密（Cython编译出来的二进制文件）
        又可以正常被 python 脚本使用，
        所以这种方案是可行的，但需要使用 Cython 编译
        所以这可能需要了解些 Cython 的语法
        Cython 是介于 C 和 Python 之间的编译器，
        它完全兼容 Python 语法，但又增加了一些特有的语法，
        从而可以更容易的调用 C 接口
    二是打包时加密	
.各种python文件格式
    *.pyi文件是Python中的类型提示文件，用于提供代码的静态类型信息
    一般用于帮助开发人员进行类型检查和静态分析
    *.pyi文件的命名约定通常与相应的.py文件相同，以便它们可以被自动关联在一起。
    *.pyc是Python字节码文件的扩展名，用于存储已编译的Python源代码的中间表示形式，
    因为是二进制文件所以我们无法正常阅读里面的代码。
    *.pyd是Python扩展模块的扩展名，用于表示使用C或C++编写的二进制Python扩展模块文件。
    *.pyd文件是编译后的二进制文件，它包含了编译后的扩展模块代码以及与Python解释器交互所需的信息。
    此外，.pyd文件通过import语句在Python中导入和使用，就像导入普通的Python模块一样。
    当相同文件名的pyd和py文件在同级目录之中，将会优先执行pyd文件。
    但在PyCharm中,按住Ctrl用鼠标左键点击方法名，则会跳转到py文件代码，pyd将会被忽略
    *.pyw是Python窗口化脚本文件的扩展名。
    它表示一种特殊类型的Python脚本文件，用于创建没有命令行界面（即控制台窗口）的窗口化应用程序。
    *.pyx 是Cython源代码文件的扩展名。
    Cython是一种编译型的静态类型扩展语言，
    它允许在Python代码中使用C语言的语法和特性，以提高性能并与C语言库进行交互。
    fb.pyx(需使用cythonize命令进行编译)
.python与c++交互
    1. 使用 python 原生接口 ctypes
    提供了调用 c 库的方法，但因为所有的变量本质上还是动态类型，所以效率比较低
    2. 使用 cython
        在 py 语法的基础上，添加了一些新的语法，可以高效调用任何c/c++的库
    3. 使用 pybind11
        如果有用c++来编写python模块的需求，可以使用 pybind11
        在C++中，借助 pybind11 框架，编译出的库，可以被 python 直接调用，就跟调用 py 自身模块的语法一样
    在写python时, 我们可以通过Profile等耗时分析工具, 
    找出比较用时的代码块, 对这一块用C++进行优化. 没必要优化所有的部分.
    其实要使 py 程序执行的块，可以不使用默认的 CPython 解释器，改用 PyPy，
    PyPy 是用 Python 实现的 Python 解释器的动态编译器，
    PyPy 是 CPython 的一种快速且功能强大的替代方案，它的速度提升非常明显，
    但它也不是万能的，有一些局限性，PyPy最适合纯Python应用程序，不适用于C扩展
    （它支持Python语言的所有核心部分以及大多数的Python语言标准库函数模块）
    另外，用 pypy 打包 exe 很麻烦，不能借助 pyinstaller 生成安装包
.linux命令行调试python脚本
    python -m pdb test.py
    h(elp)  [comman] #打印可用指令及帮助信息
    r(eturn)         #运行代码直到下一个断点或当前函数返回
    b(reak) [[filename:]lineno | function[,condition]]  #指定文件某行或函数体来设置断点
    l(ist)  [first[, last]]  #查看指定代码段
    n(ext)      #执行下一行
    s(tep)      #执行下一行，若为函数则进入函数体
    p(rint)     #打印某个变量
    a(rgs)      #打印当前函数的参数
    w(here)     #打印堆栈信息
    d(own)      #移至下层堆栈
    u(p)        #移至上层堆栈
    j(ump)      #跳转到指定行
    c(ontinue)  #继续执行
    disable [bpnumber [bpnumber]]   #失效断点
    enable[bpnumber [bpnumber]]     #启用断点
    cl(ear) [filename:lineno | bpnumber [bpnumber]] #删除断点
    q(uit)/exit #中止调试并退出
.qt编程
    .在线帮助手册
        https://doc.qt.io/qtforpython-6/modules.html
    .继承qt类及其子类
        注意事项：应该总是调用父类的构造方法：
        class MyCls(QMainWindow):
            def __init__(self, parent=None):
                super(当前类名, self).__init__(parent)
        因为 python 的子类，一旦实现了自己的构造函数，
        则如果不主动写上，否则不会自动调用父类的构造函数
    .信号槽
        所有继承自QObject或其子类（如QWidget）的类都可以包含信号和槽
        您可以将任意数量的信号连接到单个插槽，也可以将信号连接到任意数量的插槽。
        甚至可以将一个信号直接连接到另一个信号。
        Connect ()返回一个 QMetaObject.Connection 对象，
        该对象可以与 disconnect () 方法一起用于切断连接。
        
        例：
            button = QPushButton("Call function")
            button.clicked.connect(function)  #button有个clicked信号
        .信号槽的特点：
            一个信号可以连接多个槽
            一个信号可以连接另外一个信号
            信号参数可以是任何Python类型
            一个槽可以监听多个信号
            信号与槽的连接方式可以是同步连接，也可以是异步连接。
            信号与槽的连接可能会跨线程
            信号可能会断开
        .定义信号
            声明的信号的类型为 QtCore.Signal() 
            注：在 PyQt6 和 PySide2 中的信号都为 Signal 类型，在 PyQt5 中为 pyqtSignal 类型
            信号携带的参数，也是是python类型，也可以是qt类型或c类型：
            signal1 = Signal(int)                   # Python types
            signal2 = Signal(QUrl)                  # Qt Types
            signal3 = Signal(int, str, int)         # more than one type
            signal4 = Signal((float,), (QDate,))    # optional types
            还可以通过命名参数name，重新制定信号的名称：
            signal5 = Signal(int, name='rangeChanged')
            如果不指定时，该信号的名字会与被指定给的变量同名，
            像如上面，该信号被指定了名字后，要想发送该信号，就变为：rangeChanged.emit(...)
        .定义槽函数
            槽函数应该（不是强制）带有 @QtCore.Slot() 装饰器，如：
            @Slot(str)  #括号中的 str 是槽函数所接受的参数的类型，PyQt5 中使用 @pyqtSlot()
            def slot_function(self, s):
            不带装饰器也是可以的，但会造成运行时开销，
            因为这将推迟到创建连接时，将方法添加到QMetaObject中
            而且，要想 QtCore.QMetaObject.connectSlotsByName，必须使用这种装饰器
            一个函数也可以通过多个装饰器，表明该槽函数支持多种类型的参数，如：
            @Slot(int)
            @Slot(str)
            def say_something(self, arg):
                if isinstance(arg, int):
                    print("This is a number:", arg)
                elif isinstance(arg, str):
                    print("This is a string:", arg)
        .操作信号
            使用obj.signal.connectconnect(槽函数名)函数可以把信号绑定到槽函数上。
            使用obj.signal.disconnect(槽函数名)函数可以解除信号与槽的函数绑定
            使用signal.emit(参数..)函数可以发射信号
pycharm在线帮助手册            
    https://www.jetbrains.com/help/pycharm/2022.1/quick-start-guide.html            