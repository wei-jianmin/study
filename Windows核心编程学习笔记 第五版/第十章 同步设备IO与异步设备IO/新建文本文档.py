windows�³����ġ��豸�������豸�����ܹ���֮ͨ�ŵ��κζ��������������豸�У�
�ļ���Ŀ¼������̨�����ڡ����ڡ��ܵ����׽��֡��ʼ���

windows�����ܵط�װ���豸֮��Ĳ��죬����ζ�ţ�������������ͬ�ķ�ʽ��д��ͬ���͵��豸��
��Ӧ��ʶ����Щ����

���豸������
    HANDLE CreateFile(  LPCTSTR lpFileName,   
                        DWORD dwDesiredAccess,        //�Ժ��ַ�ʽ�򿪣���GENERIC_READ��GENERIC_WRITE 
                        DWORD dwShareMode,            //ָ�����ڵĹ�������
                        LPSECURITY_ATTRIBUTES lpSecurityAttributes, 
                        DWORD dwCreationDisposition,  //�Ƿ񴴽����Ǵ����е��ļ�
                        DWORD dwFlagsAndAttributes,   //��Ǻ�����
                        HANDLE hTemplateFile);        //ģ���ļ����
    ����CreateFile���������ǲ����ܴ��ļ���Ŀ¼���豸���������Դ򿪴��ڡ����ڡ������ܵ����豸��
    ͨ��lpFileName��ֵ�Ĳ�ͬ�����ֲ�ͬ���豸����򿪴��ڴ�"COM1"��"COM2"�ȣ��򿪲��ڴ���LPT1������LPT2����
    �򿪿���̨���봫"CONIN1"��"CONIN2"���򿪿���̨�����"CONOUT1"��"CONOUT2"�ȡ�
    ���������豸�����ñ�ĺ�������/�򿪵ģ��紮��ʹ��Socket��accept��AcceptEx�����򿪣�
    ����̨��CreateConsoleScreenBuffer��GetStdHandle�򿪣��ܵ���CreatePipe�򿪵ȣ���Щ��Ϊһ�����˽⼴�ɡ�
    ע�⣬CreateFileʧ��ʱ�����ص�ֵ����NULL������INVALID_HANDLE_VALUE(-1)��

�ر��豸������
    �ر��豸�������Դ�����豸��˵��ʹ��BOOL CloseHandle(HANDLE hObject)���ɣ�
    ��socket��ʹ��int closesocket(SOCKET sock)������

���򿪵��豸���������
    DWORD GetFileType(HANDLE hDevice) �������Լ��򿪵��������豸�������·���ֵ��
    0x0000 FILE_TYPE_UNKNOWN : δ֪�豸
    0x0001 FILE_TYPE_DISK    : �����ļ�
    0x0002 FILE_TYPE_CHAR    ���ַ��ļ���һ���ǲ��ڡ����ڻ����̨�� 
    0x0003 FILE_TYPE_PIPE    ���ܵ��ļ�
    0x8000 FILE_TYPE_REMOTE  ��Զ���ļ�
    
