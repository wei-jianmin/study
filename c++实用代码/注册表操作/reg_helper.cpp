#include <Windows.h>
#include <algorithm>
#include "reg_helper.h"

RegHelper::RegHelper(const char* reg_path,bool auto_create/*=false*/,const char* mode/*="rwx"*/)
{
	_pk = NULL;
	error_code = 0;
	error_str = "成功";

	if(reg_path==NULL || strlen(reg_path)<6)
	{
		error_str = "打开注册表失败，参数错误";
		return;
	}
	if(reg_path[0]!='H' || reg_path[1]!='K')
	{
		error_str = "打开注册表失败，参数错误";
		return;
	}
	
	unsigned long sam = ParseRegMode(mode);

	bool b = RegOpenPath(reg_path,sam);
	if(b)
	{
		return;
	}
	if(error_code!=ERROR_FILE_NOT_FOUND && error_code!=ERROR_PATH_NOT_FOUND)
	{
		return;
	}

	if(auto_create)
	{
		std::string s0,s1;
		s0 = FormatPath(reg_path);
		int idx = s0.rfind('\\');
		if(idx>0)
		{
			s1=s0.substr(idx+1);
			s0=s0.substr(0,idx);
			bool b = RegCreateSubKey(s0.c_str(),s1.c_str(),sam);
			if(!b)
			{
				error_str = "创建注册表项失败";
				_pk = NULL;
				return;
			}
		}
		else
		{
			error_str = "注册表打开失败，路径错误";
			_pk = NULL;
			return;
		}
	}
}

RegHelper::~RegHelper()
{
	if(_pk)
	{
		RegCloseKey((HKEY)_pk);
	}
}

bool RegHelper::IsOpen()
{
	if(_pk)
		return true;
	else
		return false;
}

bool RegHelper::DeleteKey(const char* key_name)
{
	if(!_pk)
	{
		error_str = "注册表项打开失败";
		return false;
	}

	error_code = RegDeleteKeyA(  
					(HKEY)_pk, // handle to open key  
					key_name // subkey name  
					); 
	if(error_code == ERROR_SUCCESS)
		return true;
	else
	{
		error_str = "删除注册表项失败：";
		error_str += GetSysError(error_code);
		return false;
	}
}

std::string RegHelper::GetItemValue(const char* item_name,RegValueType* value_type/*=NULL*/)
{
	if(!_pk)
	{
		error_str = "注册表项打开失败";
		return "";
	}

	DWORD vtype,data_size;
	long error_code = RegQueryValueExA(  
							(HKEY)_pk, // handle to key  
							item_name, // value name  
							0, // reserved  
							&vtype, // type buffer  
							NULL, // data buffer  
							&data_size // size of data buffer  
							); 
	if(error_code == ERROR_SUCCESS)
	{
		unsigned char* pvalue = (unsigned char*)malloc(data_size);
		if(pvalue)
		{
			error_code = RegQueryValueExA(  
							(HKEY)_pk, // handle to key  
							item_name, // value name  
							0, // reserved  
							&vtype, // type buffer  
							pvalue, // data buffer  
							&data_size // size of data buffer  
							); 

			std::string strv;
			switch(vtype)
			{
			case REG_SZ:
			case REG_EXPAND_SZ:
				strv = (char*)pvalue;
				break;
			case REG_BINARY:
				strv.assign((char*)pvalue,data_size);
				break;
			case REG_DWORD:
				strv.assign(20,0);
				sprintf_s((char*)strv.c_str(),20,"%d",*(DWORD*)pvalue);
				break;
			case REG_MULTI_SZ:
				strv.assign((char*)pvalue,data_size);
				std::replace(strv.begin(),strv.end(),'\0','\n');
				break;
			case REG_QWORD:
				strv.assign(50,0);
				sprintf_s((char*)strv.c_str(),50,"%ld",*(unsigned long long*)pvalue);
				break;
			default:
				strv = "";
				error_str = "获取的注册表值为不可识别的数据类型";
			}
			free(pvalue);
			if(value_type)
			{
				*value_type = (RegValueType)vtype;
			}
			return strv;
		}
		else
		{
			error_str = "注册表值获取失败，申请内存失败";
		}
	}
	else
	{
		error_str = "获取注册表键值失败：";
		error_str += GetSysError(error_code);
	}
	return "";
}

