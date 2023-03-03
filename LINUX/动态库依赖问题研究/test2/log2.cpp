#include <stdio.h>
int g_ver;
void setver(int v)
{
	char buf[100];
	sprintf(buf,"this is in log2, setver = %d",v);
	g_ver = v;
}
int ver()
{
	char buf[100];
	sprintf(buf,"this is in log2, ver = %d",g_ver);
	puts(buf);
}
