#include "stdafx.h"
#include "SimpleLog.h"
#include <Windows.h>
#include <stdio.h>
#include <IO.H>
using namespace std;

bool CSimpleLog::prefix=false;
char* CSimpleLog::str_prefix=NULL;
CSimpleLog::CSimpleLog()
{
	isopen=false;
}
CSimpleLog::CSimpleLog(char *path,char* mode)
{
	isopen=false;
	if(path == NULL)
		return;
	msg_dup_count=0;	//�����ظ���Ϣ
	last_msg.empty();
	//���ļ�
	int a=_access(path,6);
	DWORD dw=GetLastError();
	if(a!=0)
	{
#ifndef _SILENT
		char buf[200]="���캯�����ļ������ڻ�û�ж�дȨ��\n";
		strcat(buf,path);
		MessageBox(NULL,buf,"����",MB_OK|MB_ICONHAND);
#endif
		return;
	}
		//֮ǰ�Ĳ����ܱ�֤�ļ��������ж�дȨ��
	if(strcmp("a+",mode)==0)
	{
		HANDLE hFile = CreateFileA(path, GENERIC_READ,          // open for reading
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
				ZeroMemory(&st_file, sizeof(SYSTEMTIME));
				FileTimeToSystemTime(&ftCreate, &st_file);
				GetLocalTime(&st_cpu);
				long t_f,t_c;
				t_f=st_file.wYear*500+st_file.wMonth*40+st_file.wDay;	//�ļ�����ʱ��
				t_c=st_cpu.wYear*500+st_cpu.wMonth*40+st_cpu.wDay;		//���Ե�ǰʱ��
				CloseHandle(hFile);
				if(t_c!=t_f)
				{
					file=fopen(path,"w+");	//����ļ�����
					fclose(file);
				}
			}
			else
				CloseHandle(hFile);
		}
	}
	file=fopen(path,mode);
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
#ifndef _SILENT
		char buffer[10];
		_itoa( dw, buffer, 16 );
		char buffer2[20]={"ErrNo=0x"};
		strcat(buffer2,buffer);
		char buffer3[40]="�ļ��򿪴���";
		strcat(buffer3,buffer2);
		MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
