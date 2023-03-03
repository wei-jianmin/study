class QObject
 {
    Q_OBJECT
    Q_PROPERTY(QString objectName READ objectName WRITE setObjectName)  #Q_PROPERTY需要用moc进行编译
    Q_DECLARE_PRIVATE(QObject)  #声明实现了返回QObjectPrivate*的d_func函数，返回的就是QObjectData* d_ptr成员变量
  public:
    Q_INVOKABLE explicit QObject(QObject *parent=0);
    virtual ~QObject();

   '属性方法
    QString objectName() const;
    void setObjectName(const QString &name);
   
   '事件/事件过滤器
    virtual bool event(QEvent *);
    virtual bool eventFilter(QObject *, QEvent *);

   '字符串转换
    'ifdef qdoc
    static QString tr(const char *sourceText, const char *comment = 0, int n = -1);
    static QString trUtf8(const char *sourceText, const char *comment = 0, int n = -1);
   
   '获取元对象
    virtual const QMetaObject *metaObject() const;
    static const QMetaObject staticMetaObject;
    'endif
   
   '字符串转换
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

   '线程 
    QThread *thread() const;
    void moveToThread(QThread *thread);
   
   '定时器
    int startTimer(int interval);
    void killTimer(int id);

   '子对象 内联函数
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

   '设置父对象
    void setParent(QObject *);
    
   '事件过滤器
    void installEventFilter(QObject *);
    void removeEventFilter(QObject *);

   '信号连接与断开
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

   '输出对象信息
    void dumpObjectTree();
    void dumpObjectInfo();

   '属性 
    'ifndef QT_NO_PROPERTIES
    bool setProperty(const char *name, const QVariant &value);
    QVariant property(const char *name) const;
    QList<QByteArray> dynamicPropertyNames() const;
    'endif // QT_NO_PROPERTIES

   '用户数据
    'ifndef QT_NO_USERDATA
    static uint registerUserData();
    void setUserData(uint id, QObjectUserData* data);
    QObjectUserData* userData(uint id) const;
    'endif // QT_NO_USERDATA

  Q_SIGNALS:
    void destroyed(QObject * = 0);
    
  public Q_SLOTS:
    void deleteLater();
    
  public:
    inline QObject *parent() const { return d_ptr->parent; }

    inline bool inherits(const char *classname) const
        { return const_cast<QObject *>(this)->qt_metacast(classname) != 0; }

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
    QScopedPointer<QObjectData> d_ptr;  #一旦出了作用域，就自动释放的智能指针

    static const QMetaObject staticQtMetaObject;
   
   '声明友元类
    friend struct QMetaObject;
    friend class QApplication;
    friend class QApplicationPrivate;
    friend class QCoreApplication;
    friend class QCoreApplicationPrivate;
    friend class QWidget;
    friend class QThreadData;

  private:
    Q_DISABLE_COPY(QObject)     #禁用拷贝构造函数和=赋值函数
    Q_PRIVATE_SLOT(d_func(), void _q_reregisterTimers(void *))  #一个方法是私有的，但又想将其变为公有的槽函数，则使用该宏
 };
  
class QObjectData 
 {
  public:
    virtual ~QObjectData() = 0;
    QObject *q_ptr;         
    QObject *parent;
    QObjectList children;

    uint isWidget : 1;
    uint blockSig : 1;
    uint wasDeleted : 1;
    uint isDeletingChildren : 1;
    uint sendChildEvents : 1;
    uint receiveChildEvents : 1;
    uint isWindow : 1; //for QWindow
    uint unused : 25;
    int postedEvents;
    QDynamicMetaObjectData *metaObject;
    QMetaObject *dynamicMetaObject() const;
 };

