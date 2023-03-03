#include <stdio.h>
#include <stdlib.h>
#include "jsonhelper.h"
#include "utils.h"
#include <Windows.h>

using namespace JsonHelper;

void test_make_json();
void test_make_json2();
void test_parse_json();
void test_add_child();
void test_del_child();
void test_del_child2();
void test_change_child();

int main()
{
	_CrtMemState s1,s2,s3;
	_CrtMemCheckpoint(&s1);
	puts("----------------------test_make_json----------------------");
	test_make_json();
	puts("----------------------test_make_json2----------------------");
	test_make_json2();
	puts("----------------------test_parse_json----------------------");
	test_parse_json();
	puts("----------------------test_del_child----------------------");
	test_del_child();
	puts("----------------------test_add_child----------------------");
	test_add_child();
	puts("----------------------test_change_child----------------------");
	test_change_child();
	puts("----------------------test_del_child2----------------------");
	test_del_child2();
	puts("--------------------------------------------");

	_CrtMemCheckpoint(&s2);
	if(_CrtMemDifference(&s3,&s1,&s2))
	{
		_CrtMemDumpStatistics(&s3);
		puts("********************内存泄漏********************");
	}
	else
		puts("no mem leak");

	system("pause");
	return 0;
}

//创建节点、添加节点、转为字符串
void test_make_json()
{
	JsonElement *pe;
	try
	{
		pe = new JsonElement;	//等价于 new JsonElement("",(JsonElement*)0);
		pe->add_child_jelement(new JsonElement("name1",true));
		pe->add_child_jelement(new JsonElement("name2",3));
		JsonElement *p2 = new JsonElement("name3");
		p2->add_child_jelement(new JsonElement("name4","string"));
		p2->add_child_jelement(new JsonElement("name4","string2")); //当值为STRING类型时，不能直接传字符串，否则会认定为布尔类型
		p2->add_child_jelement(new JsonElement("name5",false));
		pe->add_child_jelement(p2);

		std::string str_json = pe->get_json(true);
		puts(str_json.c_str());
		delete pe;
	}
	catch (JsonError e)
	{
		puts(e.what().c_str());
	}
	catch (...)
	{
		puts("unknown error");
	}
}

//测试将节点转换为字符串
void test_make_json2()
{
	JsonElement * pe;
	try
	{
		pe = new JsonElement("test");
		pe->add_child_jelement(new JsonElement("c0",0));
		pe->add_child_jelement(new JsonElement("c1",1));
		pe->add_child_jelement(new JsonElement("c2",(JsonElement*)0));	//等价于 pe->add_child_jelement(new JsonElement("c2"));
		pe->add_child_jelement(new JsonElement("c3",(JsonElement*)0));	//当值为ELEMENT类型时，不能直接传NULL，否则会认定为NUMBER类型
		pe->add_child_jelement(new JsonElement("c4"));
		pe->add_child_jelement(new JsonElement("c5"));
		pe->add_child_jelement(new JsonElement("c6","6"));
		pe->get_child_at(2)->add_child_jelement(new JsonElement("c20",20));
		pe->get_child_at(2)->add_child_jelement(new JsonElement("c21",21));
		pe->get_child_at(2)->add_child_jelement(new JsonElement("c22",22));
		pe->get_child_at(3)->add_child_jelement(new JsonElement("c30","30"));
		pe->get_child_at(3)->add_child_jelement(new JsonElement("c31","31"));
		pe->get_child_at(3)->add_child_jelement(new JsonElement("c32","32"));
		pe->get_child_at(4)->add_child_jelement(new JsonElement(NULL,"40"));
		pe->get_child_at(4)->add_child_jelement(new JsonElement(NULL,41));
		pe->get_child_at(4)->add_child_jelement(new JsonElement(NULL,false));
		JsonElement * ptmp;
		ptmp = pe->get_child_at(5)->add_child_jelement(new JsonElement(NULL));
		ptmp->add_child_jelement(new JsonElement("c500",500));
		ptmp->add_child_jelement(new JsonElement("c501",501));
		ptmp->add_child_jelement(new JsonElement("c502",502));
		ptmp = pe->get_child_at(5)->add_child_jelement(new JsonElement(NULL));
		ptmp->add_child_jelement(new JsonElement("c510",510));
		ptmp->add_child_jelement(new JsonElement("c511",511));
		ptmp->add_child_jelement(new JsonElement("c512",512));
		ptmp = pe->get_child_at(5)->add_child_jelement(new JsonElement(NULL));
		ptmp->add_child_jelement(new JsonElement("c520",520));
		ptmp->add_child_jelement(new JsonElement("c521",521));
		ptmp->add_child_jelement(new JsonElement("c522",522));
		ptmp = pe->get_child_at(5)->add_child_jelement(new JsonElement(NULL));
		ptmp->add_child_jelement(new JsonElement("c530",530));
		ptmp->add_child_jelement(new JsonElement("c531",531));
		ptmp->add_child_jelement(new JsonElement("c532",532));
		std::string s = pe->get_json(true);
		puts(s.c_str());
		delete pe;
	}
	catch (JsonError e)
	{
		puts(e.what().c_str());
	}
	catch (...)
	{
		puts("unknown error");
	}
}

