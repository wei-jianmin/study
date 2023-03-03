第二章
    2.1 子类化QDialog
        使用类的前置声明
            在头文件中使用前置声明，在cpp文件中真正包含头文件，
            这样可以避免头文件过大，如果有多个地方包含这个头文件，
            可以减小代码体积，提高编译速度。
        伙伴
            在UI编译器中，可以为label设置伙伴（setBuddy）,
            可以在label获得焦点时，将焦点转移到伙伴身上
        布局器
            布局器调用addWidget方法，可以自动为所添加的子对象设置父类
            tips for using layouts
            when use a layout, you don`t need to pass a parent when constructing the child widgets.
            the layout will auto reparent the widgets (using set parent()) .
            so they are children of the widget on which the layout is installed.
        信号槽的特点
            当一个信号连接了多个槽时，槽的调用顺序不一定与连接顺序一致。
            连接的信号槽，可以用disconnect取消关联
    2.3 快速设计对话框
        父子对象机制
            父子对象机制是在QObject中实现的
            删除父对象，会递归删除其子对象，
            删除子对象，会自动从其父对象的“子对象列表”中将之删除。
            对于窗口部件，子对象会显示在父对象中。
        对话框的返回结果
            accept()关闭对话框，返回QDialog::Accepted(=1),
            reject()关闭对象矿，返回QDialog::rejected(=0)。
    2.4 改变形状的对话框
        把窗体的sizeConstraint属性设为QLayout::SetFixedSize。
        TODO: 学习以下类
            QTabWidget QStackedWidget QToolBox
            QListWidget QTableWidget QTreeWidget
            QListView QTreeView QTableView
    2.5 动态对话框
        动态对话框即动态加载.ui文件。
        QUILoader成员函数讲解
            void addPluginPath(const QString &path)
            void clearPluginPaths()
            //上面两个函数控制插件查找目录，插件即第三方控件（包括自定义控件）
            QStringList availableLayouts() const
            QStringList availableWidgets() const
            //上面函数列出所有的可用控件即布局器（包括自带的和三方的）
            virtual QAction *createAction(QObject *parent = Q_NULLPTR, const QString &name = QString())
            virtual QActionGroup *createActionGroup(QObject *parent = Q_NULLPTR, const QString &name = QString())
            virtual QLayout *createLayout(const QString &className, QObject *parent = Q_NULLPTR, const QString &name = QString())
            virtual QWidget *createWidget(const QString &className, QWidget *parent = Q_NULLPTR, const QString &name = QString())
            //上面这些函数用于创建控件、布局器、action等，QUILoader根据.ui文件创建各个对象时，就是回调的这些函数
            void setWorkingDirectory(const QDir &dir)
            QDir workingDirectory() const
            //上面函数用于设置当前工作目录，查找资源（如图标）时，以此为基本路径
            QWidget *load(QIODevice *device, QWidget *parentWidget = Q_NULLPTR)
            //上面的函数根据ui文件，动态创建对象
        使用举例：
            QUILoader uiloader;
            QWidget * dlg = uiloader.load(QIODevice *device, QWidget *parentWidget = Q_NULLPTR);
            QButton* btn1 = dlg->findchild<QButton*>("btn1");
            ......
            

        
        
        
            