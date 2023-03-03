��زο���<<file://socket_manager�еĽṹ�����.h>>

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
���ܣ��ڲ����õ��� socket��Ա�� send ����
��socket�ڸմ�����ʱ���ǿյ�
ͨ�� add_socket ������
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

// �� socket.c : socket_register�����У������� add_socket ����
// �� add_socket �Ĳ��� create Ҳ���ⲿ�����Ĳ���
// socket_default_socket.c�е����� add_socket��
// create = socket_default_socket_create
// �Σ�file://socket_default_socket.c
// socket_dynamic_plugin.c��Ҳ������ add_socket,
// create = socket_dynamic_socket_create
// socket_win_plugin.c ��Ҳ������ add_socket��
// create = socket_win_socket_create
// �����⼸��create����������PLUGIN_CALLBACK��ӵ�
// �� file://plugin_feature�еĽṹ�����.h
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

//sockets�д���һЩ������������ͷ��ʼ�Ƴ���
//ֱ���ҵ�һ���ܳɹ�����socket�ĺ���
//��socket��Ա��Ŵ��������Ĵ������(socket_t)
//��create��Ա��Ÿô�������
static void create_socket(private_socket_manager_t *this)
{
	socket_constructor_t create;
	//����ܴ�sockets�г�Աȡ��
	while (this->sockets->remove_first(this->sockets,
									   (void**)&create) == SUCCESS)
	{
		this->socket = create();    //����ȡ���Ĵ�������������socket_t
		if (this->socket)       //��������ɹ������¼�ô���������������ѭ��
		{
			this->create = create;
			break;
		}
	}
}