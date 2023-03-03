与关键段、读写锁等用户模式下的同步机制相比，内核对象唯一的缺点就是他们的性能。

几乎每一种内核对象都可以用来作为线程同步的工具，
因为这些内核对象都要么处于触发状态，要么处于非触发状态，
而有这两种状态，就能够应付大多数的线程同步问题了。

下面这些内核对象既可以处于触发状态，也可以处于未触发状态：
  进程、线程、事件、信号量、互斥量、
  作业、文件及控制台的标准输入/输出/错误流、可等待的计时器
  其中，事件、信号量、互斥量、可等待计时器是系统专门为线程同步而提供的机制。
  
等待函数
  等待函数使一个线程主动进入等待状态，直到指定的内核对象被触发为止。
  如果相应的内核对象在这之前已经处于触发状态了，则等待换函数就不会进入等待状态了。
  DWORD WaitForSingleObject(HANDLE hHandle, DWORD dwMilliseconds);  
    第二个参数指定最长等待时间，可以为INFINITE.
    如果等待的对象被触发，返回值为WAIT_OBJECT_0；如果超时，返回WAIT_TIMEOUT；如果输入参数无效，返回WAIT_FAILD；
  DWORD WaitForMultipleObjects(  DWORD nCount,   CONST HANDLE* lpHandles, 
                                 BOOL fWaitAll,   DWORD dwMilliseconds );
    nCount表示希望等待的内核对象数量，最大值为64，lpHandles为要等待的内核对象的句柄的数组
    fWaitAll指定是要等待所有对象都触发才返回，还是有一个触发就返回，最后一个参数指明等待超时时间。
    如果fWaitAll指明为TRUE，则所有对象都触发后，函数返回WAIT_OBJECT_0，
    如果fWaitAll指明为FALSE，则数组中的第n个（从第0个算起）对象被触发，返回 WAIT_OBJECT_0 + n 。

等待成功引起的副作用
  等待成功（返回WAIT_OBJECT_0的相对值）对某些内核对象会有不同的副作用，
  如自动重置对象，在函数成功返回之前（也就是在等待函数内部），他会将自动重置对象的触发状态设置为非触发状态，
  对不同的内核对象有不同的副作用，对有的内核对象（如进程、线程），则完全没有副作用。
    
事件内核对象 
  在所有的内核对象中，最简单的应该就是事件内核对象了
  事件包含三个元素：
    一个使用计数（这一点和所有的其它内核对象一样）
    一个表示事件是自动重置，还是手动重置的布尔值
    一个表示事件是否被触发的布尔值
  当一个手动重置的事件被触发时，所有等待的线程都将变为可调度状态，
  而一个自动重置事件被触发的时候，则只有一个等待该事件的线程会变为可调度状态
  等待函数的返回后，会将那些自动重置的事件改为未触发状态（等待函数的副作用）
  函数：
    HANDLE CreateEvent(LPSECURITY_ATTRIBUTES lpEventAttributes, BOOL bManualReset, BOOL bInitialState, LPTSTR lpName );
    HANDLE CreateEventEx(LPSECURITY_ATTRIBUTES lpEventAttributes, LPCTSTR lpName, DWORD dwFlags, DWORD dwDesiredAccess);
    HANDLE OpenEvent(DWORD dwDesiredAccess, BOOL bInheritHandle, LPCTSTR lpName ); 
	BOOL CloseHandle(HANDLE hObject); 
    BOOL SetEvent(HANDLE hEvent); 
    BOOL ResetEvent(HANDLE hEvent); 
    BOOL PulseEvent(HANDLE hEvent); 
  函数说明：
    安全属性参数lpEventAttributes在第三章介绍过了，bManualReset表示是否手动重置，bInitialState表示初始状态是否是触发的，
    dwFlags相当于把bInitialState和bManualReset整合到一块了，最低位对应bManualReset，倒数第二位对应bInitialState，
    dwDesiredAccess允许我们指定创建事件时，返回的句柄（对事件）具有何种访问权限，而CreateEvent总是授予全部权限。
    dwDesiredAccess在系统中已经有同名事件对象时，体现最为明显，CreateEvent只有在能拿到该同名对象全部权限的情况下才会成功返回。
    当不再使用事件内核对象时，应该使用CloseHandle函数来关闭它。SetEvent和ResetEvent设置对象的触发与非触发状态。
    对自动重置对象来说，通常不需要调用ResetEvent，等待函数会自动将事件重置。
    PulseEvent会短暂的将事件设为触发状态然后立马将其恢复为未触发状态，这相当于调用SetEvent之后紧跟着调用ResetEvent一样，
    对手动重置事件调用PulseEvent，当事件被脉冲触发的时候，仍是让所有等待该事件的线程都变为可调度状态，
    对自动重置事件调用PulseEvent，当事件被脉冲触发的时候，仍是只有一个等待该事件的线程变为可调度状态。
    实际PulseEvent用处不大，平时较少使用。
      
