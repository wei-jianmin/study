/*
 * ���ļ���ͬͷ�ļ�����MFC/dll�������棬����theApp���������������Ա��
   unsigned long err;
   CString strRet;
   CString strErrMsg;
 * �������еĺ���������ע���У��漰�������ע����ע��������ֵ
 * ע�����ָ����ע���༭�������ġ��ļ��С�����
 * ע����ָ����ע���༭�����Ҳ�ġ��ļ�������
 * ע���(��)ֵָ����ע���༭�������Ҳࡰ�ļ�������������
 */
#include "StdAfx.h"
#include "regist_op.h"
#include "dffs.h"				//CdffsApp���ͷ�ļ�
//#include <vld.h>
/*Error codes are 32-bit values (bit 31 is the most significant bit).Bit 29 is reserved 
  for application-defined error codes; no system error code has this bit set.If you are
  defining an error code for your application, set this bit to one. That indicates that 
  the error code has been defined by an application, and ensures that your error code 
  does not conflict with any error codes defined by the system. */
#define USER_ERROR				0X40000000
#define ERROR_OK				0
#define ERROR_PARAMS			USER_ERROR+1	//��������
#define ERROR_PARAMS_NULL		USER_ERROR+2	//��������:����Ϊ��
#define ERROR_PARAMS_KEYTYPE	USER_ERROR+3	//��������:
#define ERROR_VALUETYPE			USER_ERROR+4	//��֧�ֵļ�ֵ����

extern 
/*
 * ������ֻ֧�ֶ�DWORD���ͻ��ַ������ͼ�ֵ�Ķ�ȡ
 * ����ע�����ԭ����ֵ��ʲô���ͣ�������ת��Ϊ�ַ������ͽ��з���
 * ���ص��ַ���ĩβ����������ӻ��з�
 * �����ĵ�������������ڴ��ͷ�����
 * �����������ֵΪ�գ���ͨ��getLastErrorMsg��getLastError��ѯ����ԭ��
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
	if (lr != ERROR_SUCCESS)		//��ע���ʧ��
	{
		theApp.err=lr;
		return NULL;
	}
	//��ע���ɹ�
	DWORD dwType=REG_NONE;
    DWORD dwCount=0;
	lr = RegQueryValueEx(hKey, (LPCTSTR)strKeyName, NULL, &dwType,NULL, &dwCount);
	if (lr != ERROR_SUCCESS)		//��ѯע���ʧ��
	{
		RegCloseKey(hKey);
		theApp.err=lr;
		return NULL;
	}
	if(dwType==REG_DWORD_LITTLE_ENDIAN || dwType==REG_DWORD_BIG_ENDIAN)
	{
		DWORD buf;
		lr = RegQueryValueEx(hKey, (LPCTSTR)strKeyName, NULL, &dwType,(LPBYTE)&buf, &dwCount);
		if (lr != ERROR_SUCCESS)		//��ѯע���ʧ��
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
		if (lr != ERROR_SUCCESS)		//��ѯע���ʧ��
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
 * KeyAddr����һ������Ϊ��
 * ���KeyNameΪ�գ����ٹ�KeyValue��ֻ����KeyAddr��ע�������в���
   ���delΪ��0��˵������ɾ��ע��������������������ע����������Ĭ�ϣ�
 * ���KeyName��Ϊ�գ���˵���ǶԼ����в���
   ���KeyValueΪ�գ��򽫼�ֵ��Ϊ���ַ���
   ���delΪ��0��˵������ɾ������������������޸�/���ע����ֵ������Ĭ�ϣ�
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

	if((KeyName==NULL || strlen(KeyName)==0) && del==0)	//������
	{
		DWORD dwCreate;	//�������Ƿ��Ѿ�����
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
	else if((KeyName==NULL || strlen(KeyName)==0) && del!=0)	//ɾ����
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
		if (lr != ERROR_SUCCESS)		//��ע���ʧ��
		{
			theApp.err=lr;
			return lr;
		}
		lr=RegDeleteKey(hKey,(LPCTSTR)delName);
		RegCloseKey(hKey);
		theApp.err=lr;
		return lr;
	}
	else if((KeyName!=NULL && strlen(KeyName)> 0) && del==0)	//�޸ġ�������
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
		if (lr != ERROR_SUCCESS)		//��ע���ʧ��
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
		if(strcmp(pch,KeyValue)==0)	//˵�����õ�ֵΪ����
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
	else	//ɾ����
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
		if (lr != ERROR_SUCCESS)		//��ע���ʧ��
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
	if(err)			//˵���ǳ������
	{
		switch(theApp.err)
		{

		case ERROR_OK:
			theApp.strErrMsg="(�������)����ִ�гɹ���\n";
			break;
		case ERROR_PARAMS:
			theApp.strErrMsg="(�������)��������\n";
			break;
		case ERROR_PARAMS_NULL:
			theApp.strErrMsg="(�������)�������󣺺�������Ϊ�ա�\n";
			break;
		case ERROR_PARAMS_KEYTYPE:
			theApp.strErrMsg="(�������)�������󣺲�����ʽ����\n";
			break;
		case ERROR_VALUETYPE:
			theApp.strErrMsg="(�������)��֧�ֵļ�ֵ���͡�\n";
			break;
		default:
			theApp.strErrMsg="(�������)δ֪����\n";
			break;
		}
	}
	else
	{
		TCHAR* lpMsgBuf;
		FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER|FORMAT_MESSAGE_FROM_SYSTEM,NULL,theApp.err,0,(LPTSTR)&lpMsgBuf,0,NULL);

		theApp.strErrMsg="(ϵͳ��������)";
		theApp.strErrMsg+=lpMsgBuf;
		if(lpMsgBuf!=NULL)
		{
			LocalFree(lpMsgBuf);
			lpMsgBuf=NULL;
		}	
	}
	return (LPCTSTR)theApp.strErrMsg;
}

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
*/