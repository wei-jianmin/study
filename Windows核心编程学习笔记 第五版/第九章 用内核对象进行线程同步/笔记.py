��ؼ��Ρ���д�����û�ģʽ�µ�ͬ��������ȣ��ں˶���Ψһ��ȱ��������ǵ����ܡ�

����ÿһ���ں˶��󶼿���������Ϊ�߳�ͬ���Ĺ��ߣ�
��Ϊ��Щ�ں˶���Ҫô���ڴ���״̬��Ҫô���ڷǴ���״̬��
����������״̬�����ܹ�Ӧ����������߳�ͬ�������ˡ�

������Щ�ں˶���ȿ��Դ��ڴ���״̬��Ҳ���Դ���δ����״̬��
  ���̡��̡߳��¼����ź�������������
  ��ҵ���ļ�������̨�ı�׼����/���/���������ɵȴ��ļ�ʱ��
  ���У��¼����ź��������������ɵȴ���ʱ����ϵͳר��Ϊ�߳�ͬ�����ṩ�Ļ��ơ�
  
�ȴ�����
  �ȴ�����ʹһ���߳���������ȴ�״̬��ֱ��ָ�����ں˶��󱻴���Ϊֹ��
  �����Ӧ���ں˶�������֮ǰ�Ѿ����ڴ���״̬�ˣ���ȴ��������Ͳ������ȴ�״̬�ˡ�
  DWORD WaitForSingleObject(HANDLE hHandle, DWORD dwMilliseconds);  
    �ڶ�������ָ����ȴ�ʱ�䣬����ΪINFINITE.
    ����ȴ��Ķ��󱻴���������ֵΪWAIT_OBJECT_0�������ʱ������WAIT_TIMEOUT��������������Ч������WAIT_FAILD��
  DWORD WaitForMultipleObjects(  DWORD nCount,   CONST HANDLE* lpHandles, 
                                 BOOL fWaitAll,   DWORD dwMilliseconds );
    nCount��ʾϣ���ȴ����ں˶������������ֵΪ64��lpHandlesΪҪ�ȴ����ں˶���ľ��������
    fWaitAllָ����Ҫ�ȴ����ж��󶼴����ŷ��أ�������һ�������ͷ��أ����һ������ָ���ȴ���ʱʱ�䡣
    ���fWaitAllָ��ΪTRUE�������ж��󶼴����󣬺�������WAIT_OBJECT_0��
    ���fWaitAllָ��ΪFALSE���������еĵ�n�����ӵ�0�����𣩶��󱻴��������� WAIT_OBJECT_0 + n ��

�ȴ��ɹ�����ĸ�����
  �ȴ��ɹ�������WAIT_OBJECT_0�����ֵ����ĳЩ�ں˶�����в�ͬ�ĸ����ã�
  ���Զ����ö����ں����ɹ�����֮ǰ��Ҳ�����ڵȴ������ڲ��������Ὣ�Զ����ö���Ĵ���״̬����Ϊ�Ǵ���״̬��
  �Բ�ͬ���ں˶����в�ͬ�ĸ����ã����е��ں˶�������̡��̣߳�������ȫû�и����á�
    
