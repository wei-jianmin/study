/**
 * Resolve hosts by DNS name but do so in a separate thread (calling
 * getaddrinfo(3) directly might block indefinitely, or at least a very long
 * time if no DNS servers are reachable).
 */
struct host_resolver_t {

	/**
	 * Resolve host from the given DNS name.
	 *
	 * @param name		name to lookup
	 * @param family	requested address family
	 * @return			resolved host or NULL if failed or canceled
	 */
	host_t *(*resolve)(host_resolver_t *this, char *name, int family);

	/**
	 * Flush the queue of queries. No new queries will be accepted afterwards.
	 */
	void (*flush)(host_resolver_t *this);

	/**
	 * Destroy a host_resolver_t.
	 */
	void (*destroy)(host_resolver_t *this);
};

===============================================

/**
 * Private data of host_resolver_t
 */
struct private_host_resolver_t {

	/**
	 * Public interface
	 */
	host_resolver_t public;

	/**
	 * Hashtable to check for queued queries, query_t*
	 */
	hashtable_t *queries;

	/**
	 * Queue for queries, query_t*
	 */
	linked_list_t *queue;

	/**
	 * Mutex to safely access private data
	 */
	mutex_t *mutex;

	/**
	 * Condvar（条件变量） to signal arrival of new queries
	 */
	condvar_t *new_query;

	/**
	 * Minimum number of resolver threads
	 */
	u_int min_threads;

	/**
	 * Maximum number of resolver threads
	 */
	u_int max_threads;

	/**
	 * Current number of threads
	 */
	u_int threads;

	/**
	 * Current number of busy threads
	 */
	u_int busy_threads;

	/**
	 * Pool of threads, thread_t*
	 */
	linked_list_t *pool;

	/**
	 * TRUE if no new queries are accepted
	 */
	bool disabled;

};

typedef struct {
	/** DNS name we are looking for */
	char *name;
	/** address family we request */
	int family;
	/** Condvar to signal completion of a query */
	condvar_t *done;
	/** refcount */
	refcount_t refcount;
	/** the result if successful */
	host_t *result;
} query_t;