QObject
    Q_DECLARE_PRIVATE(QObject)  实现了返回QObjectPrivate*的d_func函数
        QObjectPrivate* d_func()
            return reinterpret_cast<QObjectPrivate *>(qGetPtrHelper(d_ptr));
                template <typename T> static inline T *qGetPtrHelper(T *ptr) 
                    return ptr; 
                d_ptr可以是一个智能指针,qGetPtrHelper的作用是触发智能指针的隐式强制转换(当作为参数传递给原始指针时)
        protected : QScopedPointer<QObjectData> d_ptr;
    数据成员：
        QScopedPointer<QObjectData> d_ptr;
        static const QMetaObject staticQtMetaObject;
        
QObjectData 和 QObjectPrivate
    QString objectName;
    QObjectPrivate继承并扩展了QObjectData
    QObjectData中
        记录的父对象指针，孩子列表等，为实现父子对象，提供了数据支撑，
        还记录了是否是widget、是否接收子对象的事件消息、是否处于信号阻塞等功能
    QObjectPrivate中
        记录线程数据 QThreadData *threadData 如：拥有该对象的线程id等
        记录额外数据 ExtraData   *extraData  
            QVector<QObjectUserData *> userData;    用户数据
            QList<QByteArray> propertyNames;        属性名
            QVector<QVariant> propertyValues;       属性值
            QString objectName;                     对象名
            QVector<int> runningTimers;             运行时长
            QList<QPointer<QObject> > eventFilters; 事件过滤
        记录连接(connection)列表  QVector<QObjectPrivate::ConnectionList> *connectionLists;
            struct ConnectionList
                Connection *first;
                Connection *last;
            struct Connection
                QObject *sender;    发送对象的指针
                uint signal_index
                QObject *receiver;   接受对象的指针
                ushort method_offset;    
                ushort method_relative; 
                union
                    StaticMetaCallFunction callFunction;         接受对象的qt_static_metacall函数的指针
                    QtPrivate::QSlotObjectBase *slotObj;
                QAtomicPointer<const int> argumentTypes;     参数值数组指针
                ushort connectionType；
                ushort isSlotObject;
                Connection *next;
                Connection **prev;
                ...
                
Q_D(Class)原理
    QObject中有个成员QScopedPointer<QObjectData> d_ptr;
    所以QObject的子类均可使用该成员变量，
    获取并使用该成员变量有个简单的方法，使用Q_D(Class)宏 ： 
    'Q_D(Class) Class##Private * const d = d_func()
    'd_func()返回的就是d_ptr的值
    以QThread为例，该类直接继承自QObject
    QThread的构造函数为：
        QThread::QThread(QObject *parent) : QObject(*(new QThreadPrivate), parent)
            Q_D(QThread);
            d->data->thread = this;
    QObject的构造函数为：
        QObject::QObject(QObjectPrivate &dd, QObject *parent) : d_ptr(&dd)
            Q_D(QObject);
            d_ptr->q_ptr = this;
            d->threadData = (parent && !parent->thread()) ? parent->d_func()->threadData : QThreadData::current();
            d->threadData->ref();
            if (parent) 
                if (!check_parent_thread(parent, parent ? parent->d_func()->threadData : 0, d->threadData))
                    parent = 0;
                if (d->isWidget) 
                    if (parent)
                        d->parent = parent;
                        d->parent->d_func()->children.append(this);
                else 
                    setParent(parent);
            qt_addObject(this);
    通过这两个类的构造函数可以看出，
    QThread类在构造时，创建了QThreadPrivate对象，并将其地址赋值给d_ptr;
    QThreadPrivate继承自QObjectPrivate，继承自QObjectData；
    扩展：
        上面函数中QThreadData::current()的作用就是创建一个QThreadData对象，
        并记录线程id=CurrentThreadId()，线程运行状态为true，线程结束状态为false;
        check_parent_thread函数的作用确保第一个参数不为空，且第二个参数!=第三个参数，否则将当前对象的parrent设为0
        从QObject的构造函数还可以看出，如果是widget类对象，且指定了父对象，则会将该widget对象添加到其父对象的孩子列表中
        setParren函数
            适用于非widget类对象，但其内部也是将该对象添加到父对象的孩子列表中，
            setParrent函数还会检查父对象是不是和当前对象在一个线程中，
            如果当前类之前有个旧的父对象，还会将该类从旧父对象的孩子列表中删除
            还会向父对象发出“添加孩子事件” 
                QChildEvent e(QEvent::ChildAdded, q);
                QCoreApplication::sendEvent(parent, &e);
        在QObject的析构函数中，会删除孩子列表中记录的对象
