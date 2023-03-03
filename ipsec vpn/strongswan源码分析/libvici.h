/**
 * Event registration
 */
typedef struct {
	/** name of event */
	char *name;
	/** callback function */
	vici_event_cb_t cb;
	/** user data for callback */
	void *user;
} event_t;

/**
 * Wait state signaled by asynchronous on_read callback
 */
typedef enum {
	WAIT_IDLE = 0,
	WAIT_SUCCESS,
	WAIT_FAILURE,
	WAIT_READ_ERROR,
} wait_state_t;

/**
 * Private vici connection contex.
 */
struct vici_conn_t {
	/** connection stream */
	stream_t *stream;
	/** event registrations, as char* => event_t */
	hashtable_t *events;
	/** connection lock */
	mutex_t *mutex;
	/** condvar to signal incoming response */
	condvar_t *cond;
	/** queued response message */
	chunk_t queue;
	/** asynchronous read error */
	int error;
	/** wait state */
	wait_state_t wait;
};

/**
 * Private vici request message.
 */
struct vici_req_t {
	/** connection context */
	vici_conn_t *conn;
	/** name of request message */
	char *name;
	/** message builder */
	vici_builder_t *b;
};

/**
 * Private vici response/event message.
 */
struct vici_res_t {
	/** response message */
	vici_message_t *message;
	/** allocated strings */
	linked_list_t *strings;
	/** item enumerator */
	enumerator_t *enumerator;
	/** currently enumerating type */
	vici_type_t type;
	/** currently enumerating name */
	char *name;
	/** currently enumerating value */
	chunk_t value;
	/** section nesting level of callback parser */
	int level;
};