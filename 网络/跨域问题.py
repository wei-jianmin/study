�ο����ϣ�
    https://developer.mozilla.org/zh-CN/docs/Web/Security/Same-origin_policy
    
�������ͬԴ����
    ͬԴ�Ķ���
        ������� URL �� protocol��port (en-US) (�����ָ���Ļ�)�� host ����ͬ�Ļ����������� URL ��ͬԴ
        �������Ҳ����Ϊ��Э��/����/�˿�Ԫ�顱
        * IE �е�����
            ���ŷ�Χ��Trust Zones��
                �����໥֮��߶Ȼ��ŵ��������繫˾������corporate domains��������ͬԴ�������ơ�
            �˿�
                IE δ���˿ں����뵽ͬԴ���Եļ����
            ��Щ������ǲ��淶�ģ����������Ҳδ����֧��
    ��Դ�������
        ͬԴ���Կ��Ʋ�ͬԴ֮��Ľ�����������ʹ��XMLHttpRequest �� <img> ��ǩʱ����ܵ�ͬԴ���Ե�Լ��
        ��Щ����ͨ����Ϊ���ࣺ
            ����д����
                һ���Ǳ�����ġ��������ӣ�links�����ض����Լ����ύ��
            ������ԴǶ��
                һ���Ǳ�����
            ���������
                һ���ǲ��������
                
ʵ�ֿ����9�ַ���(�������ת����ҳ��)
    jsonp ��https://blog.csdn.net/qq_17175013/article/details/88984206
    cors ��https://blog.csdn.net/qq_17175013/article/details/88984274
        Access-Control-Allow-Origi
        ���壺�����ĸ�Դ���Է���
        ʵ�ʲ�����
            ���һ�������һ��������
            ǰ�˷����󵽺�˵�ʱ�򣬺�˻��ж��Ƿ��ڰ������
                ����ڣ�������Ӧͷ�����ø�ͷ��
                res.setHeader('Access-Control-Allow-Origin',ǰ�˵���);
            ......
    postMessage ��https://blog.csdn.net/qq_17175013/article/details/89165586
    document.domain ��https://blog.csdn.net/qq_17175013/article/details/89115629
    window.name ��https://blog.csdn.net/qq_17175013/article/details/89007334
    location.hash ��https://blog.csdn.net/qq_17175013/article/details/89115400
    websocket ��webSocket�������ڿ�������
    http-proxy
    nginx
            