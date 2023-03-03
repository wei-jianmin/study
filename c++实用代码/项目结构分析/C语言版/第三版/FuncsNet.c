#include "FuncsNet.h"
#include <stdio.h>
#include <memory.h>
#include <string.h>
#include <Windows.h>
#include <dbghelp.h>	//用于支持查看函数调用堆栈
#include <assert.h>
#pragma comment( lib, "dbghelp.lib" )
#define XML_FORMAT 1
#define min2(a, b)  (((a) < (b)) ? (a) : (b)) 
long getcallstack( void*lpEP,char buf[3][MaxFuncNameLen],int* err);
int LocateFuncPos(FuncsNet *pthis,const char* funcname1,const char* funcname2);
void _OpenLog(FuncsNet *pthis,const char* path,const char* mode)
{
	if(pthis==NULL)
		return;
	if(path==NULL || mode==NULL)
	{
		strcpy(pthis->err_msg,"openlog,parram error!");
		return;
	}
	if(pthis->initialed ==0)
	{
		strcpy(pthis->err_msg,"log haven't initialed!");
		return;
	}
	if(pthis->logopened!=0)
	{
		fclose(pthis->file);
	}
	pthis->file=fopen(path,mode);
	pthis->logopened=1;
	memcpy(pthis->file_path,path,strlen(path));
}

void _CloseLog(FuncsNet *pthis)
{
	if(pthis==NULL)
	{
		return;
	}
	if(pthis->logopened==1)
	{
		int i=0;
		for(i=pthis->ident-1;i>=0;i--)
		{
			fwrite(pthis->blanks,i*2,1,pthis->file);
			fwrite("</",2,1,pthis->file);
			fwrite(pthis->names.name_buf[i],\
				strlen(pthis->names.name_buf[i]),1,pthis->file);
			fwrite(">",1,1,pthis->file);
			fwrite("\n",1,1,pthis->file);
		}
		fflush(pthis->file);
		fclose(pthis->file);
	}
	pthis->logopened=0;
}

void MsgBox(char *p1,char *p2)
{
	char buf[256]={0};
	char *p=p1;
	p+=(strrchr(p1,'\\')-p);
	p++;
	strcat(buf,"NameStackDepth not enough\nfile : ");
	strcat(buf,p);
	strcat(buf,"\nfunc : ");
	strcat(buf,p2);
	MessageBoxA(NULL,buf,"error",MB_OK|MB_ICONERROR);
}

void _LogFunc(FuncsNet *pthis)
{
	char buf[3][MaxFuncNameLen]={0};
	int err=0;
	if(pthis==NULL)
		return;
	if(pthis->logopened>0){
		__try
		{
			RaiseException(1,0,0,0);
		}
		__except(getcallstack(GetExceptionInformation(),buf,&err))
		{
			(0);
		}
	}
	if(err!=0)	//无法获取所在函数的名字
	{
		strcpy(pthis->err_msg,buf[0]);
		return;
	}
	//buf[1]存了父函数的名字，buf[0]存了当前函数的名字
	if(pthis->logopened>0)
	{
		int ident=0;
		ident=LocateFuncPos(pthis,buf[1],buf[2]);		
#ifdef XML_FORMAT
		if(pthis->ident>ident)
		{
			int i=0;
			for(i=pthis->ident-1;i>=ident;i--)
			{
				fwrite(pthis->blanks,i*2,1,pthis->file);
				fwrite("</",2,1,pthis->file);
				fwrite(pthis->names.name_buf[i],\
					strlen(pthis->names.name_buf[i]),1,pthis->file);
				fwrite(">",1,1,pthis->file);
				fwrite("\n",1,1,pthis->file);
			}
		}
		pthis->ident=ident;
		if(pthis->ident>=NameStackDepth-1)
		{
			MsgBox(__FILE__,__FUNCDNAME__);
			
			assert(0);
		}
		strcpy(pthis->names.name_buf[pthis->names.index++],buf[0]);
		memset(pthis->func_info,0,1024);
		memcpy(pthis->func_info,buf[0],min2(1024,strlen(buf[0])));
		if(pthis->ident>0)
		{
			fwrite(pthis->blanks,pthis->ident*2,1,pthis->file);
		}
		fwrite("<",1,1,pthis->file);
		fwrite(pthis->func_info,strlen(pthis->func_info),1,pthis->file);
		fwrite(">",1,1,pthis->file);
		fwrite("\n",1,1,pthis->file);
#else
		pthis->ident=ident;
		strcpy(pthis->names.name_buf[pthis->names.index++],buf[0]);
		memset(pthis->func_info,0,1024);
		memcpy(pthis->func_info,buf[0],min2(1024,strlen(buf[0])));
		if(pthis->ident>0)
		{
			fwrite(pthis->blanks,pthis->ident*2-1,1,pthis->file);
			if(pthis->delegatecall>0)
				fwrite("+",1,1,pthis->file);
			else
				fwrite("-",1,1,pthis->file);
		}
		fwrite(pthis->func_info,strlen(pthis->func_info),1,pthis->file);
		fwrite("\n",1,1,pthis->file);
#endif
		fflush(pthis->file);
		pthis->ident++;
	}
	else if(pthis->logopened==0)
	{
		strcpy(pthis->err_msg,"log haven't opened!");
	}
}

