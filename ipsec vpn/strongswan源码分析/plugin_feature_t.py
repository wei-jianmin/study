/*
   本文件名虽未plugin_feature_t.py，但包含的内容不止这些
   而是详细跟踪了privete_plugin_loader_t结构中plugins的赋值过程 
   这个过程是在plugin_loader.c（插件加载器）中发起的   
*/

file://plugin_feature中的结构与变量.h

plugin_feature_t中有三个成员： &plugin_feature_t
    kind为枚举型（int）：用于插件特性分类
    type为枚举型（int）：用于插件具体功能分类
    arg为union类型，针对不同的kind和type值，有不同的结构形式
    
PLUGIN_xxx 宏展开：    //参： file://plugin_feature中的结构与变量.h@对构建宏的展开说明
    //type的值常见的是CUSTOM，但也可能是EAP_SERVER/EAP_PEER/DH/PRF/SIGNER/PRIVKEY/CRYPTER/...    
    PLUGIN_PROVIDE(type, ...)       //参数为：插件名字、存给arg.custom的值
        _PLUGIN_FEATURE_##type(PROVIDE, __VA_ARGS__)
            _PLUGIN_FEATURE_CUSTOM(kind = PROVIDE, name)	
                __PLUGIN_FEATURE(kind = PROVIDE, type = CUSTOM, .custom = name)
                    (plugin_feature_t){ FEATURE_PROVIDE, FEATURE_CUSTOM, { __VA_ARGS__ }}
                    
    //type的值常见的是CUSTOM，但也可能是EAP_SERVER/EAP_PEER/DH/PRF/SIGNER/PRIVKEY/CRYPTER/...               
    PLUGIN_DEPENDS(type, ...)       //参数为：插件名字、存给arg.custom的值
        _PLUGIN_FEATURE_##type(DEPENDS, __VA_ARGS__)
            _PLUGIN_FEATURE_CUSTOM(kind = DEPENDS, name)
                __PLUGIN_FEATURE(kind = DEPENDS, type = CUSTOM, .custom = name)
                    (plugin_feature_t){ FEATURE_DEPENDS, FEATURE_CUSTOM, { __VA_ARGS__ }}
                    
    //type的值常见的是CUSTOM，但也可能是EAP_SERVER/EAP_PEER/DH/PRF/SIGNER/PRIVKEY/CRYPTER/...               
    PLUGIN_SDEPENDS(type, ...)      //件数为：插件名字、存给arg.custom的值
        _PLUGIN_FEATURE_##type(DEPENDS, __VA_ARGS__)
            _PLUGIN_FEATURE_CUSTOM(kind = SDEPENDS, name)
                __PLUGIN_FEATURE(kind = SDEPENDS, type = CUSTOM, .custom = name)            
                    (plugin_feature_t){ FEATURE_SDEPENDS, FEATURE_CUSTOM, { __VA_ARGS__ }}
                    
    //type取值为PUBKEY、CERT_DECODE、RNG、CRYPTER、PRF、HASHER等等，不会是CUSTOM            
    PLUGIN_REGISTER(type, f, ...)   //参数为：注册函数地址、？    
        _PLUGIN_FEATURE_REGISTER_##type(type, f, ##__VA_ARGS__)
            __PLUGIN_FEATURE_REGISTER_BUILDER(type, f, final)
                (plugin_feature_t){ FEATURE_REGISTER, FEATURE_##type, .arg.reg = {.f = _f, .final = _final, }}
                
    PLUGIN_CALLBACK(cb, data)       //参数为：回调函数地址、传给回调函数的参数
        _PLUGIN_FEATURE_CALLBACK(cb, data)
            (plugin_feature_t){ FEATURE_CALLBACK, FEATURE_NONE, .arg.cb = { .f = _cb, .data = _data } }
        
    PLUGIN_xxx 宏展开的结果来看，都是得到一个plugin_feature_t结构

daemon::initialize(...)
    plugin_feature_t features[] = {
            { FEATURE_PROVIDE, FEATURE_CUSTOM, { __VA_ARGS__ }}
            PLUGIN_PROVIDE(CUSTOM, "libcharon"),
                PLUGIN_DEPENDS(NONCE_GEN),
                PLUGIN_DEPENDS(CUSTOM, "libcharon-sa-managers"),
                PLUGIN_DEPENDS(CUSTOM, "libcharon-receiver"),
                PLUGIN_DEPENDS(CUSTOM, "kernel-ipsec"),
                PLUGIN_DEPENDS(CUSTOM, "kernel-net"),
            PLUGIN_CALLBACK((plugin_feature_callback_t)sender_receiver_cb, this),
                PLUGIN_PROVIDE(CUSTOM, "libcharon-receiver"),
                    PLUGIN_DEPENDS(HASHER, HASH_SHA1),
                    PLUGIN_DEPENDS(RNG, RNG_STRONG),
                    PLUGIN_DEPENDS(CUSTOM, "socket"),
            PLUGIN_CALLBACK((plugin_feature_callback_t)sa_managers_cb, this),
                PLUGIN_PROVIDE(CUSTOM, "libcharon-sa-managers"),
                    PLUGIN_DEPENDS(HASHER, HASH_SHA1),
                    PLUGIN_DEPENDS(RNG, RNG_WEAK),
        };
    宏替换后结果： &charon.features
    plugin_feature_t features[] = {
            { FEATURE_PROVIDE, CUSTOM, .custom="libcharon" },
                { FEATURE_DEPENDS, NONCE_GEN },
                { FEATURE_DEPENDS, CUSTOM, .custom="libcharon-sa-managers" },
                { FEATURE_DEPENDS, CUSTOM, .custom="libcharon-receiver" },
                { FEATURE_DEPENDS, CUSTOM, .custom="kernel-ipsec" },
                { FEATURE_DEPENDS, CUSTOM, .custom="kernel-net" },
            { FEATURE_CALLBACK, FEATURE_NONE, .cb = { .f = sender_receiver_cb, .data = this } },
                { FEATURE_PROVIDE, CUSTOM, .custom="libcharon-receiver" },
                    { FEATURE_DEPENDS, HASHER, .hasher=HASH_SHA1 },
                    { FEATURE_DEPENDS, RNG, .rng_quality=RNG_STRONG },
                    { FEATURE_DEPENDS, CUSTOM, .custom="socket" },
            { FEATURE_CALLBACK, FEATURE_NONE, .cb = { .f = sa_managers_cb, .data = this } },
                { FEATURE_PROVIDE, CUSTOM, .custom="libcharon-sa-managers" },
                    { FEATURE_DEPENDS, HASHER, .hasher=HASH_SHA1 },
                    { FEATURE_DEPENDS, RNG, .rng_quality=RNG_WEAK }
        }  
    
    static_features_t *sfeatures;  //源码plugin_loader.c中  @static_features_t
    sfeatures.public = {
                    .get_name = _get_static_name,
                    .get_features = _get_static_features,
                        调用 sfeatures.reload(sfeatures.reload_data) 或返回 FALSE
                    .reload = _static_reload,
                    .destroy = _static_destroy,
                },
    sfeatures.name = "charon"
    sfeatures.reload = reload = 0
    sfeatures.reload_data = reload_data = 0
    sfeatures.features = copy(features);
    sfeatures.count = count(features);
    
    plugin_t *plugin = sfeatures.public
    
    plugin_entry_t *entry;                  //@plugin_entry_t
    entry.plugin = plugin                   //plugin_t *  @plugin_t
    entry.critical = true
    entry.features =  linked_list_create()  //linked_list_t *
    
    //file://plugin_loader中的结构与变量.h@private_plugin_loader_t
    private_plugin_loader_t * this = lib->plugins;  
    this->plugins->insert_last(entry);  
    
    //以上过程参：file://../imgs/plugin_loader的plugins赋值.png
    
    register_features(this, entry);     //参：file://plugin_loader分析.py
        private_plugin_loader_t *this = lib->plugins; 
        plugin_feature_t *feature, *reg;
        //参 file://plugin_loader中的结构与变量.h@registered_feature_t
        registered_feature_t *registered, lookup;
        provided_feature_t *provided;
    
        通过 entry->plugin->get_features 得到 sfeatures.features, 存给数组指针：feature
        int count = sfeatures.features数组个数
        
        遍历 sfeatures.features  
            如果是 FEATURE_PROVIDE
                registered = 从 this->features（registered_feature_t链表） 中子成员匹配上文feature的成员
                没找到
                    this->features->put(key=registered, value=registered)
                        registered.feature = 数组指针：feature
                        registered.plugins = linked_list_create()
                registered.plugins.insert(provided)
                    provided.entry = 上文中的 entry
                    provided.feature = 数组指针：feature
                    provided.reg = reg (首次为NULL)
                    provided.dependencies = count--
                    
struct static_features_t {       //&static_features_t
	plugin_t public;    // Implements plugin_t interface
	char *name;         // Name of the module registering these features
	bool (*reload)(void *data);  // Optional reload function for features
	void *reload_data;           // User data to pass to reload function
	plugin_feature_t *features;  // Static plugin features @plugin_feature_t
	int count;                   // Number of plugin features
} ;    

struct plugin_t {                         //&plugin_t
	char* (*get_name)(plugin_t *this);    //* Get the name of the plugin.
	int  (*get_features)(plugin_t *this,  //Get plugin features with dependencies.
                         plugin_feature_t *features[]);  
	bool (*reload)(plugin_t *this);       // Try to reload plugin configuration.
	void (*destroy)(plugin_t *this);      //Destroy a plugin instance.
};

struct plugin_entry_t {       //&plugin_entry_t
	plugin_t *plugin;         //Plugin instance
	bool critical;            //TRUE, if the plugin is marked as critical
	void *handle;             //dlopen handle, if in separate lib
	linked_list_t *features;  //List of features, as provided_feature_t
};
