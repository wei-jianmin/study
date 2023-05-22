#include <QCoreApplication>
#include <QFile>
#include <QTextStream>
#include <QTextCodec>
#include <QFileInfo>
#include <stdio.h>

int max_line = 60;

int TestPreSpaceCount(const char* ba)
{
    for(int i=0;i<strlen(ba);i++)
    {
        if(ba[i]!=' ')
            return i;
    }
    return 0;
}
bool NotBlankLine(const char* ba)
{
    for(int i=0;i<strlen(ba);i++)
    {
        if(ba[i]>=33 && ba[i]<=126)
            return true;
    }
    return false;
}

const char* FirstVisibleChar(const char* ba)
{
    const char* p = ba;
    while((p[0]<33 || p[0]>126))
        p++;
    return p;
}

bool BeginWithNum(const char* ba)
{
    bool yes = false;
    const char* p = ba;
    while((p[0]<33 || p[0]>126))
        p++;
    if(p[0]>='0' && p[0]<='9')
    {
        for(int i=0;i<=6;i++)
        {
            if(p[i]<'0' || p[i]>'9')  //如果不是数字
            {
                if(p[i]!=' ' || p[i]!='\t' || p[i]!='.')
                    return true;
                else
                    return false;
            }
        }
    }
    return false;
    }

void DealwithFile(QString filename)
{
    printf("请设置待处理文件的最大行宽，该值应略小于待处理文件的实际最大行宽（默认值为60）：\n");
    char buf[10]= {0};
    scanf("%d",buf);
    int l = atoi(buf);
    if(l>1)
        max_line = l;
    printf("设置行宽为 %d\n",max_line);

    QFileInfo qfi(filename);
    QString filename2 = qfi.absolutePath() + qfi.baseName() + "_2." + qfi.suffix();
    std::string sf2 = filename2.toStdString();
    FILE * pf = fopen(sf2.c_str(),"w");
    if(!pf)
    {
        printf("写打开 %s 失败\n",sf2.c_str());
        return;
    }
    else
    {
        printf("处理后的文件保存为 %s\n",sf2.c_str());
    }
    QTextStream stm(pf,QIODevice::WriteOnly);
    //stm.setCodec(QTextCodec::codecForName("utf-8"));
    QFile qf(filename);
    qf.open(QIODevice::ReadOnly);
    char ba[512]={0};
    int ident = 0;
    int last_line_len = 0;
    bool last_line_begin_with_num = false;
    int lineno=0;
    while( 0<=qf.readLine(ba,510))
    {
        lineno++;
        if(ba[strlen(ba)-1]=='\n')
            ba[strlen(ba)-1] = '\0';
        if(ba[strlen(ba)-1]=='\r')
            ba[strlen(ba)-1] = '\0';
        ba[strlen(ba)]=' ';     //去掉末尾的换行符，并在末尾添加空格

        if(NotBlankLine(ba))   //本行不为空
        {
            bool begin_with_num = BeginWithNum(ba);
            int ident_ = TestPreSpaceCount(ba);   //该行前面的空格数
            int line_len = strlen(ba);
            if( last_line_len > max_line &&
                ident_ >= ident &&
                !(ident==ident_ && last_line_begin_with_num==true && begin_with_num==true)
              )
            {
                stm << FirstVisibleChar(ba);
            }
            else
            {
                stm << "\n" << ba;
            }

            ident = ident_;
            last_line_begin_with_num = begin_with_num;
            last_line_len = line_len;
        }
        else  //本行为空
        {
            stm << "\n";
            ident = 0;
            last_line_len = 0;
            last_line_begin_with_num = false;
        }
    }
    qf.close();
    if(pf)
        fclose(pf);
}

int main(int argc, char *argv[])
{
    //QCoreApplication a(argc, argv);
    do
    {
        QFile qf;
        QString filename;
        if(argc<2)
        {
            puts("功能： 将man命令存成的文件，段落中不必要的断行去掉\n");
            puts("请指定一个文件名作为参数（按回车键继续）：");
            char buf[1024];
            gets(buf);
            for(int i=0;i<strlen(buf);i++)
            {
                if(buf[i]=='\\')
                    buf[i]='/';
            }
            filename = buf;
        }
        else
            filename = argv[1];
        if( !QFile::exists(filename))
        {
            printf("文件不存在：%s\n",filename.toStdString().c_str());
            break;
        }
        qf.setFileName(filename);
        if(!qf.open(QIODevice::ReadOnly))
        {
            puts("打开文件失败");
            break;
        }
        qf.close();
        DealwithFile(filename);
    }while(false);
    puts("处理完成，回车键退出");
    getchar();
    return 0;
    //return a.exec();
}
