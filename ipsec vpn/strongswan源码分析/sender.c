/**
 * Private data of a sender_t object.
 */
struct private_sender_t {
	//Public part of a sender_t object. 
	sender_t public;
	//The packets are stored in a linked list 
	linked_list_t *list;
	//mutex to synchronize access to list 
	mutex_t *mutex;
	//condvar to signal for packets added to list 
	condvar_t *got;
	//condvar to signal for packets sent 
	condvar_t *sent;
	//Delay for sending outgoing packets, to simulate larger RTT 
	int send_delay;
	//Specific message type to delay, 0 for any 
	int send_delay_type;
	//Delay request messages? 
	bool send_delay_request;
	//Delay response messages? 
	bool send_delay_response;
};

=======================================================

sender_t * sender_create()
{
	private_sender_t *this;
	INIT(this,
		.public = {
			.send = _send_,
			.send_no_marker = _send_no_marker,
			.flush = _flush,
			.destroy = _destroy,
		},
		.list = linked_list_create(),
		.mutex = mutex_create(MUTEX_TYPE_DEFAULT),
		.got = condvar_create(CONDVAR_TYPE_DEFAULT),
		.sent = condvar_create(CONDVAR_TYPE_DEFAULT),
		.send_delay = lib->settings->get_int(lib->settings,
									"%s.send_delay", 0, lib->ns),
		.send_delay_type = lib->settings->get_int(lib->settings,
									"%s.send_delay_type", 0, lib->ns),
		.send_delay_request = lib->settings->get_bool(lib->settings,
									"%s.send_delay_request", TRUE, lib->ns),
		.send_delay_response = lib->settings->get_bool(lib->settings,
									"%s.send_delay_response", TRUE, lib->ns),
	);
	lib->processor->queue_job(lib->processor,
		(job_t*)callback_job_create_with_prio((callback_job_cb_t)send_packets,
			this, NULL, (callback_job_cancel_t)return_false, JOB_PRIO_CRITICAL));
	return &this->public;
}