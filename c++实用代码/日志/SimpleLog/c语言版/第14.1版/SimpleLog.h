#define SIMPLELOG_VER "第14版"

#ifndef _SIMPLELOG_H
#define _SIMPLELOG_H
#include <stdio.h>
#include <stdlib.h>
#define _SILENT					//出错时禁止弹出窗口
#define DROP_CLASS_FLAG			//msgbox2，WRITELOG2函数在自动添加函数名时，去掉可能开头的类名
#define VIEWCALLONELINE			//将VIEWCALL的日志写为一行
//#define NOT_USE_SIMPLE_LOG	//如果想去掉日志语句，则把该语句启用
#define NULLCHK					//只有pLog不为空时，才调用写日志的相关方法
#define WRITE_FILE_INFO
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
    6.所有写日志相关的宏，开头带L的为宽字节版本，开头不带L的，为多字节版本
	7.WRITELOG2,LWRITELOG2的第二个参数只能为常量的格式控制字符串，不能为字符串变量
    --------------------------------------------------------------
    日志使用举例 
	使用举例1（写日志,c++方式）:
	  SimpleLog *log;
	  log=new SimpleLog;
	  InitSimpleLog(log);
	  log->open(log,"C:\\123.log"+,"a+");
	  log->write(log,"%d:%s",123,"aaa");
	  log->close(log);
	  delete log;
	使用举例2（写日志,宏方式）：
	  SimpleLog *log2;
	  OPENLOG(log2,"C:\\123.log","a+");	
	  WRITELOG(log2,"%d:%s",123,"aaa");				//基本写日志语句
	  WRITELOG2(log2,"%d:%s",456,"bbb");			//日志语句自动添加所在函数名称
	  SET_LOGPREFIX(log2,"LopPreFix:");				//设置写日志前缀
	  FIX_WRITELOG(log2,"%d:%s",789,"ccc");			//在日志语句前添加指定的前缀
	  LWRITELOG(log2,L"%d:%s",123,L"aaa");			//基本写日志语句
  	  LWRITELOG2(log2,L"%d:%s",456,L"bbb");			//日志语句自动添加所在函数名称
	  LSET_LOGPREFIX(log2,L"LopPreFix:");			//设置写日志前缀
	  LFIX_WRITELOG(log2,L"%d:%s",789,L"ccc");		//在日志语句前添加指定的前缀
	  CLOSELOG(log2);
	使用举例3（查看函数调用堆栈）：
	  SimpleLog *log2;
	  OPENLOG(log2,"C:\\123.log","a+");
	  VIEWCALL(log2,6);								//方法1，后面的数字6为查看堆栈层数
	  __try											//方法2
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
#define LWRITELOG(pLog,strF,...)
#define WRITELOG2(pLog,strF,...)
#define LWRITELOG2(pLog,strF,...)
#define CLOSELOG(pLog)
#define VIEWCALL(pLog,depth)
#define DUMPCALL(pLog,depth)
#define SET_LOGPREFIX(pLog,str)
#define UNSET_LOGPREFIX(pLog)
#define FIX_WRITELOG(pLog,strF,...)
#define LSET_LOGPREFIX(pLog,str)
#define LUNSET_LOGPREFIX(pLog)
#define LFIX_WRITELOG(pLog,strF,...)
#endif
//================================================================
#define __STR2WSTR222(str,s) L##str##L": "##s
#define _STR2WSTR222(str,s) __STR2WSTR222(str,s)
#define FUNCTIONW(s) _STR2WSTR222(__FUNCTION__,s)
#ifdef NULLCHK
#define IFPLOG(s) if(s)
#else
#define IFPLOG(s) 
#endif
#pragma region 消息框
#ifndef msgbox
#define msgbox(hwnd,caption,strF,...) MsgBoxEx((hWnd)hwnd,caption,strF,__VA_ARGS__)
#endif
#pragma endregion
#pragma region 日志基本操作
#ifndef OPENLOG
#define OPENLOG(pLog,path,mode) pLog=(SimpleLog*)malloc(sizeof(SimpleLog)),InitSimpleLog(pLog),pLog->open(pLog,path,mode)
#endif
#ifndef WRITELOG
#define WRITELOG(pLog,strF,...) IFPLOG(pLog) pLog->write(pLog,strF,__VA_ARGS__)
#endif
#ifndef BWRITELOG
#define BWRITELOG(pLog,prefix,pstr,len) IFPLOG(pLog) pLog->writebytes(pLog,NULL,prefix,pstr,len)
#endif
#ifndef LWRITELOG		//写日志函数(宽字节版)
#define LWRITELOG(pLog,strF,...) IFPLOG(pLog) pLog->lwrite(pLog,strF,__VA_ARGS__)
#endif
#ifndef CLOSELOG
#define CLOSELOG(pLog) IFPLOG(pLog) pLog->close(pLog),free(pLog),pLog=NULL
#endif
#pragma endregion
#pragma region 加前缀的写操作
#ifndef SET_LOGPREFIX
#define SET_LOGPREFIX(pLog,str) char* SimpleLogPrefix=str
#endif
#ifndef UNSET_LOGPREFIX
#define UNSET_LOGPREFIX(pLog) IFPLOG(pLog) pLog->pstr_prefix=NULL
#endif
#ifndef FIX_WRITELOG
#define FIX_WRITELOG(pLog,strF,...) IFPLOG(pLog) pLog->pstr_prefix=SimpleLogPrefix,pLog->prefix=1,pLog->write(pLog,strF,__VA_ARGS__)
#endif
#ifndef LSET_LOGPREFIX
#define LSET_LOGPREFIX(pLog,str) wchar_t* SimpleLogPrefixL=str
#endif
#ifndef LUNSET_LOGPREFIX
#define LUNSET_LOGPREFIX(pLog) IFPLOG(pLog) pLog->pstr_prefix_l=NULL
#endif
#ifndef LFIX_WRITELOG
#define LFIX_WRITELOG(pLog,strF,...) IFPLOG(pLog) pLog->pstr_prefix_l=SimpleLogPrefixL,pLog->prefix=1,pLog->lwrite(pLog,strF,__VA_ARGS__)
#endif
#pragma endregion
#pragma region 扩展功能,需VS编译环境支持
#ifdef _MSC_VER		//如果使用的是VS编译器 
#ifndef msgbox2		//消息框函数，自动添加所在函数名
#define msgbox2(strF,...) MsgBoxEx(NULL,"提示：","!!"##__FUNCTION__##"：\n"##strF,__VA_ARGS__)
#endif
#ifndef WRITELOG2	//写日志函数，自动添加所在函数名
#define WRITELOG2(pLog,strF,...) IFPLOG(pLog) pLog->write(pLog,"!!"##__FUNCTION__##": "##strF,__VA_ARGS__)
#endif
#ifndef BWRITELOG2	//写日志函数，自动添加所在函数名
#define BWRITELOG2(pLog,prefix,pstr,len) IFPLOG(pLog) pLog->writebytes(pLog,__FUNCTION__##": ",prefix,(const char*)(pstr),len)
#endif
#ifndef LWRITELOG2	//写日志函数(宽字节版)，自动添加所在函数名
#define LWRITELOG2(pLog,strF,...) IFPLOG(pLog) pLog->lwrite(pLog,L"!!"##FUNCTIONW(strF),__VA_ARGS__)
#endif
#ifndef VIEWCALL	//查看调用堆栈函数，depth指定查看调用堆栈深度
#define VIEWCALL(pLog,depth) IFPLOG(pLog) pLog->viewcallstack(pLog,depth)
#endif
#ifndef DUMPCALL	//查看调用堆栈函数，配合SEH使用，depth指定查看调用堆栈深度
#define DUMPCALL(pLog,depth) IFPLOG(pLog) pLog->dumpcallstack( pLog,depth,GetExceptionInformation())
#endif
#else
#ifndef msgbox2
#define msgbox2(strF,...) MsgBoxEx((hWnd)hwnd,caption,strF,__VA_ARGS__)
#endif
#ifndef WRITELOG2
#define WRITELOG2(pLog,strF,...) IFPLOG pLog->write(pLog,strF,__VA_ARGS__)
#endif
#ifndef VIEWCALL
#define VIEWCALL(pLog,depth) IFPLOG pLog->write(pLog,"不是VS编译器,无法查看函数调用堆栈")
#endif
#ifndef DUMPCALL
#define DUMPCALL(pLog,depth) IFPLOG pLog->dumpcallstack(pLog,depth,0)
#endif
#endif
#pragma endregion

//=================================================================
typedef struct hWnd__ {int unused;} *hWnd;
typedef struct SimpleLogTag SimpleLog;
struct SimpleLogTag
{
	void (*close)(SimpleLog* log);
	int  (*write)(SimpleLog* log,const char *format,...);
	int  (*lwrite)(SimpleLog* log,const wchar_t *wformat,...);
	int	 (*writebytes)(SimpleLog* log,const char* pfun,const char* prefix,const char *pbytes,int len);
	int  (*open)(SimpleLog* log,const char *path,const char* mode);	
	void (*viewcallstack)(SimpleLog* log,int depth);
	unsigned long (*dumpcallstack)(SimpleLog* log,int depth,void*lpEP);
	FILE *file;		//日志文件
	int  msg_dup_count;
	int  isopen;
	int  prefix; 
	char filepath[1024];
	char last_msg[20480];
	char *pstr_prefix;
	wchar_t * pstr_prefix_l;
};
void InitSimpleLog(SimpleLog* log);
void MsgBoxEx(hWnd hwnd,const char* caption,const char *FormatMsg,...);
#endif