可等待的计时器内核对象     
  可等待内核对象其实跟事件内核对象差不多，
  只是他不是立即出发的，而是可以等待一段时间触发，或者循环等待触发。
  函数：
	HANDLE WINAPI CreateWaitableTimer(LPSECURITY_ATTRIBUTES lpTimerAttributes,BOOL bManualReset,LPCTSTR lpTimerName);
	HANDLE WINAPI OpenWaitableTimer(DWORD dwDesiredAccess,BOOL bInheritHandle,LPCTSTR lpTimerName);
	BOOL WINAPI SetWaitableTimer(HANDLE hTimer,const LARGE_INTEGER* pDueTime,LONG lPeriod,
							     PTIMERAPCROUTINE pfnCompletionRoutine,LPVOID lpArgToCompletionRoutine,BOOL fResume);
	BOOL WINAPI CancelWaitableTimer(HANDLE hTimer);
	BOOL CloseHandle(HANDLE hObject); 	
  函数说明：
	创建时，bManualReset参数设置手动重置，还是自动重置，手动时，所有等待该计时器的线程都会变成可调度的，
	自动时，将只会有一个变成可调度的（该线程的等待函数会重置该计时器为未触发状态）。
	计时器对象创建时总是未触发的，如果触发，只能使用SetWaitableTimer方法，
	pDueTime既可以传入正值，也可以传入负值，当传入正值时，表示的UTC时间，传入负值时，表示的是相对时间，
	LARGE_INTEGER和FILETIME结构一致（都是由两个四字节数构成），但前者要求8字节对齐，而后者指要求4字节对齐就可以，
	得到pDueTime值的方法可为：
		struct SYSTEMTIME {   
			WORD wYear; WORD wMonth; WORD wDayOfWeek; WORD wDay;   
			WORD wHour; WORD wMinute; WORD wSecond; WORD wMilliseconds; };	//跟struct tm结构不一样
		void GetSystemTime(LPSYSTEMTIME lpSystemTime); 	//得到系统时间，也可以手动指定一个未来的时间
		BOOL SystemTimeToFileTime(const SYSTEMTIME* lpSystemTime, LPFILETIME lpFileTime); //获取的本地时区时间
		BOOL LocalFileTimeToFileTime(const FILETIME* lpLocalFileTime, LPFILETIME lpFileTime); 	//转为UTC时间
	pDueTime传入负值时，表示从当前时间算起，多久后第一次触发定时器对象，以0.1微秒为单位。
	lPeriod表从定时器触发后，每隔多少时间触发一次，单位为微秒，如果为0，表就触发一次。
	fResume如果为TRUE，而且系统支持电源管理，那么在计时器触发的时候，系统会退出省电模式。
	如设为TRUE，但系统不支持省电模式，GetLastError就会返回ERROR_NOT_SUPPORTED。一般设为FALSE。
	pfnCompletionRoutine和lpArgToCompletionRoutine是设置回调函数及回调函数参数用的，一般不用，传NULL即可。
	用CancelWaitableTimer取消计时器后，那之前SetWaitableTimer设置的那些定时参数就不管用了，
	如果想让计时器再次能用（触发），需要用SetWaitableTimer重新设置计时器的相关计时参数。
	定时器内核对象与用户定时器相比，不需要用户界面基础设施(指定窗口句柄),而且是可以跨线程/进程的。

