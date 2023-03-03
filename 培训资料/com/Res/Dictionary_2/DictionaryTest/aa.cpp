#include <Windows.h>
#include "IDictionary.h"

#define DLLADDR L"D:\\Documents\\Visual Studio 2005\\Projects\\Dictionary\\debug\\Dictionary.dll"
#define msg(s) MessageBoxA(NULL,s,"call dll func:",MB_OK)

int main()
{
	typedef void* (*pfun)();			//����ָ��dll�к����ĺ���ָ��
	HINSTANCE hlib = LoadLibrary(DLLADDR);
	if(!hlib)
	{
	   msg("���ؿ�ʧ��");
	   return -1;
	}
	pfun fun = (pfun)GetProcAddress(hlib,"func");
	if(!fun)
	{
	   msg("��ȡ��������ʧ��");
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
	//-------ԭʼ�ĵ��÷�ʽ--------
	typedef void (*pfun2)();
	ULONG *pv;
	pv=(ULONG*)fun();
	if(pv)
	{
		ULONG vtAddr = (ULONG)(*pv);	//�麯����ĵ�ַ
		pfun2 p;
		p=(pfun2)(*(ULONG*)vtAddr);	//ȡ���麯������ǰ4���ֽڵ�����,��Initialize�ĵ�ַ
		p();
		p=(pfun2)(*(ULONG*)(vtAddr+4));	//ȡ���麯�����е�4��8�ֽڵ����ݣ���Loadlibrary�ĵ�ַ
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