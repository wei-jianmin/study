后端（Backends）是一个提供配置信息的可插拔模块/插件模块（pluggable modules）
它必须提供一个（？一组）api，以供守护进程来读取配置信息
They have to implement an API which the daemon core uses to get configuration

在 stroke_socket_create 中
    创建并初始化了 private_stroke_socket_t 对象
    该对象含有（并创建、初始化了）cred（内存证书）、ca（ipsec.conf/ca）、config（内存配置backend--管理内存中的配置）、
    attribute（IKEv2 cfg attribute provider）、list、uri、service（Service accepting stroke connections）等等成员
    其中，config 成员会同时添加到 charon->backends 中（其它的，如ca、cred会同时添加到 lib->credmgr 中）
    由此可见，backends起到对加载到内存的配置的管理（读取）的用处
    
在 register_vici 中  
    为已存在的 vici （private_vici_plugin_t）创建了 
    query、control、cred、authority、config、attrs 等等成员对象
    他们的功能分别是：
        query：      Query helper, provides various commands to query/list daemon info.
        control：    Control helper, provides initiate/terminate and other commands.
        cred：       In-memory credential backend, managed by VICI.
        authority：  In-memory certification authority backend, managed by VICI.
        config：     In-memory configuration backend, managed by VICI.
        attr：       IKE configuration attribute backend for vici.
    其中，config会添加到charon->backends（其他的，如 attrs->provider会添加到charon->attributes等）
    同上，backends起到对加载到内存的配置的管理（读取）的用处