#pragma once
#include <string>
#include <string.h>

namespace JsonHelper{

class JsonError;
class JsonParser;

/*
 * 一个JsonElement，是一个键值对节点
 * 值的类型有Bool,Number,String,Element四种
 * 当创建一个JsonElement时，
 * 如果指定了名字，它就是个有名节点(默认),即使名字为空字符串
 * 如果指定名字为NULL，它就是个无名节点
 * 一个有名节点的兄弟节点，应该也是有名节点
 * 一个无名节点的兄弟节点，应该也是无名节点
 * 一个节点的所有子节点均为无名节点时，则这些子节点被解释成数组
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
	//JsonElement(const char* k="");
	//创建BOOLEAN节点，当k为NULL时，创建无名节点，否则为有名节点
	JsonElement(const char* k, bool v);
	//创建NUMBER节点，当k为NULL时，创建无名节点，否则为有名节点
	JsonElement(const char* k, int v);
	//创建NUMBER节点，当k为NULL时，创建无名节点，否则为有名节点
	JsonElement(const char* k, double v);
	//创建STRING节点，当k为NULL时，创建无名节点，否则为有名节点
	JsonElement(const char* k, const char* v);
	//创建ELEMENT节点，当k为NULL时，创建无名节点，否则为有名节点
	JsonElement(const char* k="", JsonElement* v=NULL);

	//#获取节点
	//获取当前节点的祖先节点
	JsonElement * get_root_element();
	//获取当前节点的父节点
	JsonElement * get_parent() { return parent; }
	//获取当前节点的前一个节点（没有兄弟节点时，返回自己）
	JsonElement * get_sibling_prev() { return prev; }
	//获取当前节点的后一个节点（没有兄弟节点时，返回自己）
	JsonElement * get_sibling_next() { return next; }
	//获取当前节点的第一个兄弟节点（可能为自己）
	JsonElement * get_sibling_first();
	//获取当前节点的最后一个兄弟节点（可能为自己）
	JsonElement * get_sibling_last();
	//获取第n个兄弟节点（第一个兄弟节点为0，如果为负数，则反向查找）
	JsonElement * get_sibling_at(int index);
	//获取当前节点的第一个孩子
	JsonElement * get_child_first() { return element_value.e; }
	//获取当前节点的最后一个孩子
	JsonElement * get_child_last();
	//获取当前节点的第n个孩子（第一个孩子为0，当为负数时，从最后一个孩子向前算起）
	JsonElement * get_child_at(int index);

	//#获取节点属性
	//判断当前节点是否为有名节点
	bool has_name() { return hasname; }
	//获取当前节点名字
	std::string get_name() { return element_name; }
	//获取当前节点的子节点个数
	unsigned short get_children_count();
	//获取兄弟节点个数（包括自己）
	unsigned short get_sibling_count();
	//获取当前节点中存放的数据
	bool get_value_boolean() { return element_value.b; }
	double get_value_number() { return element_value.n; }
	std::string get_value_string() { return element_value.s; }
	JsonElement* get_value_element() { return element_value.e; }
	//获取当前节点（所存数据）的类型
	element_type get_value_type() { return element_value.type; }


	//#设置节点属性
	//设置当前节点的名字
	void set_name(const char* n);
	//设置当前节点所存放的数据
	void set_value(bool b);
	void set_value(int i);
	void set_value(double d);
	void set_value(JsonElement* e);
	void set_value(const char* s);

	//#增删节点
	//将当前节点从节点树中分离（分离的节点由用户负责释放）
	void detach();
	//删除所有子节点（自动释放）
	void remove_all_children();
	//删除子节点，index的值同get_child_at
	void remove_child(int index);
	//将节点放到一个ELEMENT节点下，作为它最小的孩子，成功则返回插入的子节点，否则返回自身
	JsonElement *add_child_last(JsonElement * e);
	//将节点放到一个ELEMENT节点下，作为它最大的孩子，成功则返回插入的子节点，否则返回自身
	JsonElement *add_child_first(JsonElement * e);
	//将一个节点插入到当前节点的前面，成功则返回插入的子节点，否则返回自身
	JsonElement *add_sibling_before(JsonElement *e);
	//将一个节点插入到当前节点的后面，成功则返回插入的子节点，否则返回自身
	JsonElement *add_sibling_after(JsonElement *e);
	//将一个节点插入到当前节点所在链表的开始位置，成功则返回插入的子节点，否则返回自身
	JsonElement *add_sibling_first(JsonElement *e);
	//将一个节点插入到当前节点所在链表的结束位置，成功则返回插入的子节点，否则返回自身
	JsonElement *add_sibling_last(JsonElement *e);

	//#json串转换
	//将节点转换为json字符串
	std::string get_json(bool formated=true);
	//将json字符串转换为节点
	static JsonElement* new_jelement_from_json(const std::string & str_json);

private:
	void free_children();
	//将节点放到一个空的ELEMENT节点下，作为它的孩子，成功则返回插入的子节点，否则返回自身
	JsonElement *set_child_jelement(JsonElement * e);
	void get_node_value(std::string & str_value,bool formated,int depth);
	bool check_before_add_child(JsonElement * e);
	bool check_before_add_sibling(JsonElement * e);

private:
	std::string element_name;
	bool hasname;
	Value element_value;
	JsonElement *next,*prev,*parent;
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
		NO_CHILD,
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