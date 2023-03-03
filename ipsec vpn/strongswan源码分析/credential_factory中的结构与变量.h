/**
 * Kind of credential（凭据）.
 * 
 * 尽管密码容器不是真正可信的，但我们仍用凭据工厂来创建他们
 * While crypto containers are not really credentials, we still use the
 * credential factory and builders create them.
 */
enum credential_type_t {
	/** private key, implemented in private_key_t */
	CRED_PRIVATE_KEY,
	/** public key, implemented in public_key_t */
	CRED_PUBLIC_KEY,
	/** certificates, implemented in certificate_t */
	CRED_CERTIFICATE,
	/** crypto container, implemented in container_t */
	CRED_CONTAINER,
};

/**
 * Manages credential construction functions and creates instances.
 */
struct credential_factory_t {

	/**
	 * 创建凭据
	 * Create a credential using a list of builder_part_t's.
	 *
	 * The variable argument list takes builder_part_t types followed
	 * by the type specific value. The list must be terminated using BUILD_END.
	 * All passed parts get cloned/refcounted by the builder functions,
	 * so free up allocated resources after successful and unsuccessful
	 * invocations.
	 *
	 * @param type			credential type to build
	 * @param subtype		subtype specific for type of the credential
	 * @param ...			build_part_t arguments, BUILD_END terminated.
	 * @return				type specific credential, NULL if failed
	 */
	void* (*create)(credential_factory_t *this, credential_type_t type,
					int subtype, ...);

	/**
	 * Register a credential builder function.
	 *
	 * The final flag indicates if the registered builder can build such
	 * a credential itself the most common encoding, without the need
	 * for an additional builder.
	 *
	 * @param type			type of credential the builder creates
	 * @param subtype		subtype of the credential, type specific
	 * @param final			TRUE if this build does not invoke other builders
	 * @param constructor	builder constructor function to register
	 */
	void (*add_builder)(credential_factory_t *this,
						credential_type_t type, int subtype, bool final,
						builder_function_t constructor);
	/**
	 * Unregister a credential builder function.
	 *
	 * @param constructor	constructor function to unregister.
	 */
	void (*remove_builder)(credential_factory_t *this,
						   builder_function_t constructor);

	/**
	 * Create an enumerator over registered builder types.
	 *
	 * The enumerator returns only builder types registered with the final
	 * flag set.
	 *
	 * @return				enumerator (credential_type_t, int subtype)
	 */
	enumerator_t* (*create_builder_enumerator)(credential_factory_t *this);

	/**
	 * Destroy a credential_factory instance.
	 */
	void (*destroy)(credential_factory_t *this);
};

============================================================

/**
 * private data of credential_factory
 */
struct private_credential_factory_t {

	/**
	 * public functions
	 */
	credential_factory_t public;

	/**
	 * list with entry_t
	 */
	linked_list_t *constructors;

	/**
	 * Thread specific recursiveness counter
	 */
	thread_value_t *recursive;

	/**
	 * lock access to builders
	 */
	rwlock_t *lock;
};

struct entry_t {
	/** kind of credential builder */
	credential_type_t type;
	/** subtype of credential, e.g. certificate_type_t */
	int subtype;
	/** registered with final flag? */
	bool final;
	/** builder function */
	builder_function_t constructor;
};