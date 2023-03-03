/*
 * 本文件连同头文件放在MFC/dll工程里面，请在theApp中添加以下三个成员：
   unsigned long err;
   CString strRet;
   CString strErrMsg;
 * 本代码中的函数操作及注释中，涉及三个术语：注册表项、注册表键、键值
 * 注册表项指的是注册表编辑器中左侧的“文件夹”部分
 * 注册表键指的是注册表编辑器中右侧的“文件”部分
 * 注册表(键)值指的是注册表编辑器中是右侧“文件”的数据内容
 */
#include "StdAfx.h"
#include "regist_op.h"
#include "dffs.h"				//CdffsApp类的头文件
//#include <vld.h>
/*Error codes are 32-bit values (bit 31 is the most significant bit).Bit 29 is reserved 
  for application-defined error codes; no system error code has this bit set.If you are
  defining an error code for your application, set this bit to one. That indicates that 
  the error code has been defined by an application, and ensures that your error code 
  does not conflict with any error codes defined by the system. */
#define USER_ERROR				0X40000000
#define ERROR_OK				0
#define ERROR_PARAMS			USER_ERROR+1	//参数错误
#define ERROR_PARAMS_NULL		USER_ERROR+2	//参数错误:参数为空
#define ERROR_PARAMS_KEYTYPE	USER_ERROR+3	//参数错误:
#define ERROR_VALUETYPE			USER_ERROR+4	//不支持的键值类型

extern 
/*
 * 本函数只支持对DWORD类型或字符串类型键值的读取
 * 无论注册表中原来的值是什么类型，函数都转化为字符串类型进行返回
 * 返回的字符串末尾不会主动添加换行符
 * 函数的调用者无需关心内存释放问题
 * 如果函数返回值为空，可通过getLastErrorMsg或getLastError查询错误原因
 */