CreateFile�������
    CreateFile��Ϊ��ḻ�Ĳ���������Ϊ�����ṩ�˸�ǿ�Ķ����ԡ�
    �����ڴ��ļ�ʱ�������ʹ��fopen��CreateFile���������ǽ��и���Ķ��ƣ�
    ���Ƿ�ʹ�û��棬�Ƿ��ļ��ر��Զ�ɾ�����Ƿ��ռ�򿪣��Ƿ��첽�򿪣�����ϵͳ�ļ�/�����ļ��ȡ�
    ����Ͷ���Щ��������ϸ��˵����
    lpFileName
        ���ǲ���ǰ��ġ����豸������С���Ѿ��ᵽ���ģ��ò����ȿ������ض������ƣ���ʾ�ض����豸��Ҳ������ĳ���ļ�·����
    dwDesiredAccess
        ����������ֵ�������ʽ��
        0   �������Ҫ��д���豸����ֻ��ı��豸�����ã����޸��ļ���ʱ����������Դ�0
        GENERIC_READ  ��
        GENERIC_WRITE д
    dwShareMode
        �����豸���ظ������ԣ�����Ϊ����ֵ����ϣ�
        0                 ��ռ�ķ��ʣ�����豸�Ѿ��򿪣��ٴδ򿪸��豸��ʧ�ܡ�
        FILE_SHARE_READ   ��������ַ�ʽ�򿪣���ζ�ź����ٴ򿪸��豸ʱ��������ֻ����ʽ�򿪵ģ����Ǵ�ʧ��
                          �������֮ǰ���ļ��Ѿ��Է�ֻ���ķ�ʽ���ˣ��ǽ�ʹ�ñ��δ�ʧ��
        FILE_SHARE_WRITE  ��������ַ�ʽ�򿪣���ζ�ź����ٴ򿪸��豸ʱ��������ֻд��ʽ�򿪵ģ����Ǵ�ʧ��
                          �������֮ǰ���ļ��Ѿ��Է�ֻд�ķ�ʽ���ˣ��ǽ�ʹ�ñ��δ�ʧ��
        FILE_SHARE_READ|FILE_SHARE_WRITE  �����������д�Ĵ򿪷�ʽ��ֻ�����/ֻ����д�Ĵ򿪷�ʽ�����ͻ�ģ�
                          ����ζ������ļ������ַ�ʽ���ˣ��Ͳ�������ֻ�����(/д)�ķ�ʽ�򿪣���ʧ�ܣ���
                          ��Ϊ�����ϵͳ�㲻���׸��ļ�������ֻ�����(/д)�����ǹ����д����֮��Ȼ��
        FILE_SHARE_DELETE ɾ�ļ�Ȩ�޹���ʹ�øñ�Ǵ򿪣������ɾ���ļ���Ȩ�ޡ�
    lpSecurityAttributes
        ָ��SECURITY_ATTRIBUTES�ṹ������ָ����ȫ��Ϣ�Լ��Ƿ������صľ�����ӽ������̳С�
        ֻ����NTFS��ʽ�����д������ļ����Ż�ʹ�øò�����Ҳ���Դ�NULL��Ĭ��ֵ������������²�֧�ָò�����Ӧ�ô�NULL
    dwCreationDisposition
        ����������ֵ��
        CREATE_NEW        �������ļ���������ļ��Ѿ����ڣ���������ʧ��
        CREATE_ALWAYS     �������ļ���������ļ��Ѿ����ڣ��򸲸�ԭ���ļ������ļ��ض�Ϊ0��
        OPEN_EXISTING     �������ļ�������ļ������ڣ����ʧ�ܣ�����򿪵��Ƿ��ļ��豸���紮�ڣ������ʹ�ø�ֵ��
        OPEN_ALWAYS       �������ļ�������ļ������ڣ��򴴽��ļ�
        TRUNCATE_EXISTING �������ļ��������ļ��ض�Ϊ0������ļ������ڣ���������ʧ��
        ע����ʹ��OPEN_ALWAYSʱ������ļ��Ѵ��ڣ������������򿪲���д�ļ�������GetLastError,��Ȼ���ء��ļ��Ѵ��ڡ�����
    dwFlagsAndAttributes
        �Ӳ��������־Ϳ��Կ������������ֹ��ܣ����ñ�Ǻ���������
        ֧�ֵı��ֵ�У�            
            FILE_FLAG_NO_BUFFERING          0x20000000    ��д�ļ�ʱ����ʹ�ø��ٻ��棬ֱ��д����̵�������
														  ʹ�����ַ�ʽ�򿪵��ļ������ļ��ķ��ʴ����������ƣ�
														  ��ÿ�ζ�дλ�ü���д����������С����Ϊ����������С����������
														  ��Ҫд���ļ������ݻ��������ڴ��ջ��Ҳ������������ģ����ݴ��̲�ͬ��
														  �еĿ��ܲ�ǿ�ƴ�������VirtualAlloc����Ļ��������ڴ�ҳ�����
														  ���������ڴ�ҳ��С��������С����������
														  ����ʹ��GetDiskFreeSpace������ȷ���������Ĵ�С��
            FILE_FLAG_RANDOM_ACCESS         0x10000000    ��ʾ�����Ҫ���ļ������д�����ʹ����FILE_FLAG_NO_BUFFERING��
                                                          ��ñ�ǻ����
            FILE_FLAG_SEQUENTIAL_SCAN       0x08000000    ��ʾ�������Ҫ��ǰ��ȡ�ļ������ʹ����FILE_FLAG_NO_BUFFERING��
                                                          ��ñ�ǻ����
            FILE_FLAG_WRITE_THROUGH         0x80000000    ��ֹ���ļ�д�������л��棬�Է�ֹ���ݶ�ʧ����������ʹ�û��棩��
                                                          ����������ļ���������ֱ������д�����������
            FILE_FLAG_OVERLAPPED            0x40000000    Ϊ�첽��д��/�����ļ������������ϸ���ܡ�            
            FILE_FLAG_DELETE_ON_CLOSE       0x04000000    �ļ����о�����ر�ʱ���ļ��Զ�ɾ����
            FILE_FLAG_BACKUP_SEMANTICS      0x02000000    Ϊ���ݻ�ԭ�������򿪻򴴽��ļ���
            FILE_FLAG_POSIX_SEMANTICS       0x01000000    ����POSIX��������ļ������ļ�·�������ִ�Сд��linux�¾��������ģ�
                                                          ע�⣬���ʹ���˸ñ�ǣ���ôwindowsӦ�ó�����ܻ��޷����ʸ��ļ�
            FILE_FLAG_OPEN_REPARSE_POINT    0x00200000    ���ع�ע
            FILE_FLAG_OPEN_NO_RECALL        0x00100000    ���ع�ע
            FILE_FLAG_FIRST_PIPE_INSTANCE   0x00080000    ���ع�ע
        ֧�ֵ������У�
            FILE_ATTRIBUTE_READONLY             0x00000001  �򿪻򴴽�ֻ���ļ�
            FILE_ATTRIBUTE_HIDDEN               0x00000002  �򿪻򴴽������ļ�
            FILE_ATTRIBUTE_SYSTEM               0x00000004  �򿪻򴴽�ϵͳ�ļ�
            FILE_ATTRIBUTE_DIRECTORY            0x00000010  �򿪻򴴽�Ŀ¼
            FILE_ATTRIBUTE_NORMAL               0x00000080  �򿪻򴴽���ͨ�ļ������ܺ��������Թ��ã� 
            FILE_ATTRIBUTE_TEMPORARY            0x00000100  ��ʱ�򿪣�������㹻�ĸ��ٻ�����ã��;�����д����̣�
            FILE_ATTRIBUTE_ARCHIVE              0x00000020  �򿪻򴴽��浵�ļ�
            FILE_ATTRIBUTE_COMPRESSED           0x00000800  �ļ�������ѹ����
            FILE_ATTRIBUTE_ENCRYPTED            0x00004000  �ļ��Ǿ������ܵ�
            FILE_ATTRIBUTE_OFFLINE              0x00001000  �ļ�����ڣ����ļ������ѱ�ת�Ƶ��ѻ��洢�����ˡ�
            FILE_ATTRIBUTE_NOT_CONTENT_INDEXED  0x00002000  �����������񲻻���ļ���������
            FILE_ATTRIBUTE_VIRTUAL              0x00010000  δ֪
            FILE_ATTRIBUTE_DEVICE               0x00000040  δ֪
            FILE_ATTRIBUTE_SPARSE_FILE          0x00000200  δ֪
            FILE_ATTRIBUTE_REPARSE_POINT        0x00000400  δ֪
        ע�����ͬʱʹ�� FILE_FLAG_DELETE_ON_CLOSE �� FILE_ATTRIBUTE_TEMPORARY ��������ᾡ������������ļ���
            �������ļ���С�����ƣ�ֻ�����ļ�������һ����Сʱ���Ż������Ĳ���ء�
    hTemplateFile
        ������һ���Ѵ��ļ��ľ����Ҳ����Ϊ�գ�����������һ���������CreateFile�����dwFlagsAndAttributes������
        ��ʹ����hTemplateFile�ļ�ͬ�������ã�ǰ����hTemplateFile�ļ������ǿɶ��ģ�������ò���ֻ�Դ����ļ����ã�
        ����Ǵ��ļ�(�ļ��Ѵ���)������Ըò�����
                          
