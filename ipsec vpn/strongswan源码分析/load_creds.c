/**
 * Context used to track loaded secrets
 */
struct load_ctx_t{
	/** vici connection */
	vici_conn_t *conn;
	/** format options */
	command_format_options_t format;
	/** read setting */
	settings_t *cfg;
	/** don't prompt user for password */
	bool noprompt;
	/** list of key ids of loaded private keys */
	hashtable_t *keys;
	/** list of unique ids of loaded shared keys */
	hashtable_t *shared;
};