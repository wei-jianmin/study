在Web开发项目中，nginx常用作为静态文件服务器处理静态文件
并负责将动态请求转发至应用服务器

https://www.yiibai.com/nginx/nginx-architecture.html
Nginx架构
    nginx大量使用复用和事件通知
    连接在有限数量的单线程进程(称为工作者,worker)的循环中处理
    在每个工作者(worker)中，nginx可以处理每秒数千个并发连接和请求
    nginx不会为每个连接生成一个进程或线程。 
    相反，工作(worker)进程接受来自共享“listen”套接字的新请求，
    并在每个工作(worker)内执行高效的运行循环，
    以处理每个工作(worker)中的数千个连接。 
启动，停止和重新加载Nginx配置

    
