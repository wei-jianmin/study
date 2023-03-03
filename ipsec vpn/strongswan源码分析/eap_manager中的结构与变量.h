/**
 * The EAP manager manages all EAP implementations and creates instances.
 *
 * A plugin registers it's implemented EAP method at the manager by
 * providing type and a constructor function. The manager then instantiates
 * eap_method_t instances through the provided constructor to handle
 * EAP authentication.
 */
struct eap_manager_t {

	/**
	 * Register a EAP method implementation.
	 *
	 * @param method		vendor specific method, if vendor != 0
	 * @param vendor		vendor ID, 0 for non-vendor (default) EAP methods
	 * @param role			EAP role of the registered method
	 * @param constructor	constructor function, returns an eap_method_t
	 */
	void (*add_method)(eap_manager_t *this, eap_type_t type, uint32_t vendor,
					   eap_role_t role, eap_constructor_t constructor);

	/**
	 * Unregister a EAP method implementation using it's constructor.
	 *
	 * @param constructor	constructor function to remove, as added in add_method
	 */
	void (*remove_method)(eap_manager_t *this, eap_constructor_t constructor);

	/**
	 * Enumerate the registered EAP authentication methods for the given role.
	 *
	 * @note Only authentication types are enumerated (e.g. EAP-Identity is not
	 * even though it is registered as method with this manager).
	 *
	 * @param role			EAP role of methods to enumerate
	 * @return				enumerator over (eap_type_t type, uint32_t vendor)
	 */
	enumerator_t* (*create_enumerator)(eap_manager_t *this, eap_role_t role);

	/**
	 * Create a new EAP method instance.
	 *
	 * @param type			type of the EAP method
	 * @param vendor		vendor ID, 0 for non-vendor (default) EAP methods
	 * @param role			role of EAP method, either EAP_SERVER or EAP_PEER
	 * @param server		identity of the server
	 * @param peer			identity of the peer (client)
	 * @return				EAP method instance, NULL if no constructor found
	 */
	eap_method_t* (*create_instance)(eap_manager_t *this, eap_type_t type,
									 uint32_t vendor, eap_role_t role,
									 identification_t *server,
									 identification_t *peer);

	/**
	 * Destroy a eap_manager instance.
	 */
	void (*destroy)(eap_manager_t *this);
};

===============================================

/**
 * EAP constructor entry
 */
struct eap_entry_t {

	/**
	 * EAP method type, vendor specific if vendor is set
	 */
	eap_type_t type;

	/**
	 * vendor ID, 0 for default EAP methods
	 */
	uint32_t vendor;

	/**
	 * Role of the method returned by the constructor, EAP_SERVER or EAP_PEER
	 */
	eap_role_t role;

	/**
	 * constructor function to create instance
	 */
	eap_constructor_t constructor;
};

/**
 * private data of eap_manager
 */
struct private_eap_manager_t {

	/**
	 * public functions
	 */
	eap_manager_t public;

	/**
	 * list of eap_entry_t's
	 */
	linked_list_t *methods;

	/**
	 * rwlock to lock methods
	 */
	rwlock_t *lock;
};