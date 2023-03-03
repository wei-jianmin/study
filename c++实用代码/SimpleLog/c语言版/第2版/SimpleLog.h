//第2版
#ifndef _SIMPLELOG_H
#define _SIMPLELOG_H
#include <stdio.h>
#include <stdlib.h>
#define _SILENT
/*   
	使用举例1:
	SimpleLog *log=new SimpleLog;	//c++的方式
	InitSimpleLog(log);
	log->open(log,"C:\\123.log","a+");
	log->write(log,"%d:%s",123,"aaa");
	log->close(log);
	delete log;
	使用举例2：
	SimpleLog *log2;
	NEWLOG(log2);
	OPENLOG(log2,"C:\\123.log","a+");
	WRITELOG(log2,"%d:%s",456,"bbb");
	SET_LOGPREFIX(log2,"LopPreFix:");
	FIX_WRITELOG(log2,"%d:%s",789,"ccc");
	CLOSELOG(log2);
	使用举例3：
	SimpleLog* plog;		//在文件的开始位置加上：extern SimpleLog SimpleLogDefault;
	plog=(SimpleLog*)malloc(sizeof(SimpleLog));
	*plog=SimpleLogDefault;
	OPENLOG(plog,"C:\\a.txt","a+");
	WRITELOG2(plog,"%d--%d--%f--%s",1,2,3.4,"abc");
	CLOSELOG(plog);
	注：
	要在vc++项目中使用，在SimpleLog.c文件上右键,属性,C/C++,预编译头，选择不使用预编译头
	在包含头文件时，使用
	extern "C" {
	#include "SimpleLog.h"
	};
*/
//===============================================================

#pragma region 消息框宏:msgbox(s)
#ifndef msgbox
#define msgbox(str) ::MessageBox(NULL,str,"caption",MB_OK)
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
#ifndef WRITELOG2	//仅能保证在VC下正常使用
#define WRITELOG2(pLog,strF,...) pLog->write(pLog,"{"##__FUNCTION__##"} "##strF,__VA_ARGS__)
#endif
#ifndef CLOSELOG
#define CLOSELOG(pLog) pLog->close(pLog),free(pLog)
#endif
#pragma endregion
#pragma region 加前缀的写操作
#ifndef SET_LOGPREFIX
#define SET_LOGPREFIX(pLog,str) char* SimpleLogPrefix=str
#endif
#ifndef UNSET_LOGPREFIX
#define UNSET_LOGPREFIX(pLog) pLog->pstr_prefix=NULL
#endif
#ifndef FIX_WRITELOG
#define FIX_WRITELOG(pLog,strF,...) pLog->pstr_prefix=SimpleLogPrefix,pLog->prefix=1,pLog->write(pLog,strF,__VA_ARGS__)
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
	char filepath[256];
	char last_msg[2048];
	char *pstr_prefix;
	void (*close)(SimpleLog* log);
	int  (*write)(SimpleLog* log,const char *format,...);
	int  (*open)(SimpleLog* log,const char *path,const char* mode);	
};
void InitSimpleLog(SimpleLog* log);
void testabc();
#endif
