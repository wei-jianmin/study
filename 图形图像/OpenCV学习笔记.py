<< ѧϰOpenCV 3 ���İ� >>
�ڶ��� OpenCV��̽
    ͷ�ļ���
        ��ֱ�Ӱ���OpenCV2/opencv.hpp,
        ���ļ��������OpenCV����ģ���ͷ�ļ�
        opencv2/
            core/               �ṹ����ѧ����
                core_c.h        ��ʽC���Ľṹ������
                core.hpp        ��ʽC++���Ľṹ����ѧ����
            flann/              ���ڽ�����ƥ�亯��
                miniflann.hpp   ���ڽ�����ƥ�亯��
            imgproc/            ͼ������
                imgproc_c.h     ��ʽC����ͼ������
                imgproc.hpp     ��ʽC++����ͼ������
            video/              ��Ƭ����㷨���Ӿ�׷��
                photo.hpp       �����ͻָ���Ƭ����㷨
                video.hpp       �Ӿ�׷�ټ������ָ�
            featuresd/          ����׷�ٵĶ�ά����
                features2d.hpp  ����׷�ٵĶ�ά����
            objdetect/          ������
                objdetect.hpp   ����������������latent  SVM��������HoG������ƽ��Ƭ�����
            calib3d/            �Ӿ����    
                calib3d.hpp     У׼��˫Ŀ�Ӿ����
            ml/                 ����ѧϰ
                ml.hpp          ����ѧϰ�����ࡢģʽʶ��
            highgui/            ���漰�û�����
                highgui.hpp     ��ʽC++������ʾ���������������������������
            contrib/            �û����׵Ĵ���
                contrib.hpp     �û����׵Ĵ��롢Ƥ����⡢ģ��Mean-shift׷�١�spin image�㷨������������           
    ��ʾͼƬ 
        #include<opencv2/highgui/highgui.hpp"
        cv::Mat img = cv::imread("c:/1.bmp");
        if(img.empty()) return -1;
        cv::nameWindow("eg1",cv::WINDOW_AUTOSIZE);
        cv::imshow("eg1",img);
        cv::waitKey(0);
        cv::destroyWindow("eg1");
        cv::Mat�ṹ���������洢�������͵�ͼ��
    ������Ƶ
        #include<opencv2/highgui/highgui.hpp"
        #include<opencv2/imgproc/imgproc.hpp"
        int bar_pos=0;
        cv::Mat frame;
        cv::VideoCapture cap;
        cap.open( ? );      //������Ƶ�ļ�·��
        
        int frames = cap.get(cv::CAP_PROP_FRAME_COUNT); //��ȡ֡��
        int w = cap.get(cv::CAP_PROP_FRAME_WIDTH);
        int h = cap.get(cv::CAP_PROP_FRAME_HEIGHT);
        
        cv::namedWindow("eg3",cv::WINDOW_AUTOSIZE);
        cv::createTrackbar("pos","eg3",&bar_pos,frames,bar_callback);
        
        while(1)
            cap>>frame;     //��ȡ��Ƶ֡
            if(frame.empty()) break;
            cv::imshow("eg3",frame);
            int cur_pos = cap.get(cv::CAP_PROP_POS_FRAMES);
            cv::setTrackbarPos("pos","eg3",cur_pos);
            char c = cv::waitKey(33);
            if(c=='x') break;
        
        void bar_callback(int pos,void*)
            //pos�����϶����λ�ã����Դ˿�����Ƶ���Ž���
            cap.set(cv::CAP_PROP_POS_FRAMES,pos);   //����λ��
    ͼ����
        cv::Mat img1,img2;
        img1 = cv::imread("img�ļ�·��");
        cv::pyrDown(img1,img2);         //��˹ģ���򽵲���
        cv::GaussianBlur(img2,img2,cv::Size(5,5),3,3);    //����blue()��medianBlue()��bilateralFilter()
        cv::cvtColor(img2,img2,cv::COLOR_BGR2GRAY);
        cv::Canny(img2,img2,10,100,3,true);
        cv::Vec3b color = img1.at<cv::Vec3b>(x,y);
        uchar blue = color[0];
        uchar green = color[1];
        uchar red = color[2];
    ¼������ͷ
        cv::VideoCapture cap;
        cap.open( 0 );      //�򿪵�һ������ͷ
        if(cap.isOpened() == false)
            return;
        double fps = cap.get(cv::CAP_PROP_FPS);
        cv::Size size(
            cap.get(cv::CAP_PROP_FRAME_WIDTH),
            cap.get(cv::CAP_PROP_FRAME_HEIGHT));
        cv::VideoWriter writer;
        writer.open("·��",CV_FOURCC('M','J','P','G'),fps,size);
        cv::Mat frame;
        while(1)
            cap >> frame;
            if(frame.empty()) break;
            writer << frame;
            char c = cv::waitKey(10);
            if(c=='x') break;
