定义：一般将进程定义成一个正在运行的程序的一个实例

构成：
    一个内核对象
        操作系统用它来管理进程。内核对象合适系统保存进程统计信息的地方
    一块地址空间
        保护可执行程序(exe/dll)的代码、数据，此外还保护动态内存分配，如线程的堆、栈的分配
        
执行：
    线程负责执行进程地址空间包含的代码
    一个进程可以有多个线程，每个线程有一组CPU寄存器，及线程自己的堆栈

两种应用程序类型：
    GUI（图形用户界面）程序和CUI（控制台用户界面）程序
    这两者的界面是模糊的，GUI中可以创建控制台，控制台程序中也可以创建窗口
    程序运行时，加载程序(loader)会检查可执行文件的文件头，并获取这个标示值(子系统值).
    如果该值表明是个CUI程序，不管是从控制台打开的该程序，还是从窗口中打开的，加载程序会确保其有一个控制台窗口。
    而如果不是个CUI程序，则操作系统就不再关心应用程序的界面是什么类型的。
    
程序入口点：
    操作系统实际并不是调用我们所写的main函数，
    而是调用在链接时，使用-entry选项设置的，一个C/C++运行库实现的函数（称为启动函数），
    该函数将完成C/C++运行库的初始化操作（使我们可以调用malloc、free之类的函数），
    该函数还确保了我们声明（并同时定义）的全局和静态C++对象能被正确的构造。
    启动函数完成的工作：
        获取指向新进程的完整命令行的一个指针
        获取指向新进程的环境变量的一个指针
        初始化C/C++运行库的全局变量（如果包含了stdlib.h，我们就可以访问这些变量）
            可使用的C/C++运行库的全局变量:
                #经测试，_osver、_winmajor、_winminor、_winver不被vs识别
                unsigned int _osver     操作系统的构建版本号，如vista RTM为build 6000，则_osver=6000，请换用GetVersionEx
                unsigned int _winmajor  十六禁止的windows主版本号，Vista该值为6，请换用GetVersionEx
                unsigned int _winminor  十六禁止的windows次版本号，Vista该值为0，请换用GetVersionEx
                unsigned int _winver    (_winmajor<<8)+_winminor，请换用GetVersionEx
                unsigned int __argc     命令行传来的参数个数，请换用GetCommandLine
                char[]         __argv     一个数组指针，数组的每一项指向一个命令行参数，请换用GetCommandLine
                wchar_t[]      __argv     一个数组指针，数组的每一项指向一个命令行参数，请换用GetCommandLine
                char[]         _environ   一个数组指针，数组的每一项指向一个环境字符串，请换用GetEnvironmentStrings或GetEnvironmentVariable
                wchar_t[]      _wenviron  一个数组指针，数组的每一项指向一个环境字符串，请换用GetEnvironmentStrings或GetEnvironmentVariable
                char         _pgmptr    正在运行的程序的完整路径名，请换用GetModuleFileName
                wchar_t      _wpgmptr   正在运行的程序的完整路径名，请换用GetModuleFileName
        初始化C运行库内存分配函数(malloc/calloc)和其它底层I/O例程使用的堆
        调用所有全局和静态C++类对象的构造函数
    完成了这些初始化工作之后，程序才进入我们的入口点函数。
    我们一般的main函数都带有两个参数argc和argv，用以接受命令行输入的参数，
    实际该函数还可以带第三个输入参数 TCHAR* env[]，用以接受进程的环境变量。
    但不推荐使用这种方法，而建议直接使用相应的windows API函数。
    如果是GUI程序，会在程序的第一个参数传入HINSTANCE，
    HINSTANCE和HMODULE在32位系统上完全等价，只有在之前的16位系统中，两者才有区别。
    WinMain的hInstanceExe参数实际值是一个内存地址：
        系统将可执行文件加载到进程地址空间的位置，
        例如加载到0x00400000这个地址，则hInstanceExe的值就是0x00400000,
        具体实际加载到哪个基地址，是由链接器决定的，不同的链接器使用不同的默认基地址，
        vs使用的默认基地址是0x00400000,使用/BASE:address链接器开关，可以更改该基地址。
    C运行库的启动函数执行一个GUI程序时，会调用WinAPI函数GetCommondLine先获取命令行参数，
    然后将第一个参数（可执行文件的名称）去掉，把剩下的值传给WinMain的pszCmdLine参数。
    我们可以在WinMain调用GetCommondLine来获取完整的命令行的指针。
    
程序的结束：
    main函数结束后，启动函数调用C运行库函数exit，向其传递main函数的返回值。
    exit函数执行如下任务：
        调用所有用_onexit方法注册的函数
        调用所有全局和静态c++类对象的析构函数
        对DEBUG的程序，如果设置了_CRTDBG_LEAK_CHECK_DF标识，就调用_CrtDumpMemoryLeaks函数生成内存泄漏报告
        调用系统函数ExitProcess函数，向其传递main函数的返回值（杀死进程，设置退出代码）
        
进程的环境变量
    每个进程都有一个与他关联的环境块，这是在进程的地址空间中分配的。
    GetEnvironmentStrings函数用来获取完整的环境块，并用FreeEnvironmentStrings函数来释放该内存块。
    程序的命令行参数即是存放在这里面的。
    对于控制台程序来说，还可以使用TCHAR*env[]参数来获取，env数组中，最后一个值是NULL表明是数组的末尾。
    系统进程的环境变量
        用户登录windows时，系统会创建外壳(shell)进程，并将一组环境变量与其关联。
        系统通过两个注册表的位置来获得初始的环境变量：
        系统环境变量：HKLM/SYSTEM/CurrentControlSet/Control/Session Manager/Environment
        用户环境变量：HKCU/Environment
        通过注册表修改了环境变量后，为了是改动对所有应用程序生效，用户必须注销重新登录，
        有的应用程序（如资源管理器、任务管理器、控制面板）可以在主窗口接受到WM_SETTINGCHANGE消息时，用新的注册表项来更新他的环境块。
    通常子进程会继承这一组环境变量，不过父进程可以控制哪些环境变量允许子进程继承。
    注意，这里所说的继承，是指子进程获得父进程环境变量的一个副本，这个副本是子进程所有的。
    用户创建子进程时，经常使用环境控制所创建子进程的行为（因为子进程会继承该环境变量值）。
    GetEnvironmentVariable函数可以判断一个环境变量是否存在，如果存在，他的值又是什么。
    
    
    
    
    