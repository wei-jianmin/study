/**
 * POSIX capability dropping abstraction layer.
 * POSIX capabilities 允许为进程细化权限
 * 除了标准的UNIX权限方案之外，它们为系统资源定义了新的一组权限
 * 参：https://www.cnblogs.com/sky-heaven/p/9481508.html
 */
struct capabilities_t {

	/**
	 * 保持一个权能（当调用drop()后仍会保持）
	 * Register a capability to keep while calling drop(). Verifies that the
	 * capability is currently held.
	 *
	 * @note CAP_CHOWN is handled specially as it might not be required.
	 *
	 * @param cap		capability to keep
	 * @return			FALSE if the capability is currently not held
	 */
	bool (*keep)(capabilities_t *this,
				 u_int cap) __attribute__((warn_unused_result));

	/**
	 * Check if the given capability is currently held.
	 *
	 * @note CAP_CHOWN is handled specially as it might not be required.
	 *
	 * @param cap		capability to check
	 * @return			TRUE if the capability is currently held
	 */
	bool (*check)(capabilities_t *this, u_int cap);

	/**
	 * Get the user ID set through set_uid/resolve_uid.
	 *
	 * @return			currently set user ID
	 */
	uid_t (*get_uid)(capabilities_t *this);

	/**
	 * Get the group ID set through set_gid/resolve_gid.
	 *
	 * @return			currently set group ID
	 */
	gid_t (*get_gid)(capabilities_t *this);

	/**
	 * Set the numerical user ID to use during rights dropping.
	 *
	 * @param uid		user ID to use
	 */
	void (*set_uid)(capabilities_t *this, uid_t uid);

	/**
	 * Set the numerical group ID to use during rights dropping.
	 *
	 * @param gid		group ID to use
	 */
	void (*set_gid)(capabilities_t *this, gid_t gid);

	/**
	 * Resolve a username and set the user ID accordingly.
	 *
	 * @param username	username get the uid for
	 * @return			TRUE if username resolved and uid set
	 */
	bool (*resolve_uid)(capabilities_t *this, char *username);

	/**
	 * Resolve a groupname and set the group ID accordingly.
	 *
	 * @param groupname	groupname to get the gid for
	 * @return			TRUE if groupname resolved and gid set
	 */
	bool (*resolve_gid)(capabilities_t *this, char *groupname);

	/**
	 * 丢弃之间没有通过keep方法保持的功能
	 * Drop all capabilities not previously passed to keep(), switch to UID/GID.
	 *
	 * @return			TRUE if capability drop successful
	 */
	bool (*drop)(capabilities_t *this);

	/**
	 * Destroy a capabilities_t.
	 */
	void (*destroy)(capabilities_t *this);
};

========================================================

/**
 * Private data of an capabilities_t object.
 */
struct private_capabilities_t {

	/**
	 * Public capabilities_t interface.
	 */
	capabilities_t public;

	/**
	 * user ID to switch during rights dropping
	 */
	uid_t uid;

	/**
	 * group ID to switch during rights dropping
	 */
	gid_t gid;

	/**
	 * capabilities to keep
	 */
#ifdef CAPABILITIES_LIBCAP
	cap_t caps;
#endif /* CAPABILITIES_LIBCAP */
#ifdef CAPABILITIES_NATIVE
	struct __user_cap_data_struct caps[2];  ///usr/include/linux/capability.h
#endif /* CAPABILITIES_NATIVE */

#ifdef EMULATE_R_FUNCS
	/**
	 * mutex to emulate get(pw|gr)nam_r functions
	 */
	mutex_t *mutex;
#endif
};


