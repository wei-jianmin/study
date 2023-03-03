/**
 * A loader and multiplexer（多路复用器） to use multiple backends.
 *
 * Charon 允许同时使用多个配置后端
 * Charon allows the use of multiple configuration backends simultaneously. To
 * access all this backends by a single call, this class wraps multiple
 * backends behind a single object.
 * 各个backend执行配置文件的实际查找工作,像如vici、stroke、uci等，都是不同的backend
 * @verbatim

   +---------+      +-----------+         +--------------+     |
   |         |      |           |       +--------------+ |     |
   | daemon  |----->| backend_- |     +--------------+ |-+  <==|==> IPC
   |  core   |      | manager   |---->|   backends   |-+       |
   |         |----->|           |     +--------------+         |
   |         |      |           |                              |
   +---------+      +-----------+                              |

   @endverbatim
 */
struct backend_manager_t {

	/**
	 * Get an ike_config identified by two hosts.
	 *
	 * @param my_host			address of own host
	 * @param other_host		address of remote host
	 * @param version			IKE version to get a config for
	 * @return					matching ike_config, or NULL if none found
	 */
	ike_cfg_t* (*get_ike_cfg)(backend_manager_t *this,
							  host_t *my_host, host_t *other_host,
							  ike_version_t version);

	/**
	 * Create an enumerator over all matching IKE configs.
	 *
	 * Pass NULL as parameters to match any. The enumerator enumerates over
	 * ike_cfgs, ordered by priority (best match first).
	 *
	 * @param me				local address
	 * @param other				remote address
	 * @param version			IKE version to get a config for
	 * @return 					enumerator over ike_cfg
	 */
	enumerator_t* (*create_ike_cfg_enumerator)(backend_manager_t *this,
							host_t *me, host_t *other, ike_version_t version);

	/**
	 * Get a peer_config identified by it's name.
	 *
	 * @param name				name of the peer_config
	 * @return					matching peer_config, or NULL if none found
	 */
	peer_cfg_t* (*get_peer_cfg_by_name)(backend_manager_t *this, char *name);

	/**
	 * Create an enumerator over all matching peer configs.
	 *
	 * Pass NULL as parameters to match any. The enumerator enumerates over
	 * peer_cfgs, ordered by priority (best match first).
	 *
	 * @param me				local address
	 * @param other				remote address
	 * @param my_id				IDr in first authentication round
	 * @param other_id			IDi in first authentication round
	 * @param version			IKE version to get a config for
	 * @return 					enumerator over peer_cfg_t
	 */
	enumerator_t* (*create_peer_cfg_enumerator)(backend_manager_t *this,
							host_t *me, host_t *other, identification_t *my_id,
							identification_t *other_id, ike_version_t version);
	/**
	 * Register a backend on the manager.
	 *
	 * @param backend			backend to register
	 */
	void (*add_backend)(backend_manager_t *this, backend_t *backend);

	/**
	 * Unregister a backend.
	 *
	 * @param backend			backend to unregister
	 */
	void (*remove_backend)(backend_manager_t *this, backend_t *backend);

	/**
	 * Destroys a backend_manager_t object.
	 */
	void (*destroy) (backend_manager_t *this);
};

===========================================================

/**
 * match of an ike_cfg
 */
typedef enum ike_cfg_match_t {
	/* doesn't match at all */
	MATCH_NONE		= 0x00,
	/* match for a %any host. For both hosts, hence skip 0x02 */
	MATCH_ANY		= 0x01,
	/* IKE version matches exactly (config is not for any version) */
	MATCH_VERSION	= 0x04,
	/* local identity matches */
	MATCH_ME		= 0x08,
	/* remote identity matches */
	MATCH_OTHER		= 0x10,
} ike_cfg_match_t;

/**
 * Private data of an backend_manager_t object.
 */
struct private_backend_manager_t {

	/**
	 * Public part of backend_manager_t object.
	 */
	backend_manager_t public;

	/**
	 * list of registered backends
	 */
	linked_list_t *backends;

	/**
	 * rwlock for backends
	 */
	rwlock_t *lock;
};

/**
 * match of an ike_cfg
 */
typedef enum ike_cfg_match_t {
	/* doesn't match at all */
	MATCH_NONE		= 0x00,
	/* match for a %any host. For both hosts, hence skip 0x02 */
	MATCH_ANY		= 0x01,
	/* IKE version matches exactly (config is not for any version) */
	MATCH_VERSION	= 0x04,
	/* local identity matches */
	MATCH_ME		= 0x08,
	/* remote identity matches */
	MATCH_OTHER		= 0x10,
} ike_cfg_match_t;

/**
 * data to pass nested IKE enumerator
 */
typedef struct {
	private_backend_manager_t *this;
	host_t *me;
	host_t *other;
} ike_data_t;

/**
 * list element to help sorting
 */
typedef struct {
	ike_cfg_match_t match;
	ike_cfg_t *cfg;
} ike_match_entry_t;

/**
 * data to pass nested peer enumerator
 */
typedef struct {
	rwlock_t *lock;
	identification_t *me;
	identification_t *other;
} peer_data_t;

/**
 * list element to help sorting
 */
typedef struct {
	id_match_t match_peer;
	ike_cfg_match_t match_ike;
	peer_cfg_t *cfg;
} match_entry_t;