相关宏定义
    'define Q_DECLARE_PRIVATE(Class) 
        inline Class##Private* d_func() { return reinterpret_cast<Class##Private *>(qGetPtrHelper(d_ptr)); } 
        inline const Class##Private* d_func() const { return reinterpret_cast<const Class##Private *>(qGetPtrHelper(d_ptr)); } 
        friend class Class##Private;
    'define signals Q_SIGNALS    
    'define slots   Q_SLOTS
    'define Q_SIGNALS public QT_ANNOTATE_ACCESS_SPECIFIER(qt_signal)
    'define Q_SLOTS          QT_ANNOTATE_ACCESS_SPECIFIER(qt_slot)
    'define QT_ANNOTATE_ACCESS_SPECIFIER(x)
    'define Q_DISABLE_COPY(Class) Class(const Class &) Q_DECL_EQ_DELETE; Class &operator=(const Class &) Q_DECL_EQ_DELETE;
    'define Q_DECL_EQ_DELETE = delete
    'define Q_PRIVATE_SLOT(d, signature) QT_ANNOTATE_CLASS2(qt_private_slot, d, signature)
    'define QT_ANNOTATE_CLASS2(type, a1, a2)
    'define Q_D(Class) Class##Private * const d = d_func()
    
QObject函数实现
    QObject::QObject(QObject *parent) : d_ptr(new QObjectPrivate)
     {
        Q_D(QObject);
        d_ptr->q_ptr = this;
        d->threadData = (parent && !parent->thread()) ? parent->d_func()->threadData : QThreadData::current();
        d->threadData->ref();
        if (parent) {
            QT_TRY {
                if (!check_parent_thread(parent, parent ? parent->d_func()->threadData : 0, d->threadData))
                    parent = 0;
                setParent(parent);
            } QT_CATCH(...) {
                d->threadData->deref();
                QT_RETHROW;
            }
        }
        qt_addObject(this);
     }

    QString QObject::objectName() const
     {
        Q_D(const QObject);
        return d->objectName;
     }   
    
    void QObject::setObjectName(const QString &name)
     {
        Q_D(QObject);
        bool objectNameChanged = d->declarativeData && d->objectName != name;

        d->objectName = name;

        if (objectNameChanged) 
            d->declarativeData->objectNameChanged(d->declarativeData, this);
     }
    
    bool QObject::event(QEvent *e)
     {
        switch (e->type()) {
        case QEvent::Timer:
            timerEvent((QTimerEvent*)e);
            break;

    #ifdef QT3_SUPPORT
        case QEvent::ChildInsertedRequest:
            d_func()->sendPendingChildInsertedEvents();
            break;
    #endif

        case QEvent::ChildAdded:
        case QEvent::ChildPolished:
    #ifdef QT3_SUPPORT
        case QEvent::ChildInserted:
    #endif
        case QEvent::ChildRemoved:
            childEvent((QChildEvent*)e);
            break;

        case QEvent::DeferredDelete:
            qDeleteInEventHandler(this);
            break;

        case QEvent::MetaCall:
            {
    #ifdef QT_JAMBI_BUILD
                d_func()->inEventHandler = false;
    #endif
                QMetaCallEvent *mce = static_cast<QMetaCallEvent*>(e);
                QObjectPrivate::Sender currentSender;
                currentSender.sender = const_cast<QObject*>(mce->sender());
                currentSender.signal = mce->signalId();
                currentSender.ref = 1;
                QObjectPrivate::Sender * const previousSender =
                    QObjectPrivate::setCurrentSender(this, &currentSender);
    #if defined(QT_NO_EXCEPTIONS)
                mce->placeMetaCall(this);
    #else
                QT_TRY {
                    mce->placeMetaCall(this);
                } QT_CATCH(...) {
                    QObjectPrivate::resetCurrentSender(this, &currentSender, previousSender);
                    QT_RETHROW;
                }
    #endif
                QObjectPrivate::resetCurrentSender(this, &currentSender, previousSender);
                break;
            }

        case QEvent::ThreadChange: {
            Q_D(QObject);
            QThreadData *threadData = d->threadData;
            QAbstractEventDispatcher *eventDispatcher = threadData->eventDispatcher;
            if (eventDispatcher) {
                QList<QPair<int, int> > timers = eventDispatcher->registeredTimers(this);
                if (!timers.isEmpty()) {
                    // set inThreadChangeEvent to true to tell the dispatcher not to release out timer ids
                    // back to the pool (since the timer ids are moving to a new thread).
                    d->inThreadChangeEvent = true;
                    eventDispatcher->unregisterTimers(this);
                    d->inThreadChangeEvent = false;
                    QMetaObject::invokeMethod(this, "_q_reregisterTimers", Qt::QueuedConnection,
                                              Q_ARG(void*, (new QList<QPair<int, int> >(timers))));
                }
            }
            break;
        }

        default:
            if (e->type() >= QEvent::User) {
                customEvent(e);
                break;
            }
            return false;
        }
        return true;
     }
    
    bool QObject::eventFilter(QObject * /* watched */, QEvent * /* event */)
     {
        return false;
     }

    #该函数存在于moc_qobject.cpp文件中
    const QMetaObject *QObject::metaObject() const
     {
        return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
     }
    
    QThread *QObject::thread() const
     {
        return d_func()->threadData->thread;
     }

    void QObject::moveToThread(QThread *targetThread)
     {
        Q_D(QObject);

        if (d->threadData->thread == targetThread) {
            // object is already in this thread
            return;
        }

        if (d->parent != 0) {
            qWarning("QObject::moveToThread: Cannot move objects with a parent");
            return;
        }
        if (d->isWidget) {
            qWarning("QObject::moveToThread: Widgets cannot be moved to a new thread");
            return;
        }

        QThreadData *currentData = QThreadData::current();
        QThreadData *targetData = targetThread ? QThreadData::get2(targetThread) : new QThreadData(0);
        if (d->threadData->thread == 0 && currentData == targetData) {
            // one exception to the rule: we allow moving objects with no thread affinity to the current thread
            currentData = d->threadData;
        } else if (d->threadData != currentData) {
            qWarning("QObject::moveToThread: Current thread (%p) is not the object's thread (%p).\n"
                     "Cannot move to target thread (%p)\n",
                     currentData->thread, d->threadData->thread, targetData->thread);

    #ifdef Q_WS_MAC
            qWarning("On Mac OS X, you might be loading two sets of Qt binaries into the same process. "
                     "Check that all plugins are compiled against the right Qt binaries. Export "
                     "DYLD_PRINT_LIBRARIES=1 and check that only one set of binaries are being loaded.");
    #endif

            return;
        }

        // prepare to move
        d->moveToThread_helper();

        QOrderedMutexLocker locker(&currentData->postEventList.mutex,
                                   &targetData->postEventList.mutex);

        // keep currentData alive (since we've got it locked)
        currentData->ref();

        // move the object
        d_func()->setThreadData_helper(currentData, targetData);

        locker.unlock();

        // now currentData can commit suicide if it wants to
        currentData->deref();
     }
    
    int QObject::startTimer(int interval)
     {
        Q_D(QObject);

        if (interval < 0) {
            qWarning("QObject::startTimer: QTimer cannot have a negative interval");
            return 0;
        }

        d->pendTimer = true;                                // set timer flag

        if (!d->threadData->eventDispatcher) {
            qWarning("QObject::startTimer: QTimer can only be used with threads started with QThread");
            return 0;
        }
        return d->threadData->eventDispatcher->registerTimer(interval, this);
     }

    void QObject::killTimer(int id)
     {
        Q_D(QObject);
        if (d->threadData->eventDispatcher)
            d->threadData->eventDispatcher->unregisterTimer(id);
     }
     
    void QObject::setParent(QObject *parent)
     {
        Q_D(QObject);
        Q_ASSERT(!d->isWidget);
        d->setParent_helper(parent);
     }
    
    void QObject::installEventFilter(QObject *obj)
     {
        Q_D(QObject);
        if (!obj)
            return;
        if (d->threadData != obj->d_func()->threadData) {
            qWarning("QObject::installEventFilter(): Cannot filter events for objects in a different thread.");
            return;
        }

        // clean up unused items in the list
        d->eventFilters.removeAll((QObject*)0);
        d->eventFilters.removeAll(obj);
        d->eventFilters.prepend(obj);
     }

    void QObject::removeEventFilter(QObject *obj)
     {
        Q_D(QObject);
        for (int i = 0; i < d->eventFilters.count(); ++i) {
            if (d->eventFilters.at(i) == obj)
                d->eventFilters[i] = 0;
        }
     }
    
    bool QObject::connect(const QObject *sender, const char *signal,
                      const QObject *receiver, const char *method,
                      Qt::ConnectionType type)
     {
        {
            const void *cbdata[] = { sender, signal, receiver, method, &type };
            if (QInternal::activateCallbacks(QInternal::ConnectCallback, (void **) cbdata))
                return true;
        }

    #ifndef QT_NO_DEBUG
        bool warnCompat = true;
    #endif
        if (type == Qt::AutoCompatConnection) {
            type = Qt::AutoConnection;
    #ifndef QT_NO_DEBUG
            warnCompat = false;
    #endif
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

    #ifndef QT_NO_DEBUG
        if (warnCompat) {
            QMetaMethod smethod = smeta->method(signal_absolute_index);
            QMetaMethod rmethod = rmeta->method(method_index_relative + rmeta->methodOffset());
            check_and_warn_compat(smeta, smethod, rmeta, rmethod);
        }
    #endif
        if (!QMetaObjectPrivate::connect(sender, signal_index, receiver, method_index_relative, rmeta ,type, types))
            return false;
        const_cast<QObject*>(sender)->connectNotify(signal - 1);
        return true;
     }

    bool QObject::connect(const QObject *sender, const QMetaMethod &signal,
                          const QObject *receiver, const QMetaMethod &method,
                          Qt::ConnectionType type)
     {
    #ifndef QT_NO_DEBUG
        bool warnCompat = true;
    #endif
        if (type == Qt::AutoCompatConnection) {
            type = Qt::AutoConnection;
    #ifndef QT_NO_DEBUG
            warnCompat = false;
    #endif
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

    #ifndef QT_NO_DEBUG
        if (warnCompat)
            check_and_warn_compat(smeta, signal, rmeta, method);
    #endif
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

    void QObject::dumpObjectTree()
     {
        dumpRecursive(0, this);
     }
    
    static void dumpRecursive(int level, QObject *object)
     {
    #if defined(QT_DEBUG)
        if (object) {
            QByteArray buf;
            buf.fill(' ', level / 2 * 8);
            if (level % 2)
                buf += "    ";
            QString name = object->objectName();
            QString flags = QLatin1String("");
    #if 0
            if (qApp->focusWidget() == object)
                flags += 'F';
            if (object->isWidgetType()) {
                QWidget * w = (QWidget *)object;
                if (w->isVisible()) {
                    QString t("<%1,%2,%3,%4>");
                    flags += t.arg(w->x()).arg(w->y()).arg(w->width()).arg(w->height());
                } else {
                    flags += 'I';
                }
            }
    #endif
            qDebug("%s%s::%s %s", (const char*)buf, object->metaObject()->className(), name.toLocal8Bit().data(),
                   flags.toLatin1().data());
            QObjectList children = object->children();
            if (!children.isEmpty()) {
                for (int i = 0; i < children.size(); ++i)
                    dumpRecursive(level+1, children.at(i));
            }
        }
    #else
        Q_UNUSED(level)
            Q_UNUSED(object)
    #endif
     }
    
    void QObject::dumpObjectInfo()
     {
    #if defined(QT_DEBUG)
        qDebug("OBJECT %s::%s", metaObject()->className(),
               objectName().isEmpty() ? "unnamed" : objectName().toLocal8Bit().data());

        Q_D(QObject);
        QMutexLocker locker(signalSlotLock(this));

        // first, look for connections where this object is the sender
        qDebug("  SIGNALS OUT");

        if (d->connectionLists) {
            int offset = 0;
            int offsetToNextMetaObject = 0;
            for (int signal_index = 0; signal_index < d->connectionLists->count(); ++signal_index) {
                if (signal_index >= offsetToNextMetaObject) {
                    const QMetaObject *mo = metaObject();
                    int signalOffset, methodOffset;
                    computeOffsets(mo, &signalOffset, &methodOffset);
                    while (signalOffset > signal_index) {
                        mo = mo->superClass();
                        offsetToNextMetaObject = signalOffset;
                        computeOffsets(mo, &signalOffset, &methodOffset);
                    }
                    offset = methodOffset - signalOffset;
                }
                const QMetaMethod signal = metaObject()->method(signal_index + offset);
                qDebug("        signal: %s", signal.signature());

                // receivers
                const QObjectPrivate::Connection *c =
                    d->connectionLists->at(signal_index).first;
                while (c) {
                    if (!c->receiver) {
                        qDebug("          <Disconnected receiver>");
                        c = c->nextConnectionList;
                        continue;
                    }
                    const QMetaObject *receiverMetaObject = c->receiver->metaObject();
                    const QMetaMethod method = receiverMetaObject->method(c->method());
                    qDebug("          --> %s::%s %s",
                           receiverMetaObject->className(),
                           c->receiver->objectName().isEmpty() ? "unnamed" : qPrintable(c->receiver->objectName()),
                           method.signature());
                    c = c->nextConnectionList;
                }
            }
        } else {
            qDebug( "        <None>" );
        }

        // now look for connections where this object is the receiver
        qDebug("  SIGNALS IN");

        if (d->senders) {
            for (QObjectPrivate::Connection *s = d->senders; s; s = s->next) {
                const QMetaMethod slot = metaObject()->method(s->method());
                qDebug("          <-- %s::%s  %s",
                       s->sender->metaObject()->className(),
                       s->sender->objectName().isEmpty() ? "unnamed" : qPrintable(s->sender->objectName()),
                       slot.signature());
            }
        } else {
            qDebug("        <None>");
        }
    #endif
     }
    
    bool QObject::setProperty(const char *name, const QVariant &value)
     {
        Q_D(QObject);
        const QMetaObject* meta = metaObject();
        if (!name || !meta)
            return false;

        int id = meta->indexOfProperty(name);
        if (id < 0) {
            if (!d->extraData)
                d->extraData = new QObjectPrivate::ExtraData;

            const int idx = d->extraData->propertyNames.indexOf(name);

            if (!value.isValid()) {
                if (idx == -1)
                    return false;
                d->extraData->propertyNames.removeAt(idx);
                d->extraData->propertyValues.removeAt(idx);
            } else {
                if (idx == -1) {
                    d->extraData->propertyNames.append(name);
                    d->extraData->propertyValues.append(value);
                } else {
                    d->extraData->propertyValues[idx] = value;
                }
            }

            QDynamicPropertyChangeEvent ev(name);
            QCoreApplication::sendEvent(this, &ev);

            return false;
        }
        QMetaProperty p = meta->property(id);
    #ifndef QT_NO_DEBUG
        if (!p.isWritable())
            qWarning("%s::setProperty: Property \"%s\" invalid,"
                     " read-only or does not exist", metaObject()->className(), name);
    #endif
        return p.write(this, value);
     }
    
    QVariant QObject::property(const char *name) const
     {
        Q_D(const QObject);
        const QMetaObject* meta = metaObject();
        if (!name || !meta)
            return QVariant();

        int id = meta->indexOfProperty(name);
        if (id < 0) {
            if (!d->extraData)
                return QVariant();
            const int i = d->extraData->propertyNames.indexOf(name);
            return d->extraData->propertyValues.value(i);
        }
        QMetaProperty p = meta->property(id);
    #ifndef QT_NO_DEBUG
        if (!p.isReadable())
            qWarning("%s::property: Property \"%s\" invalid or does not exist",
                     metaObject()->className(), name);
    #endif
        return p.read(this);
     }
    
    QList<QByteArray> QObject::dynamicPropertyNames() const
     {
        Q_D(const QObject);
        if (d->extraData)
            return d->extraData->propertyNames;
        return QList<QByteArray>();
     }
    
    uint QObject::registerUserData()
     {
        static int user_data_registration = 0;
        return user_data_registration++;
     }
    
    void QObject::setUserData(uint id, QObjectUserData* data)
     {
        Q_D(QObject);
        if (!d->extraData)
            d->extraData = new QObjectPrivate::ExtraData;

        if (d->extraData->userData.size() <= (int) id)
            d->extraData->userData.resize((int) id + 1);
        d->extraData->userData[id] = data;
     }

    QObjectUserData* QObject::userData(uint id) const
     {
        Q_D(const QObject);
        if (!d->extraData)
            return 0;
        if ((int)id < d->extraData->userData.size())
            return d->extraData->userData.at(id);
        return 0;
     }
    
    QObject *QObject::sender() const
     {
        Q_D(const QObject);

        QMutexLocker locker(signalSlotLock(this));
        if (!d->currentSender)
            return 0;

        for (QObjectPrivate::Connection *c = d->senders; c; c = c->next) {
            if (c->sender == d->currentSender->sender)
                return d->currentSender->sender;
        }

        return 0;
     }
    
    int QObject::senderSignalIndex() const
     {
        Q_D(const QObject);

        QMutexLocker locker(signalSlotLock(this));
        if (!d->currentSender)
            return -1;

        for (QObjectPrivate::Connection *c = d->senders; c; c = c->next) {
            if (c->sender == d->currentSender->sender)
                return d->currentSender->signal;
        }

        return -1;
     }
    
    int QObject::receivers(const char *signal) const
     {
        Q_D(const QObject);
        int receivers = 0;
        if (signal) {
            QByteArray signal_name = QMetaObject::normalizedSignature(signal);
            signal = signal_name;
    #ifndef QT_NO_DEBUG
            if (!check_signal_macro(this, signal, "receivers", "bind"))
                return 0;
    #endif
            signal++; // skip code
            int signal_index = d->signalIndex(signal);
            if (signal_index < 0) {
    #ifndef QT_NO_DEBUG
                err_method_notfound(this, signal-1, "receivers");
    #endif
                return false;
            }

            Q_D(const QObject);
            QMutexLocker locker(signalSlotLock(this));
            if (d->connectionLists) {
                if (signal_index < d->connectionLists->count()) {
                    const QObjectPrivate::Connection *c =
                        d->connectionLists->at(signal_index).first;
                    while (c) {
                        receivers += c->receiver ? 1 : 0;
                        c = c->nextConnectionList;
                    }
                }
            }
        }
        return receivers;
     }
    
    void QObject::timerEvent(QTimerEvent *)
     {
     }
    
    void QObject::childEvent(QChildEvent * /* event */)
     {
     }
    
    void QObject::customEvent(QEvent * /* event */)
     {
     }
    
    void QObject::connectNotify(const char *)
     {
     }

    void QObject::disconnectNotify(const char *)
     {
     }
    
    static int methodIndexToSignalIndex(const QMetaObject *metaObject, int signal_index)
     {
        if (signal_index < 0)
            return signal_index;
        while (metaObject && metaObject->methodOffset() > signal_index)
            metaObject = metaObject->superClass();

        if (metaObject) {
            int signalOffset, methodOffset;
            computeOffsets(metaObject, &signalOffset, &methodOffset);
            if (signal_index < metaObject->methodCount())
                signal_index = QMetaObjectPrivate::originalClone(metaObject, signal_index - methodOffset) + signalOffset;
            else
                signal_index = signal_index - methodOffset + signalOffset;
        }
        return signal_index;
     }