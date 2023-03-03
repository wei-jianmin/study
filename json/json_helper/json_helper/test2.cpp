#include <stdio.h>
#include <string>
#include <io.h>
#include <Windows.h>
#include <time.h>

__declspec(dllexport) int RAND_SEED;
__declspec(dllexport) void set_rand(int i)
{
	RAND_SEED = i;
}
_declspec(dllexport) int get_rand()
{
	RAND_SEED=(RAND_SEED*123+59)%65536;
	return RAND_SEED;
}
void func(int i)
{
	long handle;
	struct _finddata_t fileinfo;
	handle = _findfirst("C:/seal*",&fileinfo);
	if(handle!=-1)
	{
		do
		{
			printf("%s\n",fileinfo.name);
		}while(!_findnext(handle,&fileinfo));
	}
	
	puts("func int");
}
void func(double i)
{
	puts("func int");
}
void func(std::string s)
{
	puts("func string");
}
void func(bool b)
{
	puts("func bool");
}
void func(const char* p)
{
	puts("func string");
}
int main2()
{
	func("asdf");
	int t = time(NULL);
	int size = sizeof(int);
	size = sizeof(long);
	size = sizeof(short);
	size = sizeof(long long);
	set_rand(t%65536);
	for(int i=0;i<100;i++)
		printf("%d    ",get_rand());
	/*
	func(true);
	func(3);
	func("asdf");
	*/
	getchar();
	return 0;
}