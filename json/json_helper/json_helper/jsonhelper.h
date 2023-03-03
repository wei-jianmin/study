#pragma once
#include <string>
#include <string.h>

//#define THROW_JSON_ERROR  /*�����ش���ʱ���Ƿ��׳��쳣*/

namespace JsonHelper{

class JsonError;
class JsonParser;
class JsonElement;

class IBase
{
public:
	IBase(){ ref_count = 0; }
	virtual void AddRef() { ref_count++; }
	virtual void SubRef() { ref_count--; }
	virtual int  GetRef() { return ref_count; }
private:
	int ref_count;
};

class JsonElementPtr
{
public:
	JsonElementPtr(){
		imp_ = NULL;
	}
	JsonElementPtr(JsonElement* ptr);
	JsonElementPtr(const JsonElementPtr& ptr);
	~JsonElementPtr(); 
public:
	/*bool operator == (JsonElement* ptr) {
		return ptr==imp_;
	}*/
	bool operator == (JsonElement* ptr) const{
		return ptr==imp_;
	}
	/*bool operator != (JsonElement* ptr) {
		return ptr!=imp_;
	}*/
	bool operator != (JsonElement* ptr) const{
		return ptr!=imp_;
	}
	/*bool operator == (const JsonElementPtr& ptr) {
		return ptr.imp_ == imp_;
	}*/
	bool operator == (const JsonElementPtr& ptr) const{
		return ptr.imp_ == imp_;
	}
	/*bool operator != (const JsonElementPtr& ptr) {
		return ptr.imp_ != imp_;
	}*/
	bool operator != (const JsonElementPtr& ptr) const{
		return ptr.imp_ != imp_;
	}
	void operator = (const JsonElementPtr& ptr);
	void operator =(const JsonElement* ptr);
	JsonElement* operator ->()  {
		if(imp_){
			return imp_;
		}
		throw std::runtime_error("access through NULL pointer"); 
	}
	JsonElement* operator ->()  const{
		if(imp_){
			return imp_;
		}
		throw std::runtime_error("access through NULL pointer"); 
	}
	bool IsNull() const  {
		return (imp_ == NULL);
	}
	bool IsNotNull() const {
		return (imp_ != NULL);
	}
private:
	JsonElement* Get() {
		return imp_;
	}
	JsonElement* Get() const {
		return imp_;
	}
private:
	JsonElement* imp_;
};

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
class JsonElement : private IBase
{
public:
	enum element_type {BOOLEAN,NUMBER,STRING,ELEMENT};

private:
	friend class JsonParser;
	friend class JsonElementPtr;
	struct Value  //������Variant����
	{
		//�ڵ�ֵ
		bool b;
		double n;
		std::string s;
		JsonElementPtr e;

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
	//����BOOLEAN�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	static JsonElementPtr MakeElement(const char* k, bool v)
	{
		return JsonElementPtr(new JsonElement(k,v));
	}
	//����NUMBER�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	static JsonElementPtr MakeElement(const char* k, int v)
	{
		return JsonElementPtr(new JsonElement(k,v));
	}
	//����NUMBER�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	static JsonElementPtr MakeElement(const char* k, double v)
	{
		return JsonElementPtr(new JsonElement(k,v));
	}
	//����STRING�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	static JsonElementPtr MakeElement(const char* k, const char* v)
	{
		return JsonElementPtr(new JsonElement(k,v));
	}
	//����ELEMENT�ڵ㣬��kΪNULLʱ�����������ڵ㣬����Ϊ�����ڵ�
	static JsonElementPtr MakeElement(const char* k="", JsonElementPtr v=NULL)
	{
		return JsonElementPtr(new JsonElement(k,v));
	}

public:
	//#��ȡ�ڵ�
	//��ȡ��ǰ�ڵ�����Ƚڵ�
	JsonElementPtr get_root_element();
	//��ȡ��ǰ�ڵ�ĸ��ڵ�
	JsonElementPtr get_parent() { return parent; }
	//��ȡ��ǰ�ڵ��ǰһ���ڵ㣨û���ֵܽڵ�ʱ�������Լ���
	JsonElementPtr get_sibling_prev() { return prev; }
	//��ȡ��ǰ�ڵ�ĺ�һ���ڵ㣨û���ֵܽڵ�ʱ�������Լ���
	JsonElementPtr get_sibling_next() { return next; }
	//��ȡ��ǰ�ڵ�ĵ�һ���ֵܽڵ㣨����Ϊ�Լ���
	JsonElementPtr get_sibling_first();
	//��ȡ��ǰ�ڵ�����һ���ֵܽڵ㣨����Ϊ�Լ���
	JsonElementPtr get_sibling_last();
	//��ȡ��n���ֵܽڵ㣨��һ���ֵܽڵ�Ϊ0�����Ϊ������������ң�
	JsonElementPtr get_sibling_at(int index);
	//��ȡ��ǰ�ڵ�ĵ�һ������
	JsonElementPtr get_child_first() { return element_value.e; }
	//��ȡ��ǰ�ڵ�����һ������
	JsonElementPtr get_child_last();
	//��ȡ��ǰ�ڵ�ĵ�n�����ӣ���һ������Ϊ0����Ϊ����ʱ�������һ��������ǰ����
	JsonElementPtr get_child_at(int index);
	//����ָ����·����ȡ�ڵ�,·������Ϊ��/���ڵ���/һ���ӽڵ���/�����ӽڵ���/...
	JsonElementPtr get_element_bypath(const char* path);
	JsonElementPtr get_element_bypath(const JsonElementPtr& parent, const char* path);

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
	JsonElementPtr get_value_element() { return element_value.e; }
	//��ȡ��ǰ�ڵ㣨�������ݣ�������
	element_type get_value_type() { return element_value.type; }

