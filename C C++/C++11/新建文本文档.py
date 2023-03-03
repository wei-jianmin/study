主要参考资料
    《深入理解c++11:c++11新特性解析与应用.pdf》
编译器支持情况  '关键字： gcc4.3，gcc4,7，vs2010，vs2015
    首先需要说明的是，c++11的改进很大，需要编译器做大量的工作，
    这对于大多数编译器供应商来说，只能分阶段的发布若干编译版本，
    逐步支持c++11的所有特性。
    gcc 从4.3版本开始简单支持c++11, 从4.7开始初步支持c++11，从4.8开始完全支持c++11
    需带选项 -std=c++11（默认的是使用c++98） 才能正常编译c++11的代码
    通过man gcc，查看对关于-std选项的描述(determine the language standard)
    可以查看当前gcc是否支持c++11规范
    vs2010开始支持c++11，但支持的还不是很完善，
    一直到了vs2015，才算对c++11的各种特性有了全面的支持。
    可以参考https://blog.csdn.net/qing666888/article/details/78260923
    该页面总结了个版本vs对c++11~c++14的支持情况。
    或者参考https://zh.cppreference.com/w/cpp/compiler_support#cpp11
    该页面汇总了各个编译器（包括vs、gcc）对c++各个版本的支持情况
c++各版本对比  '关键字：c++98、c++03、c++11、140、600
    c++98和c++03的差别很小，c++03主要对c++98标准中的漏洞进行了修复
    核心语言规则没有改动，所以人们习惯把这两个标准合称为c++98/03,
    或者直接简写为c++98。
    c++11则带来了数量可观的变化，这包括了约140个新特性，
    及对c++03中600个缺陷的修正。
c++发展编年史  '关键字： c++98，c++03，TR1，c++0x，c++11
    1990年  c++语言问世，但没有涉及库
    1998年  第一个c++标准：c98，
            包括了核心语言及STL、locale、iostream、numeric、string等诸多特性的描述
    2003年  第二个c++标准：c03
            核心语言及库与c++98一致，但包含了TC1（technical corrigendum 1,技术勘误表1）
    2005年  TR1（technical reprot 1,技术报告1）
            核心语言不变，tr1作为c++标准的‘非规范出版物’，包含了14个可能引入新标准的库
    2008年  基本上c++0x标准的核心特性都制定完成了
            c++0x标准包括了13个源自于tr1的库和70个新的库，修正了约300个bug
            此外新标准草案还包括了70多个新语言特性，及约300个语言缺陷的修正
    2011年  11月，c++11发布
c++特性一览 '关键字： 略
    暂时略过
与C99兼容  '关键字：__STDC_OSTED__，__func__，_Pragma，不定参数，宽窄字符串连接，long long
    c的最新标准是1999年的c99标准，而c++11前的最新标准是c++03，而c++03又与1998年的c++98基本一致，
    也就是说，c++98/03标准中，没有完全包含c99标准，而c++11中对c99中的漏网之鱼进行了包含。
    c++11增加的c99标准
        c99中预定义的宏
            __STDC_OSTED__  如果编译器所在环境中有完整的标准C库，该宏为1，否则为0
            使用qt5.9测试，不支持该宏
        __func__预定义标识符
            按照标准定义，编译器会隐式的在函数定义中添加__func__标识符，
            如： void func() {
                    static const char* __func__ = "func";
                    ...... }
            __func__不能作为函数参数的默认值
        _Pragma操作符
            _Pragma与'#pragma'功能一样,如'#pragma once'等同于_Pragma("once")
            相比预处理指令'#pragma'，_Pragma是个操作符，因此可以在一些宏中使用
        不定参数宏定义、__VA_ARGS__
            在c99中，程序员可以使用变长参数的宏定义
            变长参数的宏定义，是指在宏定制中，参数列表的最后一个参数为省略号
            而预定义宏__VA_ARGS__则可以在宏定义的实现部分替换省略号所代表的字符串
            如 #define PR(...) printf(__VA_ARGS__)
        宽窄字符串连接
            将窄字符和宽字符进行连接时，
            支持c++11标准的编译器会将窄字符串转换成宽字符串，
            然后再与宽字符串进行连接
            然后再与宽字符串进行连接
        支持long long类型
            两种：long long 和 unsigned long long， c++11中要求至少占64位(8字节)
            我们在写常数字面量时，可以用LL或ll后缀表示一个long long类型的字面量
            在ULL或ull或Ull或uLL表一个unsigned long long类型的字面量
            如：  long long ll; ll = 32LL;
使用__cplusplus宏  '关键字：201103
    在一些C/C++混编的代码中，常常会有如下的写法：
    '''
        #ifdef __cplusplus
        extern "C" {
        #endif
        //一些代码
        #ifdef __cplusplus
        }
        #endif
    '''
    事实上，__cplusplus宏不仅可以区分是否为c或c++编译器，还能区分c++编译器的版本
    在c++03标准中，__cplusplus的值为199711L，在c++11中，__cplusplus的值为201103L
    因此如果代码中使用了c++11特性，可以通过该值，判断编译器是否支持c++11
    '''
        #if __cplusplus < 201103L
        #error "should use c++11" //预处理时遇到该命令，将停止编译，并打印错误信息
        #endif
    '''
使用断言  '关键字：assert，static_assert
    在c++中，在<cassert>或<assert.h>中提供了assert宏，用于在运行时断言。
    如 void func(int i) { assert(i>0); ... }  //确保i大于0
    如果断言条件不满足，就会终止程序的运行
    使用断言的意义
        有时候，某个数据"正常不应该出现"，
        如果出现了，则不知道将会在哪个地方导致程序运行出现问题，
        对于这样的问题，等到程序崩溃了，其实很难发现到底是哪里导致的，
        此时，可以通过断言来及早发现异常，即使处理
        而在程序发行的时候，使用断言则是无意义的，甚至还更容易触发断言，
        导致原来可以执行的程序发生崩溃，
        所以在发行时，应该禁用断言。
    在c++中，可以通过定义宏NDEBUG来禁用assert宏
    但assert宏是在运行阶段才起作用的
    有时我们希望在编译阶段能做一些断言，
    在c++11中，引入了static_assert来解决这个问题
    它接受两个参数，一个是断言表达式，表达式通常返回一个布尔值
    另一个参数为警告信息字符串
    需注意的是，static_assert的断言表达式必须是在编译期可以计算的表达式，即常量表达式
    static_assert(sizeof(int)==8,"xx");   //正确使用
    void func(int i) { static_assert(i>0,"xx"); ...}   //错误使用
异常处理  '关键字：弃用throw，使用noexcept
    在c++98已经支持了异常处理系统，如
    void func() throw(int,double) { ... }
    在func函数声明之后，定义了动态异常声明throw(int,double)，
    该声明指出了func可能抛出的异常类型。
    但因为该特性很少被使用，因此在c++11中被弃用了，
    而表示函数不会抛出异常的动态异常声明throw()，可被noexcept异常声明取代
    如果noexcept修饰的函数抛出了异常，编译器可选择直接调用std::terminate()终止程序
    noexcept用两种使用方式：
        void func() noexcept;  //声明后直接使用noexcept关键字
        void func() noexcept(常量表达式);  
        //表达式的结果为bool型，true表不会抛出异常，false表可能抛出异常
    使用noexcept可以有效阻止异常的传播与扩散
    上面的noexcept是作为修饰符，标明函数是否会抛出异常
快速初始化类成员变量  '关键字：就地初始化
    在c++98中，只有静态整形成员或静态枚举型成员，才可以在类的定义中直接赋值，
    这种声明方式我们也称为“就地”声明。
    但在c++11中，则允许使用等号=或花括号{}进行“就地”的非静态成员变量初始化，
    如 struct init { int a=1; double b{1.2}; }
    附注：就地声明和构造函数的初始化列表，两者不冲突，可以同时使用，
    但初始化列表方式“后作用于”成员变量赋值，所以如果两者同时存在，
    则初始化列表方式赋的值，将是变量的真正值。
    另注： 对于非常量的静态成员，c++11与c++98保持了一致。
非静态成员的sizeof  '关键字：sizeof(类名::非静态成员变量)
    在c语言中，sizeof是个运算符（就像加减乘除运算符一样），
    在c++98中，sizeof求非静态成员变量的大小，sizeof(类名::非静态成员变量);
    会编译报错，c++11中，这样做是允许的
friend关键字  '关键字：模板类支持友元
    C++11对friend关键字进行了一些改进，
    在c++98中，声明一个类A为当前类的友元时，语句为： friend class A;
    在c++11中，这种方式仍然兼容，但去掉class关键字也是可以的，及friend A;
    甚至friend还可以跟类的别名，如 typedef A CA; friend CA;
    c++11对c++98的这一点改进，使得模板类也可以使用友元了，
    如 template <typename T>   class B { friend T; ...... }
    这个例子里，模板参数类T，可以访问B的私有成员，这在c++98中是做不到的。
final/override关键字   '关键字： 虚函数重载 
    重载的概念：子类与父类具有相同签名的虚函数
    如果我们不希望一个虚函数被子类重载，在c++98中，没有办法做到这一点，
    在c++11中，可通过final描述符，确保虚函数不会被子类重载，
    使用方法是在虚函数的声明后，加上final ：virtual void func() final;
    这样，如果派生类重载了该函数，则编译会报错。
    而override描述符，则表明一个虚函数是从父类或祖先类中重载而来的，
    如果父类或祖先类中没有相同签名的函数，编译器会报错，
    因此，使用override，既能指示这个函数是重载而来的，又可以保证函数签名没有写错。
    写法如: void func() override;
    最后注意，这两个关键字都是作用于虚函数的，final/override可以用作变量名使用，
    只有这两个描述符出现在特定位置（虚函数声明之后）才起到特定的作用。
    通过这样的设计，之前c++98中使用了final/override的代码就可以兼容编译了。
