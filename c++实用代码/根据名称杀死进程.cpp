#include <Windows.h>
#include <TLHELP32.H>
//根据程序名获取进程ID
DWORD KillProcessByName(int argc,const char* argv[])
{
	//获取进程信息
	HANDLE hProcessSnap = ::CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	if (hProcessSnap == INVALID_HANDLE_VALUE)
		return 0;

	DWORD dwProcessID = 0;
	PROCESSENTRY32 stProcessEntry32 = { 0 };
	stProcessEntry32.dwSize = sizeof(stProcessEntry32);
	BOOL bSucceed = ::Process32First(hProcessSnap, &stProcessEntry32);
	DWORD killCount=0;
	for (;;)
	{
		if (!bSucceed)
			break;

		bSucceed = ::Process32Next(hProcessSnap, &stProcessEntry32);
		bool find_flag =false;
		for(int i=0;i<argc;i++)
		{
			if(stricmp(stProcessEntry32.szExeFile, argv[i]) == 0)
			{
				find_flag = true;
				break;
			}
		}
		if (find_flag)
		{
			dwProcessID = stProcessEntry32.th32ProcessID;
			HANDLE hProcessHandle = NULL;
			hProcessHandle = ::OpenProcess(PROCESS_TERMINATE, FALSE, dwProcessID);
			if(hProcessHandle)
			{
				::TerminateProcess(hProcessHandle, 200);
				killCount++;
				if (hProcessHandle != NULL)
					CloseHandle(hProcessHandle);
			}
		}
	}
	::CloseHandle(hProcessSnap);
	return killCount;
}