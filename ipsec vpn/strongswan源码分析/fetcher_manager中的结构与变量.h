/**
 * 使用注册的 fetcher_t 实例，从 URIs 中获取 status_t
 * Fetches from URIs using registered fetcher_t instances.
 */
struct fetcher_manager_t {

	/**
	 * Fetch data from URI.
	 *
	 * The variable argument list contains fetcher_option_t's, followed
	 * by a option specific data argument.
	 * If no FETCH_CALLBACK function is given as option, userdata must be
	 * a chunk_t*. This chunk gets allocated, accumulated data using the
	 * fetcher_default_callback() function.
	 *
	 * @param uri			URI to fetch from
	 * @param userdata		userdata to pass to callback function.
	 * @param options		FETCH_END terminated fetcher_option_t arguments
	 * @return				status indicating result of fetch
	 */
	status_t (*fetch)(fetcher_manager_t *this, char *url, void *userdata, ...);

	/**
	 * Register a fetcher implementation.
	 *
	 * @param constructor	fetcher constructor function
	 * @param url			URL type this fetcher fetches, e.g. "http://"
	 */
	void (*add_fetcher)(fetcher_manager_t *this,
						fetcher_constructor_t constructor, char *url);

	/**
	 * Unregister a previously registered fetcher implementation.
	 *
	 * @param constructor	fetcher constructor function to unregister
	 */
	void (*remove_fetcher)(fetcher_manager_t *this,
						   fetcher_constructor_t constructor);

	/**
	 * Destroy a fetcher_manager instance.
	 */
	void (*destroy)(fetcher_manager_t *this);
};


============================================================

/**
 * private data of fetcher_manager
 */
struct private_fetcher_manager_t {

	/**
	 * public functions
	 */
	fetcher_manager_t public;

	/**
	 * list of registered fetchers, as entry_t
	 */
	linked_list_t *fetchers;

	/**
	 * read write lock to list
	 */
	rwlock_t *lock;
};

typedef struct {
	/** associated fetcher construction function */
	fetcher_constructor_t create;
	/** URL this fetcher support */
	char *url;
} entry_t;