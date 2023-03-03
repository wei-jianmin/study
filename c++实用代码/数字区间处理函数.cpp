#include <string>
#include <vector>
#include <algorithm>

void str_replace(std::string& ori,const std::string& src,const std::string& dst)
{
	int pos=0;
	while(true)
	{
		pos = ori.find(src.c_str());
		if(pos == -1) break;
		ori = ori.replace(pos,src.length(),dst.c_str());
	}
}

/*
处理如：1，5-3，7     
变为   ： 1，3，4，5，7
支持将中文的逗号变为英文的
支持将连续的 - 或 ，变为单个的
支持空格作为分隔符，等同于,
支持以,或-开始或结尾（自动删除）
不支持负数
写法举例：
	，   1，  3  4，12-7，，，            等同于  1,3,4,7-12
	---13  15，，		    等同于  13,15
	-，，-12，12，-，-，--，，          等同于  12,12
	12 ----    14                                       等同于  12-14
	12 - 14                                              等同于  12-14
	12 , -14                                             等同于  12-14
	12 ， 14                                           等同于  12,14
	12-,--，，-14                                   等同于  12-14
*/
int parse_range(const char* rng,std::vector<int>& vec)
{
	//参数检查与预处理
	if(rng==NULL) return 0;
	int rng_len = strlen(rng);
	if(rng_len==0 || rng_len>255) return 0;
	std::string str_rng = rng;
	str_replace(str_rng," ",",");
	str_replace(str_rng,"，",",");
	str_replace(str_rng,",,",",");
	str_replace(str_rng,"-,","-");
	str_replace(str_rng,",-","-");
	str_replace(str_rng,"--","-");
	int valid_start=0,valid_end=str_rng.length()-1;
	while(str_rng.at(valid_start)==',' || str_rng.at(valid_start)=='-')
	{
		valid_start++;
		if(valid_start == valid_end) return 0;
	}
	while(str_rng.at(valid_end)==',' || str_rng.at(valid_end)=='-') valid_end--;
	char rng_buf[256]={0};
	strncpy(rng_buf,str_rng.c_str()+valid_start,valid_end-valid_start+1);
	const char* forbid="0123456789-,";
	if(strstr(rng_buf,",-")>0) return 0;
	if(strstr(rng_buf,"-,")>0) return 0;
	for(int i=0;i<strlen(rng_buf);i++)
	{
		if(strchr(forbid,rng_buf[i])==NULL)
			return 0;   //存在不合法字符
	}
	//按，分割
	char* p = strtok(rng_buf,",");
	while(p)
	{
		const char* pslash = strchr(p,'-');
		if(pslash)
		{
			int i1=atoi(p);
			int i2=atoi(pslash+1);
			if(i1>i2)
			{
				int i=i1;
				i1=i2;
				i2=i;
			}
			for(int i=i1;i<=i2;i++)
				vec.push_back(i);
		}
		else
			vec.push_back(atoi(p));
		p = strtok(NULL,",");
	}
	//排序，去重
	sort(vec.begin(),vec.end());
	std::vector<int>::iterator iter = unique(vec.begin(),vec.end());
	vec.resize(iter - vec.begin());
	return vec.size();
}

int main()
{
	while(1)
	{
		printf("请输入：\t");
		char buf[1024]={0};
		scanf("%[^\n]%*c",buf);
		//const char* p = "1,3-8,12";
		std::vector<int> vec;
		parse_range(buf,vec);
		printf("处理后：\t");
		for(int i=0;i<vec.size();i++)
		{
			printf("%d ",vec.at(i));
		}
		printf("\n");
	}
	system("pause");
	return 0;
}