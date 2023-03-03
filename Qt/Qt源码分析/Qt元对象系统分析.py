Q_OBJECT宏预处理后的效果(MinGW)：
    public:
        _Pragma("GCC diagnostic push")
        static const QMetaObject  staticMetaObject; 
        static const QMetaObject &getStaticMetaObject();
        virtual const QMetaObject *metaObject() const; 
        virtual void *qt_metacast(const char *);
        virtual int qt_metacall(QMetaObject::Call, int, void **); 
        #字符串转换，调用的是元对象类QMetaObject的转换方法
        static inline QString tr(const char *s, const char *c = Q_NULLPTR, int n = -1) 
            return staticMetaObject.tr(s, c, n); 
        static inline QString trUtf8(const char *s, const char *c = Q_NULLPTR, int n = -1) 
            return staticMetaObject.tr(s, c, n);
    private:
        static void qt_static_metacall(QObject *, QMetaObject::Call, int, void **); 
        _Pragma("GCC diagnostic pop")
        struct QPrivateSignal {};

    小结：
    ● _Pragma
      _Pragma("GCC diagnostic push")
      记录当前为GCC配置的诊断选项
      _Pragma("GCC diagnostic pop")
      恢复之前存储的
      
    ● 声明了3+2个公有函数：（3个虚函数+2个静态函数）	
        virtual QMetaObject *metaObject();          //获取类的元对象
            //这个函数是获取当前类对象里面内部元对象的公开接口
        virtual void *qt_metacast(const char *);    //动态类型识别
            //qt_metacast 是程序运行时的对象指针转换，它可以将派生类对象的指针安全地转为基类对象指针
            //这是 Qt 不依赖编译器特性，自己实现的运行时类型转换
            //qt_metacast 参数是基类名称字符串，返回值是转换后的基类对象指针，如果转换不成功，返回 NULL。
        virtual int qt_metacall(QMetaObject::Call, int, void **);   //实现对信号槽和属性的支持
            //qt_metacall 是非常重要的虚函数，  
            //在信号到槽的执行过程中，qt_metacall 就是负责槽函数的调用，
            //属性系统的读写等也是靠 qt_metacall 实现。
        static QString tr(const char *s, const char *c = Q_NULLPTR, int n = -1);
        static QString trUtf8(const char *s, const char *c = Q_NULLPTR, int n = -1);
        //提供字符编码转换
        
    ● 声明了1个私有静态函数：
        static void qt_static_metacall(QObject *, QMetaObject::Call, int, void **); 
            //前面的qt_metacall调用该私有静态函数实现槽函数调用，真正调用槽函数的就是 qt_static_metacall
            
    ● 声明了1个公有成员变量（类的元对象）：
        static const QMetaObject  taticMetaObject; 
            //这句定义了关键的静态元对象 staticMetaObject，这个对象会保存该类的元对象系统信息。
            //使用静态元对象，说明该类的所有实例都会共享这个静态元对象，而不需要重复占用内存。
            
    ● 声明了一个私有结构体：
        struct QPrivateSignal {};
            //QPrivateSignal 是一个私有的空结构体，对函数功能来说没啥用，
            //就是在信号被触发时，挂在参数里提醒程序员这是一个私有信号的触发。
			
=============================================================================================================

对一个moc文件的分析（qt5.4）：
    #data字段是一个由byte数组组成的数组，数组大小根据信号&槽个数有关，这个数组在调用QObject的connect函数时用来匹配信号名或槽名。
    #stringdata 存放的是字符资源，存放全部的信号名、槽名、类名。
    struct qt_meta_stringdata_MainWindow_t {
        QByteArrayData data[7];
        char stringdata0[45];
     };
    
    'define QT_MOC_LITERAL(idx, ofs, len) \
    {{-1}, len, 0, 0, qptrdiff(offsetof(qt_meta_stringdata_MainWindow_t, stringdata0) + ofs - idx * sizeof(QByteArrayData)) } 
        'define Q_BASIC_ATOMIC_INITIALIZER(a) { (a) }
        'define Q_REFCOUNT_INITIALIZE_STATIC { Q_BASIC_ATOMIC_INITIALIZER(-1) }
        'define Q_STATIC_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(size, offset)   { Q_REFCOUNT_INITIALIZE_STATIC, size, 0, 0, offset } 
        'define Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(size, offset)    Q_STATIC_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(size, offset)
        'define QT_MOC_LITERAL(idx, ofs, len)  Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, qptrdiff(offsetof(qt_meta_stringdata_MainWindow_t, stringdata0) + ofs - idx * sizeof(QByteArrayData)) )
    
    static const qt_meta_stringdata_MainWindow_t qt_meta_stringdata_MainWindow = {
        {
            QT_MOC_LITERAL(0, 0, 8),    //个数与qt_meta_stringdata_MainWindow_t结构体中data数组的长度相匹配
            QT_MOC_LITERAL(1, 9, 5),    //第一个参数是数组索引
            QT_MOC_LITERAL(2, 15, 0),   //第二个参数是在stringdata字段中的开始位置
            QT_MOC_LITERAL(3, 16, 5),   //第三个参数是长度。
            QT_MOC_LITERAL(4, 22, 5),   //如这里的4,22,5，就表示第4个字符串（从第0个开始算起），偏移量为22，长度为5，即“iTemp”
            QT_MOC_LITERAL(5, 28, 7),   //可以认为这个结构体就是个带索引的字符串数组
            QT_MOC_LITERAL(6, 36, 7)    
        },
        “CTestMoc\0Test1\0\0Test2\0iTemp\0OnTest1\0OnTest2\0”    //与qt_meta_stringdata_MainWindow_t结构体中stringdata0字符数组的长度相匹配
     };

    #这个结构体描述的是信号&槽在调用时的索引、参数、返回值等信息。
    #这个数组的前14个uint 描述的是元对象的私有信息，定义在qmetaobject_p.h文件的QMetaObjectPrivate结构体当中
    #也就是说该数组与QMetaObjectPrivate类相对应
    #QMetaObject类中的一些关于方法调用的关键函数，如indexOfSignal、indexOfSlot、connect、disconnect，都是在QMetaObjectPrivate中实现的
    static const uint qt_meta_data_MainWindow[] = {
           // content:
           7,       // revision
           0,       // classname
           0,    0, // classinfo
           4,    14, // methods  //这个信息描述的是信号&槽的个数和在表中的偏移量，即14个uint之后是信号&槽的信息，4表示有4个信号槽
           0,    0, // properties
           0,    0, // enums/sets
           0,    0, // constructors
           0,       // flags
           2,       // signalCount
           // signals: name, argc, parameters, tag, flags   //每描述一个信号需要5个uint
           1, 0, 34, 2, 0x06,
        　 3, 1, 35, 2, 0x06,
        　 // slots:   name, argc, parameters, tag, flags   //每描述一个槽也需要5个uint
           // name：对应的是上面qt_meta_stringdata_MainWindow中索引，例如1 对应的是Test1
           // argc：参数个数
           // parameters ： 参数的在qt_meta_data_CTestMoc这个表中的索引位置。
           // tag：这个字段的数值对应的是qt_meta_stringdata_MainWindow 索引，在这个moc文件里对应的是一个空字符串，具体怎么用，在源代码里没看懂。
       　　// flags：是一个特征值，是在 enum MethodFlags 枚举中定义。
        　 5, 0, 38, 2, 0x08,
        　 6, 1, 39, 2, 0x08,
        　 // signals: parameters
        　 QMetaType::Void,
        　 QMetaType::Void, QMetaType::Int, 4,
        　 // slots: parameters
        　 QMetaType::Void,
        　 QMetaType::Void, QMetaType::Int, 4,
           0        // eod
     };

    void MainWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
        Q_UNUSED(_o);
        Q_UNUSED(_id);
        Q_UNUSED(_c);
        Q_UNUSED(_a);

    const QMetaObject MainWindow::staticMetaObject = {
        { &QMainWindow::staticMetaObject, 
          qt_meta_stringdata_MainWindow.data,
          qt_meta_data_MainWindow,  
          qt_static_metacall, 
          nullptr, 
          nullptr }
     };


    const QMetaObject *MainWindow::metaObject() const
        return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;

    void *MainWindow::qt_metacast(const char *_clname)
        if (!_clname) return nullptr;
        if (!strcmp(_clname, qt_meta_stringdata_MainWindow.stringdata0))
            return static_cast<void*>(const_cast< MainWindow*>(this));
        return QMainWindow::qt_metacast(_clname);

    int MainWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
        _id = QMainWindow::qt_metacall(_c, _id, _a);
        return _id;

    处理后：		
    static const qt_meta_stringdata_MainWindow_t qt_meta_stringdata_MainWindow = {
        {
         //QT_MOC_LITERAL(0, 0, 10) // "MainWindow"
         //Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(10, qptrdiff(offsetof(qt_meta_stringdata_MainWindow_t, stringdata0) + 0 - 0 * sizeof(QByteArrayData)) )
         { { {-1} }, 10, 0, 0, qptrdiff(offsetof(qt_meta_stringdata_MainWindow_t, stringdata0) + 0 - 0 * sizeof(QByteArrayData)) }
        },
        "MainWindow"
     };

=============================================================================================================
  
