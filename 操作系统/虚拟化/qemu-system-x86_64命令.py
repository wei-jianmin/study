

��-smp ������

<����>�����ÿͻ�����smpϵͳ��
<��ʽ>��-smp [cpus=]n[,maxcpus=cpus][,cores=cores][,threads=threads][,sockets=sockets]
<����>��
[cpus=]n                    ���ÿͻ�����ʹ���߼���CPU������Ĭ��ֵ��1����
[,maxcpus=cpus]       ���ÿͻ��������ܱ�ʹ�õ�CPU�������������Ȳ��hot-plug���CPU�����ܳ���maxcpus���ޣ���
[,cores=cores]           ����ÿ��CPU socket�ϵ�core������Ĭ��ֵ��1����
[,threads=threads]    ����ÿ��CPU core�ϵ��߳�����Ĭ��ֵ��1����
[,sockets=sockets]    ���ÿͻ������ܵ�CPU socket������
<ʾ��>��
[root@server01 ~]# qemu-system-x86_64  -smp 1,sockets=1,cores=2,threads=2 -boot cd -hda /server/kvm-1.qcow2  -enable-kvm?
 

��-cpu ������

<����>������CPUģ�͡�
<��ʽ>��-cpu cpu select CPU ('-cpu help' for list)
<����>��
help    �鿴֧�ֵ�CPU���͡�
 <˵��>��
Ĭ���������ͻ����ṩqemu64��qemu32�Ļ���CPUģ�͡����������Զ�CPU�����ṩһЩ�߼��Ĺ��˹��ܣ��ÿͻ�����ͬһ��Ӳ��ƽ̨�ϵĶ�̬Ǩ�ƻ����ƽ���Ͱ�ȫ��
�ڿͻ����в鿴CPU��Ϣ(cat /proc/cpuinfo)��model name���ǵ�ǰCPUģ�͵����ơ�
 

��-m ������

<����>�������ڴ��С��
<��ʽ>��-m [size=]megs[,slots=n,maxmem=size]
<����>��
[size=]megs    ���ÿͻ����ڴ��С��֧��M��GΪ��λ��Ĭ��Ϊ128MB��
[,slots=n,maxmem=size]     ����֧���Ȳ�ε��ڴ��С��
<ʾ��>��
[root@server01 ~]# qemu-system-x86_64 -m 1GB -boot cd -hda /server/kvm-1.qcow2 -mem-path /dev/hugepages 
 

??

��-mem-path ������

<����>��ʹ��huge page��
<��ʽ>��-mem-path FILE provide backing storage for guest RAM
<˵��>��
�����ڴ�����ܼ��͵�Ӧ�ã�ʹ��huge page�ǿ��ԱȽ����Ե���߿ͻ������ܡ� 
ʹ��huge page���ڴ治�ܱ�������swap out����Ҳ����ʹ��ballooning��ʽ�Զ�������
x86֧��2MB��С�Ĵ�ҳ��huge page��
<ʾ��>�� 
[root@server01 ~]# cat /proc/meminfo
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
# �鿴ϵͳ���ڴ�ҳ��С
[root@server01 ~]# getconf PAGESIZE
4096
# guazai 
[root@server01 ~]# mount -t hugetlbfs hugetlbfs  /dev/hugepages
# ���� hugepage������
[root@server01 ~]# sysctl vm.nr_hugepages=1024
 
[root@server01 ~]# qemu-system-x86_64 -m 1024 -hda /server/kvm-1.qcow2 -mem-path /dev/hugepages -vnc :1 -enable-kvm
# HugePage����Ӧ���õ�512������ʵ��û���õ���ô�࣬����Ϊ�ͻ���ʵ��δʹ�õ�1G�ڴ档
# ���㷽ʽ��2M(HugePage size)*512(HugePage number)=1G(�ͻ������ڴ棩
[root@server01 ~]# cat /proc/meminfo
HugePages_Total:    1024
HugePages_Free:      899
HugePages_Rsvd:      387
HugePages_Surp:        0
Hugepagesize:       2048 kB
# ����-mem-prealloc������HugePageʹ��������Ϊ512�ˡ�
[root@server01 ~]# qemu-system-x86_64 -m 1024 -hda /server/kvm-1.qcow2 -mem-prealloc -mem-path /dev/hugepages -vnc :1 -enable-kvm 
[root@server01 ~]# cat /proc/meminfo
HugePages_Total:    1024
HugePages_Free:      899
HugePages_Rsvd:      387
HugePages_Surp:        0
Hugepagesize:       2048 kB 

