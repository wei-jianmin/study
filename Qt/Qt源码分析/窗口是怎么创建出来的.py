qt version 5.9.0

以QWidget为例，QWidget继承自QObject
QWidget的构造函数中，调用QWidgetPrivate::init

窗口的创建，采用逆向分析法，首先确定，创建窗口，一定会最终用到win API，
根据这个思路，在qt源码中搜索RegisterClass，然后在搜到的文件中打上断点，
执行代码 QWidget wg; wg.show(); 最终定位在qwindowscontext.cpp中。
根据调用堆栈，可以看出
1   QWindowsContext::registerWindowClass      qwindowscontext.cpp     536  0x62a52e5a
        。。。
        wc.lpfnWndProc  = proc/*参数*/ = qWindowsWndProc
        wc.lpszClassName = cname/*参数*/ = "Qt5QWindowIcon"
        WORD atom = RegisterClassEx(&wc);
        d->m_registeredWindowClassNames.insert(cname);
        return cname;
2   QWindowsContext::registerWindowClass      qwindowscontext.cpp     481  0x62a53920 
        return registerWindowClass(cname="Qt5QWindowIcon", proc=qWindowsWndProc, ...);
3   WindowCreationData::create                qwindowswindow.cpp      605  0x62b60c53 
        QString windowClassName = QWindowsContext::instance()->registerWindowClass(w);
        WindowData result;      'typedef QWindowsWindowData WindowData;
        result.hwnd = CreateWindowEx(...);
        。。。
        return result;
4   QWindowsWindowData::create                qwindowswindow.cpp      1200 0x62a46b56 
        WindowCreationData creationData;
        QWindowsWindowData result = creationData.create(w, parameters, title);
            QWindowsWindowData类的定义：
                Qt::WindowFlags flags;
                QRect geometry;
                QMargins frame; // Do not use directly for windows, see FrameDirty.
                QMargins customMargins; // User-defined, additional frame for NCCALCSIZE
                HWND hwnd = 0;
                bool embedded = false;
                static QWindowsWindowData create(const QWindow *w,
                                                 const QWindowsWindowData &parameters,
                                                 const QString &title);
        。。。
5   QWindowsIntegration::createPlatformWindow qwindowsintegration.cpp 322  0x62a4d6d6 
        。。。
        QWindowsWindowData obtained = QWindowsWindowData::create(...);  //320行
        QWindowsWindow *result = createPlatformWindowHelper(window, obtained);  //334行
            retrun new QWindowsWindow(window/*来自于参数*/, data);
                QWindowsWindow继承自QWindowsBaseWindow继承自QPlatformWindow
                QWindowsWindow类中有成员QWindowsWindowData m_data， 
                m_data存放了data参数，也就是存放了QWindowsWindowData obtained对象
        return result;
6   QWindowPrivate::create                    qwindow.cpp             438  0xa562455  
        Q_Q(QWindow);   // QWindow * q = 对应QWindow对象的指针
        platformWindow/*QWindowPrivate的成员变量*/ = platformIntegration->createPlatformWindow(q);
        检查q是否有子控件，如果有，则创建这些子控件窗口
7   QWindow::create                           qwindow.cpp             619  0xa5627c2  
        Q_D(QWindow);
        d->create(false);
8   QWidgetPrivate::create_sys                qwidget.cpp             1478 0x9e0bf6   
        ...
        QWindow *win = topData()->window;   //1419行
            topData()  #这一步完成了extra和extra->topextra的创建，但extra->topextra->window是空的
                const_cast<QWidgetPrivate *>(this)->createTLExtra();
                    QWidgetPrivate::createTLExtra()
                        if (!extra)     #QWExtra *extra,是QWidgetPrivate的成员变量，QWExtra : QWindowExtra
                            createExtra();
                        if (!extra->topextra)  #QTLWExtra *topextra,是QWExtra的成员变量, QTLWExtra : QTopLevelWindowExtra
                            QTLWExtra* x = extra->topextra = new QTLWExtra;
                            初始化x成员变量
                return extra->topextra;
        if (!win) 
            createTLSysExtra(); #这一步完成了extra->topextra->window的创建
                extra->topextra->window = new QWidgetWindow(q); #QWindow *window，是QTLWExtra的成员变量
                extra->topextra->window->setMinimumSize();
                extra->topextra->window->setMaximumSize();
                extra->topextra->window->setOpacity();
                extra->topextra->window->setProperty();
            win = topData()->window;
        #经过上面这两部，extra、extra->topextra、extra->topextra->window都创建出来了
        。。。win->setFlags、win->setProperty、win->setScreen、win->setFormat等等
        win->create();  //1478行
        。。。
//  到这里先梳理一下：
        QWidget中d_ptr,指向QWidgetPrivate;
        QWidgetPrivate中有QWExtra *extra; /*qwidget_p.h:667*/
        QWExtra中有QTLWExtra *topextra;   /*qwidget_p.h:232*/
        QTLWExtra中有QWindow *window;     /*qwidget_p.h:163*/
        QWindow中有d_ptr,指向QWindowPrivate;
        QWindowPrivate中有QPlatformWindow *platformWindow;  /*qwindow_p.h:157*/
        QPlatformWindow派生QWindowsBaseWindow派生QWindowsWindow
        QWindowsWindow类中有成员QWindowsWindowData m_data;  /*qwindowswindow.h:338*/
        QWindowsWindowData中有HWND hwnd成员，存放着窗口句柄
9   QWidget::create                           qwidget.cpp             1338 0x9e01ad   
        Q_D(QWidget)
        。。。
        d->create_sys(...);
        d->setModal_sys();
        。。。
10  QWidget::setVisible                       qwidget.cpp             8179 0x9eca11   
11  QWidget::show                             qwidget.cpp             7782 0x9e9974   
12  qMain                                     main.cpp                15   0x401698   
13  WinMain *16                               qtmain_win.cpp          104  0x4030a5   
14  main                                                                   0x403f3d 

综上，在QWidget类中拿到窗口句柄的方法是：
    Q_D(QWidget);                          //QWidgetPrivate * const d = d_func()
    QPlatformWindow * w1 = d->topData()    //QTLWExtra *
                            ->window       //QWindow *
                            ->handle();    //QPlatformWindow *
    QWindowsWindow * w2 = reinterpret_cast<QWindowsWindow *>w1;
    HWND hwnd = w2->handle();              //m_data.hwnd
    但是实际上，这种方法并不可行，原因是d_func()是私有方法
    只有一个类中有Q_DECLARE_PRIVATE定义，才能在该类中使用这个宏
    一个变通的方法是直接使用d_ptr指针（这是QObject中的一个protected的成员）
    然后将该d_ptr指针转成QWidgetPrivate使用
    
    QWidget对象的winId()方法，得到的是否是窗口的句柄？
    winId()
        QWidget *that = const_cast<QWidget*>(this);
        that->d_func()->createWinId();
        return that->data->winid;
        //QWidgetData *data是QWidget的成员变量
    返回值是 14550978 = 0xDE07C2
    通过spy++获得的该窗口的句柄值为0XDE07C2
    说明这是窗口的句柄