	//#���ýڵ�����
	//���õ�ǰ�ڵ������
	bool set_name(const char* n);
	//���õ�ǰ�ڵ�����ŵ�����
	void set_value(bool b);
	void set_value(int i);
	void set_value(double d);
	void set_value(JsonElementPtr& e);
	void set_value(const char* s);

	//#��ɾ�ڵ�
	//����ǰ�ڵ�ӽڵ����з��루����Ľڵ����û������ͷţ�
	void detach();
	//ɾ�������ӽڵ㣨�Զ��ͷţ�
	void remove_all_children();
	//ɾ���ӽڵ㣬index��ֵͬget_child_at
	void remove_child(int index);
	//���ڵ�ŵ�һ��ELEMENT�ڵ��£���Ϊ����С�ĺ��ӣ��ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElementPtr add_child_last(const JsonElementPtr& e);
	//���ڵ�ŵ�һ��ELEMENT�ڵ��£���Ϊ�����ĺ��ӣ��ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElementPtr add_child_first(const JsonElementPtr& e);
	//��һ���ڵ���뵽��ǰ�ڵ��ǰ�棬�ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElementPtr add_sibling_before(const JsonElementPtr& e);
	//��һ���ڵ���뵽��ǰ�ڵ�ĺ��棬�ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElementPtr add_sibling_after(const JsonElementPtr& e);
	//��һ���ڵ���뵽��ǰ�ڵ���������Ŀ�ʼλ�ã��ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElementPtr add_sibling_first(const JsonElementPtr& e);
	//��һ���ڵ���뵽��ǰ�ڵ���������Ľ���λ�ã��ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElementPtr add_sibling_last(const JsonElementPtr& e);

	//#json��ת��
	//���ڵ�ת��Ϊjson�ַ���
	std::string get_json(bool formated=true);
	//��json�ַ���ת��Ϊ�ڵ�
	static JsonElementPtr new_jelement_from_json(const std::string & str_json);

	static std::string get_last_error() { return last_error; }

private:
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
	JsonElement(const char* k="", const JsonElementPtr& v=NULL);

private:
	//void free_children();
	static void throw_error(int err_num,const char* err_msg);
	//���ڵ�ŵ�һ���յ�ELEMENT�ڵ��£���Ϊ���ĺ��ӣ��ɹ��򷵻ز�����ӽڵ㣬���򷵻�����
	JsonElementPtr set_child_jelement(const JsonElementPtr& e);
	bool get_node_value(std::string & str_value,bool formated,int depth);
	bool check_before_add_child(const JsonElementPtr& e);
	bool check_before_add_sibling(const JsonElementPtr& e);

private:
	bool hasname;
	std::string element_name; 
	Value element_value;
	JsonElementPtr next,prev,parent;
	static std::string last_error;
};

//Json�ַ���������
class JsonParser
{
public:
	JsonElementPtr new_jelement_from_json(std::string str_json);

private:
	void throw_format_error();
	bool dealwith_name_part(const JsonElementPtr& pe);
	bool dealwith_bool_part(const JsonElementPtr& pe);
	bool dealwith_num_part(const JsonElementPtr& pe);
	bool dealwith_string_part(const JsonElementPtr& pe);
	bool dealwith_ele_part(const JsonElementPtr& pe);
	bool dealwith_array_part(const JsonElementPtr& pe);
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