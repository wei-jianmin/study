问题产生的根源剖析
    跨源资源共享（CORS，或称跨域资源共享）是一种基于 HTTP 头的机制
    同源策略(Same origin policy)是一种约定，
    它是浏览器最核心也最基本的安全功能，
    如果缺少了同源策略，则浏览器的正常功能可能都会受到影响。
    众所周知出于安全的考虑，浏览器有个同源策略：
    对于不同源的站点之间的相互请求会做限制（跨域限制是浏览器行为，不是服务器行为）
    跨源资源共享标准新增了一组 HTTP 标头字段，
    允许服务器声明哪些源站通过浏览器有权限访问哪些资源
    浏览器和服务器到底是如何判定有没有跨域呢？
    首先浏览器在发起请求时，根据请求的目标url，就可判断出是否同源，
    如果不同源，则检查服务端返回的http头中的字段，
    如果允许跨域，则使用，否则，不会加载返回的结果
    域："协议://域名:端口"，当着三者中任意一个变化，就是跨域了
    不同的域下面存了不同的数据，例如cookie等，
    在浏览器端发送的请求，会带上用户在对方网站的cookie，
    所以如果用户已登录，对方网站识别的身份是真正的处于登录状态用户。
    在服务器端发送的请求，取不到用户在对方网站的cookie，所以对方网站识别的身份是未登录
    浏览器发起同源请求时，肯定会带上本域的cookie（cookie是存在浏览器端的），
    访问其他网站的接口，发起跨域请求的时候，cookie默认不会带上去的

为什么浏览器要用同源策略控制   
    如果没有同源策略，不同源的数据和资源就能相互随意访问
    想想当我们访问了一个恶意网站，如果没有同源策略 
    那么这个网站就能通过 js 访问 document.cookie 
    得到用户关于的各个网站的sessionID 
    其中可能有银行网站、http://qq.com、github等
    通过已经建立好的session连接进行攻击的（CSRF 攻击）
    同源策略无法完全防御CSRF 这里需要服务端配合
    再如通过一个iframe 加载淘宝的登录页面
    等用户登录这个网站时，会认为这是淘宝的正确页面
    在这里面输入了用户名密码，如果没有同源策略
    这个恶意万战就能通过dom操作获取到用户输入的值
    但因为有了同源策略，就不能在iframe中成功加载淘宝页面了
    
Access-Control-Allow-Headers:
Access-Control-Allow-Methods:
Access-Control-Allow-Origin:
    
xhr(XMLHttpRequest) vs. fetch    
    
    
参考资料：
    https://developer.mozilla.org/zh-CN/docs/Web/Security/Same-origin_policy
    
浏览器的同源策略
    同源的定义
        如果两个 URL 的 protocol、port (en-US) (如果有指定的话)和 host 都相同的话，则这两个 URL 是同源
        这个方案也被称为“协议/主机/端口元组”
        * IE 中的特例
            授信范围（Trust Zones）
                两个相互之间高度互信的域名，如公司域名（corporate domains），则不受同源策略限制。
            端口
                IE 未将端口号纳入到同源策略的检查中
            这些差异点是不规范的，其它浏览器也未做出支持
    跨源网络访问
        同源策略控制不同源之间的交互，例如在使用XMLHttpRequest 或 <img> 标签时则会受到同源策略的约束
        这些交互通常分为三类：
            跨域写操作
                一般是被允许的。例如链接（links），重定向以及表单提交。
            跨域资源嵌入
                一般是被允许
            跨域读操作
                一般是不被允许的
                
实现跨域的9种方法(点击可跳转详情页面)
    1.jsonp 
        https://blog.csdn.net/qq_17175013/article/details/88984206
    2.cors 
        https://blog.csdn.net/qq_17175013/article/details/88984274
        Access-Control-Allow-Origi
        含义：允许哪个源可以访问
        实际操作：
            后端一般会设置一个白名单
            前端发请求到后端的时候，后端会判断是否在白名单里，
                如果在，则在响应头里设置该头：
                res.setHeader('Access-Control-Allow-Origin',前端的域);
            ......
    3.postMessage ：https://blog.csdn.net/qq_17175013/article/details/89165586
    4.document.domain ：https://blog.csdn.net/qq_17175013/article/details/89115629
    5.window.name ：https://blog.csdn.net/qq_17175013/article/details/89007334
    6.location.hash ：https://blog.csdn.net/qq_17175013/article/details/89115400
    7.websocket ：webSocket本身不存在跨域问题
    8.http-proxy
    9.nginx
解决跨域的方法    
    前端：
        1. <script>标签是不受跨域影响,只要herf,src属性的标签都不收跨域的影响
        2. 利用JSONP
           JSONP能实现的跨域的原理：
           底层利用script实现，发送请求的传递callback的参数；
           服务端可以到这个参数，给这个参数加上一个()然后直接返回给浏览器；
           浏览器接收到返回的内容后就会解析成一个js的函数调用，前提先要定义这个函数。
   后端：
            