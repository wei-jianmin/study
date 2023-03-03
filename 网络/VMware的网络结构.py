nat模式
    https://www.toutiao.com/article/4099362512/?wid=1660008298342
    结构图：file://imgs/VMware nat模式网络结构.jpg 
    在讲解上图之前，我们先了解一些预备知识
        1. nat模式下，VMware在本机创建了一个虚拟网卡 Vmnet8
           图：file://imgs/nat模式VMware创建的虚拟网卡.jpg
        2. vmware还在宿主机中创建了几个服务，其中
           VMware NAT Service和VMware DHCP Service
           就是为了让nat模式能正常工作而创建的
           图：file://imgs/nat模式VMware创建的服务.jpg
           VMware NAT Service相当于在宿主机中创建了一个虚拟路由器
           VMware DHCP Service则相当于在宿主机中创建了一个虚拟DHCP服务器
    现在我们来看上面的结构图，可以看到本机除了物理网卡，还多了个VMnet8网卡
    所以本机（宿主机）相当于双网卡（实际不止两个网卡，还有别的虚拟网卡）
    本机的VMnet8网卡与虚拟机的网卡，以及虚拟DHCP服务器都连接在虚拟路由器下
    所以上面这几个设备的ip需配置为是同一网段的，他们之间可以互相通信
    备注：各设备的ip配置情况
        本机ip：192.168.3.44
        VMnet8的ip：192.168.4.1
        虚拟机的ip：192.168.4.127
        虚拟DHCP的ip：192.168.4.0
        虚拟路由器的ip：192.168.4.2
    而虚拟路由器的wan口又连接到宿主机的物理网卡上，
    所以借助路由器的转发，虚拟机就可以上网了，
    而且物理网卡的ip没必要与虚拟路由器的ip处于同一网段
    那宿主机中的程序又是如何与虚拟机通信的？
    先看下本机的路由表：file://imgs/本机的路由表.jpg
    可以看到只要访问4网段的ip，就会通过 192.168.4.1 网卡发出去
    而这个ip，正是虚拟网卡VMnet8的ip，图：file://imgs/vmnet8的ip地址.jpg
    而vmnet8虚拟网卡，又与虚拟机连在同一路由器（的lan口）下
    所以主机能访问到虚拟机的ip
    那虚拟机中能ping通（访问）主机物理网卡的ip有是什么原因呢？
    其实这也很好理解，从虚拟机内部看，
    宿主机的物理网卡属于本虚拟机所连接的路由器的上级设备，所以当然能够访问了
    与桥接模式相比，nat模式有个“缺点”：
    与宿主机处于同一网段的其他电脑，没法访问当前宿主机的虚拟机（所提供的服务）
    为什么上面的这个“缺点”要加引号呢，这是因为这个缺点也是有办法解决的，
    解决办法就是接口转发，图：file://imgs/VMware nat模式配置端口映射.png
    配置完接口转发后，虚拟机通过该主机端口对外提供代理服务，
    访问宿主机的tcp/udp指定端口时，代理服务将收到的tcp包VMnet8转发给虚拟机
    在本机测试下ssh连接虚拟机：图：file://imgs/借助端口映射 本机访问虚拟机.jpg
    可见本机虽然访问的是127.0.0.1，但借助端口转发，连接到虚拟机了
    用其他电脑连接VMware中的虚拟机，同样可以，
    图：file://imgs/从其他电脑访问本电脑中的虚拟机.jpg
    
桥接模式
    https://www.cnblogs.com/haoabcd2010/p/8683656.html
    虚拟网卡 VMnet0 是对应桥接模式的，它表示的是桥接模式下的虚拟交换机？
    在桥接的作用下，类似于把物理主机虚拟为一个交换机，
    所有桥接设置的虚拟机连接到这个交换机的一个接口上，
    物理主机也同样插在这个交换机当中，所以所有桥接下的网卡与网卡都是交换模式的，
    相互可以访问而不干扰。在桥接模式下，虚拟机ip地址需要与主机在同一个网段，
    如果需要联网，则网关与DNS需要与主机网卡一致。
    其网络结构如下图所示：
    file://imgs/VMware 桥接模式结构图.png
    附注：
        交换机的各个口都是平级的，不像路由器一样分WAN口和LAN口，
        但交换机可以将不同的口分成不同的组(vLAN)，数据只在同一组的各个接口间流通