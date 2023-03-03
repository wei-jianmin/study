第一卷
    第3章 基本语法
        Java区分大小写；每个句子必须用分号结束；
        main函数
            类中可以包含main函数，main函数的参数为 Strings[] args
            每个函数前面带 public 关键字，main函数前面还应该带 static 关键字
            返回值为 void，如果正常退出，则java应用程序返回0，
            如果希望终止时返回其它代码，则应调用System.exit()方法
        类定义：
            类名的命名规范为大驼峰命名法
            源代码文件的名字，与公共类的名字相同（并用.java作为扩展名）
            类名前带有public关键字，类的结束大括号后面无需跟 ; 作为结束符
            在命令行中通过java命令运行程序时，后面跟的是类名，而不是class文件名
        注释：
            单行注释：//
            多行注释：/*   */
            文档注释：/**  */
                这种注释方法可用来自动生成文档
        数据类型：
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
                如 \u000a 等同于 \n， " 等同于 \u0022
                所以 "\u0022+\u0022" 等同于 "" + ""，而不是 "\" + \""
                特别的，如 //c:\users\administrator 会报错，
                因为 \u 后面没有跟着4个十六进制数
            布尔：boolean
                在 C 中，数值是否为0或指针是否为空可作为布尔判断依据，在java中不允许
            常量：在变量类型前加关键字 finial 指示常量
                finial指示这个变量只能被赋值1次（c语言用的是const关键字）
        运算符：
            同 C 语言
        类型转换：
            同 C 语言，如 double a=3.2; int b = (int) a;
        移位运算：
            与C相比，增加了>>>，用0填充高位，而>>则是用符号位填充高位
            C/C++中，>>的实现方式没有规定，所以实现者可能使用算数移位（扩展符号位）
            或者使用逻辑移位（高位填充0），也就是说，C/C++的>>移位结果依赖于具体实现
        枚举：
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
            打印输出到“ 标准输出流”（即控制台窗口）只要调用 System.out.println 即可    
            然而，读取“ 标准输人流” System.in 就没有那么简单了
            要想通过控制台进行输人，首先需要构造一个 Scanner 对象，并与“ 标准输人流” System.in 关联 
            Scanner in = new Scanner(System.in);
            就可以使用 Scanner 类的各种方法实现输入操作了
            例如， nextLine() 方法将输入一行、next()读取一个单词（以空白为分隔符）、
            nextInt()读取一个整数、nextDouble()读取一个浮点数
            最后，在程序的最开始添加上一行  import java.util.*;  //Scanner 类定义在java.util 包中
            当使用的类不是定义在基本java.lang 包中时， 一定要使用 import 指示字将相应的包加载进来
            从控制台读取密码
                因为输入是可见的， 所以 Scanner 类不适用于从控制台读取密码
                Java SE 6 特别引入了 Console 类实现这个目的：
                Console cons = System.console();
                String username = cons.readLine("User name: ")；
                char [] passwd = cons.readPassword("Password: ");
                采用 Console 对象处理输入不如采用 Scanner 方便。每次只能读取一行输入， 
                而没有能够读取一个单词或一个数值的方法
            Scanner类提供的方法
                ? Scanner (InputStream in)  用给定的输入流创建一个 Scanner 对象。
                ? String nextLine( )        读取输入的下一行内容。
                ? String next( )            读取输入的下一个单词（以空格作为分隔符)。
                ? int nextlnt( )
                ? double nextDouble( )      读取并转换下一个表示整数或浮点数的字符序列。
                ? boolean hasNext( )        检测输人中是否还有其他单词。
                ? boolean hasNextInt( )
                ? boolean hasNextDouble( )  检测是否还有表示整数或浮点数的下一个字符序列。
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
        大数值
            如果基本的整数和浮点数精度不能够满足需求， 那么可以使用jaVa.math 包中的两个
            很有用的类：Biglnteger 和 BigDecimaL 这两个类可以处理包含任意长度数字序列的数值。
            Biglnteger 类实现了任意精度的整数运算， BigDecimal 实现了任意精度的浮点数运算。
            使用静态的 valueOf 方法可以将普通的数值转换为大数值：
            Biglnteger a = Biglnteger.valueOf(100);
            不能使用人们熟悉的算术运算符（如：+ 和 *) 处理大数值，
            而应使用大数值类提供的add和multiply方法
            注：与 C++ 不同， Java 没有提供运算符重载功能，程序员无法重定义 + 和 * 运算符
            Biglnteger成员方法：
                ? Biglnteger add(Biglnteger other)
                ? Biglnteger subtract(Biglnteger other)
                ? Biglnteger multipiy(Biginteger other)
                ? Biglnteger divide(Biglnteger other)
                ? Biglnteger mod(Biglnteger other)
                  返冋这个大整数和另一个大整数 other 的和、 差、 积、 商以及余数。
                ? int compareTo(Biglnteger other)
                  如果这个大整数与另一个大整数 other 相等， 返回 0; 
                  如果这个大整数小于另一个大整数 other, 返回负数； 否则， 返回正数。
                ? static Biglnteger valueOf(1ong x) 返回值等于 x 的大整数
            BigDecimal成员方法：
                ? BigDecimal add(BigDecimal other)
                ? BigDecimal subtract(BigDecimal other)
                ? BigDecimal multipiy(BigDecimal other)
                ? BigDecimal divide(BigDecimal other RoundingMode mode) 5.0
                  返回这个大实数与另一个大实数 other 的和、 差、 积、 商。
                  要想计算商， 必须给出舍入方式 （ rounding mode。) 
                  RoundingMode.HALF UP 是在学校中学习的四舍五入方式
                  它适用于常规的计算。有关其他的舍入方式请参看 Apr文档。
                ? int compareTo(BigDecimal other)
                  如果这个大实数与另一个大实数相等， 返回 0 ; 
                  要想计算商， 必须给出舍返回负数； 否则，返回正数。
                ? static BigDecimal valueOf(1 ong x)
                ? static BigDecimal valueOf(1 ong x ,int scale)
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
                ? static String toString(type[] a) 
                  返回包含 a 中数据元素的字符串， 这些数据元素被放在括号内， 并用逗号分隔。
                  参数： a 类型为 int、long、short、char、 byte、boolean、float 或 double 的数组。
                ? static type copyOf(type[] a, int length)
                ? static type copyOfRange(type[] a , int start , int end)
                  返回与 a 类型相同的一个数组， 其长度为 length 或者 end-start， 数组元素为 a 的值。
                  参数： a 类型为 int、 long、short、char、byte、boolean、float 或 double 的数组。
                  start  起始下标（包含这个值）0，
                  end    终止下标（不包含这个值）。 这个值可能大于 a.length，这时，结果为 0 或 false。
                  length 拷贝的数据元素长度。如果 length 值大于 a.length， 结果为 0 或 false ;
                         否则， 数组中只有前面 length 个数据元素的拷 W 值。
                ? static void sort(t y p e [ 2 a)
                  采用优化的快速排序算法对数组进行排序。
                  参数：a 类型为 int、long、short、char、byte、boolean、float 或 double 的数组。
                ? static int binarySearch(type[] a , type v)
                ? static int binarySearch(type[] a, int start, int end , type v) 
                  采用二分搜索算法查找值 v。如果查找成功， 则返回相应的下标值； 
                  否则返回一个负数值r。 -r-1 是为保持 a 有序 v 应插入的位置。
                  参数： 
                  a     类型为 int、 long、 short、 char、 byte、 boolean 、 float 或 double 的有序数组。
                  start 起始下标（包含这个值）。
                  end   终止下标（不包含这个值。)
                  v     同 a 的数据元素类型相同的值。
                ? static void fi11(type[] a , type v)
                  将数组的所有数据元素值设置为 v。
                  参数： 
                  a     类型为 int、 long、short、char、byte、boolean 、 float 或 double 的数组。
                  v     与 a 数据元素类型相同的一个值。
                ? static boolean equals(type[] a, type[] b)
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