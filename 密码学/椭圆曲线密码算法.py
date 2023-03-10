椭圆曲线密码学（ECC，Elliptic Curve Cryptogphay）
背后的数学原理，是椭圆曲线上的离散对数难题:
给定素数p和椭圆曲线E，对Q=kP，在已知P，Q 的情况下求出小于p的正整数k。
可以证明由k和P计算Q比较容易，而由Q和P计算k则比较困难
    
椭圆曲线加密
    参考资料：
        https://www.zhihu.com/question/26662683
    设Fp表示具有p个元素有限域，p为大于3的素数。
    Fp上的椭圆曲线E是一个点集：
    E : { (x,y) | y^2 = x^3 + ax + b, a,b,x,y∈Fp }
    a,b满足不等式： 4*a^3 + 27*b^2 != 0
    该椭圆并不是真正的椭圆，其样式大概如图 file://椭圆曲线图.png
    我们已经知到了椭圆曲线的图象，但点与点之间好象没有什么联系。
    我们能不能建立一个类似于在实数轴上加法的运算法则呢？
    这就要定义椭圆曲线的加法群：
        任意取椭圆曲线上两点P、Q（若P、Q两点重合，则作P点的切线），
        作直线交于椭圆曲线的另一点R'，过R'做y轴的平行线交于R，定义P+Q=R。
        这样，加法的和也在椭圆曲线上，并同样具备加法的交换律、结合律
        参考图片 file://椭圆曲线上点的加法运算.png
        同点加法:
        若有k个相同的点P相加，记作kP, 则P+P+P=2P+P=3P
        参考图片 file://椭圆曲线上多点的加法运算.png
    离散椭圆曲线上的加法运算：
        1.无穷远点 O∞是零元，有O∞+ O∞= O∞，O∞+P=P
        2.P(x,y)的负元是 (x,-y mod p)= (x,p-y) ，有P+(-P)= O∞
        3.P(x1,y1),Q(x2,y2)的和R(x3,y3) 有如下关系：
            x3≡k2-x1-x2(mod p)
            y3≡k(x1-x3)-y1(mod p)
            若P=Q  则 k=(3x2+a)/2y1mod p
            若P≠Q，则k=(y2-y1)/(x2-x1) mod p
    如果椭圆曲线上一点P，存在最小的正整数n使得数乘nP=O∞ ,则将n称为P的阶
    若n不存在，则P是无限阶的，参考图片：file://离散椭圆曲线上点P的阶.jpg
    椭圆曲线加密
        考虑P=kG ，其中P、G为椭圆曲线Ep(a,b)上的点，
        n为G的阶（nG=O∞），k为小于n的整数。
        则给定P和G，根据加法法则，计算P很容易，
        但反过来，给定P和G，求k就非常困难。
        因为实际使用中的ECC原则上把p取得相当大，n也相当大，
        要把n个解点逐一算出来是不可能的。
        这就是椭圆曲线加密算法的数学依据
        点G称为基点（base point）
        k（k<n）为私有密钥（privte key）
        P为公开密钥（public key)
        
ECC保密通信算法
    参考资料：
        https://www.zhihu.com/question/26662683
    1.Alice选定一条椭圆曲线E，并取椭圆曲线上一点作为基点G  
      假设选定E29(4,20)，基点G(13,23) , 基点G的阶数n=37
    2.Alice选择一个私有密钥k（k<n），并生成公开密钥 P=kG   
      比如25, P= kG = 25G = (14,6）
    3.Alice将E和点P、G传给Bob
    4.Bob收到信息后，将待传输的明文编码到上的一点M（编码方法略），
      并产生一个随机整数r（r<n,n为G的阶数）   
      假设r=6  要加密的信息为3,
      因为M也要在E29(4,20) 所以M=(3,28)
    5.Bob计算点 C1=M+rP 和 C2=rG  
      C1= M+6P= M+6*25*G=M+2G=(3,28)+(27,27)=(6,12)  
      C2=6G=(5,7)
    6.Bob将C1、C2传给Alice
    7.Alice收到信息后，计算C1-kC2，结果就应该是点M  
      C1-kC2 =(6,12)-25C2 =(6,12)-25*6G =(6,12)-2G 
             =(6,12)-(27,27) =(6,12)+(27,2) =(3,28)
