#include <Windows.h>
#include "Dictionary.h"
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