对一个moc文件的分析（qt4.8.7):
    #最有价值的数据成员，被staticMetaObject记录
    #与QMetaObjectPrivate类结构相对应
    static const uint qt_meta_data_MainWindow[] = {
           #content:
           6,       // revision
           0,       // classname
           0,    0, // classinfoCount , classinfoData(类信息在该数组中的偏移量)
           0,    0, // methodCount , methodData(函数信息在该数组中的偏移量)
           0,    0, // propertieCount , propertieData(属性信息在该数组中的偏移量)
           0,    0, // enumeratorCount , enumeratorData(枚举信息在该数组中的偏移量)
           0,    0, // constructorCount , constructorData(构造函数信息在该数组中的偏移量)
           0,       // flags
           0,       // signalCount
           0        // eod
           //classinfoData
             每组有2个值
           //methodData
           //propertieData
             每组有3个值
           //enumeratorData
             每组有4个值
           //constructorData
             每组有5个值，第一个值指向的是在qt_meta_stringdata_MainWindow字符串中的偏移量（即构造函数名称）
     };
     static const uint qt_meta_data_QObject[] = {
         // content:
               6,       // revision
               0,       // classname
               0,    0, // classinfo
               4,   14, // methods      #从下面可见，只记录信号和槽，其他函数没记录
               1,   34, // properties
               0,    0, // enums/sets
               2,   37, // constructors
               0,       // flags
               2,       // signalCount
         // signals: signature, parameters, type, tag, flags
               9,    8,    8,    8, 0x05,
              29,    8,    8,    8, 0x25,
         // slots: signature, parameters, type, tag, flags
              41,    8,    8,    8, 0x0a,
              55,    8,    8,    8, 0x08,
         // properties: name, type, flags
              90,   82, 0x0a095103,
         // constructors: signature, parameters, type, tag, flags
             108,  101,    8,    8, 0x0e,
             126,    8,    8,    8, 0x2e,
             
               0        // eod
        };

    #本类的名字标识字符串，被staticMetaObject记录
    static const char qt_meta_stringdata_MainWindow[] = {
        "MainWindow\0"
     };

    #静态私有成员变量，被staticMetaObject记录
    const QMetaObjectExtraData MainWindow::staticMetaObjectExtraData = {
        0,  qt_static_metacall /*静态私有成员函数*/ 
     };

    #公有静态成员变量，最关键的数据成员
    const QMetaObject MainWindow::staticMetaObject = {
        { 
          &QMainWindow::staticMetaObject,   #基类的元数据
          qt_meta_stringdata_MainWindow,    #当前类的名字标记
          qt_meta_data_MainWindow,          #元数据的索引数组
          &staticMetaObjectExtraData        #扩展元数据表
        }
     };

    #公有静态成员函数，获取本类中QMetaObject&
    const QMetaObject &MainWindow::getStaticMetaObject() { return staticMetaObject; }
        void(_o);
        void(_id);
        void(_c);
        void(_a);
        
    #公有虚函数，通过基类指针获取子类对象的QMetaObject*
    const QMetaObject *MainWindow::metaObject() const
        return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;

    #公有虚函数，根据名字标识字符串，从子类往基类找，返回找到的类对象的指针
    void *MainWindow::qt_metacast(const char *_clname)
        if (!_clname) return 0;
        if (!strcmp(_clname, qt_meta_stringdata_MainWindow))
            return static_cast<void*>(const_cast< MainWindow*>(this));
        return QMainWindow::qt_metacast(_clname);

    #公有虚函数，QMetaObject::Call为枚举类型
    int MainWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
        _id = QMainWindow::qt_metacall(_c, _id, _a);
        if (_id < 0)
            return _id;
        return _id;
    
    #私有静态函数，在本文件中，此函数没有实际意义
    void MainWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
        Q_UNUSED(_o);   #define Q_UNUSED(x) (void)x  即表示这是无意义的一行
        Q_UNUSED(_id);
        Q_UNUSED(_c);
        Q_UNUSED(_a);
     #其它项目中的一个例子,可见，通过此函数，可以调到类中的各个方法、属性，效用类比com中的invoke   
     void FlightInfo::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
      {
        if (_c == QMetaObject::InvokeMetaMethod) {
            Q_ASSERT(staticMetaObject.cast(_o));
            FlightInfo *_t = static_cast<FlightInfo *>(_o);
            switch (_id) {
                case 0: _t->handleNetworkData((*reinterpret_cast< QNetworkReply*(*)>(_a[1]))); 
                break;
                case 1: _t->today(); 
                break;
                case 2: _t->yesterday(); 
                break;
                case 3: _t->searchFlight(); 
                break;
                case 4: _t->startSearch(); 
                break;
                case 5: _t->randomFlight(); 
                break;
                case 6: _t->request((*reinterpret_cast< const QString(*)>(_a[1])),
                                    (*reinterpret_cast< const QDate(*)>(_a[2]))); 
                break;
                default: ;
            }
        }
      }
        
=============================================================================================================

