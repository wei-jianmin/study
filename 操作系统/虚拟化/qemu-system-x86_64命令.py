

【-smp 参数】

<作用>：配置客户机的smp系统。
<格式>：-smp [cpus=]n[,maxcpus=cpus][,cores=cores][,threads=threads][,sockets=sockets]
<子项>：
[cpus=]n                    设置客户机中使用逻辑的CPU数量（默认值是1）。
[,maxcpus=cpus]       设置客户机最大可能被使用的CPU数量（可以用热插拔hot-plug添加CPU，不能超过maxcpus上限）。
[,cores=cores]           设置每个CPU socket上的core数量（默认值是1）。
[,threads=threads]    设置每个CPU core上的线程数（默认值是1）。
[,sockets=sockets]    设置客户机中总的CPU socket数量。
<示例>：
[root@server01 ~]# qemu-system-x86_64  -smp 1,sockets=1,cores=2,threads=2 -boot cd -hda /server/kvm-1.qcow2  -enable-kvm?
 

【-cpu 参数】

<作用>：设置CPU模型。
<格式>：-cpu cpu select CPU ('-cpu help' for list)
<子项>：
help    查看支持的CPU类型。
 <说明>：
默认情况会给客户机提供qemu64或qemu32的基本CPU模型。这样做可以对CPU特性提供一些高级的过滤功能，让客户机在同一组硬件平台上的动态迁移会更加平滑和安全。
在客户机中查看CPU信息(cat /proc/cpuinfo)，model name就是当前CPU模型的名称。
 

【-m 参数】

<作用>：设置内存大小。
<格式>：-m [size=]megs[,slots=n,maxmem=size]
<子项>：
[size=]megs    设置客户机内存大小，支持M、G为单位，默认为128MB。
[,slots=n,maxmem=size]     设置支持热插拔的内存大小。
<示例>：
[root@server01 ~]# qemu-system-x86_64 -m 1GB -boot cd -hda /server/kvm-1.qcow2 -mem-path /dev/hugepages 
 

??

【-mem-path 参数】

<作用>：使用huge page。
<格式>：-mem-path FILE provide backing storage for guest RAM
<说明>：
对于内存访问密集型的应用，使用huge page是可以比较明显地提高客户机性能。 
使用huge page的内存不能被换出（swap out），也不能使用ballooning方式自动增长。
x86支持2MB大小的大页（huge page）
<示例>： 
[root@server01 ~]# cat /proc/meminfo
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
# 查看系统的内存页大小
[root@server01 ~]# getconf PAGESIZE
4096
# guazai 
[root@server01 ~]# mount -t hugetlbfs hugetlbfs  /dev/hugepages
# 设置 hugepage的数量
[root@server01 ~]# sysctl vm.nr_hugepages=1024
 
[root@server01 ~]# qemu-system-x86_64 -m 1024 -hda /server/kvm-1.qcow2 -mem-path /dev/hugepages -vnc :1 -enable-kvm
# HugePage数量应该用掉512个，而实际没有用掉那么多，是因为客户机实际未使用到1G内存。
# 计算方式：2M(HugePage size)*512(HugePage number)=1G(客户机的内存）
[root@server01 ~]# cat /proc/meminfo
HugePages_Total:    1024
HugePages_Free:      899
HugePages_Rsvd:      387
HugePages_Surp:        0
Hugepagesize:       2048 kB
# 配置-mem-prealloc参数后，HugePage使用数量变为512了。
[root@server01 ~]# qemu-system-x86_64 -m 1024 -hda /server/kvm-1.qcow2 -mem-prealloc -mem-path /dev/hugepages -vnc :1 -enable-kvm 
[root@server01 ~]# cat /proc/meminfo
HugePages_Total:    1024
HugePages_Free:      899
HugePages_Rsvd:      387
HugePages_Surp:        0
Hugepagesize:       2048 kB 

【-mem-prealloc 参数】

<作用>：使宿主机在客户机启动时就全部分配好客户机的内存。
<格式>：-mem-prealloc preallocate guest memory (use with -mem-path)
<说明>：
<示例>：
 

【-hda/-hdb/-hdc/-hdd 参数】

<作用>：为客户机指定块存储设备，指定客户机种的第一个IDE设备（序号0）
<格式>：-hda file
<说明>：
若客户机使用PIIX_IDE驱动，显示为/dev/hda设备；
若客户机使用ata_piix驱动，显示为/dev/sda设备。
若没有使用-hdx的参数，则默认使用-hda参数；
可以将宿主机的一块硬盘作为-hda的参数使用；
若文件名包含逗号，应使用两个连续的逗号进行转义。
<示例>：
 

【-fda/-fdb 参数】

<作用>：为客户机指定软盘设备，指定客户机的第一个软盘设备（序号0）
<格式>：-fda file
<说明>：
-fda指定的设备，在客户机中显示为/dev/fd0
-fdb指定的设备，在客户机中显示/dev/fd1
<示例>：
 

【-cdrom 参数】

<作用>：为客户机指定光盘CD-ROM。
<格式>：-cdrom file use 'file' as IDE cdrom image (cdrom is ide1 master)
<说明>：
可以将宿主机的光驱（/dev/cdrom）设备作为-cdrom参数使用。
-cdrom参数不能与-hdc参数同时使用，因为-cdrom就是客户机里的第三个IDE设备
<示例>：
 

【-mtdblock 参数】

<作用>：为客户机指定一个Flash存储器（闪存）。
<格式>：-mtdblock file use 'file' as on-board Flash memory image
<说明>：
<示例>：
 

【-sd 参数】

<作用>：为客户机指定一个SD卡。
<格式>：-sd file use 'file' as SecureDigital card image
<说明>：
<示例>：
 