�ļ�����    
    ��ȡ�ļ���С
        DWORD GetFileSize(HANDLE hFile, LPDWORD lpFileSizeHigh);
        BOOL GetFileSizeEx(HANDLE hFile,PLARGE_INTEGER lpFileSize);
        DWORD WINAPI GetCompressedFileSize(LPCTSTR lpFileName,LPDWORD lpFileSizeHigh);
        GetFileSize����ֵΪ�ļ���С������ļ���Сֵ����DWORD������lpFileSizeHigh���գ�
        ����������£��Ƽ�ʹ��GetFileSizeEx�������������ϵĲ�֧�ָú�����ϵͳ��
        GetCompressedFileSize�õ������ļ��ڴ�����ռ�õ��ֽ�����
        ����ļ������ڴ�������ѹ����ŵģ����ֵ��С��GetFileSize�õ���ֵ��
    �����ļ�ָ��λ��
        DWORD SetFilePointer( HANDLE hFile,   LONG lDistanceToMove, 
                              PLONG lpDistanceToMoveHigh,   DWORD dwMoveMethod); 
        BOOL SetFilePointerEx( HANDLE hFile, LARGE_INTEGER liDistanceToMove, 
                               PLARGE_INTEGER lpNewFilePointer, DWORD dwMoveMethod);
        ������
          DistanceToMove����ָ���ƶ����룬����Ϊ������    
          MoveMethodָ���ƶ���׼�㣺FILE_BEGIN/FILE_CURRENT/FILE_END      
          lpNewFilePointer�����ƶ�����ļ�ָ��λ�ã�ͨ�����ļ�ָ���ƶ�0�ֽڣ����Ի�ȡ��ǰ�ļ�ָ��λ��
        �ļ���ָ��λ���ǿ��Գ�����ǰ�ļ���С�ģ�����λ���µĶ�д����ʹ�ļ��м�һ�������ǿյġ�
        ����ļ����ǣ�ʹ�õ�FILE_FLAG_NO_BUFFER���������ļ��ƶ�λ��ֻ����������С����������
        ��CreateFile����/�򿪵�ͬһ���ļ�����Ϊ��������ͬ���ں˶���������ͬһ���ļ���
        ���Ի���Գ���һ���ļ���дָ�룬���߻���Ӱ�죬
        �����ʹ��DuplicateHandle���Ƴ������ں˶���������Ϊ��ָ��һ���ں˶������Թ����ļ���дָ�롣
    �����ļ�β
        BOOL SetEndOfFile(HANDLE hFile);
        ͨ�������ļ�β�����Խضϻ������ļ���С��ǰ���FILE_END����ֵ��Ϊ�µ��ļ�βλ�á�
        ͨ���ڹرյ�ʱ��ϵͳ���������ļ�β��

