/**
 * Flag to indicate signaled wait_sigint()
 */
static bool sigint_signaled = FALSE;

/**
 * Condvar to wait in wait_sigint()
 */
static condvar_t *sigint_cond;

/**
 * Mutex to check signaling()
 */
static mutex_t *sigint_mutex;

struct linux_dirent64 {
	uint64_t d_ino;
	int64_t d_off;
	unsigned short	d_reclen;
	unsigned char d_type;
	char d_name[256];
};