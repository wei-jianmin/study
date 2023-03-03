/**
 * Listens to and handles kernel events.
 */
struct kernel_handler_t {

	/**
	 * Implements the kernel listener interface.
	 */
	kernel_listener_t listener;

	/**
	 * Destroy this instance.
	 */
	void (*destroy)(kernel_handler_t *this);

};

===========================================================

/**
 * Private data of a kernel_handler_t object.
 */
struct private_kernel_handler_t {

	/**
	 * Public part of kernel_handler_t object.
	 */
	kernel_handler_t public;
};