//第12版
#include "SimpleLog.h"
#include <Windows.h>
#include <IO.H>
#include <locale.h>
#include <WinVer.h>
//#include <vadefs.h>	//定义了va_list
#include <dbghelp.h>	//用于支持查看函数调用堆栈
#pragma comment( lib, "dbghelp.lib" )
#pragma comment(lib, "User32.lib")
#pragma comment(lib, "version")

//返回n个英文字宽所对应的字数(两个英文字宽对应一个汉字)
static int Cal(wchar_t *pwc,int n)
{
	int width=0;
	int i=0;
	for(i=0;i<n;i++)
	{
		width++;
		if(pwc[i]>0x3000 && pwc[i]<0x9FFF)	//中日韩
		{
			width++;
		}
		if(width>=44)
			break;
	}
	return i;
}
static int openlog(SimpleLog* log,const char *path,const char* mode)
{
	int a;
	unsigned long dw;
	if(log==NULL)
		return 0;
	log->isopen=0;
	if(path == NULL)
		return 0;
	log->msg_dup_count=0;	//控制重复消息
	memset(log->last_msg,0,2048);
	//打开文件
	a=_access(path,6);
	dw=GetLastError();
	if(a!=0)
	{
#ifndef _SILENT
		char buf[200]="构造函数：文件不存在或没有读写权限\n";
		strcat(buf,path);
		MessageBox(NULL,buf,"错误",MB_OK|MB_ICONHAND);
#endif
		return 0;
	}
	strcpy(log->filepath,path);
	//之前的步骤能保证文件存在且有读写权限
	if(strcmp("a+",mode)==0)
	{
		HANDLE hFile;
		hFile = CreateFileA(path, GENERIC_READ,          // open for reading
			FILE_SHARE_READ,							 // share for reading
			NULL,										 // default security
			OPEN_EXISTING,								 // existing file only
			FILE_FLAG_BACKUP_SEMANTICS ,				 // normal file
			NULL);
		if(hFile!=NULL)
		{
			SYSTEMTIME st_file,st_cpu;
			FILETIME ftCreate, ftModify, ftAccess;
			if (GetFileTime(hFile, &ftCreate, &ftAccess, &ftModify))
			{
				long t_f,t_c;
				ZeroMemory(&st_file, sizeof(SYSTEMTIME));
				FileTimeToSystemTime(&ftModify, &st_file);
				GetLocalTime(&st_cpu);
				t_f=st_file.wYear*500+st_file.wMonth*40+st_file.wDay;	//文件创建时间
				t_c=st_cpu.wYear*500+st_cpu.wMonth*40+st_cpu.wDay;		//电脑当前时间
				CloseHandle(hFile);
				if(t_c!=t_f)
				{
					log->file=fopen(path,"w+");			//清空文件内容
					fclose(log->file);
				}
			}
			else
				CloseHandle(hFile);
		}
	}
	log->file=fopen(path,mode);
	dw=GetLastError();
	if(log->file !=NULL)
	{
		char timebuf[20]={0};
		SYSTEMTIME sys; 
		log->isopen=1;
		//写入时间
		GetLocalTime(&sys); 
		strcpy(timebuf,"----------------");
		fwrite(timebuf,strlen(timebuf),1,log->file);
		memset(timebuf,0,sizeof(timebuf));
#ifdef _MSC_VER
		sprintf_s(timebuf,sizeof(timebuf),"%04d-%02d-%02d",sys.wYear,sys.wMonth, sys.wDay);
#else
		sprintf(timebuf,"%04d-%02d-%02d",sys.wYear,sys.wMonth, sys.wDay);
#endif
		fwrite(timebuf,strlen(timebuf),1,log->file);
		memset(timebuf,0,sizeof(timebuf));
		strcpy(timebuf,"------------------");
		fwrite(timebuf,strlen(timebuf),1,log->file);
		fwrite("\n",1,1,log->file);
#ifdef WRITE_FILE_INFO
		{
			const int LINEWIDTH = 44;
			char path0[MAX_PATH]={0};
			wchar_t path1[_MAX_PATH] = {0};		//模块路径名
			wchar_t path2[MAX_PATH]={0};		//加换行符的模块路径名
			wchar_t *ppath1=path1;
			wchar_t *ppath2=path2;
			char path3[MAX_PATH*2]={0};
			int offset=0;
			DWORD dwLen =0;
			char *pszAppVersion=NULL;
			GetModuleFileNameA(NULL,path0,MAX_PATH);//得到程序模块名称，全路径，多字节
			GetModuleFileNameW(NULL,path1,MAX_PATH);//得到程序模块名称，全路径，宽字节
			wcscpy(path2,L"MoudlePath=");
			ppath2+=11;
			wcscpy(ppath2,ppath1);
			offset=Cal(path2,LINEWIDTH-11);
			ppath1+=offset;
			ppath2+=offset;
			ppath2[0]='\n';
			ppath2++;
			while(strlen(ppath1)>0)
			{
				wcscpy(ppath2,ppath1);
				offset=Cal(ppath2,LINEWIDTH);
				ppath1+=offset;
				ppath2+=offset;
				ppath2[0]='\n';
				ppath2++;
			}
			setlocale(LC_ALL,"");
			wcstombs(path3,path2,MAX_PATH*2);
			
			//获取当前文件的版本信息
			dwLen = GetFileVersionInfoSizeA(path0,NULL); 
			pszAppVersion = (char*)calloc(dwLen+1,1);
			memset(pszAppVersion,0,dwLen+1);
			if(pszAppVersion)
			{
				if(dwLen>0)
				{
					UINT nLen=0;
					VS_FIXEDFILEINFO *pFileInfo=NULL;
					char* strVersion;
					memset(pszAppVersion,0,sizeof(char)*(dwLen+1));
					GetFileVersionInfoA(path0,(DWORD)0,dwLen,pszAppVersion);
					VerQueryValue(pszAppVersion,"\\",(LPVOID*)&pFileInfo,&nLen);
					strVersion = (char*)calloc(50,1);
					memset(strVersion,0,50);
					if(strVersion && pFileInfo)
					{
						//获取版本号
						sprintf(strVersion,"FileVersion=%d.%d.%d.%d\n",HIWORD(pFileInfo->dwFileVersionMS),
							LOWORD(pFileInfo->dwFileVersionMS),
							HIWORD(pFileInfo->dwFileVersionLS),
							LOWORD(pFileInfo->dwFileVersionLS));
						fwrite(strVersion,strlen(strVersion),1,log->file);
						free(strVersion);
					}
				}
				free(pszAppVersion);
			}
			fwrite(path3,strlen(path3),1,log->file);
			fwrite("\n",1,1,log->file);
			fflush(log->file);
			memset(path2,0,MAX_PATH);
			strcpy(path2,"--------------------------------------------\n");
			fwrite(path2,strlen(path2),1,log->file);
			fflush(log->file);
		}
#endif
		return 0;
	}
	else
	{
#ifndef _SILENT
		char buffer[10];
		char buffer2[20]={"ErrNo=0x"};
		char buffer3[40]="文件打开错误，";
		_itoa( dw, buffer, 16 );	
		strcat(buffer2,buffer);
		strcat(buffer3,buffer2);
		MessageBox(NULL,buffer3,"错误",MB_OK|MB_ICONHAND);
#endif
		return 0;
	}

}
static void closelog(SimpleLog* log)
{
	if(log->isopen)
	{
		char buf[50]="----------------write finish----------------\n\n";
		fwrite(buf,strlen(buf),1,log->file);
		fflush(log->file);
		fclose(log->file);
	}
	log->isopen=0;
	return;
}

