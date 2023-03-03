#include "stdafx.h"
#include "func.h"
#include <Windows.h>
Cfunc::Cfunc()
{
}
Cfunc::~Cfunc()
{
}
//��ȫ�Ļ�ȡ��ʵϵͳ��Ϣ
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
//��ò���ϵͳλ��
int Cfunc::GetSystemBits()
{
	SYSTEM_INFO si;
	SafeGetNativeSystemInfo(&si);
	if(si.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_AMD64 || si.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_IA64)
		return 64;
	else
		return 32;
}
//��ò���ϵͳ����
void Cfunc::GetSysName(CString &osname){
			 SYSTEM_INFO info;	//�øýṹ�ж�64ΪAMD������
			 GetSystemInfo(&info);	//���øú������ṹ
			 OSVERSIONINFOEX os;	//����ϵͳ��Ϣ
			 //OSVERSIONINFOEXA os;
			 os.dwOSVersionInfoSize=sizeof(OSVERSIONINFOEX);
			 osname=_T("unknown OperatingSystem.");	//�ȼٶ�����ϵͳ����δ֪
			 if ( GetVersionEx( (LPOSVERSIONINFOW) &os ) )		//os����ջ���󣩴���
				
				{
					
					//������ݰ汾��Ϣ�жϲ���ϵͳ����
					switch(os.dwMajorVersion)	//�ж����汾��
					{
					case 4:
						switch(os.dwMinorVersion)	//�жϴΰ汾��
						{
						case 0:
							if (os.dwPlatformId ==	VER_PLATFORM_WIN32_NT)
							{
								osname=_T("Microsoft Window NT 4.0");	//1996��7�·���
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
							osname=_T("Microsoft Windows 2000");	//99��12�·���
							break;
						case 1:
							osname=_T("Microsoft windows XP");	//01��8�·���
							break;
						case 2:
							if (os.wProductType == VER_NT_WORKSTATION && info.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_AMD64)	//��Ʒ���ͺʹ���������
							{
								osname=_T("Microsoft Windows XP Professional X64 Edition");
							}
							else if ( GetSystemMetrics(SM_SERVERR2) != 0)	//metrics: ������n.��
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

// ��ȡ����ϵͳ�汾
void Cfunc::GetVersionMark(CString &vmark)
{
	
	OSVERSIONINFOEX os;
	os.dwOSVersionInfoSize=sizeof(OSVERSIONINFOEX);
	vmark=_T("unknown version");
	//if(GetVersionEx((LPOSVERSIONINFOW)os))
	if ( GetVersionEx( (LPOSVERSIONINFOW) &os ) )		//os����ջ���󣩴���

	{

		//������ݰ汾��Ϣ�жϲ���ϵͳ����
		switch(os.dwMajorVersion)	//�ж����汾��
		{
		/*
		case 4:
			switch(os.dwMinorVersion)	//�жϴΰ汾��
			{
			case 0:
				if (os.dwPlatformId ==	VER_PLATFORM_WIN32_NT)
				{
					osname=_T("Microsoft Window NT 4.0");	//1996��7�·���
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
//��uninstall�Ӽ��в�������汾��Ϣ���ʺ�����װ���
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
	if(lr != ERROR_SUCCESS)		//��ע���ʧ��
	{
		ver.Format(_T("%s"),"��ע���ʧ��");
		return ver;
	}
	for(index =0; ;index++)
	{
		lr = RegEnumKey(hKey, index, buffer, sizeof(buffer));	//���ҵ���ָ����ŵ��Ӽ������Ʒ���buffer��
		switch(lr)
		{
		case ERROR_SUCCESS:	//�ɹ����һ���Ӽ�
			ver.Format(_T("%s"),softwareName);
			res = checkSoftwareVersion(buffer,hKey,softwareName,ver);	//����һ���Ӽ�
			break;
		case ERROR_NO_MORE_ITEMS:	//û�������Ӽ��ˣ��������
			ver.Format(_T("%s"),_T("���������û�ҵ�ƥ�����"));
			RegCloseKey(hKey);
			MessageBoxW(NULL,_T("no match software"),_T("caption"),MB_OK);
			return ver;
		default:	//���������δ���������
			ver.Format(_T("%s"),_T("����ʧ�ܣ�δ���������"));
			RegCloseKey(hKey);
			//MessageBoxW(NULL,_T("search fail"),_T("caption"),MB_OK);
			return ver;
		}
		if (res == 0)	//�ɹ���ȡ����汾
		{
			//MessageBoxW(NULL,_T("get software version!"),_T("caption"),MB_OK);
			break;
		}
	}
	return ver;
}
//����name��ȡע������ֵ�����Ϣ��ֵ��������value�У����ﲻ����ֵ������Ϣ
LRESULT Cfunc::GetValue(HKEY hKey, LPCTSTR name, LPTSTR value, LPLONG size)
{
	return ::RegQueryValueEx(hKey, name, NULL, NULL, (LPBYTE)value, (LPDWORD)size);
}
//����name��ȡע�����µ�ֵ��Ҫ��ֵ����ΪDWORD�ͣ���������value��
//ע�⣺��ʵ��������ǲ���Ҫ�ģ�֮ǰ��Ϊ��ʶ�ϵĴ����������������
//�����ĵ�����������������ȡ����ָ�����ֵ�ֵ������ͣ�������������������������������Ϊ���ṩ����ֵ
LRESULT Cfunc::GetValue2(HKEY hKey, LPCTSTR name, LPDWORD value)
{
	DWORD dwType = REG_DWORD;
	DWORD size=sizeof(DWORD);
	return ::RegQueryValueEx(hKey, name, NULL, &dwType, (LPBYTE)value, &size);
}
//�ڲ����������������������ߣ�GetSoftwareInfo()
//��uninstall�Ӽ��в�������汾��Ϣ���ʺ�����װ���
//�ɹ�����0��ʧ�ܷ��ظ�ֵ
int Cfunc::checkSoftwareVersion(LPCTSTR szKey , HKEY hParent , LPCTSTR softwareName ,CString & ver)
{
	CString ver2;
	LRESULT lr;
	HKEY hKey;
	LONG size;
	TCHAR buffer[MAX_PATH] ;
	lr = RegOpenKey(hParent, szKey, &hKey);
	//���ܴ�ע������Ӽ���
	if(lr != ERROR_SUCCESS)
	{
		//cout << _T("���ܴ�ע���") << szKey << _T("(") << lr << _T(")") << endl;
		ver.Format(_T("%s"),_T("error on opening subkey"));
		return -1;
	} 
	//ע���򿪳ɹ�
	size = sizeof(buffer);
	lr = GetValue(hKey, _T("DisplayName"), &buffer[0], &size);	//����Ӽ���ָ��ֵ
	ver2.Format(_T("%s"),buffer);	
	if(lr == ERROR_SUCCESS)		//�ҵ���һ����ֵ
	{
		if(ver2.Find(ver) >= 0)	//����ֵ��������ƣ��Ƿ�����Ҫ��
		{
			size = sizeof(buffer);
			lr = GetValue(hKey, _T("DisplayVersion"), &buffer[0], &size);
			//��ȡ����汾�ųɹ�
			if(ERROR_SUCCESS == lr && size > 0)
			{
				RegCloseKey(hKey);
				ver.Format(_T("version : %s"),buffer);
				return 0;
			}
			else	//��ȡ�汾ʧ�ܣ����� -4
			{
				RegCloseKey(hKey);
				ver.Format(_T("%s"),_T("unknown version"));
				return -4;
			}
		}
		else	//�ҵ��˼�ֵ��������Ҫ�ģ����� -3
		{
			ver.Format(_T("%s"),_T("disMatch softwareName"));
			return -3;
		}
	}
	else	//û�ҵ��ü�ֵ������ -3
	{  
		RegCloseKey(hKey);
		ver.Format(_T("%s"),_T("unknown softwareName"));
		return -2;
	}	
	//���������
	//
	//size = sizeof(buffer);
	//lr = GetValue(hKey, _T("Publisher"), &buffer[0], &size);
	//if(ERROR_SUCCESS == lr && size > 0)
	//{
	//	//cout << _T("�����̣�") << buffer << endl;
	//}
	//
}
//���ָ������ֵ�������
bool Cfunc::regGetItemValue(hk_t hkType, LPCTSTR keyAddr, LPCTSTR keyValue,CString &res)
{
	unsigned long index;
	TCHAR buffer[MAX_PATH];
	HKEY hKey;
	LRESULT lr;
	LONG size;
	res.Empty();
	if (hkType == HKLM)
		lr = RegOpenKey(HKEY_LOCAL_MACHINE, keyAddr, &hKey);	//�ɼ��ó�ָ��ָ���·����������Ĵ�ע����
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
		res.Format(_T("%s"), _T("hkType��������"));
		return false;
	}
	if (lr != ERROR_SUCCESS)		//��ע���ʧ��
	{
		res.Format(_T("%s"), _T("��ע���ʧ��"));
		return false;
	}
	//ע���򿪳ɹ�
	size = sizeof(buffer);
	lr = GetValue(hKey, keyValue, &buffer[0], &size);	//���ֵ�������
	if (lr == ERROR_SUCCESS)		//�ҵ��˶�Ӧֵ��
	{
		res.Format(_T("%s"), buffer);
		RegCloseKey(hKey);
		return true;
	}
	else
	{
		res.Format(_T("%s"), _T("��ȡֵ��ʧ��"));
		RegCloseKey(hKey);
		return false;
	}
}
//��ü���ָ��ֵ���������Ϣ
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
	if (lr != ERROR_SUCCESS)		//��ע���ʧ��
	{
		///MessageBox(NULL, _T("��ע���ʧ��"), _T("notion"), MB_OK);
		return false;
	}
	//ע���򿪳ɹ�

	size = sizeof(buffer);
	//lr = GetValue2(hKey, keyValue, &buffer, &size);	//����Ӽ���ָ��ֵ
	lr = GetValue2(hKey, keyValue, &buffer);
	if (lr == ERROR_SUCCESS)		//�ҵ���һ����ֵ
	{
		//MessageBox(NULL, _T("�ҵ���һ����ֵ"), _T("notion"), MB_OK);
		RegCloseKey(hKey);
		res = buffer;
		return true;
	}
	else
	{
		//MessageBox(NULL, _T("������ֵʧ��"), _T("notion"), MB_OK);
		RegCloseKey(hKey);
		res = buffer;
		return false;
	}
}
//�ж�IE������Ƕ���λ��
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
//��ȡIE����վ�㣨�������֣�������CListBox������
void Cfunc::getSafeStations(CListBox &list)
{
	HKEY hKey;
	LRESULT lr;
	lr = RegOpenKey(HKEY_CURRENT_USER, _T(DOMAINS), & hKey);
	if(lr != ERROR_SUCCESS)		//��ע���ʧ��
	{
		//info.Format(_T("%s"),"��ע���ʧ��");
		return;
	}
	enumKey1(list,hKey);
	RegCloseKey(hKey);
	return;
}
//��getSafeStations�������ã�ר����ǿ�������������ط�����
//���ݴ򿪵ļ��ľ����ö���������е��Ӽ���������CListBox���ͱ�����
//�ú������ڶ�ȡ�����Ӽ�ר�ã�������ָ��ļ�����û�������Ӽ�����������Ӽ��������˵��øú�����ȡ
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
		lr = RegEnumKey(hKey, index, buffer, sizeof(buffer));	//���ҵ���ָ����ŵ��Ӽ������Ʒ���buffer��
		switch(lr)
		{
		case ERROR_SUCCESS:	//�ɹ����һ���Ӽ�
			station.Format(_T("%s"),buffer);	//�ݴ��Ӽ�����
			lr = RegOpenKey(hKey, buffer, & hKey2);	//��ĩ�ڶ��Ӽ�----------------------�����ȡ�Ӽ�ʧ�ܣ�
			if(lr != ERROR_SUCCESS)		//��ĩ�ڶ����Ӽ�ʧ��
			{
				//list.AddString(station);
				return;	
			}
			index++;
			enumKey2(list,hKey2,station);		//ĩ�ڶ����Ӽ��򿪳ɹ�
			RegCloseKey(hKey2);
			break;
		default:
			return;	//���ĩ�ڶ����Ӽ�ʧ�ܣ�����
		}
	}
}
//��enumKey1�������ã�ר����ǿ�������������ط�����
//���ݴ򿪼��ľ����ö���������е��Ӽ���������CListBox���ͱ�����
//��3������Ϊ������Ϣ��ÿ��CListBox������дһ�У����������Ϣ�������������
void Cfunc::enumKey2(CListBox &list,HKEY hKey2,CString station)
{
	LRESULT lr;
	unsigned long index;
	CString station2;
	TCHAR buffer[MAX_PATH]={0};
	index=0;
	while(1)	//��ĩ�ڶ��Ӽ��ɹ�
	{
		lr = RegEnumKey(hKey2, index, buffer, sizeof(buffer));	//ö��ĩ��һ�Ӽ�����buffer��
		switch( lr)
		{
		case ERROR_SUCCESS:
			station2.Empty();
			station2.Format(_T("%s."),buffer);	//�ݴ��Ӽ�����
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
//����ָ�����µ������Ӽ������ѷ���keyWord���Ӽ����µ�ֵ�����б�������
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
	if(lr != ERROR_SUCCESS)		//��ע���ʧ��
	{
		return;
	}
	for(index =0; ;index++)
	{
		lr = RegEnumKey(hKey, index, buffer, sizeof(buffer));	//���ҵ���ָ����ŵ��Ӽ������Ʒ���buffer��
		switch(lr)
		{
		case ERROR_SUCCESS:	//�ɹ����һ���Ӽ�
			checkEnumKey(buffer,hKey,keyWords,list);	//����һ���Ӽ�
			break;
		case ERROR_NO_MORE_ITEMS:	//û�������Ӽ��ˣ��������
			//ver.Format(_T("%s"),_T("���������û�ҵ�ƥ�����"));
			RegCloseKey(hKey);
			//MessageBoxW(NULL,_T("no match software"),_T("caption"),MB_OK);
			return;
		default:	//���������δ���������
			//ver.Format(_T("%s"),_T("����ʧ�ܣ�δ���������"));
			RegCloseKey(hKey);
			//MessageBoxW(NULL,_T("search faild"),_T("caption"),MB_OK);
			return;
		}
	}
	return;
}
//��getKeyWords��������
void Cfunc::checkEnumKey(LPCTSTR szKey , HKEY hParent , LPCTSTR keyWords ,CListBox &list)
{
	CString ver2;
	LRESULT lr;
	HKEY hKey;
	LONG size;
	TCHAR buffer[MAX_PATH] ;
	lr = RegOpenKey(hParent, szKey, &hKey);
	//���ܴ�ע������Ӽ���
	if(lr != ERROR_SUCCESS)
		return ;
	//ע���򿪳ɹ�
	size = sizeof(buffer);
	lr = GetValue(hKey, keyWords, &buffer[0], &size);	//����Ӽ���ָ��ֵ
	ver2.Format(_T("%s"),buffer);	
	if(lr == ERROR_SUCCESS)		//�ҵ��˸ü�ֵ
	{
		list.AddString(ver2);
	}
	else	//û�ҵ��ü�ֵ
	{  
		return;
	}	
}
//IE�����������վ���õ��ĺ����������վ�㵽ע���������ᵯ��������ʾ
bool Cfunc::addIP(CString ip)
{
	CString parrentKey,childKey;
	CString str,subStr;
	int i;
	parrentKey.Empty();
	childKey.Empty();
	if(isLegal(ip) != true)	//�Ƿ��ַ�����
	{
		MessageBox(GetActiveWindow(),_T("���ڷǷ��ַ������ʧ�ܣ�\n�����Գ�����\
			'Internet����/��ȫ'��������ӡ�"),_T("��ʾ"),MB_OK);
		return false;
	}
	if(isDomain(ip)== false)	//��ip
	{
		MessageBox(GetActiveWindow(),_T("��ip"),_T("��ʾ"),MB_OK);
		ipFormat(ip);	//�Ϸ�ip�����ip�ı�׼ת��
		
	}
	else	//������
	{
		MessageBox(GetActiveWindow(),_T("������"),_T("��ʾ"),MB_OK);
		str=ip;
		subStr=separate2(str,'.');
		parrentKey=subStr;
		if(subStr.IsEmpty() == true)	//����û�зֶ�
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
		if( parrentKey == ip)	//ipȡ�����κ󣬻���û�������Ķ�
		{
			MessageBox(GetActiveWindow(),parrentKey,_T("��Ӽ�"),MB_OK);
			Cfunc func;
			func.regAddKey(HKCU,_T(DOMAINS),parrentKey);
			parrentKey=_T("\\")+parrentKey;
			parrentKey = _T(DOMAINS)+parrentKey;
			func.regAddValue(HKCU,parrentKey,_T("*"),REG_DWORD,_T("2"));
		}
		else
		{
			MessageBox(GetActiveWindow(),parrentKey,_T("��Ӹ���"),MB_OK);
			Cfunc func;
			func.regAddKey(HKCU,_T(DOMAINS),parrentKey);
			MessageBox(GetActiveWindow(),childKey,_T("����Ӽ�"),MB_OK);
			parrentKey=_T("\\")+parrentKey;
			func.regAddKey(HKCU,_T(DOMAINS)+parrentKey,childKey);
			parrentKey=_T(DOMAINS)+parrentKey+_T("\\")+childKey;
			func.regAddValue(HKCU,parrentKey,_T("*"),REG_DWORD,_T("2"));
		}
	}
	return true;

}
//�ж��ַ������Ƿ��зǷ��ַ�
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
//�ж��Ǻ���ĸ�����������Ǵ����ֵ�ip,����������true
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
		if (subStr.IsEmpty() == true)		//�����֣���ֻ��һ���ֶ�
			break;
		//pSubStr=subStr.GetBuffer(1024);
		num=strtoi(subStr);			//�����֣����ж���һ�����ֶ�
		//subStr.ReleaseBuffer();
		if(num > 255)				//�ҵ�һ�ֶ����ִ���255
			return true;
	}
	return false;
}
//�ַ�����������һ��delimΪ�ֽ������str��Ϊ�����ַ�����ǰ������������ֵ���������β���ʽ���أ� .֮ǰ���ַ����Ҳ��.,�������Ƿָ�����
CString Cfunc::separate(CString & str,char delim)
{
	int pos;
	CString subStr;
	//pos = str.ReverseFind('.');
	subStr.Empty();
	pos=findDelim(str,delim);	//�õ�����0ʼλ�ã�0ʼλ����n����˵����ǰ����n���ַ�
	if(pos < 0)
		return subStr;
	subStr=str.Left(pos);
	str.Delete(0,pos+1);
	return subStr;
}
//�ַ������������һ��delimΪ�ֽ������str��Ϊ�����ַ�������������������ֵ��ǰ�����β���ʽ����
CString Cfunc::separate2(CString & str,char delim)
{
	int pos;
	CString subStr;
	CString tmpStr;
	subStr.Empty();
	pos = reverseFindDelim(str,delim);
	if (pos < 0)
		return subStr;
	//pos=str.Find('.');	//�õ�����0ʼλ�ã�0ʼλ����n����˵����ǰ����n���ַ�
	subStr=str.Left(pos);
	str.Delete(0,pos+1);
	// subStr <-> str
	tmpStr=subStr;
	subStr=str;
	str=tmpStr;
	return subStr;
}
//CString ת�޷������Σ������Ƿ��ַ�����
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
//CString ת���Σ������Ƿ��ַ�����
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
//�ַ������������ҷָ����һ�γ��ֵ�λ�ã����λ��Ϊ0��֮ǰ������ͬ���ĸ����ָ������������������ķָ���
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
//�ַ���������������ҷָ����һ�γ��ֵ�λ�ã����λ��Ϊ0��֮ǰ������ͬ���ĸ����ָ������������������ķָ���
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
//���ַ����ĵ�index��delim֮��ȡlen���ַ�����
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
//�����ַ���str�ĵ�index��index+1��delim֮����ַ�
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
//ע�����Ӽ�������Ӽ�ֵ
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
		//��LPCTSTR����������Ȼ��ʾע�����ӳɹ�����ʵ�����ʧ�ܣ���LPTSTR��ɽ�������⣬�������´�ע�����ܿ���
		if(res != ERROR_SUCCESS)
		{
			MessageBox(GetActiveWindow(),_T("ע��������ʧ�ܣ�"),_T("��ʾ"),MB_OK);
			keyPath.ReleaseBuffer();
			return false;
		}
		MessageBox(GetActiveWindow(),_T("ע�������ӳɹ���"),_T("��ʾ"),MB_OK);
		keyPath.ReleaseBuffer();
		RegCloseKey(hkey);
		return true;
	}
	else if (hk == HKCU)
	{
		res=RegCreateKeyEx(HKEY_CURRENT_USER,lptstr,0,NULL,REG_OPTION_NON_VOLATILE,KEY_ALL_ACCESS,NULL,&hkey,&dwDisp);
		if(res != ERROR_SUCCESS)
		{
			MessageBox(GetActiveWindow(),_T("ע��������ʧ�ܣ�"),_T("��ʾ"),MB_OK);
			keyPath.ReleaseBuffer();
			return false;
		}
		MessageBox(GetActiveWindow(),_T("ע�������ӳɹ���"),_T("��ʾ"),MB_OK);
		keyPath.ReleaseBuffer();
		RegCloseKey(hkey);
		return true;
	}
	else
		keyPath.ReleaseBuffer();
		return false;
}
//ע������ֵ
bool Cfunc::regAddValue(hk_t hk,CString path,CString name,DWORD dataType,CString value)
{
	LRESULT lr;
	HKEY hKey;
	LPTSTR	lptstr;
	LPCTSTR lpctstr;
	lptstr=path.GetBuffer(1024);
	//��ע���
	//��ڲ�����hk���ж�
	if (hk == HKLM)
	{
		lr = RegOpenKey(HKEY_LOCAL_MACHINE,lptstr, & hKey);
		path.ReleaseBuffer();
		if(lr != ERROR_SUCCESS)
		{
			MessageBox(GetActiveWindow(),_T("ע����ʧ��\nֵ���ʧ��"),_T("��ʾ"),MB_OK);
			return	false;
		}
	}
	else if (hk == HKCU)
	{
		lr = RegOpenKey(HKEY_CURRENT_USER,lptstr, & hKey);
		path.ReleaseBuffer();
		if(lr != ERROR_SUCCESS)
		{
			MessageBox(GetActiveWindow(),_T("ע����ʧ��\nֵ���ʧ��"),_T("��ʾ"),MB_OK);
			return	false;
		}
	}
	else
	{
		MessageBox(GetActiveWindow(),_T("δ֪����ڲ���(hk)\nֵ���ʧ��"),_T("��ʾ"),MB_OK);
		return false;
	}
	//��Ӽ�ֵ
	//��ڲ���(dataType)�ж�
	if(dataType == REG_DWORD)
	{
		int val;
		val=strtoi(value);
		lpctstr=name;
		lr=RegSetValueEx(hKey,lpctstr,NULL,dataType,(LPBYTE)&val,sizeof(DWORD));
		if(lr == ERROR_SUCCESS)
		{
			MessageBox(GetActiveWindow(),_T("ֵ��ӳɹ�"),_T("��ʾ"),MB_OK);
			RegCloseKey(hKey);
			return true;
		}
		else
		{
			MessageBox(GetActiveWindow(),_T("ֵ���ʧ��"),_T("��ʾ"),MB_OK);
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
			MessageBox(GetActiveWindow(),_T("ֵ��ӳɹ�"),_T("��ʾ"),MB_OK);
			RegCloseKey(hKey);	
			value.ReleaseBuffer();
			return true;
		}
		else
		{
			MessageBox(GetActiveWindow(),_T("ֵ���ʧ��"),_T("��ʾ"),MB_OK);
			RegCloseKey(hKey);	
			value.ReleaseBuffer();
			return true;
		}
	}
	else
	{
		MessageBox(GetActiveWindow(),_T("δ֪����ڲ���(dataType)\nֵ���ʧ��"),_T("��ʾ"),MB_OK);
		return false;
	}

}
//���office�汾
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
//ת��office�汾
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
	int carry;		//��
	int remainder;	//����
	CString str_rem;//����ת���ɵ��ַ���
	CString pool;	//���ݻ����
	CString result;	//���IP
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
//��ȡ��ִ���ļ��汾��Ϣ,ժ������,������4��ע�Ͳ���Ϊ�Ķ�����
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
	//�β���char *AppName��������룺1812(��Դ����û�з���)�����������ڱ������⡣
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
					TranslationPtr[0].wLanguage,TranslationPtr[0].wCodePage);	//ת�����ɹ�
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
	GetTempPath(MAX_PATH,path);	//��õ�temp·����β���з�б��
	CString strPath;
	strPath=path;
	return strPath;
}
//·����β���з�б��
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