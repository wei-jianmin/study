//����Ŀ����Ϊ���ֽ�
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
	//��������������Ϊ�ȴ�������0Ϊ���޵ȴ�,���һ������Ϊ�Ƿ�����
	return resp;
}

//1. ��������������������ʱָ���Ĳ���
int main(int argc, char *argv[])
{
	char tmp_buf[50]={0};
	for(int i=0;i<argc;i++)
	{
		sprintf(tmp_buf,"main ��%d/%d������",i,argc);
		show_msg(tmp_buf,argv[i]);
	}
#if 1					//���ж������ʱ�������ñȽϷ���
	SERVICE_TABLE_ENTRY tbls[2];
	tbls[0].lpServiceName = "SERV BY WJM";   //��ΪNULL�����������˶������ʱ����ô��������ָ��
	tbls[0].lpServiceProc = (LPSERVICE_MAIN_FUNCTIONA)myproc;
	tbls[1].lpServiceName = NULL;
	tbls[1].lpServiceProc = NULL;   //һ��������ܰ������ɸ����񡣷��ɱ�����һ��������򶼱���Ϊ NULL ָ��

	//��������Ŀ��Ʒ��ɻ��̣߳������ɱ������еķ���ִ����֮�󣨷���Ϊֹͣ״̬������������ʱ���󣬸ú������÷��أ�������ֹ��
	StartServiceCtrlDispatcher(tbls);
#else
	myproc(0,NULL);		//��ֻ��һ������ʱ������ֱ��������
#endif
}

//2. ��������������������ʱָ���Ĳ���
VOID WINAPI myproc(DWORD   dwNumServicesArgs,LPSTR   *lpServiceArgVectors)
{
	char tmp_buf[50]={0};
	for(int i=0;i<dwNumServicesArgs;i++)
	{
		sprintf(tmp_buf,"myproc ��%d/%d������",i,dwNumServicesArgs);
		show_msg(tmp_buf,lpServiceArgVectors[i]);
	}
	// 1: Ϊ����ע�������������ʵ���Զ�����������
	show_msg("myproc","ע����ƴ���������");
	hServiceStatusHandle = RegisterServiceCtrlHandler("SERV BY WJM", my_handle_func);  //Ϊ����ע����ƴ�������������һ��Ӧ�þ���õ�ִ��

	// 2�����÷����ڹ���״̬�������һЩ��ʼ��֮��Ĺ���
	ServiceStatus.dwServiceType        = SERVICE_WIN32;			 //һ�㶼��Ϊ��ֵ����
	ServiceStatus.dwCurrentState       = SERVICE_START_PENDING;  //�������𣬴�״̬�²�����ܿ���ָ��������my_handle_func��������
	ServiceStatus.dwControlsAccepted   = SERVICE_ACCEPT_STOP | SERVICE_ACCEPT_SHUTDOWN | SERVICE_ACCEPT_PAUSE_CONTINUE;  //�ɽ�����Щ���͵�ָ��
	ServiceStatus.dwWin32ExitCode      = 0;      //���뷵�ش���Ӧ��ΪERROR_SERVICE_SPECIFIC_ERROR ������dwServiceSpecificExitCode�д��Ŵ�����
	ServiceStatus.dwServiceSpecificExitCode = 0; //����������ʱ�����񷵻ظô�����
	ServiceStatus.dwCheckPoint         = 0;      //����Ľ�չ״ֵ̬������������ʱӦ��������ʼ����ÿһ��ʱ������ֵ��������û��������ֹͣ����ͣ���������ʱ�����ֵӦ������
		//dwWaitHintָʾ�´μ��ʱ�䣺������������ֹͣ����ͣ�������������Ĺ���ʱ�䣬�Ժ���ơ�
		//��ָ����ʱ������ȥ֮ǰ������Ӧ�ö�SetServiceStatus����������һ�ε��ã�������dwCheckPointֵ��ı�dwCurrentState��
		//�����dwWaitHintָ����ʱ������ȥ�ˣ���dwCheckPointû�б����ӻ�dwCurrentStateû�иı䣬
		//������ƹ������������Ƴ��������Ϊ�����˴���Ӧ��ֹͣ�÷���
		//Ȼ��������÷���������������һ�����̣�������ƹ�����������ֹ�÷��������Ϊ��Ҳ������ֹ����ý��̵���������
		//ʵ�ʲ��ԣ����ı�dwCheckPoint��ֵ
	ServiceStatus.dwWaitHint           = 200;  
	SetServiceStatus(hServiceStatusHandle, &ServiceStatus);
	show_msg("myproc","ʹ�����ڹ���״̬");


	// 3����ɳ�ʼ������
	//......��ʼ������.........//
	show_msg("myproc","��ɳ�ʼ������");
	
	// 4. �ı�״̬Ϊ����״̬
	ServiceStatus.dwCurrentState       = SERVICE_RUNNING;
	ServiceStatus.dwCheckPoint         = 1;
	ServiceStatus.dwWaitHint           = 5000;  
	SetServiceStatus(hServiceStatusHandle, &ServiceStatus);
	show_msg("myproc","ʹ����������״̬");


	// 5. ѭ��
	stop_flag = false;
	unsigned int count = 1;
	while(1)
	{
		Sleep(1000);
		
		if(stop_flag)
		{
			show_msg("����","���񼴽�ֹͣ");
			//��my_handle_func�������˷���״̬
			return;
		}
		else
		{
			count++;
			ServiceStatus.dwCheckPoint         = count;
			show_msg("����","���������ڰ���ȷ����ť");
			SetServiceStatus(hServiceStatusHandle, &ServiceStatus);
		}
	}

	//�߳������Ľ�����ʽӦ����������״̬ΪSERVICE_STOPPED��Ȼ������̣߳�������Ǳ��̣߳�����ѭ����ȴ����߳��˳�������Ӧ�ñ������� ExitThread �����߳�
}