������ OpenCV�������� 
    OpenCV�Ļ�������������Ҫ�������ࣺ
        ֱ�Ӵ�c++�м̳з�չ�����ͣ���int�����顢���󡢵㡢���ε�
        ���������������ռ�ָ�롢��ֹ�������
        �����������ͣ����ʹ�����cv::Mat
    ������
        cv::Vec<> ģ�������࣬��Ϊ�̶������࣬
            ����stl�е�����������С�����ѹ�벻�ܳ���9�����ݣ�
            ��ΪС��Ҳ�������漰�ĸ���Ч��
            cv::Vec2i,cv::Vec3i,cv::Vec4d�����������ƣ�������typedef cv::Vec<>�����ġ�
            �ṩ��˳�Ա������cross()
        cv::Matx<> ���Ƕ�ά�ľ�����ģ�������࣬��Ϊ�̶������ࡣ
            һ�㴦������ʹ�û�ʹ�ø��࣬������ͼ�����͵�����Ӧ����cv::Mat��
            Ĭ�Ϲ��캯��: cv::Matx33f��3*3��С����cv::Matx43d��
            ����Ԫ��ֵ��ȵľ���all(x)
            ����ȫ�����zeros()
            ����ȫ1����ones()
            ���쵥λ����eye()
            �������ȷֲ��ľ���randu(min,max)
            �������ڷֲ�����nrandn(mean,variance)
            �������㣺m1=m0��m1*m0��m1+m0��m1-m0��m1==m0��m1!=m0��
                      m1*a��a*m1��m1/a��m1.dot(m2)��m1.ddot(m2)��m1.mul(m2)
            �ı������״��reshape<>()
            ��ȡ�Ӿ���: get_minor<>()
            ��ȡ��i�У� row(i)
            ��ȡ��j�У� col(j)
            ��ȡ�Խ��ߣ� diag()
            ת�þ��� t()
            �����inv(method); Ĭ��ֵΪcv::DECOMP_LU
            ������ϵͳ�� solve<>(),solve()
        cv::Point_<>ģ���࣬��������Ҫʹ�õ���cv::Point2i��cv::Point3f�����ı���
            �����ṩ���(dot)�����(cross)���жϵ�ǰ���Ƿ��ھ�����(inside)��
            ��̶�������ת��(cv::Vec3f)�ȳ�Ա������
            ����ֱ����C�ӿ�����CvPoint��CvPoint2D32f����ת����
        cv::Scalar_<>ģ���࣬�����Ǹ���άPoint�࣬�̳�cv::Vec<double,4>������
            �ṩ������ˣ�mul���ȳ�Ա������ͬʱ�̳�cv::Vec<>�ṩ�ķ���
            �������ʽC���Խӿڵ�CvScalar���ɻ�����
        cv::Size,ʵ����cv::Size2i�ı��������⻹��cv::Size2f
            �ṩ��������ĳ�Ա����area()
        cv::Rect,�������;��εı�������¼�����󶥿��
            �ṩ��ȡ���Ͻ�(tl)�����½�(br)���жϵ��Ƿ��ھ�����(contains)�ȳ�Ա������
            ������&,|���������������εĽ����벢����
            ������==,!=������������ж����������Ƿ���ȡ�
            ������+,+=�����������ƽ��/���ž��Ρ�
        cv::RotatedRect�������ײ�û��ʹ��ģ���C++�ӿ���֮һ��
            �Ǹ��������ĵ㡢��С�ͽǶȵȳ�Ա����
            �ṩ��ȡ�ĸ�������ĳ�Ա����potins(pts[4])
        cv::Complexf��������
            .re ��ʵ�����֣�.im �� ��������
            conj() �� �����
    ��������
        cv::TermCriteria ��ຯ����Ҫ�ṩһ����ֹ�����Ծ�����ʱ�˳�
        cv::Range  ȷ��һ���������������У���start��end����Ԫ��
        cv::Ptr ����ָ��,֧��*��->�������
            ʹ�þ����� cv::Ptr<Matx33f> p(new cv::Matx33f);
                       cv::Ptr<Matx33f> p2 = makePtr<cv::Matx33f>();
            ֧��release�����ֶ��ͷ�
            empty()�����жϸ�ָ���Ƿ�ָ��һ���Ѿ��ͷŵ��Ķ����ΪNULL
        cv::Exception �쳣�࣬�̳���std::exception
            ��code��err��func��file��line�ȳ�Ա����
            CV_Error(errorcode��description)�� �� �׳��쳣
            CV_Error_(errorcode��printf_fmt_str, [args]) �꣺����������
            CV_Assert(condition)��CV_DbgAssert(condition)�꣺���������ϣ������쳣