�¼��ں˶��� 
  �����е��ں˶����У���򵥵�Ӧ�þ����¼��ں˶�����
  �¼���������Ԫ�أ�
    һ��ʹ�ü�������һ������е������ں˶���һ����
    һ����ʾ�¼����Զ����ã������ֶ����õĲ���ֵ
    һ����ʾ�¼��Ƿ񱻴����Ĳ���ֵ
  ��һ���ֶ����õ��¼�������ʱ�����еȴ����̶߳�����Ϊ�ɵ���״̬��
  ��һ���Զ������¼���������ʱ����ֻ��һ���ȴ����¼����̻߳��Ϊ�ɵ���״̬
  �ȴ������ķ��غ󣬻Ὣ��Щ�Զ����õ��¼���Ϊδ����״̬���ȴ������ĸ����ã�
  ������
    HANDLE CreateEvent(LPSECURITY_ATTRIBUTES lpEventAttributes, BOOL bManualReset, BOOL bInitialState, LPTSTR lpName );
    HANDLE CreateEventEx(LPSECURITY_ATTRIBUTES lpEventAttributes, LPCTSTR lpName, DWORD dwFlags, DWORD dwDesiredAccess);
    HANDLE OpenEvent(DWORD dwDesiredAccess, BOOL bInheritHandle, LPCTSTR lpName ); 
	BOOL CloseHandle(HANDLE hObject); 
    BOOL SetEvent(HANDLE hEvent); 
    BOOL ResetEvent(HANDLE hEvent); 
    BOOL PulseEvent(HANDLE hEvent); 
  ����˵����
    ��ȫ���Բ���lpEventAttributes�ڵ����½��ܹ��ˣ�bManualReset��ʾ�Ƿ��ֶ����ã�bInitialState��ʾ��ʼ״̬�Ƿ��Ǵ����ģ�
    dwFlags�൱�ڰ�bInitialState��bManualReset���ϵ�һ���ˣ����λ��ӦbManualReset�������ڶ�λ��ӦbInitialState��
    dwDesiredAccess��������ָ�������¼�ʱ�����صľ�������¼������к��ַ���Ȩ�ޣ���CreateEvent��������ȫ��Ȩ�ޡ�
    dwDesiredAccess��ϵͳ���Ѿ���ͬ���¼�����ʱ��������Ϊ���ԣ�CreateEventֻ�������õ���ͬ������ȫ��Ȩ�޵�����²Ż�ɹ����ء�
    ������ʹ���¼��ں˶���ʱ��Ӧ��ʹ��CloseHandle�������ر�����SetEvent��ResetEvent���ö���Ĵ�����Ǵ���״̬��
    ���Զ����ö�����˵��ͨ������Ҫ����ResetEvent���ȴ��������Զ����¼����á�
    PulseEvent����ݵĽ��¼���Ϊ����״̬Ȼ��������ָ�Ϊδ����״̬�����൱�ڵ���SetEvent֮������ŵ���ResetEventһ����
    ���ֶ������¼�����PulseEvent�����¼������崥����ʱ�����������еȴ����¼����̶߳���Ϊ�ɵ���״̬��
    ���Զ������¼�����PulseEvent�����¼������崥����ʱ������ֻ��һ���ȴ����¼����̱߳�Ϊ�ɵ���״̬��
    ʵ��PulseEvent�ô�����ƽʱ����ʹ�á�
      