bool RegHelper::SetItemValue(const char* item_name,RegValueType value_type,const std::string value)
{
	if(!_pk)
	{
		error_str = "注册表项打开失败";
		return false;
	}
	if( value_type==reg_undef0   || 
		value_type==reg_undef1 || 
		value_type==reg_undef2 || 
		value_type==reg_undef3
	   )
	{
		error_str = "注册表键值写入失败，不支持的数据类型";
		return false;
	}

	if(value_type==reg_none)
	{
		error_code = RegDeleteValueA(  
						(HKEY)_pk, // handle to key  
						item_name // value name  
						); 
		if(error_code == ERROR_SUCCESS)
			return true;
		else
		{
			error_str = "注册表键值写入失败：";
			error_str += GetSysError(error_code);
			return false;
		}
	}

	std::string value2;
	if(value_type==reg_dword || value_type==reg_dword_bigendian || value_type==reg_qword)
	{
		unsigned long long ll = 0;
		for(unsigned int i=0;i<value.length();i++)
		{
			char c = value[i];
			ll *= 10;
			int v = c-'0';
			if(v>9)
			{
				error_str = "注册表值写入失败，错误的value值";
				return false;
			}
			ll += (c-'0');
		}
		
		if(value_type==reg_dword)
		{
			unsigned long l = ll & 0xFFFFFFFF;
			value2.clear();
			value2.assign(4,'\0');
			value2[3] = (char)((l & 0xFF000000) >> 24);
			value2[2] = (char)((l & 0xFF0000) >> 16);
			value2[1] = (char)((l & 0xFF00) >> 8);
			value2[0] = (char)(l & 0xFF);
		}
		else if(value_type==reg_dword_bigendian)
		{
			unsigned long l = ll & 0xFFFFFFFF;
			value2.clear();
			value2.assign(4,'\0');
			value2[0] = (char)((l & 0xFF000000) >> 24);
			value2[1] = (char)((l & 0xFF0000) >> 16);
			value2[2] = (char)((l & 0xFF00) >> 8);
			value2[3] = (char)(l & 0xFF);
		}
		else
		{
			value2.clear();
			value2.assign(8,'\0');
			value2[7] = (char)((ll & 0xFF00000000000000) >> 56);
			value2[6] = (char)((ll & 0xFF000000000000) >> 48);
			value2[5] = (char)((ll & 0xFF0000000000) >> 40);
			value2[4] = (char)((ll & 0xFF00000000) >> 32);
			value2[3] = (char)((ll & 0xFF000000) >> 24);
			value2[2] = (char)((ll & 0xFF0000) >> 16);
			value2[1] = (char)((ll & 0xFF00) >> 8);
			value2[0] = (char)(ll & 0xFF);
		}
	}
	else if(value_type == reg_multi_sz)
	{
		value2 = value;
		replace(value2.begin(),value2.end(),'\n','\0');
	}
	else
		value2 = value;

	error_code = RegSetValueExA(  
					(HKEY)_pk, // handle to key  
					item_name, // value name  
					0, // reserved  
					value_type, // value type  
					(const unsigned char*)value2.c_str(), // value data  
					value2.length() // size of value data  
					); 

	if(error_code == ERROR_SUCCESS)
		return true;
	else
	{
		error_str = "注册表键值写入失败：";
		error_str += GetSysError(error_code);
		return false;
	}
}

std::list<std::string> RegHelper::EnumKey()
{
	std::list<std::string> lst;
	if(!_pk)
	{
		error_str = "注册表项打开失败";
		return lst;
	}

	DWORD index = 0;
	DWORD size=256;
	do
	{
		std::string s(size,'\0');
		error_code = RegEnumKeyExA(  
						(HKEY)_pk, // handle to key to enumerate  
						index, // subkey index  
						(char*)s.c_str(), // subkey name  
						&size, // size of subkey buffer  
						NULL, // reserved  
						NULL, // class string buffer  
						NULL, // size of class string buffer  
						NULL // last write time  
						); 
		if(error_code==ERROR_SUCCESS)
		{
			lst.push_back(s);
			index++;
			size=256;
			continue;
		}
		else if(error_code==ERROR_MORE_DATA)
		{
			size+=256;
			continue;
		}
		else if(error_code==ERROR_NO_MORE_ITEMS)
		{
			error_str="枚举注册表子项完成";
			break;
		}
		else
		{
			error_str = "枚举注册表项失败：";
			error_str += GetSysError(error_code);
			break;
		}
	}while(true);
	
	return lst;
}

std::list<std::string> RegHelper::EnumItem()
{
	std::list<std::string> lst;
	if(!_pk)
	{
		error_str = "注册表项打开失败";
		return lst;
	}
	
	DWORD index = 0;
	do 
	{
		char name[256]={0};
		DWORD name_size=256;
		error_code = RegEnumValueA(  
						(HKEY)_pk, // handle to key to query  
						index, // index of value to query  
						name, // value buffer  
						&name_size, // size of value buffer  
						NULL, // reserved  
						NULL, // type buffer  
						NULL, // data buffer  
						NULL // size of data buffer  
						);
		if(error_code==ERROR_SUCCESS)
		{
			lst.push_back(name);
			index++;
			continue;
		}
		else if(error_code==ERROR_NO_MORE_ITEMS)
		{
			error_str="枚举注册表项键值完成";
			break;
		}
		else
		{
			error_str = "枚举注册表键值失败：";
			error_str += GetSysError(error_code);
			break;
		}
	} while (true);
	return lst;
}

