#include "stdafx.h"
#include "func.h"
#include <Windows.h>
Cfunc::Cfunc()
{
}
Cfunc::~Cfunc()
{
}
//安全的获取真实系统信息
void Cfunc::SafeGetNativeSystemInfo(__out LPSYSTEM_INFO lpSystemInfo)
{
	if(NULL == lpSystemInfo)
		return ;
	typedef VOID (WINAPI *LPFN_GetNativeSystemInfo) (LPSYSTEM_INFO lpSystemInfo);
	LPFN_GetNativeSystemInfo nsInfo=(LPFN_GetNativeSystemInfo)GetProcAddress(GetModuleHandle(_T("kernel32")),"GetNativeSystemInfo");;
	if (NULL == nsInfo)
	{
		nsInfo(lpSystemInfo);
	}
	else
	{
		GetSystemInfo(lpSystemInfo);
	}
}
//获得操作系统位数
int Cfunc::GetSystemBits()
{
	SYSTEM_INFO si;
	SafeGetNativeSystemInfo(&si);
	if(si.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_AMD64 || si.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_IA64)
		return 64;
	else
		return 32;
}
//获得操作系统名称
void Cfunc::GetSysName(CString &osname){
			 SYSTEM_INFO info;	//用该结构判断64为AMD处理器
			 GetSystemInfo(&info);	//调用该函数填充结构
			 OSVERSIONINFOEX os;	//操作系统信息
			 //OSVERSIONINFOEXA os;
			 os.dwOSVersionInfoSize=sizeof(OSVERSIONINFOEX);
			 osname=_T("unknown OperatingSystem.");	//先假定操作系统名称未知
			 if ( GetVersionEx( (LPOSVERSIONINFOW) &os ) )		//os对象（栈对象）存在
				
				{
					
					//下面根据版本信息判断操作系统名称
					switch(os.dwMajorVersion)	//判断主版本号
					{
					case 4:
						switch(os.dwMinorVersion)	//判断次版本号
						{
						case 0:
							if (os.dwPlatformId ==	VER_PLATFORM_WIN32_NT)
							{
								osname=_T("Microsoft Window NT 4.0");	//1996年7月发布
							}
							else if (os.dwPlatformId == VER_PLATFORM_WIN32_WINDOWS)
							{
								osname=_T("Microsoft Windows 95");
							}
							break;
						case 10:
							osname=_T("Microsoft Windows 98");
							break;
						case 90:
							osname=_T("Microsoft Window Me");
							break;
						}
						break;
					case 5:
						switch(os.dwMinorVersion)
						{
						case 0:
							osname=_T("Microsoft Windows 2000");	//99年12月发布
							break;
						case 1:
							osname=_T("Microsoft windows XP");	//01年8月发布
							break;
						case 2:
							if (os.wProductType == VER_NT_WORKSTATION && info.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_AMD64)	//产品类型和处理器技术
							{
								osname=_T("Microsoft Windows XP Professional X64 Edition");
							}
							else if ( GetSystemMetrics(SM_SERVERR2) != 0)	//metrics: 度量（n.）
							{
								osname=_T("Microsoft Windows Server 2003 R2");
							}
							break;
						}
						break;
					case 6:
						switch(os.dwMinorVersion)
						{
						case 0:
							if(os.wProductType == VER_NT_WORKSTATION)
								osname=_T("Microsoft Windows Vista");
							else
								osname=_T("Microsoft Windows Server 2008");
							break;
						case 1:
							if(os.wProductType == VER_NT_WORKSTATION)
								osname=_T("Microsoft Windows 7");
							else
								osname=_T("Microsoft Windows Server 2008 R2");
							break;
						}
						break;
					}
				}
}

