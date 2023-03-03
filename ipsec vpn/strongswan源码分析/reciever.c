struct private_receiver_t {
	// Public part of a receiver_t object. 
	receiver_t public;
	// Registered callback for ESP packets 
	struct {
		receiver_esp_cb_t cb;
		void *data;
	} esp_cb;
	// Mutex for ESP callback 
	mutex_t *esp_cb_mutex;
	// current secret to use for cookie calculation 
	char secret[SECRET_LENGTH];
	// previous secret used to verify older cookies 
	char secret_old[SECRET_LENGTH];
	// how many times we have used "secret" so far 
	uint32_t secret_used;
	// time we did the cookie switch 
	uint32_t secret_switch;
	// time offset to use, hides our system time 
	uint32_t secret_offset;
	// the RNG to use for secret generation 
	rng_t *rng;
	// hasher to use for cookie calculation 
	hasher_t *hasher;
	// require cookies after this many half open IKE_SAs 
	uint32_t cookie_threshold;
	// timestamp of last cookie requested 
	time_t last_cookie;
	// how many half open IKE_SAs per peer before blocking 
	uint32_t block_threshold;
	// Drop IKE_SA_INIT requests if processor job load exceeds this limit 
	u_int init_limit_job_load;
	// Drop IKE_SA_INIT requests if half open IKE_SA count exceeds this limit 
	u_int init_limit_half_open;
	// Delay for receiving incoming packets, to simulate larger RTT 
	int receive_delay;
	// Specific message type to delay, 0 for any 
	int receive_delay_type;
	// Delay request messages? 
	bool receive_delay_request;
	// Delay response messages? 
	bool receive_delay_response;
	// Endpoint is allowed to act as an initiator only 
	bool initiator_only;
};

=============================================================================

//创建出来的 private_receiver_t，cb成员是空的，通过add_esp_cb添加
//在 kernel_libipsec_router.c:kernel_libipsec_router_create()中，调用了add_esp_cb
receiver_t *receiver_create()
{
	private_receiver_t *this;
	uint32_t now = time_monotonic(NULL);

	INIT(this,
		.public = {
			.add_esp_cb = _add_esp_cb,
			.del_esp_cb = _del_esp_cb,
			.destroy = _destroy,
		},
		.esp_cb_mutex = mutex_create(MUTEX_TYPE_DEFAULT),
		.secret_switch = now,
		.secret_offset = random() % now,
	);

	if (lib->settings->get_bool(lib->settings,
								"%s.dos_protection", TRUE, lib->ns))
	{
		this->cookie_threshold = lib->settings->get_int(lib->settings,
					"%s.cookie_threshold", COOKIE_THRESHOLD_DEFAULT, lib->ns);
		this->block_threshold = lib->settings->get_int(lib->settings,
					"%s.block_threshold", BLOCK_THRESHOLD_DEFAULT, lib->ns);
	}
	this->init_limit_job_load = lib->settings->get_int(lib->settings,
					"%s.init_limit_job_load", 0, lib->ns);
	this->init_limit_half_open = lib->settings->get_int(lib->settings,
					"%s.init_limit_half_open", 0, lib->ns);
	this->receive_delay = lib->settings->get_int(lib->settings,
					"%s.receive_delay", 0, lib->ns);
	this->receive_delay_type = lib->settings->get_int(lib->settings,
					"%s.receive_delay_type", 0, lib->ns);
	this->receive_delay_request = lib->settings->get_bool(lib->settings,
					"%s.receive_delay_request", TRUE, lib->ns);
	this->receive_delay_response = lib->settings->get_bool(lib->settings,
					"%s.receive_delay_response", TRUE, lib->ns);
	this->initiator_only = lib->settings->get_bool(lib->settings,
					"%s.initiator_only", FALSE, lib->ns);

	this->hasher = lib->crypto->create_hasher(lib->crypto, HASH_SHA1);
	if (!this->hasher)
	{
		DBG1(DBG_NET, "creating cookie hasher failed, no hashers supported");
		free(this);
		return NULL;
	}
	this->rng = lib->crypto->create_rng(lib->crypto, RNG_STRONG);
	if (!this->rng)
	{
		DBG1(DBG_NET, "creating cookie RNG failed, no RNG supported");
		this->hasher->destroy(this->hasher);
		free(this);
		return NULL;
	}
	if (!this->rng->get_bytes(this->rng, SECRET_LENGTH, this->secret))
	{
		DBG1(DBG_NET, "creating cookie secret failed");
		destroy(this);
		return NULL;
	}
	memcpy(this->secret_old, this->secret, SECRET_LENGTH);

	lib->processor->queue_job(lib->processor,
		(job_t*)callback_job_create_with_prio((callback_job_cb_t)receive_packets,
			this, NULL, (callback_job_cancel_t)return_false, JOB_PRIO_CRITICAL));

	return &this->public;
}