std::string RegHelper::GetErrorString()
{
	return error_str;
}

unsigned long RegHelper::ParseRegMode(const char* mode)
{
	unsigned long sam = 0;
	int imode = 0;
	std::string s = mode;
	s = mode;
	if(s.find('r')!=-1)
	{
		sam |= KEY_READ;
		imode += 4;
	}
	if(s.find('w')!=-1)
	{
		sam |= KEY_WRITE;
		imode += 2;
	}
	if(s.find('x')!=-1)
	{
		sam |= KEY_EXECUTE;
		imode += 1;
	}
	if(imode == 7)
	{
		sam = KEY_ALL_ACCESS;
	}
	return sam;
}

bool RegHelper::RegOpenPath(const char* reg_path,unsigned long sam)
{
	HKEY hk = NULL;
	int path_idx = -1;
	std::string s = reg_path;
	if(s.find("HKLM\\") == 0)
	{
		hk = HKEY_LOCAL_MACHINE;
		path_idx = 5;
	}
	else if(s.find("HKCU\\") == 0)
	{
		hk = HKEY_CURRENT_USER;
		path_idx = 5;
	}
	else if(s.find("HKCR\\") == 0)
	{
		hk = HKEY_CLASSES_ROOT;
		path_idx = 5;
	}
	else if(s.find("HKU\\") == 0)
	{
		hk = HKEY_USERS;
		path_idx = 4;
	}
	else if(s.find("HKEY_LOCAL_MACHINE\\") == 0)
	{
		hk = HKEY_LOCAL_MACHINE;
		path_idx = 19;
	}
	else if(s.find("HKEY_CURRENT_USER\\") == 0)
	{
		hk = HKEY_CURRENT_USER;
		path_idx = 18;
	}
	else if(s.find("HKEY_CLASSES_ROOT\\") == 0)
	{
		hk = HKEY_CLASSES_ROOT;
		path_idx = 18;
	}
	else if(s.find("HKEY_USERS\\") == 0)
	{
		hk = HKEY_USERS;
		path_idx = 11;
	}
	if(hk == NULL)
	{
		error_str = "打开注册表失败，路径错误";
		return false;
	}

	s = s.substr(path_idx);
	error_code = RegOpenKeyExA(  
		hk, // handle to open key  
		s.c_str(), // subkey name  
		0, // reserved  
		sam, // security access mask  
		(PHKEY)&_pk// handle to open key  
		);
	if(error_code == ERROR_SUCCESS)
	{
		return true;
	}
	else
	{
		error_str = "打开注册表项失败：";
		error_str += GetSysError(error_code);
		return false;
	}
}

bool RegHelper::RegCreateSubKey(const char* reg_path,const char* key_name,unsigned long sam)
{
	do 
	{
		if(!RegOpenPath(reg_path,sam))
		{
			std::string s0,s1;
			s0 = reg_path;
			int idx = s0.rfind('\\');
			if(idx>0)
			{
				s1=s0.substr(idx+1);
				s0=s0.substr(0,idx);
				if(false == RegCreateSubKey(s0.c_str(),s1.c_str(),sam))
				{
					break;
				}
			}
			else
			{
				error_str = "打开注册表失败，路径错误";
				return false;
			}
		}
		
		if(key_name && strlen(key_name)>0)
		{
			DWORD disp;
			LONG l = RegCreateKeyExA(  
				(HKEY)_pk, // handle to open key  
				key_name, // subkey name  
				0, // reserved  
				"", // class string  
				REG_OPTION_NON_VOLATILE, // special options  
				sam, // desired security access  
				NULL, // inheritance  
				(PHKEY)&_pk, // key handle  
				&disp // disposition value buffer  
				); 
			if(l == ERROR_SUCCESS)
			{
				return true;
			}
			else
			{
				GetSysError(l);
				return false;
			}
		}
	} while (false);

	return false;
}

void RegHelper::FormatPath(std::string &str)
{
	std::replace(str.begin(),str.end(),'/','\\');
}

std::string RegHelper::FormatPath(const char* p)
{
	std::string str = p;
	FormatPath(str);
	return str;
}

std::string RegHelper::GetSysError(unsigned long e)
{
	char* buffer;
	::FormatMessageA(
		FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM,
		NULL,e,0,( LPSTR )&buffer,0,NULL );
	std::string s = buffer;
	LocalFree( buffer ); 
	return s;
}

