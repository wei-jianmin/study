//第2版
#include "SimpleLog.h"
#include <Windows.h>
#include <IO.H>
#include <vadefs.h>
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
				t_f=st_file.wYear*500+st_file.wMonth*40+st_file.wDay;	//文件创建时间
				t_c=st_cpu.wYear*500+st_cpu.wMonth*40+st_cpu.wDay;		//电脑当前时间
				CloseHandle(hFile);
				if(t_c!=t_f)
				{
					log->file=fopen(path,"w+");	//清空文件内容
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
		
		sprintf_s(timebuf,sizeof(timebuf),"%02d:%02d:%02d.%03d",sys.wHour,sys.wMinute, sys.wSecond,sys.wMilliseconds);
		//写入时间
		l1=l2=l3=l4=0;
		l1=fwrite(timebuf,strlen(timebuf),1,log->file);
		l2=fwrite("\t",1,1,log->file);
		if(log->prefix)	//写前缀
		{	
			if(strlen(log->pstr_prefix)!=0)
				fwrite(log->pstr_prefix,strlen(log->pstr_prefix),1,log->file);
			log->prefix=0;
		}
		//写入传来的消息,如果传来的消息符合{Class::Func} msg格式，则转为Func: msg格式
		{
			char buf[2048]={0};
			size=(int)strlen(pmsg);
			if(size<2048)
			{
				char namebuf[128]={0};
				char *p;
				int len=-1;
				memcpy(buf,pmsg,size);
				p=strchr(buf,' ');		//如果消息中含有空格
				if(p!=NULL)
				{
					p[0]=0;				//buf中此时存了第一个空格之前的字符串
					len=strlen(buf);
					p=strchr(buf,':');
					//如果符合{Class::Func} msg格式
					if(buf[0]=='{' && buf[strlen(buf)-1]=='}' &&
						strlen(p)>0 && p[0]==':' && p[1]==':')
					{
						p+=2;
						memcpy(namebuf,p,strlen(p));
						memcpy(buf,namebuf,strlen(namebuf));
						buf[strlen(namebuf)-1]=':';
						memcpy(buf+strlen(namebuf),pmsg+len,strlen(pmsg)-strlen(namebuf));
					}
					else
					{
						memcpy(buf,pmsg,size);
					}
				}
				
				l3=fwrite(buf,strlen(buf),1,log->file);
			}
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

void InitSimpleLog(SimpleLog* log)
{
	log->close=closelog;
	log->open=openlog;
	log->write=writelog;
	log->isopen=0;
	log->file=NULL;		//日志文件
	log->msg_dup_count=0;
	log->prefix=0;
	log->pstr_prefix=NULL;
	memset(log->filepath,0,256);
	memset(log->last_msg,0,2048);
}
void testabc()
{
	int i;
	i=3;
}
SimpleLog SimpleLogDefault={NULL,0,0,0,"","",NULL,closelog,writelog,openlog};
