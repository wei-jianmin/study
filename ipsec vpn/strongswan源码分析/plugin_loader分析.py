ͼ��file://../imgs/strongswan������ƽṹ��ϵ.png
�ģ�file://plugin_feature�еĽṹ�����.h
load_plugins
    char* plugins = modular_pluginlist(list); //���������ļ�����ݲ���������Ĭ��ֵ���õ�Ҫ���ص�ģ�飬�����ȼ�����
        listΪ�������������ù̶�ֵ <�Σ�file://strongswan��Ҫ���̼����ݽṹ.py@pluginsֵ>
        �������ļ���charon.load_moudlar��Ĭ��ֵΪFALSE��������ɹ�
            enumerator = �����ļ���charon.plugins
            load_def = FALSE
        ����
            enumerator = ����ͨ�� plugins �õ�������
            load_def = TRUE
        �� charon.plugins.enumerator.load �������Ϊ���ȼ� prio��Ĭ��0��
        ��� prio Ϊ 0
            ��� load_def=FALSE��prio = 1 ��prio�����ֵΪ���������Ԫ�ظ�����
        ���������������
        enumerator = ����������
        �ۺ�����������ģ����������
        
    for token in plugins
        plugin_loaded(this=lib->plugins, token)  //����Ƿ��Ѿ�������
            this->plugins �ģ��� filter=plugin_filter ��ö����-
        ��� this->paths(�������·��) ��Ϊ��
            this->paths->find_first(...,&file)  //�����������ļ�·������ iile ��
        ���fileΪ�գ���Ĭ��·���в��Ҹ��ļ�
            path = "/usr/lib/ipsec/plugins"  //��������˸��ֲ���Ķ�̬��
        �õ� file = Ҫ���صĲ����̬��ľ���·��
        critical = ������б��еĲ��������!����true:false
        plugin_entry_t *entry = load_plugin("�����","�����̬��·��",critical) 
            Ĭ�ϼ������� RTLD_LAZY
            plugin_entry_t *entry;  //�Σ�file://../imgs/plugin_loader��plugins��ֵ.png
            create_plugin(handel=RTLD_DEFAULT=NULL,"�����",integrity=FALSE,critical,&entry) 
                //�������Ѽ��صĿ�(RTLD_DEFAULT)��������������"�����_plugin_create"���磺des_plugin_create
                ���ҵ��ĺ���ָ���� constructor
                if(integrity/*FALSE*/)
                    ...
                if( !constructor ) return NOT_FOUND;
                plugin_t *plugin = constructor();
                *entry.plugin = plugin
                *entry.critical = critical
                *entry.features = linked_list_create()
                return SUCESS
            ���溯�����سɹ�
                this->plugins->insert_last(entry)
            if (lib->integrity /*=0*/)
                ...
            �������� charon.dlopen_use_rtld_now �Ƿ�Ϊ��
                ���Ϊ�棬�������Ը�Ϊ RTLD_NOW
            �������Լ��� RTLD_NODELETE  //��dlclose ()�ڼ䲻ж�ؿ⣬�������Ժ�ʹ��dlopen ()���¼��ؿ�ʱ����ʼ�����еľ�̬����
            void * handle = dlopen(file)
            create_plugin(...,&entry)   <�� file://../imgs/strongswan������ƽṹ��ϵ2.png>
                ���ط��� �����_plugin_create �����캯����
                plugin_t *plugin 
                entry.plugin   = �����_plugin_create()  //���ò���ĵ�������
                entry.features = linked_list_create()
            entry->handle = handle;
            this->plugins->insert_last(this->plugins, entry);
            return entry
        register_features(this=lib->plugins, entry)   
            //�Σ�file://../imgs/strongswan������ƽṹ��ϵ2.png
            //����plugin_loader.c�еĺ���
            //�ѴӲ����ȡ����feature����ӵ�entry�У���entry��¼��provided��; 
            //��provided�ŵ�registered��; ��registered�ŵ�this->features��
            //�Σ�file://../imgs/plugin_loader��plugins��ֵ.png
            plugin_feature_t *feature,*reg
            entry->plugin->get_features(&feature)  //��Ӧ��̬���еĺ�����ͨ��PLUGIN_REGISTER��PLUGIN_PROVIDE�Ⱥ괴����plugin_feature_t����
            ���� feature ����
                feature->kind == FEATURE_PROVIDE
                    �� this->features �����Ƿ���ڵ�ǰ feature  //ʹ�� this->features->get���ȽϹ�ϣ
                        ���û�У��� 
                            registered = new registered_feature_t
                            registered.feature = feature
                            registered.plugins =  linked_list_create()
                            �� registered ���뵽 this->features
                    provided = new provided_feature_t
                        provided.entry = entry
                        provided.feature = feature
                        provided.reg = reg
                    registered->plugins->insert_last(provided)
                    entry->features->insert_last(provided)
                feature->kind == FEATURE_REGISTER / FEATURE_CALLBACK
                    reg = feature
    
    load_features(this)
        С�᣺
            1. ���� private_plugin_lodert_t -> plugins��ÿ���б�Ԫ��ָ��һ�� plugin_entry_t �ṹ
            2. ���� plugin_entry_t -> features��ÿ���б�Ԫ��ָ��һ�� provide_feature_t �ṹ
            3. ���õ��� rovide_feature_t �ṹ���� load_provided ����
            4. �� load_provided ������
               4.1 �õ����������
                   ����ͨ�� entry ��Աָ�룬ָ�� plugin_entry_t �ṹ
                   ��ͨ�� plugin_entry_t �� plugin ��Ա���ɵõ��ò��������
               4.2 ��� provided->loading = TRUE��
              *4.3 ���� load_feature���� provided ��Ϊ��������
                   4.3.1 �� load_feature �������ȵ��� load_dependencies ,�� provide ��Ϊ��������
                         4.3.1 load_dependencies �ڲ��ȱ��� provide �� feature����1��ʼ������ PROVIDE �����Ա���
                               ������� FEATURE_DEPENDS �� FEATURE_SDEPEND ֮������ͣ��ͽ�������
                               ��زο���file://plugin_feature_t.py@charon.features
                         4.3.2 �� private_plugin_loader_t �� features ���ҵ�'����'������� feature ƥ�����
                               ������ҵ�������� load_registered ���������Ѹ�ƥ����(registered_feature_t)��Ϊ��������
                               ����Ҳ�����ɵģ������ʾ��Ϣ
                               ע1������������5.1��ѭ���б����õ�
                               ע2��load_registered �ڲ�ö�� registered->plugins,
                                    Ȼ���ö�ٵ��� provided_feature_t �ṹ���� load_provided �������еݹ����
                   4.3.2 'ִ��'feature
                         plugin_feature_load(provided->entry->plugin, provided->feature,provided->reg)
                         ����� FEATURE_CALLBACK������лص���������������
                         ���򣬸��� feature->type������Ӧ�Ĳ������д���֧�ֵ�feature->type�У�
                            lib->crypto֧�ֵģ�
                                FEATURE_CRYPTER��FEATURE_AEAD��FEATURE_SIGNER��FEATURE_HASHER
                                FEATURE_PRF��FEATURE_XOF��FEATURE_DH��FEATURE_RNG��FEATURE_NONCE_GEN
                            lib->creds֧�ֵģ�
                                FEATURE_PRIVKEY��FEATURE_PRIVKEY_GEN��FEATURE_PUBKEY��FEATURE_CERT_DECODE
                                FEATURE_CERT_ENCODE��FEATURE_CONTAINER_ENCODE��FEATURE_CONTAINER_DECODE
                            lib->db֧�ֵģ�
                                FEATURE_DATABASE
                            lib->fetcher֧�ֵģ�
                                FEATURE_FETCHER
                            lib->resolver֧�ֵģ�
                                FEATURE_RESOLVER
                            �������� FEATURE_EAP_SERVER��FEATURE_XAUTH_SERVER��FEATURE_EAP_PEER�ȵȣ��Ǹú�����֧�ֵ�
               4.4 ����ִ����󣬱�� provided->loading = FALSE
            ��  ���ϣ�load_features�����Ĺ��ܾ��Ǳ���private_plugin_lodert_t���е�plugins�����е�features��
               (��private_plugin_loader_t��features���ҳ�ƥ���)������������ϵ��ִ�����в��������features
        //�Σ�file://../imgs/plugin_loader��plugins��ֵ.png
        for plugin_entry_t : plugin in this->plugins  //�����������
            for provided_feature_t : provided in plugin->features  //��������ṩ�ĸ�������(features)
                load_provided(provided)
                    name = plugin������
                    provide = ��������(features)�����ͺ�ֵ����ɵ��ַ���
                    ���feature��loading���Ϊ��
                        ��ʾ "loop detected while loading $provide in plugin $name"
                        ����������
                    ��feature��loading���Ϊ��
                    load_feature(provided)
                        load_dependencies(provided)  //ȷ��/ʹ������������/�������ɼ��أ���ݹ����load_provided()
                            ����  provided->feature[]
                                �ж� provided->feature[i].kind ��Ϊ FEATURE_DEPENDS �� FEATURE_SDEPEND
                                    ������ѭ��
                                registered = �� private_plugin_loader_t �е� features �У��ҵ�ƥ���feature
                                if(registered) load_registered(registered)
                                    for provided_feature_t : provided in registered->plugins
                                        load_provided(provided)
                                            if(provided->loaded || provided->failed) return;
                                            name = ��Ӧ���������
                                            provide = ��������(features)�����ͺ�ֵ����ɵ��ַ���
                                            ���feature��loading���Ϊ��
                                                ��ʾ "loop detected while loading $provide in plugin $name"
                                                ����������
                                            ������
                            �����˳�
                        plugin_feature_load(plugin=provided->entry->plugin, feature=provided->feature, reg=provided->reg)
                            if(reg is NULL) return TRUE;  //��ʱ���账���feature
                            provided->reg->kind == FEATURE_CALLBACK
                                provided->reg->arg.cb.f(plugin,feature,TRUE/*ע����ע��*/,reg->arg.cb.data)  //����ṩ�ĺ���
                            provided->reg->kind == FEATURE_REGISTER
                                switch (provided->feature->type)
                                    ���ݲ�ͬ��������������º����е�һ�֣�
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
                    feature��loading���Ϊ��
        purge_plugins(private_plugin_loader_t *this)
            С�᣺
                ����this->plugins�����е���Щentry�������entry�ĵ�һ��(provided_feature_t)��loaded��־��Ϊfalse
                ���ͷŸ�entry�������رն�̬�⣩�����ͷ�this->plugins��this->features�У����entry��������
            for entry in this->plugins
                �����entry�У�features�б�ĵ�һ��(provided_feature_t)��loaded��־��Ϊfalse��
                    this->plugins��ɾ����entry��  //�Ӳ����������plugins���Ƴ�
                    unregister_features(private_plugin_loader_t *this, plugin_entry_t *entry)
                        for provided in entry->features
                            entry->features->remove_at(provided)  //��entry��features���Ƴ�
                            unregister_feature(this, provided)
                                registered_feature_t *registered = this->features->get(provided)
                                registered->plugins->remove(provided)  //ͨ��registered->pluginsֻ��һ���ڵ�
                                �ж�registered->plugins�Ƿ�Ϊ��
                                    this->features->remove(provided->feature)  //�Ӳ����������features���Ƴ�
                                    registerde->plugins->destory()     //��������
                    plugin_entry_destroy(entry);
                        if(entry->handle)  dlclose(entry->handle)
                        entry->features->destroy()      //����entry->features����
                        �ͷ�entry
        this->loaded_plugins = loaded_plugins_list(this);
            ����this->plugins����ȡ�����֣���������б�
                
                                    
                                    