【-pflash 参数】

<作用>：为客户机指定一个并行Flash存储器。
<格式>：-pflash file use 'file' as a parallel flash image
<说明>：
<示例>：
 

 

【-drive 参数】

<作用>：详细定义一个存储驱动器
<格式>：-drive [file=file][,if=type][,bus=n][,unit=m][,media=d][,index=i] [,snapshot=on|off][,cache=writethrough|writeback|none|directsync|unsafe][,aio=threads|native][,format=f][,addr=A][,id=name][,readonly=on|off]
[,serial=s]
<说明>：
<子项>：
[file=file]：加载file镜像文件到客户机的驱动器中。
[,if=type]：指定驱动器使用的接口类型：可用的类型有：ide、scsi、virtio、sd、floopy、pflash等。
[,bus=n]：设置驱动器在客户机中的总线编号。
[,unit=m]：设置驱动器在客户机中的单元编号。
[,media=d]：设置驱动器中媒介的类型，值为disk或cdrom。
[,index=i]：设置在通一种接口的驱动器中的索引编号。
[,snapshot=on|off]：当值为on时，qemu不会将磁盘数据的更改写回到镜像文件中，而是写到临时文件中，可以在qemu moinitor中使用commit命令强制将磁盘数据保存回镜像文件中。
[,cache=writethrough|writeback|none|directsync|unsafe]：设置宿主机对块设备数据访问的cache模式。，
writethrough（直写模式）：调用write写入数据的同时将数据写入磁盘缓存和后端块设备中。
writeback（回写模式）：调用write写入数据时只将数据写入到磁盘缓存中，当数据被换出缓存时才写入到后端存储中。优点写入数据块，缺点系统掉电数据无法恢复。
[,aio=threads|native]：选择异步IO的方式
threads：为aio参数的默认值，让一个线程池去处理异步IO；
native：只适用于cache=none的情况，使用的是linux原生的AIO。
[,format=f]：指定使用的磁盘格式，默认是QEMU自动检测磁盘格式的。
[,serial=s]：指定分配给设备的序列号。
[,addr=A]：分配给驱动器控制器的PCI地址，只在使用virtio接口时适用。
[,id=name]：设置驱动器的ID，可以在QEMU monitor中用info block看到。
[,readonly=on|off]：设置驱动器是否只读。
<示例>：
 

【-boot 参数】

<作用>：设置客户机启动顺序。
<格式>：-boot [order=drives][,once=drives][,menu=on|off]
<说明>：
在qemu模拟的x86平台中，用"a"、"b"分别表示第一和第二软驱，用"c"表示第一个硬盘，用"d"表示CD-ROM光驱，用"n"表示从网络启动。
默认从硬盘启动。
<子项>：
[order=drives]：设置启动顺序。
[,once=drives]：只设置下一次启动的顺序，再重启后无效。
[,menu=on|off]：设置交互式的启动菜单（需要BIOS支持）。
<示例>：
 

【-net nic 参数】

<作用>：创建客户机的网卡
<格式>：-net nic[,vlan=n][,netdev=nd][,macaddr=mac][,model=type][,name=str][,addr=str][,vectors=v]
<说明>：
需要向一个客户机提供多个网卡，可以多次使用-net参数。
<子项>：
[,vlan=n]：网卡所属VLAN。
[,netdev=nd]：
[,macaddr=mac]：设置网卡的MAC地址。
[,model=type]：设置模拟的网卡类型。
[,name=str]：设置网卡的名称。
[,addr=str]：设置网卡的PCI设备地址。
[,vectors=v]：设置王阿卡设备的MSI-X向量的数量，仅对使用virtio驱动有效。
<示例>：
[root@server01 server]# qemu-system-x86_64 -m 1024 -smp 2 -boot cd -hda /server/kvm-1.qcow2  -enable-kvm -vnc :1 -net nic,macaddr=52:54:00:12:34:22,model=e1000,addr=08 -net nic
 



 

 

【-netdev tap 参数】

<作用>：创建一个tap设备作为后端，这个tap设备可以连接到bridge、fd、vhost等设备或者模块来为虚拟机网络接口创造数据包通路
<格式>：-netdev tap,id=str[,fd=h][,fds=x:y:...:z][,ifname=name][,script=file][,downscript=dfile]
<说明>：
<子项>：
<示例>：
tunctl -u $(whoami) -t tap1
ip link set tap1 up
brctl addif br0 tap1
qemu-system-x86_64 -m 1024 -smp 2  /server/kvm-1.qcow2 -enable-kvm -vnc :1 -netdev tap,id=xk1,ifname=tap1,script=no -net nic
 



 

【-netdev bridge 参数】

<作用>：配置私有网桥。
<格式>：-netdev bridge,id=str[,br=bridge][,helper=helper]
<说明>：
<子项>：
<示例>：
【-netdev user 参数】

<作用>：配置内部用户网络，与其它任何vm和外部网络都不通，属于宿主host和qemu内部的网络通道。
<格式>：-netdev user,id=str[,ipv4[=on|off]][,net=addr[/mask]][,host=addr][,ipv6[=on|off]][,ipv6-net=addr[/int]][,ipv6-host=addr][,restrict=on|off][,hostname=host][,dhcpstart=addr][,dns=addr][,ipv6-dns=addr][,dnssearch=domain][,tftp=dir][,bootfile=f][,hostfwd=rule][,guestfwd=rule][,smb=dir[,smbserver=addr]]
<说明>：
从vm上访问外部网络相当于在宿主host上访问。
但是User Networking不支持某些网络特性，例如ICMP报文，因此在vm中不能使用ping命令。
<子项>：
<示例>：