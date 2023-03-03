<< 学习OpenCV 3 中文版 >>
第二章 OpenCV初探
    头文件：
        可直接包含OpenCV2/opencv.hpp,
        该文件里面包含OpenCV各个模块的头文件
        opencv2/
            core/               结构及数学运算
                core_c.h        旧式C风格的结构及运算
                core.hpp        新式C++风格的结构及数学运算
            flann/              最邻近搜索匹配函数
                miniflann.hpp   最邻近搜索匹配函数
            imgproc/            图像处理函数
                imgproc_c.h     旧式C风格的图像处理函数
                imgproc.hpp     新式C++风格的图像处理函数
            video/              照片相关算法、视觉追踪
                photo.hpp       操作和恢复照片相关算法
                video.hpp       视觉追踪及背景分割
            featuresd/          用于追踪的二维特征
                features2d.hpp  用于追踪的二维特征
            objdetect/          分类器
                objdetect.hpp   级联人脸分类器、latent  SVM分类器、HoG特征和平面片检测器
            calib3d/            视觉相关    
                calib3d.hpp     校准及双目视觉相关
            ml/                 机器学习
                ml.hpp          机器学习、聚类、模式识别
            highgui/            界面及用户交互
                highgui.hpp     新式C++风格的显示、滑动条、鼠标操作、输入输出等
            contrib/            用户贡献的代码
                contrib.hpp     用户贡献的代码、皮肤检测、模糊Mean-shift追踪、spin image算法及自相似特征           
    显示图片 
        #include<opencv2/highgui/highgui.hpp"
        cv::Mat img = cv::imread("c:/1.bmp");
        if(img.empty()) return -1;
        cv::nameWindow("eg1",cv::WINDOW_AUTOSIZE);
        cv::imshow("eg1",img);
        cv::waitKey(0);
        cv::destroyWindow("eg1");
        cv::Mat结构可以用来存储各种类型的图像。
    播放视频
        #include<opencv2/highgui/highgui.hpp"
        #include<opencv2/imgproc/imgproc.hpp"
        int bar_pos=0;
        cv::Mat frame;
        cv::VideoCapture cap;
        cap.open( ? );      //传入视频文件路径
        
        int frames = cap.get(cv::CAP_PROP_FRAME_COUNT); //获取帧数
        int w = cap.get(cv::CAP_PROP_FRAME_WIDTH);
        int h = cap.get(cv::CAP_PROP_FRAME_HEIGHT);
        
        cv::namedWindow("eg3",cv::WINDOW_AUTOSIZE);
        cv::createTrackbar("pos","eg3",&bar_pos,frames,bar_callback);
        
        while(1)
            cap>>frame;     //获取视频帧
            if(frame.empty()) break;
            cv::imshow("eg3",frame);
            int cur_pos = cap.get(cv::CAP_PROP_POS_FRAMES);
            cv::setTrackbarPos("pos","eg3",cur_pos);
            char c = cv::waitKey(33);
            if(c=='x') break;
        
        void bar_callback(int pos,void*)
            //pos代表拖动后的位置，可以此控制视频播放进度
            cap.set(cv::CAP_PROP_POS_FRAMES,pos);   //设置位置
    图像处理
        cv::Mat img1,img2;
        img1 = cv::imread("img文件路径");
        cv::pyrDown(img1,img2);         //高斯模糊或降采样
        cv::GaussianBlur(img2,img2,cv::Size(5,5),3,3);    //还有blue()、medianBlue()、bilateralFilter()
        cv::cvtColor(img2,img2,cv::COLOR_BGR2GRAY);
        cv::Canny(img2,img2,10,100,3,true);
        cv::Vec3b color = img1.at<cv::Vec3b>(x,y);
        uchar blue = color[0];
        uchar green = color[1];
        uchar red = color[2];
    录制摄像头
        cv::VideoCapture cap;
        cap.open( 0 );      //打开第一个摄像头
        if(cap.isOpened() == false)
            return;
        double fps = cap.get(cv::CAP_PROP_FPS);
        cv::Size size(
            cap.get(cv::CAP_PROP_FRAME_WIDTH),
            cap.get(cv::CAP_PROP_FRAME_HEIGHT));
        cv::VideoWriter writer;
        writer.open("路径",CV_FOURCC('M','J','P','G'),fps,size);
        cv::Mat frame;
        while(1)
            cap >> frame;
            if(frame.empty()) break;
            writer << frame;
            char c = cv::waitKey(10);
            if(c=='x') break;
