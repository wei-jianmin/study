#include "utils.h"
#include <windows.h>
#include <stdio.h>

void Trace(const char *format,...)
{
	if(format==NULL)
		return;
	char buf[2048]={0};
	va_list arg_ptr;
	va_start(arg_ptr,format);	//�ѹ̶�������ַ���ȷ����ε��ڴ���ʼ��ַ��
	vsprintf(buf,format,arg_ptr);
	va_end(arg_ptr);
	//OutputDebugStringA(buf);
	puts(buf);
}
