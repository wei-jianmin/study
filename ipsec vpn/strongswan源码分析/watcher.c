参：file://watcher中的结构与变量.h
/**
 * Private data of an watcher_t object.
 */
struct private_watcher_t {

	/**
	 * Public watcher_t interface.
	 */
	watcher_t public;

	/**
	 * List of registered FDs
	 */
	entry_t *fds;

	/**
	 * Last registered FD
	 */
	entry_t *last;

	/**
	 * Number of registered FDs
	 */
	u_int count;

	/**
	 * Pending update of FD list?
	 */
	bool pending;

	/**
	 * Running state of watcher
	 */
	watcher_state_t state;

	/**
	 * Lock to access FD list
	 */
	mutex_t *mutex;

	/**
	 * Condvar to signal completion of callback
	 */
	condvar_t *condvar;

	/**
	 * Notification pipe to signal watcher thread
	 */
	int notify[2];

	/**
	 * List of callback jobs to process by watcher thread, as job_t
	 */
	linked_list_t *jobs;
};

/**
 * Entry for a registered file descriptor
 */
struct entry_t {
	/** file descriptor */
	int fd;
	/** events to watch */
	watcher_event_t events;
	/** registered callback function */
	watcher_cb_t cb;
	/** user data to pass to callback */
	void *data;
	/** callback(s) currently active? */
	int in_callback;
	/** next registered fd */
	entry_t *next;
};

===============================================

watcher_t *watcher_create()
{
	private_watcher_t *this;

	INIT(this,
		.public = {
			.add = _add,
			.remove = _remove_,
			.get_state = _get_state,
			.destroy = _destroy,
		},
		.mutex = mutex_create(MUTEX_TYPE_DEFAULT),
		.condvar = condvar_create(CONDVAR_TYPE_DEFAULT),
		.jobs = linked_list_create(),
		.notify = {-1, -1},
		.state = WATCHER_STOPPED,
	);

	if (!create_notify(this))
	{
		DBG1(DBG_LIB, "creating watcher notify pipe failed: %s",
			 strerror(errno));
	}
	return &this->public;
}

// Create a notify pipe with a one-directional pipe
static bool create_notify(private_watcher_t *this)
{
	int flags;

	if (pipe(this->notify) == 0)  //notify是一对管道文件描述符
	{
		/* use non-blocking I/O on read-end of notify pipe */
		flags = fcntl(this->notify[0], F_GETFL);  //getflag, 用于设置非阻塞读
		if (flags != -1 &&
			fcntl(this->notify[0], F_SETFL, flags | O_NONBLOCK) != -1)
		{
			return TRUE;
		}
		DBG1(DBG_LIB, "setting watcher notify pipe read-end non-blocking "
			 "failed: %s", strerror(errno));
	}
	return FALSE;
}

METHOD(watcher_t, add, void,
	private_watcher_t *this, int fd, watcher_event_t events,
	watcher_cb_t cb, void *data)
{
	entry_t *entry;

	INIT(entry,
		.fd = fd,
		.events = events,
		.cb = cb,
		.data = data,
	);

	this->mutex->lock(this->mutex);
	add_entry(this, entry);
	if (this->state == WATCHER_STOPPED)
	{
		this->state = WATCHER_QUEUED;
		lib->processor->queue_job(lib->processor,
			(job_t*)callback_job_create_with_prio((void*)watch, this,
				NULL, (callback_job_cancel_t)return_false, JOB_PRIO_CRITICAL));
	}
	else
	{
		update(this);
	}
	this->mutex->unlock(this->mutex);
}