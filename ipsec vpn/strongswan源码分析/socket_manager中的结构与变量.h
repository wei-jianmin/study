/**
 * Handle pluggable socket implementations and send/receive packets through it.
 * 处理插件式的socket实现，并通过它发送/接收数据包
 */
struct socket_manager_t {

	/**
	 * Receive a packet using the registered socket.
	 *
	 * @param packet		allocated packet that has been received
	 * @return
	 *						- SUCCESS when packet successfully received
	 *						- FAILED when unable to receive
	 */
	status_t (*receive)(socket_manager_t *this, packet_t **packet);

	/**
	 * Send a packet using the registered socket.
	 *
	 * @param packet		packet to send out
	 * @return
	 *						- SUCCESS when packet successfully sent
	 *						- FAILED when unable to send
	 */
	status_t (*send)(socket_manager_t *this, packet_t *packet);

	/**
	 * Get the port the registered socket is listening on.
	 *
	 * @param nat_t			TRUE to get the port used to float in case of NAT-T
	 * @return				the port, or 0, if no socket is registered
	 */
	uint16_t (*get_port)(socket_manager_t *this, bool nat_t);

	/**
	 * Get the address families the registered socket is listening on.
	 *
	 * @return				address families
	 */
	socket_family_t (*supported_families)(socket_manager_t *this);

	/**
	 * Register a socket constructor.
	 *
	 * @param create		constructor for the socket
	 */
	void (*add_socket)(socket_manager_t *this, socket_constructor_t create);

	/**
	 * Unregister a registered socket constructor.
	 *
	 * @param create		constructor for the socket
	 */
	void (*remove_socket)(socket_manager_t *this, socket_constructor_t create);

	/**
	 * Destroy a socket_manager_t.
	 */
	void (*destroy)(socket_manager_t *this);
};

===================================================

/**
 * Private data of an socket_manager_t object.
 */
struct private_socket_manager_t {

	/**
	 * Public socket_manager_t interface.
	 */
	socket_manager_t public;

	/**
	 * List of registered socket constructors
	 */
	linked_list_t *sockets;

	/**
	 * Instantiated socket implementation
	 */
	socket_t *socket;

	/**
	 * The constructor used to create the current socket
	 */
	socket_constructor_t create;

	/**
	 * Lock for sockets list
	 */
	rwlock_t *lock;
};