#endif
		return;
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
bool CSimpleLog::resetpath(char *path,char *mode/* ="a+" */)
{
	if(path == NULL)
		return false;
	if(isopen)
	{
		char buf[50]="----------------write finish----------------\n\n";
		fwrite(buf,strlen(buf),1,file);
		fclose(file);
	}
	isopen=false;
	msg_dup_count=0;	//�����ظ���Ϣ
	last_msg.empty();
	//���ļ�
	int a=_access(path,6);
	DWORD dw=GetLastError();
	if(a!=0)
	{
#ifndef _SILENT
		char buf[200]="���캯�����ļ������ڻ�û�ж�дȨ��\n";
		strcat(buf,path);
		MessageBox(NULL,buf,"����",MB_OK|MB_ICONHAND);
#endif
		return false;
	}
	//֮ǰ�Ĳ����ܱ�֤�ļ��������ж�дȨ��
	if(strcmp("a+",mode)==0)	//������ø���ģʽ�򿪣���������������ļ���ʱ����
	{
		HANDLE hFile = CreateFileA(path, GENERIC_READ,          // open for reading
			FILE_SHARE_READ,       // share for reading
			NULL,                            // default security
			OPEN_EXISTING,          // existing file only
			FILE_FLAG_BACKUP_SEMANTICS , // normal file
			NULL);
		if(hFile!=NULL)
		{
			SYSTEMTIME st_file,st_cpu;
			FILETIME ftCreate, ftModify, ftAccess;
			if (GetFileTime(hFile, &ftCreate, &ftAccess, &ftModify))	//��ȡ�ļ�����ʱ��
			{
				ZeroMemory(&st_file, sizeof(SYSTEMTIME));
				FileTimeToSystemTime(&ftCreate, &st_file);
				GetLocalTime(&st_cpu);
				long t_f,t_c;
				t_f=st_file.wYear*500+st_file.wMonth*40+st_file.wDay;	//�ļ���������
				t_c=st_cpu.wYear*500+st_cpu.wMonth*40+st_cpu.wDay;		//���Ե�ǰ����
				CloseHandle(hFile);
				if(t_c!=t_f)
				{
					file=fopen(path,"w+");	//����ļ�����
					fclose(file);
				}
			}
			else
				CloseHandle(hFile);
		}
	}
	file=fopen(path,mode);
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
		return true;
	}
	else
	{
#ifndef _SILENT
		char buffer[10];
		_itoa( dw, buffer, 16 );
		char buffer2[20]={"ErrNo=0x"};
		strcat(buffer2,buffer);
		char buffer3[40]="�ļ��򿪴���";
		strcat(buffer3,buffer2);
		MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
#endif
		return false;
	}
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
				l=fwrite("same as above ......\t",21,1,file);	//д21���ֽ�
				DWORD dw=GetLastError();
				fflush(file);
				if(l!=1)
				{
#ifndef _SILENT
					char buffer[10];
					_itoa( dw, buffer, 16 );
					char buffer2[20]={"ErrNo=0x"};
					strcat(buffer2,buffer);
					char buffer3[40]="�ļ�д�����";
					strcat(buffer3,buffer2);
					MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
#endif
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
#ifndef _SILENT
				char buffer[10];
				_itoa( dw, buffer, 16 );
				char buffer2[20]={"ErrNo=0x"};
				strcat(buffer2,buffer);
				char buffer3[40]="�ļ�д�����";
				strcat(buffer3,buffer2);
				MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
#endif
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
		if(prefix)	//дǰ׺
		{	
			if(str_prefix !=NULL)
				fwrite(str_prefix,strlen(str_prefix),1,file);
			prefix=false;
		}
		//д�봫������Ϣ
		int size=(int)strlen(pmsg);
		l3=fwrite(pmsg,size+1,1,file);
		l4=fwrite("\n",1,1,file);
		DWORD dw=GetLastError();
		fflush(file);
		if(dw !=0 && l1*l2*l3*l4!=1)
		{
#ifndef _SILENT
			char buffer[10];
			_itoa( dw, buffer, 16 );
			char buffer2[20]={"ErrNo=0x"};
			strcat(buffer2,buffer);
			char buffer3[40]="�ļ�д�����";
			strcat(buffer3,buffer2);
			MessageBox(NULL,buffer3,"����",MB_OK|MB_ICONHAND);
			MessageBox(NULL,pmsg,"д��������Ϣ:",MB_OK|MB_ICONHAND);
#endif
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
#ifndef _SILENT
		char buf[200]="��̬clear���ļ������ڻ�û�ж�дȨ��\n";
		strcat(buf,path);
		MessageBox(NULL,buf,"����",MB_OK|MB_ICONHAND);
#endif
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
		if(prefix)	//дǰ׺
		{	
			if(str_prefix !=NULL)
				fwrite(str_prefix,strlen(str_prefix),1,file);
			prefix=false;
		}
		fwrite(timebuf,strlen(timebuf),1,file);
		fwrite("\n",1,1,file);
		fclose(file);
		return true;
	}
	return false;
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
	vsprintf(buf,info,arg_ptr);	//vswprintf
	va_end(arg_ptr);
	return write(path,buf);
}

char* CSimpleLog::WcharToChar(wchar_t* wc)//���ֽ�ת���ֽ� 
{
	int len= WideCharToMultiByte(CP_ACP,0,wc,wcslen(wc),NULL,0,NULL,NULL);   
	char* m_char=new char[len+1];   
	WideCharToMultiByte(CP_ACP,0,wc,wcslen(wc),m_char,len,NULL,NULL);   
	m_char[len]='\0';   
	return m_char;  
}

bool CSimpleLog::write(wchar_t *path,wchar_t *info)
{
	char *p1=WcharToChar(path);
	char *p2=WcharToChar(info);
	bool b=writex(p1,p2);
	delete[] p1;
	delete[] p2;
	return b;
}
bool CSimpleLog::writelog(wchar_t *pmsg)
{
	char *p1=WcharToChar(pmsg);
	bool b=writelog(p1);
	delete[] p1;
	return true;
}

bool CSimpleLog::writex(wchar_t * path,wchar_t * info,...)
{
	if(path==NULL)
		return false;
	wchar_t buf[2048]={0};
	va_list arg_ptr;
	va_start(arg_ptr,info);	//�ѹ̶�������ַ���ȷ����ε��ڴ���ʼ��ַ��
	vswprintf(buf,info,arg_ptr);	//
	va_end(arg_ptr);
	return write(path,buf);
}

bool CSimpleLog::writelogx(wchar_t *format,...)
{
	if(!isopen)
		return false;
	if(format==NULL)
		return false;
	wchar_t buf[2048]={0};
	va_list arg_ptr;
	va_start(arg_ptr,format);	//�ѹ̶�������ַ���ȷ����ε��ڴ���ʼ��ַ��
	vswprintf(buf,format,arg_ptr);
	va_end(arg_ptr);
	return writelog(buf);
}