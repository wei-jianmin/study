// Libstrongswan �������ģ���������ص�ȫ�ֱ���
struct library_t {
	// ��ȡ������ע����������
	void* (*get)(library_t *this, char *name);
	// [ȡ��]ʹ�ø�������ע���������
	bool (*set)(library_t *this, char *name, void *object);
	// Namespace used for settings etc.����ʹ�ÿ�Ķ������ļ������ƣ�
	const char *ns;
	// ���� library_init() ����Ҫ�����ļ�, the default, or NULL
	char *conf;
	// Printf �ҹ�ע�Ṥ��
	printf_hook_t *printf_hook;
	// Proposal keywords registry���᰸�ؼ���ע���
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
	// URL ��ȡ����
	fetcher_manager_t *fetcher;
	// DNS ������������
	resolver_manager_t *resolver;
	// ���ݿ⽨�칤��
	database_factory_t *db;
	// ������ع���
	plugin_loader_t *plugins;
	// ʹ���̳߳ش�����ҵ
	processor_t *processor;
	// schedule jobs
	scheduler_t *scheduler;
	// �ļ����������
	watcher_t *watcher;
	// Streams and Services
	stream_manager_t *streams;
	// ͨ�� DNS ���ƽ�������
	host_resolver_t *hosts;
	// �������ļ����صĸ�������
	settings_t *settings;
	// ������֤���������Ե������Լ����
	integrity_checker_t *integrity;
	// й©�����������ѹ��������ã�
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
	refcount_t ref; // ���ü���
#ifdef LEAK_DETECTIVE
	FILE *ld_out;   // Where to write leak detective output to
#endif
};

