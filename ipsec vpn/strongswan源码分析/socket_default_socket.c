socket_default_socket_t *socket_default_socket_create()
{
	private_socket_default_socket_t *this;
	INIT(this,
		.public = {
			.socket = {
				.send = _sender,
				.receive = _receiver,
				.get_port = _get_port,
				.supported_families = _supported_families,
				.destroy = _destroy,
			},
		},
		.port = lib->settings->get_int(lib->settings,
							"%s.port", CHARON_UDP_PORT, lib->ns),
		.natt = lib->settings->get_int(lib->settings,
							"%s.port_nat_t", CHARON_NATT_PORT, lib->ns),
		.max_packet = lib->settings->get_int(lib->settings,
							"%s.max_packet", PACKET_MAX_DEFAULT, lib->ns),
		.set_source = lib->settings->get_bool(lib->settings,
							"%s.plugins.socket-default.set_source", TRUE,
							lib->ns),
		.set_sourceif = lib->settings->get_bool(lib->settings,
							"%s.plugins.socket-default.set_sourceif", FALSE,
							lib->ns),
	);

	if (this->port && this->port == this->natt)
	{
		DBG1(DBG_NET, "IKE ports can't be equal, will allocate NAT-T "
			 "port randomly");
		this->natt = 0;
	}
	if ((this->port && this->port < 1024) || (this->natt && this->natt < 1024))
	{
		if (!lib->caps->check(lib->caps, CAP_NET_BIND_SERVICE))
		{
			/* required to bind ports < 1024 */
			DBG1(DBG_NET, "socket-default plugin requires CAP_NET_BIND_SERVICE "
				 "capability");
			destroy(this);
			return NULL;
		}
	}
	/* we allocate IPv6 sockets first as that will reserve randomly allocated
	 * ports also for IPv4. On OS X, we have to do it the other way round
	 * for the same effect. */
#ifdef __APPLE__
	open_socketpair(this, AF_INET, &this->ipv4, &this->ipv4_natt, "IPv4");
	open_socketpair(this, AF_INET6, &this->ipv6, &this->ipv6_natt, "IPv6");
#else /* !__APPLE__ */
	open_socketpair(this, AF_INET6, &this->ipv6, &this->ipv6_natt, "IPv6");
	open_socketpair(this, AF_INET, &this->ipv4, &this->ipv4_natt, "IPv4");
#endif /* __APPLE__ */

	if (this->ipv4 == -1 && this->ipv6 == -1)
	{
		DBG1(DBG_NET, "could not create any sockets");
		destroy(this);
		return NULL;
	}

	return &this->public;
}

// 相当于private_socket_default_socket_t的成员方法
METHOD(socket_t, sender, status_t,
	private_socket_default_socket_t *this, packet_t *packet)
{
	int sport, skt = -1, family;
	ssize_t bytes_sent;
	chunk_t data;
	host_t *src, *dst;
	struct msghdr msg;
	struct iovec iov;
	uint8_t *dscp;  //参：file://DCSP知识点介绍.txt

	src = packet->get_source(packet);
	dst = packet->get_destination(packet);
	data = packet->get_data(packet);

	DBG2(DBG_NET, "sending packet: from %#H to %#H", src, dst);

	/* send data */
	sport = src->get_port(src);
	family = dst->get_family(dst);
	if (sport == 0 || sport == this->port)
	{
		switch (family)
		{
			case AF_INET:
				skt = this->ipv4;
				dscp = &this->dscp4;
				break;
			case AF_INET6:
				skt = this->ipv6;
				dscp = &this->dscp6;
				break;
			default:
				return FAILED;
		}
	}
	else if (sport == this->natt)
	{
		switch (family)
		{
			case AF_INET:
				skt = this->ipv4_natt;
				dscp = &this->dscp4_natt;
				break;
			case AF_INET6:
				skt = this->ipv6_natt;
				dscp = &this->dscp6_natt;
				break;
			default:
				return FAILED;
		}
	}
	if (skt == -1)
	{
		DBG1(DBG_NET, "no socket found to send IPv%d packet from port %d",
			 family == AF_INET ? 4 : 6, sport);
		return FAILED;
	}

	/* setting DSCP values per-packet in a cmsg seems not to be supported
	 * on Linux. We instead setsockopt() before sending it, this should be
	 * safe as only a single thread calls send(). */
	if (*dscp != packet->get_dscp(packet))
	{
		if (family == AF_INET)
		{
			uint8_t ds4;

			ds4 = packet->get_dscp(packet) << 2;
			if (setsockopt(skt, SOL_IP, IP_TOS, &ds4, sizeof(ds4)) == 0)
			{
				*dscp = packet->get_dscp(packet);
			}
			else
			{
				DBG1(DBG_NET, "unable to set IP_TOS on socket: %s",
					 strerror(errno));
			}
		}
		else
		{
			u_int ds6;

			ds6 = packet->get_dscp(packet) << 2;
			if (setsockopt(skt, SOL_IPV6, IPV6_TCLASS, &ds6, sizeof(ds6)) == 0)
			{
				*dscp = packet->get_dscp(packet);
			}
			else
			{
				DBG1(DBG_NET, "unable to set IPV6_TCLASS on socket: %s",
					 strerror(errno));
			}
		}
	}

	memset(&msg, 0, sizeof(struct msghdr));
	msg.msg_name = dst->get_sockaddr(dst);;
	msg.msg_namelen = *dst->get_sockaddr_len(dst);
	iov.iov_base = data.ptr;
	iov.iov_len = data.len;
	msg.msg_iov = &iov;
	msg.msg_iovlen = 1;
	msg.msg_flags = 0;

	if (this->set_source && !src->is_anyaddr(src))
	{
		if (family == AF_INET)
		{
			bytes_sent = send_msg_v4(this, skt, &msg, src);
		}
		else
		{
			bytes_sent = send_msg_v6(this, skt, &msg, src);
		}
	}
	else
	{
		bytes_sent = send_msg_generic(skt, &msg);
	}

	if (bytes_sent != data.len)
	{
		DBG1(DBG_NET, "error writing to socket: %s", strerror(errno));
		return FAILED;
	}
	return SUCCESS;
}
