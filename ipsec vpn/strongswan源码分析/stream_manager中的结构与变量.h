/**
 * Manages client-server connections and services using stream_t backends.
 * 管理客户端-服务器连接，
 */
struct stream_manager_t {

	/**
	 * Create a client-server connection to a service.
	 *
	 * @param uri		URI of service to connect to
	 * @return			stream instance, NULL on error
	 */
	stream_t* (*connect)(stream_manager_t *this, char *uri);

	/**
	 * Create a new service under an URI to accept() client connections.
	 *
	 * @param uri		URI of service to provide
	 * @param backlog	size of the backlog queue, as passed to listen()
	 * @return			service, NULL on error
	 */
	stream_service_t* (*create_service)(stream_manager_t *this, char *uri,
										int backlog);

	/**
	 * Register a stream backend to the manager.
	 *
	 * @param prefix	prefix of URIs to use the backend for
	 * @param create	constructor function for the stream
	 */
	void (*add_stream)(stream_manager_t *this, char *prefix,
					   stream_constructor_t create);

	/**
	 * Unregister stream backends from the manager.
	 *
	 * @param create	constructor function passed to add_stream()
	 */
	void (*remove_stream)(stream_manager_t *this, stream_constructor_t create);

	/**
	 * Register a stream service backend to the manager.
	 *
	 * @param prefix	prefix of URIs to use the backend for
	 * @param create	constructor function for the stream service
	 */
	void (*add_service)(stream_manager_t *this, char *prefix,
						stream_service_constructor_t create);

	/**
	 * Unregister stream service backends from the manager.
	 *
	 * @param create	constructor function passed to add_service()
	 */
	void (*remove_service)(stream_manager_t *this,
						   stream_service_constructor_t create);

	/**
	 * Destroy a stream_manager_t.
	 */
	void (*destroy)(stream_manager_t *this);
};


========================================================================

/**
 * Private data of an stream_manager_t object.
 */
struct private_stream_manager_t {

	/**
	 * Public stream_manager_t interface.
	 */
	stream_manager_t public;

	/**
	 * List of registered stream constructors, as stream_entry_t
	 */
	linked_list_t *streams;

	/**
	 * List of registered service constructors, as service_entry_t
	 */
	linked_list_t *services;

	/**
	 * Lock for all lists
	 */
	rwlock_t *lock;
};

/**
 * Registered stream backend
 */
typedef struct {
	/** URI prefix */
	char *prefix;
	/** constructor function */
	stream_constructor_t create;
} stream_entry_t;

/**
 * Registered service backend
 */
typedef struct {
	/** URI prefix */
	char *prefix;
	/** constructor function */
	stream_service_constructor_t create;
} service_entry_t;