�ɵȴ��ļ�ʱ���ں˶���     
  �ɵȴ��ں˶�����ʵ���¼��ں˶����࣬
  ֻ�����������������ģ����ǿ��Եȴ�һ��ʱ�䴥��������ѭ���ȴ�������
  ������
	HANDLE WINAPI CreateWaitableTimer(LPSECURITY_ATTRIBUTES lpTimerAttributes,BOOL bManualReset,LPCTSTR lpTimerName);
	HANDLE WINAPI OpenWaitableTimer(DWORD dwDesiredAccess,BOOL bInheritHandle,LPCTSTR lpTimerName);
	BOOL WINAPI SetWaitableTimer(HANDLE hTimer,const LARGE_INTEGER* pDueTime,LONG lPeriod,
							     PTIMERAPCROUTINE pfnCompletionRoutine,LPVOID lpArgToCompletionRoutine,BOOL fResume);
	BOOL WINAPI CancelWaitableTimer(HANDLE hTimer);
	BOOL CloseHandle(HANDLE hObject); 	
  ����˵����
	����ʱ��bManualReset���������ֶ����ã������Զ����ã��ֶ�ʱ�����еȴ��ü�ʱ�����̶߳����ɿɵ��ȵģ�
	�Զ�ʱ����ֻ����һ����ɿɵ��ȵģ����̵߳ĵȴ����������øü�ʱ��Ϊδ����״̬����
	��ʱ�����󴴽�ʱ����δ�����ģ����������ֻ��ʹ��SetWaitableTimer������
	pDueTime�ȿ��Դ�����ֵ��Ҳ���Դ��븺ֵ����������ֵʱ����ʾ��UTCʱ�䣬���븺ֵʱ����ʾ�������ʱ�䣬
	LARGE_INTEGER��FILETIME�ṹһ�£��������������ֽ������ɣ�����ǰ��Ҫ��8�ֽڶ��룬������ָҪ��4�ֽڶ���Ϳ��ԣ�
	�õ�pDueTimeֵ�ķ�����Ϊ��
		struct SYSTEMTIME {   
			WORD wYear; WORD wMonth; WORD wDayOfWeek; WORD wDay;   
			WORD wHour; WORD wMinute; WORD wSecond; WORD wMilliseconds; };	//��struct tm�ṹ��һ��
		void GetSystemTime(LPSYSTEMTIME lpSystemTime); 	//�õ�ϵͳʱ�䣬Ҳ�����ֶ�ָ��һ��δ����ʱ��
		BOOL SystemTimeToFileTime(const SYSTEMTIME* lpSystemTime, LPFILETIME lpFileTime); //��ȡ�ı���ʱ��ʱ��
		BOOL LocalFileTimeToFileTime(const FILETIME* lpLocalFileTime, LPFILETIME lpFileTime); 	//תΪUTCʱ��
	pDueTime���븺ֵʱ����ʾ�ӵ�ǰʱ�����𣬶�ú��һ�δ�����ʱ��������0.1΢��Ϊ��λ��
	lPeriod��Ӷ�ʱ��������ÿ������ʱ�䴥��һ�Σ���λΪ΢�룬���Ϊ0����ʹ���һ�Ρ�
	fResume���ΪTRUE������ϵͳ֧�ֵ�Դ������ô�ڼ�ʱ��������ʱ��ϵͳ���˳�ʡ��ģʽ��
	����ΪTRUE����ϵͳ��֧��ʡ��ģʽ��GetLastError�ͻ᷵��ERROR_NOT_SUPPORTED��һ����ΪFALSE��
	pfnCompletionRoutine��lpArgToCompletionRoutine�����ûص��������ص����������õģ�һ�㲻�ã���NULL���ɡ�
	��CancelWaitableTimerȡ����ʱ������֮ǰSetWaitableTimer���õ���Щ��ʱ�����Ͳ������ˣ�
	������ü�ʱ���ٴ����ã�����������Ҫ��SetWaitableTimer�������ü�ʱ������ؼ�ʱ������
	��ʱ���ں˶������û���ʱ����ȣ�����Ҫ�û����������ʩ(ָ�����ھ��),�����ǿ��Կ��߳�/���̵ġ�

�ź����ں˶���	
  �������ں˶�����ͬ����Ҳ����һ��ʹ�ü�������
  ������������������32λֵ��һ�������Դ������һ����ǰ��Դ������������ֵ���ǿ�ָ���ġ�
  ������
	HANDLE CreateSemaphore(LPSECURITY_ATTRIBUTES lpSemaphoreAttributes, 
						   LONG lInitialCount, LONG lMaximumCount, LPCTSTR lpName );
    HANDLE CreateSemaphoreEx(LPSECURITY_ATTRIBUTES lpSemaphoreAttributes,
							 LONG lInitialCount,LONG lMaximumCount,LPCTSTR lpName, 
							 DWORD dwFlags,DWORD dwDesiredAccess);
	HANDLE OpenSemaphore(DWORD dwDesiredAccess,BOOL bInheritHandle,LPCTSTR lpName);
	BOOL ReleaseSemaphore(HANDLE hSemaphore,LONG lReleaseCount,LPLONG lpPreviousCount);
  ����˵����
	CreateSemaphoreEx��dwFlags������ϵͳ�����ģ�Ӧ��Ϊ0�������Ĳ������������¼��ں˶������غ���һ����
	ReleaseSemaphore��lpPreviousCount�Ǹ�������������ص���ԭʼ����Դ����
	ReleaseSemaphore��ͨ����lReleaseCount=0����ȡ�ź����ĵ�ǰֵ�ǲ����еģ�
	Ҳ����˵��û�а취�ڲ��ı䵱ǰ�ź���ֵ������£��Ϳ��Ի�ȡ��ԭʼֵ��
	���ź�����ֵ>0������£��ȴ������ĳɹ�ִ�л����ĵ��ź�����һ������ֵ���ȴ������ɹ�ִ�еĸ����ã���
	
