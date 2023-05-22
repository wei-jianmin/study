#pragma once
#include <fstream>

//typedef unsigned long DWORD;

class CSimpleLog
{
public:
	CSimpleLog(char *path);
	~CSimpleLog();
	bool writelog(char *pmsg);
	bool writelogx(char *format,...);
	bool clear();
	static bool clear(char*path);
	static bool write(char *path,char *info);
	static bool writex(char * path,char * info,...);
private:
	//DWORD time;
	std::string last_msg;
	FILE *file;		//日志文件
	int msg_dup_count;
	bool isopen;
};

#ifndef THIS_WRITELOG
#define THIS_WRITELOG(s) pThis->m_log.writelog(s)
#endif

#ifndef WRITELOG
#define WRITELOG(s) m_log.writelog(s)
#endif

#ifndef THIS_WRITELOG_ 
#define THIS_WRITELOG_(s) pThis->m_log.writelog(s);
#endif

#ifndef WRITELOG_
#define WRITELOG_(s) m_log.writelog(s);
#endif

#ifndef msgbox
#define msgbox(s) MessageBox(NULL,s,"caption",MB_OK)
#endif

//-------------------------------------------------------

#ifndef THIS_WRITELOGX
#define THIS_WRITELOGX(s,...) pThis->m_log.writelogx(s,__VA_ARGS__)
#endif

#ifndef WRITELOGX
#define WRITELOGX(s,...) m_log.writelogx(s,__VA_ARGS__)
#endif

#ifndef THIS_WRITELOGX_ 
#define THIS_WRITELOGX_(s,...) pThis->m_log.writelogx(s,__VA_ARGS__);
#endif

#ifndef WRITELOGX_
#define WRITELOGX_(s,...) m_log.writelogx(s,__VA_ARGS__);
#endif

//-------------------------------------------------------------

#ifndef S_WRITELOG
#define S_WRITELOG(f,s) CSimpleLog::write(f,s)
#endif

#ifndef S_WRITELOG_
#define S_WRITELOG_(f,s) CSimpleLog::write(f,s);
#endif

#ifndef S_WRITELOGX
#define S_WRITELOGX(f,s,...) CSimpleLog::writex(f,s,__VA_ARGS__)
#endif

#ifndef S_WRITELOGX_
#define S_WRITELOGX_(f,s,...) CSimpleLog::writex(f,s,__VA_ARGS__);
#endif
