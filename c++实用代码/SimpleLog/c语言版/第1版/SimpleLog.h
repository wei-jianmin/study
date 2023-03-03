//第1版
#pragma once
#ifndef SIMPLELOG
#define SIMPLELOG
#include <stdio.h>
#include <stdlib.h>
#define _SILENT
/*   
	使用举例1:
	#include "SimpleLog.h"
	SimpleLog *log=(SimpleLog*)malloc(sizeof(SimpleLog));
	InitSimpleLog(log);
	log->open(log,"C:\\123.log","a+");
	log->write(log,"%d:%s",123,"aaa");
	log->close(log);
	free(log);
	使用举例2：
	#include "SimpleLog.h"
	SimpleLog *log2;
	NEWLOG(log2);
	OPENLOG(log2,"C:\\123.log","a+");
	WRITELOG(log2,"%d:%s",456,"bbb");
	SET_LOGPREFIX(log2,"LopPreFix:");
	FIX_WRITELOG(log2,"%d:%s",789,"ccc");
	CLOSELOG(log2);
	使用举例3：
	#include "SimpleLog.h"
	extern SimpleLog SimpleLogDefault;
	SimpleLog *log3;
	log3=(SimpleLog*)malloc(sizeof(SimpleLog));
	*log3=SimpleLogDefault;
	log->open(log,"C:\\123.log","a+");
	log->write(log,"%d:%s",123,"aaa");
	plog->close(plog);
	free(log);

*/
//===============================================================

#pragma region 消息框宏:msgbox(s)
#ifndef msgbox
#define msgbox(caption,strF,...)  SimpleMsgbox(caption,strF,__VA_ARGS__)
#endif
#pragma endregion
#ifndef NEWLOG
#define NEWLOG(pLog) pLog=(SimpleLog*)malloc(sizeof(SimpleLog));InitSimpleLog(pLog)
#endif
#ifndef OPENLOG
#define OPENLOG(pLog,path,mode) pLog->open(pLog,path,mode)
#endif
#ifndef WRITELOG
#define WRITELOG(pLog,strF,...) pLog->write(pLog,strF,__VA_ARGS__)
#endif
#ifndef CLOSELOG
#define CLOSELOG(pLog) pLog->close(pLog),free(pLog)
#endif
#pragma endregion
#pragma region 加前缀的写操作
#ifndef DEF_LOGPREFIX
#define DEF_LOGPREFIX(pLog,str) char* pLog##_StrLogPreFix=str
#endif
#ifndef UNDEF_LOGPREFIX
#define UNDEF_LOGPREFIX(pLog) pLog->unsetprefix(pLog)
#endif
#ifndef FIX_WRITELOG
#define FIX_WRITELOG(pLog,strF,...) pLog->setprefix(pLog,pLog##_StrLogPreFix),\
									pLog->prefix=1,\
									pLog->write(pLog,strF,__VA_ARGS__)
#endif
#pragma endregion

//=================================================================
typedef struct SimpleLogTag SimpleLog;
struct SimpleLogTag
{
	FILE *file;		//日志文件
	int  msg_dup_count;
	int  isopen;
	int  prefix;
	char last_msg[2048];
	char str_prefix[128];
	void (*init)();
	void (*close)(SimpleLog* log);
	void (*unsetprefix)(SimpleLog* log);
	void (*setprefix)(SimpleLog* log,char* prefix);
	int  (*write)(SimpleLog* log,const char *format,...);
	int  (*open)(SimpleLog* log,const char *path,const char* mode);	
};
void InitSimpleLog(SimpleLog* log);
void SimpleMsgbox(const char* caption,const char *format,...);
#endif