�������ں˶���
  �������ں˶������һ��ʹ�ü�����һ���߳�ID�Լ�һ���ݹ�������߳�ID��ʾ��ǰռ���������������ϵͳ�е��ĸ��̣߳�
  �ݹ������ʾ����߳�ռ�øû������Ĵ�����
  �������Ĺ���
	�߳�ID=0������Ч�̣߳���ζ�ŵ�ǰ���߳�ռ�øû��������߳��ͷ��˸û�����������ʱ�����ڴ���״̬��
	�߳�ID != 0,�����߳�ռ���˸û���������ʱ������δ����״̬��
	�����������ں˶��󶼲�ͬ���ǣ����������С��߳�����Ȩ���ĸ��
  ������
	HANDLE CreateMutex(LPSECURITY_ATTRIBUTES lpMutexAttributes, BOOL bInitialOwner, LPCTSTR lpName);
	HANDLE WINAPI CreateMutexEx(LPSECURITY_ATTRIBUTES lpMutexAttributes, LPCTSTR lpName, 
								DWORD dwFlags, DWORD dwDesiredAccess);
	HANDLE WINAPI OpenMutex(DWORD dwDesiredAccess, BOOL bInheritHandle, LPCTSTR lpName);
	BOOL ReleaseMutex(HANDLE hMutex);
  ����˵����
    CreateMutex�е�bInitialOwner�������TRUE���Ǹ�������������߳�ID������Ϊ�����̵߳�ID���ݹ������Ϊ1��
	��˴����Ļ����������ڷǴ���״̬�����һ���̵߳ȴ�һ���������������������¼���߳�ID�Ǳ��̵߳ģ�
	��ֱ�ӽ����ȴ������ǻ���������ĵݹ������1������̵߳ȴ��Ļ��������߳�ID�뱾�̲߳�һ�£�ID != 0����
	��ֻ�л���������ĵݹ������Ϊ0�󣨻��������߳�IDҲ����ű�Ϊ0�����ȴ������Ż�ɹ������ȴ���
	CreateMutexEx�е�dwFlags��ӦCreateMutex�е�bInitialOwner��ReleaseMutex�����ͷ�һ�λ��������ݹ������1����
	���������Ҳ���߳���صģ�������������߳�ID�뱾�߳�ID��һ�£���ReleaseMutex��������ʧ�ܡ�
	���ռ�û��������߳�����ȫ�ͷŸû�����֮ǰ��ֹ���û������൱�ڱ������ˣ�
	��ϵͳ��Ѹû�������ID��Ϊ0���ݹ������Ϊ0��ʹ�䴦�ڴ���״̬��
	�������Ϊ�������������Ļ��������󱻴�������ȴ�������ȻҲ�ǵȴ��ɹ����أ�������ֵ����WAIT_OBJECT_0�ˣ�
	����WAIT_ABANDONED������������������߳������������ģ���Ҳ�ǻ�������������е������
	ʵ���к��ٻ����߳������������������������������ڴ���������в��ᱻ���ԡ�
	
�����߳�ͬ��������
  
  