对等体的配置，由 ID 指定。
对等配置定义了两个给定 ID 之间的连接。 
它只包含一个 ike_cfg_t，用于启动。
此外，它还包含多个 child_cfg_t，定义该对等体允许哪些 CHILD_SA。
                          +-------------------+        +---------------+
   +---------------+      |     peer_cfg      |      +---------------+ |
   |    ike_cfg    |      +-------------------+      |   child_cfg   | |
   +---------------+      | - ids             |      +---------------+ |
   | - hosts       | 1  1 | - cas             | 1  n | - proposals   | |
   | - proposals   |<-----| - auth info       |----->| - traffic sel | |
   | - ...         |      | - dpd config      |      | - ...         |-+
   +---------------+      | - ...             |      +---------------+
                          +-------------------+
                             | 1         0 |
                             |             |
                             v n         n V
             +-------------------+     +-------------------+
           +-------------------+ |   +-------------------+ |
           |     auth_cfg      | |   |     auth_cfg      | |
           +-------------------+ |   +-------------------+ |
           | - local rules     |-+   | - remote constr.  |-+
           +-------------------+     +-------------------+
每个 peer_cfg 都有两个附加的身份验证配置列表。
本地身份验证配置定义了如何针对远程对等方进行身份验证。 
每个配置都使用多重身份验证扩展 (RFC4739) 强制执行。
远程身份验证配置作为约束处理。 
对等方必须满足这些规则中的每一个（使用多重身份验证，以任何顺序）才能访问配置。

