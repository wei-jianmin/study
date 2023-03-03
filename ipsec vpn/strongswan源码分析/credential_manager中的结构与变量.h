#使用集合结构，管理证书、共享key、私有key、公钥key、信任证书，
#提供枚举器进行检索

/**
 * Type of a credential hook error/event.
 */
enum credential_hook_type_t {
	/** The certificate has expired (or is not yet valid) */
	CRED_HOOK_EXPIRED,
	/** The certificate has been revoked */
	CRED_HOOK_REVOKED,
	/** Checking certificate revocation failed. This does not necessarily mean
	 *  the certificate is rejected, just that revocation checking failed. */
	CRED_HOOK_VALIDATION_FAILED,
	/** No trusted issuer certificate has been found for this certificate */
	CRED_HOOK_NO_ISSUER,
	/** Encountered a self-signed (root) certificate, but it is not trusted */
	CRED_HOOK_UNTRUSTED_ROOT,
	/** Maximum trust chain length exceeded for certificate */
	CRED_HOOK_EXCEEDED_PATH_LEN,
	/** The certificate violates some other kind of policy and gets rejected */
	CRED_HOOK_POLICY_VIOLATION,
};

/**
 * Manages credentials using credential_sets.
 *
 * 凭证管理器是凭证框架的入口点。 它使用所谓的“集合”以模块化方式访问凭证。 
 * 这些是通过 credential_set_t 接口实现的。
 * 管理器还进行信任链验证和信任状态缓存。 
 * 如果集合本身需要凭据，则可以调用管理器方法。
 * 该管理器使用迭代锁.
 *
 * @verbatim

  +-------+        +----------------+
  |   A   |        |                |          +------------------+
  |   u   | -----> |                | ------>  |  +------------------+
  |   t   |        |   credential-  |          |  |  +------------------+
  |   h   | -----> |     manager    | ------>  +--|  |   credential-    | => IPC
  |   e   |        |                |             +--|       sets       |
  |   n   |   +--> |                | ------>        +------------------+
  |   t   |   |    |                |                        |
  |   i   |   |    |                |                        |
  |   c   |   |    +----------------+                        |
  |   a   |   |                                              |
  |   t   |   +----------------------------------------------+
  |   o   |                    may be recursive
  |   r   |
  +-------+

   @endverbatim
 *
 * The credential manager uses rwlocks for performance reasons. Credential
 * sets must be fully thread-safe.
 */
struct credential_manager_t {

	/**
	 * Create an enumerator over all certificates.
	 *
	 * @param cert		kind of certificate
	 * @param key		kind of key in certificate
	 * @param id		subject this certificate belongs to
	 * @param trusted	TRUE to list trusted certificates only
	 * @return			enumerator over the certificates
	 */
	enumerator_t *(*create_cert_enumerator)(credential_manager_t *this,
								certificate_type_t cert, key_type_t key,
								identification_t *id, bool trusted);
	/**
	 * Create an enumerator over all shared keys.
	 *
	 * The enumerator enumerates over:
	 *  shared_key_t*, id_match_t me, id_match_t other
	 * But must accept values for the id_matches.
	 *
	 * @param type		kind of requested shared key
	 * @param first		first subject between key is shared
	 * @param second	second subject between key is shared
	 * @return			enumerator over (shared_key_t*,id_match_t,id_match_t)
	 */
	enumerator_t *(*create_shared_enumerator)(credential_manager_t *this,
								shared_key_type_t type,
								identification_t *first, identification_t *second);
	/**
	 * Create an enumerator over all Certificate Distribution Points.
	 *
	 * @param type		kind of certificate the point distributes
	 * @param id		identification of the distributed certificate
	 * @return			enumerator of CDPs as char*
	 */
	enumerator_t *(*create_cdp_enumerator)(credential_manager_t *this,
								certificate_type_t type, identification_t *id);
	/**
	 * Get a trusted or untrusted certificate.
	 *
	 * @param cert		kind of certificate
	 * @param key		kind of key in certificate
	 * @param id		subject this certificate belongs to
	 * @param trusted	TRUE to get a trusted certificate only
	 * @return			certificate, if found, NULL otherwise
	 */
	certificate_t *(*get_cert)(credential_manager_t *this,
							   certificate_type_t cert, key_type_t key,
							   identification_t *id, bool trusted);
	/**
	 * Get the best matching shared key for two IDs.
	 *
	 * @param type		kind of requested shared key
	 * @param me		own identity
	 * @param other		peer identity
	 * @return			shared_key_t, NULL if none found
	 */
	shared_key_t *(*get_shared)(credential_manager_t *this, shared_key_type_t type,
								identification_t *me, identification_t *other);
	/**
	 * Get a private key to create a signature.
	 *
	 * The get_private() method gets a secret private key identified by either
	 * the keyid itself or an id the key belongs to.
	 * The auth parameter contains additional information, such as recipients
	 * trusted CA certs. Auth gets filled with subject and CA certificates
	 * needed to validate a created signature.
	 *
	 * @param type		type of the key to get
	 * @param id		identification the key belongs to
	 * @param auth		auth config, including trusted CA certificates
	 * @return			private_key_t, NULL if none found
	 */
	private_key_t* (*get_private)(credential_manager_t *this, key_type_t type,
								  identification_t *id, auth_cfg_t *auth);

