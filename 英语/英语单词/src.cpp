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
	strftime(tAll, sizeof(tAll), "%Y年%m月%d日", std::localtime(&currenttime));
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
	path += "单词";
	if(1/*word_*split_*explain_==0*/)
	{
		if(word_!=0)
			path+="_英";
		if(split_!=0)
		{
			path+="_拼";
			path+=split_+'0';
		}
		if(explain_!=0)
			path+="_译";
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
	path += "说明.txt";
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
			stm << ";如果句首没指定个数，单词的默认重复次数"<<endl;
			stm << "repeat_times=2"<<endl;
			stm << ";生成的文件中是否包含英语单词部分"<<endl;
			stm << "word=1"<<endl;
			stm << ";生成的文件中是否包含拆分的字母部分"<<endl;
			stm << ";=0:绝对不拆分,=1:优先不拆分,=2:优先拆分,=3:绝对拆分"<<endl;
			stm << "split=2"<<endl;
			stm << ";生成的文件中是否包含汉语释义部分"<<endl;
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
			stm << "可以直接把英语单词文件拖到本程序上运行"<<endl;
			stm << "否则默认打开本目录下的words.txt文件，没有则运行失败"<<endl;
			stm << "当前目录下没有配置文件时，会自动生成配置文件"<<endl;
			stm << "通过配置文件可控制生成文件的默认格式"<<endl;
			stm << "英语单词文件的格式为：[n] 英文单词 [-] 汉语释义"<<endl;
			stm << "每个英语单词和其汉语释义占一行，中间用空格隔开"<<endl;
			stm << "如果英文单词前有数字，则该单词重复指定次数，否则重复默认次数"<<endl;
			stm << "如果英语单词和汉语释义之间有减号(-)，且-前后都有空格，则该单词不进行拆分"<<endl;
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
		//std::locale::global(loc);//恢复全局locale
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
			//std::locale::global(loc);//恢复全局locale
			cout<<"open file "<<file_name2<<" error"<<endl;
			system("pause");
			return false;
		}

		write_file << "第" << i+1 << "遍" << endl;

		int times = 0;
		int pos = 0;
		bool has_sub=false;	//单词后面是否有-
		bool has_add=false;	//单词后面是否有+
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
					write_file << line_left << "。";
				switch(split_)
				{
				case 0:		//绝对不拆分
					has_add=false;
				case 1:		//优先不拆分
					if(has_add)
					{
						write_separated_word(write_file,line_left);
						write_file << "。";
					}
					break;
				case 3:		//绝对拆分
					has_sub = false;
				case 2:		//优先拆分
					if(has_sub==false)
					{
						write_separated_word(write_file,line_left);
						write_file << "。";
					}
					break;
				default:
					break;
				}
				if(explain_!=0)
					write_file << line_right << "。";
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
	std::locale loc = std::locale::global(std::locale(""));//设置全局locale为本地环境
	submain(argc,argv);
	std::locale::global(loc);//恢复全局locale
	return 0;
}