//3. ���ƴ������봦����� Windows ��Ϣ�Ĵ��ڻص������ǳ����ƣ������ SCM ������ʲô���󲢲�ȡ��Ӧ�ж�
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
	show_msg("myproc","ʹ������ֹͣ״̬");
}

/* �����в�������
	sc create aaabbb binPath= F:\VSProjects\aaa\Win32\Debug\aaa.exe
	sc start aaabbb
	sc stop aaabbb
	sc delete aaabbb
*/

//���Դ���������ϵͳ����
bool TestStartService()
{
	//�򿪷�����ƹ�����
	SC_HANDLE hScm = OpenSCManager(NULL, NULL, SC_MANAGER_CREATE_SERVICE);
	if (hScm == NULL)
	{
		return false;
	}
	//����ϵͳ���񣬲����ܶ࣬�ɲ鿴�����ĵ�
	SC_HANDLE hService = CreateService(hScm, "MySerivce", "MyService", SERVICE_ALL_ACCESS,
		SERVICE_WIN32_OWN_PROCESS, SERVICE_AUTO_START, SERVICE_ERROR_NORMAL, GetExeFullPath(), 
		NULL, NULL, "", NULL, "");
	if (hService == NULL)
	{
		return false;
	}
	//����ϵͳ����
	if (StartService(hService, 0, NULL) == false)
	{
		return false;
	}
	//�ͷž��
	CloseServiceHandle(hScm);
	CloseServiceHandle(hService);
	return true;
}


//ͨ��������������
#define SERVICE_NO_ERROR 0
#define OPEN_SCMANAGER_ERROR 2
#define OPEN_SERVICE_ERROR 3
#define QUERY_SERVICESTATUS_ERROR 4
#define STOP_SERVICE_ERROR 5
#define START_SERVICE_ERROR 6
  
int RestartService()
{
 
    // �򿪷���������
    SC_HANDLE hSC = ::OpenSCManager( NULL,
        NULL, GENERIC_EXECUTE);
    if( hSC == NULL)
    {      
        return OPEN_SCMANAGER_ERROR;
    }
    // ��apache����
    SC_HANDLE hSvc = ::OpenService( hSC, "apache",
        SERVICE_START | SERVICE_QUERY_STATUS | SERVICE_STOP);
    if( hSvc == NULL)
    {
        ::CloseServiceHandle( hSC);
        return OPEN_SERVICE_ERROR;
    }
    // ��÷����״̬
    SERVICE_STATUS status;
    if( ::QueryServiceStatus( hSvc, &status) == FALSE)
    {
        ::CloseServiceHandle( hSvc);
        ::CloseServiceHandle( hSC);
        return QUERY_SERVICESTATUS_ERROR;
    }
    //�����������״̬��ֹͣ����
    if( status.dwCurrentState == SERVICE_RUNNING)
    {
        // ֹͣ����
        if( ::ControlService( hSvc,
            SERVICE_CONTROL_STOP, &status) == FALSE)
        {
            ::CloseServiceHandle( hSvc);
            ::CloseServiceHandle( hSC);
            return STOP_SERVICE_ERROR;
        }
        // �ȴ�����ֹͣ
        while( ::QueryServiceStatus( hSvc, &status) == TRUE)
        {
            ::Sleep( status.dwWaitHint);
            if( status.dwCurrentState == SERVICE_STOPPED)
            {
                break;
            }
        }
    }
   
    // ��������
    if( ::StartService( hSvc, NULL, NULL) == FALSE)
    {
        ::CloseServiceHandle( hSvc);
        ::CloseServiceHandle( hSC);
        return START_SERVICE_ERROR;
    }
    // �ȴ���������
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