1. ����׼��
    ���
        https://docs.strongswan.org/docs/5.9/config/quickstart.html
        ���ö˵��˵�����ģʽ��sun:192.168.3.99  moon:192.168.3.108
    ֤�����ɣ�
        https://docs.strongswan.org/docs/5.9/pki/pkiQuickstart.html
        file://ʹ��strongswan��pki��������rsa֤��.txt
        ע1�����ɵ�ed25519֤�飬swanctl����˽Կ������Ϊ����rsa֤��
        ע2��֤��ķ���·��һ��Ҫ��ȷ
             charon������ʱ�����һЩ����֤��·����ʾ���磺
             00[DMN] Starting IKE charon daemon 
             00[LIB] openssl FIPS mode(2) - enabled 
             00[CFG] loading ca certificates from '/etc/strongswan/ipsec.d/cacerts'
             00[CFG] loading aa certificates from '/etc/strongswan/ipsec.d/aacerts'
             00[CFG] loading ocsp signer certificates from '/etc/strongswan/ipsec.d/ocspcerts'
             00[CFG] loading attribute certificates from '/etc/strongswan/ipsec.d/acerts'
             ����Ҫ��������֤�����������Ŀ¼��
             /etc/strongswan/swanctl/x509ca/strongswanCert.pem
             /etc/strongswan/swanctl/x509/sunCert.pem
             /etc/strongswan/swanctl/private/sunKey.pem
     ����֤����������ã�
        swanctl --help
        swanctl --load-creds  //load certificates and private keys into the charon
        swanctl --load-conns  //loads the connections defined in swanctl.conf    
        ִ���������charon�����������Ϣ��
            12[CFG] loaded certificate 'C=CH, O=strongswan, CN=sun.strongswan.org'
            06[CFG] loaded certificate 'C=CH, O=strongSwan, CN=strongSwan Root CA'
            15[CFG] loaded RSA private key
            12[CFG]   id not specified, defaulting to cert subject 'C=CH, O=strongswan, CN=sun.strongswan.org'
            12[CFG] added vici connection: host-host
            12[CFG] installing 'host-host'
            //ǰ���12��06���������Ǹ��߳��������Ϣ�� [CFG]����������������־
    wiresharkץ��
        �ڲ�����charonʱ��3.99��������ping 3.108
        3.108 ����charon��δִ��swanctl�������ǰ��3.99��������pingͨ3.108
        3.108 ����charon����ִ��swanctl��������3.99�޷�pingͨ3.108
        3.99 ����charon����ִ��swanctl��������3.99����pingͨ3.108
    ע��������Ҫ����ǽ���ȷſ�udp 500/[4500]�˿ڣ�
        ����޷�pingͨ�����������ҷ���ǽ�����ԭ������ӷſ�ah/esp/icmp/tcp/udp��Э��
        ���⣬���עץ����spi��ip xfrm status�г���spi�Ƿ�һ�£������һ�£�˵�������SA���ԣ��������
2. ISAKMP���ķ�װ
        �Σ�https://blog.csdn.net/bytxl/article/details/36016141
        �Σ�file://YDT1897.pdf:��26ҳ
        ͼ��file://../imgs/ISAKMP���ķ�װ.png
        IP����ͷ
            Դ��ַsrc�����˷���IKEЭ�̵�IP��ַ�������ǽӿ�IP��ַ��Ҳ������ͨ���������õ�IP��ַ��
            Ŀ��IP��ַDst���Զ˷���IKEЭ�̵�IP��ַ�����������á�
        UDP����ͷ
            IKEЭ��ʹ�ö˿ں�500����Э�̡���ӦЭ�̡�
            ��ͨ��˫�����й̶�IP��ַʱ������˿���Э�̹����б��ֲ��䡣
            ��ͨ��˫��֮����NAT�豸ʱ��NAT��Խ��������IKEЭ��������⴦���������أ���
        ISAKMP����ͷ
            Initiator��s Cookie��SPI����responder��s Cookie��SPI����
                ��IKEv1�汾��ΪCookie����IKEv2�汾��CookieΪIKE��SPI��Ψһ��ʶһ��IKE SA��
            Next Payload��
                ��ʶ��Ϣ����һ���غɵ����͡�
                һ��ISAKMP�����п���װ�ض���غɣ����ֶ��ṩ�غ�֮��ġ����ӡ�������
                ����ǰ�غ�����Ϣ�����һ���غɣ�����ֶ�Ϊ0��
            Version��
                IKE�汾��1/2��
            Exchange Type��
                IKE����Ľ������͡��������Ͷ�����ISAKMP��Ϣ��ѭ�Ľ���˳��
                        ��������                ֵ
                         NONE                    0
                         Base                    1
                         Identity Protection     2
                         Authentication Only     3
                         Aggressive              4
                         Informational           5
                         ISAKMP Future Use       6 - 31
                         DOI Specific Use        32 - 239   //34:IKE_SA_INIT
                         Private Use             240 - 255
            Flags��
                Ϊ ISAKMP �������õĸ���ѡ��
            Message ID��
                Ψһ����Ϣ��ʶ��������ʶ���2�׶ε�Э��״̬��
            Message Length��
                ȫ����Ϣ��ͷ����Ч�غɣ�������λ����
            Type Payload / ISAKMP Payload��
                �غ����ͣ�ISAKMP����Я��������Э��IKE SA��IPSec SA�ġ�����������
                �غ������кܶ��֣���ͬ�غ�Я���ġ�����������ͬ��
                �Σ�file://YDT1897.pdf:��8ҳ
            ˵����
                1��IKE�����������й�һ�δ�ĸĽ����ϵ�IKE����ΪIKEv1���Ľ����IKE����ΪIKEv2��
                   ���߿��Կ����Ǹ��ӹ�ϵ��Ѫ����У��������ܲ��䣻����ʤ�������������˳���Ľ�����
                2��IKEv1�汾�п����ڽ��������ֶβ鿴Э��ģʽ
                   �׶�1��Ϊ����ģʽ����ģʽ��Ұ��ģʽ���׶�2���ÿ���ģʽ��
                   ��ģʽ������������Ұ��ģʽ��Ϊ�����ʵ����������ġ�
                   IKEv2�汾�ж����˲鿴����IKE SA��CHILD SA����ӦIKEv1��IPSec SA����IKE_SA_INIT��
                   IKE_AUTH��������һ��CHILD SA����CREATE_CHILD_SA������������CHILD SA����      
2. ץ������        
    ��һ��IKE_SA_INIT
        �ɼ���ISAKMP��������Ǹ�UDPЭ�飬ʹ�õĶ˿ں���500