	/**
	 * Create an enumerator over trusted certificates.
	 *
	 * This method creates an enumerator over trusted certificates. The auth
	 * parameter (if given) receives the trustchain used to validate
	 * the certificate. The resulting enumerator enumerates over
	 * certificate_t*, auth_cfg_t*.
	 * If online is set, revocations are checked online for the whole
	 * trustchain.
	 *
	 * @param type		type of the key we want a certificate for
	 * @param id		subject of the certificate
	 * @param online	whether revocations should be checked online
	 * @return			enumerator
	 */
	enumerator_t* (*create_trusted_enumerator)(credential_manager_t *this,
					key_type_t type, identification_t *id, bool online);

	/**
	 * Create an enumerator over trusted public keys.
	 *
	 * This method creates an enumerator over trusted public keys to verify a
	 * signature created by id. The auth parameter contains additional
	 * authentication infos, e.g. peer and intermediate certificates.
	 * The resulting enumerator enumerates over public_key_t *, auth_cfg_t *,
	 * where the auth config helper contains rules for constraint checks.
	 * This function is very similar to create_trusted_enumerator(), but
	 * gets public keys directly.
	 * If online is set, revocations are checked online for the whole
	 * trustchain.
	 *
	 * @param type		type of the key to get
	 * @param id		owner of the key, signer of the signature
	 * @param auth		authentication infos
	 * @param online	whether revocations should be checked online
	 * @return			enumerator
	 */
	enumerator_t* (*create_public_enumerator)(credential_manager_t *this,
					key_type_t type, identification_t *id, auth_cfg_t *auth,
					bool online);

	/**
	 * Cache a certificate by invoking cache_cert() on all registered sets.
	 *
	 * @param cert		certificate to cache
	 */
	void (*cache_cert)(credential_manager_t *this, certificate_t *cert);

	/**
	 * Flush the certificate cache.
	 *
	 * Only the managers local cache is flushed, but not the sets cache filled
	 * by the cache_cert() method.
	 *
	 * @param type		type of certificate to flush, or CERT_ANY
	 */
	void (*flush_cache)(credential_manager_t *this, certificate_type_t type);

	/**
	 * Check if a given subject certificate is issued by an issuer certificate.
	 *
	 * This operation does signature verification using the credential
	 * manager's cache to speed up the operation.
	 *
	 * @param subject	subject certificate to check
	 * @param issuer	issuer certificate that potentially has signed subject
	 * @param scheme	receives used signature scheme and parameters, if
	 *					given (allocated)
	 * @return			TRUE if issuer signed subject
	 */
	bool (*issued_by)(credential_manager_t *this,
					  certificate_t *subject, certificate_t *issuer,
					  signature_params_t **scheme);

	/**
	 * Register a credential set to the manager.
	 *
	 * @param set		set to register
	 */
	void (*add_set)(credential_manager_t *this, credential_set_t *set);

	/**
	 * Unregister a credential set from the manager.
	 *
	 * @param set		set to unregister
	 */
	void (*remove_set)(credential_manager_t *this, credential_set_t *set);

	/**
	 * Register a thread local credential set to the manager.
	 *
	 * To add a credential set for the current trustchain verification
	 * operation, sets may be added for the calling thread only. This
	 * does not require a write lock and is therefore a much cheaper
	 * operation.
	 * The exclusive option allows to disable all other credential sets
	 * until the set is deregistered.
	 *
	 * @param set		set to register
	 * @param exclusive	TRUE to disable all other sets for this thread
	 */
	void (*add_local_set)(credential_manager_t *this, credential_set_t *set,
						  bool exclusive);

	/**
	 * Unregister a thread local credential set from the manager.
	 *
	 * @param set		set to unregister
	 */
	void (*remove_local_set)(credential_manager_t *this, credential_set_t *set);