各种结构/类的声明
    struct QMetaObject
        '函数部分
          '获取数据成员
            const char *className() const;
            const QMetaObject *superClass() const;

          '类型转换
            #用于向参数给定的子类转换：查找参数的父级链，如果元对象与当前类的元对象一致，则返回该参数，否则返回0
            QObject *cast(QObject *obj) const;
            const QObject *cast(const QObject *obj) const;

          '编码转换
            #实际内部调用的QCoreApplication::translate
            QString tr(const char *s, const char *c) const;
            QString trUtf8(const char *s, const char *c) const;
            QString tr(const char *s, const char *c, int n) const;
            QString trUtf8(const char *s, const char *c, int n) const;

          '获取各种成员偏移量
            #各父级元对象（不包括自己）的d.data(=qt_meta_data_MainWindow)中methodCount的累加和
            int methodOffset() const;
            #各父级元对象（不包括自己）的d.data(=qt_meta_data_MainWindow)中enumeratorCount的累加和
            int enumeratorOffset() const;
            #各父级元对象（不包括自己）的d.data(=qt_meta_data_MainWindow)中propertyCount的累加和
            int propertyOffset() const;
            #各父级元对象（不包括自己）的d.data(=qt_meta_data_MainWindow)中classInfoCount的累加和
            int classInfoOffset() const;

          '获取各种成员个数
            #当前元对象（不包括自己）的d.data(=qt_meta_data_MainWindow)中methodCount的值
            int constructorCount() const;
            #当前元对象（不包括自己）的d.data(=qt_meta_data_MainWindow)中methodCount的值
            int methodCount() const;
            #当前元对象（不包括自己）的d.data(=qt_meta_data_MainWindow)中enumeratorCount的值
            int enumeratorCount() const;
            #当前元对象（不包括自己）的d.data(=qt_meta_data_MainWindow)中propertyCount的值
            int propertyCount() const;
            #当前元对象（不包括自己）的d.data(=qt_meta_data_MainWindow)中classInfoCount的值
            int classInfoCount() const;

          '获取各种成员索引号
            #遍历当前元对象d.data(=qt_meta_data_MainWindow)中每个构造函数信息，找到与constructor匹配的序号
            int indexOfConstructor(const char *constructor) const;
            #遍历当前元对象d.data(=qt_meta_data_MainWindow)中每个方法函数信息，找到与method匹配的序号
            int indexOfMethod(const char *method) const;
            #遍历当前元对象d.data(=qt_meta_data_MainWindow)中每个方法函数信息，找到与signal匹配的序号
            int indexOfSignal(const char *signal) const;
            #遍历当前元对象d.data(=qt_meta_data_MainWindow)中每个方法函数信息，找到与slot匹配的序号
            int indexOfSlot(const char *slot) const;
            #遍历当前元对象d.data(=qt_meta_data_MainWindow)中每个enumerator信息，找到与enumerator匹配的序号
            int indexOfEnumerator(const char *name) const;
            #遍历当前元对象d.data(=qt_meta_data_MainWindow)中每个property信息，找到与property匹配的序号
            int indexOfProperty(const char *name) const;
            #遍历当前元对象d.data(=qt_meta_data_MainWindow)中每个classInfo信息，找到与classInfo匹配的序号
            int indexOfClassInfo(const char *name) const;

          '获取索引对应元素的信息
            #获得priv(d.data)中第index个constructor的信息，赋值给result.handle，同时将对象自身指针赋值给result.mobj
            QMetaMethod constructor(int index) const;
            #获得priv(d.data)中第index个method的信息，赋值给result.handle，同时将对象自身指针赋值给result.mobj
            QMetaMethod method(int index) const;
            #获得priv(d.data)中第index个enumerator的信息，赋值给result.handle，同时将对象自身指针赋值给result.mobj
            QMetaEnum enumerator(int index) const;
            #获得priv(d.data)中第index个property的信息，赋值给result.handle，同时将对象自身指针赋值给result.mobj
            QMetaProperty property(int index) const;
            #获得priv(d.data)中第index个classInfo的信息，赋值给result.handle，同时将对象自身指针赋值给result.mobj
            QMetaClassInfo classInfo(int index) const;

          '未分类        
            QMetaProperty userProperty() const;

            static bool checkConnectArgs(const char *signal, const char *method);
            static QByteArray normalizedSignature(const char *method);
            static QByteArray normalizedType(const char *type);

          '信号槽连接
            #internal index-based connect
            static bool connect(const QObject *sender, int signal_index,
                                const QObject *receiver, int method_index,
                                int type = 0, int *types = 0);
            #internal index-based disconnect
            static bool disconnect(const QObject *sender, int signal_index,
                                   const QObject *receiver, int method_index);
            static bool disconnectOne(const QObject *sender, int signal_index,
                                      const QObject *receiver, int method_index);
            #internal slot-name based connect
            static void connectSlotsByName(QObject *o);

          '信号激活
            #internal index-based signal activation
            static void activate(QObject *sender, int signal_index, void **argv);  //obsolete
            static void activate(QObject *sender, int from_signal_index, int to_signal_index, void **argv); //obsolete
            static void activate(QObject *sender, const QMetaObject *, int local_signal_index, void **argv);
            static void activate(QObject *sender, const QMetaObject *, int from_local_signal_index, int to_local_signal_index, void **argv); //obsolete
        
          '未分类
            #internal guarded pointers
            static void addGuard(QObject **ptr);
            static void removeGuard(QObject **ptr);
            static void changeGuard(QObject **ptr, QObject *o);
        
          'invokeMethod
            static bool invokeMethod(QObject *obj, const char *member,
                                     Qt::ConnectionType,
                                     QGenericReturnArgument ret,
                                     QGenericArgument val0 = QGenericArgument(0),
                                     QGenericArgument val1 = QGenericArgument(),
                                     QGenericArgument val2 = QGenericArgument(),
                                     QGenericArgument val3 = QGenericArgument(),
                                     QGenericArgument val4 = QGenericArgument(),
                                     QGenericArgument val5 = QGenericArgument(),
                                     QGenericArgument val6 = QGenericArgument(),
                                     QGenericArgument val7 = QGenericArgument(),
                                     QGenericArgument val8 = QGenericArgument(),
                                     QGenericArgument val9 = QGenericArgument());

            static inline bool invokeMethod(QObject *obj, const char *member,
                                     QGenericReturnArgument ret,
                                     QGenericArgument val0 = QGenericArgument(0),
                                     QGenericArgument val1 = QGenericArgument(),
                                     QGenericArgument val2 = QGenericArgument(),
                                     QGenericArgument val3 = QGenericArgument(),
                                     QGenericArgument val4 = QGenericArgument(),
                                     QGenericArgument val5 = QGenericArgument(),
                                     QGenericArgument val6 = QGenericArgument(),
                                     QGenericArgument val7 = QGenericArgument(),
                                     QGenericArgument val8 = QGenericArgument(),
                                     QGenericArgument val9 = QGenericArgument())
                return invokeMethod(obj, member, Qt::AutoConnection, ret, val0, val1, val2, val3,
                        val4, val5, val6, val7, val8, val9);

            static inline bool invokeMethod(QObject *obj, const char *member,
                                     Qt::ConnectionType type,
                                     QGenericArgument val0 = QGenericArgument(0),
                                     QGenericArgument val1 = QGenericArgument(),
                                     QGenericArgument val2 = QGenericArgument(),
                                     QGenericArgument val3 = QGenericArgument(),
                                     QGenericArgument val4 = QGenericArgument(),
                                     QGenericArgument val5 = QGenericArgument(),
                                     QGenericArgument val6 = QGenericArgument(),
                                     QGenericArgument val7 = QGenericArgument(),
                                     QGenericArgument val8 = QGenericArgument(),
                                     QGenericArgument val9 = QGenericArgument())
                return invokeMethod(obj, member, type, QGenericReturnArgument(), val0, val1, val2,
                                         val3, val4, val5, val6, val7, val8, val9);

            static inline bool invokeMethod(QObject *obj, const char *member,
                                     QGenericArgument val0 = QGenericArgument(0),
                                     QGenericArgument val1 = QGenericArgument(),
                                     QGenericArgument val2 = QGenericArgument(),
                                     QGenericArgument val3 = QGenericArgument(),
                                     QGenericArgument val4 = QGenericArgument(),
                                     QGenericArgument val5 = QGenericArgument(),
                                     QGenericArgument val6 = QGenericArgument(),
                                     QGenericArgument val7 = QGenericArgument(),
                                     QGenericArgument val8 = QGenericArgument(),
                                     QGenericArgument val9 = QGenericArgument())
                return invokeMethod(obj, member, Qt::AutoConnection, QGenericReturnArgument(), val0,
                        val1, val2, val3, val4, val5, val6, val7, val8, val9);

          '创建对象
            QObject *newInstance(QGenericArgument val0 = QGenericArgument(0),
                                 QGenericArgument val1 = QGenericArgument(),
                                 QGenericArgument val2 = QGenericArgument(),
                                 QGenericArgument val3 = QGenericArgument(),
                                 QGenericArgument val4 = QGenericArgument(),
                                 QGenericArgument val5 = QGenericArgument(),
                                 QGenericArgument val6 = QGenericArgument(),
                                 QGenericArgument val7 = QGenericArgument(),
                                 QGenericArgument val8 = QGenericArgument(),
                                 QGenericArgument val9 = QGenericArgument()) const;
          
          'Call枚举类型声明
            enum Call {
                InvokeMetaMethod,
                ReadProperty,
                WriteProperty,
                ResetProperty,
                QueryPropertyDesignable,
                QueryPropertyScriptable,
                QueryPropertyStored,
                QueryPropertyEditable,
                QueryPropertyUser,
                CreateInstance
             };
             
          '未分类
            int static_metacall(Call, int, void **) const;
            static int metacall(QObject *, Call, int, void **);
        
        '数据成员
            struct { // private data
                const QMetaObject *superdata;
                const char *stringdata;
                const uint *data;
                const void *extradata;
            } d;
        
    =============================================================================================================

    struct QMetaObjectPrivate
      '数据成员
        int revision;
        int className;
        int classInfoCount, classInfoData;
        int methodCount, methodData;
        int propertyCount, propertyData;
        int enumeratorCount, enumeratorData;
        int constructorCount, constructorData; //since revision 2
        int flags; //since revision 3
        int signalCount; //since revision 4
        // revision 5 introduces changes in normalized signatures, no new members
        // revision 6 added qt_static_metacall as a member of each Q_OBJECT and inside QMetaObject itself
      
      '函数成员
        static inline const QMetaObjectPrivate *get(const QMetaObject *metaobject)
        { return reinterpret_cast<const QMetaObjectPrivate*>(metaobject->d.data); }

        static int indexOfSignalRelative(const QMetaObject **baseObject,
                                         const char* name,
                                         bool normalizeStringData);
        static int indexOfSlotRelative(const QMetaObject **m,
                               const char *slot,
                               bool normalizeStringData);
        static int originalClone(const QMetaObject *obj, int local_method_index);

        'ifndef QT_NO_QOBJECT
        //defined in qobject.cpp
        enum DisconnectType { DisconnectAll, DisconnectOne };
        static void memberIndexes(const QObject *obj, const QMetaMethod &member,
                                  int *signalIndex, int *methodIndex);
        static bool connect(const QObject *sender, int signal_index,
                            const QObject *receiver, int method_index_relative,
                            const QMetaObject *rmeta = 0,
                            int type = 0, int *types = 0);
        static bool disconnect(const QObject *sender, int signal_index,
                               const QObject *receiver, int method_index,
                               DisconnectType = DisconnectAll);
        static inline bool disconnectHelper(QObjectPrivate::Connection *c,
                                            const QObject *receiver, int method_index,
                                            QMutex *senderMutex, DisconnectType);
        'endif

    =============================================================================================================

    struct QMetaObjectExtraData
     {
        'ifdef Q_NO_DATA_RELOCATION
        const QMetaObjectAccessor *objects;
        'else
        const QMetaObject **objects;
        'endif

        typedef void (*StaticMetacallFunction)(QObject *, QMetaObject::Call, int, void **); //from revision 6
        //typedef int (*StaticMetaCall)(QMetaObject::Call, int, void **); //used from revison 2 until revison 5
        StaticMetacallFunction static_metacall;
     };

    =============================================================================================================

    class QMetaMethod
     {
     public:
        inline QMetaMethod() : mobj(0),handle(0) {}

        const char *signature() const;
        const char *typeName() const;
        QList<QByteArray> parameterTypes() const;
        QList<QByteArray> parameterNames() const;
        const char *tag() const;
        enum Access { Private, Protected, Public };
        Access access() const;
        enum MethodType { Method, Signal, Slot, Constructor };
        MethodType methodType() const;
        enum Attributes { Compatibility = 0x1, Cloned = 0x2, Scriptable = 0x4 };
        int attributes() const;
        int methodIndex() const;
        int revision() const;

        inline const QMetaObject *enclosingMetaObject() const { return mobj; }

        bool invoke(QObject *object,
                    Qt::ConnectionType connectionType,
                    QGenericReturnArgument returnValue,
                    QGenericArgument val0 = QGenericArgument(0),
                    QGenericArgument val1 = QGenericArgument(),
                    QGenericArgument val2 = QGenericArgument(),
                    QGenericArgument val3 = QGenericArgument(),
                    QGenericArgument val4 = QGenericArgument(),
                    QGenericArgument val5 = QGenericArgument(),
                    QGenericArgument val6 = QGenericArgument(),
                    QGenericArgument val7 = QGenericArgument(),
                    QGenericArgument val8 = QGenericArgument(),
                    QGenericArgument val9 = QGenericArgument()) const;
        inline bool invoke(QObject *object,
                           QGenericReturnArgument returnValue,
                           QGenericArgument val0 = QGenericArgument(0),
                           QGenericArgument val1 = QGenericArgument(),
                           QGenericArgument val2 = QGenericArgument(),
                           QGenericArgument val3 = QGenericArgument(),
                           QGenericArgument val4 = QGenericArgument(),
                           QGenericArgument val5 = QGenericArgument(),
                           QGenericArgument val6 = QGenericArgument(),
                           QGenericArgument val7 = QGenericArgument(),
                           QGenericArgument val8 = QGenericArgument(),
                           QGenericArgument val9 = QGenericArgument()) const
        {
            return invoke(object, Qt::AutoConnection, returnValue,
                          val0, val1, val2, val3, val4, val5, val6, val7, val8, val9);
        }
        inline bool invoke(QObject *object,
                           Qt::ConnectionType connectionType,
                           QGenericArgument val0 = QGenericArgument(0),
                           QGenericArgument val1 = QGenericArgument(),
                           QGenericArgument val2 = QGenericArgument(),
                           QGenericArgument val3 = QGenericArgument(),
                           QGenericArgument val4 = QGenericArgument(),
                           QGenericArgument val5 = QGenericArgument(),
                           QGenericArgument val6 = QGenericArgument(),
                           QGenericArgument val7 = QGenericArgument(),
                           QGenericArgument val8 = QGenericArgument(),
                           QGenericArgument val9 = QGenericArgument()) const
        {
            return invoke(object, connectionType, QGenericReturnArgument(),
                          val0, val1, val2, val3, val4, val5, val6, val7, val8, val9);
        }
        inline bool invoke(QObject *object,
                           QGenericArgument val0 = QGenericArgument(0),
                           QGenericArgument val1 = QGenericArgument(),
                           QGenericArgument val2 = QGenericArgument(),
                           QGenericArgument val3 = QGenericArgument(),
                           QGenericArgument val4 = QGenericArgument(),
                           QGenericArgument val5 = QGenericArgument(),
                           QGenericArgument val6 = QGenericArgument(),
                           QGenericArgument val7 = QGenericArgument(),
                           QGenericArgument val8 = QGenericArgument(),
                           QGenericArgument val9 = QGenericArgument()) const
        {
            return invoke(object, Qt::AutoConnection, QGenericReturnArgument(),
                          val0, val1, val2, val3, val4, val5, val6, val7, val8, val9);
        }

     private:
        const QMetaObject *mobj;
        uint handle;
        friend struct QMetaObject;
        friend struct QMetaObjectPrivate;
        friend class QObject;
     };

    =============================================================================================================

    class QMetaEnum
     {
     public:
        inline QMetaEnum() : mobj(0),handle(0) {}

        const char *name() const;
        bool isFlag() const;

        int keyCount() const;
        const char *key(int index) const;
        int value(int index) const;

        const char *scope() const;

        int keyToValue(const char *key) const;
        const char* valueToKey(int value) const;
        int keysToValue(const char * keys) const;
        QByteArray valueToKeys(int value) const;

        inline const QMetaObject *enclosingMetaObject() const { return mobj; }

        inline bool isValid() const { return name() != 0; }
     private:
        const QMetaObject *mobj;
        uint handle;
        friend struct QMetaObject;
     };

    =============================================================================================================

    class QMetaProperty
     {
     public:
        QMetaProperty();

        const char *name() const;
        const char *typeName() const;
        QVariant::Type type() const;
        int userType() const;
        int propertyIndex() const;

        bool isReadable() const;
        bool isWritable() const;
        bool isResettable() const;
        bool isDesignable(const QObject *obj = 0) const;
        bool isScriptable(const QObject *obj = 0) const;
        bool isStored(const QObject *obj = 0) const;
        bool isEditable(const QObject *obj = 0) const;
        bool isUser(const QObject *obj = 0) const;
        bool isConstant() const;
        bool isFinal() const;

        bool isFlagType() const;
        bool isEnumType() const;
        QMetaEnum enumerator() const;

        bool hasNotifySignal() const;
        QMetaMethod notifySignal() const;
        int notifySignalIndex() const;

        int revision() const;

        QVariant read(const QObject *obj) const;
        bool write(QObject *obj, const QVariant &value) const;
        bool reset(QObject *obj) const;

        bool hasStdCppSet() const;
        inline bool isValid() const { return isReadable(); }
        inline const QMetaObject *enclosingMetaObject() const { return mobj; }

     private:
        const QMetaObject *mobj;
        uint handle;
        int idx;
        QMetaEnum menum;
        friend struct QMetaObject;
     };

    =============================================================================================================

    class QMetaClassInfo
     {
     public:
        inline QMetaClassInfo() : mobj(0),handle(0) {}
        const char *name() const;
        const char *value() const;
        inline const QMetaObject *enclosingMetaObject() const { return mobj; }
     private:
        const QMetaObject *mobj;
        uint handle;
        friend struct QMetaObject;
     };

    =============================================================================================================
    
    class QObject
     {
        Q_OBJECT
        Q_PROPERTY(QString objectName READ objectName WRITE setObjectName)  #Q_PROPERTY需要用moc进行编译
        Q_DECLARE_PRIVATE(QObject)
      public:
        Q_INVOKABLE explicit QObject(QObject *parent=0);
        virtual ~QObject();

        #属性方法
        QString objectName() const;
        void setObjectName(const QString &name);
        
        virtual bool event(QEvent *);
        virtual bool eventFilter(QObject *, QEvent *);

        'ifdef qdoc
        static QString tr(const char *sourceText, const char *comment = 0, int n = -1);
        static QString trUtf8(const char *sourceText, const char *comment = 0, int n = -1);
        virtual const QMetaObject *metaObject() const;
        static const QMetaObject staticMetaObject;
        'endif
        
        'ifdef QT_NO_TRANSLATION
        static QString tr(const char *sourceText, const char *, int)
            { return QString::fromLatin1(sourceText); }
        static QString tr(const char *sourceText, const char * = 0)
            { return QString::fromLatin1(sourceText); }
        'ifndef QT_NO_TEXTCODEC
        static QString trUtf8(const char *sourceText, const char *, int)
            { return QString::fromUtf8(sourceText); }
        static QString trUtf8(const char *sourceText, const char * = 0)
            { return QString::fromUtf8(sourceText); }
        'endif
        'endif //QT_NO_TRANSLATION

        inline bool isWidgetType() const { return d_ptr->isWidget; }

        inline bool signalsBlocked() const { return d_ptr->blockSig; }
        bool blockSignals(bool b);

        QThread *thread() const;
        void moveToThread(QThread *thread);

        int startTimer(int interval);
        void killTimer(int id);

        template<typename T>
        inline T findChild(const QString &aName = QString()) const
        { return static_cast<T>(qt_qFindChild_helper(this, aName, reinterpret_cast<T>(0)->staticMetaObject)); }

        template<typename T>
        inline QList<T> findChildren(const QString &aName = QString()) const
        {
            QList<T> list;
            union {
                QList<T> *typedList;
                QList<void *> *voidList;
            } u;
            u.typedList = &list;
            qt_qFindChildren_helper(this, aName, 0, reinterpret_cast<T>(0)->staticMetaObject, u.voidList);
            return list;
        }

        'ifndef QT_NO_REGEXP
        template<typename T>
        inline QList<T> findChildren(const QRegExp &re) const
        {
            QList<T> list;
            union {
                QList<T> *typedList;
                QList<void *> *voidList;
            } u;
            u.typedList = &list;
            qt_qFindChildren_helper(this, QString(), &re, reinterpret_cast<T>(0)->staticMetaObject, u.voidList);
            return list;
        }
        'endif

        inline const QObjectList &children() const { return d_ptr->children; }

        void setParent(QObject *);
        void installEventFilter(QObject *);
        void removeEventFilter(QObject *);

        static bool connect(const QObject *sender, const char *signal,
                            const QObject *receiver, const char *member, Qt::ConnectionType =
                            'ifdef qdoc
                            Qt::AutoConnection
                            'else
                            Qt::AutoConnection
                            'endif
                            );
            
        static bool connect(const QObject *sender, const QMetaMethod &signal,
                            const QObject *receiver, const QMetaMethod &method,
                            Qt::ConnectionType type = 
                            'ifdef qdoc
                            Qt::AutoConnection
                            'else
                            Qt::AutoConnection
                            'endif
                            );

        inline bool connect(const QObject *sender, const char *signal,
                            const char *member, Qt::ConnectionType type =
                            'ifdef qdoc
                            Qt::AutoConnection
                            'else
                            Qt::AutoConnection
                            'endif
                            ) const;

        static bool disconnect(const QObject *sender, const char *signal,
                               const QObject *receiver, const char *member);
        static bool disconnect(const QObject *sender, const QMetaMethod &signal,
                               const QObject *receiver, const QMetaMethod &member);
        inline bool disconnect(const char *signal = 0,
                               const QObject *receiver = 0, const char *member = 0)
            { return disconnect(this, signal, receiver, member); }
        inline bool disconnect(const QObject *receiver, const char *member = 0)
            { return disconnect(this, 0, receiver, member); }

        void dumpObjectTree();
        void dumpObjectInfo();

        'ifndef QT_NO_PROPERTIES
        bool setProperty(const char *name, const QVariant &value);
        QVariant property(const char *name) const;
        QList<QByteArray> dynamicPropertyNames() const;
        'endif // QT_NO_PROPERTIES

        'ifndef QT_NO_USERDATA
        static uint registerUserData();
        void setUserData(uint id, QObjectUserData* data);
        QObjectUserData* userData(uint id) const;
        'endif // QT_NO_USERDATA

      Q_SIGNALS:
        void destroyed(QObject * = 0);

      public:
        inline QObject *parent() const { return d_ptr->parent; }

        inline bool inherits(const char *classname) const
            { return const_cast<QObject *>(this)->qt_metacast(classname) != 0; }

      public Q_SLOTS:
        void deleteLater();

      protected:
        QObject *sender() const;
        int senderSignalIndex() const;
        int receivers(const char* signal) const;

        virtual void timerEvent(QTimerEvent *);
        virtual void childEvent(QChildEvent *);
        virtual void customEvent(QEvent *);

        virtual void connectNotify(const char *signal);
        virtual void disconnectNotify(const char *signal);

      protected:
        QObject(QObjectPrivate &dd, QObject *parent = 0);

      protected:
        QScopedPointer<QObjectData> d_ptr;

        static const QMetaObject staticQtMetaObject;

        friend struct QMetaObject;
        friend class QApplication;
        friend class QApplicationPrivate;
        friend class QCoreApplication;
        friend class QCoreApplicationPrivate;
        friend class QWidget;
        friend class QThreadData;

      private:
        Q_DISABLE_COPY(QObject)
        Q_PRIVATE_SLOT(d_func(), void _q_reregisterTimers(void *))
     };

