#include "jsonhelper.h"
#include <iostream>
#include <sstream>
#include <stdexcept>


namespace JsonHelper {

	std::string JsonElement::last_error="";

//JsonElement::JsonElement(const char* k)
//{
//	if(k)
//	{
//		name = k;
//		hasname = true;
//	}
//	else
//	{
//		name = "";
//		hasname = false;
//	}
//	element_value.type = ELEMENT;
//	element_value.e = NULL;
//	next = this;
//	prev = this;
//	parent = NULL;
//}

JsonElement::JsonElement(const char* k, JsonElement* v)
{
	if(k)
	{
		element_name = k;
		hasname = true;
	}
	else
	{
		element_name = "";
		hasname = false;
	}
	element_value.type = ELEMENT;
	element_value.e = v;
	next = this;
	prev = this;
	parent = NULL;
	ref_count = 0;
}

JsonElement::JsonElement(const char* k, double v)
{
	if(k)
	{
		element_name = k;
		hasname = true;
	}
	else
	{
		element_name = "";
		hasname = false;
	}
	element_value.type = NUMBER;
	element_value.n	 = v;
	next = this;
	prev = this;
	parent = NULL;
	ref_count = 0;
}

JsonElement::JsonElement(const char* k, const char* v)
{
	if(k)
	{
		element_name = k;
		hasname =true;
	}
	else
	{
		element_name = "";
		hasname = false;
	}
	
	element_value.type = STRING;
	element_value.s = v;
	next = this;
	prev = this;
	parent = NULL;
	ref_count = 0;
}

JsonElement::JsonElement(const char* k, bool v)
{
	if(k)
	{
		element_name = k;
		hasname = true;
	}
	else
	{
		element_name = "";
		hasname = false;
	}
	element_value.type = BOOLEAN;
	element_value.b = v;
	next = this;
	prev = this;
	parent = NULL;
	ref_count = 0;
}

JsonElement::JsonElement(const char* k, int v)
{
	if(k)
	{
		element_name = k;
		hasname = true;
	}
	else
	{
		element_name = "";
		hasname = false;
	}
	element_value.type = NUMBER;
	element_value.n	 = v;
	next = this;
	prev = this;
	parent = NULL;
	ref_count = 0;
}

JsonElement::~JsonElement()
{
	detach();
	free_children();
}

void JsonElement::free_children()
{
	if(element_value.type != ELEMENT)
		return;

	while(element_value.e)
		delete element_value.e;
}

void JsonElement::throw_error(int err_num,const char* err_msg)
{
	if(err_msg && strlen(err_msg)>0)
		last_error = err_msg;
	else
		last_error = "unknown error";

#ifdef THROW_JSON_ERROR
	throw JsonError(err_num,err_msg);
#endif
}

bool JsonElement::set_name(const char* n)
{
	if(n!=NULL && hasname)
	{
		element_name = n;
		return true;
	}
	else if(n==NULL)
	{
		throw_error(JsonError::PARAM_NULL,"param is null");	
		return false;
	}
	else
	{
		throw_error(JsonError::SETNAME_FOR_NONAME_ELE,"set name for an unnamed element");
		return false;
	}
}

void JsonElement::set_value( bool b )
{
	if(element_value.type == ELEMENT)
	{
		while(element_value.e)
		{
			delete element_value.e;
		}
	}
	element_value.b = b;
	element_value.n = 0;
	element_value.s = "";
	element_value.type = BOOLEAN;
}

void JsonElement::set_value( int i )
{
	if(element_value.type == ELEMENT)
	{
		while(element_value.e)
		{
			delete element_value.e;
		}
	}
	element_value.s = "";
	element_value.b = false;
	element_value.n = i;
	element_value.type = NUMBER;
}

void JsonElement::set_value( double d )
{
	if(element_value.type == ELEMENT)
	{
		while(element_value.e)
		{
			delete element_value.e;
		}
	}
	element_value.s = "";
	element_value.b = false;
	element_value.n = d;
	element_value.type = NUMBER;
}

void JsonElement::set_value( JsonElement* e )
{
	if(element_value.type == ELEMENT)
	{
		while(element_value.e)
		{
			delete element_value.e;
		}
	}
	e->parent = this;
	element_value.e = e;
	element_value.b = false;
	element_value.n = 0;
	element_value.s = "";
	element_value.type = BOOLEAN;
}

void JsonElement::set_value( const char* s )
{
	if(element_value.type == ELEMENT)
	{
		if(element_value.e)
		{
			delete element_value.e;
			element_value.e = NULL;
		}
	}
	element_value.b = false;
	element_value.n = 0;
	element_value.s = s;
	element_value.type = STRING;
}

//一个子节点必须被分离出来之后，才能手动删除
void JsonElement::detach()
{
	if(this->next == this)	//没有兄弟节点
	{
		if(parent)
			this->parent->element_value.e = NULL;
	}
	else
	{
		if(parent && parent->element_value.e==this)
			parent->element_value.e = this->next;
		this->prev->next = this->next;
		this->next->prev = this->prev;
	}
	this->parent = NULL;
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
	while(element_value.e)
		delete element_value.e;
}

bool JsonElement::check_before_add_sibling(JsonElement * e)
{
	if(e==NULL)
	{
		throw_error(JsonError::PARAM_NULL,"param is null");	
		return false;
	}
	if(e->parent!=NULL || e->next!=e)
	{
		throw_error(JsonError::UNINDEPENDENT_ELE_UNDER_ELE,"push not independent child jelement in element");	
		return false;
	}
	if(this->hasname)
	{
		if(e->hasname == false)
		{
			throw_error(JsonError::NONAME_ELE_AFTER_ELE,"add noname element after a named element");
			return false;
		}
	}
	else
	{
		if(e->hasname)
		{
			throw_error(JsonError::ELE_AFTER_NONAME_ELE,"add named element after a noname element");
			return false;
		}
	}
	return true;
}

//只有当前键值对是ELEMENT类型时，才允许增加
JsonElement * JsonElement::set_child_jelement(JsonElement * e)
{
	if(e==NULL)
	{
		throw_error(JsonError::PARAM_NULL,"param is null");	
		return NULL;
	}
	if(e->parent!=NULL || e->next!=e)
	{
		throw_error(JsonError::UNINDEPENDENT_ELE_UNDER_ELE,"push not independent child jelement in element");	
		return NULL;
	}
	if(element_value.type != ELEMENT)
	{
		char * err_msg = NULL;
		if(element_value.type == BOOLEAN)
			err_msg = "push child jelement in boolean element";
		else if(element_value.type == NUMBER)
			err_msg = "push child jelement in number element";
		else if(element_value.type == STRING)
			err_msg = "push child jelement in string element";
		throw_error(JsonError::JELEMENT_UNDER_NON_ELEMENT,err_msg);
		return NULL;
	}
	if(this->element_value.e != NULL)
	{
		throw_error(JsonError::JELEMENT_UNDER_NOTBLANK_ELEMENT,"push child jelement in not blank element");	
		return NULL;
	}
	if(e->parent!=NULL || e->next!=e)
	{
		throw_error(JsonError::UNINDEPENDENT_ELE_UNDER_ELE,"push not independent child jelement in element");	
		return NULL;
	}
	e->parent = this;
	this->element_value.e = e;
	return e;
}

bool JsonElement::check_before_add_child(JsonElement * e)
{
	if(e==NULL)
	{
		throw_error(JsonError::PARAM_NULL,"param is null");	
		return false;
	}
	if(e->parent!=NULL || e->next!=e)
	{
		throw_error(JsonError::UNINDEPENDENT_ELE_UNDER_ELE,"push not independent child jelement in element");	
		return false;
	}
	return true;
}

//成功返回子节点，失败返回本节点
JsonElement * JsonElement::add_child_last(JsonElement * e)
{
	if(!check_before_add_child(e))
		return NULL;
	if(this->element_value.e == NULL)
	{
		return set_child_jelement(e);
	}
	else
	{
		JsonElement * pe = this->element_value.e;
		e->prev = pe->prev;
		e->next = pe;
		pe->prev = e;
		e->prev->next = e;
		e->parent = pe->parent;
		return e;
	}
}

//成功返回子节点，失败返回本节点
JsonElement * JsonElement::add_child_first(JsonElement * e)
{
	JsonElement * pe = add_child_last(e);
	pe->parent->element_value.e = pe;
	return e;
}

JsonElement * JsonElement::add_sibling_before(JsonElement *e)
{
	if(!check_before_add_sibling(e))
		return NULL;
	prev->next = e;
	e->next = this;
	e->prev = prev;
	prev = e;
	e->parent = parent;
	return e;
}

JsonElement * JsonElement::add_sibling_after(JsonElement *e)
{
	if(!check_before_add_sibling(e))
		return NULL;
	next->prev = e;
	e->next = next;
	e->prev = this;
	next = e;
	e->parent = parent;
	return e;
}

JsonElement * JsonElement::add_sibling_first(JsonElement *e)
{
	if(!check_before_add_sibling(e))
		return NULL;
	if(parent)
	{
		JsonElement * pfirst = parent->element_value.e;	
		e->prev = pfirst->prev;
		e->next = pfirst;
		e->prev->next = e;
		pfirst->prev = e;
		parent->element_value.e = e;
		e->parent = parent;
		return e;
	}
	else
	{
		return add_sibling_before(e);
	}
}

JsonElement * JsonElement::add_sibling_last(JsonElement *e)
{
	if(!check_before_add_sibling(e))
		return NULL;
	if(parent)
	{
		JsonElement * plast = parent->element_value.e->prev;
		e->prev = plast;
		e->next = plast->next;
		plast->next = e;
		e->next->prev = e;
		e->parent = parent;
		return e;
	}
	else
	{
		return add_sibling_after(e);
	}
}

JsonElement * JsonElement::get_sibling_first()
{
	if(parent)
		return parent->element_value.e;
	else
		return this;
}

JsonElement * JsonElement::get_sibling_at(int index)
{
	unsigned short count = get_sibling_count();

	if(index >= count || index < -count)
	{
		throw_error(JsonError::OUT_OF_RANGE,"get sibling out of range");
		return NULL;
	}


	JsonElement * p = get_sibling_first();

	if(index >= 0)
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

JsonElement * JsonElement::get_sibling_last()
{
	if(parent)
		return parent->element_value.e->prev;
	else
		return this;
}

JsonElement * JsonElement::get_root_element()
{
	JsonElement * p = parent;
	if(p == NULL)
		return this;
	while(p->parent)
		p = p->parent;
	return p;
}

JsonElement * JsonElement::get_child_last()
{
	JsonElement * p = element_value.e;
	if(p==NULL)
	{
		throw_error(JsonError::NO_CHILD,"no child");
		return NULL;
	}
	return p->prev;
}

JsonElement * JsonElement::get_child_at( int index )
{
	unsigned short count = get_children_count();
	if(count == 0)
	{
		throw_error(JsonError::NO_CHILD,"no child");
		return NULL;
	}

	if(index >= count || index < -count)
	{
		throw_error(JsonError::OUT_OF_RANGE,"get child out of range");
		return NULL;
	}

	
	JsonElement * p = element_value.e;

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

JsonHelper::JsonElement * JsonElement::get_element_bypath(const char* path)
{
	return get_element_bypath(get_root_element(),path);
}

JsonHelper::JsonElement * JsonElement::get_element_bypath(JsonElement* parent, const char* path)
{
	if(parent==NULL || path==NULL || strlen(path)==0 || path[0]!='/')
		return NULL;
	
	std::string name;
	JsonElement* first = parent->get_child_first();
	JsonElement* child = first;

	while(child)
	{
		name = child->get_name();
		if(name.empty()==false)
		{
			if(strncmp(name.c_str(),path+1,name.length())==0)
			{
				const char* tmp = strchr(path+1,'/');
				if(tmp) //如果后面还有路径
					return get_element_bypath(child,tmp);
				else   //path到头了
					return child;
			}
			else
			{
				child = child->get_sibling_next();
				if(child == first)  //已经查询到最后一个节点
				{
					return NULL;
				}
			}
		}
		else
		{
			if(path[1]!='[')
				return NULL; //碰到了无名节点
			else
			{
				int num=0,index=2,len=strlen(path);
				for(;index<len;index++)
				{
					char c = path[index];
					if(c>='0' && c<='9')
						num = num*10+c-'0';
					else if(c==']')
						break;
					else  //碰到了错误的符号
						return NULL;
				}
				child = parent->get_child_at(num);
				return get_element_bypath(child,path+index+1);
			}
		}
	}
	return NULL;
}

unsigned short JsonElement::get_children_count()
{
	if(element_value.e)
	{
		unsigned short count =1;
		JsonElement * p = element_value.e;
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

unsigned short JsonElement::get_sibling_count()
{
	unsigned short count=1;
	JsonElement *pnext = next;
	while(pnext != this)
	{
		++count;
		pnext = pnext->next;
	}
	return count;
}

bool JsonElement::get_node_value(std::string & str_value,bool formated,int depth)
{
	std::stringstream stm_tmp;
	JsonElement * pele = this;

	if(formated)
	{
		depth++;
	}

	if(pele)
	{
		if(pele->element_value.type == BOOLEAN)
		{
			if(element_value.b)
				stm_tmp << "true" ;
			else
				stm_tmp << "false" ;
		}
		else if(pele->element_value.type == NUMBER)
		{
			stm_tmp << element_value.n ;
		}
		else if(pele->element_value.type == STRING)
		{
			stm_tmp << "\"" << element_value.s << "\"" ;
		}
		else if(pele->element_value.type == ELEMENT)
		{
			JsonElement * pe = pele->element_value.e;
			if(pe == NULL)
			{
				str_value = "{ }";
				last_error = "try to show an element with no value";
				//throw_error(JsonError::NULL_VALUE_ELEMENT,"try to show an element with no value");
				return false;
			}
			
			if(pe->hasname) stm_tmp << "{";
			else stm_tmp << "[";
			if(formated) stm_tmp << "\n";

			JsonElement * phead = pe;
			do
			{
				std::string str_tmp;
				for(int i=0;i<depth;i++) stm_tmp << "    ";
				if(pe->hasname)
					stm_tmp << "\"" << pe->element_name << "\":";
				pe->get_node_value(str_tmp,formated,depth);
				stm_tmp  << str_tmp;
				if(pe->next != phead)
					stm_tmp << ",";
				if(formated) stm_tmp << "\n";
				pe = pe->next;
			}while(pe != pele->element_value.e);

			pe = pele->element_value.e;
			for(int i=0;i<depth-1;i++) stm_tmp << "    ";
			if(pe->hasname) stm_tmp << "}";
			else stm_tmp << "]";
		}
	}
	str_value = stm_tmp.str();
	return true;
}

std::string JsonElement::get_json(bool formated)
{
	if(element_value.type != ELEMENT)
	{
		throw_error(JsonError::FORMAT_NOT_ELEMENT,"type isnot ELEMENT,cannot be formated");
		return "";
	}

	int depth = 0;
	std::string json_string;
	get_node_value(json_string,formated,depth);
	return json_string;
}

JsonElementPtr JsonElement::new_jelement_from_json(const std::string & str_json)
{
	JsonParser parser;
	return parser.new_jelement_from_json(str_json);
}

void JsonParser::throw_format_error()
{
	JsonElement::throw_error(JsonError::JSON_FORMAT_ERROR,"counted format error when parse json");
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
		pe->element_value.type = JsonElement::BOOLEAN;
		pe->element_value.b = false;
		index += 5;
		return true;
	}
	else if(_stricmp(json_value.substr(index,4).c_str(),"true")==0)
	{
		pe->element_value.type = JsonElement::BOOLEAN;
		pe->element_value.b = true;
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
	pe->element_value.type = JsonElement::NUMBER;
	pe->element_value.n = f;
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
		pe->element_value.type = JsonElement::STRING;
		pe->element_value.s = "";
		return true;
	}

	pe->element_value.type = JsonElement::STRING;
	pe->element_value.s = json_value.substr(index,str_len);
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
		pe->add_child_last(pe2);
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
		pe->add_child_last(pe2);
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

JsonElementPtr JsonParser::new_jelement_from_json(std::string str_json)
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
		return JsonElementPtr(pe);
	}
	catch(std::out_of_range &e)
	{
		char buf[5]={0};
		_itoa_s(index,buf,10);
		std::string str_err = "json format error near position ";
		str_err += buf;
		str_err += " : ";
		str_err += e.what();
		JsonElement::throw_error(JsonError::JSON_FORMAT_ERROR,str_err.c_str());
		return JsonElementPtr(NULL);
	}
}

} //namespace JsonHelper