相关参考：<<file://socket_manager中的结构与变量.h>>

&socket_manager_create
socket_manager_t *socket_manager_create()
{
	private_socket_manager_t *this;

	INIT(this,
		.public = {
			.send = _sender,
			.receive = _receiver,
			.get_port = _get_port,
			.supported_families = _supported_families,
			.add_socket = _add_socket,
			.remove_socket = _remove_socket,
			.destroy = _destroy,
		},
		.sockets = linked_list_create(),
		.lock = rwlock_create(RWLOCK_TYPE_DEFAULT),
	);

	return &this->public;
}

&sender
/*
功能：内部调用的是 socket成员的 send 方法
该socket在刚创建的时候，是空的
通过 add_socket 方法，
*/
METHOD(socket_manager_t, sender, status_t,
	private_socket_manager_t *this, packet_t *packet)
{
	status_t status;
	this->lock->read_lock(this->lock);
	if (!this->socket)
	{
		DBG1(DBG_NET, "no socket implementation registered, sending failed");
		this->lock->unlock(this->lock);
		return NOT_SUPPORTED;
	}
	status = this->socket->send(this->socket, packet);
	this->lock->unlock(this->lock);
	return status;
}

// 在 socket.c : socket_register函数中，调用了 add_socket 函数
// 而 add_socket 的参数 create 也是外部传来的参数
// socket_default_socket.c中调用了 add_socket，
// create = socket_default_socket_create
// 参：file://socket_default_socket.c
// socket_dynamic_plugin.c中也调用了 add_socket,
// create = socket_dynamic_socket_create
// socket_win_plugin.c 中也调用了 add_socket，
// create = socket_win_socket_create
// 上面这几个create函数，都是PLUGIN_CALLBACK添加的
// 参 file://plugin_feature中的结构与变量.h
METHOD(socket_manager_t, add_socket, void,
	private_socket_manager_t *this, socket_constructor_t create)
{
	this->lock->write_lock(this->lock);
	this->sockets->insert_last(this->sockets, create);
	if (this->socket == NULL)
	{
		create_socket(this);
	}
	this->lock->unlock(this->lock);
}

//sockets中存了一些创建函数，从头开始移出，
//直到找到一个能成功创建socket的函数
//用socket成员存放创建函数的创建结果(socket_t)
//用create成员存放该创建函数
static void create_socket(private_socket_manager_t *this)
{
	socket_constructor_t create;
	//如果能从sockets中成员取到
	while (this->sockets->remove_first(this->sockets,
									   (void**)&create) == SUCCESS)
	{
		this->socket = create();    //调用取到的创建函数，创建socket_t
		if (this->socket)       //如果创建成功，则记录该创建函数，并结束循环
		{
			this->create = create;
			break;
		}
	}
}