/*
   ���ļ�����δplugin_feature_t.py�������������ݲ�ֹ��Щ
   ������ϸ������privete_plugin_loader_t�ṹ��plugins�ĸ�ֵ���� 
   �����������plugin_loader.c��������������з����   
*/

file://plugin_feature�еĽṹ�����.h

plugin_feature_t����������Ա�� &plugin_feature_t
    kindΪö���ͣ�int�������ڲ�����Է���
    typeΪö���ͣ�int�������ڲ�����幦�ܷ���
    argΪunion���ͣ���Բ�ͬ��kind��typeֵ���в�ͬ�Ľṹ��ʽ
    
PLUGIN_xxx ��չ����    //�Σ� file://plugin_feature�еĽṹ�����.h@�Թ������չ��˵��
    //type��ֵ��������CUSTOM����Ҳ������EAP_SERVER/EAP_PEER/DH/PRF/SIGNER/PRIVKEY/CRYPTER/...    
    PLUGIN_PROVIDE(type, ...)       //����Ϊ��������֡����arg.custom��ֵ
        _PLUGIN_FEATURE_##type(PROVIDE, __VA_ARGS__)
            _PLUGIN_FEATURE_CUSTOM(kind = PROVIDE, name)	
                __PLUGIN_FEATURE(kind = PROVIDE, type = CUSTOM, .custom = name)
                    (plugin_feature_t){ FEATURE_PROVIDE, FEATURE_CUSTOM, { __VA_ARGS__ }}
                    
    //type��ֵ��������CUSTOM����Ҳ������EAP_SERVER/EAP_PEER/DH/PRF/SIGNER/PRIVKEY/CRYPTER/...               
    PLUGIN_DEPENDS(type, ...)       //����Ϊ��������֡����arg.custom��ֵ
        _PLUGIN_FEATURE_##type(DEPENDS, __VA_ARGS__)
            _PLUGIN_FEATURE_CUSTOM(kind = DEPENDS, name)
                __PLUGIN_FEATURE(kind = DEPENDS, type = CUSTOM, .custom = name)
                    (plugin_feature_t){ FEATURE_DEPENDS, FEATURE_CUSTOM, { __VA_ARGS__ }}
                    
    //type��ֵ��������CUSTOM����Ҳ������EAP_SERVER/EAP_PEER/DH/PRF/SIGNER/PRIVKEY/CRYPTER/...               
    PLUGIN_SDEPENDS(type, ...)      //����Ϊ��������֡����arg.custom��ֵ
        _PLUGIN_FEATURE_##type(DEPENDS, __VA_ARGS__)
            _PLUGIN_FEATURE_CUSTOM(kind = SDEPENDS, name)
                __PLUGIN_FEATURE(kind = SDEPENDS, type = CUSTOM, .custom = name)            
                    (plugin_feature_t){ FEATURE_SDEPENDS, FEATURE_CUSTOM, { __VA_ARGS__ }}
                    
    //typeȡֵΪPUBKEY��CERT_DECODE��RNG��CRYPTER��PRF��HASHER�ȵȣ�������CUSTOM            
    PLUGIN_REGISTER(type, f, ...)   //����Ϊ��ע�ắ����ַ����    
        _PLUGIN_FEATURE_REGISTER_##type(type, f, ##__VA_ARGS__)
            __PLUGIN_FEATURE_REGISTER_BUILDER(type, f, final)
                (plugin_feature_t){ FEATURE_REGISTER, FEATURE_##type, .arg.reg = {.f = _f, .final = _final, }}
                
    PLUGIN_CALLBACK(cb, data)       //����Ϊ���ص�������ַ�������ص������Ĳ���
        _PLUGIN_FEATURE_CALLBACK(cb, data)
            (plugin_feature_t){ FEATURE_CALLBACK, FEATURE_NONE, .arg.cb = { .f = _cb, .data = _data } }
        
    PLUGIN_xxx ��չ���Ľ�����������ǵõ�һ��plugin_feature_t�ṹ

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
    ���滻������ &charon.features
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
    
    static_features_t *sfeatures;  //Դ��plugin_loader.c��  @static_features_t
    sfeatures.public = {
                    .get_name = _get_static_name,
                    .get_features = _get_static_features,
                        ���� sfeatures.reload(sfeatures.reload_data) �򷵻� FALSE
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
    
    //file://plugin_loader�еĽṹ�����.h@private_plugin_loader_t
    private_plugin_loader_t * this = lib->plugins;  
    this->plugins->insert_last(entry);  
    
    //���Ϲ��̲Σ�file://../imgs/plugin_loader��plugins��ֵ.png
    
    register_features(this, entry);     //�Σ�file://plugin_loader����.py
        private_plugin_loader_t *this = lib->plugins; 
        plugin_feature_t *feature, *reg;
        //�� file://plugin_loader�еĽṹ�����.h@registered_feature_t
        registered_feature_t *registered, lookup;
        provided_feature_t *provided;
    
        ͨ�� entry->plugin->get_features �õ� sfeatures.features, �������ָ�룺feature
        int count = sfeatures.features�������
        
        ���� sfeatures.features  
            ����� FEATURE_PROVIDE
                registered = �� this->features��registered_feature_t���� ���ӳ�Աƥ������feature�ĳ�Ա
                û�ҵ�
                    this->features->put(key=registered, value=registered)
                        registered.feature = ����ָ�룺feature
                        registered.plugins = linked_list_create()
                registered.plugins.insert(provided)
                    provided.entry = �����е� entry
                    provided.feature = ����ָ�룺feature
                    provided.reg = reg (�״�ΪNULL)
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
