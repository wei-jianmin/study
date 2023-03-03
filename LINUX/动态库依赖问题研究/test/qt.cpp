#include <stdio.h>
int count = 1;
extern "C" void func()
{
    printf("func in qt 1.1.1, count=%d\n",count);
}