第三章 OpenCV数据类型 
    OpenCV的基础数据类型主要分三大类：
        直接从c++中继承发展的类型，如int、数组、矩阵、点、矩形等
        辅助对象，如垃圾收集指针、终止条件类等
        大型数组类型，典型代表是cv::Mat
    简单类型
        cv::Vec<> 模板容器类，称为固定向量类，
            它比stl中的容器类容量小（最多压入不能超过9个数据）
            因为小，也允许它涉及的更高效。
            cv::Vec2i,cv::Vec3i,cv::Vec4d等这样的名称，都是由typedef cv::Vec<>声明的。
            提供叉乘成员函数：cross()
        cv::Matx<> 则是二维的矩阵型模板容器类，称为固定矩阵类。
            一般处理矩阵的使用会使用该类，而像如图像或大型点阵，则应该用cv::Mat。
            默认构造函数: cv::Matx33f（3*3大小）、cv::Matx43d等
            构造元素值相等的矩阵：all(x)
            构造全零矩阵：zeros()
            构造全1矩阵：ones()
            构造单位矩阵：eye()
            创建均匀分布的矩阵：randu(min,max)
            创建正在分布矩阵：nrandn(mean,variance)
            矩阵运算：m1=m0、m1*m0、m1+m0、m1-m0、m1==m0、m1!=m0、
                      m1*a、a*m1、m1/a、m1.dot(m2)、m1.ddot(m2)、m1.mul(m2)
            改变矩阵形状：reshape<>()
            提取子矩阵: get_minor<>()
            提取第i行： row(i)
            提取第j列： col(j)
            提取对角线： diag()
            转置矩阵： t()
            逆矩阵：inv(method); 默认值为cv::DECOMP_LU
            解线性系统： solve<>(),solve()
        cv::Point_<>模板类，程序中主要使用的是cv::Point2i、cv::Point3f这样的别名
            类内提供点乘(dot)、叉乘(cross)、判断当前点是否在矩形内(inside)、
            向固定向量类转换(cv::Vec3f)等成员方法。
            可以直接与C接口类型CvPoint、CvPoint2D32f互相转换。
        cv::Scalar_<>模板类，本质是个四维Point类，继承cv::Vec<double,4>而来。
            提供矩阵相乘（mul）等成员函数，同时继承cv::Vec<>提供的方法
            可以与旧式C语言接口的CvScalar自由互换。
        cv::Size,实际是cv::Size2i的别名，另外还有cv::Size2f
            提供计算面积的成员方法area()
        cv::Rect,整数类型矩形的别名，记录的是左顶宽高
            提供获取左上角(tl)、右下角(br)、判断点是否在矩形内(contains)等成员方法。
            重载了&,|运算符，用于求矩形的交集与并集。
            重载了==,!=运算符，用于判断两个矩形是否相等。
            重载了+,+=运算符，用于平移/缩放矩形。
        cv::RotatedRect，少数底层没有使用模板的C++接口类之一。
            是个包含中心点、大小和角度等成员变量
            提供获取四个角坐标的成员方法potins(pts[4])
        cv::Complexf，复数类
            .re ：实数部分，.im ： 虚数部分
            conj() ： 共轭复数
    辅助对象
        cv::TermCriteria 许多函数需要提供一个终止条件以决定何时退出
        cv::Range  确定一个连续的整数序列，有start和end两个元素
        cv::Ptr 智能指针,支持*、->等运算符
            使用举例： cv::Ptr<Matx33f> p(new cv::Matx33f);
                       cv::Ptr<Matx33f> p2 = makePtr<cv::Matx33f>();
            支持release（）手动释放
            empty()方法判断该指针是否指向一个已经释放掉的对象或为NULL
        cv::Exception 异常类，继承自std::exception
            有code、err、func、file、line等成员变量
            CV_Error(errorcode，description)宏 ： 抛出异常
            CV_Error_(errorcode，printf_fmt_str, [args]) 宏：与上面类似
            CV_Assert(condition)、CV_DbgAssert(condition)宏：条件不符合，发出异常