=============================================================================================================


=============================================================================================================


=============================================================================================================

QMetaObject类函数实现
    inline const char *QMetaObject::className() const
     { return d.stringdata; }

    inline const QMetaObject *QMetaObject::superClass() const
     { return d.superdata; }
     
    inline const char *QMetaObject::superClassName() const
     { return d.superdata ? d.superdata->className() : 0; }

    QObject *QMetaObject::newInstance(QGenericArgument val0,
                                      QGenericArgument val1,
                                      QGenericArgument val2,
                                      QGenericArgument val3,
                                      QGenericArgument val4,
                                      QGenericArgument val5,
                                      QGenericArgument val6,
                                      QGenericArgument val7,
                                      QGenericArgument val8,
                                      QGenericArgument val9) const
     {
        QByteArray constructorName = className();
        {
            int idx = constructorName.lastIndexOf(':');
            if (idx != -1)
                constructorName.remove(0, idx+1); // remove qualified part
        }
        QVarLengthArray<char, 512> sig;
        sig.append(constructorName.constData(), constructorName.length());
        sig.append('(');

        enum { MaximumParamCount = 10 };
        const char *typeNames[] = {val0.name(), val1.name(), val2.name(), val3.name(), val4.name(),
                                   val5.name(), val6.name(), val7.name(), val8.name(), val9.name()};

        int paramCount;
        for (paramCount = 0; paramCount < MaximumParamCount; ++paramCount) {
            int len = qstrlen(typeNames[paramCount]);
            if (len <= 0)
                break;
            sig.append(typeNames[paramCount], len);
            sig.append(',');
        }
        if (paramCount == 0)
            sig.append(')'); // no parameters
        else
            sig[sig.size() - 1] = ')';
        sig.append('\0');

        int idx = indexOfConstructor(sig.constData());
        if (idx < 0) {
            QByteArray norm = QMetaObject::normalizedSignature(sig.constData());
            idx = indexOfConstructor(norm.constData());
        }
        if (idx < 0)
            return 0;

        QVariant ret(QMetaType::QObjectStar, (void*)0);
        void *param[] = {ret.data(), val0.data(), val1.data(), val2.data(), val3.data(), val4.data(),
                         val5.data(), val6.data(), val7.data(), val8.data(), val9.data()};

        if (static_metacall(CreateInstance, idx, param) >= 0)
            return 0;
        return *reinterpret_cast<QObject**>(param[0]);
     }

    int QMetaObject::static_metacall(Call cl, int idx, void **argv) const
     {
        const QMetaObjectExtraData *extra = reinterpret_cast<const QMetaObjectExtraData *>(d.extradata);
        if (priv(d.data)->revision >= 6) {
            if (!extra || !extra->static_metacall)
                return 0;
            extra->static_metacall(0, cl, idx, argv);
            return -1;
        } else if (priv(d.data)->revision >= 2) {
            if (!extra || !extra->static_metacall)
                return 0;
            typedefine int (*OldMetacall)(QMetaObject::Call, int, void **);
            OldMetacall o = reinterpret_cast<OldMetacall>(extra->static_metacall);
            return o(cl, idx, argv);
        }
        return 0;
     }

    int QMetaObject::metacall(QObject *object, Call cl, int idx, void **argv)
     {
        if (QMetaObject *mo = object->d_ptr->metaObject)
            return static_cast<QAbstractDynamicMetaObject*>(mo)->metaCall(cl, idx, argv);
        else
            return object->qt_metacall(cl, idx, argv);
     }

    #用于向参数给定的子类转换：查找参数的父级链，如果元对象与当前类的元对象一致，则返回该参数，否则返回0
    QObject *QMetaObject::cast(QObject *obj) const
     {
        if (obj) {
            const QMetaObject *m = obj->metaObject();
            do {
                if (m == this)
                    return obj;
            } while ((m = m->d.superdata));
        }
        return 0;
     }

    const QObject *QMetaObject::cast(const QObject *obj) const
     {
        if (obj) {
            const QMetaObject *m = obj->metaObject();
            do {
                if (m == this)
                    return obj;
            } while ((m = m->d.superdata));
        }
        return 0;
     }

    QString QMetaObject::tr(const char *s, const char *c) const
     {
        return QCoreApplication::translate(d.stringdata, s, c, QCoreApplication::CodecForTr);
     }

    QString QMetaObject::tr(const char *s, const char *c, int n) const
     {
        return QCoreApplication::translate(d.stringdata, s, c, QCoreApplication::CodecForTr, n);
     }

    QString QMetaObject::trUtf8(const char *s, const char *c) const
     {
        return QCoreApplication::translate(d.stringdata, s, c, QCoreApplication::UnicodeUTF8);
     }

    QString QMetaObject::trUtf8(const char *s, const char *c, int n) const
     {
        return QCoreApplication::translate(d.stringdata, s, c, QCoreApplication::UnicodeUTF8, n);
     }

    #各父级元对象（不包括自己）的d.data(=qt_meta_data_MainWindow)中methodCount的累加和
    int QMetaObject::methodOffset() const
     {
        int offset = 0;
        const QMetaObject *m = d.superdata;
        while (m) {
            offset += priv(m->d.data)->methodCount;
            m = m->d.superdata;
        }
        return offset;
     }
     
    static inline const QMetaObjectPrivate *priv(const uint* data)
     { return reinterpret_cast<const QMetaObjectPrivate*>(data); }

    int QMetaObject::enumeratorOffset() const
     {
        int offset = 0;
        const QMetaObject *m = d.superdata;
        while (m) {
            offset += priv(m->d.data)->enumeratorCount;
            m = m->d.superdata;
        }
        return offset;
     }

    int QMetaObject::propertyOffset() const
     {
        int offset = 0;
        const QMetaObject *m = d.superdata;
        while (m) {
            offset += priv(m->d.data)->propertyCount;
            m = m->d.superdata;
        }
        return offset;
     }

    int QMetaObject::classInfoOffset() const
     {
        int offset = 0;
        const QMetaObject *m = d.superdata;
        while (m) {
            offset += priv(m->d.data)->classInfoCount;
            m = m->d.superdata;
        }
        return offset;
     }

    int QMetaObject::constructorCount() const
     {
        if (priv(d.data)->revision < 2)
            return 0;
        return priv(d.data)->constructorCount;
     }

    int QMetaObject::methodCount() const
     {
        int n = priv(d.data)->methodCount;
        const QMetaObject *m = d.superdata;
        while (m) {
            n += priv(m->d.data)->methodCount;
            m = m->d.superdata;
         }
        return n;
     }

    int QMetaObject::enumeratorCount() const
     {
        int n = priv(d.data)->enumeratorCount;
        const QMetaObject *m = d.superdata;
        while (m) {
            n += priv(m->d.data)->enumeratorCount;
            m = m->d.superdata;
         }
        return n;
     }

    int QMetaObject::propertyCount() const
     {
        int n = priv(d.data)->propertyCount;
        const QMetaObject *m = d.superdata;
        while (m) {
            n += priv(m->d.data)->propertyCount;
            m = m->d.superdata;
         }
        return n;
     }

    int QMetaObject::classInfoCount() const
     {
        int n = priv(d.data)->classInfoCount;
        const QMetaObject *m = d.superdata;
        while (m) {
            n += priv(m->d.data)->classInfoCount;
            m = m->d.superdata;
         }
        return n;
     }

    #遍历当前元对象d.data(=qt_meta_data_MainWindow)中每个构造函数信息，找到与constructor的序号
    int QMetaObject::indexOfConstructor(const char *constructor) const
     {
        if (priv(d.data)->revision < 2)
            return -1;
        for (int i = priv(d.data)->constructorCount-1; i >= 0; --i) {
            const char *data = d.stringdata + d.data[priv(d.data)->constructorData + 5*i];
            if (data[0] == constructor[0] && strcmp(constructor + 1, data + 1) == 0) {
                return i;
             }
         }
        return -1;
     }

    #返回method在d.data(=qt_meta_data_MainWindow)数组中的位置（可能是某级父类中的位置）
    int QMetaObject::indexOfMethod(const char *method) const
     {
        const QMetaObject *m = this;
        int i = indexOfMethodRelative<0>(&m, method, false);
        if (i < 0) {
            m = this;
            i = indexOfMethodRelative<0>(&m, method, true);
         }
        if (i >= 0)
            i += m->methodOffset();
        return i;
     }

    #MethodType用于表明是信号函数，还是槽函数，还是所有函数，这会影响寻找范围
    #遍历baseObject类及各级父类，
    #   遍历d.data(=qt_meta_data_MainWindow)中记录的方法名/信号函数名/槽函数名，
    #       if(normalizeStringData)  将参数名用QMetaObject::normalizedSignature处理
    #       法名与method参数比较
    #       如果相同，就将该类指针存给baseObject，并函数返回函数序号
    #   找不到，返回 -1
    template<int MethodType>
    static inline int indexOfMethodRelative(const QMetaObject **baseObject,
                                            const char *method,
                                            bool normalizeStringData)
     {
        for (const QMetaObject *m = *baseObject; m; m = m->d.superdata) {
            int i = (MethodType == MethodSignal/*=4*/ && priv(m->d.data)->revision >= 4)
                    ? (priv(m->d.data)->signalCount - 1) : (priv(m->d.data)->methodCount - 1);
            const int end = (MethodType == MethodSlot/*=8*/ && priv(m->d.data)->revision >= 4)
                            ? (priv(m->d.data)->signalCount) : 0;
            if (!normalizeStringData) {
                for (; i >= end; --i) {
                    const char *stringdata = m->d.stringdata + m->d.data[priv(m->d.data)->methodData + 5*i];
                    if (method[0] == stringdata[0] && strcmp(method + 1, stringdata + 1) == 0) {
                        *baseObject = m;
                        return i;
                    }
                }
            } else if (priv(m->d.data)->revision < 5) {
                for (; i >= end; --i) {
                    const char *stringdata = (m->d.stringdata + m->d.data[priv(m->d.data)->methodData + 5 * i]);
                    const QByteArray normalizedSignature = QMetaObject::normalizedSignature(stringdata);
                    if (normalizedSignature == method) {
                        *baseObject = m;
                        return i;
                    }
                }
            }
        }
        return -1;
     }

    int QMetaObject::indexOfSignal(const char *signal) const
     {
        const QMetaObject *m = this;
        int i = QMetaObjectPrivate::indexOfSignalRelative(&m, signal, false);
        if (i < 0) {
            m = this;
            i = QMetaObjectPrivate::indexOfSignalRelative(&m, signal, true);
         }
        if (i >= 0)
            i += m->methodOffset();
        return i;
     }

    int QMetaObjectPrivate::indexOfSignalRelative(const QMetaObject **baseObject,
                                                  const char *signal,
                                                  bool normalizeStringData)
     {
        int i = indexOfMethodRelative<MethodSignal>(baseObject, signal, normalizeStringData);
        const QMetaObject *m = *baseObject;
        if (i >= 0 && m && m->d.superdata) {
            int conflict = m->d.superdata->indexOfMethod(signal);
            if (conflict >= 0)
                qWarning("QMetaObject::indexOfSignal: signal %s from %s redefined in %s",
                         signal, m->d.superdata->d.stringdata, m->d.stringdata);
         }
        return i;
     }

    int QMetaObject::indexOfSlot(const char *slot) const
     {
        const QMetaObject *m = this;
        int i = QMetaObjectPrivate::indexOfSlotRelative(&m, slot, false);
        if (i < 0)
            i = QMetaObjectPrivate::indexOfSlotRelative(&m, slot, true);
        if (i >= 0)
            i += m->methodOffset();
        return i;
     }

     int QMetaObject::indexOfEnumerator(const char *name) const
     {
        const QMetaObject *m = this;
        while (m) {
            const QMetaObjectPrivate *d = priv(m->d.data);
            for (int i = d->enumeratorCount - 1; i >= 0; --i) {
                const char *prop = m->d.stringdata + m->d.data[d->enumeratorData + 4*i];
                if (name[0] == prop[0] && strcmp(name + 1, prop + 1) == 0) {
                    i += m->enumeratorOffset();
                    return i;
                 }
             }
            m = m->d.superdata;
         }
        return -1;
     }

    int QMetaObject::indexOfProperty(const char *name) const
     {
        const QMetaObject *m = this;
        while (m) {
            const QMetaObjectPrivate *d = priv(m->d.data);
            for (int i = d->propertyCount-1; i >= 0; --i) {
                const char *prop = m->d.stringdata + m->d.data[d->propertyData + 3*i];
                if (name[0] == prop[0] && strcmp(name + 1, prop + 1) == 0) {
                    i += m->propertyOffset();
                    return i;
                 }
             }
            m = m->d.superdata;
         }

        if (priv(this->d.data)->revision >= 3 && (priv(this->d.data)->flags & DynamicMetaObject)) {
            QAbstractDynamicMetaObject *me = 
                const_cast<QAbstractDynamicMetaObject *>(static_cast<const QAbstractDynamicMetaObject *>(this));

            return me->createProperty(name, 0);
         }

        return -1;
     }

    int QMetaObject::indexOfClassInfo(const char *name) const
     {
        int i = -1;
        const QMetaObject *m = this;
        while (m && i < 0) {
            for (i = priv(m->d.data)->classInfoCount-1; i >= 0; --i)
                if (strcmp(name, m->d.stringdata
                           + m->d.data[priv(m->d.data)->classInfoData + 2*i]) == 0) {
                    i += m->classInfoOffset();
                    break;
                 }
            m = m->d.superdata;
         }
        return i;
     }
    
    #获得priv(d.data)中第index个constructor的信息，赋值给result.handle，同时将对象自身指针赋值给result.mobj
    QMetaMethod QMetaObject::constructor(int index) const
     {
        int i = index;
        QMetaMethod result;
        if (priv(d.data)->revision >= 2 && i >= 0 && i < priv(d.data)->constructorCount) {
            result.mobj = this;
            result.handle = priv(d.data)->constructorData + 5*i;
         }
        return result;
     }

    #获得priv(d.data)中第index个method的信息，赋值给result.handle，同时将对象自身指针赋值给result.mobj
    QMetaMethod QMetaObject::method(int index) const
     {
        int i = index;
        i -= methodOffset();
        if (i < 0 && d.superdata)
            return d.superdata->method(index);

        QMetaMethod result;
        if (i >= 0 && i < priv(d.data)->methodCount) {
            result.mobj = this;
            result.handle = priv(d.data)->methodData + 5*i;
         }
        return result;
     }

    QMetaEnum QMetaObject::enumerator(int index) const
     {
        int i = index;
        i -= enumeratorOffset();
        if (i < 0 && d.superdata)
            return d.superdata->enumerator(index);

        QMetaEnum result;
        if (i >= 0 && i < priv(d.data)->enumeratorCount) {
            result.mobj = this;
            result.handle = priv(d.data)->enumeratorData + 4*i;
         }
        return result;
     }

    QMetaProperty QMetaObject::property(int index) const
     {
        int i = index;
        i -= propertyOffset();
        if (i < 0 && d.superdata)
            return d.superdata->property(index);

        QMetaProperty result;
        if (i >= 0 && i < priv(d.data)->propertyCount) {
            int handle = priv(d.data)->propertyData + 3*i;
            int flags = d.data[handle + 2];
            const char *type = d.stringdata + d.data[handle + 1];
            result.mobj = this;
            result.handle = handle;
            result.idx = i;

            if (flags & EnumOrFlag) {
                result.menum = enumerator(indexOfEnumerator(type));
                if (!result.menum.isValid()) {
                    QByteArray enum_name = type;
                    QByteArray scope_name = d.stringdata;
                    int s = enum_name.lastIndexOf("::");
                    if (s > 0) {
                        scope_name = enum_name.left(s);
                        enum_name = enum_name.mid(s + 2);
                     }
                    const QMetaObject *scope = 0;
                    if (scope_name == "Qt")
                        scope = &QObject::staticQtMetaObject;
                    else
                        scope = QMetaObject_findMetaObject(this, scope_name);
                    if (scope)
                        result.menum = scope->enumerator(scope->indexOfEnumerator(enum_name));
                 }
             }
         }
        return result;
     }
     
     #遍历本节点及各级父节点
     #取 ((QMetaObjectExtraData *)d.extradata)->objects
     static const QMetaObject *QMetaObject_findMetaObject(const QMetaObject *self, const char *name)
     {
        while (self) {
            if (strcmp(self->d.stringdata, name) == 0)
                return self;
            if (self->d.extradata) {
                'ifdefine Q_NO_DATA_RELOCATION
                const QMetaObjectAccessor *e;
                Q_ASSERT(priv(self->d.data)->revision >= 2);
                'else
                const QMetaObject **e;
                if (priv(self->d.data)->revision < 2) {
                    e = (const QMetaObject**)(self->d.extradata);
                 } else
                'endif
                 {
                    const QMetaObjectExtraData *extra = (const QMetaObjectExtraData*)(self->d.extradata);
                    e = extra->objects;
                 }
                if (e) {
                    while (*e) {
                        'ifdefine Q_NO_DATA_RELOCATION
                        if (const QMetaObject *m =QMetaObject_findMetaObject(&((*e)()), name))
                        'else
                        if (const QMetaObject *m =QMetaObject_findMetaObject((*e), name))
                        'endif
                            return m;
                        ++e;
                     }
                 }
             }
            self = self->d.superdata;
         }
        return self;
     }

    QMetaProperty QMetaObject::userProperty() const
     {
        const int propCount = propertyCount();
        for (int i = propCount - 1; i >= 0; --i) {
            const QMetaProperty prop = property(i);
            if (prop.isUser())
                return prop;
         }
        return QMetaProperty();
     }

    QMetaClassInfo QMetaObject::classInfo(int index) const
     {
        int i = index;
        i -= classInfoOffset();
        if (i < 0 && d.superdata)
            return d.superdata->classInfo(index);

        QMetaClassInfo result;
        if (i >= 0 && i < priv(d.data)->classInfoCount) {
            result.mobj = this;
            result.handle = priv(d.data)->classInfoData + 2*i;
         }
        return result;
     }

    bool QMetaObject::checkConnectArgs(const char *signal, const char *method)
     {
        const char *s1 = signal;
        const char *s2 = method;
        while (*s1++ != '(') { }                        // scan to first '('
        while (*s2++ != '(') { }
        if (*s2 == ')' || qstrcmp(s1,s2) == 0)        // method has no args or
            return true;                                //   exact match
        int s1len = qstrlen(s1);
        int s2len = qstrlen(s2);
        if (s2len < s1len && strncmp(s1,s2,s2len-1)==0 && s1[s2len-1]==',')
            return true;                                // method has less args
        return false;
     }
    
    QByteArray QMetaObject::normalizedType(const char *type)
     {
        QByteArray result;

        if (!type || !*type)
            return result;

        QVarLengthArray<char> stackbuf(qstrlen(type) + 1);
        qRemoveWhitespace(type, stackbuf.data());
        int templdepth = 0;
        qNormalizeType(stackbuf.data(), templdepth, result);

        return result;
     }

    QByteArray QMetaObject::normalizedSignature(const char *method)
     {
        QByteArray result;
        if (!method || !*method)
            return result;
        int len = int(strlen(method));
        QVarLengthArray<char> stackbuf(len + 1);
        char *d = stackbuf.data();
        qRemoveWhitespace(method, d);

        result.reserve(len);

        int argdepth = 0;
        int templdepth = 0;
        while (*d) {
            if (argdepth == 1) {
                d = qNormalizeType(d, templdepth, result);
                if (!*d) //most likely an invalid signature.
                    break;
             }
            if (*d == '(')
                ++argdepth;
            if (*d == ')')
                --argdepth;
            result += *d++;
         }

        return result;
     }

    bool QMetaObject::invokeMethod(QObject *obj,
                                   const char *member,
                                   Qt::ConnectionType type,
                                   QGenericReturnArgument ret,
                                   QGenericArgument val0,
                                   QGenericArgument val1,
                                   QGenericArgument val2,
                                   QGenericArgument val3,
                                   QGenericArgument val4,
                                   QGenericArgument val5,
                                   QGenericArgument val6,
                                   QGenericArgument val7,
                                   QGenericArgument val8,
                                   QGenericArgument val9)
     {
        if (!obj)
            return false;

        QVarLengthArray<char, 512> sig;
        int len = qstrlen(member);
        if (len <= 0)
            return false;
        sig.append(member, len);
        sig.append('(');

        const char *typeNames[] = {ret.name(), val0.name(), val1.name(), val2.name(), val3.name(),
                                   val4.name(), val5.name(), val6.name(), val7.name(), val8.name(),
                                   val9.name()};

        int paramCount;
        for (paramCount = 1; paramCount < MaximumParamCount; ++paramCount) {
            len = qstrlen(typeNames[paramCount]);
            if (len <= 0)
                break;
            sig.append(typeNames[paramCount], len);
            sig.append(',');
         }
        if (paramCount == 1)
            sig.append(')'); // no parameters
        else
            sig[sig.size() - 1] = ')';
        sig.append('\0');

        int idx = obj->metaObject()->indexOfMethod(sig.constData());
        if (idx < 0) {
            QByteArray norm = QMetaObject::normalizedSignature(sig.constData());
            idx = obj->metaObject()->indexOfMethod(norm.constData());
         }

        if (idx < 0 || idx >= obj->metaObject()->methodCount()) {
            qWarning("QMetaObject::invokeMethod: No such method %s::%s",
                     obj->metaObject()->className(), sig.constData());
            return false;
         }
        QMetaMethod method = obj->metaObject()->method(idx);
        return method.invoke(obj, type, ret,
                             val0, val1, val2, val3, val4, val5, val6, val7, val8, val9);
     }
     
    void QMetaObject::addGuard(QObject **ptr)
     {
        if (!*ptr)
            return;
        GuardHash *hash = guardHash();
        if (!hash) {
            *ptr = 0;
            return;
        }
        QMutexLocker locker(guardHashLock());
        QObjectPrivate::get(*ptr)->hasGuards = true;
        hash->insert(*ptr, ptr);
     }

    void QMetaObject::removeGuard(QObject **ptr)
     {
        if (!*ptr)
            return;
        GuardHash *hash = guardHash();
        /* check that the hash is empty - otherwise we might detach
           the shared_null hash, which will alloc, which is not nice */
        if (!hash || hash->isEmpty())
            return;
        QMutexLocker locker(guardHashLock());
        if (!*ptr) //check again, under the lock
            return;
        GuardHash::iterator it = hash->find(*ptr);
        const GuardHash::iterator end = hash->end();
        bool more = false; //if the QObject has more pointer attached to it.
        for (; it.key() == *ptr && it != end; ++it) {
            if (it.value() == ptr) {
                it = hash->erase(it);
                if (!more) more = (it != end && it.key() == *ptr);
                break;
            }
            more = true;
        }
        if (!more)
            QObjectPrivate::get(*ptr)->hasGuards = false;
     } 
    
    void QMetaObject::changeGuard(QObject **ptr, QObject *o)
     {
        GuardHash *hash = guardHash();
        if (!hash) {
            *ptr = 0;
            return;
        }
        QMutexLocker locker(guardHashLock());
        if (o) {
            hash->insert(o, ptr);
            QObjectPrivate::get(o)->hasGuards = true;
        }
        if (*ptr) {
            bool more = false; //if the QObject has more pointer attached to it.
            GuardHash::iterator it = hash->find(*ptr);
            const GuardHash::iterator end = hash->end();
            for (; it.key() == *ptr && it != end; ++it) {
                if (it.value() == ptr) {
                    it = hash->erase(it);
                    if (!more) more = (it != end && it.key() == *ptr);
                    break;
                }
                more = true;
            }
            if (!more)
                QObjectPrivate::get(*ptr)->hasGuards = false;
        }
        *ptr = o;
     }
    
    bool QMetaObject::connect(const QObject *sender, int signal_index,
                          const QObject *receiver, int method_index, int type, int *types)
     {
        signal_index = methodIndexToSignalIndex(sender->metaObject(), signal_index);
        return QMetaObjectPrivate::connect(sender, signal_index,
                                           receiver, method_index,
                                           0, //FIXME, we could speed this connection up by computing the relative index
                                           type, types);
     }

    bool QMetaObject::disconnectOne(const QObject *sender, int signal_index,
                                    const QObject *receiver, int method_index)
     {
        signal_index = methodIndexToSignalIndex(sender->metaObject(), signal_index);
        return QMetaObjectPrivate::disconnect(sender, signal_index,
                                              receiver, method_index,
                                              QMetaObjectPrivate::DisconnectOne);
     }

    void QMetaObject::connectSlotsByName(QObject *o)
     {
        if (!o)
            return;
        const QMetaObject *mo = o->metaObject();
        Q_ASSERT(mo);
        const QObjectList list = o->findChildren<QObject *>(QString());
        for (int i = 0; i < mo->methodCount(); ++i) {
            const char *slot = mo->method(i).signature();
            Q_ASSERT(slot);
            if (slot[0] != 'o' || slot[1] != 'n' || slot[2] != '_')
                continue;
            bool foundIt = false;
            for(int j = 0; j < list.count(); ++j) {
                const QObject *co = list.at(j);
                QByteArray objName = co->objectName().toAscii();
                int len = objName.length();
                if (!len || qstrncmp(slot + 3, objName.data(), len) || slot[len+3] != '_')
                    continue;
                int sigIndex = co->d_func()->signalIndex(slot + len + 4);
                if (sigIndex < 0) { // search for compatible signals
                    const QMetaObject *smo = co->metaObject();
                    int slotlen = qstrlen(slot + len + 4) - 1;
                    for (int k = 0; k < co->metaObject()->methodCount(); ++k) {
                        QMetaMethod method = smo->method(k);
                        if (method.methodType() != QMetaMethod::Signal)
                            continue;

                        if (!qstrncmp(method.signature(), slot + len + 4, slotlen)) {
                            int signalOffset, methodOffset;
                            computeOffsets(method.enclosingMetaObject(), &signalOffset, &methodOffset);
                            sigIndex = k + - methodOffset + signalOffset;
                            break;
                        }
                    }
                }
                if (sigIndex < 0)
                    continue;
                if (QMetaObjectPrivate::connect(co, sigIndex, o, i)) {
                    foundIt = true;
                    break;
                }
            }
            if (foundIt) {
                // we found our slot, now skip all overloads
                while (mo->method(i + 1).attributes() & QMetaMethod::Cloned)
                      ++i;
            } else if (!(mo->method(i).attributes() & QMetaMethod::Cloned)) {
                qWarning("QMetaObject::connectSlotsByName: No matching signal for %s", slot);
            }
        }
     }

    void QMetaObject::activate(QObject *sender, int from_signal_index, int to_signal_index, void **argv)
     {
        Q_UNUSED(to_signal_index);
        activate(sender, from_signal_index, argv);
     }

    void QMetaObject::activate(QObject *sender, const QMetaObject *m, int local_signal_index,
                               void **argv)
     {
        int signalOffset;
        int methodOffset;
        computeOffsets(m, &signalOffset, &methodOffset);

        int signal_index = signalOffset + local_signal_index;

        if (!sender->d_func()->isSignalConnected(signal_index))
            return; // nothing connected to these signals, and no spy

        if (sender->d_func()->blockSig)
            return;

        int signal_absolute_index = methodOffset + local_signal_index;

        void *empty_argv[] = { 0 };
        if (qt_signal_spy_callback_set.signal_begin_callback != 0) {
            qt_signal_spy_callback_set.signal_begin_callback(sender, signal_absolute_index,
                                                             argv ? argv : empty_argv);
        }

        Qt::HANDLE currentThreadId = QThread::currentThreadId();

        QMutexLocker locker(signalSlotLock(sender));
        QObjectConnectionListVector *connectionLists = sender->d_func()->connectionLists;
        if (!connectionLists) {
            locker.unlock();
            if (qt_signal_spy_callback_set.signal_end_callback != 0)
                qt_signal_spy_callback_set.signal_end_callback(sender, signal_absolute_index);
            return;
        }
        ++connectionLists->inUse;


        const QObjectPrivate::ConnectionList *list;
        if (signal_index < connectionLists->count())
            list = &connectionLists->at(signal_index);
        else
            list = &connectionLists->allsignals;

        do {
            QObjectPrivate::Connection *c = list->first;
            if (!c) continue;
            // We need to check against last here to ensure that signals added
            // during the signal emission are not emitted in this emission.
            QObjectPrivate::Connection *last = list->last;

            do {
                if (!c->receiver)
                    continue;

                QObject * const receiver = c->receiver;
                const bool receiverInSameThread = currentThreadId == receiver->d_func()->threadData->threadId;

                // determine if this connection should be sent immediately or
                // put into the event queue
                if ((c->connectionType == Qt::AutoConnection && !receiverInSameThread)
                    || (c->connectionType == Qt::QueuedConnection)) {
                    queued_activate(sender, signal_absolute_index, c, argv ? argv : empty_argv);
                    continue;
    'ifndef QT_NO_THREAD
                } else if (c->connectionType == Qt::BlockingQueuedConnection) {
                    locker.unlock();
                    if (receiverInSameThread) {
                        qWarning("Qt: Dead lock detected while activating a BlockingQueuedConnection: "
                        "Sender is %s(%p), receiver is %s(%p)",
                        sender->metaObject()->className(), sender,
                        receiver->metaObject()->className(), receiver);
                    }
                    QSemaphore semaphore;
                    QCoreApplication::postEvent(receiver, new QMetaCallEvent(c->method_offset, c->method_relative,
                                                                             c->callFunction,
                                                                             sender, signal_absolute_index,
                                                                             0, 0,
                                                                             argv ? argv : empty_argv,
                                                                             &semaphore));
                    semaphore.acquire();
                    locker.relock();
                    continue;
    'endif
                }

                QObjectPrivate::Sender currentSender;
                QObjectPrivate::Sender *previousSender = 0;
                if (receiverInSameThread) {
                    currentSender.sender = sender;
                    currentSender.signal = signal_absolute_index;
                    currentSender.ref = 1;
                    previousSender = QObjectPrivate::setCurrentSender(receiver, &currentSender);
                }
                const QObjectPrivate::StaticMetaCallFunction callFunction = c->callFunction;
                const int method_relative = c->method_relative;
                if (callFunction && c->method_offset <= receiver->metaObject()->methodOffset()) {
                    //we compare the vtable to make sure we are not in the destructor of the object.
                    locker.unlock();
                    if (qt_signal_spy_callback_set.slot_begin_callback != 0)
                        qt_signal_spy_callback_set.slot_begin_callback(receiver, c->method(), argv ? argv : empty_argv);

    #if defined(QT_NO_EXCEPTIONS)
                    callFunction(receiver, QMetaObject::InvokeMetaMethod, method_relative, argv ? argv : empty_argv);
    'else
                    QT_TRY {
                        callFunction(receiver, QMetaObject::InvokeMetaMethod, method_relative, argv ? argv : empty_argv);
                    } QT_CATCH(...) {
                        locker.relock();
                        if (receiverInSameThread)
                            QObjectPrivate::resetCurrentSender(receiver, &currentSender, previousSender);

                        --connectionLists->inUse;
                        Q_ASSERT(connectionLists->inUse >= 0);
                        if (connectionLists->orphaned && !connectionLists->inUse)
                            delete connectionLists;
                        QT_RETHROW;
                    }
    'endif
                    if (qt_signal_spy_callback_set.slot_end_callback != 0)
                        qt_signal_spy_callback_set.slot_end_callback(receiver, c->method());
                    locker.relock();
                } else {
                    const int method = method_relative + c->method_offset;
                    locker.unlock();

                    if (qt_signal_spy_callback_set.slot_begin_callback != 0) {
                        qt_signal_spy_callback_set.slot_begin_callback(receiver,
                                                                    method,
                                                                    argv ? argv : empty_argv);
                    }

    #if defined(QT_NO_EXCEPTIONS)
                    metacall(receiver, QMetaObject::InvokeMetaMethod, method, argv ? argv : empty_argv);
    'else
                    QT_TRY {
                        metacall(receiver, QMetaObject::InvokeMetaMethod, method, argv ? argv : empty_argv);
                    } QT_CATCH(...) {
                        locker.relock();
                        if (receiverInSameThread)
                            QObjectPrivate::resetCurrentSender(receiver, &currentSender, previousSender);

                        --connectionLists->inUse;
                        Q_ASSERT(connectionLists->inUse >= 0);
                        if (connectionLists->orphaned && !connectionLists->inUse)
                            delete connectionLists;
                        QT_RETHROW;
                    }
    'endif

                    if (qt_signal_spy_callback_set.slot_end_callback != 0)
                        qt_signal_spy_callback_set.slot_end_callback(receiver, method);

                    locker.relock();
                }

                if (receiverInSameThread)
                    QObjectPrivate::resetCurrentSender(receiver, &currentSender, previousSender);

                if (connectionLists->orphaned)
                    break;
            } while (c != last && (c = c->nextConnectionList) != 0);

            if (connectionLists->orphaned)
                break;
        } while (list != &connectionLists->allsignals &&
            //start over for all signals;
            ((list = &connectionLists->allsignals), true));

        --connectionLists->inUse;
        Q_ASSERT(connectionLists->inUse >= 0);
        if (connectionLists->orphaned) {
            if (!connectionLists->inUse)
                delete connectionLists;
        } else if (connectionLists->dirty) {
            sender->d_func()->cleanConnectionLists();
        }

        locker.unlock();

        if (qt_signal_spy_callback_set.signal_end_callback != 0)
            qt_signal_spy_callback_set.signal_end_callback(sender, signal_absolute_index);
     }

    void QMetaObject::activate(QObject *sender, int signal_index, void **argv)
     {
        const QMetaObject *mo = sender->metaObject();
        while (mo->methodOffset() > signal_index)
            mo = mo->superClass();
        activate(sender, mo, signal_index - mo->methodOffset(), argv);
     }

    void QMetaObject::activate(QObject *sender, const QMetaObject *m,
                               int from_local_signal_index, int to_local_signal_index, void **argv)
     {
        Q_UNUSED(to_local_signal_index);
        Q_ASSERT(from_local_signal_index == QMetaObjectPrivate::originalClone(m, to_local_signal_index));
        activate(sender, m, from_local_signal_index, argv);
     }
     
