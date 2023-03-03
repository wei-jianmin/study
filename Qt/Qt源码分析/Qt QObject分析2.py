QObject
    Q_DECLARE_PRIVATE(QObject)  ʵ���˷���QObjectPrivate*��d_func����
        QObjectPrivate* d_func()
            return reinterpret_cast<QObjectPrivate *>(qGetPtrHelper(d_ptr));
                template <typename T> static inline T *qGetPtrHelper(T *ptr) 
                    return ptr; 
                d_ptr������һ������ָ��,qGetPtrHelper�������Ǵ�������ָ�����ʽǿ��ת��(����Ϊ�������ݸ�ԭʼָ��ʱ)
        protected : QScopedPointer<QObjectData> d_ptr;
    ���ݳ�Ա��
        QScopedPointer<QObjectData> d_ptr;
        static const QMetaObject staticQtMetaObject;
        
QObjectData �� QObjectPrivate
    QString objectName;
    QObjectPrivate�̳в���չ��QObjectData
    QObjectData��
        ��¼�ĸ�����ָ�룬�����б�ȣ�Ϊʵ�ָ��Ӷ����ṩ������֧�ţ�
        ����¼���Ƿ���widget���Ƿ�����Ӷ�����¼���Ϣ���Ƿ����ź������ȹ���
    QObjectPrivate��
        ��¼�߳����� QThreadData *threadData �磺ӵ�иö�����߳�id��
        ��¼�������� ExtraData   *extraData  
            QVector<QObjectUserData *> userData;    �û�����
            QList<QByteArray> propertyNames;        ������
            QVector<QVariant> propertyValues;       ����ֵ
            QString objectName;                     ������
            QVector<int> runningTimers;             ����ʱ��
            QList<QPointer<QObject> > eventFilters; �¼�����
        ��¼����(connection)�б�  QVector<QObjectPrivate::ConnectionList> *connectionLists;
            struct ConnectionList
                Connection *first;
                Connection *last;
            struct Connection
                QObject *sender;    ���Ͷ����ָ��
                uint signal_index
                QObject *receiver;   ���ܶ����ָ��
                ushort method_offset;    
                ushort method_relative; 
                union
                    StaticMetaCallFunction callFunction;         ���ܶ����qt_static_metacall������ָ��
                    QtPrivate::QSlotObjectBase *slotObj;
                QAtomicPointer<const int> argumentTypes;     ����ֵ����ָ��
                ushort connectionType��
                ushort isSlotObject;
                Connection *next;
                Connection **prev;
                ...
                
Q_D(Class)ԭ��
    QObject���и���ԱQScopedPointer<QObjectData> d_ptr;
    ����QObject���������ʹ�øó�Ա������
    ��ȡ��ʹ�øó�Ա�����и��򵥵ķ�����ʹ��Q_D(Class)�� �� 
    'Q_D(Class) Class##Private * const d = d_func()
    'd_func()���صľ���d_ptr��ֵ
    ��QThreadΪ��������ֱ�Ӽ̳���QObject
    QThread�Ĺ��캯��Ϊ��
        QThread::QThread(QObject *parent) : QObject(*(new QThreadPrivate), parent)
            Q_D(QThread);
            d->data->thread = this;
    QObject�Ĺ��캯��Ϊ��
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
    ͨ����������Ĺ��캯�����Կ�����
    QThread���ڹ���ʱ��������QThreadPrivate���󣬲������ַ��ֵ��d_ptr;
    QThreadPrivate�̳���QObjectPrivate���̳���QObjectData��
    ��չ��
        ���溯����QThreadData::current()�����þ��Ǵ���һ��QThreadData����
        ����¼�߳�id=CurrentThreadId()���߳�����״̬Ϊtrue���߳̽���״̬Ϊfalse;
        check_parent_thread����������ȷ����һ��������Ϊ�գ��ҵڶ�������!=���������������򽫵�ǰ�����parrent��Ϊ0
        ��QObject�Ĺ��캯�������Կ����������widget�������ָ���˸�������Ὣ��widget������ӵ��丸����ĺ����б���
        setParren����
            �����ڷ�widget����󣬵����ڲ�Ҳ�ǽ��ö�����ӵ�������ĺ����б��У�
            setParrent���������鸸�����ǲ��Ǻ͵�ǰ������һ���߳��У�
            �����ǰ��֮ǰ�и��ɵĸ����󣬻��Ὣ����Ӿɸ�����ĺ����б���ɾ��
            �����򸸶��󷢳�����Ӻ����¼��� 
                QChildEvent e(QEvent::ChildAdded, q);
                QCoreApplication::sendEvent(parent, &e);
        ��QObject�����������У���ɾ�������б��м�¼�Ķ���
