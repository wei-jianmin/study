继承关系：
    QAppliction继承自QGuiApplication,
    QGuiApplication继承自QCoreApplication
    QCoreApplication通常继承自QObject
    如果定义了QT_NO_QOBJECT宏，则没有父类
    
class Q_CORE_EXPORT QCoreApplication : public QObject
{
    Q_OBJECT        //支持元对象功能
    Q_PROPERTY(QString applicationName READ applicationName WRITE setApplicationName NOTIFY applicationNameChanged)
    Q_PROPERTY(QString applicationVersion READ applicationVersion WRITE setApplicationVersion NOTIFY applicationVersionChanged)
    Q_PROPERTY(QString organizationName READ organizationName WRITE setOrganizationName NOTIFY organizationNameChanged)
    Q_PROPERTY(QString organizationDomain READ organizationDomain WRITE setOrganizationDomain NOTIFY organizationDomainChanged)
    Q_PROPERTY(bool quitLockEnabled READ isQuitLockEnabled WRITE setQuitLockEnabled)

    Q_DECLARE_PRIVATE(QCoreApplication)     //定义获取QCoreApplicationPrivate*的函数
  public:
    enum { ApplicationFlags = QT_VERSION };
    QCoreApplication(int &argc, char **argv, int = ApplicationFlags);
    ~QCoreApplication();
    void installNativeEventFilter(QAbstractNativeEventFilter *filterObj);
    void removeNativeEventFilter(QAbstractNativeEventFilter *filterObj);
    virtual bool notify(QObject *, QEvent *);
   静态方法
    static QStringList arguments();

    static void setAttribute(Qt::ApplicationAttribute attribute, bool on = true);
    static bool testAttribute(Qt::ApplicationAttribute attribute);

    static void setOrganizationDomain(const QString &orgDomain);
    static QString organizationDomain();
    static void setOrganizationName(const QString &orgName);
    static QString organizationName();
    static void setApplicationName(const QString &application);
    static QString applicationName();
    static void setApplicationVersion(const QString &version);
    static QString applicationVersion();

    static void setSetuidAllowed(bool allow);
    static bool isSetuidAllowed();

    static QCoreApplication *instance() { return self; }

    static int exec();
    static void processEvents(QEventLoop::ProcessEventsFlags flags = QEventLoop::AllEvents);
    static void processEvents(QEventLoop::ProcessEventsFlags flags, int maxtime);
    static void exit(int retcode=0);

    static bool sendEvent(QObject *receiver, QEvent *event);
    static void postEvent(QObject *receiver, QEvent *event, int priority = Qt::NormalEventPriority);
    static void sendPostedEvents(QObject *receiver = Q_NULLPTR, int event_type = 0);
    static void removePostedEvents(QObject *receiver, int eventType = 0);
    #if QT_DEPRECATED_SINCE(5, 3)
    QT_DEPRECATED static bool hasPendingEvents();
    #endif
    static QAbstractEventDispatcher *eventDispatcher();
    static void setEventDispatcher(QAbstractEventDispatcher *eventDispatcher);

    static bool startingUp();
    static bool closingDown();

    static QString applicationDirPath();
    static QString applicationFilePath();
    static qint64 applicationPid();

    #if QT_CONFIG(library)
    static void setLibraryPaths(const QStringList &);
    static QStringList libraryPaths();
    static void addLibraryPath(const QString &);
    static void removeLibraryPath(const QString &);
    #endif // QT_CONFIG(library)

    static bool installTranslator(QTranslator * messageFile);
    static bool removeTranslator(QTranslator * messageFile);

    static QString translate(const char * context,
                             const char * key,
                             const char * disambiguation = Q_NULLPTR,
                             int n = -1);
    #if QT_DEPRECATED_SINCE(5, 0)
    enum Encoding { UnicodeUTF8, Latin1, DefaultCodec = UnicodeUTF8, CodecForTr = UnicodeUTF8 };
    QT_DEPRECATED static inline QString translate(const char * context, const char * key,
                                                  const char * disambiguation, Encoding, int n = -1)
                                                 { return translate(context, key, disambiguation, n); }
    #endif

    #  if QT_DEPRECATED_SINCE(5, 9)
    QT_DEPRECATED static void flush();
    #  endif
  
    static bool isQuitLockEnabled();
    static void setQuitLockEnabled(bool enabled);
    
