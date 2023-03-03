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
#pragma region 获得系统信息
	//获得系统名
	void GetSysName(CString &osname);
	//安全获得本地系统信息
	VOID SafeGetNativeSystemInfo (__out LPSYSTEM_INFO lpSystemInfo);
	//获取系统位数
	int GetSystemBits();
	//获取系统版本
	void GetVersionMark(CString &vmark);
#pragma endregion 

#pragma region 获得软件信息
	//获取软件信息
	CString GetSoftwareInfo(LPCTSTR softwareName);
	//检查软件版本
	int checkSoftwareVersion(LPCTSTR szKey , HKEY hParent , LPCTSTR softwareName ,CString & ver);
	//获取可执行文件相关信息,需 #pragma  comment(lib,"Version.lib");
	CString getExeInfo(CString AppName);
#pragma endregion

#pragma region 获得路径信息
	CString getTempPath();
	CString getModulePath();
#pragma endregion

#pragma region 注册表操作
	//获得指定键下值项的数据
	bool regGetItemValue(hk_t hkType, LPCTSTR keyAddr, LPCTSTR keyValue, CString &res);
	//获得指定键下值项的数据
	bool regGetItemValue(hk_t hkType, LPCTSTR keyAddr, LPCTSTR keyValue, int &res);
	//搜索指定键下的所有子键，并把符合keyWord的子键其下的值放入列表框变量中
	void getKeyWords(CListBox &list,LPCTSTR keyPath,LPCTSTR keyWords);
	//根据给定键的路径，获取其下值项的数据内容
	bool getRegItemValue(hk_t hk,CString sKeyPath,CString sItemName,LPTSTR value, LPDWORD size);
	//注册表添加键
	bool regAddKey(hk_t hk,CString path,CString key);
	//注册表添加值项
	bool regAddValue(hk_t hk,CString path,CString name,DWORD dataType,CString value);
	//获取值项的数据内容
	LRESULT GetValue(HKEY hKey, LPCTSTR name, LPTSTR value, LPLONG size);
	//获取值项的数据内容
	LRESULT GetValue2(HKEY hKey, LPCTSTR name, LPDWORD value);
#pragma endregion

#pragma region 字符串操作
	//字符串型转整形（如"246"->246）
	int strtoi(CString str);
	//字符串型转无符号整形（如"246"->246）
	UINT strtoui(CString str);
	//根据分隔符从左边分割字符串,前者做返回值
	CString separate(CString & str,char delim);
	//根据分隔符从右边分割字符串,后者做返回值
	CString separate2(CString & str,char delim);
	//查找分隔符位置
	int findDelim(CString str,char delim);
	//反向查找分隔符位置
	int reverseFindDelim(CString str,char delim);
	//从字符串的第index个delim之后取len个字符返回
	CString getStrAfterDelim(CString str,TCHAR delim,int index,int len);
	//返回字符串str的第index到index+1个delim之间的字符,如果index超过str中delim个数，则返回最后一个字段
	CString getStrAfterDelim(CString str,TCHAR delim,int index);
#pragma endregion

#pragma region Office操作
	//获取office版本
	bool getOfficeVersion(CString &ver);
	//office版本转换（内部版本与外部版本之间切换）
	bool OfficeVersionConvert(CString &ver);
#pragma endregion

#pragma region IE操作
	//ip合法性检查
	bool isLegal(CString ip);
	//获取IE位数
	int  myGetIEBits();
	//获取安全站点
	void getSafeStations(CListBox &list);
#pragma endregion

#pragma region 获取时间信息
	CString getDateTime2(void);
	CString getDateTime(void);
	CString getDateTime1(void);
#pragma endregion

#pragma region 配置文件操作

#pragma endregion
protected:
	void enumKey2(CListBox &list,HKEY hKey2,CString station);
	void enumKey1(CListBox &list,HKEY hKey);
	void checkEnumKey(LPCTSTR szKey , HKEY hParent , LPCTSTR keyWords ,CListBox &list);
	//添加信任站点
	bool addIP(CString ip);
	bool isDomain(CString ip);
	//是合法的ip，对ip值格式化为标准ip，如ip=260 -> ip=255.5
	bool ipFormat(CString &ip);
public:
	
};
#endif _CFUNC_H_