const char* regRead(const char* KeyAddr, const char* KeyName)
{
	CString strKeyAddr,strKeyName;
	if(KeyName==NULL || KeyAddr==NULL)
	{
		theApp.err=ERROR_PARAMS_NULL;
		return NULL;
	}
	if(strlen(KeyAddr)==0 || strlen(KeyName)==0)
	{
		theApp.err=ERROR_PARAMS_NULL;
		return NULL;
	}
	
	strKeyName=KeyName;
	strKeyAddr=KeyAddr;
	strKeyAddr.Replace('/','\\');

	int slashPos;
	slashPos=strKeyAddr.Find('\\');
	if(slashPos<=1)
	{
		theApp.err=ERROR_PARAMS;
		return NULL;
	}

	CString strKeyType,strKeyPath;
	strKeyType=strKeyAddr.Left(slashPos);
	strKeyPath=strKeyAddr.Right(strKeyAddr.GetLength()-slashPos-1);

	LONG lr;
	HKEY hKey;
	if (strKeyType == "HKLM" || strKeyType=="HKEY_LOCAL_MACHINE")
		lr = RegOpenKeyEx(HKEY_LOCAL_MACHINE, (LPCTSTR)strKeyPath, 0, KEY_READ, &hKey);
	else if (strKeyType == "HKCU" || strKeyType=="HKEY_CURRENT_USER")
		lr = RegOpenKeyEx(HKEY_CURRENT_USER, (LPCTSTR)strKeyPath, 0, KEY_READ, &hKey);
	else if (strKeyType == "HKCR" || strKeyType=="HKEY_CLASSES_ROOT")
		lr = RegOpenKeyEx(HKEY_CLASSES_ROOT, (LPCTSTR)strKeyPath, 0, KEY_READ, &hKey);
	else if (strKeyType == "HKU" || strKeyType=="HKEY_USERS")
		lr = RegOpenKeyEx(HKEY_USERS, (LPCTSTR)strKeyPath, 0, KEY_READ, &hKey);
	else if (strKeyType == "HKCC" || strKeyType=="HKEY_CURRENT_CONFIG")
		lr = RegOpenKeyEx(HKEY_CURRENT_CONFIG, (LPCTSTR)strKeyPath, 0, KEY_READ, &hKey);
	else
	{
		theApp.err=ERROR_PARAMS_KEYTYPE;
		return NULL;	
	}
	if (lr != ERROR_SUCCESS)		//打开注册表失败
	{
		theApp.err=lr;
		return NULL;
	}
	//打开注册表成功
	DWORD dwType=REG_NONE;
    DWORD dwCount=0;
	lr = RegQueryValueEx(hKey, (LPCTSTR)strKeyName, NULL, &dwType,NULL, &dwCount);
	if (lr != ERROR_SUCCESS)		//查询注册表失败
	{
		RegCloseKey(hKey);
		theApp.err=lr;
		return NULL;
	}
	if(dwType==REG_DWORD_LITTLE_ENDIAN || dwType==REG_DWORD_BIG_ENDIAN)
	{
		DWORD buf;
		lr = RegQueryValueEx(hKey, (LPCTSTR)strKeyName, NULL, &dwType,(LPBYTE)&buf, &dwCount);
		if (lr != ERROR_SUCCESS)		//查询注册表失败
		{
			RegCloseKey(hKey);
			theApp.err=lr;
			return NULL;
		}
		theApp.strRet.Format("%d",buf);
	}
	else if(dwType== REG_SZ || dwType== REG_EXPAND_SZ||
			dwType==REG_MULTI_SZ || dwType==REG_RESOURCE_LIST)
	{
		BYTE *buf=new BYTE[dwCount];
		lr = RegQueryValueEx(hKey, (LPCTSTR)strKeyName, NULL, &dwType,buf, &dwCount);
		if (lr != ERROR_SUCCESS)		//查询注册表失败
		{
			RegCloseKey(hKey);
			theApp.err=lr;
			return NULL;
		}
		theApp.strRet=buf;
		delete[] buf;
	}
	else
	{
		theApp.err=ERROR_VALUETYPE;
		RegCloseKey(hKey);
		return NULL;
	}
	theApp.err = ERROR_OK;
	return (LPCTSTR)theApp.strRet;
}
/*
 * KeyAddr参数一定不能为空
 * 如果KeyName为空，则不再管KeyValue，只参照KeyAddr对注册表项进行操作
   如果del为非0，说明进行删除注册表项操作，否则进行添加注册表项操作（默认）
 * 如果KeyName不为空，则说明是对键进行操作
   如果KeyValue为空，则将键值设为空字符串
   如果del为非0，说明进行删除键操作，否则进行修改/添加注册表键值操作（默认）
 */
