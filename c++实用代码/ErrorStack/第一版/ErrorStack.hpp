/* 
* 功能说明：
* ErrorStack类通常作为函数的返回值使用
* 每个ErrorStack对象能记录多级(/多个)错误码
* 并将这个错误码序列编码成个唯一的错误代号(uint32)
* 同时也能根据这个错误代号查询到相应的错误码序列
* 然后通过查询"错误码-错误信息转换表"
* 将错误码序列转换成错误信息描述序列
* 使用注意：
* 需在源文件中调用 INIT_ERROR_STACK 宏 (1次)
* 如果想使用本文件内置的"错误码-错误信息转换表"
* 需先自行完善 init_global_err_map 函数
*/

#ifndef ERROR_STACK_HPP
#define ERROR_STACK_HPP
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <map>

//#define ERROR_STACK_NAMESPACE utils
#ifdef ERROR_STACK_NAMESPACE  /*使用命名空间*/
namespace ERROR_STACK_NAMESPACE 
{
#endif

//静态成员初始化宏
#define INIT_ERROR_STACK ErrorStack::Robot ErrorStack::_robot;\
	  std::map<unsigned int,void*> ErrorStack::_err_stack_map;
	

//内置的"错误码-错误信息转换表"
typedef unsigned int value_type;
std::map<value_type,std::string> g_err_map;
void init_global_err_map()
{
	//g_err_map[ERR1] = "error discription 1";
	//g_err_map[ERR2] = "error discription 2";
}

#define MAX_CALL_LEVEL 99  /*定义支持最多多少级嵌套*/
#define ERR_CODE_BASE 100  /*所返回错误索引的最小值*/

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
	//将新的错误码增加到错误序列中
	ErrorStack& pushError(value_type err)
	{
		if(_err_stack._index < MAX_CALL_LEVEL-1)
			_err_stack._index++;
		_err_stack._values[_err_stack._index] = err;
		return *this;
	}
	//使得该类可赋值为无符号整数，相当于初始化
	ErrorStack& operator = (value_type err)
	{
		_err_stack._index = 0;
		memset(&_err_stack._values,0,MAX_CALL_LEVEL*sizeof(value_type));
		_err_stack._values[_err_stack._index] = err;
	}
	//使得当前类可以与无符号整数进行比较
	bool operator == (value_type v)
	{
		return _err_stack._values[_err_stack._index] == v;
	}
	//使得当前类可以与无符号整数进行比较
	bool operator != (value_type v)
	{
		return _err_stack._values[_err_stack._index] != v;
	}
	//将错误序列转为错误代号
	unsigned int getErrorCode()
	{
		unsigned int err_code = crc32(_err_stack);
		if(_err_stack_map.find(err_code) == _err_stack_map.end())
			_err_stack_map[err_code] = new InnerErrorStack(_err_stack);
		return err_code;
	}
	/*
	* 获取历史存入的错误代号
	* index 取值：0为当前，1为上次，2为上上次，以此类推
	*/
	value_type getHistoryError(unsigned int index=0)
	{
		if(index > _err_stack._index)
			return 0;
		index = _err_stack._index - index;
		return _err_stack._values[_err_stack._index];
	}
	/*
	* 将错误代号转为错误码序列，然后查询内置的"错误码-错误信息转换表"
	* 将错误码序列转为错误信息描述序列
	* 要调用此函数，需先自行完善本文件中的 init_global_err_map 函数
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
	* 将错误代号转为错误码序列，然后查询外部的"错误码-错误信息转换表"
	* 将错误码序列转为错误信息描述序列
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
	class Robot /*辅助类*/
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
	struct InnerErrorStack /*数据类*/
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
		unsigned int _index;  //永远指向最后一个有值的位置
	};
private:
	//将错误码序列转为错误代号的函数
	unsigned int crc32(const InnerErrorStack& es)
	{
		return crc32((unsigned char*)es._values,(es._index+1)*sizeof(value_type));
	}
	//将错误码序列转为错误代号的函数
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
	static Robot _robot;  //辅助工具
	InnerErrorStack _err_stack;  //当前对象的错误码序列
	static std::map<unsigned int,void*> _err_stack_map;  //"错误代号-错误序列"关系表
};

#ifdef ERROR_STACK_NAMESPACE
}
#endif

#endif //头文件保护