#include <iostream>
#include <fstream>
#include <string>
#include <ctime>
#include <Windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <io.h>
using namespace std;

#define READ_CFG(s,v) GetPrivateProfileIntA("common",#s,v,cfg_name.c_str())
string get_config_file_name();

void write_separated_word(fstream & stm,string & word)
{
	string s(word.length()*2-1,',');
	for(int i=0;i<word.length();i++)
	{
		s[i*2] = word[i];
	}
	stm << s;
}

string get_time()
{
	string stime;
	time_t currenttime = std::time(0);	
	char tAll[255];
	strftime(tAll, sizeof(tAll), "%Y��%m��%d��", std::localtime(&currenttime));
	stime = tAll;
	return stime;
}

string get_write_file_name()
{
	string cfg_name = get_config_file_name();
	int word_ = READ_CFG(word,1);
	int split_ = READ_CFG(split,2);
	int explain_ = READ_CFG(explain,1);
	string path;
	char buf[256]={0};
	GetModuleFileNameA(NULL,buf,256);
	char *p = strrchr(buf,'\\');
	p[1]=0;
	path = buf;
	path += get_time();
	path += "����";
	if(1/*word_*split_*explain_==0*/)
	{
		if(word_!=0)
			path+="_Ӣ";
		if(split_!=0)
		{
			path+="_ƴ";
			path+=split_+'0';
		}
		if(explain_!=0)
			path+="_��";
	}
	path += ".txt";
	return path;
}

string get_comment_file_name()
{
	string path;
	char buf[256]={0};
	GetModuleFileNameA(NULL,buf,256);
	char *p = strrchr(buf,'\\');
	p[1]=0;
	path = buf;
	path += "˵��.txt";
	return path;
}

string get_config_file_name()
{
	string path;
	char buf[256]={0};
	GetModuleFileNameA(NULL,buf,256);
	char *p = strrchr(buf,'\\');
	p[1]=0;
	path = buf;
	path += "config.ini";
	return path;
}

string get_read_file_name()
{
	string path;
	char buf[256]={0};
	GetModuleFileNameA(NULL,buf,256);
	char *p = strrchr(buf,'\\');
	p[1]=0;
	path = buf;
	path += "words.txt";
	return path;
}
void make_config()
{
	string cfg_name = get_config_file_name();
	if(access(cfg_name.c_str(),0)==-1)
	{
		fstream stm(cfg_name.c_str(),ios::out);
		if(stm.is_open())
		{
			stm << "[common]"<<endl;
			stm << ";�������ûָ�����������ʵ�Ĭ���ظ�����"<<endl;
			stm << "repeat_times=2"<<endl;
			stm << ";���ɵ��ļ����Ƿ����Ӣ�ﵥ�ʲ���"<<endl;
			stm << "word=1"<<endl;
			stm << ";���ɵ��ļ����Ƿ������ֵ���ĸ����"<<endl;
			stm << ";=0:���Բ����,=1:���Ȳ����,=2:���Ȳ��,=3:���Բ��"<<endl;
			stm << "split=2"<<endl;
			stm << ";���ɵ��ļ����Ƿ�����������岿��"<<endl;
			stm << "explain=1"<<endl;
			stm.close();
		}
	}
}

