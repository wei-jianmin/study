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
�����磺1��5-3��7     
��Ϊ   �� 1��3��4��5��7
֧�ֽ����ĵĶ��ű�ΪӢ�ĵ�
֧�ֽ������� - �� ����Ϊ������
֧�ֿո���Ϊ�ָ�������ͬ��,
֧����,��-��ʼ���β���Զ�ɾ����
��֧�ָ���
д��������
	��   1��  3  4��12-7������            ��ͬ��  1,3,4,7-12
	---13  15����		    ��ͬ��  13,15
	-����-12��12��-��-��--����          ��ͬ��  12,12
	12 ----    14                                       ��ͬ��  12-14
	12 - 14                                              ��ͬ��  12-14
	12 , -14                                             ��ͬ��  12-14
	12 �� 14                                           ��ͬ��  12,14
	12-,--����-14                                   ��ͬ��  12-14
*/
int parse_range(const char* rng,std::vector<int>& vec)
{
	//���������Ԥ����
	if(rng==NULL) return 0;
	int rng_len = strlen(rng);
	if(rng_len==0 || rng_len>255) return 0;
	std::string str_rng = rng;
	str_replace(str_rng," ",",");
	str_replace(str_rng,"��",",");
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
			return 0;   //���ڲ��Ϸ��ַ�
	}
	//�����ָ�
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
	//����ȥ��
	sort(vec.begin(),vec.end());
	std::vector<int>::iterator iter = unique(vec.begin(),vec.end());
	vec.resize(iter - vec.begin());
	return vec.size();
}

int main()
{
	while(1)
	{
		printf("�����룺\t");
		char buf[1024]={0};
		scanf("%[^\n]%*c",buf);
		//const char* p = "1,3-8,12";
		std::vector<int> vec;
		parse_range(buf,vec);
		printf("�����\t");
		for(int i=0;i<vec.size();i++)
		{
			printf("%d ",vec.at(i));
		}
		printf("\n");
	}
	system("pause");
	return 0;
}