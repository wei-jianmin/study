VMware������а�װstrongswan
    �ѵ����������
    NetworkManager-strongswan
    NetworkManager-strongswan-gnome.x86_64
    strongswan-charon-nm.x86_64 
        �� NetworkManager-strongswan ����
    strongswan-libipsec.x86_64
    strongswan.x86_64
    ��أ�
    network-manager-strongswan
        NetworkManager attempts to keep an active network connection 
        available at all times. 
        It is intended primarily for laptops where it allows easy switching 
        between local wireless networks, 
        it��s also useful on desktops with a selection of different interfaces to use. 
        It is not intended for usage on servers.
        This package provides a VPN plugin for strongSwan, 
        providing easy access to IKEv2 IPSec VPN's.
        
https://www.cnblogs.com/shaoyangz/p/10345698.html
�ṩ��һ���˵��˵�����ʵ����˵��Ҳ�Ƚϵ�λ
    swanctlʹ��vici������Ƽ���
        λ�� /usr/sbin/swanctl
        ʹ�� /etc/swanctl Ŀ¼�µ��ļ�
    starterʹ��stroke��������Ƽ���
        λ�� /usr/libexec/ipsec
        ʹ�� /etc �µ� ipsec.conf��ipsec.secrets

https://docs.strongswan.org/docs/5.9/config/quickstart.html
�����м���strongswan�Ĺٷ�����        
    
https://www.strongswan.org/testing/testresults
�����ṩ��ȫ��ĸ������ε�strongswan����ʵ��
    
swanctl.conf �����ļ����﷨
    https://docs.strongswan.org/docs/5.9/swanctl/swanctlConf.html
    ������swanctl.conf�Ĺٷ�˵��
    ���ļ�Ϊ swanctl --load-* commands.swanctl.conf �ṩ���ӡ����ܺ� IP ��ַ��    
    <authorities>
        ������֤�����������ԵĲ���
    <connections>
        ���� IKE �������õĲ���
    <secrets>
        ���� IKE/EAP/XAuth �����֤��˽Կ���ܵ�����
        ecret ���ֲ��þ����ض�ǰ׺���Ӳ��֣���ǰ׺���� secret ���͡�
        �����鶨���κ�˽Կ���ܿ����Ϊʹ�ü�����Կû�������İ�ȫ�ô���
        �ڼ���ƾ��ʱ��Ҫôδ���ܵش洢��Կ��Ҫô�ֶ�������Կ
        
swanctl��vici�Ĺ�ϵ
    The vici [?vit?i] plugin provides VICI, the Versatile IKE Configuration Interface
    swanctl	��ͨ�� vici �ӿڽ���ͨ�ŵ����úͿ���ʵ�ó���
    vici �����strongswan�Ĳ�����ṩ�˶๦�� IKE ���ƽӿڣ�
    ����˼�壬��Ϊ�ⲿӦ�ó����ṩ��һ���ӿڣ�
    �����������ã������Կ��ƺͼ��� IKE �ػ����� charon
    strongSwanͨ������������ض�����Ķ���ϵͳ���ṩIKE������
    ����ϵͳ�Ŀ�����Աͨ����Ҫ�Զ����úͿ��� IKE �ػ�����
    ���еĺͽӿڴ�δ����Ƴ��Զ����ġ�
    ��д��Щ���ߵĽű������ѣ�������Ϣ���鷳��
    VICI��ͼͨ���ṩ�ȶ���IPC�����̼�ͨ�ţ��ӿ�������ϵͳ�����̵������
    �����ⲿ���߲�ѯ�����úͿ���IKE�ػ����̡�
    VICI������ͻ�����û���swanctl��
    ����һ���������úͿ���charon��������Ӧ�ó���
    Ĭ������£��ò����������״̬��
    ������ʹ�� ./configure ѡ�����vici �� --disable-vici
    
    
    
        