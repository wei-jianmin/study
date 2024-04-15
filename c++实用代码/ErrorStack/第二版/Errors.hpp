/* 
* ����˵����
* Errors��ͨ����Ϊ�����ķ���ֵʹ��
* ÿ��Errors�����ܼ�¼�༶(/���)������
* ����������������б���ɸ�Ψһ�Ĵ������(uint32)
* ͬʱҲ�ܸ������������Ų�ѯ����Ӧ�Ĵ���������
* Ȼ��ͨ����ѯ"������-������Ϣת����"
* ������������ת���ɴ�����Ϣ��������
* ʹ��ע�⣺
* ����Դ�ļ��е��� INIT_ERROR_STACK �� (1��)
* �����ʹ�ñ��ļ����õ�"������-������Ϣת����"
* ���ȳ�ʼ��������ת������ʹ�����º꣺
* BEGIN_SET_ERR_MAP��SET_ERR_MAP_VALUE��END_SET_ERR_MAP
*/

#ifndef ERROR_STACK_HPP
#define ERROR_STACK_HPP
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <map>

//֧�������ռ䣬��ʹ�������ռ䣬ֻ�������һ��ע������
//#define ERROR_STACK_NAMESPACE utils
#ifdef ERROR_STACK_NAMESPACE
#define ERRORS_NAMESPACE ERROR_STACK_NAMESPACE::
namespace ERROR_STACK_NAMESPACE {
#else
#define ERRORS_NAMESPACE
#endif

//��̬��Ա��ʼ����
#define INIT_ERRORS ERRORS_NAMESPACE Errors::Robot ERRORS_NAMESPACE Errors::_robot;\
	std::map<unsigned int,void*> ERRORS_NAMESPACE Errors::_err_stack_map;

//���õ�"������-������Ϣת����"
typedef unsigned int value_type;
std::map<value_type,std::string> g_err_map;
#define BEGIN_SET_ERR_MAP  class CInitGlobalErrmap { public: CInitGlobalErrmap() {
#define SET_ERR_MAP_VALUE(K,V)  ERRORS_NAMESPACE g_err_map[K] = V;
#define END_SET_ERR_MAP  }} g_init_global_err_map;

#define MAX_CALL_LEVEL 99  /*����֧�������ټ�Ƕ��*/
class Errors
{
public:
	Errors(){}
	Errors(value_type err)
	{
		_err_stack.clear();
		_err_stack._values[0] = err;
	}
	Errors(const Errors& es)
	{
		_err_stack = es._err_stack;
	}
	~Errors(){}
	//�����ʷ��������
	void clear()
	{
		_err_stack.clear();
	}
	//���µĴ��������ӵ�����������
	Errors& pushError(value_type err)
	{
		if(_err_stack._index==0 && _err_stack._values[0]==0)
		{
			_err_stack._values[0] = err;
			return *this;
		}
		if(_err_stack._index < MAX_CALL_LEVEL-1)
			_err_stack._index++;
		_err_stack._values[_err_stack._index] = err;
		return *this;
	}
	//ʹ�ø�����໥�丳ֵ
	Errors& operator = (const Errors& es)
	{
		_err_stack = es._err_stack;
		return *this;
	}
	//ͬ pushError
	Errors& operator + (value_type err)
	{
		return pushError(err);
	}
	//ͬ pushError
	void operator += (value_type err)
	{
		pushError(err);
	}
	//ʹ�õ�ǰ��������޷����������бȽ�
	bool operator == (value_type v)
	{
		return _err_stack._values[_err_stack._index] == v;
	}
	//ʹ�õ�ǰ��(�����һ��������)�������޷����������бȽ�
	bool operator != (value_type v)
	{
		return _err_stack._values[_err_stack._index] != v;
	}
	//����������תΪ�������
	unsigned int getErrorCode()
	{
		if(_err_stack._index==0 && _err_stack._values[0]==0)
			return 0;
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
	 * ��������Ĵ��������У���ѯ"������-������Ϣת����"
	 * ������������תΪ������Ϣ��������
	 */
	std::string getErrorString(const std::map<value_type,std::string>& err_map=g_err_map,const char* seperator=":")
	{
		std::string retv = "";
		unsigned int err_code = 0;
		std::map<value_type,std::string>::const_iterator citer = err_map.begin();
		for(unsigned int index = _err_stack._index;index>0;index--)
		{
			err_code = _err_stack[index];
			citer = err_map.find(err_code);
			if(citer == err_map.end())
			{
				retv.append(seperator);
				continue;
			}
			retv.append(citer->second);
			retv.append(seperator);
		}
		err_code = _err_stack[0];
		citer = err_map.find(err_code);
		if(citer != err_map.end())
			retv.append(citer->second);
		return retv;
	}
	/*
	* ���������תΪ���������У�Ȼ����ղ��������"������-������Ϣת����"(err_map)
	* ������������תΪ������Ϣ��������
	* ����err_mapʹ���ⲿ����Ĳ��������ʹ��Ĭ�ϲ��������ȶ� g_err_map ��ʼ������ʹ�����º���ɣ�
	* BEGIN_SET_ERR_MAP��SET_ERR_MAP_VALUE��END_SET_ERR_MAP
	*/
	static std::string getErrorString(unsigned int errcode,const std::map<value_type,std::string>& err_map=g_err_map,const char* seperator=":")
	{
		if(errcode==0 || err_map.size()==0)
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
		Robot(){}
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
			clear();
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
		void clear()
		{
			_index = 0;
			memset(&_values,0,MAX_CALL_LEVEL*sizeof(value_type));
		}
		value_type _values[MAX_CALL_LEVEL];
		unsigned int _index;  //��Զָ�����һ����ֵ��λ��
	};
private:
	//��Ϊֱ�Ӹ�ֵ�����������岻��ȷ�����Խ�֮����
	Errors& operator = (value_type err){}
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