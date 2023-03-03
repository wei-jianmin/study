#ifndef ERROR_STACK_HPP
#define ERROR_STACK_HPP
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <map>

#include <Windows.h>
#define log(S) OutputDebugStringA(S);OutputDebugStringA("\n")

//#define ERROR_STACK_NAMESPACE utils
#ifdef ERROR_STACK_NAMESPACE
namespace ERROR_STACK_NAMESPACE 
{
#endif

typedef unsigned int value_type;
std::map<value_type,std::string> g_err_map;
void init_global_err_map()
{
	//g_err_map[ERR] = "error discription";
}

#define INIT_ERROR_STACK \
	std::map<unsigned int,void*> ErrorStack::_err_stack_map;\
	ErrorStack::Robot ErrorStack::_robot;\
	unsigned int ErrorStack::_err_code = ERR_CODE_BASE;

#define MAX_CALL_LEVEL 99  /*定义支持最多多少级嵌套*/
#define ERR_CODE_BASE 100  /*所返回错误索引的最小值*/

class ErrorStack
{
public:
	ErrorStack(){}
	ErrorStack(value_type err)
	{
		_err_stack._index = 0;
		_err_stack.values[_err_stack._index] = err;
	}
	ErrorStack(const ErrorStack& es)
	{
		_err_stack = es._err_stack;
	}
	ErrorStack& pushError(value_type err)
	{
		if(_err_stack._index < MAX_CALL_LEVEL-1)
			_err_stack._index++;
		_err_stack.values[_err_stack._index] = err;
		return *this;
	}
	~ErrorStack()
	{
		log("free ErrorStack");
	}
	ErrorStack& operator = (value_type err)
	{
		_err_stack._index = 0;
		memset(&_err_stack.values,0,MAX_CALL_LEVEL*sizeof(value_type));
		_err_stack.values[_err_stack._index] = err;
	}
	bool operator == (value_type v)
	{
		return _err_stack.values[_err_stack._index] == v;
	}
	bool operator != (value_type v)
	{
		return _err_stack.values[_err_stack._index] != v;
	}
	unsigned int getErrorCode()
	{
		int err_code = _err_code;
		_err_stack_map[_err_code++] = new InnerErrorStack(_err_stack);
		return err_code;
	}
	/*
	 * index 取值：0为当前，1为上次，2为上上次，以此类推
	 * 
	 */
	value_type getHistoryError(unsigned int index=0)
	{
		if(index > _err_stack._index)
			return 0;
		index = _err_stack._index - index;
		return _err_stack.values[_err_stack._index];
	}
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
	class Robot
	{
	public:
		Robot()
		{
			log("robot construct");
			init_global_err_map();
		}
		~Robot()
		{
			log("robot destruct");
			if(_err_stack_map.size() > 0)
			{
				log("_err_stack_map size > 0");
				for (std::map<unsigned int,void*>::iterator iter = _err_stack_map.begin();
					iter != _err_stack_map.end(); iter++)
				{
					log("iter _err_stack_map");
					if(iter->second)
					{
						log("free iter->second");
						InnerErrorStack * pes = reinterpret_cast<InnerErrorStack*>(iter->second);
						if(pes)
							delete pes;
						else
							delete iter->second;
					}
				}
				log("clear _err_stack_map");
				_err_stack_map.clear();
			}
		}
	};
	static Robot _robot;
private:
	struct InnerErrorStack
	{
		InnerErrorStack()
		{
			log("new InnerErrorStack");
			_index = 0;
			memset(&values,0,MAX_CALL_LEVEL*sizeof(value_type));
		}
		InnerErrorStack(const InnerErrorStack& v)
		{
			log("new InnerErrorStack 2");
			_index = v._index;
			memcpy(&values,&v,MAX_CALL_LEVEL*sizeof(value_type));
		}
		~InnerErrorStack()
		{
			log("delete InnerErrorStack");
		}
		value_type values[MAX_CALL_LEVEL];
		void operator = (const InnerErrorStack& v)
		{
			log("= InnerErrorStack");
			_index = v._index;
			memcpy(&values,&v,MAX_CALL_LEVEL*sizeof(value_type));
		}
		value_type operator [] (unsigned int index)
		{
			if(index<0 || index>=MAX_CALL_LEVEL)
				return 0;
			return values[index];
		}
		unsigned int _index;  //永远指向最后一个有值的位置
	} _err_stack;
	static unsigned int _err_code; //错误索引
	static std::map<unsigned int,void*> _err_stack_map;
};

#ifdef ERROR_STACK_NAMESPACE
}
#endif

#endif //头文件保护