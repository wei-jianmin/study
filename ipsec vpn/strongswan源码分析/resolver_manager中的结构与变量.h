/**
 * The resolver_manager manages the resolver implementations and
 * creates instances of them.
 *
 * A resolver plugin is registered by providing its constructor function
 * to the manager. The manager creates instances of the resolver plugin
 * using the registered constructor function.
 */
struct resolver_manager_t {

	/**
	 * Register a resolver implementation.
	 *
	 * @param constructor	resolver constructor function
	 */
	void (*add_resolver)(resolver_manager_t *this,
						 resolver_constructor_t constructor);

	/**
	 * Unregister a previously registered resolver implementation.
	 *
	 * @param constructor	resolver constructor function to unregister
	 */
	void (*remove_resolver)(resolver_manager_t *this,
							resolver_constructor_t constructor);

	/**
	 * Get a new resolver instance.
	 *
	 * @return 				resolver instance.
	 */
	resolver_t* (*create)(resolver_manager_t *this);

	/**
	 * Destroy a resolver_manager instance.
	 */
	void (*destroy)(resolver_manager_t *this);
};

==============================================================

/**
 * private data of resolver_manager
 */
struct private_resolver_manager_t {

	/**
	 * public functions
	 */
	resolver_manager_t public;

	/**
	 * constructor function to create resolver instances
	 */
	resolver_constructor_t constructor;
};