模板函数的新特性  '关键字：默认模板参数，显式实例化模板函数
    省略模板函数的模板类型
        如果模板函数中，函数的参数列表涵盖了所有的模板类型，
        且在调用该模板函数时，编译器能够猜测出模板类型对应的实际类型，
        则此种情况下，调用模板函数时，无需通过<>特别指定模板函数的类型。
        如：
            template <typename T1,typename T2>
            void func(T1 t1,T2 t2) { ... }
            则 func(1,2); 可正常编译，无需 func<int,int>(1,2);
            另外 func<>(1,2); func<float>(1,2); 等写法也是能正常编译的。
        当函数参数列表没有完全涵盖所有模板类型时，
        可以通过<>指定部分类型的方式，完成函数的调用
        当然这里的指定部分类型，应该以"能让编译器根据调用语句推测出所有模板类型"为准
        如：
            template <typename T1,typename T2>
            void func(T2 t)
            {
                T1 t3;
                t3 = t;
            };
            func<float>(3);
            这种是可以编译通过的：
            func<float>优先起作用，从而T1类型得以确定，T2类型未决。
            继而通过函数参数的实参(3)，确定T2的类型为整形。
            但如果改为如下方式：
            template <typename T1,typename T2>
            void func(T1 t)
            {
                T2 t3;
                t3 = t;
            };
            func<float>(3);
            则按照上面的分析，先根据func<float>，确定T1类型为float，
            T2类型未决，继承根据调用函数的实参进行推测，
            但看函数定义可以知道，根据函数实参退出来的也是T1的类型，
            仍无法确定T2的类型，
            但函数体内又使用了T2类型，
            此时编译就会报错。
        另外，类模板不支持省略模板类型的语法。
    模板函数的默认模板参数
        在c++11中，模板函数可以可普通函数一样，带有默认的模板参数了。
        （附注：模板类的默认模板参数，则是从C++98就开始允许了的）
        template <typename T = int> class A {}   //c++98 c++11都可以编译通过
        template <typename T = int> void func() {}  //c++98会编译失败
        需注意的是，如果模板类有多个模板参数，要想为模板参数指定默认值，
        应该按“从右往左”的规则进行指定，即必须先为后面的类模板参数指定默认值。
        而这个规则条件，对指定模板函数的默认参数则不是必须的。
        例： template <typename T1=int,typename T2> class A{}   //报错
        template<typename T1=int,typename T2> void func() {}    //可以
        调用模板函数：
            template<class T1,class T2=int> void func(T1 t1=0, T2 t2=0);
            func(1,'c');         //编译器理解为 func<int,char>(1,'c');
            func(1);             //编译器理解为 func<int,int>(1,0);
            func();              //报错，编译器无法推导出T1模板参数是什么类型的
            func<int>();         //编译器理解为 func<int,int>(0,0);
            func<int,char>();    //编译器理解为func<int,char>(0,0);
            有一点需要说明一下，模板函数的默认形参（t1=0,t2=0）不作为模板参数的推导依据
            函数模板参数的类型判断，总是以函数的实参的类型来推导的
    模板函数之外部模板
        例如有个模板函数 template<typename T> void func(T t){}
        当a.c中使用了该模板函数 func(1);
        同时b.c中也使用该模板函数 func(2);
        编译器在编译a.c时，会在a.c中添加 void func(int t){}   //实例化模板
        编译器在编译b.c时，有会在b.c中添加 void func(int t){}
        可见，在a.c和b.c中，会有两份完全相同的func代码，造成了代码冗余
        编译器可能会进行智能优化，将这两份代码只记录一份，但这会增加编译链接时间，
        在c++11中，允许我们声明外部模板，就跟extern int i 声明外部变量一样:
        我们可以在a.c中使用 template void func<int>(int);
        就可在a.c中“显式地实例化”模板函数，这是c++98就支持的，
        而在b.c中，使用extern template void func<int>(int); 
        声明外部函数模板，这是c++11中加入的新特性。
        这样，编译器就可以很容易的控制func模板函数只生成一份实例代码了。
        附注：一般代码量不大的情况下，依赖编译器的优化就行了，无需特意使用外部模板声明，
        只有当代码量很大，使用模板函数很多，编译很耗时的项目时，才推荐使用外部模板声明。
    局部类型与匿名类型作模板实参
        c++98不允许匿名类/匿名对象、局部类/局部对象做模板参数
        c++11取消了这种限制
        例：
        template <typename T> void func(T t){};
        template <typename T> class X{}
        struct A{} a;        //全局类, 全局变量
        struct {} b;         //匿名类型变量
        typedef struct{} B;  //匿名类
        void test()
        {
            struct C{} c;    //局部类，局部变量
            X<A> x1;         //c++98，c++11都可以
            func(a);         //c++98，c++11都可以
            X<B> x2;         //c++98不行，c++11可以
            func(b);         //c++98不行，c++11可以
            X<C> x3;         //c++98不行，c++11可以
            func(c);         //c++98不行，c++11可以
        }
构造函数  '关键字：using，继承构造函数，委派构造函数
    c++98的烦恼
        一：费事的构造函数
            假设A中有好几种构造函数，B继承A
            则B的实例是无法直接使用A类的各种构造函数的
            只能是B提供相应个数的构造函数，
            通过初始化列表的方法，调用A的相应构造函数
        二：多管闲事的重写函数
            假设A中有好几种函数func，这些函数的名字一样，参数不同
            如果B中重写了这个函数func，则B中就没法再用A中的各种func了
    c++98的解决方案：using
        其实针对上面第二种问题，c++98就有解决方案，即使用using A::func;
        这样，在B类中就能使用A类中的各种func函数了。
    c++11的解决方案：继承构造函数
        c++11把using功能扩展到构造函数上了：子类可以使用using声明继承基类的构造函数
        方法： using A::A;  //这在c++98中不会报错，但也不起作用
        不过使用继承构造函数，有个问题，就是没法对B中的成员进行初始化，
        但我们可以使用“就地声明”来配合解决此问题。
        例：
            class A
            {
            public:
                int i,j;
                std::string s;
                A(int a):i(a),j(12),s("abc"){}
                void speak() { printf("i=%d,j=%d,s=%s\n",i,j,s.c_str()); }
            };
            class B:public A
            {
            public:
                using A::A;  //或者使用委派构造函数：B(int a) : A(a) {}
                using A::speak;
                void speak(std::string s) { cout<<s<<endl; }
            };
            int main()
            {
                B b(5);      //如果没有 using A::A;     就会报错
                b.speak();   //如果没有 using A::speak; 就会报错
            }
        注意：B中使用了A::A，并不一定就会真正继承A中的所有构造函数，
        而是编译器发现当需要某个构造函数时，才为其添加该构造函数。
        另外，如果
    c++11的其它解决方案：委派构造函数
        委派构造函数的思想就是某个构造函数只完成部分工作，
        其它工作通过调用另一个构造函数来完成，
        如：
            class A {
              public:
                A() { puts("construct A"); }
                A(int i) _val(i) { A(); }  
                int _val;
            }
        像上例中这样，在A(int i)构造函数中，把剩余工作委派给A()构造函数，
        这样会减少一些构造函数的书写操作，但可惜这样的用法在C++中是不允许的，
        但在c++11中，有办法达到同样的功能：A(int i) : A() { _val = i; }
        在这里，我们把被调用的A()称为目标构造函数，把A(int i)称为委派构造函数
        这里的委派，指当前构造函数把一部分活委派给其它构造函数(目标构造函数)了
        注意：
            构造函数不能同时“委派”和使用初始化列表
            委派构造函数因为使用了“委派”，所以就不能再有初始化列表了，
            这时只能在函数体中完成对相关类成员的赋值
            但被委派的构造构造函数则既可以使用初始化列表、
            也可以使用“委派”，只要不是同时使用这两者就行。
        使用这种“委派构造函数”的方式来精简构造函数代码时，
        建议把最为“通用”的代码抽离出来，作为目标构造函数
        甚至可以使用模板函数作为目标构造函数，从而使目标构造函数更“通用”
        另外需要说明的是，初始化列表或委派构造函数，总是优先于{函数体}执行的
