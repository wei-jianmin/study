/*
使用说明及注意事项：
● 只支持多字节编译模式
● 请尽量调用宏，而不是直接调用类的成员方法
● 静态写日志方法与非静态写日志方法不要在同一段时间内对同一个日志文件进行操作
● 如果使用带前缀功能的宏（宏中有FIX），请注意配合SET_LOGPREFIX、UNSET_LOGPREFIX宏使用
● 所有的宏都有2中版本，他们的名字基本一致，区别是：末尾带下划线的宏，使用时，句尾无需再加分号
● #pragma once、#pragma (end)region是VS特有的关键字，如果编译器不支持，可将其直接去掉
*/
#pragma once
#include <fstream>
//===============================================================
#define _SILENT
//===============================================================
#pragma region 消息框宏:msgbox(s)
#ifndef msgbox
#define msgbox(s) ::MessageBox(NULL,s,"caption",MB_OK)
#endif
#pragma endregion
#ifndef SETPATH
#define SETPATH(s,...) m_log.resetpath(s,__VA_ARGS__)
#endif
#pragma region 基本调用:WRITELOG(s)、WRITELOGX(s,...)
#ifndef WRITELOG
#define WRITELOG(s) m_log.writelog(s)
#endif
#ifndef WRITELOGX
#define WRITELOGX(s,...) m_log.writelogx(s,__VA_ARGS__)
#endif
#pragma endregion
#pragma region 加前缀的：SET_LOGPREFIX(s)、UNSET_LOGPREFIX、FIX_WRITELOG(s)、FIX_WRITELOGX(s,...)
#ifndef SET_LOGPREFIX
#define SET_LOGPREFIX(s) char* strLogPreFix=s
#endif
#ifndef UNSET_LOGPREFIX
#define UNSET_LOGPREFIX CSimpleLog::str_prefix=NULL
#endif
#ifndef FIX_WRITELOG
#define FIX_WRITELOG(s)  CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		m_log.writelog(s)
#endif
#ifndef FIX_WRITELOGX
#define FIX_WRITELOGX(s,...) CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		m_log.writelogx(s,__VA_ARGS__)
#endif
#pragma endregion
#pragma region 通过this指针调用：THIS_WRITELOG(s)、THIS_WRITELOGX(s,...)
#ifndef THIS_WRITELOG
#define THIS_WRITELOG(s) pThis->m_log.writelog(s)
#endif
#ifndef THIS_WRITELOGX
#define THIS_WRITELOGX(s,...) pThis->m_log.writelogx(s,__VA_ARGS__)
#endif
#pragma endregion
#pragma region 通过this指针调用加前缀的：THIS_FIX_WRITELOG(s)、THIS_FIX_WRITELOGX(s,...)
#ifndef THIS_FIX_WRITELOG
#define THIS_FIX_WRITELOG(s) CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		pThis->m_log.writelog(s)
#endif
#ifndef THIS_FIX_WRITELOGX
#define THIS_FIX_WRITELOGX(s,...) CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		pThis->m_log.writelogx(s,__VA_ARGS__)
#endif
#pragma endregion
#pragma region 调用静态函数：S_WRITELOG(f,s)、S_WRITELOGX(f,s,...)、S_CLEARLOG(f)、S_CLRLOG(f)
#ifndef S_WRITELOG
#define S_WRITELOG(f,s) CSimpleLog::write(f,s)
#endif
#ifndef S_WRITELOGX
#define S_WRITELOGX(f,s,...) CSimpleLog::writex(f,s,__VA_ARGS__)
#endif
#ifndef S_CLEARLOG
#define  S_CLEARLOG(f) CSimpleLog::clear(f)
#endif
#ifndef S_CLRLOG
#define S_CLRLOG(f) CSimpleLog::clear(f)
#endif
#pragma endregion
#pragma region 静态加前缀的：S_FIX_WRITELOG(f,s)、S_FIX_WRITELOGX(f,s,...)
#ifndef S_FIX_WRITELOG
#define S_FIX_WRITELOG(f,s)  CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		CSimpleLog::write(f,s)
#endif
#ifndef S_FIX_WRITELOGX
#define S_FIX_WRITELOGX(f,s,...) CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		CSimpleLog::writex(f,s,__VA_ARGS__)
#endif
#pragma endregion
//===============================================================
#pragma region 句尾带分号的对应宏
#ifndef msgbox_
#define msgbox_(s) MessageBox(NULL,s,"caption",MB_OK);
#endif
#ifndef WRITELOG_
#define WRITELOG_(s) m_log.writelog(s);
#endif
#ifndef WRITELOGX_
#define WRITELOGX_(s,...) m_log.writelogx(s,__VA_ARGS__);
#endif
#ifndef THIS_WRITELOG_ 
#define THIS_WRITELOG_(s) pThis->m_log.writelog(s);
#endif
#ifndef THIS_WRITELOGX_ 
#define THIS_WRITELOGX_(s,...) pThis->m_log.writelogx(s,__VA_ARGS__);
#endif
#ifndef S_WRITELOG_
#define S_WRITELOG_(f,s) CSimpleLog::write(f,s);
#endif
#ifndef S_WRITELOGX_
#define S_WRITELOGX_(f,s,...) CSimpleLog::writex(f,s,__VA_ARGS__);
#endif
#ifndef S_CLEARLOG_
#define  S_CLEARLOG_(f) CSimpleLog::clear(f);
#endif
#ifndef S_CLRLOG_
#define S_CLRLOG_(f) CSimpleLog::clear(f);
#endif
#ifndef SET_LOGPREFIX_
#define SET_LOGPREFIX_(s) char* strLogPreFix=s;
#endif
#ifndef UNSET_LOGPREFIX_
#define UNSET_LOGPREFIX_ CSimpleLog::str_prefix=NULL;
#endif
#ifndef FIX_WRITELOG_
#define FIX_WRITELOG_(s)  CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		WRITELOG(s);
#endif
#ifndef FIX_WRITELOGX_
#define FIX_WRITELOGX_(s,...) CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		WRITELOGX(s,...);
#endif
#ifndef THIS_FIX_WRITELOG_
#define THIS_FIX_WRITELOG_(s) CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		pThis->m_log.writelog(s);
#endif
#ifndef THIS_FIX_WRITELOGX_
#define THIS_FIX_WRITELOGX_(s,...) CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		pThis->m_log.writelogx(s,__VA_ARGS__);
#endif
#pragma endregion
//===============================================================
//类声明
class CSimpleLog
{
public:
	CSimpleLog();
	CSimpleLog(char *path,char* mode="a+");
	~CSimpleLog();
	bool resetpath(char *path,char *mode="a+");
	bool writelog(char *pmsg);
	bool writelog(wchar_t *pmsg);
	bool writelogx(char *format,...);
	bool writelogx(wchar_t *format,...);
	static bool clear(char*path);
	static bool write(char *path,char *info);
	static bool write(wchar_t *path,wchar_t *info);
	static bool writex(char * path,char * info,...);
	static bool writex(wchar_t * path,wchar_t * info,...);
	static char* WcharToChar(wchar_t* wc);//宽字节转单字节 
	bool clear();
private:
	//DWORD time;
	std::string last_msg;
	FILE *file;		//日志文件
	int msg_dup_count;
	bool isopen;
public:
	static bool prefix;
	static char* str_prefix;
};
