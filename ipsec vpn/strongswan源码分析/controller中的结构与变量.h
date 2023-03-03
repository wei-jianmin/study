/**
 * 控制器（Controller）提供了简单的API，供各种插件访问和控制守护进程（例如：初始化IKE_SA等）
 
 * 控制器提供一个简单地接口以运行actions
 * The controller provides a simple interface to run actions.
 *
 * 控制器通过创建作业来启动操作。 然后它尝试通过在总线上监听来评估操作的结果。
 * The controller starts actions by creating jobs. It then tries to
 * evaluate the result of the operation by listening on the bus.
 *
 * Passing NULL as callback to the managers function calls them asynchronously.
 * If a callback is specified, they are called synchronously. There is a default
 * callback "controller_cb_empty" if you want to call a function
 * synchronously, but don't need a callback.
 */
struct controller_t {

	/**
	 * Create an enumerator for all IKE_SAs.
	 *
	 * The enumerator blocks the IKE_SA manager until it gets destroyed. Do
	 * not call another interface/manager method while the enumerator is alive.
	 *
	 * @param wait			TRUE to wait for checked out SAs, FALSE to skip
	 * @return				enumerator, locks IKE_SA manager until destroyed
	 */
	enumerator_t* (*create_ike_sa_enumerator)(controller_t *this, bool wait);

	/**
	 * Initiate a CHILD_SA, and if required, an IKE_SA.
	 *
	 * If a callback is provided the function is synchronous and thus blocks
	 * until the IKE_SA is established or failed.
	 *
	 * @param peer_cfg		peer_cfg to use for IKE_SA setup
	 * @param child_cfg		child_cfg to set up CHILD_SA from
	 * @param cb			logging callback
	 * @param param			parameter to include in each call of cb
	 * @param timeout		timeout in ms to wait for callbacks, 0 to disable
	 * @param limits		whether to check limits regarding IKE_SA initiation
	 * @return
	 *						- SUCCESS, if CHILD_SA established
	 *						- FAILED, if setup failed
	 *						- NEED_MORE, if callback returned FALSE
	 *						- OUT_OF_RES if timed out
	 *						- INVALID_STATE if limits prevented initiation
	 */
	status_t (*initiate)(controller_t *this,
						 peer_cfg_t *peer_cfg, child_cfg_t *child_cfg,
						 controller_cb_t callback, void *param, u_int timeout,
						 bool limits);

	/**
	 * Terminate an IKE_SA and all of its CHILD_SAs.
	 *
	 * If a callback is provided the function is synchronous and thus blocks
	 * until the IKE_SA is properly deleted, or the call timed out.
	 *
	 * @param unique_id		unique id of the IKE_SA to terminate.
	 * @param force			whether to immediately destroy the IKE_SA without
	 *						waiting for a response or retransmitting the delete,
	 *						if a callback is provided and timeout is > 0 the
	 *						IKE_SA is destroyed once the timeout is reached but
	 *						retransmits are sent until then
	 * @param cb			logging callback
	 * @param param			parameter to include in each call of cb
	 * @param timeout		timeout in ms to wait for callbacks, 0 to disable
	 * @return
	 *						- SUCCESS, if CHILD_SA terminated
	 *						- NOT_FOUND, if no such CHILD_SA found
	 *						- NEED_MORE, if callback returned FALSE
	 *						- OUT_OF_RES if timed out
	 */
	status_t (*terminate_ike)(controller_t *this, uint32_t unique_id,
							  bool force, controller_cb_t callback, void *param,
							  u_int timeout);

	/**
	 * Terminate a CHILD_SA.
	 *
	 * If a callback is provided the function is synchronous and thus blocks
	 * until the CHILD_SA is properly deleted, or the call timed out.
	 *
	 * @param unique_id		CHILD_SA unique ID to terminate
	 * @param cb			logging callback
	 * @param param			parameter to include in each call of cb
	 * @param timeout		timeout in ms to wait for callbacks, 0 to disable
	 * @return
	 *						- SUCCESS, if CHILD_SA terminated
	 *						- NOT_FOUND, if no such CHILD_SA found
	 *						- NEED_MORE, if callback returned FALSE
	 *						- OUT_OF_RES if timed out
	 */
	status_t (*terminate_child)(controller_t *this, uint32_t unique_id,
								controller_cb_t callback, void *param,
								u_int timeout);

	/**
	 * Destroy a controller_t instance.
	 */
	void (*destroy) (controller_t *this);
};

=========================================================

/**
 * Private data of an stroke_t object.
 */
struct private_controller_t {

	/**
	 * Public part of stroke_t object.
	 */
	controller_t public;
};

/**
 * helper struct for the logger interface
 */
struct interface_logger_t {
	/**
	 * public logger interface
	 */
	logger_t public;  //logger.h

	/**
	 * reference to the listener
	 */
	interface_listener_t *listener;

	/**
	 *  interface callback (listener gets redirected to here)
	 */
	controller_cb_t callback;

	/**
	 * user parameter to pass to callback
	 */
	void *param;
};

/**
 * helper struct to map listener callbacks to interface callbacks
 */
struct interface_listener_t {

	/**
	 * public bus listener interface
	 */
	listener_t public;

	/**
	 * logger interface
	 */
	interface_logger_t logger;

	/**
	 * status of the operation, return to method callers
	 */
	status_t status;

	/**
	 * child configuration, used for initiate
	 */
	child_cfg_t *child_cfg;

	/**
	 * peer configuration, used for initiate
	 */
	peer_cfg_t *peer_cfg;

	/**
	 * IKE_SA to handle
	 */
	ike_sa_t *ike_sa;

	/**
	 * unique ID, used for various methods
	 */
	uint32_t id;

	/**
	 * semaphore to implement wait_for_listener()
	 */
	semaphore_t *done;

	/**
	 * spinlock to update the IKE_SA handle properly
	 */
	spinlock_t *lock;

	union {
		/**
		 * whether to check limits during initiation
		 */
		bool limits;

		/**
		 * whether to force termination
		 */
		bool force;
	} options;
};

/**
 * job for asynchronous listen operations
 */
struct interface_job_t {

	/**
	 * job interface
	 */
	job_t public;

	/**
	 * associated listener
	 */
	interface_listener_t listener;

	/**
	 * the job is reference counted as the thread executing a job as well as
	 * the thread waiting in wait_for_listener() require it but either of them
	 * could be done first
	 */
	refcount_t refcount;
};