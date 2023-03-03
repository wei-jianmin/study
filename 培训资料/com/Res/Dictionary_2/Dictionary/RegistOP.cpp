#include "RegistOP.h"
#include <Windows.h>
#include <WinReg.h>
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
		lr=RegOpenKeyExW(HKEY_LOCAL_MACHINE,sKeyPath,0,KEY_READ,&hKey);
		if(lr != ERROR_SUCCESS)	return false;
		l=RegQueryValueExW(hKey,sItemName,NULL,NULL,(LPBYTE)value,size);
		if(l != ERROR_SUCCESS) return false;
		return true;
	}
	else if(hk == HKCU)
	{
		lr=RegOpenKeyExW(HKEY_CURRENT_USER,sKeyPath,0,KEY_READ,&hKey);
		if(lr != ERROR_SUCCESS)	return false;
		l=RegQueryValueExW(hKey,sItemName,NULL,NULL,(LPBYTE)value,size);
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
