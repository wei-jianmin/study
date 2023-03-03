/* 
* ����˵����
* ErrorStack��ͨ����Ϊ�����ķ���ֵʹ��
* ÿ��ErrorStack�����ܼ�¼�༶(/���)������
* ����������������б���ɸ�Ψһ�Ĵ������(uint32)
* ͬʱҲ�ܸ������������Ų�ѯ����Ӧ�Ĵ���������
* Ȼ��ͨ����ѯ"������-������Ϣת����"
* ������������ת���ɴ�����Ϣ��������
* ʹ��ע�⣺
* ����Դ�ļ��е��� INIT_ERROR_STACK �� (1��)
* �����ʹ�ñ��ļ����õ�"������-������Ϣת����"
* ������������ init_global_err_map ����
*/

#ifndef ERROR_STACK_HPP
#define ERROR_STACK_HPP
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <map>

//#define ERROR_STACK_NAMESPACE utils
#ifdef ERROR_STACK_NAMESPACE  /*ʹ�������ռ�*/
namespace ERROR_STACK_NAMESPACE 
{
#endif

//��̬��Ա��ʼ����
#define INIT_ERROR_STACK ErrorStack::Robot ErrorStack::_robot;\
	  std::map<unsigned int,void*> ErrorStack::_err_stack_map;
	

//���õ�"������-������Ϣת����"
typedef unsigned int value_type;
std::map<value_type,std::string> g_err_map;
void init_global_err_map()
{
	//g_err_map[ERR1] = "error discription 1";
	//g_err_map[ERR2] = "error discription 2";
}

#define MAX_CALL_LEVEL 99  /*����֧�������ټ�Ƕ��*/
#define ERR_CODE_BASE 100  /*�����ش�����������Сֵ*/

class ErrorStack
{
public:
	ErrorStack(){}
	ErrorStack(value_type err)
	{
		_err_stack._index = 0;
		_err_stack._values[_err_stack._index] = err;
	}
	ErrorStack(const ErrorStack& es)
	{
		_err_stack = es._err_stack;
	}
	~ErrorStack(){}
	//���µĴ��������ӵ�����������
	ErrorStack& pushError(value_type err)
	{
		if(_err_stack._index < MAX_CALL_LEVEL-1)
			_err_stack._index++;
		_err_stack._values[_err_stack._index] = err;
		return *this;
	}
	//ʹ�ø���ɸ�ֵΪ�޷����������൱�ڳ�ʼ��
	ErrorStack& operator = (value_type err)
	{
		_err_stack._index = 0;
		memset(&_err_stack._values,0,MAX_CALL_LEVEL*sizeof(value_type));
		_err_stack._values[_err_stack._index] = err;
	}
	//ʹ�õ�ǰ��������޷����������бȽ�
	bool operator == (value_type v)
	{
		return _err_stack._values[_err_stack._index] == v;
	}
	//ʹ�õ�ǰ��������޷����������бȽ�
	bool operator != (value_type v)
	{
		return _err_stack._values[_err_stack._index] != v;
	}
	//����������תΪ�������
	unsigned int getErrorCode()
	{
		unsigned int err_code = crc32(_err_stack);
		if(_err_stack_map.find(err_code) == _err_stack_map.end())
			_err_stack_map[err_code] = new InnerErrorStack(_err_stack);
		return err_code;
	}
	/*
	* ��ȡ��ʷ����Ĵ������
	* index ȡֵ��0Ϊ��ǰ��1Ϊ�ϴΣ�2Ϊ���ϴΣ��Դ�����
	*/
	value_type getHistoryError(unsigned int index=0)
	{
		if(index > _err_stack._index)
			return 0;
		index = _err_stack._index - index;
		return _err_stack._values[_err_stack._index];
	}
	/*
	* ���������תΪ���������У�Ȼ���ѯ���õ�"������-������Ϣת����"
	* ������������תΪ������Ϣ��������
	* Ҫ���ô˺����������������Ʊ��ļ��е� init_global_err_map ����
	*/
	static std::string getErrorString(unsigned int errcode,const char* seperator=":")
	{
		if(g_err_map.size() == 0)
			return "";
		std::map<unsigned int,void*>::iterator perr = _err_stack_map.find(errcode);
		if(perr == _err_stack_map.end())
			return "";
		InnerErrorStack * perr_stack = reinterpret_cast<InnerErrorStack *>(perr->second);
		if(perr_stack == NULL)
			return "";
		std::string retv = "";
		value_type err_code = 0;
		std::map<value_type,std::string>::const_iterator citer = g_err_map.begin();
		for(unsigned int index = perr_stack->_index;index>0;index--)
		{
			err_code = (*perr_stack)[index];
			citer = g_err_map.find(err_code);
			if(citer == g_err_map.end())
			{
				retv.append(seperator);
				continue;
			}
			retv.append(citer->second);
			retv.append(seperator);
		}
		err_code = (*perr_stack)[0];
		citer = g_err_map.find(err_code);
		if(citer != g_err_map.end())
			retv.append(citer->second);
		return retv;
	}
	/*
	* ���������תΪ���������У�Ȼ���ѯ�ⲿ��"������-������Ϣת����"
	* ������������תΪ������Ϣ��������
	*/
	static std::string getErrorString(const std::map<value_type,std::string>& err_map,unsigned int errcode,const char* seperator=":")
	{
		if(err_map.size() == 0)
			return "";
		std::map<unsigned int,void*>::iterator perr = _err_stack_map.find(errcode);
		if(perr == _err_stack_map.end())
			return "";
		InnerErrorStack * perr_stack = reinterpret_cast<InnerErrorStack *>(perr->second);
		if(perr_stack == NULL)
			return "";
		std::string retv = "";
		value_type err_code = 0;
		std::map<value_type,std::string>::const_iterator citer = err_map.begin();
		for(unsigned int index = perr_stack->_index;index>0;index--)
		{
			err_code = (*perr_stack)[index];
			citer = err_map.find(err_code);
			if(citer == err_map.end())
			{
				retv.append(seperator);
				continue;
			}
			retv.append(citer->second);
			retv.append(seperator);
		}
		err_code = (*perr_stack)[0];
		citer = err_map.find(err_code);
		if(citer != err_map.end())
			retv.append(citer->second);
		return retv;
	}
public:
	class Robot /*������*/
	{
	public:
		Robot()
		{
			init_global_err_map();
		}
		~Robot()
		{
			if(_err_stack_map.size() > 0)
			{
				for (std::map<unsigned int,void*>::iterator iter = _err_stack_map.begin();
					iter != _err_stack_map.end(); iter++)
				{
					if(iter->second)
					{
						InnerErrorStack * pes = reinterpret_cast<InnerErrorStack*>(iter->second);
						if(pes)
							delete pes;
						else
							delete iter->second;
					}
				}
				_err_stack_map.clear();
			}
		}
	};
private:
	struct InnerErrorStack /*������*/
	{
		InnerErrorStack()
		{
			_index = 0;
			memset(&_values,0,MAX_CALL_LEVEL*sizeof(value_type));
		}
		InnerErrorStack(const InnerErrorStack& v)
		{
			_index = v._index;
			memcpy(&_values,&v,MAX_CALL_LEVEL*sizeof(value_type));
		}
		~InnerErrorStack()
		{
		}
		void operator = (const InnerErrorStack& v)
		{
			_index = v._index;
			memcpy(&_values,&v,MAX_CALL_LEVEL*sizeof(value_type));
		}
		value_type operator [] (unsigned int index)
		{
			if(index<0 || index>=MAX_CALL_LEVEL)
				return 0;
			return _values[index];
		}
		value_type _values[MAX_CALL_LEVEL];
		unsigned int _index;  //��Զָ�����һ����ֵ��λ��
	};
private:
	//������������תΪ������ŵĺ���
	unsigned int crc32(const InnerErrorStack& es)
	{
		return crc32((unsigned char*)es._values,(es._index+1)*sizeof(value_type));
	}
	//������������תΪ������ŵĺ���
	unsigned int crc32(unsigned char *buf, int len)
	{
		int i, j;
		unsigned int crc, mask;
		crc = 0xFFFFFFFF;
		for (i = 0; i < len; i++) {
			crc = crc ^ (unsigned int)buf[i];
			for (j = 7; j >= 0; j--) {    // Do eight times.
				mask = -(crc & 1);
				crc = (crc >> 1) ^ (0xEDB88320 & mask);
			}
		}
		return ~crc;
	}
private:
	static Robot _robot;  //��������
	InnerErrorStack _err_stack;  //��ǰ����Ĵ���������
	static std::map<unsigned int,void*> _err_stack_map;  //"�������-��������"��ϵ��
};

#ifdef ERROR_STACK_NAMESPACE
}
#endif

#endif //ͷ�ļ�����