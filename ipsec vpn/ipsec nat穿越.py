https://blog.csdn.net/qq_38265137/article/details/89423809

ipsec使用 AH 和 ESP 对报文进行封装
    AH只能用来验证，没有加密的功能，而ESP同时具有加密和验证的功能，
    AH和ESP可以单独使用也可以配合使用
    
有传输模式和隧道模式两种：
    隧道模式
        在隧道模式下，AH头或ESP头添加到原始IP头之前，然后再生成一个新的报文头放到AH头或ESP头之前
        图：file://imgs/ipsec vpn隧道模式封装策略.png
    传输模式
        在传输模式中，AH头或ESP头插入到IP头与传输层协议头之间：
        图：file://imgs/ipsec vpn传输模式封装策略.png
        传输模式不改变报文头，隧道的源和目的地址就是最终通信双方的源和目的地址，
        通信双方只能保护自己发出的消息，不能保护一个网络的消息。
        所以该模式只适用于两台主机之间通信
        
在经过nat设备时，需要把你内部的ip_port转换为对外的ip_port
对于AH协议，它保护报文的全部（包括ip头部），所以 AH 封装的报文不支持nat穿越
对于ESP协议，按照现有的条件也无法进行nat穿越（无法进行nat转换）：
    ESP封装的报文，开始是ip头，可以转换为对外的ip
    当ip头后面跟的不是tcp头，而是esp头，
    esp头是这样的：file://imgs/esp头.png
    可见esp头是不带端口号的，
    传输模式下，esp头后面跟的是tcp头（隧道模式下是ip-tcp头）
    理论上可以替换该tcp头的端口号，可是该tcp头是加密的，
    所以网关无法替换该tcp头中的端口号
    
nat穿越的解决办法（nat-t）    
    看ESP传输模式进行nat穿越时遇到的问题，就是无法进行port转换
    对此，对ESP协议进行一定的修改，
    让esp进行封装时，在添加最外层的ip时，在ip头后面带个端口号
    （这样就相当于将esp封装为udp报文了，而不是原来的ip报文了）
    这样，nat设备就能对该报文的ip、端口进行外网转换了
    同时新改esp因为不验证ip头和端口，所以验证这一块也没问题
    这样就能做到nat穿越了
    可以发现这种方式不仅适合于esp传输模式，还同样适合于esp隧道模式
    这种技术称作 NAT-T 技术，图：file://imgs/esp nat穿越.png
    
关键NAT-T的3个问题：
    IPSEC网关如何知道自己是否需要支持NAT-T？
        决定双方是否支持NAT-T（和下一条的判断peers之间是否有NAT存在）
        的任务是在IKEv1的第一阶段完成，
        NAT-T能力探测使用IKEv1第一阶段1-2个包交换来实现，
        双方互相交换NAT-T的Vendor ID来表示本段是否支持NAT-T。
    IPSEC网关如何判定经过NAT的设备？
        为了决定Peers之间是否有NAT存在，Peer会发送一个hash负载
        （源目IP和端口的哈希），如果双方计算的hash和接受的hash值匹配，
        那么Peers之间就没有NAT存在（就采用ESP封装），
        如果hash值不同，那么Peers就需要使用NAT-T技术封装穿越NAT。
        hash负载也叫作NAT-D负载，
        在主模式中的3-4个包发送，在野蛮模式的2-3个包中发送。
        IKEV1通过3-4个包的NAT-D参数来判定
        通过源IP源端口, 目的IP 目的端口算HASH值
        如果HASH值相同，说明没有经过NAT，如果HASH值不等，说明经过了NAT
    什么时候添加UDP的端口？
        如果确定了经过nat，就在IKEV1的通过5 6的时候，增加 UDP 4500端口 
        
对IKEv1/IKEv2的NAT穿越协商过程，请参见原文链接

--------------------------------------------------------------------------------------
https://blog.csdn.net/ddv_9527/article/details/5679469
    NAT-T设计简单，不需要改动已有的设备或者协议，只需要边界设备支持即可。
    这个技术的基本思路是在IPSec封装好的数据包外再进行一次UDP的数据封装。
    这样，当此数据包穿过NAT网关时，被修改的只是最外层的IP/UDP数据，
    而对其内部真正的IPSec 数据没有进行改动；
    在目的主机处再把外层的IP/UDP封装去掉，就可以获得完整的IPSec数据包。
    NAT-T在实际运作时，第一步是探测通信双方是否支持NAT-T，
    这主要通过IKE协商时彼此发送的第一个数据包来判断。
    在判断双方均支持NAT-T后，进入到第二步NAT设备的发现，
    即去发现在上方的链路中间是否存在NAT设备，
    通过判断通信双发的IP地址或者端口是否发生了改变而得知。
    当发现上方的链路中存在NAT设备后，
    通信双方NAT-T开始协商所采用的数据包封装方式，至此完成协商过程。

