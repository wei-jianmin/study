#include <stdio.h>
int g_ver;
void setver(int v)
{
	char buf[100];
	sprintf(buf,"this is in log1, setver = %d",v);
	g_ver = v;
}
int ver()
{
	char buf[100];
	sprintf(buf,"this is in log1, ver = %d",g_ver);
	puts(buf);
}
