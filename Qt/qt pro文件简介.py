qt��ͬ���̵�pro�ļ����ݣ�
    qt�������
        TEMPLATE = app
        QT �� +core +gui +widgets               //ģ������
        TARGET = qtwidget_porj
    qt����̨��
        TEMPLATE = app
        QT �� +core  -gui                       //ģ������
        CONFIG �� -app_bundle +c++11 +console   //�������
        TARGET = qtconsole_proj
    qt��c++����
        TEMPLATE = app
        CONFIG �� -qt -app_bundle +c++11 +console   
    qt��c++
        TEMPLATE = lib                          //��������
        QT : -core gui
        TARGET = qt_cplus_lib                   //Ҫ���ɵĳ��������
        DEFINES += QT_CPLUS_LIB_LIBRARY         //Ԥ�����
        
���Բο�����ҳ��
    https://www.cnblogs.com/Braveliu/p/5107550.html       
        
=====================================================

pro�ļ���֧�ֵĿ����
�Σ�https://blog.csdn.net/hebbely/article/details/66970821
1.  ע��  #        
2.  CONFIT
    release	    ��Ŀ��releaseģʽ���������Ҳָ����debug����ʹ�ú��ߡ�
    debug	    ��Ŀ��debugģʽ������
    debug_and_release	��Ŀ׼����debug��release����ģʽ������
    debug_and_release_target	[Ĭ��]���Ҳָ����debug_and_release�����յ�debug��release�����ڲ�ͬ��Ŀ¼��
    build_all	���ָ����debug_and_release��Ĭ������£�����Ŀ�ṹ��Ϊdebug��releaseģʽ��
    autogen_precompile_source	�Զ�����һ��.cpp�ļ���������.pro��ָ����Ԥ����ͷ�ļ���
    ordered	    ʹ��subdirsģ��ʱ����ѡ��ָ��Ӧ�ð���Ŀ¼�б��˳�������ǡ�
    precompile_header	��������Ŀ��ʹ��Ԥ����ͷ�ļ���֧�֡�
    warn_on	    ������Ӧ����������ܶ�ľ��档���Ҳָ����warn_off�����һ����Ч��
    warn_off	������Ӧ������������ٵľ��档
    exceptions	�����쳣֧�֡�Ĭ�����á�
    exceptions_off	�����쳣֧�֡�
    rtti	    ����RTTI֧�֡�Ĭ������£�ʹ�ñ�����Ĭ�ϡ�
    rtti_off	����RTTI֧�֡�Ĭ������£�ʹ�ñ�����Ĭ�ϡ�
    stl	        ����STL֧�֡�Ĭ������£�ʹ�ñ�����Ĭ�ϡ�
    stl_off	    ����STL֧�֡�Ĭ������£�ʹ�ñ�����Ĭ�ϡ�
    thread	    �����߳�֧�֡���CONFIG����qtʱ���ã�����ȱʡ���á�
    c++11	    ����c++11֧�֡������������֧��c++11���ѡ�û��Ӱ�졣Ĭ�Ͻ��á�
    c++14	    ����c++14֧�֡������������֧��c++14���ѡ�û��Ӱ�졣Ĭ�Ͻ��á�
    console	    ֻ����appģ�� Ӧ�ó�����һ��windows�Ŀ���̨Ӧ�ó���
    windows	    ֻ����appģ�� Ӧ�ó�����һ��windows�Ĵ���Ӧ�ó���
    testcase	?
    depend_includepath	?
    dll	        ֻ���ڡ�lib��ģ�壬����һ������⣨dll��
    staticlib	ֻ���ڡ�lib��ģ�壬��һ����̬��
    plugin	    ֻ���ڡ�lib��ģ�壬����һ����������ʹdllѡ����Ч
    qt          Ӧ�ó����Ǹ�QT���򣬲���Qt�⽫�ᱻ����
    x11         Ӧ�ó����Ǹ�x11Ӧ�ó�����
3.  QT       ָ��ʹ�õ�Qt��ģ��
    ָ����Ŀ��ʹ��Qt��ģ�顣Ĭ������£�QT����core��gui
    ����뽨��һ��������Qt GUIģ�����Ŀ������ʹ�á� -=��������
    QT += core gui widgets xml network
    QT -= gui # ����ʹ��coreģ��
    �����ʹ��QT���κ�ģ�飬�紿c++����̨������ CONFIG -= qt
4.  TARGET   ָ��Ŀ���ļ�������
    Ĭ������°�������Ŀ�ļ��Ļ�������
    TARGET = LidarPlus
    ������Ŀ������һ����ִ���ļ���Windows��ΪLidarPlus.exe��Unix��ΪLidarPlus
5.  TEMPLATE     ָ����������MakeFile
    ģ���������qmakeΪ���Ӧ�ó�����������makefile���ɹ�ʹ�õ�ѡ������
    ѡ��	˵��
    app	    ����һ�����ڹ���Ӧ�ó����Makefile��Ĭ�ϣ�
    lib	    ����һ�����ڹ������Makefile
    subdirs	����һ�����ڹ���Ŀ����Ŀ¼��Makefile����Ŀ¼ʹ��SUBDIRS����ָ��
    aux	    ����һ�������κζ�����Makefile��
    vcapp	��������Windows������һ��Visual StudioӦ�ó�����Ŀ
    vclib	��������Windows������һ��Visual Studio����Ŀ��
6.  SOURCES  ָ����Ŀ�е�����Դ�ļ�
7.  HEADERS  ָ����Ŀ�е�����ͷ�ļ�
8.  FROMS    ָ����Ŀ�е�UI�ļ�
    ָ����Ŀ�е�UI�ļ�����Щ�ļ��ڱ���ǰ��uic����
    ���еĹ�����ЩUI�ļ������������ͷ�ļ���Դ�ļ������Զ�����ӵ���Ŀ�С�
