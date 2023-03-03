//将项目设置为多字节
#include <Windows.h>
#include <WtsApi32.h>
#include <string.h>
#include <tchar.h>
#include <stdio.h>
#pragma comment(lib,"WtsApi32")

SERVICE_STATUS ServiceStatus;
SERVICE_STATUS_HANDLE hServiceStatusHandle;
bool stop_flag;

VOID WINAPI my_handle_func(DWORD    dwControl);
VOID WINAPI myproc(DWORD   dwNumServicesArgs,LPSTR   *lpServiceArgVectors);

DWORD show_msg(char *title,char* msg)
{
	DWORD resp;
	WTSSendMessage(	WTS_CURRENT_SERVER_HANDLE, 
					WTSGetActiveConsoleSessionId(),
					title,_tcslen(title),
					msg,_tcslen(msg), 
					MB_OK, 0, &resp, true);  
	//倒数第三个参数为等待秒数，0为无限等待,最后一个参数为是否阻塞
	return resp;
}

//1. 接收用命令行启动服务时指定的参数
int main(int argc, char *argv[])
{
	char tmp_buf[50]={0};
	for(int i=0;i<argc;i++)
	{
		sprintf(tmp_buf,"main 第%d/%d个参数",i,argc);
		show_msg(tmp_buf,argv[i]);
	}
#if 1					//当有多个服务时，这样用比较方便
	SERVICE_TABLE_ENTRY tbls[2];
	tbls[0].lpServiceName = "SERV BY WJM";   //可为NULL，但当定义了多个服务时，那么这个域必须指定
	tbls[0].lpServiceProc = (LPSERVICE_MAIN_FUNCTIONA)myproc;
	tbls[1].lpServiceName = NULL;
	tbls[1].lpServiceProc = NULL;   //一个程序可能包含若干个服务。分派表的最后一项的两个域都必须为 NULL 指针

	//启动服务的控制分派机线程，当分派表中所有的服务执行完之后（服务为停止状态），或发生运行时错误，该函数调用返回，进程终止。
	StartServiceCtrlDispatcher(tbls);
#else
	myproc(0,NULL);		//当只有一个服务时，可以直接这样用
#endif
}

//2. 接收用命令行启动服务时指定的参数
VOID WINAPI myproc(DWORD   dwNumServicesArgs,LPSTR   *lpServiceArgVectors)
{
	char tmp_buf[50]={0};
	for(int i=0;i<dwNumServicesArgs;i++)
	{
		sprintf(tmp_buf,"myproc 第%d/%d个参数",i,dwNumServicesArgs);
		show_msg(tmp_buf,lpServiceArgVectors[i]);
	}
	// 1: 为服务注册控制器函数（实际自动创建来服务）
	show_msg("myproc","注册控制处理器函数");
	hServiceStatusHandle = RegisterServiceCtrlHandler("SERV BY WJM", my_handle_func);  //为服务注册控制处理器函数，这一步应该尽快得到执行

	// 2：先让服务处于挂起状态，好完成一些初始化之类的工作
	ServiceStatus.dwServiceType        = SERVICE_WIN32;			 //一般都设为此值即可
	ServiceStatus.dwCurrentState       = SERVICE_START_PENDING;  //启动挂起，此状态下不会接受控制指令（不会调用my_handle_func函数）。
	ServiceStatus.dwControlsAccepted   = SERVICE_ACCEPT_STOP | SERVICE_ACCEPT_SHUTDOWN | SERVICE_ACCEPT_PAUSE_CONTINUE;  //可接受哪些类型的指令
	ServiceStatus.dwWin32ExitCode      = 0;      //当想返回错误，应设为ERROR_SERVICE_SPECIFIC_ERROR ，表明dwServiceSpecificExitCode中存着错误码
	ServiceStatus.dwServiceSpecificExitCode = 0; //当发生错误时，服务返回该错误码
	ServiceStatus.dwCheckPoint         = 0;      //服务的进展状态值，服务在启动时应在完成其初始化的每一步时递增此值，当服务没有启动、停止、暂停或继续操作时，这个值应该是零
		//dwWaitHint指示下次检查时间：待定的启动、停止、暂停或继续操作所需的估计时间，以毫秒计。
		//在指定的时间量过去之前，服务应该对SetServiceStatus函数进行下一次调用，并增加dwCheckPoint值或改变dwCurrentState。
		//如果由dwWaitHint指定的时间量过去了，而dwCheckPoint没有被增加或dwCurrentState没有改变，
		//服务控制管理器或服务控制程序可以认为发生了错误，应该停止该服务。
		//然而，如果该服务与其他服务共享一个进程，服务控制管理器不能终止该服务程序，因为它也必须终止共享该进程的其他服务。
		//实际测试，不改变dwCheckPoint的值
	ServiceStatus.dwWaitHint           = 200;  
	SetServiceStatus(hServiceStatusHandle, &ServiceStatus);
	show_msg("myproc","使服务处于挂起状态");


	// 3：完成初始化工作
	//......初始化工作.........//
	show_msg("myproc","完成初始化工作");
	
	// 4. 改变状态为运行状态
	ServiceStatus.dwCurrentState       = SERVICE_RUNNING;
	ServiceStatus.dwCheckPoint         = 1;
	ServiceStatus.dwWaitHint           = 5000;  
	SetServiceStatus(hServiceStatusHandle, &ServiceStatus);
	show_msg("myproc","使服务处于运行状态");


	// 5. 循环
	stop_flag = false;
	unsigned int count = 1;
	while(1)
	{
		Sleep(1000);
		
		if(stop_flag)
		{
			show_msg("标题","服务即将停止");
			//在my_handle_func中设置了服务状态
			return;
		}
		else
		{
			count++;
			ServiceStatus.dwCheckPoint         = count;
			show_msg("标题","请在三秒内按下确定按钮");
			SetServiceStatus(hServiceStatusHandle, &ServiceStatus);
		}
	}

	//线程正常的结束方式应该是先设置状态为SERVICE_STOPPED，然后服务线程（这里就是本线程）结束循环或等待，线程退出，而不应该暴力的用 ExitThread 结束线程
}

