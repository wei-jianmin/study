/**
 * Manage policies to create SAs from traffic. 为从流量创建 SA 管理策略
 */
struct trap_manager_t {

	/**
	 * Install a policy as a trap.
	 *
	 * @param peer		peer configuration to initiate on trap
	 * @param child 	child configuration to install as a trap
	 * @return			TRUE if successfully installed
	 */
	bool (*install)(trap_manager_t *this, peer_cfg_t *peer, child_cfg_t *child);

	/**
	 * Uninstall a trap policy.
	 *
	 * If no peer configuration name is given the first matching child
	 * configuration is uninstalled.
	 *
	 * @param peer		peer configuration name or NULL
	 * @param child		child configuration name
	 * @return			TRUE if uninstalled successfully
	 */
	bool (*uninstall)(trap_manager_t *this, char *peer, char *child);

	/**
	 * Create an enumerator over all installed traps.
	 *
	 * @return			enumerator over (peer_cfg_t, child_sa_t)
	 */
	enumerator_t* (*create_enumerator)(trap_manager_t *this);

	/**
	 * Acquire an SA triggered by an installed trap.
	 *
	 * @param reqid		requid of the triggering CHILD_SA
	 * @param src		source of the triggering packet
	 * @param dst		destination of the triggering packet
	 */
	void (*acquire)(trap_manager_t *this, uint32_t reqid,
					traffic_selector_t *src, traffic_selector_t *dst);

	/**
	 * Clear any installed trap.
	 */
	void (*flush)(trap_manager_t *this);

	/**
	 * Destroy a trap_manager_t.
	 */
	void (*destroy)(trap_manager_t *this);
};

===================================================================

/**
 * Private data of an trap_manager_t object.
 */
struct private_trap_manager_t {

	/**
	 * Public trap_manager_t interface.
	 */
	trap_manager_t public;

	/**
	 * Installed traps, as entry_t
	 */
	linked_list_t *traps;

	/**
	 * read write lock for traps list
	 */
	rwlock_t *lock;

	/**
	 * listener to track acquiring IKE_SAs
	 */
	trap_listener_t listener;

	/**
	 * list of acquires we currently handle
	 */
	linked_list_t *acquires;

	/**
	 * mutex for list of acquires
	 */
	mutex_t *mutex;

	/**
	 * number of threads currently installing trap policies, or INSTALL_DISABLED
	 */
	u_int installing;

	/**
	 * condvar to signal trap policy installation
	 */
	rwlock_condvar_t *condvar;

	/**
	 * Whether to ignore traffic selectors from acquires
	 */
	bool ignore_acquire_ts;
};

/**
 * listener to track acquires 跟踪获取的监听者
 */
struct trap_listener_t {

	/**
	 * Implements listener interface
	 */
	listener_t listener;

	/**
	 * points to trap_manager
	 */
	private_trap_manager_t *traps;
};

/**
 * A installed trap entry
 */
typedef struct {
	/** name of the trapped CHILD_SA */
	char *name;
	/** ref to peer_cfg to initiate */
	peer_cfg_t *peer_cfg;
	/** ref to instantiated CHILD_SA (i.e the trap policy) */
	child_sa_t *child_sa;
	/** TRUE in case of wildcard Transport Mode SA */
	bool wildcard;
} entry_t;

/**
 * A handled acquire
 */
typedef struct {
	/** pending IKE_SA connecting upon acquire */
	ike_sa_t *ike_sa;
	/** reqid of pending trap policy */
	uint32_t reqid;
	/** destination address (wildcard case) */
	host_t *dst;
} acquire_t;