/**
 * Handles crypto modules and creates instances.
 */
struct crypto_factory_t {

	/**
	 * Create a crypter instance.
	 *
	 * @param algo			encryption algorithm
	 * @param key_size		length of the key in bytes
	 * @return				crypter_t instance, NULL if not supported
	 */
	crypter_t* (*create_crypter)(crypto_factory_t *this,
								 encryption_algorithm_t algo, size_t key_size);

	/**
	 * Create a aead instance.
	 * aead : Authenticated Encryption with Associated Data
	 *        带有关联数据的经过身份验证的加密
     *        可以验证解密密钥是否正确的一种对称加密算法
	 *
	 * @param algo			encryption algorithm
	 * @param key_size		length of the key in bytes
	 * @param salt_size		size of salt, implicit part of the nonce
	 * @return				aead_t instance, NULL if not supported
	 */
	aead_t* (*create_aead)(crypto_factory_t *this,
						   encryption_algorithm_t algo,
						   size_t key_size, size_t salt_size);

	/**
	 * Create a symmetric signer instance.
	 *
	 * @param algo			MAC algorithm to use
	 * @return				signer_t instance, NULL if not supported
	 */
	signer_t* (*create_signer)(crypto_factory_t *this,
							   integrity_algorithm_t algo);

	/**
	 * Create a hasher instance.
	 *
	 * @param algo			hash algorithm
	 * @return				hasher_t instance, NULL if not supported
	 */
	hasher_t* (*create_hasher)(crypto_factory_t *this, hash_algorithm_t algo);

	/**
	 * Create a pseudo random function instance.
	 *
	 * @param algo			PRF(伪随机数) algorithm to use
	 * @return				prf_t instance, NULL if not supported
	 */
	prf_t* (*create_prf)(crypto_factory_t *this, pseudo_random_function_t algo);

	/**
	 * Create an extended output function instance.
	 *
	 * @param algo			XOF algorithm to use
	 *                      XOF : ?--扩展SHA3，其输出的哈希值可以使任意指定长度
	 * @return				xof_t instance, NULL if not supported
	 */
	xof_t* (*create_xof)(crypto_factory_t *this, ext_out_function_t algo);

	/**
	 * Create a source of randomness.
	 *
	 * @param quality		required randomness quality  
	 *                      rng : 随机数发生器
	 * @return				rng_t instance, NULL if no RNG with such a quality
	 */
	rng_t* (*create_rng)(crypto_factory_t *this, rng_quality_t quality);

	/**
	 * Create a nonce generator(随机数发生器) instance.
	 *
	 * @return				nonce_gen_t instance, NULL if not supported
	 */
	nonce_gen_t* (*create_nonce_gen)(crypto_factory_t *this);

	/**
	 * Create a diffie hellman instance.
	 *
	 * Additional arguments are passed to the DH constructor.
	 *
	 * @param group			diffie hellman group
	 * @return				diffie_hellman_t instance, NULL if not supported
	 */
	diffie_hellman_t* (*create_dh)(crypto_factory_t *this,
								   diffie_hellman_group_t group, ...);

	/**
	 * Register a crypter constructor.
	 *
	 * @param algo			algorithm to constructor
	 * @param key size		key size to perform benchmarking for
	 * @param plugin_name	plugin that registered this algorithm
	 * @param create		constructor function for that algorithm
	 * @return				TRUE if registered, FALSE if test vector failed
	 */
	bool (*add_crypter)(crypto_factory_t *this, encryption_algorithm_t algo,
						size_t key_size, const char *plugin_name,
						crypter_constructor_t create);

	/**
	 * Unregister a crypter constructor.
	 *
	 * @param create		constructor function to unregister
	 */
	void (*remove_crypter)(crypto_factory_t *this, crypter_constructor_t create);

	/**
	 * Unregister a aead constructor.
	 *
	 * @param create		constructor function to unregister
	 */
	void (*remove_aead)(crypto_factory_t *this, aead_constructor_t create);

	/**
	 * Register a aead constructor.
	 *
	 * @param algo			algorithm to constructor
	 * @param key size		key size to perform benchmarking for
	 * @param plugin_name	plugin that registered this algorithm
	 * @param create		constructor function for that algorithm
	 * @return				TRUE if registered, FALSE if test vector failed
	 */
	bool (*add_aead)(crypto_factory_t *this, encryption_algorithm_t algo,
					 size_t key_size, const char *plugin_name,
					 aead_constructor_t create);