unsigned long regWrite(const char* KeyAddr, const char* KeyName, const char* KeyValue, const int del)
{
	CString strKeyAddr;
	if(KeyAddr==NULL || strlen(KeyAddr)==0)
	{
		theApp.err=ERROR_PARAMS_NULL;
		return ERROR_PARAMS_NULL;
	}

	strKeyAddr=KeyAddr;
	strKeyAddr.Replace('/','\\');

	int slashPos;
	slashPos=strKeyAddr.Find('\\');
	if(slashPos<=1)
	{
		theApp.err=ERROR_PARAMS;
		return ERROR_PARAMS;
	}
	if(strKeyAddr.Find("\\\\")!=-1)
	{
		theApp.err=ERROR_PARAMS;
		return ERROR_PARAMS;
	}
	CString strKeyType,strKeyPath;
	strKeyType=strKeyAddr.Left(slashPos);
	strKeyPath=strKeyAddr.Right(strKeyAddr.GetLength()-slashPos-1);

	LONG lr;
	HKEY hKey;

	if((KeyName==NULL || strlen(KeyName)==0) && del==0)	//创建项
	{
		DWORD dwCreate;	//表明项是否已经存在
		if (strKeyType == "HKLM" || strKeyType=="HKEY_LOCAL_MACHINE")
			lr = RegCreateKeyEx(HKEY_LOCAL_MACHINE,(LPCTSTR)strKeyPath,0,
								NULL,REG_OPTION_NON_VOLATILE,KEY_ALL_ACCESS,
								NULL,&hKey,&dwCreate);
		else if (strKeyType == "HKCU" || strKeyType=="HKEY_CURRENT_USER")
			lr = RegCreateKeyEx(HKEY_LOCAL_MACHINE,(LPCTSTR)strKeyPath,0,
								NULL,REG_OPTION_NON_VOLATILE,KEY_ALL_ACCESS,
								NULL,&hKey,&dwCreate);
		else if (strKeyType == "HKCR" || strKeyType=="HKEY_CLASSES_ROOT")
			lr = RegCreateKeyEx(HKEY_CLASSES_ROOT,(LPCTSTR)strKeyPath,0,
								NULL,REG_OPTION_NON_VOLATILE,KEY_ALL_ACCESS,
								NULL,&hKey,&dwCreate);
		else if (strKeyType == "HKU" || strKeyType=="HKEY_USERS")
			lr = RegCreateKeyEx(HKEY_USERS,(LPCTSTR)strKeyPath,0,
								NULL,REG_OPTION_NON_VOLATILE,KEY_ALL_ACCESS,
								NULL,&hKey,&dwCreate);
		else if (strKeyType == "HKCC" || strKeyType=="HKEY_CURRENT_CONFIG")
			lr = RegCreateKeyEx(HKEY_CURRENT_CONFIG,(LPCTSTR)strKeyPath,0,
								NULL,REG_OPTION_NON_VOLATILE,KEY_ALL_ACCESS,
								NULL,&hKey,&dwCreate);
		else
		{
			theApp.err=ERROR_PARAMS_KEYTYPE;
			return ERROR_PARAMS_KEYTYPE;	
		}
		if(lr==ERROR_SUCCESS)
			RegCloseKey(hKey);
		theApp.err=lr;
		return lr;
	}
	else if((KeyName==NULL || strlen(KeyName)==0) && del!=0)	//删除项
	{
		CString strKeyPath2,delName;
		slashPos=strKeyPath.ReverseFind('\\');
		if(slashPos == -1)
		{
			strKeyPath2="";
			delName=strKeyPath;
		}
		else
		{
			strKeyPath2=strKeyPath.Left(slashPos);
			delName=strKeyPath.Right(strKeyPath.GetLength()-slashPos-1);
		}
		if (strKeyType == "HKLM" || strKeyType=="HKEY_LOCAL_MACHINE")
			lr = RegOpenKeyEx(HKEY_LOCAL_MACHINE, (LPCTSTR)strKeyPath2, 0, KEY_WRITE, &hKey);
		else if (strKeyType == "HKCU" || strKeyType=="HKEY_CURRENT_USER")
			lr = RegOpenKeyEx(HKEY_CURRENT_USER, (LPCTSTR)strKeyPath2, 0, KEY_WRITE, &hKey);
		else if (strKeyType == "HKCR" || strKeyType=="HKEY_CLASSES_ROOT")
			lr = RegOpenKeyEx(HKEY_CLASSES_ROOT, (LPCTSTR)strKeyPath2, 0, KEY_WRITE, &hKey);
		else if (strKeyType == "HKU" || strKeyType=="HKEY_USERS")
			lr = RegOpenKeyEx(HKEY_USERS, (LPCTSTR)strKeyPath2, 0, KEY_WRITE, &hKey);
		else if (strKeyType == "HKCC" || strKeyType=="HKEY_CURRENT_CONFIG")
			lr = RegOpenKeyEx(HKEY_CURRENT_CONFIG, (LPCTSTR)strKeyPath2, 0, KEY_WRITE, &hKey);
		else
		{
			theApp.err=ERROR_PARAMS_KEYTYPE;
			return ERROR_PARAMS_KEYTYPE;	
		}
		if (lr != ERROR_SUCCESS)		//打开注册表失败
		{
			theApp.err=lr;
			return lr;
		}
		lr=RegDeleteKey(hKey,(LPCTSTR)delName);
		RegCloseKey(hKey);
		theApp.err=lr;
		return lr;
	}
	else if((KeyName!=NULL && strlen(KeyName)> 0) && del==0)	//修改、创建键
	{
		if(KeyValue==NULL || strlen(KeyValue)==0)
		{
			theApp.err=ERROR_PARAMS_NULL;
			return ERROR_PARAMS_NULL;
		}
		if (strKeyType == "HKLM" || strKeyType=="HKEY_LOCAL_MACHINE")
			lr = RegOpenKeyEx(HKEY_LOCAL_MACHINE, (LPCTSTR)strKeyPath, 0, KEY_WRITE, &hKey);
		else if (strKeyType == "HKCU" || strKeyType=="HKEY_CURRENT_USER")
			lr = RegOpenKeyEx(HKEY_CURRENT_USER, (LPCTSTR)strKeyPath, 0, KEY_WRITE, &hKey);
		else if (strKeyType == "HKCR" || strKeyType=="HKEY_CLASSES_ROOT")
			lr = RegOpenKeyEx(HKEY_CLASSES_ROOT, (LPCTSTR)strKeyPath, 0, KEY_WRITE, &hKey);
		else if (strKeyType == "HKU" || strKeyType=="HKEY_USERS")
			lr = RegOpenKeyEx(HKEY_USERS, (LPCTSTR)strKeyPath, 0, KEY_WRITE, &hKey);
		else if (strKeyType == "HKCC" || strKeyType=="HKEY_CURRENT_CONFIG")
			lr = RegOpenKeyEx(HKEY_CURRENT_CONFIG, (LPCTSTR)strKeyPath, 0, KEY_WRITE, &hKey);
		else
		{
			theApp.err=ERROR_PARAMS_KEYTYPE;
			return ERROR_PARAMS_KEYTYPE;	
		}
		if (lr != ERROR_SUCCESS)		//打开注册表失败
		{
			theApp.err=lr;
			return lr;
		}
		
		DWORD cbData;
		CString strKeyName=KeyName;
		long val=_ttol(KeyValue);
		char ch_buf[10]={0};
		const char* pch=_ltot(val,ch_buf,10);
		DWORD dwType;
		if(strcmp(pch,KeyValue)==0)	//说明设置的值为数字
		{
			dwType=REG_DWORD;
			cbData=4;
			lr=RegSetValueEx(hKey,(LPCTSTR)strKeyName,0,dwType,(CONST BYTE*)&val,cbData);
		}
		else
		{
			dwType=REG_SZ;
			cbData=strlen(KeyValue);
			lr=RegSetValueEx(hKey,(LPCTSTR)strKeyName,0,dwType,(CONST BYTE*)KeyValue,cbData);
		}
		RegCloseKey(hKey);
		theApp.err=lr;
		return lr;
	}	
	else	//删除键
	{
		if(KeyName==NULL)
		{
			theApp.err=ERROR_PARAMS_NULL;
			return ERROR_PARAMS_NULL;
		}
		if (strKeyType == "HKLM" || strKeyType=="HKEY_LOCAL_MACHINE")
			lr = RegOpenKeyEx(HKEY_LOCAL_MACHINE, (LPCTSTR)strKeyPath, 0, KEY_WRITE, &hKey);
		else if (strKeyType == "HKCU" || strKeyType=="HKEY_CURRENT_USER")
			lr = RegOpenKeyEx(HKEY_CURRENT_USER, (LPCTSTR)strKeyPath, 0, KEY_WRITE, &hKey);
		else if (strKeyType == "HKCR" || strKeyType=="HKEY_CLASSES_ROOT")
			lr = RegOpenKeyEx(HKEY_CLASSES_ROOT, (LPCTSTR)strKeyPath, 0, KEY_WRITE, &hKey);
		else if (strKeyType == "HKU" || strKeyType=="HKEY_USERS")
			lr = RegOpenKeyEx(HKEY_USERS, (LPCTSTR)strKeyPath, 0, KEY_WRITE, &hKey);
		else if (strKeyType == "HKCC" || strKeyType=="HKEY_CURRENT_CONFIG")
			lr = RegOpenKeyEx(HKEY_CURRENT_CONFIG, (LPCTSTR)strKeyPath, 0, KEY_WRITE, &hKey);
		else
		{
			theApp.err=ERROR_PARAMS_KEYTYPE;
			return ERROR_PARAMS_KEYTYPE;	
		}
		if (lr != ERROR_SUCCESS)		//打开注册表失败
		{
			theApp.err=lr;
			return lr;
		}
		lr=RegDeleteValue(hKey,(LPCTSTR)KeyName);
		RegCloseKey(hKey);
		theApp.err=lr;
		return lr;
	}
	
}
unsigned long getLastError()
{
	return theApp.err;
}
const char* getLastErrorMsg()
{
	unsigned long err;
	err = theApp.err & USER_ERROR;
	if(err)			//说明是程序错误
	{
		switch(theApp.err)
		{

		case ERROR_OK:
			theApp.strErrMsg="(程序错误)函数执行成功。\n";
			break;
		case ERROR_PARAMS:
			theApp.strErrMsg="(程序错误)参数错误。\n";
			break;
		case ERROR_PARAMS_NULL:
			theApp.strErrMsg="(程序错误)参数错误：函数参数为空。\n";
			break;
		case ERROR_PARAMS_KEYTYPE:
			theApp.strErrMsg="(程序错误)参数错误：参数格式错误。\n";
			break;
		case ERROR_VALUETYPE:
			theApp.strErrMsg="(程序错误)不支持的键值类型。\n";
			break;
		default:
			theApp.strErrMsg="(程序错误)未知错误。\n";
			break;
		}
	}
	else
	{
		TCHAR* lpMsgBuf;
		FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER|FORMAT_MESSAGE_FROM_SYSTEM,NULL,theApp.err,0,(LPTSTR)&lpMsgBuf,0,NULL);

		theApp.strErrMsg="(系统函数错误)";
		theApp.strErrMsg+=lpMsgBuf;
		if(lpMsgBuf!=NULL)
		{
			LocalFree(lpMsgBuf);
			lpMsgBuf=NULL;
		}	
	}
	return (LPCTSTR)theApp.strErrMsg;
}

