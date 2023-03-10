//第6版
#ifndef _SIMPLELOG_H
#define _SIMPLELOG_H
#include <stdio.h>
#include <stdlib.h>
#define _SILENT					//出错时禁止弹出窗口
#define DROP_CLASS_FLAG			//msgbox2，WRITELOG2函数在自动添加函数名时，去掉可能开头的类名
//#define NOT_USE_SIMPLE_LOG	//如果想去掉日志语句，则把该语句启用
/*================================================================
	文件说明：
	1.要在vc++项目中使用，在SimpleLog.c文件上右键,属性,C/C++,预编译头，选择不使用预编译头
	在包含头文件时，使用
	extern "C" {
	#include "SimpleLog.h"
	};
	2.推荐使用宏的方式调用日志语句，因为其使用更方便，功能更强大，也更便于统一控制和修改
	3.OPENLOG,CLOSELOG和FIX_WRITELOG为组合语句，如果这样的语句放在if等语句下时，注意用{}括起来
	4.本代码虽然使用C编写，但因为其引用头文件的问题，所以并不适用于非Windows环境
	5.像如msgbox2，WRITELOG2，DUMPCALL，VIEWCALL等语句只能保证在vs编译器下正常使用，
	  如果使用其它编译器，如MinGW，则可能被简化或忽略，具体请参看相应宏定义
    --------------------------------------------------------------
    日志使用举例 
	使用举例1（写日志,c++方式）:
	SimpleLog *log;
	log=new SimpleLog;
	InitSimpleLog(log);
	log->open(log,"C:\\123.log","a+");
	log->write(log,"%d:%s",123,"aaa");
	log->close(log);
	delete log;
	使用举例2（写日志,宏方式）：
	SimpleLog *log2;
	OPENLOG(log2,"C:\\123.log","a+");	
	WRITELOG(log2,"%d:%s",123,"aaa");	//基本写日志语句
	WRITELOG2(log2,"%d:%s",456,"bbb");	//日志语句自动添加所在函数名称
	SET_LOGPREFIX(log2,"LopPreFix:");	//设置写日志前缀
	FIX_WRITELOG(log2,"%d:%s",789,"ccc");	//在日志语句前添加指定的前缀
	CLOSELOG(log2);
	使用举例3（查看函数调用堆栈）：
	SimpleLog *log2;
	OPENLOG(log2,"C:\\123.log","a+");
	VIEWCALL(log2,6);					//方法1，后面的数字6为查看堆栈层数
	__try								//方法2
	{
		RaiseException(1,0,0,0);
	}
	__except(DUMPCALL(log2,6))
	{
		(0);
	}
	CLOSELOG(log2);
//----------------------------------------------------------------*/
#ifdef NOT_USE_SIMPLE_LOG
#define msgbox(hwnd,caption,strF,...)
#define msgbox2(strF,...)
#define OPENLOG(pLog,path,mode)
#define WRITELOG(pLog,strF,...)
#define WRITELOG2(pLog,strF,...)
#define CLOSELOG(pLog)
#define VIEWCALL(pLog,depth)
#define DUMPCALL(pLog,depth)
#define SET_LOGPREFIX(pLog,str)
#define UNSET_LOGPREFIX(pLog)
#define FIX_WRITELOG(pLog,strF,...)
#endif
//================================================================
#pragma region 消息框
#ifndef msgbox
#define msgbox(hwnd,caption,strF,...) MsgBoxEx((hWnd)hwnd,caption,strF,__VA_ARGS__)
#endif
#pragma endregion
#pragma region 日志基本操作
#ifndef OPENLOG
#define OPENLOG(pLog,path,mode) pLog=(SimpleLog*)malloc(sizeof(SimpleLog));InitSimpleLog(pLog);pLog->open(pLog,path,mode)
#endif
#ifndef WRITELOG
#define WRITELOG(pLog,strF,...) pLog->write(pLog,strF,__VA_ARGS__)
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
#pragma region 扩展功能,需VS编译环境支持
#ifdef _MSC_VER		//如果使用的是VS编译器 
#ifndef msgbox2		//消息框函数，自动添加所在函数名
#define msgbox2(strF,...) MsgBoxEx(NULL,"提示：","!!"##__FUNCTION__##"：\n"##strF,__VA_ARGS__)
#endif
#ifndef WRITELOG2	//写日志函数，自动添加所在函数名
#define WRITELOG2(pLog,strF,...) pLog->write(pLog,"!!"##__FUNCTION__##": "##strF,__VA_ARGS__)
#endif
#ifndef VIEWCALL	//查看调用堆栈函数，depth指定查看调用堆栈深度
#define VIEWCALL(pLog,depth) pLog->viewcallstack(pLog,depth)
#endif
#ifndef DUMPCALL	//查看调用堆栈函数，配合SEH使用，depth指定查看调用堆栈深度
#define DUMPCALL(pLog,depth) pLog->dumpcallstack( pLog,depth,GetExceptionInformation())
#endif
#else
#ifndef msgbox2
#define msgbox2(strF,...) MsgBoxEx((hWnd)hwnd,caption,strF,__VA_ARGS__)
#endif
#ifndef WRITELOG2
#define WRITELOG2(pLog,strF,...) pLog->write(pLog,strF,__VA_ARGS__)
#endif
#ifndef VIEWCALL
#define VIEWCALL(pLog,depth) pLog->write(pLog,"不是VS编译器,无法查看函数调用堆栈")
#endif
#ifndef DUMPCALL
#define DUMPCALL(pLog,depth) pLog->dumpcallstack(pLog,depth,0)
#endif
#endif
#pragma endregion

//=================================================================
typedef struct hWnd__ {int unused;} *hWnd;
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
	void (*viewcallstack)(SimpleLog* log,int depth);
	unsigned long (*dumpcallstack)(SimpleLog* log,int depth,void*lpEP);
};
void InitSimpleLog(SimpleLog* log);
void MsgBoxEx(hWnd hwnd,const char* caption,const char *FormatMsg,...);
#endif