static int writelog(SimpleLog* log,const char *format,...)
{
	char pmsg[2048]={0};
	va_list arg_ptr;
	if(!log->isopen)
		return 0;
	if(format==NULL)
		return 0;
	
	va_start(arg_ptr,format);	//已固定参数地址起点确定变参的内存起始地址。
	vsprintf(pmsg,format,arg_ptr);
	va_end(arg_ptr);		// 要写的内容已经存在了pmsg中

	if(log->isopen)
	{
		//if(log->last_msg.compare(pmsg)==0)		//消息发生重复
		int len=min(2048,strlen(pmsg)+1);
		char timebuf[20]={0};
		SYSTEMTIME sys; 
		unsigned int l1,l2,l3,l4;
		unsigned long dw=0;
		int size=0;
		GetLocalTime(&sys); 
		if(strncmp(log->last_msg,pmsg,len)==0)
		{
			log->msg_dup_count++;				//记录消息重复次数
			if(log->msg_dup_count==1)			//消息重复一次
			{
				unsigned int l=0;
				unsigned long dw=0;
				l=fwrite("same as above ......\n",21,1,log->file);	//写21个字节
				dw=GetLastError();
				fflush(log->file);
				if(l!=1)
				{
#ifndef _SILENT
					char buffer[10];
					char buffer2[20]={"ErrNo=0x"};
					char buffer3[40]="文件写入错误，";
					_itoa( dw, buffer, 16 );
					strcat(buffer2,buffer);
					strcat(buffer3,buffer2);
					MessageBox(NULL,buffer3,"错误",MB_OK|MB_ICONHAND);
#endif
					return 0;
				}
				return 0;
			}
			else if(log->msg_dup_count>1)		//消息重复多次，不用写到日志
			{
				return 0;
			}
		}
		else if(log->msg_dup_count>0)			//消息之前重复过，现在不重复了
		{
			char buf[5];
			unsigned long dw=0;
			unsigned int l1=0,l2=0;
			fwrite("repeated times=",16,1,log->file);		//写16个字节
			_itoa( log->msg_dup_count, buf, 5);
			l1=fwrite(buf,strlen(buf)+1,1,log->file);
			l2=fwrite("\n",1,1,log->file);
			dw=GetLastError();
			fflush(log->file);
			log->msg_dup_count=0;				//重复次数置0
			if(dw !=0 && l1*l2!=1)
			{
#ifndef _SILENT
				char buffer[10];
				char buffer2[20]={"ErrNo=0x"};
				char buffer3[40]="文件写入错误，";
				_itoa( dw, buffer, 16 );
				strcat(buffer2,buffer);
				strcat(buffer3,buffer2);
				MessageBox(NULL,buffer3,"错误",MB_OK|MB_ICONHAND);
#endif
				return 0;
			}
		}
/*
		DWORD t,t1,t2;
		t=GetTickCount()-time;
		t1=t/1000;
		t2=t%1000;
		if(t1>999)
		{
			t1=0;
			time+=1000;
		}
		char buffer1[10]={0};
		char buffer2[10]={0};
		_itoa( t1, buffer1, 10 );
		_itoa( t2, buffer2, 10 );
*/
		
		//消息不为空，写入时间
		if(strlen(pmsg)>0)
		{
#ifdef _MSC_VER
			sprintf_s(timebuf,sizeof(timebuf),"%02d:%02d:%02d.%03d",sys.wHour,sys.wMinute, sys.wSecond,sys.wMilliseconds);
#else
			sprintf(timebuf,"%02d:%02d:%02d.%03d",sys.wHour,sys.wMinute, sys.wSecond,sys.wMilliseconds);
#endif
			l1=l2=l3=l4=0;
			l1=fwrite(timebuf,strlen(timebuf),1,log->file);
			l2=fwrite("\t",1,1,log->file);
		}
		
		if(log->prefix)	//写前缀
		{	
			if(strlen(log->pstr_prefix)!=0)
				fwrite(log->pstr_prefix,strlen(log->pstr_prefix),1,log->file);
			log->prefix=0;
		}
		//写入传来的消息,如果传来的消息符合!!Class::Func msg格式，则转为Func: msg格式
		{
			char *pm=pmsg;
			if(pm[0]=='!' && pm[1]=='!')	//初步确定是带类名及函数名的
			{
#ifdef DROP_CLASS_FLAG
				pm=strchr(pmsg,':');
				if(pm!=NULL && pm[1]==':')	//再次确定是带类名及函数名的
				{
					pm+=2;					//pm指向函数名
				}
				else if(pm!=NULL && pmsg[0]=='!' && pmsg[1]=='!')	//说明是以!!开头，含有:字符，但不含::的字符串
				{
					pm=pmsg+2;
				}
				else						//说明不是以!!开头
				{
					pm=pmsg;
				}
#else
				pm+=2;
#endif
				fwrite(pm,strlen(pm),1,log->file);
			}
			else
				fwrite(pmsg,strlen(pmsg),1,log->file);
			l4=fwrite("\n",1,1,log->file);			//换行
		}
		dw=GetLastError();
		fflush(log->file);
		if(dw !=0 && l1*l2*l3*l4!=1)
		{
#ifndef _SILENT
			char buffer[10];
			char buffer2[20]={"ErrNo=0x"};
			char buffer3[40]="文件写入错误，";
			_itoa( dw, buffer, 16 );
			strcat(buffer2,buffer);
			strcat(buffer3,buffer2);
			MessageBox(NULL,buffer3,"错误",MB_OK|MB_ICONHAND);
			MessageBox(NULL,pmsg,"写入错误的信息:",MB_OK|MB_ICONHAND);
#endif
			return 0;
		}
		memset(log->last_msg,0,2048);
		len=min(2048,strlen(pmsg)+1);
		memcpy(log->last_msg,pmsg,len);
		return 0;
	}
	return 0;
}

