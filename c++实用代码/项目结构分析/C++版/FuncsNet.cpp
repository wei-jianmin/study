#include "FuncsNet.h"
#include <memory.h>
#include <string.h>

int FuncsNet::ident=0;
int FuncsNet::initialed=0;
FILE * FuncsNet::file=NULL;
char FuncsNet::blanks[200]={0};
char FuncsNet::file_path[256]={0};
char FuncsNet::err_msg[256]={0};

#define min2(a, b)  (((a) < (b)) ? (a) : (b)) 

void FuncsNet::Initial(const char* path,const char* mode)
{
	file=fopen(path,mode);
	initialed=1;
	memcpy(file_path,path,strlen(path));
}
void FuncsNet::Initial(FILE *pfile)
{
	file=pfile;
	initialed=2;
}
void FuncsNet::UnInitial()
{
	if(initialed==1)
		fclose(file);
	initialed=0;
}
FILE *FuncsNet::GetFile()
{
	return file;
}
FuncsNet::FuncsNet(const char* info)
{
	if(initialed>0)
	{
		memset(func_info,0,1024);
		memcpy(func_info,info,min2(1024,strlen(info)));
		fwrite(blanks,ident*2,1,file);
		fwrite("<",1,1,file);
		fwrite(func_info,strlen(func_info),1,file);
		fwrite(">",1,1,file);
		fwrite("\n",1,1,file);
		fflush(file);
		ident++;
	}
	else if(initialed==0)
	{
		strcpy(err_msg,"haven't initialed!");
		initialed=-1;
	}
}

FuncsNet::~FuncsNet(void)
{
	if(initialed>0)
	{
		fwrite(blanks,ident*2,1,file);fflush(file);
		fwrite("</",2,1,file);fflush(file);
		fwrite(func_info,strlen(func_info),1,file);fflush(file);
		fwrite(">",1,1,file);fflush(file);
		fwrite("\n",1,1,file);
		fflush(file);
		ident--;
	}
}
