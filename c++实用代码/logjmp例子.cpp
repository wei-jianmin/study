#include <stdio.h>
#include <setjmp.h>

/*
setjmp和logjmp是配合使用的，用它们可以实现跳转的功能，
和goto语句很类似，不同的是goto只能实现在同一个函数之内的跳转，
而setjmp和logjmp可以实现在不同函数间的跳转
用法：
首先用setjmp设置跳转的地点，
setjmp的参数buf是用来保存设置跳转点时的函数使用的重要数据，
当从其他函数跳转回来，如果不用这个保存的数据恢复当前函数的一些数据的话，跳转回来是不能运行的。
第一次设置的时候setjmp返回值为0
使用longjmp就可以跳转到setjmp的地方了，参数buf就是使用setjmp的时候保存的，
而第二个参数会在跳转以后把这个值让setjmp返回的，也就是longjmp第二个参数，
就是跳转到setjmp之后setjmp函数要返回的值
*/

jmp_buf jb1,jb2,jb3;

void func3()
{
	puts("3_1");
	puts("3_2");
	longjmp(jb3,3);
	puts("3_3");
}


void func2()
{
	puts("2_1");
	if(0==setjmp(jb3))
		func3();
	else
		puts("2_2");
	longjmp(jb2,2);
	puts("2_3");
}

void func1()
{
	puts("1_1");
	if(0==setjmp(jb2))
		func2();
	else
		puts("1_2");
	longjmp(jb1,1);
	puts("1_3");
}


int main()
{
	puts("0_1");
	if(setjmp(jb1)==0)
	{
		puts("0_2");
		func1();
	}
	else
		puts("0_3");
	return 0;
}