static int writebytes(SimpleLog* log,const char* pfun,const char* prefix,const char *pbytes,int len)
{
	char pmsg[2048]={0};
	unsigned char c;
	char h;
	int i = 0;
	unsigned char*str=(unsigned char*)pbytes;
	int strLen=len;
	char *result=pmsg;
	if(len<1 || len>=1024)
		return 0;
	while (strLen--)
	{
		c = *str++;
		//取字符的高四位
		h = (c >> 4) & 0x0F;
		if (h < 10)
		{
			//如果是 0-9 
			result[i++] = h + 48;
		}
		else
		{
			//如果是 A-F
			result[i++] = h + 55;
		}
		//取字符的低四位
		h = c & 0x0F;
		if (h < 10)
		{
			//如果是 0-9 
			result[i++] = h + 48;//'0'
		}
		else
		{
			//如果是 A-F
			result[i++] = h + 55;//'A'-10
		}
	}


	if(log->isopen)
	{
		//if(log->last_msg.compare(pmsg)==0)		//消息发生重复
		int len=min(2048,strlen(pmsg)+1);
		char timebuf[20]={0};
		char tmpmsgbuf[2048]={0};
		SYSTEMTIME sys; 
		unsigned int l1,l2,l3,l4;
		unsigned long dw=0;
		int size=0;
		GetLocalTime(&sys); 
		memcpy(tmpmsgbuf,pmsg,len);
		if(prefix && strlen(prefix)>0)
			strcat(tmpmsgbuf,prefix);
		if(pfun && strlen(pfun)>0)
			strcat(tmpmsgbuf,pfun);
		tmpmsgbuf[2047]=0;
		if(strcmp(log->last_msg,tmpmsgbuf,len)==0)
		{
			log->msg_dup_count++;				//记录消息重复次数
			if(log->msg_dup_count==1)			//消息重复一次
			{
				unsigned int l=0;
				unsigned long dw=0;
				l=fwrite("same as above ......\n",21,1,log->file);	//写21个字节
				dw=GetLastError();
				fflush(log->file);
				if(l!=1)
				{
#ifndef _SILENT
					char buffer[10];
					char buffer2[20]={"ErrNo=0x"};
					char buffer3[40]="文件写入错误，";
					_itoa( dw, buffer, 16 );
					strcat(buffer2,buffer);
					strcat(buffer3,buffer2);
					MessageBox(NULL,buffer3,"错误",MB_OK|MB_ICONHAND);
#endif
					return 0;
				}
				return 0;
			}
			else if(log->msg_dup_count>1)		//消息重复多次，不用写到日志
			{
				return 0;
			}
		}
		else if(log->msg_dup_count>0)			//消息之前重复过，现在不重复了
		{
			char buf[5];
			unsigned long dw=0;
			unsigned int l1=0,l2=0;
			fwrite("repeated times=",16,1,log->file);		//写16个字节
			_itoa( log->msg_dup_count, buf, 5);
			l1=fwrite(buf,strlen(buf)+1,1,log->file);
			l2=fwrite("\n",1,1,log->file);
			dw=GetLastError();
			fflush(log->file);
			log->msg_dup_count=0;				//重复次数置0
			if(dw !=0 && l1*l2!=1)
			{
#ifndef _SILENT
				char buffer[10];
				char buffer2[20]={"ErrNo=0x"};
				char buffer3[40]="文件写入错误，";
				_itoa( dw, buffer, 16 );
				strcat(buffer2,buffer);
				strcat(buffer3,buffer2);
				MessageBox(NULL,buffer3,"错误",MB_OK|MB_ICONHAND);
#endif
				return 0;
			}
		}
		
		//消息不为空，写入时间
		if(strlen(pmsg)>0)
		{
#ifdef _MSC_VER
			sprintf_s(timebuf,sizeof(timebuf),"%02d:%02d:%02d.%03d",sys.wHour,sys.wMinute, sys.wSecond,sys.wMilliseconds);
#else
			sprintf(timebuf,"%02d:%02d:%02d.%03d",sys.wHour,sys.wMinute, sys.wSecond,sys.wMilliseconds);
#endif
			l1=l2=l3=l4=0;
			l1=fwrite(timebuf,strlen(timebuf),1,log->file);
			l2=fwrite("\t",1,1,log->file);
		}
		
		if(log->prefix)	//写前缀
		{	
			if(strlen(log->pstr_prefix)!=0)
				fwrite(log->pstr_prefix,strlen(log->pstr_prefix),1,log->file);
			log->prefix=0;
		}
		//写入传来的消息,如果传来的消息符合!!Class::Func msg格式，则转为Func: msg格式
		{
			char *pm=pmsg;
			if(pfun != NULL && strlen(pfun)>0)
			{
				fwrite(pfun,strlen(pfun),1,log->file);
			}
			if(prefix != NULL && strlen(prefix)>0)
				fwrite(prefix,strlen(prefix),1,log->file);
			fwrite(pmsg,strlen(pmsg),1,log->file);
			l4=fwrite("\n",1,1,log->file);			//换行
		}
		dw=GetLastError();
		fflush(log->file);
		if(dw !=0 && l1*l2*l3*l4!=1)
		{
#ifndef _SILENT
			char buffer[10];
			char buffer2[20]={"ErrNo=0x"};
			char buffer3[40]="文件写入错误，";
			_itoa( dw, buffer, 16 );
			strcat(buffer2,buffer);
			strcat(buffer3,buffer2);
			MessageBox(NULL,buffer3,"错误",MB_OK|MB_ICONHAND);
			MessageBox(NULL,pmsg,"写入错误的信息:",MB_OK|MB_ICONHAND);
#endif
			return 0;
		}
		memset(log->last_msg,0,2048);
		len=min(2048,strlen(pmsg)+1);
		memcpy(log->last_msg,pmsg,len);
		if(prefix && strlen(prefix)>0)
			strcat(log->last_msg,prefix);
		if(pfun && strlen(pfun)>0)
			strcat(log->last_msg,pfun);
		return 0;
	}
	return 0;
}

