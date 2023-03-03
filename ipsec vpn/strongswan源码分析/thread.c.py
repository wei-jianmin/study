# Called by the main thread to initialize the thread management
threads_init
    private_thread_t *main_thread = thread_create_internal();
        private_thread_t *this;
        this 初始化
            this.public.cancel = _cancel
            this.public.kill = _kill_
            this.public.detach = _detach
            this.public.join = _join
            this.cleanup_handlers = linked_list_create()
            this.mutex = mutex_create(MUTEX_TYPE_DEFAULT)
        return this
    dummy1 = thread_value_create(NULL);
        file://thread_value.c.py
        
struct private_thread_t {
	// Public interface.
	thread_t public;  #  libstrongswan\threading\thread.h
	// Identificator of this thread (human-readable/thread ID).
	u_int id;
	// ID of the underlying thread.
	pthread_t thread_id;  #  typedef uintptr_t pthread_t
	// Main function of this thread (NULL for the main thread).
	thread_main_t main;  #  typedef void *(*thread_main_t)(void *arg);
	// Argument for the main function.
	void * arg;
	// Stack of cleanup handlers.
	linked_list_t * cleanup_handlers;
	// Mutex to make modifying thread properties safe.
	mutex_t * mutex;
	// TRUE if this thread has been detached or joined, 
    // i.e. can be cleaned up after terminating.
	bool detached_or_joined;
	// TRUE if the threads has terminated 
	// (cancelled, via thread_exit or returned from the main function)
	bool terminated;
};

# 一个假的thread
static thread_value_t *dummy1;

# 将线程对象存在一个特定的值（thread-specific value）中
static thread_value_t *current_thread;
        