//获得指定键下值项的数据
bool regGetItemValue(hk_t hkType, LPCTSTR keyAddr, LPCTSTR keyValue,CString &res)
{
	unsigned long index;
	TCHAR buffer[MAX_PATH];
	HKEY hKey;
	LRESULT lr;
	LONG size;
	res.Empty();
	if (hkType == HKLM)
		lr = RegOpenKey(HKEY_LOCAL_MACHINE, keyAddr, &hKey);	//可见用常指针指向的路径即可无误的打开注册表键
	else if (hkType == HKCU)
		lr = RegOpenKey(HKEY_CURRENT_USER, keyAddr, &hKey);
	else if (hkType == HKCR)
		lr = RegOpenKey(HKEY_CLASSES_ROOT, keyAddr, &hKey);
	else if (hkType == HKU)
		lr = RegOpenKey(HKEY_USERS, keyAddr, &hKey);
	else if (hkType == HKCC)
		lr = RegOpenKey(HKEY_CURRENT_CONFIG, keyAddr, &hKey);
	else
	{
		res.Format(_T("%s"), _T("hkType参数错误"));
		return false;
	}
	if (lr != ERROR_SUCCESS)		//打开注册表失败
	{
		res.Format(_T("%s"), _T("打开注册表失败"));
		return false;
	}
	//注册表打开成功
	size = sizeof(buffer);
	lr = GetValue(hKey, keyValue, &buffer[0], &size);	//获得值项的数据
	if (lr == ERROR_SUCCESS)		//找到了对应值项
	{
		res.Format(_T("%s"), buffer);
		RegCloseKey(hKey);
		return true;
	}
	else
	{
		res.Format(_T("%s"), _T("获取值项失败"));
		RegCloseKey(hKey);
		return false;
	}
}
//获得键下指定值项的数据信息
bool regGetItemValue(hk_t hkType, LPCTSTR keyAddr, LPCTSTR keyValue, int &res)
{
	unsigned long index;
	DWORD buffer;
	HKEY hKey;
	LRESULT lr;
	LONG size;
	res = -1;
	if (hkType == HKLM)
		lr = RegOpenKey(HKEY_LOCAL_MACHINE, keyAddr, &hKey);
	else if (hkType == HKCU)
		lr = RegOpenKey(HKEY_CURRENT_USER, keyAddr, &hKey);
	else if (hkType == HKCR)
		lr = RegOpenKey(HKEY_CLASSES_ROOT, keyAddr, &hKey);
	else if (hkType == HKU)
		lr = RegOpenKey(HKEY_USERS, keyAddr, &hKey);
	else if (hkType == HKCC)
		lr = RegOpenKey(HKEY_CURRENT_CONFIG, keyAddr, &hKey);
	else
	{
		//MessageBox(NULL, _T("hkType Error"), _T("notion"), MB_OK);
		return false;
	}
	if (lr != ERROR_SUCCESS)		//打开注册表失败
	{
		///MessageBox(NULL, _T("打开注册表失败"), _T("notion"), MB_OK);
		return false;
	}
	//注册表打开成功

	size = sizeof(buffer);
	//lr = GetValue2(hKey, keyValue, &buffer, &size);	//获得子键的指定值
	lr = GetValue2(hKey, keyValue, &buffer);
	if (lr == ERROR_SUCCESS)		//找到了一个键值
	{
		//MessageBox(NULL, _T("找到了一个键值"), _T("notion"), MB_OK);
		RegCloseKey(hKey);
		res = buffer;
		return true;
	}
	else
	{
		//MessageBox(NULL, _T("检索键值失败"), _T("notion"), MB_OK);
		RegCloseKey(hKey);
		res = buffer;
		return false;
	}
}

