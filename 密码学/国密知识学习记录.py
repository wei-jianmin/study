ѧϰԵ�ɣ�
    ��C++ �з�  �о��� gmssl  ���  �޸� nginx ����
    ���������� ssl Э��
    ���� һ�� stunnel �Ĺ��� �������о���
���ϲ��ң�
    https://www.gmssl.cn/gmssl/index.jsp  ����sslʵ����  
        �ṩ��x86_64������CentOS7ϵͳ�¿��õ�gmssl_openssl���gmssl_nginx���ߣ�����Դ�룩
        ������nginx�Ĳ�����ʹ�÷�����ʾ��
        ��������
            ���������ᵽ��
            "����SSL�ܹ�������ͬһ���˿ڣ�����Ӧ֧�ֱ�׼HTTPS/����HTTPS",
            ���ԣ�Nginx���������ͨ����֧�ֹ���֤�飬����Ϊʹ����gmssl(��̬��)�Ĺ�ϵ
            ����SSL�ջ���
            ����SSLʵ��ʹ���У���Ҫ����֤�顢����U�ܡ���������/��������
            ����������Ȼ�����ϣ������γ���������ط�����
        ����U�ܰ���
            ��Ҫ���������ǵ�һ��ߣ�ʹ�øù��ߣ�
            ���Է���������������֤�飬����֤�鵼���key�У���������key��
        ����SDK
            ����JCE/JSSE
                GMSDK(Java��)�ṩһ����java��JCE/JSSE����ʵ�֣�
                ����ISV�ṩ����SSL�������ɡ�
                ֧�ֵ������SSL/˫�����SSL��
                ֧�ֹ���U��(SKF�ӿ�)��
                ֧��Netty(��ҵ��)��
                ֧��Jetty(��ҵ��)��
                ֧��Spring Boot(��ҵ��)��
                ֧��OkHttp(��ҵ��)��
            ����OpenSSL
                GMSDK(OpenSSL��)�ṩһ��OpenSSL�Ĺ���ʵ�֣�
                ����ISV�ṩ����SSL�������ɡ�
                ֧�ֵ������SSL/˫�����SSL��
                ֧�ֹ���U��(SKF�ӿ�)��
    https://www.zhihu.com/question/26236094  ���˰ѹ����㷨���ɵ� OpenSSL ���ô
        GmSSL (http://gmssl.org) ��֧�ֹ����㷨�ͱ�׼��OpenSSL��֧��
        ��һ���ṩ�˷ḻ����ѧ���ܺͰ�ȫ���ܵĿ�Դ�������
    https://blog.csdn.net/wxh0000mm/category_8817109.html   opensslϵ�н���
    ������Դgmssl
        https://github.com/guanzhi/gmssl-v3-dev  guanzhi
        https://github.com/GmSSL  GmSSl��֧�ֹ����㷨��OpenSSL��֧��
    �����찲��Դ ssl+nginx
        https://github.com/jntass/TASSL-1.1.1b  tassl
            ���������찲�Ƽ����޹�˾֧�ֹ���֤���Э���TASSL
            OpenSSL��һ�׼�����Դ����İ�ȫ�׽�������ѧ�����⣬������Ҫ�������㷨�����õ���Կ��֤���װ�����ܼ�SSL/TLSЭ�飬
            ���ṩ�ḻ��API���Թ�Ӧ�ó��򿪷������Ի�����Ŀ��ʹ�á����㷺�ؼ����ڸ������͵Ĳ���ϵͳ�У�
            ��Ϊ��������֮һ������IT�����ߵ�ϲ������ʹ��ĳЩ����ϵͳû�н��伯��Ϊ�����ͨ��Դ�������أ�
            Ҳ��ʮ�����ɵع���OpenSSL�Ŀ�����Ӧ�û�����
            ����OpenSSL�Ĺ���ʮ��ǿ���ҷḻ��Ҳ�����˹��ܵ�����㷨�����Ƕ��ڹ��ܵ�SSLЭ�鲢��֧�֡�
            ������ƹ㼰�о��й�����������ϵ�Ĺ�����밮������˵��ȴ��ʮ�����ε����顣 
            ����Ҳ�����Ų��������ͬ�ʣ������Ž�OpenSSL���ܻ��������඼�����ڹ�˾�ڲ�����ʹ�ã�����ڹ���SSL���ƹ㲻����
            ���������״�����������찲��˾������ʱ����о���������2017���ϰ����Ƴ��찲�����OpenSSL��Ҳ����TaSSL��
            ������й�����������ϵ�޷���������OpenSSLӦ�õ�ʵ�����⡣�����������Ƴ��˸���openssl-1.1.1b�汾��tassl-1.1.1b_R_0.8�汾��
            ����Դ�����ʽ�ṩ����������Ҳο�ʹ�ã�Ϊ�ٽ����ܵ��ƹ��Ӧ�ù����Լ���һ��������
            (һ)�찲TaSSL-1.1.1b_v1.0�汾�Ĺ����ص�
            1.֧�ֵ��ý����찲���ܻ�����ܿ����м��ٺ�����ȫ������
            2.������nginx-1.16.0֧�ֹ��ܣ�nginx��Դ��ַ��https://github.com/jntass/Nginx_Tassl
            3.������360�����������������ķ��ʡ�
            4.�޸���bug��һЩ�������⡣
            ssl��ص�API
            CNTLS_client_method()����ȡ����TLSv1.1��׼Э������SSL/TLS��ط�������ʹ�ÿͻ���ʹ�ñ�׼��TLSv1.1Э��������֡�ͨѶ��
            SSL_CTX_check_enc_private_key()��SSL_check_enc_private_key()��SSL_use_enc_PrivateKey()��
            SSL_use_enc_PrivateKey_ASN1()��SSL_CTX_use_enc_PrivateKey()��SSL_CTX_use_enc_PrivateKey_ASN1()��
            SSL_use_enc_PrivateKey_file()��SSL_CTX_use_enc_PrivateKey_file() Ϊ֧�ֹ���˫֤����ϵ����ӵĺ�����
            (��)TASSLʹ��˵��
            Ŀǰ��Դ�İ汾�ǻ���OpenSSL 1.1.1b 26 Feb 2019�汾��
            ����tassl-1.1.1b_v1.4�汾�� ���ص�ַ��https://github.com/jntass/TASSL-1.1.1b/archive/V_1.4.tar.gz
            �ϴ������뻷�������н�ѹ���롣
            tar xvf TASSL-1.1.1b-1.4.tar.gz
            cd TASSL-1.1.1b-1.4
            chmod u+x ./config
            ./config --prefix=/root/lib_r/tassl
            make
            make install
            ���밲װĿ¼�����˱�׼��openssl���ͷ�ļ��⣬������tassl_demo������Ŀ¼
            cd /root/lib_r/tassl/tassl_demo�����У�
            a) certĿ¼:
            �������ɲ���֤��Ľű�gen_sm2_cert.sh
            ִ��./ gen_sm2_cert.sh�����ɲ���֤��Ŀ¼certs
            b) cryptoĿ¼��
            �������Թ����㷨��ʾ��
            ִ��./mk.sh���б������
            c) sslĿ¼��
            ��������sslͨѶ�Ŀͻ��˺ͷ����
            ִ��./mk.sh���б������
        https://github.com/jntass/Nginx_Tassl  nginx_tassl
            ���ʹnginx����tasslʵ�ֹ���sslЭ�飿
            ���巽�����£�
            ����Tassl-1.1.1b_R_0.8.tgz�汾���б��룬����װ��/root/lib_r/tassl�У�
            ��������Ŀ¼��Ҫ�ڵڶ�����configureʱ���滻--with-openssl��Ŀ¼��
            ���ؽ����찲�޸ĵ�nginx-1.16.0_tassl.tgz֧�ֹ��ܵ�nginx���б��롣
            ע��configure��Ҫ������Ԥװ��pcre(����pcre2)��zlib������ᱨ��
            ./configure --with-http_ssl_module --with-stream --with-stream_ssl_module 
                        --with-openssl=/root/lib_r/tassl --prefix=/root/nginx
            make
            make install
            ����nginx��
            ����nginx.conf֤�鲿�֣�
            ssl_certificate /root/lib_r/tassl/tassl_demo/cert/certs/SS.crt; #/ǩ��֤��/
            ssl_certificate_key /root/lib_r/tassl/tassl_demo/cert/certs/SS.key; #/ǩ��˽Կ/
            ssl_enc_certificate /root/lib_r/tassl/tassl_demo/cert/certs/SE.crt; #/����֤��/
            ssl_enc_certificate_key /root/lib_r/tassl/tassl_demo/cert/certs/SE.key; #/����˽Կ/
            ע�⣺ǩ��֤���֤����;��������ǩ�����ܣ�����֤���֤����;�������ݼ��ܹ��ܡ�
            ������ܲ���ȷ���ᵼ������ʧ�ܡ�����tassl_demo/cert/�еĽű����ɵ�֤���Ѿ��߱���Ӧ����,�����������ԡ�
            �����������������360��������в��Թ�����վ��
            a) ���������
            ���ص�ַ��https://www.mesince.com/zh-cn/browser
            �����һ������ʧ�ܣ���ô����������᳢�Թ����㷨�������Ժ�����Ӷ���ʹ�ù����㷨���޷��ɹ���
            ��ʱ��Ҫ������������У����������ݣ�����������е����ݣ���ô���������һ���ٽ�������ʱ�������ȳ��Թ����㷨��
            b) 360�����
            ���ص�ַ��https://browser.360.cn/se/ver/gmzb.html
            360����������汾Ŀǰ�϶ࡣ���Һ��°汾��Windows 10ϵͳ����ż���Եĵ���ϵͳ������ 
            ����360Ҫ���Լ���Ӹ�֤�飬���û����ӻᵼ��SSL������ɺ���ʾ֤�鲻��ȷ�� 
            ��Ӹ�֤�鷽��������֤�����ctl.dat�ļ��У�
            Ȼ��Ѵ��ļ�����%appdata%/360se6\Application\User Data\Default\ctlĿ¼�У�
            ע�⣺�����"User Data\Default\ctl"��Ŀ¼�������ڣ���Ҫ�ֹ������� 
            ������β��ԣ�Ŀǰ������Ӹ�֤����Ч�İ汾360_mini_installer_sm_7.exe��
            �Ѿ���������һ���ֿ���https://github.com/jntass/GM_BROWERS �������ǵĲ��Ի�����Windows 7ϵͳ��
        https://blog.csdn.net/u011893782/article/details/106281764?
          utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault
          %7EBlogCommendFromBaidu%7Edefault-6.no_search_link&depth_1-
          utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault
          %7EBlogCommendFromBaidu%7Edefault-6.no_search_link ���Թ���
            1. ��������tassl����֤��demo���ű�·��/root/lib_r/tassl/tassl_demo/cert/gen_sm2_cert.sh
               ֤��������/root/lib_r/tassl/tassl_demo/cert/certs��
            2. ����Nginx�İ�װ·��/root/nginx�������ļ�/root/nginx/conf/nginx.conf��ָ��������֤���˽Կ
                proxy_ssl_certificate          /root/tasscard_engine/cert/server/sm2/org_ss.crt;
                proxy_ssl_certificate_key      /root/tasscard_engine/cert/server/sm2/org_ss.key;
                proxy_ssl_enc_certificate      /root/tasscard_engine/cert/server/sm2/org_se.crt;
                proxy_ssl_enc_certificate_key  /root/tasscard_engine/cert/server/sm2/org_se.key;
    pcre���飺
        PCRE(Perl Compatible Regular Expressions��Perl���ݵ�������ʽ)
        PCRE����һϵ�к�����ɣ�ʵ������Perl5��ͬ���﷨�������������ʽƥ�书�ܡ�
        PCRE�����Լ���native API��ͬʱҲ������һϵ�е�wrapper�����Լ���POSIX������ʽAPI��
        ��һ����C���Ա�д��������ʽ�����⡣
        PCRE��һ���������ĺ����⣬��Boost֮���������ʽ��С�öࡣ
        PCREʮ�����ã�ͬʱ����Ҳ��ǿ�����ܳ�����POSIX������ʽ���һЩ�����������ʽ�⡣
        PCRE����C����ʵ�ֵģ���C++ʵ�ְ汾��PCRE++��
        PCREʹ�ý̳̣�
            https://www.cnblogs.com/LiuYanYGZ/p/5903946.html
            https://ivanzz1001.github.io/records/post/nginx/2018/11/20/nginx-source_part56_1
    nginx����
        �ٶȰٿƣ�
            Nginx(engine x)��һ�������ܵ�HTTP�ͷ������web��������ͬʱҲ�ṩ��IMAP/POP3/SMTP����
            Nginx��һ����������Web ������/�������������������ʼ���IMAP/POP3�����������
            �й���½ʹ��nginx��վ�û��У��ٶȡ����������ˡ����ס���Ѷ���Ա���
            �����Ӹ߲���������£�Nginx��Apache���񲻴�����Ʒ��
            Nginx������������������������ϰ��Ǿ���ѡ������ƽ̨֮һ��
            �ܹ�֧�ָߴ� 50,000 ����������������Ӧ��
            Nginx��Ϊ���ؾ������
                Nginx �ȿ������ڲ�ֱ��֧�� Rails �� PHP ���������з���
                Ҳ����֧����Ϊ HTTP������������з���֧�� SSL �� TLSSNI��
            �����ص㣺
                Nginx������ȫ��C���Դ�ͷд�ɡ�
                Nginx���Լ��ĺ����⣬���ҳ���zlib��PCRE��OpenSSL֮�⣬��׼ģ��ֻʹ��ϵͳC�⺯����
            �����������
                Nginx ͬʱҲ��һ���ǳ�������ʼ��������
            Nginx ��һ����װ�ǳ��ļ򵥡������ļ��ǳ���ࣨ���ܹ�֧��perl�﷨����Bug�ǳ��ٵķ���
            Nginx �����ر����ף����Ҽ�����������7*24��������У���ʹ����������Ҳ����Ҫ����������
            �㻹�ܹ�����Ϸ��������½�������汾��������
        https://www.cnblogs.com/muhy/p/10528543.html  Nginx����ԭ��
            Nginx����Ϳ����й���վ������HTTP������Ҳ������Ϊ������������ʹ��.
            ������� vs �������
                �ͻ���֪����������������������������λ�ڿͻ��࣬�𵽻�����ٵĵ�Ч����
                �Կͻ��˶��ԣ�������������������ԭʼ�����������ҿͻ��˲���Ҫ�����κ��ر������
                �ͻ����������������ռ��е����ݷ�����ͨ����
            ���ŷ�������ж����ĸ�ԭʼ������ת�����󣬲�����õ����ݷ��ظ��ͻ��ˡ�
            ͨ�Ż��Ʋ���epollģ�ͣ�֧�ָ���Ĳ������ӡ�
            ��� Nginx Proxy ��˵�ĳ̨ Web ������崻��ˣ�����Ӱ��ǰ�˷��ʡ�
            Nginx���¼�������ƣ�
                ����һ��������web��������˵���¼�ͨ�����������ͣ������¼����źš���ʱ����
                Nginxʹ���첽���������¼�������ơ�
                ���嵽ϵͳ���þ�����select/poll/epoll/kqueue������ϵͳ���á�
                ��epollΪ�������¼�û��׼����ʱ���ͷ���epoll(����)���档
                ������¼�׼�����ˣ���ô��ȥ����
                ����¼����ص���EAGAIN����ô�����������epoll���档
                �Ӷ���ֻҪ���¼�׼�����ˣ����Ǿ�ȥ��������
                ֻ�е�����ʱ�䶼û��׼����ʱ������epoll������š�
                ���� �����ǾͿ��Բ�����������Ĳ����ˣ���Ȼ������Ĳ���������ָδ�����������
                �߳�ֻ��һ��������ͬʱ�ܴ��������Ȼֻ��һ���ˣ�ֻ�����������в��ϵ��л����ѣ�
                �л�Ҳ����Ϊ�첽�¼�δ׼���ã��������ó��ġ�
                ������л���û���κδ��ۣ���������Ϊѭ��������׼���õ��¼�����ʵ�Ͼ��������ġ�
                ����߳���ȣ������¼�����ʽ���кܴ�����Ƶģ�����Ҫ�����̣߳�
                ÿ������ռ�õ��ڴ�Ҳ���٣�û���������л����¼�����ǳ�����������
                �������ٶ�Ҳ���ᵼ����ν����Դ�˷ѣ��������л�����
            Nginx���ڲ������̣�ģ��
                nginx���Զ���̵ķ�ʽ�������ģ���ȻnginxҲ��֧�ֶ��̵߳ķ�ʽ��,
                ֻ�����������ķ�ʽ���Ƕ���̵ķ�ʽ��Ҳ��nginx��Ĭ�Ϸ�ʽ��
                nginx�������󣬻���һ��master���̺Ͷ��worker���̡�
                master������Ҫ��������worker���̣�
                    �������������źţ����worker���̷����źţ�
                    ��� worker���̵�����״̬,��worker�����˳���(�쳣�����)��
                    ���Զ����������µ�worker���̡�
                �������������¼������Ƿ���worker�������������ˡ�
                ���worker����֮���ǶԵȵ�,����ͬ�Ⱦ������Կͻ��˵�����,�����̻���֮���Ƕ����ġ�
                һ������,ֻ������һ��worker�����д���,һ��worker����,�����ܴ����������̵�����
                worker���̵ĸ����ǿ������õģ�һ�����ǻ����������cpu����һ�¡�
                master�����ڽӵ�./nginx -s reload�źź󣬻������¼��������ļ���
                Ȼ���������µĽ��̣����������ϵĽ��̷����źţ��������ǿ��Թ��������ˡ�
                �µĽ����������󣬾Ϳ�ʼ�����µ����󣬶��ϵĽ������յ����� master���źź�
                �Ͳ��ٽ����µ����󣬲����ڵ�ǰ�����е�����δ���������������ɺ����˳���
                worker����֮����ƽ�ȵģ�ÿ�����̣���������Ļ���Ҳ��һ���ģ�
                ÿ��worker���̶��Ǵ�master ����fork(����)������
                ��master�������棬�Ƚ������socket������ͬһip��port����
                Ȼ����fork����Ӧ��worker���̣�ÿ��worker���̶�����ȥaccept���Ե�socket��
                ��һ�����ӽ�����������accept�����socket����Ľ��̣������յ�֪ͨ��
                ��ֻ��һ�����̿���accept������ӣ���������acceptʧ�ܣ�������ν�ľ�Ⱥ����
                ��Ȼ��nginxҲ�����Ӷ�����������nginx�ṩ��һ��accept_mutex���������
                �������ϣ����ǿ��Կ�����һ������accept�ϵ�һ�ѹ�������
                ���������֮��ͬһʱ�̣���ֻ����һ��������accpet���ӣ������Ͳ����о�Ⱥ�����ˡ�
                accept_mutex��һ���ɿ�ѡ����ǿ�����ʾ�عص���Ĭ���Ǵ򿪵ġ�
                nginx�������ֽ���ģ����ʲô�ô��أ����ö����Ľ��̣������û���֮�䲻��Ӱ�죬
                һ�������˳����������̻��ڹ��������񲻻��жϣ�
                master������ܿ����������µ�worker���̡�
                ��Ȼ��worker���̵��쳣�˳����϶��ǳ�����bug�ˣ��쳣�˳���
                ��ᵼ�µ�ǰworker�ϵ���������ʧ�ܣ���������Ӱ�쵽�����������Խ����˷��ա�
                ÿ��work�߳�����Ϊʹ����epool�첽�������ķ�ʽ�������������Կ��Զಢ������
                ������IIS��ÿ�����󶼻��ռһ�������̣߳���ͬʱ�м�ǧ�����󣬾͵��м�ǧ���̣߳�
                ��Щ�̲߳���ռ���ڴ�󣬶���ǰ�̼��л�������cpu����Ҳ�ܴ��������ܾ��ϲ�ȥ�ˡ�
            Nginx��δ���һ������
                nginx������ʱ������������ļ����õ���Ҫ�����Ķ˿���ip��ַ��
                Ȼ����nginx��master�������棬�ȳ�ʼ���������ص�socket
                (����socket������addrreuse��ѡ��󶨵�ָ����ip��ַ�˿ڣ���listen)��
                Ȼ����fork������ӽ��̳�����Ȼ���ӽ��̻Ὰ��accept�µ����ӡ�
                �˺󣬿ͻ��˾Ϳ�����nginx���������ˡ�
                ���ͻ�����nginx�����������֣���nginx������һ�����Ӻ�
                ��ʱ��ĳһ���ӽ��̻�accept�ɹ����õ���������õ����ӵ� socket��
                Ȼ�󴴽�nginx�����ӵķ�װ����ngx_connection_t�ṹ�塣
                ���ţ����ö�д�¼�����������Ӷ�д�¼�����ͻ��˽������ݵĽ�����
                ���nginx��ͻ����������ص����ӣ����ˣ�һ�����Ӿ����������ˡ�
                ��Ȼ��nginxҲ�ǿ�����Ϊ�ͻ�������������server�����ݵģ���upstreamģ�飩
                ��ʱ��������server���������ӣ�Ҳ��װ��ngx_connection_t�С�
                ��Ϊ�ͻ��ˣ�nginx�Ȼ�ȡһ��ngx_connection_t�ṹ�壬
                Ȼ�󴴽�socket��������socket�����ԣ� �������������
                Ȼ����ͨ����Ӷ�д�¼�������connect/read/write���������ӣ�
                ���ص����ӣ����ͷ�ngx_connection_t��
                nginx��ʵ��ʱ����ͨ��һ�����ӳ�������ģ�
                ÿ��worker���̶���һ�����������ӳأ����ӳصĴ�С��worker_connections��
                ��������ӳ����汣�����ʵ������ʵ�����ӣ�
                ��ֻ��һ��worker_connections��С��һ��ngx_connection_t�ṹ�����顣
                nginx��ͨ��һ������free_connections���������еĿ���ngx_connection_t��
                ÿ�λ�ȡһ������ʱ���ʹӿ������������л�ȡһ����������ٷŻؿ��������������档
                ����worker_connections������һ��Nginx�������ܽ����������������
                ��Ҫע����ǣ���Nginx��Ϊ�������ʹ��ʱ����һ���������������ӣ�
                һ�������Կͻ��˵����ӣ�һ����Nginx�����������������ӡ�
        https://www.php.cn/nginx/422205.html  Nginx��Tomcat�ĶԱ�
            Tomcat ��������һ����ѵĿ���Դ�����Web Ӧ�÷�����������������Ӧ�÷�������
            ����С��ϵͳ�Ͳ��������û����Ǻܶ�ĳ����±��ձ�ʹ�ã��ǿ����͵���JSP �������ѡ��
            tomcatһ��������̬�����Ż��õõ���֧��jsp�Ľ�������Ҫ����JDK֧�֡�
            nginx����һ��������̬�������߱���̬�������ܣ�
            ��Ҫ�������������ͨ���������Эͬ�ž߱���̬���ܣ�����php��tomcat��
            ����proxypass��win2008��iis��������ASP�Ķ�̬���ӵȣ�
            ��nginx�ھ�̬�ϵĹ��ܷǳ�ǿ��Ҳ�������ʿ��ƣ�
            ���ҿ������ɸ���Э�鸺�ط�����
            �����ܷ�������ٲ���ϵͳ���ŵ�����£�tomcatһ��֧�ֲ���������100������ˣ�
            nginx�ھ�̬����֧�ֲ������ɴＸ��
        https://www.cnblogs.com/crazylqy/p/6891929.html Nginx���� : ��֯�ṹ��ʹ��
            Nginx ���ں˺�ģ�����
                �ں�
                    �ں˵���Ʒǳ�΢С�ͼ�࣬��ɵĹ���Ҳ�ǳ��򵥣�
                    ����ͨ�����������ļ����ͻ�������ӳ�䵽һ�� location block
                    ��location �� Nginx�����е�һ��ָ����� URL ƥ�䣩��
                    �������location�������õ�ÿ��ָ���������ͬ��ģ��ȥ�����Ӧ�Ĺ�����
                ģ��    
                    ����ģ�飺
                        HTTP ģ�顢 EVENT ģ��� MAIL ģ��
                    ����ģ�飺 
                        HTTP Access ģ�顢HTTP FastCGI ģ�顢
                        HTTP Proxy ģ��� HTTP Rewriteģ��
                    ������ģ�飺
                        HTTP Upstream Request Hash ģ�顢 
                        Notice ģ��� HTTP Access Keyģ�顣
            Nginxʹ��
                ������whereis nginx�ҵ�NginxĿ¼����Ŀ¼��
                conf ��������ļ���html �����ҳ�ļ�
                logs �����־��    sbin   shell������ֹͣ�Ƚű�
                ��sbinĿ¼�£�./nginx����nginx
                ���¶�ȡ�����ļ��� nginx -s reload
                Nginx�źſ��ƣ�
                    TERM, INT  ����ֹͣ��ɱ�����̣�
                    QUIT       ���ŵĹرս��̣���������������ٹر�
                    HUP        �ı������ļ���ƽ�����ض������ļ�
                    USR1       �ض���־������־����/�շָ�ʱ����
                    USR2       ƽ��������
                    WINCH       ���ŹرվɵĽ��̣����USR2����������
                ��� nginx.conf�����ļ�   ./nginx -t
                ����  ./nginx -s reload
                ֹͣ  ./nginx -s stop
            ѧϰNginx�Ƽ��鼮��
                1. ����������Nginx��
                2. ��ʵսNginx��ȡ��Apache�ĸ�����Web��������
                3. ���������Nginx��ģ�鿪����ܹ�������
                4. ���������Nginx��ģ�鿪����ܹ�������
                5. ����սNginx������������Web��������������ά��
                6. ����սNginxϵͳ��������Web�������������ά��
        https://www.cnblogs.com/crazylqy/p/6891954.html Nginx������������&�����ļ�ģ��
            ʲô����������
                ��������ʹ�õ����������Ӳ��������
                ����һ̨�������������ϵķ����������ֳ�һ̨̨�����⡱��������
                ÿ̨����������������һ����������վ�����Ծ��ж�����������
                ����������Intemet���������ܣ�WWW��FTP��Email�ȣ���
                ͬһ̨�����ϵ���������֮������ȫ�����ġ�
                ����վ������������ÿһ̨����������һ̨������������ȫһ����
                ������������������Ϊÿ��Ҫ���е���վ�ṩһ̨������Nginx������
                �򵥶�����һ��Nginx���̡�
                ���������ṩ����ͬһ̨��������ͬһ��Nginx���������ж����վ�Ĺ��ܡ�
            Nginx��������
                Nginx���������ļ��ǣ�nginx.conf��nginx.conf��Ҫ������£�
                # ȫ���� �м��������ӽ��̣�һ������ΪCPU�� * ����
                worker_processes  1;
                events {
                        # һ��������nginx���������ӵ�����
                        # ��1��word��ͬʱ����������ӣ�һ���ӽ��������������1024������
                        worker_connections  1024;
                }
                # ����HTTP���������ö�
                http {
                    # ��������������
                    server {
                        # ��λ���������·�����ļ��ٴζ�λ��
                        location  {
                        }
                    }
                    server {
                               ...
                    }
                }
            ������������������
                server {  
                    #�����˿� 80  
                    listen 80;   
                    #��������abc.com;  
                    server_name abc.com;
                    location / {              
                        # ���û���·�������nginx��Ŀ¼��Ҳ��д�ɾ���·��  
                        root    abc;  
                        # Ĭ����ת��index.htmlҳ��  
                        index index.html;                 
                    }  
                }
                ʹ��nginx -s reload ���������ļ�
                ��windows�������޸�host  192.168.197.142 abc.com
                Ȼ����windows������з���http://abc.com:80/�����ܷ���abc�е�index.html
            ���ڶ˿ڵ�������������
                server {
                    listen  2022;
                    server_name     abc.com;
                    location / {
                       root    /home;
                       index index.html;
                    }
                }
            ����IP��ַ������������
                server {
                    listen  80;
                    server_name  192.168.197.142;
                    location / {
                        root    ip;
                        index index.html;
                    }
                }
        https://www.cnblogs.com/crazylqy/p/6891991.html Nginx��־����
        https://www.cnblogs.com/crazylqy/p/6892010.html Location������ReWrite�﷨
        https://www.idcspy.com/15617.html Nginx�����ļ��ṹ���ܽ�ĺ�һ��
            ��Ҫ�ֳ��Ĳ���
                main��ȫ�����ã���
                    main�������õ�ָ�Ӱ�쵽�������в������ã�
                server���������ã���
                    server���ֵ�ָ����Ҫ����ָ����������������IP�Ͷ˿ڣ�
                upstream�����η��������ã���ҪΪ����������ؾ���������ã���
                    upstream��ָ����������һϵ�еĺ�˷����������÷��������˷������ĸ��ؾ��⣻
                location��URLƥ���ض�λ�ú�����ã���
                    location��������ƥ����ҳλ�ã����磬��Ŀ¼��/������/images�����ȵȣ���
            �ļ��ṹ
                1��ȫ�ֿ飺
                    ����Ӱ��nginxȫ�ֵ�ָ�
                    һ��������nginx���������û��飬nginx����pid���·������־���·����
                    �����ļ����룬��������worker process���ȡ�
                2��events�飺
                    ����Ӱ��nginx��������Ӱ�����û����������ӡ�
                    ��ÿ�����̵������������ѡȡ�����¼�����ģ�ʹ�����������
                    �Ƿ�����ͬʱ���ܶ����·���ӣ�������������������л��ȡ�
                3��http�飺
                    ����Ƕ�׶��server��
                    ���ô������棬��־����Ⱦ���������ܺ͵�����ģ������á�
                    ���ļ����룬mime-type���壬��־�Զ��壬�Ƿ�ʹ��sendfile�����ļ���
                    ���ӳ�ʱʱ�䣬�������������ȡ�
                4��server�飺
                    ����������������ز�����һ��http�п����ж��server��
                5��location�飺
                    ���������·�ɣ��Լ�����ҳ��Ĵ��������
        https://www.cnblogs.com/hunttown/p/5759959.html ������ϸע�͵�Nginx�����ļ�ʾ��
            ######Nginx�����ļ�nginx.conf�������#####
            #����Nginx���е��û����û���
            user www www;
            #nginx����������������Ϊ����CPU�ܺ�������
            worker_processes 8;
            #ȫ�ִ�����־�������ͣ�[ debug | info | notice | warn | error | crit ]
            error_log /usr/local/nginx/logs/error.log info;
            #����pid�ļ�
            pid /usr/local/nginx/logs/nginx.pid;
            #ָ�����̿��Դ򿪵��������������Ŀ
            #����ģʽ������������
            #���ָ����ָ��һ��nginx���̴򿪵�����ļ���������Ŀ��
            #����ֵӦ���������ļ�����ulimit -n����nginx�����������
            #����nginx�������󲢲�����ô���ȣ����������ulimit -n ��ֵ����һ�¡�
            #������linux 2.6�ں��¿����ļ�����Ϊ65535��worker_rlimit_nofile����ӦӦ����д65535��
            #������Ϊnginx����ʱ�������󵽽��̲�������ô�ľ��⣬���Լ�����д10240��
            #�ܲ������ﵽ3-4��ʱ���н��̿��ܳ���10240�ˣ���ʱ�᷵��502����
            worker_rlimit_nofile 65535;
            events
            {
                #�ο��¼�ģ�ͣ�use [ kqueue | rtsig | epoll | /dev/poll | select | poll ]; 
                #epollģ����Linux 2.6���ϰ汾�ں��еĸ���������I/Oģ�ͣ�
                #linux����epoll���������FreeBSD���棬����kqueueģ�͡�
                #����˵����
                #��apache���࣬nginx��Բ�ͬ�Ĳ���ϵͳ���в�ͬ���¼�ģ��
                #A����׼�¼�ģ��
                #Select��poll���ڱ�׼�¼�ģ�ͣ�
                #�����ǰϵͳ�����ڸ���Ч�ķ�����nginx��ѡ��select��poll
                #B����Ч�¼�ģ��
                #Kqueue��ʹ����FreeBSD 4.1+, OpenBSD 2.9+, NetBSD 2.0 �� MacOS X.
                #ʹ��˫��������MacOS Xϵͳʹ��kqueue���ܻ�����ں˱�����
                #Epoll��ʹ����Linux�ں�2.6�汾���Ժ��ϵͳ��
                #/dev/poll��ʹ����Solaris 7 11/99+��HP/UX 11.22+ (eventport)��
                #IRIX 6.5.15+ �� Tru64 UNIX 5.1A+��
                #Eventport��ʹ����Solaris 10�� Ϊ�˷�ֹ�����ں˱��������⣬ �б�Ҫ��װ��ȫ������
                use epoll;
                #����������������������������=������*��������
                #����Ӳ����������ǰ�湤��������������ã������󣬵��Ǳ��cpu�ܵ�100%���С�
                #ÿ����������������������������ÿ̨nginx�����������������Ϊ��
                worker_connections 65535;
                #keepalive��ʱʱ�䡣
                keepalive_timeout 60;
                #�ͻ�������ͷ���Ļ�������С��������Ը������ϵͳ��ҳ��С�����ã�
                #һ��һ������ͷ�Ĵ�С���ᳬ��1k��
                #��������һ��ϵͳ��ҳ��Ҫ����1k��������������Ϊ��ҳ��С��
                #��ҳ��С����������getconf PAGESIZE ȡ�á�
                #[root@web001 ~]# getconf PAGESIZE
                #4096
                #��Ҳ��client_header_buffer_size����4k�������
                #����client_header_buffer_size��ֵ��������Ϊ��ϵͳ��ҳ��С������������
                client_header_buffer_size 4k;
                #�����Ϊ���ļ�ָ�����棬Ĭ����û�����õģ�
                #maxָ����������������ʹ��ļ���һ�£�
                #inactive��ָ�����೤ʱ���ļ�û�������ɾ�����档
                open_file_cache max=65535 inactive=60s;
                #�����ָ�೤ʱ����һ�λ������Ч��Ϣ��
                #�﷨:open_file_cache_valid time Ĭ��ֵ:open_file_cache_valid 60 
                #ʹ�ã�/Ӱ�죩�ֶ�:http, server, location 
                #���ָ��ָ���˺�ʱ��Ҫ���open_file_cache�л�����Ŀ����Ч��Ϣ.
                open_file_cache_valid 80s;
                #open_file_cacheָ���е�inactive����ʱ�����ļ�������ʹ�ô�����
                #�������������֣��ļ�������һֱ���ڻ����д򿪵ģ�
                #�������������һ���ļ���inactiveʱ����һ��û��ʹ�ã��������Ƴ���
                #�﷨:open_file_cache_min_uses number Ĭ��ֵ:open_file_cache_min_uses 1 
                #ʹ���ֶ�:http, server, location  
                #���ָ��ָ������open_file_cacheָ����Ч�Ĳ�����һ����ʱ�䷶Χ�ڿ���ʹ�õ���С�ļ���,
                #���ʹ�ø����ֵ,�ļ���������cache�����Ǵ�״̬.
                open_file_cache_min_uses 1;
                #�﷨:open_file_cache_errors on | off Ĭ��ֵ:open_file_cache_errors off 
                #ʹ���ֶ�:http, server, location ���ָ��ָ���Ƿ�������һ���ļ��Ǽ�¼cache����.
                open_file_cache_errors on;
            }
            #�趨http���������������ķ���������ṩ���ؾ���֧��
            http
            {
                #�ļ���չ�����ļ�����ӳ���
                include mime.types;
                #Ĭ���ļ�����
                default_type application/octet-stream;
                #Ĭ�ϱ���
                #charset utf-8;
                #���������ֵ�hash���С
                #������������ֵ�hash������ָ��server_names_hash_max_size 
                #��server_names_hash_bucket_size�����Ƶġ�
                #����hash bucket size���ǵ���hash��Ĵ�С��������һ·�����������С�ı�����
                #�ڼ��������ڴ��еĴ�ȡ������ʹ�ڴ������м��ٲ���hash���ֵ��Ϊ���ܡ�
                #���hash bucket size����һ·����������Ĵ�С��
                #��ô�ڲ��Ҽ���ʱ�������������ڴ��в��ҵĴ���Ϊ2��
                #��һ����ȷ���洢��Ԫ�ĵ�ַ���ڶ������ڴ洢��Ԫ�в��Ҽ� ֵ��
                #��ˣ����Nginx������Ҫ����hash max size �� hash bucket size����ʾ��
                #��ô��Ҫ��������ǰһ�������Ĵ�С.
                server_names_hash_bucket_size 128;
                #�ͻ�������ͷ���Ļ�������С��������Ը������ϵͳ��ҳ��С�����ã�
                #һ��һ�������ͷ����С���ᳬ��1k����������һ��ϵͳ��ҳ��Ҫ����1k��
                #������������Ϊ��ҳ��С����ҳ��С����������getconf PAGESIZEȡ�á�
                client_header_buffer_size 32k;
                #�ͻ�����ͷ�����С��nginxĬ�ϻ���client_header_buffer_size���buffer����ȡheaderֵ��
                #���header��������ʹ��large_client_header_buffers����ȡ��
                large_client_header_buffers 4 64k;
                #�趨ͨ��nginx�ϴ��ļ��Ĵ�С
                client_max_body_size 8m;
                #������Ч�ļ�����ģʽ��sendfileָ��ָ��nginx�Ƿ����sendfile����(zero copy��ʽ)������ļ���
                #������ͨӦ����Ϊ on����������������ص�Ӧ�ô���IO�ظ���Ӧ�ã�������Ϊoff��
                #��ƽ�����������I/O�����ٶȣ�����ϵͳ�ĸ��ء�ע�⣺���ͼƬ��ʾ������������ĳ�off��
                sendfile on;
                #����Ŀ¼�б���ʣ��������ط�������Ĭ�Ϲرա�
                autoindex on;
                #��ѡ��������ֹʹ��socke��TCP_CORK��ѡ���ѡ�����ʹ��sendfile��ʱ��ʹ��
                tcp_nopush on;
                tcp_nodelay on;
                #�����ӳ�ʱʱ�䣬��λ����
                keepalive_timeout 120;
                #FastCGI��ز�����Ϊ�˸�����վ�����ܣ�������Դռ�ã���߷����ٶȡ�
                #���������������˼������⡣
                fastcgi_connect_timeout 300;
                fastcgi_send_timeout 300;
                fastcgi_read_timeout 300;
                fastcgi_buffer_size 64k;
                fastcgi_buffers 4 64k;
                fastcgi_busy_buffers_size 128k;
                fastcgi_temp_file_write_size 128k;
                #gzipģ������
                gzip on;               #����gzipѹ�����
                gzip_min_length 1k;    #��Сѹ���ļ���С
                gzip_buffers 4 16k;    #ѹ��������
                gzip_http_version 1.0; #ѹ���汾��Ĭ��1.1��ǰ�������squid2.5��ʹ��1.0��
                gzip_comp_level 2;     #ѹ���ȼ�
                #ѹ�����ͣ�Ĭ�Ͼ��Ѿ�����textml����������Ͳ�����д�ˣ�
                #д��ȥҲ���������⣬���ǻ���һ��warn��
                gzip_types text/plain application/x-javascript text/css application/xml;    
                gzip_vary on;
                #��������IP��������ʱ����Ҫʹ��
                #limit_zone crawler $binary_remote_addr 10m;
                #���ؾ�������
                upstream piao.jd.com 
                {
                    #upstream�ĸ��ؾ��⣬weight��Ȩ�أ����Ը��ݻ������ö���Ȩ�ء�
                    #weigth������ʾȨֵ��ȨֵԽ�߱����䵽�ļ���Խ��
                    #nginx��upstreamĿǰ֧��5�ַ�ʽ�ķ���
                    #1����ѯ��Ĭ�ϣ�
                    #ÿ������ʱ��˳����һ���䵽��ͬ�ĺ�˷������������˷�����down�������Զ��޳���
                    #2��weight
                    #ָ����ѯ���ʣ�weight�ͷ��ʱ��ʳ����ȣ����ں�˷��������ܲ����������
                    #���磺
                    #upstream bakend {
                    #    server 192.168.0.14 weight=10;
                    #    server 192.168.0.15 weight=10;
                    #}
                    #3��ip_hash
                    #ÿ�����󰴷���ip��hash������䣬����ÿ���ÿ͹̶�����һ����˷�������
                    #���Խ��session�����⡣
                    #���磺
                    #upstream bakend {
                    #    ip_hash;
                    #    server 192.168.0.14:88;
                    #    server 192.168.0.15:80;
                    #}
                    #4��fair����������
                    #����˷���������Ӧʱ��������������Ӧʱ��̵����ȷ��䡣
                    #upstream backend {
                    #    server server1;
                    #    server server2;
                    #    fair;
                    #}
                    #5��url_hash����������
                    #������url��hash�������������ʹÿ��url����ͬһ����˷�������
                    #��˷�����Ϊ����ʱ�Ƚ���Ч��
                    #������upstream�м���hash��䣬server����в���д��weight�������Ĳ���,
                    #    hash_method��ʹ�õ�hash�㷨
                    #upstream backend {
                    #    server squid1:3128;
                    #    server squid2:3128;
                    #    hash $request_uri;
                    #    hash_method crc32;
                    #}
                    #tips:
                    #upstream bakend{#���帺�ؾ����豸��Ip���豸״̬}{
                    #    ip_hash;
                    #    server 127.0.0.1:9090 down;
                    #    server 127.0.0.1:8080 weight=2;
                    #    server 127.0.0.1:6060;
                    #    server 127.0.0.1:7070 backup;
                    #}
                    #����Ҫʹ�ø��ؾ����server������ proxy_pass http://bakend/;
                    #ÿ���豸��״̬����Ϊ:
                    #1.down��ʾ��ǰ��server��ʱ�����븺��
                    #2.weightΪweightԽ�󣬸��ص�Ȩ�ؾ�Խ��
                    #3.max_fails����������ʧ�ܵĴ���Ĭ��Ϊ1.������������ʱ��
                    #             ����proxy_next_upstreamģ�鶨��Ĵ���
                    #4.fail_timeout:max_fails��ʧ�ܺ���ͣ��ʱ�䡣
                    #5.backup�� �������еķ�backup����down����æ��ʱ��
                    #           ����backup������������̨����ѹ�������ᡣ
                    #nginx֧��ͬʱ���ö���ĸ��ؾ��⣬���������õ�server��ʹ�á�
                    #client_body_in_file_only����ΪOn 
                    #���Խ�client post���������ݼ�¼���ļ���������debug
                    #client_body_temp_path���ü�¼�ļ���Ŀ¼ �����������3��Ŀ¼
                    #location��URL����ƥ��.���Խ����ض�����߽����µĴ��� ���ؾ���
                    server 192.168.80.121:80 weight=3;
                    server 192.168.80.122:80 weight=2;
                    server 192.168.80.123:80 weight=3;
                } 
                #��������������
                server
                {
                    #�����˿�
                    listen 80;
                    #���������ж�����ÿո����
                    server_name www.jd.com jd.com;
                    index index.html index.htm index.php;
                    root /data/www/jd;
                    #��******���и��ؾ���
                    location ~ .*.(php|php5)?$
                    {
                        fastcgi_pass 127.0.0.1:9000;
                        fastcgi_index index.php;
                        include fastcgi.conf;
                    }ldd n
                    #ͼƬ����ʱ������
                    location ~ .*.(gif|jpg|jpeg|png|bmp|swf)$
                    {
                        expires 10d;
                    }
                    #JS��CSS����ʱ������
                    location ~ .*.(js|css)?$
                    {
                        expires 1h;
                    }
                    #��־��ʽ�趨
                    #$remote_addr��$http_x_forwarded_for���Լ�¼�ͻ��˵�ip��ַ��
                    #$remote_user��������¼�ͻ����û����ƣ�
                    #$time_local�� ������¼����ʱ����ʱ����
                    #$request�� ������¼�����url��httpЭ�飻
                    #$status�� ������¼����״̬���ɹ���200��
                    #$body_bytes_sent ����¼���͸��ͻ����ļ��������ݴ�С��
                    #$http_referer��������¼���Ǹ�ҳ�����ӷ��ʹ����ģ�
                    #$http_user_agent����¼�ͻ�������������Ϣ��
                    #ͨ��web���������ڷ������ĺ��棬�����Ͳ��ܻ�ȡ���ͻ���IP��ַ�ˣ�
                    #ͨ��$remote_add�õ���IP��ַ�Ƿ�������������iP��ַ��
                    #��������������ת�������httpͷ��Ϣ�У���������x_forwarded_for��Ϣ��
                    #���Լ�¼ԭ�пͻ��˵�IP��ַ��ԭ���ͻ��˵�����ķ�������ַ��
                    log_format access '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" $http_x_forwarded_for';
                    #���屾���������ķ�����־
                    access_log  /usr/local/nginx/logs/host.access.log  main;
                    access_log  /usr/local/nginx/logs/host.access.404.log  log404;
                    #�� "/" ���÷������
                    location / {
                        proxy_pass http://127.0.0.1:88;
                        proxy_redirect off;
                        proxy_set_header X-Real-IP $remote_addr;
                        #��˵�Web����������ͨ��X-Forwarded-For��ȡ�û���ʵIP
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        #������һЩ�����������ã���ѡ��
                        proxy_set_header Host $host;
                        #����ͻ������������ļ��ֽ���
                        client_max_body_size 10m;
                        #�������������û������������ֽ�����
                        #�����������Ϊ�Ƚϴ����ֵ������256k����ô��
                        #����ʹ��firefox����IE����������ύ����С��256k��ͼƬ������������
                        #���ע�͸�ָ�ʹ��Ĭ�ϵ�client_body_buffer_size���ã�
                        #Ҳ���ǲ���ϵͳҳ���С��������8k����16k������ͳ����ˡ�
                        #����ʹ��firefox4.0����IE8.0���ύһ���Ƚϴ�200k���ҵ�ͼƬ��
                        #������500 Internal Server Error����
                        client_body_buffer_size 128k;
                        #��ʾʹnginx��ֹHTTPӦ�����Ϊ400���߸��ߵ�Ӧ��
                        proxy_intercept_errors on;
                        #��˷��������ӵĳ�ʱʱ��_�������ֵȺ���Ӧ��ʱʱ��
                        #nginx����˷��������ӳ�ʱʱ��(�������ӳ�ʱ)
                        proxy_connect_timeout 90;
                        #��˷��������ݻش�ʱ��(�����ͳ�ʱ)
                        #��˷��������ݻش�ʱ��_�����ڹ涨ʱ��֮�ں�˷��������봫�����е�����
                        proxy_send_timeout 90;
                        #���ӳɹ��󣬺�˷�������Ӧʱ��(������ճ�ʱ)
                        #���ӳɹ���_�Ⱥ��˷�������Ӧʱ��_��ʵ�Ѿ������˵��Ŷ�֮�еȺ���
                        #��Ҳ����˵�Ǻ�˷��������������ʱ�䣩
                        proxy_read_timeout 90;
                        #���ô����������nginx�������û�ͷ��Ϣ�Ļ�������С
                        #���ôӱ������������ȡ�ĵ�һ����Ӧ��Ļ�������С��
                        #ͨ��������ⲿ��Ӧ���а���һ��С��Ӧ��ͷ��
                        #Ĭ����������ֵ�Ĵ�СΪָ��proxy_buffers��ָ����һ���������Ĵ�С��
                        #�������Խ�������Ϊ��С
                        proxy_buffer_size 4k;
                        #proxy_buffers����������ҳƽ����32k���µ�����
                        #�������ڶ�ȡӦ�����Ա�������������Ļ�������Ŀ�ʹ�С��
                        #Ĭ�����ҲΪ��ҳ��С�����ݲ���ϵͳ�Ĳ�ͬ������4k����8k
                        proxy_buffers 4 32k;
                        #�߸����»����С��proxy_buffers*2��
                        proxy_busy_buffers_size 64k;
                        #������д��proxy_temp_pathʱ���ݵĴ�С��
                        #Ԥ��һ�����������ڴ����ļ�ʱ����̫��
                        #�趨�����ļ��д�С���������ֵ������upstream��������
                        proxy_temp_file_write_size 64k;
                    }
                    #�趨�鿴Nginx״̬�ĵ�ַ
                    location /NginxStatus {
                        stub_status on;
                        access_log on;
                        auth_basic "NginxStatus";
                        auth_basic_user_file confpasswd;
                        #htpasswd�ļ������ݿ�����apache�ṩ��htpasswd������������
                    }
                    #���ض������뷴���������
                    #����jsp��ҳ�������tomcat��resin����
                    location ~ .(jsp|jspx|do)?$ {
                        proxy_set_header Host $host;
                        proxy_set_header X-Real-IP $remote_addr;
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        proxy_pass http://127.0.0.1:8080;
                    }
                    #���о�̬�ļ���nginxֱ�Ӷ�ȡ������tomcat��resin
                    location ~ .*.(htm|html|gif|jpg|jpeg|png|bmp|swf|ioc|rar|
                                   zip|txt|flv|mid|doc|ppt|pdf|xls|mp3|wma)$
                    {
                        expires 15d; 
                    }
                    location ~ .*.(js|css)?$
                    {
                        expires 1h;
                    }
                }
            }
        http://www.ttlsa.com/nginx/nginx-tutorial-from-entry-to-the-master-ttlsa/ Nginx�����ŵ���ͨ
        https://www.jianshu.com/p/b164c001a555 Nginx��������
    ����Nginx
        https://blog.csdn.net/arv002/article/details/109431639 ���ܰ�Nginx�����ļ�Server���ֲο�
        https://blog.csdn.net/qq_15077747/article/details/108220046 ��������nginx֧�ֹ���
        https://blog.csdn.net/u011893782/article/details/106281764 ����SM2 Https���������������
            tassl�����������ɹ���֤�鼰key�ļ�
            ���������ΪNginx����̬ҳ�������ʱ������֧��HTTP/HTTPSҳ�����
            �������Nginx�ķ�������ܣ�����
                /root/lib_r/tassl//lib/engines-1.1/tasscard_sm4.so: 
                cannot open shared object file: No such file or directory
            ��Nginx_TasslԴ��������tasscard����http/modules/ngx_http_proxy_module.c
            ��http/modules/ngx_http_ssl_module.c�������ļ��з��ָùؼ���
            Ӧ����ô�ģ��д���һ���о�
    epoll����
        ��select�ĶԱȣ�
            Select �ص㣺select ѡ������ʱ���Ǳ������о����Ҳ����˵������¼���Ӧʱ��
            select ��Ҫ�������о�����ܻ�ȡ����Щ������¼�֪ͨ�����Ч���Ƿǳ��͡�
            epoll ���ص㣺epoll ���ھ���¼���ѡ���Ǳ����ģ����¼���Ӧ�ģ�
            ���Ǿ�����¼���������ѡ�����������Ҫ������������������Ч�ʷǳ���