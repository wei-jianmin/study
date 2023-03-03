/**
 * ����ṩ�������Ĺ��ܣ�����ע�Ṧ�ܡ�
  
 * ÿ��������᷵��һ����������б�����������������������ϵ��ע����Щ���ԡ�  
 * FEATURE_PROVIDE �궨���˲���ṩ�����ԣ�
 * Ӳ��DEPENDS������SDEPEND��������������֮ǰ����� PROVIDE ������ء� 
 * ������������Ҫ�����ܹҹ�������ػ������У���Ҫ��������ػ������ϣ���ʵ��ĳ�ֹ��ܣ���
 * ������ʹ�� REGISTER �� CALLBACK ��Ŀ(entries)�� 
 * ÿ�� PROVIDE ���ܶ�ʹ��֮ǰ����� REGISTER/CALLBACK ��Ŀ��  
 * REGISTER ��Ŀ������ֱ�Ӵ��ݸ���ع������򹤳�������/ƾ֤�����ȣ��ġ�
 * ͨ�õġ���(����)teature��ע�ắ���� 
 * �ص�������ͨ�ã�������س�����ûص�������ע�ᡣ 
 * �������κ� REGISTER/CALLBACK ��Ŀ֮ǰ�г���ʹ��ע���ص������� PROVIDE ���ܣ�
 * ��ʹ�� NOOP �����ꡣ
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
 
 plugin_feature_t�ļ�Ҫ�ṹ
   struct plugin_feature_t {
       enum kind;
       enum type;
       union arg;
   }
 
 PLUGIN_PROVIDE
 * Ϊ�˷���ش��������б���ʹ�����º�������/���� plugin_feature_t �ṹ����
 * PLUGIN_REGISTER, PLUGIN_CALLBACK, PLUGIN_NOOP, 
 * PLUGIN_PROVIDE, PLUGIN_DEPENDS, PLUGIN_SDEPEND. 
 * ʹ����������ʾע��ĺ����������������һ���ṩ������������ģ����磺
 * Use indentation to show how the registration functions
 * and dependencies are related to a provided feature, such as:
 *
 * @verbatim
    // �������ԣ�����һ�����������������������Զ�ʹ��ͬһ���ص�����ע��
	// two features, one with two dependencies, both use a callback to register
	PLUGIN_CALLBACK(...),
		PLUGIN_PROVIDE(...),
			PLUGIN_DEPENDS(...),
			PLUGIN_SDEPEND(...),
		PLUGIN_PROVIDE(...),
    // ע��һ������һ�����������Ե�һ�㷽�� 
	// common constructor to register for a feature with one dependency
	PLUGIN_REGISTER(...),
		PLUGIN_PROVIDE(...),
			PLUGIN_DEPENDS(...),
	// feature that does not use a registration function
	PLUGIN_NOOP,
		PLUGIN_PROVIDE(...),
	@endverbatim
 *  ʵ���� nm_backend.c
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
    
�Թ������չ��˵��  &�Թ������չ��˵��
    PLUGIN_PROVIDE(type, ...)  //��: PLUGIN_PROVIDE(CUSTOM, "NetworkManager backend")
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
    �ɼ�������ÿ�ֺ꣬���ǹ�����һ��plugin_feature_t�ṹ
 */
struct plugin_feature_t {
	/** kind of entry ��Ŀ����*/
	enum {
		/* plugin provides this feature ����ṩ������ */
		FEATURE_PROVIDE,
		/* a feature depends on this feature, hard dependency  ���Ӳ����������*/
		FEATURE_DEPENDS,
		/* a feature can optionally use this feature, soft dependency ��������������� */
		FEATURE_SDEPEND,
		/* register the specified function for all following features Ϊ���������ע��ָ���ĺ���*/
		FEATURE_REGISTER,
		/* use a callback to register all following features ʹ��һ���ص�������ע�����������*/
		FEATURE_CALLBACK,
	} kind;
	/* type of feature ��������*/
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
	/** More specific data for each type ���ÿ�����͵ĸ�������*/
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