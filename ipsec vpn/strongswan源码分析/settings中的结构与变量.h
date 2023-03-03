/* 
    �����ļ�����֯�ص㣺
    �ڵ��� { 
        ���ݼ���
    ��
    ���ݼ��Ͽ���ֱ���Ǽ�ֵ�ԡ�������include�ؼ���+�ļ��������������ӽڵ�
    �磺
        a = 1
        sec1 {
            b = 2  //����ֱ���Ǽ�ֵ����ʽ
            include x.conf  //�����ļ�֧�����·����֧��*ƥ�䣬�ļ�ԭ��չ��
            sec1-1 {  //Ƕ���ӽڵ㣬Ƕ�׼���û������
                c = 3
            }
            b = 4  //�Ḳ�ǵ�֮ǰ��ֵ
        }
        sec2 {
        }
	Ҫ���ȡ c ��ֵ��ͨ��get�������� set1.sec1-1.c ������
*/    
struct settings_t {

	/**
	 * Get a settings value as a string.
	 *
	 * @param key		key including sections, printf style format
	 * @param def		value returned if key not found
	 * @param ...		argument list for key
	 * @return			value pointing to internal string
	 */
	char* (*get_str)(settings_t *this, char *key, char *def, ...);

	/**
	 * Get a boolean yes|no, true|false value.
	 *
	 * @param key		key including sections, printf style format
	 * @param def		value returned if key not found
	 * @param ...		argument list for key
	 * @return			value of the key
	 */
	bool (*get_bool)(settings_t *this, char *key, int def, ...);

	/**
	 * Get an integer value.
	 *
	 * @param key		key including sections, printf style format
	 * @param def		value returned if key not found
	 * @param ...		argument list for key
	 * @return			value of the key
	 */
	int (*get_int)(settings_t *this, char *key, int def, ...);

	/**
	 * Get an double value.
	 *
	 * @param key		key including sections, printf style format
	 * @param def		value returned if key not found
	 * @param ...		argument list for key
	 * @return			value of the key
	 */
	double (*get_double)(settings_t *this, char *key, double def, ...);

	/**
	 * Get a time value.
	 *
	 * @param key		key including sections, printf style format
	 * @param def		value returned if key not found
	 * @param ...		argument list for key
	 * @return			value of the key (in seconds)
	 */
	uint32_t (*get_time)(settings_t *this, char *key, uint32_t def, ...);

	/**
	 * Set a string value.
	 *
	 * @param key		key including sections, printf style format
	 * @param value		value to set (gets cloned)
	 * @param ...		argument list for key
	 */
	void (*set_str)(settings_t *this, char *key, char *value, ...);

	/**
	 * Set a boolean value.
	 *
	 * @param key		key including sections, printf style format
	 * @param value		value to set
	 * @param ...		argument list for key
	 */
	void (*set_bool)(settings_t *this, char *key, int value, ...);

	/**
	 * Set an integer value.
	 *
	 * @param key		key including sections, printf style format
	 * @param value		value to set
	 * @param ...		argument list for key
	 */
	void (*set_int)(settings_t *this, char *key, int value, ...);

	/**
	 * Set an double value.
	 *
	 * @param key		key including sections, printf style format
	 * @param value		value to set
	 * @param ...		argument list for key
	 */
	void (*set_double)(settings_t *this, char *key, double value, ...);

	/**
	 * Set a time value.
	 *
	 * @param key		key including sections, printf style format
	 * @param def		value to set
	 * @param ...		argument list for key
	 */
	void (*set_time)(settings_t *this, char *key, uint32_t value, ...);

	/**
	 * Set a default for string value.
	 *
	 * @param key		key including sections, printf style format
	 * @param def		value to set if unconfigured
	 * @param ...		argument list for key
	 * @return			TRUE if a new default value for key has been set
	 */
	bool (*set_default_str)(settings_t *this, char *key, char *value, ...);

	/**
	 * Create an enumerator over subsection names of a section.
	 *
	 * @param section	section including parents, printf style format
	 * @param ...		argument list for key
	 * @return			enumerator over subsection names
	 */
	enumerator_t* (*create_section_enumerator)(settings_t *this,
											   char *section, ...);

	/**
	 * Create an enumerator over key/value pairs in a section.
	 *
	 * @param section	section name to list key/value pairs of, printf style
	 * @param ...		argument list for section
	 * @return			enumerator over (char *key, char *value)
	 */
	enumerator_t* (*create_key_value_enumerator)(settings_t *this,
												 char *section, ...);

	/**
	 * Add a fallback for the given section.
	 *
	 * Example: When the fallback 'section-two' is configured for
	 * 'section-one.two' any failed lookup for a section or key in
	 * 'section-one.two' will result in a lookup for the same section/key
	 * in 'section-two'.
	 *
	 * @note Additional arguments will be applied to both section format
	 * strings so they must be compatible. And they are evaluated immediately,
	 * so arguments can't contain dots.
	 *
	 * @param section	section for which a fallback is configured, printf style
	 * @param fallback	fallback section, printf style
	 * @param ...		argument list for section and fallback
	 */
	void (*add_fallback)(settings_t *this, const char *section,
						 const char *fallback, ...);

