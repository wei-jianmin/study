#pragma once
#include <string>
#include <string.h>

namespace JsonHelper{

class JsonError;
class JsonParser;

/*
 * һ��JsonElement����һ����ֵ�Խڵ�
 * ֵ��������Bool,Number,String,Element����
 * Ϊ�������֣�JsonElement��JE : ��ָ���еļ�ֵ�Խڵ㣬
 *              BoolJElement��BJE : ��ֵָΪBool�ļ�ֵ�Խڵ㣬
 *              NumberJElement��NJE : ��ֵָΪNumber�ļ�ֵ�Խڵ㣬
 *              StringJElement��SJE : ��ֵָΪString�ļ�ֵ�Խڵ㣬
 *              ElementJElement��EJE : ��ֵָΪElement�ļ�ֵ�Խڵ㣬
 * ������һ��JsonElement�ǣ����ָ�������֣������Ǹ�����JE
 * ������һ��JsonElement�ǣ����ָ������ΪNULL�������Ǹ�����JE
 * һ��˵һ��JsonElementʱ��ͨ��Ĭ��ָ����JE
 * һ������JE����ɸ�����һ������JE��һ������JE����ɸ�����һ������JE
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
	JsonElement(const char* k="");
	//����BOOLEAN�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	JsonElement(const char* k, bool v);
	//����NUMBER�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	JsonElement(const char* k, int v);
	//����NUMBER�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	JsonElement(const char* k, double v);
	//����ELEMENT�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	JsonElement(const char* k, JsonElement* v);
	//����STRING�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	JsonElement(const char* k,const char* v);

	//#��ȡ�ڵ�
	//��ȡ��ǰ�ڵ�����Ƚڵ�
	JsonElement * get_top();
	//��ȡ��ǰ�ڵ���۵ܽڵ㣨����Ϊ�Լ���
	JsonElement * get_end();
	//��ȡ��ǰ�ڵ�ĳ��ֽڵ㣨����Ϊ�Լ���
	JsonElement * get_head();
	//��ȡ��ǰ�ڵ�����һ������
	JsonElement * get_last_child();
	//��ȡ��ǰ�ڵ�ĵ�n�����ӣ���һ������Ϊ0����Ϊ����ʱ�������һ��������ǰ����
	JsonElement * get_child_at(int index);
	//��ȡ��ǰ�ڵ��ǰһ���ڵ㣨û���ֵܽڵ�ʱ�������Լ���
	JsonElement * get_prev() { return prev; }
	//��ȡ��ǰ�ڵ�ĺ�һ���ڵ㣨û���ֵܽڵ�ʱ�������Լ���
	JsonElement * get_next() { return next; }
	//��ȡ��ǰ�ڵ�ĸ��ڵ�
	JsonElement * get_super() { return super; }
	//��ȡ��ǰ�ڵ�ĵ�һ������
	JsonElement * get_first_child() { return value.e; }

	//#��ȡ�ڵ�����
	//�жϵ�ǰ�ڵ��Ƿ�Ϊ�����ڵ�
	bool has_name() { return hasname; }
	//��ȡ��ǰ�ڵ�����
	std::string get_name() { return name; }
	//��ȡ��ǰ�ڵ���ӽڵ����
	unsigned short get_children_count();
	//��ȡ��ǰ�ڵ��д�ŵ�����
	bool get_value_boolean() { return value.b; }
	double get_value_number() { return value.n; }
	std::string get_value_string() { return value.s; }
	JsonElement* get_value_element() { return value.e; }
	//��ȡ��ǰ�ڵ㣨�������ݣ�������
	element_type get_value_type() { return value.type; }


	//#���ýڵ�����
	//���õ�ǰ�ڵ������
	void set_name(const char* n);
	//���õ�ǰ�ڵ�����ŵ�����
	void set_value_boolean(bool b);
	void set_value_number(double d);
	void set_value_element(JsonElement* e);
	void set_value_string(const std::string &s);

	//#��ɾ�ڵ�
	//����ǰ�ڵ�ӽڵ����з��루����Ľڵ����Լ������ͷţ�
	void detach();
	void remove_all_children();
	void remove_child(int index);
	//��һ���ڵ���뵽��ǰ�ڵ�ĺ��棬�ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElement *pushback_jelement(JsonElement * e);
	//���ڵ�ŵ�һ��ELEMENT�ڵ��£���Ϊ����С�ĺ��ӣ��ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElement *add_child_jelement(JsonElement * e);

	//#json��ת��
	//���ڵ�ת��Ϊjson�ַ���
	std::string get_json(bool formated);
	//��json�ַ���ת��Ϊ�ڵ�
	static JsonElement* new_jelement_from_json(const std::string & str_json);

private:
	void free_children();
	//���ڵ�ŵ�һ���յ�ELEMENT�ڵ��£���Ϊ���ĺ��ӣ��ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElement *set_child_jelement(JsonElement * e);
	void get_node_value(std::string & str_value,bool formated,int depth);

private:
	std::string name;
	bool hasname;
	Value value;
	JsonElement *next,*prev,*super;
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