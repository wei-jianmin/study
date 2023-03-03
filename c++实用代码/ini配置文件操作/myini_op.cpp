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
	if(strPath.Left(1) == _T(".")) //使用的是相对路径
	{
		char szCurPath[MAX_PATH];
		HMODULE moudle=GetModuleHandle(0);
		moudle=(HMODULE)AfxGetInstanceHandle();
		GetModuleFileNameA(moudle,szCurPath,MAX_PATH);
		CStringA strCurPath;
		strCurPath=szCurPath;
		CString strtemp;
		strtemp.Format(_T("模块路径：%s"),(wchar_t*)_bstr_t(szCurPath));
#ifdef _DEBUG
		AfxMessageBox(strtemp);
#endif
		int nPos=strCurPath.ReverseFind('\\');	//按数组顺序，第一个字符的位置为
		int len=strCurPath.GetLength();	//不算结束符
		CStringA str=strCurPath.Left(nPos+1);		//处理掉获取当前路径时最后的文件名
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
		info=_T("配置文件路径：");
		info+=tmpFile;
		AfxMessageBox(info);
		AfxMessageBox(_T("配置文件目录不正确或该目录下没有配置文件"));
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
		//AfxMessageBox(_T("错误的配置文件路径"));
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
		//AfxMessageBox(_T("错误的配置文件路径"));
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
		//AfxMessageBox(_T("错误的配置文件路径"));
		return -1;
	}
	UINT res;
	int i;
	res=GetPrivateProfileIntA(appName,keyName,defaultValue,iniPath.c_str());
	i=res;
	return i;
}
