��ˣ�Backends����һ���ṩ������Ϣ�Ŀɲ��ģ��/���ģ�飨pluggable modules��
�������ṩһ������һ�飩api���Թ��ػ���������ȡ������Ϣ
They have to implement an API which the daemon core uses to get configuration

�� stroke_socket_create ��
    ��������ʼ���� private_stroke_socket_t ����
    �ö����У�����������ʼ���ˣ�cred���ڴ�֤�飩��ca��ipsec.conf/ca����config���ڴ�����backend--�����ڴ��е����ã���
    attribute��IKEv2 cfg attribute provider����list��uri��service��Service accepting stroke connections���ȵȳ�Ա
    ���У�config ��Ա��ͬʱ��ӵ� charon->backends �У������ģ���ca��cred��ͬʱ��ӵ� lib->credmgr �У�
    �ɴ˿ɼ���backends�𵽶Լ��ص��ڴ�����õĹ�����ȡ�����ô�
    
�� register_vici ��  
    Ϊ�Ѵ��ڵ� vici ��private_vici_plugin_t�������� 
    query��control��cred��authority��config��attrs �ȵȳ�Ա����
    ���ǵĹ��ֱܷ��ǣ�
        query��      Query helper, provides various commands to query/list daemon info.
        control��    Control helper, provides initiate/terminate and other commands.
        cred��       In-memory credential backend, managed by VICI.
        authority��  In-memory certification authority backend, managed by VICI.
        config��     In-memory configuration backend, managed by VICI.
        attr��       IKE configuration attribute backend for vici.
    ���У�config����ӵ�charon->backends�������ģ��� attrs->provider����ӵ�charon->attributes�ȣ�
    ͬ�ϣ�backends�𵽶Լ��ص��ڴ�����õĹ�����ȡ�����ô