/**
 * The plugin_loader loads plugins from a directory and initializes them
 */
struct plugin_loader_t {

	/**
	 * 添加一个静态插件特性，不是通过插件加载（而添加）的
	 * Add static plugin features, not loaded via plugins.
	 * 跟插件提供的特性相似
	 * Similar to features provided by plugins they are evaluated during load(),
	 * and unloaded when unload() is called.
	 *
	 * If critical is TRUE load() will fail if any of the added features could
	 * not be loaded.
	 *
	 * If a reload callback function is given, it gets invoked for the
	 * registered feature set when reload() is invoked on the plugin_loader.
	 *
	 * @note The name should be unique otherwise a plugin with the same name is
	 * not loaded.
	 *
	 * @param name			name of the component adding the features
	 * @param features		array of plugin features
	 * @param count			number of features in the array
	 * @param critical		TRUE if the features are critical
	 * @param reload		feature reload callback, or NULL
	 * @param reload_data	user data to pass to reload callback
	 */
	void (*add_static_features) (plugin_loader_t *this, const char *name,
								 struct plugin_feature_t *features, int count,
								 bool critical, bool (*reload)(void*),
								 void *reload_data);

	/**
	 * Load a list of plugins.
	 * 插件列表中关键插件使用！作为结尾。加载关键插件失败，将导致加载退出
	 * 额外的搜索路径可通过add_path()添加，先按添加顺序搜索插件，然后再搜索默认路径
	 * 如果<namespace>.load_modular有效，则要加载的插件取决于他们在
	 *  \<ns>.plugins.\<plugin>.load 位置的加载选项。
	 * 加载顺序取决于配置的优先级，同一优先级的，取决于他们在列表中的顺序
	 * 未在列表中找到的插件首先按字母顺序加载。
	 * 注意，尽管该方法可以被多次调用，但在插件功能及其依赖项
	 *（特别是软依赖项）方面，目前并不真正支持这一点。
	 * @param list			space separated list of plugins to load
	 * @return				TRUE if all critical plugins loaded successfully
	 */
	bool (*load)(plugin_loader_t *this, char *list);

	/**
	 * Add an additional search path for plugins.
	 *
	 * These will be searched in the order they were added.
	 *
	 * @param path			path containing loadable plugins
	 */
	void (*add_path)(plugin_loader_t *this, char *path);

	/**
	 * Reload the configuration of one or multiple plugins.
	 *
	 * @param				space separated plugin names to reload, NULL for all
	 * @return				number of plugins that did support reloading
	 */
	u_int (*reload)(plugin_loader_t *this, char *list);

	/**
	 * Unload all loaded plugins.
	 */
	void (*unload)(plugin_loader_t *this);

	/**
	 * Create an enumerator over all loaded plugins.
	 *
	 * In addition to the plugin, the enumerator optionally provides a list of
	 * pointers to plugin features currently loaded.
	 * This list has to be destroyed.
	 *
	 * @return				enumerator over plugin_t*, linked_list_t*
	 */
	enumerator_t* (*create_plugin_enumerator)(plugin_loader_t *this);

	/**
	 * Check if the given feature is available and loaded.
	 *
	 * @param feature		feature to check
	 * @return				TRUE if feature available
	 */
	bool (*has_feature)(plugin_loader_t *this, struct plugin_feature_t feature);

	/**
	 * Get a simple list the names of all loaded plugins.
	 *
	 * The function returns internal data, do not free.
	 *
	 * @return				list of the names of all loaded plugins
	 */
	char* (*loaded_plugins)(plugin_loader_t *this);

	/**
	 * Log status about loaded plugins and features.
	 *
	 * @param level			log level to use
	 */
	void (*status)(plugin_loader_t *this, level_t level);

	/**
	 * Unload loaded plugins, destroy plugin_loader instance.
	 */
	void (*destroy)(plugin_loader_t *this);
};

======================================================================