  public Q_SLOTS:
    static void quit();

  Q_SIGNALS:
    void aboutToQuit(QPrivateSignal);

    void organizationNameChanged();
    void organizationDomainChanged();
    void applicationNameChanged();
    void applicationVersionChanged();

  protected:
    bool event(QEvent *) Q_DECL_OVERRIDE;

    virtual bool compressEvent(QEvent *, QObject *receiver, QPostEventList *);

  protected:
    QCoreApplication(QCoreApplicationPrivate &p);

    QScopedPointer<QCoreApplicationPrivate> d_ptr;

  private:
    static bool sendSpontaneousEvent(QObject *receiver, QEvent *event);
    #  if QT_DEPRECATED_SINCE(5,6)
    QT_DEPRECATED bool notifyInternal(QObject *receiver, QEvent *event); // ### Qt6 BIC: remove me
    #  endif
    static bool notifyInternal2(QObject *receiver, QEvent *);

    static QCoreApplication *self;

    Q_DISABLE_COPY(QCoreApplication)

    friend class QApplication;
    friend class QApplicationPrivate;
    friend class QGuiApplication;
    friend class QGuiApplicationPrivate;
    friend class QWidget;
    friend class QWidgetWindow;
    friend class QWidgetPrivate;
    friend class QEventDispatcherUNIXPrivate;
    friend class QCocoaEventDispatcherPrivate;
    friend bool qt_sendSpontaneousEvent(QObject*, QEvent*);
    friend Q_CORE_EXPORT QString qAppName();
    friend class QClassFactory;
};

class Q_CORE_EXPORT QCoreApplicationPrivate : public QObjectPrivate
{
    Q_DECLARE_PUBLIC(QCoreApplication)

  public:
    enum Type {Tty,Gui};

    QCoreApplicationPrivate(int &aargc,  char **aargv, uint flags);
    ~QCoreApplicationPrivate();

    void init();

    QString appName() const;
    QString appVersion() const;

    #ifdef Q_OS_DARWIN
    static QString infoDictionaryStringProperty(const QString &propertyName);
    #endif

    static void initLocale();

    static bool checkInstance(const char *method);

    bool sendThroughApplicationEventFilters(QObject *, QEvent *);
    static bool sendThroughObjectEventFilters(QObject *, QEvent *);
    static bool notify_helper(QObject *, QEvent *);
    static inline void setEventSpontaneous(QEvent *e, bool spontaneous) { e->spont = spontaneous; }

    virtual void createEventDispatcher();
    virtual void eventDispatcherReady();
    static void removePostedEvent(QEvent *);
    #ifdef Q_OS_WIN
    static void removePostedTimerEvent(QObject *object, int timerId);
    #endif

    QAtomicInt quitLockRef;
    void ref();
    void deref();
    virtual bool shouldQuit() {
      return true;
    }
    void maybeQuit();

    static QBasicAtomicPointer<QThread> theMainThread;
    static QThread *mainThread();
    static bool threadRequiresCoreApplication();

    static void sendPostedEvents(QObject *receiver, int event_type, QThreadData *data);

    static void checkReceiverThread(QObject *receiver);
    void cleanupThreadData();

    int &argc;
    char **argv;
    #if defined(Q_OS_WIN) && !defined(Q_OS_WINRT)
    int origArgc;
    char **origArgv; // store unmodified arguments for QCoreApplication::arguments()
    #endif
    void appendApplicationPathToLibraryPaths(void);

    #ifndef QT_NO_TRANSLATION
    QTranslatorList translators;

    static bool isTranslatorInstalled(QTranslator *translator);
    #endif

    QCoreApplicationPrivate::Type application_type;

    QString cachedApplicationDirPath;
    static QString *cachedApplicationFilePath;
    static void setApplicationFilePath(const QString &path);
    static inline void clearApplicationFilePath() { delete cachedApplicationFilePath; cachedApplicationFilePath = 0; }

    void execCleanup();

    bool in_exec;
    bool aboutToQuitEmitted;
    bool threadData_clean;

    static QAbstractEventDispatcher *eventDispatcher;
    static bool is_app_running;
    static bool is_app_closing;

    static bool setuidAllowed;
    static uint attribs;
    static inline bool testAttribute(uint flag) { return attribs & (1 << flag); }
    static int app_compile_version;

