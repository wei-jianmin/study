#include <Windows.h>
#include "IDictionary.h"

#define DLLADDR L"D:\\Documents\\Visual Studio 2005\\Projects\\Dictionary\\debug\\Dictionary.dll"
#define msg(s) MessageBoxA(NULL,s,"call dll func:",MB_OK)

int main()
{
	typedef void* (*pfun)();			//定义指向dll中函数的函数指针
	HINSTANCE hlib = LoadLibrary(DLLADDR);
	if(!hlib)
	{
	   msg("加载库失败");
	   return -1;
	}
	pfun fun = (pfun)GetProcAddress(hlib,"func");
	if(!fun)
	{
	   msg("获取导出函数失败");
	   return -1;
	}
	//-----------------------------------------------------------
	IDictionary *pD;
	pD=(IDictionary *)fun();
	if(pD)
	{
		pD->Initialize();
		
		pD->InsertWord();
		pD->LookupWord();
		pD->DeleteWord();

		pD->RestoreLibrary();
		pD->FreeLibrary();
	}
	//-------原始的调用方式--------
	typedef void (*pfun2)();
	ULONG *pv;
	pv=(ULONG*)fun();
	if(pv)
	{
		ULONG vtAddr = (ULONG)(*pv);	//虚函数表的地址
		pfun2 p;
		p=(pfun2)(*(ULONG*)vtAddr);	//取出虚函数表中前4个字节的内容,即Initialize的地址
		p();
		p=(pfun2)(*(ULONG*)(vtAddr+4));	//取出虚函数表中第4到8字节的内容，即Loadlibrary的地址
		p();
		p=(pfun2)(*(ULONG*)(vtAddr+8));	//InsertWord
		p();
		p=(pfun2)(*(ULONG*)(vtAddr+12));	//DeleteWord
		p();
		p=(pfun2)(*(ULONG*)(vtAddr+16));	//LookupWord
		p();
	}
	//-----------------------------------------------------------
	FreeLibrary(hlib);
}