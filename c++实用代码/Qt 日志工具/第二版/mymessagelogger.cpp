#include "mymessagelogger.h"
#include <QDateTime>

QString MyMessageLogger::_context = "";
bool MyMessageLogger::_show_date = true;
bool MyMessageLogger::_show_time = true;
bool MyMessageLogger::_show_log_level = true;
bool MyMessageLogger::_show_func_name = true;
ushort MyMessageLogger::_min_valid_log_level = 0;
ushort MyMessageLogger::_max_valid_log_level = 65535;
QFile* MyMessageLogger::_file = new QFile;
MyMessageLogger::AutoDelete MyMessageLogger::_auto_delete;

bool MyMessageLogger::setControl(MyControlType t, QVariant v)
{
    if(t == set_all_default)
    {
        _show_date = true;
        _show_time = true;
        _show_log_level = true;
        _show_func_name = true;
        _min_valid_log_level = 0;
        _max_valid_log_level = 65535;
        _file->setFileName("");
        _file->close();
        return true;
    }
    if(v.type() == QVariant::Bool)
    {
        switch (t) {
        case set_show_func_name:
            _show_func_name = v.toBool();
            break;
        case set_show_log_level:
            _show_log_level = v.toBool();
            break;
        case set_show_time:
            _show_time = v.toBool();
            break;
        case set_show_date:
            _show_date = v.toBool();
            break;
        default:
            return false;
        }
        return true;
    }
    else if(v.type() == QVariant::Int)
    {
        int i = v.toInt();
        if(i<0 || i>65535)  return false;
        switch (t) {
        case set_log_level_min:
            _min_valid_log_level = i;
            break;
        case set_log_level_max:
            _max_valid_log_level = i;
            break;
        default:
            return false;
        }
        return true;
    }
    else if(v.type() == QVariant::String)
    {
        if(t != set_log_path) return false;
        if(_file->isOpen()) _file->close();
        QRegExp reg(R"(^[A-Za-z]\:([\\\/][^/\:*?"|<>\n]+)+$)");
        QString log_path_name = v.toString();
        if(log_path_name.length()>0 && reg.exactMatch(log_path_name))
        {
            _file->setFileName(log_path_name);
            _file->open(QIODevice::WriteOnly | QIODevice::Append);
            return true;
        }
        return false;
    }
    else
        return false;
}

MyMessageLogger MyMessageLogger::qdebug(ushort level,const QString& funcname)
{
    MyMessageLogger dbg;
    if(level<_min_valid_log_level || level>_max_valid_log_level)
        return dbg;
    if(_file->isOpen())
        dbg._qdebug = new QDebug(_file);
    else
        dbg._qdebug = new QDebug(QtDebugMsg);
    dbg._qdebug->setAutoInsertSpaces(false);
    dbg._log_level = level;
    if(_show_date || _show_time)
    {
        QDateTime date_time = QDateTime::currentDateTime();
        if(_show_date && _show_time)
            *(dbg._qdebug) << qPrintable(date_time.toString("[yyyy-MM-dd hh:mm:ss.zzz] "));
        else if(_show_date)
            *(dbg._qdebug) << qPrintable(date_time.toString("[yyyy-MM-dd] "));
        else if(_show_time)
            *(dbg._qdebug) << qPrintable(date_time.toString("[hh:mm:ss.zzz] "));
        dbg._has_output = true;
    }
    if(_show_log_level)
    {
        char buf[15]={0};
        sprintf(buf,"[%05d] ",level);
        *(dbg._qdebug)<<buf;
        dbg._has_output = true;
    }
    if(_show_func_name && funcname.length()>0)
    {
        *(dbg._qdebug) << "[" << qPrintable(funcname.section(' ',1,1).section('(',0,0)) <<"] ";
        dbg._has_output = true;
    }
    return dbg;
}

MyMessageLogger MyAutoFuncLog::operator<<(const QString& s)
{
    MyMessageLogger dbg;
    dbg._log_level = _level;
    if(_level<dbg._min_valid_log_level || _level>dbg._max_valid_log_level)
        return dbg;
    if(s.length()>1 && s.split('|').count()==2)
    {
        _s1 = s.section(' ',0,0);
        _s2 = s.section(' ',1,1);
    }
    if(dbg._file->isOpen())
        dbg._qdebug = new QDebug(dbg._file);
    else
        dbg._qdebug = new QDebug(QtDebugMsg);
    dbg._qdebug->setAutoInsertSpaces(false);
    if(MyMessageLogger::_show_date || MyMessageLogger::_show_time)
    {
        QDateTime date_time = QDateTime::currentDateTime();
        if(MyMessageLogger::_show_date && MyMessageLogger::_show_time)
            *(dbg._qdebug) << qPrintable(date_time.toString("[yyyy-MM-dd hh:mm:ss.zzz] "));
        else if(MyMessageLogger::_show_date)
            *(dbg._qdebug) << qPrintable(date_time.toString("[yyyy-MM-dd] "));
        else if(MyMessageLogger::_show_time)
            *(dbg._qdebug) << qPrintable(date_time.toString("[hh:mm:ss.zzz] "));
        dbg._has_output = true;
    }
    if(MyMessageLogger::_show_log_level)
    {
        char buf[15]={0};
        sprintf(buf,"[%05d]",_level);
        *(dbg._qdebug)<<buf;
        dbg._has_output = true;
    }
    if(MyMessageLogger::_show_func_name && _func_name.length()>0)
    {
        *(dbg._qdebug) << " [" << qPrintable(_func_name.section(' ',1,1).section('(',0,0)) <<"] "<<qPrintable(_s1)<<" ";
        dbg._has_output = true;
    }
    return dbg;
}
