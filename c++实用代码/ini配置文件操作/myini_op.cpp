#include "StdAfx.h"
#include "myini_op.h"
#include<comutil.h>
#pragma comment(lib,"comsuppw.lib")
using namespace _com_util;
myini_op::myini_op(void)
{
	
}

myini_op::~myini_op(void)
{

}

bool myini_op::Init(const char * path,const char *name)
{
	iniName=name;
	errPath=true;
	CStringA strPath;
	strPath=path;
	if(strPath.IsEmpty())
	{
		iniPath.clear();
		return false;
	}
	if(strPath.Right(1) == _T("\\"))
		strPath=strPath.Left(strPath.GetLength()-1);
	if(strPath.Left(1) == _T(".")) //ʹ�õ������·��
	{
		char szCurPath[MAX_PATH];
		HMODULE moudle=GetModuleHandle(0);
		moudle=(HMODULE)AfxGetInstanceHandle();
		GetModuleFileNameA(moudle,szCurPath,MAX_PATH);
		CStringA strCurPath;
		strCurPath=szCurPath;
		CString strtemp;
		strtemp.Format(_T("ģ��·����%s"),(wchar_t*)_bstr_t(szCurPath));
#ifdef _DEBUG
		AfxMessageBox(strtemp);
#endif
		int nPos=strCurPath.ReverseFind('\\');	//������˳�򣬵�һ���ַ���λ��Ϊ
		int len=strCurPath.GetLength();	//���������
		CStringA str=strCurPath.Left(nPos+1);		//�������ȡ��ǰ·��ʱ�����ļ���
		strPath=str+strPath.Right(strPath.GetLength()-2)+"\\";
		strPath+=iniName.data();
		iniPath=strPath.GetBuffer();
		strPath.ReleaseBuffer();
	}
	else
	{
		strPath+="\\";
		strPath+=iniPath.data();
		iniPath=strPath.GetBuffer();
		strPath.ReleaseBuffer();
	}
	CFileFind finder;
	CString tmpFile;

#ifdef _UNICODE
	tmpFile=_com_util::ConvertStringToBSTR(strPath.GetBuffer());
#else
	tmpFile=strPath.GetBuffer();
#endif
	strPath.ReleaseBuffer();
	if(!finder.FindFile((LPCTSTR)tmpFile))
	{
		CString info;
		info=_T("�����ļ�·����");
		info+=tmpFile;
		AfxMessageBox(info);
		AfxMessageBox(_T("�����ļ�Ŀ¼����ȷ���Ŀ¼��û�������ļ�"));
		return false;
	}
	errPath=false;
}

const char* myini_op::getIniPath()
{
	return iniPath.c_str();
}

bool myini_op::write(const char * appName,const char * keyName,const char * value)
{
	if(errPath)
	{
		//AfxMessageBox(_T("����������ļ�·��"));
		return false;
	}
	BOOL b=WritePrivateProfileStringA(appName,keyName,value,iniPath.c_str());
	if(b)
		return true;
	else
		return false;
}

const char* myini_op::readString(const char * appName,const char * keyName,const char * defaultValue)
{
	if(errPath)
	{
		//AfxMessageBox(_T("����������ļ�·��"));
		return "";
	}
	char szbuff[MAX_PATH]={0};
	GetPrivateProfileStringA(appName,keyName,defaultValue,szbuff,MAX_PATH,iniPath.c_str());
	string res;
	res=szbuff;
	return res.c_str();
}

int myini_op::readInt(const char * appName,const char * keyName,const int defaultValue)
{
	if(errPath)
	{
		//AfxMessageBox(_T("����������ļ�·��"));
		return -1;
	}
	UINT res;
	int i;
	res=GetPrivateProfileIntA(appName,keyName,defaultValue,iniPath.c_str());
	i=res;
	return i;
}
