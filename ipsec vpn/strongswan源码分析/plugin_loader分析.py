图：file://../imgs/strongswan插件机制结构关系.png
文：file://plugin_feature中的结构与变量.h
load_plugins
    char* plugins = modular_pluginlist(list); //根据配置文件或根据参数传来的默认值，得到要加载的模块，按优先级排序
        list为参数传来的内置固定值 <参：file://strongswan简要流程及数据结构.py@plugins值>
        读配置文件的charon.load_moudlar（默认值为FALSE），如果成功
            enumerator = 配置文件的charon.plugins
            load_def = FALSE
        否则
            enumerator = 上面通过 plugins 得到的数组
            load_def = TRUE
        读 charon.plugins.enumerator.load 配置项，记为优先级 prio（默认0）
        如果 prio 为 0
            如果 load_def=FALSE，prio = 1 （prio的最大值为上面数组的元素个数）
        对上面的数组排序
        enumerator = 排序后的数组
        综合排序后数组的模块名，返回
        
    for token in plugins
        plugin_loaded(this=lib->plugins, token)  //检查是否已经加载了
            this->plugins 的，带 filter=plugin_filter 的枚举器-
        如果 this->paths(插件搜索路径) 不为空
            this->paths->find_first(...,&file)  //将搜索到的文件路径存在 iile 中
        如果file为空，在默认路径中查找该文件
            path = "/usr/lib/ipsec/plugins"  //这下面放了各种插件的动态库
        得到 file = 要加载的插件动态库的具体路径
        critical = （插件列表中的插件后后面带!）？true:false
        plugin_entry_t *entry = load_plugin("插件名","插件动态库路径",critical) 
            默认加载特性 RTLD_LAZY
            plugin_entry_t *entry;  //参：file://../imgs/plugin_loader的plugins赋值.png
            create_plugin(handel=RTLD_DEFAULT=NULL,"插件名",integrity=FALSE,critical,&entry) 
                //在所有已加载的库(RTLD_DEFAULT)中搜索函数符号"插件名_plugin_create"，如：des_plugin_create
                将找到的函数指针村给 constructor
                if(integrity/*FALSE*/)
                    ...
                if( !constructor ) return NOT_FOUND;
                plugin_t *plugin = constructor();
                *entry.plugin = plugin
                *entry.critical = critical
                *entry.features = linked_list_create()
                return SUCESS
            上面函数返回成功
                this->plugins->insert_last(entry)
            if (lib->integrity /*=0*/)
                ...
            看配置项 charon.dlopen_use_rtld_now 是否为真
                如果为真，加载特性改为 RTLD_NOW
            加载特性加上 RTLD_NODELETE  //在dlclose ()期间不卸载库，并且在以后使用dlopen ()重新加载库时不初始化库中的静态变量
            void * handle = dlopen(file)
            create_plugin(...,&entry)   <参 file://../imgs/strongswan插件机制结构关系2.png>
                加载符号 插件名_plugin_create （构造函数）
                plugin_t *plugin 
                entry.plugin   = 插件名_plugin_create()  //调用插件的导出方法
                entry.features = linked_list_create()
            entry->handle = handle;
            this->plugins->insert_last(this->plugins, entry);
            return entry
        register_features(this=lib->plugins, entry)   
            //参：file://../imgs/strongswan插件机制结构关系2.png
            //这是plugin_loader.c中的函数
            //把从插件获取到的feature，添加到entry中；把entry记录到provided中; 
            //把provided放到registered中; 把registered放到this->features中
            //参：file://../imgs/plugin_loader的plugins赋值.png
            plugin_feature_t *feature,*reg
            entry->plugin->get_features(&feature)  //相应动态库中的函数，通过PLUGIN_REGISTER、PLUGIN_PROVIDE等宏创建的plugin_feature_t数组
            遍历 feature 数组
                feature->kind == FEATURE_PROVIDE
                    在 this->features 中找是否存在当前 feature  //使用 this->features->get，比较哈希
                        如果没有，就 
                            registered = new registered_feature_t
                            registered.feature = feature
                            registered.plugins =  linked_list_create()
                            将 registered 加入到 this->features
                    provided = new provided_feature_t
                        provided.entry = entry
                        provided.feature = feature
                        provided.reg = reg
                    registered->plugins->insert_last(provided)
                    entry->features->insert_last(provided)
                feature->kind == FEATURE_REGISTER / FEATURE_CALLBACK
                    reg = feature
    
    load_features(this)
        小结：
            1. 遍历 private_plugin_lodert_t -> plugins，每个列表元素指向一个 plugin_entry_t 结构
            2. 遍历 plugin_entry_t -> features，每个列表元素指向一个 provide_feature_t 结构
            3. 将得到的 rovide_feature_t 结构传给 load_provided 函数
            4. 在 load_provided 函数内
               4.1 得到插件的名字
                   可以通过 entry 成员指针，指回 plugin_entry_t 结构
                   再通过 plugin_entry_t 的 plugin 成员，可得到该插件的名字
               4.2 标记 provided->loading = TRUE，
              *4.3 调用 load_feature，把 provided 作为参数传入
                   4.3.1 在 load_feature 函数中先调用 load_dependencies ,把 provide 作为参数传入
                         4.3.1 load_dependencies 内部先遍历 provide 的 feature，从1开始，跳过 PROVIDE 型特性本身
                               如果碰到 FEATURE_DEPENDS 或 FEATURE_SDEPEND 之外的类型，就结束遍历
                               相关参考：file://plugin_feature_t.py@charon.features
                         4.3.2 在 private_plugin_loader_t 的 features 中找到'所有'与上面的 feature 匹配的项
                               如果能找到，则调用 load_registered 函数，并把该匹配项(registered_feature_t)作为参数传入
                               如果找不到配成的，输出提示信息
                               注1：这块代码是在5.1的循环中被调用的
                               注2：load_registered 内部枚举 registered->plugins,
                                    然后把枚举到的 provided_feature_t 结构传给 load_provided 函数进行递归调用
                   4.3.2 '执行'feature
                         plugin_feature_load(provided->entry->plugin, provided->feature,provided->reg)
                         如果是 FEATURE_CALLBACK，则进行回调函数的真正调用
                         否则，根据 feature->type，对相应的参数进行处理，支持的feature->type有：
                            lib->crypto支持的：
                                FEATURE_CRYPTER、FEATURE_AEAD、FEATURE_SIGNER、FEATURE_HASHER
                                FEATURE_PRF、FEATURE_XOF、FEATURE_DH、FEATURE_RNG、FEATURE_NONCE_GEN
                            lib->creds支持的：
                                FEATURE_PRIVKEY、FEATURE_PRIVKEY_GEN、FEATURE_PUBKEY、FEATURE_CERT_DECODE
                                FEATURE_CERT_ENCODE、FEATURE_CONTAINER_ENCODE、FEATURE_CONTAINER_DECODE
                            lib->db支持的：
                                FEATURE_DATABASE
                            lib->fetcher支持的：
                                FEATURE_FETCHER
                            lib->resolver支持的：
                                FEATURE_RESOLVER
                            其它像如 FEATURE_EAP_SERVER、FEATURE_XAUTH_SERVER、FEATURE_EAP_PEER等等，是该函数不支持的
               4.4 函数执行完后，标记 provided->loading = FALSE
            ●  综上，load_features函数的功能就是遍历private_plugin_lodert_t所有的plugins的所有的features，
               (在private_plugin_loader_t的features中找出匹配的)，按照依赖关系，执行所有插件的所有features
        //参：file://../imgs/plugin_loader的plugins赋值.png
        for plugin_entry_t : plugin in this->plugins  //遍历各个插件
            for provided_feature_t : provided in plugin->features  //遍历插件提供的各个特性(features)
                load_provided(provided)
                    name = plugin的名字
                    provide = 根据特性(features)的类型和值，组成的字符串
                    如果feature的loading标记为真
                        提示 "loop detected while loading $provide in plugin $name"
                        本函数返回
                    设feature的loading标记为真
                    load_feature(provided)
                        load_dependencies(provided)  //确保/使得依赖的特性/插件先完成加载，会递归调用load_provided()
                            遍历  provided->feature[]
                                判断 provided->feature[i].kind 不为 FEATURE_DEPENDS 或 FEATURE_SDEPEND
                                    结束本循环
                                registered = 在 private_plugin_loader_t 中的 features 中，找到匹配的feature
                                if(registered) load_registered(registered)
                                    for provided_feature_t : provided in registered->plugins
                                        load_provided(provided)
                                            if(provided->loaded || provided->failed) return;
                                            name = 对应插件的名字
                                            provide = 根据特性(features)的类型和值，组成的字符串
                                            如果feature的loading标记为真
                                                提示 "loop detected while loading $provide in plugin $name"
                                                本函数返回
                                            。。。
                            函数退出
                        plugin_feature_load(plugin=provided->entry->plugin, feature=provided->feature, reg=provided->reg)
                            if(reg is NULL) return TRUE;  //此时无需处理该feature
                            provided->reg->kind == FEATURE_CALLBACK
                                provided->reg->arg.cb.f(plugin,feature,TRUE/*注册与注销*/,reg->arg.cb.data)  //插件提供的函数
                            provided->reg->kind == FEATURE_REGISTER
                                switch (provided->feature->type)
                                    根据不同的情况，调用如下函数中的一种：
                                        lib->crypto->add_crypter
                                        lib->crypto->add_aead
                                        lib->crypto->add_signer
                                        lib->crypto->add_hasher
                                        lib->crypto->add_prf
                                        lib->crypto->add_xof
                                        lib->crypto->add_dh
                                        lib->crypto->add_rng
                                        lib->crypto->add_nonce_gen
                                        lib->creds->add_builder
                                        lib->db->add_database
                                        lib->fetcher->add_fetcher
                                        lib->resolver->add_resolver
                        provided->loaded = TRUE;
                        this->loaded->insert_first(provided)
                    feature的loading标记为假
        purge_plugins(private_plugin_loader_t *this)
            小结：
                遍历this->plugins链表中的那些entry，如果该entry的第一项(provided_feature_t)的loaded标志项为false
                则释放该entry（包括关闭动态库），并释放this->plugins和this->features中，与该entry关联的项
            for entry in this->plugins
                如果该entry中，features列表的第一项(provided_feature_t)的loaded标志项为false，
                    this->plugins中删除该entry项  //从插件管理器的plugins中移除
                    unregister_features(private_plugin_loader_t *this, plugin_entry_t *entry)
                        for provided in entry->features
                            entry->features->remove_at(provided)  //从entry的features中移除
                            unregister_feature(this, provided)
                                registered_feature_t *registered = this->features->get(provided)
                                registered->plugins->remove(provided)  //通常registered->plugins只存一个节点
                                判断registered->plugins是否为空
                                    this->features->remove(provided->feature)  //从插件管理器的features中移除
                                    registerde->plugins->destory()     //销毁链表
                    plugin_entry_destroy(entry);
                        if(entry->handle)  dlclose(entry->handle)
                        entry->features->destroy()      //销毁entry->features链表
                        释放entry
        this->loaded_plugins = loaded_plugins_list(this);
            遍历this->plugins，获取其名字，组成名字列表
                
                                    
                                    