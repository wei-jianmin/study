/**
 * Manage PASS and DROP shunt£¨·ÖÁ÷£© policy excepting traffic from IPsec SAs.
 */
struct shunt_manager_t {

	/**
	 * Install a policy as a shunt.
	 *
	 * @param ns		namespace (e.g. name of a connection or plugin), cloned
	 * @param child		child configuration to install as a shunt
	 * @return			TRUE if installed successfully
	 */
	bool (*install)(shunt_manager_t *this, char *ns, child_cfg_t *child);

	/**
	 * Uninstall a shunt policy.
	 *
	 * If no namespace is given the first matching child configuration is
	 * removed.
	 *
	 * @param ns		namespace (same as given during installation) or NULL
	 * @param name	 	name of child configuration to uninstall as a shunt
	 * @return			TRUE if uninstalled successfully
	 */
	bool (*uninstall)(shunt_manager_t *this, char *ns, char *name);

	/**
	 * Create an enumerator over all installed shunts.
	 *
	 * @return			enumerator over (char*, child_cfg_t*)
	 */
	enumerator_t* (*create_enumerator)(shunt_manager_t *this);

	/**
	 * Clear any installed shunt.
	 */
	void (*flush)(shunt_manager_t *this);

	/**
	 * Destroy a shunt_manager_t.
	 */
	void (*destroy)(shunt_manager_t *this);
};
};
};
};

==========================================================

/**
 * Private data of an shunt_manager_t object.
 */
struct private_shunt_manager_t {

	/**
	 * Public shunt_manager_t interface.
	 */
	shunt_manager_t public;

	/**
	 * Installed shunts, as entry_t
	 */
	linked_list_t *shunts;

	/**
	 * Lock to safely access the list of shunts
	 */
	rwlock_t *lock;

	/**
	 * Number of threads currently installing shunts, or INSTALL_DISABLED
	 */
	u_int installing;

	/**
	 * Condvar to signal shunt installation
	 */
	rwlock_condvar_t *condvar;
};

/**
 * Config entry for a shunt
 */
typedef struct {
	/**
	 * Configured namespace
	 */
	char *ns;

	/**
	 * Child config
	 */
	child_cfg_t *cfg;  //child_cfg.h

} entry_t;