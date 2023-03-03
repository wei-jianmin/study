//��5��
#include "SimpleLog.h"
#include <Windows.h>
#include <IO.H>
#include <vadefs.h>
#include <dbghelp.h>	//����֧�ֲ鿴�������ö�ջ
#pragma comment( lib, "dbghelp.lib" )


static int openlog(SimpleLog* log,const char *path,const char* mode)
{
	int a;
	unsigned long dw;
	if(log==NULL)
		return 0;
	log->isopen=0;
	if(path == NULL)
		return 0;
	log->msg_dup_count=0;	//�����ظ���Ϣ
	memset(log->last_msg,0,2048);
	//���ļ�
	a=_access(path,6);
	dw=GetLastError();
	if(a!=0)
	{
#ifndef _SILENT
		char buf[200]="���캯�����ļ������ڻ�û�ж�дȨ��\n";
		strcat(buf,path);
		MessageBox(NULL,buf,"����",MB_OK|MB_ICONHAND);
#endif
		return 0;
	}
	strcpy(log->filepath,path);
	//֮ǰ�Ĳ����ܱ�֤�ļ��������ж�дȨ��
	if(strcmp("a+",mode)==0)
	{
		HANDLE hFile;
		hFile = CreateFileA(path, GENERIC_READ,          // open for reading
			FILE_SHARE_READ,       // share for reading
			NULL,                            // default security
			OPEN_EXISTING,          // existing file only
			FILE_FLAG_BACKUP_SEMANTICS , // normal file
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
				t_f=st_file.wYear*500+st_file.wMonth*40+st_file.wDay;	//�ļ�����ʱ��
				t_c=st_cpu.wYear*500+st_cpu.wMonth*40+st_cpu.wDay;		//���Ե�ǰʱ��
				CloseHandle(hFile);
				if(t_c!=t_f)
				{
					log->file=fopen(path,"w+");	//����ļ�����
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
		//д��ʱ��
		GetLocalTime(&sys); 
		strcpy(timebuf,"----------------");
		fwrite(timebuf,strlen(timebuf),1,log->file);
		memset(timebuf,0,sizeof(timebuf));
		sprintf_s(timebuf,sizeof(timebuf),"%04d-%02d-%02d",sys.wYear,sys.wMonth, sys.wDay);
		fwrite(timebuf,strlen(timebuf),1,log->file);
		memset(timebuf,0,sizeof(timebuf));
		strcpy(timebuf,"----------------");
		fwrite(timebuf,strlen(timebuf),1,log->file);
		fwrite("\n",1,1,log->file);
		return 0;
	}
	else
	{
#ifndef _SILENT
		char buffer[10];
		char buffer2[20]={"ErrNo=0x"};
		char buffer3[40]="�ļ��򿪴���";
		_itoa( dw, buffer, 16 );	
		strcat(buffer2,buffer);
		strcat(buffer3,buffer2);
		MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
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
	
	va_start(arg_ptr,format);	//�ѹ̶�������ַ���ȷ����ε��ڴ���ʼ��ַ��
	vsprintf(pmsg,format,arg_ptr);
	va_end(arg_ptr);		// Ҫд�������Ѿ�������pmsg��

	if(log->isopen)
	{
		//if(log->last_msg.compare(pmsg)==0)		//��Ϣ�����ظ�
		int len=min(2048,strlen(pmsg)+1);
		char timebuf[20]={0};
		SYSTEMTIME sys; 
		unsigned int l1,l2,l3,l4;
		unsigned long dw=0;
		int size=0;
		GetLocalTime(&sys); 
		if(strncmp(log->last_msg,pmsg,len)==0)
		{
			log->msg_dup_count++;				//��¼��Ϣ�ظ�����
			if(log->msg_dup_count==1)			//��Ϣ�ظ�һ��
			{
				unsigned int l=0;
				unsigned long dw=0;
				l=fwrite("same as above ......\n",21,1,log->file);	//д21���ֽ�
				dw=GetLastError();
				fflush(log->file);
				if(l!=1)
				{
#ifndef _SILENT
					char buffer[10];
					char buffer2[20]={"ErrNo=0x"};
					char buffer3[40]="�ļ�д�����";
					_itoa( dw, buffer, 16 );
					strcat(buffer2,buffer);
					strcat(buffer3,buffer2);
					MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
#endif
					return 0;
				}
				return 0;
			}
			else if(log->msg_dup_count>1)		//��Ϣ�ظ���Σ�����д����־
			{
				return 0;
			}
		}
		else if(log->msg_dup_count>0)			//��Ϣ֮ǰ�ظ��������ڲ��ظ���
		{
			char buf[5];
			unsigned long dw=0;
			unsigned int l1=0,l2=0;
			fwrite("repeated times=",16,1,log->file);		//д16���ֽ�
			_itoa( log->msg_dup_count, buf, 5);
			l1=fwrite(buf,strlen(buf)+1,1,log->file);
			l2=fwrite("\n",1,1,log->file);
			dw=GetLastError();
			fflush(log->file);
			log->msg_dup_count=0;				//�ظ�������0
			if(dw !=0 && l1*l2!=1)
			{
#ifndef _SILENT
				char buffer[10];
				char buffer2[20]={"ErrNo=0x"};
				char buffer3[40]="�ļ�д�����";
				_itoa( dw, buffer, 16 );
				strcat(buffer2,buffer);
				strcat(buffer3,buffer2);
				MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
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
		
		//��Ϣ��Ϊ�գ�д��ʱ��
		if(strlen(pmsg)>0)
		{
			sprintf_s(timebuf,sizeof(timebuf),"%02d:%02d:%02d.%03d",sys.wHour,sys.wMinute, sys.wSecond,sys.wMilliseconds);
			l1=l2=l3=l4=0;
			l1=fwrite(timebuf,strlen(timebuf),1,log->file);
			l2=fwrite("\t",1,1,log->file);
		}
		
		if(log->prefix)	//дǰ׺
		{	
			if(strlen(log->pstr_prefix)!=0)
				fwrite(log->pstr_prefix,strlen(log->pstr_prefix),1,log->file);
			log->prefix=0;
		}
		//д�봫������Ϣ,�����������Ϣ����!!Class::Func msg��ʽ����תΪFunc: msg��ʽ
		{
			char *pm=pmsg;
			if(pm[0]=='!' && pm[1]=='!')	//����ȷ���Ǵ���������������
			{
#ifdef DROP_CLASS_FLAG
				pm=strchr(pmsg,':');
				if(pm!=NULL && pm[1]==':')	//�ٴ�ȷ���Ǵ���������������
				{
					pm+=2;					//pmָ������
				}
				else if(pm==NULL)			//˵������!!��ͷ��������::���ַ��������Բ���!!Class::Func msg��ʽ
					pm=pmsg;
#else
				pm+=2;
#endif
				fwrite(pm,strlen(pm),1,log->file);
			}
			else
				fwrite(pmsg,strlen(pmsg),1,log->file);
			l4=fwrite("\n",1,1,log->file);			//����
		}
		dw=GetLastError();
		fflush(log->file);
		if(dw !=0 && l1*l2*l3*l4!=1)
		{
#ifndef _SILENT
			char buffer[10];
			char buffer2[20]={"ErrNo=0x"};
			char buffer3[40]="�ļ�д�����";
			_itoa( dw, buffer, 16 );
			strcat(buffer2,buffer);
			strcat(buffer3,buffer2);
			MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
			MessageBox(NULL,pmsg,"д��������Ϣ:",MB_OK|MB_ICONHAND);
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
			return 0;
		if(format==NULL)
			return 0;

		va_start(arg_ptr,format);	//�ѹ̶�������ַ���ȷ����ε��ڴ���ʼ��ַ��
		vsprintf(pmsg,format,arg_ptr);
		va_end(arg_ptr);		// Ҫд�������Ѿ�������pmsg��

		fwrite(pmsg,strlen(pmsg),1,log->file);
		fwrite("\n",1,1,log->file);
		err=GetLastError();
		fflush(log->file);
		if(err !=0)
		{
#ifndef _SILENT
			char buffer[10];
			char buffer2[20]={"ErrNo=0x"};
			char buffer3[40]="�ļ�д�����";
			_itoa( dw, buffer, 16 );
			strcat(buffer2,buffer);
			strcat(buffer3,buffer2);
			MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
			MessageBox(NULL,pmsg,"д��������Ϣ:",MB_OK|MB_ICONHAND);
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
/*
	depth��stepover֮������ĺ�������
*/
static void dump_callstack( CONTEXT *context ,SimpleLog* log,int depth,int stepover)
{
	STACKFRAME sf;
	DWORD machineType = IMAGE_FILE_MACHINE_I386/*IMAGE_FILE_MACHINE_IA64*/;
	DWORD err;
	HANDLE hProcess;
	HANDLE hThread;
	int k;
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
		simpwrite(log,"\t�������ö�ջ�����");
	}
	else
	{
		simpwrite(log,"\t��ʼ��dbghelpʧ�ܣ��޷��鿴�������ö�ջ");
		return;
	}

	for(k=1;k<=depth+stepover;k++)
	{
		unsigned char       symbolbuffer [SYMBOLBUFFERSIZE];
		SYMBOL_INFO        *pfunctioninfo;
		// ƫ���� 
		DWORD64 symDisplacement;
		// ��ȡ��һ��ջ֡
		if( !StackWalk(machineType, hProcess, hThread, &sf, context, 0, SymFunctionTableAccess, SymGetModuleBase, 0 ) )
		{
			simpwrite(log,"\t��ȡջ֡ʧ��");
			break;
		}
		// ���֡����ȷ�� 
		if( sf.AddrFrame.Offset == 0 )
		{
			simpwrite(log,"\t��ȡջ֡����");
			break;
		}
		// ���ڵ��õĺ�������
		pfunctioninfo = (SYMBOL_INFO*)symbolbuffer;
		memset(pfunctioninfo, 0x0, SYMBOLBUFFERSIZE);
		pfunctioninfo->SizeOfStruct = sizeof(SYMBOL_INFO);
		pfunctioninfo->MaxNameLen = MAXSYMBOLNAMELENGTH;
		// ��ȡ���� 
		if( SymFromAddr( hProcess, sf.AddrPC.Offset,&symDisplacement,pfunctioninfo ) )
		{
			if(k<=stepover)	//˵���Ǳ�VIEWSTACK���õ�
			{
				continue;
			}
			if(k==stepover+1)
			{
				simpwrite(log, "\t��ǰ������:\t%s", pfunctioninfo->Name );
			}
			else
			{
				simpwrite(log, "\t��������:\t%s", pfunctioninfo->Name );
			}
		}
		else
		{
			err=GetLastError();
			simpwrite(log, "\t��Ч�ĺ��������������:%d",err);
		}

		/* ��ȡ�кż������ļ�
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
	SymCleanup( hProcess );
}

static unsigned long dumpcallstack( SimpleLog* log,int depth, void*lpEP)
{
	LPEXCEPTION_POINTERS lpEI=(LPEXCEPTION_POINTERS)lpEP;
	if(depth<=0)
		return EXCEPTION_EXECUTE_HANDLER;
	if(log==NULL)
		return EXCEPTION_EXECUTE_HANDLER;
	if(!log->isopen)
		return EXCEPTION_EXECUTE_HANDLER;
	dump_callstack( lpEI->ContextRecord,log,depth,1);
	return EXCEPTION_EXECUTE_HANDLER ;
}
static unsigned long dumpcallstack2( SimpleLog* log,int depth, int stepover, void*lpEP)
{
	LPEXCEPTION_POINTERS lpEI=(LPEXCEPTION_POINTERS)lpEP;
	if(depth<=0)
		return EXCEPTION_EXECUTE_HANDLER;
	if(log==NULL)
		return EXCEPTION_EXECUTE_HANDLER;
	if(!log->isopen)
		return EXCEPTION_EXECUTE_HANDLER;
	dump_callstack( lpEI->ContextRecord,log,depth,stepover);
	return EXCEPTION_EXECUTE_HANDLER ;
}
static void viewcallstack(SimpleLog* log,int depth)
{
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
}

void InitSimpleLog(SimpleLog* log)
{
	log->close=closelog;
	log->open=openlog;
	log->write=writelog;
	log->viewcallstack=viewcallstack;
	log->dumpcallstack=dumpcallstack;
	log->isopen=0;
	log->file=NULL;		//��־�ļ�
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
		return 0;
	va_start(arg_ptr,FormatMsg);	//�ѹ̶�������ַ���ȷ����ε��ڴ���ʼ��ַ��
	vsprintf(pmsg,FormatMsg,arg_ptr);
	va_end(arg_ptr);		// Ҫд�������Ѿ�������pmsg��

	if(pmsg[0]=='!' && pmsg[1]=='!')
	{
#ifdef DROP_CLASS_FLAG
		char*p;
		p=strchr(pmsg,':');
		if(p!=NULL && p[0]==':' && p[1]==':')
		{
			pc=p+2;
		}
#else
		pc+=2;
#endif
	}

	MessageBox(hwnd,pc,caption,MB_OK);
}



SimpleLog SimpleLogDefault={NULL,0,0,0,"","",NULL,closelog,writelog,openlog,viewcallstack,dumpcallstack};
