/**
* 特点：
*   支持多线程
*   支持通过level控制日志的输出级别
*   可方便的在控制台输出或存文件两种方式之间切换
*   自动在要输出的每条日志信息之前添加日志时间和所在函数名
* 使用方法：
*   通常应该使用如下宏来完成日志方法调用，
*   除非你熟悉该工具类的代码，否则不建议直接调用日志类中的函数
*   如果是Release版，日志默认不会添加所在函数名，要使其带函数名信息，
*   只需在pro文件中添加 DEFINES+=QT_MESSAGELOGCONTEXT，并重新编译即可
* 1.mylog_init ：
*   该宏接受三个参数，
*   第一个参数为最小输出日志等级(默认值为0)，低于该等级的日志不会输出
*   第二个参数为最大输出日志等级(默认值为65535)，高于该等级的日志不会输出
*   第三个是日志文件的名字(默认值为空)，为绝对路径，如为无效路径，则在控制台输出日志信息
*   日志等级参数的数据类型为无符号short，如果没有调用过mylog_init方法，
*   则初始化最小输出日志等级为65535，最大输出日志等级为0，这意味着所有的日志都不会被输出
*   mylog_init因为修改的是静态成员，所以在整个工程中只调用一次即可
*   mylog_init(...)使用方法如：
*   mylog_init();                   //控制台输出，输出日志等级最小为0，最大65535
*   mylog_init(3);                  //控制台输出，输出日志等级最小为3，最大65535
*   mylog_init(100,999);            //控制台输出，输出日志等级最小为100，最大999
*   mylog_init(3,3,"D:/123.log");   //日志输出到文件，输出日志等级最小为3，最大3
* 2.mylog(LEVEL) ：
*   mylog(LEVEL)与qDebug()用法一样，但可以指定LEVEL值，无符号short类型，
*   如果LEVEL值小于mylog_init时设置的“最小输出日志等级”，则该条日志不会输出
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
#define mylog_init    MyMessageLogger::init
#define mylog0        MyMessageLogger::qdebug(0,QT_MESSAGELOG_FUNC)
#define mylog(LEVEL)  MyMessageLogger::qdebug(LEVEL,QT_MESSAGELOG_FUNC)
#define mylogf0       AutoFuncLog autofunclog__(0,QT_MESSAGELOG_FUNC); autofunclog__<<""
#define mylogf(LEVEL) AutoFuncLog autofunclog__(LEVEL,QT_MESSAGELOG_FUNC); autofunclog__<<""

#ifndef MYMESSAGELOGGER_H
#define MYMESSAGELOGGER_H

#include <QDebug>
#include <QFile>

class MyMessageLogger
{
public:
    friend class AutoFuncLog;
    static void init(ushort min_valid_log_level=0,ushort max_valid_log_level=65535,const QString& log_path_name="");
    static MyMessageLogger qdebug(ushort level=0,const QString& funcname="");
    template <typename T> MyMessageLogger &operator<<(T t) {
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
    static ushort _min_valid_log_level,_max_valid_log_level;
private:
    static struct AutoDelete
    {
        ~AutoDelete(){ if(_file){_file->close(); delete _file;} }
    } _auto_delete;
};

class AutoFuncLog
{
public:
    AutoFuncLog(ushort level=0,const QString &func_name="")
    {
        _s1 = ">>>>";
        _s2 = "<<<<";
        _level = level;
        _func_name = func_name;
    }
    ~AutoFuncLog()
    {
        MyMessageLogger::qdebug(_level,_func_name)<<qPrintable(_s2)<<"\n\n";
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

#endif // MYMESSAGELOGGER_H
