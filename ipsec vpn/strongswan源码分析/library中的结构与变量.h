// Libstrongswan 库上下文，包含库相关的全局变量
struct library_t {
	// 获取按名称注册的任意对象
	void* (*get)(library_t *this, char *name);
	// [取消]使用给定名称注册任意对象
	bool (*set)(library_t *this, char *name, void *object);
	// Namespace used for settings etc.（即使用库的二进制文件的名称）
	const char *ns;
	// 传给 library_init() 的主要配置文件, the default, or NULL
	char *conf;
	// Printf 挂钩注册工具
	printf_hook_t *printf_hook;
	// Proposal keywords registry（提案关键字注册表）
	proposal_keywords_t *proposal;
	// POSIX capability dropping
	capabilities_t *caps;
	// crypto algorithm registry and factory
	crypto_factory_t *crypto;
	// credential constructor registry and factory
	credential_factory_t *creds;
	// Manager for the credential set backends
	credential_manager_t *credmgr;
	// Credential encoding registry and factory
	cred_encoding_t *encoding;
	// URL 获取工具
	fetcher_manager_t *fetcher;
	// DNS 解析器管理器
	resolver_manager_t *resolver;
	// 数据库建造工厂
	database_factory_t *db;
	// 插件加载工具
	plugin_loader_t *plugins;
	// 使用线程池处理作业
	processor_t *processor;
	// schedule jobs
	scheduler_t *scheduler;
	// 文件描述符监控
	watcher_t *watcher;
	// Streams and Services
	stream_manager_t *streams;
	// 通过 DNS 名称解析主机
	host_resolver_t *hosts;
	// 从设置文件加载的各种设置
	settings_t *settings;
	// 用于验证代码完整性的完整性检查器
	integrity_checker_t *integrity;
	// 泄漏检测器（如果已构建并启用）
	leak_detective_t *leak_detective;
};

------------------------------------------------------------------------------

static char *namespaces[MAX_NAMESPACES];
static int ns_count;
library_t *lib = NULL;

struct private_library_t {
	library_t public;
	hashtable_t *objects;   // Hashtable with registered objects (name => object)
	bool init_failed;   // Integrity check failed?
	refcount_t ref; // 引用计数
#ifdef LEAK_DETECTIVE
	FILE *ld_out;   // Where to write leak detective output to
#endif
};