//该函数会修改pthis->names.index
int LocateFuncPos(FuncsNet *pthis,const char* funcname1,const char* funcname2)
{
	int index=0;
	int find=0;
	if(pthis->names.index==0)
		return 0;
	index=pthis->names.index;
	pthis->delegatecall=0;
	while(index>0)
	{
		index--;
		if(strcmp(pthis->names.name_buf[index],funcname1)==0)
		{
			find=1;
			break;
		}
	}
	if(index==0)	//考虑代理调用的情况：B代理调用C，A通过调用B间接调用C
	{
		index=pthis->names.index;
		while(index>0)
		{
			index--;
			if(strcmp(pthis->names.name_buf[index],funcname2)==0)
			{
				pthis->delegatecall=1;
				find=1;
				break;
			}
		}
	}
	if(find)
		index++;
	pthis->names.index=index;
	return index;
}
void InitialFuncsNet(FuncsNet *pthis)
{
	int i;
	if(pthis==NULL)
		return;
#ifndef _MSC_VER	//如果不是微软编译器
	pthis->initialed=0;
	strcpy(pthis->err_msg,"_MSC_VER undefined");
	return;
#endif
#ifndef _DEBUG	//如果不是debug模式
	pthis->initialed=0;
	strcpy(pthis->err_msg,"_DEBUG undefined");
	return;
#endif
	if(MaxFuncNameLen<50)
	{
		strcpy(pthis->err_msg,"MaxFuncNameLen shoud not less than 50");
		return;
	}
	if(NameStackDepth<40)
	{
		strcpy(pthis->err_msg,"NameStackDepth shoud not less than 40");
		return;
	}
	pthis->logopened=0;
	pthis->ident=0;
	pthis->file=NULL;
	for(i=0;i<256;i+=2)
	{
		pthis->file_path[i]=0;
		pthis->file_path[i+1]=0;
		pthis->err_msg[i]=0;
		pthis->err_msg[i+1]=0;
#ifdef XML_FORMAT
		pthis->blanks[i]=' ';
#else
		pthis->blanks[i]='|';
#endif
		pthis->blanks[i+1]=' ';
	}
	pthis->OpenLog=_OpenLog;
	pthis->RegFunc=_LogFunc;
	pthis->CloseLog=_CloseLog;
	pthis->initialed=1;
	pthis->names.index=0;
	pthis->delegatecall=0;
	for(i=0;i<NameStackDepth;i++)
	{
		memset(pthis->names.name_buf[i],0,MaxFuncNameLen);
	}
}

