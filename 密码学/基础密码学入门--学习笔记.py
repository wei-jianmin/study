参：https://zhuanlan.zhihu.com/p/270872278
    常见的hash算法分类 
        MD5
            MD5算法是一种常见的hash算法，其摘要值长度固定是128比特，
            目前MD5已经被证实是一种不安全的算法
        SHA-1
            类似MD5，摘要值长度是160比特
            目前SHA-1算法在严谨的加密学中已经被证明是不安全的
            尽量使用SHA-2类的Hash算法
        SHA-2
            目前建议使用的Hash算法，截至目前是安全的
            主要有四种算法，分别是SHA-256、SHA-512、SHA-224、SHA-384
            输出的长度分别是256比特、512比特、224比特、384比特
        SHA-3
            SHA-3算法并不是为了取代SHA-2算法，
            而是一种在设计上和SHA-2完全不同的算法
            主要有四种算法，分别是SHA3-256、SHA3-512、SHA3-224、SHA3-384
            输出的长度分别是256比特、512比特、224比特、384比特
    对称加密算法
        加密和解密使用同样的一个密钥
        对称加密算法有两种类型，分别是流密码算法（stream ciphers）和 块密码算法（block ciphers）
        流密码算法
            RC4 
                可变密钥长度，建议2048比特  目前已被证明不安全
            ChaCha
                可变密钥长度，建议256比特   一种新型的流密码算法
        块密码算法
            参看：file://密码学入门_块密码算法.jpg
            建议使用AES
                该算法是对称加密算法的标准算法
                AES算法使用的密钥通过口令和Salt生成，同样的口令和Salt会生成同样的密钥
                Salt的主要作用是为了保证同样的口令可以生成不同的密钥，是明文传输的
    消息验证码(MAC)算法
        为什么需要MAC算法
            hash算法只可以验证数据的完整性，但是无法保证数据防篡改
            如果原文和哈希值在从A发给B的过程中，被C调包了，则B无法察觉
            而MAC算法，使用双方约定好的密钥，对原文进行MAC运算，
            A将原文和MAC值发给B，B用同样的密钥对原文进行MAC运算，并将结果与A发来的MAC比较
            只要密钥不被除A、B外的第三者知道，就不会存在数据被掉包的风险
        MAC算法分类
            CBC-MAC
                对称密码算法中，CBC 模式使用最后一个分组的输出结果作为 MAC
                需要注意的是，基于 CBC 模式的 MAC 有许多安全特性与 CBC 模式并不相同，
                包括不能使用初始向量(初始向量为全 0)， 
                以及只能为约定好长度的消息产生鉴别码等。
            HMAC
                HMAC 是利用杂凑算法，将一个密钥和一个消息作为输入，生成一个消息摘要作为输出
                HMAC结合Hash算法有多种变种，比如HMAC-SHA-1、HMAC-SHA256、HMAC-SHA512
                不要误以为HMAC算法就是Hash算法加上一个密钥，
                HMAC算法只是基于Hash算法的，内部的实现还是相当复杂的。
    公开密钥算法
        公开密钥算法不是一个算法而是一组算法，
        如果公开密钥算法用于加密解密运算，习惯上称为非对称加密算法
    秘钥
        如何生成密钥
            基于伪随机生成器生成密钥
            基于口令的加密（Password-based Encryption，简称PBE）算法产生密钥
                PBE算法生成的密钥一般情况下无须存储，因为使用同样的口令就能生成同样的密钥，这是其优点之一
                PBE算法生成的密钥有时候并不是为了使用该密钥，而有其他用途
        密钥存储与运输
            静态密钥
                密钥硬编码在代码中。
                以口头、邮件的方式传输密钥
            动态密钥
                密钥协商算法
    密钥协商算法
        会话密钥
            动态密钥也叫会话密钥，会话密钥只有服务器端和特定的客户端才能知晓
            会话密钥的作用就是为了加密解密通信数据
            会话密钥的意思就是该密钥不用存储，一旦客户端和服务器端的连接关闭，该密钥就会消失
            常见会话密钥可以使用伪随机数生成器生成，数量也可以无限多
            通信双方所持有的会话密钥是相同的，也就是说，会话密钥是对称密钥
        RSA密钥协商算法如何工作的
            1.客户端初始化连接服务器端，服务器发送RSA密钥对的公钥给客户端。
            2.客户端生成一个随机值，这个值必须是随机的，不能被攻击者猜出，这个值就是会话密钥。
            3.客户端使用服务器RSA密钥对的公钥加密会话密钥，并发送给服务器端，
              由于攻击者没有服务器的私钥，所以无法解密会话密钥。
            4.服务器端用它的私钥解密出会话密钥。
            5.至此双方完成连接，接下来服务器端和客户端可以使用对称加密算法和会话密钥加密解密数据
            注：这个方案用途非常广泛，HTTPS本身也是借鉴了这个方案，只是在设计上更严谨
        DH密钥协商算法
            RSA密钥协商算法传输会话密钥的时候，
            会话密钥完全由客户端控制，并没有服务器的参与，所以叫作密钥传输
            DH算法原理参：file://DH算法原理及ssl实现过程.txt
            