��-mem-prealloc ������

<����>��ʹ�������ڿͻ�������ʱ��ȫ������ÿͻ������ڴ档
<��ʽ>��-mem-prealloc preallocate guest memory (use with -mem-path)
<˵��>��
<ʾ��>��
 

��-hda/-hdb/-hdc/-hdd ������

<����>��Ϊ�ͻ���ָ����洢�豸��ָ���ͻ����ֵĵ�һ��IDE�豸�����0��
<��ʽ>��-hda file
<˵��>��
���ͻ���ʹ��PIIX_IDE��������ʾΪ/dev/hda�豸��
���ͻ���ʹ��ata_piix��������ʾΪ/dev/sda�豸��
��û��ʹ��-hdx�Ĳ�������Ĭ��ʹ��-hda������
���Խ���������һ��Ӳ����Ϊ-hda�Ĳ���ʹ�ã�
���ļ����������ţ�Ӧʹ�����������Ķ��Ž���ת�塣
<ʾ��>��
 

��-fda/-fdb ������

<����>��Ϊ�ͻ���ָ�������豸��ָ���ͻ����ĵ�һ�������豸�����0��
<��ʽ>��-fda file
<˵��>��
-fdaָ�����豸���ڿͻ�������ʾΪ/dev/fd0
-fdbָ�����豸���ڿͻ�������ʾ/dev/fd1
<ʾ��>��
 

��-cdrom ������

<����>��Ϊ�ͻ���ָ������CD-ROM��
<��ʽ>��-cdrom file use 'file' as IDE cdrom image (cdrom is ide1 master)
<˵��>��
���Խ��������Ĺ�����/dev/cdrom���豸��Ϊ-cdrom����ʹ�á�
-cdrom����������-hdc����ͬʱʹ�ã���Ϊ-cdrom���ǿͻ�����ĵ�����IDE�豸
<ʾ��>��
 

��-mtdblock ������

<����>��Ϊ�ͻ���ָ��һ��Flash�洢�������棩��
<��ʽ>��-mtdblock file use 'file' as on-board Flash memory image
<˵��>��
<ʾ��>��
 

��-sd ������

<����>��Ϊ�ͻ���ָ��һ��SD����
<��ʽ>��-sd file use 'file' as SecureDigital card image
<˵��>��
<ʾ��>��
 

��-pflash ������

<����>��Ϊ�ͻ���ָ��һ������Flash�洢����
<��ʽ>��-pflash file use 'file' as a parallel flash image
<˵��>��
<ʾ��>��
 

 

��-drive ������

<����>����ϸ����һ���洢������
<��ʽ>��-drive [file=file][,if=type][,bus=n][,unit=m][,media=d][,index=i] [,snapshot=on|off][,cache=writethrough|writeback|none|directsync|unsafe][,aio=threads|native][,format=f][,addr=A][,id=name][,readonly=on|off]
[,serial=s]
<˵��>��
<����>��
[file=file]������file�����ļ����ͻ������������С�
[,if=type]��ָ��������ʹ�õĽӿ����ͣ����õ������У�ide��scsi��virtio��sd��floopy��pflash�ȡ�
[,bus=n]�������������ڿͻ����е����߱�š�
[,unit=m]�������������ڿͻ����еĵ�Ԫ��š�
[,media=d]��������������ý������ͣ�ֵΪdisk��cdrom��
[,index=i]��������ͨһ�ֽӿڵ��������е�������š�
[,snapshot=on|off]����ֵΪonʱ��qemu���Ὣ�������ݵĸ���д�ص������ļ��У�����д����ʱ�ļ��У�������qemu moinitor��ʹ��commit����ǿ�ƽ��������ݱ���ؾ����ļ��С�
[,cache=writethrough|writeback|none|directsync|unsafe]�������������Կ��豸���ݷ��ʵ�cacheģʽ����
writethrough��ֱдģʽ��������writeд�����ݵ�ͬʱ������д����̻���ͺ�˿��豸�С�
writeback����дģʽ��������writeд������ʱֻ������д�뵽���̻����У������ݱ���������ʱ��д�뵽��˴洢�С��ŵ�д�����ݿ飬ȱ��ϵͳ���������޷��ָ���
[,aio=threads|native]��ѡ���첽IO�ķ�ʽ
threads��Ϊaio������Ĭ��ֵ����һ���̳߳�ȥ�����첽IO��
native��ֻ������cache=none�������ʹ�õ���linuxԭ����AIO��
[,format=f]��ָ��ʹ�õĴ��̸�ʽ��Ĭ����QEMU�Զ������̸�ʽ�ġ�
[,serial=s]��ָ��������豸�����кš�
[,addr=A]���������������������PCI��ַ��ֻ��ʹ��virtio�ӿ�ʱ���á�
[,id=name]��������������ID��������QEMU monitor����info block������
[,readonly=on|off]�������������Ƿ�ֻ����
<ʾ��>��
 