	/**
	 * Register a signer constructor.
	 *
	 * @param algo			algorithm to constructor
	 * @param plugin_name	plugin that registered this algorithm
	 * @param create		constructor function for that algorithm
	 * @return				TRUE if registered, FALSE if test vector failed
	 */
	bool (*add_signer)(crypto_factory_t *this, integrity_algorithm_t algo,
					    const char *plugin_name, signer_constructor_t create);

	/**
	 * Unregister a signer constructor.
	 *
	 * @param create		constructor function to unregister
	 */
	void (*remove_signer)(crypto_factory_t *this, signer_constructor_t create);

	/**
	 * Register a hasher constructor.
	 *
	 * @param algo			algorithm to constructor
	 * @param plugin_name	plugin that registered this algorithm
	 * @param create		constructor function for that algorithm
	 * @return				TRUE if registered, FALSE if test vector failed
	 */
	bool (*add_hasher)(crypto_factory_t *this, hash_algorithm_t algo,
					   const char *plugin_name, hasher_constructor_t create);

	/**
	 * Unregister a hasher constructor.
	 *
	 * @param create		constructor function to unregister
	 */
	void (*remove_hasher)(crypto_factory_t *this, hasher_constructor_t create);

	/**
	 * Register a prf constructor.
	 *
	 * @param algo			algorithm to constructor
	 * @param plugin_name	plugin that registered this algorithm
	 * @param create		constructor function for that algorithm
	 * @return				TRUE if registered, FALSE if test vector failed
	 */
	bool (*add_prf)(crypto_factory_t *this, pseudo_random_function_t algo,
					const char *plugin_name, prf_constructor_t create);

	/**
	 * Unregister a prf constructor.
	 *
	 * @param create		constructor function to unregister
	 */
	void (*remove_prf)(crypto_factory_t *this, prf_constructor_t create);

	/**
	 * Register an xof constructor.
	 *
	 * @param algo			algorithm to constructor
	 * @param plugin_name	plugin that registered this algorithm
	 * @param create		constructor function for that algorithm
	 * @return				TRUE if registered, FALSE if test vector failed
	 */
	bool (*add_xof)(crypto_factory_t *this, ext_out_function_t algo,
					const char *plugin_name, xof_constructor_t create);

	/**
	 * Unregister an xof constructor.
	 *
	 * @param create		constructor function to unregister
	 */
	void (*remove_xof)(crypto_factory_t *this, xof_constructor_t create);

	/**
	 * Register a source of randomness.
	 *
	 * @param quality		quality of randomness this RNG serves
	 * @param plugin_name	plugin that registered this algorithm
	 * @param create		constructor function for such a quality
	 * @return				TRUE if registered, FALSE if test vector failed
	 */
	bool (*add_rng)(crypto_factory_t *this, rng_quality_t quality,
					const char *plugin_name, rng_constructor_t create);

	/**
	 * Unregister a source of randomness.
	 *
	 * @param create		constructor function to unregister
	 */
	void (*remove_rng)(crypto_factory_t *this, rng_constructor_t create);

	/**
	 * Register a nonce generator.
	 *
	 * @param plugin_name	plugin that registered this algorithm
	 * @param create		constructor function for that nonce generator
	 * @return				TRUE if registered, FALSE if test vector failed
	 */
	bool (*add_nonce_gen)(crypto_factory_t *this, const char *plugin_name,
						  nonce_gen_constructor_t create);

	/**
	 * Unregister a nonce generator.
	 *
	 * @param create		constructor function to unregister
	 */
	void (*remove_nonce_gen)(crypto_factory_t *this,
							 nonce_gen_constructor_t create);

	/**
	 * Register a diffie hellman constructor.
	 *
	 * @param group			dh group to constructor
	 * @param plugin_name	plugin that registered this algorithm
	 * @param create		constructor function for that algorithm
	 * @return				TRUE if registered, FALSE if test vector failed
	 */
	bool (*add_dh)(crypto_factory_t *this, diffie_hellman_group_t group,
				   const char *plugin_name, dh_constructor_t create);

	/**
	 * Unregister a diffie hellman constructor.
	 *
	 * @param create		constructor function to unregister
	 */
	void (*remove_dh)(crypto_factory_t *this, dh_constructor_t create);

	/**
	 * Create an enumerator over all registered crypter algorithms.
	 *
	 * @return				enumerator over encryption_algorithm_t, plugin
	 */
	enumerator_t* (*create_crypter_enumerator)(crypto_factory_t *this);

	/**
	 * Create an enumerator over all registered aead algorithms.
	 *
	 * @return				enumerator over encryption_algorithm_t, plugin
	 */
	enumerator_t* (*create_aead_enumerator)(crypto_factory_t *this);

