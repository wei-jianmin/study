/**
 * Interface to the ipsec subsystem of the kernel.
 *
 * The kernel ipsec interface handles the communication with the kernel
 * for SA and policy management. It allows setup of these, and provides
 * further the handling of kernel events.
 * Policy information are cached in the interface. This is necessary to do
 * reference counting. The Linux kernel does not allow the same policy
 * installed twice, but we need this as CHILD_SA exist multiple times
 * when rekeying. That's why we do reference counting of policies.
 */
struct kernel_ipsec_t {

	/**
	 * Get the feature set supported by this kernel backend.
	 *
	 * @return				ORed feature-set of backend
	 */
	kernel_feature_t (*get_features)(kernel_ipsec_t *this);

	/**
	 * Get a SPI from the kernel.
	 *
	 * @param src		source address of SA
	 * @param dst		destination address of SA
	 * @param protocol	protocol for SA (ESP/AH)
	 * @param spi		allocated spi
	 * @return			SUCCESS if operation completed
	 */
	status_t (*get_spi)(kernel_ipsec_t *this, host_t *src, host_t *dst,
						uint8_t protocol, uint32_t *spi);

	/**
	 * Get a Compression Parameter Index (CPI) from the kernel.
	 *
	 * @param src		source address of SA
	 * @param dst		destination address of SA
	 * @param cpi		allocated cpi
	 * @return			SUCCESS if operation completed
	 */
	status_t (*get_cpi)(kernel_ipsec_t *this, host_t *src, host_t *dst,
						uint16_t *cpi);

	/**
	 * Add an SA to the SAD.
	 *
	 * This function does install a single SA for a single protocol in one
	 * direction.
	 *
	 * @param id			data identifying this SA
	 * @param data			data for this SA
	 * @return				SUCCESS if operation completed
	 */
	status_t (*add_sa)(kernel_ipsec_t *this, kernel_ipsec_sa_id_t *id,
					   kernel_ipsec_add_sa_t *data);

	/**
	 * Update the hosts on an installed SA.
	 *
	 * We cannot directly update the destination address as the kernel
	 * requires the spi, the protocol AND the destination address (and family)
	 * to identify SAs. Therefore if the destination address changed we
	 * create a new SA and delete the old one.
	 *
	 * @param id			data identifying this SA
	 * @param data			updated data for this SA
	 * @return				SUCCESS if operation completed, NOT_SUPPORTED if
	 *						the kernel interface can't update the SA
	 */
	status_t (*update_sa)(kernel_ipsec_t *this, kernel_ipsec_sa_id_t *id,
						  kernel_ipsec_update_sa_t *data);

	/**
	 * Query the number of bytes processed by an SA from the SAD.
	 *
	 * @param id			data identifying this SA
	 * @param data			data to query the SA
	 * @param[out] bytes	the number of bytes processed by SA
	 * @param[out] packets	number of packets processed by SA
	 * @param[out] time		last (monotonic) time of SA use
	 * @return				SUCCESS if operation completed
	 */
	status_t (*query_sa)(kernel_ipsec_t *this, kernel_ipsec_sa_id_t *id,
						 kernel_ipsec_query_sa_t *data, uint64_t *bytes,
						 uint64_t *packets, time_t *time);

	/**
	 * Delete a previously installed SA from the SAD.
	 *
	 * @param id			data identifying this SA
	 * @param data			data to delete the SA
	 * @return				SUCCESS if operation completed
	 */
	status_t (*del_sa)(kernel_ipsec_t *this, kernel_ipsec_sa_id_t *id,
					   kernel_ipsec_del_sa_t *data);

	/**
	 * Flush all SAs from the SAD.
	 *
	 * @return				SUCCESS if operation completed
	 */
	status_t (*flush_sas)(kernel_ipsec_t *this);

	/**
	 * Add a policy to the SPD.
	 *
	 * @param id			data identifying this policy
	 * @param data			data for this policy
	 * @return				SUCCESS if operation completed
	 */
	status_t (*add_policy)(kernel_ipsec_t *this,
						   kernel_ipsec_policy_id_t *id,
						   kernel_ipsec_manage_policy_t *data);

	/**
	 * Query the use time of a policy.
	 *
	 * The use time of a policy is the time the policy was used for the last
	 * time. It is not the system time, but a monotonic timestamp as returned
	 * by time_monotonic.
	 *
	 * @param id			data identifying this policy
	 * @param data			data to query the policy
	 * @param[out] use_time	the monotonic timestamp of this SA's last use
	 * @return				SUCCESS if operation completed
	 */
	status_t (*query_policy)(kernel_ipsec_t *this,
							 kernel_ipsec_policy_id_t *id,
							 kernel_ipsec_query_policy_t *data,
							 time_t *use_time);

	/**
	 * Remove a policy from the SPD.
	 *
	 * @param id			data identifying this policy
	 * @param data			data for this policy
	 * @return				SUCCESS if operation completed
	 */
	status_t (*del_policy)(kernel_ipsec_t *this,
						   kernel_ipsec_policy_id_t *id,
						   kernel_ipsec_manage_policy_t *data);

	/**
	 * Flush all policies from the SPD.
	 *
	 * @return				SUCCESS if operation completed
	 */
	status_t (*flush_policies)(kernel_ipsec_t *this);

	/**
	 * Install a bypass policy for the given socket.
	 *
	 * @param fd			socket file descriptor to setup policy for
	 * @param family		protocol family of the socket
	 * @return				TRUE of policy set up successfully
	 */
	bool (*bypass_socket)(kernel_ipsec_t *this, int fd, int family);

	/**
	 * Enable decapsulation of ESP-in-UDP packets for the given port/socket.
	 *
	 * @param fd			socket file descriptor
	 * @param family		protocol family of the socket
	 * @param port			the UDP port
	 * @return				TRUE if UDP decapsulation was enabled successfully
	 */
	bool (*enable_udp_decap)(kernel_ipsec_t *this, int fd, int family,
							 uint16_t port);

	/**
	 * Destroy the implementation.
	 */
	void (*destroy)(kernel_ipsec_t *this);
};