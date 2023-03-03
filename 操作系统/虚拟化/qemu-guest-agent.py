qemu guest agent简称qga， 是运行在虚拟机内部的一个守护程序（qemu-guest-agent.service），
他可以管理应用程序，执行宿主机发出的命令。

QEMU为宿主机和虚拟机提供了一个数据通道（channel），
这个通道的两端分别是在虚拟机内看到的串口和在宿主机上看到的unix socket文件

宿主机与虚拟机内的qga通讯就扩展了对虚拟机的控制能力，例如在宿主机上获取虚拟机的ip地址等

libvrit提供了专门的 virDomainQemuAgentCommand API（对应virsh qemu-agent-command命令）来和qemu-guest-agent通讯，
另外有些libvirt内置api也可以支持qga，例如reboot、shutdown等。