ͬ����д�ļ�
    ��д����
        BOOL ReadFile( HANDLE hFile, LPVOID lpBuffer,   
                       DWORD nNumberOfBytesToRead, 
                       LPDWORD lpNumberOfBytesRead,   
                       LPOVERLAPPED lpOverlapped); 
        BOOL WriteFile( HANDLE hFile, LPCVOID lpBuffer, 
                        DWORD nNumberOfBytesToWrite,   
                        LPDWORD lpNumberOfBytesWritten, 
                        LPOVERLAPPED lpOverlapped); 
         ʹ��ͬ����д��lpOverlapped����Ӧ����Ϊ�գ�ͬʱҪ����ļ���ʱ��
        ����ѡ���첽��ʽ�򿪣���ʹ��FILE_FLAG_OVERLAPPED��־����
    ˢ�»�����
        BOOL FlushFileBuffers(HANDLE hFile);
        ������д�ļ�����ʹ�û��棨Ĭ�ϻ����ǿ����ģ���
        ��д���ڡ��ʼ��ۡ��ܵ����豸��Ҳ����ʹ�û��档
        ʹ��FlushFileBuffers���������Խ������е�����ǿ��д�뵽�豸��
        Ҫ�ɹ�����FlushFileBuffers��������Ҫ���豸����дȨ�ޡ�
    ��������
        BOOL CancelSynchronousIo(HANDLE hThread);
        ��һ���߳���ͬ����������ʱ����ʱ�����Խ�����һ���߳���ǿ�ƽ������̵߳�ͬ��������
        ��ʱ��ԭ�̵߳�ͬ�������˳�����״̬����ʧ�ܷ��أ�GetLassError����ERROR_OPERATION_ABORTED��
        �˳��������̴߳�����״̬�л�������״̬����ʾ���Ա�cpu���ȡ�
        �����������Ĳ��Ƕ�д�������̣߳������᷵��FALSE��GetLasterror����ERROR_NOT_FOUND��
        ע�⣬hThread��Ҫ��THREAD_TERMINATEȨ�ޣ�����CancelSynchronousIo�᷵��ʧ�ܣ�
        GetLastError����ERROR_ACCESS_DENIED����CreateThread��_beginthreadex��������/�򿪵��̣߳�
        ��THREAD_ALL_ACCESS�ģ���ȻҲ������THREAD_TERMINATEȨ�ޡ�
        ���ǵ�ʹ��OpenThread���߳�ʱ����ע��ͨ���������ƴ򿪾���THREAD_TERMINATEȨ�޵��̡߳�
        
�첽��д�ļ�
    ���첽��ʽ���豸
        ��CreateFile���豸������dwFlagsAndAttributes������ָ��FILE_FLAG_OVERLAPPED��־��
    ���첽��ʽ��д
        BOOL ReadFile( HANDLE hFile, LPVOID lpBuffer,   
                       DWORD nNumberOfBytesToRead, 
                       LPDWORD lpNumberOfBytesRead,   
                       LPOVERLAPPED lpOverlapped); 
        BOOL WriteFile( HANDLE hFile, LPCVOID lpBuffer, 
                        DWORD nNumberOfBytesToWrite,   
                        LPDWORD lpNumberOfBytesWritten, 
                        LPOVERLAPPED lpOverlapped); 
        �첽��дʱ�������ļ��Ƿ���FILE_FLAG_OVERLAPPED��ʽ�򿪵ġ�
        lpNumberOfBytesRead/lpNumberOfBytesWritten�������첽��дʱ����û������ģ���Ϊ��������ʱ��
        ������֪����д�˶������ݣ��������ֵ��NULL���С���ͨ�������lpOverlapped����д�˶����ֽڣ�
        pOverlappedָ��OVERLAPPED�ṹ��
        struct OVERLAPPED ��
            [out] DWORD Internal;           //���ش�����
            [out] DWORD InternalHigh;       //���ض�д�˶����ֽ�
            [in]  DWORD Offset;             //�첽��дλ�ã��첽��дʹ�ø�ָ�룬�������ļ�ָ�룩
            [in]  DWORD OffsetHigh;         //�첽��дλ�ã����ڷ��ļ��豸��Ӧ�ý�������ֵ��Ϊ0��
            [in]  HANDLE hEvent;
        ����д��������ʱ�����Ƚ�Internal��ֵ��ΪSTATUS_PENDING��pend�����ҡ��Ⱥ����˼����
        ���ļ��豸������ָ����дλ�ã����뽫Offset��OffsetHigh��Ϊ0��
        ע�����
            1.��������һ����˳����Ӧi/o�����б�
              ��������һ���첽��/д��ϵͳͨ���ѱ�������ŵ���Ӧ�豸������i/o�����б��С�
              ���豸ȴ��һ���ǰ������ȳ���˳������Ӧ��i/o�����б�ģ�����ڴ����ļ���Ϊ�˽��ʹ�ͷ��
              �ƶ���Ѱ��ʱ�䣬�ļ�ϵͳ��������i/o�������������Ѱ����Щ��дλ���뵱ǰ��ͷλ�ñȽϽ�������
            2.�ļ���д������һ������첽ִ��
              ��������һ���첽��/д��ϵͳ��һ����������ŵ���Ӧ�豸������i/o�����б��С�
              �����д�ļ�ʱ����������Ѿ��ڸ��߻������ˣ���ôϵͳ�Ͳ����ٸ�����������Ҫ�����ˣ�
              ��ȻҲ���ð�i/o����ŵ�����������i/o�����б����ˡ�
              ����������£���Ȼ�ļ������첽��ʽ�򿪵ģ�����д����ʵ������ͬ��������
              ���⣬����ĳЩ�����������ļ�׷������ʱ����һ����ͬ����ʽ���еģ������ļ����Ժ��ַ�ʽ�򿪡�
            3.��ȷ��ʶReadFile��WriteFile�����ķ���ֵ
              ��������I/O��������ͬ����ʽִ�еģ���ôReadFile��WriteFile�᷵�ط�0ֵ��
              ���������I/O���������첽��ʽִ�еģ���ôReadFile��WriteFile�᷵��FALSE��
              ���ⲻ���ж��Ƕ�д�����Ƿ���ĳ����ˣ�����Ӧ����GetLastError��������飨�Ƿ������
              ���GetLastError���ص���ERROR_IO_PENDING��˵������ִ�гɹ��ˣ�i/o�����ѱ��ŵ���Ӧ�����Ķ������ˣ�
              ���������ֵ����ͨ���Ǳ��������ˣ���������ԭ������Ϊ�������⣬
              ��ͨ������Ϊ����һ��������i/o������δ��ɣ����������Ҫ��һЩi/o������ɺ��ٵ���ReadFile/WriteFile������
            4.���첽i/o����֮ǰ��һ�������ͷ�/���ٲ��������OVERLAPPED�ṹ��
              ����������OVERLAPPED�ṹ����ʱ��ͨ������ʹ�þֲ���������ʽ��
    ȡ�������е�i/o����
        ��ʽһ��BOOL CancelIo(HANDLE hFile);
            ͨ���ú��������Խ���ǰ�߳���ӵġ��йظ��ļ��������첽i/o����Ӷ�����ɾ����
        ��ʽ�����ر��ļ�
            ͨ�����ַ�ʽ�����Խ��йظ��ļ��������첽i/o����Ӷ�����ɾ����
        ��ʽ�����߳���ֹ
            ͨ�����ַ�ʽ�����Ե�ǰ�߳���ӵ������첽i/o����Ӷ�����ɾ����
        ��ʽ�ģ�BOOL CancelIoEx(HANDLE hFile, LPOVERLAPPED lpOverlapped);
            ͨ�����ַ�ʽ�������йظ��ļ��ġ���lpOverlapped�������i/o����Ӷ�����ɾ����
            ע�⣬��CancelIo������ͬ���ǣ��ú����������ڵ�ǰ�߳���ӵ�i/o����
            ���lpOverlapped��NULL����Ч��ͬ��ʽ�������ļ���ص������첽i/o����Ӷ�����ɾ����
        ע����ȡ����i/o������OVERLAPPED���صĴ�������ERROR_OPERATION_ABORTED��

�����첽I/O�������֪ͨ
    1. �����豸�ں˶���
       ��ʹ��WaitForSingleObject��WaitForMultipleObject�ȴ��豸�ں˶���
       �첽��д�����ᣨ�ڽ�i/o������ӵ�����֮ǰ�����豸�ں˶�����Ϊδ����״̬��
       �����豸�������������i/o����󣬻Ὣ���ں˶�����Ϊ����״̬��
       ȱ�㣺
            �ȴ��豸�ں˶���Ὣ�߳���Ϊ����״̬����ʧȥ���ļ��첽��д�����塣
            ������Ҳ���ܴ����ͬһ�ļ��Ķ���첽��д����������
            ��ΪֻҪ��һ���첽��д����ˣ��ȴ������ͷ��أ��������ж����ĸ��첽��д�����ˡ�
    2. �����¼��ں˶���
       �豸�������ĳi/o����󣬲����ܽ��豸�ں˶�����Ϊ����״̬��
       ������OVERLAPPED��hEvent������Ϊ�յ�ʱ�򣬵���SetEvent����hEvent�¼��ں˶�����Ϊ����״̬��
       ���ԣ����ǳ����񷽷�1�����ȴ��豸�ں˶����⣬Ҳ���Եȴ�hEvent�¼��ں˶���
       ���⣬Ϊ����΢��ߵ����ܣ����ǿ����ٵ���SetFileCompletionNotificationModes������
       �����������򣬵���д��ɺ󣬲��ô�����Ӧ���豸�ں˶���
       ��ȱ�㣺 
            ����˷���1�У����ܴ����ͬһ�ļ��Ķ���첽��д�����ȱ�ݣ�
            ��ͬ������������̣߳�ʧȥ���첽��д�����塣
            ���⣬�������д��������ͬһ��OVERLAPPED�ṹʱ��Ҳ�����жϵ����ĸ���д��������ˡ�
    3. ʹ�ÿ�����I/O
       ��ϵͳ����һ���̵߳�ʱ�򣬻���ͬ���Ĵ���һ�����첽���̵��á���APC�����У�
       �ö�����������̶߳�Ӧ�ģ����ǿ����ڷ����첽��д����ʱ�������豸���������i/o��д��ɺ�
       ���ö��С���ʹ�ô�ͳ��ReadFile/WriteFile�������޷�������һ��ģ���Ҫ����
       ReadFileEx��WriteFileEx������
       BOOL ReadFileEx( HANDLE hFile,
                        LPVOID lpBuffer,
                        DWORD nNumberOfBytesToRead,
                        LPOVERLAPPED lpOverlapped,
                        LPOVERLAPPED_COMPLETION_ROUTINE lpCompletionRoutine );
       BOOL WriteFileEx( HANDLE hFile,
                         LPCVOID lpBuffer,
                         DWORD nNumberOfBytesToWrite,
                         LPOVERLAPPED lpOverlapped,
                         LPOVERLAPPED_COMPLETION_ROUTINE lpCompletionRoutine );
       ��������������˵�ǵ���Ϊ�첽��д����Ƶģ�����ȥ�������Ա����д�˶����ֽڵ��Ǹ������������첽��дҲ�ò��ϣ�
       ������˸�lpCompletionRoutine�������ò���Ҫ��һ������ָ�룬���豸�����������I/O����󣬻����APC���У�
       ���оͰ����ú���ָ��(���⻹����OVERLAPPED�ṹ��ָ��)��������������ReadFileEx/WriteFileEx�ĺ�����������
       ����Ļص���������ʽΪ�� VOID WINAPI CompletionRoutine(DWORD dwError,DWORD dwNumBytes,OVERLAPPED *po);
       ����dwError��dwNumBytes����������OVERLAPPED�ṹ�е�ǰ������Ա��������ʹ����ֽ�����
       ���߳�ִ�е��ض��ĵȴ�����ʱ���߳̾ͻ���APC���У������ö������еĻص�������
       ��Щ�ض��ĵȴ�������
            DWORD SleepEx(DWORD dwMilliseconds, BOOL bAlertable);
            DWORD WaitForSingleObjectEx(HANDLE hHandle, DWORD dwMilliseconds, BOOL bAlertable);
            DWORD WaitForMultipleObjectsEx(DWORD nCount, const HANDLE* lpHandles,
                                           BOOL bWaitAll, DWORD dwMilliseconds, BOOL bAlertable);
            DWORD WINAPI SignalObjectAndWait(������);
            BOOL WINAPI GetQueuedCompletionStatusEx(������);
            DWORD MsgWaitForMultipleObjectsEx(������);
            ���Կ�������Щ��������и�bAlertable���������Կ����Ƿ��߳���Ϊ��������״̬����
            ��Щ����Ҳ��Ϊ���ʹ���̵߳ġ��첽���̵��á����ж�ר����Ƶġ�
            ��ִ����Щ������ʱ�򣬻����ȼ���̵߳�APC���У������Ϊ�գ��ͻ���ִ��APC�������еĻص�������
            ��APC�����е������������ɺ���Щ�ȴ�����Ҳ�����������״̬�ˣ����ǳɹ����ء�
            ֻ���ڵ�����Щ�ȴ�����ʱ��APC����Ϊ�յ�����£����ǲŻ���һ��ĵȴ��������������̡߳�
            �����ȴ��ĺ��������עAPC���У����䲻Ϊ��ʱ��Ҳ������ȴ�״̬��������APC�������еĵȴ�������
            ��ͨ����Щ�ȴ������ķ��أ��鿴��������Ϊʲô�������ȴ��ģ�Ҳ����GetLastError����
            �����WAIT_IO_COMPLETION���Ǳ����ȴ�����������ԭ���Ǵ�����APC�����е�����һ�
       ȱ�㣺
            ��Ϊʹ���˻ص����������ô���д����������Щ��
            ����������ǣ��ûص�������ΪReadFileEx��WriteFileEx�����һ��������
            ��;����˻ص�����Ҳ���ڷ��������i/o�߳��н��еġ�
            ���һ���̷߳�����i/o�����Ǹ��߳̾͵ö����е���Щ������Ӧ��
            ��ʹ�����̶߳����ڿ���״̬��
            ��Ϊ����ȱ�ݣ��������ַ���������Ч��ʹ��cpu��Դ�����Բ��Ƽ�ʹ�á�
       �ŵ㣺
            ������ŵ㣬����������ʹ�����ַ������ȴ�i/o��������ʹ��ǰ���ַ������ŵ㣬
            �������ۻ��ڻ���APC���ƣ����Ը����Ǵ�����Щ�ô���
            �����ᵽһ������������۷ǳ����õĺ��� 
            DWORD QueueUserAPC(PAPCFUNC pfnAPC,HANDLE hThread,ULONG_PTR dwData);
                ����PAPCFUNC�Ķ���Ϊ typedef VOID WINAPI (*PAPCFUNC)(ULONG_PTR dwParam);
                �����ѵ��̻߳�ִ�иûص�������
                �ڶ�������hThread��һ���̵߳ľ����
                ����ϵͳ������Ҫ������ӵ��ĸ��̵߳�APC�����У�
                ����߳̿�����ϵͳ�е��κ��̣߳����hThread������һ�������еģ�
                ��pfnAPC��ָ��ĺ�����ַ��Ҳ�������Ǹ������еĺ�����ַ��
                QueueUserAPC���������һ������dwData�����Ǵ����ص�������ֵ��
                �ú����ķ���ֵ����DWORD���͵ģ�����ʵֻ��0�ͷ�0���֣�0��ɹ���
            ���ǽ�������������������ҵ���һ���̼߳䷢��֪ͨ�ķ������������Կ���̣�
            �������ַ����������ó������ŵ��˳��̡߳�
            ���̴߳��ڿ����ѵȴ�״̬ʱ���������Ϊ����̣߳���һ���Ǳ����̵ģ�����
            QueueUserAPC��ʹ�ñ��̱߳������ȴ��������ص�ֵΪWAIT_IO_COMPLETION��
            ������ǵȴ������ں˶����򷵻�ֵΪWAIT_OBJECT_0+n����
            ��ʱ�����߳̾Ϳ�����һЩ����������ɽ����˳��̣߳�
            ��ʱ��Ȼ�ص�����pfnAPC�����ᱻ���ã�����ʱͨ�������������κι���������Ϊ�ռ��ɡ�
            �й� QueueUserAPC���Σ�
            file://..\..\WIN32\WSAWaitForMultipleEvents �� MsgWaitForMultipleObjectsEx.txt
    4.  ʹ��I/O��ɶ˿�
        ������
            ΢�������ɶ˿ڵı����ǣ����̲߳�����Ӧģ�Ͳ��������������ǰ㷢��������������
            �����̲߳�����Ӧ��ÿ��һ���ͻ������󣬷���˾ʹ���һ����Ӧ�̣߳���
            ������Ϊ�����������̫����߳�ͬʱ����ʱ���߳��л�������̫���ʱ�䣬
            ������cpu��û����ʱ��������ִ���߳������ˣ����⣬�̵߳Ĵ���������Ҳ�Ứ��һ����cpuʱ�䡣
            �Ǹ��ж��ٸ��̲߳�������أ����ǣ�ͬʱ���е��߳���=cpu��������ע������ָ���ǿɱ�ִ�е��̣߳�
            �����������������̣߳�һ���������߳���������cpu���������ͻ����̴߳��ھ���״̬��
            �ȴ�cpu������ͻ�ʹcpu����ʱ���������߳��л���
            I/O��ɶ˿ڵĽ���취����ʹ���̳߳ء�
        CreateIoCompletionPort����˵����
            HANDLE CreateIoCompletionPort(
                    HANDLE FileHandle,
                    HANDLE ExistingCompletionPort,
                    ULONG_PTR CompletionKey,
                    DWORD NumberOfConcurrentThreads );
            FileHandle��
                ȷ�е�˵��Ӧ����IO�豸�ں˶���ľ������Ϊ�����ļ��ں˶���
                ������socket���ܵ����ʼ��۵��ں˶���Ҳ��ʹ����ɶ˿ڡ�
                ������ļ��ں˶��󣬸��ļ��ں˶��������ʹ��FILE_FLAG_OVERLAPPED��ʽ�򿪵ġ�
                �������Ĳ�����INVALID_HANDLE_VALUE������ֻ�Ǵ�����ɶ˿ڣ�������IO�豸�ں˶����������
                ��ʱ��ExistingCompletionPort�������봫NULL����CompletionKey������ᱻ���ԡ�
            ExistingCompletionPort��
                ��ɶ˿��ں˶���ľ��
                �������һ���Ѵ��ڵ���ɶ˿��ں˶���ľ����������FileHandle�����ɶ˿��������
                �������ص�Ҳ���Ǹò���������Ǹ���ɶ˿ڵľ���������Ǵ���һ���µ���ɶ˿��ں˶���
                ����������NULL����������һ����ɶ˿��ں˶��󣬲�����һ������������ļ����(�豸���)��֮������
            CompletionKey��
                ϵͳ�ڲ�����ʹ�øò������������Ǽ�¼�ò���������ɶ˿ڼ�⵽����/�������¼�ʱ�����ò����ٷ��ظ��û�ʹ�á�
            NumberOfConcurrentThreads��
                ������ɶ˿���ͬһʱ�䣬������ж����̴߳��ڿ�����״̬�������0����I/O�˿ڻ�ʹ��Ĭ��ֵ����cpu������
                ��ExistingCompletionPort��Ϊ��ʱ���ò��������ԡ�
            �����⼸�������໥��Լ���ص㣬���Խ��ú����ֳ�����Ӧ�����Σ�
                ����(�����κ��豸������)��ɶ˿��ں˶���
                    ��һ��������INVALID_HANDLE_VALUE����Ӧ�ģ��ڶ���������NULL��
                    ������������Ϊ�����ԣ����Կ��Դ�0��ֻʹ�õ��ĸ�������
                ���ļ�(�豸)�ں˶����������ɶ˿ڣ�
                    ��һ���������ļ�(�豸)�ں˶���ľ�����ڶ����������Ѵ��ڵ���ɶ˿ڵľ����
                    ��Ϊ��ʱ���ĸ��������غ��ԣ����Կ��Դ�0���������������Լ���Ҫ��ֵ��
            CreateIoCompletionPort����Ҫ��SECURITY_ATTRIBUTES
                ����Ψһ��һ�������ں˶��󣬲���Ҫָ���ò����ĺ�����
                ������Ϊ�ú�������Ƴ����ǽ�����ǰ����ʹ�ã������漰������̡�
        ����ɶ˿ڶ����������ݽṹ��
            �豸�б�
                ÿ����¼������hDevice dwCompletionKey
                ��ʾ��ǰ��ɶ˿ڶ�����Щ�ļ�(�豸)�ں˶������Ȥ��
                hDevice��CreateIoCompletionPort����ĵ�һ��������
                dwCompletionKey��CreateIoCompletionPort����ĵ�����������
                ÿ��CreateIoCompletionPort������ɺ󣬾ͻ������б�
                �����̽�ĳ�豸�رպ���ϵͳ���ñ��еĶ�Ӧ��ɾ����
                ��һ���첽I/O�������ʱ��ϵͳ����ÿ����ɶ˿ڵ��豸�б�һ��һ��������ֻ�ᴴ��һ����ɶ˿��ں˶��󣩣�
                �����Ƿ�Ե�ǰ�豸����Ȥ������ǣ��ͻ���������I/O��ɶ��С�
            I/O��ɶ���
                ÿ����¼������dwByteTransferred dwCompletionKey pOverlapped dwError
                dwByteTransferred��¼�Ѵ�����ֽ�����
                dwCompletionKey�����豸��������ɶ˿�ʱ�����ֵ��
                pOverlapped�贴���ļ�(�豸)�ں˶���ʱָ���ġ�
                dwError������룬��ʵ����pOverlappedָ��ṹ�ĵ�һ����Ա��ֵ��
                ����ɶ˿ڹ�ע���豸����첽i/o����ʱ�������ö��С�
                �����ڲ�ʵ����ͬ����ʽ��ɵ��첽i/o���������ϣ����֮��ӵ���ɶ˿��У�
                ����Ե���SetFileCompletionNotificationModes������������FILE_SKIP_COMPLETION_PROT_ON_SUCESS��־����������ܡ�
                ���ȴ��̶߳����е�һ���̵߳õ�ִ��ʱ���ͻ�ɾ���������е�һ�
            �ȴ��߳�ջ
                ÿ����¼������dwThreadId
                ��ĳ���̵߳���GetQueuedCompletionStatus�����ȴ�����ɶ˿�ʱ���������߳�id��¼�ڴ˱��С�
                Ҫ��ĳ���Ѵ����ڴ˱��е��߳��̳߳����Ƴ���������;����
                    ���߳̽���
                    �����߳���һ���µ���ɶ˿ڹ��������ٴε���GetQueuedCompletionStatus������
                    ���ٵ�ǰ��ɶ˿ڣ���õȴ��߳�ջ��ȻҲ��֮�ͷ�
                ��ĳ���ļ�(�豸)��I/O���ʱ���ʹӸ��б��л���һ���̣߳�
                ͬʱ���ѵ��̵߳���������CreateIoCompletionPort������NumberOfConcurrentThreads������Լ�ġ�
                ֮����ʹ��ջ�ṹ�������̳߳ص��ص�����Ӧ�ģ��������ŵ��ǿ���ʹ�õ��߳���Դ��
                �̳߳����̵߳����������վ��飬Ӧ����CreateIoCompletionPort��NumberOfConcurrentThreadsֵ��2����С��
            ���ͷ��߳��б�
                ÿ����¼������dwThreadId
                �ȴ��̶߳����е�ÿ���̵߳õ�ִ�к󣬾ͽ�֮�ӵȴ��̶߳������Ƴ����ŵ��������С�
                �����߳��ٴε���GetQueuedCompletionStatus����ʱ���ֽ����طŷ���ȴ��̶߳����С�
                �����߳�����������������������ͻὫ���߳�id�Ƶ�����ͣ�߳��б��С�
            ����ͣ�߳��б�
                ÿ����¼������dwThreadId
                ��������̱߳����ѣ���������״̬�󣬽�֮�Żص����ͷ��߳��б��С�
            �ܽ᣺
                1+1+3��һ����Ȥ�豸�б�һ���豸��д��ɻ����б������߳�id�б�
        GetQueuedCompletionStatus����˵����
           BOOL GetQueuedCompletionStatus(
                    HANDLE CompletionPort,
                    LPDWORD lpNumberOfBytes,
                    PULONG_PTR lpCompletionKey,
                    LPOVERLAPPED* lpOverlapped,
                    DWORD dwMilliseconds );
            CompletionPort��
                ����ĸ���ɶ˿ڽ��м��ӵȴ���
            lpNumberOfBytes��lpCompletionKey��lpOverlapped��
                ������������I/O��ɶ��еļ�¼����һ�µġ�
            dwMilliseconds��
                �ȴ���ʱʱ�䡣
            ȷ���ȴ����ص�ԭ��
                �������FALSE,���������ˡ�
                ���lpOverlapped��Ϊ�գ������м�¼�˴����롣
                ������GetLassError��ȡ������(��WAIT_TIMEOUT��ȴ���ʱ)��
        GetQueuedCompletionStatusEx����˵����
            BOOL GetQueuedCompletionStatusEx(
                    [in]  HANDLE CompletionPort,
                    [out] LPOVERLAPPED_ENTRY lpCompletionPortEntries,
                    [in]  ULONG ulCount,
                    [out] PULONG ulNumEntriesRemoved,
                    [in]  DWORD dwMilliseconds,
                    [in]  BOOL fAlertable );
            ��GetQueuedCompletionStatus��ͬ���ǣ��ú�����һ��ȡ��I/O��ɶ����еĶ��/�����
            CompletionPort:
                ����ĸ���ɶ˿ڽ��м��ӵȴ���
            lpCompletionPortEntries��
                ָ��OVERLAPPED_ENTRY���飬ʢ�Ŵ�I/O��ɶ�����ȡ���ĸ�����¼��
                struct OVERLAPPED_ENTRY
                    ULONG_PTR lpCompletionKey;
                    LPOVERLAPPED lpOverlapped;
                    ULONG_PTR Internal;                 //����
                    DWORD dwNumberOfBytesTransferred;
            ulCount��
                OVERLAPPED_ENTRY����ĳ���
            ulNumEntriesRemoved��
                ʵ��ȡ���˶�����
            dwMilliseconds��
                ��ʱ�ȴ�ʱ��
            fAlertable��
                �Ƿ��߳���Ϊ������״̬
                �����ΪFALSE��������һֱ�ȴ���ֱ��I/O��ɶ��в�Ϊ�գ���ʱ��
                ���ΪTRUE�����������һ���������������߳̽��������״̬��
        PostQueuedCompletionStatus����˵����
            BOOL PostQueuedCompletionStatus(
                    HANDLE CompletionPort,
                    DWORD dwNumberOfBytesTransferred,
                    ULONG_PTR dwCompletionKey,
                    LPOVERLAPPED lpOverlapped );
            �ú��������ֶ�ģ��i/o��д��ɣ�����Ӧ�����ݷŵ�ָ����ɶ˿ڵ�I/O��ɶ����С�
            ͨ���ú������Ϳ��Ը��̳߳��еĺ�������ͨ�ţ��磺Ҫ���̳߳��е����к������˳���
            ���Զ�ε��øú�������ָ���ض���dwCompletionKeyֵ�������е��߳�ִ��ʱ��
            ���ָ��ض�ֵ������߳̾��˳��ˣ�����߳̾ʹ���ɶ˿ڵ��߳��б����Ƴ��ˣ�
            ���N�Σ��̳߳��е������̶߳����������˳��ˡ�
            ע�⣺ʹ�����ַ�ʽ���̳߳��е��߳�ͨ��ʱ��Ӧ��ע�⵽��ջʽ���õ��ص㡣
        
        
