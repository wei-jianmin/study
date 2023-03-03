/* 
 * 说明： 
 * 使用qdebug(int level=0)，取代原来的qDebug() 
 * 只有当level处于MY_MIN_DEBUG_LEVEL~MY_MAX_DEBUG_LEVEL之间时才将日志信息输出
 * 使用qtrace(int level=0), 在qdebug的基础上，自动添加所在函数的名字
 */
#ifndef MYQDEBUG_H
#define MYQDEBUG_H

#include <QDebug>

#ifndef MY_MIN_DEBUG_LEVEL
#define MY_MIN_DEBUG_LEVEL 0
#endif
#ifndef MY_MAX_DEBUG_LEVEL
#define MY_MAX_DEBUG_LEVEL 1000
#endif

class MyQDebug
{
public:
    MyQDebug(int level=0) { _level = level; _debug = NULL; }
    ~MyQDebug() { if(_debug) delete _debug; }	//当析构时，才将日志输出
    template <typename T>
    MyQDebug & operator <<(T t)
    {
        if(_level>=MY_MIN_DEBUG_LEVEL && _level<=MY_MAX_DEBUG_LEVEL)
        {
            if(_debug==NULL)
            {
                _debug = new QDebug(QtDebugMsg);
                (*_debug) << "[level" << _level << "] ";
            }
            (*_debug)<<t;
        }
        return *this;
    }
private:
    int _level;
    QDebug *_debug;
};

//qSetMessagePattern("%{appname} %{type} %{time [yyyy-MM-dd hh:mm:ss]} %{file} %{line} %{function} %{message}");


//inline MyQDebug qdebug(unsigned int level=0) { return MyQDebug(level); }
inline MyQDebug qdebug(unsigned int level=0,const char* fcname=NULL) { MyQDebug db(level); if(fcname)db<<"["<<fcname<<"]"; return db; }

#ifndef qtrace
#define qtrace(LEVEL) qdebug(LEVEL,__FUNCTION__)
#endif

#endif // MYQDEBUG_H
