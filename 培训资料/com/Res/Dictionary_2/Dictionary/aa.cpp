#include <Windows.h>
#include "Dictionary.h"
#include <afxdisp.h>
//EXTERN_C{
//	__declspec(dllexport) int __stdcall func( );
//};
void* __stdcall func( )
{
	::MessageBox(NULL,L"创建了CDictionary对象，返回了该对象的指针",L"动态库导出函数",MB_OK);
	CDictionary *pD;
	pD=new CDictionary;
	return pD;
}
//<--2017年7月13日 ，组件支持注册与反注册
HRESULT __stdcall DllRegisterServer(void)
{
	::MessageBox(NULL,L"调用组件的注册方法",L"动态库导出函数",MB_OK);

	return 0;
}

HRESULT __stdcall DllUnregisterServer(void)
{
	::MessageBox(NULL,L"调用组件的反注册方法",L"动态库导出函数",MB_OK);
	return 0;
}
//2017年7月13日-->