//宽字节版本的写日志函数
static int lwritelog(SimpleLog* log,const wchar_t *wformat,...)
{
	wchar_t pmsgw[4096]={0};
	char pmsg[2048]={0};
	va_list arg_ptr;

	if(!log->isopen)
		return 0;
	if(wformat==NULL)
		return 0;

	va_start(arg_ptr,wformat);	//已固定参数地址起点确定变参的内存起始地址。
	vswprintf_s(pmsgw,4090,wformat,arg_ptr);
	va_end(arg_ptr);			// 要写的内容已经存在了pmsg中
	
	setlocale(LC_ALL,"");
	wcstombs(pmsg,pmsgw,2048);
	return writelog(log,pmsg);
}

//没有添加时间、重复判断、添加前缀、类名识别、自动换行等功能
static void simpwrite(SimpleLog*log,const char* format, ...)
{
	if(log==NULL)
		return;
	if(log->isopen)
	{
		int len;
		unsigned long err;
		char pmsg[2048]={0};
		va_list arg_ptr;
		if(!log->isopen)
			return;
		if(format==NULL)
			return;

		va_start(arg_ptr,format);	//已固定参数地址起点确定变参的内存起始地址。
		vsprintf(pmsg,format,arg_ptr);
		va_end(arg_ptr);		// 要写的内容已经存在了pmsg中

		fwrite(pmsg,strlen(pmsg),1,log->file);
		//fwrite("\n",1,1,log->file);
		err=GetLastError();
		fflush(log->file);
		if(err !=0)
		{
#ifndef _SILENT
			char buffer[10];
			char buffer2[20]={"ErrNo=0x"};
			char buffer3[40]="文件写入错误，";
			_itoa( dw, buffer, 16 );
			strcat(buffer2,buffer);
			strcat(buffer3,buffer2);
			MessageBox(NULL,buffer3,"错误",MB_OK|MB_ICONHAND);
			MessageBox(NULL,pmsg,"写入错误的信息:",MB_OK|MB_ICONHAND);
#endif
			return ;
		}
		memset(log->last_msg,0,2048);
		len=min(2048,strlen(pmsg)+1);
		memcpy(log->last_msg,pmsg,len);
	}
}