#define MAXSYMBOLNAMELENGTH 256
#define SYMBOLBUFFERSIZE (sizeof(SYMBOL_INFO) + (MAXSYMBOLNAMELENGTH * sizeof(TCHAR)) - 1)
long getcallstack( void*lpEP,char buf[3][MaxFuncNameLen],int *err)
{
#ifdef _MSC_VER	
	int k;
	LPEXCEPTION_POINTERS lpEI=(LPEXCEPTION_POINTERS)lpEP;
	CONTEXT *context=lpEI->ContextRecord;

	STACKFRAME sf;
	DWORD machineType = IMAGE_FILE_MACHINE_I386/*IMAGE_FILE_MACHINE_IA64*/;
	HANDLE hProcess;
	HANDLE hThread;
	CHAR *pmsg=NULL;

	unsigned char       symbolbuffer [SYMBOLBUFFERSIZE];
	SYMBOL_INFO        *pfunctioninfo;
	// 偏移量 
	DWORD64 symDisplacement;

	hProcess = GetCurrentProcess();
	hThread = GetCurrentThread();

	memset( &sf, 0, sizeof( STACKFRAME ) );

	sf.AddrPC.Offset = context->Eip;
	sf.AddrPC.Mode = AddrModeFlat;
	sf.AddrStack.Offset = context->Esp;
	sf.AddrStack.Mode = AddrModeFlat;
	sf.AddrFrame.Offset = context->Ebp;
	sf.AddrFrame.Mode = AddrModeFlat;
	/// init dbghelp.dll
	if( !SymInitialize( hProcess, NULL, TRUE ) )
	{
		strcpy(buf[0],"dumpcallstack,dbghelp failed to intialed");
		(*err)=2;
		return EXCEPTION_EXECUTE_HANDLER;
	}
	for(k=1;k<=3;k++)
	{
		// 获取下一个栈帧
		if( !StackWalk(machineType, hProcess, hThread, &sf, context, 0, SymFunctionTableAccess, SymGetModuleBase, 0 ) )
		{
			strcpy(buf[0],"failed to get stack frame");
			*err=3;
			return EXCEPTION_EXECUTE_HANDLER;
		}
	}
	// 检查帧的正确性 
	if( sf.AddrFrame.Offset == 0 )
	{
		strcpy(buf[0],"stack frame error");
		*err=4;
		return EXCEPTION_EXECUTE_HANDLER;
	}
	// 正在调用的函数名字
	pfunctioninfo = (SYMBOL_INFO*)symbolbuffer;
	memset(pfunctioninfo, 0x0, SYMBOLBUFFERSIZE);
	pfunctioninfo->SizeOfStruct = sizeof(SYMBOL_INFO);
	pfunctioninfo->MaxNameLen = MAXSYMBOLNAMELENGTH;
	// 获取符号
	if( SymFromAddr( hProcess, sf.AddrPC.Offset,&symDisplacement,pfunctioninfo ) )
	{
		strncpy(buf[0],pfunctioninfo->Name,min2(MaxFuncNameLen,strlen(pfunctioninfo->Name)));
		*err=0;
	}
	else
	{
		strcpy(buf[0],"failed to func name");
		*err=6;
		return EXCEPTION_EXECUTE_HANDLER;
	}
	
	// 获取下一个栈帧
	if( !StackWalk(machineType, hProcess, hThread, &sf, context, 0, SymFunctionTableAccess, SymGetModuleBase, 0 ) )
	{
		strcpy(buf[0],"failed to get stack frame 2");
		*err=7;
		return EXCEPTION_EXECUTE_HANDLER;
	}
	// 检查帧的正确性 
	if( sf.AddrFrame.Offset == 0 )
	{
		strcpy(buf[0],"stack frame error 2");
		*err=8;
		return EXCEPTION_EXECUTE_HANDLER;
	}
	// 正在调用的函数名字
	pfunctioninfo = (SYMBOL_INFO*)symbolbuffer;
	memset(pfunctioninfo, 0x0, SYMBOLBUFFERSIZE);
	pfunctioninfo->SizeOfStruct = sizeof(SYMBOL_INFO);
	pfunctioninfo->MaxNameLen = MAXSYMBOLNAMELENGTH;
	// 获取符号
	if( SymFromAddr( hProcess, sf.AddrPC.Offset,&symDisplacement,pfunctioninfo ) )
	{
		//strncpy(buf[1],pfunctioninfo->Name,50);
		strncpy(buf[1],pfunctioninfo->Name,min2(MaxFuncNameLen,strlen(pfunctioninfo->Name)));
		*err=0;
	}
	else
	{
		strcpy(buf[0],"failed to func name 2");
		*err=9;
	}

	// 获取下下个栈帧
	if( !StackWalk(machineType, hProcess, hThread, &sf, context, 0, SymFunctionTableAccess, SymGetModuleBase, 0 ) )
	{
		strcpy(buf[0],"failed to get stack frame 2");
		*err=10;
		return EXCEPTION_EXECUTE_HANDLER;
	}
	// 检查帧的正确性 
	if( sf.AddrFrame.Offset == 0 )
	{
		strcpy(buf[0],"stack frame error 2");
		*err=11;
		return EXCEPTION_EXECUTE_HANDLER;
	}
	// 正在调用的函数名字
	pfunctioninfo = (SYMBOL_INFO*)symbolbuffer;
	memset(pfunctioninfo, 0x0, SYMBOLBUFFERSIZE);
	pfunctioninfo->SizeOfStruct = sizeof(SYMBOL_INFO);
	pfunctioninfo->MaxNameLen = MAXSYMBOLNAMELENGTH;
	// 获取符号
	if( SymFromAddr( hProcess, sf.AddrPC.Offset,&symDisplacement,pfunctioninfo ) )
	{
		//strncpy(buf[2],pfunctioninfo->Name,50);
		strncpy(buf[2],pfunctioninfo->Name,min2(MaxFuncNameLen,strlen(pfunctioninfo->Name)));
		*err=0;
	}
	else
	{
		strcpy(buf[0],"failed to func name 2");
		*err=12;
	}

	SymCleanup( hProcess );
	return EXCEPTION_EXECUTE_HANDLER;
#else	//没有定义_MSC_VER
	strcpy(buf,"compiler not supported");
	return 1;
#endif
}
