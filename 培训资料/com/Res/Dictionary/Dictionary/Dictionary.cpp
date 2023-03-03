#include "Dictionary.h"
#include <Windows.h>

#define msg(s) MessageBoxA(NULL,s,"call dll func:",MB_OK)


void CDictionary::Initialize()
{
	msg("调用了 Initialize 成员函数");
}
void CDictionary::Loadlibrary()
{
	msg("调用了 LoadLibrary 成员函数");
}
void CDictionary::InsertWord()
{
	msg("调用了 InsertWord 成员函数");
}
void CDictionary::DeleteWord()
{
	msg("调用了 DeleteWord 成员函数");
}
void CDictionary::LookupWord()
{
	msg("调用了 LookupWord 成员函数");
}
void CDictionary::RestoreLibrary()
{
	msg("调用了 RestoreLibrary 成员函数");
}

void CDictionary::FreeLibrary()
{
	msg("调用了 FreeLibrary 成员函数");
}