//将字符串转换为节点
void test_parse_json()
{
	char * pjson = "{\
					   \"sites\": {\
						   \"site\": [\
							   {\
								   \"id\": \"1\",\
								   \"name\": \"百度\",\
								   \"url\": \"www.baidu.com\"\
							   },\
							   {\
								   \"id\": \"2\",\
								   \"name\": \"好123\",\
								   \"url\": \"www.hao123\"\
							   },\
							   {\
								   \"id\": \"3\",\
								   \"name\": \"谷歌\",\
								   \"ur l\": \"www.google.com\"\
							   }\
						   ]\
					   }\
				   }";
	try
	{
		DWORD t1,t2,t3,t4;
		JsonElement * pe;
		std::string str_json;

		t1 = GetTickCount();
		for(int i=0;i<1000;i++)								//耗时约100ms						
		{	
			pe = JsonElement::new_jelement_from_json(pjson);
			delete pe;
		}
		t2 = GetTickCount();
		pe = JsonElement::new_jelement_from_json(pjson);	
		t3 = GetTickCount();
		for(int i=0;i<1000;i++)								//耗时约200ms	
		{
			str_json = pe->get_json(true);					
		}
		t4 = GetTickCount();

		puts(str_json.c_str());
		printf("1000次new_jelement_from_json耗时%dms,1000次get_json耗时%dms\n",t2-t1,t4-t3);
		delete pe;
	}
	catch(JsonError &e)
	{
		puts(e.what().c_str());
	}
}

//添加子节点
void test_add_child()
{
	char * pjson = "{\
				   \"sites\": {\
				   \"site\": [\
				   {\
				   \"id\": \"1\",\
				   \"name\": \"百度\",\
				   \"url\": \"www.baidu.com\"\
				   },\
				   {\
				   \"id\": \"2\",\
				   \"name\": \"好123\",\
				   \"url\": \"www.hao123\"\
				   },\
				   {\
				   \"id\": \"3\",\
				   \"name\": \"谷歌\",\
				   \"ur l\": \"www.google.com\"\
				   }\
				   ]\
				   }\
				   }";
	try
	{
		JsonElement* pe = JsonElement::new_jelement_from_json(pjson);	

		std::string str_json;
		puts("-------------------------根节点为----------------------------");
		str_json = pe->get_json(true);						
		puts(str_json.c_str());
		puts("----------------------一级子节点为--------------------------");
		str_json = pe->get_first_child()->get_json(true);						
		puts(str_json.c_str());
		puts("----------------------二级子节点为--------------------------");
		str_json = pe->get_first_child()->get_first_child()->get_json(true);						
		puts(str_json.c_str());
		puts("----------------------三级子节点为--------------------------");
		str_json = pe->get_first_child()->get_first_child()->get_first_child()->get_json(true);						
		puts(str_json.c_str());
		puts("----------------为三级子节点添加兄弟节点-------------------");
		JsonElement * psub = new JsonElement(NULL);
		psub->add_child_jelement(new JsonElement("aaa",true));
		psub->add_child_jelement(new JsonElement("bbb","this is a string"));
		psub->add_child_jelement(new JsonElement("ccc",123.3));
		pe->get_first_child()->get_first_child()->get_first_child()->pushback_jelement(psub);
		str_json = pe->get_json(true);						
		puts(str_json.c_str());
		delete pe;
	}
	catch(JsonError &e)
	{
		puts(e.what().c_str());
	}
}