	/**
	 * Register a certificate validator to the manager.
	 *
	 * @param vdtr		validator to register
	 */
	void (*add_validator)(credential_manager_t *this, cert_validator_t *vdtr);

	/**
	 * Remove a certificate validator from the manager.
	 *
	 * @param vdtr		validator to unregister
	 */
	void (*remove_validator)(credential_manager_t *this, cert_validator_t *vdtr);

	/**
	 * Set a hook to call on certain credential validation errors.
	 *
	 * @param hook		hook to register, NULL to unregister
	 * @param data		data to pass to hook
	 */
	void (*set_hook)(credential_manager_t *this, credential_hook_t hook,
					 void *data);

	/**
	 * Call the registered credential hook, if any.
	 *
	 * While hooks are usually called by the credential manager itself, some
	 * validator plugins might raise hooks as well if they consider certificates
	 * invalid.
	 *
	 * @param type		type of the event
	 * @param cert		associated certificate
	 */
	void (*call_hook)(credential_manager_t *this, credential_hook_type_t type,
					  certificate_t *cert);

	/**
	 * Destroy a credential_manager instance.
	 */
	void (*destroy)(credential_manager_t *this);
};

================================================================

/**
 * private data of credential_manager
 */
struct private_credential_manager_t {

	/**
	 * public functions
	 */
	credential_manager_t public;

	/**
	 * list of credential sets
	 */
	linked_list_t *sets;

	/**
	 * thread local set of credentials, linked_list_t with credential_set_t's
	 */
	thread_value_t *local_sets;

	/**
	 * Exclusive local sets, linked_list_t with credential_set_t
	 */
	thread_value_t *exclusive_local_sets;

	/**
	 * trust relationship and certificate cache
	 */
	cert_cache_t *cache;

	/**
	 * certificates queued for persistent caching
	 */
	linked_list_t *cache_queue;

	/**
	 * list of certificate validators, cert_validator_t
	 */
	linked_list_t *validators;

	/**
	 * read-write lock to sets list
	 */
	rwlock_t *lock;

	/**
	 * mutex for cache queue
	 */
	mutex_t *queue_mutex;

	/**
	 * Registered hook to call on validation errors
	 */
	credential_hook_t hook;

	/**
	 * Registered data to pass to hook
	 */
	void *hook_data;
};

/** data to pass to create_private_enumerator */
typedef struct {
	private_credential_manager_t *this;
	key_type_t type;
	identification_t* keyid;
} private_data_t;

/** data to pass to create_cert_enumerator */
typedef struct {
	private_credential_manager_t *this;
	certificate_type_t cert;
	key_type_t key;
	identification_t *id;
	bool trusted;
} cert_data_t;

/** data to pass to create_cdp_enumerator */
typedef struct {
	private_credential_manager_t *this;
	certificate_type_t type;
	identification_t *id;
} cdp_data_t;

/** data to pass to create_shared_enumerator */
typedef struct {
	private_credential_manager_t *this;
	shared_key_type_t type;
	identification_t *me;
	identification_t *other;
} shared_data_t;

/** enumerator over local and global sets */
typedef struct {
	/** implements enumerator_t */
	enumerator_t public;
	/** enumerator over global sets */
	enumerator_t *global;
	/** enumerator over local sets */
	enumerator_t *local;
	/** enumerator over exclusive local sets */
	enumerator_t *exclusive;
} sets_enumerator_t;

/**
 * enumerator for trusted certificates
 */
typedef struct {
	/** implements enumerator_t interface */
	enumerator_t public;
	/** enumerator over candidate peer certificates */
	enumerator_t *candidates;
	/** reference to the credential_manager */
	private_credential_manager_t *this;
	/** type of the requested key */
	key_type_t type;
	/** identity the requested key belongs to */
	identification_t *id;
	/** TRUE to do CRL/OCSP checking */
	bool online;
	/** pretrusted certificate we have served at first invocation */
	certificate_t *pretrusted;
	/** currently enumerating auth config */
	auth_cfg_t *auth;
	/** list of failed candidates */
	linked_list_t *failed;
} trusted_enumerator_t;

/**
 * enumerator for public keys
 */
typedef struct {
	/** implements enumerator_t interface */
	enumerator_t public;
	/** enumerator over candidate peer certificates */
	enumerator_t *inner;
	/** reference to the credential_manager */
	private_credential_manager_t *this;
	/** currently enumerating key */
	public_key_t *current;
	/** credset wrapper around auth config */
	auth_cfg_wrapper_t *wrapper;
} public_enumerator_t;
