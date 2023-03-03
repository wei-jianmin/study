#include <Windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include <process.h> 

//SRWLOCK g_srwlock;
CRITICAL_SECTION g_cs;
CONDITION_VARIABLE g_cv;

unsigned __stdcall thread_1(void*)
{
	puts("thread_1 : try enter critical section");
	EnterCriticalSection(&g_cs);
	puts("thread_1 : get in critical section, sleep 1000");
	Sleep(1000);
	puts("thread_1 : sleep finish, start sleep condition");
	SleepConditionVariableCS(&g_cv,&g_cs,INFINITE);
	puts("thread_1 : sleep condition ok, sleep 2000");
	Sleep(2000);
	puts("thread_1 : sleep finish, start leave critical section");
	LeaveCriticalSection(&g_cs);
	puts("thread_1 : leave critical section ok");
	puts("thread_1 : return");
	return 0;
}

unsigned __stdcall thread_2(void*)
{
	puts("thread_2 : sleep 500");
	Sleep(500);
	puts("thread_2 : try enter critical section");
	EnterCriticalSection(&g_cs);
	puts("thread_2 : enter critical section ok, sleep 1000");
	Sleep(1000);
	puts("thread_2 : sleep finish, start wake condition");
	WakeConditionVariable(&g_cv);
	puts("thread_2 : wake condition ok, sleep 1000");
	Sleep(1000);
	puts("thread_2 : sleep finish, start leave critical section");
	LeaveCriticalSection(&g_cs);
	puts("thread_2 : leave critical section ok, sleep 1000");
	Sleep(1000);
	puts("thread_2 : sleep finish, try enter critical section");
	EnterCriticalSection(&g_cs);
	puts("thread_2 : enter critical section ok, sleep 1000");
	Sleep(1000);
	puts("thread_2 : sleep finish, start leave critical section");
	LeaveCriticalSection(&g_cs);
	puts("thread_2 : leave critical section ok");
	puts("thread_2 : return");
	return 0;
}

int main()
{
	InitializeCriticalSection(&g_cs);
	//InitializeSRWLock(&g_srwlock);
	InitializeConditionVariable(&g_cv);
	_beginthreadex(NULL,0,thread_1,NULL,0,NULL);
	_beginthreadex(NULL,0,thread_2,NULL,0,NULL);
	//system("pause");
	getchar();
	return 0;
}