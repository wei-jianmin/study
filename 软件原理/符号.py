关于符号表
    动态符号表  vs  [静态]符号表
        动态符号表 (.dynsym) 用来保存与动态链接相关的导入导出符号，不包括模块内部的符号。
        而 .symtab 则保存所有符号，包括 .dynsym 中的符号。
        .symtab 和 .dynsym 都有相对应的辅助表 :
        .symtab -> .strtab(String Table)符号字符串表
        .dynsym -> .dynstr(Dynamic String Table)动态符号字符串表
        动态符号表中所包含的符号的符号名保存在动态符号字符串表 .dynstr 中
        使用 readelf --dyn-syms 查看 .dynsym 表
        静态链接中有一个专门的段叫符号表 -- “.symtab”(Symbol Table)， 
        里面保存了所有关于该目标文件的符号的定义和引用。
        动态链接中有一个段叫 动态符号表 -- “.dynsym”(Dynamic Symbol) ，
        但.dynsym 相对于 .symtab 只保存了与动态链接相关的导入导出符号.
        使用readelf -s，可查看文件的符号表节，注意是小写的s，大写的-S表查看所有节q
        “.dynsym”只保留“.symtab”中的全局符号(global symbols )。
        命令strip可以去掉elf文件中“.symtab”，但不会去掉“.dynsym”。
        /lib里的共享对象库.so文件在使用nm时提示no symbol是因为被strip了。
        所以需要查看动态符号表“.dynsym”，加上-D
    全局符号 参：https://blog.csdn.net/seaer0903/article/details/6677150
        强符号和弱符号
            编译器会把源文件的全局符号(global symbol)分成强(strong)和弱(weak)两类
            编译器认为函数与初始化了的全局变量都是强符号，而未初始化的全局变量则成了弱符号
        符号在多个目标文件中存在时：
            规则1: 不允许强符号被多次定义(即不同的目标文件中不能有同名的强符号)；
            规则2: 如果一个符号在某个目标文件中是强符号，在其它文件中都是弱符号，那么选择强符号；
            规则3: 如果一个符号在所有目标文件中都是弱符号，那么选择其中任意一个；
        链接器完成的工作：更详细的说明请参见原网页
            符号解析(symbol resolution)阶段，链接器按照所有目标文件和库文件出现在命令行中的顺序从左至右依次扫描它们
            在此期间它要维护若干个集合:
            (1)集合E是将被合并到一起组成可执行文件的所有目标文件集合；
            (2)集合U是未解析符号(unresolved symbols，比如已经被引用但是还未被定义的符号)的集合；
            (3)集合D是所有之前已被加入到E的目标文件定义的符号集合。
            一开始，E、U、D都是空的。
            (1): 对命令行中的每一个输入文件f，链接器确定它是目标文件还是库文件，
                 如果它是目标文件，就把f加入到E，并把f中未解析的符号和已定义的符号分别加入到U、D集合中，然后处理下一个输入文件。
            (2): 如果f是一个库文件，链接器会尝试把U中的所有未解析符号与f中各目标模块定义的符号进行匹配。
                 如果某个目标模块m定义了一个U中的未解析符号，那么就把m加入到E中，
                 并把m中未解析的符号和已定义的符号分别加入到U、D集合中。
                 不断地对f中的所有目标模块重复这个过程直至到达一个不动点(fixed point)，此时U和D不再变化。
                 而那些未加入到E中的f里的目标模块就被简单地丢弃，链接器继续处理下一输入文件。
            (3): 如果处理过程中往D加入一个已存在的符号，或者当扫描完所有输入文件时U非空，链接器报错并停止动作。
                 否则，它把E中的所有目标文件合并在一起生成可执行文件。
        附：VS编译选项 /ML、/MLd、/MT、/MTd、/MD、/MDd  ： 编译时指定链接缺省库
            VC带的编译器名字叫cl.exe，它有这么几个与标准程序库有关的选项: /ML、/MLd、/MT、/MTd、/MD、/MDd。
            这些选项告诉编译器应用程序想使用什么版本的C标准程序库。
            /ML(缺省选项)对应单线程静态版的标准程序库(libc.lib)；
            /MT对应多线程静态版标准库(libcmt.lib)，此时编译器会自动定义_MT宏；
            /MD对应多线程DLL版(导入库msvcrt.lib，DLL是msvcrt.dll)，编译器自动定义_MT和_DLL两个宏。
            后面加d的选项都会让编译器自动多定义一个_DEBUG宏，表示要使用对应标准库的调试版，因此
            /MLd对应调试版单线程静态标准库(libcd.lib)，
            /MTd对应调试版多线程静态标准库(libcmtd.lib)，
            /MDd对应调试版多线程DLL标准库(导入库msvcrtd.lib，DLL是msvcrtd.dll)。
            当编译器干完了活，为了在连接是知道一个个目标文件到底谁依赖谁，
            所以在cl编译出的目标文件中会有一个专门的区域存放一些指导链接器如何工作的信息，
            其中一个信息就是缺省库（cl命令编译出的.obj目标文件中搜索"-defaultlib"字符串）
            vs的项目配置属性页/C&C++/代码生成/运行库，就是跟这里相对应的。
            vs的项目配置属性页/链接器/输入/忽略所有默认库，就是跟这里相对应的。
            另外，用dumpbin /DIRECTIVES my.lib，然后在输出中找那些"Linker Directives"引导的信息
            你一定会发现每一处这样的信息都会包含若干个类似"-defaultlib:XXXX"这样的字符串，
            其中XXXX便代表目标模块指定的缺省库名。
            
