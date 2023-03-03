#pragma once
#include <string>
#include <string.h>

namespace JsonHelper{

class JsonError;
class JsonParser;

/*
 * 一个JsonElement，是一个键值对节点
 * 值的类型有Bool,Number,String,Element四种
 * 为便于区分，JsonElement或JE : 泛指所有的键值对节点，
 *              BoolJElement或BJE : 特指值为Bool的键值对节点，
 *              NumberJElement或NJE : 特指值为Number的键值对节点，
 *              StringJElement或SJE : 特指值为String的键值对节点，
 *              ElementJElement或EJE : 特指值为Element的键值对节点，
 * 当创建一个JsonElement是，如果指定了名字，它就是个有名JE
 * 当创建一个JsonElement是，如果指定名字为NULL，它就是个无名JE
 * 一般说一个JsonElement时，通常默认指有名JE
 * 一个有名JE后面可跟有另一个有名JE，一个无名JE后面可跟有另一个无名JE
 */
class JsonElement
{
public:
	enum element_type {BOOLEAN,NUMBER,STRING,ELEMENT};

private:
	friend class JsonParser;
	struct Value
	{
		//节点值
		bool b;
		double n;
		std::string s;
		JsonElement *e;

		//节点值类型
		element_type type;

		//结构体默认构造函数
		Value()
		{
			b = false;
			n = 0;
			e = NULL;
			s = "";
			type = ELEMENT;
		}
	};

public:
	//#构造与析构
	//析构函数自动释放子节点
	~JsonElement();
	//创建ELEMENT节点，当k为NULL时，创建无名节点，否则为有名节点
	JsonElement(const char* k="");
	//创建BOOLEAN节点，当k为NULL时，创建无名节点，否则为有名节点
	JsonElement(const char* k, bool v);
	//创建NUMBER节点，当k为NULL时，创建无名节点，否则为有名节点
	JsonElement(const char* k, int v);
	//创建NUMBER节点，当k为NULL时，创建无名节点，否则为有名节点
	JsonElement(const char* k, double v);
	//创建ELEMENT节点，当k为NULL时，创建无名节点，否则为有名节点
	JsonElement(const char* k, JsonElement* v);
	//创建STRING节点，当k为NULL时，创建无名节点，否则为有名节点
	JsonElement(const char* k,const char* v);

	//#获取节点
	//获取当前节点的祖先节点
	JsonElement * get_top();
	//获取当前节点的幺弟节点（可能为自己）
	JsonElement * get_end();
	//获取当前节点的长兄节点（可能为自己）
	JsonElement * get_head();
	//获取当前节点的最后一个孩子
	JsonElement * get_last_child();
	//获取当前节点的第n个孩子（第一个孩子为0，当为负数时，从最后一个孩子向前算起）
	JsonElement * get_child_at(int index);
	//获取当前节点的前一个节点（没有兄弟节点时，返回自己）
	JsonElement * get_prev() { return prev; }
	//获取当前节点的后一个节点（没有兄弟节点时，返回自己）
	JsonElement * get_next() { return next; }
	//获取当前节点的父节点
	JsonElement * get_super() { return super; }
	//获取当前节点的第一个孩子
	JsonElement * get_first_child() { return value.e; }

	//#获取节点属性
	//判断当前节点是否为有名节点
	bool has_name() { return hasname; }
	//获取当前节点名字
	std::string get_name() { return name; }
	//获取当前节点的子节点个数
	unsigned short get_children_count();
	//获取当前节点中存放的数据
	bool get_value_boolean() { return value.b; }
	double get_value_number() { return value.n; }
	std::string get_value_string() { return value.s; }
	JsonElement* get_value_element() { return value.e; }
	//获取当前节点（所存数据）的类型
	element_type get_value_type() { return value.type; }


	//#设置节点属性
	//设置当前节点的名字
	void set_name(const char* n);
	//设置当前节点所存放的数据
	void set_value_boolean(bool b);
	void set_value_number(double d);
	void set_value_element(JsonElement* e);
	void set_value_string(const std::string &s);

	//#增删节点
	//将当前节点从节点树中分离（分离的节点由自己负责释放）
	void detach();
	void remove_all_children();
	void remove_child(int index);
	//将一个节点插入到当前节点的后面，成功则返回插入的子节点，否则返回自身
	JsonElement *pushback_jelement(JsonElement * e);
	//将节点放到一个ELEMENT节点下，作为它最小的孩子，成功则返回插入的子节点，否则返回自身
	JsonElement *add_child_jelement(JsonElement * e);

	//#json串转换
	//将节点转换为json字符串
	std::string get_json(bool formated);
	//将json字符串转换为节点
	static JsonElement* new_jelement_from_json(const std::string & str_json);

private:
	void free_children();
	//将节点放到一个空的ELEMENT节点下，作为它的孩子，成功则返回插入的子节点，否则返回自身
	JsonElement *set_child_jelement(JsonElement * e);
	void get_node_value(std::string & str_value,bool formated,int depth);

private:
	std::string name;
	bool hasname;
	Value value;
	JsonElement *next,*prev,*super;
};

//Json字符串解析类
class JsonParser
{
public:
	JsonElement * new_jelement_from_json(std::string str_json);

private:
	void throw_format_error();
	bool dealwith_name_part(JsonElement * pe);
	bool dealwith_bool_part(JsonElement* pe);
	bool dealwith_num_part(JsonElement* pe);
	bool dealwith_string_part(JsonElement* pe);
	bool dealwith_ele_part(JsonElement* pe);
	bool dealwith_array_part(JsonElement* pe);
	std::string dealwith_json(const std::string &str_json);

private:
	std::string json_value;
	int index;
	int json_len;
};

//异常类
class JsonError
{
public:
	enum {
		PARAM_NULL,
		NULL_STRING,
		OUT_OF_RANGE,
		JSON_FORMAT_ERROR,
		NULL_VALUE_ELEMENT,
		FORMAT_NOT_ELEMENT,
		NONAME_ELE_AFTER_ELE,
		ELE_AFTER_NONAME_ELE,
		SETNAME_FOR_NONAME_ELE,
		JELEMENT_UNDER_NON_ELEMENT,
		UNINDEPENDENT_ELE_UNDER_ELE,
		DELETE_UNINDEPENDENT_JELEMENT,
		JELEMENT_UNDER_NOTBLANK_ELEMENT
	};
	JsonError(int err_num,const char* err_msg)
	{
		err_num_ = err_num;
		if(!err_msg || strlen(err_msg)<=0)
			err_msg_ = "unknown error";
		else
			err_msg_ = err_msg;
	}
	std::string what(){return err_msg_;}
	int value(){return err_num_;}
private:
	std::string err_msg_;
	int err_num_;
};

}  //namespace JsonHelper