//搜索指定键下的所有子键，并把符合keyWord的子键其下的值放入列表框变量中
void getKeyWords(CListBox &list,LPCTSTR keyPath,LPCTSTR keyWords)
{
	unsigned long index;
	TCHAR buffer[MAX_PATH];
	HKEY hKey;
	LRESULT lr;
	CString ver;
	int res;
	res=1;
	ver.Empty();
	lr = RegOpenKey(HKEY_CURRENT_USER, keyPath, & hKey);
	if(lr != ERROR_SUCCESS)		//打开注册表失败
	{
		return;
	}
	for(index =0; ;index++)
	{
		lr = RegEnumKey(hKey, index, buffer, sizeof(buffer));	//查找到的指定序号的子键的名称放入buffer中
		switch(lr)
		{
		case ERROR_SUCCESS:	//成功获得一个子键
			checkEnumKey(buffer,hKey,keyWords,list);	//操作一个子键
			break;
		case ERROR_NO_MORE_ITEMS:	//没有其它子键了，完成搜索
			//ver.Format(_T("%s"),_T("完成搜索，没找到匹配软件"));
			RegCloseKey(hKey);
			//MessageBoxW(NULL,_T("no match software"),_T("caption"),MB_OK);
			return;
		default:	//其它情况，未能完成搜索
			//ver.Format(_T("%s"),_T("查找失败，未能完成搜索"));
			RegCloseKey(hKey);
			//MessageBoxW(NULL,_T("search faild"),_T("caption"),MB_OK);
			return;
		}
	}
	return;
}

