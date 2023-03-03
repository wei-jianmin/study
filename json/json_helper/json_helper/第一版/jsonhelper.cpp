#include "jsonhelper.h"
#include <iostream>
#include <sstream>
#include <stdexcept>

namespace JsonHelper {

JsonElement::JsonElement(const char* k)
{
	if(k)
	{
		name = k;
		hasname = true;
	}
	else
	{
		name = "";
		hasname = false;
	}
	value.type = ELEMENT;
	value.e = NULL;
	next = this;
	prev = this;
	super = NULL;
}

JsonElement::JsonElement(const char* k, JsonElement* v){
	if(k)
	{
		name = k;
		hasname = true;
	}
	else
	{
		name = "";
		hasname = false;
	}
	value.type = ELEMENT;
	value.e = v;
	next = this;
	prev = this;
	super = NULL;
}

JsonElement::JsonElement(const char* k, double v)
{
	if(k)
	{
		name = k;
		hasname = true;
	}
	else
	{
		name = "";
		hasname = false;
	}
	value.type = NUMBER;
	value.n	 = v;
	next = this;
	prev = this;
	super = NULL;
}

JsonElement::JsonElement(const char* k, const char* v)
{
	if(k)
	{
		name = k;
		hasname =true;
	}
	else
	{
		name = "";
		hasname = false;
	}
	
	value.type = STRING;
	value.s = v;
	next = this;
	prev = this;
	super = NULL;
}

JsonElement::JsonElement(const char* k, bool v)
{
	if(k)
	{
		name = k;
		hasname = true;
	}
	else
	{
		name = "";
		hasname = false;
	}
	value.type = BOOLEAN;
	value.b = v;
	next = this;
	prev = this;
	super = NULL;
}

JsonElement::JsonElement(const char* k, int v)
{
	if(k)
	{
		name = k;
		hasname = true;
	}
	else
	{
		name = "";
		hasname = false;
	}
	value.type = NUMBER;
	value.n	 = v;
	next = this;
	prev = this;
	super = NULL;
}

JsonElement::~JsonElement()
{
	detach();
	free_children();
}

void JsonElement::free_children()
{
	if(value.type != ELEMENT)
		return;

	JsonElement * p = value.e;
	JsonElement * p2;

	if(p==NULL)
		return;

	do 
	{
		p2 = p;
		p = p->next;
		delete p2;
	} while (value.e);
}

void JsonElement::set_name(const char* n)
{
	if(n!=NULL && hasname)
	{
		name = n;
	}
	else if(n==NULL)
	{
		throw JsonError(JsonError::PARAM_NULL,"param is null");	
	}
	else
	{
		throw JsonError(JsonError::SETNAME_FOR_NONAME_ELE,"set name for an unnamed element");
	}
}

void JsonElement::set_value_boolean( bool b )
{
	if(value.type == ELEMENT)
	{
		if(value.e)
		{
			delete value.e;
			value.e = NULL;
		}
	}
	value.b = b;
	value.n = 0;
	value.s = "";
	value.type = BOOLEAN;
}

void JsonElement::set_value_number( double d )
{
	if(value.type == ELEMENT)
	{
		if(value.e)
		{
			delete value.e;
			value.e = NULL;
		}
	}
	value.s = "";
	value.b = false;
	value.n = d;
	value.type = NUMBER;
}

void JsonElement::set_value_element( JsonElement* e )
{
	if(value.type == ELEMENT)
	{
		if(value.e)
		{
			delete value.e;
			value.e = NULL;
		}
	}
	e->super = this;
	value.e = e;
	value.b = false;
	value.n = 0;
	value.s = "";
	value.type = BOOLEAN;
}

void JsonElement::set_value_string( const std::string &s )
{
	if(value.type == ELEMENT)
	{
		if(value.e)
		{
			delete value.e;
			value.e = NULL;
		}
	}
	value.b = false;
	value.n = 0;
	value.s = s;
	value.type = STRING;
}

//一个子节点必须被分离出来之后，才能手动删除
void JsonElement::detach()
{
	if(this->next == this)	//没有兄弟节点
	{
		if(super)
			this->super->value.e = NULL;
	}
	else
	{
		if(super && super->value.e==this)
			super->value.e = this->next;
		this->prev->next = this->next;
		this->next->prev = this->prev;
	}
	this->super = NULL;
	return;
}

void JsonElement::remove_child( int index )
{
	JsonElement * pe = get_child_at(index);
	if(pe)
	{
		delete pe;
	}
}

void JsonElement::remove_all_children()
{
	JsonElement * plast = value.e->prev;
	JsonElement * pe = value.e;
	JsonElement * ptmp = NULL;
	do
	{
		ptmp = pe->next;
		delete pe;
		pe = ptmp;
	} while(pe != plast);
	delete pe;
}

//在当前键值对的后面追加
JsonElement * JsonElement::pushback_jelement(JsonElement * e)
{
	if(e==NULL)
	{
		throw JsonError(JsonError::PARAM_NULL,"param is null");	
		return this;
	}
	if(e->super!=NULL || e->next!=e)
	{
		throw JsonError(JsonError::UNINDEPENDENT_ELE_UNDER_ELE,"push not independent child jelement in element");	
		return this;
	}
	if(this->hasname)
	{
		if(e->hasname == false)
		{
			throw JsonError(JsonError::NONAME_ELE_AFTER_ELE,"add noname element after a named element");
			return this;
		}
	}
	else
	{
		if(e->hasname)
		{
			throw JsonError(JsonError::ELE_AFTER_NONAME_ELE,"add named element after a noname element");
			return this;
		}
	}
	e->next = this->next;
	e->prev = this;
	this->next = e;
	e->next->prev = e;
	e->super = this->super;
	return e;
}

//只有当前键值对是ELEMENT类型时，才允许增加
JsonElement * JsonElement::set_child_jelement(JsonElement * e)
{
	if(e==NULL)
	{
		throw JsonError(JsonError::PARAM_NULL,"param is null");	
		return this;
	}
	if(e->super!=NULL || e->next!=e)
	{
		throw JsonError(JsonError::UNINDEPENDENT_ELE_UNDER_ELE,"push not independent child jelement in element");	
		return this;
	}
	if(value.type != ELEMENT)
	{
		char * err_msg = NULL;
		if(value.type == BOOLEAN)
			err_msg = "push child jelement in boolean element";
		else if(value.type == NUMBER)
			err_msg = "push child jelement in number element";
		else if(value.type == STRING)
			err_msg = "push child jelement in string element";
		throw JsonError(JsonError::JELEMENT_UNDER_NON_ELEMENT,err_msg);
		return this;
	}
	if(this->value.e != NULL)
	{
		throw JsonError(JsonError::JELEMENT_UNDER_NOTBLANK_ELEMENT,"push child jelement in not blank element");	
		return this;
	}
	if(e->super!=NULL || e->next!=e)
	{
		throw JsonError(JsonError::UNINDEPENDENT_ELE_UNDER_ELE,"push not independent child jelement in element");	
		return this;
	}
	e->super = this;
	this->value.e = e;
	return e;
}

//成功返回子节点，失败返回本节点
JsonElement * JsonElement::add_child_jelement(JsonElement * e)
{
	if(e==NULL)
	{
		throw JsonError(JsonError::PARAM_NULL,"param is null");	
		return this;
	}
	if(e->super!=NULL || e->next!=e)
	{
		throw JsonError(JsonError::UNINDEPENDENT_ELE_UNDER_ELE,"push not independent child jelement in element");	
		return this;
	}
	if(this->value.e == NULL)
	{
		return set_child_jelement(e);
	}
	else
	{
		JsonElement * pe = this->value.e;
		e->prev = pe->prev;
		e->next = pe;
		pe->prev = e;
		e->prev->next = e;
		e->super = pe->super;
		return e;
	}
}

JsonElement * JsonElement::get_head()
{
	if(super)
		return super->value.e;
	else
		return this;
}

JsonElement * JsonElement::get_end()
{
	if(super)
		return super->value.e->prev;
	else
		return this;
}

JsonElement * JsonElement::get_top()
{
	JsonElement * p = super;
	if(p == NULL)
		return this;
	while(p->super)
		p = p->super;
	return p;
}

JsonElement * JsonElement::get_last_child()
{
	JsonElement * p = value.e;
	if(p==NULL)
		return NULL;
	return p->prev;
}

JsonElement * JsonElement::get_child_at( int index )
{
	unsigned short count = get_children_count();
	if(count == 0)
		return NULL;

	if(index >= count || index < -count)
	{
		throw JsonError(JsonError::OUT_OF_RANGE,"get child out of range");
		return NULL;
	}

	
	JsonElement * p = value.e;

	if(index == 0)
	{
		return p;
	}
	else if(index > 0)
	{
		while(index>0)
		{
			p = p->next;
			index--;
		}
	}
	else
	{
		while(index<0)
		{
			p = p->prev;
			index++;
		}
	}
	return p;
}

unsigned short JsonElement::get_children_count()
{
	if(value.e)
	{
		unsigned short count =1;
		JsonElement * p = value.e;
		JsonElement * p2 = p->next;
		while(p2!=p)
		{
			count++;
			p2=p2->next;
		}
		return count;
	}
	else
	{
		return 0;
	}
}

void JsonElement::get_node_value(std::string & str_value,bool formated,int depth)
{
	std::stringstream stm_tmp;
	JsonElement * pele = this;

	if(formated)
	{
		depth++;
	}

	if(pele)
	{
		if(pele->value.type == BOOLEAN)
		{
			if(value.b)
				stm_tmp << "true" ;
			else
				stm_tmp << "false" ;
		}
		else if(pele->value.type == NUMBER)
		{
			stm_tmp << value.n ;
		}
		else if(pele->value.type == STRING)
		{
			stm_tmp << "\"" << value.s << "\"" ;
		}
		else if(pele->value.type == ELEMENT)
		{
			JsonElement * pe = pele->value.e;
			if(pe == NULL)
			{
				throw JsonError(JsonError::NULL_VALUE_ELEMENT,"try to show an element with no value");
				return;
			}
			
			if(pe->hasname) stm_tmp << "{";
			else stm_tmp << "[";
			if(formated) stm_tmp << "\n";

			JsonElement * phead = pe;
			do
			{
				std::string str_tmp;
				for(int i=0;i<depth;i++) stm_tmp << "\t";
				if(pe->hasname)
					stm_tmp << "\"" << pe->name << "\":";
				pe->get_node_value(str_tmp,formated,depth);
				stm_tmp  << str_tmp;
				if(pe->next != phead)
					stm_tmp << ",";
				if(formated) stm_tmp << "\n";
				pe = pe->next;
			}while(pe != pele->value.e);

			pe = pele->value.e;
			for(int i=0;i<depth-1;i++) stm_tmp << "\t";
			if(pe->hasname) stm_tmp << "}";
			else stm_tmp << "]";
		}
	}
	str_value = stm_tmp.str();
}

std::string JsonElement::get_json(bool formated)
{
	if(value.type != ELEMENT)
	{
		throw JsonError(JsonError::FORMAT_NOT_ELEMENT,"type isnot ELEMENT,cannot be formated");
		return "";
	}

	int depth = 0;
	std::string json_string;
	get_node_value(json_string,formated,depth);
	return json_string;
}

JsonElement* JsonElement::new_jelement_from_json(const std::string & str_json)
{
	JsonParser parser;
	return parser.new_jelement_from_json(str_json);
}

void JsonParser::throw_format_error()
{
	throw JsonError(JsonError::JSON_FORMAT_ERROR,"counted format error when parse json");
}

bool JsonParser::dealwith_name_part(JsonElement * pe)
{
	if(json_value.at(index)!='"')
	{
		return false;
	}
	index++;

	int name_len=0;
	while(index < json_len)
	{
		if(json_value[index+name_len]=='"' && json_value[index+name_len-1]!='\\')
			break;
		name_len++;
	}

	if(name_len==0)
	{
		pe->set_name("");
		return true;
	}

	pe->set_name(json_value.substr(index,name_len).c_str());
	index += (name_len+1);
	return true;
}

bool JsonParser::dealwith_bool_part(JsonElement* pe)
{
	if(_stricmp(json_value.substr(index,5).c_str(),"false")==0)
	{
		pe->value.type = JsonElement::BOOLEAN;
		pe->value.b = false;
		index += 5;
		return true;
	}
	else if(_stricmp(json_value.substr(index,4).c_str(),"true")==0)
	{
		pe->value.type = JsonElement::BOOLEAN;
		pe->value.b = true;
		index += 4;
		return true;
	}
	else
	{
		return false;
	}
}

bool JsonParser::dealwith_num_part(JsonElement* pe)
{
	const char* pnums = "0123456789.";
	int i=index;
	while(strchr(pnums,json_value.at(i))!=NULL) i++;
	if(i==index)
	{
		return false;
	}
	double f = atof(json_value.substr(index,i-index).c_str());
	pe->value.type = JsonElement::NUMBER;
	pe->value.n = f;
	index = i;
	return true;
}

bool JsonParser::dealwith_string_part(JsonElement* pe)
{
	if(json_value.at(index)!='"')
	{
		return false;
	}
	index++;

	int str_len=0;
	while(index < json_len)
	{
		if(json_value[index+str_len]=='"' && json_value[index+str_len-1]!='\\')
			break;
		str_len++;
	}

	if(str_len==0)
	{
		pe->value.type = JsonElement::STRING;
		pe->value.s = "";
		return true;
	}

	pe->value.type = JsonElement::STRING;
	pe->value.s = json_value.substr(index,str_len);
	index += (str_len+1);
	return true;

}

bool JsonParser::dealwith_ele_part(JsonElement* pe)
{
	if(json_value.at(index)!='{')
	{
		return false;
	}
	index++;
	while(json_value.at(index)!='}')
	{
		JsonElement *pe2 = new JsonElement;
		dealwith_name_part(pe2);
		if(json_value.at(index)!=':')
		{
			throw_format_error();
			return false;
		}
		index++;
		bool b = dealwith_bool_part(pe2) || dealwith_num_part(pe2) || dealwith_string_part(pe2) ||dealwith_ele_part(pe2) || dealwith_array_part(pe2);
		if(b==false)
		{
			throw_format_error();
			return false;
		}
		pe->add_child_jelement(pe2);
		if(json_value.at(index)!=',')
			break;
		index++;
	}
	index++;
	return true;
}

bool JsonParser::dealwith_array_part(JsonElement* pe)
{
	if(json_value.at(index)!='[')
	{
		return false;
	}
	index++;
	while(json_value.at(index)!=']')
	{
		JsonElement* pe2 = new JsonElement(NULL);
		bool b = dealwith_bool_part(pe2) || dealwith_num_part(pe2) || dealwith_string_part(pe2)  || dealwith_ele_part(pe2) || dealwith_array_part(pe2);
		if(b == false)
		{
			throw_format_error();
			return false;
		}
		pe->add_child_jelement(pe2);
		if(json_value.at(index)!=',')
			break;
		index++;
	}
	index++;
	return true;
}

//检查基本的括号/引号匹配，消除非字符串空格
std::string JsonParser::dealwith_json(const std::string &str_json)
{
	unsigned int pos_src=0,pos_dst=0;
	bool in_string=false;
	char stack[10]={0};
	unsigned int stack_index = 0;
	const char* white_chars=" \t\n\v";
	const char* special_chars="\\~`!@#$%^&*()_-+=';|<>?/";
	std::string str_tmp(str_json.length(),0);

	if(str_json[0]=='\\') return "";

	while(pos_src<str_json.length())
	{
		if(in_string)
		{
			if(str_json[pos_src-1]!='\\' && str_json[pos_src]=='"')
				in_string=false;
			str_tmp[pos_dst++] = str_json[pos_src++];
			continue;
		}
		else
		{
			if(strchr(special_chars,str_json[pos_src]))
				return "";
			if(strchr(white_chars,str_json[pos_src]))
			{
				pos_src++;
				continue;
			}
			if(str_json[pos_src]=='[')
			{
				stack[stack_index++] = ']';
				if(stack_index >= 10)
					return "";
			}
			if(str_json[pos_src]=='{')
			{
				stack[stack_index++] = '}';
				if(stack_index >= 10)
					return "";
			}
			if(str_json[pos_src]==']' || str_json[pos_src]=='}')
			{
				stack_index--;
				if(stack_index<0)
					return "";
				if(stack[stack_index] != str_json[pos_src])
					return "";
			}
			if(str_json[pos_src]=='"')
				in_string = true;
			str_tmp[pos_dst++] = str_json[pos_src++];
			continue;
		}
	}
	str_tmp.resize(str_tmp.length());
	return str_tmp;
}

JsonElement * JsonParser::new_jelement_from_json(std::string str_json)
{
	index = 0;
	json_value=dealwith_json(str_json);
	json_len = json_value.length();
	if(json_len<2)
		throw_format_error();

	JsonElement * pe = new JsonElement;
	try
	{
		pe->set_name("");
		dealwith_ele_part(pe);
		return pe;
	}
	catch(std::out_of_range &e)
	{
		char buf[5]={0};
		_itoa_s(index,buf,10);
		std::string str_err = "json format error near position ";
		str_err += buf;
		str_err += " : ";
		str_err += e.what();
		throw JsonError(JsonError::JSON_FORMAT_ERROR,str_err.c_str());
		return NULL;
	}
}

} //namespace JsonHelper