//删除子节点
void test_del_child()
{
	char * pjson = "{\
				   \"sites\": {\
				   \"site\": [\
				   {\
				   \"id\": \"1\",\
				   \"name\": \"百度\",\
				   \"url\": \"www.baidu.com\"\
				   },\
				   {\
				   \"id\": \"2\",\
				   \"name\": \"好123\",\
				   \"url\": \"www.hao123\"\
				   },\
				   {\
				   \"id\": \"3\",\
				   \"name\": \"谷歌\",\
				   \"ur l\": \"www.google.com\"\
				   }\
				   ]\
				   }\
				   }";
	try
	{
		JsonElement* pe = JsonElement::new_jelement_from_json(pjson);	

		std::string str_json;
		str_json = pe->get_json(true);						
		puts(str_json.c_str());
		puts("-------------------------------------------------------------");
		JsonElement * ptmp  = pe->get_first_child()->get_first_child()->get_first_child();
		delete ptmp;
		str_json = pe->get_json(true);						
		puts(str_json.c_str());
		delete pe;
	}
	catch(JsonError &e)
	{
		puts(e.what().c_str());
	}
}

//读写子节点数据
void test_change_child()
{
	char * pjson = "{\
				   \"sites\": {\
				   \"site\": [\
				   {\
				   \"id\": \"1\",\
				   \"name\": \"百度\",\
				   \"url\": \"www.baidu.com\"\
				   },\
				   {\
				   \"id\": \"2\",\
				   \"name\": \"好123\",\
				   \"url\": \"www.hao123\"\
				   },\
				   {\
				   \"id\": \"3\",\
				   \"name\": \"谷歌\",\
				   \"ur l\": \"www.google.com\"\
				   }\
				   ]\
				   }\
				   }";
	try
	{
		JsonElement* pe = JsonElement::new_jelement_from_json(pjson);	

		puts("---------------------原始数据----------------------");
		std::string str_json;
		str_json = pe->get_json(true);						
		puts(str_json.c_str());
		puts("-----------------将\"百度\"修改为\"百度首页\"----------------------");
		JsonElement * ptmp  = pe->get_first_child()->get_first_child()->get_first_child()->get_child_at(1);
		if(ptmp->get_name() == "name")
		{
			if(ptmp->get_value_type() == JsonElement::STRING) //或 if(v.type == JsonElement::STRING)
			{
				std::string s = ptmp->get_value_string();
				printf("读到的元素的内容为：\"%s\"，将其修改为\"百度首页\"\n",s.c_str());
				s = "百度首页";
				ptmp->set_value_string(s);
			}
		}
		str_json = pe->get_json(true);						
		puts(str_json.c_str());
		delete pe;
	}
	catch(JsonError &e)
	{
		puts(e.what().c_str());
	}
}

void test_del_child2()
{
	try
	{
		JsonElement * pe = new JsonElement;
		pe->add_child_jelement(new JsonElement("a0","a0"));
		pe->add_child_jelement(new JsonElement("a1","a1"));
		pe->add_child_jelement(new JsonElement("a2","a2"));
		pe->add_child_jelement(new JsonElement("a3","a3"));
		pe->add_child_jelement(new JsonElement("a4","a4"));
		pe->add_child_jelement(new JsonElement("a5","a5"));
		pe->add_child_jelement(new JsonElement("a6","a6"));
		pe->add_child_jelement(new JsonElement("a7","a7"));
		pe->add_child_jelement(new JsonElement("a8","a8"));
		pe->remove_child(-2);
		std::string sjson = pe->get_json(true);
		puts(sjson.c_str());
		pe->remove_child(3);
		sjson = pe->get_json(true);
		puts(sjson.c_str());
		pe->remove_all_children();
		pe->add_child_jelement(new JsonElement("b","b"));
		sjson = pe->get_json(true);
		puts(sjson.c_str());
		delete pe;
	}
	catch(JsonError &e)
	{
		puts(e.what().c_str());
	}
}