#ifdef STATIC_PLUGIN_CONSTRUCTORS
/**
 * Statically registered constructors
 */
static hashtable_t *plugin_constructors = NULL;
#endif

/**
 * private data of plugin_loader &private_plugin_loader_t
 */
struct private_plugin_loader_t {

	/**
	 * public functions
	 */
	plugin_loader_t public;

	/**
	 * 插件列表
	 * List of plugins, as plugin_entry_t
	 */
	linked_list_t *plugins;

	/**
	 * 注册特性的哈希表
	 * Hashtable for registered features, as registered_feature_t
	 */
	hashtable_t *features;

	/**
	 * 加载的特性（逆序存放）
	 * Loaded features (stored in reverse order), as provided_feature_t
	 */
	linked_list_t *loaded;

	/**
	 * 搜索路径
	 * List of paths to search for plugins
	 */
	linked_list_t *paths;

	/**
	 * 加载插件的名字序列
	 * List of names of loaded plugins
	 */
	char *loaded_plugins;

	/**
	 * Statistics collected while loading features
	 */
	struct {
		/** Number of features that failed to load */
		int failed;
		/** Number of features that failed because of unmet dependencies */
		int depends;
		/** Number of features in critical plugins that failed to load */
		int critical;
	} stats;
};

/**
 * 注册的特性
 * Registered plugin feature
 */
struct registered_feature_t {  &registered_feature_t

	/**
	 * 注册的特性
	 * The registered feature
	 */
	plugin_feature_t *feature;

	/**
	 * 提供此特性的插件的列表
	 * List of plugins providing this feature, as provided_feature_t
	 */
	linked_list_t *plugins;
};

/**
 * 插件所提供的特性：对一个特性的整体描述，内容包括了
 * 其依赖的特性、哪个插件提供的该特性、该特性的注册或回调入口信息等
 * Feature as provided by a plugin
 */
struct provided_feature_t {

	/**
	 * 提供该特性的插件
	 * Plugin providing the feature
	 */
	plugin_entry_t *entry;

	/**
	 * 注册或回调入口
	 * FEATURE_REGISTER or FEATURE_CALLBACK entry
	 */
	plugin_feature_t *reg;

	/**
	 * 提供的功能（后跟依赖项）
	 * The provided feature (followed by dependencies)
	 */
	plugin_feature_t *feature;

	/**
	 * Maximum number of dependencies (following feature)
	 */
	int dependencies;

	/**
	 * TRUE if currently loading this feature (to prevent loops)
	 */
	bool loading;

	/**
	 * TRUE if feature loaded
	 */
	bool loaded;

	/**
	 * TRUE if feature failed to load
	 */
	bool failed;
};

/**
 * Entry for a plugin
 */
struct plugin_entry_t {

	/**
	 * Plugin instance
	 */
	plugin_t *plugin;

	/**
	 * TRUE, if the plugin is marked as critical
	 */
	bool critical;

	/**
	 * dlopen handle, if in separate lib
	 */
	void *handle;

	/**
	 * 插件提供的各种特性
	 * List of features, as provided_feature_t
	 */
	linked_list_t *features;
};

/**
 * Wrapper for static plugin features
 * &static_features_t
 */
typedef struct {

	/**
	 * Implements plugin_t interface
	 */
	plugin_t public;

	/**
	 * Name of the module registering these features
	 */
	char *name;

	/**
	 * Optional reload function for features
	 */
	bool (*reload)(void *data);

	/**
	 * User data to pass to reload function
	 */
	void *reload_data;

	/**
	 * Static plugin features
     * 参：file://plugin_feature中的结构与变量.h
	 */
	plugin_feature_t *features;

	/**
	 * Number of plugin features
	 */
	int count;

} static_features_t;

/**
 * Used to sort plugins by priority
 */
typedef struct {
	/* name of the plugin */
	char *name;
	/* the plugins priority */
	int prio;
	/* default priority */
	int def;
} plugin_priority_t;