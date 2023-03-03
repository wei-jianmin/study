/**
 * 插件提供或依赖的功能，包括注册功能。
  
 * 每个插件都会返回一个插件特性列表，允许插件加载器解析依赖关系并注册这些特性。  
 * FEATURE_PROVIDE 宏定义了插件提供的特性，
 * 硬（DEPENDS）或软（SDEPEND）依赖描述，与之前定义的 PROVIDE 功能相关。 
 * 如果插件特性需要将功能挂钩到库或守护程序中（需要勾到库或守护进程上，以实现某种功能），
 * 它可以使用 REGISTER 或 CALLBACK 条目(entries)。 
 * 每个 PROVIDE 功能都使用之前定义的 REGISTER/CALLBACK 条目。  
 * REGISTER 条目定义了直接传递给相关管理器或工厂（加密/凭证工厂等）的、
 * 通用的、对(后面)teature的注册函数。 
 * 回调函数更通用，允许加载程序调用回调来进行注册。 
 * 必须在任何 REGISTER/CALLBACK 条目之前列出不使用注册或回调函数的 PROVIDE 功能，
 * 或使用 NOOP 辅助宏。
 * Each plugin returns a list of plugin features, allowing the plugin loader
 * to resolve dependencies and register the feature. FEATURE_PROVIDE defines
 * features provided by the plugin, hard (DEPENDS) or soft (SDEPEND) dependency
 * specified is related to the previously defined PROVIDE feature.
 * If a plugin feature requires to hook in functionality into the library
 * or a daemon, it can use REGISTER or CALLBACK entries. Each PROVIDE feature
 * uses the REGISTER/CALLBACK entry defined previously. The REGISTER entry
 * defines a common feature registration function directly passed to the
 * associated manager or factory (crypto/credential factory etc.). A callback
 * function is more generic allows the loader to invoke a callback to do
 * the registration. PROVIDE features that do not use a registration or callback
 * function must be listed before any REGISTER/CALLBACK entry, or use the NOOP
 * helper macro.
 
 plugin_feature_t的简要结构
   struct plugin_feature_t {
       enum kind;
       enum type;
       union arg;
   }
 
 PLUGIN_PROVIDE
 * 为了方便地创建功能列表，请使用如下宏来创建/产生 plugin_feature_t 结构数组
 * PLUGIN_REGISTER, PLUGIN_CALLBACK, PLUGIN_NOOP, 
 * PLUGIN_PROVIDE, PLUGIN_DEPENDS, PLUGIN_SDEPEND. 
 * 使用缩进来显示注册的函数或依赖是如何与一个提供的特性相关联的，像如：
 * Use indentation to show how the registration functions
 * and dependencies are related to a provided feature, such as:
 *
 * @verbatim
    // 两个特性，其中一个有两个依赖，这两个特性都使用同一个回调进行注册
	// two features, one with two dependencies, both use a callback to register
	PLUGIN_CALLBACK(...),
		PLUGIN_PROVIDE(...),
			PLUGIN_DEPENDS(...),
			PLUGIN_SDEPEND(...),
		PLUGIN_PROVIDE(...),
    // 注册一个包含一个依赖的特性的一般方法 
	// common constructor to register for a feature with one dependency
	PLUGIN_REGISTER(...),
		PLUGIN_PROVIDE(...),
			PLUGIN_DEPENDS(...),
	// feature that does not use a registration function
	PLUGIN_NOOP,
		PLUGIN_PROVIDE(...),
	@endverbatim
 *  实例： nm_backend.c
    // Initialize/deinitialize NetworkManager backend
    static bool nm_backend_cb(void *plugin,plugin_feature_t *feature,
                               bool reg, void *data)
    {
        if (reg)
        {
            return nm_backend_init();
        }
        nm_backend_deinit();
        return TRUE;
    }
    void nm_backend_register()
    {
        static plugin_feature_t features[] = {
            PLUGIN_CALLBACK((plugin_feature_callback_t)nm_backend_cb, NULL),
                PLUGIN_PROVIDE(CUSTOM, "NetworkManager backend"),
                    PLUGIN_DEPENDS(CUSTOM, "libcharon"),
                    PLUGIN_SDEPEND(PRIVKEY, KEY_RSA),
                    PLUGIN_SDEPEND(PRIVKEY, KEY_ECDSA),
                    PLUGIN_SDEPEND(CERT_DECODE, CERT_ANY),
                    PLUGIN_SDEPEND(CERT_DECODE, CERT_X509),
        };
        lib->plugins->add_static_features(lib->plugins, "nm-backend", features,
                                          countof(features), TRUE, NULL, NULL);
    }
    
对构建宏的展开说明  &对构建宏的展开说明
    PLUGIN_PROVIDE(type, ...)  //如: PLUGIN_PROVIDE(CUSTOM, "NetworkManager backend")
        _PLUGIN_FEATURE_##type(PROVIDE, __VA_ARGS__)
            _PLUGIN_FEATURE_CUSTOM(PROVIDE, name)  //type == CUSTOM
                __PLUGIN_FEATURE(PROVIDE, CUSTOM, .custom = name)
                    (plugin_feature_t){FEATURE_PROVIDE,FEATURE_CUSTOM,{.custom = name}}
            _PLUGIN_FEATURE_HASHER(PROVIDE, name)
                __PLUGIN_FEATURE(PROVIDE, HASHER, .hasher = alg)
                    (plugin_feature_t){FEATURE_PROVIDE,FEATURE_HASHER,{.hasher = alg}}
            _PLUGIN_FEATURE_PRIVKEY(PROVIDE, name)
                __PLUGIN_FEATURE(PROVIDE, PRIVKEY, .privkey = type)
                    (plugin_feature_t){FEATURE_PROVIDE,FEATURE_PRIVKEY,{.privkey = type}}
            _PLUGIN_FEATURE_CERT_DECODE(PROVIDE, name)
                __PLUGIN_FEATURE(kind, CERT_DECODE, .cert = type)
                    (plugin_feature_t){FEATURE_PROVIDE,FEATURE_CERT_DECODE,{.cert = type}}
     PLUGIN_DEPENDS(type, ...) 
        _PLUGIN_FEATURE_##type(DEPENDS, __VA_ARGS__)
            _PLUGIN_FEATURE_CUSTOM(DEPENDS, name)  //type == CUSTOM
                __PLUGIN_FEATURE(DEPENDS, CUSTOM, .custom = name)
                    (plugin_feature_t){FEATURE_DEPENDS,FEATURE_CUSTOM,{.custom = name}}
    PLUGIN_REGISTER(type, f, ...)
        _PLUGIN_FEATURE_REGISTER_##type(type, f, ##__VA_ARGS__)
            _PLUGIN_FEATURE_REGISTER_DH(type, f)
                __PLUGIN_FEATURE_REGISTER(type, f)
                    (plugin_feature_t){ FEATURE_REGISTER, FEATURE_##type, .arg.reg.f = _f }
            _PLUGIN_FEATURE_REGISTER_RNG(type, f)
                __PLUGIN_FEATURE_REGISTER(type, f)
                    (plugin_feature_t){ FEATURE_REGISTER, FEATURE_##type, .arg.reg.f = _f }
     PLUGIN_CALLBACK(cb, data)
        _PLUGIN_FEATURE_CALLBACK(cb, data)
             (plugin_feature_t){FEATURE_CALLBACK,FEATURE_NONE,.arg.cb={.f=_cb,.data=_data}}
    PLUGIN_NOOP
        _PLUGIN_FEATURE_CALLBACK(NULL, NULL)
    可见，上面每种宏，都是构造了一个plugin_feature_t结构
 */