//3. 控制处理器与处理各种 Windows 消息的窗口回调函数非常类似，它检查 SCM 发送了什么请求并采取相应行动
VOID WINAPI my_handle_func(DWORD    dwControl)
{
	switch(dwControl) 
	{
	case SERVICE_CONTROL_STOP:
	case SERVICE_CONTROL_SHUTDOWN:
		ServiceStatus.dwWin32ExitCode = 0; 
		ServiceStatus.dwCurrentState  = SERVICE_STOPPED; 
		ServiceStatus.dwCheckPoint    = 0; 
		ServiceStatus.dwWaitHint      = 0;
		//add you quit code here
		stop_flag = true;
		break; 
	default:
		return; 
	};
	SetServiceStatus(hServiceStatusHandle,  &ServiceStatus);
	show_msg("myproc","使服务处于停止状态");
}

/* 命令行操作举例
	sc create aaabbb binPath= F:\VSProjects\aaa\Win32\Debug\aaa.exe
	sc start aaabbb
	sc stop aaabbb
	sc delete aaabbb
*/

//测试创建、启动系统服务
bool TestStartService()
{
	//打开服务控制管理器
	SC_HANDLE hScm = OpenSCManager(NULL, NULL, SC_MANAGER_CREATE_SERVICE);
	if (hScm == NULL)
	{
		return false;
	}
	//创建系统服务，参数很多，可查看帮助文档
	SC_HANDLE hService = CreateService(hScm, "MySerivce", "MyService", SERVICE_ALL_ACCESS,
		SERVICE_WIN32_OWN_PROCESS, SERVICE_AUTO_START, SERVICE_ERROR_NORMAL, GetExeFullPath(), 
		NULL, NULL, "", NULL, "");
	if (hService == NULL)
	{
		return false;
	}
	//启动系统服务
	if (StartService(hService, 0, NULL) == false)
	{
		return false;
	}
	//释放句柄
	CloseServiceHandle(hScm);
	CloseServiceHandle(hService);
	return true;
}


//通过代码重启服务
#define SERVICE_NO_ERROR 0
#define OPEN_SCMANAGER_ERROR 2
#define OPEN_SERVICE_ERROR 3
#define QUERY_SERVICESTATUS_ERROR 4
#define STOP_SERVICE_ERROR 5
#define START_SERVICE_ERROR 6
  
int RestartService()
{
 
    // 打开服务管理对象
    SC_HANDLE hSC = ::OpenSCManager( NULL,
        NULL, GENERIC_EXECUTE);
    if( hSC == NULL)
    {      
        return OPEN_SCMANAGER_ERROR;
    }
    // 打开apache服务。
    SC_HANDLE hSvc = ::OpenService( hSC, "apache",
        SERVICE_START | SERVICE_QUERY_STATUS | SERVICE_STOP);
    if( hSvc == NULL)
    {
        ::CloseServiceHandle( hSC);
        return OPEN_SERVICE_ERROR;
    }
    // 获得服务的状态
    SERVICE_STATUS status;
    if( ::QueryServiceStatus( hSvc, &status) == FALSE)
    {
        ::CloseServiceHandle( hSvc);
        ::CloseServiceHandle( hSC);
        return QUERY_SERVICESTATUS_ERROR;
    }
    //如果处于运行状态则停止服务
    if( status.dwCurrentState == SERVICE_RUNNING)
    {
        // 停止服务
        if( ::ControlService( hSvc,
            SERVICE_CONTROL_STOP, &status) == FALSE)
        {
            ::CloseServiceHandle( hSvc);
            ::CloseServiceHandle( hSC);
            return STOP_SERVICE_ERROR;
        }
        // 等待服务停止
        while( ::QueryServiceStatus( hSvc, &status) == TRUE)
        {
            ::Sleep( status.dwWaitHint);
            if( status.dwCurrentState == SERVICE_STOPPED)
            {
                break;
            }
        }
    }
   
    // 启动服务
    if( ::StartService( hSvc, NULL, NULL) == FALSE)
    {
        ::CloseServiceHandle( hSvc);
        ::CloseServiceHandle( hSC);
        return START_SERVICE_ERROR;
    }
    // 等待服务启动
    while( ::QueryServiceStatus( hSvc, &status) == TRUE)
    {
        ::Sleep( status.dwWaitHint);
        if( status.dwCurrentState == SERVICE_RUNNING)
        {          
            break;
        }
    }
   
    ::CloseServiceHandle( hSvc);
    ::CloseServiceHandle( hSC);
    return SERVICE_NO_ERROR;
}