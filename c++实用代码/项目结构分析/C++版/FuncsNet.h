#pragma once
#include <stdio.h>
#define REGFUNC FuncsNet _funcsnet(__FUNCTION__)
class FuncsNet
{
public:
	FuncsNet(const char* info);
	~FuncsNet(void);
private:
	char func_info[1024];
	static int ident;
	static int initialed;
	static char file_path[256];
	static FILE *file;
	static char blanks[200];
	static char err_msg[256];
public:
	static void Initial(const char* path,const char* mode);
	static void Initial(FILE *pfile);
	static void UnInitial();
	static FILE* GetFile();
};
