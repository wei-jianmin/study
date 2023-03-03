#ifndef _CFUNC_H_
#define _CFUNC_H_
#pragma  comment(lib,"Version.lib")
//#pragma  comment(lib,"Coredll.lib");
#include"stdafx.h"
#include <WinBase.h>
#define UNISTALL "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
#define DOMAINS  "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\ZoneMap\\Domains"
#define RANGES   "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\ZoneMap\\Ranges"
#define IEVER "software\\Microsoft\\Internet Explorer"
#define ZONES0 "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Zones\\0"
#define ZONES1 "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Zones\\1"
#define ZONES2 "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Zones\\2"
#define ZONES3 "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Zones\\3"
#define ZONES4 "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Zones\\4"
#define HKLM 1
#define HKCU 2
#define HKU  3
#define HKCR 4
#define HKCC 5
#define COLOR1 RGB(222,222,222)
#define COLOR2 RGB(217,230,232)
typedef int hk_t;
class Cfunc

{
public:
	Cfunc();
	~Cfunc();
#pragma region ���ϵͳ��Ϣ
	//���ϵͳ��
	void GetSysName(CString &osname);
	//��ȫ��ñ���ϵͳ��Ϣ
	VOID SafeGetNativeSystemInfo (__out LPSYSTEM_INFO lpSystemInfo);
	//��ȡϵͳλ��
	int GetSystemBits();
	//��ȡϵͳ�汾
	void GetVersionMark(CString &vmark);
#pragma endregion 

#pragma region ��������Ϣ
	//��ȡ�����Ϣ
	CString GetSoftwareInfo(LPCTSTR softwareName);
	//�������汾
	int checkSoftwareVersion(LPCTSTR szKey , HKEY hParent , LPCTSTR softwareName ,CString & ver);
	//��ȡ��ִ���ļ������Ϣ,�� #pragma  comment(lib,"Version.lib");
	CString getExeInfo(CString AppName);
#pragma endregion

#pragma region ���·����Ϣ
	CString getTempPath();
	CString getModulePath();
#pragma endregion

#pragma region ע������
	//���ָ������ֵ�������
	bool regGetItemValue(hk_t hkType, LPCTSTR keyAddr, LPCTSTR keyValue, CString &res);
	//���ָ������ֵ�������
	bool regGetItemValue(hk_t hkType, LPCTSTR keyAddr, LPCTSTR keyValue, int &res);
	//����ָ�����µ������Ӽ������ѷ���keyWord���Ӽ����µ�ֵ�����б�������
	void getKeyWords(CListBox &list,LPCTSTR keyPath,LPCTSTR keyWords);
	//���ݸ�������·������ȡ����ֵ�����������
	bool getRegItemValue(hk_t hk,CString sKeyPath,CString sItemName,LPTSTR value, LPDWORD size);
	//ע�����Ӽ�
	bool regAddKey(hk_t hk,CString path,CString key);
	//ע������ֵ��
	bool regAddValue(hk_t hk,CString path,CString name,DWORD dataType,CString value);
	//��ȡֵ�����������
	LRESULT GetValue(HKEY hKey, LPCTSTR name, LPTSTR value, LPLONG size);
	//��ȡֵ�����������
	LRESULT GetValue2(HKEY hKey, LPCTSTR name, LPDWORD value);
#pragma endregion

#pragma region �ַ�������
	//�ַ�����ת���Σ���"246"->246��
	int strtoi(CString str);
	//�ַ�����ת�޷������Σ���"246"->246��
	UINT strtoui(CString str);
	//���ݷָ�������߷ָ��ַ���,ǰ��������ֵ
	CString separate(CString & str,char delim);
	//���ݷָ������ұ߷ָ��ַ���,����������ֵ
	CString separate2(CString & str,char delim);
	//���ҷָ���λ��
	int findDelim(CString str,char delim);
	//������ҷָ���λ��
	int reverseFindDelim(CString str,char delim);
	//���ַ����ĵ�index��delim֮��ȡlen���ַ�����
	CString getStrAfterDelim(CString str,TCHAR delim,int index,int len);
	//�����ַ���str�ĵ�index��index+1��delim֮����ַ�,���index����str��delim�������򷵻����һ���ֶ�
	CString getStrAfterDelim(CString str,TCHAR delim,int index);
#pragma endregion

#pragma region Office����
	//��ȡoffice�汾
	bool getOfficeVersion(CString &ver);
	//office�汾ת�����ڲ��汾���ⲿ�汾֮���л���
	bool OfficeVersionConvert(CString &ver);
#pragma endregion

#pragma region IE����
	//ip�Ϸ��Լ��
	bool isLegal(CString ip);
	//��ȡIEλ��
	int  myGetIEBits();
	//��ȡ��ȫվ��
	void getSafeStations(CListBox &list);
#pragma endregion

#pragma region ��ȡʱ����Ϣ
	CString getDateTime2(void);
	CString getDateTime(void);
	CString getDateTime1(void);
#pragma endregion

#pragma region �����ļ�����

#pragma endregion
protected:
	void enumKey2(CListBox &list,HKEY hKey2,CString station);
	void enumKey1(CListBox &list,HKEY hKey);
	void checkEnumKey(LPCTSTR szKey , HKEY hParent , LPCTSTR keyWords ,CListBox &list);
	//�������վ��
	bool addIP(CString ip);
	bool isDomain(CString ip);
	//�ǺϷ���ip����ipֵ��ʽ��Ϊ��׼ip����ip=260 -> ip=255.5
	bool ipFormat(CString &ip);
public:
	
};
#endif _CFUNC_H_
