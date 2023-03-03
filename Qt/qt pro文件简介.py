qt不同工程的pro文件内容：
    qt界面程序：
        TEMPLATE = app
        QT ： +core +gui +widgets               //模块引用
        TARGET = qtwidget_porj
    qt控制台：
        TEMPLATE = app
        QT ： +core  -gui                       //模块引用
        CONFIG ： -app_bundle +c++11 +console   //编译控制
        TARGET = qtconsole_proj
    qt纯c++程序：
        TEMPLATE = app
        CONFIG ： -qt -app_bundle +c++11 +console   
    qt库c++
        TEMPLATE = lib                          //程序类型
        QT : -core gui
        TARGET = qt_cplus_lib                   //要生成的程序的名称
        DEFINES += QT_CPLUS_LIB_LIBRARY         //预定义宏
        
可以参考的网页：
    https://www.cnblogs.com/Braveliu/p/5107550.html       
        
=====================================================

pro文件中支持的控制项：
参：https://blog.csdn.net/hebbely/article/details/66970821
1.  注释  #        
2.  CONFIT
    release	    项目以release模式构建。如果也指定了debug，则使用后者。
    debug	    项目以debug模式构建。
    debug_and_release	项目准备以debug和release两种模式构建。
    debug_and_release_target	[默认]如果也指定了debug_and_release，最终的debug和release构建在不同的目录。
    build_all	如果指定了debug_and_release，默认情况下，该项目会构建为debug和release模式。
    autogen_precompile_source	自动生成一个.cpp文件，包含在.pro中指定的预编译头文件。
    ordered	    使用subdirs模板时，此选项指定应该按照目录列表的顺序处理它们。
    precompile_header	可以在项目中使用预编译头文件的支持。
    warn_on	    编译器应该输出尽可能多的警告。如果也指定了warn_off，最后一个生效。
    warn_off	编译器应该输出尽可能少的警告。
    exceptions	启用异常支持。默认设置。
    exceptions_off	禁用异常支持。
    rtti	    启用RTTI支持。默认情况下，使用编译器默认。
    rtti_off	禁用RTTI支持。默认情况下，使用编译器默认。
    stl	        启用STL支持。默认情况下，使用编译器默认。
    stl_off	    禁用STL支持。默认情况下，使用编译器默认。
    thread	    启用线程支持。当CONFIG包括qt时启用，这是缺省设置。
    c++11	    启用c++11支持。如果编译器不支持c++11这个选项，没有影响。默认禁用。
    c++14	    启用c++14支持。如果编译器不支持c++14这个选项，没有影响。默认禁用。
    console	    只用于app模板 应用程序是一个windows的控制台应用程序
    windows	    只用于app模板 应用程序是一个windows的窗口应用程序
    testcase	?
    depend_includepath	?
    dll	        只用于”lib”模板，库是一个共享库（dll）
    staticlib	只用于“lib”模板，库一个静态库
    plugin	    只用于“lib”模板，库是一个插件，这会使dll选项生效
    qt          应用程序是个QT程序，并且Qt库将会被连接
    x11         应用程序是个x11应用程序或库
3.  QT       指定使用的Qt的模块
    指定项目中使用Qt的模块。默认情况下，QT包含core和gui
    如果想建立一个不包含Qt GUI模块的项目，可以使用“ -=”操作符
    QT += core gui widgets xml network
    QT -= gui # 仅仅使用core模块
    如果不使用QT的任何模块，如纯c++控制台，则需 CONFIG -= qt
4.  TARGET   指定目标文件的名称
    默认情况下包含的项目文件的基本名称
    TARGET = LidarPlus
    上面项目会生成一个可执行文件，Windows下为LidarPlus.exe，Unix下为LidarPlus
5.  TEMPLATE     指定生成哪种MakeFile
    模板变量告诉qmake为这个应用程序生成哪种makefile，可供使用的选项如下
    选项	说明
    app	    创建一个用于构建应用程序的Makefile（默认）
    lib	    创建一个用于构建库的Makefile
    subdirs	创建一个用于构建目标子目录的Makefile，子目录使用SUBDIRS变量指定
    aux	    创建一个不建任何东西的Makefile。
    vcapp	仅适用于Windows。创建一个Visual Studio应用程序项目
    vclib	仅适用于Windows。创建一个Visual Studio库项目。
6.  SOURCES  指定项目中的所有源文件
7.  HEADERS  指定项目中的所有头文件
8.  FROMS    指定项目中的UI文件
    指定项目中的UI文件，这些文件在编译前被uic处理。
    所有的构建这些UI文件所需的依赖、头文件和源文件都会自动被添加到项目中。
