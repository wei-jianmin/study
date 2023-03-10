https
    https 其实就是 http + tls/ssl,
        SSL ：Secure Sockets Layer 安全套接字协
        TLS : Transport Layer Security 传输层安全
        tls 是基于ssl的扩展，可以认为是后续的ssl版本，一般将两者视为同义词
    https建立连接的过程
        客户端向服务器发送支持的加密协议(tls)及版本
        服务端返回支持的加密协议
        服务端返回证书
        客户端验证证书有效性
        客户端生成对称密钥，用服务器证书的公钥加密后，返回给服务器
        服务器私钥解密，拿到对称密钥
        服务器用对称密钥加密finish信号发给客户端
        之后客户端的请求和服务器的回复都使用对称密钥加密
    ssl层工作在http层和tcp层之间，（ssl验证是通过tcp协议进行的）
    当建立https连接时，先建立ssl连接（完成身份认证，密码协商等），
    之后就是正常的http通讯流程了，只不过ssl层将http层的数据加工后发给tcp层。
    也就是说，https是将http加密后在网络上传输，
    因为http数据比较大，非对称加密速度又比较慢，所以选择用对称加密，
    所以浏览器跟服务器就得实现商定个对称密钥，
    怎么互通这个对称密钥，而不怕被第三方窃听，是问题的关键。

    解决思路：
    使用非对称加密方法，将对称密钥加密有在网络上传输，具体做法：
      以https://www.baidu.com为例：
      百度发来网站自己的证书，里面含公钥，
      客户端拿到该公钥，就可以加密传输“对称密钥了”：
        浏览器使用该公钥加密“对称密钥”，
        加密后的对称密钥发给网站，网站解密得到“对称密钥”
      
    为什么这种方式能防窃听：
      对称密钥是以密文的形式在网络上流通的
      只有发来网站证书的网站，才能解密得到对称密钥
      所以第三方网站即便拿到了密文的“对称密钥”，
      因其没有对应的私钥，所以也不会造成威胁
      
    一个前提：
      以上的讨论，隐含了一个假设：浏览器拿到的是真正的百度发来的证书
      中间人攻击：
        如果有个假的百度（百复: https://www.baifu.com）,
        他想知道用户在搜索什么，
        他劫持浏览器发起的，对百度的连接请求，
        然后假冒浏览器，把该请求原样发给百度，
        百度不会关心发起连接的客户端的真伪，只要有连接请求，就接受
        百度将自己的证书发给百复
        如果百复将百度的证书再发给浏览器  --- x
          浏览器用该证书加密"对称密钥"，意图发给百度，但实际落到百复手里，
          百复面对该加密的“对称密钥”束手无策：
            再发给百度，那百度解密得到对称密钥，那百度就和浏览器商量好了使用那个对称密钥加密数据，百复还是啥也不知道，白忙活了
            不发给百度，那百度得不到答复，就会断开连接
              告诉浏览器连接建立好了，可以发数据，客户端发来的使用对称密钥加密的数据，百复不知道是什么
              不回复浏览器，浏览器请求百度失败，百复也达不到窃取数据的目的
        所以百复不能选择将百度的证书发给浏览器，而是发自己的证书给浏览器 --- x
          浏览器侧会检查证书的有效性：
            证书信息中记录了颁发者证书
              颁发者证书一般是CA机构下发的
              颁发者证书又称根证书，即对网站证书验证签名时，应使用哪个证书中的公钥进行验证
            浏览器中，或者系统中，能找到该颁发者证书，
            就使用该颁发者证书中的公钥，解密网站证书的签名值，得到一个哈希值，
            再对网站证书中的原文信息哈希，得到另一个哈希值，
            这两个哈希值对比，如果一致，说明网站证书是真实可靠的
          看证书的信息是否正确：
            证书信息中记录了网站的域名，如baidu.com
          看证书的密钥用途是否正确
      通过对中间人攻击的分析，可见https是可以防止这种形式的攻击的。
      
    其它说明：
        https默认端口是443，http默认端口是80
        ssl协议位于tcp协议与应用层协议之间，内部又分为两层：
            ssl记录协议：位于tcp之上，提供数据封装、加解密功能
            ssl握手协议：位于ssl记录协议之上，在实际数据传输前，
                         验证双份身份、协商加密算法、交换密钥等。
         ssl/tls是依托于tcp的，还有个dtls，是同样的tls逻辑应用与udp之上。
        