    void processCommandLineArguments();
    QString qmljs_debug_arguments; // a string containing arguments for js/qml debugging.
    inline QString qmljsDebugArgumentsString() { return qmljs_debug_arguments; }

    QCoreApplication *q_ptr;
};


QCoreApplicationPrivate的构造函数（内部调用Init函数）大概主要完成如下工作：
    读配置文件
        获取QT_LOGGING_CONF环境变量（记录配置文件路径），如果存在，就读配置文件
        获取QT_LOGGING_RULES环境变量（记录配置项字符串），如果存在，就解析配置项
        读取当前路径下的qtlogging.ini文件，如果存在，就读该配置文件
        在用户system目录下QtProject文件夹下查找qtlogging.ini文件
        如果以上任何位置能读取到配置项，就更新这些配置项？
    记录命令行参数，解析命令行，看看是否有"-qmljsdebugger="参数
    包装调用了 setlocale(LC_ALL, "");
    使用createEventDispatcher函数创建“事件分发器”

QGuiApplicationPrivate的构造函数（内部调用Init函数）大概主要完成如下工作：
    调用QCoreApplicationPrivate::init()
    初始化调色板
    初始化字体
    注册GUI类型
    与ANIMATION及OPENGL相关的准备
    处理命令行参数（-plugin、-reverse、-session、-testability、-style=）
    设置布局顺序（从左到右/从右到左）
    关联QGuiApplication::applicationNameChanged信号
        到QGuiApplication::applicationDisplayNameChanged槽
 
QApplicationPrivate的构造函数（内部调用Init函数）大概主要完成如下工作：
    调用QGuiApplicationPrivate::init()
    初始化资源
        Q_INIT_RESOURCE(qstyle);
        Q_INIT_RESOURCE(qmessagebox);
        关于Q_INIT_RESOURCE
            Q_INIT_RESOURCE是Qt的资源机制（resource mechanism)，
            它使程序在编译时将图片存储在.cpp文件中，运行时连接它。
            这要求你建立一个Qt资源文件***.qrc，在***.qrc中指定图片位置。
            编译时编译器将***.qrc中指定的图片以二进制数的形式
            存储到Qt自动建立的名为qrc_***.cpp的文件中，
            这里的***就是你建立***.qrc时的名字，
            而你在main()函数中使用Q_INIT_RESOURCE(name)宏时的name也必须是这个**
    处理命令行参数
        -qdevel、-stylesheet、-widgetcount
    qt_init(必须在调用initialize前先调用该函数)
        初始化QColormap
        初始化工具提示面板(tooltip palette)
        设置控件字体
    initialize 
        注册Widgets变量
        创建程序样式
    。。。
        
 
exec函数（静态函数）
先做一些条件检查    
    包括QCoreApplication是不是已经存在实例
    QCoreApplication是不是和exec在同一线程中
    检查eventloop？
创建QEventLoop对象eventLoop
执行eventLoop.exec()

class Q_CORE_EXPORT QEventLoop : public QObject
{
    Q_OBJECT
    Q_DECLARE_PRIVATE(QEventLoop)

  public:
    explicit QEventLoop(QObject *parent = Q_NULLPTR);
    ~QEventLoop();

    enum ProcessEventsFlag {
        AllEvents = 0x00,
        ExcludeUserInputEvents = 0x01,
        ExcludeSocketNotifiers = 0x02,
        WaitForMoreEvents = 0x04,
        X11ExcludeTimers = 0x08,
        EventLoopExec = 0x20,
        DialogExec = 0x40
    };
    Q_DECLARE_FLAGS(ProcessEventsFlags, ProcessEventsFlag)

    bool processEvents(ProcessEventsFlags flags = AllEvents);
    void processEvents(ProcessEventsFlags flags, int maximumTime);

    int exec(ProcessEventsFlags flags = AllEvents);
    void exit(int returnCode = 0);
    bool isRunning() const;

    void wakeUp();

    bool event(QEvent *event) Q_DECL_OVERRIDE;

  public Q_SLOTS:
    void quit();
};

