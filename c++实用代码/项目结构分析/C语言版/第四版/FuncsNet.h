#pragma once
#include <stdio.h>
#include <stdlib.h>

#ifndef OPENLOGF
#define OPENLOGF(pLog,path,mode) pLog=(FuncsNet*)malloc(sizeof(FuncsNet)),InitialFuncsNet(pLog),pLog->OpenLog(pLog,path,mode)
#endif
#ifndef REGFUNC
#define REGFUNC(pLog) if(pLog) pLog->RegFunc(pLog)
#endif
#ifndef CLOSELOGF
#define CLOSELOGF(pLog) if(pLog) pLog->CloseLog(pLog),free(pLog),pLog=NULL
#endif


#define MAX_CALL_STACK 30
#define NameStackDepth 40
#define MaxFuncNameLen 50
typedef struct NameStack_tag
{
	char name_buf[NameStackDepth][MaxFuncNameLen];
	int index;				//指向name_buf的可写位置
} NameStack;
typedef struct FuncsNet_tag
{
	char func_info[1024];	//待写文件的信息
	int ident;				//当前函数的层级
	int initialed;			//结构体是否已经初始化标记
	int logopened;			//日志文件打开标记
	char file_path[256];	//日志文件路径
	FILE *file;				//日志文件指针
	char blanks[256];
	char err_msg[256];		//错误信息
	NameStack names;		//记录函数调用历史路线
	int delegatecall;		//代理调用层级，目前只支持一级代理调用
	void (*OpenLog)(struct FuncsNet_tag *pThis,const char* path,const char* mode);
	void (*CloseLog)(struct FuncsNet_tag *pThis);
	void (*RegFunc)(struct FuncsNet_tag *pThis);
} FuncsNet;
void InitialFuncsNet(FuncsNet *pthis);