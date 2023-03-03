/**
* 特点：
*   支持多线程
*   支持通过level控制日志的输出级别
*   可方便的在控制台输出或存文件两种方式之间切换
*   可选择在要输出的每条日志信息之前添加日志时间、日志等级、所在函数名等信息
* 使用方法：
*   通常应该使用如下宏来完成日志方法调用，
*   除非你熟悉该工具类的代码，否则不建议直接调用日志类中的函数
*   如果是Release版，日志默认不会添加所在函数名，要使其带函数名信息，
*   只需在pro文件中添加 DEFINES+=QT_MESSAGELOGCONTEXT，并重新编译即可
* 1.mylog_ctrl ：
*   该宏接受两个参数，
*   第一个参数为枚举类型，具体值参看枚举类MyControlType的定义
*   第二个参数为variant类型，具体传入的类型应根据第一个参数的值相匹配
*   通过该方法修改的控制项，均以静态变量保存，在整个项目中（而不是当前文件或当前类中）有效
*   如果没有修改过任何控制项，则所有控制项均有其默认值，具体参看枚举类MyControlType的定义
* 2.mylog(LEVEL) ：
*   mylog(LEVEL)与qDebug()用法一样，但可以指定LEVEL值，unsigned short类型，
*   如果LEVEL值小于“最小输出日志等级”，或大于“最大输出日志等级”，则该条日志不会输出
*   mylog(LEVEL)使用方法如：mylog(1)<<"xxxx";
* 3.mylogf(LEVEL) ：
*   mylogf(LEVEL)的用法与mylog(LEVEL)一样，都支持通过<<输出日志信息，
*   但功能有所增强，mylogf(LEVEL)一般放在函数的开始位置，
*   它会在要输出的日志信息前追加">>>>"字符串，表明进入函数，
*   而在函数退出时，自动输出"<<<<"字符串，表明函数成功退出。
*   mylogf(LEVEL)使用方法如：mylogf(1)<<"param : xxxx";
*   mylogf(LEVEL)也可以不加任何输出信息，如mylogf(1);
*   此时，该宏将在进入函数时，输出">>>>"，函数退出时，输入"<<<<"。
* 4.mylog0/mylogf0 ：
*   mylog0  等价于 mylog(0)
*   mylogf0 等价于 mylogf(0)
**/

///宏方法：
#define ENABLE_MYLOG 0
#if ENABLE_MYLOG
#define mylog_ctrl    MyMessageLogger::setControl
#define mylog0        MyMessageLogger::qdebug(0,QT_MESSAGELOG_FUNC)
#define mylog(LEVEL)  MyMessageLogger::qdebug(LEVEL,QT_MESSAGELOG_FUNC)
#define mylogf0       MyAutoFuncLog autofunclog__(0,QT_MESSAGELOG_FUNC); autofunclog__<<""
#define mylogf(LEVEL) MyAutoFuncLog autofunclog__(LEVEL,QT_MESSAGELOG_FUNC); autofunclog__<<""
#else
#define NUTHING
#define mylog_ctrl(...)
#define mylog0        if(0) MyFakeLogger::qdebug()
#define mylog(LEVEL)  if(0) MyFakeLogger::qdebug()
#define mylogf0       if(0) MyFakeLogger::qdebug()
#define mylogf(LEVEL) if(0) MyFakeLogger::qdebug()
#endif

#ifndef MYMESSAGELOGGER_H
#define MYMESSAGELOGGER_H

#include <QDebug>
#include <QFile>

enum MyControlType{
    set_log_level_min,  //设置最小输出日志等级，低于该阈值的日志不会输出，对应数据类型为unsigned short，默认值为0
    set_log_level_max,  //设置最大输出日志等级，高于该阈值的日志不会输出，对应数据类型为unsigned short，默认值为65535
    set_log_path,       //设置日志文件路径，当不是一个有效路径时，日志在控制台输出，对应数据类型为string，默认值为空
    set_show_date,      //在每条日志前添加日期信息，对应数据类型为bool，默认值为true
    set_show_time,      //在每条日志前添加时间信息，对应数据类型为bool，默认值为true
    set_show_log_level, //在每条日志前添加当前日志等级信息，对应数据类型为bool，默认值为true
    set_show_func_name, //在每条日志前添加日志所在函数名信息，对应数据类型为bool，默认值为true
    set_all_default     //将上面所有的值设为默认值
};

class MyMessageLogger
{
public:
    friend class MyAutoFuncLog;
    static bool setControl(MyControlType t,QVariant v);
    static MyMessageLogger qdebug(ushort level=0,const QString& funcname="");
    template <typename T> MyMessageLogger &operator<<(const T& t) {
        if(_log_level<_min_valid_log_level || _log_level>_max_valid_log_level) return *this;
        if(_qdebug) {*_qdebug<<t; _has_output=true;} return *this;
    }
    ~MyMessageLogger() {
        if(_qdebug) {
            if(_file->isOpen() && _has_output) (*_qdebug)<<"\n";
            delete _qdebug;
        }
    }
private:
    QDebug *_qdebug{nullptr};
    ushort _log_level{0};
    bool _has_output{false};
    static QFile *_file;
    static QString _context;
    static bool _show_date,_show_time,_show_log_level,_show_func_name;
    static ushort _min_valid_log_level,_max_valid_log_level;
private:
    static struct AutoDelete
    {
        ~AutoDelete(){ if(_file){_file->close(); delete _file;} }
    } _auto_delete;
};

class MyAutoFuncLog
{
public:
    MyAutoFuncLog(ushort level=0,const QString &func_name="")
    {
        _s1 = ">>>>";
        _s2 = "<<<<";
        _level = level;
        _func_name = func_name;
    }
    ~MyAutoFuncLog()
    {
        MyMessageLogger::qdebug(_level,_func_name)<<qPrintable(_s2);
    }
    /*
     * 该运算符函数用以完成函数进入日志的真实输出
     * s参数用以指定函数进入及退出标记，
     * 有效的s通过|分隔为两段，如">>>>|<<<<"
     * 通常应使用mylogf宏，而不是直接调用该函数
     */
    MyMessageLogger operator<<(const QString& s);
private:
    ushort _level;
    QString _func_name;
    QString _s1,_s2;
};

class MyFakeLogger
{
public:
    static MyFakeLogger qdebug() { MyFakeLogger log; return log; }
    template <typename T> MyFakeLogger &operator<<(const T& t) { (t); return *this; }
};
#endif // MYMESSAGELOGGER_H
