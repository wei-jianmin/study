学习缘由：
    让C++ 研发  研究下 gmssl  配合  修改 nginx 代码
    跑起来国密 ssl 协议
    还有 一个 stunnel 的工程 让他们研究下
资料查找：
    https://www.gmssl.cn/gmssl/index.jsp  国密ssl实验室  
        提供了x86_64环境，CentOS7系统下可用的gmssl_openssl库和gmssl_nginx工具（不是源码）
        讲解了nginx的部署与使用方法、示例
        关于我们
            在这里面提到：
            "国密SSL能够做到在同一个端口，自适应支持标准HTTPS/国密HTTPS",
            所以，Nginx与浏览器的通信能支持国密证书，是因为使用了gmssl(动态库)的关系
            国密SSL闭环：
            国密SSL实际使用中，需要国密证书、国密U盾、国密网关/服务器、
            国密浏览器等互相配合，才能形成完整的落地方案。
        国密U盾伴侣
            主要介绍了他们的一款工具，使用该工具，
            可以方便的在线申请国密证书，并将证书导入的key中（适配龙脉key）
        国密SDK
            国密JCE/JSSE
                GMSDK(Java版)提供一个纯java的JCE/JSSE国密实现，
                面向ISV提供国密SSL开发集成。
                支持单向国密SSL/双向国密SSL。
                支持国密U盾(SKF接口)。
                支持Netty(商业版)。
                支持Jetty(商业版)。
                支持Spring Boot(商业版)。
                支持OkHttp(商业版)。
            国密OpenSSL
                GMSDK(OpenSSL版)提供一个OpenSSL的国密实现，
                面向ISV提供国密SSL开发集成。
                支持单向国密SSL/双向国密SSL。
                支持国密U盾(SKF接口)。
    https://www.zhihu.com/question/26236094  有人把国密算法集成到 OpenSSL 里的么
        GmSSL (http://gmssl.org) 是支持国密算法和标准的OpenSSL分支，
        是一个提供了丰富密码学功能和安全功能的开源软件包。
    https://blog.csdn.net/wxh0000mm/category_8817109.html   openssl系列讲解
    其它开源gmssl
        https://github.com/guanzhi/gmssl-v3-dev  guanzhi
        https://github.com/GmSSL  GmSSl（支持国密算法的OpenSSL分支）
    江南天安开源 ssl+nginx
        https://github.com/jntass/TASSL-1.1.1b  tassl
            北京江南天安科技有限公司支持国密证书和协议的TASSL
            OpenSSL是一套件开放源代码的安全套接字密码学基础库，囊括主要的密码算法、常用的密钥和证书封装管理功能及SSL/TLS协议，
            并提供丰富的API，以供应用程序开发、测试或其它目的使用。它广泛地集成在各种类型的操作系统中，
            作为其基础组件之一，深爱广大IT爱好者的喜爱。即使用某些操作系统没有将其集成为组件，通过源代码下载，
            也是十分轻松地构建OpenSSL的开发及应用环境。
            尽管OpenSSL的功能十分强大且丰富，也包含了国密的相关算法，但是对于国密的SSL协议并不支持。
            这对于推广及研究中国商用密码体系的广大密码爱好者来说，却是十分无奈的事情。 
            国内也存在着不少密码界同仁，尝试着将OpenSSL国密化，但其大多都局限于公司内部交流使用，这对于国密SSL的推广不利。
            针对这种现状，北京江南天安公司经过长时间的研究分析，于2017年上半年推出天安版国密OpenSSL，也就是TaSSL，
            解决了中国商用密码体系无法构建基于OpenSSL应用的实际问题。现在我们又推出了给予openssl-1.1.1b版本的tassl-1.1.1b_R_0.8版本。
            现以源码的形式提供出来，供大家参考使用，为促进国密的推广和应用贡献自己的一份力量。
            (一)天安TaSSL-1.1.1b_v1.0版本的功能特点
            1.支持调用江南天安加密机或加密卡进行加速和物理安全防护。
            2.适配了nginx-1.16.0支持国密，nginx开源地址：https://github.com/jntass/Nginx_Tassl
            3.适配了360浏览器和密信浏览器的访问。
            4.修复了bug和一些其他问题。
            ssl相关的API
            CNTLS_client_method()：获取国密TLSv1.1标准协议的相关SSL/TLS相关方法，以使用客户端使用标准的TLSv1.1协议进行握手、通讯；
            SSL_CTX_check_enc_private_key()、SSL_check_enc_private_key()、SSL_use_enc_PrivateKey()、
            SSL_use_enc_PrivateKey_ASN1()、SSL_CTX_use_enc_PrivateKey()、SSL_CTX_use_enc_PrivateKey_ASN1()、
            SSL_use_enc_PrivateKey_file()、SSL_CTX_use_enc_PrivateKey_file() 为支持国密双证书体系而添加的函数。
            (三)TASSL使用说明
            目前开源的版本是基于OpenSSL 1.1.1b 26 Feb 2019版本；
            下载tassl-1.1.1b_v1.4版本。 下载地址：https://github.com/jntass/TASSL-1.1.1b/archive/V_1.4.tar.gz
            上传至编译环境，进行解压编译。
            tar xvf TASSL-1.1.1b-1.4.tar.gz
            cd TASSL-1.1.1b-1.4
            chmod u+x ./config
            ./config --prefix=/root/lib_r/tassl
            make
            make install
            进入安装目录，除了标准的openssl库和头文件外，还会有tassl_demo的例子目录
            cd /root/lib_r/tassl/tassl_demo，其中：
            a) cert目录:
            包含生成测试证书的脚本gen_sm2_cert.sh
            执行./ gen_sm2_cert.sh则生成测试证书目录certs
            b) crypto目录：
            包含测试国密算法的示例
            执行./mk.sh进行编译测试
            c) ssl目录：
            包含国密ssl通讯的客户端和服务端
            执行./mk.sh进行编译测试
        https://github.com/jntass/Nginx_Tassl  nginx_tassl
            如何使nginx调用tassl实现国密ssl协议？
            具体方法如下：
            下载Tassl-1.1.1b_R_0.8.tgz版本进行编译，并安装到/root/lib_r/tassl中，
            如是其他目录需要在第二步的configure时，替换--with-openssl的目录。
            下载江南天安修改的nginx-1.16.0_tassl.tgz支持国密的nginx进行编译。
            注意configure需要电脑中预装了pcre(不是pcre2)和zlib，否则会报错。
            ./configure --with-http_ssl_module --with-stream --with-stream_ssl_module 
                        --with-openssl=/root/lib_r/tassl --prefix=/root/nginx
            make
            make install
            配置nginx。
            配置nginx.conf证书部分：
            ssl_certificate /root/lib_r/tassl/tassl_demo/cert/certs/SS.crt; #/签名证书/
            ssl_certificate_key /root/lib_r/tassl/tassl_demo/cert/certs/SS.key; #/签名私钥/
            ssl_enc_certificate /root/lib_r/tassl/tassl_demo/cert/certs/SE.crt; #/加密证书/
            ssl_enc_certificate_key /root/lib_r/tassl/tassl_demo/cert/certs/SE.key; #/加密私钥/
            注意：签名证书的证书用途需有数据签名功能，加密证书的证书用途需有数据加密功能。
            如果功能不正确，会导致握手失败。调用tassl_demo/cert/中的脚本生成的证书已经具备相应功能,可以用来测试。
            下载密信浏览器或者360浏览器进行测试国密网站。
            a) 密信浏览器
            下载地址：https://www.mesince.com/zh-cn/browser
            如果第一次连接失败，那么密信浏览器会尝试国际算法，导致以后的连接都会使用国际算法，无法成功。
            此时需要在浏览器设置中，清楚浏览数据，进行清楚所有的数据，那么浏览器在下一次再进行连接时，会首先尝试国密算法。
            b) 360浏览器
            下载地址：https://browser.360.cn/se/ver/gmzb.html
            360国密浏览器版本目前较多。而且和新版本的Windows 10系统，会偶发性的导致系统重启。 
            而且360要求自己添加根证书，如果没有添加会导致SSL握手完成后显示证书不正确。 
            添加跟证书方法：将根证书放在ctl.dat文件中，
            然后把此文件放在%appdata%/360se6\Application\User Data\Default\ctl目录中，
            注意：上面从"User Data\Default\ctl"的目录并不存在，需要手工创建。 
            经过多次测试，目前可以添加根证书生效的版本360_mini_installer_sm_7.exe，
            已经附件到另一个仓库中https://github.com/jntass/GM_BROWERS 而且我们的测试环境是Windows 7系统。
        https://blog.csdn.net/u011893782/article/details/106281764?
          utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault
          %7EBlogCommendFromBaidu%7Edefault-6.no_search_link&depth_1-
          utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault
          %7EBlogCommendFromBaidu%7Edefault-6.no_search_link 测试功能
            1. 运行运行tassl生成证书demo，脚本路径/root/lib_r/tassl/tassl_demo/cert/gen_sm2_cert.sh
               证书生成在/root/lib_r/tassl/tassl_demo/cert/certs下
            2. 配置Nginx的安装路径/root/nginx，配置文件/root/nginx/conf/nginx.conf，指明服务器证书和私钥
                proxy_ssl_certificate          /root/tasscard_engine/cert/server/sm2/org_ss.crt;
                proxy_ssl_certificate_key      /root/tasscard_engine/cert/server/sm2/org_ss.key;
                proxy_ssl_enc_certificate      /root/tasscard_engine/cert/server/sm2/org_se.crt;
                proxy_ssl_enc_certificate_key  /root/tasscard_engine/cert/server/sm2/org_se.key;
    pcre库简介：
        PCRE(Perl Compatible Regular Expressions，Perl兼容的正则表达式)
        PCRE库由一系列函数组成，实现了与Perl5相同的语法、语义的正则表达式匹配功能。
        PCRE有其自己的native API，同时也包含了一系列的wrapper函数以兼容POSIX正则表达式API。
        是一个用C语言编写的正则表达式函数库。
        PCRE是一个轻量级的函数库，比Boost之类的正则表达式库小得多。
        PCRE十分易用，同时功能也很强大，性能超过了POSIX正则表达式库和一些经典的正则表达式库。
        PCRE是用C语言实现的，其C++实现版本是PCRE++。
        PCRE使用教程：
            https://www.cnblogs.com/LiuYanYGZ/p/5903946.html
            https://ivanzz1001.github.io/records/post/nginx/2018/11/20/nginx-source_part56_1
    nginx介绍
        百度百科：
            Nginx(engine x)是一个高性能的HTTP和反向代理web服务器，同时也提供了IMAP/POP3/SMTP服务
            Nginx是一款轻量级的Web 服务器/反向代理服务器及电子邮件（IMAP/POP3）代理服务器
            中国大陆使用nginx网站用户有：百度、京东、新浪、网易、腾讯、淘宝等
            在连接高并发的情况下，Nginx是Apache服务不错的替代品：
            Nginx在美国是做虚拟主机生意的老板们经常选择的软件平台之一。
            能够支持高达 50,000 个并发连接数的响应。
            Nginx作为负载均衡服务：
                Nginx 既可以在内部直接支持 Rails 和 PHP 程序对外进行服务，
                也可以支持作为 HTTP代理服务对外进行服务。支持 SSL 和 TLSSNI。
            代码特点：
                Nginx代码完全用C语言从头写成。
                Nginx有自己的函数库，并且除了zlib、PCRE和OpenSSL之外，标准模块只使用系统C库函数。
            代理服务器：
                Nginx 同时也是一个非常优秀的邮件代理服务
            Nginx 是一个安装非常的简单、配置文件非常简洁（还能够支持perl语法）、Bug非常少的服务。
            Nginx 启动特别容易，并且几乎可以做到7*24不间断运行，即使运行数个月也不需要重新启动。
            你还能够不间断服务的情况下进行软件版本的升级。
        https://www.cnblogs.com/muhy/p/10528543.html  Nginx工作原理
            Nginx本身就可以托管网站，进行HTTP服务处理，也可以作为反向代理服务器使用.
            正向代理 vs 反向代理
                客户端知道正向代理服务器，正向代理服务器位于客户侧，起到缓冲加速的等效果。
                对客户端而言，反向代理服务器就像是原始服务器，并且客户端不需要进行任何特别的设置
                客户端向反向代理的命名空间中的内容发送普通请求，
            接着反向代理将判断向哪个原始服务器转交请求，并将获得的内容返回给客户端。
            通信机制采用epoll模型，支持更大的并发连接。
            如果 Nginx Proxy 后端的某台 Web 服务器宕机了，不会影响前端访问。
            Nginx的事件处理机制：
                对于一个基本的web服务器来说，事件通常有三种类型，网络事件、信号、定时器。
                Nginx使用异步非阻塞的事件处理机制。
                具体到系统调用就是像select/poll/epoll/kqueue这样的系统调用。
                以epoll为例：当事件没有准备好时，就放入epoll(队列)里面。
                如果有事件准备好了，那么就去处理；
                如果事件返回的是EAGAIN，那么继续将其放入epoll里面。
                从而，只要有事件准备好了，我们就去处理她，
                只有当所有时间都没有准备好时，才在epoll里面等着。
                这样 ，我们就可以并发处理大量的并发了，当然，这里的并发请求，是指未处理完的请求，
                线程只有一个，所以同时能处理的请求当然只有一个了，只是在请求间进行不断地切换而已，
                切换也是因为异步事件未准备好，而主动让出的。
                这里的切换是没有任何代价，你可以理解为循环处理多个准备好的事件，事实上就是这样的。
                与多线程相比，这种事件处理方式是有很大的优势的，不需要创建线程，
                每个请求占用的内存也很少，没有上下文切换，事件处理非常的轻量级。
                并发数再多也不会导致无谓的资源浪费（上下文切换）。
            Nginx的内部（进程）模型
                nginx是以多进程的方式来工作的，当然nginx也是支持多线程的方式的,
                只是我们主流的方式还是多进程的方式，也是nginx的默认方式。
                nginx在启动后，会有一个master进程和多个worker进程。
                master进程主要用来管理worker进程：
                    接收来自外界的信号，向各worker进程发送信号，
                    监控 worker进程的运行状态,当worker进程退出后(异常情况下)，
                    会自动重新启动新的worker进程。
                而基本的网络事件，则是放在worker进程中来处理了。
                多个worker进程之间是对等的,他们同等竞争来自客户端的请求,各进程互相之间是独立的。
                一个请求,只可能在一个worker进程中处理,一个worker进程,不可能处理其它进程的请求。
                worker进程的个数是可以设置的，一般我们会设置与机器cpu核数一致。
                master进程在接到./nginx -s reload信号后，会先重新加载配置文件，
                然后再启动新的进程，并向所有老的进程发送信号，告诉他们可以光荣退休了。
                新的进程在启动后，就开始接收新的请求，而老的进程在收到来自 master的信号后，
                就不再接收新的请求，并且在当前进程中的所有未处理完的请求处理完成后，再退出。
                worker进程之间是平等的，每个进程，处理请求的机会也是一样的，
                每个worker进程都是从master 进程fork(分配)过来，
                在master进程里面，先建立多个socket（监听同一ip和port），
                然后再fork出相应个worker进程，每个worker进程都可以去accept各自的socket。
                当一个连接进来后，所有在accept在这个socket上面的进程，都会收到通知，
                而只有一个进程可以accept这个连接，其它的则accept失败，这是所谓的惊群现象。
                当然，nginx也不会视而不见，所以nginx提供了一个accept_mutex这个东西，
                从名字上，我们可以看这是一个加在accept上的一把共享锁。
                有了这把锁之后，同一时刻，就只会有一个进程在accpet连接，这样就不会有惊群问题了。
                accept_mutex是一个可控选项，我们可以显示地关掉，默认是打开的。
                nginx采用这种进程模型有什么好处呢？采用独立的进程，可以让互相之间不会影响，
                一个进程退出后，其它进程还在工作，服务不会中断，
                master进程则很快重新启动新的worker进程。
                当然，worker进程的异常退出，肯定是程序有bug了，异常退出，
                这会导致当前worker上的所有请求失败，不过不会影响到所有请求，所以降低了风险。
                每个work线程中因为使用了epool异步非阻塞的方式来处理请求，所以可以多并发请求。
                而像如IIS，每个请求都会独占一个工作线程，那同时有几千个请求，就得有几千个线程，
                这些线程不但占用内存大，而且前程间切换带来的cpu开销也很大，所以性能就上不去了。
            Nginx如何处理一个请求
                nginx在启动时，会解析配置文件，得到需要监听的端口与ip地址，
                然后在nginx的master进程里面，先初始化好这个监控的socket
                (创建socket，设置addrreuse等选项，绑定到指定的ip地址端口，再listen)，
                然后再fork出多个子进程出来，然后子进程会竞争accept新的连接。
                此后，客户端就可以向nginx发起连接了。
                当客户端与nginx进行三次握手，与nginx建立好一个连接后，
                此时，某一个子进程会accept成功，得到这个建立好的连接的 socket，
                然后创建nginx对连接的封装，即ngx_connection_t结构体。
                接着，设置读写事件处理函数并添加读写事件来与客户端进行数据的交换。
                最后，nginx或客户端来主动关掉连接，到此，一个连接就寿终正寝了。
                当然，nginx也是可以作为客户端来请求其它server的数据的（如upstream模块）
                此时，与其它server创建的连接，也封装在ngx_connection_t中。
                作为客户端，nginx先获取一个ngx_connection_t结构体，
                然后创建socket，并设置socket的属性（ 比如非阻塞）。
                然后再通过添加读写事件，调用connect/read/write来调用连接，
                最后关掉连接，并释放ngx_connection_t。
                nginx在实现时，是通过一个连接池来管理的，
                每个worker进程都有一个独立的连接池，连接池的大小是worker_connections。
                这里的连接池里面保存的其实不是真实的连接，
                它只是一个worker_connections大小的一个ngx_connection_t结构的数组。
                nginx会通过一个链表free_connections来保存所有的空闲ngx_connection_t。
                每次获取一个连接时，就从空闲连接链表中获取一个，用完后，再放回空闲连接链表里面。
                所以worker_connections代表了一个Nginx进程所能建立的最大连接数。
                需要注意的是，当Nginx作为反向代理使用时，会一次性消耗两个链接，
                一个是来自客户端的链接，一个是Nginx到真正服务器的链接。
        https://www.php.cn/nginx/422205.html  Nginx和Tomcat的对比
            Tomcat 服务器是一个免费的开放源代码的Web 应用服务器，属于轻量级应用服务器，
            在中小型系统和并发访问用户不是很多的场合下被普遍使用，是开发和调试JSP 程序的首选。
            tomcat一般是做动态解析才会用得到，支持jsp的解析，需要配置JDK支持。
            nginx，则一般是做静态，本身不具备动态解析功能，
            需要配置其他插件或通过其他软件协同才具备动态功能，比如php，tomcat，
            或者proxypass到win2008的iis服务器做ASP的动态链接等，
            但nginx在静态上的功能非常强大，也可做访问控制，
            而且可以做成各种协议负载服务器
            在性能方面如果再不做系统调优的情况下，tomcat一般支持并发并不高100个差不多了；
            nginx在静态方面支持并发轻松达几万。
        https://www.cnblogs.com/crazylqy/p/6891929.html Nginx入门 : 组织结构与使用
            Nginx 由内核和模块组成
                内核
                    内核的设计非常微小和简洁，完成的工作也非常简单，
                    仅仅通过查找配置文件将客户端请求映射到一个 location block
                    （location 是 Nginx配置中的一个指令，用于 URL 匹配），
                    而在这个location中所配置的每个指令将会启动不同的模块去完成相应的工作。
                模块    
                    核心模块：
                        HTTP 模块、 EVENT 模块和 MAIL 模块
                    基础模块： 
                        HTTP Access 模块、HTTP FastCGI 模块、
                        HTTP Proxy 模块和 HTTP Rewrite模块
                    第三方模块：
                        HTTP Upstream Request Hash 模块、 
                        Notice 模块和 HTTP Access Key模块。
            Nginx使用
                可以用whereis nginx找到Nginx目录，该目录下
                conf 存放配置文件，html 存放网页文件
                logs 存放日志，    sbin   shell启动、停止等脚本
                在sbin目录下，./nginx启动nginx
                重新读取配置文件： nginx -s reload
                Nginx信号控制：
                    TERM, INT  快速停止（杀死进程）
                    QUIT       优雅的关闭进程，即等请求结束后再关闭
                    HUP        改变配置文件，平滑的重读配置文件
                    USR1       重读日志，在日志按月/日分割时有用
                    USR2       平滑的升级
                    WINCH       优雅关闭旧的进程（配合USR2进行升级）
                检查 nginx.conf配置文件   ./nginx -t
                重启  ./nginx -s reload
                停止  ./nginx -s stop
            学习Nginx推荐书籍：
                1. 《深入剖析Nginx》
                2. 《实战Nginx：取代Apache的高性能Web服务器》
                3. 《深入理解Nginx：模块开发与架构解析》
                4. 《深入理解Nginx：模块开发与架构解析》
                5. 《决战Nginx技术卷：高性能Web服务器部署与运维》
                6. 《决战Nginx系统卷：高性能Web服务器详解与运维》
        https://www.cnblogs.com/crazylqy/p/6891954.html Nginx虚拟主机配置&配置文件模型
            什么是虚拟主机
                虚拟主机使用的是特殊的软硬件技术，
                它把一台运行在因特网上的服务器主机分成一台台“虚拟”的主机，
                每台虚拟主机都可以是一个独立的网站，可以具有独立的域名，
                具有完整的Intemet服务器功能（WWW、FTP、Email等），
                同一台主机上的虚拟主机之间是完全独立的。
                从网站访问者来看，每一台虚拟主机和一台独立的主机完全一样。
                利用虚拟主机，不用为每个要运行的网站提供一台单独的Nginx服务器
                或单独运行一组Nginx进程。
                虚拟主机提供了在同一台服务器、同一组Nginx进程上运行多个网站的功能。
            Nginx基本配置
                Nginx的主配置文件是：nginx.conf，nginx.conf主要组成如下：
                # 全局区 有几个工作子进程，一般设置为CPU数 * 核数
                worker_processes  1;
                events {
                        # 一般是配置nginx进程与连接的特性
                        # 如1个word能同时允许多少连接，一个子进程最大允许连接1024个连接
                        worker_connections  1024;
                }
                # 配置HTTP服务器配置段
                http {
                    # 配置虚拟主机段
                    server {
                        # 定位，把特殊的路径或文件再次定位。
                        location  {
                        }
                    }
                    server {
                               ...
                    }
                }
            基于域名的虚拟主机
                server {  
                    #监听端口 80  
                    listen 80;   
                    #监听域名abc.com;  
                    server_name abc.com;
                    location / {              
                        # 设置基础路径，相对nginx根目录，也可写成绝对路径  
                        root    abc;  
                        # 默认跳转到index.html页面  
                        index index.html;                 
                    }  
                }
                使用nginx -s reload 重载配置文件
                在windows电脑中修改host  192.168.197.142 abc.com
                然后再windows浏览器中访问http://abc.com:80/，就能访问abc中的index.html
            基于端口的虚拟主机配置
                server {
                    listen  2022;
                    server_name     abc.com;
                    location / {
                       root    /home;
                       index index.html;
                    }
                }
            基于IP地址虚拟主机配置
                server {
                    listen  80;
                    server_name  192.168.197.142;
                    location / {
                        root    ip;
                        index index.html;
                    }
                }
        https://www.cnblogs.com/crazylqy/p/6891991.html Nginx日志管理
        https://www.cnblogs.com/crazylqy/p/6892010.html Location配置与ReWrite语法
        https://www.idcspy.com/15617.html Nginx配置文件结构，总结的很一般
            主要分成四部分
                main（全局设置）：
                    main部分设置的指令将影响到其它所有部分设置；
                server（主机设置）：
                    server部分的指令主要用于指定虚拟主机域名、IP和端口；
                upstream（上游服务器设置，主要为反向代理、负载均衡相关配置）：
                    upstream的指令用于设置一系列的后端服务器，设置反向代理及后端服务器的负载均衡；
                location（URL匹配特定位置后的设置）：
                    location部分用于匹配网页位置（比如，根目录“/”，“/images”，等等）；
            文件结构
                1、全局块：
                    配置影响nginx全局的指令。
                    一般有运行nginx服务器的用户组，nginx进程pid存放路径，日志存放路径，
                    配置文件引入，允许生成worker process数等。
                2、events块：
                    配置影响nginx服务器或影响与用户的网络连接。
                    有每个进程的最大连接数，选取哪种事件驱动模型处理连接请求，
                    是否允许同时接受多个网路连接，开启多个网络连接序列化等。
                3、http块：
                    可以嵌套多个server，
                    配置代理，缓存，日志定义等绝大多数功能和第三方模块的配置。
                    如文件引入，mime-type定义，日志自定义，是否使用sendfile传输文件，
                    连接超时时间，单连接请求数等。
                4、server块：
                    配置虚拟主机的相关参数，一个http中可以有多个server。
                5、location块：
                    配置请求的路由，以及各种页面的处理情况。
        https://www.cnblogs.com/hunttown/p/5759959.html 带有详细注释的Nginx配置文件示例
            ######Nginx配置文件nginx.conf中文详解#####
            #定义Nginx运行的用户和用户组
            user www www;
            #nginx进程数，建议设置为等于CPU总核心数。
            worker_processes 8;
            #全局错误日志定义类型，[ debug | info | notice | warn | error | crit ]
            error_log /usr/local/nginx/logs/error.log info;
            #进程pid文件
            pid /usr/local/nginx/logs/nginx.pid;
            #指定进程可以打开的最大描述符：数目
            #工作模式与连接数上限
            #这个指令是指当一个nginx进程打开的最多文件描述符数目，
            #理论值应该是最多打开文件数（ulimit -n）与nginx进程数相除，
            #但是nginx分配请求并不是那么均匀，所以最好与ulimit -n 的值保持一致。
            #现在在linux 2.6内核下开启文件打开数为65535，worker_rlimit_nofile就相应应该填写65535。
            #这是因为nginx调度时分配请求到进程并不是那么的均衡，所以假如填写10240，
            #总并发量达到3-4万时就有进程可能超过10240了，这时会返回502错误。
            worker_rlimit_nofile 65535;
            events
            {
                #参考事件模型，use [ kqueue | rtsig | epoll | /dev/poll | select | poll ]; 
                #epoll模型是Linux 2.6以上版本内核中的高性能网络I/O模型，
                #linux建议epoll，如果跑在FreeBSD上面，就用kqueue模型。
                #补充说明：
                #与apache相类，nginx针对不同的操作系统，有不同的事件模型
                #A）标准事件模型
                #Select、poll属于标准事件模型，
                #如果当前系统不存在更有效的方法，nginx会选择select或poll
                #B）高效事件模型
                #Kqueue：使用于FreeBSD 4.1+, OpenBSD 2.9+, NetBSD 2.0 和 MacOS X.
                #使用双处理器的MacOS X系统使用kqueue可能会造成内核崩溃。
                #Epoll：使用于Linux内核2.6版本及以后的系统。
                #/dev/poll：使用于Solaris 7 11/99+，HP/UX 11.22+ (eventport)，
                #IRIX 6.5.15+ 和 Tru64 UNIX 5.1A+。
                #Eventport：使用于Solaris 10。 为了防止出现内核崩溃的问题， 有必要安装安全补丁。
                use epoll;
                #单个进程最大连接数（最大连接数=连接数*进程数）
                #根据硬件调整，和前面工作进程配合起来用，尽量大，但是别把cpu跑到100%就行。
                #每个进程允许的最多连接数，理论上每台nginx服务器的最大连接数为。
                worker_connections 65535;
                #keepalive超时时间。
                keepalive_timeout 60;
                #客户端请求头部的缓冲区大小。这个可以根据你的系统分页大小来设置，
                #一般一个请求头的大小不会超过1k，
                #不过由于一般系统分页都要大于1k，所以这里设置为分页大小。
                #分页大小可以用命令getconf PAGESIZE 取得。
                #[root@web001 ~]# getconf PAGESIZE
                #4096
                #但也有client_header_buffer_size超过4k的情况，
                #但是client_header_buffer_size该值必须设置为“系统分页大小”的整倍数。
                client_header_buffer_size 4k;
                #这个将为打开文件指定缓存，默认是没有启用的，
                #max指定缓存数量，建议和打开文件数一致，
                #inactive是指经过多长时间文件没被请求后删除缓存。
                open_file_cache max=65535 inactive=60s;
                #这个是指多长时间检查一次缓存的有效信息。
                #语法:open_file_cache_valid time 默认值:open_file_cache_valid 60 
                #使用（/影响）字段:http, server, location 
                #这个指令指定了何时需要检查open_file_cache中缓存项目的有效信息.
                open_file_cache_valid 80s;
                #open_file_cache指令中的inactive参数时间内文件的最少使用次数，
                #如果超过这个数字，文件描述符一直是在缓存中打开的，
                #如上例，如果有一个文件在inactive时间内一次没被使用，它将被移除。
                #语法:open_file_cache_min_uses number 默认值:open_file_cache_min_uses 1 
                #使用字段:http, server, location  
                #这个指令指定了在open_file_cache指令无效的参数中一定的时间范围内可以使用的最小文件数,
                #如果使用更大的值,文件描述符在cache中总是打开状态.
                open_file_cache_min_uses 1;
                #语法:open_file_cache_errors on | off 默认值:open_file_cache_errors off 
                #使用字段:http, server, location 这个指令指定是否在搜索一个文件是记录cache错误.
                open_file_cache_errors on;
            }
            #设定http服务器，利用它的反向代理功能提供负载均衡支持
            http
            {
                #文件扩展名与文件类型映射表
                include mime.types;
                #默认文件类型
                default_type application/octet-stream;
                #默认编码
                #charset utf-8;
                #服务器名字的hash表大小
                #保存服务器名字的hash表是由指令server_names_hash_max_size 
                #和server_names_hash_bucket_size所控制的。
                #参数hash bucket size总是等于hash表的大小，并且是一路处理器缓存大小的倍数。
                #在减少了在内存中的存取次数后，使在处理器中加速查找hash表键值成为可能。
                #如果hash bucket size等于一路处理器缓存的大小，
                #那么在查找键的时候，最坏的情况下在内存中查找的次数为2。
                #第一次是确定存储单元的地址，第二次是在存储单元中查找键 值。
                #因此，如果Nginx给出需要增大hash max size 或 hash bucket size的提示，
                #那么首要的是增大前一个参数的大小.
                server_names_hash_bucket_size 128;
                #客户端请求头部的缓冲区大小。这个可以根据你的系统分页大小来设置，
                #一般一个请求的头部大小不会超过1k，不过由于一般系统分页都要大于1k，
                #所以这里设置为分页大小。分页大小可以用命令getconf PAGESIZE取得。
                client_header_buffer_size 32k;
                #客户请求头缓冲大小。nginx默认会用client_header_buffer_size这个buffer来读取header值，
                #如果header过大，它会使用large_client_header_buffers来读取。
                large_client_header_buffers 4 64k;
                #设定通过nginx上传文件的大小
                client_max_body_size 8m;
                #开启高效文件传输模式，sendfile指令指定nginx是否调用sendfile函数(zero copy方式)来输出文件，
                #对于普通应用设为 on，如果用来进行下载等应用磁盘IO重负载应用，可设置为off，
                #以平衡磁盘与网络I/O处理速度，降低系统的负载。注意：如果图片显示不正常把这个改成off。
                sendfile on;
                #开启目录列表访问，合适下载服务器，默认关闭。
                autoindex on;
                #此选项允许或禁止使用socke的TCP_CORK的选项，此选项仅在使用sendfile的时候使用
                tcp_nopush on;
                tcp_nodelay on;
                #长连接超时时间，单位是秒
                keepalive_timeout 120;
                #FastCGI相关参数是为了改善网站的性能：减少资源占用，提高访问速度。
                #下面参数看字面意思都能理解。
                fastcgi_connect_timeout 300;
                fastcgi_send_timeout 300;
                fastcgi_read_timeout 300;
                fastcgi_buffer_size 64k;
                fastcgi_buffers 4 64k;
                fastcgi_busy_buffers_size 128k;
                fastcgi_temp_file_write_size 128k;
                #gzip模块设置
                gzip on;               #开启gzip压缩输出
                gzip_min_length 1k;    #最小压缩文件大小
                gzip_buffers 4 16k;    #压缩缓冲区
                gzip_http_version 1.0; #压缩版本（默认1.1，前端如果是squid2.5请使用1.0）
                gzip_comp_level 2;     #压缩等级
                #压缩类型，默认就已经包含textml，所以下面就不用再写了，
                #写上去也不会有问题，但是会有一个warn。
                gzip_types text/plain application/x-javascript text/css application/xml;    
                gzip_vary on;
                #开启限制IP连接数的时候需要使用
                #limit_zone crawler $binary_remote_addr 10m;
                #负载均衡配置
                upstream piao.jd.com 
                {
                    #upstream的负载均衡，weight是权重，可以根据机器配置定义权重。
                    #weigth参数表示权值，权值越高被分配到的几率越大。
                    #nginx的upstream目前支持5种方式的分配
                    #1、轮询（默认）
                    #每个请求按时间顺序逐一分配到不同的后端服务器，如果后端服务器down掉，能自动剔除。
                    #2、weight
                    #指定轮询几率，weight和访问比率成正比，用于后端服务器性能不均的情况。
                    #例如：
                    #upstream bakend {
                    #    server 192.168.0.14 weight=10;
                    #    server 192.168.0.15 weight=10;
                    #}
                    #3、ip_hash
                    #每个请求按访问ip的hash结果分配，这样每个访客固定访问一个后端服务器，
                    #可以解决session的问题。
                    #例如：
                    #upstream bakend {
                    #    ip_hash;
                    #    server 192.168.0.14:88;
                    #    server 192.168.0.15:80;
                    #}
                    #4、fair（第三方）
                    #按后端服务器的响应时间来分配请求，响应时间短的优先分配。
                    #upstream backend {
                    #    server server1;
                    #    server server2;
                    #    fair;
                    #}
                    #5、url_hash（第三方）
                    #按访问url的hash结果来分配请求，使每个url定向到同一个后端服务器，
                    #后端服务器为缓存时比较有效。
                    #例：在upstream中加入hash语句，server语句中不能写入weight等其他的参数,
                    #    hash_method是使用的hash算法
                    #upstream backend {
                    #    server squid1:3128;
                    #    server squid2:3128;
                    #    hash $request_uri;
                    #    hash_method crc32;
                    #}
                    #tips:
                    #upstream bakend{#定义负载均衡设备的Ip及设备状态}{
                    #    ip_hash;
                    #    server 127.0.0.1:9090 down;
                    #    server 127.0.0.1:8080 weight=2;
                    #    server 127.0.0.1:6060;
                    #    server 127.0.0.1:7070 backup;
                    #}
                    #在需要使用负载均衡的server中增加 proxy_pass http://bakend/;
                    #每个设备的状态设置为:
                    #1.down表示单前的server暂时不参与负载
                    #2.weight为weight越大，负载的权重就越大。
                    #3.max_fails：允许请求失败的次数默认为1.当超过最大次数时，
                    #             返回proxy_next_upstream模块定义的错误
                    #4.fail_timeout:max_fails次失败后，暂停的时间。
                    #5.backup： 其它所有的非backup机器down或者忙的时候，
                    #           请求backup机器。所以这台机器压力会最轻。
                    #nginx支持同时设置多组的负载均衡，用来给不用的server来使用。
                    #client_body_in_file_only设置为On 
                    #可以讲client post过来的数据记录到文件中用来做debug
                    #client_body_temp_path设置记录文件的目录 可以设置最多3层目录
                    #location对URL进行匹配.可以进行重定向或者进行新的代理 负载均衡
                    server 192.168.80.121:80 weight=3;
                    server 192.168.80.122:80 weight=2;
                    server 192.168.80.123:80 weight=3;
                } 
                #虚拟主机的配置
                server
                {
                    #监听端口
                    listen 80;
                    #域名可以有多个，用空格隔开
                    server_name www.jd.com jd.com;
                    index index.html index.htm index.php;
                    root /data/www/jd;
                    #对******进行负载均衡
                    location ~ .*.(php|php5)?$
                    {
                        fastcgi_pass 127.0.0.1:9000;
                        fastcgi_index index.php;
                        include fastcgi.conf;
                    }ldd n
                    #图片缓存时间设置
                    location ~ .*.(gif|jpg|jpeg|png|bmp|swf)$
                    {
                        expires 10d;
                    }
                    #JS和CSS缓存时间设置
                    location ~ .*.(js|css)?$
                    {
                        expires 1h;
                    }
                    #日志格式设定
                    #$remote_addr与$http_x_forwarded_for用以记录客户端的ip地址；
                    #$remote_user：用来记录客户端用户名称；
                    #$time_local： 用来记录访问时间与时区；
                    #$request： 用来记录请求的url与http协议；
                    #$status： 用来记录请求状态；成功是200，
                    #$body_bytes_sent ：记录发送给客户端文件主体内容大小；
                    #$http_referer：用来记录从那个页面链接访问过来的；
                    #$http_user_agent：记录客户浏览器的相关信息；
                    #通常web服务器放在反向代理的后面，这样就不能获取到客户的IP地址了，
                    #通过$remote_add拿到的IP地址是反向代理服务器的iP地址。
                    #反向代理服务器在转发请求的http头信息中，可以增加x_forwarded_for信息，
                    #用以记录原有客户端的IP地址和原来客户端的请求的服务器地址。
                    log_format access '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" $http_x_forwarded_for';
                    #定义本虚拟主机的访问日志
                    access_log  /usr/local/nginx/logs/host.access.log  main;
                    access_log  /usr/local/nginx/logs/host.access.404.log  log404;
                    #对 "/" 启用反向代理
                    location / {
                        proxy_pass http://127.0.0.1:88;
                        proxy_redirect off;
                        proxy_set_header X-Real-IP $remote_addr;
                        #后端的Web服务器可以通过X-Forwarded-For获取用户真实IP
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        #以下是一些反向代理的配置，可选。
                        proxy_set_header Host $host;
                        #允许客户端请求的最大单文件字节数
                        client_max_body_size 10m;
                        #缓冲区代理缓冲用户端请求的最大字节数，
                        #如果把它设置为比较大的数值，例如256k，那么，
                        #无论使用firefox还是IE浏览器，来提交任意小于256k的图片，都很正常。
                        #如果注释该指令，使用默认的client_body_buffer_size设置，
                        #也就是操作系统页面大小的两倍，8k或者16k，问题就出现了。
                        #无论使用firefox4.0还是IE8.0，提交一个比较大，200k左右的图片，
                        #都返回500 Internal Server Error错误
                        client_body_buffer_size 128k;
                        #表示使nginx阻止HTTP应答代码为400或者更高的应答。
                        proxy_intercept_errors on;
                        #后端服务器连接的超时时间_发起握手等候响应超时时间
                        #nginx跟后端服务器连接超时时间(代理连接超时)
                        proxy_connect_timeout 90;
                        #后端服务器数据回传时间(代理发送超时)
                        #后端服务器数据回传时间_就是在规定时间之内后端服务器必须传完所有的数据
                        proxy_send_timeout 90;
                        #连接成功后，后端服务器响应时间(代理接收超时)
                        #连接成功后_等候后端服务器响应时间_其实已经进入后端的排队之中等候处理
                        #（也可以说是后端服务器处理请求的时间）
                        proxy_read_timeout 90;
                        #设置代理服务器（nginx）保存用户头信息的缓冲区大小
                        #设置从被代理服务器读取的第一部分应答的缓冲区大小，
                        #通常情况下这部分应答中包含一个小的应答头，
                        #默认情况下这个值的大小为指令proxy_buffers中指定的一个缓冲区的大小，
                        #不过可以将其设置为更小
                        proxy_buffer_size 4k;
                        #proxy_buffers缓冲区，网页平均在32k以下的设置
                        #设置用于读取应答（来自被代理服务器）的缓冲区数目和大小，
                        #默认情况也为分页大小，根据操作系统的不同可能是4k或者8k
                        proxy_buffers 4 32k;
                        #高负荷下缓冲大小（proxy_buffers*2）
                        proxy_busy_buffers_size 64k;
                        #设置在写入proxy_temp_path时数据的大小，
                        #预防一个工作进程在传递文件时阻塞太长
                        #设定缓存文件夹大小，大于这个值，将从upstream服务器传
                        proxy_temp_file_write_size 64k;
                    }
                    #设定查看Nginx状态的地址
                    location /NginxStatus {
                        stub_status on;
                        access_log on;
                        auth_basic "NginxStatus";
                        auth_basic_user_file confpasswd;
                        #htpasswd文件的内容可以用apache提供的htpasswd工具来产生。
                    }
                    #本地动静分离反向代理配置
                    #所有jsp的页面均交由tomcat或resin处理
                    location ~ .(jsp|jspx|do)?$ {
                        proxy_set_header Host $host;
                        proxy_set_header X-Real-IP $remote_addr;
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        proxy_pass http://127.0.0.1:8080;
                    }
                    #所有静态文件由nginx直接读取不经过tomcat或resin
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
        http://www.ttlsa.com/nginx/nginx-tutorial-from-entry-to-the-master-ttlsa/ Nginx从入门到精通
        https://www.jianshu.com/p/b164c001a555 Nginx虚拟主机
    国密Nginx
        https://blog.csdn.net/arv002/article/details/109431639 国密版Nginx配置文件Server部分参考
        https://blog.csdn.net/qq_15077747/article/details/108220046 编译配置nginx支持国密
        https://blog.csdn.net/u011893782/article/details/106281764 国密SM2 Https服务器搭建完整方案
            tassl可以正常生成国密证书及key文件
            如果仅配置为Nginx做静态页面服务器时，可以支持HTTP/HTTPS页面访问
            如果开启Nginx的反向代理功能，报错：
                /root/lib_r/tassl//lib/engines-1.1/tasscard_sm4.so: 
                cannot open shared object file: No such file or directory
            在Nginx_Tassl源码中搜索tasscard，在http/modules/ngx_http_proxy_module.c
            和http/modules/ngx_http_ssl_module.c这两个文件中发现该关键词
            应该怎么改，有待近一步研究
    epoll介绍
        与select的对比：
            Select 特点：select 选择句柄的时候，是遍历所有句柄，也就是说句柄有事件响应时，
            select 需要遍历所有句柄才能获取到哪些句柄有事件通知，因此效率是非常低。
            epoll 的特点：epoll 对于句柄事件的选择不是遍历的，是事件响应的，
            就是句柄上事件来就马上选择出来，不需要遍历整个句柄链表，因此效率非常高