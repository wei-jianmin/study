#include <Windows.h>
#include "Dictionary.h"
//EXTERN_C{
//	__declspec(dllexport) int __stdcall func( );
//};
void* __stdcall func( )
{
	::MessageBox(NULL,L"������CDictionary���󣬷����˸ö����ָ��",L"��̬�⵼������",MB_OK);
	CDictionary *pD;
	pD=new CDictionary;
	return pD;
}
