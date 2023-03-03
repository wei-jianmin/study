Interlocked系列函数会以原子的方式来操控一个值
  LONG InterlockedIncrement( IN PLONG  Addend );  //普通的变量加减操作，可以对应的不止一条汇编语句
  LONG InterlockedDecrement( IN PLONG  Addend );
  LONG   InterlockedExchangeAdd(IN OUT PLONG  Addend, IN LONG  Value);   //返回值是改变前的值
  LONGLONG __cdecl InterlockedExchangeAdd64(__in_out LONGLONG volatile* Addend, __in LONGLONG Value);  //返回值是改变前的值
  LONG InterlockedCompareExchange(IN OUT PLONG  Destination, IN LONG  Exchange, IN LONG  Comparand );
  PVOID InterlockedCompareExchangePointer( IN OUT PVOID  *Destination, IN PVOID  Exchange, IN PVOID  Comparand );
  InterlockedCompareExchange执行的操作：
      old_val = *Destination; 
      if(*Destination==Comparand) *Destination=Exchange; 
      return old_val;
  我们必须确保传给这些函数的变量地址是经过对齐的，否则这些函数可能会失效，
  C运行库提供了一个_aligned_malloc函数，我们可以用这个函数来分配一块对齐过的内存。
  void * _aligned_malloc(size_t size, size_t alignment); alignment表示要对齐到的字节边界，应该 = 2^N (N = 1、2、3 ...)
  Interlocked系列函数并不会在用户态和内核态之间转换，而是执行的非常快（通常小于50个CPU周期）。
  
线程同步：  
Interlocked系列函数值适用于修改一个值的情形，如果要以原子方式访问复杂的数据结构，就得选择其他的方式。  
思路：
  当线程想要访问共享资源，或是想要得到一些“特殊事件”的通知时，
  线程调用系统方法，并将线程等待的资源以参数形式传入。
  当条件当前不满足时，系统把当前线程挂起（对线程来说，相当于阻塞住了），等条件满足了，再唤醒该线程。