#define MAXSYMBOLNAMELENGTH 256
#define SYMBOLBUFFERSIZE (sizeof(SYMBOL_INFO) + (MAXSYMBOLNAMELENGTH * sizeof(TCHAR)) - 1)
//	depth是stepover之后检索的函数层数
static void dump_callstack( CONTEXT *context ,SimpleLog* log,int depth,int stepover)
{
#ifdef _MSC_VER	 
	STACKFRAME sf;
	DWORD machineType = IMAGE_FILE_MACHINE_I386/*IMAGE_FILE_MACHINE_IA64*/;
	DWORD err;
	HANDLE hProcess;
	HANDLE hThread;
	int k;
	CHAR *pmsg=NULL;
	if(log==NULL)
		return;
	if(!log->isopen)
		return;

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
	if( SymInitialize( hProcess, NULL, TRUE ) )
	{
#ifndef VIEWCALLONELINE
		simpwrite(log,"函数调用堆栈情况：\n");
#endif
	}
	else
	{
		simpwrite(log,"初始化dbghelp失败，无法查看函数调用堆栈\n");
		return;
	}

	for(k=1;k<=depth+stepover;k++)
	{
		unsigned char       symbolbuffer [SYMBOLBUFFERSIZE];
		SYMBOL_INFO        *pfunctioninfo;
		// 偏移量 
		DWORD64 symDisplacement;
		// 获取下一个栈帧
		if( !StackWalk(machineType, hProcess, hThread, &sf, context, 0, SymFunctionTableAccess, SymGetModuleBase, 0 ) )
		{
			simpwrite(log,"获取栈帧失败\n");
			break;
		}
		// 检查帧的正确性 
		if( sf.AddrFrame.Offset == 0 )
		{
			simpwrite(log,"获取栈帧错误\n");
			break;
		}
		// 正在调用的函数名字
		pfunctioninfo = (SYMBOL_INFO*)symbolbuffer;
		memset(pfunctioninfo, 0x0, SYMBOLBUFFERSIZE);
		pfunctioninfo->SizeOfStruct = sizeof(SYMBOL_INFO);
		pfunctioninfo->MaxNameLen = MAXSYMBOLNAMELENGTH;
		// 获取符号
#ifdef VIEWCALLONELINE
		if( SymFromAddr( hProcess, sf.AddrPC.Offset,&symDisplacement,pfunctioninfo ) )
		{
			if(k<=stepover)	//说明是被VIEWSTACK调用的
			{
				continue;
			}
			if(k==stepover+1)
			{
				SYSTEMTIME sys; 
				char timebuf[20]={0};
				GetLocalTime(&sys); 
#ifdef _MSC_VER
				sprintf_s(timebuf,sizeof(timebuf),"%02d:%02d:%02d.%03d",sys.wHour,sys.wMinute, sys.wSecond,sys.wMilliseconds);
#else
				sprintf(timebuf,"%02d:%02d:%02d.%03d",sys.wHour,sys.wMinute, sys.wSecond,sys.wMilliseconds);
#endif
				fwrite(timebuf,strlen(timebuf),1,log->file);
				fwrite("\t",1,1,log->file);
#ifdef DROP_CLASS_FLAG
				pmsg=strchr(pfunctioninfo->Name,':');
				if(pmsg!=NULL)
					simpwrite(log, "%s: CallStack {this",pmsg+2);
				else
					simpwrite(log, "%s: CallStack {this",pfunctioninfo->Name);
#else
				simpwrite(log, "%s: CallStack {this",pfunctioninfo->Name);
#endif
			}
			else
			{
#ifdef DROP_CLASS_FLAG
				pmsg=strchr(pfunctioninfo->Name,':');
				if(pmsg!=NULL)
					simpwrite(log, " => %s", pmsg+2);
				else
					simpwrite(log, " => %s", pfunctioninfo->Name);	
#else
				simpwrite(log, " => %s", pfunctioninfo->Name);	
#endif
			}
		}
		else
		{
			err=GetLastError();
			simpwrite(log, " => Unknown(err=%d)",err);
		}
#else
		if( SymFromAddr( hProcess, sf.AddrPC.Offset,&symDisplacement,pfunctioninfo ) )
		{
			if(k<=stepover)	//说明是被VIEWSTACK调用的
			{
				continue;
			}
			if(k==stepover+1)
			{
				simpwrite(log, "当前函数名:\t%s\n", pfunctioninfo->Name );
			}
			else
			{
				simpwrite(log, "父函数名:\t%s\n", pfunctioninfo->Name );
			}
		}
		else
		{
			err=GetLastError();
			simpwrite(log, "无效的函数名，错误代码:%d\n",err);
		}
#endif
		/* 获取行号及所在文件
		IMAGEHLP_LINE lineInfo = { sizeof(IMAGEHLP_LINE) };
		DWORD dwLineDisplacement;

		if( SymGetLineFromAddr( hProcess, sf.AddrPC.Offset, &dwLineDisplacement, &lineInfo ) )
		{
			printf( "[Source File : %s]\n", lineInfo.FileName ); 
			printf( "[Source Line : %u]\n", lineInfo.LineNumber ); 
		}
		else
		{
			printf( "SymGetLineFromAddr failed!\n" );
		}
		*/
	}
	/*
	if( SymCleanup( hProcess ) )
	{
		printf( "Cleanup dbghelp ok.\n" );
	}
	*/
#ifdef VIEWCALLONELINE
	simpwrite(log, "}\n");
#endif
	SymCleanup( hProcess );
#else
	return;
#endif
}

