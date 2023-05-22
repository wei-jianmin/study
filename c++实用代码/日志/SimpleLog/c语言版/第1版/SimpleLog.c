//��1��
#include "SimpleLog.h"
#include <Windows.h>
#include <IO.H>
#include <stdarg.h>		//��VC��ʹ��ʱ����Ҫ�������ļ� 
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
		
		if(strncmp(log->last_msg,pmsg,len)==0)
		{
			log->msg_dup_count++;				//��¼��Ϣ�ظ�����
			if(log->msg_dup_count==1)			//��Ϣ�ظ�һ��
			{
				unsigned int l=0;
				unsigned long dw=0;
				l=fwrite("\t\tsame as above ......\n",23,1,log->file);	//д21���ֽ�
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
			fwrite("\t\trepeated times=",18,1,log->file);		//д16���ֽ�
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
		GetLocalTime(&sys); 
		sprintf_s(timebuf,sizeof(timebuf),"%02d:%02d:%02d.%03d",sys.wHour,sys.wMinute, sys.wSecond,sys.wMilliseconds);
		//д��ʱ��
		l1=l2=l3=l4=0;
		l1=fwrite(timebuf,strlen(timebuf),1,log->file);
		l2=fwrite("\t",1,1,log->file);
		if(log->prefix)	//дǰ׺
		{	
			if(strlen(log->str_prefix)!=0)
				fwrite(log->str_prefix,strlen(log->str_prefix),1,log->file);
			log->prefix=0;
		}
		//д�봫������Ϣ
		size=(int)strlen(pmsg);
		l3=fwrite(pmsg,size+1,1,log->file);
		l4=fwrite("\n",1,1,log->file);
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
static void setlogprefix(SimpleLog* log,char* prefix)
{
	memset(log->str_prefix,0,128);
	memcpy(log->str_prefix,prefix,min(128,strlen(prefix)+1));
}
static void unsetlogprefix(SimpleLog* log)
{
	memset(log->str_prefix,0,128);
}
void InitSimpleLog(SimpleLog* log)
{
	log->close=closelog;
	log->open=openlog;
	log->write=writelog;
	log->setprefix=setlogprefix;
	log->unsetprefix=unsetlogprefix;
	log->isopen=0;
	log->file=NULL;		//��־�ļ�
	log->msg_dup_count=0;
	log->prefix=0;
	memset(log->str_prefix,0,128);
}

void SimpleMsgbox(const char* caption,const char *format,...)
{
	char pmsg[2048]={0};
	va_list arg_ptr;
	va_start(arg_ptr,format);	//�ѹ̶�������ַ���ȷ����ε��ڴ���ʼ��ַ��
	vsprintf(pmsg,format,arg_ptr);
	va_end(arg_ptr);		// Ҫд�������Ѿ�������pmsg��
	MessageBoxA(NULL,pmsg,caption,MB_OK);
}

SimpleLog SimpleLogDefault={NULL,0,0,0,"","",closelog,unsetlogprefix,setlogprefix,writelog,openlog};