=============================================================================================================

QMetaObjectPrivate类的函数实现
    bool QMetaObjectPrivate::connect(const QObject *sender, int signal_index,
                                     const QObject *receiver, int method_index,
                                     const QMetaObject *rmeta, #receiver的QMetaObject
                                     int type, int *types)
     {
        QObject *s = const_cast<QObject *>(sender);
        QObject *r = const_cast<QObject *>(receiver);

        int method_offset = rmeta ? rmeta->methodOffset() : 0;
        
        typedef void (*StaticMetaCallFunction)(QObject *, QMetaObject::Call, int, void **);
        QObjectPrivate::StaticMetaCallFunction callFunction =
            (rmeta && QMetaObjectPrivate::get(rmeta)->revision >= 6 && rmeta->d.extradata)
            ? reinterpret_cast<const QMetaObjectExtraData *>(rmeta->d.extradata)->static_metacall : 0;

        QOrderedMutexLocker locker(signalSlotLock(sender),
                                   signalSlotLock(receiver));

        if (type & Qt::UniqueConnection) {
            QObjectConnectionListVector *connectionLists = QObjectPrivate::get(s)->connectionLists;
            if (connectionLists && connectionLists->count() > signal_index) {
                const QObjectPrivate::Connection *c2 =
                    (*connectionLists)[signal_index].first;

                int method_index_absolute = method_index + method_offset;

                while (c2) {
                    if (c2->receiver == receiver && c2->method() == method_index_absolute)
                        return false;
                    c2 = c2->nextConnectionList;
                }
            }
            type &= Qt::UniqueConnection - 1;
        }

        QObjectPrivate::Connection *c = new QObjectPrivate::Connection;
        c->sender = s;
        c->receiver = r;
        c->method_relative = method_index;
        c->method_offset = method_offset;
        c->connectionType = type;
        c->argumentTypes = types;
        c->nextConnectionList = 0;
        c->callFunction = callFunction;

        QT_TRY {
            QObjectPrivate::get(s)->addConnection(signal_index, c);
        } QT_CATCH(...) {
            delete c;
            QT_RETHROW;
        }

        c->prev = &(QObjectPrivate::get(r)->senders);
        c->next = *c->prev;
        *c->prev = c;
        if (c->next)
            c->next->prev = &c->next;

        QObjectPrivate *const sender_d = QObjectPrivate::get(s);
        if (signal_index < 0) {
            sender_d->connectedSignals[0] = sender_d->connectedSignals[1] = ~0;
        } else if (signal_index < (int)sizeof(sender_d->connectedSignals) * 8) {
            sender_d->connectedSignals[signal_index >> 5] |= (1 << (signal_index & 0x1f));
        }

        return true;
     }

