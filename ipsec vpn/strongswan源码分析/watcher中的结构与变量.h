/**
 * What events to watch for a file descriptor.
 */
enum watcher_event_t {
	WATCHER_READ = (1<<0),
	WATCHER_WRITE = (1<<1),
	WATCHER_EXCEPT = (1<<2),
};
/**
 * State the watcher currently is in
 */
enum watcher_state_t {
	/** no watcher thread running or queued */
	WATCHER_STOPPED = 0,
	/** a job has been queued for watching, but not yet started */
	WATCHER_QUEUED,
	/** a watcher thread is active, dispatching socket events */
	WATCHER_RUNNING,
};
/**
 * Watch multiple file descriptors using select().
 * 使用select，监视多个文件描述符
 */
struct watcher_t {
	/**
	 * Start watching a new file descriptor.
	 * 内部将参数组织成entry结构，添加到FDs中
	 * Multiple callbacks can be registered for the same file descriptor, and
	 * all of them get notified. Such callbacks are executed concurrently.
	 *
	 * @param fd		file descriptor to start watching
	 * @param events	ORed set of events to watch
	 * @param cb		callback function to invoke on events
	 * @param data		data to pass to cb()
	 */
	void (*add)(watcher_t *this, int fd, watcher_event_t events,
				watcher_cb_t cb, void *data);
	/**
	 * Stop watching a previously registered file descriptor.
	 *
	 * This call blocks until any active callback for this FD returns. All
	 * callbacks registered for that FD get unregistered.
	 *
	 * @param fd		file descriptor to stop watching
	 */
	void (*remove)(watcher_t *this, int fd);
	/**
	 * Get the current watcher state
	 *
	 * @return			currently active watcher state
	 */
	watcher_state_t (*get_state)(watcher_t *this);
	/**
	 * Destroy a watcher_t.
	 */
	void (*destroy)(watcher_t *this);
};
========================================================
/**
 * Private data of an watcher_t object.
 * 监视多组文件句柄，socket也是文件句柄
 */
struct private_watcher_t {
	// Public watcher_t interface. 
	watcher_t public;
	// List of registered FDs 
	entry_t *fds;
	// Last registered FD 
	entry_t *last;
	// Number of registered FDs 
	u_int count;
	// Pending update of FD list? 
	bool pending;
	// Running state of watcher ，枚举类型
	watcher_state_t state;
	// Lock to access FD list 
	mutex_t *mutex;
	// Condvar to signal completion of callback 
	condvar_t *condvar;
	// Notification pipe to signal watcher thread
    // 一对管道文件描述符 
	int notify[2];
	// List of callback jobs to process by watcher thread, as job_t 
	linked_list_t *jobs;
};
/**
 * Entry for a registered file descriptor
 */
struct entry_t {
	/** file descriptor */
	int fd;                     //要监视的文件描述符
	/** events to watch */
	watcher_event_t events;     //要监视的事件，枚举类型
	/** registered callback function */
	watcher_cb_t cb;            //事件发生后要调用的函数
	/** user data to pass to callback */
	void *data;                 //传给回调函数的参数
	/** callback(s) currently active? */
	int in_callback;            //在执行回调前设置
	/** next registered fd */
	entry_t *next;              //链表下一个，
};
/**
 * Data we pass on for an async notification
 */
typedef struct {
	/** file descriptor */
	int fd;
	/** event type */
	watcher_event_t event;
	/** registered callback function */
	watcher_cb_t cb;
	/** user data to pass to callback */
	void *data;
	/** keep registered? */0
	bool keep;
	/** reference to watcher */
	private_watcher_t *this;
} notify_data_t;