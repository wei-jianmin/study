/**
 * Interface to the network subsystem of the kernel.
 * 内核中网络子系统(对网卡的封装)的接口，
 * 参：file://F:/Desktop/学习笔记/网络/Linux下数据包的收发过程.py@网络设备子系统
 * The kernel network interface handles the communication with the kernel
 * for interface and IP address management.
 */
struct kernel_net_t {

	/**
	 * Get the feature set supported by this kernel backend.
	 *
	 * @return				ORed feature-set of backend
	 */
	kernel_feature_t (*get_features)(kernel_net_t *this);

	/**
	 * Get our outgoing source address for a destination.
	 *
	 * Does a route lookup to get the source address used to reach dest.
	 * The returned host is allocated and must be destroyed.
	 * An optional src address can be used to check if a route is available
	 * for the given source to dest.
	 *
	 * @param dest			target destination address
	 * @param src			source address to check, or NULL
	 * @return				outgoing source address, NULL if unreachable
	 */
	host_t* (*get_source_addr)(kernel_net_t *this, host_t *dest, host_t *src);

	/**
	 * Get the next hop for a destination.
	 *
	 * Does a route lookup to get the next hop used to reach dest.
	 * The returned host is allocated and must be destroyed.
	 * An optional src address can be used to check if a route is available
	 * for the given source to dest.
	 *
	 * @param dest			target destination address
	 * @param prefix		prefix length if dest is a subnet, -1 for auto
	 * @param src			source address to check, or NULL
	 * @param[out] iface	allocated name of the interface to reach dest, if
	 *						available (optional)
	 * @return				next hop address, NULL if unreachable
	 */
	host_t* (*get_nexthop)(kernel_net_t *this, host_t *dest, int prefix,
						   host_t *src, char **iface);

	/**
     * 这里的interface，应该指的是网卡，本地可能有多个网卡，包括虚拟网卡
     * 猜测该接口的功能可能是根据ip，查找路由，获取对应要发往的网卡的名字
     * 如果网卡没启动，或在过滤列表中，则返回失败
	 * Get the interface name of a local address. Interfaces that are down or
	 * ignored by config are not considered.
	 *
	 * @param host			address to get interface name from
	 * @param name			allocated interface name (optional)
	 * @return				TRUE if interface found and usable
	 */
	bool (*get_interface) (kernel_net_t *this, host_t *host, char **name);

	/**
	 * Creates an enumerator over all local addresses.
	 *
	 * This function blocks an internal cached address list until the
	 * enumerator gets destroyed.
	 * The hosts are read-only, do not modify of free.
	 *
	 * @param which			a combination of address types to enumerate
	 * @return				enumerator over host_t's
	 */
	enumerator_t *(*create_address_enumerator) (kernel_net_t *this,
												kernel_address_type_t which);

	/**
	 * Creates an enumerator over all local subnets.
	 *
	 * Local subnets are subnets the host is directly connected to.
	 *
	 * The enumerator returns the network, subnet mask and interface.
	 *
	 * @return				enumerator over host_t*, uint8_t, char*
	 */
	enumerator_t *(*create_local_subnet_enumerator)(kernel_net_t *this);

	/**
	 * Add a virtual IP to an interface. 为网卡分配ip
	 *
	 * Virtual IPs are attached to an interface. If an IP is added multiple
	 * times, the IP is refcounted and not removed until del_ip() was called
	 * as many times as add_ip().
	 *
	 * @param virtual_ip	virtual ip address to assign
	 * @param prefix		prefix length to install with IP address, -1 for auto
	 * @param iface			interface to install virtual IP on
	 * @return				SUCCESS if operation completed
	 */
	status_t (*add_ip) (kernel_net_t *this, host_t *virtual_ip, int prefix,
						char *iface);

	/**
	 * Remove a virtual IP from an interface.
	 *
	 * The kernel interface uses refcounting, see add_ip().
	 *
	 * @param virtual_ip	virtual ip address to remove
	 * @param prefix		prefix length of the IP to uninstall, -1 for auto
	 * @param wait			TRUE to wait until IP is gone
	 * @return				SUCCESS if operation completed
	 */
	status_t (*del_ip) (kernel_net_t *this, host_t *virtual_ip, int prefix,
						bool wait);

	/**
	 * Add a route.
	 *
	 * @param dst_net		destination net
	 * @param prefixlen		destination net prefix length
	 * @param gateway		gateway for this route
	 * @param src_ip		source ip of the route
	 * @param if_name		name of the interface the route is bound to
	 * @return				SUCCESS if operation completed
	 *						ALREADY_DONE if the route already exists
	 */
	status_t (*add_route) (kernel_net_t *this, chunk_t dst_net,
						   uint8_t prefixlen, host_t *gateway, host_t *src_ip,
						   char *if_name);

	/**
	 * Delete a route.
	 *
	 * @param dst_net		destination net
	 * @param prefixlen		destination net prefix length
	 * @param gateway		gateway for this route
	 * @param src_ip		source ip of the route
	 * @param if_name		name of the interface the route is bound to
	 * @return				SUCCESS if operation completed
	 */
	status_t (*del_route) (kernel_net_t *this, chunk_t dst_net,
						   uint8_t prefixlen, host_t *gateway, host_t *src_ip,
						   char *if_name);

	/**
	 * Destroy the implementation.
	 */
	void (*destroy) (kernel_net_t *this);
};
