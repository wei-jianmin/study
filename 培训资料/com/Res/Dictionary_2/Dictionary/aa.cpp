#include <Windows.h>
#include "Dictionary.h"
#include <afxdisp.h>
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
//<--2017��7��13�� �����֧��ע���뷴ע��
HRESULT __stdcall DllRegisterServer(void)
{
	::MessageBox(NULL,L"���������ע�᷽��",L"��̬�⵼������",MB_OK);

	return 0;
}

HRESULT __stdcall DllUnregisterServer(void)
{
	::MessageBox(NULL,L"��������ķ�ע�᷽��",L"��̬�⵼������",MB_OK);
	return 0;
}
//2017��7��13��-->