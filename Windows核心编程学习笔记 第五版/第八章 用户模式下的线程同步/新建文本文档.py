Interlockedϵ�к�������ԭ�ӵķ�ʽ���ٿ�һ��ֵ
  LONG InterlockedIncrement( IN PLONG  Addend );  //��ͨ�ı����Ӽ����������Զ�Ӧ�Ĳ�ֹһ��������
  LONG InterlockedDecrement( IN PLONG  Addend );
  LONG   InterlockedExchangeAdd(IN OUT PLONG  Addend, IN LONG  Value);   //����ֵ�Ǹı�ǰ��ֵ
  LONGLONG __cdecl InterlockedExchangeAdd64(__in_out LONGLONG volatile* Addend, __in LONGLONG Value);  //����ֵ�Ǹı�ǰ��ֵ
  LONG InterlockedCompareExchange(IN OUT PLONG  Destination, IN LONG  Exchange, IN LONG  Comparand );
  PVOID InterlockedCompareExchangePointer( IN OUT PVOID  *Destination, IN PVOID  Exchange, IN PVOID  Comparand );
  InterlockedCompareExchangeִ�еĲ�����
      old_val = *Destination; 
      if(*Destination==Comparand) *Destination=Exchange; 
      return old_val;
  ���Ǳ���ȷ��������Щ�����ı�����ַ�Ǿ�������ģ�������Щ�������ܻ�ʧЧ��
  C���п��ṩ��һ��_aligned_malloc���������ǿ������������������һ���������ڴ档
  void * _aligned_malloc(size_t size, size_t alignment); alignment��ʾҪ���뵽���ֽڱ߽磬Ӧ�� = 2^N (N = 1��2��3 ...)
  Interlockedϵ�к������������û�̬���ں�̬֮��ת��������ִ�еķǳ��죨ͨ��С��50��CPU���ڣ���
  
�߳�ͬ����  
Interlockedϵ�к���ֵ�������޸�һ��ֵ�����Σ����Ҫ��ԭ�ӷ�ʽ���ʸ��ӵ����ݽṹ���͵�ѡ�������ķ�ʽ��  
˼·��
  ���߳���Ҫ���ʹ�����Դ��������Ҫ�õ�һЩ�������¼�����֪ͨʱ��
  �̵߳���ϵͳ�����������̵߳ȴ�����Դ�Բ�����ʽ���롣
  ��������ǰ������ʱ��ϵͳ�ѵ�ǰ�̹߳��𣨶��߳���˵���൱������ס�ˣ��������������ˣ��ٻ��Ѹ��̡߳�
������ 
  �� �ؼ���
    ������
      CRITICAL_SECTION global_cs;
      void InitializeCriticalSection(PCRITICAL_SECTION pcs);  //����EnterCriticalSection֮ǰ������õ����������
      void EnterCriticalSection(PCRITICAL_SECTION pcs);
      BOOL TryEnterCriticalSection(PCRITICAL_SECTION pcs);    //����EnterCriticalSection��ֻ����ʧ��ʱ����FALSE�������������ȴ�
      void LeaveCriticalSection(PCRITICAL_SECTION pcs);
      void DeleteCriticalSection(LPCRITICAL_SECTION lpCriticalSection);   //��ӦInitializeCriticalSection������CRITICAL_SECTION
    ����˵����
      �ؼ��β������ڶ������֮����߳�ͬ����
      ֻҪ����һ���̻߳���ʹ�ùؼ��Σ��Ͳ�Ӧ�õ���DeleteCriticalSection�����øùؼ��νṹ��
      EnterCriticalSection������̣߳����������ʱ�䲻�������޳��ģ�
        ע�����HKEY_LOCAL_MACHINE/System/CurrentcontrolSet/Control/Session Manager�е�CriticalSectionTimeoutֵ�����䳬ʱʱ�䣬
        ���ֵ����Ϊ��λ��һ����30�죬�����Լ����ã�����ҪŪ��̫С������С��3�롣
      ʹ��TryEnterCriticalSection�������سɹ�ʱ����Ч����EnterCriticalSection��һ�µģ���ʱӦ�ö�Ӧ�ĵ���LeaveCriticalSection��
      InitializeCriticalSection�ڲ����������ڴ�Ĳ����������ã�������ڴ�����ʧ�ܣ������׳�STATUS_NO_MEMORY�쳣��
        ���ǿ���ʹ��InitializeCriticalSectionAndSpinCount ��������ɹؼ��γ�ʼ���Ĳ��������ķ���ֵ�ǲ����ͣ��ڴ����ʧ��ʱ������FALSE
      ֻ�е����������߳�����ͬһ���ؼ���(ͬʱ��EnterCriticalSection)ʱ��ϵͳ�Ż᲻�ò�����һ���¼��ں˶���
        ��������Ŀ���ǽ�ʡϵͳ��Դ���˺���¼��ں˶���һֱ���ڣ�ֱ������DeleteCriticalSection��ϵͳ�Ż��ͷ�����¼��ں˶���
        ��WinXp֮ǰ��������ڴ治�㵼�´����¼��ں˶���ʧ�ܣ����亱��������ͬʱ��EnterCriticalSection���׳�EXCEPTION_INVALID_HANDLE�쳣
  �� ��д��(��ռ������)
    ���ó�����
      �ڶ���д��ģ���У���һ�������̶߳�һ������д�������ж���̶߳���������������
      ���ʹ�ùؼ��α������ٽ���Դ����ĳ���߳��ڶ�����д��ʱ�������̶߳����ܷ��ʸ��ٽ���Դ����Ȼ���е��Ч��
      ʹ�ö�д���������������ĳ���߳���д��ʱ�������̶߳����ܷ��ʸ��ٽ���Դ����ĳ���̶߳����ٽ���Դʱ���������߳��Կ��Է��ʸ��ٽ���Դ��
    ������    
      VOID WINAPI InitializeSRWLock(PSRWLOCK SRWLock);
      VOID WINAPI AcquireSRWLockExclusive(PSRWLOCK SRWLock);    //��ռ��
      VOID WINAPI ReleaseSRWLockExclusive(PSRWLOCK SRWLock);
      VOID WINAPI AcquireSRWLockShared(PSRWLOCK SRWLock);       //������
      VOID WINAPI ReleaseSRWLockShared(PSRWLOCK SRWLock);
    ����˵����
      д��Ӧ��ʹ�ö�ռ��������Ӧ��ʹ�ù�����
      �޷���֤��������Ȩ���̱߳���������Ȩ��˳�� SRW���Ȳ��ǹ�ƽ��Ҳ����FIFO��
      ��������ؼ�������TryEnter(Shared/Exclusive)SRWLock���������ռ�ã����������Ի�ȡ�����̻߳ᱻ������
      ����Ƕ�׵�����ͬһ����Դ������ζ��������
      ������ɾ��������SRWLOCK�ĺ�����ϵͳ���Զ�ִ��������
      SRW��ͬ����д����˼
      typedef struct _RTL_SRWLOCK { PVOID Ptr; } SRWLOCK,*PSRWLOCK;
  �� ��������
    ˵����
      ��������������һ�ǻ��⣬���ǵȴ�����������Ϊ�̼߳���ڹ������ݣ��ȴ�������Ϊ�̼߳����������
      ǰ��Ĺؼ��κͶ�д�������ǽ���̶߳���Դ�Ļ���������⣬��������������Ϊ�˽���߳����������⡣
      Ϊ�˷�ֹ�����������������Ǻ����ᣨ�ؼ���/��д����һ��ʹ�á�
    ������
      VOID InitializeConditionVariable (PCONDITION_VARIABLE pConditionVariable);
      BOOL SleepConditionVariableCS(PCONDITION_VARIABLE pConditionVariable, PCRITICAL_SECTION pCriticalSection, DWORD dwMilliseconds);
      BOOL SleepConditionVariableSRW(PCONDITION_VARIABLE pConditionVariable, PSRWLOCK pSRWLock, DWORD dwMilliseconds, ULONG Flags);
      VOID WakeConditionVariable(PCONDITION_VARIABLE pConditionVariable);
      VOID WakeAllConditionVariable(PCONDITION_VARIABLE pConditionVariable);
    ����˵����
      pConditionVariable ָ��һ���Ѿ���ʼ������������
      pCriticalSection/pSRWLock ����ͬ���Թ�����Դ�ķ���
      dwMilliseconds ��ȴ�ʱ�䣬����ΪINFINITE
      Flags ������������ʱ����ǰ�߳��Ƕ�ռ����0�������ǹ�������CONDITION_VARIABLE_LOCKMODE_SHARED��
      �ڹ涨ʱ��������δ��������������FALSE
    ����˵����
      �������������������ȴ�ʱ���ȴ�ʱ����Ϊ���ޣ������ͷŹؼ��λ��д������ֻ����ʱ�ͷţ����ȴ���ɺ󻹻��ȡ��
      ���������������̵߳Ĵ������õ�����ʱ�������������ò��ظղ��ͷŵ�����
      �����������Ȼ�ȴ���ע���ʱ�ȴ��Ĳ��������������ǵȴ�������ֱ���ɹ��õ���֮�󣬸��������ųɹ�����
      �̵߳���SleepConditionVariableCS/SleepConditionVariableSRW���������������������
      ͨ��WakeConditionVariable/WakeAllConditionVariable��������������������������̡߳�
      WakeConditionVariable�ǻ���һ����������������������̣߳�
      WakeAllConditionVariable�ǻ���������������������������̣߳��������ж����̶߳��ڵȴ�����
      �������ȴ������ʱ�ͷ��������Կ��Է��֣�����Ӧ�ô����ڼ��������֮��ģ�վ��ϵͳapi����ߵĽǶȿ���Ϊʲô��������Ҫ��Ƴɸ������ʹ�ã�
          ��Ϊһ�㶼���жϵ�ĳ������������ʱ���Ż���if����ڵ��������ȴ���������ж��������Ա������߳���Ϊ�棬��������������ڶ���̹߳�������
          ������Ӧ��ͨ����������������ʹ�������ȴ����ĵط�����Ȼ���ڱ��������������ڣ�����1��
      typedef struct _RTL_CONDITION_VARIABLE { PVOID Ptr; } CONDITION_VARIABLE, *PCONDITION_VARIABLE; 
    ��1��
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
      ������
        ����д����������ģ���Ϊ�߳�A����ready�ᱻ�߳�B�Ķ�������ready�����ٽ���Դ���������߳�A��B�ж�Ӧ�ñ�������
        ������������д�������߳�Aִ�е���3��ʱ(��ûִ��)���л������߳�B���߳�B��ready��Ϊtrue�����ͷ������źţ�����ʱ�����ȴ�����Ϊ�գ����Ը��źŶ�ʧ
        Ȼ���л��߳�A�ĵ�3�䣬�Ӷ��߳�A���ŵ��������ȴ������У�����Ϊ�߳�B�Ѿ������ˣ������߳�A��Զ�Ȳ��������źţ�A��һֱ�ȴ���ȥ��
    ��2��
        ����1
            bool ready=false;
        �߳�A:
            1. pthread_mutex_lock(&mutex);
            2. while (false == ready) {
            3.     pthread_mutex_unlock(&mutex);
            4.     pthread_mutex_lock(&mutex);
            5. }
            6. pthread_mutex_lock(&mutex);
        �߳�B:
            1. pthread_mutex_lock(&mutex);
            2. ready = true;
            3. pthread_mutex_unlock(&mutex);
            4. pthread_mutex_lock(&mutex);
            5. ������
        ������
            �����о�������1��thread B���ڵ����⣬�����������
            �ְ�ԭthread A�е�������������滻Ϊ����-��������
            �������߳�A�ڵ�3���������Ϊ��û�еȴ�������ͨ�����������߳��л���
            ����Ϊreadyʼ��Ϊfalse�����Ը��̻߳��ڵ�2-5��֮��ѭ����
            ����ѭ���ڼ��߳�A��ʱ��Ƭ�����ˣ�������߳�A���һ���ִ��λ�ò��ã����в�ͬ�����
            ����ǵ�4��ִ�����ˣ���ʱ�л����߳�B�����߳�B��Ϊ�����������㣬���Ի��ٴΰ�cpu�ø�A
            �����3�仹ûִ�У���ʱ�л���B����ͬ����ˣ�
            ֻ�е�ĳһ�Σ������߳�A�ĵ�3�����ִ���꣬��4����仹ûִ�У���ʱ�л���B��
            �߳�B���ܳɹ��õ�����ִ������Ĳ�����
            ���ԣ����Է�������á�����-�����������滻��������ʱ��
            ��ȻҲ�����ܴﵽĿ�ģ���Ч���Ǽ�����£��޷����ܵģ�
            ��������������ֹ�ǡ�����-��������ô�򵥣�����������ȴ�һ�������������ڶ���Դ��Ϊ0���ź�������aqure����
            �Ӷ������̵߳ȴ�����cpu�ø��߳�B�����߳�B��pthread_cond_signal(&cond)
    ��3��
        ����2
            bool ready=false;
        �߳�A:
            1. pthread_mutex_lock(&mutex);
            2. while (false == ready) {
            3.     pthread_mutex_unlock(&mutex);
                   pthread_mutex_lock(&mutex2);
            4.     pthread_mutex_lock(&mutex);
            5. }
            6. pthread_mutex_lock(&mutex);
        �߳�B:
            1. pthread_mutex_lock(&mutex);
            2. ready = true;
            3. pthread_mutex_unlock(&mutex);
            4. pthread_mutex_lock(&mutex);
            5. ������
        ������
        
������ʹ��Interlockedϵ�к���������ʹ�ùؼ��Ρ���д�����������������Ƕ������û�ģʽ����ɵģ��������ں�״̬���л����������ĺô������ٶȿ죬
������Ҳ��������ԣ����������������û����ɿ���̵��߳�ͬ����ʹ���ں˶��������ɿ���̵��߳�ͬ��������Ϊ�漰�ں�̬ת���������ٶ���Խ�����
ʵ��ѡ������ͬ���ֶΣ�Ӧ���ݾ������������ǽ����ڵ��߳�ͬ������ע�����ܣ���ʹ�ùؼ��Ρ���д���ǱȽϺ��ʵġ�
      


  

