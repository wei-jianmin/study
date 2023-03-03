/**
 * The processor uses threads to process queued jobs.
 * ������������ڲ�ά�� threads
 */
struct processor_t {

	/**
	 * Get the total number of threads used by the processor.
	 *
	 * @return				size of thread pool
	 */
	u_int (*get_total_threads) (processor_t *this);  //��ȡ���߳���

	/**
	 * Get the number of threads currently waiting for work.
	 *
	 * @return				number of idle threads
	 */
	u_int (*get_idle_threads) (processor_t *this);  //��ȡ�����߳���

	/**
	 * Get the number of threads currently working, per priority class.
	 *
	 * @param				priority to check
	 * @return				number of threads in priority working
	 */
	u_int (*get_working_threads)(processor_t *this, job_priority_t prio);  //��ȡ��ÿһ���ȼ��£����ڹ������߳���

	/**
	 * Get the number of queued jobs for a specified priority.
	 *
	 * @param prio			priority class to get job load for
	 * @return				number of items in queue
	 */
	u_int (*get_job_load) (processor_t *this, job_priority_t prio);   //���̼����˶��ٸ�Ҫִ�е�job

	/**
	 * Adds a job to the queue.
	 *
	 * This function is non blocking and adds a job_t to the queue.
	 *
	 * @param job			job to add to the queue
	 */
	void (*queue_job) (processor_t *this, job_t *job);   //�����̣��Ķ��У������job ���������ģ�

	/**
	 * Directly execute a job with an idle worker thread.
	 *
	 * If no idle thread is available, the job gets executed by the calling
	 * thread.
	 *
	 * @param job			job, gets destroyed
	 */
	void (*execute_job)(processor_t *this, job_t *job);   //�ý���ֱ��ִ��һ��job�������ģ�

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
	void (*set_threads)(processor_t *this, u_int count);  //���ý������̳߳صĴ�С

	/**
	 * Sets the number of threads to 0 and cancels all blocking jobs, then waits
	 * for all threads to be terminated.
	 */
    //����̳߳أ��ر������̣߳������������job���У��ȴ����У�����ִ��job�ģ��߳̽���
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
	 * ��ǰ�������е��߳������������е�
	 * �� charon.c��main �� charon->start ��lib->processor->set_threads ʱ
	 * ����� desired_threads-total_threads ��worker���ŵ� threads ������
	 * ���� total_threads = desired_threads
	 * total_threads ���Դ��� desired_threads��������С�� desired_threads
	 */
	u_int total_threads;

	/**
	 * �ܹ���Ҫ���߳���
	 * Desired number of threads
	 */
	u_int desired_threads;

	/**
	 * 5�����ȼ��ֱ���ж��ٷǿ����߳�
	 * Number of threads currently working, for each priority
	 */
	u_int working_threads[JOB_PRIO_MAX];  

	/**
	 * 5�����ȼ��ֱ������/��Ҫ�����̣߳����������̺߳Ϳ����̣߳� ��
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
	 * ÿ�����ȼ���Ӧһ�������б�
	 * A list of queued jobs for each priority
	 */
	linked_list_t *jobs[JOB_PRIO_MAX];
	
	/**
	 * ���̳߳��й��������̣߳�worker_thread_t������
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