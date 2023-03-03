typedef int hk_t;
#define HKLM 1
#define HKCU 2
#define HKU  3
#define HKCR 4
#define HKCC 5
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
LRESULT GetValue2(HKEY hKey, LPCTSTR name, LPDWORD value);
void checkEnumKey(LPCTSTR szKey , HKEY hParent , LPCTSTR keyWords ,CListBox &list);
int strtoi(CString str);


