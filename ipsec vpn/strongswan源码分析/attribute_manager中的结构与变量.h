/**
 * IKE配置属性管理器分发或处理属性
 * The attribute manager hands out attributes or handles them.
 *
 * The attribute manager manages both, attribute providers and attribute
 * handlers. 
 * '属性分发'负责分发属性--如果一个连接对端需要它们
 * '属性处理'负责当从请求的对端收到属性时，处理它们
 * Attribute providers are responsible to hand out attributes if
 * a connecting peer requests them. Handlers handle such attributes if they
 * are received on the requesting peer.
 */
struct attribute_manager_t {

	/**
	 * Acquire a virtual IP address to assign to a peer.
	 *
	 * @param pools			list of pool names (char*) to acquire from
	 * @param ike_sa		associated IKE_SA for which an address is requested
	 * @param requested		IP in configuration request
	 * @return				allocated address, NULL to serve none
	 */
	host_t* (*acquire_address)(attribute_manager_t *this,
							   linked_list_t *pool, ike_sa_t *ike_sa,
							   host_t *requested);

	/**
	 * Release a previously acquired address.
	 *
	 * @param pools			list of pool names (char*) to release to
	 * @param address		address to release
	 * @param ike_sa		associated IKE_SA for which an address is released
	 * @return				TRUE if address released to pool
	 */
	bool (*release_address)(attribute_manager_t *this,
							linked_list_t *pools, host_t *address,
							ike_sa_t *ike_sa);

	/**
	 * Create an enumerator over attributes to hand out to a peer.
	 *
	 * @param pool			list of pools names (char*) to query attributes from
	 * @param ike_sa		associated IKE_SA for which attributes are requested
	 * @param vip			list of virtual IPs (host_t*) to assign to peer
	 * @return				enumerator (configuration_attribute_type_t, chunk_t)
	 */
	enumerator_t* (*create_responder_enumerator)(attribute_manager_t *this,
									linked_list_t *pool, ike_sa_t *ike_sa,
									linked_list_t *vips);

	/**
	 * Register an attribute provider to the manager.
	 *
	 * @param provider		attribute provider to register
	 */
	void (*add_provider)(attribute_manager_t *this,
						 attribute_provider_t *provider);
	/**
	 * Unregister an attribute provider from the manager.
	 *
	 * @param provider		attribute provider to unregister
	 */
	void (*remove_provider)(attribute_manager_t *this,
							attribute_provider_t *provider);

	/**
	 * Handle a configuration attribute by passing them to the handlers.
	 *
	 * @param ike_sa		associated IKE_SA to handle an attribute for
	 * @param handler		handler we requested the attribute for, if any
	 * @param type			type of configuration attribute
	 * @param data			associated attribute data
	 * @return				handler which handled this attribute, NULL if none
	 */
	attribute_handler_t* (*handle)(attribute_manager_t *this,
						ike_sa_t *ike_sa, attribute_handler_t *handler,
						configuration_attribute_type_t type, chunk_t data);

	/**
	 * Release an attribute previously handle()d by a handler.
	 *
	 * @param ike_sa		associated IKE_SA to release an attribute for
	 * @param server		server from which the attribute was received
	 * @param type			type of attribute to release
	 * @param data			associated attribute data
	 */
	void (*release)(attribute_manager_t *this, attribute_handler_t *handler,
						ike_sa_t *ike_sa, configuration_attribute_type_t type,
						chunk_t data);

	/**
	 * Create an enumerator over attributes to request from server.
	 *
	 * @param ike_sa		associated IKE_SA to request attributes for
	 * @param vip			list of virtual IPs (host_t*) going to request
	 * @return				enumerator (attribute_handler_t, ca_type_t, chunk_t)
	 */
	enumerator_t* (*create_initiator_enumerator)(attribute_manager_t *this,
									ike_sa_t *ike_sa, linked_list_t *vips);

	/**
	 * Register an attribute handler to the manager.
	 *
	 * @param handler		attribute handler to register
	 */
	void (*add_handler)(attribute_manager_t *this,
						attribute_handler_t *handler);

	/**
	 * Unregister an attribute handler from the manager.
	 *
	 * @param handler		attribute handler to unregister
	 */
	void (*remove_handler)(attribute_manager_t *this,
						   attribute_handler_t *handler);

	/**
	 * Destroy a attribute_manager instance.
	 */
	void (*destroy)(attribute_manager_t *this);
};

======================================================================

/**
 * private data of attribute_manager
 */
struct private_attribute_manager_t {

	/**
	 * public functions
	 */
	attribute_manager_t public;

	/**
	 * list of registered providers
	 */
	linked_list_t *providers;

	/**
	 * list of registered handlers
	 */
	linked_list_t *handlers;

	/**
	 * rwlock provider list
	 */
	rwlock_t *lock;
};

/**
 * Data to pass to enumerator filters
 */
typedef struct {
	/** attribute group pools */
	linked_list_t *pools;
	/** associated IKE_SA */
	ike_sa_t *ike_sa;
	/** requesting/assigned virtual IPs */
	linked_list_t *vips;
} enum_data_t;

/**
 * Enumerator implementation to enumerate nested initiator attributes
 */
typedef struct {
	/** implements enumerator_t */
	enumerator_t public;
	/** back ref */
	private_attribute_manager_t *this;
	/** currently processing handler */
	attribute_handler_t *handler;
	/** outer enumerator over handlers */
	enumerator_t *outer;
	/** inner enumerator over current handlers attributes */
	enumerator_t *inner;
	/** IKE_SA to request attributes for */
	ike_sa_t *ike_sa;
	/** virtual IPs we are requesting along with attriubutes */
	linked_list_t *vips;
} initiator_enumerator_t;