struct plugin_feature_t {
	/** kind of entry 条目类型*/
	enum {
		/* plugin provides this feature 插件提供该特性 */
		FEATURE_PROVIDE,
		/* a feature depends on this feature, hard dependency  插件硬依赖该特性*/
		FEATURE_DEPENDS,
		/* a feature can optionally use this feature, soft dependency 插件软依赖该特性 */
		FEATURE_SDEPEND,
		/* register the specified function for all following features 为下面的特性注册指定的函数*/
		FEATURE_REGISTER,
		/* use a callback to register all following features 使用一个回调函数来注册下面的特性*/
		FEATURE_CALLBACK,
	} kind;
	/* type of feature 功能特性*/
	enum {
		/** not a feature */
		FEATURE_NONE,
		/** crypter_t */
		FEATURE_CRYPTER,
		/** aead_t */
		FEATURE_AEAD,
		/** signer_t */
		FEATURE_SIGNER,
		/** hasher_t */
		FEATURE_HASHER,
		/** prf_t */
		FEATURE_PRF,
		/** xof_t */
		FEATURE_XOF,
		/** diffie_hellman_t */
		FEATURE_DH,
		/** rng_t */
		FEATURE_RNG,
		/** nonce_gen_t */
		FEATURE_NONCE_GEN,
		/** generic private key support */
		FEATURE_PRIVKEY,
		/** generating new private keys */
		FEATURE_PRIVKEY_GEN,
		/** private_key_t->sign() */
		FEATURE_PRIVKEY_SIGN,
		/** private_key_t->decrypt() */
		FEATURE_PRIVKEY_DECRYPT,
		/** generic public key support */
		FEATURE_PUBKEY,
		/** public_key_t->verify() */
		FEATURE_PUBKEY_VERIFY,
		/** public_key_t->encrypt() */
		FEATURE_PUBKEY_ENCRYPT,
		/** parsing certificates */
		FEATURE_CERT_DECODE,
		/** generating certificates */
		FEATURE_CERT_ENCODE,
		/** parsing containers */
		FEATURE_CONTAINER_DECODE,
		/** generating containers */
		FEATURE_CONTAINER_ENCODE,
		/** EAP server implementation */
		FEATURE_EAP_SERVER,
		/** EAP peer implementation */
		FEATURE_EAP_PEER,
		/** XAuth server implementation */
		FEATURE_XAUTH_SERVER,
		/** XAuth peer implementation */
		FEATURE_XAUTH_PEER,
		/** database_t */
		FEATURE_DATABASE,
		/** fetcher_t */
		FEATURE_FETCHER,
		/** resolver_t */
		FEATURE_RESOLVER,
		/** custom feature, described with a string */
		FEATURE_CUSTOM,
	} type;
	/** More specific data for each type 针对每种类型的更多描述*/
	union {
		/** FEATURE_CRYPTER */
		struct {
			encryption_algorithm_t alg;
			size_t key_size;
		} crypter;
		/** FEATURE_AEAD */
		struct {
			encryption_algorithm_t alg;
			size_t key_size;
		} aead;
		/** FEATURE_SIGNER */
		integrity_algorithm_t signer;
		/** FEATURE_PRF */
		pseudo_random_function_t prf;
		/** FEATURE_XOFF */
		ext_out_function_t xof;
		/** FEATURE_HASHER */
		hash_algorithm_t hasher;
		/** FEATURE_DH */
		diffie_hellman_group_t dh_group;
		/** FEATURE_RNG */
		rng_quality_t rng_quality;
		/** FEATURE_PRIVKEY */
		key_type_t privkey;
		/** FEATURE_PRIVKEY_GEN */
		key_type_t privkey_gen;
		/** FEATURE_PRIVKEY_SIGN */
		signature_scheme_t privkey_sign;
		/** FEATURE_PRIVKEY_DECRYPT */
		encryption_scheme_t privkey_decrypt;
		/** FEATURE_PUBKEY */
		key_type_t pubkey;
		/** FEATURE_PUBKEY_VERIFY */
		signature_scheme_t pubkey_verify;
		/** FEATURE_PUBKEY_ENCRYPT */
		encryption_scheme_t pubkey_encrypt;
		/** FEATURE_CERT_DECODE/ENCODE */
		certificate_type_t cert;
		/** FEATURE_CONTAINER_DECODE/ENCODE */
		container_type_t container;
		/** FEATURE_EAP_SERVER/CLIENT */
		eap_vendor_type_t eap;
		/** FEATURE_DATABASE */
		db_driver_t database;
		/** FEATURE_FETCHER */
		char *fetcher;
		/** FEATURE_CUSTOM */
		char *custom;
		/** FEATURE_XAUTH_SERVER/CLIENT */
		char *xauth;

		/** FEATURE_REGISTER */
		struct {
			/** final flag to pass for builder_function_t */
			bool final;
			/** feature specific function to register for this type */
			void *f;
		} reg;

		/** FEATURE_CALLBACK */
		struct {
			/** callback function to invoke for registration */
			plugin_feature_callback_t f;
			/** data to pass to callback */
			void *data;
		} cb;
	} arg;
};