挑战应答机制（CRAM : challenge-response authentication mechanism）
    总介
        CRAM是一种实现身份验证时但参考技术方案，也就是说，
        当需要验证身份时，可使用参考使用这种方式。
    流程（基于客户端持有服务器的证书）
        1. 客户向认证服务器发出请求，要求进行身份认证；
        2. 认证服务器从用户数据库中查询用户是否是合法的用户，
           若不是，则不做进一步处理；
        3. 认证服务器内部产生一个随机数，作为"提问"，发送给客户；
        4. 客户将口令和随机数合并，使用单向Hash函数（例如MD5算法）
           生成一个字节串作为应答；
        5. 认证服务器将应答串与自己的计算结果比较，若二者相同，
           则通过一次认证；否则，认证失败；
        6. 认证服务器通知客户认证成功或失败。
        
        以后的认证由客户不定时地发起，过程中没有了客户认证请求一步。
        两次认证的时间间的密钥隔不能太短，
        否则就给网络、客户和认证服务器带来太大的开销；
        也不能太长，否则不能保证用户不被他人盗用IP地址，一般定为1-2分钟。
    流程（基于服务器知道用户的密码）
        1. 客户端请求一个受保护的资源。
        2. 服务器发送一个挑战字符串C。
        3. 客户端产生一个随机字符串R。
           客户端根据C、R以及用户的密码产生一个哈希值。
           客户端把R以及哈希值发到服务器端。
        4. 服务器根据保存的用户密码以及R重新计算一个哈希值。
           服务器将重新计算的哈希值与客户端发来的哈希值进行比较，
           如果相等，则认证通过，把受保护的资源返回给客户端，
           否则返回一个错误的认证信息。
    目的
        如何在受到窃听的信道中完成身份认证，但不泄露任何秘密
        如果不使用，会遭到窃听和重放攻击。
        什么是重放攻击
            客户端A向服务器发送表明身份的包，攻击者记录下该包，
            下次攻击者想连接服务器的时候，就给服务器发送上面记录下的包，
            假装自己是客户端A
    从验证身份说起
            用户张三通过客户端页面向服务器请求某些特定资源时(如个人信息展示页面), 
        需要确认用户张三的身份，如果身份验证失败，则不允许访问该页面，这就是身份验证的意义。
            身份验证的基本手段，是将张三的用户名和密码告诉服务器，
        服务器将用户名和密码与数据库里的比对，成功，则表明用户身份的有效性
            用户名可以以明文的形式在网络上传输，但密码则不合适，
        解决办法是将密码进行哈希后传给服务器，服务器则根据张三从数据库中
        取出相应的密码，并计算hash值，然后与用户传来的密码hash比较，
        以此来判断用户张三身份的有效性。
            通过上面的方式，即使第三方李四拿到用户名张三和其密码的hash值，
        也不能知道张三的密码是什么，这看似安全，但实则漏洞明显：
        李四只要每次拿张三的名字和张三密码的hash值告诉给服务器，
        则服务器就会认为这是张三登录的，并且身份是有效的，这就是所谓的重放攻击。
            解决办法可以有多种，一种办法是张三在生成密码的哈希值时，
        不是直接对密码hash，而是将密码与当前时间拼合后做hash，
        服务端也是同样的操作，从数据库中取出张三的密码，
        然后将该密码与当前时间拼合后作hash，然后与张三传来的hash值作比较。
        但这里有个问题，张三做hash时，取的时间，与服务器做hash时取得时间可能是不一致的，
        即便张三机器的时间与服务器的时间完全同步，也会因数据在网络中传输操作的延时，
        存在1~n秒的时差。
            所以我们变通一下：张三把hash(时间+密码)传给服务器时，同时将时间以明文形式传给服务器，
        服务器拿到该明文的时间后，与服务器的时间比较，看是否在误差范围以内，
        如果是，就计算hash(张三传来的时间+数据库中张三的密码)，然后与张三传来的hash比较
        这样以来，李四就没法用张三的hash和张三的名字冒充登录了:
        李四拿到哈希后，既不能还原出张三的密码，拿该哈希值传给服务器后，
        也会因为时间超时而验证不通过。
            除了上面加时间戳方式，也可以使用随机数的方式，操作办法是，
        服务器每次连接时都现生成个随机数，把该随机数传给传给张三，
        张三把hash(服务端传来的随机数+自己的密码)传给服务器，
        服务器端则计算hash(本次为张三生成的随机数+数据库里张三的密码)，
        然后比较这两个hash，验证张三的身份，而这种方式就是挑战认证方式的原型。
    挑战认证为什么是客户端发起，而不是服务器发起
        客户端页面一般是在请求某种服务器上的某种需要分身验证的资源时(如分身信息展示页面)，
        才主动发起（否则他请求该资源就提示没有权限），所以从这种意义上说，
        也不能算是客户端“主动”发起的，而是他不得已而为之。
      
https vs. CRAM
    https是为了验证服务器A（如百度）确实是服务器A，而不是假冒A的服务器（如百复），
    同时还起到传递对称密钥（加密传输数据）的作用。
    CRAM则是为了验证用户a（如张三）确实是用户a，而不是假冒a的用户（如李四）。
    
CRAM举例
    ppp协议（链路层协议）中鉴别阶段使用的CHAP协议，就是一种挑战应答方式的协议
    通常我们判断一个用户名密码是否正确，可以直接把用户名密码明文发给服务端
    服务端比较数据库中记录的密码，判断密码是否正确
    但这样极不安全，所以，在此基础上进行改进，把密码计算哈希，
    然后把用户名和hash（密码）发给服务端
    但这样也存在隐患，第三方截获了用户名和hash（密码）后，仍可以冒充真正的用户进行登录
    所以，在此基础上，再次改进，（CHAP协议就是一个典型例子：
    （CHAP协议就是一个典型例子://blog.csdn.net/bytxl/article/details/50111971）
    服务端可以先将一个每次都不一样的随机字符串发给客户端，
    客户端将此字符串与自己的密码拼接后再做hash，然后把哈希值和用户名发给服务端
    服务端同样用发给客户端的随机数和从数据库中取到的用户密码拼接后求哈希，
    然后与用户传来的哈希值做比较，这样，即使携带用户名和hash(随机字符串+密码)的数据包被截获
    也没有意义，因为随机字符串是每次/经常变的，
    服务端可能每过一段时间就变一次，每变一次就向服务端进行一次互相验证
    所以这种方式是比较安全的，这就是挑战应答模式