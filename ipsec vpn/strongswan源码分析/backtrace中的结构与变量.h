/**
 * A backtrace registers the frames on the stack during creation.
 */
struct backtrace_t {

	/**
	 * Log the backtrace to a FILE stream.
	 *
	 * If no file pointer is given, the backtrace is reported over the debug
	 * framework to the registered dbg() callback function.
	 *
	 * @param file		FILE to log backtrace to, NULL for dbg() function
	 * @param detailed	TRUE to resolve line/file using addr2line (slow)
	 */
	void (*log)(backtrace_t *this, FILE *file, bool detailed);

	/**
	 * Check if the backtrace contains a frame having a function in a list.
	 *
	 * @param		function name array
	 * @param		number of elements in function array
	 * @return		TRUE if one of the functions is in the stack
	 */
	bool (*contains_function)(backtrace_t *this, char *function[], int count);

	/**
	 * Check two backtraces for equality.
	 *
	 * @param other	backtrace to compare to this
	 * @return		TRUE if backtraces are equal
	 */
	bool (*equals)(backtrace_t *this, backtrace_t *other);

	/**
	 * Create a copy of this backtrace.
	 *
	 * @return		cloned copy
	 */
	backtrace_t* (*clone)(backtrace_t *this);

	/**
	 * Create an enumerator over the stack frame addresses.
	 *
	 * @return		enumerator_t over void*
	 */
	enumerator_t* (*create_frame_enumerator)(backtrace_t *this);

	/**
	 * Destroy a backtrace instance.
	 */
	void (*destroy)(backtrace_t *this);
};


======================================================================

/**
 * Mutex to access non-thread-safe dbghelp functions
 */
static mutex_t *dbghelp_mutex;
/**
 * bfd entry cache
 */
static hashtable_t *bfds;

static mutex_t *bfd_mutex;

/**
 * Private data of an backtrace_t object.
 */
struct private_backtrace_t {

	/**
	 * Public backtrace_t interface.
	 */
	backtrace_t public;

	/**
	 * Number of stacks frames obtained in stack_frames
	 */
	int frame_count;

	/**
	 * Recorded stack frames.
	 */
	void *frames[];   //维护一个frames数组
};

typedef struct {
	/** binary file name on disk */
	char *filename;
	/** bfd handle */
	bfd *abfd;
	/** loaded symbols */
	asymbol **syms;
} bfd_entry_t;

typedef struct {
	/** used bfd entry */
	bfd_entry_t *entry;
	/** backtrace address */
	bfd_vma vma;
	/** stream to log to */
	FILE *file;
	/** TRUE if complete */
	bool found;
} bfd_find_data_t;