// 获取操作系统版本
void Cfunc::GetVersionMark(CString &vmark)
{
	
	OSVERSIONINFOEX os;
	os.dwOSVersionInfoSize=sizeof(OSVERSIONINFOEX);
	vmark=_T("unknown version");
	//if(GetVersionEx((LPOSVERSIONINFOW)os))
	if ( GetVersionEx( (LPOSVERSIONINFOW) &os ) )		//os对象（栈对象）存在

	{

		//下面根据版本信息判断操作系统名称
		switch(os.dwMajorVersion)	//判断主版本号
		{
		/*
		case 4:
			switch(os.dwMinorVersion)	//判断次版本号
			{
			case 0:
				if (os.dwPlatformId ==	VER_PLATFORM_WIN32_NT)
				{
					osname=_T("Microsoft Window NT 4.0");	//1996年7月发布
				}
				else if (os.dwPlatformId == VER_PLATFORM_WIN32_WINDOWS)
				{
					osname=_T("Microsoft Windows 95");
				}
				break;
			case 10:
				osname=_T("Microsoft Windows 98");
				break;
			case 90:
				osname=_T("Microsoft Window Me");
				break;
			}
			break;	*/
		case 5:
			switch(os.dwMinorVersion)
			{
			case 0:
				if(os.wSuiteMask == VER_SUITE_ENTERPRISE)
					vmark=_T("Advanced Server");
				break;
			case 1:
				if(os.wSuiteMask == VER_SUITE_EMBEDDEDNT)
					vmark=_T("Embedded");
				else if(os.wSuiteMask == VER_SUITE_PERSONAL)
					vmark=_T("Home Edition");
				else
					vmark=_T("Professional");
				break;
			case 2:
				if(GetSystemMetrics(SM_SERVERR2) == 0 && os.wSuiteMask == VER_SUITE_BLADE)	//windows server 2003
					vmark=_T("Compute Cluster Edition");
				else if(GetSystemMetrics(SM_SERVERR2) == 0 && os.wSuiteMask == VER_SUITE_STORAGE_SERVER)
					vmark=_T("Storage Server");
				else if (GetSystemMetrics(SM_SERVERR2) == 0 && os.wSuiteMask == VER_SUITE_DATACENTER)
					vmark=_T("Datecenter Edition");
				else if (GetSystemMetrics(SM_SERVERR2) == 0 && os.wSuiteMask == VER_SUITE_COMPUTE_SERVER)
					vmark=_T("Compute Cluster Edition");
				else if (GetSystemMetrics(SM_SERVERR2) == 0 && os.wSuiteMask == VER_SUITE_ENTERPRISE)
					vmark=_T("Enterprise Edition");
				else if (GetSystemMetrics(SM_SERVERR2) != 0 && os.wSuiteMask == VER_SUITE_STORAGE_SERVER)
					vmark=_T("Storage Server");
				break;
			}
			break;
		case 6:
			switch(os.dwMinorVersion)
			{
			case 0:
				if(os.wProductType != VER_NT_WORKSTATION && os.wSuiteMask == VER_SUITE_DATACENTER)
					vmark=_T("Datacenter Server");
				else if(os.wProductType != VER_NT_WORKSTATION && os.wSuiteMask == VER_SUITE_ENTERPRISE)
					vmark=_T("EnterPrise");
				else if(os.wProductType == VER_NT_WORKSTATION && os.wSuiteMask == VER_SUITE_PERSONAL)
					vmark=_T("Home");
				break;
			case 1:
				if(os.wProductType == VER_NT_WORKSTATION)
					vmark=_T("unknown1");
				else
					vmark=_T("unknown2");
				break;
			}
			break;
		}
	}
}
//从uninstall子键中查找软件版本信息，适合于自装软件
CString Cfunc::GetSoftwareInfo(LPCTSTR softwareName)
{
	unsigned long index;
	TCHAR buffer[MAX_PATH];
	HKEY hKey;
	LRESULT lr;
	CString ver;
	int res;
	res=1;
	ver.Empty();
	lr = RegOpenKey(HKEY_LOCAL_MACHINE, _T("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall"), & hKey);
	if(lr != ERROR_SUCCESS)		//打开注册表失败
	{
		ver.Format(_T("%s"),"打开注册表失败");
		return ver;
	}
	for(index =0; ;index++)
	{
		lr = RegEnumKey(hKey, index, buffer, sizeof(buffer));	//查找到的指定序号的子键的名称放入buffer中
		switch(lr)
		{
		case ERROR_SUCCESS:	//成功获得一个子键
			ver.Format(_T("%s"),softwareName);
			res = checkSoftwareVersion(buffer,hKey,softwareName,ver);	//操作一个子键
			break;
		case ERROR_NO_MORE_ITEMS:	//没有其它子键了，完成搜索
			ver.Format(_T("%s"),_T("完成搜索，没找到匹配软件"));
			RegCloseKey(hKey);
			MessageBoxW(NULL,_T("no match software"),_T("caption"),MB_OK);
			return ver;
		default:	//其它情况，未能完成搜索
			ver.Format(_T("%s"),_T("查找失败，未能完成搜索"));
			RegCloseKey(hKey);
			//MessageBoxW(NULL,_T("search fail"),_T("caption"),MB_OK);
			return ver;
		}
		if (res == 0)	//成功获取软件版本
		{
			//MessageBoxW(NULL,_T("get software version!"),_T("caption"),MB_OK);
			break;
		}
	}
	return ver;
}
//根据name获取注册表键下值项的信息，值结果存放在value中，这里不返回值类型信息
LRESULT Cfunc::GetValue(HKEY hKey, LPCTSTR name, LPTSTR value, LPLONG size)
{
	return ::RegQueryValueEx(hKey, name, NULL, NULL, (LPBYTE)value, (LPDWORD)size);
}
//根据name读取注册表键下的值，要求值类型为DWORD型，结果存放在value中
//注意：其实这个函数是不必要的，之前因为认识上的错误才添加了这个函数
//函数的第三个参数是用来获取具有指定名字的值项的类型，是输出参数，而不是输入参数，无需为其提供类型值
LRESULT Cfunc::GetValue2(HKEY hKey, LPCTSTR name, LPDWORD value)
{
	DWORD dwType = REG_DWORD;
	DWORD size=sizeof(DWORD);
	return ::RegQueryValueEx(hKey, name, NULL, &dwType, (LPBYTE)value, &size);
}
//内部函数，被调函数，调用者：GetSoftwareInfo()
//从uninstall子键中查找软件版本信息，适合于自装软件
//成功返回0，失败返回负值
int Cfunc::checkSoftwareVersion(LPCTSTR szKey , HKEY hParent , LPCTSTR softwareName ,CString & ver)
{
	CString ver2;
	LRESULT lr;
	HKEY hKey;
	LONG size;
	TCHAR buffer[MAX_PATH] ;
	lr = RegOpenKey(hParent, szKey, &hKey);
	//不能打开注册表（打开子键）
	if(lr != ERROR_SUCCESS)
	{
		//cout << _T("不能打开注册表！") << szKey << _T("(") << lr << _T(")") << endl;
		ver.Format(_T("%s"),_T("error on opening subkey"));
		return -1;
	} 
	//注册表打开成功
	size = sizeof(buffer);
	lr = GetValue(hKey, _T("DisplayName"), &buffer[0], &size);	//获得子键的指定值
	ver2.Format(_T("%s"),buffer);	
	if(lr == ERROR_SUCCESS)		//找到了一个键值
	{
		if(ver2.Find(ver) >= 0)	//看该值（软件名称）是否是想要的
		{
			size = sizeof(buffer);
			lr = GetValue(hKey, _T("DisplayVersion"), &buffer[0], &size);
			//获取软件版本号成功
			if(ERROR_SUCCESS == lr && size > 0)
			{
				RegCloseKey(hKey);
				ver.Format(_T("version : %s"),buffer);
				return 0;
			}
			else	//获取版本失败，返回 -4
			{
				RegCloseKey(hKey);
				ver.Format(_T("%s"),_T("unknown version"));
				return -4;
			}
		}
		else	//找到了键值但不是想要的，返回 -3
		{
			ver.Format(_T("%s"),_T("disMatch softwareName"));
			return -3;
		}
	}
	else	//没找到该键值，返回 -3
	{  
		RegCloseKey(hKey);
		ver.Format(_T("%s"),_T("unknown softwareName"));
		return -2;
	}	
	//软件开发商
	//
	//size = sizeof(buffer);
	//lr = GetValue(hKey, _T("Publisher"), &buffer[0], &size);
	//if(ERROR_SUCCESS == lr && size > 0)
	//{
	//	//cout << _T("开发商：") << buffer << endl;
	//}
	//
}
//获得指定键下值项的数据
bool Cfunc::regGetItemValue(hk_t hkType, LPCTSTR keyAddr, LPCTSTR keyValue,CString &res)
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
bool Cfunc::regGetItemValue(hk_t hkType, LPCTSTR keyAddr, LPCTSTR keyValue, int &res)
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
//判断IE浏览器是多少位的
int Cfunc::myGetIEBits()
{
	int sysBits;
	CString res;
	sysBits=GetSystemBits();
	if (sysBits == 32)
	{
		return 32;
	} 
	else
	{
		if(regGetItemValue(HKLM,_T(IEVER),_T("version"),res))
			sysBits=64;
		else
			sysBits=0;
		if(regGetItemValue(HKLM,_T("SOFTWARE//Wow6432Node//Microsoft//Internet Explorer"),_T("version"),res))
			sysBits+=32;
		return sysBits;
	}
}
//获取IE信任站点（域名部分），放入CListBox变量中
void Cfunc::getSafeStations(CListBox &list)
{
	HKEY hKey;
	LRESULT lr;
	lr = RegOpenKey(HKEY_CURRENT_USER, _T(DOMAINS), & hKey);
	if(lr != ERROR_SUCCESS)		//打开注册表失败
	{
		//info.Format(_T("%s"),"打开注册表失败");
		return;
	}
	enumKey1(list,hKey);
	RegCloseKey(hKey);
	return;
}
//被getSafeStations函数调用，专用型强，不宜在其它地方调用
//根据打开的键的句柄，枚举其下所有的子键，并放入CListBox类型变量中
//该函数用于读取两级子键专用，如果句柄指向的键其下没有两级子键或多于两级子键，都不宜调用该函数读取
void Cfunc::enumKey1(CListBox &list,HKEY hKey)
{
	TCHAR buffer[MAX_PATH]={0};
	LRESULT lr;
	unsigned long index;
	CString station;
	HKEY hKey2;
	index=0;
	while(1)
	{
		lr = RegEnumKey(hKey, index, buffer, sizeof(buffer));	//查找到的指定序号的子键的名称放入buffer中
		switch(lr)
		{
		case ERROR_SUCCESS:	//成功获得一个子键
			station.Format(_T("%s"),buffer);	//暂存子键名称
			lr = RegOpenKey(hKey, buffer, & hKey2);	//打开末第二子键----------------------这里读取子键失败！
			if(lr != ERROR_SUCCESS)		//打开末第二级子键失败
			{
				//list.AddString(station);
				return;	
			}
			index++;
			enumKey2(list,hKey2,station);		//末第二级子键打开成功
			RegCloseKey(hKey2);
			break;
		default:
			return;	//获得末第二级子键失败，返回
		}
	}
}
//被enumKey1函数调用，专用型强，不宜在其它地方调用
//根据打开键的句柄，枚举其下所有的子键，并放入CListBox类型变量中
//第3个参数为附加信息，每往CListBox变量中写一行，这个附加信息都会出现在行首
void Cfunc::enumKey2(CListBox &list,HKEY hKey2,CString station)
{
	LRESULT lr;
	unsigned long index;
	CString station2;
	TCHAR buffer[MAX_PATH]={0};
	index=0;
	while(1)	//打开末第二子键成功
	{
		lr = RegEnumKey(hKey2, index, buffer, sizeof(buffer));	//枚举末第一子键放入buffer中
		switch( lr)
		{
		case ERROR_SUCCESS:
			station2.Empty();
			station2.Format(_T("%s."),buffer);	//暂存子键名称
			station2 += station;
			list.AddString(station2);
			index++;
			break;
		default:
			list.AddString(station);
			index++;
			return;
		}
	}
}
//搜索指定键下的所有子键，并把符合keyWord的子键其下的值放入列表框变量中
void Cfunc::getKeyWords(CListBox &list,LPCTSTR keyPath,LPCTSTR keyWords)
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
//被getKeyWords函数调用
void Cfunc::checkEnumKey(LPCTSTR szKey , HKEY hParent , LPCTSTR keyWords ,CListBox &list)
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
//IE类中添加信任站点用到的函数：：添加站点到注册表，如出错，会弹出错误提示
bool Cfunc::addIP(CString ip)
{
	CString parrentKey,childKey;
	CString str,subStr;
	int i;
	parrentKey.Empty();
	childKey.Empty();
	if(isLegal(ip) != true)	//非法字符处理
	{
		MessageBox(GetActiveWindow(),_T("存在非法字符，添加失败！\n您可以尝试在\
			'Internet属性/安全'中重新添加。"),_T("提示"),MB_OK);
		return false;
	}
	if(isDomain(ip)== false)	//是ip
	{
		MessageBox(GetActiveWindow(),_T("是ip"),_T("提示"),MB_OK);
		ipFormat(ip);	//合法ip，完成ip的标准转化
		
	}
	else	//是域名
	{
		MessageBox(GetActiveWindow(),_T("是域名"),_T("提示"),MB_OK);
		str=ip;
		subStr=separate2(str,'.');
		parrentKey=subStr;
		if(subStr.IsEmpty() == true)	//域名没有分段
			parrentKey=str;
		else
		{
			for(i=0;i<2;i++)
			{
				subStr=separate2(str,'.');
				if(subStr.IsEmpty()==true)
				{
					parrentKey = str + _T(".") + parrentKey;
					break;
				}
				parrentKey = subStr + _T(".") + parrentKey;
			}
			childKey=str;
		}
		if( parrentKey == ip)	//ip取完三段后，还有没有其它的段
		{
			MessageBox(GetActiveWindow(),parrentKey,_T("添加键"),MB_OK);
			Cfunc func;
			func.regAddKey(HKCU,_T(DOMAINS),parrentKey);
			parrentKey=_T("\\")+parrentKey;
			parrentKey = _T(DOMAINS)+parrentKey;
			func.regAddValue(HKCU,parrentKey,_T("*"),REG_DWORD,_T("2"));
		}
		else
		{
			MessageBox(GetActiveWindow(),parrentKey,_T("添加父键"),MB_OK);
			Cfunc func;
			func.regAddKey(HKCU,_T(DOMAINS),parrentKey);
			MessageBox(GetActiveWindow(),childKey,_T("添加子键"),MB_OK);
			parrentKey=_T("\\")+parrentKey;
			func.regAddKey(HKCU,_T(DOMAINS)+parrentKey,childKey);
			parrentKey=_T(DOMAINS)+parrentKey+_T("\\")+childKey;
			func.regAddValue(HKCU,parrentKey,_T("*"),REG_DWORD,_T("2"));
		}
	}
	return true;

}
//判断字符串中是否有非法字符
bool Cfunc::isLegal(CString ip)
{
	if(ip.Find('\\') >= 0)
		return false;
	if(ip.Find('*') >= 0)
		return false;
	int len,index;
	char ch;
	len=ip.GetLength();
	for(index = 0 ; index < len ; index++)
	{
		ch=ip[index];
		if ( ch > 127 || ch < 0)
			return false;
	}
	return true;
}
//判断是含字母的域名，还是纯数字的ip,是域名返回true
bool Cfunc::isDomain(CString ip)
{
	int len,index,num;
	char ch;
	CString str,subStr;
	len=ip.GetLength();
	for(index = 0 ; index < len ; index++)
	{
		ch=ip[index];
		if (( ch < '0' || ch > '9') && ch !='.')
			return true;
	}
	str=ip;
	int i;
	for(i=0;i<3;i++)
	{
		subStr=separate(str,'.');
		if (subStr.IsEmpty() == true)		//是数字，但只有一个字段
			break;
		//pSubStr=subStr.GetBuffer(1024);
		num=strtoi(subStr);			//是数字，但有多于一个的字段
		//subStr.ReleaseBuffer();
		if(num > 255)				//且第一字段数字大于255
			return true;
	}
	return false;
}
//字符串操作，第一个delim为分界符，将str分为两个字符串，前者做函数返回值，后者以形参形式返回（ .之前的字符如果也是.,则不认作是分隔符）
CString Cfunc::separate(CString & str,char delim)
{
	int pos;
	CString subStr;
	//pos = str.ReverseFind('.');
	subStr.Empty();
	pos=findDelim(str,delim);	//得到的是0始位置，0始位置是n，则说明其前面有n个字符
	if(pos < 0)
		return subStr;
	subStr=str.Left(pos);
	str.Delete(0,pos+1);
	return subStr;
}
//字符串操作，最后一个delim为分界符，将str分为两个字符串，后者做函数返回值，前者以形参形式返回
CString Cfunc::separate2(CString & str,char delim)
{
	int pos;
	CString subStr;
	CString tmpStr;
	subStr.Empty();
	pos = reverseFindDelim(str,delim);
	if (pos < 0)
		return subStr;
	//pos=str.Find('.');	//得到的是0始位置，0始位置是n，则说明其前面有n个字符
	subStr=str.Left(pos);
	str.Delete(0,pos+1);
	// subStr <-> str
	tmpStr=subStr;
	subStr=str;
	str=tmpStr;
	return subStr;
}
//CString 转无符号整形，遇到非法字符返回
UINT Cfunc::strtoui(CString str)
{
	UINT res=0;
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
//CString 转整形，遇到非法字符返回
int Cfunc::strtoi(CString str)
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
//字符串操作，查找分割符第一次出现的位置，如果位置为0或之前紧临有同样的给定分隔符，则不算作是真正的分隔符
int Cfunc::findDelim(CString str,char delim)
{
	int pos,offset;
	offset=0;
	pos=str.Find(delim);
	if(pos < 0)
		return -1;
	while(pos >= 0)
	{
		if(pos == 0)
		{
			str.Delete(0);
			offset++;
		}
		else
			break;
		pos=str.Find(delim);
	}
	if(pos > 0)
		return pos+offset;
	else
		return -1;
}
//字符串操作，反向查找分割符第一次出现的位置，如果位置为0或之前紧临有同样的给定分隔符，则不算作是真正的分隔符
int Cfunc::reverseFindDelim(CString str,char delim)
{
	int pos,offset;
	offset=0;
	pos=str.ReverseFind(delim);
	if(pos < 0)
		return -1;
	while(pos > 0)
	{
		if(pos == str.GetLength()-1)
			str.Delete(pos);
		else if( str[pos-1] == delim)
			str.Delete(pos);
		else
			break;
		pos=str.ReverseFind(delim);
	}
	return pos;
}
//从字符串的第index个delim之后取len个字符返回
CString Cfunc::getStrAfterDelim(CString str,TCHAR delim,int index,int len)
{
	int pos;
	if(len <=0 || index == 0)
		return _T("");
	if(index == 0)
		return str.Left(len);
	for(int i=1;i<=index;i++)
	{
		pos=str.Find(delim,pos);
	}

	CString tmpStr,tmpStr2;
	tmpStr=str.Right(str.GetLength()-pos);
	tmpStr2=tmpStr.Left(len);
	return tmpStr2;
}
//返回字符串str的第index到index+1个delim之间的字符
CString Cfunc::getStrAfterDelim(CString str,TCHAR delim,int index)
{
	int pos=0;
	int len;
	len=str.Find(delim);
	CString ret;
	ret.Empty();
	if(len == -1)
		return ret;
	if(index == 0)
	{
		ret=str.Left(len);
		return ret;
	}
	//CString leaveStr;
	int i;
	for(i=1;i<=index;i++)
	{
		str=str.Right(str.GetLength()-str.Find(delim)-1);
		if(str.Find(delim) == -1)
			return str;
	}

	len=str.Find(delim);
	ret=str.Left(len);
	return ret;
}
//注册表添加键，不添加键值
bool Cfunc::regAddKey(hk_t hk,CString path,CString key)
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
bool Cfunc::regAddValue(hk_t hk,CString path,CString name,DWORD dataType,CString value)
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
//检查office版本
bool Cfunc::getOfficeVersion(CString &ver)
{
	ver.Empty();
	HKEY hk0,hk8,hk9,hk10,hk11,hk12,hk14;
	hk0=hk8=hk9=hk10=hk11=hk12=hk14=NULL;
	LRESULT r0,r8,r9,r10,r11,r12,r14;
	r0=r8=r9=r10=r11=r12=r14=-1;
	r0=RegOpenKey(HKEY_LOCAL_MACHINE,_T("SOFTWARE\\Microsoft"),&hk0);
	if(r0 != ERROR_SUCCESS) 
		return false;
	else
		RegCloseKey(hk0);
	r8=RegOpenKey(HKEY_LOCAL_MACHINE,_T("SOFTWARE\\Microsoft\\Office\\8.0\\Word\\InstallRoot"),&hk8);
	if(r8 == ERROR_SUCCESS)	
	{
		ver=_T("97");
		RegCloseKey(hk8);
	}
	r9=RegOpenKey(HKEY_LOCAL_MACHINE,_T("SOFTWARE\\Microsoft\\Office\\9.0\\Word\\InstallRoot"),&hk9);
	if(r9 == ERROR_SUCCESS)	
	{
		ver.IsEmpty() ? ver=_T("2000")  : ver+=_T(" & 2000");
		RegCloseKey(hk9);
	}
	r10=RegOpenKey(HKEY_LOCAL_MACHINE,_T("SOFTWARE\\Microsoft\\Office\\10.0\\Word\\InstallRoot"),&hk10);
	if(r10 == ERROR_SUCCESS)	
	{
		ver.IsEmpty() ? ver=_T("xp") : ver+=_T(" & xp");
		RegCloseKey(hk10);
	}
	r11=RegOpenKey(HKEY_LOCAL_MACHINE,_T("SOFTWARE\\Microsoft\\Office\\11.0\\Word\\InstallRoot"),&hk11);
	if(r11 == ERROR_SUCCESS)	
	{
		ver.IsEmpty() ? ver=_T("2003") : ver+=_T(" & 2003");
		RegCloseKey(hk11);
	}
	r12=RegOpenKey(HKEY_LOCAL_MACHINE,_T("SOFTWARE\\Microsoft\\Office\\12.0\\Word\\InstallRoot"),&hk12);
	if(r12 == ERROR_SUCCESS)	
	{
		ver.IsEmpty() ? ver=_T("2007") : ver+=_T(" & 2007");
		RegCloseKey(hk12);
	}
	r14=RegOpenKey(HKEY_LOCAL_MACHINE,_T("SOFTWARE\\Microsoft\\Office\\14.0\\Word\\InstallRoot"),&hk14);
	if(r14 ==ERROR_SUCCESS)	
	{
		ver.IsEmpty() ? ver=_T("2010") : ver+=_T(" & 2010");
		RegCloseKey(hk14);
	}
	return true;
}
//转换office版本
bool Cfunc::OfficeVersionConvert(CString &ver)
{
	CString ver2;
	ver2.Empty();
	if(ver.Compare(_T("11.0")) == 0)
		ver2.Format(_T("%s"),_T("2003"));
	else if(ver.Compare(_T("2003")) == 0)
		ver2.Format(_T("%s"),_T("11.0"));
	else if(ver.Compare(_T("8.0")) == 0)
		ver2.Format(_T("%s"),_T("97"));
	else if(ver.Compare(_T("97")) == 0)
		ver2.Format(_T("%s"),_T("8.0"));
	else if(ver.Compare(_T("9.0")) == 0)
		ver2.Format(_T("%s"),_T("2000"));
	else if(ver.Compare(_T("2000")) == 0)
		ver2.Format(_T("%s"),_T("9.0"));
	else if(ver.Compare(_T("xp")) == 0)
		ver2.Format(_T("%s"),_T("10.0"));
	else if(ver.Compare(_T("10.0")) == 0)
		ver2.Format(_T("%s"),_T("xp"));
	else if(ver.Compare(_T("12.0")) == 0)
		ver2.Format(_T("%s"),_T("2007"));
	else if(ver.Compare(_T("2007")) == 0)
		ver2.Format(_T("%s"),_T("12.0"));
	else if(ver.Compare(_T("14.0")) == 0)
		ver2.Format(_T("%s"),_T("2010"));
	else if(ver.Compare(_T("2010")) == 0)
		ver2.Format(_T("%s"),_T("14.0"));

	ver=ver2;
	if(ver2.IsEmpty())
		return false;
	else
		return true;
}
bool Cfunc::ipFormat(CString &ip)
{
	int len,index;
	char ch;
	Cfunc func;
	len=ip.GetLength();
	for(index = 0 ; index < len ; index++)
	{
		ch=ip[index];
		if (( ch < '0' || ch > '9') && ch !='.')
			return false;
	}
	int carry;		//商
	int remainder;	//余数
	CString str_rem;//余数转换成的字符串
	CString pool;	//数据缓冲池
	CString result;	//结果IP
	pool.Empty();
	carry=0;
	pool=Cfunc::separate2(ip,'.');
	if(pool.IsEmpty())
	{
		pool=ip;
		ip.Empty();
	}
	while(1)
	{
		if(pool.IsEmpty() && carry == 0)
			break;
		carry += Cfunc::strtoi(pool);
		remainder=carry % 255;
		carry /= 255;
		str_rem.Format(_T("%d"),remainder);
		if(result.IsEmpty())
			result=str_rem;
		else
			result=str_rem+_T(".")+result;
		pool=separate2(ip,'.');
		if(pool.IsEmpty())
		{
			pool=ip;
			ip.Empty();
		}
	}
	ip=result;
	return true;
}
//获取可执行文件版本信息,摘自网络,代码中4处注释部分为改动部分
CString Cfunc::getExeInfo(CString AppName)
{
	CString AppVersion;
	DWORD RessorceVersionInfoSize;
	DWORD JustAJunkVariable;
	CHAR * VersionInfoPtr;
	struct LANGANDCODEPAGE{
		WORD wLanguage;
		WORD wCodePage;
	} *TranslationPtr;
	CHAR *InformationPtr;
	UINT VersionInfoSize;
	CHAR VersionValue[255];
	CString VersionValue2;
	LPTSTR lpVersionValue2;
	//SetLastError(3);
	//DWORD err=GetLastError();
	RessorceVersionInfoSize=10;
	//RessorceVersionInfoSize=GetFileVersionInfoSizeW((LPCTSTR)AppName,&JustAJunkVariable);
	//形参用char *AppName，错误代码：1812(资源数据没有发现)，可能是由于编码问题。
	RessorceVersionInfoSize=GetFileVersionInfoSizeW(AppName,NULL);
	//err=GetLastError();	//
	if( 0 != RessorceVersionInfoSize)
	{
		VersionInfoPtr=new CHAR[RessorceVersionInfoSize];
		if(GetFileVersionInfoW((LPCTSTR)AppName,0,RessorceVersionInfoSize,VersionInfoPtr))
		{
			if(!VerQueryValueW(VersionInfoPtr,_T("\\VarFileInfo\\Translation"),\
				(LPVOID *)&TranslationPtr,&VersionInfoSize))
			{
				delete[] VersionInfoPtr;
				return AppVersion;
			}
		}
		//wsprintf((LPTSTR)VersionValue,_T("\\StringFileInfo\\%04x%04x\\FileVersion"),\
					TranslationPtr[0].wLanguage,TranslationPtr[0].wCodePage);	//转换不成功
		VersionValue2.Format(_T("\\StringFileInfo\\%04x%04x\\FileVersion"),\
								TranslationPtr[0].wLanguage,TranslationPtr[0].wCodePage);
		lpVersionValue2=VersionValue2.GetBuffer(512);
		//if(!VerQueryValueW(VersionInfoPtr,(LPTSTR)VersionValue,(LPVOID *)&InformationPtr,&VersionInfoSize))
		if(!VerQueryValueW(VersionInfoPtr,lpVersionValue2,(LPVOID *)&InformationPtr,&VersionInfoSize))
		{
			delete[] VersionInfoPtr;
			return AppVersion;
		}
		if(strlen(InformationPtr)>0)	
		{
			//AppVersion=CString(InformationPtr);
			AppVersion.Format(_T("%s"),InformationPtr);
		}
		delete[] VersionInfoPtr;
	}
	return AppVersion;
}
bool Cfunc::getRegItemValue(hk_t hk,CString sKeyPath,CString sItemName,LPTSTR value, LPDWORD size)
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