��-boot ������

<����>�����ÿͻ�������˳��
<��ʽ>��-boot [order=drives][,once=drives][,menu=on|off]
<˵��>��
��qemuģ���x86ƽ̨�У���"a"��"b"�ֱ��ʾ��һ�͵ڶ���������"c"��ʾ��һ��Ӳ�̣���"d"��ʾCD-ROM��������"n"��ʾ������������
Ĭ�ϴ�Ӳ��������
<����>��
[order=drives]����������˳��
[,once=drives]��ֻ������һ��������˳������������Ч��
[,menu=on|off]�����ý���ʽ�������˵�����ҪBIOS֧�֣���
<ʾ��>��
 

��-net nic ������

<����>�������ͻ���������
<��ʽ>��-net nic[,vlan=n][,netdev=nd][,macaddr=mac][,model=type][,name=str][,addr=str][,vectors=v]
<˵��>��
��Ҫ��һ���ͻ����ṩ������������Զ��ʹ��-net������
<����>��
[,vlan=n]����������VLAN��
[,netdev=nd]��
[,macaddr=mac]������������MAC��ַ��
[,model=type]������ģ����������͡�
[,name=str]���������������ơ�
[,addr=str]������������PCI�豸��ַ��
[,vectors=v]�������������豸��MSI-X����������������ʹ��virtio������Ч��
<ʾ��>��
[root@server01 server]# qemu-system-x86_64 -m 1024 -smp 2 -boot cd -hda /server/kvm-1.qcow2  -enable-kvm -vnc :1 -net nic,macaddr=52:54:00:12:34:22,model=e1000,addr=08 -net nic
 



 

 

��-netdev tap ������

<����>������һ��tap�豸��Ϊ��ˣ����tap�豸�������ӵ�bridge��fd��vhost���豸����ģ����Ϊ���������ӿڴ������ݰ�ͨ·
<��ʽ>��-netdev tap,id=str[,fd=h][,fds=x:y:...:z][,ifname=name][,script=file][,downscript=dfile]
<˵��>��
<����>��
<ʾ��>��
tunctl -u $(whoami) -t tap1
ip link set tap1 up
brctl addif br0 tap1
qemu-system-x86_64 -m 1024 -smp 2  /server/kvm-1.qcow2 -enable-kvm -vnc :1 -netdev tap,id=xk1,ifname=tap1,script=no -net nic
 



 

��-netdev bridge ������

<����>������˽�����š�
<��ʽ>��-netdev bridge,id=str[,br=bridge][,helper=helper]
<˵��>��
<����>��
<ʾ��>��
��-netdev user ������

<����>�������ڲ��û����磬�������κ�vm���ⲿ���綼��ͨ����������host��qemu�ڲ�������ͨ����
<��ʽ>��-netdev user,id=str[,ipv4[=on|off]][,net=addr[/mask]][,host=addr][,ipv6[=on|off]][,ipv6-net=addr[/int]][,ipv6-host=addr][,restrict=on|off][,hostname=host][,dhcpstart=addr][,dns=addr][,ipv6-dns=addr][,dnssearch=domain][,tftp=dir][,bootfile=f][,hostfwd=rule][,guestfwd=rule][,smb=dir[,smbserver=addr]]
<˵��>��
��vm�Ϸ����ⲿ�����൱��������host�Ϸ��ʡ�
����User Networking��֧��ĳЩ�������ԣ�����ICMP���ģ������vm�в���ʹ��ping���
<����>��
<ʾ��>��