	/**
	 * Load settings from the files matching the given pattern.
	 *
	 * If merge is TRUE, existing sections are extended, existing values
	 * replaced, by those found in the loaded files. If it is FALSE, existing
	 * sections are purged before reading the new config.
	 *
	 * @note If any of the files matching the pattern fails to load, no settings
	 * are added at all. So, it's all or nothing.
	 *
	 * @param pattern	file pattern
	 * @param merge		TRUE to merge config with existing values
	 * @return			TRUE, if settings were loaded successfully
	 */
	bool (*load_files)(settings_t *this, char *pattern, bool merge);

	/**
	 * Load settings from the files matching the given pattern.
	 *
	 * If merge is TRUE, existing sections are extended, existing values
	 * replaced, by those found in the loaded files. If it is FALSE, existing
	 * sections are purged before reading the new config.
	 *
	 * All settings are loaded relative to the given section. The section is
	 * created, if it does not yet exist.
	 *
	 * @note If any of the files matching the pattern fails to load, no settings
	 * are added at all. So, it's all or nothing.
	 *
	 * @param pattern	file pattern
	 * @param merge		TRUE to merge config with existing values
	 * @param section	section name of parent section, printf style
	 * @param ...		argument list for section
	 * @return			TRUE, if settings were loaded successfully
	 */
	bool (*load_files_section)(settings_t *this, char *pattern, bool merge,
							   char *section, ...);

	/**
	 * Load settings from the given string.
	 *
	 * If merge is TRUE, existing sections are extended, existing values
	 * replaced, by those found in the string. If it is FALSE, existing
	 * sections are purged before reading the new config.
	 *
	 * @note If the string contains _include_ statements they should be
	 * absolute paths.
	 *
	 * @note If any failures occur, no settings are added at all. So, it's all
	 * or nothing.
	 *
	 * @param settings	string to parse
	 * @param merge		TRUE to merge config with existing values
	 * @return			TRUE, if settings were loaded successfully
	 */
	bool (*load_string)(settings_t *this, char *settings, bool merge);

	/**
	 * Load settings from the given string.
	 *
	 * If merge is TRUE, existing sections are extended, existing values
	 * replaced, by those found in the string. If it is FALSE, existing
	 * sections are purged before reading the new config.
	 *
	 * All settings are loaded relative to the given section. The section is
	 * created, if it does not yet exist.
	 *
	 * @note If the string contains _include_ statements they should be
	 * absolute paths.
	 *
	 * @note If any failures occur, no settings are added at all. So, it's all
	 * or nothing.
	 *
	 * @param settings	string to parse
	 * @param merge		TRUE to merge config with existing values
	 * @param section	section name of parent section, printf style
	 * @param ...		argument list for section
	 * @return			TRUE, if settings were loaded successfully
	 */
	bool (*load_string_section)(settings_t *this, char *settings, bool merge,
								char *section, ...);

	/**
	 * Destroy a settings instance.
	 */
	void (*destroy)(settings_t *this);
};


============================================================
#������ժ��settings_types.h��ͬ����settings.c����

/**
 * Key/value pair.
 */
struct kv_t {

	/**
	 * Key string, relative, not the full name.
	 */
	char *key;

	/**
	 * Value as string.
	 */
	char *value;
};

/**
 * Section reference.
 */
struct section_ref_t {

	/**
	 * Name of the referenced section.
	 */
	char *name;  //���õ�section������

	/**
	 * TRUE for permanent references that were added programmatically via
	 * add_fallback() and are not removed during reloads/purges.
	 */
	bool permanent;  //������add_fallback����ӵ�,���ᱻreloads��purges�Ƴ�
};

/**
 * Section containing subsections and key value pairs.
 * �����Ϊ���԰���kvֵ����section������section������û��section�����Լ�������
 */
struct section_t {

	/**
	 * Name of the section.
	 */
	char *name;   //section������

	/**
	 * Referenced sections, as section_ref_t.
	 */
	array_t *references;  //���õ�section

	/**
	 * Subsections, as section_t.
	 */
	array_t *sections;  //section�����������section���Ӷ��γ����νṹ��

	/**
	 * Subsections in original order, as section_t (pointer to obj in sections).
	 */
	array_t *sections_order;   //��ԭʼ�������е���sections

	/**
	 * Key value pairs, as kv_t.
	 */
	array_t *kv;

	/**
	 * Key value pairs in original order, as kv_t (pointer to obj in kv).
	 */
	array_t *kv_order;   //��ԭʼ���������kvֵ
};

============================================================


/**
 * Private data of settings
 */
struct private_settings_t {

	/**
	 * Public interface
	 */
	settings_t public;  //���ʽӿ�

	/**
	 * Top level section
	 */
	section_t *top;

	/**
	 * Contents of replaced settings (char*)
	 *
	 * FIXME: This is required because the pointer returned by get_str()
	 * is not refcounted.  Might cause ever increasing usage stats.
	 */
	array_t *contents;  //setting�����ļ��б��滻�����ݣ��ַ�����ʽ

	/**
	 * Lock to safely access the settings
	 */
	rwlock_t *lock;
};

/**
 * Data for enumerators
 */
typedef struct {
	/** settings_t instance */
	private_settings_t *settings;
	/** sections to enumerate */
	array_t *sections;
	/** sections/keys that were already enumerated */
	hashtable_t *seen;
} enumerator_data_t;  //ö��section����ʱ����Ҫ�������ṹ