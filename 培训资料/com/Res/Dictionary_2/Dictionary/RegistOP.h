typedef int hk_t;
#define HKLM 1
#define HKCU 2
#define HKU  3
#define HKCR 4
#define HKCC 5
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
LRESULT GetValue2(HKEY hKey, LPCTSTR name, LPDWORD value);
void checkEnumKey(LPCTSTR szKey , HKEY hParent , LPCTSTR keyWords ,CListBox &list);
int strtoi(CString str);


