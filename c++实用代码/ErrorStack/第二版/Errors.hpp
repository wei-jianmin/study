/* 
* 功能说明：
* Errors类通常作为函数的返回值使用
* 每个Errors对象能记录多级(/多个)错误码
* 并将这个错误码序列编码成个唯一的错误代号(uint32)
* 同时也能根据这个错误代号查询到相应的错误码序列
* 然后通过查询"错误码-错误信息转换表"
* 将错误码序列转换成错误信息描述序列
* 使用注意：
* 需在源文件中调用 INIT_ERROR_STACK 宏 (1次)
* 如果想使用本文件内置的"错误码-错误信息转换表"
* 需先初始化该内置转换表，可使用如下宏：
* BEGIN_SET_ERR_MAP、SET_ERR_MAP_VALUE、END_SET_ERR_MAP
*/

#ifndef ERROR_STACK_HPP
#define ERROR_STACK_HPP
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <map>

//支持命名空间，不使用命名空间，只需把下面一行注掉即可
//#define ERROR_STACK_NAMESPACE utils
#ifdef ERROR_STACK_NAMESPACE
#define ERRORS_NAMESPACE ERROR_STACK_NAMESPACE::
namespace ERROR_STACK_NAMESPACE {
#else
#define ERRORS_NAMESPACE
#endif

//静态成员初始化宏
#define INIT_ERRORS ERRORS_NAMESPACE Errors::Robot ERRORS_NAMESPACE Errors::_robot;\
	std::map<unsigned int,void*> ERRORS_NAMESPACE Errors::_err_stack_map;

//内置的"错误码-错误信息转换表"
typedef unsigned int value_type;
std::map<value_type,std::string> g_err_map;
#define BEGIN_SET_ERR_MAP  class CInitGlobalErrmap { public: CInitGlobalErrmap() {
#define SET_ERR_MAP_VALUE(K,V)  ERRORS_NAMESPACE g_err_map[K] = V;
#define END_SET_ERR_MAP  }} g_init_global_err_map;

#define MAX_CALL_LEVEL 99  /*定义支持最多多少级嵌套*/
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
	//清空历史错误序列
	void clear()
	{
		_err_stack.clear();
	}
	//将新的错误码增加到错误序列中
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
	//使得该类可相互间赋值
	Errors& operator = (const Errors& es)
	{
		_err_stack = es._err_stack;
		return *this;
	}
	//同 pushError
	Errors& operator + (value_type err)
	{
		return pushError(err);
	}
	//同 pushError
	void operator += (value_type err)
	{
		pushError(err);
	}
	//使得当前类可以与无符号整数进行比较
	bool operator == (value_type v)
	{
		return _err_stack._values[_err_stack._index] == v;
	}
	//使得当前类(的最后一个错误码)可以与无符号整数进行比较
	bool operator != (value_type v)
	{
		return _err_stack._values[_err_stack._index] != v;
	}
	//将错误序列转为错误代号
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
	 * 根据自身的错误码序列，查询"错误码-错误信息转换表"
	 * 将错误码序列转为错误信息描述序列
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
	* 将错误代号转为错误码序列，然后参照参数传入的"错误码-错误信息转换表"(err_map)
	* 将错误码序列转为错误信息描述序列
	* 除非err_map使用外部传入的参数，如果使用默认参数，需先对 g_err_map 初始化，可使用如下宏完成：
	* BEGIN_SET_ERR_MAP、SET_ERR_MAP_VALUE、END_SET_ERR_MAP
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
	class Robot /*辅助类*/
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
	struct InnerErrorStack /*数据类*/
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
		unsigned int _index;  //永远指向最后一个有值的位置
	};
private:
	//因为直接赋值整数功能意义不明确，所以将之隐藏
	Errors& operator = (value_type err){}
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