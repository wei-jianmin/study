#pragma once
#include <stdio.h>
#include <stdlib.h>

#ifndef OPENLOGF
#define OPENLOGF(pLog,path,mode) pLog=(FuncsNet*)malloc(sizeof(FuncsNet)),InitialFuncsNet(pLog),pLog->OpenLog(pLog,path,mode)
#endif
#ifndef REGFUNC
#define REGFUNC(pLog) if(pLog) pLog->RegFunc(pLog,__FUNCTION__)
#endif
#ifndef CLOSELOGF
#define CLOSELOGF(pLog) if(pLog) pLog->CloseLog(pLog),free(pLog),pLog=NULL
#endif
typedef struct NameStack_tag
{
	char name_buf[40][50];
	int index;				//ָ��name_buf�Ŀ�дλ��
} NameStack;
typedef struct FuncsNet_tag
{
	char func_info[1024];	//��д�ļ�����Ϣ
	int ident;				//��ǰ�����Ĳ㼶
	int initialed;			//�ṹ���Ƿ��Ѿ���ʼ�����
	int logopened;			//��־�ļ��򿪱��
	char file_path[256];	//��־�ļ�·��
	FILE *file;				//��־�ļ�ָ��
	char blanks[256];
	char err_msg[256];		//������Ϣ
	NameStack names;		//��¼����������ʷ·��
	int delegatecall;		//������ò㼶��Ŀǰֻ֧��һ���������
	void (*OpenLog)(struct FuncsNet_tag *pThis,const char* path,const char* mode);
	void (*CloseLog)(struct FuncsNet_tag *pThis);
	void (*RegFunc)(struct FuncsNet_tag *pThis,const char* info);
} FuncsNet;
void InitialFuncsNet(FuncsNet *pthis);