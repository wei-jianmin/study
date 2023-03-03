qt version 5.9.0

QMetaObject和QMetaObjectPrivate
    QMtaObject 该类没有父类
        该类的数据成员是个结构体类对象d：
          struct {
            const QMetaObject *superdata;                       //指向父类
            const QByteArrayData *stringdata;                   //字符串字典
            const uint *data;                                   //实际被转换成QMetaObjectPrivate*使用
            'typedef void (*StaticMetacallFunction)(QObject *, QMetaObject::Call, int, void **);
            StaticMetacallFunction static_metacall;             //moc文件中qt_static_metacall函数的指针
            const QMetaObject * const *relatedMetaObjects;      //一般不用，赋值为0
            void *extradata;                                    //保留以后用
          } d;
        该类提供的功能包括但不限于：
            提供对成员的动态识别与调用
            向父类的类型转换(cast)
            编码转换(tr)
            信号槽连接(connect)
            信号激活(activate)
            动态创建对象(newInstance)
    QMetaObjectPrivate
        实现对QMetaObject中d.data数据(类的元数据)的解析，
        QMetaObject类中的一些关于方法调用的关键函数及信号槽连接函数等，
        如indexOfSignal、indexOfSlot、connect、disconnect，都是在该类中实现的
        
在一般类中，通过使用Q_OBJECT宏，使类包含QMetaObject成员对象
    Q_OBJECT宏的展开效果
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
    同时Q_OBJECT宏还会指示使用moc编译器，根据头文件，生成相应类的moc文件
    
调用QObject::connect方法时，
借助QMetaObject和QMetaObjectPrivate，
可以获得有关信号发送者、信号函数、信号接受者、槽函数的特定信息，
这些信息会被添加到发送者的"信号槽列表"中————参看QObjectPrivate
每个线程有个信号队列，在线程事件循环中，会检查信号队列，
如果队列中有信号，就找到信号相应的对象，
查找该对象“信号槽列表”，完成对相应槽的调用。
关于信号队列，实际应该是事件队列，
发出信号，其实是抛出QMetaCallEvent事件。

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
而线程的事件循环从该事件列表中取出事件对象，根据事件对象中记录的被调函数的信息
完成对槽函数的调用。
