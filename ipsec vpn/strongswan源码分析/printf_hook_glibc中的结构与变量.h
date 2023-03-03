/**
 * Argument types to pass to printf hook.
 */
enum printf_hook_argtype_t {
	PRINTF_HOOK_ARGTYPE_END,
	PRINTF_HOOK_ARGTYPE_INT,
	PRINTF_HOOK_ARGTYPE_POINTER,
};

/**
 * Properties of the format specifier
 */
struct printf_hook_spec_t {

	/**
	 * TRUE if a '#' was used in the format specifier
	 */
	int hash;

	/**
	 * TRUE if a '-' was used in the format specifier
	 */
	int minus;

	/**
	 * TRUE if a '+' was used in the format specifier
	 */
	int plus;

	/**
	 * The width as given in the format specifier.
	 */
	int width;
};

/**
 * Printf handler management.
 */
struct printf_hook_t {

	/**
	 * Register a printf handler.
	 *
	 * @param spec		printf hook format character
	 * @param hook		hook function
	 * @param ...		list of PRINTF_HOOK_ARGTYPE_*, MUST end with PRINTF_HOOK_ARGTYPE_END
	 */
	void (*add_handler)(printf_hook_t *this, char spec,
						printf_hook_function_t hook, ...);

	/**
	 * Destroy a printf_hook instance.
	 */
	void (*destroy)(printf_hook_t *this);
};

============================================================

static printf_hook_handler_t *printf_hooks[58];

/**
 * private data of printf_hook
 */
struct private_printf_hook_t {

	/**
	 * public functions
	 */
	printf_hook_t public;
};

/**
 * struct with information about a registered handler
 */
struct printf_hook_handler_t {

	/**
	 * callback function
	 */
	printf_hook_function_t hook;

	/**
	 * number of arguments
	 */
	int numargs;

	/**
	 * types of the arguments, PA_*
	 */
	int argtypes[3];
};

/**
 * Data to pass to a printf hook.
 */
struct printf_hook_data_t {

	/**
	 * Output FILE stream
	 */
	FILE *stream;;
};