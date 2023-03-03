/**
 * The scheduler(调度器) queues timed events which are then passed to the processor.
 * 调度器基于堆数据结构，这是一种特殊的树，有如下特性：
 * 所有子节点的key，要么都大于父节点，要么都小于父节点，所以根节点要么最小，要么最大
 * 我们使用事件被调度的时间作为key值，此时根节点则总是下次要触发的那个事件
 * 早先调度器的实现是使用的有序链表(来存放事件)，这种方式的优势是删除下一个事件很高效，
 * 并且追加事件也很高效，问题是当事件的数量变得很多时，在中间插入节点会越来越慢（需遍历）
 * 每个连接会产生几个事件：IKE-rekey, NAT-keepalive,重传, 过期(半开) 等等.
 * 所以一个网关要处理上千个连接时，需要高效的维护大量的事件，而且为了线程安全，
 * 就得使用锁，这会使事情变得更加复杂，当事件在被插入队列时，事件将没有事件被处理，
 * 所以需要插入事件足够快
 * 这就是对数据结构的优势。插入事件到堆中很快，而且删除根节点也很快。
 * 假设在队列中需要10000次比较，则在堆结构中，最坏的情况是需要大约13.3次比较
 * 其实现是使用一个二叉树指向一个一维数组，这减少了存储开销且便于导航：
 * 在n位置的子节点，在数组中的位置是2n和2n+1，因此上下的导航简化为对索引的计算
 * 按如下方法在堆中插入元素：堆总是从左到右填充，直到这一行满了，然后添加新的行
 * 对应到数组中，这变为将元素添加到第一个空闲位置，在一位数组中，其位置等同于
 * 当前堆中元素的数量。然后对堆属性需要被恢复，也就是说，新的元素需要向上交换
 * 直到符合堆的结构特点
 * 从堆中移除事件与之类似。实际存在根位置（数组的第1个位置）
 * 当它被移除后，先把最后一个元素放在第一个位置，然后按照向下交换的方法，
 * 直到恢复堆的结构特点
 */
struct scheduler_t {

	// 添加一个event到队列（堆）中，并指定什么时间执行该事件，使用相对时间，以秒为单位
	void (*schedule_job) (scheduler_t *this, job_t *job, uint32_t s);

	// 添加一个event到队列（堆）中，并指定什么时间执行该事件，使用相对时间，以毫秒为单位
	void (*schedule_job_ms) (scheduler_t *this, job_t *job, uint32_t ms);

	// 添加一个event到队列（堆）中，并指定什么时间执行该事件，使用绝对时间
	void (*schedule_job_tv) (scheduler_t *this, job_t *job, timeval_t tv);

	// 返回有多少个事件待执行
	u_int (*get_job_load) (scheduler_t *this);

	// 删除所有待调度的事件
	void (*flush)(scheduler_t *this);

	// 自销毁
	void (*destroy) (scheduler_t *this);
};

==================================================

struct event_t {
	timeval_t time;  //什么时候产生的该事件
	job_t *job;     //该事件要执行什么操作（干什么）
};

/**
 * Private data of a scheduler_t object.
 */
struct private_scheduler_t {

	/**
	 * Public part of a scheduler_t object.
	 */
	 scheduler_t public;

	/**
	 * The heap in which the events are stored.
	 */
	event_t **heap;

	/**
	 * The size of the heap.
	 */
	u_int heap_size;

	/**
	 * The number of scheduled events.
	 */
	u_int event_count;

	/**
	 * Exclusive access to list
	 */
	mutex_t *mutex;

	/**
	 * Condvar to wait for next job.
	 */
	condvar_t *condvar;
};


