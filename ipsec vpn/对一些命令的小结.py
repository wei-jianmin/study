route ：查看路由表
    file://D:/workspace/projects/baseroot/base/depts/jc1/private/weijianmin/学习笔记/网络/路由表.txt

=========================================================    

策略路由  
    引自：file://D:/workspace/projects/baseroot/base/depts/jc1/private/weijianmin/学习笔记/ipsec vpn/strongswan/strongswan详解.py
    Linux 策略路由的实现需要多个路由表和一个路由策略数据库（RPDB）。
    你可以通过输入以下命令列出 RPDB 中的策略：ip rule show
    输出应该显示这样的内容：
        0:     from all lookup local 
        220:   from all lookup 220 
        32766: from all lookup main 
        32767: from all lookup default
    要在表中列出可用的路由（例如，local），使用以下命令：
    ip route list table local
    输出应该是这样的：
        broadcast 127.0.0.0 dev lo proto kernel scope link src 127.0.0.1
        local 127.0.0.0/8 dev lo proto kernel scope host src 127.0.0.1
        local 127.0.0.1 dev lo proto kernel scope host src 127.0.0.1
        broadcast 127.255.255.255 dev lo proto kernel scope link src 127.0.0.1
        broadcast 192.168.3.0 dev br0 proto kernel scope link src 192.168.3.229
        local 192.168.3.229 dev br0 proto kernel scope host src 192.168.3.229
        broadcast 192.168.3.255 dev br0 proto kernel scope link src 192.168.3.229
        broadcast 192.168.122.0 dev virbr0 proto kernel scope link src 192.168.122.1
        local 192.168.122.1 dev virbr0 proto kernel scope host src 192.168.122.1
        broadcast 192.168.122.255 dev virbr0 proto kernel scope link src 192.168.122.1
        
========================================================= 

使用ipsec工具配置sa
    引自：file://D:/workspace/projects/baseroot/base/depts/jc1/private/weijianmin/学习笔记/ipsec vpn/strongswan/strongswan详解.py    
    1 使用racoon配置sa
        setkey add 192.168.0.1 192.168.1.2 esp 0x10001
                    -m tunnel
                    -E des-cbc 0x3ffe05014819ffff
                    -A hmac-md5 "authentication!!"
        从以上信息可以很容易看出各个参数表达的含义，
        其中-E代表加密算法和它的key，-A代表验证算法和它的key。0x10001为spi
    2 使用racoon配置policy(有关racoon，参：https://blog.csdn.net/ai58203/article/details/101469199）
        setkey spdadd 10.0.11.41/32[21] 10.0.11.33/32[any] any
                      -P out ipsec esp/tunnel/192.168.0.1-192.168.1.2/require
        第一行代表五元组，any代表协议。
        第二行代表policy的具体描述：方向，action，template   

========================================================= 

配置xfrm
       file://D:/workspace/projects/baseroot/base/depts/jc1/private/weijianmin/学习笔记/ipsec vpn/IP XFRM配置示例.txt 
       
=========================================================

strongswan 生成证书：
    pki --gen --type ed25519 --outform pem > strongswanKey.pem

    pki --self --ca --lifetime 3652 --in strongswanKey.pem \
               --dn "C=CH, O=strongSwan, CN=strongSwan Root CA" \
               --outform pem > strongswanCert.pem
     
    pki --print --in strongswanCert.pem

    pki --gen --type ed25519 --outform pem > moonKey.pem

    pki --req --type priv --in moonKey.pem \
              --dn "C=CH, O=strongswan, CN=moon.strongswan.org" \
              --san moon.strongswan.org --outform pem > moonReq.pem
              
    pki --issue --cacert strongswanCert.pem --cakey strongswanKey.pem \
                --type pkcs10 --in moonReq.pem --serial 01 --lifetime 1826 \
                --outform pem > moonCert.pem          
               
    pki --gen --type ed25519 --outform pem > sunKey.pem

    pki --req --type priv --in sunKey.pem \
              --dn "C=CH, O=strongswan, CN=sun.strongswan.org" \
              --san sun.strongswan.org --outform pem > sunReq.pem
              
    pki --issue --cacert strongswanCert.pem --cakey strongswanKey.pem \
                --type pkcs10 --in sunReq.pem --serial 01 --lifetime 1826 \
                --outform pem > sunCert.pem
            
=========================================================

查看路由跳数  traceroute  ip

=========================================================

swanctl证书放置位置及加载命令
    /etc/swanctl/x509ca/strongswanCert.pem
    /etc/swanctl/x509/sunCert.pem
    /etc/swanctl/private/sunKey.pem
    swanctl --load-creds        
    swanctl --load-conns

=========================================================

arp -a 查看本机缓存的arp表，通常可用来判断网段内哪些ip被占用

=========================================================

ip xfrm state 查看SA    // wireshark解码esp包时，会使用该命令列出的数据
ip xfrm state flush 清空SA数据库

==========================================================

ipsec-tool 工具
    libipsec：PF_KEY实现库
        为实现racoon和Setkey模块与内核交互，需使用PF_KEYv2套接字
    setkey：用于配置SAD（安全关联数据库）和SPD（安全策略数据库）
    racoon：IKE守护程序，用于自动建立IPsec连接
        一个密钥管理守护进程，实现用户中的IKE密钥协商模块，
        主要用于自动方式下与通信对端相应模块的SA协商
    racoonctl：操作racoon的shell工具
    
==============================================================

策略路由 
     strongSwan 使用了"策略路由"这一网络功能
     Linux 策略路由的实现需要多个路由表和一个路由策略数据库（RPDB）
     ip rule help
        ip rule { add | del } SELECTOR ACTION
        ip rule { flush | save | restore }
        ip rule [ list [ SELECTOR ]]
        SELECTOR := [ not ] [ from PREFIX ] [ to PREFIX ] [ tos TOS ] [ fwmark FWMARK[/MASK] ]
                    [ iif STRING ] [ oif STRING ] [ pref NUMBER ] [ l3mdev ]
                    [ uidrange NUMBER-NUMBER ]
        ACTION := [ table TABLE_ID ]
                  [ nat ADDRESS ]
                  [ realms [SRCREALM/]DSTREALM ]
                  [ goto NUMBER ]
                  SUPPRESSOR
        SUPPRESSOR := [ suppress_prefixlength NUMBER ]
                      [ suppress_ifgroup DEVGROUP ]
        TABLE_ID := [ local | main | default | NUMBER ]
     ip rule show：列出 RPDB 中的策略
        例：
        0:     from all lookup local 
        220:   from all lookup 220 
        32766: from all lookup main 
        32767: from all lookup default
     ip route list table local：列出local表中可用的路由
        可用的规则从最高优先级（0）到最低优先级（32767）进行扫描，
        一旦 RPDB 策略匹配，就会使用指定的表来查找下一跳
        如果路由过程无法从规则所指示的路由表计算出数据包的下一跳，
        则继续处理到 RPDB 中的下一条规则
        from 关键字表示对源 IP 地址的选择符，
        但由于也使用了 all ，所以表示所有数据包都会匹配
        默认情况下，strongSwan 会插入一个优先级为 220 的策略规则。
        当 Ubuntu Linux 启动时，它会设置三个表：local（id 255）、main（254）和default（253）
        本地路由表包含本地和广播地址的高优先级控制路由。
        这个表是供内核内部使用的，不应该从用户空间修改。
        主路由表是在没有指定表时使用的普通表。
        默认表通常是空的，当没有其他表匹配时使用。

==============================================================        
        
file://ip route 和  ip rule.py        

==============================================================