void make_comment()
{
	string com_name = get_comment_file_name();
	if(access(com_name.c_str(),0)==-1)
	{
		fstream stm(com_name.c_str(),ios::out);
		if(stm.is_open())
		{
			stm << "����ֱ�Ӱ�Ӣ�ﵥ���ļ��ϵ�������������"<<endl;
			stm << "����Ĭ�ϴ򿪱�Ŀ¼�µ�words.txt�ļ���û��������ʧ��"<<endl;
			stm << "��ǰĿ¼��û�������ļ�ʱ�����Զ����������ļ�"<<endl;
			stm << "ͨ�������ļ��ɿ��������ļ���Ĭ�ϸ�ʽ"<<endl;
			stm << "Ӣ�ﵥ���ļ��ĸ�ʽΪ��[n] Ӣ�ĵ��� [-] ��������"<<endl;
			stm << "ÿ��Ӣ�ﵥ�ʺ��人������ռһ�У��м��ÿո����"<<endl;
			stm << "���Ӣ�ĵ���ǰ�����֣���õ����ظ�ָ�������������ظ�Ĭ�ϴ���"<<endl;
			stm << "���Ӣ�ﵥ�ʺͺ�������֮���м���(-)����-ǰ���пո���õ��ʲ����в��"<<endl;
			stm.close();
		}
	}
}
bool doit(int argc,char *argv[])
{
	make_comment();
	make_config();
	string cfg_name = get_config_file_name();
	int repeat_times = READ_CFG(repeat_times,1);
	int word_ = READ_CFG(word,1);
	int split_ = READ_CFG(split,2);
	int explain_ = READ_CFG(explain,1);

	string file_name = get_write_file_name();

	string file_name2;
	if(argc>1)
		file_name2 = argv[1];
	else
		file_name2 = get_read_file_name();

	fstream write_file;
	write_file.open(file_name.c_str(),fstream::out);

	if(!write_file.is_open())
	{
		cout<<"open file "<<file_name<<" error"<<endl;
		//std::locale::global(loc);//�ָ�ȫ��locale
		system("pause");
		return false;
	}

	write_file << get_time() << endl << endl;

	string line,line_left,line_right;
	for(int i=0;i<10;i++)
	{
		fstream read_file;
		read_file.open(file_name2.c_str(),fstream::in);
		if(!read_file.is_open())
		{
			//std::locale::global(loc);//�ָ�ȫ��locale
			cout<<"open file "<<file_name2<<" error"<<endl;
			system("pause");
			return false;
		}

		write_file << "��" << i+1 << "��" << endl;

		int times = 0;
		int pos = 0;
		bool has_sub=false;	//���ʺ����Ƿ���-
		bool has_add=false;	//���ʺ����Ƿ���+
		while(getline(read_file, line))
		{
			if(line.length()<1)
				continue;
			has_sub=false;
			has_add=false;
			times = repeat_times;
			if(line[0]>='0' && line[0]<='9')
			{
				times = line[0]-'0';
				pos = line.find(' ');
				line.erase(0,pos+1);
			}
			pos = line.find(' ');
			line_left = line.substr(0,pos);
			line_right = line.substr(pos+1,-1);
			if(line_right[0]=='-' && line_right[1]==' ')
			{
				line_right.erase(0,2);
				has_sub=true;
			}
			else if(line_right[0]=='+' && line_right[1]==' ')
			{
				line_right.erase(0,2);
				has_add=true;
			}
			while(times>0)
			{
				if(word_!=0)
					write_file << line_left << "��";
				switch(split_)
				{
				case 0:		//���Բ����
					has_add=false;
				case 1:		//���Ȳ����
					if(has_add)
					{
						write_separated_word(write_file,line_left);
						write_file << "��";
					}
					break;
				case 3:		//���Բ��
					has_sub = false;
				case 2:		//���Ȳ��
					if(has_sub==false)
					{
						write_separated_word(write_file,line_left);
						write_file << "��";
					}
					break;
				default:
					break;
				}
				if(explain_!=0)
					write_file << line_right << "��";
				--times;
			}
			write_file << endl;
		}

		read_file.close();
		write_file << endl;
	}

	write_file.close();
	return true;
}
void submain(int argc,char *argv[])
{
	string cfg_name = get_config_file_name();
	int split_ = READ_CFG(split,2);
	std::string sp="";
	sp += split_+'0';
	if(split_==9)
	{
		int b=false;
		do 
		{
			WritePrivateProfileStringA("common","split","0",cfg_name.c_str());
			b = doit(argc,argv);
			if(!b) break;
			WritePrivateProfileStringA("common","split","1",cfg_name.c_str());
			b = doit(argc,argv);
			if(!b) break;
			WritePrivateProfileStringA("common","split","2",cfg_name.c_str());
			b = doit(argc,argv);
			if(!b) break;
			WritePrivateProfileStringA("common","split","3",cfg_name.c_str());
			b = doit(argc,argv);
			if(!b) break;
			WritePrivateProfileStringA("common","split",sp.c_str(),cfg_name.c_str());
		} while (false);
	}
	else
	{
		doit(argc,argv);
	}
}
int main(int argc,char *argv[])
{	
	std::locale loc = std::locale::global(std::locale(""));//����ȫ��localeΪ���ػ���
	submain(argc,argv);
	std::locale::global(loc);//�ָ�ȫ��locale
	return 0;
}