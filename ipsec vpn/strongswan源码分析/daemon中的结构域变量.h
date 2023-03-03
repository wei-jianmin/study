/**
 * Main class of daemon, contains some globals.
 */
struct daemon_t {

	/**
	 * Socket manager instance
	 */
	socket_manager_t *socket;

	/**
	 * Kernel interface to communicate with kernel
	 */
	kernel_interface_t *kernel;

	/**
	 * A ike_sa_manager_t instance.
	 */
	ike_sa_manager_t *ike_sa_manager;

	/**
	 * A child_sa_manager_t instance.
	 */
	child_sa_manager_t *child_sa_manager;

	/**
	 * Manager for triggering policies, called traps
	 */
	trap_manager_t *traps;

	/**
	 * Manager for shunt PASS|DROP policies
	 */
	shunt_manager_t *shunts;

	/**
	 * Manager for IKE redirect providers
	 */
	redirect_manager_t *redirect;

	/**
	 * Manager for the different configuration backends.
	 */
	backend_manager_t *backends;

	/**
	 * The Sender-Thread.
	 */
	sender_t *sender;

	/**
	 * The Receiver-Thread.
	 */
	receiver_t *receiver;

	/**
	 * Manager for IKE configuration attributes
	 */
	attribute_manager_t *attributes;

	/**
	 * The signaling bus.
	 */
	bus_t *bus;

	/**
	 * Controller to control the daemon
	 */
	controller_t *controller;

	/**
	 * EAP manager to maintain registered EAP methods
	 */
	eap_manager_t *eap;

	/**
	 * XAuth manager to maintain registered XAuth methods
	 */
	xauth_manager_t *xauth;

#ifdef ME
	/**
	 * Connect manager
	 */
	connect_manager_t *connect_manager;

	/**
	 * Mediation manager
	 */
	mediation_manager_t *mediation_manager;
#endif /* ME */

	/**
	 * Initialize the daemon.
	 *
	 * @param plugins	list of plugins to load
	 * @return			TRUE, if successful
	 */
	bool (*initialize)(daemon_t *this, char *plugins);

	/**
	 * Starts the daemon, i.e. spawns the threads of the thread pool.
	 */
	void (*start)(daemon_t *this);

	/**
	 * Load/Reload loggers defined in strongswan.conf
	 *
	 * If none are defined in strongswan.conf default loggers configured via
	 * set_default_loggers() are loaded.
	 */
	void (*load_loggers)(daemon_t *this);

	/**
	 * Configure default loggers if none are defined in strongswan.conf
	 *
	 * @param levels	debug levels used to create default loggers if none are
	 *					defined in strongswan.conf (NULL to disable)
	 * @param to_stderr	TRUE to log to stderr/stdout if no loggers are defined
	 * 					in strongswan.conf (logging to syslog is always enabled)
	 */
	void (*set_default_loggers)(daemon_t *this, level_t levels[DBG_MAX],
								bool to_stderr);

	/**
	 * Set the log level for the given log group for all loaded loggers.
	 *
	 * This change is not persistent and gets reset if loggers are reloaded
	 * via load_loggers().
	 *
	 * @param group		log group
	 * @param level		log level
	 */
	void (*set_level)(daemon_t *this, debug_t group, level_t level);
};

========================================================================

daemon_t *charon;

/**
 * hook in library for debugging messages
 */
extern void (*dbg) (debug_t group, level_t level, char *fmt, ...);

/**
 * we store the previous debug function so we can reset it
 */
static void (*dbg_old) (debug_t group, level_t level, char *fmt, ...);

/**
 * Static array for logger registration using __attribute__((constructor))
 */
static custom_logger_entry_t custom_loggers[MAX_CUSTOM_LOGGERS];
static int custom_logger_count;

========================================================================

/**
 * Private additions to daemon_t, contains threads and internal functions.
 */
struct private_daemon_t {
	/**
	 * Public members of daemon_t.
	 */
	daemon_t public;

	/**
	 * Handler for kernel events
	 */
	kernel_handler_t *kernel_handler;

	/**
	 * A list of installed loggers (as logger_entry_t*)
	 */
	linked_list_t *loggers;

	/**
	 * Cached log levels for default loggers
	 */
	level_t *levels;

	/**
	 * Whether to log to stdout/err by default
	 */
	bool to_stderr;

	/**
	 * Identifier used for syslog (in the openlog call)
	 */
	char *syslog_identifier;

	/**
	 * Mutex for configured loggers
	 */
	mutex_t *mutex;

	/**
	 * Integrity check failed?
	 */
	bool integrity_failed;

	/**
	 * Number of times we have been initialized
	 */
	refcount_t ref;
};

/**
 * Data for registered custom loggers
 */
typedef struct {
	/**
	 * Name of the custom logger (also used for loglevel configuration)
	 */
	char *name;

	/**
	 * Constructor to be called for custom logger creation
	 */
	custom_logger_constructor_t constructor;  //º¯ÊýÖ¸Õë

} custom_logger_entry_t;

/**
 * Types of supported loggers
 */
typedef enum {
	/**
	 * Syslog logger instance
	 */
	SYS_LOGGER,

	/**
	 * File logger instance
	 */
	FILE_LOGGER,

	/**
	 * Custom logger instance
	 */
	CUSTOM_LOGGER,

} logger_type_t;

/**
 * Some metadata about configured loggers
 */
typedef struct {
	/**
	 * Target of the logger (syslog facility or filename)
	 */
	char *target;

	/**
	 * Type of logger
	 */
	logger_type_t type;

	/**
	 * The actual logger
	 */
	union {
		sys_logger_t *sys;
		file_logger_t *file;
		custom_logger_t *custom;
	} logger;

} logger_entry_t;