9.  DEFINES  Ԥ�����
10. RESOURCES    ָ����Դ�ļ� (qrc) ������
    �磺 RESOURCES += Resource/resource.qrc
11. DEPENDPATH   �������ʱ���������·��
12. INCLUDEPATH  ͷ�ļ��İ���·��
    ���·�������ո���Ҫʹ�����Ű���
13. LIBS     ָ�����ӵ���Ŀ�еĿ��б�
    ����ʹ��Unix -l (library) �� -L (library path) ��־
    ���·�������ո���Ҫʹ�����Ű���·��
    win32:LIBS += c:/mylibs/math.lib
    unix:LIBS += -L/usr/local/lib -lmath
14. DESTDIR  ָ���ںδ�����Ŀ���ļ�
15. MOC_DIR  ָ��moc�������м��ļ����õ�Ŀ¼
16. OBJECTS_DIR  ָ�������м��ļ�.o��.obj�����õ�Ŀ¼
17. RCC_DIR  ָ��Qt��Դ����������ļ���Ŀ¼
    .qrc�ļ�ת����qrc_*.h�ļ��Ĵ��Ŀ¼
18. UI_DIR   ָ������uic�������м��ļ����õ�Ŀ¼
    .ui�ļ�ת����ui_*.h�ļ��Ĵ��Ŀ¼
19. RC_FILE  ָ��Ӧ�ó�����Դ�ļ�������
    ���� RC_FILE += $$PWD/UrgBenri.rc
20. RC_ICONS
21. CODECFORSRC  ָ��Դ�ļ����뷽ʽ
22. ƽ̨��ش���
    �磺
    win32:RC_FILE += $$PWD/UrgBenri.rc
    macx:ICON = $$PWD/icons/UrgBenri.icns
    win32 {
        CONFIG += embed_manifest_exe
    }
23. ��Ƕmanifest�ļ�
    Qt4.1.3֮��İ汾�ṩ��CONFIGѡ�����ṩ��Ƕmanifest�ļ��Ĺ���
    CONFIG += embed_manifest_exe
    CONFIG += embed_manifest_dll��Ĭ�Ͽ�����
24. Qt���ñ���
    QMAKE_TARGET_COMPANY��ָ����ĿĿ��Ĺ�˾���ƣ���������Windows
    QMAKE_TARGET_PRODUCT��ָ����ĿĿ��Ĳ�Ʒ���ƣ���������Windows
    QMAKE_TARGET_DESCRIPTION��ָ����ĿĿ���������Ϣ����������Windows
    QMAKE_TARGET_COPYRIGHT��ָ����ĿĿ��İ�Ȩ��Ϣ����������Windows
    PACKAGE_DOMAIN��
    PACKAGE_VERSION��
    RC_CODEPAGE��ָ��Ӧ�ñ�������һ��.rc�ļ��еĴ���ҳ����������Windows
    RC_LANG��ָ��Ӧ�ñ�������һ��.rc�ļ��е����ԣ���������Windows
    RC_ICONS��ָ��Ӧ�ñ�������һ��.rc�ļ��е�ͼ�꣬��������Windows
    VERSION��ָ������汾��
    BUILD_NUMBER��
    APP_REVISION��
    APP_VERSION_DATE��
    APP_VERSION��
    ע�⣺QMAKE_TARGET_COMPANY��QMAKE_TARGET_DESCRIPTION��
    QMAKE_TARGET_COPYRIGHT��QMAKE_TARGET_PRODUCT��RC_CODEPAGE��RC_LANG
    ����������Windows�� ����ֻ����VERSION��RC_ICONS ���������ã�
    ����RC_FILE�� RES_FILE����û�б����õ��������Ч  
    
qmake֮CONFIG(debug, debug|release)
    CONFIG(debug, debug|release) �����﷨��ʲô�����أ�    
    ����������ǰ����Ҫ�жϵ�active��ѡ������ǻ����ѡ���һ�����ϡ�

    �� Qt ����У��������õĶ��� qmake������д��Ӧpro�ļ���
    ʵ���о�����Ҫ�� debug �� release ���ֱ���ģʽ ���ò�ͬ��ѡ��ȷ�˵���Ӳ�ͬ��
    ���������⣬�򵥿���qmake��manual�������˶���д��������������ݣ�
    debug {
        LIBS += -L../lib1 -lhellod
    }
    release {
        LIBS += -L../lib2 -lhello
    }
    �ܲ��ң���ô��ͨ����������������
    ����򿪿����ɵ�makefile�ļ����ᷢ�� ������debug����release�������������䶼��ͬʱ�����á�
    Ҳ����˵�������൱��
    LIBS += -L../lib1 -lhellod -L../lib2 -lhelloԭ��
    ���Ǻ�Υ��ֱ���ģ���ΪCONFIG����ͬʱ���� debug �� release����ֻ��һ������active
    �������������ֵ����ʱ��������õĴ���active״̬��
    ���磺
    CONFIG = debug
    CONFIG += release
    ...
    ��������£�release����active״̬������debug �� release ����ͨ������Ĳ��ԡ�
    ��ν��
        CONFIG(debug, debug|release) {
            LIBS += -L../lib1 -lhellod
        } else {
            LIBS += -L../lib2 -lhello
        }
    ��
        CONFIG(debug, debug|release)��LIBS += -L../lib1 -lhellod
        CONFIG(release, debug|release)��LIBS += -L../lib2 -lhello