	/**
	 * Create an enumerator over all registered signer algorithms.
	 *
	 * @return				enumerator over integrity_algorithm_t, plugin
	 */
	enumerator_t* (*create_signer_enumerator)(crypto_factory_t *this);

	/**
	 * Create an enumerator over all registered hasher algorithms.
	 *
	 * @return				enumerator over hash_algorithm_t, plugin
	 */
	enumerator_t* (*create_hasher_enumerator)(crypto_factory_t *this);

	/**
	 * Create an enumerator over all registered PRFs.
	 *
	 * @return				enumerator over pseudo_random_function_t, plugin
	 */
	enumerator_t* (*create_prf_enumerator)(crypto_factory_t *this);

	/**
	 * Create an enumerator over all registered XOFs.
	 *
	 * @return				enumerator over ext_out_function_t, plugin
	 */
	enumerator_t* (*create_xof_enumerator)(crypto_factory_t *this);

	/**
	 * Create an enumerator over all registered diffie hellman groups.
	 *
	 * @return				enumerator over diffie_hellman_group_t, plugin
	 */
	enumerator_t* (*create_dh_enumerator)(crypto_factory_t *this);

	/**
	 * Create an enumerator over all registered random generators.
	 *
	 * @return				enumerator over rng_quality_t, plugin
	 */
	enumerator_t* (*create_rng_enumerator)(crypto_factory_t *this);

	/**
	 * Create an enumerator over all registered nonce generators.
	 *
	 * @return				enumerator over plugin
	 */
	enumerator_t* (*create_nonce_gen_enumerator)(crypto_factory_t *this);

	/**
	 * Add a test vector to the crypto factory.
	 *
	 * @param type			type of the test vector
	 * @param vector		pointer to a test vector, defined in crypto_tester.h
	 */
	void (*add_test_vector)(crypto_factory_t *this, transform_type_t type,
							void *vector);

	/**
	 * Create an enumerator verifying transforms using known test vectors.
	 *
	 * The resulting enumerator enumerates over an u_int with the type
	 * specific transform identifier, the plugin name providing the transform,
	 * and a boolean value indicating success/failure for the given transform.
	 *
	 * @param type			transform type to test
	 * @return				enumerator over (u_int, char*, bool)
	 */
	enumerator_t* (*create_verify_enumerator)(crypto_factory_t *this,
											  transform_type_t type);

	/**
	 * Destroy a crypto_factory instance.
	 */
	void (*destroy)(crypto_factory_t *this);
};

======================================================================

struct entry_t {
	/**
	 * algorithm
	 */
	u_int algo;

	/**
	 * plugin that registered this algorithm
	 */
	const char *plugin_name;

	/**
	 * benchmarked speed
	 */
	u_int speed;

	/**
	 * constructor
	 */
	union {
		crypter_constructor_t create_crypter;
		aead_constructor_t create_aead;
		signer_constructor_t create_signer;
		hasher_constructor_t create_hasher;
		prf_constructor_t create_prf;
		xof_constructor_t create_xof;
		rng_constructor_t create_rng;
		nonce_gen_constructor_t create_nonce_gen;
		dh_constructor_t create_dh;
		void *create;
	};
};

/**
 * private data of crypto_factory
 */
struct private_crypto_factory_t {

	/**
	 * public functions
	 */
	crypto_factory_t public;

	/**
	 * registered crypters, as entry_t
	 */
	linked_list_t *crypters;

	/**
	 * registered aead transforms, as entry_t
	 */
	linked_list_t *aeads;

	/**
	 * registered signers, as entry_t
	 */
	linked_list_t *signers;

	/**
	 * registered hashers, as entry_t
	 */
	linked_list_t *hashers;

	/**
	 * registered prfs, as entry_t
	 */
	linked_list_t *prfs;

	/**
	 * registered xofs, as entry_t
	 */
	linked_list_t *xofs;

	/**
	 * registered rngs, as entry_t
	 */
	linked_list_t *rngs;

	/**
	 * registered nonce generators, as entry_t
	 */
	linked_list_t *nonce_gens;

	/**
	 * registered diffie hellman, as entry_t
	 */
	linked_list_t *dhs;

	/**
	 * test manager to test crypto algorithms
	 */
	crypto_tester_t *tester;

	/**
	 * whether to test algorithms during registration
	 */
	bool test_on_add;

	/**
	 * whether to test algorithms on each crypto primitive construction
	 */
	bool test_on_create;

	/**
	 * run algorithm benchmark during registration
	 */
	bool bench;

	/**
	 * Number of failed test vectors during "add".
	 */
	u_int test_failures;

	/**
	 * rwlock to lock access to modules
	 */
	rwlock_t *lock;
};
