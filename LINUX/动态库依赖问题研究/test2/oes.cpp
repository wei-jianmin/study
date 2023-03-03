#include <stdio.h>
#include "log.h"
extern "C" void runoes()
{
	puts("get in oes");
	ver();
	puts("set log subver = 2");
	setver(2);
	ver();
	return ;
}
	
