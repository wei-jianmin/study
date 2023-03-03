#include "stdafx.h"
#include "SimpleLog.h"
#include <Windows.h>
#include <stdio.h>
#include <IO.H>
using namespace std;

CSimpleLog::CSimpleLog(char *path)
{
	isopen=false;
	if(path == NULL)
		return;
	msg_dup_count=0;
	last_msg.empty();
	//���ļ�
	int a=_access(path,6);
	DWORD dw=GetLastError();
	if(a!=0)
	{
		char buf[200]="���캯�����ļ������ڻ�û�ж�дȨ��\n";
		strcat(buf,path);
		MessageBox(NULL,buf,"����",MB_OK|MB_ICONHAND);
		return;
	}
	file=fopen(path,"w+");
	dw=GetLastError();
	if(file !=NULL)
	{
		isopen=true;
		//д��ʱ��
		char timebuf[20]={0};
		SYSTEMTIME sys; 
		GetLocalTime(&sys); 
		strcpy_s(timebuf,"----------------");
		fwrite(timebuf,strlen(timebuf),1,file);
		memset(timebuf,0,sizeof(timebuf));
		sprintf_s(timebuf,sizeof(timebuf),"%04d-%02d-%02d",sys.wYear,sys.wMonth, sys.wDay);
		fwrite(timebuf,strlen(timebuf),1,file);
		memset(timebuf,0,sizeof(timebuf));
		strcpy_s(timebuf,"----------------");
		fwrite(timebuf,strlen(timebuf),1,file);
		fwrite("\n",1,1,file);
		return;
	}
	else
	{
		char buffer[10];
		_itoa( dw, buffer, 16 );
		char buffer2[20]={"ErrNo=0x"};
		strcat(buffer2,buffer);
		char buffer3[40]="�ļ��򿪴���";
		strcat(buffer3,buffer2);
		MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
	}

}
CSimpleLog::~CSimpleLog()
{
	if(isopen)
	{
		char buf[50]="----------------write finish----------------\n\n";
		fwrite(buf,strlen(buf),1,file);
		fclose(file);
	}
	isopen=false;
	return;
}
bool CSimpleLog::writelog(char *pmsg)
{
	if(!isopen)
		return false;
	if(isopen)
	{
		if(last_msg.compare(pmsg)==0)		//��Ϣ�����ظ�
		{
			msg_dup_count++;				//��¼��Ϣ�ظ�����
			if(msg_dup_count==1)			//��Ϣ�ظ�һ��
			{
				size_t l=0;
				l=fwrite("\t......  ",9,1,file);	//д6���ֽ�
				DWORD dw=GetLastError();
				fflush(file);
				if(l!=1)
				{
					char buffer[10];
					_itoa( dw, buffer, 16 );
					char buffer2[20]={"ErrNo=0x"};
					strcat(buffer2,buffer);
					char buffer3[40]="�ļ�д�����";
					strcat(buffer3,buffer2);
					MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
					return false;
				}
				return true;
			}
			else if(msg_dup_count>1)		//��Ϣ�ظ���Σ�����д����־
			{
				return true;
			}
		}
		else if(msg_dup_count>0)			//��Ϣ֮ǰ�ظ��������ڲ��ظ���
		{
			fwrite("repeated times=",16,1,file);		//д16���ֽ�
			char buf[5];
			size_t l1=0,l2=0;
			_itoa( msg_dup_count, buf, 5);
			l1=fwrite(buf,strlen(buf)+1,1,file);
			l2=fwrite("\n",1,1,file);
			DWORD dw=GetLastError();
			fflush(file);
			msg_dup_count=0;				//�ظ�������0
			if(dw !=0 && l1*l2!=1)
			{
				char buffer[10];
				_itoa( dw, buffer, 16 );
				char buffer2[20]={"ErrNo=0x"};
				strcat(buffer2,buffer);
				char buffer3[40]="�ļ�д�����";
				strcat(buffer3,buffer2);
				MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
				return false;
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
		char timebuf[20]={0};
		SYSTEMTIME sys; 
		GetLocalTime(&sys); 
		sprintf_s(timebuf,sizeof(timebuf),"%02d:%02d:%02d.%03d",sys.wHour,sys.wMinute, sys.wSecond,sys.wMilliseconds);
		//д��ʱ��
		size_t l1,l2,l3,l4;
		l1=l2=l3=l4=0;
		l1=fwrite(timebuf,strlen(timebuf),1,file);
		l2=fwrite("\t",1,1,file);
		//д�봫������Ϣ
		int size=(int)strlen(pmsg);
		l3=fwrite(pmsg,size+1,1,file);
		l4=fwrite("\n",1,1,file);
		DWORD dw=GetLastError();
		fflush(file);
		if(dw !=0 && l1*l2*l3*l4!=1)
		{
			char buffer[10];
			_itoa( dw, buffer, 16 );
			char buffer2[20]={"ErrNo=0x"};
			strcat(buffer2,buffer);
			char buffer3[40]="�ļ�д�����";
			strcat(buffer3,buffer2);
			MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
			MessageBox(NULL,pmsg,"д��������Ϣ:",MB_OK|MB_ICONHAND);
			return false;
		}
		last_msg=pmsg;
		return true;
	}
	return false;
}


bool CSimpleLog::writelogx(char *format,...)
{
	if(!isopen)
		return false;
	if(format==NULL)
		return false;
	char buf[2048]={0};
	va_list arg_ptr;
	va_start(arg_ptr,format);	//�ѹ̶�������ַ���ȷ����ε��ڴ���ʼ��ַ��
	vsprintf(buf,format,arg_ptr);
	va_end(arg_ptr);
	return writelog(buf);
}
bool CSimpleLog::clear()
{
	return false;
}
bool CSimpleLog::clear(char*path)
{
	if(path==NULL)
		return false;
	int a=_access(path,6);
	DWORD dw=GetLastError();
	if(a!=0)
	{
		char buf[200]="��̬clear���ļ������ڻ�û�ж�дȨ��\n";
		strcat(buf,path);
		MessageBox(NULL,buf,"����",MB_OK|MB_ICONHAND);
		return false;
	}
	FILE *file;
	file=fopen(path,"w+");
	if(file!=NULL)
	{
		fclose(file);
		return true;
	}
	else
		return false;
}
bool CSimpleLog::write(char *path,char *info)
{
	if(path == NULL || info==NULL)
		return false;
	//���ļ�
	int a=_access(path,6);
	DWORD dw=GetLastError();
	if(a!=0)
	{
		//char buf[200]="��̬write���ļ������ڻ�û�ж�дȨ��\n";
		//strcat(buf,path);
		//MessageBox(NULL,buf,"����",MB_OK|MB_ICONHAND);
		return false;
	}
	FILE *file;
	file=fopen(path,"a+");
	dw=GetLastError();
	if(file !=NULL)
	{
		//д��ʱ��
		char timebuf[2048]={0};
		SYSTEMTIME sys; 
		GetLocalTime(&sys); 
		//sprintf_s(timebuf,sizeof(timebuf),"%04d-%02d-%02d",sys.wYear,sys.wMonth, sys.wDay);
		sprintf_s(timebuf,sizeof(timebuf),"%02d:%02d:%02d.%03d\t%s",sys.wHour,sys.wMinute, sys.wSecond,sys.wMilliseconds,info);
		fwrite(timebuf,strlen(timebuf),1,file);
		fwrite("\n",1,1,file);
		fclose(file);
		return true;
	}
// 	else
// 	{
// 		char buffer[10];
// 		_itoa( dw, buffer, 16 );
// 		char buffer2[20]={"ErrNo=0x"};
// 		strcat(buffer2,buffer);
// 		char buffer3[40]="�ļ��򿪴���";
// 		strcat(buffer3,buffer2);
// 		MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
// 	}
}
bool CSimpleLog::writex(char * path,char * info,...)
{
	if(path==NULL)
		return false;
	char buf[2048]={0};
	va_list arg_ptr;
	va_start(arg_ptr,info);	//�ѹ̶�������ַ���ȷ����ε��ڴ���ʼ��ַ��
	vsprintf(buf,info,arg_ptr);
	va_end(arg_ptr);
	return write(path,buf);
}