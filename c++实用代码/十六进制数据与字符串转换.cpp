#include <stdio.h>
int main(int argc, char *argv[])
{
	char c;
	c=0xf;
	c+=55;
loop:
	printf("1. ʮ�������ַ���תʮ��������\n"
		   "2. ʮ��������תʮ�������ַ���\n"
		   "��ѡ���������:");
	char sel = getchar();
	while('\n' != (c=getchar()));
	if(sel!='1' && sel!='2')
		goto loop;
loop2:
	printf("������Ҫת�����ļ�:");
	char buf[512]={0};
	gets(buf);
	FILE * pf = fopen(buf,"rb");
	if(pf == NULL)
	{
		puts("���ļ�ʧ��");
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
		puts("������ļ�ʧ�ܣ�����ļ�Ϊ��");
		puts(buf2);
		puts("�����ļ��Ƿ�ռ�ã��ļ�·���Ƿ���ЩȨ��");
		goto loop2;
	}
	fseek(pf,0,SEEK_SET);
	fseek(pf2,0,SEEK_SET);
	unsigned char b,bl,bh;
	int rc;
	int count=0;
	switch(sel)
	{
	case '1':		//ʮ�������ַ���תʮ��������
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
				printf("��ԭ�ĵ�%d���ַ�������ת������\n",count);
				goto loop2;
			}
			if(bh>='0' && bh<='9') bh-='0';
			else if(bh>='a' && bh<='f') bh-=87;
			else if(bh>='A' && bh<='F') bh-=55;
			else
			{
				puts("ԭ�ļ����ݴ���");
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
	puts("ת����ɣ������ļ�:");
	puts(buf2);
	puts("����x�˳���������������ת��");
	sel = getchar();
	if(sel != 'x')
		goto loop;
	else
		return 0;
}