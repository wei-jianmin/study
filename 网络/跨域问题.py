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
    jsonp ：https://blog.csdn.net/qq_17175013/article/details/88984206
    cors ：https://blog.csdn.net/qq_17175013/article/details/88984274
        Access-Control-Allow-Origi
        含义：允许哪个源可以访问
        实际操作：
            后端一般会设置一个白名单
            前端发请求到后端的时候，后端会判断是否在白名单里，
                如果在，则在响应头里设置该头：
                res.setHeader('Access-Control-Allow-Origin',前端的域);
            ......
    postMessage ：https://blog.csdn.net/qq_17175013/article/details/89165586
    document.domain ：https://blog.csdn.net/qq_17175013/article/details/89115629
    window.name ：https://blog.csdn.net/qq_17175013/article/details/89007334
    location.hash ：https://blog.csdn.net/qq_17175013/article/details/89115400
    websocket ：webSocket本身不存在跨域问题
    http-proxy
    nginx
            