bool getRegItemValue(hk_t hk,CString sKeyPath,CString sItemName,LPTSTR value, LPDWORD size)
{
	HKEY hKey;
	LRESULT lr;
	LONG l;
	if(hk == HKLM)
	{
		lr=RegOpenKeyEx(HKEY_LOCAL_MACHINE,sKeyPath,0,KEY_READ,&hKey);
		if(lr != ERROR_SUCCESS)	return false;
		l=RegQueryValueEx(hKey,sItemName,NULL,NULL,(LPBYTE)value,size);
		if(l != ERROR_SUCCESS) return false;
		return true;
	}
	else if(hk == HKCU)
	{
		lr=RegOpenKeyEx(HKEY_CURRENT_USER,sKeyPath,0,KEY_READ,&hKey);
		if(lr != ERROR_SUCCESS)	return false;
		l=RegQueryValueEx(hKey,sItemName,NULL,NULL,(LPBYTE)value,size);
		if(l != ERROR_SUCCESS) return false;
		return true;
	}
	else
		return false;

}

bool regAddKey(hk_t hk,CString path,CString key)
{
	//TCHAR buffer[MAX_PATH]=_T("Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\ZoneMap\\Domains\\wei.j.m");
	LONG res;
	CString keyPath;
	LPTSTR lptstr;
	HKEY hkey;
	DWORD dwDisp;
	keyPath.Empty();
	keyPath=path+_T("\\")+key;
	lptstr=keyPath.GetBuffer(1024);
	if(hk == HKLM)
	{
		res=RegCreateKeyEx(HKEY_LOCAL_MACHINE,lptstr,0,NULL,REG_OPTION_NON_VOLATILE,KEY_ALL_ACCESS,NULL,&hkey,&dwDisp);
		//用LPCTSTR作参数，虽然提示注册表添加成功，但实际添加失败，用LPTSTR则可解决此问题，但需重新打开注册表才能看到
		if(res != ERROR_SUCCESS)
		{
			MessageBox(GetActiveWindow(),_T("注册表项添加失败！"),_T("提示"),MB_OK);
			keyPath.ReleaseBuffer();
			return false;
		}
		MessageBox(GetActiveWindow(),_T("注册表项添加成功！"),_T("提示"),MB_OK);
		keyPath.ReleaseBuffer();
		RegCloseKey(hkey);
		return true;
	}
	else if (hk == HKCU)
	{
		res=RegCreateKeyEx(HKEY_CURRENT_USER,lptstr,0,NULL,REG_OPTION_NON_VOLATILE,KEY_ALL_ACCESS,NULL,&hkey,&dwDisp);
		if(res != ERROR_SUCCESS)
		{
			MessageBox(GetActiveWindow(),_T("注册表项添加失败！"),_T("提示"),MB_OK);
			keyPath.ReleaseBuffer();
			return false;
		}
		MessageBox(GetActiveWindow(),_T("注册表项添加成功！"),_T("提示"),MB_OK);
		keyPath.ReleaseBuffer();
		RegCloseKey(hkey);
		return true;
	}
	else
		keyPath.ReleaseBuffer();
	return false;
}
//注册表添加值
bool regAddValue(hk_t hk,CString path,CString name,DWORD dataType,CString value)
{
	LRESULT lr;
	HKEY hKey;
	LPTSTR	lptstr;
	LPCTSTR lpctstr;
	lptstr=path.GetBuffer(1024);
	//打开注册表
	//入口参数（hk）判断
	if (hk == HKLM)
	{
		lr = RegOpenKey(HKEY_LOCAL_MACHINE,lptstr, & hKey);
		path.ReleaseBuffer();
		if(lr != ERROR_SUCCESS)
		{
			MessageBox(GetActiveWindow(),_T("注册表打开失败\n值添加失败"),_T("提示"),MB_OK);
			return	false;
		}
	}
	else if (hk == HKCU)
	{
		lr = RegOpenKey(HKEY_CURRENT_USER,lptstr, & hKey);
		path.ReleaseBuffer();
		if(lr != ERROR_SUCCESS)
		{
			MessageBox(GetActiveWindow(),_T("注册表打开失败\n值添加失败"),_T("提示"),MB_OK);
			return	false;
		}
	}
	else
	{
		MessageBox(GetActiveWindow(),_T("未知的入口参数(hk)\n值添加失败"),_T("提示"),MB_OK);
		return false;
	}
	//添加键值
	//入口参数(dataType)判断
	if(dataType == REG_DWORD)
	{
		int val;
		val=strtoi(value);
		lpctstr=name;
		lr=RegSetValueEx(hKey,lpctstr,NULL,dataType,(LPBYTE)&val,sizeof(DWORD));
		if(lr == ERROR_SUCCESS)
		{
			MessageBox(GetActiveWindow(),_T("值添加成功"),_T("提示"),MB_OK);
			RegCloseKey(hKey);
			return true;
		}
		else
		{
			MessageBox(GetActiveWindow(),_T("值添加失败"),_T("提示"),MB_OK);
			RegCloseKey(hKey);
			return false;
		}
	}
	else if(dataType == REG_SZ)
	{
		lpctstr=name;
		lptstr=value.GetBuffer(1024);
		//lr=RegSetValueEx(hKey,lptstr,NULL,dataType,(LPBYTE)0x2,1);
		//lr=RegSetValueEx(hKey,_T("ProductName"),NULL,REG_SZ,(LPBYTE)"MyAppName",sizeof("MyAppName"));
		//lr=RegSetValueEx(hKey,lptstr,NULL,REG_SZ,(LPBYTE)"MyAppName",sizeof("MyAppName"));
		lr=RegSetValueEx(hKey,lpctstr,NULL,dataType,(LPBYTE)lptstr,sizeof(DWORD));
		if(lr == ERROR_SUCCESS)
		{
			MessageBox(GetActiveWindow(),_T("值添加成功"),_T("提示"),MB_OK);
			RegCloseKey(hKey);	
			value.ReleaseBuffer();
			return true;
		}
		else
		{
			MessageBox(GetActiveWindow(),_T("值添加失败"),_T("提示"),MB_OK);
			RegCloseKey(hKey);	
			value.ReleaseBuffer();
			return true;
		}
	}
	else
	{
		MessageBox(GetActiveWindow(),_T("未知的入口参数(dataType)\n值添加失败"),_T("提示"),MB_OK);
		return false;
	}

}

