#include <stdio.h>
#include <stdlib.h>
#include "jsonhelper.h"
#include "utils.h"
#include <Windows.h>

using namespace JsonHelper;

void test_make_json();
void test_make_json2();
void test_make_json3();
void test_make_json4();
void test_parse_json();
void test_add_child();
void test_del_child();
void test_del_child2();
void test_change_child();

int main()
{
	_CrtMemState s1,s2,s3;
	_CrtMemCheckpoint(&s1);
	puts("----------------------test_make_json4----------------------");
	test_make_json4();
	_CrtMemCheckpoint(&s2);
	if(_CrtMemDifference(&s3,&s1,&s2))
	{
		_CrtMemDumpStatistics(&s3);
		puts("********************�ڴ�й© 1********************");
		getchar();
	}
	else
		puts("no mem leak");
	puts("----------------------test_make_json----------------------");
	test_make_json();
	_CrtMemCheckpoint(&s2);
	if(_CrtMemDifference(&s3,&s1,&s2))
	{
		_CrtMemDumpStatistics(&s3);
		puts("********************�ڴ�й© 2********************");
		getchar();
	}
	else
		puts("no mem leak");
	puts("----------------------test_make_json2----------------------");
	test_make_json2();
	_CrtMemCheckpoint(&s2);
	if(_CrtMemDifference(&s3,&s1,&s2))
	{
		_CrtMemDumpStatistics(&s3);
		puts("********************�ڴ�й© 3********************");
		getchar();
	}
	else
		puts("no mem leak");
	puts("----------------------test_parse_json----------------------");
	test_parse_json();
	_CrtMemCheckpoint(&s2);
	if(_CrtMemDifference(&s3,&s1,&s2))
	{
		_CrtMemDumpStatistics(&s3);
		puts("********************�ڴ�й© 4********************");
		getchar();
	}
	else
		puts("no mem leak");
	puts("----------------------test_del_child----------------------");
	test_del_child();
	_CrtMemCheckpoint(&s2);
	if(_CrtMemDifference(&s3,&s1,&s2))
	{
		_CrtMemDumpStatistics(&s3);
		puts("********************�ڴ�й© 5********************");
		getchar();
	}
	else
		puts("no mem leak");
	puts("----------------------test_add_child----------------------");
	test_add_child();
	_CrtMemCheckpoint(&s2);
	if(_CrtMemDifference(&s3,&s1,&s2))
	{
		_CrtMemDumpStatistics(&s3);
		puts("********************�ڴ�й© 6********************");
		getchar();
	}
	else
		puts("no mem leak");
	puts("----------------------test_change_child----------------------");
	test_change_child();
	_CrtMemCheckpoint(&s2);
	if(_CrtMemDifference(&s3,&s1,&s2))
	{
		_CrtMemDumpStatistics(&s3);
		puts("********************�ڴ�й© 7********************");
		getchar();
	}
	else
		puts("no mem leak");
	puts("----------------------test_del_child2----------------------");
	test_del_child2();
	_CrtMemCheckpoint(&s2);
	if(_CrtMemDifference(&s3,&s1,&s2))
	{
		_CrtMemDumpStatistics(&s3);
		puts("********************�ڴ�й© 8********************");
		getchar();
	}
	else
		puts("no mem leak");

	system("pause");
	return 0;
}

