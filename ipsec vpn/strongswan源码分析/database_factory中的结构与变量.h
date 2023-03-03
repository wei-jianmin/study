/**
 * Create instances of database connections using registered constructors.
 */
struct database_factory_t {

	/**
	 * Create a database connection instance.
	 *
	 * @param uri		implementation specific connection URI
	 * @return			database_t instance, NULL if not supported/failed
	 */
	database_t* (*create)(database_factory_t *this, char *uri);

	/**
	 * Register a database constructor.
	 *
	 * @param create	database constructor to register
	 */
	void (*add_database)(database_factory_t *this, database_constructor_t create);

	/**
	 * Unregister a previously registered database constructor.
	 *
	 * @param create	database constructor to unregister
	 */
	void (*remove_database)(database_factory_t *this, database_constructor_t create);

	/**
	 * Destroy a database_factory instance.
	 */
	void (*destroy)(database_factory_t *this);
};

=========================================================

/**
 * private data of database_factory
 */
struct private_database_factory_t {

	/**
	 * public functions
	 */
	database_factory_t public;

	/**
	 * list of registered database_t implementations
	 */
	linked_list_t *databases;

	/**
	 * mutex to lock access to databases
	 */
	mutex_t *mutex;
};