/* 
    配置文件的组织特点：
    节点名 { 
        内容集合
    ｝
    内容集合可以直接是键值对、可以是include关键字+文件名、还可以是子节点
    如：
        a = 1
        sec1 {
            b = 2  //内容直接是键值对形式
            include x.conf  //引用文件支持相对路径，支持*匹配，文件原地展开
            sec1-1 {  //嵌套子节点，嵌套级数没有限制
                c = 3
            }
            b = 4  //会覆盖掉之前的值
        }
        sec2 {
        }
	要想获取 c 的值，通过get方法，用 set1.sec1-1.c 键检索
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
#该内容摘自settings_types.h，同样被settings.c包含

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
	char *name;  //引用的section的名字

	/**
	 * TRUE for permanent references that were added programmatically via
	 * add_fallback() and are not removed during reloads/purges.
	 */
	bool permanent;  //被代码add_fallback所添加的,不会被reloads或purges移除
};

/**
 * Section containing subsections and key value pairs.
 * 被设计为可以包含kv值、子section、引用section，并且没有section都有自己的名字
 */
struct section_t {

	/**
	 * Name of the section.
	 */
	char *name;   //section的名字

	/**
	 * Referenced sections, as section_ref_t.
	 */
	array_t *references;  //引用的section

	/**
	 * Subsections, as section_t.
	 */
	array_t *sections;  //section下面可以有子section（从而形成树形结构）

	/**
	 * Subsections in original order, as section_t (pointer to obj in sections).
	 */
	array_t *sections_order;   //按原始允许排列的子sections

	/**
	 * Key value pairs, as kv_t.
	 */
	array_t *kv;

	/**
	 * Key value pairs in original order, as kv_t (pointer to obj in kv).
	 */
	array_t *kv_order;   //按原始允许排序的kv值
};

============================================================


/**
 * Private data of settings
 */
struct private_settings_t {

	/**
	 * Public interface
	 */
	settings_t public;  //访问接口

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
	array_t *contents;  //setting配置文件中被替换的内容，字符串形式

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
} enumerator_data_t;  //枚举section树的时候，需要借助本结构