//根据name获取注册表键下值项的信息，值结果存放在value中，这里不返回值类型信息
LRESULT GetValue(HKEY hKey, LPCTSTR name, LPTSTR value, LPLONG size)
{
	return ::RegQueryValueEx(hKey, name, NULL, NULL, (LPBYTE)value, (LPDWORD)size);
}
//根据name读取注册表键下的值，要求值类型为DWORD型，结果存放在value中
//注意：其实这个函数是不必要的，之前因为认识上的错误才添加了这个函数
//函数的第三个参数是用来获取具有指定名字的值项的类型，是输出参数，而不是输入参数，无需为其提供类型值
LRESULT GetValue2(HKEY hKey, LPCTSTR name, LPDWORD value)
{
	DWORD dwType = REG_DWORD;
	DWORD size=sizeof(DWORD);
	return ::RegQueryValueEx(hKey, name, NULL, &dwType, (LPBYTE)value, &size);
}
//被getKeyWords函数调用
void checkEnumKey(LPCTSTR szKey , HKEY hParent , LPCTSTR keyWords ,CListBox &list)
{
	CString ver2;
	LRESULT lr;
	HKEY hKey;
	LONG size;
	TCHAR buffer[MAX_PATH] ;
	lr = RegOpenKey(hParent, szKey, &hKey);
	//不能打开注册表（打开子键）
	if(lr != ERROR_SUCCESS)
		return ;
	//注册表打开成功
	size = sizeof(buffer);
	lr = GetValue(hKey, keyWords, &buffer[0], &size);	//获得子键的指定值
	ver2.Format(_T("%s"),buffer);	
	if(lr == ERROR_SUCCESS)		//找到了该键值
	{
		list.AddString(ver2);
	}
	else	//没找到该键值
	{  
		return;
	}	
}

//CString 转整形，遇到非法字符返回
int strtoi(CString str)
{
	int res=0;
	int len=str.GetLength();
	int i;
	char ch;
	for(i=0;i<len;i++)
	{
		ch=str[i];
		if(ch>'9' || ch<'0')
			break;
		res *= 10;
		res += atoi( &ch );
	}
	return res;
}
*/