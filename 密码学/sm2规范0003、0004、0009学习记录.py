sm2是一组算法
    sm2-1 椭圆曲线数字签名算法
    sm2-2 椭圆曲线密钥协商协议
    sm2-3 椭圆曲线加密算法

sm2的密钥对
    sm2私钥，简记为k，长度256位，>=1,<=n-1（n为sm2算法的阶）
    sm2公钥，简记为Q，是sm2曲线上的一个点，有横、纵坐标(x,y)来表示，
             每个坐标分量的长度是256位，共512位

数据格式
    密钥数据格式：
        私钥：INTEGER
        公钥：BIT STRING : 04||X||Y，X和Y分别为公钥的x分量和y分量
    明文加密后的数据格式：
        SM2Cipher ::= SEQUENCE  {
            XCoordinate  INTEGER,                   -公钥x分量，256位
            YCoordinate  INTEGER,                   -公钥y分量，256位
            HASH         OCTET STRING SIZE(32),     -sm3杂凑值,256位
            CipherText   OCTET STRING               -密文
        }
        HASH = SM3(x2 || m || y2)                   -m为明文数据
    签名数据格式：
        SM2Signature::= {
            R INTEGER,          -签名值的第一部分
            S INTEGER           -签名值得第二部分
        }
        
加密算法流程
    1. 产生随机数k
    2. C1 = (x1,y1) = kG，将(x1,y1)转为比特串
    3. 找出Pb，满足S=[h]Pb不是无穷远点，否则会报错退出
    4. (x2,y2) = [k]Pb，将(x2,y2)转为比特串
    5. t = KDF(x2||y2,klen)
    6. C2 = M ⊕ t 
    7. C3 = Hash(x2 || M || y2)
    8. C = C1 || C2 || C3  （或 C = C1 || C3 || C2 , 具体是哪种，由双方约定）
    
密钥对保护数据格式
    将SM2私钥对称加密，并用外部SM2公钥加密对称密钥，然后把这两者放到如下架构中：
    SM2EnvelopedKey ::= SEQUENCE{
        symAlgID                AlogorithmIdentifier,   --对称密码算法标识
        sysEncryptedKey         SM2Cipher,              --对称密钥密文
        Sm2PublicKey            SM2PublicKey,           --SM2公钥
        Sm2EncryptedPrivateKey  BIT STRING              --SM2私钥密文
    }
    
Z值
    Z = SM3（ENTL || ID || a || b || xG || yG || xA || yA）
    ENTL      由2个字节表示的ID的比特长度
    ID        用户身份标识
    a、b      系统曲线参数
    xG、yG    曲线基点
    xA、yA    用户的公钥
    
杂凑值H
    H = SM3（Z || M）
    M         待签名消息
    
计算过程（相关的方法函数）
    生成SM2密钥对
        输入：无
        输出：私钥k(长度256位)，公钥Q(长度512位)
    加密
        输入：公钥Q，明文字符串m
        输出：密文c（c的数据格式在前面已介绍）
    解密
        输入：私钥d、密文c
        输出：明文字符串m
    签名
        输入：私钥d、杂凑值H
        输出：签名值sign
    验证
        输入：杂凑值H、签名值sign、公钥Q
        输出：真/假

密钥协商
    假定协商双方为A、B，其密钥对分别为（dA,QA）、（dB,QB）
    阶段1：
        A产生临时密钥对(rA,RA)，将 RA 和 A的身份标识IDA 发给B
        B产生临时密钥对(rB,RB)，将 RB 和 B的身份标识IDB 发给A
    阶段2：
        A计算共享密钥
            输入：
                QB  ： B的公钥
                RB  ： B的临时公钥
                IDB ： B的身份标识
                dA  ： A的私钥
                QA  ： A的公钥
                rA  ： A的临时私钥
                RA  ： A的临时公钥
                IDA ： A的身份标识
                klen： 需要输出的密钥数据的比特长度
            输出：
                K   ： 长度为klen的密钥数据
        B计算公钥密钥：
            输入：
                QA  ： A的公钥
                RA  ： A的临时公钥
                IDA ： A的身份标识
                dB  ： B的私钥
                QB  ： B的公钥
                rB  ： B的临时私钥
                RB  ： B的临时公钥
                IDB ： B的身份标识
                klen： 需要输出的密钥数据的比特长度
            输出：
                K   ： 长度为klen的密钥数据