=============================================================================================================

QObject类的函数实现

    bool QObject::connect(const QObject *sender, const char *signal,
                          const QObject *receiver, const char *method,
                          Qt::ConnectionType type)
     {
        {
            const void *cbdata[] = { sender, signal, receiver, method, &type };
            if (QInternal::activateCallbacks(QInternal::ConnectCallback, (void **) cbdata))
                return true;
        }

        'ifndef QT_NO_DEBUG
        bool warnCompat = true;
        'endif
        if (type == Qt::AutoCompatConnection) {
            type = Qt::AutoConnection;
        'ifndef QT_NO_DEBUG
            warnCompat = false;
        'endif
        }

        if (sender == 0 || receiver == 0 || signal == 0 || method == 0) {
            qWarning("QObject::connect: Cannot connect %s::%s to %s::%s",
                     sender ? sender->metaObject()->className() : "(null)",
                     (signal && *signal) ? signal+1 : "(null)",
                     receiver ? receiver->metaObject()->className() : "(null)",
                     (method && *method) ? method+1 : "(null)");
            return false;
        }
        QByteArray tmp_signal_name;

        if (!check_signal_macro(sender, signal, "connect", "bind"))
            return false;
        const QMetaObject *smeta = sender->metaObject();
        const char *signal_arg = signal;
        ++signal; //skip code
        int signal_index = QMetaObjectPrivate::indexOfSignalRelative(&smeta, signal, false);
        if (signal_index < 0) {
            // check for normalized signatures
            tmp_signal_name = QMetaObject::normalizedSignature(signal - 1);
            signal = tmp_signal_name.constData() + 1;

            smeta = sender->metaObject();
            signal_index = QMetaObjectPrivate::indexOfSignalRelative(&smeta, signal, false);
        }
        if (signal_index < 0) {
            // re-use tmp_signal_name and signal from above

            smeta = sender->metaObject();
            signal_index = QMetaObjectPrivate::indexOfSignalRelative(&smeta, signal, true);
        }
        if (signal_index < 0) {
            err_method_notfound(sender, signal_arg, "connect");
            err_info_about_objects("connect", sender, receiver);
            return false;
        }
        signal_index = QMetaObjectPrivate::originalClone(smeta, signal_index);
        int signalOffset, methodOffset;
        computeOffsets(smeta, &signalOffset, &methodOffset);
        int signal_absolute_index = signal_index + methodOffset;
        signal_index += signalOffset;

        QByteArray tmp_method_name;
        int membcode = extract_code(method);

        if (!check_method_code(membcode, receiver, method, "connect"))
            return false;
        const char *method_arg = method;
        ++method; // skip code

        const QMetaObject *rmeta = receiver->metaObject();
        int method_index_relative = -1;
        switch (membcode) {
        case QSLOT_CODE:
            method_index_relative = QMetaObjectPrivate::indexOfSlotRelative(&rmeta, method, false);
            break;
        case QSIGNAL_CODE:
            method_index_relative = QMetaObjectPrivate::indexOfSignalRelative(&rmeta, method, false);
            break;
        }

        if (method_index_relative < 0) {
            // check for normalized methods
            tmp_method_name = QMetaObject::normalizedSignature(method);
            method = tmp_method_name.constData();

            // rmeta may have been modified above
            rmeta = receiver->metaObject();
            switch (membcode) {
            case QSLOT_CODE:
                method_index_relative = QMetaObjectPrivate::indexOfSlotRelative(&rmeta, method, false);
                if (method_index_relative < 0)
                    method_index_relative = QMetaObjectPrivate::indexOfSlotRelative(&rmeta, method, true);
                break;
            case QSIGNAL_CODE:
                method_index_relative = QMetaObjectPrivate::indexOfSignalRelative(&rmeta, method, false);
                if (method_index_relative < 0)
                    method_index_relative = QMetaObjectPrivate::indexOfSignalRelative(&rmeta, method, true);
                break;
            }
        }

        if (method_index_relative < 0) {
            err_method_notfound(receiver, method_arg, "connect");
            err_info_about_objects("connect", sender, receiver);
            return false;
        }

        if (!QMetaObject::checkConnectArgs(signal, method)) {
            qWarning("QObject::connect: Incompatible sender/receiver arguments"
                     "\n        %s::%s --> %s::%s",
                     sender->metaObject()->className(), signal,
                     receiver->metaObject()->className(), method);
            return false;
        }

        int *types = 0;
        if ((type == Qt::QueuedConnection)
                && !(types = queuedConnectionTypes(smeta->method(signal_absolute_index).parameterTypes())))
            return false;

        'ifndef QT_NO_DEBUG
        if (warnCompat) {
            QMetaMethod smethod = smeta->method(signal_absolute_index);
            QMetaMethod rmethod = rmeta->method(method_index_relative + rmeta->methodOffset());
            check_and_warn_compat(smeta, smethod, rmeta, rmethod);
        }
        'endif
        if (!QMetaObjectPrivate::connect(sender, signal_index, receiver, method_index_relative, rmeta ,type, types))
            return false;
        const_cast<QObject*>(sender)->connectNotify(signal - 1);
        return true;
     }

    bool QObject::connect(const QObject *sender, const QMetaMethod &signal,
                          const QObject *receiver, const QMetaMethod &method,
                          Qt::ConnectionType type)
     {
        'ifndef QT_NO_DEBUG
        bool warnCompat = true;
        'endif
        if (type == Qt::AutoCompatConnection) {
            type = Qt::AutoConnection;
        'ifndef QT_NO_DEBUG
            warnCompat = false;
        'endif
        }

        if (sender == 0
                || receiver == 0
                || signal.methodType() != QMetaMethod::Signal
                || method.methodType() == QMetaMethod::Constructor) {
            qWarning("QObject::connect: Cannot connect %s::%s to %s::%s",
                     sender ? sender->metaObject()->className() : "(null)",
                     signal.signature(),
                     receiver ? receiver->metaObject()->className() : "(null)",
                     method.signature() );
            return false;
        }

        QVarLengthArray<char> signalSignature;
        QObjectPrivate::signalSignature(signal, &signalSignature);

        {
            QByteArray methodSignature;
            methodSignature.reserve(qstrlen(method.signature())+1);
            methodSignature.append((char)(method.methodType() == QMetaMethod::Slot ? QSLOT_CODE
                                        : method.methodType() == QMetaMethod::Signal ? QSIGNAL_CODE : 0  + '0'));
            methodSignature.append(method.signature());
            const void *cbdata[] = { sender, signalSignature.constData(), receiver, methodSignature.constData(), &type };
            if (QInternal::activateCallbacks(QInternal::ConnectCallback, (void **) cbdata))
                return true;
        }


        int signal_index;
        int method_index;
        {
            int dummy;
            QMetaObjectPrivate::memberIndexes(sender, signal, &signal_index, &dummy);
            QMetaObjectPrivate::memberIndexes(receiver, method, &dummy, &method_index);
        }

        const QMetaObject *smeta = sender->metaObject();
        const QMetaObject *rmeta = receiver->metaObject();
        if (signal_index == -1) {
            qWarning("QObject::connect: Can't find signal %s on instance of class %s",
                     signal.signature(), smeta->className());
            return false;
        }
        if (method_index == -1) {
            qWarning("QObject::connect: Can't find method %s on instance of class %s",
                     method.signature(), rmeta->className());
            return false;
        }
        
        if (!QMetaObject::checkConnectArgs(signal.signature(), method.signature())) {
            qWarning("QObject::connect: Incompatible sender/receiver arguments"
                     "\n        %s::%s --> %s::%s",
                     smeta->className(), signal.signature(),
                     rmeta->className(), method.signature());
            return false;
        }

        int *types = 0;
        if ((type == Qt::QueuedConnection)
                && !(types = queuedConnectionTypes(signal.parameterTypes())))
            return false;

    'ifndef QT_NO_DEBUG
        if (warnCompat)
            check_and_warn_compat(smeta, signal, rmeta, method);
    'endif
        if (!QMetaObjectPrivate::connect(sender, signal_index, receiver, method_index, 0, type, types))
            return false;

        const_cast<QObject*>(sender)->connectNotify(signalSignature.constData());
        return true;
     }

    bool QObject::disconnect(const QObject *sender, const char *signal,
                             const QObject *receiver, const char *method)
     {
        if (sender == 0 || (receiver == 0 && method != 0)) {
            qWarning("Object::disconnect: Unexpected null parameter");
            return false;
        }

        {
            const void *cbdata[] = { sender, signal, receiver, method };
            if (QInternal::activateCallbacks(QInternal::DisconnectCallback, (void **) cbdata))
                return true;
        }

        const char *signal_arg = signal;
        QByteArray signal_name;
        bool signal_found = false;
        if (signal) {
            QT_TRY {
                signal_name = QMetaObject::normalizedSignature(signal);
                signal = signal_name.constData();
            } QT_CATCH (const std::bad_alloc &) {
                // if the signal is already normalized, we can continue.
                if (sender->metaObject()->indexOfSignal(signal + 1) == -1)
                    QT_RETHROW;
            }

            if (!check_signal_macro(sender, signal, "disconnect", "unbind"))
                return false;
            signal++; // skip code
        }

        QByteArray method_name;
        const char *method_arg = method;
        int membcode = -1;
        bool method_found = false;
        if (method) {
            QT_TRY {
                method_name = QMetaObject::normalizedSignature(method);
                method = method_name.constData();
            } QT_CATCH(const std::bad_alloc &) {
                // if the method is already normalized, we can continue.
                if (receiver->metaObject()->indexOfMethod(method + 1) == -1)
                    QT_RETHROW;
            }

            membcode = extract_code(method);
            if (!check_method_code(membcode, receiver, method, "disconnect"))
                return false;
            method++; // skip code
        }

        /* We now iterate through all the sender's and receiver's meta
         * objects in order to also disconnect possibly shadowed signals
         * and slots with the same signature.
        */
        bool res = false;
        const QMetaObject *smeta = sender->metaObject();
        do {
            int signal_index = -1;
            if (signal) {
                signal_index = QMetaObjectPrivate::indexOfSignalRelative(&smeta, signal, false);
                if (signal_index < 0)
                    signal_index = QMetaObjectPrivate::indexOfSignalRelative(&smeta, signal, true);
                if (signal_index < 0)
                    break;
                signal_index = QMetaObjectPrivate::originalClone(smeta, signal_index);
                int signalOffset, methodOffset;
                computeOffsets(smeta, &signalOffset, &methodOffset);
                signal_index += signalOffset;
                signal_found = true;
            }

            if (!method) {
                res |= QMetaObjectPrivate::disconnect(sender, signal_index, receiver, -1);
            } else {
                const QMetaObject *rmeta = receiver->metaObject();
                do {
                    int method_index = rmeta->indexOfMethod(method);
                    if (method_index >= 0)
                        while (method_index < rmeta->methodOffset())
                                rmeta = rmeta->superClass();
                    if (method_index < 0)
                        break;
                    res |= QMetaObjectPrivate::disconnect(sender, signal_index, receiver, method_index);
                    method_found = true;
                } while ((rmeta = rmeta->superClass()));
            }
        } while (signal && (smeta = smeta->superClass()));

        if (signal && !signal_found) {
            err_method_notfound(sender, signal_arg, "disconnect");
            err_info_about_objects("disconnect", sender, receiver);
        } else if (method && !method_found) {
            err_method_notfound(receiver, method_arg, "disconnect");
            err_info_about_objects("disconnect", sender, receiver);
        }
        if (res)
            const_cast<QObject*>(sender)->disconnectNotify(signal ? (signal - 1) : 0);
        return res;
     }

    bool QObject::disconnect(const QObject *sender, const QMetaMethod &signal,
                             const QObject *receiver, const QMetaMethod &method)
     {
        if (sender == 0 || (receiver == 0 && method.mobj != 0)) {
            qWarning("Object::disconnect: Unexpected null parameter");
            return false;
        }
        if (signal.mobj) {
            if(signal.methodType() != QMetaMethod::Signal) {
                qWarning("Object::%s: Attempt to %s non-signal %s::%s",
                         "disconnect","unbind",
                         sender->metaObject()->className(), signal.signature());
                return false;
            }
        }
        if (method.mobj) {
            if(method.methodType() == QMetaMethod::Constructor) {
                qWarning("QObject::disconect: cannot use constructor as argument %s::%s",
                         receiver->metaObject()->className(), method.signature());
                return false;
            }
        }

        QVarLengthArray<char> signalSignature;
        if (signal.mobj)
            QObjectPrivate::signalSignature(signal, &signalSignature);

        {
            QByteArray methodSignature;
            if (method.mobj) {
                methodSignature.reserve(qstrlen(method.signature())+1);
                methodSignature.append((char)(method.methodType() == QMetaMethod::Slot ? QSLOT_CODE
                                            : method.methodType() == QMetaMethod::Signal ? QSIGNAL_CODE : 0  + '0'));
                methodSignature.append(method.signature());
            }
            const void *cbdata[] = { sender, signal.mobj ? signalSignature.constData() : 0,
                                     receiver, method.mobj ? methodSignature.constData() : 0 };
            if (QInternal::activateCallbacks(QInternal::DisconnectCallback, (void **) cbdata))
                return true;
        }

        int signal_index;
        int method_index;
        {
            int dummy;
            QMetaObjectPrivate::memberIndexes(sender, signal, &signal_index, &dummy);
            QMetaObjectPrivate::memberIndexes(receiver, method, &dummy, &method_index);
        }
        // If we are here sender is not null. If signal is not null while signal_index
        // is -1 then this signal is not a member of sender.
        if (signal.mobj && signal_index == -1) {
            qWarning("QObject::disconect: signal %s not found on class %s",
                     signal.signature(), sender->metaObject()->className());
            return false;
        }
        // If this condition is true then method is not a member of receeiver.
        if (receiver && method.mobj && method_index == -1) {
            qWarning("QObject::disconect: method %s not found on class %s",
                     method.signature(), receiver->metaObject()->className());
            return false;
        }

        if (!QMetaObjectPrivate::disconnect(sender, signal_index, receiver, method_index))
            return false;

        const_cast<QObject*>(sender)->disconnectNotify(method.mobj ? signalSignature.constData() : 0);
        return true;
     }

=============================================================================================================     



=============================================================================================================



=============================================================================================================



=============================================================================================================



=============================================================================================================



=============================================================================================================



=============================================================================================================



=============================================================================================================