方案： 
  ● 关键段
    函数：
      CRITICAL_SECTION global_cs;
      void InitializeCriticalSection(PCRITICAL_SECTION pcs);  //调用EnterCriticalSection之前必须调用调用这个函数
      void EnterCriticalSection(PCRITICAL_SECTION pcs);
      BOOL TryEnterCriticalSection(PCRITICAL_SECTION pcs);    //类似EnterCriticalSection，只不过失败时返回FALSE，而不是引发等待
      void LeaveCriticalSection(PCRITICAL_SECTION pcs);
      void DeleteCriticalSection(LPCRITICAL_SECTION lpCriticalSection);   //对应InitializeCriticalSection，重置CRITICAL_SECTION
    函数说明；
      关键段不能用于多个进程之间的线程同步。
      只要还有一个线程还在使用关键段，就不应该调用DeleteCriticalSection来重置该关键段结构。
      EnterCriticalSection会挂起线程，但这个挂起时间不会是无限长的，
        注册表项HKEY_LOCAL_MACHINE/System/CurrentcontrolSet/Control/Session Manager中的CriticalSectionTimeout值决定其超时时间，
        这个值以秒为单位，一般是30天，可以自己设置，但不要弄得太小，比如小于3秒。
      使用TryEnterCriticalSection，当返回成功时，其效果与EnterCriticalSection是一致的，此时应该对应的调用LeaveCriticalSection。
      InitializeCriticalSection内部会有申请内存的操作（调试用），如果内存申请失败，函数抛出STATUS_NO_MEMORY异常。
        我们可以使用InitializeCriticalSectionAndSpinCount 函数来完成关键段初始化的操作，它的返回值是布尔型，内存分配失败时，返回FALSE
      只有当两个或多个线程争夺同一个关键段(同时调EnterCriticalSection)时，系统才会不得不创建一个事件内核对象，
        这样做的目的是节省系统资源，此后该事件内核对象一直存在，直到调用DeleteCriticalSection后，系统才会释放这个事件内核对象。
        在WinXp之前，如果因内存不足导致创建事件内核对象失败（极其罕见），则同时调EnterCriticalSection会抛出EXCEPTION_INVALID_HANDLE异常
  ● 读写锁(独占共享锁)
    适用场景：
      在读者写者模型中，有一个或多个线程对一块区域写操作，有多个线程对这块区域读操作。
      如果使用关键段保护该临界资源，则某个线程在读或者写的时候，其它线程都不能访问该临界资源，显然这有点低效。
      使用读写锁，则可以做到，某个线程在写的时候，其它线程都不能访问该临界资源，当某个线程读该临界资源时，其它读线程仍可以访问该临界资源。
    函数：    
      VOID WINAPI InitializeSRWLock(PSRWLOCK SRWLock);
      VOID WINAPI AcquireSRWLockExclusive(PSRWLOCK SRWLock);    //独占锁
      VOID WINAPI ReleaseSRWLockExclusive(PSRWLOCK SRWLock);
      VOID WINAPI AcquireSRWLockShared(PSRWLOCK SRWLock);       //共享锁
      VOID WINAPI ReleaseSRWLockShared(PSRWLOCK SRWLock);
    函数说明：
      写者应该使用独占锁，读者应该使用共享锁
      无法保证请求所有权的线程被授予所有权的顺序； SRW锁既不是公平的也不是FIFO。
      不存在像关键段那样TryEnter(Shared/Exclusive)SRWLock，如果锁被占用，则其它尝试获取锁的线程会被阻塞。
      不能嵌套的锁定同一个资源（这意味着死锁）
      不存在删除或销毁SRWLOCK的函数，系统会自动执行清理工作
      SRW是同步读写的意思
      typedef struct _RTL_SRWLOCK { PVOID Ptr; } SRWLOCK,*PSRWLOCK;
  ● 条件变量
    说明：
      并发有两大需求，一是互斥，二是等待。互斥是因为线程间存在共享数据，等待则是因为线程间存在依赖。
      前面的关键段和读写锁，都是解决线程对资源的互斥访问问题，而条件变量就是为了解决线程依赖的问题。
      为了防止竞争，条件变量总是和锁结（关键段/读写锁）一起使用。
    函数：
      VOID InitializeConditionVariable (PCONDITION_VARIABLE pConditionVariable);
      BOOL SleepConditionVariableCS(PCONDITION_VARIABLE pConditionVariable, PCRITICAL_SECTION pCriticalSection, DWORD dwMilliseconds);
      BOOL SleepConditionVariableSRW(PCONDITION_VARIABLE pConditionVariable, PSRWLOCK pSRWLock, DWORD dwMilliseconds, ULONG Flags);
      VOID WakeConditionVariable(PCONDITION_VARIABLE pConditionVariable);
      VOID WakeAllConditionVariable(PCONDITION_VARIABLE pConditionVariable);
    参数说明：
      pConditionVariable 指向一个已经初始化的条件变量
      pCriticalSection/pSRWLock 用以同步对共享资源的访问
      dwMilliseconds 最长等待时间，可以为INFINITE
      Flags 当条件被触发时，当前线程是独占锁（0），还是共享锁（CONDITION_VARIABLE_LOCKMODE_SHARED）
      在规定时间内条件未触发，函数返回FALSE
    函数说明：
      条件语句在条件不满足等待时（等待时间设为无限），会释放关键段或读写锁，但只是临时释放，当等待完成后还会获取锁
      当条件（因其它线程的触发）得到满足时，如果条件语句拿不回刚才释放的锁，
      则条件语句仍然等待（注意此时等待的不再是条件，而是等待锁），直到成功拿到锁之后，该条件语句才成功返回
      线程调用SleepConditionVariableCS/SleepConditionVariableSRW，因条件不满足而阻塞，
      通过WakeConditionVariable/WakeAllConditionVariable来唤醒因条件不满足而阻塞的线程。
      WakeConditionVariable是唤醒一个因条件不满足而阻塞的线程，
      WakeAllConditionVariable是唤醒所有因条件不满足而阻塞的线程（例如所有读者线程都在等待读）
      从条件等待语句临时释放锁的特性可以发现，它是应该存在于加锁区间段之间的，站在系统api设计者的角度看，为什么条件变量要设计成跟锁配合使用？
          因为一般都是判断当某个条件不满足时，才会在if语句内调用条件等待，而这个判断条件可以被其它线程设为真，所以这个条件属于多个线程共享数据
          所以它应该通过锁来保护，所以使用条件等待语句的地方，必然处于被锁保护的区间内，见例1。
      typedef struct _RTL_CONDITION_VARIABLE { PVOID Ptr; } CONDITION_VARIABLE, *PCONDITION_VARIABLE; 
    例1：
      bool ready=false;
      thread A:
        1: pthread_mutex_lock(&mutex);
        2: while (false == ready) {
        3:     pthread_cond_wait(&cond, &mutex);
        4: }
        5: pthread_mutex_unlock(&mutex);
      thread B:
        1: ready = true;
        2: pthread_cond_signal(&cond);
      分析：
        这种写法是有问题的，因为线程A的中ready会被线程B改动，所以ready属于临界资源，所以在线程A和B中都应该被保护，
        像上面这样的写法，当线程A执行到第3句时(还没执行)，切换到了线程B，线程B将ready设为true，并释放条件信号，但此时条件等待队列为空，所以该信号丢失
        然后切回线程A的第3句，从而线程A被放到了条件等待队列中，但因为线程B已经结束了，所以线程A永远等不到条件信号，A将一直等待下去。
    例2：
        仿例1
            bool ready=false;
        线程A:
            1. pthread_mutex_lock(&mutex);
            2. while (false == ready) {
            3.     pthread_mutex_unlock(&mutex);
            4.     pthread_mutex_lock(&mutex);
            5. }
            6. pthread_mutex_lock(&mutex);
        线程B:
            1. pthread_mutex_lock(&mutex);
            2. ready = true;
            3. pthread_mutex_unlock(&mutex);
            4. pthread_mutex_lock(&mutex);
            5. 。。。
        分析：
            该例中纠正了例1中thread B存在的问题，添加了锁变量
            又把原thread A中的条件变量语句替换为解锁-加锁操作
            这样当线程A在第3句解锁后，因为它没有等待，所以通常不会引起线程切换，
            但因为ready始终为false，所以该线程会在第2-5句之间循环。
            当在循环期间线程A的时间片用完了，则根据线程A最后一句的执行位置不用，而有不同的情况
            如果是第4句执行完了，这时切换到线程B，则线程B因为锁条件不满足，所以会再次把cpu让给A
            如果第3句还没执行，这时切换到B，则同样如此，
            只有当某一次，正好线程A的第3条语句执行完，第4条语句还没执行，这时切换到B，
            线程B才能成功拿到锁并执行下面的操作，
            所以，可以发现如果用“解锁-加锁”操作替换条件变量时，
            虽然也最终能达到目的，但效率是及其低下，无法接受的，
            所以条件变量不止是“解锁-加锁”那么简单，它还会另外等待一个条件，类似于对资源数为0的信号量进行aqure操作
            从而引起线程等待，把cpu让给线程B，而线程B的pthread_cond_signal(&cond)
    例3：
        仿例2
            bool ready=false;
        线程A:
            1. pthread_mutex_lock(&mutex);
            2. while (false == ready) {
            3.     pthread_mutex_unlock(&mutex);
                   pthread_mutex_lock(&mutex2);
            4.     pthread_mutex_lock(&mutex);
            5. }
            6. pthread_mutex_lock(&mutex);
        线程B:
            1. pthread_mutex_lock(&mutex);
            2. ready = true;
            3. pthread_mutex_unlock(&mutex);
            4. pthread_mutex_lock(&mutex);
            5. 。。。
        分析：
        
无论是使用Interlocked系列函数，还是使用关键段、读写锁、条件变量，他们都是在用户模式下完成的，不会有内核状态的切换，所以最大的好处就是速度快，
但他们也有其局限性，最大的问题就是他们没法完成跨进程的线程同步。使用内核对象可以完成跨进程的线程同步，但因为涉及内核态转换，所以速度相对较慢，
实际选用哪种同步手段，应根据具体情况，如果是进程内的线程同步，且注重性能，则使用关键段、读写锁是比较合适的。
      


  

