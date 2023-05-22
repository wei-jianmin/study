#include "mymessagelogger.h"
#include <QDateTime>

QString MyMessageLogger::_context = "";
ushort MyMessageLogger::_min_valid_log_level = 65535;
ushort MyMessageLogger::_max_valid_log_level = 0;
QFile* MyMessageLogger::_file = new QFile;
MyMessageLogger::AutoDelete MyMessageLogger::_auto_delete;

void MyMessageLogger::init(ushort min_valid_log_level,ushort max_valid_log_level,const QString& log_path_name)
{
    _min_valid_log_level = min_valid_log_level;
    _max_valid_log_level = max_valid_log_level;
    QRegExp reg(R"(^[A-Za-z]\:([\\\/][^/\:*?"|<>\n]+)+$)");
    if(log_path_name.length()>0 && reg.exactMatch(log_path_name))
    {
        if(_file->isOpen()) _file->close();
        _file->setFileName(log_path_name);
        _file->open(QIODevice::WriteOnly | QIODevice::Append);
    }
}


MyMessageLogger MyMessageLogger::qdebug(ushort level,const QString& funcname)
{
    MyMessageLogger dbg;
    if(_file->isOpen())
        dbg._qdebug = new QDebug(_file);
    else
        dbg._qdebug = new QDebug(QtDebugMsg);
    dbg._qdebug->setAutoInsertSpaces(false);
    dbg._log_level = level;
    if(level>=_min_valid_log_level && level<=_max_valid_log_level && funcname.length()>0)
    {
        *(dbg._qdebug) << qPrintable(QDateTime::currentDateTime().toString("[yyyy-MM-dd hh:mm:ss.zzz]"))
                       << " [" << qPrintable(funcname.section(' ',1,1).section('(',0,0)) <<"] ";
        dbg._has_output = true;
    }
    return dbg;
}

MyMessageLogger AutoFuncLog::operator<<(const QString& s)
{
    if(s.length()>1 && s.split('|').count()==2)
    {
        _s1 = s.section(' ',0,0);
        _s2 = s.section(' ',1,1);
    }
    MyMessageLogger dbg;
    if(dbg._file->isOpen())
        dbg._qdebug = new QDebug(dbg._file);
    else
        dbg._qdebug = new QDebug(QtDebugMsg);
    dbg._qdebug->setAutoInsertSpaces(false);
    dbg._log_level = _level;
    if(_level>=dbg._min_valid_log_level && _level<=dbg._max_valid_log_level && _func_name.length()>0)
    {
        *(dbg._qdebug) << qPrintable(QDateTime::currentDateTime().toString("[yyyy-MM-dd hh:mm:ss.zzz]"))
                       << " [" << qPrintable(_func_name.section(' ',1,1).section('(',0,0)) <<"] "<<qPrintable(_s1)<<" ";
        dbg._has_output = true;
    }
    return dbg;
}
