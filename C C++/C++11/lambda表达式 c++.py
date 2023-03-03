格式：[ capture ] ( params ) opt ->ret { body; };
    capture 是捕获列表，必选
    params  是参数表，可选
    opt     是函数选项，可选
    ret     是返回值类型，可选，省略时，连前面的->一块去掉
    body    是函数体，必选
    
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
