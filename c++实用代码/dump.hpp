#pragma once

#ifdef _WINDOWS

#include <Windows.h>
#include <dbghelp.h>
#define DUMP_FILE ".\\crash_point.dmp"
#include <string>

#pragma comment(lib,"dbghelp.lib")

#define SET_DUMP SetUnhandledExceptionFilter((LPTOP_LEVEL_EXCEPTION_FILTER)ApplicationCrashHandler)

void CreateDumpFile(LPCSTR lpstrDumpFilePathName, EXCEPTION_POINTERS *pException)
{
	HANDLE hDumpFile = CreateFileA(lpstrDumpFilePathName, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
	MINIDUMP_EXCEPTION_INFORMATION dumpInfo;
	dumpInfo.ExceptionPointers = pException;
	dumpInfo.ThreadId = GetCurrentThreadId();
	dumpInfo.ClientPointers = TRUE;
	MiniDumpWriteDump(GetCurrentProcess(), GetCurrentProcessId(), hDumpFile, MiniDumpNormal, &dumpInfo, NULL, NULL);
	CloseHandle(hDumpFile);
}

LONG WINAPI ApplicationCrashHandler(EXCEPTION_POINTERS *pException)
{
	char szPath[512];
	GetModuleFileNameA(NULL,szPath,512);
	char *pChar = strrchr( szPath, '\\');
	*(pChar+1) = 0;
	std::string strPath = szPath;
	SYSTEMTIME syst;
	GetLocalTime(&syst);
	char strCount[100];
	sprintf_s(strCount,100,"%d.%.2d.%.2d.%.2d.%.2d.%.2d.%.3d.dmp",syst.wYear- 2000,syst.wMonth,syst.wDay,syst.wHour,syst.wMinute,syst.wSecond,syst.wMilliseconds);
	strPath +=std::string(strCount);
	MakeSureDirectoryPathExists(strPath.c_str());
	CreateDumpFile(strPath.c_str(), pException);
	FatalAppExitA(0,"*** Unhandled Exception! ***");
	return EXCEPTION_EXECUTE_HANDLER;
}
#else
#define SET_DUMP (0)
#endif