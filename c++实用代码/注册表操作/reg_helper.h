#ifndef REG_HELPER_H
#define REG_HELPER_H

#include <string>
#include <list>
#ifndef NULL 
#define NULL 0
#endif

class RegHelper
{
public:
	enum RegValueType{  reg_none=0,reg_sz,reg_expand_sz,reg_binary,reg_dword,
						reg_dword_bigendian,reg_undef0,reg_multi_sz,
						reg_undef1,reg_undef2,reg_undef3,reg_qword         };

	RegHelper(const char* reg_path,bool auto_create=false,const char* mode="rwx");
	~RegHelper();
	bool IsOpen();
	bool DeleteKey(const char* key_name);
	std::string GetItemValue(const char* item_name,RegValueType* value_type=NULL);
	/*
	 * ��д����������Ϊ reg_dword��reg_dword_bigendian �� reg_qword��
	 * �뽫10�����������ַ�����ʽ��ֵ������ value .
	 * ��д����������Ϊ reg_mulstring ʱ��ÿ���ַ�����\n�ָ� .
	 * ��д����������Ϊ reg_none ʱ����ɾ���ü�ֵ
	 */
	bool SetItemValue(const char* item_name,RegValueType value_type,const std::string value);
	std::list<std::string> EnumKey();
	std::list<std::string> EnumItem();
	std::string GetErrorString();
private:
	bool RegCreateSubKey(const char* reg_path,const char* key_name,unsigned long sam);
	bool RegOpenPath(const char* reg_path,unsigned long sam);
	void FormatPath(std::string &str);
	unsigned long ParseRegMode(const char* mode);
	std::string FormatPath(const char* p);
	std::string GetSysError(unsigned long e);
private:
	struct { int unused; } * _pk; 
	long error_code;
	std::string error_str;
};

#endif //REG_HELPER_H