������ ͼ��ʹ�����������
    ����������ϡ������
        �������飬��ζ��ֵΪ0��Ԫ����Ȼռ�ÿռ�
        ϡ�����飬��ζ��ֻΪֵ��Ϊ0��Ԫ�ط���ռ�
        �������д��ڴ���ֵ��Ϊ0��Ԫ��ʱ��ʹ��ϡ�����鷴�����˷ѿռ�
        ���������д���0ֵԪ��ʱ���ʺ�ʹ��ϡ������
    cv::Mat��
        ͼ����԰���ͬά�ȴ洢
            ͼ����԰�һά����洢�����е������������δ���������
            Ҳ���԰���ά����洢�����ذ�����˳��洢��������
            �����԰���ά����洢��ÿ��ͨ��������ռ��һ��ƽ��
        Mat�洢���ݵķ�ʽ��data+step[]
            ���о��󣬶��и�flag��Ա������ʾ�������ͣ�dims��ʾά��
            dataָ��ָ���������ݵĴ洢λ�ã�refcount��ʾ���ü�����
            row/col��ʾ��������ά�ȴ�����άʱ��Ч����
            step[]��������/��/��ɫƽ����ռ���ֽ����Ĵ�С��
            ��һ����ά���飬���i�У���j�����ص�λ��Ϊ��
            mtx.data+mtx.step[0]*i+mtx.step[1]*j,
            step[0]��¼һ��������ռ�ֽ�����step[1]��¼һ��������ռ�ֽ���
        ����Mat����
            ʹ�ò��������Ĺ��캯��
                �������� cv::Mat mat����������������������û�д�С���������͵ģ�
                ֮��ͨ��mat.create(3,3,CV_32FC3);�ﵽ�����ڴ������Ŀ��
                CV_32FC3����ͨ����32λ�������ݣ������Ļ����磺
                CV_{8U,16S,16U,32S,32F,64F}C{1,2,3}��C����������ֱ�ʾͨ������
                ���Ҫ��������3ͨ���ģ�Ӧ��ʹ��CV_{8U,16S,16U,32S,32F,64F}C(x)
                ����xΪͨ���������Ǹ��������磺
                CV_8UC(4)���������ڴ���8λCMYK��ͨ���Ĵ���ɫ������ͼ��
                ��ʵCV_32FC3�ȼ���CV_32FC(3)��������Ϊ#define CV_32FC3 CV_32FC(3)
                ֻ�Ƕ��ڳ���3ͨ���ģ�û����صĺ궨�塣
                ��Щ��/�����ı�����һЩ����ֵ�������������ʽ��Ҳ������cv::DateType<>
                ģ���type��Աֵ���磺cv::DataType<cv::Complexf>::type
            ���ι��캯��
                ���ι��캯��������20�����������õĿ���ֻ�����еļ���
                cv::Mat(int rows,int cols,int type);
                cv::Mat(int rows,int cols,int type,const Scalar&s); 
                cv::Mat(cv::Size sz,int type);
                cv::Mat(cv::Size sz,int type,const Scalar&s); //s�������ڳ�ʼ��Ԫ��ֵ
                cv::Mat(cv::Size sz,int type,void *data,size_t step=AUTO_STEP); //Mat��ʹ��data����
                cv::Mat(const Mat& mat);
                cv::Mat(const Mat& mat,const cv::Range& rows,const cv::Range& cols); //����ָ������
                cv::Mat(const Mat& mat,const cv::Rect& roi);
                cv::Mat(const cv:MatExpr& expr);    //��������ʽ����
                �Ӿɵ�cvMat��IplImage����cv::Mat
                    cv::Mat(const CvMat* old,bool copyData=false);
                    cv::Mat(const IplImage *old,bool copyData=false);
                ����Ϊģ����ʽ�Ĺ��캯��
                    cv::Mat(const cv::Vec<T,n>& vec,bool copyData=true);
                    cv::Mat(const cv::Matx<T,m,n> &vec,bool copyData=true);
                    cv::Mat(const std::vector<T>& vec,bool copyData=true);
                �����������ڴ�����άͼ��ģ�������ͼ��
            ����cv::Mat�ľ�̬����
                cv::Mat::zeros(rows,cols,type);
                cv::Mat::ones(rows,cols,type);  //ֻ���õ�1ͨ��������ͨ����Ϊ0
                cv::Mat::eye(rows,cols,type);   //ֻ���õ�1ͨ��������ͨ����Ϊ0
        ��ȡԪ��
            ͨ��λ�÷���
                ģ�庯��at<>() : ��ȡ��������
                    �磺cv::Vec2f vec = mat.at<cv::Vec2f>(3,3);
                    Ȼ��ʹ��vec[2]�õ���2��ͨ���ϵ����أ�
                    Ҳ����ֱ��дΪmat.at<cv::Vec2f>(3,3)[2];
                ģ�庯��Ptr<>() �� ��ȡĳ��
                    �磺cv::Vec2f *pvec = mat.at<cv::Vec2f>(3);
                ֱ�Ӳ�������ָ��data
                    ��һ����ά���飬���i�У���j�����ص�λ��Ϊ��
                    mtx.data+mtx.step[0]*i+mtx.step[1]*j
                    ���ַ�����Ϊԭʼ��ֱ�ӣ�Ч����죬�����Ƽ�
                Mat�����������˵��
                    ��Ա����isContinuous()�����������Ƿ��������ģ�
                    �������Ԫ����ÿ��ĩβ�����洢��û�м�϶���򷽷�����true�� 
                    ����������false�� ��Ȼ������1x1��1xN�������������ġ�
                    һ����Mat :: create�����ľ������������ġ� 
                    ���ǣ����ʹ��Mat :: col��Mat :: diag����ȡ�����һ���֣�
                    ����Ϊ�ⲿ��������ݹ������ͷ������������ܲ��پ��д����ԡ�
            ʹ�õ���������
                cv::MatConstIterator<>��cv::MatIterator<>
                ʹ�õ�����ָ�룬���Բ������Mat�ڲ������ڴ��Ƿ��������ģ����ʹ�������ǳ�����
            ͨ�����������Ԫ��
                ͨ��Mat�ĳ�Ա���������Ի�ȡ��mat��һ���Ӽ�����ĳһ�С�ĳһ�С�ĳ���Ӿ����
                    m2=m1.row(i);
                    m2=m1.col(j);
                    m2=m1.rowRange(i0,i1);
                    m2=m1.colRange(j0,j1);
                    m2=m1.rowRange(cv::Range(i0,i1));
                    m2=m1.colRange(cv::Range(j0,j1));
                    m2=m1.diag(d);  //�Խ��ߣ����Ϊ����������ƫ�ƣ�Ϊ����������ƫ��
                    m2=m1(cv::Range(i0,i1),cv::Range(j0,j1));  �Ӿ���
                    m2=m1(cv::Rect(i0,i1,w,h));
                    m2=m1(ranges);
                    ��Ҫ˵�����ǣ�ͨ�����ַ�ʽ�õ���Mat����data��ԭMatָ�������һ�£�
                    ��ֻ�Ǳ���ͼ��������Ϣ������Ϊ�˸���ĸ��ƣ���m2ͼ��ĸ��Ļ�Ӱ��m
        Mat�������������
            m2=m1 ����ʱ���������ݿ�����m2�൱�ڶ�m1��һ������
            m2=m1+m0 : ��������ָ��ָ��m2,�������һ���µ��ڴ���
            �������㣺
                m0+m1,m0-m1
                m0+s; m0-s; s+m0; s-m0; ����͵���Ԫ�صļӼ�
                s*m0; m0*s;
                m0*m1       �����˷�
                m0.mul(m1); Ԫ�ؼ����
                m0/m1;      Ԫ�ؼ����
                m0.inv(method)
                m0.t()
                m0>m1; m0>=m1; m0==m1; m0<=m1; m0<m1;  ��Ԫ�رȽϣ�����Ԫ��ֵΪ0/255��uchar����
                m0&m1; m0|m1; m0^m1; ~m0; Ԫ��ֱ�Ӱ�λ���������ص�Ҳ�Ǿ���
                m0&s; m0|s; m0^s; s&m0; s|m0; s^m0;
                min(m0,m1); max(m0,m1); min(m0,s); max(m0,s); min(s,m0); max(s,m0);
                cv::abs(m0);
                m0.cross(m1); m0.dot(m1);  ��ˣ����ж�Ӧ��˵ĺͣ����ˣ���ӦԪ����ˣ�
                ���־���˷��ĶԱȣ�
                    dot
                        Mat�����dot������չ��һά�����ĵ�˲�����
                        ������Mat������չ��һ���У��У�������
                        ֮��ִ�������ĵ�����㣬
                        ��ȻҪ�����dot���������Mat�������������ȫһ��
                        ����ֵΪdouble����
                    mul
                        Ԫ�ض�Ӧ��ˣ����ص����Ǿ���
                    *
                        ���������Ĳ��
                    cross
                        �÷�����������3Ԫ��vector�Ĳ�ˣ�vector����Ϊ3Ԫ�صĸ������͡�
                ����ת��
                    �����㷢�����ʱ�����Զ���飬�������ֵתΪ���/��Сֵ��
        Mat��ĸ��ຯ����Ա
            m1=m0.clone(); 
            m0.copyTo(m1); 
            m0.copyTo(m1,mask);  ֻ����mask��ָʾ������
            m0.convertTo(m1,type,scale,offset);
            m0.setTo(s,mask);  ����m0����Ԫ��Ϊs,�������mask����ֻ��mask������в���
            m0.push_back(s);  ��ĩβ����һ��m*1��С������
            m0.push_back(m1);  m*n����m0��k*n����m1�������ߺϲ��󣬷ŵ�m1��
            m-.pop_back(d);   ��m*n��С�ľ������Ƴ�d�У�Ĭ����1��
            m0.locateROI(size,offset);  ��m0�ĳߴ�д�뵽cv::Size�ͱ���size�У�
                                        ���m0��һ��������е�һ������
                                        �򻹻�д��һ��Point���͵�offset
            m0.adjustROI(t,b,l,r);  ͨ���ĸ�ֵ������ROI��Χ
            m0.total();  ������������Ԫ�ص���Ŀ��ͬһͨ���ڵ���һ��Ԫ�أ�
            m0.isContinuous();  m0����֮����û�п�϶
            m0.elemSize()  ����m0��λ���ȣ�����ͨ�����㣬����12
            m0.elemSize1()  ����m0�����Ԫ�ص�λ���ȣ�����ͨ�����㣬����4
            m0.type()   ����m0Ԫ�ص����ͣ���CV_32FC3
            m0.depth()  ����m0ͨ���е�Ԫ�����ͣ���CV_32F
            m0.channels()  ����m0ͨ����Ŀ
            m0.empty()  ����Ϊ��ʱ����true����m0.total==0��m.data==NULL
    cv::SparseMat��
        ϡ������������з�0Ԫ�طǳ��ٵ�ʱ��ʹ��
        ϡ�����һ����˵�����ٶȶ�����
        ϡ�����ĺ����ܶ඼�����ڳ��ܾ���Mat
        ϡ�����ʹ�ù�ϣ�����洢��0Ԫ��(��Ԫ���ڼ�����Ϊ0���Իᱻ�洢)
        ����ϡ�������е�Ԫ��
            ���ַ��ʻ��ƣ�
                cv::SparseMat::ptr()
                    uchar *cv::SparseMat::ptr(int i0,bool createMissing,size* hashval=0);
                        ���ڷ���һά���飬��һ��������Ԫ��������
                        �ڶ���������Ԫ��ʵ�ֲ�������������ʱ���Ƿ񱻴���
                cv::SparseMat::ref()
                cv::SparseMat::value()
                cv::SparseMat::find()
                        
                