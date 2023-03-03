/**
 * The scheduler(������) queues timed events which are then passed to the processor.
 * ���������ڶ����ݽṹ������һ��������������������ԣ�
 * �����ӽڵ��key��Ҫô�����ڸ��ڵ㣬Ҫô��С�ڸ��ڵ㣬���Ը��ڵ�Ҫô��С��Ҫô���
 * ����ʹ���¼������ȵ�ʱ����Ϊkeyֵ����ʱ���ڵ��������´�Ҫ�������Ǹ��¼�
 * ���ȵ�������ʵ����ʹ�õ���������(������¼�)�����ַ�ʽ��������ɾ����һ���¼��ܸ�Ч��
 * ����׷���¼�Ҳ�ܸ�Ч�������ǵ��¼���������úܶ�ʱ�����м����ڵ��Խ��Խ�����������
 * ÿ�����ӻ���������¼���IKE-rekey, NAT-keepalive,�ش�, ����(�뿪) �ȵ�.
 * ����һ������Ҫ������ǧ������ʱ����Ҫ��Ч��ά���������¼�������Ϊ���̰߳�ȫ��
 * �͵�ʹ���������ʹ�����ø��Ӹ��ӣ����¼��ڱ��������ʱ���¼���û���¼�������
 * ������Ҫ�����¼��㹻��
 * ����Ƕ����ݽṹ�����ơ������¼������кܿ죬����ɾ�����ڵ�Ҳ�ܿ졣
 * �����ڶ�������Ҫ10000�αȽϣ����ڶѽṹ�У�����������Ҫ��Լ13.3�αȽ�
 * ��ʵ����ʹ��һ��������ָ��һ��һά���飬������˴洢�����ұ��ڵ�����
 * ��nλ�õ��ӽڵ㣬�������е�λ����2n��2n+1��������µĵ�����Ϊ�������ļ���
 * �����·����ڶ��в���Ԫ�أ������Ǵ�������䣬ֱ����һ�����ˣ�Ȼ������µ���
 * ��Ӧ�������У����Ϊ��Ԫ����ӵ���һ������λ�ã���һλ�����У���λ�õ�ͬ��
 * ��ǰ����Ԫ�ص�������Ȼ��Զ�������Ҫ���ָ���Ҳ����˵���µ�Ԫ����Ҫ���Ͻ���
 * ֱ�����϶ѵĽṹ�ص�
 * �Ӷ����Ƴ��¼���֮���ơ�ʵ�ʴ��ڸ�λ�ã�����ĵ�1��λ�ã�
 * �������Ƴ����Ȱ����һ��Ԫ�ط��ڵ�һ��λ�ã�Ȼ�������½����ķ�����
 * ֱ���ָ��ѵĽṹ�ص�
 */
struct scheduler_t {

	// ���һ��event�����У��ѣ��У���ָ��ʲôʱ��ִ�и��¼���ʹ�����ʱ�䣬����Ϊ��λ
	void (*schedule_job) (scheduler_t *this, job_t *job, uint32_t s);

	// ���һ��event�����У��ѣ��У���ָ��ʲôʱ��ִ�и��¼���ʹ�����ʱ�䣬�Ժ���Ϊ��λ
	void (*schedule_job_ms) (scheduler_t *this, job_t *job, uint32_t ms);

	// ���һ��event�����У��ѣ��У���ָ��ʲôʱ��ִ�и��¼���ʹ�þ���ʱ��
	void (*schedule_job_tv) (scheduler_t *this, job_t *job, timeval_t tv);

	// �����ж��ٸ��¼���ִ��
	u_int (*get_job_load) (scheduler_t *this);

	// ɾ�����д����ȵ��¼�
	void (*flush)(scheduler_t *this);

	// ������
	void (*destroy) (scheduler_t *this);
};

==================================================

struct event_t {
	timeval_t time;  //ʲôʱ������ĸ��¼�
	job_t *job;     //���¼�Ҫִ��ʲô��������ʲô��
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