控制共享文件的导出符号
    参：https://www.cnblogs.com/blogs-of-lxl/p/10818403.html
    法1 gcc的c++ visibility支持
        Linux动态库中默认符号都是导出的，但也可以通过编译选项控制默认不导出：
        gcc 在链接时设置 -fvisibility=hidden，则不加 visibility声明的都默认为hidden; 
        gcc 默认设置 -fvisibility=default，即全部可见；
        -fvisibility还有可选值internal和protected，不过这两个值几乎从不使用。
        另外，也可对单独的符号（类、函数或变量）控制其是否导出
        如果一个类被标识为hidden，则其所有成员都会被隐藏
        注： 这种方式只影响动态符号表（.dynsymco）
        如； int x __attribute__((visibility ("hidden")));  
            //或  __attribute__((visibility ("hidden"))) int x;
        如果x是定义在一个动态库中，则动态连接时，无法从另一个动态库中引用
        尽管链接器可以知道x，但不能用于动态连接
    法2 使用链接参数 --retain-symbols-file 控制静态符号表，--version-script 控制动态符号表，
        后面都是接含有导出符号的文件的名字
        这两个参数在移植windows下的动态库很有用，windows下的DEF文件能控制导出符号，
        我们可以在linux下的构建脚本中解析DEF生成一个导出符号文件（xxx.sym/xxx.map），
        然后作为-Wl,-retain-symbols-file，-Wl,-version-script的链接选项的参数
        –retain-symbols-file=xxx.sym 控制静态符号表，–version-script=xxx.map 控制动态符号表
        此时，除了指定导出的符号外，其它全部为仅内部可见
        .sym文件的格式为直接按行列出要导出的符号，如：
            func_1
            func_3
        .map文件的写法有点类似结构体的写法，如：
            {
            global:
              func_1;
              func_2;
            local: *;
            };            
    法3 Pragmas
        将符号标识为default或者hidden的另外一种方法是使用GCC 4.0新引入的pragma指令
        GCC可见性pragma的优点是可以快速地标识一整块函数，而不需要将可见性属性应用到每个函数中
        如：
        void f() { }
        #pragma GCC visibility push(default)
        void g() { }
        void h() { }
        #pragma GCC visibility pop
        在这个例子中，函数g和h被标识为default，因此无论-fvisibility选项如何设置，都会输出；
        而函数f则遵循-fvisibility选项设置的任何值。
        push和pop两个关键字标识这个pragma可以被嵌套。
        
什么是  hidden symbol ： 就是目标文件/库中存在，但没有暴露出来的符号