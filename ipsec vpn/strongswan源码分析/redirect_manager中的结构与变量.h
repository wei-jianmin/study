/**
 * Manages redirect providers.
 */
struct redirect_manager_t {

	/**
	 * Add a redirect provider.
	 *
	 * All registered providers are queried until one of them decides to
	 * redirect a client.
	 *
	 * A provider may be called concurrently for different IKE_SAs.
	 *
	 * @param provider	provider to register
	 */
	void (*add_provider)(redirect_manager_t *this,
						 redirect_provider_t *provider);

	/**
	 * Remove a redirect provider.
	 *
	 * @param provider	provider to unregister
	 */
	void (*remove_provider)(redirect_manager_t *this,
							redirect_provider_t *provider);

	/**
	 * Determine whether a client should be redirected upon receipt of the
	 * IKE_SA_INIT message.
	 *
	 * @param ike_sa		IKE_SA for which this is called
	 * @param gateway[out]	new IKE gateway (IP or FQDN)
	 * @return				TRUE if client should be redirected, FALSE otherwise
	 */
	bool (*redirect_on_init)(redirect_manager_t *this, ike_sa_t *ike_sa,
							 identification_t **gateway);

	/**
	 * Determine whether a client should be redirected after the IKE_AUTH has
	 * been handled.  Should be called after the client is authenticated and
	 * when the server authenticates itself.
	 *
	 * @param ike_sa		IKE_SA for which this is called
	 * @param gateway[out]	new IKE gateway (IP or FQDN)
	 * @return				TRUE if client should be redirected, FALSE otherwise
	 */
	bool (*redirect_on_auth)(redirect_manager_t *this, ike_sa_t *ike_sa,
							 identification_t **gateway);

	/**
	 * Destroy this instance.
	 */
	void (*destroy)(redirect_manager_t *this);
};

===================================================================

/**
 * Gateway identify types
 *
 * The encoding is the same as that for corresponding ID payloads.
 */
typedef enum {
	/** IPv4 address of the VPN gateway */
	GATEWAY_ID_TYPE_IPV4 = 1,
	/** IPv6 address of the VPN gateway */
	GATEWAY_ID_TYPE_IPV6 = 2,
	/** FQDN of the VPN gateway */
	GATEWAY_ID_TYPE_FQDN = 3,
} gateway_id_type_t;

/**
 * Private data
 */
struct private_redirect_manager_t {

	/**
	 * Public interface
	 */
	redirect_manager_t public;

	/**
	 * Registered providers
	 */
	linked_list_t *providers;

	/**
	 * Lock to access list of providers
	 */
	rwlock_t *lock;
};