9.  DEFINES  预定义宏
10. RESOURCES    指定资源文件 (qrc) 的名称
    如： RESOURCES += Resource/resource.qrc
11. DEPENDPATH   程序编译时依赖的相关路径
12. INCLUDEPATH  头文件的包含路径
    如果路径包含空格，需要使用引号包含
13. LIBS     指定链接到项目中的库列表
    可以使用Unix -l (library) 和 -L (library path) 标志
    如果路径包含空格，需要使用引号包含路径
    win32:LIBS += c:/mylibs/math.lib
    unix:LIBS += -L/usr/local/lib -lmath
14. DESTDIR  指定在何处放置目标文件
15. MOC_DIR  指定moc的所有中间文件放置的目录
16. OBJECTS_DIR  指定所有中间文件.o（.obj）放置的目录
17. RCC_DIR  指定Qt资源编译器输出文件的目录
    .qrc文件转换成qrc_*.h文件的存放目录
18. UI_DIR   指定来自uic的所有中间文件放置的目录
    .ui文件转化成ui_*.h文件的存放目录
19. RC_FILE  指定应用程序资源文件的名称
    例： RC_FILE += $$PWD/UrgBenri.rc
20. RC_ICONS
21. CODECFORSRC  指定源文件编码方式
22. 平台相关处理
    如：
    win32:RC_FILE += $$PWD/UrgBenri.rc
    macx:ICON = $$PWD/icons/UrgBenri.icns
    win32 {
        CONFIG += embed_manifest_exe
    }
23. 内嵌manifest文件
    Qt4.1.3之后的版本提供了CONFIG选项来提供内嵌manifest文件的功能
    CONFIG += embed_manifest_exe
    CONFIG += embed_manifest_dll（默认开启）
24. Qt内置变量
    QMAKE_TARGET_COMPANY：指定项目目标的公司名称，仅适用于Windows
    QMAKE_TARGET_PRODUCT：指定项目目标的产品名称，仅适用于Windows
    QMAKE_TARGET_DESCRIPTION：指定项目目标的描述信息，仅适用于Windows
    QMAKE_TARGET_COPYRIGHT：指定项目目标的版权信息，仅适用于Windows
    PACKAGE_DOMAIN：
    PACKAGE_VERSION：
    RC_CODEPAGE：指定应该被包含进一个.rc文件中的代码页，仅适用于Windows
    RC_LANG：指定应该被包含进一个.rc文件中的语言，仅适用于Windows
    RC_ICONS：指定应该被包含进一个.rc文件中的图标，仅适用于Windows
    VERSION：指定程序版本号
    BUILD_NUMBER：
    APP_REVISION：
    APP_VERSION_DATE：
    APP_VERSION：
    注意：QMAKE_TARGET_COMPANY、QMAKE_TARGET_DESCRIPTION、
    QMAKE_TARGET_COPYRIGHT、QMAKE_TARGET_PRODUCT、RC_CODEPAGE、RC_LANG
    均仅适用于Windows， 而且只有在VERSION或RC_ICONS 变量被设置，
    并且RC_FILE和 RES_FILE变量没有被设置的情况下生效  
    
qmake之CONFIG(debug, debug|release)
    CONFIG(debug, debug|release) 这种语法是什么含义呢？    
    两个参数，前者是要判断的active的选项，后者是互斥的选项的一个集合。

    在 Qt 编程中，多数人用的都是 qmake，并编写相应pro文件。
    实际中经常需要对 debug 与 release 两种编译模式 设置不同的选项，比方说链接不同库
    遇到该问题，简单看看qmake的manual，不少人都会写出类似下面的内容：
    debug {
        LIBS += -L../lib1 -lhellod
    }
    release {
        LIBS += -L../lib2 -lhello
    }
    很不幸，这么做通常不能正常工作。
    如果打开看生成的makefile文件，会发现 无论是debug还是release，上面的两个语句都会同时起作用。
    也就是说，上面相当于
    LIBS += -L../lib1 -lhellod -L../lib2 -lhello原因
    这是很违反直觉的，因为CONFIG可以同时定义 debug 和 release，但只有一个处于active
    （当两个互斥的值出现时，最后设置的处于active状态）
    比如：
    CONFIG = debug
    CONFIG += release
    ...
    这种情况下，release处于active状态，但，debug 和 release 都能通过上面的测试。
    如何解决
        CONFIG(debug, debug|release) {
            LIBS += -L../lib1 -lhellod
        } else {
            LIBS += -L../lib2 -lhello
        }
    或
        CONFIG(debug, debug|release)：LIBS += -L../lib1 -lhellod
        CONFIG(release, debug|release)：LIBS += -L../lib2 -lhello