struct peer_cfg_t {
	/**
	 * Get the name of the peer_cfg. 
	 * Returned object is not getting cloned. 
	 * @return				peer_cfg's name
	 */
	char* (*get_name) (peer_cfg_t *this);
	/**
	 * Get the IKE version to use for initiating. 
	 * @return				IKE major version
	 */
	ike_version_t (*get_ike_version)(peer_cfg_t *this);
	/**
	 * Get the IKE config to use for initiaton. 
	 * @return				the IKE config to use
	 */
	ike_cfg_t* (*get_ike_cfg) (peer_cfg_t *this);
	/**
	 * Attach a CHILD config. 
	 * @param child_cfg		CHILD config to add
	 */
	void (*add_child_cfg) (peer_cfg_t *this, child_cfg_t *child_cfg);
	/**
	 * Detach a CHILD config, pointed to by an enumerator. 
	 * @param enumerator	enumerator indicating element position
	 */
	void (*remove_child_cfg)(peer_cfg_t *this, enumerator_t *enumerator);
	/**
	 * Replace the CHILD configs with those in the given PEER config. 
	 * The enumerator enumerates the removed and added CHILD configs
	 * (child_cfg_t*, bool), where the flag is FALSE for removed configs and
	 * TRUE for added configs. Configs that are equal are not enumerated. 
	 * @param other			other config to get CHILD configs from
	 * @return				an enumerator over removed/added CHILD configs
	 */
	enumerator_t* (*replace_child_cfgs)(peer_cfg_t *this, peer_cfg_t *other);
	/**
	 * Create an enumerator for all attached CHILD configs. 
	 * @return				an enumerator over all CHILD configs.
	 */
	enumerator_t* (*create_child_cfg_enumerator) (peer_cfg_t *this);
	/**
	 * Select a CHILD config from traffic selectors. 
	 * @param my_ts			TS for local side
	 * @param other_ts		TS for remote side
	 * @param my_hosts		hosts to narrow down dynamic TS for local side
	 * @param other_hosts	hosts to narrow down dynamic TS for remote side
	 * @return				selected CHILD config, or NULL if no match found
	 */
	child_cfg_t* (*select_child_cfg) (peer_cfg_t *this,
							linked_list_t *my_ts, linked_list_t *other_ts,
							linked_list_t *my_hosts, linked_list_t *other_hosts);
	/**
	 * Add an authentication config to the peer configuration. 
	 * @param cfg			config to add
	 * @param local			TRUE for local rules, FALSE for remote constraints
	 */
	void (*add_auth_cfg)(peer_cfg_t *this, auth_cfg_t *cfg, bool local);
	/**
	 * Create an enumerator over registered authentication configs. 
	 * @param local			TRUE for local rules, FALSE for remote constraints
	 * @return				enumerator over auth_cfg_t*
	 */
	enumerator_t* (*create_auth_cfg_enumerator)(peer_cfg_t *this, bool local);
	/**
	 * Should a certificate be sent for this connection? 
	 * @return			certificate sending policy
	 */
	cert_policy_t (*get_cert_policy) (peer_cfg_t *this);
	/**
	 * How to handle uniqueness of IKE_SAs? 
	 * @return			unique policy
	 */
	unique_policy_t (*get_unique_policy) (peer_cfg_t *this);
	/**
	 * Get the max number of retries after timeout. 
	 * @return			max number retries
	 */
	uint32_t (*get_keyingtries) (peer_cfg_t *this);
	/**
	 * Get a time to start rekeying. 
	 * @param jitter	subtract a jitter value to randomize time
	 * @return			time in s when to start rekeying, 0 disables rekeying
	 */
	uint32_t (*get_rekey_time)(peer_cfg_t *this, bool jitter);
	/**
	 * Get a time to start reauthentication. 
	 * @param jitter	subtract a jitter value to randomize time
	 * @return			time in s when to start reauthentication, 0 disables it
	 */
	uint32_t (*get_reauth_time)(peer_cfg_t *this, bool jitter);
	/**
	 * Get the timeout of a rekeying/reauthenticating SA. 
	 * @return			timeout in s
	 */
	uint32_t (*get_over_time)(peer_cfg_t *this);
	/**
	 * Use MOBIKE (RFC4555) if peer supports it? 
	 * @return			TRUE to enable MOBIKE support
	 */
	bool (*use_mobike) (peer_cfg_t *this);
	/**
	 * Use/Accept aggressive mode with IKEv1?. 
	 * @return			TRUE to use aggressive mode
	 */
	bool (*use_aggressive)(peer_cfg_t *this);
	/**
	 * Use pull or push mode for mode config? 
	 * @return			TRUE to use pull, FALSE to use push mode
	 */
	bool (*use_pull_mode)(peer_cfg_t *this);
	/**
	 * Get the DPD check interval. 
	 * @return			dpd_delay in seconds
	 */
	uint32_t (*get_dpd) (peer_cfg_t *this);
	/**
	 * Get the DPD timeout interval (IKEv1 only) 
	 * @return			dpd_timeout in seconds
	 */
	uint32_t (*get_dpd_timeout) (peer_cfg_t *this);
	/**
	 * Add a virtual IP to request as initiator. 
	 * @param vip			virtual IP to request, may be %any or %any6
	 */
	void (*add_virtual_ip)(peer_cfg_t *this, host_t *vip);
	/**
	 * Create an enumerator over virtual IPs to request. 
	 * The returned enumerator enumerates over IPs added with add_virtual_ip(). 
	 * @return				enumerator over host_t*
	 */
	enumerator_t* (*create_virtual_ip_enumerator)(peer_cfg_t *this);
	/**
	 * Add a pool name this configuration uses to select virtual IPs. 
	 * @param name			pool name to use for virtual IP lookup
	 */
	void (*add_pool)(peer_cfg_t *this, char *name);
	/**
	 * Create an enumerator over pool names of this config. 
	 * @return				enumerator over char*
	 */
	enumerator_t* (*create_pool_enumerator)(peer_cfg_t *this);
	/**
	 * Get the PPK ID to use with this peer. 
	 * @return				PPK id
	 */
	identification_t *(*get_ppk_id)(peer_cfg_t *this);
	/**
	 * Whether a PPK is required with this peer. 
	 * @return				TRUE, if a PPK is required
	 */
	bool (*ppk_required)(peer_cfg_t *this);
#ifdef ME
	/**
	 * Is this a mediation connection? 
	 * @return				TRUE, if this is a mediation connection
	 */
	bool (*is_mediation)(peer_cfg_t *this);
	/**
	 * Get name of the connection this one is mediated through. 
	 * @return				the name of the mediation connection
	 */
	char* (*get_mediated_by)(peer_cfg_t *this);
	/**
	 * Get the id of the other peer at the mediation server. 
	 * This is the leftid of the peer's connection with the mediation server. 
	 * If it is not configured, it is assumed to be the same as the right id
	 * of this connection. 
	 * @return				the id of the other peer
	 */
	identification_t* (*get_peer_id)(peer_cfg_t *this);
#endif /* ME */
	/**
	 * Check if two peer configurations are equal. 
	 * This method does not compare associated ike/child_cfg. 
	 * @param other			candidate to check for equality against this
	 * @return				TRUE if peer_cfg and ike_cfg are equal
	 */
	bool (*equals)(peer_cfg_t *this, peer_cfg_t *other);
	/**
	 * Increase reference count. 
	 * @return				reference to this
	 */
	peer_cfg_t* (*get_ref) (peer_cfg_t *this);
	/**
	 * Destroys the peer_cfg object. 
	 * Decrements the internal reference counter and
	 * destroys the peer_cfg when it reaches zero.
	 */
	void (*destroy) (peer_cfg_t *this);
};