左值、右值与右值引用  '关键字：移动构造函数，右值引用，左值、纯右值、将亡值
    函数返回对象类型时的讨论
        如 string func() { string s="abc"; return s; }   string s2 = func();
        函数在返回s时，会先产生一个临时变量s`，作为作为待返回对象，
        这个临时变量s`的创建，则会触发一次拷贝构造函数，之后析构s，
        再之后将s`赋值给s2，然后s`调用析构函数。
        可见这个临时变量s`会消费一次构造和析构函数，
        如果这个构造/析构函数很费时间，如涉及大内存的分配与释放、读文件等，
        则会造成不必要的浪费。
        类似的,当对象类似作为函数参数时，也有同样的问题。
        注：用qt5.9 Debug测试，没调拷贝构造或赋值函数，说明代码还是被优化了。
        c++11基于此，提出右值的概念，一定程度上可以缓解如上问题。
    判断方法1：等号判断法
        int i=1,j=2,k=3;
        i = j+k;
        k = i;
        一个典型的判断左值与右值的方法是，看其在等号的左边还是右边，
        在这层意义上，i=j+k中，i为左值，j+k为右值， k=i中，k为左值，i为右值
        (理解：能被=赋值的，是左值，不能被=赋值的是右值)
    判断方法2：有名取址判断法
        另一个被广泛认同的判断方法是，如果是可以取地址的、有名字的，就是左值，
        反之，就是右值。如果按照这种判断方法，只要是等号左边的，肯定是符合左值的标准的，
        但等号右边的，却不一定就是右值，如i=j+k中，i有名字（i），可以取值（&i）,
        所以i是左值，j+k没有一个名字，也不可以取值（&(b+c)是编译不过的），
        所以j+k是右值，但k=i中，k是左值，而i却不符合右值的条件。
        （理解：真正占用内存空间的变量是左值）
    进一步讲，右值又分为两种类型：将亡值、纯右值
        □□纯右值是c++98中提出的概念，如一个函数返回一个对象类型，返回的这个对象就是纯右值，
        一些运算表达式，如上面的j+k，又如1+3, 产生的临时变量，也是纯右值，
        字面量值，如2、'c'、true等，也是纯右值，
        类型转换函数的返回值、lambda表达式等，也都是纯右值。
        □□将亡值是c++11引入的概念，它是跟"右值引用"相关的表达式，
        该表达式通常是将要移为它用的对象，
        如返回类型为T&&的函数的返回值，std::move的返回值，T&&类型转换函数的返回值等，
        如一个函数，返回 T&& 类型，
        表示该表达式返回的是将要被移动（移为它用）的值，这样的值称为将亡值。
    右值引用：
        T func() { T t; return t; }
        T && a = func();
        这里func()返回了一个右值，而a则为右值引用，其引用的是func函数返回的临时变量。
        为了区分c++98中的引用类型，可将之前的引用，称为左值引用。
        共同点： 都必须立即初始化。
        区别：左值引用是具名变量的别名，右值引用是不具名变量（匿名变量）的别名
        在T && a = func();中，本来func()返回的右值（临时变量）在表达式结束后，
        该临时变量也就自动终结了，但通过右值引用的声明，使得该右值“重获新生”，
        只要该右值引用a还“活着”，则func返回的右值，就会一直存在。
        注意：
            右值引用，引用的得是右值才行，如int a; int && b = a; 这是不行的，
            因为a不是个右值，但 int && b = a+2; 这是可以的， a+2是个右值。
        那上面的T && a = func();  如果写为 T & a = func(); 是否可以呢？ 
        答案是编译时会报错，但如果写为 const T & a = func()；就不会报错。
        这是因为，在c++98中，"常量左值引用" 就是个万能的类型，
        它在这里等同于"常量右值引用"。而(非常量)右值引用则可以对引用的对象进行修改。
        另一个例子： const int & i = 3;  这在c++98中是常见的，
        但其实，这也是个"常量左值引用" 引用"右值"的例子。
        再一个例子：void f(const T & t) { ... }  f(func());
        这在c++98中也是可以正常编译的，而这里的参数t,就是"常量左值引用" 引用func返回的"右值"
        最后的这两个例子，按c++11的用法，则可以写为：
        int && i = 3;
        void f(T && t) {...} f(func());
    移动构造函数：
        定义
            进一步，如果把拷贝构造函数 A(A &a) { ... } 变为
            A(A && a) { ... } ，则称为移动构造函数
            移动构造函数的精髓就是把参数a对象的指针成员指向的内存直接挪为己用，
            并把a中相应的指针成员设置为nullptr。
            不用担心a在析构时，delete空指针的问题，因为c++11中允许delete空指针了。
        什么情况下考虑使用移动构造函数：
            移动构造函数主要适用于成员变量中有指针类型，且指向的数据比较庞大时，
            此时在移动构造函数的函数体中，可以直接 _ptr = a._ptr; a._ptr = NULL;
            不用担心a.ptr赋值为NULL后，a在析构时，如果delete _ptr; 因引发崩溃，
            经测：char*p = NULL;delete p; 在vs2008中会运行出错(vs2008不支持移动构造)
            在vs2015中正常执行，不会崩溃，可见在c++11中，为了配合移动构造函数的功能，
            已经允许delete空指针了。
        与常量左值引用作构造函数参数的区别：
            使用常量左值引用 A(const A &a){ ... }，有时也能起到替代效果，
            但这意味着这里的a是不可修改的，所以也就无法将a中的指针成员设置为NULL，
            所以它不能取代右值引用。
            A(const A & a); 这是构造函数的常量左值引用版本，
            该构造函数会被当做拷贝构造函数使用，
            而A(A &&a)；才会被用作移动构造函数。
        std::move(..)
            使用该函数，可以强制把一个左值转化为右值，
            如 A a; A && a2 = std::move(a);
            '''这里就把a变为右值，从而可以赋值有右值引用类型的a2，
            之后，a和a2都是可以正常使用的，且上面步骤不会引发移动构造函数，
            再继续试验 A a3 = a; 和 A a4 = std::move(a);
            前句会引发拷贝构造函数，后句会引发移动构造函数，
            移动构造函数执行完后，因为A的移动构造函数会释放a中的指针成员，
            所以会导致之后无法再使用a中的指针成员变量。'''
            经在vs2015中测试，上述语句不会引发移动构造函数，
            ----因为a2不是个真实对象，而只是个引用，所以不会引发构造函数。
            也没有引起a的析构，a在这之后仍可以正常使用，
            所以上面的效果就跟使用左值引用一样。
            如果把上面代码改为A a; A a2 = std::move(a);
            则会引发移动构造函数，且这之后a不能再使用在移动构造函数中被“移动”的成员。
            另外如 A f() { A a; return a;} A&& a3 = f(); 也会引发移动构造函数。
            总结：
                std::move(a)，本身不会对a的使用产生任何的影响，
                a仍可以正常使用，包括修改和访问成员变量等。
                但std::move()的返回类型为右值类型，
                这意味着 T a2 = std::move(a),将会触发移动构造函数，
                所以之后就不能正常访问a中的指针成员了，但其它成员变量仍可正常使用。
        什么时候会触发移动构造函数的调用：
            当类中同时包含拷贝构造函数和移动构造函数时，如果使用临时对象初始化当前类的对象，
            编译器会优先调用移动构造函数来完成此操作。
            只有当类中没有合适的移动构造函数时，编译器才会退而求其次，调用拷贝构造函数。
    默认构造函数：
        默认编译器会为类隐式的生成移动构造函数（意味着不使用就不生成）
        如果如果主动声明了拷贝构造函数、拷贝赋值函数、移动赋值函数、
        析构函数中的一个或多个，编译器都不会再隐式生成默认版本的构造函数。
        默认的移动构造函数，跟默认的拷贝构造函数一样，只做一些按位拷贝的工作，
        这通常是不够的（至少需要把原对象的相关指针置空），
        所以通常有需要时，必须自定义实现移动构造函数。
变量初始化赋值  '关键字：变量名{}
    c++98就有的初始化列表方式: 如 int arr[3] = {1,2,3};
    c++11引入的新初始化列表方式：
        使用变量名后面紧跟{}，完成变量初始化的方式，是c++11新引入的，
        这种变量初始化方式不仅可以用来完成类成员变量的就地初始化，
        还能用于完成普通变量（非类成员变量）的初始化。
        int arr[] = {1,2,3};          //c++98和c++11均编译通过
        int arr[]{1,2,3};             //c++11特有
        std::vector<int> vec{1,2,3};  //c++11特有
        std::map<int,std::string> 
            m{{0,"张三"},{1,"李四"}}; //c++11特有
        std::map<int,std::string> 
            m={{0,"张三"},{1,"李四"}};//c++11特有
        int * p = new int(1);         //c++98和c++11均编译通过
        int * p2 = new int{2};        //c++11特有
        vector<int> func() {return {1,3}; }  //c++11特有
        class D
        {
          public:
            D(int i,int j,int k,C c)
            {
                _i=i;
                _j = j;
                _k = k;
            }
            int _i,_j,_k;
            void speak()
            {
                printf("%d,%d,%d\n",_i,_j,_k);
            }
        };
        D d{1,2,3};                   //c++11特有
    让自定义函数或自定义类的构造函数支持“初始化列表”形式的参数
        #include <initializer_list>
        void myprint(initializer_list<int> arr)
        {
            auto i = arr.begin();
            for(; i != arr.end(); i++)
                printf("%d\t",*i);
        }
        myprint({1,2,3,4});   //qt5.9测试，把initializer_list换成list，效果相同
        class A
        {
        public:
            A(initializer_list<pair<int,std::string>> lst)
            {
                auto i = lst.begin();
                for(; i != lst.end; i++)
                    _vec.push_back(*i);
            }
        private:
            std::vector<pair<int,std::string>> _vec;
        }
        A a = {{1,"aaa"},{2,"bbb"},{3,"ccc"}}; 
        A b{{1,"aaa"},{2,"bbb"},{3,"ccc"}};
    初始化列表赋值方式，可以应对“数据类型收窄”
        如 int i = 1.2; double d=3; int j=d; 等等
        上面发生的这些隐式转换，都会使得数据长度发生变化，或精度丢失，
        而如果使用初始化列表赋值的方式时，编译器会检查是否发生类型收窄，
        如果发现，会编译报错（但经vs2015测试，这种检查机制还有待优化）
        另注：圆括号方式不会检查，大括号方式才会检查
        	int arr[] = { 1.1 , 2.1 , 3.1 };    //编译成功
            int arr2[]{ 1.1 , 2.1 , 3.1 };      //编译成功
            int aa = { 3.3 };                   //编译报错
            int bb{ 3.3 };                      //编译报错
            int cc(3.3);                        //编译成功
POD类型（plain old data）  '关键字：与C兼容
    名词解释
        POD类型是C++中常见的概念，用来说明类/结构体的属性，
        具体来说它是指没有使用面相对象的思想来设计的类/结构体。
        POD的全称是Plain Old Data，
        Plain表明它是一个普通的类型，没有虚函数虚继承等特性；
        Old表明它与C中的结构体完全兼容。
        POD类型在C++中有两个独立的特性：
        支持静态初始化（static initialization）
        拥有和C语言一样的内存布局（memory layout）
        现在提起POD类型通常是指有这两个特性的类，
        且这个类的非静态成员也是POD类型。
    用途：
        1. 可以安全的使用memset、memcpy，对POD类型数据进行操作
        2. 因为与C内存布局兼容，所以c++程序可以忽c函数进行互操作
用户自定义字面量  '关键字： 重载""运算符，""运算符参数形式
    对于内置类型： 如 整形、布尔型、字符型、字符串等
    编译器会自动根据“字面量”，识别出是什么类型，
    如true,1,"abc"，会相应识别为布尔、整数型、字符串，
    但我们有时还希望编译器可以将特定的字面量识别为我们自定义的类型
    如我们自定义一个class Weight; 
    希望把 50kg，60g 这样的值，自动匹配识别为Weight类型
    c++11使这种愿望变成了现实：
    通过重载""运算符函数：
    Weight operator "" _kg (unsigned long long v) {
        return { (unsigned int)v };  }
    就可这样使用了： Weight w = 32_kg;
    注意：
    1. 该函数不能是类的成员函数
    2. "" 和后缀(_kg)之间要有空格隔开
    3. 后缀推荐以_开头，不成文约定，否则可能跟23L这样的混淆
    4. ""运算符参数形式只能有如下几种：
       T operator "" _xx (unsigned long long v);    # T t=13_xx;
       T operator "" _xx (long double v);    # T t=13.2_xx;
       T operator "" _xx (const char* p);    # T t=8字节表示不了的数xx;
       T operator "" _xx (const char* p,size_t n);  # T t="13"_xx;
定义类型别名  '关键字： using、为模板定义别名
    在c++98中，一般用typedef定义类型别名
    在c++11中，using也具有了这种能力，与typedef效果相同
    typedef unsinged int uint;
    using uint32 = unsigned int;
    int main() {
        cout << is_same<uint,uint32>::value <<endl;  //输出 1
    }  //is_samve是个c++11提供的模板函数，用以判断两个类型是否一致
    之所以在有typedef的基础上，又引入了using语法，
    是因为它在有时比使用typedef更灵活、更简洁明了，
    更特别的时，在为模板定义别名时，如：
    template<typename T> 
    using MapString = std::map<T,char*>;
    MapString<int> aaa;
    这里我们将std::map<T,char*> 等价为 MapString，就像宏一样，
    然后可以对MapString进行实例化，这是用typedef别名做不到的
对右尖括号>的改进  '关键字：两个连续的>>，C++98有时会无法编译通过
    在c++98中，两个连续的>>，中间没有空格，通常会优先解释为右移符号，
    如 static_cast<vector<int>>(vec);   //无法编译通过
    在c++11中，编译器会更智能，能正确识别上面代码，不会报错
auto类型  '关键字： auto变量要初始化赋值
    像如vb、js、python、perl等，使用变量时，可以无需预先声明，
    程序在运行时，自动根据赋给变量的值的特点，推断出变量类型，
    这种类型推导，主要发生在运行阶段，事实上，在编译阶段，
    也完全可以使用这种类型推导技术，而c++11就引入了这种技术。
    如果一个变量声明为auto类型，并确保在声明auto变量时，
    对变量进行初始化赋值，这样，编译器就能只能推断该变量类型。
    (先声明auto变量，正常再对其进行赋值使用，编译时会报错.
    从这个意义上讲，auto并不是一种类型，而只是一个类型的占位符
    在编译时，会把auto替换为变量实际的类型)
    auto关键字的历史
        事实上，auto不是c++11新引入的关键字，而是在c++98中就有了
        在98中，auto表示的具有自动存储期的局部变量，所有的局部变量
        如果没有static修饰，都默认是auto类型的，
        所以绝大多数的代码，声明局部变量时，并不会特意指明auto关键字，
        所以c++11对auto关键字进行了重定义，auto不再表示自定存储期语义
    auto的优势
        在声明迭代器指针时，使用auto会很方便，如:
            std::list<int> lst;  
            for(auto iter=lst.begin(); iter != lst.end(); i++) { ... }
        auto在一定程度上，支持泛型编程，如：
            template<typename T1,typename T2>
            float sum(T1 &t1, T2 &t2) {
                auto s = t1+t2;
                return s;
            }
            如果T1为int，T2为long，则auto自动推导为long
            如果T1为float，T2为double，则auto自动推导为double
            但因为函数返回值类型的限制，所以auto的效果有限。
         auto的使用限制
            auto不能用于声明函数参数类型
            auto不能用于声明数组
            auto不能用于声明类的非静态成员变量（即使就地初始化也不行）
            可以用valatile，pointer（*），reference（&），rvalue reference（&&） 来修饰auto
            用auto声明的变量必须初始化
            auto不能与其他类型组合连用
            函数和模板参数不能被声明为auto
            定义在堆上的变量，使用了auto的表达式必须被初始化
            因为auto是一个占位符，并不是一个他自己的类型，因此不能用于类型转换或其他一些操作，如sizeof和typeid
            定义在一个auto序列的变量必须始终推导成同一类型
                auto x1 = 5, x2 = 5.0, x3='r'; 错误，必须是初始化为同一类型</span>
            auto不能自动推导成CV-qualifiers (constant & volatile qualifiers)
            auto会退化成指向数组的指针，除非被声明为引用
运行时类型识别(RTTI)  '关键字： type_info类，typeid运算符
    c++98就开始支持RTTI了，
    RTTI机制为每个类型，产生一个相应的type_info类型的数据（不包括模板类型）
    class type_info {
    public:
        _CRTIMP const char* name() const;   //人类可读
        _CRTIMP bool operator==(const type_info& rhs) const;
        _CRTIMP bool operator!=(const type_info& rhs) const;
        _CRTIMP virtual ~type_info();
        _CRTIMP const char* raw_name() const;   //人类不可读
        _CRTIMP int before(const type_info& rhs) const;
    };
    使用typeid运算符，就会返回变量相应的type_info数据（的引用）
    经测，typeid的参数还可以是常量，如typeid(3).name()也是可以的。
    type_info中有用的就是前三个函数，如: typeid(int).name();
    c++11为type_info类添加了unsigned int hash_code()成员函数。
    dynamic_cast的转换也是依赖于RTTI的，
    不过由于RTTI会带来运行时的开销，所以一些编译器支持将其关闭。
decltype  '关键字： decltype(i) j = 0;
    decl_type运算符的出现目的，一定程度上与auto的目的是一致的，
    就是希望编译器在编译时，自动识别数据类型，
    猜测：decltype应该是根据typeid(变量),得到该变量的类型信息
    tecl_type的用法：
        int i;
        decltype(i) j = 0;  //int
        float a;
        double b;
        decltype(a+b) c;    //double
追踪返回类型  '关键字： 返回类型后置，auto,->decltype()
    追踪返回类型是c++11引入的新语法
    我们希望c++11可以这样： 
    decltype(t1+t2) sum(T1 t1,T2 t2)
    {   return t1+t2; }
    但编译器却不允许这样做，编译器在推导decl_type(t1+t2)时，
    表达式中的t1和t2都未声明，编译时，编译器只能从左到右地
    读入符号，所以decl_type(t1+t2)只能出现在t1,t2的定义之后
    为此，c++11引入新的定义函数返回值类型的语法：
    auto sum(T1 t1,T2 t2) -> decltype(t1+t2)
    {   return t1+t2; }
    auto 和 -> 返回数据类型，
    构成了“追踪返回类型”函数的两个的两个基本元素
    所以，按这种语法：
    int func(char *p) 可写为 auto func(char* p) -> int
    追踪返回类型还可以用在函数指针的声明中：
    int (*pfunc)(); 可写为 auto (*pfunc)() -> int;
    追踪返回类型感觉还是主要用于模板函数的返回值。
基于范围的for循环 '关键字： for( : ), 此种用法，stl容器迭代的是引用而不是指针
    c++11新增
    int arr[5] = {1,2,3,4,5};
    for(int &e : arr) e *= 2;
    for后面的括号内，由冒号分成了两部分，
    第一部分是迭代变量，第二部分是被迭代范围
    用这种方法，遍历数组和stl容器会方便很多。
    上面的for循环，跟普通的for循环一样，
    内部可以使用continue、break等控制字。
    自定义容器类也可以支持上面的语法形式，但需要满足如下条件：
    1. 有begin()、end()函数
    2. 迭代对象支持++和==操作
    注意，如果遍历数组，前提不需数组的大小已知，
    如 void func(int a[]) { for (auto e : a) cout << e; }
    是不对的，因为a的大小不确定。
    注意2，如果是遍历stl容器，且使用auto声明迭代对象时，
    此时的auto不是迭代器指针类型，而是迭代器指针的解引用形式：
    vector<int> v = {1,2,3,4,5};
    for(auto &e:v) e *= 2;  //e前面不要带*（不要写为*e *= 2）
    //理解：e是元素的引用，而不是元素的指针
枚举类型、枚举类 '关键字： enum class 类名
    c/c++的enum有个很奇怪的设定，就是enum类型的成员，不需要加
    所在枚举类型的名字的限定，即可直接使用。
    这就与namespace、class、struct、union等，
    必须通过"名字::成员名"访问的特性有些格格不入。
    针对枚举类型的缺点，c++11引入了一种新的枚举类型，称为枚举类
    又称强枚举类型， enum class 类名 {成员1,成员2,...,成员n};
    或enum struct 类名 {成员1,成员2,...,成员n}; 两者效果等价。
    用这种方式声明的枚举类型，
    1. 要使用枚举成员，必须带上类名限定符
    2. 不能和整形隐式的相互转换
    3. 可以指定成员的类型，方法是在类名后面加":type",默认int
       type可以是wchar_t外的任何整形，如char、DWORD、long等
    对原有枚举类型enum的改进
    1. 原有enum 的类型名后面也支持":type"形式
    2. enum的成员，既可以直接使用，可以看加enum类型名限定
智能指针 '关键字： unique_ptr、shared_ptr、weak_ptr、make_unique,make_shared
    在c++98中使用模板类型auto_ptr实现智能指针，如auto_ptr(new int)
    不过auto_ptr有一些缺点，如atuo_ptr(new int[3])是不行的，
    因为auto_ptr不能调用delete[]，一个auto_ptr指针赋值给另一个指针时，
    原来的指针自动变为不可用。
    c++11中废弃了auto_ptr，改用unique_ptr/shared_ptr/weak_ptr等来管理对象
    需要引用<memory>头文件。
    这些指针都重载了*运算符
    智能指针等号运算符不支持*指针赋值，构造函数可以接受*指针参数
    智能指针重载了=、==、!=、比较、->、*等运算符。
    应该养成使用指针指针对象的习惯，尽量避免使用*指针。
    unique_ptr
        不能和其它指针共同指向同一块对象内存(不支持复制)，如：
        unique_ptr<int> p1(new int(11));
        unique_ptr<int> p2 = p1;  //不支持拷贝构造函数，编译报错
        unique_ptr<int> p3 = std::move(p1);   //支持移动构造函数
        另外，智能指针可以接受对象的地址，如：
        A a;  unique_ptr<A> up1(&a);
        不用担心智能指针析构时的内存释放问题，可以测试：
        int i=3; int *pi = &i; delete(pi); 
        可以发现代码可以正常执行，且执行后，查看pi的值，仍为3
        要注意的是，这是在qt5.9中测试的，在vs2005中执行有问题。
        //-Note : p1只能指针内部维护了一个指针，指针真正的数据，
        //移动构造函数会挪用该内部指针
        //p3变为新的唯一指针，之后不能再使用p1了，否则运行时错误
        如果指针指向数组，使用方式为 unique_ptr<T[]> p，
        此时可通过 p[下标] 方式访问数组成员。
        此种情况下，p内部有个 T[] *_ptr 类型的成员变量，
        等同于 T** _ptr, 相当于一个二级指针。
        -MARK ： 这里不理解了
    shared_ptr
        内部实现了引用计数，可以多个指针指向同一个对象
        shared_ptr智能指针对象内部有个类似于 int * pref的成员变量，
        在构造时，会 pref = new int;
        然后当这个智能指针被赋值时，会 (*pref)++ , 析构时会(*pref)--
        int * p = new int(3);
        shared_ptr<int> ptr1(p);
        shared_ptr<int> ptr2(p);
        这段代码会引起崩溃，因为 ptr1 的构造，当构造参数为int*时，
        除了 pref = new int外，还会 (*pref)=1 ，这使得它在析构时会释放p内存
        而ptr2也会有同样的处理，所以会造成对p内存的两次释放，而引发崩溃。
        那这是不是说明，使用shared_ptr也不安全，会引起崩溃呢？
        不是的，其实，上面这段代码的不安全，根本原因是对int*的使用，
        这个int*才是不安全的根源，如果没有它，就可以完全放心的使用shared_ptr
        shared_ptr<int> ptr1(new int(3)); 
        shared_ptr<int> ptr2(ptr1);
        这样写，就完全没问题，ptr2的构造，当参数也是shared_ptr时，
        不会重新进行 pref = new int操作，而是两者公用一个pref，此时pref的值为2
        当shared_ptr析构时，会先 (*pref)--，然后看pref是否为0了，为0，
        才delete所引用的内存资源，所以ptr1/ptr2中的第一个的析构，
        只会是pref的值从2变为1，之后第二个析构时，才会真正释放指向的内存资源。
    weak_ptr
        weak_ptr只能被shared_ptr赋值，或者并另一个weak_ptr赋值(其实本质还是
        被shared_ptr赋值)。
        它可以指向shared_ptr指针指向的对象内存，却不拥有该内存（没有引用计数）
        调用成员lock()，则可返回一个新的shared_ptr对象，
        如果weak_ptr所指的对象内存变化无效，lock()会返回一个空指针，
        利用这一特性，可以用来动态检查内存块是否已经变得无效。
        上面讲了shared_ptr内部会有一个 int *pref引用计数，记录有多少个shared_ptr
        指向着同一个堆内存，其实，shared_ptr内部还有一个 int *pref2引用计数，
        它记录着另外有多少个weak_ptr，指向该堆内存。
        weak_ptr既没有重载*运算符，也没有重载->运算符，所以无法用weak_ptr访问堆内存
        weak_ptr只算是shared_ptr的一个暂存器，要使用时，应该使用其lock()方法，
        该lock方法会临时的得到一个shared_ptr(使pref计数+1)，
        之后又立即释放该shared_ptr（使pref计数-1），如:
        shared_ptr<int> pi(new int(3));
        weak_ptr<int> wpi(pi);
        *wpi.lock()++;   //int的值变为4
        shared_ptr<int> pi2(wpi.lock());  //等同于 pi2(pi)
    有了shared_ptr，为什么还要再引入weak_ptr概念？
        这是因为，shared_ptr在一种特殊情况下（环形引用），仍会引起内存泄漏：
        参：file://shared_ptr环形引用问题.png
        shared_ptr<A> pa(new A);
        shared_ptr<B> pb(new B);
        pa->_pb = pb;  // A里面有个 shared_ptr<B> _pb 成员变量
        pb->_pa = pa;  // B里面有个 shared_ptr<A> _pa 成员变量
        可知，这种情况下， pa的引用计数和pb的引用计数都是2，
        所以这时，pa，pb两个智能指针对象析构时，都不会真正释放new A堆和new B堆
        而这两个堆不释放，其内的成员变量 _pa，_pb，自然也不会被释放，
        最终造成内存泄漏。
        正是因为这个缺陷，所以才又引入的weak_ptr。
        针对本例中的情形，假设我们一定要使用上面这种（互相引用/环形引用）结构，
        而又不想将A中的成员shared_ptr<B> _pb 换成 B* _pb的形式
        （应该在代码中彻底杜绝使用B* 这种老式的指针声明方式），
        这时，就可以选用weak_ptr<B> _pb;  这样，就不会有上面的内存泄漏问题了。
    make_unique,make_shared 
        -Note : make_unique是c++14才引入的，gcc最小支持版本为6.1
        如果使用 shared_ptr<int> pi(new int(3)); 这种形式，
        则需要在pi构造时，为上面讲到的pref，pref2另外申请内存，
        这种情况下，很明显的，new int(3)堆内存和pref,pref2指向的内存是不在一块儿的
        而如果用make_shared(或make_unique)，就可以做到一次申请足够的空间（12字节），
        既能存放new int(3)（占4字节）,又能存放pref和pref2指向的内存（分别占4字节）。
        所以这种方式，效率更高，而且内存更紧凑（一定程度减小内存碎片）。
        所以推荐使用make_unique,make_shared这种方式得到unique_ptr或shared_ptr。
        -Note: make_unique<typename T>()，取代 new T(), 代码中不出现new
        使用举例：
            class Animal
            {
            private:
                std::wstring genus;
                std::wstring species;
                int age;
                double weight;
            public:
                Animal(const wstring&, const wstring&, int, double){/*...*/ }
                Animal(){}
            };
            void MakeAnimals()
            {
                //使用默认构造函数
                unique_ptr<Animal> p1 = make_unique<Animal>();  
                //使用带参构造函数
                auto p2 = make_unique<Animal>(L"Felis", L"Catus", 12, 16.5);  
                //p3 指向Animal数组，数组长度为5
                //-MARK: 这里是不是相当于声明的指针数组？
                unique_ptr<Animal[]> p3 = make_unique<Animal[]>(5);
                //数组成员赋值
                p3[0] = Animal(L"Rattus", L"norvegicus", 3, 2.1);
                p3[1] = Animal(L"Corynorhinus", L"townsendii", 4, 1.08);
                // auto p4 = p2; //C2280
                vector<unique_ptr<Animal>> vec;
                // vec.push_back(p2); //C2280
                // vector<unique_ptr<Animal>> vec2 = vec; // C2280
                // OK. p2 no longer points to anything
                vec.push_back(std::move(p2)); 
                // unique_ptr overloads operator bool
                wcout << boolalpha << (p2 == false) << endl; // Prints "true"
                // OK but now you have two pointers to the same memory location
                Animal* pAnimal = p2.get();
                // OK. p2 no longer points to anything
                Animal* p5 = p2.release();
            }
            //当你看到带unique_ptr的连接错误C2280，几乎可以肯定，
            //因为你正试图调用它的拷贝构造函数，这是一个已删除的功能。
    智能指针指向数组
        https://blog.csdn.net/weixin_43705457/article/details/97617676
        默认的智能指针时不能指向数组的，
        因为只能指针的析构中，使用delete删除，而不是delete[]，
        但我们可以在创建只能指针时，为其指定内存删除函数，从而使其可以支持数组
        例:
            bool del(int *p) { delete[] p; }
            shared_ptr<int> p(new int[5],del);
            shared_ptr<int> p2(new int[5],[](int* p){delete[] p});
        而智能指针也没有重载下标运算符，
        所以我们也不能像数组一样使用下标方式访问智能指针指向的数组元素，
        所以只能用智能指针的get()方法，得到数组的真实地址，再去访问数组元素。
    智能指针的类型转换
        https://blog.csdn.net/wei_qifan/article/details/50889184
        在编写基于虚函数的多态代码时，指针的类型转换很有用，
        比如把一个基类指针转型为一个子类指针或者反过来。
        但是对于share_ptr不能使用诸如static_cast<T*>(p.get())的形式，
        这将导致转型后的指针无法再被shared_ptr正确管理。
        为了支持这样的用法，shared_ptr提供了类似的转型函数 ：
        static_pointer_cast<T>()、
        const_pointer_cast<T>()、
        dynamic_pointer_cast<T>()，
        它们与标准的转型操作符
        static_cast<T>()、const_cast<T>()、dynamic_cast<T>()
        类似，但返回的转型后的shared_ptr。
        举例：
        shared_ptr<std::exception> sp1(new bad_exception("error"));  
        shared_ptr<bad_exception> sp2 = dynamic_pointer_cast<bad_exception>(sp1);  
        shared_ptr<std::exception> sp3 = static_pointer_cast<std::exception>(sp2);  
        assert(sp3 == sp1); 
        注意，static_pointer_cast只适用于shared_ptr,不适用于unique_ptr，
        这是因为唯一指针如果支持类型转换，则该指针就不是唯一的了。
    unique_ptr和shared_ptr之间的转换
        https://www.coder.work/article/12866
        您可以轻松高效地转换 std::unique_ptr至 std::shared_ptr
        但您无法转换 std::shared_ptr至 std::unique_ptr 
        例如:
        std::unique_ptr<std::string> unique = std::make_unique<std::string>("test");
        std::shared_ptr<std::string> shared = std::move(unique);
        或:
        std::shared_ptr<std::string> shared = std::make_unique<std::string>("test");
常量表达式  '关键字： 暂不做详细介绍
    使用constexpr关键字
    使用举例：
    constexpr int get_size(int n) { return n*3; } //常量表达式函数
    constexpr int sz = get_size(2);               //常量表达式
    char arr[get_size(4)] = {0};                  //使用
    -Note: 以当前语句为根，如 get_size(4) 这一句，不用参照上下文，即可推出函数表达式的值
    主要利用编译期计算
    常量表达式猜测只会在编译期使用，不会出现在目标代码中
    而const int i=3; 这样的代码，会在静态存储区有相应数据，
    也就是说这样的代码是会影响目标代码的，而常量表达式不会。
    因未发现其使用优势（唯一优势就是编译期计算），所以暂不做详细介绍。    
变长模板参数  '关键字： 模板参数包、解包、偏特化类、全特化类
    c++98的函数就支持变长参数了
    c99中，宏参数也开始支持变长参数了
    c++11中，支持了c99中的变长宏参数
    c++11中，新增支持了变长模板参数
    变长模板参数的语法：
        template<typename ... TS>
        class B
        {
        public:
            B() { puts("B"); }
            void func();
        };
        TS前面的三个点，表明参数是变长的
        TS是随便起的名字，它被称为“模板参数包”，
        也就是说，它指代了前面N个变长参数
        使用时，TS... 表明对这个包展开，
        TS...的使用场合：
            ◆模板参数列表
            表达式
            初始化列表
            类成员初始化列表
            基类描述列表
            通用属性列表（后面会讲）
            lambda函数捕捉列表（后面会讲）
    从上面的语法中看出，这个TS，是无法像普通变量那样可以直接拿来使用的，
    而且也没有方法将TS包中的各个参数一个个提取出来，
    (使用sizeof...(TS)可以用来获知参数包中打包了几个参数),
    这样看来，虽然上面列出来多种使用场合，
    但都似乎华而不实或者说能到达的效果有限，
    无法实现 “模板类可以接受任意个数、任意类型的模板参数” 这样的诉求，
    之所以这样，其实是我们还没有找到一个好的方法，充分利用变长模板类的优势
    变长模板类的正确打开方式，是与偏特化结合使用(类支持偏特化,函数只支持全特化)：
        模板特化参：<file://../c++ 模板特化.txt>、<file://../c++ 特化与偏特化.txt>
        template<typename ... TS>
        class B
        {
        public:
            B() { puts("原始"); }
        };
        template<typename T1,typename ... TS>  //偏特化类(特殊用法)
        class B<T1, TS...> :public B<TS...>  //-Note:这里的public B<TS...>，要求原始类的存在，才有意义
        {
        public:
            B() { puts("偏特化"); }
        };
        template<typename T1>  //全特化类(特殊用法)
        class B<T1>
        {
        public:
            B() { puts("all special 1"); }
        };
        ''' 和上面的 template<typename T1> 二选一即可
        template<>  //全特化类(特殊用法)
        class B<>
        {
        public:
            B() { puts("特化"); }
        }; '''
        int main()
        {
            B<int,int,int,int> b;
            return 0;
        }
        说明：
        上面的第三个模板类，是原始模板类的一种特化情形，
        因为模板的参数是任意个的，这里是特化为0个模板参数
        分析：
        因为特化模板类比原始模板类优先被匹配，所以
        'B<int,char,bool,long>匹配偏特化模板类 
        class B<int,TS...> : public B<TS...>  
            'B<TS...>等价于B<char,bool,long>，匹配偏特化模板类
            B<char,TS...> : public B<TS...>     
                'B<TS...>等价于B<bool,long>，匹配偏特化模板类
                B<bool,TS...> : public B<TS...>   
                    'B<TS...>等价于B<long>，匹配偏特化模板类
                    B<long,TS...> : public B<TS...>   
                        'B<TS...>等价于B<>，匹配偏特化模板类
                        B<long> : public B<>
        可以看到，编译器会向上逐级查找匹配的基类构造函数，
        在先期匹配的时候，一直匹配的是偏特化的模板类，
        直到最后一个，匹配的是那个全特化的模板类
        原始模板类一直没有被匹配到，
        但该原始模板类却是不可或缺的，否则特化模板类就没有基础
        总结：
        通过配合特化模板类，达到了让变参模板类支持任意个数、任意类型参数的效果
    变长模板函数的使用
        变长模板类通常与类的偏特化结合使用，而函数模板是不支持偏特化的，
        该怎么办呢？其实，函数模板完全没必要使用偏特化，就可以使用变长模板函数，
        从另一个角度讲，因为类不能像函数一样直接使用变长模板的特性，所以才特意引入了偏特化
        使用变长模板函数的例子：
            template <typename T1, typename ...T2>
            void func(T1 t1, T2... t2)
            {
                cout << t1 << "\n";
                func(t2...);
            }
            template <typename T>  //属于函数重载
            void func(T t)
            {
                cout << t <<"\n";
            }
            int main()
            {
                func<char*,int,bool>("asdf",32,true);
                return 0;
            }
        可以看出func函数的两种重载形式，与前面例子中两个偏特化的类是想对应的，
        区别是上面的偏特化类又继承了原始模板类（其实根据优先匹配原则，等同于继承了自身类），
        而这里的第二个func函数，则是在内部又调用了自己。
    使用变长模板参数的局限性
        无论是变参模板类，还是变参模板函数，都没法一次性获取所有的参数，
        只能在每次递归构造或递归调用时，一次提取出一个参数。
        这意味着没法一次性同时处理(运算)多个参数，
        只能对一些没有相关关联的参数单独的进行处理。
多线程支持--原子类型与原子操作  '关键字： std::atomic<>、atomic_flag、自旋锁
    原子[数据]类型
        对原子类型的访问（读写），自动成为原子操作
        #include <cstdatomic> / #include <automic>
        包括的类型：
        atomic_bool、atomic_char、atomic_schar等等,
        除此之外，你还可以用atomic模板类 std::atomic<T> t;
        将任意类型包装为原子类型,实际上面列出的这些类型，
        都是使用std::atomic<>模板类包装出来的。
        你甚至可以用_Atomic关键字(C11中的)自定义原子类型，
        不过可惜目前各个编译器对C11中原子操作的支持都非常有限。
        注意：c++11不允许原子类型进行拷贝构造、移动构造及=赋值等，
        事实上，atomic模板类没有拷贝构造、移动构造、operator=等函数
        如：
            atomic<int> ai{12}; //ok  
            atomic<int> ai2{ai};  //fail，编译报错
        但是像如 atomic<float> t{1.2f};  float f = t; 是可以的。
        这实际等价于 float f = t.load(); 
        load()为atomic类的原子成员方法，所以可以避免其它线程对t的竞争
    原子操作
        c++11中将原子操作方法，都定义为atomic模板类的成员方法，
        这包括了绝大多数的典型原子操作，如读、写、交换等。
        例
            atomic<int> ai{12}; ai+=3;  
            这里的+=,实际是atomic提供的原子操作方法
        这些原子操作包括 +=、-=、!=、&=、^=、++、--、exchange、
        is_lock_free、load、store、clean、test_and_set、
        compare_exchange_weak、compare_exchange_strong等，
        但注意并不是所有的原子类型都支持以上所有方法，
        具体可参看《深入理解C++11:C++11新特性解析与应用》201页的表
    atomic_flag原子类型与自旋锁
        自旋锁
            简言之，自旋锁是相对于阻塞锁而言的，阻塞锁会引起线程的
            挂起与恢复，而这会引起内核态和用户态之间的切换，消耗不必要的时间
            自旋锁说白了就是 while( lock.try_lock() );
            当然这只是自旋锁的最简单应用情形，但可以说明自旋锁的特点了：
            自旋锁在得不到锁时，在本线程内循环等待，空等而不是阻塞，
            如果预料线程可能需要很长时间才能拿到这个锁，那自旋锁的线程
            空等的时间就会很长，超过线程挂起恢复的时间时，那使用阻塞锁
            就是比较划算的，而如果预料某个临界资源能很快得到锁，那自旋锁
            就是比较划算的选择，当然如下面那样的简单自旋锁有个很大的缺点，
            就是这是一种抢占式的锁，即当多个线程都在自旋等待时，不确定
            那个线程最终会抢到锁，从而可能导致某个线程一直抢不到锁，
            针对这种情形，可以将上面的自旋锁代码进行改进，得到有序自旋锁
            //-Note : "自旋"：当前语句循环执行（尝试拿到锁），而不是阻塞
            更详细内容参看https://www.cnblogs.com/cxuanBlog/p/11679883.html
        atomic_flag
            与前面的atomic_bool、atomic_char等原子数据类型不同，
            从实现上来看，它不是通过atomic<>模板类包装出来的，
            而是一个单独的类，从使用特点上来看，相比于之前这些类型，
            atomic_flag是无锁的，也就是说，对其进行读写时，
            不需要加锁，不加锁就意味着不会在得不到锁时而进入阻塞状态，
            所以，这是（唯一）一个真正意义上的"原子数据类型",
            '只有这种类型，才(仅)支持test_and_set()和clear()方法',
            利用它的这种特性，我们可以实现一个自旋锁：
            std::atomic_flag lock = ATOMIC_FLAG_INIT; //即赋值为0
            while( lock.test_and_set() )
            { (0);  }   //自旋，即循环尝试获得锁
            这里的test_and_set是一种原子操作，检测是否为假，
            如果为假，就设置为真，同时将旧值(假)返回；
            如果为真，就直接返回当前值(真)，并不改变其值。
线程局部存储TLS  '关键字： thread_local
    线程局部存储是个早已有之的概念
    不同的编译器有自己的TLS标准，
    g++/clang++/xmc++支持的声明线程变量的方式为:  __thread int error;
    声明为线程变量后，每个线程都拥有该变量的一个拷贝，
    从而使得一个线程对其线程变量的修改，不应影响到另一个线程的数据。
    c++11对TSL标准做了统一的规定： int thread_local error;
程序快速退出  '关键字：exit、析构、atexit注册的函数、quick_exit()、at_quick_exit()
    main函数结束，或者exit函数调用时，程序会自动退出，
    但这种退出方式，会自动将一些没释放的类进行释放，
    实际上，程序的堆内存在进程结束时，会由操作系统统一回收（效率高）
    所以通常在程序结束时，自动调用类的析构函数释放堆内存是无意义的。
    另外，在多线程时，用exit函数来退出的话，通常需要向线程发出一个信号，
    等待线程结束后，再进行必要对象析构，调用atexit注册的函数等，
    这在逻辑上是合理的，但实际上，可能并没有必要，
    我们可能希望像杀死进程一样退出程序。
    为此，c++11引入了quick_exit()函数，他直接结束程序，
    与abort不同的是，abort是异常退出，而quick_exit是正常退出。
    此外，使用at_quick_exit()，可以注册一些在quick_exit时调用的函数。
默认函数的控制  '关键字： =default、=delete、类禁止隐式转换的3中方式
    在C++中自定义的类，编译器会默认添加一些成员函数，包括：
        构造函数
        拷贝构造函数
        拷贝赋值函数（operator =）
        移动构造函数
        移动拷贝函数
        析构函数
    此外，编译器还会为这些自定义类提供默认的操作符函数（全局）
        operator,
        operator&
        operator&&
        operator*
        operator->
        operator->*
        operator new
        operator delete
    对于这些编译器默认添加的构造函数或操作符函数，
    c++11中，可以通过在函数声明后面加上=default或=delete
    显式的添加或删除这些函数。
    例如我们为一个类定义了一个带参构造函数，那编译器就不会再为
    这个自定义类添加默认无参构造函数了，但通过在该类中添加
    类名()=default; 这样，就可以让编译器为该类添加该默认无参构造函数
    再如，如果我们想让一个类不允许隐式转换，现在有3中方法能做到：
    法1. 使用explicit关键字修饰带参构造函数
    法2. 构造函数(T t) = delete; 这样可以禁止从t隐式转换成自定义类
    法3. 同法2类似，只不过是将构造函数(T t); 声明为私有且无需提供函数实现
内存字节对齐  '关键字： offsetof、alignof、alignas
    通过offsetof方法，可以查看成员变量的偏移位置（c++98就有）
    如struct A{char c; int i; }  int of = offsetof(A,i);  //of = 4
    在c++11中，我们可以通过alignof()函数来得到一个变量或类的对齐单位
    使用alignas修饰符，可重新指定类(/结构体/变量/成员变量)的对齐单位：
    struct alignas(32) B{double r; double g; double b; double a;}
    alignas既可接受常量表达式(2的幂次)，也可接受类型作为参数,如：
    alianas(double) char c;
    注意，虽然我们可以通过alignas重新指定对齐值，但这个值总是有限的，
    如果这个值超过了平台要求的最大值，则可能导致编译或运行时出现问题。
    另经测试，struct A{char c; int i;} 对A及其各个成员变量指定alignas(1)
    结果并没有起作用，alignof(A)的值始终为4
    //-MARK : 在qt5.9中测试，struct alignas(2) A { char a,b,c,d; } s;
    //alignof(s)==2 , sizeof(s.a)==1, sizeof(a)==4，说明alignas没起作用
    除了在声明时，使用alignas指定对齐外，还提供了std::align方法，
    //-Note : 需包含头文件<memory>  -MARK:经测试，没明白std::align的用法
    使用该函数，可以在运行时根据指定的对齐方式动态的调整数据块的位置。
    typedef std::size_t Size;
    void* align(Size alignment,Size size,void*& ptr,Size len);
    该函数将ptr指向的大小为len长度的内存，进行对齐方式的调整，
    将ptr开始的size大小的数据调整为按alignment对齐。
Unicode支持  '关键字： char16/32_t、u/U""、"\u"、"\U"、mbrtoc16/32、c16/32rtomb
    c++98为了支持Unicode，定义了“宽字符”类型wchar_t，
    但在windows中，多数wchar_t实现为2字节，而在Linux中，则被实现为4字节
    在c++98中规定，wchar_t的宽度由编译器实现，
    这导致了wchar_t相关代码的不可移植性。
    这一状况在c++11中得到了改善，c++11引入了如下两种新的内置数据类型：
    char16_t : 用于存储utf-16； char32_t ：用于存储utf-32;
    对于utf-8，使用现有的char存储即可。
    此外，c++11还定义了一些常量字符串的前缀（类似于L""）:
    u8表utf-8编码，u表utf-16编码，U表utf-32编码。
    通常，当连续书写多个字符串常量时，编译器会自动将其连接起来，
    如"a""b",和"ab"的效果是一样的，而当使用字符串编码前缀时，
    连写的多个字符串会按照第一个字符串的编码前缀进行拼接，
    如u"a""b",等价于u"ab"。
    另外，c++11还识别"\u4F60"（UTF-16）、"\U3F2A448E"（utf-32）
    书写格式。
    编码转换
        C11支持的编码转换函数包括:mbrtoc16、mbrtoc32、c16rtomb、
        c32rtomb,使用这些函数，需包含<cuchar>头文件。
        C++11对字符转换的支持稍复杂点。。。
原生字符串字面量 '关键字： R"()"、u8R"()"、uR"()"、UR"()"、字符串连写
    原生字符串使用户书写的字符串“所见即所得”。
    c++11支持按R"()"的方式书写原生字符串。
    如果想生成Unicode编码的原生字符串变量，
    只需写为 u8R"()"、uR"()"、UR"()"即可。
    注意，如果Unicode使用原生字符串，则反斜杠就不管用了，
    这意味着，不能用"\u4F60"这样的方式来表示Unicode字符了。
    另外，原生字符串也支持字符串连写，
    如 u8R"(hello )""word" 等价于 u8R"(hello word)"
typename用法  '关键字： 是类型而不是变量
    不是c++11才有的
    template<typename/class T>
    void foo()
    {
        typename T::iterator * iter;
    }
    T中的iterator，既可以是一种类型，也可以是T中的成员变量
    需要用typename，告诉编译器iterator是类型，而不是变量。
    std::forward通常是用于完美转发的，它会将输入的参数原封不动地传递到下一个函数中，
    这个“原封不动”指的是，如果输入的参数是左值，那么传递给下一个函数的参数的也是左值；
    如果输入的参数是右值，那么传递给下一个函数的参数的也是右值
typeof  '关键字： 根据变量声明类型，c语言已有、不保留引用信息
    typeof不是c++11中引入的语法，而是c语言已有的语法，
    参：https://blog.csdn.net/wichace/article/details/46809043
    两者之间的区别在于decltype始终将引用保留为信息的一部分，而typeof则可能不保留
    int a = 1;
    int& ra = a;
    typeof(a) b = 1;     // int
    typeof(ra) b2 = 1;   // int
    decltype(a) b3;      // int
    decltype(ra) b4 = a; // reference to int
    推荐使用decltype取代使用typeof
lambda表达式
    格式：[ capture ] ( params ) opt -> ret { body; };
        capture 是捕获列表，
        params  是参数表，
        opt     是函数选项，
        ret     是返回值类型，
        body    是函数体
    lambda各部分讲解
        capture捕获列表
            []          不捕获任何变量。
            [=]         捕获外部作用域中所有变量，并作为副本在函数体中使用（按值捕获）。
            [&]         捕获外部作用域中所有变量，并作为引用在函数体中使用（按引用捕获）。
            [bar]       按值捕获 bar 变量，同时不捕获其他变量。
            [=,&foo]    按值捕获外部作用域中所有变量，并按引用捕获 foo 变量。
            [this]      捕获 this 的目的是可以在 lamda 中使用当前类的成员函数和成员变量。
                        捕获当前类中的 this 指针，让 lambda 表达式拥有和当前类成员函数同样的访问权限。
                        如果已经使用了 & 或者 =，就默认添加此选项。
        params参数
            lambda 表达式在没有参数列表时，参数列表是可以省略的
        ret返回值
            C++11 中允许省略 lambda 表达式的返回值
            编译器就会根据 return 语句自动推导出返回值类型
    内涵
        lambda表达式的本质可以认为是个匿名函数
    备注
        1. lambda的执行
            单独存在的一个lambda表达式函数不会被执行，就像只是声明了该函数一样，
            如 [=] { cout << "abc" << endl; }; 出现在代码体中，不会输出 "abc"。
            但如果lambda后面加上([参数])，就相当于函数的调用了，则该函数会被执行，
            如 [=] { cout << "abc" << endl; }(); 出现在代码体中，会输出 "abc"。
        2. lambda的参数
           参数列表中不能有默认参数值，且不支持可变参数 
        3. 传this参数
           参数捕获方式[this]和[&]的效果是一样的，但使用的地方不同。
           使用[this]时，访问类成员也无需在前面加this->，直接使用成员变量即可。
           [this]用在类中，无法在类中参数捕获方式捕获成员变量，
           如类中有成员x，则在成员方法中写lambda时，捕获[x]报错：不认识该变量
           换成[this->x]也不行，只能用[this]或(参数)的方式得到。
           而在普通方法中，如main，则只能用[&]方式捕获参数。
    举例
        class A
        {
            public:
            int i_ = 0;
            void func(int x, int y)
            {
                auto x1 = []{ return i_; };                    // error，没有捕获外部变量
                auto x2 = [=]{ return i_ + x + y; };           // OK，捕获所有外部变量，暗含this
                auto x3 = [&]{ return i_ + x + y; };           // OK，捕获所有外部变量，暗含this
                auto x4 = [this]{ return i_; };                // OK，捕获this指针
                auto x5 = [this]{ return i_ + x + y; };        // error，没有捕获x、y
                auto x6 = [this, x, y]{ return i_ + x + y; };  // OK，捕获this指针、x、y
                auto x7 = [this]{ return i_++; };              // OK，捕获this指针，并修改成员的值
            }
        };
        int a = 0, b = 1;
        auto f1 = []{ return a; };               // error，没有捕获外部变量
        auto f2 = [&]{ return a++; };            // OK，捕获所有外部变量，并对a执行自加运算
        auto f3 = [=]{ return a; };              // OK，捕获所有外部变量，并返回a
        auto f4 = [=]{ return a++; };            // error，a是以复制方式捕获的，无法修改
        auto f5 = [a]{ return a + b; };          // error，没有捕获变量b
        auto f6 = [a, &b]{ return a + (b++); };  // OK，捕获a和b的引用，并对b做自加运算
        auto f7 = [=, &b]{ return a + (b++); };  // OK，捕获所有外部变量和b的引用，并对b做自加运算
    其它例子：
        例1：
            sort(lbvec.begin(), lbvec.end(), [](int a, int b) -> bool { return a < b; });
        例2：
            auto x = [](int a){cout << a << endl;}(123); 
        例3：
            int a = 123;
            auto f1 = [a] { cout << a << endl; };
            auto f2 = [&a] { cout << a << endl; };
            a = 321;
            f1(); // 输出：123
            f2(); // 输出：321
            理解： 在执行第二句的时候，参数值已经传到函数的栈中了，但函数体还没有执行 -MARK
        例4：
            int m = [](int x) { return [](int y) { return y * 2; }(x)+6; }(5); //m=16 
新增std类或方法
    std::bind
        bind函数定义：
            template<typename _Func, typename... _BoundArgs>
            inline
            typename _Bind_helper<__is_socketlike<_Func>::value,
                                  _Func, _BoundArgs...>::type
            bind(_Func&& __f, _BoundArgs&&... __args)
            {
              typedef _Bind_helper<false, _Func, _BoundArgs...> __helper_type;
              typedef typename __helper_type::__maybe_type __maybe_type;
              typedef typename __helper_type::type __result_type;
              return __result_type(__maybe_type::__do_wrap(std::forward<_Func>(__f)),
                       std::forward<_BoundArgs>(__args)...);
            }
        上面代码的结构为：
            模板头 内联标记 函数返回类型 函数名(参数) { 函数体 }
            函数返回类型前面的typename，参考 <typename用法> 一节
        _Bind_helper类定义：
            template<bool _SocketLike, typename _Func, typename... _BoundArgs>
            struct _Bind_helper
            : _Bind_check_arity<typename decay<_Func>::type, _BoundArgs...>
            {
              typedef _Maybe_wrap_member_pointer<typename decay<_Func>::type>
                      __maybe_type;
              typedef typename __maybe_type::type __func_type;
              typedef _Bind<__func_type(typename decay<_BoundArgs>::type...)> type;
            };
        可以发现bind函数将我们传递的函数地址和函数参数做一个包装，
        构造一个类，返回个类的一个实例。
        函数原型：
            template <class Fn, class... Args>
            bind (Fn&& fn, Args&&... args);
            参数列表args中：
            如果绑定到一个值，则调用返回的函数对象将始终使用该值作为参数
            如果是一个形如_n的占位符，
            则调用返回的函数对象会转发传递给调用的参数
            (该参数的顺序号由占位符指定)
        功能：
            bind函数可以看作一个通用的函数适配器
            bind函数接受一个可调用对象，生成一个新的可调用对象来适配原对象。
        使用举例：
            int sum(int x,int y) { return x+y; }
            auto func = std::bind(Plus, std::placeholders::_1, 5);
            int s = func(9);  // s = 9+5 = 14
            示例代码中的_1即为形如_n的占位符，其定义在命名空间placeholders中
            void output(int a, int b) { cout << a << " " << b ; }
            uto func = bind(output, placeholders::_2, placeholders::_1);
            func(8,5);  
            示例中第二个占位符，对应参数a，对应5，第一个占位符，对应参数b，对应8
            所以输出的是 ： 5 8
            std::bind通常用来与std::function配合使用，实现回调函数。
    std::function
        参： https://zhuanlan.zhihu.com/p/390883475
        std::function是一个函数包装器，该函数包装器模板能包装任何类型的可调用实体，
        如普通函数，函数对象，lamda表达式等。使用它，需引用头文件<functional>。
        一个std::function类型对象实例可以包装下列这几种可调用实体：
        函数、函数指针、成员函数、静态函数、lamda表达式和函数对象。
        std::function对象实例可被拷贝和移动。
        当std::function对象实例未包含任何实际可调用实体时，
        调用该std::function对象实例将抛出std::bad_function_call异常。
        function的使用举例：
            参：https://blog.csdn.net/a873744779/article/details/120298574
            // 存储自由函数
            std::function<void(int)> f_display = print_num;
            f_display(-9);
            // 存储lambda表达式
            std::function<void()> f_display_42 = []() { print_num(42); };
            f_display_42();
            // 存储std::bind绑定的对象
            std::function<void()> f_display_31337 = std::bind(print_num, 31337);
            f_display_31337();
            // 存储类成员函数
            std::function<void(const Foo&, int)> f_add_display = &Foo::print_add;
            const Foo foo(314159);
            f_add_display(foo, 1);
            f_add_display(314159, 1);
            // 存储类数据成员访问器的调用
            std::function<int(Foo const&)> f_num = &Foo::num_;
            std::cout << "num_: " << f_num(foo) << '\n';
            // 存储成员函数及对象的调用
            using std::placeholders::_1;
            std::function<void(int)> f_add_display2 = std::bind( &Foo::print_add, foo, _1 );
            f_add_display2(2);
            // 存储对成员函数和对象指针的调用
            std::function<void(int)> f_add_display3 = std::bind( &Foo::print_add, &foo, _1 );
            f_add_display3(3);
            // 存储对仿函数的调用
            std::function<void(int)> f_display_obj = PrintNum();
            f_display_obj(18);
            还可参考： https://zhuanlan.zhihu.com/p/390883475
        function类的代码解析：
            template<typename _Signature>  //声明function类
            class function;  
            template<typename _Res, typename... _ArgTypes>  //function类特化
            class function<_Res(_ArgTypes...)> :   
            //这里看出_Res类应该支持()运算，且能接受热议类型、任意个数的参数
                public _Maybe_unary_or_binary_function<_Res, _ArgTypes...>,
                private _Function_base
            {
            private:
                typedef _Res _Signature_type(_ArgTypes...);
                template<typename _Functor>
                using _Invoke = decltype(__callable_functor(std::declval<_Functor&>())
                                (std::declval<_ArgTypes>()...) );
                template<typename _Tp>
                using _NotSelf = __not_<is_same<_Tp, function>>;
                template<typename _Functor>
                using _Callable = __and_<_NotSelf<_Functor>,
                       __check_func_return_type<_Invoke<_Functor>, _Res>>;
                template<typename _Cond, typename _Tp>
                using _Requires = typename enable_if<_Cond::value, _Tp>::type;
                using _Invoker_type = _Res (*)(const _Any_data&, _ArgTypes&&...);
                _Invoker_type _M_invoker;
            public:
                typedef _Res result_type;
                function() noexcept : _Function_base() { }
                function(nullptr_t) noexcept : _Function_base() { }
                function(function&& __x) : _Function_base() { __x.swap(*this); }
                function(const function& __x) : _Function_base() {
                    if (static_cast<bool>(__x)) {
                        __x._M_manager(_M_functor, __x._M_functor, __clone_functor);
                        _M_invoker = __x._M_invoker;
                        _M_manager = __x._M_manager; } }
                template<typename _Functor,
                    typename = _Requires<_Callable<_Functor>, void>> 
                function(_Functor) : _Function_base() {
                    typedef _Function_handler<_Signature_type, _Functor>
                            _My_handler;
                    if (_My_handler::_M_not_empty_function(__f)) {
                        _My_handler::_M_init_functor(_M_functor, std::move(__f));
                        _M_invoker = &_My_handler::_M_invoke;
                        _M_manager = &_My_handler::_M_manager; } }
                function& operator=(const function& __x) { 
                    function(__x).swap(*this); return *this; }
                function& operator=(function&& __x) { 
                    function(std::move(__x)).swap(*this); return *this; }
                function& operator=(nullptr_t) noexcept {
                    if (_M_manager) {
                        _M_manager(_M_functor, _M_functor, __destroy_functor);
                        _M_manager = nullptr;
                        _M_invoker = nullptr; }
                    return *this; }
                void swap(function& __x) {
                    std::swap(_M_functor, __x._M_functor);
                    std::swap(_M_manager, __x._M_manager);
                    std::swap(_M_invoker, __x._M_invoker); }
                explicit operator bool() const noexcept { return !_M_empty(); }
                _Res operator()(_ArgTypes... __args) const {
                      if (_M_empty()) __throw_bad_function_call();
                      return _M_invoker(_M_functor, std::forward<_ArgTypes>(__args)...);}
                const type_info& target_type() const noexcept;
                template<typename _Functor> _Functor* target() noexcept;
                。。。。
            }
            我们着重关注 operator()，其中的 _M_empty() ，是基类 _Function_base 的成员方法
            bool _M_empty() const { return !_M_manager; }
            typedef bool (*_Manager_type)(_Any_data&, const _Any_data&, _Manager_operation);
            _Manager_type _M_manager;
            另外，_Function_base类中有两个内部类：_Base_manager、_Ref_manager
            这两个内部类中都实现了静态 _M_manager 函数。
            在_Function_base的构造函数中，基本都对 _M_manager 进行了赋值。
            function类的私有部分声明了 _M_invoker 变量：
            typedef _Res (*_M_invoker)(const _Any_data&, _ArgTypes&&...);
            同样，function类的构造函数对 _M_invoker 进行了赋值。
            调用function的()运算符，就是调用 _M_invoker 的括号运算。
            当 std::function<void(int)> f_display = print_num; //print_num为普通函数
            会进到 function(_Functor __f) 构造函数中，执行：
            typedef _Function_handler<_Signature_type, _Functor> _My_handler;
            _My_handler::_M_not_empty_function(__f);
            _My_handler::_M_init_functor(_M_functor, std::move(__f));
            _M_invoker = &_My_handler::_M_invoke;
            _M_manager = &_My_handler::_M_manager;
            也就是说，先把普通函数指针，包装成 _My_handler 类。
            于是，对function的()调用，就是对 &_My_handler::_M_invoke 的调用，
            就是最终对普通函数的调用。
            '''
            _M_init_functor 是 _Function_base 中的静态方法：
            static void _M_init_functor(_Any_data& __functor, _Functor&& __f)
            { _M_init_functor(__functor, std::move(__f), _Local_storage()); }
            static void	_M_init_functor(_Any_data& __functor, _Functor&& __f, true_type)
            { new (__functor._M_access()) _Functor(std::move(__f)); }
            new的这种用法为就地初始化，
            起到的作用是让 __functor 存放 _Functor(std::move(__f))
            '''
    std::is_array
        定义于头文件 <type_traits>
        template< class T >
        struct is_array;
        检查 T 是否数组类型。
        若 T 为数组类型，则提供等于 true 的成员常量 value 。
        否则， value 等于 false。value为公开静态成员常量
        参：https://www.apiref.com/cpp-zh/cpp/types/is_array.html
    std::forward 
        std::move它的作用是无论你传给它的是左值还是右值，通过std::move之后都变成了右值。
        std::forward则与之不同，如果原来的值是左值，经std::forward处理后该值还是左值；
        如果原来的值是右值，经std::forward处理后它还是右值。
        例：
        template<typename T>
        void print(T & t){
            std::cout << "左值" << std::endl;
        }
        template<typename T>
        void print(T && t){
            std::cout << "右值" << std::endl;
        }
        template<typename T>
        void testForward(T && v){
            print(v);  //-MARK 不明白为什么这里的v被视作左值
            print(std::forward<T>(v)); //遵循传给v的原始数值类型
            print(std::move(v));   //统统变成右值
        }
        testForward(1);  //依次输出：左值、右值、右值
        int x = 1;
        testForward(x);  //依次输出：左值、左值、右值
        对参数 T&& v 的说明：
            T后的&&，其实是起到引用折叠的作用：
            && &  <=> &    //保持是左值
            && && <=> &&   //保持是右值
            所以，如果T无论是&类型的，还是&&类型的，都能保证其真实类型
            而 & && <==> &    /    & & <==> &     //都变成了左值
            所以不能用 T& v
    std::is_xxx模板参数类型判断
        判断类型符合某种特点，普遍具有公开的布尔成员常量value，定义于头文件 <type_traits>
        这是一系列函数，如is_arrary,is_enum,is_class,is_func,is_integer等
        具体：https://www.apiref.com/cpp-zh/cpp/types.html
    std::enable_if
        用法： std::enable_if<条件，类型T>::type
        说明：当条件为真时，std::enable_if类借助偏特化，在其中定义typename T type;
              当条件为假时，std::enable_if类中没有定义type
        源码：template<bool, typename _Tp = void>  struct enable_if { };
              template<typename _Tp>  struct enable_if<true, _Tp> { typedef _Tp type; };
        使用举例：
              template <typename T>
              typename std::enable_if<std::is_integer<T>::value,T>::type
              dosum(T t1,T t2) 
              { 
                  return t1+t2; 
              }
              template <typename T>
              typename std::enable_if<std::is_base_of<Point,T>,T>::type
              dosum(T t1,T t2) 
              {
                  T t; 
                  t.x=t1.x+t2.x; 
                  t.y=t1.y+t2.y; 
                  return t; 
              }
              dosum(3,5);      //可以编译成功
              dosum(pt1,pt2);  //可以编译成功
              dosum("a","b");  //编译报错，不支持这种参数形式
              分析：
              上面两个dosum的实现，其返回值都是在特定条件下才有意义的，
              如第一个dosum函数实现，当类型不是数字类型时，该函数不是一个合法的定义，
              因为此时std::enable_if中没有type，
              但此种情况下，只能说明该模板函数不能有效实例化，而不会报编译错误。
              例2：
              template<typename T>
              typename std::enable_if<std::is_array<T>::value,int>::type
              test()
              {
                  puts("is arrary");
                  return 1;
              }
              template<typename T>
              typename std::enable_if<!std::is_array<T>::value,void>::type
              test()
              {
                  puts("is not array");
              }
              template<typename T>
              typename std::enable_if<std::is_array<T>::value,int>::type
              test2()
              {
                  puts("is arrary");
                  return 1;
              }
              test<int>();
              test<int[]>();
              test2<int>();    //这句会编译报错
              test2<int[]>();
              分析： 本例中看似有两个签名相同的test函数，却不会编译报错，
              这是因为这是模板函数，这只是（编译器）产生真实函数代码的模板参照，
              而真正形成的函数代码，替换后的模板参数也作为函数签名的一部分。
              另外需要再次说明的是，对于模板函数，当该模板函数被代入真正类型后，
              如果得到的函数会引发编译报错，如test2<int>();
              编译器的处理方式是：
              将int代入模板函数test2中，发现如果这样做，就会导致编译报错（std::enable_if中没有type），
              所以此时编译器直接就不将int代入到test2中（从而产生一个编译报错的函数定义）了。
              于是，编译错误会定位到test2<int>(); 
              而模板函数test2只有在能编译成功的前提下才会生成真实的代码（存到二进制文件中）
              模板函数本身不会导致编译失败，编译器大不了不使用（不实例化）该模板。
              例3：
              template <typename T>
              test3()
              {
                  return 0;
              }
              test4()
              {
              }
              对这两个函数进行编译，结果只有test4给出编译警告：
              warning: no return statement in function returning non-void [-Wreturn-type]
              这也从侧面反映了模板函数不会导致编译失败
              但注意，上面这个编译原则，编译器只看模板函数实例化后的声明是否有效，
              像如下面这样：
              template <typename T>
              void test5()
              {
                  typename std::enable_if<std::is_integral<T>::value,T>::type t;
                  puts(typeid(t).name());
              }
              test5<int>();
              test5<bool>();  //编译成功，std::is_integral<bool>::value == true
              test5<int[]>();  //引起编译报错，但错误不是定位在该句，而是定位在test5中
    std::lock_guard
        std中锁的复制类，能自动加解锁
        如：std::lock_guard<std::mutex> guard(socket_mutex_);
    std::this_thread
        提供get_id()、yield()、sleep_for()、sleep_until()功能