int QEventLoop::exec(ProcessEventsFlags flags)
{
    Q_D(QEventLoop);
    //we need to protect from race condition with QThread::exit
    QMutexLocker locker(&static_cast<QThreadPrivate *>(QObjectPrivate::get(d->threadData->thread))->mutex);
    if (d->threadData->quitNow)
        return -1;

    if (d->inExec) {
        qWarning("QEventLoop::exec: instance %p has already called exec()", this);
        return -1;
    }

    struct LoopReference {
        QEventLoopPrivate *d;
        QMutexLocker &locker;

        bool exceptionCaught;
        LoopReference(QEventLoopPrivate *d, QMutexLocker &locker) : d(d), locker(locker), exceptionCaught(true)
        {
            d->inExec = true;
            d->exit.storeRelease(false);
            ++d->threadData->loopLevel;
            d->threadData->eventLoops.push(d->q_func());
            locker.unlock();
        }

        ~LoopReference()
        {
            if (exceptionCaught) {
                qWarning("Qt has caught an exception thrown from an event handler. Throwing\n"
                         "exceptions from an event handler is not supported in Qt.\n"
                         "You must not let any exception whatsoever propagate through Qt code.\n"
                         "If that is not possible, in Qt 5 you must at least reimplement\n"
                         "QCoreApplication::notify() and catch all exceptions there.\n");
            }
            locker.relock();
            QEventLoop *eventLoop = d->threadData->eventLoops.pop();
            Q_ASSERT_X(eventLoop == d->q_func(), "QEventLoop::exec()", "internal error");
            Q_UNUSED(eventLoop); // --release warning
            d->inExec = false;
            --d->threadData->loopLevel;
        }
    };
    LoopReference ref(d, locker);

    // remove posted quit events when entering a new event loop
    QCoreApplication *app = QCoreApplication::instance();
    if (app && app->thread() == thread())
        QCoreApplication::removePostedEvents(app, QEvent::Quit);

    while (!d->exit.loadAcquire())
        processEvents(flags | WaitForMoreEvents | EventLoopExec);       
    /* processEvents完成的功能：
       创建内部窗口，窗口句柄在QEventDispatcherWin32Private（windows平台）中记录
       
       从消息队列中提取消息，派发消息
       

    ref.exceptionCaught = false;
    return d->returnCode.load();
}



Q_GLOBAL_STATIC(QWindowsMessageWindowClassContext, qWindowsMessageWindowClassContext)

    namespace { 
      namespace Q_QGS_qWindowsMessageWindowClassContext {                                                     
        QBasicAtomicInt guard = Q_BASIC_ATOMIC_INITIALIZER(QtGlobalStatic::Uninitialized); 
        Q_GLOBAL_STATIC_INTERNAL_DECORATION QWindowsMessageWindowClassContext *innerFunction()   \
        {                                                           \
            struct HolderBase {                                     \
                ~HolderBase() Q_DECL_NOTHROW                        \
                { if (guard.load() == QtGlobalStatic::Initialized)  \
                      guard.store(QtGlobalStatic::Destroyed); }     \
            };                                                      \
            static struct Holder : public HolderBase {              \
                QWindowsMessageWindowClassContext value;                                         \
                Holder()                                            \
                    Q_DECL_NOEXCEPT_EXPR(noexcept(QWindowsMessageWindowClassContext ARGS))       \
                    : value ARGS                                    \
                { guard.store(QtGlobalStatic::Initialized); }       \
            } holder;                                               \
            return &holder.value;                                   \
        }                                     
      } 
    }                                                                     
    static QGlobalStatic<QWindowsMessageWindowClassContext,                                              
                         Q_QGS_qWindowsMessageWindowClassContext::innerFunction,                     
                         Q_QGS_qWindowsMessageWindowClassContext::guard> qWindowsMessageWindowClassContext;

template <typename T, T *(&innerFunction)(), QBasicAtomicInt &guard>
struct QGlobalStatic
{
    typedef T Type;

    bool isDestroyed() const { return guard.load() <= QtGlobalStatic::Destroyed; }
    bool exists() const { return guard.load() == QtGlobalStatic::Initialized; }
    operator Type *() { if (isDestroyed()) return 0; return innerFunction(); }
    Type *operator()() { if (isDestroyed()) return 0; return innerFunction(); }
    Type *operator->()
    {
      Q_ASSERT_X(!isDestroyed(), "Q_GLOBAL_STATIC", "The global static was used after being destroyed");
      return innerFunction();
    }
    Type &operator*()
    {
      Q_ASSERT_X(!isDestroyed(), "Q_GLOBAL_STATIC", "The global static was used after being destroyed");
      return *innerFunction();
    }
};