/**
 * Private data of an peer_cfg_t object
 */
struct private_peer_cfg_t {
	/**
	 * Public part
	 */
	peer_cfg_t public;
	/**
	 * Number of references hold by others to this peer_cfg
	 */
	refcount_t refcount;
	/**
	 * Name of the peer_cfg, used to query it
	 */
	char *name;
	/**
	 * IKE config associated to this peer config
	 */
	ike_cfg_t *ike_cfg;
	/**
	 * list of child configs associated to this peer config
	 */
	linked_list_t *child_cfgs;
	/**
	 * lock to access list of child_cfgs
	 */
	rwlock_t *lock;
	/**
	 * should we send a certificate
	 */
	cert_policy_t cert_policy;
	/**
	 * uniqueness of an IKE_SA
	 */
	unique_policy_t unique;
	/**
	 * number of tries after giving up if peer does not respond
	 */
	uint32_t keyingtries;
	/**
	 * enable support for MOBIKE
	 */
	bool use_mobike;
	/**
	 * Use aggressive mode?
	 */
	bool aggressive;
	/**
	 * Use pull or push in mode config?
	 */
	bool pull_mode;
	/**
	 * Time before starting rekeying
	 */
	uint32_t rekey_time;
	/**
	 * Time before starting reauthentication
	 */
	uint32_t reauth_time;
	/**
	 * Time, which specifies the range of a random value subtracted from above.
	 */
	uint32_t jitter_time;
	/**
	 * Delay before deleting a rekeying/reauthenticating SA
	 */
	uint32_t over_time;
	/**
	 * DPD check interval
	 */
	uint32_t dpd;
	/**
	 * DPD timeout interval (used for IKEv1 only)
	 */
	uint32_t dpd_timeout;
	/**
	 * List of virtual IPs (host_t*) to request
	 */
	linked_list_t *vips;
	/**
	 * List of pool names to use for virtual IP lookup
	 */
	linked_list_t *pools;
	/**
	 * local authentication configs (rulesets)
	 */
	linked_list_t *local_auth;
	/**
	 * remote authentication configs (constraints)
	 */
	linked_list_t *remote_auth;
	/**
	 * PPK ID
	 */
	identification_t *ppk_id;
	/**
	 * Whether a PPK is required
	 */
	bool ppk_required;
#ifdef ME
	/**
	 * Is this a mediation connection?
	 */
	bool mediation;
	/**
	 * Name of the mediation connection to mediate through
	 */
	char *mediated_by;
	/**
	 * ID of our peer at the mediation server (= leftid of the peer's conn with
	 * the mediation server)
	 */
	identification_t *peer_id;
#endif /* ME */
};