#pragma once
#include <string>
#include <string.h>

namespace JsonHelper{

class JsonError;
class JsonParser;

/*
 * һ��JsonElement����һ����ֵ�Խڵ�
 * ֵ��������Bool,Number,String,Element����
 * ������һ��JsonElementʱ��
 * ���ָ�������֣������Ǹ������ڵ�(Ĭ��),��ʹ����Ϊ���ַ���
 * ���ָ������ΪNULL�������Ǹ������ڵ�
 * һ�������ڵ���ֵܽڵ㣬Ӧ��Ҳ�������ڵ�
 * һ�������ڵ���ֵܽڵ㣬Ӧ��Ҳ�������ڵ�
 * һ���ڵ�������ӽڵ��Ϊ�����ڵ�ʱ������Щ�ӽڵ㱻���ͳ�����
 */
class JsonElement
{
public:
	enum element_type {BOOLEAN,NUMBER,STRING,ELEMENT};

private:
	friend class JsonParser;
	struct Value
	{
		//�ڵ�ֵ
		bool b;
		double n;
		std::string s;
		JsonElement *e;

		//�ڵ�ֵ����
		element_type type;

		//�ṹ��Ĭ�Ϲ��캯��
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
	//#����������
	//���������Զ��ͷ��ӽڵ�
	~JsonElement();
	//����ELEMENT�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	//JsonElement(const char* k="");
	//����BOOLEAN�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	JsonElement(const char* k, bool v);
	//����NUMBER�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	JsonElement(const char* k, int v);
	//����NUMBER�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	JsonElement(const char* k, double v);
	//����STRING�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	JsonElement(const char* k, const char* v);
	//����ELEMENT�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	JsonElement(const char* k="", JsonElement* v=NULL);

	//#��ȡ�ڵ�
	//��ȡ��ǰ�ڵ�����Ƚڵ�
	JsonElement * get_root_element();
	//��ȡ��ǰ�ڵ�ĸ��ڵ�
	JsonElement * get_parent() { return parent; }
	//��ȡ��ǰ�ڵ��ǰһ���ڵ㣨û���ֵܽڵ�ʱ�������Լ���
	JsonElement * get_sibling_prev() { return prev; }
	//��ȡ��ǰ�ڵ�ĺ�һ���ڵ㣨û���ֵܽڵ�ʱ�������Լ���
	JsonElement * get_sibling_next() { return next; }
	//��ȡ��ǰ�ڵ�ĵ�һ���ֵܽڵ㣨����Ϊ�Լ���
	JsonElement * get_sibling_first();
	//��ȡ��ǰ�ڵ�����һ���ֵܽڵ㣨����Ϊ�Լ���
	JsonElement * get_sibling_last();
	//��ȡ��n���ֵܽڵ㣨��һ���ֵܽڵ�Ϊ0�����Ϊ������������ң�
	JsonElement * get_sibling_at(int index);
	//��ȡ��ǰ�ڵ�ĵ�һ������
	JsonElement * get_child_first() { return element_value.e; }
	//��ȡ��ǰ�ڵ�����һ������
	JsonElement * get_child_last();
	//��ȡ��ǰ�ڵ�ĵ�n�����ӣ���һ������Ϊ0����Ϊ����ʱ�������һ��������ǰ����
	JsonElement * get_child_at(int index);

	//#��ȡ�ڵ�����
	//�жϵ�ǰ�ڵ��Ƿ�Ϊ�����ڵ�
	bool has_name() { return hasname; }
	//��ȡ��ǰ�ڵ�����
	std::string get_name() { return element_name; }
	//��ȡ��ǰ�ڵ���ӽڵ����
	unsigned short get_children_count();
	//��ȡ�ֵܽڵ�����������Լ���
	unsigned short get_sibling_count();
	//��ȡ��ǰ�ڵ��д�ŵ�����
	bool get_value_boolean() { return element_value.b; }
	double get_value_number() { return element_value.n; }
	std::string get_value_string() { return element_value.s; }
	JsonElement* get_value_element() { return element_value.e; }
	//��ȡ��ǰ�ڵ㣨�������ݣ�������
	element_type get_value_type() { return element_value.type; }


	//#���ýڵ�����
	//���õ�ǰ�ڵ������
	void set_name(const char* n);
	//���õ�ǰ�ڵ�����ŵ�����
	void set_value(bool b);
	void set_value(int i);
	void set_value(double d);
	void set_value(JsonElement* e);
	void set_value(const char* s);

	//#��ɾ�ڵ�
	//����ǰ�ڵ�ӽڵ����з��루����Ľڵ����û������ͷţ�
	void detach();
	//ɾ�������ӽڵ㣨�Զ��ͷţ�
	void remove_all_children();
	//ɾ���ӽڵ㣬index��ֵͬget_child_at
	void remove_child(int index);
	//���ڵ�ŵ�һ��ELEMENT�ڵ��£���Ϊ����С�ĺ��ӣ��ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElement *add_child_last(JsonElement * e);
	//���ڵ�ŵ�һ��ELEMENT�ڵ��£���Ϊ�����ĺ��ӣ��ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElement *add_child_first(JsonElement * e);
	//��һ���ڵ���뵽��ǰ�ڵ��ǰ�棬�ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElement *add_sibling_before(JsonElement *e);
	//��һ���ڵ���뵽��ǰ�ڵ�ĺ��棬�ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElement *add_sibling_after(JsonElement *e);
	//��һ���ڵ���뵽��ǰ�ڵ���������Ŀ�ʼλ�ã��ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElement *add_sibling_first(JsonElement *e);
	//��һ���ڵ���뵽��ǰ�ڵ���������Ľ���λ�ã��ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElement *add_sibling_last(JsonElement *e);

	//#json��ת��
	//���ڵ�ת��Ϊjson�ַ���
	std::string get_json(bool formated=true);
	//��json�ַ���ת��Ϊ�ڵ�
	static JsonElement* new_jelement_from_json(const std::string & str_json);

private:
	void free_children();
	//���ڵ�ŵ�һ���յ�ELEMENT�ڵ��£���Ϊ���ĺ��ӣ��ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
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

//Json�ַ���������
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

//�쳣��
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