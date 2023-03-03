#include "Dictionary.h"
#include <Windows.h>

#define msg(s) MessageBoxA(NULL,s,"call dll func:",MB_OK)


void CDictionary::Initialize()
{
	msg("������ Initialize ��Ա����");
}
void CDictionary::Loadlibrary()
{
	msg("������ LoadLibrary ��Ա����");
}
void CDictionary::InsertWord()
{
	msg("������ InsertWord ��Ա����");
}
void CDictionary::DeleteWord()
{
	msg("������ DeleteWord ��Ա����");
}
void CDictionary::LookupWord()
{
	msg("������ LookupWord ��Ա����");
}
void CDictionary::RestoreLibrary()
{
	msg("������ RestoreLibrary ��Ա����");
}

void CDictionary::FreeLibrary()
{
	msg("������ FreeLibrary ��Ա����");
}