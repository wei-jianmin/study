/*
ʹ��˵����ע�����
�� ֻ֧�ֶ��ֽڱ���ģʽ
�� �뾡�����ú꣬������ֱ�ӵ�����ĳ�Ա����
�� ��̬д��־������Ǿ�̬д��־������Ҫ��ͬһ��ʱ���ڶ�ͬһ����־�ļ����в���
�� ���ʹ�ô�ǰ׺���ܵĺ꣨������FIX������ע�����SET_LOGPREFIX��UNSET_LOGPREFIX��ʹ��
�� ���еĺ궼��2�а汾�����ǵ����ֻ���һ�£������ǣ�ĩβ���»��ߵĺ꣬ʹ��ʱ����β�����ټӷֺ�
�� #pragma once��#pragma (end)region��VS���еĹؼ��֣������������֧�֣��ɽ���ֱ��ȥ��
*/
#pragma once
#include <fstream>
//===============================================================
#define _SILENT
#define LOGNAME m_log
//===============================================================
#pragma region ��Ϣ���:msgbox(s)
#ifndef msgbox
#define msgbox(s) ::MessageBox(NULL,s,"caption",MB_OK)
#endif
#pragma endregion
#ifndef SETPATH
#define SETPATH(s,...) LOGNAME.resetpath(s,__VA_ARGS__)
#endif
#pragma region ��������:WRITELOG(s)��WRITELOGX(s,...)
#ifndef WRITELOG
#define WRITELOG(s) LOGNAME.writelog(s)
#endif
#ifndef WRITELOGX
#define WRITELOGX(s,...) LOGNAME.writelogx(s,__VA_ARGS__)
#endif
#pragma endregion
#pragma region ��ǰ׺�ģ�SET_LOGPREFIX(s)��UNSET_LOGPREFIX��FIX_WRITELOG(s)��FIX_WRITELOGX(s,...)
#ifndef SET_LOGPREFIX
#define SET_LOGPREFIX(s) char* strLogPreFix=s
#endif
#ifndef UNSET_LOGPREFIX
#define UNSET_LOGPREFIX CSimpleLog::str_prefix=NULL
#endif
#ifndef FIX_WRITELOG
#define FIX_WRITELOG(s)  CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		LOGNAME.writelog(s)
#endif
#ifndef FIX_WRITELOGX
#define FIX_WRITELOGX(s,...) CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		LOGNAME.writelogx(s,__VA_ARGS__)
#endif
#pragma endregion
#pragma region ͨ��thisָ����ã�THIS_WRITELOG(s)��THIS_WRITELOGX(s,...)
#ifndef THIS_WRITELOG
#define THIS_WRITELOG(s) pThis->LOGNAME.writelog(s)
#endif
#ifndef THIS_WRITELOGX
#define THIS_WRITELOGX(s,...) pThis->LOGNAME.writelogx(s,__VA_ARGS__)
#endif
#pragma endregion
#pragma region ͨ��thisָ����ü�ǰ׺�ģ�THIS_FIX_WRITELOG(s)��THIS_FIX_WRITELOGX(s,...)
#ifndef THIS_FIX_WRITELOG
#define THIS_FIX_WRITELOG(s) CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		pThis->LOGNAME.writelog(s)
#endif
#ifndef THIS_FIX_WRITELOGX
#define THIS_FIX_WRITELOGX(s,...) CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		pThis->LOGNAME.writelogx(s,__VA_ARGS__)
#endif
#pragma endregion
#pragma region ���þ�̬������S_WRITELOG(f,s)��S_WRITELOGX(f,s,...)��S_CLEARLOG(f)��S_CLRLOG(f)
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
#pragma region ��̬��ǰ׺�ģ�S_FIX_WRITELOG(f,s)��S_FIX_WRITELOGX(f,s,...)
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
#pragma region ��β���ֺŵĶ�Ӧ��
#ifndef msgbox_
#define msgbox_(s) MessageBox(NULL,s,"caption",MB_OK);
#endif
#ifndef WRITELOG_
#define WRITELOG_(s) LOGNAME.writelog(s);
#endif
#ifndef WRITELOGX_
#define WRITELOGX_(s,...) LOGNAME.writelogx(s,__VA_ARGS__);
#endif
#ifndef THIS_WRITELOG_ 
#define THIS_WRITELOG_(s) pThis->LOGNAME.writelog(s);
#endif
#ifndef THIS_WRITELOGX_ 
#define THIS_WRITELOGX_(s,...) pThis->LOGNAME.writelogx(s,__VA_ARGS__);
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
		pThis->LOGNAME.writelog(s);
#endif
#ifndef THIS_FIX_WRITELOGX_
#define THIS_FIX_WRITELOGX_(s,...) CSimpleLog::prefix=true,\
		CSimpleLog::str_prefix=strLogPreFix,\
		pThis->LOGNAME.writelogx(s,__VA_ARGS__);
#endif
#pragma endregion
//===============================================================
//������
class CSimpleLog
{
public:
	CSimpleLog();
	CSimpleLog(const char *path,const char* mode="a+");
	~CSimpleLog();
	bool resetpath(const char *path,const char *mode="a+");
	bool writelog(const char *pmsg);
	bool writelog(const wchar_t *pmsg);
	bool writelogx(const char *format,...);
	bool writelogx(const wchar_t *format,...);
	static bool clear(const char*path);
	static bool write(const char *path,const char *info);
	static bool write(const wchar_t *path,const wchar_t *info);
	static bool writex(const char * path,const char * info,...);
	static bool writex(const wchar_t * path,const wchar_t * info,...);
	static char* WcharToChar(const wchar_t* wc);//���ֽ�ת���ֽ� 
	bool clear();
private:
	//DWORD time;
	std::string last_msg;
	FILE *file;		//��־�ļ�
	int msg_dup_count;
	bool isopen;
public:
	static bool prefix;
	static char* str_prefix;
};
