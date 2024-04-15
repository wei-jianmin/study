<catalog s0/s4,t1/s8/s12 text_line_prefix=- super_text_line_prefix=.>
第一卷
    第3章 基本语法
        -Java区分大小写；每个句子必须用分号结束；
        .main函数
            类中可以包含main函数，main函数的参数为 Strings[] args
            每个函数前面带 public 关键字，main函数前面还应该带 static 关键字
            返回值为 void，如果正常退出，则java应用程序返回0，
            如果希望终止时返回其它代码，则应调用System.exit()方法
        .类定义：
            类名的命名规范为大驼峰命名法
            源代码文件的名字，与公共类的名字相同（并用.java作为扩展名）
            类名前带有public关键字，类的结束大括号后面无需跟 ; 作为结束符
            在命令行中通过java命令运行程序时，后面跟的是类名，而不是class文件名
        .注释：
            单行注释：//
            多行注释：/*   */
            文档注释：/**  */
                这种注释方法可用来自动生成文档
        .数据类型：
            整型：byte(1字节) short(2字节) int(4字节) long(8字节) 
            浮点：float(4字节) double(8字节)
            数值：长整形前缀为L或l，十六进制前缀为0x或0X，
                  八进制前缀为0（不建议使用8进制数），二进制前缀为0b或0B
                  数值支持使用下划线分隔，以使数值易读，编译器会去除这些下划线
                  float带有后缀F或f，double后缀为D或d，不带默认为double
                  NaN ：区别于正/负无穷大，非0值除0的结果是无穷大，而负数开平方的结果是 NaN
                  三者分别表示为：Double.POSITIVE_INFINITY, Double.NEGTIVE_INFINITY, Double.NaN
                  不能通过 if(x==Double.NaN) 判断，而应通过 if(Double.isNan(x)) 判断
            字符：char类型占2个字节
                除了可赋值' '表示的字符常量外，
                还可赋值十六进制数，以 \u 或 \U 开头，范围从 \u0000 到 \uffff
                注意，\u除了能表达普通字符外，还能表达转义字符，
                如 \u000a 等同于 \n， "（双引号） 等同于 \u0022
                所以 "\u0022+\u0022" 等同于 "" + "" （两个空字符串相加，u0022在编译期就被替换为双引号），而不是 "\" + \""
                特别的，如 //c:\users\administrator 会报错，
                因为 \u 后面没有跟着4个十六进制数
            布尔：boolean
                在 C 中，数值是否为0或指针是否为空可作为布尔判断依据，在java中不允许
            常量：在变量类型前加关键字 finial 指示常量
                finial指示这个变量只能被赋值1次（c语言用的是const关键字）
        .运算符：
            同 C 语言
        .类型转换：
            同 C 语言，如 double a=3.2; int b = (int) a;
        .移位运算：
            与C相比，增加了>>>，用0填充高位，而>>则是用符号位填充高位
            C/C++中，>>的实现方式没有规定，所以实现者可能使用算数移位（扩展符号位）
            或者使用逻辑移位（高位填充0），也就是说，C/C++的>>移位结果依赖于具体实现
        .枚举：
            enum Size { SMALL, MEDIUM, LARGE };
            Size s = Size.SMALL;
        字符串：
            java通过String类变量来存放字符串
            区别于c++的string类，java的String类不支持变量的修改
            java中的三种常量池：
                https://cloud.tencent.com/developer/article/1450501
                JVM常量池主要分为Class文件常量池、运行时常量池，全局字符串常量池，基本类型包装类对象常量池
                Class文件常量池
                    用 javap -v class文件，可查看class文件的常量池内容
                    class文件常量池主要存放两大常量：字面量和符号引用
                    1) 字面量
                        ● 文本字符串：如 String s = "abc";中的"abc"
                        ● 用final修饰的成员变量，包括静态变量、实例变量和局部变量
                    2) 符号引用
                        符号引用主要设涉及编译原理方面的概念，包括下面三类常量:
                        ● 类和接口的全限定名，也就是java/lang/String
                        ● 字段的名称和描述符，字段也就是类或者接口中声明的变量，包括类级别变量和实例级的变量
                        ● 方法中的名称和描述符，也即参数类型+返回值
                运行时常量池
                    运行时常量池是方法区的一部分，所以也是全局贡献的
                    jvm在执行某个类的时候，必须经过加载、链接（验证、准备、解析）、初始化，
                    类对象和普通对象是不同的，
                    类对象是在类加载的时候完成的，是jvm创建的并且是单例的，作为这个类和外界交互的入口，
                    而普通的对象一般是在调用new之后创建。
                    类加载时，把不同的class类常量池加载到运行时常量池，不同的类共用一个运行时常量池
                    不同class文件常量池中的相同的字符串会被优化为一份
                    在类的解析阶段，还会把符号引用翻译为对运行时常量池中值的引用
                全局字符串常量池
                    全局字符串池里的内容是在类加载完成，经过验证，准备阶段之后在堆中生成字符串对象实例，
                    然后将该字符串对象实例的引用值存到string pool中，实际的对象实例则是存在堆中
                    Java中创建字符串对象的两种方式： String s0 = "hello", s1 = new String("hello");
                    第1种方法中的"hello"值，是在编译期就已经确定的，它会直接进入class文件常量池中；
                    但上面两种字符串对象创建方式，无论那种，都还在堆上创建一个"hello"对象，
                    在创建s0对象的时候，还会把该对象的引用存放到全局字符串常量池中，
                    这样当后面再碰到 String s2 = "hello" 这样的句子时，
                    虚拟机会先去字符串池中找是否有equals("hello")的String对象引用，
                    如果有，就把在字符串池中"Hello"的引用复制给s2，这样就避免了新的对象的创建
                    但对于s1对象，因为它带了new关键字，所以一定会在堆中创建一个新对象，
                    而全局字符串常量池的作用就是为了减少对象的创建而存在的，
                    所以像s1这种铁定会创建对象的，是没必要将其引用存放在全局字符串常量池中的
            String类的成员方法（50多个）：
                + : 拼接字符串
                substring(开始位置，结束位置)：提取子字符串
                join(分隔符，字符串1，...,字符串n) : 拼接多个字符串，并指定分隔符
                char charAt(int index)：返回指定位置的代码单元
                int codePointAt(int index)：返回指定位置的码点
                int compareTo(String other): 字符串比较大小
                IntStream codePoints()：将该字符串的码点作为一个流返回
                new String(int[] codePoints，int offset,int count)：用数组中从offset开始的count个码点构造一个字符串
                boolean equals(Object other) : 判断字符串是否相等
                boolean equalsIgnoreCase(String other)：判断字符串是否相等，忽略大小写
                boolean startsWith(String prefix)
                boolean endsWith(string suffix)
                int indexOf(String str, int fromIndex=0)
                int indexOf(int cp, int fromIndex) : cp标识码点（0平面的码点等于代码单元）
                int lastindexOf(int cp)
                int lastindexOf(int cp, int formIndex)
                int length()
                int codePointCount(int startIndex,int ednIndex) : 计算代码点数，最后没有配对成功的也计入代码点数
                String replace(CharSequence oldString, CharSequence newString) : 替换子字符串，返回一个新字符串对象
                String substring(int beginIndex) : 提取子字符串，返回一个新字符串对象
                String substring(int beginIndex, int endIndex): 提取子字符串，返回一个新字符串对象
                String toLowerCase()
                String toUpperCase()
                String trim() : 删除头部和尾部的空格，返回一个新字符串对象
                String join(CharSequence delimiter, CharSequence... elements): 用定界符连接所有元素
            测试字符串是否相等：
                应该使用String的equals()方法或equalsIgnortCase()方法
                ==用于判断两个引用是否相等（引用的同一个对象）
            空串与Null串：
                空串""是长度为0的字符串, 用 if(str.length()==0) 或 if(str.equals("")) 判断
                String变量还可以存放一个特殊的值:null，判断方法为： if(str == null)
                有时要对上面两种情形同时判断，才能保证该字符串变量有效且不为空：
                if(str!=null && str.length()>0)
            码点和代码单元：
                码点（码位）和代码单元（码元） ：
                    与编码表中某个字符对应的码值，在Unicode标准中，码点的标识方法以 U+ 为前缀
                    因为2个字节无法存放全世界所有的字符与文字，所以将码点分为了17个将级别：
                    第0级别(/平面)码点的范围：U+0000 ~ U+FFFF，涵盖经典的 Unicode 代码
                    第1级别(/平面)码点的范围：U+10000 ~ U+1FFFF
                    第2级别(/平面)码点的范围：U+20000 ~ U+2FFFF
                    。。。
                    第16级别(/平面)码点的范围：U+100000 ~ U+10FFFF
                    所有级别(/平面)码点的范围：U+0000 ~ U+10FFFF
                    所以一个码点，也能是2个字节（1个代码单元），也可能是4个字节（2个代码单元）
                由码位得到码元：
                    首先，Unicode规定，在第0平面（BMP平面），U+D800 ~ U+DFFF范围内的值不对应任何字符
                    本来第1平面~第16平面的码点范围是：U+1000 ~ U+10FFFF,
                    将这个范围值减去 0x1000 后，范围变为： U+0000 ~ U+0FFFFF, 需要有 20bit 才能存下
                    也即是说，需要2个双字节（2个代码单元）才能存下（一个双字节16bit）
                    我们可以将这 20bit 分为高低 2 个 10bit（10bit的范围 0x0 ~ 0x3FF）
                    让每个代码单元存（共16bit）的低10bit来存放这些数值，
                    为了与0平面的码位进行区分，我们还要为这2个代码单元指定前缀，
                    因为前面说了，在第0平面的，U+D800 ~ U+DFFF范围内的值不对应任何字符
                    所以我们将高 10bit 加上 U+D800（0B1101_1000_0000_0000）得到：
                    0B1101_1000_0000_0000 ~ 0B1101_1011_1111_1111，即 0XD800 ~ 0XDBFF
                    再将低 10bit 加上 U+DC00（0B1101_1100_0000_0000）得到：
                    0B1101_1100_0000_0000 ~ 0B1101_1111_1111_1111，即 0XDC00 ~ 0XDFFF
                    所以，我们可以判断：
                    如果一个码元（2字节）落于 0XD800 ~ 0XDBFF 之间（高6位是 1101_10），
                    则这个码元存了非0平面码位的高 10bit
                    如果一个码元（2字节）落于 0XDC00 ~ 0XDFFF 之间（高6位是 1101_11），
                    则这个码元存了非0平面码位的低 10bit
                    如果一个码元（2字节）没有落于 0XD800 ~ 0XDFFF 之间（高5位不是 1101_1），
                    则这个码元是个0平面的码值
            StringBuilder 和 StringBuffer：
                 当对字符串进行修改的时候，需要使用 StringBuffer 和 StringBuilder 类。
                 和 String 类不同的是，StringBuffer 和 StringBuilder 类的对象能够被多次的修改，并且不产生新的未使用对象
                 在使用 StringBuffer 类时，每次都会对 StringBuffer 对象本身进行操作，而不是生成新的对象，
                 所以如果需要对字符串进行修改推荐使用 StringBuffer。
                 StringBuilder 类在 Java 5 中被提出，它和 StringBuffer 之间的最大不同在于 
                 StringBuilder 的方法不是线程安全的（不能同步访问）
                 由于 StringBuilder 相较于 StringBuffer 有速度优势，所以多数情况下建议使用 StringBuilder 类
                 StringBuffer 方法
                    1	StringBuffer append(String s)                   将指定的字符串追加到此字符序列。
                    2	StringBuffer reverse()                          将此字符序列用其反转形式取代。
                    3	publicelete(int start, int end)                 移除此序列的子字符串中的字符。
                    4	insert(int offset, int i)                       将 int 参数的字符串表示形式插入此序列中。
                    5	insert(int offset, String str)                  将 str 参数的字符串插入此序列中。
                    6	replace(int start, int end, String str)         使用给定 String 中的字符替换此序列的子字符串中的字符
                    7	int lastIndexOf(String str)                     返回最右边出现的指定子字符串在此字符串中的索引。
                    8	int lastIndexOf(String str, int fromIndex)      返回 String 对象中子字符串最后出现的位置。
                    9	int length()                                    返回长度（字符数）。
                    10	void setCharAt(int index, char ch)              将给定索引处的字符设置为 ch。
                    11	void setLength(int newLength)                   设置字符序列的长度。
                    12	CharSequence subSequence(int start, int end)    返回一个新的字符序列，该字符序列是此序列的子序列。
                    13	String substring(int start)                     返回一个新的 String，它包含此字符序列当前所包含的字符子序列。
                    14	String substring(int start, int end)            返回一个新的 String，它包含此序列当前所包含的字符子序列。
                    15	String toString()                               返回此序列中数据的字符串表示形式
                    17	int capacity()                                  返回当前容量。
                    18	char charAt(int index)                          返回此序列中指定索引处的 char 值。
                    19	void ensureCapacity(int minimumCapacity)        确保容量至少等于指定的最小值。
                    20	void getChars(int srcBegin, int srcEnd, char[] dst, int dstBegin)   将字符从此序列复制到目标字符数组 dst。
                    21	int indexOf(String str)                         返回第一次出现的指定子字符串在该字符串中的索引。
                    22	int indexOf(String str, int fromIndex)          从指定的索引处开始，返回第一次出现的指定子字符串在该字符串中的索引。
        输入输出：
            -打印输出到“ 标准输出流”（即控制台窗口）只要调用 System.out.println 即可    
            -然而，读取“ 标准输人流” System.in 就没有那么简单了
            -要想通过控制台进行输人，首先需要构造一个 Scanner 对象，并与“ 标准输人流” System.in 关联 
            -Scanner in = new Scanner(System.in);
            -就可以使用 Scanner 类的各种方法实现输入操作了
            -例如， nextLine() 方法将输入一行、next()读取一个单词（以空白为分隔符）、
            -nextInt()读取一个整数、nextDouble()读取一个浮点数
            -最后，在程序的最开始添加上一行  import java.util.*;  //Scanner 类定义在java.util 包中
            -当使用的类不是定义在基本java.lang 包中时， 一定要使用 import 指示字将相应的包加载进来
            -从控制台读取密码
                因为输入是可见的， 所以 Scanner 类不适用于从控制台读取密码
                Java SE 6 特别引入了 Console 类实现这个目的：
                Console cons = System.console();
                String username = cons.readLine("User name: ")；
                char [] passwd = cons.readPassword("Password: ");
                采用 Console 对象处理输入不如采用 Scanner 方便。每次只能读取一行输入， 
                而没有能够读取一个单词或一个数值的方法
            Scanner类提供的方法
                · Scanner (InputStream in)  用给定的输入流创建一个 Scanner 对象。
                · String nextLine( )        读取输入的下一行内容。
                · String next( )            读取输入的下一个单词（以空格作为分隔符)。
                · int nextlnt( )
                · double nextDouble( )      读取并转换下一个表示整数或浮点数的字符序列。
                · boolean hasNext( )        检测输人中是否还有其他单词。
                · boolean hasNextInt( )
                · boolean hasNextDouble( )  检测是否还有表示整数或浮点数的下一个字符序列。
            格式化输出
                可以使用 SyStem.0Ut.print(x) 将数值 x 输出到控制台上
                这条命令将以 x 对应的数据类型的所有非0数字位数打印输出 X （意味着所有小数位都会打印出来）
                Java SE 5.0 沿用了 C 语言库函数中的 printf方法，如 System.out.printf("%,.2f",10/3.0);
                注：可以使用 %s 转换符格式化任意的对象，
                    对于任意实现了 Formattable 接口的对象都将调用 formatTo 方法
                    否则将调用 toString 方法， 它可以将对象转换为字符串
                可以使用静态的 String.format 方法创建一个格式化的字符串：
                String message = String.format("Hello, %s. Next year , you'll be %d", name, age) ;
                关于时间的格式化问题
                    在旧的代码中，使用了 Date() 类，在新代码中，应该使用 java.time 包中的方法（第II卷第6章会介绍）
                    System.out.printfC("%l$s %2$tB %2$te, %2$tY", "Due date:", new DateQ)； //格式控制参本书第59页
            文件输入与输出
                要想对文件进行读取， 就需要一个用 File 对象构造一个 Scanner 对象
                Scanner in = new Scanner(Paths.get("niyflle.txt") , "UTF-8") ;
                如果省略字符编码， 则会使用运行这个 Java 程序的机器的“ 默认编码”，（受机器影响）
                现在，就可以利用前面介绍的任何一个 Scanner 方法对文件进行读取
                要想写入文件， 就需要构造一个 PrintWriter 对象。
                PrintWriter out = new PrintWriter("myfile.txt", "UTF-8") ;
                如果文件不存在，创建该文件。
                可以像输出到 System.out—样使用 print、 println 以及 printf命令。
                警告：Scanner还支持字符串作为构造参数，对这个字符串进行读取
                    如 Scanner in = new Scanner("c:/myfile.txt"); 
                    这并不是打开一个文件进行读取，而是读取这个字符串
                如果使用集成开发环境， 那么启动路径将由 IDE 控制（这会影响查找相对路径的文件）
                可以使用这种方法获取当前路径：String dir = System.getProperty("user.dir"):
                如果用一个不存在的文件构造一个 Scanner, 
                或者用一个不能被创建的文件名构造一个 PrintWriter,那么就会发生异常
        流程控制：
            总括：
                Java 的控制流程结构与 C 和 C++ 的控制流程结构一样， 只有很少的例外情况
                没有 goto 语句， 但 break 语句可以带标签， 可以利用它实现从内层循环跳出的目的
                另外，还有一种变形的 for 循环， 在 C 或 C++ 中没有这类循环。 
                它有点类似于 C Sharp 中的 foreach 循环
            与c++区别：
                块作用域：
                    在 C++ 中， 可以在嵌套的块中重定义一个变量。在内层定义的变量会覆盖在外层定义的变量。
                    这样， 有可能会导致程序设计错误， 因此在 Java 中不允许这样做
                从 Java SE 7 开始， case 标签还可以是字符串字面量，如：
                    String s = ...；
                    switch (s.toLowerCase())
                    {
                        case "yes":
                            ...
                            break;
                        ...
                    }
                java中不支持goto，但支持带跳转标签的break，如：
                    ...
                    mark:
                    while(...)
                    {
                        ...
                        for(...)
                        {
                            ...
                            break mark;
                            ...
                        }
                    }
                    ...
                    注：continue语句也支持跳转标签；break跳转语句也可以出现在if语句中
                for枚举：
                    for (variable : collection) statement
                    collection 这一集合表达式必须是一个数组或者是一个实现了 Iterable 接口的类对象
                    如： for(int element:arr) System.out.println(element);
        .大数值
            如果基本的整数和浮点数精度不能够满足需求， 那么可以使用jaVa.math 包中的两个
            很有用的类：Biglnteger 和 BigDecimaL 这两个类可以处理包含任意长度数字序列的数值。
            Biglnteger 类实现了任意精度的整数运算， BigDecimal 实现了任意精度的浮点数运算。
            使用静态的 valueOf 方法可以将普通的数值转换为大数值：
            Biglnteger a = Biglnteger.valueOf(100);
            不能使用人们熟悉的算术运算符（如：+ 和 *) 处理大数值，
            而应使用大数值类提供的add和multiply方法
            注：与 C++ 不同， Java 没有提供运算符重载功能，程序员无法重定义 + 和 * 运算符
            Biglnteger成员方法：
                · Biglnteger add(Biglnteger other)
                · Biglnteger subtract(Biglnteger other)
                · Biglnteger multipiy(Biginteger other)
                · Biglnteger divide(Biglnteger other)
                · Biglnteger mod(Biglnteger other)
                  返冋这个大整数和另一个大整数 other 的和、 差、 积、 商以及余数。
                · int compareTo(Biglnteger other)
                  如果这个大整数与另一个大整数 other 相等， 返回 0; 
                  如果这个大整数小于另一个大整数 other, 返回负数； 否则， 返回正数。
                · static Biglnteger valueOf(1ong x) 返回值等于 x 的大整数
            BigDecimal成员方法：
                · BigDecimal add(BigDecimal other)
                · BigDecimal subtract(BigDecimal other)
                · BigDecimal multipiy(BigDecimal other)
                · BigDecimal divide(BigDecimal other RoundingMode mode) 5.0
                  返回这个大实数与另一个大实数 other 的和、 差、 积、 商。
                  要想计算商， 必须给出舍入方式 （ rounding mode。) 
                  RoundingMode.HALF UP 是在学校中学习的四舍五入方式
                  它适用于常规的计算。有关其他的舍入方式请参看 Apr文档。
                · int compareTo(BigDecimal other)
                  如果这个大实数与另一个大实数相等， 返回 0 ; 
                  要想计算商， 必须给出舍返回负数； 否则，返回正数。
                · static BigDecimal valueOf(1 ong x)
                · static BigDecimal valueOf(1 ong x ,int scale)
                  返回值为 X 或 x / 10^scale 的一个大实数。
        数组
            数组声明：
                数组声明方式，例：int[] a;  
                不过， 上例只声明了变量 a， 并没有将 a 初始化为一个真正的数组
                可使用 new 运算符创建数组：int[] a = new int[len];
                ava中，数组属于引用类型，数组对象可以只声明而不分配空间，
                这与c++不同，c++中，int a[100]; 同时完成了定义和分配空间的工作
                创建一个数字数组时， 所有元素都初始化为 0。boolean 数组的元素会初始化为 false 
                对象数组的元素则初始化为一个特殊值 null, 这表示这些元素（还）未存放任何对象
                如：String[] names = new String[10] ;
                会创建一个包含 10 个字符串的数组， 所有字符串都为null
                与C++不同的一点是，创建的数组对象支持访问length属性，如 a.length
                定义数组时初始化，例：int[] small Primes = new int[] { 2, 3, 5, 7, 11, 13 };
                上面语句可以用简化形式：int[] small Primes = { 2, 3, 5, 7, 11, 13 }; 
                与c++区别的一点是，数组a不是指针，不能通过a+1得到数组的下一个元素
            数组拷贝：
                在 Java 中， 允许将一个数组变量拷贝给另一个数组，如：int[] luckyNumbers = smallPrimes;
                如果希望将一个数组的所有值拷贝到一个新的数组中，应该借助Array类的copyOf方法：
                int[] luckyNumbers = Arrays.copyOf(smallPrimes, luckyNumbers.length) ;
            命令行参数数组：
                public static void main(String[] args)
                与c++不同的是，args[0]不是程序名，而是命令行传来的第一个参数
            数组排序：
                可以用Array.sort(数组) 对数组进行排序（使用的是快速排序法）
            java,util.Arrays提供的方法：
                · static String toString(type[] a) 
                  返回包含 a 中数据元素的字符串， 这些数据元素被放在括号内， 并用逗号分隔。
                  参数： a 类型为 int、long、short、char、 byte、boolean、float 或 double 的数组。
                · static type copyOf(type[] a, int length)
                · static type copyOfRange(type[] a , int start , int end)
                  返回与 a 类型相同的一个数组， 其长度为 length 或者 end-start， 数组元素为 a 的值。
                  参数： a 类型为 int、 long、short、char、byte、boolean、float 或 double 的数组。
                  start  起始下标（包含这个值）0，
                  end    终止下标（不包含这个值）。 这个值可能大于 a.length，这时，结果为 0 或 false。
                  length 拷贝的数据元素长度。如果 length 值大于 a.length， 结果为 0 或 false ;
                         否则， 数组中只有前面 length 个数据元素的拷 W 值。
                · static void sort(t y p e [ 2 a)
                  采用优化的快速排序算法对数组进行排序。
                  参数：a 类型为 int、long、short、char、byte、boolean、float 或 double 的数组。
                · static int binarySearch(type[] a , type v)
                · static int binarySearch(type[] a, int start, int end , type v) 
                  采用二分搜索算法查找值 v。如果查找成功， 则返回相应的下标值； 
                  否则返回一个负数值r。 -r-1 是为保持 a 有序 v 应插入的位置。
                  参数： 
                  a     类型为 int、 long、 short、 char、 byte、 boolean 、 float 或 double 的有序数组。
                  start 起始下标（包含这个值）。
                  end   终止下标（不包含这个值。)
                  v     同 a 的数据元素类型相同的值。
                · static void fi11(type[] a , type v)
                  将数组的所有数据元素值设置为 v。
                  参数： 
                  a     类型为 int、 long、short、char、byte、boolean 、 float 或 double 的数组。
                  v     与 a 数据元素类型相同的一个值。
                · static boolean equals(type[] a, type[] b)
                  如果两个数组大小相同， 并且下标相同的元素都对应相等， 返回 true。
                  参数： a、 b 类型为 int、long、short、char、byte、boolean、float 或 double 的两个数组。
            多维数组
                double[] [] balances;
                double[] [] balances = new double[NYEARS] [NRATES]
                int[][] magicSquare = { {16, 3, 2, 13}，{5, 10, 11, 8},(9, 6, 7, 12},{4, 15, 14, 1} }；
                注 for枚举不能一次性枚举多维数组的每一个元素，而应用一个2层循环枚举一个二维数组
                可以用Arrays.deepToString(数组)，将数组内容转为一个字符串
            不规则数组
                java实际上没有多维数组，只有一维数组，多维数组被解释为"数组的数组"：
                如二维数组，引用一个一维数组对象，该数组的每个元素又都是一个一维数组的引用
                所以，可以方便的将上面的balances二维数组的两行进行交换：
                    double[] temp = balances[i]:
                    balances[i] = balances[i + 1];
                    balances[i + 1] = temp;
                还可以构造一个不规则数组，即数组的每一行都有不同的长度：
                    int [][] odds = new int [MAX] [] ;  //长度MAX的一维数组，每个元素又都是int[]类型
                    for (int n = 0; n < MAX ; n++)
                        odds[n] = new int [n + 1] ;
    第4章 对象和类
        表达类关系的UML符号
            file://imgs/表达类关系的UML符号.png
        .创建对象
            要想使用对象，就必须首先构造对象， 并指定其初始状态。然后，对对象应用方法。
            在 Java 程序设计语言中， 使用构造器（constructor) 构造新实例。
            构造器是一种特殊的方法， 用来构造并初始化对象。
            构造器的名字应该与类名相同。以 Date 为例， Date 类的构造器名为 Date。
            要想构造一个 Date 对象， 需要在构造器前面加上 new 操作符，如下所示：
            new Date()  
            这个表达式构造了一个新对象。 这个对象被初始化为当前的日期和时间
            注：new属于单目运算符，优先级非常高，仅次于.[]和表示方法调用的()。
                和其它单目运算符! -- ++ 表示正负的+- 表示强转的()处于同一等级
            如果需要的话， 也可以将这个对象传递给一个方法：
            System.out.printTn(new Date()) ;
            通常， 希望构造的对象可以多次使用， 因此，需要将对象存放在一个变量中：    
            Date birthday = new Date();
            注意，这里的 birthday 只是指向 Date 对象的一个引用，
            所以像如 Date deadline; 只是定义了一个引用，但它此时却没有引用实际对象
            它的值为null？ 所以此时，该变量还是不能使用的（否则会导致编译错误）
            必须先初始化该变量 deadline = new Date() ;
            或者让该变量引用另一个已存在的对象，如 deatline = birthday;
            这样， deadline 和 birthday 这两个引用类型的变量，将指向同一个内存对象
            在Java中，我们可能永远无法一个对象的真实内存位置，new操作符返回的也是一个引用
            注：就Date类而言，只有无参构造函数、after(Date t)、
                before(Date t)、clone()、compareTo(Date t)、
                equals(Object o)、getTime()、setTime(long t)、
                toString()等几个方法还有用，其它的都已经过时了，
                取而代之的是Calendar类
            注：C++中的引用必须在声明时初始化，但Java中的引用却可以先定义，后赋值
                所以从这一点上来说，它更类似于C++中的指针，但也有一定的安全上的区别：
                在java的使用未初始化的指针，将产生一个运行时错误，而不是获取到一个随机的结果
                另外也不必担心内存的释放问题，Java的垃圾收集器会处理这方面的问题
        .LocalDate类
            用来表示大家熟悉的日历表示法
            不要使用构造器来构造 LocalDate 类的对象。
            实际上，应当使用静态工厂方法 (factory method) 代表你调用构造器
            表达式 Local Date.now() 会构造一个新对象， 表示构造这个对象时的日期。
            可以提供年、 月和日来构造对应一个特定日期的对象： LocalDate.of(1999, 12, 31)
            将对象保存在一个对象变量中：LocalDate newYearsEve = LocalDate.of(1999, 12, 31);
            一旦有 了一个 LocalDate 对象， 
            可以用方法 getYear、 getMonthValue 和 getDayOfMonth 得到年、月和日：
            int year = newYearsEve.getYear(); // 1999
            int month = newYearsEve.getMonthValue(); // 12
            int day = newYearsEve.getDayOfMonth(); // 31
        更改器方法与访问器方法
            访问器方法：
                不改变原对象的值，而只是返回一个新对象，如：
                LocalDate aThousandDaysLater = newYearsEve.plusDays(1000);
                plusDays 方法会生成一个新的 LocalDate 对象， 
                然后把这个新对象赋给 aThousandDaysLater变量。原来的对象不做任何改动
            更改器方法：
                调用后会修改对象本身的值，如
                regorianCalendar someDay = new CregorianCalendar(1999, 11, 31);
                someDay.add(Calendar.DAY_0F_M0NTH, 1000);
                GregorianCalendar.add 方法是一个更改器方法 ( mutator method ) 
                调用这个方法后，someDay 对象的状态会改变。
            与c++对比：
                在 C++ 中， 带有 const 后缀的方法是访问器方法；默认为更改器方法。
                但是，在 Java 语言中， 访问器方法与更改器方法在语法上没有明显的区别
        .LocaData类的方法
            · static Local Time now( )
              构造一个表示当前日期的对象。
            · static LocalTime of ( int year , int month , int day )
              构造一个表示给定日期的对象。
            · int getYear( )
            · int getMonthValue( )
            · int getDayOfMonth( )
              得到当前日期的年、 月和曰。
            · DayOfWeek getDayOfWeek
              得到当前日期是星期几， 作为 DayOfWeek 类的一个实例返回。 调用 getValue 来得到
              1 ~ 7 之间的一个数， 表示这是星期几， 1 表示星期一， 7 表示星期日。
            · Local Date piusDays( int n )
            · Local Date minusDays(int n)
              生成当前日期之后或之前 n 天的日期。
        用户自定义类
            -要想创建一个完整的程序， 应该将若干类组合在一起， 其中只有一个类有 main 方法
            多个源文件的使用
                许多程序员习惯于将每一个类存在一个单独的源文件中。
                例如，将 Employee 类存放在文件 Employee.java 中， 
                将 EmployeeTest 类存放在文件 EmployeeTest.java 中
                如果喜欢这样组织文件， 将可以有两种编译源程序的方法。
                一种是使用通配符调用 Java 编译器： javac Employee*.java
                或者键人下列命令：javac EmployeeTest.java
                对于第二种方法，当 Java 编译器发现 EmployeeTestjava 使用了Employee 类时，
                会查找名为 Employee.class 的文件。如果没有找到这个文件， 
                就会自动地搜索 Employee.java, 然后，对它进行编译。
                更重要的是： 如果 Employee.java 版本较已有的 Employee.dass 文件版本新， 
                Java 编译器就会自动地重新编译这个文件。
                注：可以认为 Java 编译器内置了“ make” 功能。
            自定义类的语法点
                java中，将构造函数称为"构造器"，将类成员变量称为"实例域"
                构造器：
                    成员方法前面带public的，表明任何类的任何方法都可以调用这些方法
                    构造器与类同名。在构造类的对象时， 构造器会运行，以便将实例域初始化为所希望的状态。
                    构造器与其他的方法有一个重要的不同。构造器总是伴随着 new 操作符的执行被调用，
                    而不能对一个已经存在的对象调用其构造器（构造函数）来达到重新设置实例域（类成员）的目的。
                    注意点：所有的Java对象都是在"堆"中构造的，构造器总是伴随着new操作符一起使用
                    提示：每一个类可以有一个 main 方法。这是一个常用于对类进行单元测试的技巧
                    有些类有多个构造器，这种特性叫做重载（名字相同，参数不同）
                    当且仅当没有提供构造器时，系统会自动提供一个无参构造器
                调用构造器后的处理：
                    1 ) 所有数据域被初始化为默认值（0、false 或 null。)
                    2 ) 按照在类声明中出现的次序， 依次执行所有域初始化语句和初始化块。
                    3 ) 如果构造器第一行调用了第二个构造器， 则执行第二个构造器主体
                    4 ) 执行这个构造器的主体
                实例域：
                    实例域前面加private，可以保证类自身的方法能够访问这些实例域， 而其他类的方法不能够读写这些域
                    如果在构造器中没有显式地给域赋予初值，那么就会被自动地赋为默认值： 
                    数值为 0、布尔值为 false、 对象引用为 null，不建议这样做，这会降低程序的可读性
                    注意：域变量才有这种自动初始化为默认值的特性，局部变量没有这种特性
                    显式域初始化：
                        可以在类定义中， 直接将一个值赋给任何域，在执行构造器之前，先执行赋值操作
                        当一个类的所有构造器都希望把相同的值赋予某个特定的实例域时，这种方式特别有用。
                        初始值不一定是常量值。在下面的例子中， 可以调用方法对域进行初始化
                访问器：
                    如果类方法中想返回对象的成员，应该避免直接返回实例域本身，而应返回他们的克隆，
                    如： return  m_data.clone();  这样就可以避免在类的外部不小心修改该类的成员（这与C++在语法上有与区别）
                隐式参数；
                    成员方法的隐式参数： 在每一个方法中， 关键字 this 表示隐式参数，指代对象本身
                    用this调用另一个构造器：
                        如果构造器的第一个语句形如 this(...)，（必须是第一个语句） 这个构造器将调用同一个类的另一个构造器
                        采用这种方式使用 this 关键字非常有用， 这样对公共的构造器代码部分只编写一次即可。
                初始化块：
                    前面已经讲过两种初始化数据域的方法：
                    · 在构造器中设置值
                    · 在声明中赋值
                    实际上，Java 还有第三种机制， 称为初始化块
                    在一个类的声明中，可以包含多个代码块。只要构造类的对象，这些块就会被执行
                    初始化块就是类中用大括号包起来的一块代码
                    初始化块的例子：file://imgs/类的初始化块.jpg
                    注：这种机制不是必需的，也不常见。通常会直接将初始化代码放在构造器中
                    注：即使在类的后面定义， 仍然可以在初始化块中设置域。
                        但是， 为了避免循环定义， 不要读取在后面初始化的域。 
                静态初始化块
                    和初始化块类似，但是大括号前面有static标记，用以初始化静态域，如：
                    static
                    {
                        Random generator = new Random()；
                        nextld = generator.nextlnt(lOOOO) ;
                    }
                在 Java 中， 所有的方法都必须在类的内部定义， 但并不表示它们就是内联方法。
                final 实例域：
                    可以将实例域定义为 final。 构建对象时必须初始化这样的域。
                    在后面的操作中， 不能够再对它进行修改。
                    final 修饰符大都应用于基本 （primitive) 类型域，或不可变（immutable) 类的域
                    String类就是一个不可变的类，对于可变的类， 使用 final 修饰符可能会对读者造成混乱。
                    如： private final StringBuiIcier evaluations;
                    final 关键字只是表示存储在 evaluations 变量中的对象引用不会再指示其他 StringBuilder对象。 
                    不过这个对象可以更改：
                静态域与静态方法：
                    静态域是所有类对象共享的，其属于类，而不是对象
                    静态变量使用得比较少，但静态常量却使用得比较多，
                    如 public static final double PI = 3.14159265358979323846;
                    在程序中，可以采用 Math.PI 的形式获得这个常量。
                    另一个多次使用的静态常量是 System.out。
                    前面曾经提到过，最好不要将域设计为 public。然而， 公有常量（即 final 域）却没问题。 
                    静态方法是一种不能向对象实施操作的方法（java也支持通过对象调用静态方法，但不推荐）。 
                    类的静态方法不能非静态的实例域， 因为它不能操作对象。 但是，静态方法可以访问自身类中的静态域
                    工厂方法：静态方法的一种常见用途
                方法的参数
                    Java 参数的传递，是引用的传递，即参数变量是指向内存对象的另一个引用
                    你无法通过函数，改变原有变量的指向，但如果其指向的内存对象如果是可修改的，
                    则函数内可以修改该内存对象的成员值（借助其成员方法）
                析构与finalize方法
                    由于 Java 有自动的垃圾回收器，不需要人工回收内存， 所以 Java 不支持析构器
                    可以为任何一个类添加 finalize 方法。
                    finalize 方法将在垃圾回收器清除对象之前调用
                    在实际应用中，不要依赖于使用 finalize 方法回收任何短缺的资源， 
                    这是因为很难知道这个方法什么时候才能够调用。
                    注：有个名为 System.mnFinalizersOnExit(true) 的方法
                        能够确保 finalizer 方法在 Java 关闭前被调用。
                        不过， 这个方法并不安全，也不鼓励大家使用。
                        有一种代替的方法是使用方法 Runtime.addShutdownHook 添加“ 关闭钓子”
                        如果某个资源需要在使用完毕后立刻被关闭， 那么就需要由人工来管理。
                        对象用完时，可以应用一个 close 方法来完成相应的清理操作
        包
            相较c++的命名空间，Java有更有效的实现方式：包
            包的概念
                Java 允许使用包（ package > 将类组织起来
                标准的 Java 类库分布在多个包中， 包括 java.lang、java.util 和java.net 等
                标准的 Java 包具有一个层次结构。如同硬盘的目录嵌套一样，也可以使用嵌套层次组织包
                所有标准的 Java 包都处于java 和javax 包层次中。
                使用包的主要原因是确保类名的唯一性，对于同名的类，只要将之放在不同的包中，就不会产生冲突
                从编译器的角度来看， 嵌套的包之间没有任何关系。 
                例如，java.utU 包与java.util.jar 包毫无关系。每一个都拥有独立的类集合。
            类的导入
                一个类可以使用所属包中的所有类， 以及其他包中的公有类（public class)
                我们可以采用两种方式访问另一个包中的公有类：
                1. 每个类名之前添加完整的包名
                   如： java.tiie.LocalDate today = java.tine.Local Date.now() ;
                2. 使用 import 语句
                   可以使用 import 语句导人一个特定的类或者整个包。
                   import 语句应该位于源文件的顶部(但位于 package 语句的后面)
                   import java.util.*;  
                   然后， 就可以使用 LocalDate today = Local Date.now()；
                   如果能够明确地指出所导人的类， 将会使代码的读者更加准确地知道加载了哪些类
                   在 Eclipse 中， 可以使用菜单选项 Source—?Organize Imports
                   这样，如 import java.util.*; 将会自动地扩展为指定的导入列表
                   注意，只能使用星号（*) 导入一个包， 
                   而不能使用 import java.* 或 import java.*.* 导入以 java 为前缀的所有包。
                   导入的包中类名有冲突怎么办？
                       例如，java.util 和java.sql 包都有日期 （ Date) 类
                       import java.util.*;
                       import java.sql.*;
                       这样使用Date类时，编译器无法确定想使用的是那个包中的，
                       此时，可以采用增加一个特定的 import 语句来告诉编译器：
                       import java.util .Date; 
                       如果这两个 Date 类都需要使用， 又该怎么办呢？
                           答案是，在每个类名的前面加上完整的包名
                           java.util .Date deadline = new java.util .Date();
                           java.sql .Date today = new java.sql .Date(...);
                   在包中定位类是编译器 （ compiler) 的工作。类文件中的字节码肯定使用完整的包名来引用其他类
               import vs ＃include 
                   两者之间并没有共同之处
                   在 C++ 中， 必须使用 include 将外部特性的声明加载进来， 
                   这是因为 C++ 编译器无法查看任何文件的内部（ 除了正在编译的文件以及在头文件中明确包含的文件）
                   Java编译器可以查看其他文件的内部， 只要告诉它到哪里去查看就可以了
                   在 Java 中， 通过显式地给出包名， 如java.util.Date， 就可以不使用 import 
                   Import 语句的唯一的好处是简捷，C++中与import类似的机制是命名空间
               静态导入
                   import 语句不仅可以导人类，还增加了导人静态方法和静态域的功能
                   import static java.lang.System.*
                   就可以使用 System 类的静态方法和静态域，而不必加类名前缀
                   另外，还可以导入特定的静态方法或静态域：
                   import static java.lang.System.out;
            将类放入包中
                1.  在源文件的开头加package语句，
                    如： Employee类文件前面加 package com.horstiann.corejava;
                    如果没有在源文件中放置 package 语句， 
                    这个源文件中的类就被放置在一个默认包( defaulf package ) 中。
                    默认包是一个没有名字的包。
                2.  将包中的文件放到与完整的包名匹配的子目录中。
                    例如，com.horstmann.corejava 包中的所有源文件
                    应该被放置在子目录 com/horstmann/corejava
                    编译器也会将类文件也放在相同的目录结构中
                    注意：如果包与目录不匹配， 虚拟机就找不到类
            包的作用域
                标记为 public 的部分可以被任意的类使用；
                标记为 private 的部分只能被定义它们的类使用。
                如果没有指定 public 或 private, 
                这个部分（类、方法或变量）可以被同一个包中的所有方法访问
                基于此，一个类中的数据成员通常应该加private标记，以防被同一个包中的其它类直接访问
        .类路径
            类存储在文件系统的子目录中。类的路径必须与包名匹配
            另外， 类文件也可以存储在 JAR(Java归档 ）文件中
            在一个 JAR 文件中， 可以包含多个压缩形式的类文件和子目录
            JDK 也提供了许多的 JAR 文件， 例如，在 jre/lib/rt.jar 中包含数千个类库文件。
            JAR 文件使用 ZIP 格式组织文件和子目录。
            可以使用所有 ZIP 实用程序查看内部的 rt.jar 以及其他的 JAR 文件
            javac编译器总是在当前的目录中查找文件
            但 java 虚拟机仅在类路径中有“.”目录的时候，才查看当前目录
            如果没有设置过任何类路径， 那也并不会产生什么问题， 默认的类路径包含目录 . 
            然而如果设置了类路径，却忘记了包含“.”目录，则程序仍然可以通过编译， 但不能运行
            类路径所列出的目录和归档文件是搜寻类的起始点，
            例：/home/user/classdir:.:/home/user/archives/archive.jar
            运行时库文件（rt.jar，和在jre/lib 与 jre/lib/ext 目录下的一些其他的 JAR 文件）
            会被自动地搜索，所以不必将它们显式地列在类路径中
            虚拟机搜索类的顺序为：
                1. 首先要查看存储在jre/lib 和jre/lib/ext 目录下的归档文件中所存放的系统类文件
                2. 根据设置的类路径顺序，依次查找文件
            编译器搜索类的顺序：
                略
            java虚拟机设置类路径
                1. 使用 -classpath / -cp 选项设置
                2. 通过设置 CLASSPATH 环境变量设置
        .文档注释
            JDK 包含一个很有用的工具，叫做javadoc，它可以由源文件生成一个 HTML 文档
            如果在源代码中添加以专用的定界符 /** 开始的注释， 
            那么可以很容易地生成一个看上去具有专业水准的文档。
            javadoc 实用程序（utility) 从下面几个特性中抽取信息：
                ·包
                ·公有类与接口
                ·公有的和受保护的构造器及方法
                ·公有的和受保护的域
            每个 /** . . . */ 文档注释，在"标记"之后紧跟着自由格式文本
            "标记"由@开始， 如@author 或@param。
            自由格式文本的第一句应该是一个概要性的句子,javadoc 自动地将这些句子抽取出来形成概要页。
            在自由格式文本中，可以使用 HTML 修饰符， 
                例如，用于强调的 <em>...</eitf>、 
                用于着重强调的 <strong>...</stroiig> 
                以及包含图像的 <img ...> 等
            不过， 一定不要使用 <hl> 或 <hr>, 因为它们会与文档的格式产生冲突。
            若要键入等宽代码， 需使用 {@code ... } 而不是 <code>...</code>
            如果文档中有到其他文件的链接， 例如， 图像文件, 应该将这些文件放到子目录 doc-files 中
            javadoc 实用程序将从源目录拷贝这些目录及其中的文件到文档目录中,
            而在链接中需要使用 doc-files 目录， 例如：<img src="doc-files/uml_png" alt="UML diagram">
            类注释必须放在 import 语句之后，类定义之前
            方法注释
                每一个方法注释必须放在所描述的方法之前。除了通用标记之外， 还可以使用下面的标记：
                · @param 变量描述
                    这个标记将对当前方法的“ param” （参数）部分添加一个条目
                    这个描述可以占据多行， 并可以使用 HTML 标记。
                    一个方法的所有@param 标记必须放在一起
                · @return 描述
                    这个标记将对当前方法添加“ return” （返回）部分。
                    这个描述可以跨越多行， 并可以使用 HTML 标记。
                · @throws 类描述
                    这个标记将添加一个注释， 用于表示这个方法有可能抛出异常
            域注释：只需要对公有域（通常指的是静态常量）建立文档
            通用注释
                下面的标记可以用在类文档的注释中。
                    · @author 姓名
                        这个标记将产生一个 "author"条目。
                        可以使用多个@aUthor 标记，每个@author 标记对应一个作者
                    · @version
                        这个标记将产生一个“ version”（版本）条目。
                        这里的文本可以是对当前版本的任何描述。
                下面的标记可以用于所有的文档注释中。
                    · @since 文本
                        这个标记将产生一个“ since” （始于）条目。
                        这里的 text 可以是对引人特性的版本描述。
                        例如，?since version 1.7.10
                    · @deprecated
                        这个标记将对类、 方法或变量添加一个不再使用的注释。 
                        文本中给出了取代的建议。 例如，
                        @deprecated Use <code> setVIsible(true)</code> instead
                        通过@see 和@link标记， 可以使用超级链接， 
                        链接到 javadoc 文档的相关部分或外部文档。
                    · @see 引用
                        这个标记将在“ see also” 部分增加一个超级链接。
                        它可以用于类中，也可以用于方法中。
                        这里的引用可以选择下列情形之一：
                        1. 只要提供类、 方法或变量的名字，
                           javadoc 就在文档中插入一个超链接。例如，
                           @see com.horstraann.corejava.Employee＃raiseSalary(double)
                           建立一个链接到 com.horstmann.corejava.Employee 类的 
                           raiseSalary(double) 方法的超链接。 
                           可以省略包名， 甚至把包名和类名都省去，
                           此时，链接将定位于当前包或当前类
                           需要注意，一定要使用井号（＃，) 
                           而不要使用句号（.）分隔类名与方法名，或类名与变量名。
                           Java 编译器本身可以熟练地断定句点在分隔包、 子包、 类、
                           内部类与方法和变量时的不同含义。
                           但是 javadoc 实用程序就没有这么聪明了， 
                           因此必须对它提供帮助。
                        2. 如果@see 标记后面有一个 < 字符，就需要指定一个超链接。
                           可以超链接到任何URL。例如：
                           @see <a href="www.horstmann.com/corejava.html">
                                The Core ]ava home page</a>
                        在上述各种情况下， 都可以指定一个可选的标签（label ) 作为链接锚
                        如果省略了 label , 用户看到的锚的名称就是目标代码名或 URL。
                        如果@see 标记后面有一个双引号字符， 文本就会显示在 “ see also” 部分。
                        例如，@see "Core Java 2 volume 2n
                        可以为一个特性添加多个@see 标记，但必须将它们放在一起。
                    . 如果愿意的话， 还可以在注释中的任何位置放置指向其他类或方法的超级链接，  
                        以及插人一个专用的标记， 例如，
                        {@link package,classifeature label ]
                        这里的特性描述规则与@see 标记规则一样。
            包的注释
                要想产生包注释，需要在每一个包目录中添加一个单独的文件
                可以有如下两个选择：
                1 ) 提供一个以 package.html 命名的 HTML 文件。
                    在标记 <body>—</body> 之间的所有文本都会被抽取出来。
                2 ) 提供一个以 package-info.java 命名的 Java 文件。
                    这个文件必须包含一个初始的以 /**和 */ 界定的 Javadoc 注释， 跟随在一个包语句之后。
                    它不应该包含更多的代码或注释。
            注释的抽取
                这里，假设生成的帮助文件（HTML）将被存放在目录 docDirectory 下。执行以下步骤：
                1 ) 切换到包含想要生成文档的源文件目录。
                    如果有嵌套的包要生成文档， 例如 com.horstmann.corejava, 
                    就必须切换到包含子目录 com 的目录
                2 ) 如果是一个包，应该运行命令:
                    javadoc -d docDirectory nameOfPackage
                    或对于多个包生成文档， 运行:
                    javadoc -d docDirectory nameOfPackage1 nameOfPackage2 . . .
                    如果文件在默认包中， 就应该运行：
                    javadoc -d docDirectory *. java
                    如果省略了 -d docDirectory 选项， 那 HTML 文件就会被提取到当前目录下
                    这样有可能会带来混乱，因此不提倡这种做法
                一个很有用的选项是 -link, 用来为标准类添加超链接，例如， 如果使用命令
                javadoc -link http://docs.oracle.eom/:javase/8/docs/api *.java
                那么，所有的标准类库类都会自动地链接到 Oracle 网站的文档。
                如果使用-linksource 选项， 则每个源文件被转换为 HTML，
                并且每个类和方法名将转变为指向源代码的超链接。
                有关其他的选项， 请查阅 javadoc 实用程序的联机文档，
                http://docs.orade.eom/javase/8/docs/guides/javadoc
    第5章 继承                
        子类
            public class Manager extends Employee   &<继承类>
            {  添加方法和域  }
            与C++相比， Java 用关键字 extends 代替了 C++ 中的冒号
            在 Java 中， 所有的继承都是公有继承， 而没有 C++ 中的私有继承和保护继承
            已存在的类称为超类( superclass )、 基类（ base class ) 或父类（ parent class)
            新类称为子类（subclass、) 派生类( derived class ) 或孩子类（ child class )。
            覆盖方法
                我们希望调用基类中的相同签名的方法， 而不是当前类的这个方法，
                可以使用特定的关键字 super 解决这个问题： super.父类方法
                c++中：如果派生类中有一个具有相同签名的函数，
                则可以通过添加基类的名称后跟两个冒号base_class::foo(...)来消除它的歧义。
                有些人认为 super 与 this 引用是类似的概念， 实际上，这样比较并不太恰当
                因为 super 不是一个对象的引用， 不能将 super 赋给另一个对象变量， 
                它只是一个指示编译器调用基类方法的特殊关键字
                注意：在覆盖一个方法的时候，子类方法不能低于基类方法的可见性。
                特别是， 如果基类方法是 public, 子类方法一定要声明为 public，
                否则，不过不加public，相当于将其设置为了更严格的包访问范围，就会出错
                父类已经宣布公有的方法，子类不能对其宣布私有。
                因为有时候我们会用父类对象指向子类实例，
                原则上，我们应该可以调用父类的所有公有方法，
                如果子类能把父类方法变为私有，则就会破坏这种原则，给编程带来极大不便
            子类构造器
                public Manager(String name, double salary, int year, int month, int day)
                {
                    super(name, salary, year, month, day) ;
                    bonus = 0;
                }
                这里的关键字 super 具有不同的含义。
                语句super(n, s, year, month, day);
                是“ 调用基类 Employee 中含有 n、s、year month 和 day 参数的构造器” 的简写形式
                由于 Manager 类的构造器不能访问 Employee 类的私有域， 
                所以必须利用 Employee 类的构造器对这部分私有域进行初始化
                调用构造器的语句必须是子类构造器的第一条语句。
                如果子类的构造器没有显式地调用基类的构造器， 
                则将自动地调用基类默认（没有参数）的构造器。
                如果基类没有不带参数的构造器， 
                并且在子类的构造器中又没有显式地调用基类的其他构造器，
                则 Java 编译器将报告错误
                在 C++ 的构造函数中， 使用初始化列表语法调用基类的构造函数，而不调用super
            this 与 super
                关键字 this 有两个用途：一是引用隐式参数，二是调用该类其他的构造器 ， 
                同样，super 关键字也有两个用途：一是调用基类的方法，二是调用基类的构造器。
            多态 &<多态>
                一个对象变量（例如， 变量 e ) 可以指示多种实际类型的现象被称为多态
                在运行时能够自动地选择调用哪个方法的现象称为动态绑定
                在 Java 程序设计语言中， 对象变量是多态的，一个变量可以引用该类，及其任意子类的对象
                不同于C++，在 Java 中， 不需要将方法声明为虚拟方法。动态绑定是默认的处理方式
                如果不希望让一个方法具有虚拟特征， 可以将它标记为 final 
                注：在c++中，如果基类方法func被子类覆盖，但该基类方法不是虚函数，
                    则基类指针指向子类对象时，调用func函数，实际调用的是基类的方法
                在 Java 中， 子类数组的引用可以转换成基类数组的引用， 而不需要采用强制类型转换
                例如， 下面是一个经理数组：Manager[] managers = new Manager[10];
                将它转换成 Employee[] 数组完全是合法的： Employee[] staff = managers; // OK
            继承层次与继承链
                基类派生出来的所有类的集合被称为继承层次
                从某个特定的类到其祖先的路径被称为该类的继承链 
                Java 不支持多继承（但也已继承/实现多个接口）
            理解方法调用
                调用过程的详细描述：
                1） 编译器査看对象的声明类型和方法名
                2） 接下来，编译器将査看调用方法时提供的参数类型
                3） 如果是 private 方法、 static 方法、 final 方法或者构造器
                    那么编译器将可以准确地知道应该调用哪个方法， 
                    我们将这种调用方式称为静态绑定（ static binding )
                4） 当程序运行，并且采用动态绑定调用方法时
                    虚拟机一定调用与 x 所引用对象的实际类型最合适的那个类的方法。
                    每次调用方法都要进行搜索，时间开销相当大。
                    因此， 虚拟机预先为每个类创建了一个方法表（ method table), 
                    其中列出了所有方法的签名和实际调用的方法。
                    这样一来，在真正调用方法的时候， 虚拟机仅查找这个表就行了
            阻止继承
                有时候，可能希望阻止人们利用某个类定义子类
                不允许扩展的类被称为 final 类如果在定义类的时候
                使用了 final 修饰符就表明这个类是 final 类
                public final class Executive extends Manager
                { 。。。 }
                类中的特定方法也可以被声明为 final
                如果这样做，子类就不能覆盖这个方法
                注意这里说的是覆盖，final方法当然会被子类所拥有
                可以认为，c++默认的方法都是带final的，加了virtual就好比去掉了final
                域也可以被声明为 final。
                对于 final 域来说，构造对象之后就不允许改变它们的值了
                不过， 如果将一个类声明为 final， 
                只有其中的方法自动地成为 final，但不包括域
                将方法或类声明为 final 主要目的是： 确保它们不会在子类中改变语义。
                String 类也是 final 类，这意味着不允许任何人定义 String 的子类
                换言之， 如果有一个 String 的引用， 
                它引用的一定是一个 String 对象， 而不可能是其他类的对象
            强制类型转换
                对象引用的转换语法与数值表达式的类型转换类似， 
                仅需要用一对圆括号将目标类名括起来，并放置在需要转换的对象引用之前就可以了
                如： Manager boss = (Manager) staff[0]:
                但这有个前提，就是 staff[0] 虽然是个基类的变量类型，但其实际引用的是子类对象
                将一个值存入变量时， 编译器将检查是否允许该操作。
                将一个子类的引用赋给一个基类变量， 编译器是允许的。
                但将一个基类的引用赋给一个子类变量， 必须进行类型转换，这样才能够通过"运行时"的检査
                如果将一个指向基类对象的变量强转为其子类，java"运行时"系统将报告这个错误，
                并产生一个 ClassCastException 异常。 如果没有捕获这个异常，那么程序就会终止
                因此在进行类型转换之前， 应先查看一下是否能够成功地转换，如：
                if (staff[1] instanceof Manager) 
                {
                    boss = (Manager) staff[1]:
                }
                注意，如果 x 为 null , 则 x instanceof C 将不会产生异常， 只是返回 false。
                Java的类型转换有点像C++的dynamic_cast<>，
                但当类型转换失败时， Java 不会生成一个 null 对象，而是抛出一个异常
            抽象类  &<抽象类>   相关：@接口
                在一个类中，可以使用 abstract 关键字定义抽象函数(即C++中的纯虚函数)：
                public abstract String getDescription();  //抽象函数可以只声明，不实现
                包含抽象函数的类本身也必须声明为抽象类
                public abstract class Person
                {
                    public abstract String getDescription()；
                    ...
                }
                除了抽象方法之外，抽象类还可以包含具体数据和具体方法
                抽象类不能被实例化。
                可以定义一个抽象类的对象变量， 但是它只能引用非抽象子类的对象
            受保护访问
                最好将类中的域标记为 private, 而方法标记为 public
                在有些时候，人们希望超类中的某些方法允许被子类访问， 
                或允许子类的方法访问超类的某个域。
                为此， 需要将这些方法或域声明为 protected。
                在实际应用中，要谨慎为域变量使用 protected 属性
                受保护的方法更具有实际意义
                实际上，Java 中的受保护部分对所有子类及同一个包中的所有其他类都可见
            控制可见性的 4 个访问修饰符
                1 ) 仅对本类可见 private。
                2 ) 对所有类可见 public：
                3 ) 对本包和所有子类可见 protected。
                4 ) 对本包可见—默认，不需要修饰符。
        Object：所有类的超类
            -Object 类是 Java 中所有类的始祖， 在 Java 中每个类都是由它扩展而来的
            -如果没有明确地指出超类，Object 就被认为是这个类的超类。
            -因此可以使用 Object 类型的变量引用任何类型的对象，
            -在 C++ 中没有所有类的根类， 不过，每个指针都可以转换成 void* 指针
            -在 Java 中， 只有基本类型 （ primitive types) 不是对象， 
            -例如，数值、 字符和布尔类型的值都不是对象。
            -所有的数组类型，不管是对象数组还是基本类型的数组都扩展了 Object 类。
            equals方法
                Object 类中的 equals 方法用于检测一个对象是否等于另外一个对象
                这个方法将判断两个对象是否具有相同的引用
                我们可以在子类中重载equals方法，实现自己的判断相等的方式，
                如可以定义只要两个对象的数据成员相等，则即使不是一个对象，也也可判定为相等
                由于子类无法访问父类的私有数据成员，所以通常应该在
                子类的equals方法中，首先调用超类的equals方法进行判断
                Java 语言规范要求 equals 方法具有下面的特性：
                    1 ) 自反性： 对于任何非空引用 x, x.equals(x) 应该返回 true
                    2 ) 对称性:  对于任何引用 x 和 y,  y.equals(x) 返回 true, x.equals(y) 也应该返回 true。
                    3 ) 传递性： 对于任何引用 x、 y 和 z, 如果 x.equals(y) 返回 true， 
                                 y.equals(z) 返回 true, x.equals(z) 也应该返回 true。
                    4 ) 一致性： 如果 x 和 y 引用的对象没有发生变化，
                                 反复调用 x.equals(y) 应该返回同样的结果。
                    5 ) 对于任意非空引用 x, x.equals(null) 应该返回 false
                下面给出编写一个完美的 equals 方法的建议：
                    1 ) 显式参数命名为 otherObject, 稍后需要将它转换成另一个叫做 other 的变量。
                    2 ) 检测 this 与 otherObject 是否引用同一个对象
                        if (this = otherObject) return true;
                    3 ) 检测 otherObject 是否为 null, 如 果 为 null, 返 回 false
                    4 ) 比较 this 与 otherObject 是否属于同一个类 
                        如果 equals 的语义在每个子类中有所改变，就使用 getClass 检测：
                        if (getClass() != otherObject.getCIassO) return false;
                        如果所有的子类都拥有统一的语义，就使用 instanceof 检测：
                        if (!(otherObject instanceof ClassName)) return false;
                    5 ) 将 otherObject 转换为相应的类类型变量：
                        ClassName other = (ClassName) otherObject
                    6 ) 现在开始对所有需要比较的域进行比较了
                        对于数组类型的域， 可以使用静态的 Arrays.equals方法检测相应的数组元素是否相等。
                        java.util.Arrays 1.2
                        static Boolean equals(type[] a , type[] b) 5.0
                        如果两个数组长度相同， 并且在对应的位置上数据元素也均相同， 将返回 true
                如果在子类中重新定义 equals, 就要在其中包含调用 super.equals(other。)
                注意，子类覆盖object基类的equals时，注意函数签名应一致，
                如 public boolean equals(Employee other) ，其实就没有覆盖到object类的equals方法
                为了避免发生类型错误， 可以使用 @Override 对覆盖超类的方法进行标记
                ?Override public boolean equals(Object other)
            hashCode 方法
                由于 hashCode 方法定义在 Object 类中， 
                因此每个对象都有一个默认的散列码，其值为对象的存储地址
                String对Object的hashCode方法进行了重写
                    int hash = 0;
                    for (int i = 0; i < length0；i++)
                        hash = 31 * hash + charAt(i );
                StringBuffer 类中没有定义hashCode 方法，
                它的散列码是由 Object 类的默认 hashCode 方法导出的对象存储地址
                自定义类重写 hashCode 方法时，可以使用 ObjeCtS.hash 并提供多个参数。
                这个方法会对各个参数调用 Objects.hashCode， 并组合这些散列值
                public int hashCodeO
                {
                    return Objects,hash(name, salary, hireDay);
                }
                Equals 与 hashCode 的定义必须一致：
                    如果 x.equals(y) 返回 true, 
                    那么 x.hashCode( ) 就必须与 y.hashCode( ) 具有相同的值。 
                如果存在数组类型的域， 那么可以使用静态的 Arrays.hashCode 方法计算一个散列码， 
                这个散列码由数组元素的散列码组成。
                java.util.Objects 7
                ?static int hash(Object... objects )
                    返回一个散列码，由提供的所有对象的散列码组合而得到。
                ?static int hashCode(Object a )
                    如果 a 为 null 返回 0， 否则返回 a.hashCode()
                java.utii.Arrays 1.2
                ?static int hashCode( type[] a ) 5.0
                    计算数组 a 的散列码。组成这个数组的元素类型可以是 
                    object ，int ，long, short, char,byte, boolean, float 或 double。
            toString 方法
                在 Object 中还有一个重要的方法， 就是 toString 方法
                它用于返回表示对象值的字符串。
                绝大多数（但不是全部）的 toString方法都遵循这样的格式：
                类的名字, 随后是一对方括号括起来的域值, 如：
                public String toString()
                {
                    return getClassO.getName() + 
                           "[name=" + name +
                           ",hireDay salary:=" + salary +
                           "]";
                }
                如果父类中使用上述方法定义了toString，则子类中可以：
                public String toStringO
                {
                    return super.toString() + "[bonus=" + bonus + "]";
                }
                只要对象与一个字符串通过操作符“ +” 连接起来，
                Java 编译就会自动地调用 toString方法，以便获得这个对象的字符串描述
                所以，在调用 x.toString( ) 的地方可以用 ""+x 替代
                与 toString 不同的是， 如果 x 是基本类型， 这条语句照样能够执行。
                同样，System.out.println(x)，println方法会直接地调用 x.toString()
                Object 类定义了 toString 方法， 用来打印输出对象所属的类名和散列码
                数组继承了 object 类的 toString 方法（即没有自己实现toString方法）
                但可以调用静态方法 Arrays.toString() 将数组内容转为字符串
                强烈建议为自定义的每一个类增加 toString 方法
        .泛型数组列表
            在许多程序设计语言中， 特别是在 C++ 语言中， 必须在编译时就确定整个数组的大小
            在 Java 中，情况就好多了。它允许在运行时确定数组的大小
            int actualSize = ... ;
            Employee[] staff = new Employee[actualSize];
            当然， 这段代码并没有完全解决运行时动态更改数组的问题。
            一旦确定了数组的大小， 改变它就不太容易了。
            在 Java 中， 解决这个问题最简单的方法是使用 Java 中另外一个被称为ArrayList 的类。
            它是一个动态数组，ArrayList 是一个采用类型参数（ type parameter ) 的泛型类
            为了指定数组列表保存的元素对象类型，需要用一对尖括号将类名括起来加在后面， 
            例如， ArrayList<Employee> staff = new ArrayList<Eniployee>();
            两边都使用类型参数 Employee， 这有些繁琐。 Java SE 7中， 可以省去右边的类型参数：
            ArrayList<Employee> staff = new ArrayList()；
            注：Java SE 5.0 以前的版本没有提供泛型类， ArrayList 类中保存类型为 Object 的元素
            使用 add 方法可以将元素添加到数组列表中：
            staff.add(new Employee("Harry Hacker", ...);
            如果已经清楚或能够估计出数组可能存储的元素数量， 
            可以在填充数组之前调用ensureCapacity方法, 如staff.ensureCapacity(lOO);
            另外，还可以把"初始容量"传递给 ArrayList 构造器：
            ArrayList<Employee> staff = new ArrayList(lOO) ;
            size()方法将返回数组列表中包含的实际元素数目
            一旦能够确认数组列表的大小不再发生变化， 就可以调用 trimToSize 方法
            这个方法将存储区域的大小调整为当前元素数量所需要的存储空间数目。
            垃圾回收器将回收多余的存储空间。
            ArrayList 有点类似于 C++ 的 vector，但java没有重载 [] 运算符的能力，
            所以要访问某个元素，不能用[]语法格式，需要用set(index,value)/get(index)方法
            注意，index 从 0 开始， set 只能替换数组中已经存在的元素
            如果要为列表添加新元素，应使用 add 方法
            使用 toArray() 方法，可以将列表转为数组，然后就可以使用 [] 访问了
            除了在数组列表的尾部追加元素之外，还可以在数组列表的中间插入元素
            使用带索引参数的 add 方法 ： x.add(n,e)
            为了插人一个新元素，位于 n 之后的所有元素都要向后移动一个位置
            同样地，可以从数组列表中间删除一个元素: s.remove(n) , 该函数返回删除的元素
        .对象包装器与自动装箱
            有时， 需要将 int 这样的基本类型转换为对象
            所有的基本类型都有一个与之对应的类。
            例如，Integer 类对应基本类型 int。通常， 这些类称为包装器 （ wrapper )
            对象包装器类是不可变的，即一旦构造了包装器，就不允许更改包装在其中的值。
            同时， 对象包装器类还是 final , 因此不能定义它们的子类
            对于泛型，其尖括号中的类型参数不允许是基本类型，
            如不允许写成 ArrayList<int>， 这里就用到了 Integer 对象包装器类
            我们可以声明一个 Integer对象的数组列表：
            ArrayList<Integer> list = new ArrayList<>()；
            调用 list.add(3) 时，会自动变为 list.add(Integer.value0f(3));
            这种特性称为自动装箱
            相反地， 当将一个 Integer 对象赋给一个 int 值时， 将会自动地拆箱
            在算术表达式中也能够自动地装箱和拆箱， 如： Integer n = 3; n++;
            == 运算符也可以应用于对象包装器对象， 只不过检测的是对象是否指向同一个存储区域， 
            因此，下面的比较通常不会成立：
            Integer a = 1000;
            Integer b = 1000;
            if (a = b) . . .
            注：自动装箱规范要求 boolean、byte、char 127，
                介于-128 ~ 127之间的 short 和int 被包装到固定的对象中。
                例如， 如果在前面的例子中将 a 和 b 初始化为 100， 
                对它们进行比较(==)的结果一定成立。
            解决这个问题的办法是在两个包装器对象比较时调用 equals 方法
            由于包装器类引用可以为 null, 所以自动装箱有可能会抛出一个 NullPointerException 异常：
            Integer n = null;
            System.out.printing ( 2* n); // Throws NullPointerException
            另外， 如果在一个条件表达式中混合使用 Integer 和 Double 类型， 
            Integer 值就会拆箱，提升为 double, 再装箱为 Double:
            nteger n = 1;
            Double x = 2.0;
            System.out.println(true ? n : x); // Prints 1.0
            最后强调一下，装箱和拆箱是编译器实现的， 而不是虚拟机，
            编译器在生成类的字节码时， 会插入必要的方法调用
            java.lang.Integer 1.0
                · int intValue( )
                    以 int 的形式返回 Integer 对象的值（在 Number 类中覆盖了 intValue方法）。
                · static String toString(int i )
                    以一个新 String 对象的形式返回给定数值 i 的十进制表示。
                · static String toString(int i ,int radix )
                    返回数值 i 的基于给定 radix 参数进制的表示。
                · static int parselnt( String s)
                · static int parseInt( String s,int radix )
                    返回字符串 s 表示的整型数值， 给定字符串表示的是十进制的整数（第一种方法，)
                    或者是 radix 参数进制的整数 （第二种方法。)
                · static Integer valueOf(String s)
                · Static Integer value Of(String s, int radix)
                    返回用 s 表示的整型数值进行初始化后的一个新 Integer 对象， 给定字符串表示的是十
                    进制的整数（第一种方法，) 或者是 radix 参数进制的整数（第二种方法。)
        .参数数量可变的方法
            在 Java SE 5.0 以前的版本中，每个 Java 方法都有固定数量的参数。
            现在的版本提供了可以用可变的参数数量调用的方法（变参）
            如：public PrintStream printf(String fmt , Object... args) { return format(fmt, args); }
            printf 方法接收两个参数， 一个是格式字符串， 另一个是 Object[] 数组
            注：如果调用者提供的是整型数组或者其他基本类型的值， 自动装箱功能会将把它们转换成对象
            换句话说，对于 printf 的实现者来说，Object… 参数类型相当于 Object[]， 但后者不支持变参
            调用举例： System.out.printf("%d %s", new Object[] { new Integer(n), "widgets" } );
            自定义变参函数举例：
            public static double max(double... values)
            {
                double largest = Double.NEGATIVE_INFINITY;
                for (double v : values) if (v > largest) largest = v;
                return largest;
            }
            调用： max(1,2,3,4,5);  编译器会自动修正为 max( new double[]{1,2,3,45} )
            允许将一个数组传递给可变参数方法的最后一个参数
            所以这对java5之前，借助数组实现变参功能的函数实现了兼容
            甚至可以将 main 方法声明为： public static void main(String... args)
        .枚举类
            public enuni Size { SMALL, MEDIUM, LARGE, EXTRAJARGE };
            在比较两个枚举类型的值时， 永远不需要调用 equals, 而直接使用“ ==” 就可以了
            如果需要的话， 可以在枚举类型中添加一些构造器、 方法和域
            当然， 构造器只是在构造枚举常量的时候被调用
            public enum Size
            {
                SMALL("S"), MEDIUM("M") , LARGE("L") , EXTRA_LARGE("XL");
                private String abbreviation;
                private Size(String abbreviation) { this.abbreviation = abbreviation; }
                public String getAbbreviation() { return abbreviation; }
            }
            所有的枚举类型都是 Enum 类的子类。它们继承了这个类的许多方法。
            其中最有用的一个是 toString， 这个方法能够返回枚举常量名
            如：Size.SMALL.toString( ) 将返回字符串“ SMALL”。
            toString 的逆方法是静态方法 valueOf。
            Size s = Enum.valueOf(Size,class, "SMALL");  //将 s 设置成 Size.SMALL
            每个枚举类型都有一个静态的 values 方法，它将返回一个包含全部枚举值的数组
            Size[] values = Size.values();
        反射
            使用情形
                一般当不了解一个类（没有该类的源码或不能确定是哪个类），但又想访问该类的数据成员或方法时，
                会使用到反射，如在聚合关系模型中，一个函数的参数是Object类型，
                函数不能确定该参数具体是什么类型，也允许是各种类型，
                但能确定的一点是，该参数类型中有个特定的变量或函数，
                这时，就可以用反射访问该参数对象的数据或方法成员。
                Java的反射机制在做基础框架的时候非常有用，有一句话这么说来着：
                反射机制是很多Java框架的基石。
                而一般应用层面很少用，也不建议使用，因为反射就相当于一个作弊器，
                它使代码操作类的权利变得非常大，利用反射可以访问类的私有域、私有方法，这会破坏类的封装性，
                同时反射有时会脆弱的，编译器很难帮人们发现程序中的错误，只有在运行时才能发现错误并导致异常
                这项功能被大量地应用于 JavaBeans 中， 它是 Java 组件的体系结构
                (有关 JavaBeans 的详细内容在卷 II 中阐述)
            Class类
                在程序运行期间，Java 运行时系统始终为所有的对象维护一个被称为运行时的类型标识
                这个信息跟踪着每个对象所属的类，保存这些信息的类即为 Class 类
                获取一个类对应的Class类对象的3中方法：
                    1. Object 类中的 getClass( ) 方法将会返回一个 Class 类型的实例
                       最常用的 Class 方法是 getName。 这个方法将返回类的名字。
                       如果类在一个包里，包的名字也作为类名的一部分：
                       Random generator = new Random():
                       Class cl = generator.getClass() ;
                       String name = cl.getName(); // name is set to "java.util.Random"
                    2. 调用静态方法 forName()，获得类名对应的 Class 对象：
                       Class cl = Class.forName("java.util.Random") ;
                       这个方法只有在传入的参数是类名或接口名时才能够执行。 
                       否则，forName 方法将抛出一个 checkedexception ( 已检查异常）。
                       无论何时使用这个方法， 都应该提供一个异常处理器（exception handler) 
                       巧用 forName 方法，完成类的加载：
                            启动时， 包含 main 方法的类被加载。它会加载所有需要的类。 
                            这些被加栽的类又要加载它们需要的类， 以此类推。 
                            对于一个大型的应用程序来说， 这将会消耗很多时间， 用户会因此感到不耐烦
                            可以使用下面这个技巧给用户一种启动速度比较快的幻觉：
                            1. 确保包含 main 方法的类没有显式地引用其他的类。
                            2. 显示一个启动画面；
                            3. 通过调用 Class.forName 手工地加载其他的类。
                    3. 直接访问对象的class成员，如
                       Class dl = Random,class; // if you import java.util
                       Class cl2 = int.class;
                       Class cl3 = Doublet[].class;
                Class 类实际上是一个泛型类。例如， Employee.class 的类型是 Class<Employee>  &<class泛型类>
                但它将已经抽象的概念更加复杂化了。 在大多数实际问题中，可以忽略类型参数，而使用原始的 Class 类
                注意：鉴于历史原因 getName 方法在应用于数组类型的时候会返回一个很奇怪的名字：
                    ?Double[ ] class.getName( ) 返回“ [Ljava.lang.Double;’’
                    ?int[ ].class.getName( ) 返回“ [I ” 
                虚拟机为每个类型管理一个 Class 对象。 因此， 可以利用 == 运算符实现两个类对象比较的操作
                Class类还有一个很有用的方法 newInstance( )， 可以用来动态地创建一个类的实例：
                Object m = Class.forName("java.util.Random").newInstance(); &<class类的newInstance>
                但这种方式有个局限性，就是没法调用带参构造函数完成对象的创建，
                如果要实现这个需求，可使用Constructor 类中的 newInstance 方法，参 @Constructor类的newInstance
            捕获异常
                可以提供一个“ 捕获” 异常的处理器（handler） 对异常情况进行处理
                如果没有提供处理器， 程序就会终止，并在控制台上打印出一条信息， 其中给出了异常的类型
                异常有两种类型： 未检查异常和已检查异常
                    已检查异常是指：程序在执行到某条语句时，需要满足某种条件，否则就会引发异常，
                    所以在该条语句的上下文中做了检查，确保该语句在指定到时，能够满足所需要的条件，
                    否则，就会主动的抛出一个异常，交给函数的调用者去处理，
                    对于这种主动抛出异常的，编译器能够检查出来，并要求抛出异常函数的调用者去处理这种异常。
                    这种函数主动抛出的异常，属于已检查异常。
                    还有一种情况，就是某条语句当不满足条件时，会引发崩溃，
                    但代码的上下文中，没有对这种条件进行预防，没有抛出任何异常，
                    程序如果执行到这样的语句，就会崩溃，这样的异常，属于未检查异常。
                对于已检查异常， 编译器将会检查是否提供了处理器
                然而， 有很多常见的异常， 例如， 访问 null 引用， 都属于未检查异常
                编译器不会査看是否为这些错误提供了处理器。
                Class.forName 方法就是一个抛出已检查异常的例子。
                在第 7 章中， 将会看到几种异常处理的策略现在， 只介绍一下如何实现最简单的处理器：
                将可能抛出已检査异常的一个或多个方法调用代码放在 try 块中，然后在 catch 子句中提供处理器代码
                try
                {
                    String name = . . .; // get class name
                    Class cl = Class.forName(name) ; // might throw exception
                    dosomething with d
                }
                catch (Exception e)
                {
                    e.printStackTraceO ;
                }
            利用反射分析类的能力
                反射机制最重要的内容—检查类的结构
                在 java.lang.reflect 包中有三个类 Field、 Method 和 Constructor 
                分别用于描述类的域、 方法和构造器
                Class类中的 getFields、 getMethods 和 getConstructors 方法将分别返回
                类提供的 public 域(Field)、 方法(Method)和构造器(Constructor)的数组， 
                其中包括超类的公有成员。
                Class 类的 getDeclareFields、getDeclareMethods 和 getDeclaredConstructors 方法
                将分别返回类中声明的全部域(Field)、 方法(Method)和构造器(Constructor)， 
                其中包括私有和受保护成员，但不包括超类的成员。
                这三个类(域、 方法和构造器)都有一个叫做 getName 的方法， 用来返回域/方法/构造函数的名称。
                Field 类有一个 getType 方法， 用来返回描述域所属类型的 Class 对象。
                Method 和 Constructor 类有能够报告参数类型的方法，
                Method 类还有一个可以报告返回类型的方法。
                这三个类还有一个叫做 getModifiers 的方法， 它将返回一个整型数值， 
                用不同的位开关描述 public 和 static 这样的修饰符使用状况。
                另外， 还可以利用java.lang.refleCt 包中的 Modifieir 类的静态方法
                分析getModifiers 返回的整型数值。 
                例如， 可以使用 Modifier 类中的 isPublic、 isPrivate 或 isFinal，
                判断方法或构造器是否是 public、 private 或 final。 
                我们需要做的全部工作就是调用 Modifier 类的相应方法， 并对返回的整型数值进行分析， 
                另外，还可以利用 Modifier.toString方法将修饰符打印出来
                小结：
                    m.getClass，可得到class对象
                    再通过class对象的相应方法，又可得到 Constructor、 Method 和 Field 三个类，
                    这三个类分别描述了 m 对象的构造函数、成员函数、成员变量
                    这三个类都提供了 getName 方法，用以得到函数或变量的名字
                    其它像如函数的参数、函数的返回值，成员变量的类信息(class)，
                    以及类的可见性、成员的可见性等（有Modifier类辅助）都可得到
                本书195页（实212页）给出了一个举例的例子，可以打印出给定名字对应的类的详细信息
                （包括类名，类的可见性，是否继承父类，所有的函数的签名，都有哪些成员变量等）
            在运行时使用反射分析对象
                利用反射，还可查看类对象的成员变量的值
                这主要使用的是Filed类的 Object get(Object obj) 方法，
                get的obj参数应传入该成员变量所属的类对象（的引用）
                这里要注意，如果成员变量是私有的，则get方法将报 IllegalAccessException 异常
                也就是说，反射机制的默认行为受限于 Java 的访问控制
                然而， 如果一个 Java 程序没有受到安全管理器的控制， 就可以覆盖访问控制
                为了达到这个目的， 需要调用 Field、 Method 或 Constructor 对象的 setAccessible(bool) 方法
                setAccessible 方法是 AccessibleObject 类中的一个方法， 
                它是 Field、 Method 和 Constructor 类的公共超类，
                当 setAccessible(true) 后，就不再检查其可访问性，而可以随意读取了
                还有一个问题，注意 get 方法的返回类型是 Object，
                对于像如 int 这样的成员变量，get 会自动将之打包为 Integer
                （其实还有 getLong, getChar,getFloat等方法，可以直接获取到相应内置变量的原始值）
                与 get 对应的方法是 void set(Object obj, Object value) ，可以设置成员变量的值
                延伸：借助get方法，我们可以写出一个通用的 toString 方法
                    本书第199页（实216页）给出了该方法的实现
                    这里面讲到了如何获取成员类型为数组类型的情况
            动态为数组类型的成员变量添加新的元素
                java.lang.reflect 包中的 Array 类允许动态地创建数组。
                假设一个类对象 enterprise 的成员变量 m 是 Emploee[] 数组类型，
                （m.getClass().isArray()可判断是否为数组类型）
                （m.getClass().getComponentType()方法可得到数组成员的类型）
                如果想给该该企业添加新的雇员，同时要考虑到原有数组已满的情况，
                Object m2 = Array.newlnstance(m.getClass().getComponentType(), newLength) ;
                通过这种方法，可以正确的创建出新的长度的 Emploee[] 数组，
                然后可以利用 System.arraycopy 方法，将 m 数组的原有成员值拷贝到新数组中
                System.arraycopy(m, 0, m2, 0, Math.min(Array.getLength(m), newLength)) ;
                本书第203页（实220页）提供了 CopyOf 的实现代码
            调用任意方法
                在 Method 类中有一个 invoke 方法， 它允许调用包装在当前 Method 对象中的方法
                Object invoke(Object obj, Object... args)
                第一个参数是传递给真正成员方法的隐式参数， 其余的对象提供了显式参数
                对于静态方法，第一个参数可以被忽略， 即可以将它设置为 null
                对于内置的int,float等类型的参数或返回值，invoke 会自动的装箱与拆箱，
                但注意因为 invoke 的返回值是Object类型，所以应先将之强转为 Integer 这样的类型，
                然后才能用 int ret 接收该返回值
                要想调用invoke，必须先得到该方法对应的Method对象
                除了前面提到的getDeclareMethods获取Method数组外，还可以直接用getMethod方法得到
                Method getMethod(String name, Class<?>... parameterTypes) 
                之所以需要提供 parameterTypes 参数，
                是因为有函数重载，所以需通过参数明确想要得到哪个方法
                举例：Method m2 = Employee.class.getMethod("raiseSalary", double.class);
                注：对于Class<?>类型的参数，可以传 class 类型，参：@class泛型类
                简评：通常不见时使用 invoke 方法，这是因为
                    invoke 的参数和返回值必须是 Object 类型的。
                    这就意味着必须进行多次的类型转换。这样做将会使编译器错过检查代码的机会。
                    因此， 等到测试阶段才会发现这些错误， 找到并改正它们将会更加困难。
                    不仅如此， 使用反射获得方法指针的代码要比仅仅直接调用方法明显慢一些。
                    有鉴于此， 建议仅在必要的时候才使用 Method 对象
            调用任意构造函数创建对象
                &<Constructor类的newInstance>
                同 getMethod 类似，class 也提供有专门获得指定构造函数对应的 Constructor 的方法
                Constructor<T> getDeclaredConstructor(Class<?>... parameterTypes)  
                然后，就可以调用 Constructor 的 T newInstance(Object... initargs)  创建相应实例
                相关：@class类的newInstance
    第6章 接口、lambda表达式、内部类、代理
        接口
            定义接口  &<接口>
                在 Java 程序设计语言中， 接口不是类，而是对类的一组需求描述
                这些类要遵从接口描述的统一格式进行定义。
                接口定义举例：
                public interface Comparable
                {
                    int compareTo(Object other);
                }
                注：Arrays类的sort方法对数组进程排序，会要求数组元素的类实现了 Comparable 接口
                为了使接口更抽象，更通用，从java5开始，接口支持泛型：
                public interface Comparable<T>
                {
                    int compareTo(T other) ; // parameter has type T
                }
                接口中的所有方法自动地属于 public。 因此在接口中声明方法时，不必提供关键字public
                注：一个接口中有私有方法是没有意义的
                注：接口也是继承自Object，但不能用反射机制，反射机制内部会判断是不是接口类型
            实现接口
                一个类要"实现"一个接口, 应该用 implements 关键字  &<实现接口>
                举例：
                class Employee implements Comparable<Employee>
                {
                    public int compareTo(Employee other)
                    {
                        return Double.compare(salary, other.salary
                    }
                }
                与类只能继承一个类不同，它可以选择实现多个接口，如：
                class Employee implements Cloneable, Comparable
                注：类可以同时继承一个类，又实现了多个接口，两者不冲突
                注：普通类必须实现接口中的所有方法，抽象类不用 @抽象类
                相关： 继承类使用 extends 关键字，参 @继承类
            接口中包含常量
                接口中除了可以包含一到多个方法外，还可以包含常量（但不可以包含变量）
                接口中的常量会自动设为 public  static  final（所以在接口中定义常量时，无需加这些关键字）
            接口中定义默认方法
                从java8开始，允许在接口中实现（静态）方法（之前的版本不可以）
                但这有点违背接口概念的初衷，所以在标准库中，通常提供接口类及其伴随类
                如 Collection/Collections 或 Path/Paths
                接口中只提供函数声明，相关的实现在其伴随类中
                如果要为接口中的方法提供实现。 必须用 default 修饰符标记该方法
                public interface Comparable<T>
                {
                    default int compareTo(T other) { return 0; }
                    // By default, all elements are the same
                }
                一个接口中可以有多个默认实现，如：
                public interface MouseListener
                {
                    default void mousedieked(MouseEvent event) {}
                    default void mousePressed(MouseEvent event) {}
                    default void mouseReleased(MouseEvent event) {}
                    default void mouseEntered(MouseEvent event) {}
                    default void mouseExited(MouseEvent event) {}
                }
                解决默认方法冲突
                    实现多个接口时，如果不同接口中存在了相同签名的默认方法
                    Java按如下规则处理：
                    1 ) 超类优先。
                        如果继承的超类中提供了一个相同签名的具体方法，
                        则接口中具有相同签名的默认方法会被忽略。
                    2 ) 接口冲突。
                        如果一个超接口提供了一个默认方法，
                        另一个接口提供了一个相同签名的方法， 
                        必须覆盖这个方法来解决冲突、
                        注：即使另一个接口中没有提供相同签名的默认方法，
                            而只是包含了相同签名的函数声明，
                            Java也会报错，以要求实现类覆盖这个方法
                            当然，如果所有接口中都没有实现这个方法，
                            而只是包含相同签名的函数声明，则不会有问题
            定义接口类型变量
                接口不是类，尤其不能使用 new 运算符实例化一个接口
                然而， 尽管不能构造接口的对象，却能声明接口类型的变量
                接口变量指向实现了该接口的类实例，如
                ActionListener listener = new TimePrinter();
                接下来， 如同使用 instanceof检查一个对象是否属于某个特定类一样， 
                也可以使用 instanceof 检查一个对象是否实现了某个特定的接口
                if ( 对象 instanceof 接口 ） { ... }
            接口继承别的接口
                一个接口，可以用 extends 继承另一个接口
                注：接口继承接口，或类继承类，都用 extends 关键字，类实现接口用 implements 关键字
            接口 vs 抽象类  @抽象类
                Java之所以在提供了抽象类的语法后，还引入接口，是因为抽象类不能被多继承
                接口的优势：一个类可以选择实现多个接口
                抽象类的优势：类中可以定义成员变量
            接口与回调
                像如定时器，在c++中，可以提供一个回调函数，定时器周期性的调用它
                但java采用的是纯粹的面向对象的语言，所以它使用的方式是
                将某个类的对象传递给定时器，然后，定时器调用这个对象的方法
                由于对象可以携带一些附加的信息，所以传递一个对象比传递一个函数要灵活得多
                但是定时器需要直到调用对象的哪个方法，所以定时器要求对象实现 ActionListener 接口
                public interface ActionListener
                {
                    void actionPerfonned(ActionEvent event);
                }
                当到达指定的时间间隔时，定时器就调用 actionPerformed 方法。
                ActionEvent 参数提供了事件的相关信息，例如， 产生这个事件的源对象
            Comparator 接口
                其实这个接口前面已经提及过，对一个对象数组排序，会要求
                这些对象是实现了 Comparable 接口的类的实例
                String 类实现了Comparable<String>, 
                所以 String.compareTo 方法可以按字典顺序比较字符串
                但假如我们想按字符串数组的长度排序
                要处理这种情况，ArrayS.Sort 方法还有第二个版本
                需要传递一个数组和一个比较器作为参数，
                比较器是实现了 Comparator 接口的类对象（用它完成数组元素的比较）
                public interface Comparators  //注：不是 Comparable 接口
                {
                    int compare(T first, T second);
                }
            Cloneable 接口 （标记接口）
                这个接口指示一个类提供了一个安全的 clone 方法
                平常将一个变量赋值给两个变量，由于Java中变量的本质是引用
                所以结果将是这两个变量指向同一个对象实例，
                而 clone 方法，就是用于复制出一个与源实例具有相同成员变量值的新实例
                虽然 Object 类提供有 clone 接口，但它却是 Object 类的 protected 成员
                所以对象没法直接调用这个方法
                '''其实这是可以想象的，因为一个类中可以包含多个成员变量，
                而成员变量所对应的类中又可包含更子一级的成员变量，如此递归，
                而Java的成员变量的本质又是引用，所以Object无法准确知道究竟哪些成员变量
                应该被克隆，哪些成员变量可以共享'''
                所以交由最终类去负责真正实现 clone 接口是合理的
                但如何方便的知道一个对象/最终类，是否实现了 clone 接口呢
                其实就是看他是否实现了 Cloneable （ 用 isInstanceof 判断）
                Cloneable 接口的定义：
                public interface Cloneable {]
                可见它并没有提供任何函数声明，类实现的clone方法，是Object类的
                该接口存在的意义只是用于判定一个类是否实现了该接口 & 实现了 clone 函数
                （这是一个约定，如果一个类实现了 clone 函数，则应该实现 Cloneable 接口）
                像如 Cloneable 接口这样的，没有提供任何函数声明的接口，
                有个专有的名字：标记接口，它只是用于标记某个类实现了某个方法
                但这不影响使用标记接口定义接口类型的变量
                注：Object的clone提供了浅拷贝，如果只是想实现浅拷贝，
                    则自定义类可在公开的clone方法中直接调用Object的clone方法
                注：标准库中只有不到5%的类实现了clone
        lambda 表达式
            lambda 表达式是一个可传递的代码块， 可以在以后执行一次或多次
            参：file://../C C++/C++11/lambda表达式 c++.py
            可能跟c++的lambda表达式有些出入，java的lambda表达式格式为：
                ([[类型] 参数],...) -> 一个表达式
                ([[类型] 参数],...) -> { 多条语句; }
                可以不传递参数，此时()中是空的，也可以传递多个参数
                如果参数的类型能够推导出来，则参数的类型是可以省略的
                举例：
                (String first, String second) ->
                    {
                        if (first.lengthO < second.lengthO) return -1;
                        else if (first.lengthO > second.lengthO) return 1;
                        else return 0;
                    }
                Comparator<String> comp = (first, second) //前面的String类型省略了
                    -> first.lengthO - second.lengthO;
            函数式接口
                Java中已经有很多封装代码块的接口，如 ActionListener 或 Comparator
                对于只有一个抽象方法的接口， 需要这种接口的对象时，
                就可以提供一个 lambda 表达式。这种接口称为函数式接口
                换句话说，就是如果一个参数是函数式接口类型，
                则就可以为该参数赋值一个lambda表达式，
                甚至，将一个lambda表达式直接赋值给一个普通的函数式接口变量也是可以的
                如：BiFunction<String, String, Integer〉comp =
                    (first, second) -> first.lengthO - second.length();
                    注：BiFunction<String, String, Integer> 是个函数式接口
                如果将lambda表达式传递给非函数式接口类型的参数，则会编译报错
                理解为什么只有一个抽象方法的接口才可以用lambda表达式代替：
                    假定函数式接口可以支持多个方法，
                    则可以在接口中提供两个名字不同，但参数形式一致的方法，
                    此时lambda表达式做参数时，
                    编译器就不知道该lambda表达式对应的真正是哪个方法了
                另外要注意，函数式接口需要有且只有一个抽象方法，
                什么是抽象方法呢，就是该接口中所描述的这个方法，
                是实现该接口的类（及其父类）原先所没有的
                举例：
                Timer t = new Timer(1000, event ->
                    {
                    System.out.println("At the tone, the time is " + new Date());
                    Toolkit.getDefaultToolkit().beep();
                    });
                可见，使用lambda更加简短易读
                java API 在java.util.fimction 包中定义了很多非常通用的函数式接口
                ArrayList 类有一个 removelf 方法， 它的参数是一个 Predicate。
                Predicate 函数式接口就是在java.util.fimction 包中定义的
                下面的语句将从一个数组列表删除所有 null 值：
                list.removelf(e -> e == null);
            方法引用 略
            构造器引用  略
            lambda 的实现原理
                编译时
                    1. Lambda 表达式会生成一个方法， 方法实现了表达式的代码逻辑
                       此方法的参数列表和返回类型和lambda表达式一致
                       如果有捕获参数， 则此方法的参数可能会更多一些
                    2. 生成invokedynamic指令，调用bootstrap方法，
                       该方法的内部实现是调用 java.lang.invoke.LambdaMetafactory.metafactory方法
                       该函数返回一个 callsite 对象类型
               运行时
                    1. invokedynamic指令调用metafactory方法，得到一个 CallSite
                       此CallSite返回目标类型的一个匿名实现类， 此类关联编译时产生的方法
                    2. 调用函数式接口中的方法时，会调用匿名实现类关联的方法
            变量作用域
                通常， 你可能希望能够在 lambda 表达式中访问外围方法或类中的变量
                lambda 体中是可以直接使用其所在代码块的"最终变量"的
                    什么是"最终变量"呢？就是特指这个变量初始化之后就不会再赋新值
                    也就是说，该变量是明确声明final，或实际效果上是final的变量
                    例如，lambda体中使用了一个外部的 str 变量，
                    如果 str 变量在外面是由一个确定的值，则这是可以的
                    但如果 str 变量及lambda表达式同在一个循环语句的块中
                    且每次循环，str的值都会变化，则这就不行了
                    为什么要求是"最终变量"，官方给出的解释是：
                    虽然我们放宽了对捕获值的语法限制，
                    但我们仍然禁止捕获可变局部变量。
                    原因是像这样的习惯用法:
                    int sum = 0;
                    list.forEach(e -> {sum += e.size();});//错误
                    基本上是串行的;
                    编写这样没有竞争条件的lambda体是相当困难的。
                    除非我们愿意强制要求（最好是在编译时）这样的函数不能脱离它的捕获线程，
                    否则这个特性可能会带来比它解决的更多的麻烦。
                    Lambda表达式关闭值，而不是变量
                    换言之，也就是说，lambda表达式原则上支持在别的线程中执行
                    如果lambda要支持可以改变的变量，则处理同步是个麻烦，
                    所以干脆不支持了
                lambda 表达式的体，与嵌套块有相同的作用域，
                    这就要求lambda表达式的()中的变量，以及体中声明的局部变量
                    不能与其所在的代码块中已有的变量重名
                this指针
                    当lambda在一个函数中时，
                    lambda体中可以使用this指针，该this指针的语义
                    与其所在的代码块中使用this时的语义是一致的
                    都是指传给该函数的隐式的this指针
                    （注意不是指向函数式接口对应的类对象）
        内部类
            -内部类（ inner class ) 是定义在另一个类中的类
            -·内部类方法可以访问该类定义所在的作用域中的数据， 包括私有的数据。
            -·内部类可以对同一个包中的其他类隐藏起来。
            -·当想要定义一个回调函数（实现一个函数式接口类）且不想编写大量代码时，
            - 使用匿名 （anonymous) 内部类比较便捷。
            内部类 vs C++嵌套类
                内部类的对象有个隐式的引用，它引用了实例化该内部对象的外围类对象
                通过这个指针， 可以访问外围类对象的全部状态
                换言之，就是内部类既可以访问自身的数据域，
                也可以访问创建它的外围类对象的数据域
                静态内部类没有这种附加指针，这样的内部类与 C++ 中的嵌套类很相似
            内部类的特殊语法规则
                1. 内部类可以使用private访问控制符，但普通类要么使用public，要么不带
                   当不带时，只具有包可见性，不可使用private
                2. 创建共有内部类的对象时，使用：
                   class OuterClass
                   {
                       public class InnerClass()
                       {
                           ...
                       }
                       private String str;
                   }
                   OuterClass outer = new OuterClass();
                   OuterClass.InnerClass inner = outer.new InnerClass();
                   之所以不是 new outer.InnerClass()，是因为还要把outer的引用传给内部类对象
                3. 引用外部类变量时，其实完全的写法应该是 OuterClass.this.str
                4. 内部类中声明的所有'静态域'都必须是 final。
                   想想外部类的静态域，它是属于类的，是独立于对象的，被所有类实例共有的，
                   所以实例访问静态域时，都是看到的一致的值
                   但对于内部类，每个外部类的实例，都各自持有内部类的类实例，
                   包括内部类的静态成员，也是每个外部类对象各有一份，
                   于是，内部类的静态成员，就不再是与对象无关的了
                   outer1的内部类静态成员值可能是这个值，而outer2的内部类静态成员值可以是另一个值
                   但其实我们在内部类中使用静态成员的本意是想让静态成员被各个内部类对象共享
                   （即使这两个内部类对象分属不同的外部类实例）
                   要做到这一点，只能是将内部类的静态成员置为final，才能保证其值唯一
                5. 内部类不能有static方法
                   Java 语言规范对这个限制没有做任何解释
            编译器对内部类的处理
                内部类是一种编译器现象， 与虚拟机无关。
                编译器将会把内部类翻译成用 $ (美元符号）分隔的外部类名与内部类名的常规类文件， 
                （例如 Outer$Inner.class），而虚拟机则对此一无所知。
                编译器处理时，会在内部类中添加个 final Outer this$0; 成员变量，
                并会给所有的函数增加一个Outer类型的参数，
                而为了内部类能访问外部类的私有成员，编译器也为内部类添加了相应的方法，
                通过调不同的方法，就可得到外部类中不同的私有成员
                注：基于此，想要使用反射创建内部类，应指定类名为"Outer$Inner"
            局部内部类
                在一个函数中也可以定义内部类，这称为局部内部类
                局部类不能用 public 或 private 访问说明符进行声明。
                它的作用域被限定在声明这个局部类的块中
                与其他内部类相比较， 局部类还有一个优点
                它们不仅能够访问包含它们的外部类， 还可以访问局部变量
                不过， 那些局部变量必须事实上为 final
                （这一点和lambda表达式的要求一致，还是出于多线程的考虑）
                如下是个在方法中使用内部类的例子：
                public void start(int interval, boolean beep)
                {
                    class TimePrinter implements ActionListener
                    {
                        public void actionPerformed(ActionEvent event)
                        {
                            Systea.out.println("At the tone, the tiie is " + new Date())；
                            if (beep) Toolkit.getDefaultToolki10 ?beep();
                        }
                    }
                    ActionListener listener = new TimePrinter();
                    Timer t = new Timer(interval, listener);
                    t.start();
                }
                可以发现，当定时时间到时，该start函数肯定已经执行完了，
                此时beep参数变量原则上来说应该失效了（但内部内却使用了该参数）
                所以，编译器的实现是，
                在该内部类中添加了一个新的final类型的成员变量（但不是静态的），
                让该变量存储beep（相当于克隆出一个新的beep对象）
                该变量的赋值是在该内部类实例创建的时候完成的（这时还在start函数内），
                但该内部类实例的 actionPerformed 方法的执行，却是在定时器到后才执行
            匿名内收类
                public void start(int interval, boolean beep)
                {
                    ActionListener listener = new ActionListener()
                        {
                            public void actionPerformed(ActionEvent event)
                            {
                                System.out.println("At the tone, the time is " + new Date())；
                                if (beep) Toolkit.getDefaultToolkit().beep();
                            }
                        }；
                    Timer t = new Timer(interval, listener);
                    t.start0；
                } 
                匿名内部类因为没有名字，所以也就没有构造函数一说，但它仍会调用父类的构造函数
                new 后面的 ActionListener，也不是该匿名类的名字，而是其父类或实现接口的名字
                注意 new 的 ActionListener 类名后面紧跟一个小括号，然后才是大括号，
                java 中，只要 new 一个对象，对象后面一定跟一个小括号，匿名内部类也不例外
                匿名内部类在java8后，有更好的替代方案，就是lambda表达式
                在静态方法中获取到当前类的类名
                    你可能想到用 getClass().getName()， 但这是不行的
                    因为 getClass() 不是一个静态方法，只有一个对象实例才能调用 getClass() 方法
                    我们可以这样用： new Object(){}.getClass().getEncloseClass().getName()
                    还可以是 new Cloneable() {}.getClass().getEnclosingClass().getName() 等
            静态内部类
                如果不需要在内部类中使用外围类的成员变量，
                可以将内部类声明为static的
                静态内部类的对象除了不能访问外围类的成员外，与其他所有内部类完全一样
                静态内部类有其存在的意义：
                通常调用其它内部类时，由于需要外部类实例作为隐式参数传给内部类，
                所以要么需要"外部类对象.new 内部类()"，要么需要在外部类的非静态方法中"new 内部类()"
                但静态内部类由于不需要传外部类实例的引用，所以它可以在外部类的静态方法中创建
                c++的嵌套类更像是这里的静态内部类
        代 理
            利用代理，可以在"运行时"（不是编译期）
            创建一个（实现了一组给定接口）的类
            对于程序设计人员来说，通常用不到代理
            然而，对于系统程序设计人员来说，代理带来的灵活性却十分重要
    第7章 异常、 断言和日志
        处理错误
            异常的分类
                所有异常对象都继承自 Throwable 基类，用户也可以定义自己的异常类
                Throwable 的一级子类有两个， Error 和 Exception
                Error 描述了 Java 运行时系统的内部错误和资源耗尽错误，
                应用程序不应该抛出这种类型的对象
                在设计 Java 程序时， 需要关注 Exception 
                Exception 又有两个一级子类， lOException, RuntimeException
                通常由程序错误导致的异常，都属于 RuntimeException 分支
                如错误的类型转换、数组访问月结、访问null指针等，
                而文件读写错误、文件打开失败、根据给定的名字查找Class对象失败等
                则属于IOException分支
                有这样一句话：如果出现 RuntimeException 异常，那一定是你的问题
                Java 规范将派生于 Error 类或 RuntimeException 类的所有异常称为
                非受查( unchecked ) 异常，所有其他的异常称为受查（checked) 异常。
            声明受查异常
                编译器将核查是否为所有的受査异常（IOException分支的异常）
                提供了异常处理器
                方法应该在其首部声明（或在内部处理）所有可能抛出的受查异常
                这样可以从首部反映出这个方法可能抛出哪类受査异常。
                例如， 下面是标准类库中提供的 FilelnputStream 类的一个构造器的声明
                public Fi1elnputStream(String name) throws FileNotFoundException
                如果方法抛出多个受查异常，则 throws 受查异常类1,受查异常类2,...
                如果方法内可能产生的受查异常既没有声明，也没有在方法内被处理，
                则编译器会报错
                子类覆盖超类的（能抛出受查异常）的方法
                    此时，子类方法声明的受查异常，不能比父类方法中声明的异常更通用
                    子类方法可以声明与父类方法相同的异常，或该异常的子类，或不声明异常
                    如果父类方法没有声明异常，则子类中覆盖该方法时，也不能声明异常（注）
                    这是因为，考虑到多态，基类指针指向子类对象，调用子类方法，
                    但在调用基类指针的代码中，有可能看不到其指向的子类方法的函数签名，
                    如果要处理基类方法抛出的异常，只要用基类方法声明的异常类型接收即可，
                    子类方法只可能抛出基类方法声明的异常类，或其子类
                    注：对于上面这样的不允许声明异常的方法，如果在方法内收会产生受查异常
                    则只能选择在该方法内部消化处理掉
                声明非受查异常是允许的，但没必要，因为对于Error类异常，没法接收处理，
                而对于 RuntimeException 类异常，是代码设计的问题，应该在代码上避免
            如何抛出异常
                throw new 异常类();
                这里抛出的异常类，可以是声明的异常类，也可以是其派生类
                有些异常类，其构造函数还支持接收参数（如EOFException），从而描述问题原因
                一旦抛出异常后，函数就返回了，不会继续执行函数的剩余部分了
                注意，在Java中，只能 throw Throwable 子类的对象，
                所以要抛出的自定义异常类，也得继承自 Throwable 类，
                甚至进一步说，最好应该抛出受查异常类（IOException）的子类
            创建异常类
                Throwable（及其子类）都至少有两种构造函数，
                一种是无参的，一种接受一个字符串参数
                Throwable的toString方法，会返回字符串参数设置的内容
                自定义类建议也提供带字符串参数的构造函数，
                并在其内调用 super(str) --父类的构造函数
            捕获异常
                格式：
                    try
                    {
                        可能产生异常的代码
                    }
                    catch (异常类1 e1)
                    {
                        处理异常
                    }
                    catch (异常类2 | 异常类3 e2)  //捕获多个异常
                    {
                        处理异常
                    }
                    catch (异常类n e3)
                    {
                        处理异常
                    }
                    finally
                    {
                        所有情形下都会执行的代码，包括异常处理代码再次抛出异常时
                    }
                    后续代码：只要异常处理部分没再抛出异常，这块的代码就会被执行到
                注：catch子句及finally子句在语法上都是可以省略的，
                    当没有catch子句时，异常会在函数执行完后重新抛出
                    在try语句块中可以嵌套使用子的try语句块，
                    如果子的try语句块没有catch子句，则会在最后将异常抛出
                    并被外层的try语句块捕获（处理）
                如果代码抛出了 catch 子句中没有声明的异常，则该函数会退出
                此时要求函数声明那些没有处理的受查异常
                编译器会检查调用了（会抛出受查异常）方法的上下文，
                看该受查异常是否被在调用函数中声明或被处理
                可以在处理异常的代码中尝试使用 e.getMessage() 或 e.getClass().getName()
                捕获多个异常时，如 e2 ，该异常变量隐含为 final 变量，
                因此不能对 e2 重新赋值
                捕获多个异常的写法，不仅更简洁，还更高效
                注：支持在处理异常的代码中，选择再次 throw 该异常e ，或新的异常类
            再次抛出异常 & 异常链
                所有异常类支持 initCause(Throwable e) 和 Throwable getCause() 方法
                所以，在上面的异常处理代码中，可以选择抛出一个新的异常类，
                并把原始异常类通过 initCause 方法记录到新异常类中
                而原异常类也是有可能通过 initCause 方法存了一个更原始的异常类
                如此便形成了一个异常链，
                通过检查异常链，可一路追踪诱发异常的根本原因
            带资源的try语句
                try ( 资源类 res = new 资源类(...); 资源类2 re2 = new 资源类2(...) )
                {
                }
                注：try后面的括号中可以创建1个或多个资源类变量，用分号分隔
                要求该资源类实现了 AutoCloseable 接口，该接口中有个close方法
                无论try语句块中的代码正常完成，还是出现异常，
                都会自动调用 res.close() 和 res2.close() 方法，
                而如果 close() 时引发了新的异常，该新异常会被"抑制"：
                所谓的"抑制",是指调用原有异常（try中抛出的异常）的 addSuppressed 方法，
                将close() 时的异常添加到原有异常中（通过 getSuppressed 方法可获取到）
                使用这种方式，就不用担心 close() 时产生的异常把原来 try 子句中的异常冲掉了
                如果有需要，推荐使用这种带资源的try语句， 举例：
                try (Scanner in = new Scanner (new FileInputStream("/tmp/abc"). "UTF-8"):
                     PrintWriter out = new Pri ntWriter("out.txt"))
                {
                    while (in.hasNextO)
                    out.pri ntl n(i n.next().toUpperCaseO);
                }
            获得函数调用堆栈
                可以调用 Throwable 类的 printStackTrace 方法访问堆栈轨迹的文本描述信息
                Throwable t = new ThrowableO；
                StringWriter out = new StringWri ter() ;
                t.printStackTrace(new PrintWriter(out));
                String description = out.toStringQ ;
                一种更灵活的方法是使用 getStackTrace 方法， 
                它会得到 StackTraceElement 对象的一个数组:
                Throwable t = new ThrowableO ;
                StackTraceElement[] frames = t.getStackTrace() ;
                for (StackTraceElement frame : frames)
                    analyze frame
                StackTraceElement 类含有能够获得文件名和当前执行的代码行号的方法
                同时， 还含有能够获得类名和方法名的方法
                toString 方法将产生一个格式化的字符串， 其屮包含所获得的信息。
                静态的 Thread.getAllStackTrace 方法， 它可以产生所有线程的调用堆栈：
                Map<Thread, StackTraceElement[]> map = Thread.getAl1StackTraces() ;
                for (Thread t : map. keySet () )
                {
                    StackTraceElement[] frames = map.get(t) ;
                    analyze frames
                }
            异常处理技巧
                不要只抛出 RuntimeException 异常。应该寻找更加适当的子类或创建自己的异常类。
                不要只捕获 Thowable 异常， 否则，会使程序代码更难读、 更难维护
                不要过度使用异常，对于那些几乎不可能发生的异常，就不要声明和抛出了
                要不然该方法的使用者就需要处理或再次抛出这些几乎不会发生的异常
                通常传递异常比内部处理异常更好，让高层次的调用者选择如何处理该异常
        .使用断言
            断言机制允许在测试期间向代码中插入一些检査语句。
            当代码发布时，这些插人的检测语句将会被自动地移走
            Java 语言引人了关键字 assert。
            语法： assert 条件 [：表达式] ；
            如果条件为false，则抛出一个 AssertionError 异常
            如果有表达式，表达式将被传人 AssertionError 的构造器，并转换成一个消息字符串。
            “表达式” 部分的唯一目的是产生一个消息字符串
            AssertionError 对象并不存储表达式的值， 因此， 不可能在以后得到它。
            举例：
                assert x >= 0 : x;  //调用异常的toString，或得到的是x的值（的字符串形式）
                assert x >= 0: "x >= 0";  //调用异常的toString，或得到的是 "x > 0"
            在默认情况下， 断言被禁用。可以在运行程序时用 -enableassertions 或 -ea 选项启用：
            对于 eclipse，可以在 
            "菜单/Run/Run Configtions/Java application/类名/Arguments选项卡/VM arguments"
            中设置启动参数
            启用或禁用断言，不必重新编译程序
            （启用或禁用断言是类加载器( class loader) 的功能）
            也可以在某个类或整个包中使用断言， 例如：
            java -ea:MyClass -ea:com.mycompany.mylib... MyApp
            这条命令将开启 MyClass 类以及在 com.mycompany.mylib 包和它的子包中的所有类的断言
            也可以用选项 -disableassertions 或 -da 禁用某个特定类和包的断言
            java -ea:... -da:MyClass MyApp
            启用和禁用所有断言的 -ea 和 -da 开关不能应用到那些没有类加载器的“ 系统类”上
            对于这些系统类来说， 需要使用-enablesystemassertions/-esa 开关启用断言。
            不应该使用断言作为程序向用户通告问题的手段。
            断言只应该用于在测试阶段确定程序内部的错误位置。
        记录日志
            评价
                JUL（Java util logging），Java 原生日志框架，不需要引入第三方依赖包，
                使用简单方便，一般在小型应用中使用，主流项目中现在很少使用了。
            总述
                file://imgs/JUL架构.png
                Application：
                    Java 应用程序。
                Logger：
                    记录器，Java 应用程序通过调用记录器的方法来发布日志记录。
                Handler：
                    处理器，每一个 Logger 都可以关联一个或多个 Handler，
                    Handler 从 Logger 获取日志并将日志输出到某个目的地，
                    目的地可以是控制台，本地文件，或网络日志服务，
                    或将它们转发到操作系统日志等等。
                    通过Handler.setLevel(level.off)方法可以禁用一个 Handler，
                    也可以设置其他级别来开启此 Handler。
                Filter：
                    过滤器，根据条件过滤哪些日志记录。
                    每一个 Logger 和 Handler 都可以关联一个 Filter。
                Formatter ：
                    格式化器，负责对日志事件中的日志记录进行转换和格式化。
                Level：
                    每一条日志记录都有一个关联的日志级别，表示此条日志的重要性和紧急程度。
                    也可以对 Logger 和 Handler 设置关联的日志级别。
            使用日志api的优点：
                ?可以很容易地取消全部日志记录，或者仅仅取消某个级别的日志，
                 而且打开和关闭这个操作也很容易。
                ?可以很简单地禁止日志记录的输出， 
                 因此，将这些日志代码留在程序中的开销很小。
                ?日志记录可以被定向到不同的处理器， 
                 用于在控制台中显示， 用于存储在文件中等。
                ?日志记录器和处理器都可以对记录进行过滤。
                 过滤器可以根据过滤实现器制定的标准丢弃那些无用的记录项。
                ?日志记录可以采用不同的方式格式化，例如，纯文本或 XML。
                ?应用程序可以使用多个日志记录器， 
                 它们使用类似包名的这种具有层次结构的名字，
                 例如， com.mycompany.myapp 0
                ?在默认情况下，日志系统的配置由配置文件控制。 
                 如果需要的话， 应用程序可以替换这个配置
            基本日志
                要生成简单的日志记录，可以使用全局日志记录器（global logger) 
                并调用其 info 方法：
                Logger.getClobal().info("File->Open menu item selected");
                在默认情况下，这条记录将会显示以下内容
                May 10, 2013 10:12:15 PM LogginglmageViewer fileOpen
                INFO: File->0pen menu item selected
                但是， 如果在适当的地方（如 main 开始）调用
                Logger.getClobal ().setLevel (Level.OFF);
                将会取消所有的日志。
            高级曰志
                可以调用 Logger 的 getLogger 方法创建或获取记录器：
                private static final Logger myLogger 
                        = Logger.getLogger("com.mycompany.myapp"):
                注：声明为static，是为了共用，也为了防止其被垃圾回收
                日志的级别
                    与包名类似， 日志记录器名也具有层次结构
                    日志记录器的父与子之间将共享某些属性。 
                    例如，如果对 com.mycompany 日志记录器设置了日志级别，
                    它的子记录器也会继承这个级别 
                    通常， 有以下 9 个日志记录器级别：
                        · OFF       //关闭所有级别的记录
                        · SEVERE    //严重错误
                        · WARNING   //警告
                        · INFO      //提示
                        · CONFIG    //显示配置信息
                        · FINE      //良好
                        · FINER     //更好
                        · FINEST    //非常好
                        · ALL       //开启所有级别的记录
                    在默认情况下，只记录到 INFO 这个级别。 也可以设置其他的级別。
                    设置为 INFO 时，INFO 级别，及其之上的更严重的级别将会被显示
                    例如，logger.setLevel (Level.FINE);
                日志记录所在类名及方法名：
                    默认的日志记录将显示包含日志调用的类名和方法名
                    但是,如果虚拟机对执行过程进行了优化，就得不到准确的调用信息
                    此时，可以调用 logp 方法获得调用类和方法的确切位置：
                    void logp(Level 1, String className, String methodName, String message)
                Logger类的基本日志方法：
                    void severe(String msg) 
                    void warning(String msg) 
                    void config(String msg) 
                    void info(String msg) 
                    void fine(String msg) 
                    void finer(String msg) 
                    void finest(String msg) 
                    void log(Level level, String msg) 
                    void log(Level level, String msg, Object param1) 
                    void log(Level level, String msg, Object[] params) 
                Logger类提供了如下日志辅助方法：
                    void entering(String className, String methodName)
                    void entering(String className, String methodName , Object param)
                    void entering(String className, String methodName , Object[] params)
                    void exiting(String className, String methodName)
                    void exiting(String className, String methodName, Object result)
                    例如：
                    int read(St ring file, String pattern)
                    {
                        1ogger .entering("com.mycompany.mylib.Reader", "read",
                                         new Object[] { file, pattern } );
                        ...
                        1ogger.exiting("com.mycompany.mylib. Reader", "read" , count):
                        return count;
                    }
                    这些调用将生成 FINER 级别和以字符串 ENTRY 和 RETURN 开始的日志记录。
                    注：这只是java8版本提供的辅助方法，之后的版本可能支持变参
                Logger类记录异常信息
                    void throwing(St ring className, String methodName , Throwable t)
                    void log(Level 1, String message, Throwable t)
                    通常在catch子句中使用这两个方法
                    使用这两个方法，可以将传入的异常对象所携带的异常信息记录在日志中
                修改日志管理器配置
                    可以通过编辑配置文件来修改日志系统的各种属性
                    在默认情况下， 配置文件存在于： jre/lib/1ogging.properties
                    要想使用另一个配置文件， 
                    就要将 java.util.logging.config.file 设置为配置文件的存储位置:
                    java -Djava.util.logging.config.file=configFile MainClass
                    也可以在 main中调用 
                    System.setProperty("java.util_logging.config_file"，file)
                    要想修改默认的日志记录级别， 需要修改配置文件：.level=INFO
                    可以通过添加以下内容来指定自己的日志记录级别：
                    com.mycompany.myapp.level=FINE
                    日志记录默认并不将消息发送到控制台上
                    要想在控制台上看到 FINE 级别的消息
                    java.util.logging.ConsoleHandler.level=FINE
                处理器 Handler
                    在默认情况下, 日志记录器将记录发送到 ConsoleHandler 中
                    与日志记录器一样， 处理器也有日志记录级别。
                    日志处理器配置文件设置的默认控制台处理器的日志记录级别为
                    java.uti1.1ogging.ConsoleHandler.level =INF0
                    我们也可以为Logger安装自己的处理器
                    Logger logger = Logger.getLogger("com.mycompany.myapp") ;
                    logger.setLevel (Level.FINE) ;
                    1ogger.setUseParentHandlers(false);  //删除父类的处理器
                    Handler.handler = new ConsoleHandler();   //新建处理器
                    handler.setLevel (Level.FINE);  //设置新建处理器的级别
                    1ogger.addHandler(hander):  //将新建的处理器关联到记录器上
                    在默认情况下， 日志记录器将记录发送到自己的处理器和父处理器。
                    而原始日志记录器默认将会把所有 >=INFO 级別的记录发送到控制台
                    而自己新建的日志处理器会把 >=FINE 级别的记录发送到控制台
                    于是，>=INFO 级別的记录将会被两次发送的控制台，
                    所以我们需要删掉父类的日志处理器
                    除了上面的ConsoleHandler，还可使用 FileHandler/SocketHandler
                    FileHandler 默认记录到用户主目录的 javan.log 文件中
                    （n 是文件名的唯一编号），默认为xml格式
                    file://imgs/在配置文件中配置FileHandler.png
                        表 7-2 ：
                        %h 系统属性 user.home 的值
                        %t 系统临时目录
                        %u 用于解决冲突的唯一编号
                        %g 为循环日志记录生成的数值。
                          （当使用循环功能且模式不包括%g时，使用后缀 %g）
                        %% % 宇符
                    自定义Handler类
                        可以通过扩展 Handler 类或 StreamHandler 类自定义处理器
                过滤器
                    在默认情况下， 过滤器根据日志记录的级别进行过滤
                    每个日志记录器和处理器都可以有一个可选的过滤器来完成附加的过滤
                    还可以通过实现 Filter 接口并定义下列方法来自定义过滤器
                    boolean isLoggab1e(LogRecord record)
                    返回 true 表示这些记录应该包含在日志中
                    要想将一个过滤器安装到一个日志记录器或处理器中， 
                    只需要调用 setFilter 方法就可以了。 
                    注意，同一时刻最多只能有一个过滤器。
                格式化器
                    ConsoleHandler 类和 FileHandler 类可以生成文本和 XML 格式的日志记录
                    也可以自定义格式。这需要扩展 Formatter 类并覆盖下面这个方法：
                    String format(LogRecord record)
                    可以根据自己的愿望对记录中的信息进行格式化，并返冋结果字符串。
                    在 format 方法中， 有可能会调用下面这个方法
                    String formatMessage(LogRecord record)
                    这个方法对记录中的部分消息进行格式化、 参数替换和本地化应用操作。
                    调用 setFormatter 方法将格式化器安装到处理器中
            Logger 父子继承关系
                在 JUL 中，Logger 有父子继承关系概念
                子代 Logger 对象会继承父 Logger 的配置，
                例如日志级别，关联的 Handler，日志格式等等
                对于任何 Logger 对象，如果没对其做特殊配置，
                那么它最终都会继承 RootLogger 的配置。
        调试技巧
    第8章 泛型程序设计
        .构造函数省略泛型类型
            从 Java SE7 开始，构造函数可以省略泛型类型，
            如：ArrayList<String> files = new ArrayList<>()
            省略的类型可以从变量的类型推断得出
        .定义简单泛型类
            举例：
                public class Pair<S,T>
                {
                    private S first;
                    private T second;
                    public Pair(S first, T second)
                    {
                        this.first = first;
                        this.second = second;
                    }
                    ...
        .泛型方法
            除了定义泛型类，还可定义泛型方法
            例：
                class ArrayAlg
                {
                    //获取数组的中间元素
                    public static <T> T getMiddle(T... a)
                    {
                        return a[a.length / 2];
                    }
                }
            当调用一个泛型方法时，在方法名前的尖括号中放入具体的类型：
            String mid = ArrayAlg.<String>getMiddle("a","b","c");
            在这种情况（实际也是大多数情况）下，方法调用中可以省略 <String> 类型参数。
            编译器有足够的信息能够推断出所调用的方法。
            String middle = ArrayAlg.getHiddle("a","b","c");
            与 C++ 写法格式的比较
                在 C++ 中将类型参数放在方法名后面， 有可能会导致语法分析的歧义。
                例如，g(f<a,b>(c)) 
                可以理解将'用 f<a, b>(c) 的结果'作为参数传给 g 函数，
                或者理解为将 f<a 和 b>(c) 两个语句的结果（逗号语句）作为参数传给 g 函数
        .类型变量的限定
            有时，类或方法需要对类型变量加以约束
            如：public static <T extends Comparable> T a) . . .
            这样，就限制了 T 必须要实现 Comparable 接口才行
            T 也可以有多个限定， 如 <T extends Comparable & Cloneable> T a) . . .
            为什么使用关键字 extends 而不是 implements
                读者或许会感到奇怪？ 在此为什么使用关键字 extends 而不是 implements ? 
                毕竟，Comparable 是一个接口。
                这是因为，上面泛型中的 T ，表示要适配的类型，应该是 Comparable 的子类型 （subtype)
                选择关键字 extends 的原因是更接近子类的概念
            与 c++ 比较
                在 C++ 中不能对模板参数的类型加以限制
        泛型代码与虚拟机
            - 虚拟机没有泛型类型对象 ——— 所有对象都属于普通类
            类型擦除
                无论何时定义一个泛型类型， 都自动提供了一个相应的原始类型
                （泛型类型只有编译器能看到，编译处理后，仍存在的是原始类型）
                原始类型的名字就是删去类型参数后的泛型类型名（擦除类型变量, 并替换为限定类型）
                例，Pair<T> 的原始类型如下所示 ：
                    public class Pair
                    {
                        private Object first;
                        private Object second;
                        // 当 T 没有进行限定时，就用 Object 代替 T
                        public Pair(Object first, Object second)
                        {
                            this.first = first;
                            this.second = second;
                        }
                        。。。
                    }
                    当 T 有限定时， 如 <T extends Comparable & Serializable>，
                    此时， T 会被替换为后面的第一个限定类型，在这里 T 被替换为 Comparable
                结果是一个普通的类， 就好像泛型引入 Java 语言之前已经实现的那样。
                当实例化一个泛型类型时，其本质是创建了该泛型类型的原始类型
                泛型类型只是方便编译期代码检查，编译后，看不到泛型类型，而是转化成了其原始类型
                从这一点来看，就不会存在 c++ 中的 "模板代码膨胀" (每个模板的实例化会产生不同的类型)
                的问题，这是与 c++ 泛型的实现原理的本质区别
            翻译泛型表达式
                如：
                    Pair<Person> couple = ...;
                    Persion p = couple.getFirst();
                    编译器会在编译时，自动插入 Persion 的强制转换类型，
                    也就是说，编译器把这个方法调用翻译为两条虚拟机指令：
                    ● 对原始方法 Pair.getFirst 的调用
                    ● 将返回的 Object 类型强制转换为 Persion 类型
                    当存取一个泛型域时，也要插人强制类型转换。
                    假设 Pair 类的 first 域和 second 域都是公有的
                    则表达式：Persion p = couple.first;
                    也会在结果字节码中插人强制类型转换。
            翻译泛型方法
                类型擦除也会出现在泛型方法中。
                如 public static <T extends Comparable〉T min(T[] a)
                擦除类型后，变为： public static Comparable min(Comparable[] a)
                方法的擦除带来了两个复杂问题。看一看下面这个示例：
                class Datelnterval extends Pair<LocalDate>
                {
                    public void setSecond(Localdate second)
                    {
                        //确保第二个时间要大于第一个时间
                        if (second.compareTo(getFirst()) >= 0)
                        {
                            super.setSecond(second);
                        }
                        ...
                    }
                }   
                一个日期区间是一对 LocalDate 对象，
                并且需要覆盖这个方法来确保第二个值永远不小于第一个值
                Pair类擦除类型后，变为：
                class Datelnterval extends Pair //擦除后
                {
                    public void setSecond(LocalDate second) { . . . }
                    ...
                }
                所以， Pair 中的 void setSecond(Object second) 方法也会被 Datelnterval 继承
                于是，就引入了多态（多态也是在运行期处理的）
                考虑下面的语句序列：
                Datelnterval interval = new Datelnterval(. . .);
                Pair<Loca1Date> pair = interval; //用基类指向派生类
                pair.setSecond(aDate);
                用于 pair 引用的是 Datelnterval 的对象， 
                所以我们期望的是调用 Datelnterval 的 setSecond 方法
                而不是 Pair 自身的 setSecond 方法
                为此，编译器的解决办法是，在 Datelnterval 类中会生成一个"桥方法" :
                public void setSecond(Object second) { setSecond((Date) second); }
                此时，相当于在 Datelnterval 中覆盖了 Pair 的 setSecond 方法（函数签名一致）
                于是，在执行上面的 pair.setSecond(aDate) 语句时
                变量 pair 已经声明为类型 Pair<LocalDate>，
                所以调用的是 Pair 的 setSecond 方法
                ？？？  &<未完待续>
            调用遗留代码
                设计 Java 泛型类型时， 主要目标是允许泛型代码和遗留代码之间能够互操作。
        .与 C++ 泛型类的区别
            表面上的区别是 java 不需要使用专门的 template 关键字
            但两者有本质的区别
    第9章 集合
        集合框架
        具体的集合
        映射
        视图与包装器
        算法
        遗留的集合
    第13章 部署Java应用程序
        JAR 文件
        应用首选项的存储
        服务加载器
        applet    
    第14章 并发
        线程
        线程状态
        线程属性       
        同步        
        阻塞队列        
        线程安全的集合        
        Callable 与 Future        
        执行器        
        同步器    
JNI技术 （基于java8）
    -https://zhuanlan.zhihu.com/p/349928909
    使用情形
        -1. 平台相关的功能，通常是为了追求性能，需要对Java虚拟机进行扩展，需要使用Native的实现。
        -2. Native的实现是已经存在的功能，使用JNI协议，方便使用已有的功能，不需要重新的Java实现。
        -3. Java的.class文件安全性较差，增加安全性，将重要的逻辑在Native代码中实现。
            
                    
            
            
            