第四章 图像和大型数组类型
    稠密数组与稀疏数组
        稠密数组，意味着值为0的元素仍然占用空间
        稀疏数组，意味着只为值不为0的元素分配空间
        但数组中存在大量值不为0的元素时，使用稀疏数组反而更浪费空间
        当数组中有大量0值元素时，适合使用稀疏数组
    cv::Mat类
        图像可以按不同维度存储
            图像可以按一维数组存储，所有的像素数据依次存在数组中
            也可以按二维数组存储，像素按行列顺序存储在数组中
            还可以按三维数组存储，每个通道的像素占用一个平面
        Mat存储数据的方式：data+step[]
            所有矩阵，都有个flag成员变量表示数组类型，dims表示维度
            data指针指向真正数据的存储位置，refcount表示引用计数，
            row/col表示行列数（维度大于两维时无效）。
            step[]描述像素/行/颜色平面所占用字节数的大小，
            如一个二维数组，则第i行，第j列像素的位置为：
            mtx.data+mtx.step[0]*i+mtx.step[1]*j,
            step[0]记录一行像素所占字节数，step[1]记录一个像素所占字节数
        创建Mat数组
            使用不带参数的构造函数
                声明数组 cv::Mat mat；这样声明出来的数组是没有大小和数据类型的，
                之后通过mat.create(3,3,CV_32FC3);达到申请内存区域的目的
                CV_32FC3表三通道的32位浮点数据，其它的还有如：
                CV_{8U,16S,16U,32S,32F,64F}C{1,2,3}，C后面跟的数字表示通道数。
                如果要创建超过3通道的，应该使用CV_{8U,16S,16U,32S,32F,64F}C(x)
                其中x为通道数，这是个函数，如：
                CV_8UC(4)，可以用于创建8位CMYK四通道的带颜色索引的图像。
                其实CV_32FC3等价于CV_32FC(3)，可以认为#define CV_32FC3 CV_32FC(3)
                只是对于超过3通道的，没有相关的宏定义。
                这些宏/函数的本质是一些整数值，除了上面的形式，也可以是cv::DateType<>
                模板的type成员值，如：cv::DataType<cv::Complexf>::type
            带参构造函数
                带参构造函数将近有20来个，但常用的可能只有其中的几个
                cv::Mat(int rows,int cols,int type);
                cv::Mat(int rows,int cols,int type,const Scalar&s); 
                cv::Mat(cv::Size sz,int type);
                cv::Mat(cv::Size sz,int type,const Scalar&s); //s参数用于初始化元素值
                cv::Mat(cv::Size sz,int type,void *data,size_t step=AUTO_STEP); //Mat会使用data区域
                cv::Mat(const Mat& mat);
                cv::Mat(const Mat& mat,const cv::Range& rows,const cv::Range& cols); //复制指定区块
                cv::Mat(const Mat& mat,const cv::Rect& roi);
                cv::Mat(const cv:MatExpr& expr);    //从数组表达式构建
                从旧的cvMat或IplImage建立cv::Mat
                    cv::Mat(const CvMat* old,bool copyData=false);
                    cv::Mat(const IplImage *old,bool copyData=false);
                参数为模板形式的构造函数
                    cv::Mat(const cv::Vec<T,n>& vec,bool copyData=true);
                    cv::Mat(const cv::Matx<T,m,n> &vec,bool copyData=true);
                    cv::Mat(const std::vector<T>& vec,bool copyData=true);
                。。。（用于创建多维图像的，如立体图像）
            构造cv::Mat的静态方法
                cv::Mat::zeros(rows,cols,type);
                cv::Mat::ones(rows,cols,type);  //只设置第1通道，其它通道仍为0
                cv::Mat::eye(rows,cols,type);   //只设置第1通道，其它通道仍为0
        获取元素
            通过位置访问
                模板函数at<>() : 获取具体行列
                    如：cv::Vec2f vec = mat.at<cv::Vec2f>(3,3);
                    然后使用vec[2]得到第2个通道上的像素，
                    也可以直接写为mat.at<cv::Vec2f>(3,3)[2];
                模板函数Ptr<>() ： 获取某行
                    如：cv::Vec2f *pvec = mat.at<cv::Vec2f>(3);
                直接操作数据指针data
                    如一个二维数组，则第i行，第j列像素的位置为：
                    mtx.data+mtx.step[0]*i+mtx.step[1]*j
                    这种方法较为原始和直接，效率虽快，但不推荐
                Mat数组的连续性说明
                    成员函数isContinuous()告诉你数组是否是连续的，
                    如果矩阵元素在每行末尾连续存储而没有间隙，则方法返回true。 
                    否则，它返回false。 显然，对于1x1或1xN矩阵总是连续的。
                    一般用Mat :: create创建的矩阵总是连续的。 
                    但是，如果使用Mat :: col，Mat :: diag等提取矩阵的一部分，
                    或者为外部分配的数据构造矩阵头，则此类矩阵可能不再具有此属性。
            使用迭代器访问
                cv::MatConstIterator<>，cv::MatIterator<>
                使用迭代器指针，可以不用理会Mat内部数据内存是否是连续的，因而使用起来非常方便
            通过块访问数组元素
                通过Mat的成员函数，可以获取该mat的一个子集，如某一行、某一列、某个子矩阵等
                    m2=m1.row(i);
                    m2=m1.col(j);
                    m2=m1.rowRange(i0,i1);
                    m2=m1.colRange(j0,j1);
                    m2=m1.rowRange(cv::Range(i0,i1));
                    m2=m1.colRange(cv::Range(j0,j1));
                    m2=m1.diag(d);  //对角线，如果为正，则向上偏移，为负，则向下偏移
                    m2=m1(cv::Range(i0,i1),cv::Range(j0,j1));  子矩阵
                    m2=m1(cv::Rect(i0,i1,w,h));
                    m2=m1(ranges);
                    需要说明的是，通过这种方式得到的Mat，其data与原Mat指向的区域一致，
                    而只是变了图像描述信息，这是为了更快的复制，对m2图像的更改会影响m
        Mat对运算符的重载
            m2=m1 ：此时不发生数据拷贝，m2相当于对m1的一个引用
            m2=m1+m0 : 计算结果的指针指向m2,结果处于一个新的内存中
            矩阵运算：
                m0+m1,m0-m1
                m0+s; m0-s; s+m0; s-m0; 矩阵和单个元素的加减
                s*m0; m0*s;
                m0*m1       叉矩阵乘法
                m0.mul(m1); 元素级相乘
                m0/m1;      元素级相除
                m0.inv(method)
                m0.t()
                m0>m1; m0>=m1; m0==m1; m0<=m1; m0<m1;  按元素比较，返回元素值为0/255的uchar矩阵
                m0&m1; m0|m1; m0^m1; ~m0; 元素直接按位操作，返回的也是矩阵
                m0&s; m0|s; m0^s; s&m0; s|m0; s^m0;
                min(m0,m1); max(m0,m1); min(m0,s); max(m0,s); min(s,m0); max(s,m0);
                cv::abs(m0);
                m0.cross(m1); m0.dot(m1);  叉乘（行列对应相乘的和）与点乘（对应元素相乘）
                各种矩阵乘法的对比：
                    dot
                        Mat矩阵的dot方法扩展了一维向量的点乘操作，
                        把整个Mat矩阵扩展成一个行（列）向量，
                        之后执行向量的点乘运算，
                        仍然要求参与dot运算的两个Mat矩阵的行列数完全一致
                        返回值为double类型
                    mul
                        元素对应相乘，返回的仍是矩阵
                    *
                        两个向量的叉乘
                    cross
                        该方法计算两个3元素vector的叉乘，vector必须为3元素的浮点类型。
                饱和转换
                    当运算发成溢出时，会自动检查，并将溢出值转为最大/最小值。
        Mat类的更多函数成员
            m1=m0.clone(); 
            m0.copyTo(m1); 
            m0.copyTo(m1,mask);  只复制mask所指示的区域
            m0.convertTo(m1,type,scale,offset);
            m0.setTo(s,mask);  设置m0所有元素为s,如果存在mask，则只对mask区域进行操作
            m0.push_back(s);  在末尾增加一个m*1大小的数组
            m0.push_back(m1);  m*n矩阵m0，k*n矩阵m1，将两者合并后，放到m1中
            m-.pop_back(d);   从m*n大小的矩阵中移除d行（默认是1）
            m0.locateROI(size,offset);  将m0的尺寸写入到cv::Size型变量size中，
                                        如果m0是一个大矩阵中的一块区域，
                                        则还会写入一个Point类型的offset
            m0.adjustROI(t,b,l,r);  通过四个值，调整ROI范围
            m0.total();  计算数组序列元素的数目（同一通道内的算一个元素）
            m0.isContinuous();  m0的行之间有没有空隙
            m0.elemSize()  返回m0的位长度，如三通道浮点，返回12
            m0.elemSize1()  返回m0最基本元素的位长度，如三通道浮点，返回4
            m0.type()   返回m0元素的类型，如CV_32FC3
            m0.depth()  返回m0通道中的元素类型，如CV_32F
            m0.channels()  返回m0通道数目
            m0.empty()  数组为空时返回true，如m0.total==0或m.data==NULL
    cv::SparseMat类
        稀疏矩阵在数组中非0元素非常少的时候使用
        稀疏矩阵一般来说计算速度都更慢
        稀疏矩阵的函数很多都类似于稠密矩阵Mat
        稀疏矩阵使用哈希表来存储非0元素(当元素在计算后变为0后，仍会被存储)
        访问稀疏数组中的元素
            四种访问机制：
                cv::SparseMat::ptr()
                    uchar *cv::SparseMat::ptr(int i0,bool createMissing,size* hashval=0);
                        用于访问一维数组，第一个参数是元素索引，
                        第二个参数表元素实现不存在与数组中时，是否被创建
                cv::SparseMat::ref()
                cv::SparseMat::value()
                cv::SparseMat::find()
                        
                