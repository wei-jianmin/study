struct thread_t {

	/**
	 * Cancel this thread.
	 */
	void (*cancel)(thread_t *this);

	/**
	 * Send a signal to this thread.
	 *
	 * @param sig		the signal to be sent to this thread
	 */
	void (*kill)(thread_t *this, int sig);

	/**
	 * Detach this thread, this automatically destroys the thread object after
	 * the thread returned from its main function.
	 *
	 * @note Calling detach is like calling destroy on other objects.
	 */
	void (*detach)(thread_t *this);

	/**
	 * Join this thread, this automatically destroys the thread object
	 * afterwards.
	 *
	 * @note Calling join is like calling destroy on other objects.
	 *
	 * @return			the value returned from the thread's main function or
	 *					a call to exit.
	 */
	void *(*join)(thread_t *this);
};


=========================================================================================


/**
 * Next thread ID.
 */
static u_int next_id;

/**
 * Mutex to safely access the next thread ID.
 */
static mutex_t *id_mutex;

/**
 * Store the thread object in a thread-specific value.
 */
static thread_value_t *current_thread;

/**
 * A dummy thread value that reserved pthread_key_t value "0". A buggy PKCS#11
 * library mangles this key, without owning it, so we allocate it for them.
 * 一个有缺陷的 PKCS#11 库在没有拥有它的情况下破坏了这个key，所以我们为它们分配它
 */
static thread_value_t *dummy1;


struct private_thread_t {
	/**
	 * Public interface.
	 */
	thread_t public;

	/**
	 * Identificator of this thread (human-readable/thread ID).
	 */
	u_int id;

	/**
	 * ID of the underlying thread.
	 */
	pthread_t thread_id;

	/**
	 * Main function of this thread (NULL for the main thread).
	 */
	thread_main_t main;

	/**
	 * Argument for the main function.
	 */
	void *arg;

	/**
	 * Stack of cleanup handlers.
	 */
	linked_list_t *cleanup_handlers;

	/**
	 * Mutex to make modifying thread properties safe.
	 */
	mutex_t *mutex;

	/**
	 * TRUE if this thread has been detached or joined, i.e. can be cleaned
	 * up after terminating.
	 */
	bool detached_or_joined;

	/**
	 * TRUE if the threads has terminated (cancelled, via thread_exit or
	 * returned from the main function)
	 */
	bool terminated;

};