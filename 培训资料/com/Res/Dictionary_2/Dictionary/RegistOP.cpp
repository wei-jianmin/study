#include "RegistOP.h"
#include <Windows.h>
#include <WinReg.h>
//���ָ������ֵ�������
bool regGetItemValue(hk_t hkType, LPCTSTR keyAddr, LPCTSTR keyValue,CString &res)
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

//����ָ�����µ������Ӽ������ѷ���keyWord���Ӽ����µ�ֵ�����б�������
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
bool regAddValue(hk_t hk,CString path,CString name,DWORD dataType,CString value)
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

//����name��ȡע������ֵ�����Ϣ��ֵ��������value�У����ﲻ����ֵ������Ϣ
LRESULT GetValue(HKEY hKey, LPCTSTR name, LPTSTR value, LPLONG size)
{
	return ::RegQueryValueEx(hKey, name, NULL, NULL, (LPBYTE)value, (LPDWORD)size);
}
//����name��ȡע�����µ�ֵ��Ҫ��ֵ����ΪDWORD�ͣ���������value��
//ע�⣺��ʵ��������ǲ���Ҫ�ģ�֮ǰ��Ϊ��ʶ�ϵĴ����������������
//�����ĵ�����������������ȡ����ָ�����ֵ�ֵ������ͣ�������������������������������Ϊ���ṩ����ֵ
LRESULT GetValue2(HKEY hKey, LPCTSTR name, LPDWORD value)
{
	DWORD dwType = REG_DWORD;
	DWORD size=sizeof(DWORD);
	return ::RegQueryValueEx(hKey, name, NULL, &dwType, (LPBYTE)value, &size);
}
//��getKeyWords��������
void checkEnumKey(LPCTSTR szKey , HKEY hParent , LPCTSTR keyWords ,CListBox &list)
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

//CString ת���Σ������Ƿ��ַ�����
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
