/**
 * The processor uses threads to process queued jobs.
 * 任务管理器，内部维护 threads
 */
struct processor_t {

	/**
	 * Get the total number of threads used by the processor.
	 *
	 * @return				size of thread pool
	 */
	u_int (*get_total_threads) (processor_t *this);  //获取总线程数

	/**
	 * Get the number of threads currently waiting for work.
	 *
	 * @return				number of idle threads
	 */
	u_int (*get_idle_threads) (processor_t *this);  //获取空闲线程数

	/**
	 * Get the number of threads currently working, per priority class.
	 *
	 * @param				priority to check
	 * @return				number of threads in priority working
	 */
	u_int (*get_working_threads)(processor_t *this, job_priority_t prio);  //获取（每一优先级下）正在工作的线程数

	/**
	 * Get the number of queued jobs for a specified priority.
	 *
	 * @param prio			priority class to get job load for
	 * @return				number of items in queue
	 */
	u_int (*get_job_load) (processor_t *this, job_priority_t prio);   //进程加载了多少个要执行的job

	/**
	 * Adds a job to the queue.
	 *
	 * This function is non blocking and adds a job_t to the queue.
	 *
	 * @param job			job to add to the queue
	 */
	void (*queue_job) (processor_t *this, job_t *job);   //往进程（的队列）中添加job （非阻塞的）

	/**
	 * Directly execute a job with an idle worker thread.
	 *
	 * If no idle thread is available, the job gets executed by the calling
	 * thread.
	 *
	 * @param job			job, gets destroyed
	 */
	void (*execute_job)(processor_t *this, job_t *job);   //让进程直接执行一个job（阻塞的）

	/**
	 * Set the number of threads to use in the processor.
	 *
	 * If the number of threads is smaller than number of currently running
	 * threads, thread count is decreased. Use 0 to disable the processor.
	 *
	 * This call does not block and wait for threads to terminate if the number
	 * of threads is reduced.  Instead use cancel() for that during shutdown.
	 *
	 * @param count			number of threads to allocate
	 */
	void (*set_threads)(processor_t *this, u_int count);  //设置进行中线程池的大小

	/**
	 * Sets the number of threads to 0 and cancels all blocking jobs, then waits
	 * for all threads to be terminated.
	 */
    //清空线程池（关闭所有线程），清空阻塞的job队列，等待所有（正在执行job的）线程结束
	void (*cancel)(processor_t *this);      

	/**
	 * Destroy a processor object.
	 */
	void (*destroy) (processor_t *processor);
};

====================================================

/**
 * Private data of processor_t class.
 */
struct private_processor_t {

	/**
	 * Public processor_t interface.
	 */
	processor_t public;

	/**
	 * 当前正在运行的线程数，包括空闲的
	 * 在 charon.c：main ： charon->start ：lib->processor->set_threads 时
	 * 会添加 desired_threads-total_threads 个worker，放到 threads 链表中
	 * 并令 total_threads = desired_threads
	 * total_threads 可以大于 desired_threads，但不会小于 desired_threads
	 */
	u_int total_threads;

	/**
	 * 总共需要的线程数
	 * Desired number of threads
	 */
	u_int desired_threads;

	/**
	 * 5个优先级分别各有多少非空闲线程
	 * Number of threads currently working, for each priority
	 */
	u_int working_threads[JOB_PRIO_MAX];  

	/**
	 * 5个优先级分别各保留/需要多少线程（包括工作线程和空闲线程） ？
	 * Threads reserved for each priority 
	 */
	int prio_threads[JOB_PRIO_MAX];

	/**
	 * access to job lists is locked through this mutex
	 */
	mutex_t *mutex;

	/**
	 * Condvar to wait for new jobs
	 */
	condvar_t *job_added;

	/**
	 * Condvar to wait for terminated threads
	 */
	condvar_t *thread_terminated;

	/**
	 * 每个优先级对应一个任务列表
	 * A list of queued jobs for each priority
	 */
	linked_list_t *jobs[JOB_PRIO_MAX];
	
	/**
	 * 在线程池中管理所有线程，worker_thread_t的链表
	 * All threads managed in the pool (including threads that have been
	 * canceled, this allows to join them later), as worker_thread_t
	 */
	linked_list_t *threads;
};

/**
 * Worker thread
 */
typedef struct {

	/**
	 * Reference to the processor
	 */
	private_processor_t *processor;

	/**
	 * The actual thread
	 */
	thread_t *thread;

	/**
	 * Job currently being executed by this worker thread
	 */
	job_t *job;

	/**
	 * Priority of the current job
	 */
	job_priority_t priority;

} worker_thread_t;