#include <stdio.h>
#include <dlfcn.h>
#include "log.h"
typedef void (*prunoes)(void);
int main()
{
	ver();
	puts("reader set subver=1");
	setver(1);
	ver();
	puts("--------------------------------------");
	puts("load oes");
	void* lib = dlopen("./liboes.so",RTLD_NOW);
	if(lib==NULL)
	{
		puts("load liboes.so faild");
		return 0;
	}
	prunoes f = (prunoes)dlsym(lib,"runoes");
	if(f == NULL)
	{
		puts("get func runoes in liboes.so faild");
		return 0;
	}
	f();
	puts("--------------------------------------");
	ver();
	puts("reader set subver=1");
	setver(1);
	ver();
	dlclose(lib);
	return 0;
}
	

	
