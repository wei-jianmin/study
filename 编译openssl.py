编译openssl 1.1.1 记录
    参：https://blog.csdn.net/zhounixing/article/details/105519536
    参：https://blog.csdn.net/fksec/article/details/52667055
    参：https://blog.csdn.net/lixiang987654321/article/details/81154613
    参：https://blog.csdn.net/u012332816/article/details/81742516
    1. 下载安装perl、nasm、dmake
    2. 借助perl执行configure，生成MakeFile文件
       生成动态openssl：
           perl configure VC-WIN64A shared no-asm
       生成静态openssl：
           perl Configure VC-WIN32 no-asm no-shared 
                          --prefix="C:/openssl_lib/win32-release" 
                          --openssldir="C:/openssl_lib/win32-release/ssl" 
       生成Debug版的动态库
           Perl Configure -DDEBUG -D_DEBUG -DOPENSSL_DEBUG_KEYGEN -DSSL_DEBUG 
                          -DALG_DEBUG -DCIPHER_DEBUG  -DTLS_DEBUG  -DKSSL_DEBUG 
                          debug-VC-WIN32 no-asm --prefix=C:\MyProgramFiles\OpenSSLv1.0.2h 
                          --openssldir=C:\MyProgramFiles\OpenSSLv1.0.2h\SSL
    3. 执行nmake，按MakeFile规则编译项目
    4. 执行namke test，测试编译结果
    5. 执行namek install，完成安装
使用openssl静态库
    vs工程中使用openssl静态库
        编译时会有些函数未定义，
        这些函数定义在 Crypt32.lib Ws2_32.lib 这两个库中
    在MinGW中使用openssl静态库
        会报大量的 error: undefined reference to `_chkstk'
        因为这两个openssl静态库根本还是用vs的编译工具生成的
        而__chkstk是 Windows 特定功能，以确保堆栈空间在增长时进行映射
        它由用于 Windows目标的 LLVM 编译器生成
        因此无法用MinGW连接vs生成的静态库
        另外这两种编译器的函数重命名规则也不一样，
        这也决定了lib库一般在这两种编译器之间不通用
        所以最直接的解决办法就是不用MinGW引用vs生成的静态库