static unsigned long dumpcallstack( SimpleLog* log,int depth, void*lpEP)
{
#ifdef _MSC_VER	
	LPEXCEPTION_POINTERS lpEI=(LPEXCEPTION_POINTERS)lpEP;
	if(depth<=0)
		return EXCEPTION_EXECUTE_HANDLER;
	if(log==NULL)
		return EXCEPTION_EXECUTE_HANDLER;
	if(!log->isopen)
		return EXCEPTION_EXECUTE_HANDLER;
	dump_callstack( lpEI->ContextRecord,log,depth,1);
	return EXCEPTION_EXECUTE_HANDLER ;
#else
	return 0;
#endif
}
static unsigned long dumpcallstack2( SimpleLog* log,int depth, int stepover, void*lpEP)
{
#ifdef _MSC_VER		//如果当前是vs项目
	LPEXCEPTION_POINTERS lpEI=(LPEXCEPTION_POINTERS)lpEP;
	if(depth<=0)
		return EXCEPTION_EXECUTE_HANDLER;
	if(log==NULL)
		return EXCEPTION_EXECUTE_HANDLER;
	if(!log->isopen)
		return EXCEPTION_EXECUTE_HANDLER;
	dump_callstack( lpEI->ContextRecord,log,depth,stepover);
	return EXCEPTION_EXECUTE_HANDLER ;
#else
	return 0;
#endif
}
static void viewcallstack(SimpleLog* log,int depth)
{
#ifdef _MSC_VER	
	if(log==NULL)
		return;
	if(!log->isopen)
		return;
	if(depth<=0)
		return;
	__try
	{
		RaiseException(1,0,0,0);
	}
	__except(dumpcallstack2(log,depth,2,GetExceptionInformation()))
	{
		(0);
	}
#endif
}

