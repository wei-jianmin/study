#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

unsigned int crc32(unsigned char *buf, int len)
{
	int i, j;
	unsigned int crc, mask;
	crc = 0xFFFFFFFF;
	for (i = 0; i < len; i++) {
		crc = crc ^ (unsigned int)buf[i];
		for (j = 7; j >= 0; j--) {    // Do eight times.
			mask = -(crc & 1);
			crc = (crc >> 1) ^ (0xEDB88320 & mask);
		}
	}
	return ~crc;
}

unsigned int crc4(unsigned char *buf, int len)
{
	unsigned int crc, mask;
	crc = 0xFFFFFFFF;
	unsigned int i,j,k;
	i = *(unsigned int*)buf;
	j = *(unsigned int*)(buf+4);
	k = *(unsigned int*)(buf+8);
	unsigned int sum = i+j+k;
	//printf("%d+%d+%d = %d\n",i,j,k,sum);
	return sum;
}

void rand_buf(unsigned char buf[12])
{
	/*
	for(int i=0;i<12;i++)
		buf[i] = rand()%255;
	*/
	for(int i=0;i<3;i++)
	{
		buf[i*4] = rand()%20+1;
	}
}

int check_value(int size,unsigned int v,unsigned int vl[65536])
{
	for(int i=0;i<size;i++)
		if(v==vl[i])
			return i;
	return -1;
}

int main()
{
	srand(time(0));

	unsigned char buf[12];
	unsigned int v = 0;
	unsigned int vl[10000]={0};
	unsigned char bufl[12*10000]={0};
	unsigned int index = 0; //指向未用的那个
	memset(buf,0,12);
	buf[2] = (unsigned char)8;
	buf[6] = (unsigned char)8;
	buf[10] = (unsigned char)8;
	for(int j=0;j<100;j++)
	{
		index = 0;
		for(int i=0;i<1000;i++)
		{
			rand_buf(buf);
			v = crc4(buf,12);
			//printf("main: %d+%d+%d = %d\n",*(unsigned int*)buf,*(unsigned int *)(buf+4),*(unsigned int *)(buf+8),v);
			int w = check_value(index,v,vl);
			if(w>=0)
			{
				if(*(unsigned int*)(buf) != *(unsigned int*)(bufl+12*w) ||
					*(unsigned int*)(buf+4) != *(unsigned int*)(bufl+12*w+4) ||
					*(unsigned int*)(buf+8) != *(unsigned int*)(bufl+12*w+8))  //crc原文不一样
				printf("find duplicated %0x+%0x+%0x = %0x+%0x+%0x = %0x\n",*(unsigned int*)(buf),*(unsigned int*)(buf+4),*(unsigned int*)(buf+8),
					*(unsigned int*)(bufl+12*w),*(unsigned int*)(bufl+12*w+4),*(unsigned int*)(bufl+12*w+8),v);
			}
			vl[index]=v;
			memcpy(bufl+12*index,buf,12);
			index++;
		}
		printf("%d次循环完成\n",j);
	}
	getchar();
	return 0;
}

/*
实验结果：
每次循环测试一万条不用原文对应crc32校验码的碰撞情况，
循环测试1000次，没有发现碰撞
*/