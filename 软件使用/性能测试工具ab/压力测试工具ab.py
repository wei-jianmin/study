基本概念
    吞吐率：
        （对单个用户）1秒内能处理的请求个数
    并发数：
        某个时刻服务器所接受的请求数目
    并发用户数：
        一个用户可能同时产生多个会话
        如果用户产生多个会话，各个用户产生的会话个数是相等的
    用户平均请求等待时间：    
        处理完成所有请求数所花费的时间 /（总请求数 / 并发用户数）
    服务器平均请求等待时：
        处理完成所有请求数所花费的时间 / 总请求数
    举例：
        假设服务器能同时连2个用户，每个用户有2个连接，每个连接发了2个请求，
        则共发出8个请求，假设每个请求耗时1s，则这8个请求共耗时8s
        则：
        吞吐率 = 1
        并发率 = 2
        并发用户数 = 0.5
        用户平均请求等待时间 = 8s / ( 8 / 2 ) = 2s
        服务器平均请求等待时 = 8s / 8 = 1s
ab工具简介：
    ab全称为：apache bench
    ab是Apache超文本传输协议(HTTP)的性能测试工具
    其设计意图是描绘当前所安装的Apache的执行性能，
    主要是显示你安装的Apache每秒可以处理多少个请求
下载：
    进入apache官网 http://httpd.apache.org/ 下载apache即可
测试方法：
    ab -n 100 -c 10 http://test.com/
    其中 -n 表示请求数，-c 表示并发数
    具体参：https://httpd.apache.org/docs/2.4/programs/ab.html

ab命令语法
    ab [[选项] 选项参数] [http[s]://]hostname[:port]/path
    -n requests     ＃在测试会话中所执行的请求总个数，默认仅执行一个请求
    -c concurrency  ＃每次请求的并发数，相当于同时模拟多少个人访问url，默认是一次一个
    -t timelimit    ＃测试所进行的最大秒数。其内部隐含值是-n 50000
                    ＃它可以使对服务器的测试限制在一个固定的总时间以内
    -s timeout      ＃等待每个响应的最大值，默认为30秒
    -b windowsize   ＃TCP 发送/接收缓冲区的大小，以字节为单位
    -B address      ＃进行传出连接时要绑定到的地址
    -p postfile     ＃包含要 POST 的数据的文件，记得还要设置 -T 参数
    -u putfile      ＃包含要 PUT 的数据的文件，记得还要设置-T 参数
    -T content-type ＃POST/PUT 数据所使用的Content-type头信息
                    ＃例如：application/x-www-form-urlencoded 默认值：text/plain
    -v verbosity    ＃设置显示信息的详细程度 -4 或更大值会显示头信息
                    ＃3或更大值可以显示响应代码(404, 200等)，2或更大值可以显示警告和其它信息
    -w              ＃以HTML表的格式输出结果，默认时，它是白色背景的两列宽度的一张表
    -i              ＃执行HEAD请求，而不是GET
    -x attributes   ＃以HTML表格格式输出结果时，给 table 标签设置的属性值
                    ＃如 -x 'sytle="width=500px"' 输出的html中table标签会加上该属性<table sytle="width=500px">
    -y attributes   ＃以HTML表格格式输出结果时，给 tr 标签设置的属性值
    -z attributes   ＃以HTML表格格式输出结果时，给 td 标签设置的属性值
    -C attribute    ＃对请求附加一个Cookie:行，形式为 name=value 的一个参数对，此参数可以重复
    -H attribute    ＃对请求附加额外的头信息，此参数的典型形式是一个有效的头信息行
                    ＃其中包含了以冒号分隔的字段和值的对 (如："Accept-Encoding: zip/zop;8bit")
    -A attribute    ＃对服务器提供BASIC认证信任，用户名和密码由一个:隔开，并以base64编码形式发送
                    ＃无论服务器是否需要（即：是否发送了401认证需求代码）此字符串都会被发送
    -P attribute    ＃对一个中转代理提供BASIC认证信任，用户名和密码由一个:隔开，并以base64编码形式发送
                    ＃无论服务器是否需要（即：是否发送了401认证需求代码）此字符串都会被发送
    -X proxy:port   ＃对请求使用代理服务器
    -V              ＃显示版本号并退出
    -k              ＃启用 HTTP KeepAlive 功能，即在一个 HTTP 会话中执行多个请求，默认不启用 KeepAlive 功能
    -d              ＃不显示“XX [ms] 表内提供的百分比”（遗留支持）
    -S              ＃不显示中值和标准差值，当平均值和中值相差超过标准差的一倍或两倍时，
                    ＃也不显示警告或错误消息，默认会显示 min/avg/max 值（遗留支持）
    -q              ＃如果处理的请求数大于150，ab每处理大约10%或者100个请求时，会在stderr输出一个进度计数，此-q标记可以抑制这些信息
    -g filename     ＃把所有测试结果写入一个'gnuplot'或者TSV (以Tab分隔的)文件，
                    ＃此文件可以方便地导入到Gnuplot、IDL、Mathematica、Igor甚至Excel中，其中的第一行为标题
    -e filename     ＃产生一个以逗号分隔的(CSV)文件， 其中包含了处理每个相应百分比的请求所需要(从1%到100%)的相应百分比的(以微妙为单位)时间
                    ＃由于这种格式已经“二进制化”，所以比'gnuplot'格式更有用
    -r              ＃不要在套接字接收错误时退出
    -h              ＃显示帮助信息
    -Z ciphersuite  指定 SSL/TLS 密码套件（请参阅 openssl 密码）
    -f protocol     指定 SSL/TLS 协议（SSL2、SSL3、TLS1 或 ALL）
    