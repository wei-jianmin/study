#include <stdio.h>
int main(int argc, char *argv[])
{
	char c;
	c=0xf;
	c+=55;
loop:
	printf("1. 十六进制字符串转十六进制数\n"
		   "2. 十六进制数转十六进制字符串\n"
		   "请选择操作类型:");
	char sel = getchar();
	while('\n' != (c=getchar()));
	if(sel!='1' && sel!='2')
		goto loop;
loop2:
	printf("请输入要转换的文件:");
	char buf[512]={0};
	gets(buf);
	FILE * pf = fopen(buf,"rb");
	if(pf == NULL)
	{
		puts("打开文件失败");
		goto loop2;
	}
	char buf2[512]={0};
	char ext[10]={0};
	strcpy(buf2,buf);
	char* p = strrchr(buf2,'.');
	if(p)
	{
		strcpy(ext,p);
		p[0]=0;
		strcat(buf2,"_converted");
		strcat(buf2,ext);
	}
	else
	{
		strcat(buf2,"_converted");
	}
	FILE *pf2 = fopen(buf2,"wb");
	if(pf2 == NULL)
	{
		puts("打开输出文件失败，输出文件为：");
		puts(buf2);
		puts("请检查文件是否被占用，文件路径是否有些权限");
		goto loop2;
	}
	fseek(pf,0,SEEK_SET);
	fseek(pf2,0,SEEK_SET);
	unsigned char b,bl,bh;
	int rc;
	int count=0;
	switch(sel)
	{
	case '1':		//十六进制字符串转十六进制数
		do{
			rc=fread(&bh,1,1,pf);
			fread(&bl,1,1,pf);
			if(rc==0)
				break;
			++count;
			if(bl>='0' && bl<='9') bl-='0';
			else if(bl>='a' && bl<='f') bl-=87;
			else if(bl>='A' && bl<='F') bl-=55;
			else
			{
				printf("在原文第%d个字符处数据转换错误\n",count);
				goto loop2;
			}
			if(bh>='0' && bh<='9') bh-='0';
			else if(bh>='a' && bh<='f') bh-=87;
			else if(bh>='A' && bh<='F') bh-=55;
			else
			{
				puts("原文件数据错误");
				goto loop2;
			}
			bh<<=4;
			b = bl | bh;
			fwrite(&b,1,1,pf2);
			bl=0;
			bh=0;
		}while(true);
	case '2':
		do 
		{
			rc=fread(&b,1,1,pf);
			if(rc==0)
				break;
			bl = b & 0xf;
			bh = b & 0xf0;
			bh >>= 4;
			if(bl<=9) bl+='0';
			else bl+=55;
			if(bh<=9) bh+='0';
			else bh+=55;
			fwrite(&bh,1,1,pf2);
			fwrite(&bl,1,1,pf2);
			b=0;
		} while (true);
		break;
	}
	fclose(pf);
	fclose(pf2);
	puts("转换完成，生成文件:");
	puts(buf2);
	puts("输入x退出，输入其它继续转换");
	sel = getchar();
	if(sel != 'x')
		goto loop;
	else
		return 0;
}