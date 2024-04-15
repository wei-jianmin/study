<catalog s0>
QApplication的功能
    QApplication app(argc,argv);
    ...
    return app.exec();
    app.exec()使得程序进入事件循环状态，响应用户操作。
父子对象关系
    对象的父子关系是在QObject中实现的，父对象删除时，会遍历删除子对象。对于可视控件，父对象删除时，
    还意味着不仅该父对象会从屏幕上消失，其子对象也会从屏幕上消失   
布局重定义父组件问题
    将一个组件加入到一个布局中时，qt会自动设置这个组件的父组件。这一点在qt官方文档中有描述。
    tips for using layouts
    when use a layout, you don`t need to pass a parent when constructing the child widgets.
    the layout will auto reparent the widgets (using set parent()) .
    so they are children of the widget on which the layout is installed.
    这段话是说，layout会自动重设widgets的parent。
    经测，即使Layout的构造参数为空，也会在setLayout时，同时为Layout及其子控件统一设置parrent。
    
    关于setLayout的补充说明：
    如果widget中已经安装了一个layout，则该widget中不能安装第二个layout，
    你必须先删除第一个layout（用layout()获取，然后delete），然后才能使用setLayout。
    而如果一个layout已经安装在widget_A中，后有将之setLayout到widget_B中，
    则后设置的那个才是真正生效的，即layout将真正存在于widget_B中，而不在widget_A中。
    总结：widget和layout是一个萝卜一个坑的关系：
    一个widget是一个坑，旧的萝卜不拿走，新的萝卜放不进；
    一个layout是一个萝卜，先放到A坑，又放到B坑，则最终在B坑。

    对比：
    QLayout *p = new QLayout(parent)    同时起设置布局+设置父对象的功能
    parent->setLayout(p)                跟构造函数设置parent功能相似
    p->setParent(parent);               仅设置父对象，不起设置布局的作用
    经测试：
    QLayout *p = new QLayout(parent) ； p为成为parrent的Layout
    p->addWidget(w1);                   会将w1的父设为parent
    p->setParrent(parent2);             
    p->addWidget(w2);                   会将w2的父设为parent2
伙伴
    只有label才能设置伙伴（setBuddy）,可以在label获得焦点时，将焦点转移到伙伴身上    
使窗体自动随控件的大小变化或显示隐藏，管理自身大小:
    layout()->setSizeConstraint(QLayout::SetFixedSize);
    这样会使用户不能修改窗体的大小，而又布局负责管理窗口大小。       
使用QUiLoader创建动态对话框
    QUiLoader可以动态加载ui文件，让我们可以动态的改变程序界面，
    而不用重新编译程序。但是这也增加了设计时的工作量：
    不能通过ui直接引用各个部件了，而需要通过动态窗口对象的
    findChild这样的函数来获取窗口中的子部件
    QUiLoader uiLoader;
    QFile file("a.ui");
    QWidget * dialog =  uiLoader.load(&file);
    if(dialog)
        QLabel *tbl = dialog->findChild<QLabel*>("label1");
    findChild是模板函数，可以返回与给定的类型和名字相匹配的子对象。
    使用QUiLoader，需要在pro文件中引用uitools模块：CONFIG+=uitools
动作QAction
    一个动作就是一个信号发射器，与普通的widget相比，
    它能自然的附着到菜单或工具栏上，也能独立存在
    （无法通过界面设计师拖放，但可以通过代码创建），
    动作与界面相关的元素常见的就是文本内容和图标，
    另外还支持快捷键和鼠标悬停提示。
    设置快捷键：
    setShortcut(QKeySequence::New); 使用新建的系统默认快捷键(Ctrl+N)
    setShortcut("Ctrl+Q");          使用指定的快捷键
信号槽
    QObject::sender()返回发出信号的对象的指针。
    例：QAction *act = qobject_cast<QAction*>(sender());
    emit是qt的关键字，会被c++预处理器转成标准c++代码，emit 信号函数(); 可以发送信号，与直接调用槽函数相比，
    使用信号槽的方式更灵活。但信号槽的使用前提是继承自QObject类，并在头文件中声明Q_OBJECT宏。
    通过connect连接的信号槽，还能通过disconnect切断关联。
菜单
    菜单QMenuBar
        QMainWindow的menuBar成员函数，会在第一次调用时，通过检查
        layout()->menuBar判断是否已创建了菜单，如果没有，该函数会自动创建菜单。
        该函数返回一个指向QMenuBar的指针。
        QMenuBar的成员函数addMenu，返回的是个QMenu指针。
        QMenu类有addAction、addSeparator、addMenu(子菜单项)等方法
    右键菜单
        为widget类控件设置右键菜单方法：
        控件调用setContextMenuPolicy(Qt::CustomContextMenu)使之能响应鼠标右键
        当控件发生鼠标右击时，会发出
        QLabel::customContextMenuRequested(const QPoint & pos)信号,
        响应该信号，并在响应的槽函数中调用QMenu的exec方法，即可弹出菜单。
        也可以重新继承实现QWidget::contextMenuEvent(QContextMenuEvent * event)
        当右击控件时，会调用该函数。
    QAction
        每个继承自Widget的对象都有addAction方法，但并不是任何控件调用该方法都有意义。
        对于菜单，添加QAction对象就是添加菜单项。
        对于工具栏，添加QAction就是添加工具项。
        对于QAction，可以设置文本、图标和提示，并将其信号连接到槽上。
    鼠标右键菜单
        所有widget控件都可以支持右键菜单
        void setContextMenuPolicy ( Qt::ContextMenuPolicy policy )
        Qt::ContextMenuPolicy枚举类型包括：
            Qt::DefaultContextMenu
                利用右键事件响应函数contextMenuEvent()来弹出右键菜单。
                意味着要重写contextMenuEvent( QContextMenuEvent * event )函数。
            Qt::NoContextMenu
                没有自己的右键菜单（会显示父控件的右键菜单）
            Qt::PreventContextMenu
                与NoContextMenu相比，处理不会顺延到parent。
                意味着所有的鼠标右击事件都将交给QWidget::mousePressEvent()
                和QWidget::mouseReleaseEvent()处理。
            Qt::ActionsContextMenu
                把部件的所有action（通过addAction方法添加）当做菜单显示出来。
            Qt::CustomContextMenu
                会发出QWidget::customContextMenuRequested(const QPoint & pos)信号，
                需要将该信号与菜单响应的槽函数连接。
    addAction方法
        菜单类有自己实现的addAction方法，也有继承自QWidget的addAction方法，
        后者接受一个QAction*参数，
        但这个继承自QWidget的addAction方法通常不会为添加的QAction*对象设置父对象，
        所以给菜单添加菜单项时，一般使用菜单自己实现的addAction方法。
        而QWidget的addAction方法主要配合contextMenuEvent(Qt::ActionsContextMenu)使用              
状态栏
    同菜单栏一样，调用statusBar函数获得状态栏QStatusBar指针，
    当主窗口中没有状态栏时，会自动创建状态栏。
    状态栏提供addWidget方法(可指定伸展因子)，同QLayout一样，
    他会自动为添加到里面的控件重定义父对象为QStatusBar。      
窗口
    窗口的销毁
        new一个窗口使，即使不指定父对象，并且不手动delete也没影响，
        因为Qt会对所有窗口进行跟踪，调用closeAllWindows将关闭议程程序
        的所有窗口，除非其中有的窗口拒绝了关闭事件。
    窗口的关闭与程序的退出
        通过重新实现QWidget::closeEvent函数，可以中途截取对这个窗口的
        关闭操作，并且可以确定到底是不是真的要关闭这个窗口。
        当最后一个窗口关闭后，QAppliction就自动结束，如果有需要，
        可以通过QApplication::LastWindowClosed(false)禁用这种行为，
        这样，该应用程序会持续保持运行，直到调用QApplication::quit();
        当用户关闭一个窗口时，默认行为是隐藏它，所以他还会保留在内存中。
        在窗口的构造函数中，使用setAttribute(Qt::WA_DeleteOnClose);
        可以告诉Qt在关闭窗口时，将窗口对象删除。
        Qt::WA_DeleteOnClose属性是可以在QWidget上设置的，
        用来影响这个窗口部件的行为的，诸多标记之一。
    非模态窗口
        通过show方式显式的窗口，为非模态窗口。
        show()可以让一个隐藏的窗口变为显示的、处于最上方的、激活的，
        但如果窗口本身就是显示的，则show()就不起作用了
        show()和hide()是对应的。
        raise()可以让一个本来已经显示的窗口成为顶层窗口
        activeWindow()可以让一个本来已经显示的窗口成为激活的窗口
    模态窗口
        窗口对象.exec()可以使窗口模态显示
        如果对话框被接受(QDialog::Accepted)，则exec返回true，
        否则返回false(QDialog::Rejected)。
        确定和取消按钮通过调用调用accept()方法和reject()方法关闭窗口。
    QApplication::topLevelWidgets()可以获取所有的顶层窗口。
    启动窗口
        qt内置了个启动窗口类，当主窗口有大量初始化工作要做，显示较慢时，
        可以预先显示一个启动窗口。
        QSplashScreen是一个内置的启动窗口类，可以显示简单的图片和文字。      
注册自定义类型
    自定义的类型，如果没有注册，是不能作为信号槽参数的，也不能和QVariant之间转化
    但将自定义类型注册一下，就可以了。
    注册的方法非常简单：Q_DECLARE_METATYPE(自定义类型);       
内置控件使用
    QMainWindow
        QMainWindow的中央区域可以被任意种类的QWidget窗口部件占用，如
        标准Qt窗口部件、自定义窗口部件、带有布局管理器的QWidget、
        切分窗口(splitter)、多文档窗口部件等。。
    QTabWidget
        内置了QStackedWidget，并提供控制Tab栏
    QTextBrowser
        QTextBrowser是个只读的QTextEdit子类，他可以显示带格式的文本。
        与QLabel不同，他会在必要的时候显示滚动条，同时还支持键盘和鼠标导航。
        QtAssist就是用该控件呈现帮助文档的。
    QTextEdit
        QTextEdit可设置用于显示编辑普通文本和富文本。并支持剪切板。
    QProgressDialog
        内置的进度对话框
    QInputDialog
        内置的输入对话框
    QPushButton
        对于Button类，虽然总是支持toogle信号，但只有在checkable状态下，
        才会发出该信号。
    QButtonGroup
        使checkable按钮互斥--只有一个处于选中状态。
    QAction
        QAction可以与任何创建部件关联
    QActionGroup
        QAction跟Button一样，也是可以设置checkable的，使用QActionGroup，
        可以使多个QAction互斥--只有一个处于选中状态。
    QTableWidget
        QTableWidget的单元格属性，比如他的文本、对齐方式等，都存在QTableWidgetItem中。
        QTableWidgetItem不是一个窗口部件类，而是一个纯粹的数据类。
        当用户在一个空单元格中输入一些文本的时候，QTableWidget会自动创建一个
        QTableWidgetItem来保存这些文本。实际上，QTableWidget会在每次需要新项的时候
        把所传递的项以原型模式克隆出来。
        QTableWidget::clear方法可以用来清空所有项或任意项，但只能清除内容，而不能清除格式。
        QTableWidget有多个子窗口部件组成。在他的顶部有个水平的QHeaderView，在他的左侧，
        有个垂直的QHeaderView，还有两个QStrollBar，在他的中间，还有个名为视口的特殊窗口部件。
        所有这些窗口部件都有方法被访问到。
        通过QWidget::item()函数，可以获得一个QTableWidgetItem指针。
        setItem(int row, int column, QTableWidgetItem *item)函数可以向表格中添加一个单元。
        调用setItem时，QTableWidget会拿到QTableWidgetItem的所有权，并在正确的时候自动将其删除。            
内置类使用
    QString
        QString::arg("替换字符串")会使用自己的参数替换最小数字的%n参数，返回替换后的QString。      
类型提升
    在ui设计工程师的右键菜单中有此选项，
    如自定义了一个NewLabel，继承自QLabel，则可以将QLabel控件提升为自定义的NewLabel
    在提升窗口中有个全局包含选项，控制包含自定义类的头文件时，使用<>还是""。
    但提升的自定义类型，在ui设计师界面下不能编辑自定义的属性和信号槽。
    要想在ui设计师界面下使用自定义的信号槽，可以在右键菜单中选择"改变信号/槽"，在弹出窗口中填入自定义的信号槽。
容器变形
    在ui设计师界面中，右键容器类控件时，有"变形为"选项，可以将本容器方便的变形为其它容器。  
自定义属性
    定义Q_PROPERTY的目的在于让元对象系统能了解该数据成员
    在使用qss设计控件样式时，可以对不同的属性设计不同的样式，这样当控件的属性改变时，样式也随之变化。
    修改也属性后，要重新刷新一下控件，新的样式才会显示，如：btn->style()->polish(btn); 
自定义实现全新窗口部件
    代码部分
        通过子类化QWidget，并重新实现一些用来绘制窗口部件和相应鼠标点击事件的处理器。
        QLabel、QPushButton、QTabWidget都是用这种方法实现的。
        如果使用Q_PROPERTY注册了属性，则在Qt设计师中使用这个窗口部件时，
        在Qt设计师属性编辑器里，哪些继承与QWidget的属性下面，将会显示这些自定义属性。
    Q_OBJECT宏是必需的。
    一般需要继承mousePressEvent、mouseMoveEvent、paintEvent三个方法。
    关于paintEvent
        当窗口第一次显示时，或窗口大小改变时，或窗口被遮挡部分得以显示时，会产生一个绘制事件。
        也可以通过调用QWidget的update()或repaint()方法强制产生一个绘制事件。
        repaint会要求立即重绘，而update则是把绘制事件放在队列里(多个连续绘制事件会自动合并)，
        并在下次处理事件时，才调用一个绘制事件。
        如果为窗口设置了Qt::WA_Staticcontents属性，那个窗口改变大小时，如果窗口变大，
        则绘制事件的区域为窗口新增的区域，如果窗口变小，不会引起绘制事件。
        如果没有设置过该属性，则每当改变窗口大小时，窗口的整个可见区域生成一个绘制事件。
    在Qt设计师中集成自定义窗口部件
        提升法：
            选择一个内置Qt窗口部件，但该窗口部件要和我们自定义的窗口部件有相似的接口。
            然后右键该控件，将该控件提升为自定义控件。
            缺点是无法对自定义的属性进行访问，也没法对这个自定义窗口部件自身进行绘制。
        插件法：
            【创建项目】-【其他项目】-【qt设计师自定义控件】 编译一个插件xxx.dll和xxx.a
            然后将这两个文件放入qt/qt5.1.1/5.1.1/mingw48_32/plugins/designer下
                自定义的控件是继承自QDesignerCustomWidgetInterface接口的。
                （需要通过宏Q_INTERFACES，告诉moc，继承的QDesignerCustomWidgetInterface是个接口）
                需要自己实现QDesignerCustomWidgetInterface的各个接口。
                Qt设计师会调用createWidget()函数创建自定义控件实例。
                在自定义控件类（头文件）的末尾，使用Q_EXPORT_PLUGIN2(插件名字,插件类名)宏，
                以导出必要的函数，确保Qt设计师可以使用该插件。
                如果想自定义多个控件，可以选择从QDesignerCustomWidgetCollectionInterface派生。
事件处理
    基本概念
        事件是窗口或qt自身产生的，如鼠标事件、窗口重绘事件、定时器事件等。
        大部分事件是用户操作产生的，但有些事件则是系统自行产生的，如定时器事件。
        当使用qt编程时，通常不需要考虑事件，因为当发生某些重要的事情时，qt窗口部件会发信号。
        但对于自定义控件，或我们希望改变原生控件默认行为时，就会使用到事件。
        一般使用控件时，主要使用信号，实现(制作)控件时，主要使用事件。
    事件机制
        Qt中的事件都直接或间接继承自QEvent。
        事件产生是，qt会创建一个事件对象，事件循环最终会调用QOjbect类的event方法，
        把这个事件传给目标对象。
        需指出的是，event函数自身并不处理事件，而是根据事件类型，调用相应的事件处理器。
        事件处理器的返回值反映事件是否被接受并得到了处理。
        如QWidget的event函数将鼠标、键盘、重绘事件分别教程mousePressEvent()、
        keyPressEvent()、paintEvent()这些特定的事件处理器进行处理。
        更多信息可参考“信号槽原理”一节。
    重新实现事件处理器
        ??所有事件都是QEvent的子类。qt中的事件类型有100多种，可通过QEvent::type()返回事件类型。
        ??QObject类中有virtual bool event(QEvent*e)方法，
        该函数接收到对象的事件，如果识别并处理了事件e，则应返回true。
        ??QWidget中的event()实现了把绝大多数类型的事件，提前传给特定的事件处理器，
        如mousePressEvent()、keyPressEvent()、paintEvent()等。
        ??Tab键和shift+Tab键是个例外，在Widget::event()中，调用keyPressEvent()之前，
        会做专门处理，达到控件焦点转移的效果，
        ??如果想在自定义的编辑器控件中，让tab键起到缩进作用，则不应该重载keyPressEvent事件，
        而是应该重载event事件，在这里面判断 event->type() == QEvent::KeyPress，
        如果相等，则可以 QKeyEvent *key_event = static_cast<QKeyEvent*>(event);
        注意处理完后，不要忘记调用QWidget::event()方法来让QWidget处理其它事件。
        ??重载event事件时，如果返回true，则表明事件处理完毕了，
        如果返回false，则系统还会自动调用父类的event方法。
        ??要想让控件响应键盘事件，除了重载event或keyPressEvent外，还可以使用QAction，
        QAction支持setShortcut方法，可以设置快捷键。
    安装事件过滤器
        QObject实例可以设置在收到事件之前，先让另一个QObject实例先监视这些事件。
        例如有一组输入框控件，我们想让在按回车键后，焦点自动转移到下一个输入框，
        一种办法是重载keyPressEvent，if(event->key()==Qt::Key_Enter) focusNextChild();
        另一种办法是使用事件过滤器：让输入框事件在收到事件前，先让他的父窗口监视事件。
        具体操作为：
            1. 调用installEventFilter(QObject*)，将父窗口对象注册为监视对象。
            2. 在监视对象(这里为父窗口)的eventFilter函数中处理目标对象(子控件)的事件。
        如果为一个对象安装了多个事件过滤器，则后安装的先调用，先安装的后调用。
    5种事件过滤方法（优先级由低到高）
        1. 重载特定事件处理器方法，如mousePressEvent等
        2. 重载event(),这种的优先级比第一种更高
        3. 安装事件过滤器，这种的优先级比第二种更高
        4. 为qApp（唯一的QAppliction对象）注册事件过滤器，
           此时应用程序中，每一个对象的每个事件，在发送到其它事件过滤器之前，
           都会先发到这个事件过滤器，所以他的优先级比第四种更高
           可以用这种方法配合调式，这样可以知道在崩溃前调用了什么事件。
        5. 子类化QAppliction，并重新实现notify()
           qt内部调用QAppliction::notify()来发送一个事件。
           这里是事件的源头。
    事件的传送流程
        QWidget的event方法把绝大多数常用类型的事件处理器（如QMouseEvent等）传递给特定的事件处理器，
        如mousePressEvent(),QWidget子类重载mousePressEvent()函数，就可自定义鼠标事件处理器了。
        tab键则是一种特殊情况：QWidget::event在调用keyPressEvent函数之前，会先把焦点传递给下一个窗口部件，
        所以如果我们要想把输入框控件实现tab缩进功能，则重载keyPressEvent函数是不管用的（已经晚了），
        需要重载event()方法，在这里面单独处理tab按键的情况，然后记得return QWidget::event(event);
        把其它event的情况仍然转交给QWidget::event(),
        如果在事件到达他的目标对象之前没有得到处理，也没有被目标对象处理，
        那么就会重复这个事件处理过程，只不过这次会把原目标对象的父对象，当做新的目标对象，
        重复，直到这个时间完全得到处理，或到达了最顶层的对象为止。
        对于窗口中的按键事件，当用户按下一个按键时，这个事件会发送给当前拥有焦点的控件。
        如果控件没有处理该事件，则发给他的父控件，知道最后的QDialog对象。
    事件循环
        当调用QAppliction::exec()时，就启动了事件循环，在循环中不断检查是否有事件发生，
        （猜想线程应该事件队列）并把这些事件发送给相应的QObject。
        当处理一个事件时，可能会同时产生一些其他的事件（暂时得不到处理），
        这些事件会追加到Qt的事件队列中
    某个事件响应耗时过多的应对措施
        如果在处理一个特定事件上耗时过多，就会导致界面无法响应。
        例如在一个事件响应中保存文件，则直到文件保存完毕，才会处理窗口系统产生的其他事件。
        一种解决办法就是考虑将界面无关操作放到子线程中处理。
        另一种比较简单的解决办法是在文件保存过程中经常调用QAppliction::processEvents()，
        这个函数告诉Qt先去处理其它没被处理的事件，然后再将控制权交还给该函数的调用者。
        实际上，exec()内部就是不停调用processEvents()的while循环。
        使用第二种方法存在一个潜在问题：即可能在文件完全保存完之前，用户关闭了窗口，
        从而导致不可预料的后果，对于这个文件，解决方式是将qApp->processEvents()换成
        qApp->processEvents(QEventLoop::ExcludeUserInputEvents)，即告诉Qt不处理事件队列
        中的用户输入事件（包括鼠标事件和键盘事件）。
    自定义事件
        1. 继承QEvent类，不用定义Q_OBJECT宏，
           注意QEvent的构造函数有个枚举类型的QEvent::Type参数，表明事件类型，
           对于自定义类型，这个枚举值应该在1000~65535之间，
           推荐使用int QEvent::registerEventType()静态方法获取一个系统分配的事件类型，
           该函数返回值会在1000~65535之间。
        2. 调用静态方法QCoreApplication::postEvent(QObject *receiver, QEvent *event, int priority)
           receiver为事件接收者，event为自定义事件对象，priority优先级一般采用默认值即可
           调用postEvent的线程和receiver可以在同一个线程中，也可以在不同的线程中
           举例：QCoreApplication::postEvent(&mainWindow,new MyEvent());
           不用担心MyEvent的释放问题，在接收线程中会帮忙释放该对象，
           可以在MyEvent的析构函数中打断点跟踪自定义事件是如何被释放的。
        3. 重载事件接受者的event方法
           根据事件类型，判断如果是自定义的事件，就处理并返回true，
           否则，调用父类的event方法并返回。
        举例：            
            1.  创建Qt Widgets Application
            2.  自定义事件
                #include <QEvent>
                class MyEvent : public QEvent
                {
                public:
                    MyEvent(int data);
                    ~MyEvent();
                    int data() {return _data;}
                private:
                    int _data;
                };
                MyEvent::MyEvent(int data) : QEvent(QEvent::Type(1001))
                {
                    _data = data;
                }
            3.  创建线程，在线程中发送事件
                #include<QThread>
                #include <QWidget>
                class MyThread : public QThread
                {
                public:
                    MyThread(QWidget *main_window);
                protected:
                    void run();
                private:
                    QWidget* _pmw;  //事件接收者
                };
                #include <QCoreApplication>
                MyThread::MyThread(QWidget *main_window)
                {
                    _pmw = main_window;
                }
                void MyThread::run()
                {
                    static int i=1;
                    while(_pmw)
                    {
                        sleep(3);
                        QCoreApplication::postEvent(_pmw,new MyEvent(i));
                    }
                }
            4.  重载接受者MainWindow的event方法
                bool MainWindow::event(QEvent *event)
                {
                   if(event->type() == 1001)
                   {
                       MyEvent* e = static_cast<MyEvent*>(event);
                       //处理自定义事件
                       return true;
                   }
                   return QMainWindow::event(event);
                }
            5.  main函数中：
                #include "myevent.h"
                #include "mythread.h"
                int main(int argc, char *argv[])
                {
                    QApplication a(argc, argv);
                    MainWindow w;
                    w.show();
                    //a.postEvent(&w,new MyEvent(3)); 本线程发送自定义事件
                    MyThread t(&w);  //新线程中发送自定义事件
                    t.start();
                    return a.exec();
                }           
样式表
    基本语法
        选择器｛属性：值;｝
        当只有一条属性值时，末尾的分号可以省略，如果多条，则需用分号隔开
    选择器
        基本选择器
            通用选择器           "*"
                匹配程序中的所有widget
            类选择器             "类名"
                匹配指定类及其所有派生类
                如 QPushButton{color:red;}
                当类在命名空间中时，将命名空间和类名用--隔开
                如 utils--QPushButton
                之所以不用::隔开，是因为:表示另一种选择器
            类选择器2            ".类名"
                匹配指定类（不匹配其派生类）
                等价于 *[class~="QPushButton"]
            对象选择器(id选择器) "#对象名"
                根据对象名匹配特定对象 (大小写敏感)
                如#button_1 {color:red;}
                可以跟类选择器连用，如QPushButton#okButton
                注意：对象名虽然规范上允许有空格，但这里的对象名不能有空格
            属性选择器           "[属性=值]"  "[属性|=值]"  "[属性~=值]"
                "[属性=值]" 匹配某属性为特定值的所有控件
                "[属性|=值]" 匹配某属性以特定值开头的所有控件
                "[属性~=值]" 匹配某属性包含特定值的所有控件
                             这里的包含，指值要是单独的，亦即值的前后要与其他词有空格隔开
                             例：[objectName~="button"] {color:red;}
                这里的属性指的是用Q_PROPERTY声明的属性，且属性要受QVAirant::toString()支持
                可以跟类选择器连用，如QPushButton[flat="false"]
        复合选择器
            后代选择器           " " （空格）
                后代指的是各级子元素
                后代选择器可以通过空格一直延续下去，如: 选择器1 选择器2 选择器3{属性:值;}
                各级选择器可以使用任意一种基本选择器
            子元素选择器         ">"
                >前后虽然可以有空格，但不建议写空格
                子元素选择器只会找下级子元素，而不是各级子元素
                子元素选择器不能通过">"一直延续下去，只能有一个">"
                ">"前后可以使用任意一种基本选择器（一般使用类选择器2）
            并集选择器           ","
                将每个单独选择器匹配到的控件放到同一个结果集合中
                格式： 选择器1,选择器2,选择器3{属性:值;}
        特殊选择器
            子控件选择器         "::"
                这里的子控件，是指“复合型控件”的组成元素，
                如QSpinBox的上下箭头，文本框的滚动条等
                格式： 类选择器::子控件{属性:值;}  类选择器2::子控件{属性:值;}
                举例： QComboBox::down-arrow{ image:url(:/res/arrowdown.png);}
            伪类选择器           ":"
                格式： 类选择器:状态{属性:值;}  类选择器2:状态{属性:值;}
                举例： 如鼠标悬浮在按钮上时 QPushButton:hover{color:white;}
                       状态可以用！取反，如QPushButton:!hover{color:white;}
                多个状态可以通过":"进行连接，如 QCheckBox:hover:checket{color:red;}
                表示该选择框在“为checked，且鼠标在上面”时，前景色为红色。
                伪类选择器也支持","取并集，如QCheckBox:hover,QCheckBox:checket{color:red;}
                伪类选择可以和子控件选择器连用，如QComboBox::drop-down:hover{ ...; }
        没有选择器的情况
            如果没指定选择，相当于选择了本对象及其所有子对象
    选择器的结合规律
        例：QDialog QComboBox,QLineEdit 会被理解为 (QDialog QComboBox),QLineEdit
    层叠性
        如果一个控件被多次设置了样式，则后面的样式会覆盖前面的样式。
    继承性
        与CSS不同，一个widget默认不会自动继承父控件的字体和颜色。
        相反的，通过设置widget的setFont()或setPalette()，则会影响到其子控件。
        通过QCoreApplication::setAttribute(Qt::AA_UseStyleSheetPropagationInWidgetStyles,bool);
        可以控制样式表的继承性。
    优先级
        给控件直接设置的样式 > 给QAppliction设置的样式， 即使QAppliction中的选择器优先级更高
        选择器越特殊、越精确，其优先级越高
        id选择器 > 类选择器2 > 类选择器 > 通配符 > 继承 > 默认
    盒模型
        所有的widget，都可以被看做一个“盒子”，
        一个“盒子”包括 外边距(margin)、边框粗细(border)、内边距(padding)、内容区域(content)
        外边距指边框周围一定区域内，不能有其它控件
        边框有自己的颜色，不受盒子背景色的影响
        内边距受盒子背景色影响
        控件的width和height，指的是整合盒子的宽度或高度，
        width = 左外边距 + 左边框宽度 + 左内边距 + 内容宽度 + 右内边距 + 右边框宽度 + 右外边距
    设置控件属性
        从Qt4.3开始，控件的所有的Q_PROPERTY属性，可通过“qproperty-<属性名>”的语法形式设置，
        如： MyLabel {qproperty-pixmap : url(pixmap.png);}
             QPushButton {qproperty-iconSize : 20px 20px; }
             MyGroupBox { qproperty-titleColor: rgb(100, 200, 100); }
    样式表与窗口绘制事件
        经测，重载窗口绘制事件函数，并在其中改变该控件背景色，同时，又对该控件设置了样式表，
        结果，样式表会最终影响控件的颜色，这是因为在paint绘制函数中，会调用设置样式表，
        而样式表的设置在调用子paint方法之后。
        定外，设置样式表函数setStyleSheet也会主动触发窗口重绘。
    样式表使用建议
        建议使用全局样式表，而不是给每个控件分别设置样式表，一是便于统一管理，
        二是从内部实现代码上分析，如果分多处设置样式表，就会创建多个样式表对象，
        发送多处设置样式事件，引发多次重绘，所以从效率方面考量，不建议多处设置样式表。
模型视图结构
    与MVC的关系
        MVC包括三个元素：(数据)模型、视图、控制（用户在界面上的操作）。
        QT的InterView框架，把视图和控制结合在一块统称为视图，
        于是有了模型/视图结构。
        InterView框架还引入了代理的概念，
        通过代理，能自定义数据条目(item)的显示和编辑方式。
    模型、视图、代理的关系
        数据改变时，模型发出信号通知视图
        当用户对界面进行了操作，视图会发出信号
    模型
        如链表模型（QList）、堆栈模型（QStack），就是最简单的数据模型
        这里的模型类与之类似，只不过维护的数据元素之间的关系更复杂一些
        但是所有这些模型类，基本都是提供对内部数据元素的增删改查的功能
        另外，模型类一般都会提供不少信号接口，
        当内部数据发生某种特定变化的时候，就会发出相应的信号
        模型除了与视图关联使用外，也是可以单独使用的，用于记录管理数据
        所有的模型都基于QAbstractItemModel类。
        QAbstractItemModel
            QAbstractTableModel         表模型（抽象的，不能直接用）
                QSqlQueryModel
                    QSqlTableModel
                        QSqlRelationTableModel
            QAbstractProxyModel
                QIdentityProxyModel
                QSortFilterProxyModel
            QAbstractListModel          列表模型（抽象的，不能直接用）
                QStringListModel
                    QHelpIndexModel
            QStandardItemModel          标准模型（具体的，可以直接用）
            QHelpContentModel            
            QFileSystemModel            树模型（具体的，可以直接使用）
            QDirModel                   树模型（具体的，可以直接使用）
        QAbstractItemModel类介绍
            如链表模型（QList）、堆栈模型（QStack），就是最简单的数据模型
            QAbstractItemModel类与之类似，只不过维护的数据关系更复杂一些
            QAbstractItemModel类提供有对内部数据元素的增删改查的功能，
            如insertRow、match、sort、index、columnCount等
            QAbstractItemModel的派生类，则是对内部维护的数据元素之间的关系
            进行了更具体一些的划分：如表格型、列表型、目录型等等，
            注意，针对每种数据模型，一般也会定义专有的类来存放数据元素，
            从而为每种数据模型的专有的管理策略，提供底层支持。
            值得一提的是，QAbstractItemModel还提供了发送信号的能力，
            当内部的数据发生某些变化时，会发出特定的信号来表征这些变化
        QStandardItemModel介绍
            维护的是数据成员的类型为QStandardItem
                item通常包含文字、图标和选择框
                每个item可以有自己的背景色、字体、前景色
                默认的，每个item是enabled、selectable、checkable、editable
                你可通过调用setFlags控制上面那些可以，哪些不允许。
                可以调用setCheckState改变其选中状态
                每个item都有一个二维的子item表（使得他支持层级嵌套）
                    子表通过setRowCount和setColumnCount改变大小
                    可以通过setChild将一个item填放到子表中，
                    可通过child获取子表item的指针
                    另外还支持insertRow,insertColumn,appendRow,appendColumn，
                    removeRow,takeRow,removeColumn,takeColumn,sortChildren等
            使用该模型，你可以方便的实现成一个树模型
                使用appendRow，可以将多个items添到到模型中
                使用item访问某个item
            也可以方便的实现成一个表模型
                通常将表的尺寸传递给QStandardItemModel构造函数，
                并使用setItem（）将项目定位到表中
                可以调用setRowCount和setColumnCount来改变表的尺寸
                可以调用insertRow,insertColumn,removeRow,removeColumn
            使用setHorizontalHeaderLabels/setVerticalHeaderLabels设置表头
            还使用findItems定位元素，使用sort排序，使用clear清空
        继承抽象表模型
            因为表中的数据类型是不确定的，如可能是数字、文字或图片，
            所以数据存储维护应该是定义在继承类中的。
            继承时必需实现rowCount(),columnCount(),data()三个函数。
            建议重新实现headerData()函数--
            --因为表头是不算在表中的，所以不能通过data()/setData()访问。
            如果该模型支持编辑功能，则还应该实现setData()函数，
            并实现实现flags()函数，该函数返回值标记条目是否可编辑。
        继承抽象列表模型
            必需事先rowCount(),data()两个函数。
            建议重新实现headerData()函数
            如果该模型支持编辑功能，则还应该实现setData()函数，
            并实现实现flags()函数，该函数返回值标记条目是否可编辑。
            如果想支持列表增减条目，则应该实现insertRows()和removeRows()，
                实现insertRows时，在将行插到结构前，应先调用beginInsertRows()
                之后应立即调用endInsertRows()
                实现removeRows()时，同理，调用beginRemoveRows和endRemoveRows
                这样做是为了能够在模型变化时，自动通知关联的视图。
        QDirModel与QModelIndex
            QDirModel在一构造出来之后，就先在构造函数中枚举了根目录下的所有文件
            与QDirModel关系密切的是QModelIndex
                QModelIndex记录模型中元素的索引值，
                可由一个绝对路径得到一个索引，
                也可以根据一个索引得到一个绝对路径，
                根据这个索引，QDirModel可以获取文件的放多信息，
                如名字、图标、文件信息等
                也可根据这个索引删除文件、判断是否有子文件、设为只读等。
            QDirModel是在本线程中执行的
                所以在枚举子目录时，可能会卡死当前线程，
                导致界面暂时没有响应。
            QDirModel中有行和列的概念
                列代表的是第几级路径，  ---错误
                    如C盘或D盘这样的根目录，是第0级路径，所以列=0，
                    如C:/123是一级路径，所以列=1，
                在树模型中，QModelIndex没有使用列（总是0）
                在树模型中，对于子目录/文件，存在parent()。
                行代表的是该文件是当前目录下的第几个文件（与排序方式有关）
                    如C盘一般是第0个文件，所以行=0，
                    而D盘一般是第1个文件，所以行=1
        QFileSystemModel与QDirModel的区别
            QFileSystemModel是拥有独立线程的
                对于文件目录的获取也是异步方式的
                比如，当你创建了 QFileSystemModel的对象，
                并且setRootPath后，rowCount返回值依然是 0，
                因为枚举目录的操作是异步的可能还没开始呢，这点和QDirModel不一样
            当Model发现目录数据有变化的时候 
            再通过一些Model的信号通知它所在的ItemView，
            从而完成这个异步的目录枚举过程。
            还有一个好处就是 QFileSystemModel内置了对目录变化的监视，
                这是通过 QFileSystemWatcher 类来实现的，
                所以用QFileSystemModel就不用担心目录文件变化了，
                当有变化发生ItemView自然会收到更新的信号。
        QSortFilterProxyModel简介
            该类之所以称为代理模型，是因为他不是真正的数据模型，而只是关联数据模型，
            换句话说，他不持有item数据，而仅是处理（过滤、排序）数据，
            他需要setSourceModel与真正的数据模型相关联。
            之后视图控件不是直接跟原始数据模型绑定，而是与该代理数据模型绑定。
            该代理模型通过重载filterAcceptsRow方法，根据传来的int sourceRow,
            获取模型相应节点的值，通过返回bool值，决定是否把该条(行)过滤掉。
            程序运行时，可在改变过滤条件参考值（成员变量）后，调用invalidateFilter
            告诉代理模型过滤条件已改变，模型内部调用filterAcceptsRow方法，
            更新过滤后的内容，并把这种改变反映到视图控件上。
    视图
        所有视图类都基于QAbstractItemView
        QAbstractItemView
            QTreeView          树
                QTreeWidget
            QHeaderView
                QUndoView
                QListWidget
            QListView          列表
                QUndoView
                QListWidget
            QColumnView        横向列表
            QTableView         表
                QTableWidget
    代理
        代理的基类为QAbstractItemDelegete
            QAbstractItemDelegete
                QItemDelegate
                    QSqlRelationalDelegate
                QStyledItemDelegate
    模型索引
        为了保证数据的存取和表示的分离，InterView引入了模型索引的概念，
        也就是说，模型索引是联系模型与视图的纽带：
        每个信息条目通过模型索引来获取，视图和代理使用索引来存取数据。
        通过模型索引来存取数据条目，必须有三个属性：行号、列号、父索引。
            列表模型的索引，只用到行属性
            表模型索引，需用到行和列属性
            树模型索引，则用到行和父索引属性
        模型索引只是提供了临时索引的功能，因为数据模型是可能会改变的，
        模型可能会对内部的结构进行重新组织，此时模型索引将失效。
        如果索引要长期使用，可以使用QPersistentModelIndex来保存模型索引。
    集成了视图和模型的控件
        如QListWidget、QTreeWidget、QBableWidget等
        他们集合了视图和模型的功能
        使用这些类虽然简便，但也失去了模型/视图结构的灵活性。
    关联模型和控件
        对于tableView、listView这样的控件，是可以通过setModel方法，
        与模型进行关联的。
        而如果想让一个QLineEdit、QLineEdit、QLabel这样的控件跟模型相关联，
        有什么办法呢？ 方法就是使用QDataWidgetMapper类，
        通过这个类的addMapping(QWidget *widget, int section)或
        addMapping(QWidget*widget,int section,QByteArray &propertyName)
        方法，即可将模型与上面这样的控件进行关联
        widget参数填入要关联的控件，section参数一般是填对应模型中的第几列
        至于对应第几行，则可以通过setCurrentIndex(int index)控制
        propertyName参数用以指定使用模型中取到的数据修改控件的什么属性，
        如果不使用该参数，则默认修改的是控件的文字属性。
        另外，如果将模型关联到一个可输入的文本框上，
        则可以控制修改文本框内容时，要不要同步到模型中去，
        可以通过setSubmitPolicy(SubmitPolicy policy)来控制同步策略，
        如果是自动同步，则文本框的修改，会自动同步到对应的模型条目中，
        如果是手动模式，则需调用submit方法后，才会文本框内容同步到模型。
        注意：一个控件同时只能关联到一个模型，
        一个模型中的item项同时只能关联到一个控件。
    代理
        搜setItemDelegate，可以发现下列类（及其子类）有此成员方法：
            QAbstractItemView
            QDataWidgetMapper
            QFileDialog
            QComboBox
        listView、tableView、treeView等控件，本身只是按列、表、树
        形式展示了一些基本空间，如表头、展开按钮、网格线等，
        而具体到每个item内容的显示完全是靠代理展现的，
        这样做的目的是为了让控件的使用者能够更自由的定制item的展示形式，
        默认，他们用QItemDelegate这个类所代理，
        该类继承自QAbstractItemDelegate，
        并实现了paint()，sizeHint()等必要方法，
        我们也可以继承该类，创建我们想要的代理类，
        当为一个控件设置新的代理类时，原有的代理类将被顶替掉
        QAbstractItemView不会自动将代理类对象设为自己的子对象，
        所以当旧的代理类被顶替掉时，它就真的只是被顶替掉，而不会自动删除
        怎么用
            createEditor 
                当你想让item在某些情况下显示为特定的控件时，考虑重载该方法
                当编辑某条目时，才会调用到该方法
                你可以使用option参数的column、row方法作为控制条件，
                控制是否要创建新控件，或者什么情况下创建什么控件，
                也可以使用item的data(Qt::DisplayRole)作为控制条件
            setEditorData 
                重载该方法，将模型数据中的内容展现在item上
            setModelData
                重载该方法，将item中的数据（编辑后）回存到数据模型中
            paint
                一般不重载该方法，注意paint传来的几个参数多数都是const的
                所以不能修改这些参数（如果要使用，可根据参数构造一个内部对象）
                可直接调用painter参数的绘制方法（进行先期背景绘制）
                但测试时发现一个问题，当拖动滚动条时，不会自动调用该方法，
                所以会导致显示区域混乱（可考虑用信号槽将这两个操作关联起来）
            updateEditorGeometry
                重载这个方法设置创建的控件（参数传来的就是创建的控件）的位置
                一般是editor->setGeometry(option.rect);
    支持拖放
        如果是QListWidget、QTableWidget或QTreeWidget，
        可以直接调用如下方法使其支持拖放
            setSectionMode(QAbstractItemView::SingleSelection);
            setDragEnabled(true);
            setAcceptDrops(true);
            setDropIndicatorShown(true);
        如果是视图-模型支持拖放，则处理在视图中调用如上方法外，
        还需要重载实现模型的相关方法（参精通Qt4编程 第2版 481页）
        关键的是两个函数mimeData和dropMimeData,
        前者在拖动时把item数据放入剪切板，
        后者在鼠标放下时，从剪切板取数据放到模型item中
    选择
        使用QAbstractItemView::setSelectionModel(QItemSelectionModel*)设置选择模型
        QItemSelectionModel支持setModel(QAbstractItemModel*)方法与模型关联
        select(const QModelIndex&, QItemSelectionModel::SelectionFlags)
        select(const QItemSelection&, QItemSelectionModel::SelectionFlags)
        setCurrentIndex(const QModelIndex&, QItemSelectionModel::SelectionFlags)
        上面三个函数用以控制选择区域
        当选择发生变化时，QItemSelectionModel会发出相应信号
        上面参数中，QItemSelection是一个根据QModelIndex topLeft:bottomRight确定的范围
        并支持merge方法，可以把别的QItemSelection合并到当前QItemSelection        
编辑框自动补全
    QCompleter可以为QLineEdit或QComboBox提供输入自动补全功能，
    这两个控件支持setCompleter(QCompleter*)方法，
    而QCompleter则是支持setModel(QAbstractItemModel*)，
    并以指定的数据模型为参照，为控件提供输入建议。
    例：
    QDirModel * dir_modle = new QDirModel(this);
    QCompleter *comp = new QCompleter(this);
    comp->setModel(dir_modle);
    ui->lineEdit->setCompleter(comp);  
实现撤销/重做功能
    自定义相应的撤销重做类，继承自QUndoCommand类，
    继承实现void undo(); void redo(); 两个函数。
    定义QUndoStack成员变量，该类从名字就可以看出，是个栈结构
    支持栈操作push(QUndoCommand *cmd), 及undo()/redo()方法。
    createUndoAction/createRedoAction方法，
    则是在调用redo或redo的同时，还创建一个redo或undo的QAction
    使用例子可参考《精通Qt4编程 第2版》452页前后。   
图片处理与2D绘图
    QPainter
        支持绘制点、先、矩形、多边形、路径等，
        线和轮廓使用QPen进行绘制，画刷(QBrush)进行填充
        画笔定义线型、宽度、笔尖、端点，
        画刷定义填充模式也颜色
        使用QFont定义绘制文字的特性
        字体的属性可通过QFontInfo类获取
        字体的度量使用QFontMetrics类获取
        QFontDatabase类可得到系统所支持的字体信息的列表
        QPainter使用RenderHint来控制是否反锯齿
        QPainter接受QPaintDevice *作为参数（作为画布）
    QImage
        继承自QPaintDevice，优化了I/O操作，可以直接操作像素数据
        可以用QPainter直接在QImage上绘图，
        除了绘制文字(QFont依赖底层 GUI),其它绘制操作可以在线程中完成
        如果想在线程中绘制文字，可以用QPainterPath
        QImage对象具有隐式共享特性
        QIamge通过scanLine返回指定行的数据
        bits()函数返回第一个像素的指针，每个像素在QImage中都是用整数表示。
    QPixmap
        继承自QPaintDevice，主要用来在屏幕上显示图像数据
        也能对图像进行一些图像变换，如缩放、遮罩、变形。
        可以方便与QImage互转，在windows上，QPixmap还能与HBITMAP互转
        QPixmap主要用于屏幕后台缓冲区绘图，
        QPixmap对象可以用QLabel(pixmap)或QAbstractbutton(icon)子类显示。
        QImage对象具有隐式共享特性
    QBitmap
        从QPixmap继承，只能处理二值图像（单色位图）
    QPicture
        是可以记录和重放QPainter命令的类
    QPainterPath
        图形类（矩形、椭圆、直线、曲线等）
        QPainterPath类可以执行各种绘制图形的命令
        QPainter有drawPath方法，可接受QPainterPath对象
        绘图路径可以填充、显示轮廓、裁剪等
        使用举例：
          QLinearGradient myGradient;
          QPen myPen;
          QRectF boundingRectangle;
          QPainterPath myPath;
          myPath.addEllipse(boundingRectangle);
          QPainter painter(this);
          painter.setBrush(myGradient);
          painter.setPen(myPen);
          painter.drawPath(myPath);
    图像混合（图层叠加模式）
        只支持ARGB32或ARGB32_premultiplied格式,优先使用后者
        设置了混合模式后，对所有的绘图操作都有效，如画笔、画刷、渐变、图片
        混个模式参：QPainter::CompositeMode
        相关混合算法参精通Qt4编程 第二版 202页
    坐标变换
        Qt的坐标有QPainter控制，同时也由QPaintDevice和QPaintEngine类控制
        QPaintdevice类是所有绘图设备类的基类，
        QWidget、QPixmap、QImage、QPrinter等都是其子类。
        QPainter是在QPaintDevice上绘画，两者之间存在映射关系
        通过QPainter的scale()、rotate()、translate()、hsear()等函数，
        可以改变其映射关系，
        所有变换操作的变换矩阵可以通过QPainter的worldMatrix()函数取出,
        QPainter的save()和restore()函数可以压栈和弹栈当前的变换矩阵，
        所以可以在进行变换前先压栈一下，要恢复时，只需弹栈即可。
        为了实现更复杂的变换，还可通过setMatrix设置变换矩阵。
字体
    QFont表示字体，当创建字体对象时，qt会使用指定的字体，
    如果没有，则会寻找一种最接近的已安装字体。
    字体信息可通过QFontInfo取出
    QFontMetrics类可以获得字体的相关数据
    exactMatch函数可以判断底层窗口系统中是否有完全对应的字体
    QAppliction的setFont方法可以设置应用程序的默认字体
    更多信息参看精通Qt4编程P184
拖放
    通过QApplication::startDragTime设置用户按下鼠标多长时间才开始一个拖放操作，默认500ms
    通过QApplication::startDragDistance设置鼠标移动多少像素才开始拖动，默认4pix
    作为拖动的源
        在mousePressEvent函数中
        QMimeData *mimeData = new QMimeData;
        mimeData->setText(...);
        QDrag *drag = new QDrag(this);
        drag->setMimeData(mimeData);
        drag->setPixmap(拖动时使用的图片);
        Qt::dropAction act = drag->start();
        QMimeData是MIME类型数据的一个容器类，剪切板操作也会用到该类
        QMimeData中可以存放（同时只能是一种）image/text/html/urls/二进制数据
        Qt::dropAction是个枚举值,标识是移动数据、还是拖动数据等
    作为目的地  
        需先调用setAcceptDrops(bool)设置窗口部件是否接口拖放
        如果支持，则需继承实现dragEventEvent和dropEvent两个事件函数
        dragEventEvent在鼠标进入目标widget时产生，
        传来QDragEnterEvent* event参数，
            QDragEnterEvent继承自QDropEvent，进而继承自QEvent
            QMimeData * p = event->mimeData();
            然后判断传来的数据是否符合要求，
            符合的话，则event->accept(),否则event->ignore();
            前者设置一个accept标记（QEvent的方法），
            表明事件的接受者想要该事件，
            否则，这个事件可能被传到父widget，
            后者会将鼠标变成进制拖放的形状。
        dropEvent函数传来QDropEvent*event参数
            QMimeData * p = event->mimeData();
            拿到QMimeData中的数据，并设置控件使用该数据
            不要忘记仍然使用event->accept()，
            否则该事件还会继续传到父widget。
            而对于不符合的数据类型，调用event->ignore()
    作为被拖动的对象
        为了接受拖来的数据，需实现dragMoveEvent和dropEvent函数
    定义新的拖放操作类型      
文件管理
    获取文件信息
        通过QFileInfo，可以获取文件名、文件路径、存取权限、
        是否为目录或符号链接、文件大小、最后访问时间等信息，
        这些信息会被缓存，如果不想缓存，使用setCaching(false)
        由于文件可能中间被改变，所以还提供了refresh函数
    监视文件变化
        使用QFileSystemWatcher来监视文件或目录的改变
        通过addPath或addPaths函数来监视一个或多个文件/目录
        当监视的文件被修改或删除时，会发出fileChanged信号。 
进程线程
    创建线程的方法
        参https://www.cnblogs.com/findumars/p/5641570.html
        方法一：继承QThread
            1.继承QThread并重新实现run函数
            2.创建QThread派生类的实例
            3.调用实例的start方法启动线程、
            ??调用实例的terminate方法结束线程
            ??调用terminate后，不会立刻终止这个线程，而是取决于系统的调度策略
            ??调用wait方法等待线程安全退出
            需注意的是terminate可能在线程执行的任意一步终止，导致不可预知的后果所以不提倡使用
        方法二：继承QRunnable
            1.继承QRunnable类，实现run函数
            2.使用QThreadPool::globalInstance()->start(QRunnable*)运行一个线程任务
            说明
                QRunnable类不继承任何基类，所以其没有信号槽等特性
                QRunnable默认是自动删除的，可以通过setAutoDelete进行修改
                QThreadPool可以对同一个QRunnable实例创建多个线程执行
                当QThreadPool执行完最后一个QRunnable实例时，如果他是自动删除的，则QThreadPool会删除它
                每个qt程序都有一个全局的QThreadPool对象，可通过QThreadPool::globalInstance()获取其指针
            优缺点分析
                这是线程池技术，QThreadPool维护线程池队列，并管理当前运行线程的数目
                使用 QThread::idealThreadCount()可以知道线程池默认使用了多少个线程
                一般无需设置，qt会选择最优线程个数，当然也可以通过maxThreadCount函数手动设置
                其缺点就是无法手动强制关停某个QRunnable（因为QRunnable只是任务队列中的一些任务）
        方法三：使用moveToThread
            这是QObject中的方法：void QObject::moveToThread(QThread *targetThread)
            这个函数的功能是将当前类(继承自QObject，且不能有parrent)及其children移到参数指定的线程中
            使用举例：
                QThread thread;
                thread.start();              
                Worker work;                    //Worker是继承自QObject的对象
                work.moveToThread(&thread);     //让Worker依附于thread线程
                之后，work对象的事件处理将会在thread中进行，换句话说
                当信号触发work中的槽函数时，该槽函数是在thread中执行的
                注意QThread的声明周期不能小于Worker的声明周期（即不能提前析构）
            如果moveToThread参数传入0，意味着没有线程来执行work中被信号触发的槽函数
            该方法不推荐使用
        方法四：QtConcurrent::run
            QtConcurrent是个命名空间(qt4.4开始引入)，它提供了了一些高层api，
            用于取代互斥量、读写锁、条件变量、信号量等底层操作。
            QFuture<T> run(QThreadPool *pool, Function function, ...)
            QFuture<T> run(Function function, ...)  //等同于将上面的pool赋值为QThreadPool::globalInstance()
            使用线程池执行指定的函数，注意因为线程池任务队列的关系，函数可能不会立即执行
            run函数的function参数，传入的是个函数的指针(即函数名)。
            run函数最后的...参数，实际是qt为不同个数的参数重载了不同的run函数，最多支持5个参数。
            返回值QFuture类，用于表示异步计算的结果，result函数用于获取返回结果，
            pause()、resume()、cancel函数用于启停控制，waitForFinished用于等待线程结束。
            注意result和waitForFinished两个函数均是阻塞函数，直到有可用的返回值或线程结束。
            跟线程池一样，通过QtConcurrent::run函数启动的线程无法手动结束。
    线程的互斥与同步
        互斥量QMutex
            QMutex提供了一种保护临界区的方法，每次只允许一个(线程)访问这个临界区
            多个线程都可访问同一个QMutex对象，但只要有一个线程lock住该对象，
            其它线程再lock时，就会卡住，只有当之前lock成功的线程unlock之后，
            才会有新的线程lock成功。
            QMutex还提供tryLock方法，如果互斥量对象已被其它线程锁定，则立即返回。
            QMutexLocker是个操作QMutex的工具，QMutexLocker(QMutex*)，
            它在构造时，会调用mutex的lock方法，析构时自动调用unlock方法。
            QMutex的构造函数允许指定一个RecursionMode参数，
            如果是QMutex::Recursive模式，则一个线程可以对同一个mutex锁定多次，
            而且只有在解锁相应次数后，mutex才会真正解锁
            而如果是 QMutex::NonRecursive（默认），则只能同时锁定一次。
            成员方法：                
                void lock()
                void unlock()
                bool try_lock()
                bool tryLock(int timeout = 0)
                bool try_lock_for(std::chrono::duration<Rep, Period> duration)
                bool try_lock_until(std::chrono::time_point<Clock, Duration> timePoint)
        读写锁QReadWriteLocker
            类似QMutex，其实就是个“独占/共享锁”，
            当作为独占锁而锁定时，其它线程无法再作为独占锁或共享锁而锁定，只能等待
            当作为共享锁而锁定是，其它线程可以作为共享锁而再次锁定，但不能作为独占锁而锁定
            QReadLocker/QWriteLocker：类比QMutexLocker，是个使用读写锁的辅助小工具，
            在构造时给读写锁上锁，在析构时给读写锁自动解锁。
        信号量QSemaphore
            成员方法：
            QSemaphore(int n = 0)           
            void acquire(int n = 1)  //申请一定数量的资源，资源数量不够时阻塞
            void release(int n = 1)  //释放一定数量的资源
            bool tryAcquire(int n = 1)  //尽量获取，资源数量不够时立即失败返回
            bool tryAcquire(int n, int timeout) //同上，只不过有个最长等待时间
            int available()          //返回当前可用的资源数量
            注：release方法可以创建新资源，即当QSemphore在构造时指定只有0个资源
            仍可在之后使用release方法，产生n个可用资源。
        条件变量QWaitCondition
            并发有两大需求，一是互斥，二是等待。
            互斥是因为线程间存在共享数据，等待则是因为线程间存在依赖。
            前面的关键段和读写锁，都是解决线程对资源的互斥访问问题，
            而条件变量就是为了解决线程依赖的问题。
            为了防止竞争，条件变量总是和锁（关键段/读写锁）一起使用。
            成员方法：
                void wakeOne()
                void wakeAll()
                void notify_one()    //为了适配STL，等同于wakeOne
                void notify_all()    //为了适配STL，等同于wakeAll
                bool wait(QMutex *lockedMutex, unsigned long time)
                bool wait(QReadWriteLock *lockedRWLock, unsigned long time)
            对wait函数的说明：
                这个函数会将互斥量解锁并等待，所以这暗含了一个前提，
                即作为输入参数的锁变量，必须是事先被上锁的，
                如果这个锁变量是可重复上锁的，则wait函数立即返回，
                然后锁变量会变成解锁状态，而当前线程则会被挂起
                当其它前程发出wakeOne或wakeAll信号，
                或者等待时间超时，当前线程将不再被挂起，
                如果是因为时间超时而结束等待，则wait返回false
                wait返回后，锁变量回到之前的上锁状态
                这意味着，如果是可重复上锁的锁变量，且被上过3次锁，
                则条件解锁后，锁变量变成未上锁状态，
                而条件返回后，锁变量恢复为3次上锁状态。
            与锁变量的关系
                从其成员函数可见，条件变量不能单独使用，而是配合锁变量使用
                从这一角度，可以认为条件变量是为锁变量而创建的增强工具，
                它的行为类似于对锁变量解锁后再立即加锁，并另外等待一个条件，
                类似于对资源数为0的信号量进行aqure操作，
                从而引起A线程等待，把cpu让给其它线程，
                而其它某个B线程在执行后使得条件被满足了，就可执行唤醒操作，
                类似释放信号量资源，从而使得等待的A线程结束等待
            则是相当于释放信号量资源
        信号量 vs 互斥量 vs 条件变量
            锁变量可以认为是资源数为1的信号量
            条件变量是可以强化互斥量功能的工具
            条件变量 ≈ QMutex.lock + QSemaphore(0).acquire + QMutex.unlock
    线程的优先级控制
        具有高优先级的线程被优先调度
        在线程基类QThread中有setPriority(Priority priority)方法
        也可以在QThread的start方法中指定优先级参数。
        有0-7八个优先级，qt默认为7，操作系统默认为3，
        从0到6优先级依次增高，而当优先级为7时，则表示继承创建线程的优先级。
        注意：Linux下的qt线程没有优先级之分
            在Linux系统中，线程遵循Posix标准，posix有3中调度策略，
            其中的两种引入了优先级机制，但这两种调度策略都只能在root用户下使用
            还有一种调度策略没有引入优先级机制，这种调度策略任何用户可以使用，
            这是Linux的默认调度策略，而Qt就是使用的这种调度策略，
            且没有提供更改调度策略的方法
            这就意味着在linux下，虽然我们为线程设置了不同的优先级，
            但这不起作用，所有的线程仍然运行在同一优先级下。
    线程死锁问题
        死锁的前提：第一把锁还没解锁，就请求第二把锁（旧锁未开，等待新锁）
    优先级反转问题
        一个低优先级线程和一个高优先级线程等待同一把锁，
        当这个低优先级线程拿到了锁，高优先级线程就得等待低优先级线程
        这是合理的，但这个低优先级线程在当前cpu时间片用完时还没释放锁，
        一个耗时较长的中优先级线程就可能一直占用cpu，
        这样不但低优先级线程得不到执行，就连高优先级线程也因为锁等待而得不到执行了
        只能白白便宜了这个中优先级线程
        这种问题具有很强的隐蔽性和偶发性，开发者只能尽量注意并避免这种情况。
    线程本地存储
        有个线程本地存储的策略是使用全局的QMap<thread_id,thread_data>
        qt提供了QThreadStorage类用于存储线程的单独数据。
        成员方法：            
            bool hasLocalData() const
            T &localData()
            T localData() const
            void setLocalData(T data)  //T只能为指针类型（需通过new在堆里分配）
            QThreadStorage会接管data，当线程退出或再次调用setLocalData时，自动释放data指针
    GUI线程与非GUI线程
        在有界面的Qt程序中，主线程由GUI线程充当，且qt只能有一个GUI线程
        其它耗时的操作应交由非GUI线程完成，保证界面实时响应
    线程间通信
        可重入与线程安全
            函数可重入
                如果一个函数能被多个线程同时调用，并为每个线程提供一份单独的数据
                则称这个函数是可重入的。可重入函数是线程安全的。
                一个函数不只可能被其它线程打断，还可能被中断函数打断。
                要想函数可重入，显然不能使用全局类型变量或静态变量，而只能使用局部变量
                另外也不能访问全局类型的资源，如对某个特定路径的文件进行读写操作。
                注意：如果一个线程调用了malloc/free函数，则这个函数是不可重入的，
                因为malloc是使用全局链表来管理的，即有个全局变量记录堆哪些是占用的，
                可在哪些位置分配新空间，因为这个malloc函数内部使用了全部变量，
                所以它不是可重入的，而外部函数调用了不可重入的函数，则这个外部函数也不可重入
                很多标准I/O库函数因为使用了全局数据结构，因而也是不可冲入的。
            函数线程安全
                如果一个函数能同时被多个线程调用，并且所有的调用这引用同一份数据，
                防伪非数据时串行处理，那么称这个函数是线程安全的
                对这段话的理解是，函数内使用了全局类型变量这样的临界资源，
                但同时引入了锁机制，保证这些临界资源只能被不同线程依次使用
                注意使用malloc函数，因为malloc函数涉及使用全局变量，所以为了线程安全，
                需要使用锁保护。另外如果在线程执行malloc期间收到了信号中断，cpu就会转而处理中断函数
                如果中断处理函数中也有malloc函数且进行了，且使用同一把锁对malloc进行保护，
                则这个锁必须是可重入的，否则就会中断响应函数卡死而无法返回，造成死锁。
            类可重入
                如果一个类中的所有函数在各个实例中可被多个线程同时调用，称这个类是可重入的
                换句话说，就是不同线程各自持有(这个类的)一个类实例，
                各个线程可自由使用其持有的类实例而不用担心其它线程的操作会带来什么影响。
                所以一个类如果使用了静态变量或外部资源，则一定是不可重入的，
                像如界面类，因为使用了界面（外部资源），所以一定是不可重入的。
                许多C++类只使用自身的成员变量，因此天然是可重入的。
                大部分的Qt非界面类也是可重入的。
                一个类可重入，并不代表它是线程安全的。
                因为类可重入限定的是每个线程各自持有一个类实例的情况，
                而线程安全则关注多个线程操作同一个类实例的情况。
                通常任何没有被全局引用的C++对象都是可重入的。---怎么理解？为什么？
                可重入类只能保证可以在不同线程中操作不同的此类的对象是安全的，
                不能保证，不同线程操作同一个此类对象，是安全的；
                绝大多数Qt的非图形界面类都符合一个并不太严格的要求：
                它们都必须是可重入的，即类的不同实例可同时用于不同的线程中；
                很多Qt的非图形用户界面类，包括QImage、QString和一些容器类，
                都使用了隐式共享作为一项优化技术，
                虽然这样的优化通常会让类变成不可重入的，
                但是Qt使用原子汇编语言语言指令来实现线程安全引用计数，
                这可以让Qt的隐式共享类变成可重入的；
                只能在一个线程中（一般是主线程）实例化对象，不能再其他线程中实例化该类的对象
                这样的类就是不可重入的，这可能是由于不同对象共享同一块内存导致的
                所有的QWidget和他的子类都是不可重入的
                所以qt中的界面类实例化对象只能在主线程中（ GUI线程）
                不要在子线程中直接操作界面类对象，要使用信号与槽技术或其他技术。
            类线程安全
                如果一个类对象可以同时被多个线程操作，称这个类是线程安全的
                不同线程对同一个类的对象进行操作，
                例如在不同线程调用同一个对象的类成员函数，是安全的，互不妨碍的，
                则说明该类是线程安全的
                Qt中线程安全的类有锁、条件变量、信号量及QThreadStorage<T>
        线程与事件循环
            GUI线程是唯一允许创建QAppliction对象，并且对它调用exec函数的线程
            起始线程（GUI线程）通过QCoreApplication::exec函数启动事件循环，
            而非GUI线程通过QThread::exec函数启动事件循环。
            自定义的继承QThread的类，在继承实现run方法时，自己决定是否调用exec，
            自定义线程对象的start方法内部就是调用的run方法，
            如果run中不调用exec，则线程执行完run方法后就自动结束，
            如果调用exec，则线程不会结束(run方法不会返回),而是陷入exec事件循环。
            另外注意，自定义线程对象就跟普通的QObject对象一样，是属于当前线程的，
            只是其中的run函数则是属于新线程的。
            与QCoreApplication类似，QThread也提供退出函数exit(int)和quit()槽。
            发往一个QObject类对象的事件，由对象所属线程的事件循环负责派发。
            注意：如果一个QObject类对象在QApplication对象创建之前构造，
            则通过QObject::thread()方法查看其所属线程时，会发现线程id为0，
            表明其不属于任何线程，所以这样的对象是不能处理信号槽的
            但可以通过QObject::moveToThread()方法改变QObject对象的所属线程
            注意，如果这个QObject对象有父对象，则无法使用moveToThread方法。
        与线程中的QObject类对象交互
            可以手动调用线程安全的QCoreApplication::postEvent()函数
            向任意线程创建的对象发送消息，这个消息最终会被分派的相应线程的时间循环。
            QCoreApplication::postEvent()因为不是发送队列消息，而是直接调用，
            所以只能向本线程的对象发送消息。
            如果使用事件过滤器，则注意监控对象要和被监控对象在同一个线程才行。
            如果一个QObject型对象正在被所属线程使用，则这时在另一个线程中删除该对象
            或访问该对象的函数是不安全的，如果要删除，应该使用QObject::deleteLater,
            该函数会发出一个“延后删除”事件，并最终并目标QObject的所属线程的事件循环处理。
            注意跨线程调用QObject方法时，注意这个对象是随时可能因响应事件而在所属线程中
            被调用的，所以需要时刻注意线程安全问题。
            QObject子对象必须在其父对象所属线程中创建，即不能使用其它线程中的对象作为父对象。
            事件驱动类只能用于单线程，典型代表是时间机制类和网络模块类。为什么？？？
        信号槽连接方式
            直连方式
                槽函数在发出信号的线程中被调用(即使目标对象是属于其它线程的),
                所以，如果信号发送者与接受者不在同一线程时，使用这种连接方式应注意线程安全。
            排队方式
                发出事件，目标对象所属线程的事件循环处理事件并最终调用相应槽函数。
            自动方式
                内部判断，如果目标对象不在发出信号线程中，则使用排队方式，在同线程中，则使用直连。
    进程创建与进程间通信
        使用QProcess  
            QProcess仅仅是把Linux底层与进程相关的API进行了面向对象的封装。
            QProcess用于启动一个外部程序并与之通信。
            start启动外部程序
                创建好QProcess对象后，使用start方法启动外部程序，并可指定命令行参数
                start后，QProcess立即进入“启动状态”，但这时候外部程序还没启动好，
                当外部程序启动好后，QProcess进入“运行状态”，并发出started信号。
                waitForStarted函数可阻塞等待，直到started信号发出。
            与新进程的标准输入输出流交互
                QProcess继承自QIODevice，可通过write方法向新进程的标准输入写数据
                也可通过read/readLine/getChar等函数从新进程的标准输出读数据。
                一些接受QIODevice*参数的函数，可以传入QProcess对象，
                以新进程的输出作为数据源，如QXmlReader。
                对于新进程的标准输出，应注意，进程具有两个预定义的输出通道(stdout、stderr)，
                可以通过serreadChannel设置当前的读通道，当通道有可读数据时，发出readyRead信号
                如果是标准输出通道有数据，则同时还会发出readyReadStandardOutput信号，
                如果是错误输出通道有数据，则同时还会发出readyReadStandardError信号。
                可分别用readAllStandardOutput和readAllStandardError函数读取相应通道数据。
                此外QProcess还允许把这两个通道合并，共用标准输出通道，方法是在进程前，
                调用setReadChannelMode，并传入MergedChannels参数。
                也可以用closeWriteChannel、closeReadChannel这样的方法把不用的通道关闭。
                关闭通道后，相应通道的读写操作将失败。
                还可把新进程的输入输出通道映射为本地文件。
                此外还有阻塞函数waitForReadyRead、waitForBytesWritten，
                他们是重载的QIODevice的相应方法。
            进程退出信号
                当新进程退出时，QProcess回到初始状态（非运行状态），并发出finished信号。
                finished信号通过参数的方式，携带了进程退出时的退出码和退出状态，
                也可以通过exitCode和exitStatus这两个函数获取。
                Qt的退出状态只有两种：正常退出(0)和崩溃退出(1)。
                当进程在运行中产生错误（猜想应该是代码中调用了类似setError这样的方法），
                QProcess将发出error()信号，可以通过error函数获取最后一次的错误码，
                并通过state()函数获取此时进程所处的状态。
                此外还有阻塞函数waitForFinished，直到有道finished信号。
            新进程环境设置
                可通过setEnvironment、setWorkingDirectory为新进程设置环境变量和工作路径。
        进程间通信
            广义上的进程间通信包括两个进程通过磁盘文件或数据库交换信息，
            但常说的进程间通信，则是指具有一定效率的通信手段，通常有操作系统内核支持。
            具体而言，包括消息队列、信号量、共享存储、sock管道等。
            Linux进程通信的主要手段
                管道及命名管道
                    管道可用于具有亲缘关系的进程间通信，命名管道则使用所有进程间通信。
                信号
                    主要用于通知某事件发生了。
                消息队列
                    消息的链表，包括POSIX消息队列和System V消息队列。
                    消息队列克服了信号承载信息量少，管道只能承载无格式字节流及缓冲区大小受限等缺点
                共享内存
                    最有效率的IPC方式，常常与其它通信机制（如信号量）结合使用
                信号量
                    主要用于进程间同步及线程间同步
                套接字
                    更通用、可以跨机器、跨平台、跨语言
            Qt对进程间通信的支持
                共享内存 QSharedMemory
                    QShareMemory对象构造函数需要指定共享区的名字(自定义)。
                    也可以调用setkey方法，重新设置共享区的名字。
                    通过create(size)方法创建共享区，支持lock、unlock方法，
                    通过data()方法获取共享区的指针。
                    通过attach、detach关联已存在的共享存储区。
                套接字   QLocalSocket、QLocalServer
                    在windows中，QLocalSocket实现为有名管道，在Unix中实现为本地socket
            新型进程间通信D-Bus
                D-Bus是一种告诉的二进制消息传输协议，具有低延时、低开销的特点，非常适合本机通信。
                总线机制
                    D-Bus由几个总线组成，包括一个持久的系统总线和多个会话总线
                    系统总线在一开始系统引导时就自动，有操作系统和后台进程使用。
                    会话总线在用户登录后启动，归登录用户私有，用于用户应用程序间的通信。
                    如果一个应用程序需要获取来自系统总线的消息，也可以直接连接到系统总线，
                    但此时允许发送的消息收到限制。
                通过总线通信时，应用程序可获取其它可用的对象或服务，
                同时自己也成为一个活跃的被请求对象。
                D-Bus总线适用于有多对多通信需求的场景，但也可以用于两个程序间的直接通信。
                D-Bus的相关术语
                    信息
                    服务名
                        通过总线通信时，需要有个服务名，从而可以被同一总线上的其它应用获取。
                        有点类似ip和主机名，由以点分隔的字符（字母数字）组成。
                        服务名不是必须的，如果没有使用到总线，就无需服务名。
                    对象路径
                        一个应用通过暴露对象，为其它应用提供特定服务，从QObject派生，
                        类似url中的接口路径，命名规范类似文件系统中的路径名。
                    接口
                        类似C++或java中接口的概念，是调用者和被调用者的调用约定。
                Qt与D-Bus
                    Qt提供了一个QtDBus模块，内部封装了D-Bus协议。
                    应用程序可通过它为其它程序提供服务，其它程序可以像调用自身函数或
                    访问自身对象属性那样访问远程对象。
                    此外QtDBus还对信号槽进行了扩展，允许将远程信号和本地信号挂到远程槽中。
qt信号槽原理
    调用QObject::connect方法时，
    借助QMetaObject和QMetaObjectPrivate，
    可以获得有关信号发送者、信号函数、信号接受者、槽函数的特定信息，
    这些信息会被添加到发送者的"信号槽列表"(ConnectionList)中————参看QObjectPrivate
    每个线程有个事件队列，在线程事件循环中，会检查该队列，
    如果队列中有信号(QMetaCallEvent事件)，就找到信号相应的对象，
    查找该对象“信号槽列表”，完成对相应槽的调用。
    注：发送者发出信号时，会检查信号槽连接方式，
    如果槽函数对应的对象在其它线程中，则向其线程抛出QMetaCallEvent事件。
    发送信号函数会最终调用到当前对象invoke方法，
    在QMetaMethod::invoke(QObject *object,
                          Qt::ConnectionType connectionType,
                          QGenericReturnArgument returnValue,
                          QGenericArgument val0,...)
    方法中(qmetaobject.cpp)
    会获取QThread::currentThread()和object->thread()，
    比较两者是否一致，如果不一致且connectionType=AutoConnection，
    则令connectionType=Qt::QueuedConnection
    之后，如果是直接调用方式，则
    callFunction(object, QMetaObject::InvokeMetaMethod, idx_relative, param);
    如果是间接调用方式，则
    QCoreApplication::postEvent(object, 
                                new QMetaCallEvent(
                                    idx_offset, idx_relative, callFunction,
                                    0, -1, nargs, types, args));
        原型：static void postEvent(QObject *receiver, QEvent *event, 
                                    int priority = Qt::NormalEventPriority);  
        QThreadData * data = &receiver->d_func()->threadData;
        data->postEventList.addEvent(QPostEvent(receiver, event, priority));
        event->posted = true;
        ++receiver->d_func()->postedEvents;
        data->canWait = false;
    也就是说，postEvent把事件对象QMetaCallEvent添加到目标object所在线程对象
    (QThread/QThreadData)的事件列表(postEventList)中.
    而线程的事件循环从该事件列表中取出事件对象，根据事件对象中记录的目标对象的信息
    调用event函数，并最终完成对槽函数的调用。
        QCoreApplication的exec方法，内部调用的是QEventLoop的exec方法，
        在QEventLoop的exec方法中，可以获取当前线程的线程信息
            Q_D(QEventLoop);  d->threadData
        QEventLoop的exec方法内部又调用QEventLoop::processEvents
            Q_D(QEventLoop);
            d->threadData->eventDispatcher.load()->processEvents(flags);
                class QThreadData中有成员变量
                QAtomicPointer<QAbstractEventDispatcher> eventDispatcher;
                    QAbstractEventDispatcher(继承自QObject)具有成员函数如
                    void installNativeEventFilter(QAbstractNativeEventFilter *filterObj);
                    void removeNativeEventFilter(QAbstractNativeEventFilter *filterObj);
                    bool filterNativeEvent(const QByteArray &eventType, void *message, long *result);
                    virtual bool processEvents(QEventLoop::ProcessEventsFlags flags) = 0;
                    virtual bool hasPendingEvents() = 0; //Qt6: remove, mark final or make protected
                    virtual void registerSocketNotifier(QSocketNotifier *notifier) = 0;
                    virtual void unregisterSocketNotifier(QSocketNotifier *notifier) = 0;
                    virtual bool registerEventNotifier(QWinEventNotifier *notifier) = 0;
                    virtual void unregisterEventNotifier(QWinEventNotifier *notifier) = 0;
                    。。。
                QPostEventList postEventList;  //事件列表
                QVector<void *> tls;  //用于线程局部存储
        windows下，这个函数会进入到QWindowsGuiEventDispatcher::processEvents
        继而进入QEventDispatcherWin32::processEvents
        在该函数中，会检查Windows窗口消息队列并获取消息
        该函数又会调用到消息处理回调函数qt_internal_proc，
        该函数会处理WM_QT_SOCKETNOTIFIER(WM_USER)、
        WM_QT_ACTIVATENOTIFIERS(WM_USER+1)、
        WM_QT_SENDPOSTEDEVENTS(WM_USER+2)及WM_TIMER等4种消息，
        其它类型的消息则调用DefWindowProc函数处理。
        对于WM_QT_SENDPOSTEDEVENTS类型消息（对应信号槽），
        则调用q->sendPostedEvents(); 
        QEventDispatcherWin32 *q = 
            (QEventDispatcherWin32 *) GetWindowLongPtr(hwnd, GWLP_USERDATA);
        所以这里又从QEventDispatcherWin32::processEvents进入到
        QEventDispatcherWin32::sendPostedEvents函数中，
        并继而进入到 QCoreApplicationPrivate::sendPostedEvents中，
        继而调用QCoreApplication::sendEvent(r, e);
        r为QPostEvent中记录的receiver。
        QPostEvent是在QThreadData的postEventList中记录的。
        QCoreApplication::sendEvent调用QCoreApplication::notifyInternal2函数
        并继而调用QCoreApplication::notify，notify函数是个非常大的函数，
        它会处理各种event事件类型。
        如果receiver是widget类型，则会最终调用到QWidget::event(event);
        在event中，则会最终根据元对象信息，调用到相应的槽函数。
        而如果是非widget类型，则会通过QObject::event，最终调用到槽函数。
界面风格
    改变界面颜色
        用setPalette函数自定义界面颜色
            QApplication a(argc, argv);
            a.setStyle(new QWindowsStyle);
            QPalette pl(QColor(255,0,155));
            pl.setBrush(QPalette::WindowText,QColor(255,125,125));
            pl.setBrush(QPalette::Button,QColor(0,255,125));
            pl.setBrush(QPalette::Light,QColor(255,125,255));
            pl.setBrush(QPalette::ButtonText,QColor(125,0,0));
            pl.setBrush(QPalette::Shadow,QColor(0,125,0));
            pl.setBrush(QPalette::Highlight,QColor(0,0,125));
            pl.setBrush(QPalette::HighlightedText,QColor(255,0,0));
            a.setPalette(pl);   //还可通过第二个参数限定只用于某一类及其子类
            注1：默认风格不能改变按钮背景色，QWindowsStyle风格可以改变按钮背景色
            既可为application设置调色板，也可以为某个widget设置调色板
            注2：在qt5中，设置风格的方法不再是a.setStyle(new QWindowsStyle);
            而是改为QStringList ls = QStyleFactory::keys();
            a.setStyle(QStyleFactory::create(ls[0]));
    自定义风格类
        处理使用Qt自带的风格类QWindowsStyle，
        我们也可以继承QWindowsStyle，重写polish(QPalette&)方法，
        实现自己的CustomStyle,当调用setPalette方法时，会调用polish函数。
        另外还可重载polish(QWidget*)或polish(QApplication*)，为指定的程序或控件上色
中心窗口部件
    一个Qt主窗口应用程序必须有一个中心窗口部件。
    而中心窗口部件也是主窗口QMainWindow特有的特性。
    在QtCreator中，Qt为主窗口自动生成了一个名为centralwidget的
    QWidget类型的中心部件（参看ui_mainwindow.h文件）。
    QWidget * QMainWindow::centralWidget () const，可获得中心部件。
    中心部件可以是如下类型：
        Qt提供的标准窗口部件，如QWidget、QTextWidget等
        用户自定义的窗口部件
        分裂器--QSplitter
            QSplitter作为一个容器，可容纳多个Qt窗口部件
            此时中心部件是一个包容多个窗口部件的容器。
        工作控件部件--QWorkspace
            在一个MDI应用程序中，应用程序主窗口的中心部件是一个QWorkspace部件
        多文档部件--QMdiArea
            Qt4.3新增，用法与QWorkspace类似
    如果主窗口已经有中心部件了，在调用QMainWidget的的setCentralWidget方法
    为主窗口设置一个新的中心部件，那么原来的中心部件会被主窗口销毁掉。
    这是如果再引用原来的中心部件的话（包括delete该对象），会造成崩溃。
    在QMainWindow中直接插入控件，并选择this作为控件的构造函数参数，
    如QPushButton* pbtn = new QPushButton(this);
    会发现按钮没有显示出来，这是因为中心窗口部件把手动添加的按钮给挡住了。
    所以解决的办法是，把中心部件作为按钮的构造函数参数：
    QPushButton* pbtn = new QPushButton(ui->centralWidget);
    或QPushButton* pbtn = new QPushButton(centralWidget());
    中心部件的作用：
        中心部件的其中一个作用就是，当主窗口大小变化时，中心部件也随之变化，
        而一般添加的自定义控件，如果没有使用专门的布局器，是不会随窗口大小变化的。
        类似的，setMenuBar、setToolBar也有类似的功能，使菜单栏和状态栏能随窗口大小变化。
QWidget直接作为窗口部件
    将QWidget（或自定义的QWidget派生类）作为窗口部件，
    在窗口中添加，没有效果，设置样式表也没有用。
    因为QWidget的paintEvent函数直接就没有任何代码实现，
    要想让QWidget的自定义派生类支持样式表，
    可以在paintEvent中加入如下代码：
        QStyleOption opt;
        opt.init(this);
        QPainter p(this);
        style()->drawPrimitive(QStyle::PE_Widget,&opt,&p,this);
    提示:可以考虑继承QFrame取代继承QWidget，QFrame支持样式表。
connectSlotsByName
    QMetaObject::connectSlotsByName(QObject *o);
    根据o的元对象，得到其槽函数列表
    如果是以on_开头的，就遍历o的孩子列表，
    如果能找匹配的对象，就使用connect方法连接信号槽。
    所以这种连接信号槽的方法尤其局限性：
    即发信号的只能是自己的孩子，而信号的接受者只能是自己。
使用资源管理文件(.qrc)
    qt可以支持添加/新建.qrc格式的资源管理文件
    引用资源文件：
        如果是引用的cpp资源文件，只需按如下格式引用资源即可
        :/ + (资源管理器中)前缀 + 文件名
        如：QImage img; img.load(":/new/prefix1/image.png");
        如果是引用二进制的rcc资源文件，还需在程序开始的时候，
        多一步注册(引入)资源的操作：
        QResource::registerResource("path/xxx.rcc");
        这样程序可以动态加载该二进制资源文件，识别其包含的资源
    修改资源管理文件：
        .qrc管理文件通过qt资源文件管理器打开以编辑，
        通过资源管理器添加资源前，需先添加前缀，
        资源文件的类型包括但不限于图片、声音、视频等。
        另外，资源管理文件(.qrc)是xml格式的,如：
        <RCC>
            <qresource prefix="/new/prefix1">
                <file>main.cpp</file>
                <file>C:/24.bmp</file>
            </qresource>
        </RCC>
        所以，原则上，你也可以不使用资源管理器，
        而是直接修改.qrc文件的方式，添加新的资源文件
    编译资源文件：
        编译成cpp文件
            如果是qt工程，只需在.pro文件中添加 RESOURCES += myres.qrc,
            qt会自动使用rcc命令生成相应的.cpp文件，
            默认情况下，rcc 工具会对各个资源文件做ZIP压缩，
            然后将压缩后的ZIP数据的每个字节转换成比如 0x6f数值形式，
            所有文件压缩后的数据对应一个C++静态数组 qt_resource_data[]，
            并添加注册、取消注册、初始化、清除等函数和资源描述结构体，
            最终形成一个 qrc_xxx.cpp文件。
            如果是vs，也可以借助qt的rcc.exe命令，可以把.qrc文件编译成.cpp文件，
            rcc -name aa -no-compress "$(InputPath)" -o aa.cpp
            这种方式的好处是执行速度快，使用方便等，但坏处也很明显，
            一是会增加生成的可执行文件的体积，
            二是占用内存大，
            三是如果想替换图片，如更换皮肤，会很不方便
        生成资源二进制文件 
            使用qt的rcc.exe命令，也可以把.qrc文件编译成二进制资源文件.rcc
            rcc -binary myresource.qrc -o myresource.rcc
            使用这种方式，可以方便的替换rcc文件达到给程序换肤的效果，而不用重新编译可执行文件
        rcc语法： rcc  [options] <inputs>
          Options:
            -o file              指定输出文件（默认输出到控制台）
            -project             自动生成一个.qrc文件，文件把当前目录下的所有文件都包含为资源
            -binary              指明生成二进制的资源文件
            -name name           让导出的资源初始化函数的名字包含name
            -no-compress         关闭自动压缩
            -threshold level     压缩资源时的最大阈值
            -compress level      压缩等级
            -root path           在生成的资源索引名前追加path前缀
            -namespace           让编译生成的资源文件cpp中不包含名字控件宏(QT_BEGIN_NAMESPACE)
            -version             显示版本信息
            -help                显示帮助
    直接引用本地图片文件
        除了引用资源文件外，我们也可以直接引用本地文件，如
        QImage img; img.load("C:/image.png");
        但这种方式有个很大的问题，就是用户可以随意替换资源图片
        这是个缺点，因为容易被用户随意修改，但同时也可把这看成是个优点
        
        
======================================================================================            