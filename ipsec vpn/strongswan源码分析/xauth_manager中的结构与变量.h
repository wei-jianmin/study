/**
 * The XAuth manager manages all XAuth implementations and creates instances.
 *
 * A plugin registers it's implemented XAuth method at the manager by
 * providing type and a constructor function. The manager then instantiates
 * xauth_method_t instances through the provided constructor to handle
 * XAuth authentication.
 */
struct xauth_manager_t {

	/**
	 * Register a XAuth method implementation.
	 *
	 * @param name			backend name to register
	 * @param role			XAUTH_SERVER or XAUTH_PEER
	 * @param constructor	constructor function, returns an xauth_method_t
	 */
	void (*add_method)(xauth_manager_t *this, char *name,
					   xauth_role_t role, xauth_constructor_t constructor);

	/**
	 * Unregister a XAuth method implementation using it's constructor.
	 *
	 * @param constructor	constructor function, as added in add_method
	 */
	void (*remove_method)(xauth_manager_t *this, xauth_constructor_t constructor);

	/**
	 * Create a new XAuth method instance.
	 *
	 * The name may contain an option string, separated by a colon. This option
	 * string gets passed to the XAuth constructor to specify the behavior
	 * of the XAuth method.
	 *
	 * @param name			backend name, with optional config string
	 * @param role			XAUTH_SERVER or XAUTH_PEER
	 * @param server		identity of the server
	 * @param peer			identity of the peer (client)
	 * @return				XAUTH method instance, NULL if no constructor found
	 */
	xauth_method_t* (*create_instance)(xauth_manager_t *this,
							char *name, xauth_role_t role,
							identification_t *server, identification_t *peer);

	/**
	 * Destroy a eap_manager instance.
	 */
	void (*destroy)(xauth_manager_t *this);
};

=============================================================================

/**
 * XAuth constructor entry
 */
struct xauth_entry_t {

	/**
	 * Xauth backend name
	 */
	char *name;

	/**
	 * Role of the method, XAUTH_SERVER or XAUTH_PEER
	 */
	xauth_role_t role;

	/**
	 * constructor function to create instance
	 */
	xauth_constructor_t constructor;
};

/**
 * private data of xauth_manager
 */
struct private_xauth_manager_t {

	/**
	 * public functions
	 */
	xauth_manager_t public;

	/**
	 * list of eap_entry_t's
	 */
	linked_list_t *methods;

	/**
	 * rwlock to lock methods
	 */
	rwlock_t *lock;
};