--------------------------------------------------------------------------------------
ip xfrm 配置nat穿越
    无nat穿越时的配置
        主机A：
        ip xfrm state add src 192.168.4.127 dst 192.168.3.171 proto esp spi 0x00000301 mode tunnel auth md5 0x96358c90783bbfa3d7b196ceabe0536b enc des3_ede 0xf6ddb555acfd9d77b03ea3843f2653255afe8eb5573965df
        ip xfrm state add src 192.168.3.171 dst 192.168.4.127 proto esp spi 0x00000302 mode tunnel auth md5 0x99358c90783bbfa3d7b196ceabe0536b enc des3_ede 0xffddb555acfd9d77b03ea3843f2653255afe8eb5573965df
        ip xfrm policy add src 192.168.4.127 dst 192.168.3.171 dir out ptype main tmpl src 192.168.4.127 dst 192.168.3.171 proto esp mode tunnel
        ip xfrm policy add src 192.168.3.171 dst 192.168.4.127 dir in ptype main tmpl src 192.168.3.171 dst 192.168.4.127 proto esp mode tunnel
        主机B：
        ip xfrm state add src 192.168.4.127 dst 192.168.3.171 proto esp spi 0x00000301 mode tunnel auth md5 0x96358c90783bbfa3d7b196ceabe0536b enc des3_ede 0xf6ddb555acfd9d77b03ea3843f2653255afe8eb5573965df
        ip xfrm state add src 192.168.3.171 dst 192.168.4.127 proto esp spi 0x00000302 mode tunnel auth md5 0x99358c90783bbfa3d7b196ceabe0536b enc des3_ede 0xffddb555acfd9d77b03ea3843f2653255afe8eb5573965df
        ip xfrm policy add src 192.168.4.127 dst 192.168.3.171 dir in ptype main tmpl src 192.168.4.127 dst 192.168.3.171 proto esp mode tunnel
        ip xfrm policy add src 192.168.3.171 dst 192.168.4.127 dir out ptype main tmpl src 192.168.3.171 dst 192.168.4.127 proto esp mode tunnel
    有nat穿越时的配置
        先删除之前配置的ipsec sa：
            ip xfrm state deleteall
            ip xfrm policy与无nat穿越时的配置一致
        主机A：
        ip xfrm state add src 192.168.4.127 dst 192.168.3.171 proto esp spi 0x00000301 mode tunnel auth sha1 0x96358c90783bbfa3d7b196ceabe0536b enc aes 0xf6ddb555acfd9d77b03ea3843f2653255afe8eb5573965df encap espinudp 4500 4500 0.0.0.0
        ip xfrm state add src 192.168.3.171 dst 192.168.4.127 proto esp spi 0x00000302 mode tunnel auth sha1 0x99358c90783bbfa3d7b196ceabe0536b enc aes 0xffddb555acfd9d77b03ea3843f2653255afe8eb5573965df encap espinudp 4500 4500 0.0.0.0
        ip xfrm policy add src 192.168.4.127 dst 192.168.3.171 dir out ptype main tmpl src 192.168.4.127 dst 192.168.3.171 proto esp mode tunnel
        ip xfrm policy add src 192.168.3.171 dst 192.168.4.127 dir in ptype main tmpl src 192.168.3.171 dst 192.168.4.127 proto esp mode tunnel
        主机B：
        ip xfrm state add src 192.168.4.127 dst 192.168.3.171 proto esp spi 0x00000301 mode tunnel auth sha1 0x96358c90783bbfa3d7b196ceabe0536b enc aes 0xf6ddb555acfd9d77b03ea3843f2653255afe8eb5573965df encap espinudp 4500 4500 0.0.0.0
        ip xfrm state add src 192.168.3.171 dst 192.168.4.127 proto esp spi 0x00000302 mode tunnel auth sha1 0x99358c90783bbfa3d7b196ceabe0536b enc aes 0xffddb555acfd9d77b03ea3843f2653255afe8eb5573965df encap espinudp 4500 4500 0.0.0.0
        ip xfrm policy add src 192.168.4.127 dst 192.168.3.171 dir in ptype main tmpl src 192.168.4.127 dst 192.168.3.171 proto esp mode tunnel
        ip xfrm policy add src 192.168.3.171 dst 192.168.4.127 dir out ptype main tmpl src 192.168.3.171 dst 192.168.4.127 proto esp mode tunnel