信号量内核对象	
  与其它内核对象相同，它也包含一个使用计数器，
  但它还包含另外两个32位值：一个最大资源计数、一个当前资源计数。这两个值都是可指定的。
  函数：
	HANDLE CreateSemaphore(LPSECURITY_ATTRIBUTES lpSemaphoreAttributes, 
						   LONG lInitialCount, LONG lMaximumCount, LPCTSTR lpName );
    HANDLE CreateSemaphoreEx(LPSECURITY_ATTRIBUTES lpSemaphoreAttributes,
							 LONG lInitialCount,LONG lMaximumCount,LPCTSTR lpName, 
							 DWORD dwFlags,DWORD dwDesiredAccess);
	HANDLE OpenSemaphore(DWORD dwDesiredAccess,BOOL bInheritHandle,LPCTSTR lpName);
	BOOL ReleaseSemaphore(HANDLE hSemaphore,LONG lReleaseCount,LPLONG lpPreviousCount);
  函数说明：
	CreateSemaphoreEx的dwFlags参数是系统保留的，应设为0，其它的参数基本都和事件内核对象的相关函数一样，
	ReleaseSemaphore的lpPreviousCount是个输出参数，返回的是原始的资源数，
	ReleaseSemaphore中通过让lReleaseCount=0来获取信号量的当前值是不可行的，
	也就是说，没有办法在不改变当前信号量值的情况下，就可以获取其原始值。
	当信号量的值>0的情况下，等待函数的成功执行会消耗掉信号量的一个计数值（等待函数成功执行的副作用）。
	
互斥量内核对象
  互斥量内核对象包含一个使用计数、一个线程ID以及一个递归计数。线程ID表示当前占用这个互斥量的是系统中的哪个线程，
  递归计数表示这个线程占用该互斥量的次数。
  互斥量的规则：
	线程ID=0，表无效线程，意味着当前无线程占用该互斥量（线程释放了该互斥量），此时他处于触发状态。
	线程ID != 0,表有线程占用了该互斥量，此时它处于未触发状态。
	与所有其它内核对象都不同的是，互斥量具有“线程所有权”的概念。
  函数：
	HANDLE CreateMutex(LPSECURITY_ATTRIBUTES lpMutexAttributes, BOOL bInitialOwner, LPCTSTR lpName);
	HANDLE WINAPI CreateMutexEx(LPSECURITY_ATTRIBUTES lpMutexAttributes, LPCTSTR lpName, 
								DWORD dwFlags, DWORD dwDesiredAccess);
	HANDLE WINAPI OpenMutex(DWORD dwDesiredAccess, BOOL bInheritHandle, LPCTSTR lpName);
	BOOL ReleaseMutex(HANDLE hMutex);
  函数说明：
    CreateMutex中的bInitialOwner，如果传TRUE，那个互斥量对象的线程ID将被设为调用线程的ID，递归计数设为1，
	如此创建的互斥量对象处于非触发状态。如果一个线程等待一个互斥量，如果互斥量记录的线程ID是本线程的，
	则直接结束等待，并是互斥量对象的递归计数增1。如果线程等待的互斥量的线程ID与本线程不一致（ID != 0），
	则只有互斥量对象的递归计数变为0后（互斥量的线程ID也会跟着变为0），等待函数才会成功结束等待。
	CreateMutexEx中的dwFlags对应CreateMutex中的bInitialOwner。ReleaseMutex用以释放一次互斥量（递归计数减1），
	但这个函数也是线程相关的，如果互斥量的线程ID与本线程ID不一致，则ReleaseMutex函数返回失败。
	如果占用互斥量的线程在完全释放该互斥量之前终止，该互斥量相当于被遗弃了，
	则系统会把该互斥量的ID设为0，递归计数变为0，使其处于触发状态。
	如果是因为这种情况而引起的互斥量对象被触发，则等待函数虽然也是等待成功返回，但返回值不是WAIT_OBJECT_0了，
	而是WAIT_ABANDONED，表这个互斥量是因被线程遗弃而触发的，这也是互斥量对象才特有的情况。
	实际中很少会有线程遗弃互斥量的情况，所以这种情况在大多数程序中不会被考略。
	
其它线程同步函数：
  
  