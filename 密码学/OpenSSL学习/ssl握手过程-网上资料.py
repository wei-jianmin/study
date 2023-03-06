https://www.jianshu.com/p/8dc93f3946c3
    SSLͨ�Ź��̵Ĺٷ��淶�� RFC5246
    
�Σ� https://blog.csdn.net/H_O_W_E/article/details/125247938
    ������Ϣ�ж���������׼���
    ��������Կ�����㷨+�����֤&�����㷨+ժҪ�㷨
    rfc5289 �ж���������׼�:
        CipherSuite TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256  = {0xC0,0x2B};
        CipherSuite TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384  = {0xC0,0x2C};
        CipherSuite TLS_ECDH_ECDSA_WITH_AES_128_GCM_SHA256   = {0xC0,0x2D};
        CipherSuite TLS_ECDH_ECDSA_WITH_AES_256_GCM_SHA384   = {0xC0,0x2E};
        CipherSuite TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256    = {0xC0,0x2F};
        CipherSuite TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384    = {0xC0,0x30};
        CipherSuite TLS_ECDH_RSA_WITH_AES_128_GCM_SHA256     = {0xC0,0x31};
        CipherSuite TLS_ECDH_RSA_WITH_AES_256_GCM_SHA384     = {0xC0,0x32};
    �� TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 Ϊ����
        TLS �� ���������׼�����tlsЭ��
        ECDHE �� ��Կ����
        ECDSA_WITH_AES_128_GCM �� �����֤&�ӽ���
        SHA256 �� ժҪ
        
https://blog.csdn.net/fw0124/article/details/40983787
    ���ֹ���ʵ���Ͼ���ͨ��˫��Э�̽���һ�����ڶԳƼ��ܵ���Կ�Ĺ���
    �������ʵ���ϲ������������:client random, server random, pre-master secret.
    ǰ����������������Ĵ��͵ģ�ֻ��pre-master secret�Ǽ��ܵģ�RSA����DH)��  
    
    һ������֤���ʱ��ǩ���㷨����ѡ��RSA����DSA�㷨
        ���serverʹ��RSA֤�飬
            RSA����������ǩ��Ҳ�����������ԳƼ��ܣ�
            pre-master secret������server��RSA֤���а����Ĺ�Կ���ܵġ�
        ���serverʹ��DSA֤�飬
            DSAֻ������ǩ�������Ի���Ҫʹ��DH�㷨��������Կ��
    
    �ͻ��˷��������
        client_hello
            ��1��֧�ֵ�Э��汾������TLS 1.0
            ��2��֧�ֵļ����㷨(Cipher Specs)
            ��3���ͻ������ɵ������1(Challenge)���Ժ���������"�Ի���Կ"��
    ����˷����ͻ���
        server_hello
            ��1�� ȷ��ʹ�õ�Э��汾
            ��2�� ���������ɵ������2���Ժ���������"�Ի���Կ"
            ��3�� session id
            ��4�� ȷ��ʹ�õļ����㷨
        certificate
            ������֤��
        server_key_exchange
            �����DH�㷨�����﷢�ͷ�����ʹ�õ�DH������RSA�㷨����Ҫ��һ����
        certificate_request
            Ҫ��ͻ����ṩ֤�飬����
            ��1���ͻ��˿����ṩ��֤������
            ��2�����������ܵ�֤��distinguished name�б�
                 ������root CA����subordinate CA��
                 ���������������trust keystore, 
                 ������г�������trust keystore�е�֤���distinguished name��
        server_hello_done
            server hello����
    �ͻ��˷��������
        certificate
            �ͻ���֤��
        client_key_exchange
            ����pre-master secret���ͻ������ɵ������������
            ����ǲ���RSA�㷨��������һ��48�ֽ��������
            Ȼ����server�Ĺ�Կ����֮���ٷ��뱨���У�
            �����DH�㷨�����﷢�͵ľ��ǿͻ��˵�DH������
            ֮��������Ϳͻ��˸���DH�㷨�����Լ������ͬ��pre-master secret��
        certificate_verify
            ����"ʹ�ÿͻ���֤���<����һ��Ϊֹ�յ��ͷ��͵�����������Ϣ>ǩ��"�Ľ����
        change_cipher_spec
            �ͻ���֪ͨ��������ʼʹ�ü��ܷ�ʽ���ͱ��ġ�
            �ͻ���ʹ�������3�������client random, server random, pre-master secret, 
            �����48�ֽڵ�master secret, ������ǶԳƼ����㷨����Կ��
        finished
            �ͻ��˷��͵�һ�����ܱ��ġ�
            ʹ��HMAC�㷨�����յ��ͷ��͵�����������Ϣ��ժҪ��
            Ȼ��ͨ��RFC5246�ж����һ��α����PRF�������������ܺ��͡�
    ����˷����ͻ���
        change_cipher_spec
        finished
        
https://blog.csdn.net/fw0124/article/details/40875629
    ͼ��SSL/TLSЭ��
    
�����������
    https://blog.csdn.net/mrpre/article/details/77973464
        ��1������master key
            ����Կ�����������
                ��һ������ buf1= ��master secret�� + client_random +  server_random
                �ڶ�������PRF���㡣
                    PRF�����labelΪ buf1��secretΪpre_master_key������Ϊmaster key
            master_secret = PRF(pre_master_secret, "master secret",
                                ClientHello.random + ServerHello.random) [0..47];
        ��2�����ɶԳ���Կsymmetry key
            ��ʹ�ǻỰ�������̣�Ҳ����жԳ���Կ���㣬�Ự���ÿ��Իָ�֮ǰ��master key
            ��һ������ buf2 = ��key expansion�� + server_random + client_ranom
            �ڶ��� ���� PRF���㡣
                PRF���label�� buf2��secretΪmaster_key������Ϊsymmetry key
            key_block = PRF(SecurityParameters.master_secret,
                            "key expansion",
                            SecurityParameters.server_random +
                            SecurityParameters.client_random);
        ��3������server key exchange 
            ��server key exhange ǩ��ǰ��
            ��Ҫ��server key exchange ���Ľ���ժҪ���㣬
            ժҪ���Ǽ򵥵ĶԱ��Ľ���hash��Ҳ��Ҫ��������롣
            ��һ�� ���� buf3 = client_random + server_random + value
            �ڶ��� HASH(buf3)
        ����׿����룬�ӹ����������������������Ч��ֹ�طŹ�����
            ����session resumeʱ�򣬵�ǰ�Ự��master key����һ���Ự��master key��
            ���ֱ��ʹ�����master key���м��ܣ��ͺ����׽����طŹ�����
            ���������ɶԳ���Կʱ��ʹ�õ�ǰ�����ֵ��������master key����һ��prf��
            ʹ�õ�ǰ�ӽ��ܵ�key����һ���Ự�Ĳ�һ����
            �м��˾�û�취�ط�һ����Ч��application data��

        
    