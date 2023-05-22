//��6��
#ifndef _SIMPLELOG_H
#define _SIMPLELOG_H
#include <stdio.h>
#include <stdlib.h>
#define _SILENT					//����ʱ��ֹ��������
#define DROP_CLASS_FLAG			//msgbox2��WRITELOG2�������Զ���Ӻ�����ʱ��ȥ�����ܿ�ͷ������
//#define NOT_USE_SIMPLE_LOG	//�����ȥ����־��䣬��Ѹ��������
/*================================================================
	�ļ�˵����
	1.Ҫ��vc++��Ŀ��ʹ�ã���SimpleLog.c�ļ����Ҽ�,����,C/C++,Ԥ����ͷ��ѡ��ʹ��Ԥ����ͷ
	�ڰ���ͷ�ļ�ʱ��ʹ��
	extern "C" {
	#include "SimpleLog.h"
	};
	2.�Ƽ�ʹ�ú�ķ�ʽ������־��䣬��Ϊ��ʹ�ø����㣬���ܸ�ǿ��Ҳ������ͳһ���ƺ��޸�
	3.OPENLOG,CLOSELOG��FIX_WRITELOGΪ�����䣬���������������if�������ʱ��ע����{}������
	4.��������Ȼʹ��C��д������Ϊ������ͷ�ļ������⣬���Բ��������ڷ�Windows����
	5.����msgbox2��WRITELOG2��DUMPCALL��VIEWCALL�����ֻ�ܱ�֤��vs������������ʹ�ã�
	  ���ʹ����������������MinGW������ܱ��򻯻���ԣ�������ο���Ӧ�궨��
    --------------------------------------------------------------
    ��־ʹ�þ��� 
	ʹ�þ���1��д��־,c++��ʽ��:
	SimpleLog *log;
	log=new SimpleLog;
	InitSimpleLog(log);
	log->open(log,"C:\\123.log","a+");
	log->write(log,"%d:%s",123,"aaa");
	log->close(log);
	delete log;
	ʹ�þ���2��д��־,�귽ʽ����
	SimpleLog *log2;
	OPENLOG(log2,"C:\\123.log","a+");	
	WRITELOG(log2,"%d:%s",123,"aaa");	//����д��־���
	WRITELOG2(log2,"%d:%s",456,"bbb");	//��־����Զ�������ں�������
	SET_LOGPREFIX(log2,"LopPreFix:");	//����д��־ǰ׺
	FIX_WRITELOG(log2,"%d:%s",789,"ccc");	//����־���ǰ���ָ����ǰ׺
	CLOSELOG(log2);
	ʹ�þ���3���鿴�������ö�ջ����
	SimpleLog *log2;
	OPENLOG(log2,"C:\\123.log","a+");
	VIEWCALL(log2,6);					//����1�����������6Ϊ�鿴��ջ����
	__try								//����2
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
#pragma region ��Ϣ��
#ifndef msgbox
#define msgbox(hwnd,caption,strF,...) MsgBoxEx((hWnd)hwnd,caption,strF,__VA_ARGS__)
#endif
#pragma endregion
#pragma region ��־��������
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
#pragma region ��ǰ׺��д����
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
#pragma region ��չ����,��VS���뻷��֧��
#ifdef _MSC_VER		//���ʹ�õ���VS������ 
#ifndef msgbox2		//��Ϣ�������Զ�������ں�����
#define msgbox2(strF,...) MsgBoxEx(NULL,"��ʾ��","!!"##__FUNCTION__##"��\n"##strF,__VA_ARGS__)
#endif
#ifndef WRITELOG2	//д��־�������Զ�������ں�����
#define WRITELOG2(pLog,strF,...) pLog->write(pLog,"!!"##__FUNCTION__##": "##strF,__VA_ARGS__)
#endif
#ifndef VIEWCALL	//�鿴���ö�ջ������depthָ���鿴���ö�ջ���
#define VIEWCALL(pLog,depth) pLog->viewcallstack(pLog,depth)
#endif
#ifndef DUMPCALL	//�鿴���ö�ջ���������SEHʹ�ã�depthָ���鿴���ö�ջ���
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
#define VIEWCALL(pLog,depth) pLog->write(pLog,"����VS������,�޷��鿴�������ö�ջ")
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
	FILE *file;		//��־�ļ�
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
