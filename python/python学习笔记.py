Python3基础语法（菜鸟教程）
    空行：
        空行与缩进不同，不是python语法的一部分，空行分割只是方便阅读
    多行语句： 
        需要在行尾用\连接多行，括号中的多行语句无需行换行符
    多条语句连写：
        可以将多条语句写为一行，每条语句间通过分号分隔
    import 与 from...import：
        import将整个模块(somemodule)导入，格式为： import somemodule
        从某个模块中导入某个函数,格式为： from somemodule import somefunction
        从某个模块中导入多个函数,格式为： from somemodule import func1, func2, func3
        将某个模块中的全部函数导入，格式为： from somemodule import *
        关于 import 的小结，以 time 模块为例：
            1、将整个模块导入，例如：import time，在引用时格式为：time.sleep(1)。
            2、将整个模块中全部函数导入，例如：from time import *，在引用时格式为：sleep(1)。
            3、将模块中特定函数导入，例如：from time import sleep，在引用时格式为：sleep(1)。
            4、将模块换个别名，例如：import time as abc，在引用时格式为：abc.sleep(1)
    获取函数的帮助信息：
        可以通过python安装目录下的chm帮助文档获取函数帮助
        在python交互模式中，使用help("函数名")，可以获得该函数的帮助信息
    变量：
        变量无需声明
        多变量赋值：
            1. a = b = c = 1
            2. a, b, c = 1, 2, "runoob"  #三个值会分别赋给变量a,b,c
    数学运算：
        /  ：普通除法
        // ：整除
            //得到的结果不一定是整数，这与分子、分母类型有关
            7//2 返回值为 3 ，7.0//2 或 7//2.0 返回值为 3.0
        %  ：取余
        ** ：密乘
        数学表达式语句执行后，会默认将结果赋值给内置的只读变量_。
    标准数据类型：
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
    数字类型： 
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
    字符串：
        单引号等价于双引号
        单引号和双引号可以嵌套，被嵌套的会被解释成为普通标点符号
        三引号可以指定一个多行字符串，里面可以嵌套单引号/双引号的字符串
        连续的字符串自动拼接
        字符串支持加法和乘法运算，+用于拼接，*表字符串重复
        Python 没有单独的char字符类型，一个字符就是长度为 1 的字符串
        字符串的截取
            语法格式：变量[头下标:尾下标:步长]
            下标为负数时，表从后面数第几位，尾下标默认为-1，步长默认为1
            步长为负数时，表反向读取
            含头不含尾：头下标处的字符会输出，尾下标处的字符不会输出
            举例：
                str='123456789'
                print(str)                 # 输出字符串
                print(str[0:])             # 输出 123456789
                print(str[0:-1])           # 输出 12345678
                print(str[-1::-1])         # 输出 987654321    
                print(str[-1:0:-1])        # 输出 98765432
                print(str[0])              # 输出字符串第一个字符
                print(str[2:5])            # 输出从第三个开始到第五个的字符
                print(str[2:])             # 输出从第三个开始后的所有字符
                print(str[1:5:2])          # 输出从第二个开始到第五个且每隔一个的字符（步长为2）
                含头不含尾：
                    如 s[0:2], 希望输出的是：'012'，实际输出的是：'12'
                    单独输出 s[9],报错, s[8], 输出 '9'
                    s[0:8], 输出 '12345678',  s[0:9], 输出 '123456789'
        原生字符串
            r""为原生字符串方式，即让字符串中的\原样输出，而不发生转义
        Unicode字符串
            在python2中，字符串默认用8位的ASCII码进行存储，
            在字符串前面加标识符u，可以强制用Unicode编码
            而在python3中，字符串默认用Unicode编码
        %格式化字符串
            "格式化字符串" % (元组)   #不能用列表
            例： print ("我叫 %s 今年 %d 岁!" % ('小明', 10))
            优点：与后两种格式化字符串方法相比，这种方法能更精确的控制字符串输出格式
        str.format()方法格式化字符串   （python >= 2.6)
            这种方法有点类似Qt的字符串格式化方法，使用 {索引数字} 作占位符，索引从0开始
            例： print("我叫 {0} 今年 {1} 岁".format('小明',10))
            另外，占位符除了使用索引数字，还可以使用 {参数名} 作占位符
            例： print("我叫 {name} 今年 {age} 岁".format(name="小明",age=10))
            如果使用空占位符 {},也是允许的，此时表明依次使用第1、2、3...个参数
            例： print("我叫 {} 今年 {} 岁".format('小明',10))
            优点：这种方法使用方便，无需关心要输出变量的格式
        f-string格式化字符串   (python >= 3.6)
            这种方法有点像bash脚本中的${变量名}用法, 在python的f-string中，
            可以直接使用 {变量}、{表达式}、{变量表达式}
            但是需要在字符串前面带f-string字符串标记f
            例： name="小明";age=9; print(f"我叫 {name} 今年 {age+1} 岁")
            优点：与前两种格式化字符串方法相比，这种方法更加简洁直观方便，但它对python的版本要求高
        字符串部分内建函数
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
    列表类型：
        列表是写在方括号 [] 之间、用逗号分隔开的元素列表
        列表中元素的类型可以不相同，它支持数字，字符串甚至可以包含列表
        列表支持与字符串一样的索引方法：变量[头下标:尾下标:步长]
        列表与字符串一样，也支持加法和乘法运算，进行列表拼接或重复
        支持split、join等成员方法
        修改列表
            因为列表属于可变数据类型，所以可以对列表的元素重新指定新的值
            如：list = ['Google', 'Runoob', 1997, 2000]
            list[2] = 1996      #修改
            list.append("xxx")  #追加
            del list[0]         #删除
            于是，list 变为 ['Runoob', 1996, 2000, 'xxx']
        嵌套列表
            >>>a = ['a', 'b', 'c']
            >>> n = [1, 2, 3]
            >>> x = [a, n]
            >>> x
            [['a', 'b', 'c'], [1, 2, 3]]
            >>> x[0]
            ['a', 'b', 'c']
            >>> x[0][1]
            'b'
        列表复制
            >>> a = [1, 2, 3]
            >>> b = a           # id(a) == id(b)
            >>> c = []          # id(c) != id(a)
            >>> c = a           # id(c) == id(a)
            >>> d = a[:]        # id(d) != id(a)
            >>> e = a.copy()    # id(e) != id(a)
        列表遍历
            # 正序遍历：
            list01 = ["Googl",'Runoob',1997,2002]
            for item in list01:             #用法1
                print(item)
            for i in range(len(list01)):    #用法2    
                print(list01[i])
            # 反向遍历
            for i in range(len(list01)-1,-1,-1):    
                print(list01[i])
        部分函数&方法
            1	len(list)
                列表元素个数
            2	max(list)
                返回列表元素最大值
            3	min(list)
                返回列表元素最小值
            4	list(seq)
                将元组转换为列表，经测试，seq只要是可迭代对象，就可以转换为列表
            1	list.append(obj)
                在列表末尾添加新的对象
            2	list.count(obj)
                统计某个元素在列表中出现的次数
            3	list.extend(seq)
                在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
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
    元组类型：
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
        作为参数或函数的返回值：
            一般来说，函数的返回值一般为一个。
            而函数返回多个值的时候，通常借助元组的方式返回（也可以是list等）
                return (a,b)  #返回的是元组
                return a,b    #返回的是元组
                return [a,b]  #返回的是列表
            python中的函数还可以接收可变长参数，比如以 "*" 开头的的参数名，
            它会将所有的参数收集到一个元组上
            如：def test(*args):
                    print(type(args)) # 输出：<class 'tuple'>
        嵌套
            元组中的元素不仅可以是元组（自嵌套），还可以是列表、集合、字典等
            当这些可修改对象作为元组的元素时，所谓的元组元素不可修改，
            指的是该列表/集合/字典元素所引用的位置（指向的对象地址）不可修改，
            但该列表/集合/字典元素所指向的内存对象（中的子元素）仍是可修改的
            例：
                >>> tp=(1,2,['a','b','c'])
                >>> tp[2][0]='x'
                >>> tp
                (1, 2, ['x', 'b', 'c'])
        元组复制
            tp1=(1,2,3)
            tp2=()          # id(tp2) != id(tp1)
            tp2=tp1         # id(tp2) == id(tp1)
            tp2=tp1[:]      # id(tp2) == id(tp1) ,这是与列表不同的地方
        内置函数
            1	len(tuple)
                计算元组元素个数。	
            2	max(tuple)
                返回元组中元素最大值。	
            3	min(tuple)
                返回元组中元素最小值。	
            4	tuple(iterable)
                将可迭代对象转换为元组。
        装包与解包
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
    集合类型：
        可以使用大括号 { } 或者 set() 函数创建集合，
        集合中的元素可以无序，但不可以重复，另外，元素必需是不可变类型
        要想实现集合的嵌套，可借助frozenset方法
        注意：
            创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典
            set中的元素内部会自动排序，如
            set1={1,2,5,4}  对set1输出的结果为：{1, 2, 4, 5}
        格式：parame = {value01,value02,...} 或 set(value)
        因为是无序的，所以与字符串、列表、元组不同，集合不支持通过[]进行下标索引
        集合支持 -(差集) |(并集) &(交集) ^(并集-交集) 等运算，他们有相同的运算优先级
        使用举例：
            a = set('abracadabra')
            b = set('alacazam')
            print(a - b)     # a 和 b 的差集
            print(a | b)     # a 和 b 的并集
            print(a & b)     # a 和 b 的交集
            print(a ^ b)     # a 和 b 中不同时存在的元素
        内置方法：
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
        使用注意事项：
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
    字典类型：
        字典是一种映射类型，字典用 { } 标识，它是一个无序的 键(key) : 值(value) 的集合
        字典跟列表具有可比性：列表中的元素是通过偏移来存储的，字典中的元素是通过键来存取的
        键(key)必须使用不可变类型，且在同一个字典中，键(key)必须是唯一的，但值不必唯一
        一个字典中可以同时存在不同类型的键（只要是不可变类型就行）
        值可以取任何数据类型，但键必须是不可变的，如字符串，数字
        构造函数 dict() 可以直接从键值对序列中构建字典
        使用举例：
            dic = {}
            dic['one'] = "1 - 菜鸟教程"  #如果没有，就自动添加新的元素
            dic[2]     = "2 - 菜鸟工具"
            dic2 = {'name': 'runoob','code':1, 'site': 'www.runoob.com'}
            print (dic['one'])       # 输出键为 'one' 的值
            print (dic[2])           # 输出键为 2 的值
            print (dic2)             # 输出完整的字典
            print (dic2.keys())      # 输出所有键（返回值为dict_keys类型)
            print (dic2.values())    # 输出所有值（返回值为dict_values类型)
            print (dic2.items())     # 输出所有键值对（返回值为dict_items类型)
            dic = dict([('Runoob', 1), ('Google', 2), ('Taobao', 3)]) 
                等同于：
                tup1=('Runoob', 1)
                tup2=('Google', 2)
                tup3=('Taobao', 3)
                lst=[tup1,tup2,tup3]    
                dic=dict(lst)        # 从元组列表构建
            del dic['Runoob']        # 删除字典中的元素（键值对）
            dic.clear()              # 清空
            del dic                  # 删除字典
        部分内置函数&方法
            1	len(dict)
                计算字典元素个数，即键的总数。	
            2	str(dict)
                输出字典，可以打印的字符串表示。	
            3	type(variable)
                返回输入的变量类型，如果变量是字典就返回字典类型。
            1	dict.clear()
                删除字典内所有元素
            2	dict.copy()
                返回一个字典的浅复制
            3	dict.fromkeys((seq[, value])
                创建一个新字典，以序列seq中元素做字典的键，
                val为字典所有键对应的初始值,默认为None
            4	dict.get(key, default=None)
                返回指定键的值，如果键不在字典中返回 default 设置的默认值
            5	key in dict
                如果键在字典dict里返回true，否则返回false
            6	dict.items()
                以列表返回一个视图对象dict_items
            7	dict.keys()
                返回一个视图对象dict_keys
            8	dict.setdefault(key, default=None)
                和get()类似, 但如果键不存在，将会添加键并将值设为default
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
        使用举例：
            将字典中的键和值互换：
                >>> dic = {'a': 1,'b': 2,'c': 3}
                >>> reverse = {v: k for k, v in dic.items()}  
                #每次item赋值给k,v时，会发生解包
            通过 values 取到 key 的方法：
                >>> dic={"a":1,"b":2,"c":3}
                >>> list(dic.keys())[list(dic.values()).index(1)]
    Python数据类型转换：
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
    推导式：
        列表推导式：[表达式 for 变量 in 可迭代对象]  或  [表达式 for 变量 in 可迭代对象 if 条件]
        元组推导式：(表达式 for 变量 in 可迭代对象)  或  (表达式 for 变量 in 可迭代对象 if 条件)
        集合推导式：{表达式 for 变量 in 可迭代对象}  或  {表达式 for 变量 in 可迭代对象 if 条件}
        字典推导式：{表达式:表达式 for 变量 in 可迭代对象}  或
                    {表达式：表达式 for 变量 in 可迭代对象 if 条件}
        条件：对变量或变量表达式进行判断，滤除不符合的变量
        经常简单使用range()方法获得可迭代对象：
            range([start,] stop[, step])
            返回一个由整数元素组成的range对象，该对象像列表一样，可迭代
            start默认为0，step默认为1
    运算符：
        算术运算符
            +	加        - 两个对象相加	a + b 输出结果 31
            -	减        - 得到负数或是一个数减去另一个数	a - b 输出结果 -11
            *	乘        - 两个数相乘或是返回一个被重复若干次的字符串	a * b 输出结果 210
            /	除        - x 除以 y	b / a 输出结果 2.1
            %	取模      - 返回除法的余数	b % a 输出结果 1
            **	幂        - 返回x的y次幂	a**b 为10的21次方
            //	取整除    - 向下取接近商的整数
        比较（关系）运算符
            ==	等于      - 比较对象是否相等	(a == b) 返回 False。
                            默认会调用对象的__eq__()成员方法
            !=	不等于    - 比较两个对象是否不相等	(a != b) 返回 True。
            >	大于      - 返回x是否大于y	(a > b) 返回 False。
            <	小于      - 返回x是否小于y。所有比较运算符返回1表示真，返回0表示假。
                            这分别与特殊的变量True和False等价。
                            注意，这些变量名的大写。(a < b) 返回 True。
            >=	大于等于  - 返回x是否大于等于y。	(a >= b) 返回 False。
            <=	小于等于  - 返回x是否小于等于y
        赋值运算符
            =	简单的赋值运算符	c = a + b 将 a + b 的运算结果赋值为 c
            +=	加法赋值运算符	    c += a 等效于 c = c + a
            -=	减法赋值运算符	    c -= a 等效于 c = c - a
            *=	乘法赋值运算符	    c *= a 等效于 c = c * a
            /=	除法赋值运算符	    c /= a 等效于 c = c / a
            %=	取模赋值运算符	    c %= a 等效于 c = c % a
            **=	幂赋值运算符	    c **= a 等效于 c = c ** a
            //=	取整除赋值运算符	c //= a 等效于 c = c // a
            :=	海象运算符，可在表达式内部为变量赋值（Python3.8 版本新增）
                if (n := len(a)) > 10:
                    print(f"List is too long (expected <= 10)")
        逻辑运算符
            x and y	布尔"与" - 如果 x 为 False，x and y 返回 x 的值，否则返回 y 的计算值。	
            x or y	布尔"或" - 如果 x 是 True，它返回 x 的值，否则它返回 y 的计算值。	
            not x	布尔"非" - 如果 x 为 True，返回 False 。如果 x 为 False，它返回 True。
            例：a=10;b=20;  (a and b) 返回 20，(a or b) 返回 10，(not a) 返回 False
            拓展：print("a") and print("b")    输出 "a"
                  type(print("a")) 返回对象 <class 'NoneType'> , 该对象用作表达式时，被认定为假
                  除此之外，空列表、空字典、空元组、空字符串等，用于逻辑表达式时，也会被认定为假
                  进一步测试，如果自定义的函数，没有返回值，则等同于该函数返回了 NoneType 类型
                  常量/关键词 None 即为 NoneType 类型对象，常用其表征 null 对象，函数默认返回 None
                  定义时，函数的参数可以指定默认值为 None
                  在正则表达式中，如果没有匹配到对象，也是返回 None
                  None因为是内置对象，所以是单例的，True、False、小整数等，也都是单例对象
        位运算符
            &	按位与运算符
            |	按位或运算符
            ^	按位异或运算符
            ~	按位取反运算符
            <<	左移动运算符（非循环）
            >>	右移动运算符（非循环）
        成员运算符
            in	如果在指定的序列中找到值返回 True，否则返回 False。	
            not in	如果在指定的序列中没有找到值返回 True，否则返回 False。
            例： 3 in [1,2,3] 返回 True， 4 not in [1,2,3] 返回 True
        身份运算符
            is	是判断两个标识符是不是引用自一个对象， x is y, 类似 id(x) == id(y) 
                如果引用的是同一个对象则返回 True，否则返回 False
            is not	是判断两个标识符是不是引用自不同对象， x is not y ，类似 id(x) != id(y)
                如果引用的不是同一个对象则返回结果 True，否则返回 False。
        运算符优先级
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
            记忆： 指单基移位比等,赋值is in逻辑
    常用数学函数：
        运算函数：
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
        随机数函数：
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
        三角函数：
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
    变量的作用域：
        python中变量的作用域及用法，同C语言有很大的差别
        变量的五种作用域：
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
    流程控制：
        if-elif-else 
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
        while-else
            语法：
            while 判断条件：
                执行语句
            else：
                执行语句
            在 Python 中没有 do..while 循环，else部分不是必需的
        for-in-else
            语法：
            for 变量 in 序列:
                执行语句
            else:
                执行语句
            注：else部分不是必需的
            提示：因为python支持自动封包/解包，所以for语句中，变量可以为多个
            当想使用for完成固定次数的循环时，可搭配range()函数使用，如：
            for i in range(5):  
            range函数语法：range([start,] stop[, step])
            返回一个由整数元素组成的range对象，该对象像列表一样，可迭代
            start默认为0，step默认为1
        while/for语句后的else有什么用：
            对于while语句，之后当条件不满足（结束循环）时，才会执行else语句部分
            对于for语句，只有在枚举序列完结（结束循环）时，才会执行else语句部分
            从上可见，else部分都是在循环完成会，才会执行到
            这和直接在while/for句式结束后书写普通语句有什么区别？else是不是很鸡肋？
            其实不然，else语句部分的执行是有条件的：之后在循环正常完结，
            即while条件不满足后，或for枚举完结后，即循环正常结束后，else才会执行，
            如果是因为break语句导致的不正常完结，else部分是不会执行的
            所以我们可以在else部分书写一些只有在循环正常结束后，才允许执行的句子
        break:
            break 语句可以跳出 for 和 while 的循环体。
            如果你从 for 或 while 循环中终止，任何对应的循环 else 块将不执行
        continue:
            continue 语句被用来告诉 Python 跳过当前循环块中的剩余语句，然后继续进行下一轮循环
        pass:
            pass是空语句，不做任何事情，一般用做占位语句，是为了保持程序结构的完整性。
            如想使用一个空循环进行等待，可以用：while True: pass
            或如 if x>1 : pass #需要对x>1的情况进行处理，但具体该怎么做先临时空着，待完成
        python不支持switch-case句法
    迭代器：
        iter(iterable) -> iterator
        iter(callable, sentinel) -> iterator
        参数说明：
            iterable：
                可迭代类，基本类型中的字符串、列表、元组、集合、字典都是可迭代类
                自定义类实现了__iter__()和__next__()方法（两者缺一不可）时，该类为迭代器类
                    该类可以被for-in枚举，并可以作为iter()方法的参数，表明该类属于可迭代类型，
                    用 isinstance(o,Iterator) 方法测试，返回为 True，表明该类属于迭代器类
                    迭代器类属于可迭代类（子集）：
                        迭代器类不能通过index索引某个元素，不支持获取元素总个数，
                        只能通过next()单向前进
                        迭代器的这种流特性，使得它可以表示一个无限的数据流，如全体自然数
                        而这是用list所不能实现的
                    #关于__iter__()和__next__()方法：
                    __iter__函数向系统声明这个类可迭代，__next__定义了具体的迭代器，
                    正式的说法是：
                    实现了__iter__方法的对象是可迭代对象，实现了__next__方法的对象是迭代器
                    在代码执行过程中，for循环函数会自动检查系统信息，识别__iter__函数，
                    然后自动调用对应的__next__函数，生成一个迭代器
                自定义的类，如果定义了iter()方法或getitem()方法，该类为可迭代类
                    经测试，自定义类如果只实现了__getitem__成员方法，
                    该类可以被for-in枚举，并可以作为iter()方法的参数，表明该类属于可迭代类型，
                    但用 isinstance(o,Iterator) 方法测试，返回为 False，表明该类不是迭代器类，
                    对字符串、列表、集合等类型用 isinstance(o,Iterator) 方法测试，返回为 False
                    表明这些类型都只是可迭代类，但不是迭代器类
                    猜测这些容器类型内部，也是只实现了__getitem__成员方法
                    进一步说，list、tuple、dict、set、str，及实现了getitem()方法的自定义类，
                    都可统一称之为‘集合类型’，他们提供了按索引号获取元素的手段。
        测试自定义可迭代类：
            测试一：
                from collections import Iterable
                class myclass_1:
                    def __init__(self,*args):
                        self._list=[1,2,3,4]
                        self._index=0
                    def __getitem__(self,index):
                        return self._list[index%4-1]  #对返回数据类型不限制
                c1 = myclass_1()
                for i in c1: print(i)       #会循环输出1、2、3、4
                iter(c1)                    #不报错
            测试二：
                from collections import Iterable
                class myclass_2:
                    def __init__(self,*args):
                        self._list=[1,2,3,4]
                        self._index=0
                    def __iter__(self):
                        return self         #要求返回的是可迭代对象类型
                    def __next__(self):     #该方法必须配合__ter__方法而存在
                        self._index=self._index+1
                        if self._index>4:
                            self._index=1
                        return self._list[self._index%4-1]
                c2 = myclass_2()
                for i in c2:  print(i)      #会循环输出1、2、3、4
                iter(c2)                    #不报错
                经测试，__next__()方法必须存在，否则在后面使用for-in与iter()时会报错
                报错信息：iter() returned non-iterator of type 'myclass_2'
            测试三：
                测试代码（对测试一、测试二的整合与扩展）
                    from collections.abc import Iterator
                    #0. 定义函数，对参数进行测试
                    def tell(o):
                      if isinstance(o,Iterator): 
                          print("{0} is Iterator".format(type(o)))
                      else:
                          print("{0} is not Iterator".format(type(o)))
                      try:
                          print("for迭代结果: ",end='')
                          for i in o:  
                              print(i,end='  ')       #会循环输出1、2、3、4
                          print("\n")
                      except:
                          print("\n")
                      iter(o)                         #不报错
                    #1. 定义迭代器类1，并进行测试
                    class myclass_1:
                        def __init__(self,*args):
                            self._list=[1,2,3,4]
                            self._index=1
                        def __getitem__(self,index):
                            if index>4:
                                raise StopIteration()
                            return self._list[index]  #对返回数据类型不限制
                    c1 = myclass_1()
                    tell(c1)
                    #2. 定义迭代器类2，并进行测试
                    class myclass_2:
                        def __init__(self,*args):
                            self._list=[1,2,3,4]
                            self._index=0
                        def __iter__(self):
                            return self         #要求返回的是可迭代对象类型
                        def __next__(self):     #该方法必须配合__ter__方法而存在
                            self._index=self._index+1
                            if self._index>4:
                                raise StopIteration()
                            return self._list[self._index%4-1]
                    c2 = myclass_2()
                    tell(c2)
                    #3. 测试字符串
                    c3="asdf"
                    tell(c3)
                    #4. 测试列表
                    c4=[1,2,3,4]
                    tell(c4) 
                    #5. 测试集合
                    c5={1,2,3,4,5}
                    tell(c5)
                输出结果
                    <class '__main__.myclass_1'> is not Iterator
                    for迭代结果: 1  2  3  4
                    <class '__main__.myclass_2'> is Iterator
                    for迭代结果: 1  2  3  4
                    <class 'str'> is not Iterator
                    for迭代结果: a  s  d  f
                    <class 'list'> is not Iterator
                    for迭代结果: 1  2  3  4
                    <class 'set'> is not Iterator
                    for迭代结果: 1  2  3  4  5
                结果总结
                    ● 自定义类1，只实现了__getitem__成员方法，
                    该类可以被for-in枚举，并可以作为iter()方法的参数，
                    表明该类属于可迭代类型，
                    但用 isinstance(o,Iterator) 方法测试，返回为 False
                    ● 自定义类2，实现了__iter__()和__next__()方法，
                    该类可以被for-in枚举，并可以作为iter()方法的参数，
                    表明该类属于可迭代类型，
                    用 isinstance(o,Iterator) 方法测试，返回为 True
                    ● 字符串、列表、集合等类型，属于可迭代类型
                    但用 isinstance(o,Iterator) 方法测试，返回为 False
                    猜测这些容器类型内部，只实现了__getitem__成员方法                
    生成器：
        在 Python 中，使用了 yield 的函数被称为生成器（generator）
        举例：
            def func():
                print("---1---")
                yield 1    #yield会把后面的数据包装成generator对象进行返回
                print("---2---")
                yield "abc"
                print("---3---")
                yield [1,2,3]
                print("---finish---")
            def func2():
                yield 2
            def func3()
                return 3
            def func4()
                print("abc")
            def func5()
                func()
            def func6()
                return func()
            f1 = func()
            f2 = func2()
            f3 = func3()
            f4 = func4()
            f5 = func5()
            f6 = func6()
            type(f1) #<class 'generator'>
            type(f2) #<class 'generator'>
            type(f3) #<class 'int'>
            type(f4) #<class 'NoneType'>
            type(f5) #<class 'NoneType'>
            type(f6) #<class 'generator'>
        说明： 
            当执行完 f1=func()时，并没有打印出"---1---"
            而像如执行 f4=func4()时，是有"abc"打印输出的
            这说明在f1=func()时，在func()中，第一条语句执行前
            就执行了一条（也可能是多条）隐藏语句，
            该隐藏语句返回了generator对象
            当执行完第一条next(f1)后，才还是有"---1---"输出。
            另外，从f6=func6()中可以发现，
            迭代器函数是支持嵌套返回的，返回的类型仍然是迭代器对象
        

            