void InitSimpleLog(SimpleLog* log)
{
	log->close=closelog;
	log->open=openlog;
	log->write=writelog;
	log->writebytes=writebytes;
	log->lwrite=lwritelog;
	log->viewcallstack=viewcallstack;
	log->dumpcallstack=dumpcallstack;
	log->isopen=0;
	log->file=NULL;		//日志文件
	log->msg_dup_count=0;
	log->prefix=0;
	log->pstr_prefix=NULL;
	memset(log->filepath,0,256);
	memset(log->last_msg,0,2048);
}
void MsgBoxEx(hWnd hwnd,const char* caption,const char *FormatMsg,...)
{
	char pmsg[2048]={0};
	char *pc=pmsg;
	va_list arg_ptr;
#ifdef _SILENT
	return;
#endif
	if(FormatMsg==NULL)
		return;
	va_start(arg_ptr,FormatMsg);	//已固定参数地址起点确定变参的内存起始地址。
	vsprintf(pmsg,FormatMsg,arg_ptr);
	va_end(arg_ptr);		// 要写的内容已经存在了pmsg中

	if(pmsg[0]=='!' && pmsg[1]=='!')
	{
#ifdef DROP_CLASS_FLAG
		char*p;
		p=strchr(pmsg,':');
		if(p!=NULL && p[0]==':' && p[1]==':')	//再次确定是带类名及函数名的
		{
			pc=p+2;
		}
		else if(p!=NULL && pmsg[0]=='!' && pmsg[1]=='!')	//说明是以!!开头，含有:字符，但不含::的字符串
		{
			pc=pmsg+2;
		}
		else						//说明不是以!!开头
		{
			pc=pmsg;
		}
#else
		pc+=2;
#endif
	}

	MessageBoxA((HWND)hwnd,pc,caption,MB_OK);
}



SimpleLog SimpleLogDefault={NULL,0,0,0,"","",NULL,NULL,closelog,writelog,lwritelog,writebytes,openlog,viewcallstack,dumpcallstack};
