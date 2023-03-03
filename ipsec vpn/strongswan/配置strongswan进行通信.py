VMware虚拟机中安装strongswan
    搜到如下软件：
    NetworkManager-strongswan
    NetworkManager-strongswan-gnome.x86_64
    strongswan-charon-nm.x86_64 
        被 NetworkManager-strongswan 依赖
    strongswan-libipsec.x86_64
    strongswan.x86_64
    相关：
    network-manager-strongswan
        NetworkManager attempts to keep an active network connection 
        available at all times. 
        It is intended primarily for laptops where it allows easy switching 
        between local wireless networks, 
        it’s also useful on desktops with a selection of different interfaces to use. 
        It is not intended for usage on servers.
        This package provides a VPN plugin for strongSwan, 
        providing easy access to IKEv2 IPSec VPN's.
        
https://www.cnblogs.com/shaoyangz/p/10345698.html
提供了一个端到端的配置实例，说明也比较到位
    swanctl使用vici插件（推荐）
        位于 /usr/sbin/swanctl
        使用 /etc/swanctl 目录下的文件
    starter使用stroke插件（不推荐）
        位于 /usr/libexec/ipsec
        使用 /etc 下的 ipsec.conf、ipsec.secrets

https://docs.strongswan.org/docs/5.9/config/quickstart.html
这里有几个strongswan的官方案例        
    
https://www.strongswan.org/testing/testresults
这里提供了全面的各种情形的strongswan配置实例
    
swanctl.conf 配置文件的语法
    https://docs.strongswan.org/docs/5.9/swanctl/swanctlConf.html
    这里是swanctl.conf的官方说明
    该文件为 swanctl --load-* commands.swanctl.conf 提供连接、机密和 IP 地址池    
    <authorities>
        定义认证机构互补属性的部分
    <connections>
        定义 IKE 连接配置的部分
    <secrets>
        定义 IKE/EAP/XAuth 身份验证和私钥解密的秘密
        ecret 部分采用具有特定前缀的子部分，该前缀定义 secret 类型。
        不建议定义任何私钥解密口令，因为使用加密密钥没有真正的安全好处。
        在加载凭据时，要么未加密地存储密钥，要么手动输入密钥
        
swanctl与vici的关系
    The vici [?vit?i] plugin provides VICI, the Versatile IKE Configuration Interface
    swanctl	是通过 vici 接口进行通信的配置和控制实用程序
    vici 插件（strongswan的插件）提供了多功能 IKE 控制接口，
    顾名思义，它为外部应用程序提供了一个接口，
    不仅可以配置，还可以控制和监视 IKE 守护程序 charon
    strongSwan通常用于在针对特定需求的定制系统中提供IKE服务功能
    此类系统的开发人员通常需要自动配置和控制 IKE 守护程序
    现有的和接口从未被设计成自动化的。
    编写这些工具的脚本很困难，返回信息很麻烦。
    VICI试图通过提供稳定的IPC（进程间通信）接口来改善系统集成商的情况，
    允许外部工具查询，配置和控制IKE守护进程。
    VICI界面最突出的用户是swanctl，
    这是一个用于配置和控制charon的命令行应用程序。
    默认情况下，该插件处于启用状态，
    但可以使用 ./configure 选项禁用vici ： --disable-vici
    
    
    
        