https://blog.csdn.net/wozaiyizhideng/article/details/116995497
配置kvm直连
    1.先创建网桥
      通过brctl工具来创建网桥，这个工具是由 bridge-utils 包来提供的
      创建网桥的命令：brctl addbr br0
    2.将物理网卡绑定到网桥
      brctl addif br0 enp3s0
      查看网桥端口绑定情况：brctl show br0
    3.给网桥开启stp功能
      brctl stp br0 on
      stp协议
          STP（Spanning Tree Protocol）是生成树协议的英文缩写，
          可应用于计算机网络中树形拓扑结构建立，
          主要作用是防止网桥网络中的冗余链路形成环路工作
          STP的基本思想就是按照"树"的结构构造网络的拓扑结构，
          树的根是一个称为根桥的桥设备
          更多关于STP的信息，可参看百度百科
      此时再用 brctl show br0 查看网桥信息，可看到 STP 项的值变为yes
    4.开启网桥
      ifconfig br0 up
    5.让网桥获取ip
      dhclient br0
      dhclient命令
            dhclient命令来自于英文词组“DHCP client”的缩写，
            其功能是用于动态获取或释放IP地址
            使用dhclient命令前需要将网卡模式设置成DHCP自动获取，
            否则静态模式的网卡是不会主动向服务器获取如IP地址等网卡信息的
            常用参数：
                -r	释放ip地址
                -s	在获取ip地址之前指定DHCP服务器
                -x	停止正在运行的DHCP客户端，而不释放当前租约，
                    杀死现有的dhclient
            使用举例
                通过指定网卡发起DHCP请求，获取网卡参数： dhclient ens160
                释放系统中已获取的网卡参数：dhclient -r
                手动停止执行dhclient服务进程：dhclient -x
                    经测试发现，调用 dhclient -x 后，
                    原来用 dhclient ens160 给网卡分配的ip没有了
      在执行此命令之前，可以看到物理网卡有ip，网桥没有ip
      执行此命令之后，可以看到物理网卡和网桥都有ip了（两个ip不同），且都能ping通
      从虚拟机ping外部计算机，外部计算机抓包发现数据是从br0的ip过来的
    6.释放物理网卡的ip
      ifconfig enp3s0 0 up （不是 ifconfig enp3s0 up）
      这样再看物理网卡，就看不到ip了，
      外部计算机再ping虚拟机的物理网卡ip就ping不到了
      测试：
        调用 dhclient -x，发现原来给 br0 分配的ip没有了
        再调用 hdclient enp3s0，发现 enp3s0 有ip了
        再调用 dhclient -x，发现原来给 enp3s0 分配的ip没有了
        在执行 dhclient，后面不加网卡名，发现 br0 和 enp3s0 获取到了相同的ip
        调用过一遍 dhclient 后，如果不执行 dhclient -x，再次执行 dhclient
        报错：dhclient(14294) is already running - exiting.
    7.让虚拟机的虚拟网卡自动绑定到桥上或从桥上解绑
      在虚拟机启动网络前执行的脚本由 script 参数配置（默认 /etc/qemu-ifup）
      该脚本时将 QEMU 自动创建的 TAP 设备绑定到网桥上。
      虚拟机关闭时，QEMU 会自动解除 TAP 设备的绑定，删除 TAP 设备
      所以 qemu-ifdown 是不用配置的。
      [root@localhost ~]# cat /etc/qemu-ifup
      #!/bin/bash
      switch=br0
      ifconfig $1 up #$1为qemu调用脚本时，传来的虚拟网卡(tap)的名字
      brctl addif $switch $1
      
https://quemingfei.com/archives/linuxbridge-wang-qiao-ji-chu-      
Bridge讲解      
    Bridge（桥）是 Linux 上用来做 TCP/IP 二层协议交换的设备，
    与现实世界中的交换机功能相似。
    Bridge 设备实例可以和 Linux 上其他网络设备实例连接，既 attach 一个从设备，
    类似于在现实世界中的交换机和一个用户终端之间连接一根网线。
    当有数据到达时，Bridge 会根据报文中的 MAC 信息进行广播、转发、丢弃处理
    当一个从设备被 attach 到 Bridge 上时，
    相当于现实世界里交换机的端口被插入了一根连有终端的网线。
    这时在内核程序里，netdev_rx_handler_register()被调用，
    一个用于接受数据的回调函数被注册
    以后每当这个从设备"收到"数据时都会调用这个函数可以把数据转发到 Bridge 上
    注意，只有设备收到数据是，会调用这个函数，从设备发出时，不会调用该函数
    当 Bridge 接收到此数据时，br_handle_frame()被调用，
    进行一个和现实世界中的交换机类似的处理过程：
        判断包的类别（广播/单点），查找内部 MAC 端口映射表，定位目标端口号，
        将数据转发到目标端口或丢弃，自动更新内部 MAC 端口映射表以自我学习。
    Bridge 和现实世界中的二层交换机有一个区别：
        数据被直接发到 Bridge 上，而不是从一个端口接受。
        二层交换机或桥设备因为是工作在数据链路层的，因此是没有ip的
        但Bridge却可以分配一个ip
        这相当于 Linux 拥有了一个隐藏的虚拟网卡和 Bridge 的隐藏端口相连
    Bridge 的实现当前有一个限制：
        当一个设备被 attach 到 Bridge 上时，那个设备的 IP 会变的无效，
        Linux 不再使用那个 IP 在三层接受数据
        （但从上面的配置kvm直连，第5步中验证可知，这个限制已经没有了）