//�����ڵ㡢��ӽڵ㡢תΪ�ַ���
void test_make_json()
{
	JsonElementPtr pe;
	try
	{
		pe = JsonElement::MakeElement();	//�ȼ��� JsonElement::MakeElement("",(JsonElementPtr)0);
		pe->add_child_last(JsonElement::MakeElement("name1",true));
		pe->add_child_last(JsonElement::MakeElement("name2",3));
		JsonElementPtr p2 = JsonElement::MakeElement("name3");
		p2->add_child_last(JsonElement::MakeElement("name4","string"));
		p2->add_child_last(JsonElement::MakeElement("name4","string2")); //��ֵΪSTRING����ʱ������ֱ�Ӵ��ַ�����������϶�Ϊ��������
		p2->add_child_last(JsonElement::MakeElement("name5",false));
		pe->add_child_last(p2);

		std::string str_json = pe->get_json(true);
		puts(str_json.c_str());
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

//���Խ��ڵ�ת��Ϊ�ַ���
void test_make_json2()
{
	JsonElementPtr pe;
	try
	{
		pe = JsonElement::MakeElement("test");
		pe->add_child_last(JsonElement::MakeElement("c0",0));
		pe->add_child_last(JsonElement::MakeElement("c1",1));
		pe->add_child_last(JsonElement::MakeElement("c2",(JsonElementPtr)0));	//�ȼ��� pe->add_child_last(JsonElement::MakeElement("c2"));
		pe->add_child_last(JsonElement::MakeElement("c3",(JsonElementPtr)0));	//��ֵΪELEMENT����ʱ������ֱ�Ӵ�NULL��������϶�ΪNUMBER����
		pe->add_child_last(JsonElement::MakeElement("c4"));
		pe->add_child_last(JsonElement::MakeElement("c5"));
		pe->add_child_last(JsonElement::MakeElement("c6","6"));
		pe->get_child_at(2)->add_child_last(JsonElement::MakeElement("c20",20));
		pe->get_child_at(2)->add_child_last(JsonElement::MakeElement("c21",21));
		pe->get_child_at(2)->add_child_last(JsonElement::MakeElement("c22",22));
		pe->get_child_at(3)->add_child_last(JsonElement::MakeElement("c30","30"));
		pe->get_child_at(3)->add_child_last(JsonElement::MakeElement("c31","31"));
		pe->get_child_at(3)->add_child_last(JsonElement::MakeElement("c32","32"));
		pe->get_child_at(4)->add_child_last(JsonElement::MakeElement(NULL,"40"));
		pe->get_child_at(4)->add_child_last(JsonElement::MakeElement(NULL,41));
		pe->get_child_at(4)->add_child_last(JsonElement::MakeElement(NULL,false));
		JsonElementPtr ptmp;
		ptmp = pe->get_child_at(5)->add_child_last(JsonElement::MakeElement(NULL));
		ptmp->add_child_last(JsonElement::MakeElement("c500",500));
		ptmp->add_child_last(JsonElement::MakeElement("c501",501));
		ptmp->add_child_last(JsonElement::MakeElement("c502",502));
		ptmp = pe->get_child_at(5)->add_child_last(JsonElement::MakeElement(NULL));
		ptmp->add_child_last(JsonElement::MakeElement("c510",510));
		ptmp->add_child_last(JsonElement::MakeElement("c511",511));
		ptmp->add_child_last(JsonElement::MakeElement("c512",512));
		ptmp = pe->get_child_at(5)->add_child_last(JsonElement::MakeElement(NULL));
		ptmp->add_child_last(JsonElement::MakeElement("c520",520));
		ptmp->add_child_last(JsonElement::MakeElement("c521",521));
		ptmp->add_child_last(JsonElement::MakeElement("c522",522));
		ptmp = pe->get_child_at(5)->add_child_last(JsonElement::MakeElement(NULL));
		ptmp->add_child_last(JsonElement::MakeElement("c530",530));
		ptmp->add_child_last(JsonElement::MakeElement("c531",531));
		ptmp->add_child_last(JsonElement::MakeElement("c532",532));
		std::string s = pe->get_json(true);
		puts(s.c_str());
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

//���ַ���ת��Ϊ�ڵ�
void test_parse_json()
{
	char * pjson = "{\
					   \"sites\": {\
						   \"site\": [\
							   {\
								   \"id\": \"1\",\
								   \"name\": \"�ٶ�\",\
								   \"url\": \"www.baidu.com\"\
							   },\
							   {\
								   \"id\": \"2\",\
								   \"name\": \"��123\",\
								   \"url\": \"www.hao123\"\
							   },\
							   {\
								   \"id\": \"3\",\
								   \"name\": \"�ȸ�\",\
								   \"url\": \"www.google.com\"\
							   }\
						   ]\
					   }\
				   }";
	try
	{
		DWORD t1,t2,t3,t4;
		JsonElementPtr pe;
		std::string str_json;

		t1 = GetTickCount();
		for(int i=0;i<1000;i++)								//��ʱԼ100ms						
		{	
			pe = JsonElement::new_jelement_from_json(pjson);
		}
		t2 = GetTickCount();
		pe = JsonElement::new_jelement_from_json(pjson);	
		t3 = GetTickCount();
		for(int i=0;i<1000;i++)								//��ʱԼ200ms	
		{
			str_json = pe->get_json(true);					
		}
		t4 = GetTickCount();

		puts(str_json.c_str());
		printf("1000��new_jelement_from_json��ʱ%dms,1000��get_json��ʱ%dms\n",t2-t1,t4-t3);
	}
	catch(JsonError &e)
	{
		puts(e.what().c_str());
	}
}

void get_find_child_element()
{
	char * pjson = "{\
				   \"sites\": {\
				   \"site\": [\
				   {\
				   \"id\": \"1\",\
				   \"name\": \"�ٶ�\",\
				   \"url\": \"www.baidu.com\"\
				   },\
				   {\
				   \"id\": \"2\",\
				   \"name\": \"��123\",\
				   \"url\": \"www.hao123\"\
				   },\
				   {\
				   \"id\": \"3\",\
				   \"name\": \"�ȸ�\",\
				   \"url\": \"www.google.com\"\
				   }\
				   ]\
				   }\
				   }";
	JsonElementPtr pe = JsonElement::new_jelement_from_json(pjson);
	JsonElementPtr e = pe->get_element_bypath("/sites/site/[2]/url");
}

//����ӽڵ�
void test_add_child()
{
	char * pjson = "{\
				   \"sites\": {\
				   \"site\": [\
				   {\
				   \"id\": \"1\",\
				   \"name\": \"�ٶ�\",\
				   \"url\": \"www.baidu.com\"\
				   },\
				   {\
				   \"id\": \"2\",\
				   \"name\": \"��123\",\
				   \"url\": \"www.hao123\"\
				   },\
				   {\
				   \"id\": \"3\",\
				   \"name\": \"�ȸ�\",\
				   \"ur l\": \"www.google.com\"\
				   }\
				   ]\
				   }\
				   }";
	try
	{
		JsonElementPtr pe = JsonElement::new_jelement_from_json(pjson);	

		std::string str_json;
		puts("-------���ڵ�Ϊ-----");
		str_json = pe->get_json(true);						
		puts(str_json.c_str());
		puts("-------һ���ӽڵ�Ϊ-----");
		str_json = pe->get_child_first()->get_json(true);						
		puts(str_json.c_str());
		puts("-------�����ӽڵ�Ϊ------");
		str_json = pe->get_child_first()->get_child_first()->get_json(true);						
		puts(str_json.c_str());
		puts("-------�����ӽڵ�Ϊ-------");
		str_json = pe->get_child_first()->get_child_first()->get_child_first()->get_json(true);						
		puts(str_json.c_str());
		puts("-------Ϊ�����ӽڵ�����ֵܽڵ�-------");
		JsonElementPtr psub = JsonElement::MakeElement(NULL);
		psub->add_child_last(JsonElement::MakeElement("aaa",true));
		psub->add_child_last(JsonElement::MakeElement("bbb","this is a string"));
		psub->add_child_last(JsonElement::MakeElement("ccc",123.3));
		pe->get_child_first()->get_child_first()->get_child_first()->add_sibling_after(psub);
		str_json = pe->get_json(true);						
		puts(str_json.c_str());
	}
	catch(JsonError &e)
	{
		puts(e.what().c_str());
	}
}

//ɾ���ӽڵ�
void test_del_child()
{
	char * pjson = "{\
				   \"sites\": {\
				   \"site\": [\
				   {\
				   \"id\": \"1\",\
				   \"name\": \"�ٶ�\",\
				   \"url\": \"www.baidu.com\"\
				   },\
				   {\
				   \"id\": \"2\",\
				   \"name\": \"��123\",\
				   \"url\": \"www.hao123\"\
				   },\
				   {\
				   \"id\": \"3\",\
				   \"name\": \"�ȸ�\",\
				   \"ur l\": \"www.google.com\"\
				   }\
				   ]\
				   }\
				   }";
	try
	{
		JsonElementPtr pe = JsonElement::new_jelement_from_json(pjson);	

		std::string str_json;
		str_json = pe->get_json(true);						
		puts(str_json.c_str());
		puts("-------------------------------------------------------------");
		JsonElementPtr ptmp  = pe->get_child_first()->get_child_first()->get_child_first();
		str_json = pe->get_json(true);						
		puts(str_json.c_str());
	}
	catch(JsonError &e)
	{
		puts(e.what().c_str());
	}
}

//��д�ӽڵ�����
void test_change_child()
{
	char * pjson = "{\
				   \"sites\": {\
				   \"site\": [\
				   {\
				   \"id\": \"1\",\
				   \"name\": \"�ٶ�\",\
				   \"url\": \"www.baidu.com\"\
				   },\
				   {\
				   \"id\": \"2\",\
				   \"name\": \"��123\",\
				   \"url\": \"www.hao123\"\
				   },\
				   {\
				   \"id\": \"3\",\
				   \"name\": \"�ȸ�\",\
				   \"ur l\": \"www.google.com\"\
				   }\
				   ]\
				   }\
				   }";
	try
	{
		JsonElementPtr pe = JsonElement::new_jelement_from_json(pjson);	

		puts("---------------------ԭʼ����----------------------");
		std::string str_json;
		str_json = pe->get_json(true);						
		puts(str_json.c_str());
		puts("-----------------��\"�ٶ�\"�޸�Ϊ\"�ٶ���ҳ\"----------------------");
		JsonElementPtr ptmp  = pe->get_child_first()->get_child_first()->get_child_first()->get_child_at(1);
		if(ptmp->get_name() == "name")
		{
			if(ptmp->get_value_type() == JsonElement::STRING) //�� if(v.type == JsonElement::STRING)
			{
				std::string s = ptmp->get_value_string();
				printf("������Ԫ�ص�����Ϊ��\"%s\"�������޸�Ϊ\"�ٶ���ҳ\"\n",s.c_str());
				s = "�ٶ���ҳ";
				ptmp->set_value(s.c_str());
			}
		}
		str_json = pe->get_json(true);						
		puts(str_json.c_str());
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
		JsonElementPtr pe = JsonElement::MakeElement();
		pe->add_child_last(JsonElement::MakeElement("a0","a0"));
		pe->add_child_last(JsonElement::MakeElement("a1","a1"));
		pe->add_child_last(JsonElement::MakeElement("a2","a2"));
		pe->add_child_last(JsonElement::MakeElement("a3","a3"));
		pe->add_child_last(JsonElement::MakeElement("a4","a4"));
		pe->add_child_last(JsonElement::MakeElement("a5","a5"));
		pe->add_child_last(JsonElement::MakeElement("a6","a6"));
		pe->add_child_last(JsonElement::MakeElement("a7","a7"));
		pe->add_child_last(JsonElement::MakeElement("a8","a8"));
		pe->remove_child(-2);
		std::string sjson = pe->get_json(true);
		puts(sjson.c_str());
		pe->remove_child(3);
		sjson = pe->get_json(true);
		puts(sjson.c_str());
		pe->remove_all_children();
		pe->add_child_last(JsonElement::MakeElement("b","b"));
		sjson = pe->get_json(true);
		puts(sjson.c_str());
	}
	catch(JsonError &e)
	{
		puts(e.what().c_str());
	}
}

void test_make_json3()
{
	try
	{
		JsonElementPtr je = JsonElement::MakeElement();
		je->set_name("ͬ��ΰҵ");
		JsonElementPtr part = je->add_child_last(JsonElement::MakeElement("��֯�ܹ�"));
		je->add_child_last(JsonElement::MakeElement("�ҵĿͻ�"));
		JsonElementPtr leaders = part->add_child_last(JsonElement::MakeElement("��˾�쵼"));
		JsonElementPtr tec = part->add_child_last(JsonElement::MakeElement("������ϵ"));
		JsonElementPtr market = part->add_child_last(JsonElement::MakeElement("�г��ܲ�"));
		JsonElementPtr man = part->add_child_last(JsonElement::MakeElement("������ϵ"));
		JsonElementPtr spec = part->add_child_last(JsonElement::MakeElement("�������"));
		JsonElementPtr branch = part->add_child_last(JsonElement::MakeElement("��֧����"));
		leaders->add_child_last(JsonElement::MakeElement("�ܾ���","������"));
		leaders->add_child_last(JsonElement::MakeElement("������������","���"));
		leaders->add_child_last(JsonElement::MakeElement("����ҽ����ҵ���ܾ���","Ѧ����"));
		leaders->add_child_last(JsonElement::MakeElement("�����ܼ�","�����"));
		leaders->add_child_last(JsonElement::MakeElement("���»�����","������"));
		leaders->add_child_last(JsonElement::MakeElement("���ܾ���","�¼���"));
		leaders->add_child_last(JsonElement::MakeElement("��Ժ��ҵ���ܾ���","������"));
		tec->add_child_last(JsonElement::MakeElement("���뼼������"));
		JsonElementPtr p = tec->add_child_last(JsonElement::MakeElement("����Ӧ����ҵ��"));
		p->add_child_last(JsonElement::MakeElement("����","����"));
		p->add_child_last(JsonElement::MakeElement("������","������"));
		p->add_child_last(JsonElement::MakeElement("������","��־��"));
		p->add_child_last(JsonElement::MakeElement("c++","���ױ�"));
		p->add_child_last(JsonElement::MakeElement("c++","κ����"));
		p->add_child_last(JsonElement::MakeElement("c++","��Ƽ"));

		std::string str = je->get_json(true);
		puts(str.c_str());
	}
	catch(JsonError err)
	{
		puts(err.what().c_str());
	}
}

void test_make_json4()
{
	JsonElementPtr je = JsonElement::MakeElement();
	je->add_child_last(JsonElement::MakeElement("1",true));
	je->add_child_last(JsonElement::MakeElement("2","abc"));
	je->add_child_last(JsonElement::MakeElement("3",13));
	JsonElementPtr p = je->add_child_last(JsonElement::MakeElement("4"));
	p->add_child_last(JsonElement::MakeElement(NULL,"a"));
	p->add_child_last(JsonElement::MakeElement(NULL,"b"));
	p->add_child_last(JsonElement::MakeElement(NULL,"c"));
	puts(je->get_json().c_str());
	je->get_child_first()->set_value("bbb");
	je->get_child_at(1)->set_value(12);
	je->get_child_at(2)->set_value(15);
	je->get_child_last()->set_value(false);
	puts(je->get_json().c_str());
	je->remove_all_children();
}