CString Cfunc::getDateTime(void)
{
	SYSTEMTIME systime;
	GetLocalTime(&systime);
	CString time;
	time.Format(_T("%04d-%02d-%02d %02d:%02d:%02d.%03d"),systime.wYear,systime.wMonth,systime.wDay,systime.wHour,systime.wMinute,systime.wSecond,systime.wMilliseconds);
	return time;
}
CString Cfunc::getDateTime1(void)
{
	SYSTEMTIME systime;
	GetLocalTime(&systime);
	CString time;
	time.Format(_T("%d-%d-%d %d:%d:%d"),systime.wYear,systime.wMonth,systime.wDay,systime.wHour,systime.wMinute,systime.wSecond,systime.wMilliseconds);
	return time;
}
CString Cfunc::getDateTime2(void)
{
	SYSTEMTIME systime;
	GetLocalTime(&systime);
	CString time;
	
	time.Format(_T("%04d%02d%02d%02d%02d%02d%03d"),systime.wYear,systime.wMonth,systime.wDay,systime.wHour,systime.wMinute,systime.wSecond,systime.wMilliseconds);

	return time;
}
CString Cfunc::getTempPath()
{
	TCHAR path[MAX_PATH];
	//GetCurrentDirectory(MAX_PATH,path);
	GetTempPath(MAX_PATH,path);	//获得的temp路径结尾带有反斜线
	CString strPath;
	strPath=path;
	return strPath;
}
//路径结尾带有反斜线
CString Cfunc::getModulePath()
{
	TCHAR buf[MAX_PATH];
	GetModuleFileName((HMODULE)AfxGetInstanceHandle(), buf, sizeof(buf));
	CString strPath;
	strPath=buf;
	int pos;
	pos=strPath.ReverseFind('\\');
	strPath=strPath.Left(pos+1);
	return strPath;
}