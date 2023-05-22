windows下常见的“设备”（“设备”：能够与之通信的任何东西），常见的设备有；
文件、目录、控制台、串口、并口、管道、套接字、邮件槽

windows尽可能地封装了设备之间的差异，这意味着，允许我们以相同的方式读写不同类型的设备。
但应意识到有些函数

打开设备函数：
    HANDLE CreateFile(  LPCTSTR lpFileName,   
                        DWORD dwDesiredAccess,        //以何种方式打开，如GENERIC_READ、GENERIC_WRITE 
                        DWORD dwShareMode,            //指定串口的共享属性
                        LPSECURITY_ATTRIBUTES lpSecurityAttributes, 
                        DWORD dwCreationDisposition,  //是否创建还是打开现有的文件
                        DWORD dwFlagsAndAttributes,   //标记和属性
                        HANDLE hTemplateFile);        //模板文件句柄
    利用CreateFile函数，我们不仅能打开文件、目录等设备，还能用以打开串口、并口、命名管道等设备，
    通过lpFileName传值的不同，区分不同的设备，如打开串口传"COM1"、"COM2"等，打开并口传“LPT1”、“LPT2”，
    打开控制台输入传"CONIN1"、"CONIN2"，打开控制台输出传"CONOUT1"、"CONOUT2"等。
    其它几种设备则是用别的函数创建/打开的，如串口使用Socket、accept或AcceptEx方法打开，
    控制台用CreateConsoleScreenBuffer或GetStdHandle打开，管道用CreatePipe打开等，这些作为一般性了解即可。
    注意，CreateFile失败时，返回的值不是NULL，而是INVALID_HANDLE_VALUE(-1)。

关闭设备函数：
    关闭设备函数，对大多数设备来说，使用BOOL CloseHandle(HANDLE hObject)即可，
    对socket，使用int closesocket(SOCKET sock)函数。

检查打开的设备句柄的类型
    DWORD GetFileType(HANDLE hDevice) 函数可以检查打开的是哪种设备，有以下返回值：
    0x0000 FILE_TYPE_UNKNOWN : 未知设备
    0x0001 FILE_TYPE_DISK    : 磁盘文件
    0x0002 FILE_TYPE_CHAR    ：字符文件（一般是并口、串口或控制台） 
    0x0003 FILE_TYPE_PIPE    ：管道文件
    0x8000 FILE_TYPE_REMOTE  ：远程文件
    
CreateFile函数详解
    CreateFile因为其丰富的参数，所以为我们提供了更强的定制性。
    如用于打开文件时，相对于使用fopen，CreateFile可以让我们进行更多的定制，
    如是否使用缓存，是否文件关闭自动删除，是否独占打开，是否异步打开，创建系统文件/隐藏文件等。
    下面就对这些参数做详细的说明：
    lpFileName
        这是参数前面的“打开设备函数”小节已经提到过的，该参数既可以是特定的名称，表示特定的设备，也可以是某个文件路径。
    dwDesiredAccess
        可以是下列值的组合形式：
        0   如果不需要读写该设备，而只想改变设备的配置（如修改文件的时间戳），可以传0
        GENERIC_READ  读
        GENERIC_WRITE 写
    dwShareMode
        控制设备的重复打开特性，可以为如下值的组合：
        0                 独占的访问，如果设备已经打开，再次打开该设备会失败。
        FILE_SHARE_READ   如果以这种方式打开，意味着后面再打开该设备时，不是以只读方式打开的，就是打开失败
                          如果在这之前，文件已经以非只读的方式打开了，那将使得本次打开失败
        FILE_SHARE_WRITE  如果以这种方式打开，意味着后面再打开该设备时，不是以只写方式打开的，就是打开失败
                          如果在这之前，文件已经以非只写的方式打开了，那将使得本次打开失败
        FILE_SHARE_READ|FILE_SHARE_WRITE  这种允许共享读写的打开方式和只共享读/只共享写的打开方式是相冲突的，
                          这意味着如果文件已这种方式打开了，就不能再以只共享读(/写)的方式打开（打开失败），
                          因为这会让系统搞不明白该文件究竟是只共享读(/写)，还是共享读写。反之亦然。
        FILE_SHARE_DELETE 删文件权限共享。使用该标记打开，则具有删除文件的权限。
    lpSecurityAttributes
        指向SECURITY_ATTRIBUTES结构，用以指定安全信息以及是否允许返回的句柄被子进程所继承。
        只有在NTFS格式磁盘中创建的文件，才会使用该参数（也可以传NULL表默认值），其它情况下不支持该参数，应该传NULL
    dwCreationDisposition
        可以是下列值：
        CREATE_NEW        创建新文件，如果该文件已经存在，则函数调用失败
        CREATE_ALWAYS     创建新文件，如果该文件已经存在，则覆盖原来文件（将文件截断为0）
        OPEN_EXISTING     打开已有文件，如果文件不存在，则打开失败（如果打开的是非文件设备，如串口，则必须使用该值）
        OPEN_ALWAYS       打开已有文件，如果文件不存在，则创建文件
        TRUNCATE_EXISTING 打开已有文件，并将文件截断为0，如果文件不存在，则函数调用失败
        注：当使用OPEN_ALWAYS时，如果文件已存在，尽管能正常打开并读写文件，但用GetLastError,仍然返回“文件已存在”错误
    dwFlagsAndAttributes
        从参数的名字就可以看出，它有两种功能：设置标记和设置属性
        支持的标记值有：            
            FILE_FLAG_NO_BUFFERING          0x20000000    读写文件时，不使用高速缓存，直接写入磁盘的扇区块
														  使用这种方式打开的文件，对文件的访问存在如下限制：
														  ·每次读写位置及读写的数据量大小必须为磁盘扇区大小的整数倍；
														  ·要写入文件的数据缓冲区（内存堆栈）也需是扇区对齐的（根据磁盘不同，
														  有的可能不强制此条），VirtualAlloc分配的缓冲区是内存页对齐的
														  ————内存页大小是扇区大小的整数倍。
														  可以使用GetDiskFreeSpace函数来确定卷扇区的大小。
            FILE_FLAG_RANDOM_ACCESS         0x10000000    提示计算机要对文件随机读写，如果使用了FILE_FLAG_NO_BUFFERING，
                                                          则该标记会忽略
            FILE_FLAG_SEQUENTIAL_SCAN       0x08000000    提示计算机不要提前读取文件，如果使用了FILE_FLAG_NO_BUFFERING，
                                                          则该标记会忽略
            FILE_FLAG_WRITE_THROUGH         0x80000000    禁止对文件写操作进行缓存，以防止数据丢失（读操作仍使用缓存），
                                                          如果是网络文件，则阻塞直到数据写入服务器磁盘
            FILE_FLAG_OVERLAPPED            0x40000000    为异步读写打开/创建文件。后面会有详细介绍。            
            FILE_FLAG_DELETE_ON_CLOSE       0x04000000    文件所有句柄都关闭时，文件自动删除。
            FILE_FLAG_BACKUP_SEMANTICS      0x02000000    为备份或还原操作而打开或创建文件。
            FILE_FLAG_POSIX_SEMANTICS       0x01000000    根据POSIX规则访问文件（即文件路径名区分大小写，linux下就是这样的）
                                                          注意，如果使用了该标记，那么windows应用程序可能会无法访问该文件
            FILE_FLAG_OPEN_REPARSE_POINT    0x00200000    不必关注
            FILE_FLAG_OPEN_NO_RECALL        0x00100000    不必关注
            FILE_FLAG_FIRST_PIPE_INSTANCE   0x00080000    不必关注
        支持的属性有：
            FILE_ATTRIBUTE_READONLY             0x00000001  打开或创建只读文件
            FILE_ATTRIBUTE_HIDDEN               0x00000002  打开或创建隐藏文件
            FILE_ATTRIBUTE_SYSTEM               0x00000004  打开或创建系统文件
            FILE_ATTRIBUTE_DIRECTORY            0x00000010  打开或创建目录
            FILE_ATTRIBUTE_NORMAL               0x00000080  打开或创建普通文件（不能和其它属性共用） 
            FILE_ATTRIBUTE_TEMPORARY            0x00000100  临时打开（如果有足够的高速缓存可用，就尽量不写入磁盘）
            FILE_ATTRIBUTE_ARCHIVE              0x00000020  打开或创建存档文件
            FILE_ATTRIBUTE_COMPRESSED           0x00000800  文件数据是压缩的
            FILE_ATTRIBUTE_ENCRYPTED            0x00004000  文件是经过加密的
            FILE_ATTRIBUTE_OFFLINE              0x00001000  文件随存在，但文件内容已被转移到脱机存储器中了。
            FILE_ATTRIBUTE_NOT_CONTENT_INDEXED  0x00002000  内容索引服务不会对文件进行索引
            FILE_ATTRIBUTE_VIRTUAL              0x00010000  未知
            FILE_ATTRIBUTE_DEVICE               0x00000040  未知
            FILE_ATTRIBUTE_SPARSE_FILE          0x00000200  未知
            FILE_ATTRIBUTE_REPARSE_POINT        0x00000400  未知
        注：如果同时使用 FILE_FLAG_DELETE_ON_CLOSE 和 FILE_ATTRIBUTE_TEMPORARY 参数，则会尽量创建不落地文件。
            但这受文件大小的限制，只有在文件不超过一定大小时，才会真正的不落地。
    hTemplateFile
        可以是一个已打开文件的句柄，也可以为空，如果传入的是一个句柄，则CreateFile会忽略dwFlagsAndAttributes参数，
        而使用与hTemplateFile文件同样的设置（前提是hTemplateFile文件必须是可读的）。另外该参数只对创建文件有用，
        如果是打开文件(文件已存在)，则忽略该参数。
                          
文件操作    
    获取文件大小
        DWORD GetFileSize(HANDLE hFile, LPDWORD lpFileSizeHigh);
        BOOL GetFileSizeEx(HANDLE hFile,PLARGE_INTEGER lpFileSize);
        DWORD WINAPI GetCompressedFileSize(LPCTSTR lpFileName,LPDWORD lpFileSizeHigh);
        GetFileSize返回值为文件大小，如果文件大小值超过DWORD，则用lpFileSizeHigh接收，
        但这种情况下，推荐使用GetFileSizeEx函数（除非是老的不支持该函数的系统）
        GetCompressedFileSize得到的是文件在磁盘上占用的字节数，
        如果文件数据在磁盘上是压缩存放的，则该值会小于GetFileSize得到的值。
    设置文件指针位置
        DWORD SetFilePointer( HANDLE hFile,   LONG lDistanceToMove, 
                              PLONG lpDistanceToMoveHigh,   DWORD dwMoveMethod); 
        BOOL SetFilePointerEx( HANDLE hFile, LARGE_INTEGER liDistanceToMove, 
                               PLARGE_INTEGER lpNewFilePointer, DWORD dwMoveMethod);
        参数：
          DistanceToMove控制指针移动距离，可以为负数。    
          MoveMethod指定移动基准点：FILE_BEGIN/FILE_CURRENT/FILE_END      
          lpNewFilePointer接收移动后的文件指针位置，通过将文件指针移动0字节，可以获取当前文件指针位置
        文件的指针位置是可以超过当前文件大小的，在新位置下的读写，会使文件中间一段数据是空的。
        如果文件打开是，使用的FILE_FLAG_NO_BUFFER参数，则文件移动位置只能是扇区大小的整数倍。
        用CreateFile创建/打开的同一个文件，因为有两个不同的内核对象来管理同一个文件，
        所以会各自持有一个文件读写指针，两者互不影响，
        但如果使用DuplicateHandle复制出来的内核对象句柄，因为都指向一个内核对象，所以共享文件读写指针。
    设置文件尾
        BOOL SetEndOfFile(HANDLE hFile);
        通过设置文件尾，可以截断或增大文件大小。前面的FILE_END参数值变为新的文件尾位置。
        通常在关闭的时候，系统负责设置文件尾。

同步读写文件
    读写操作
        BOOL ReadFile( HANDLE hFile, LPVOID lpBuffer,   
                       DWORD nNumberOfBytesToRead, 
                       LPDWORD lpNumberOfBytesRead,   
                       LPOVERLAPPED lpOverlapped); 
        BOOL WriteFile( HANDLE hFile, LPCVOID lpBuffer, 
                        DWORD nNumberOfBytesToWrite,   
                        LPDWORD lpNumberOfBytesWritten, 
                        LPOVERLAPPED lpOverlapped); 
         使用同步读写，lpOverlapped参数应该置为空，同时要求打开文件的时候，
        不能选用异步方式打开（不使用FILE_FLAG_OVERLAPPED标志）。
    刷新缓冲区
        BOOL FlushFileBuffers(HANDLE hFile);
        不仅读写文件可以使用缓存（默认缓存是开启的），
        读写串口、邮件槽、管道等设备，也可以使用缓存。
        使用FlushFileBuffers函数，可以将缓存中的数据强制写入到设备。
        要成功调用FlushFileBuffers函数，需要对设备具有写权限。
    结束阻塞
        BOOL CancelSynchronousIo(HANDLE hThread);
        当一个线程因同步操作而临时卡死时，可以借助另一个线程来强制结束本线程的同步操作，
        此时，原线程的同步操作退出阻塞状态，并失败返回，GetLassError返回ERROR_OPERATION_ABORTED。
        退出阻塞的线程从阻塞状态切换到就绪状态，表示可以被cpu调度。
        如果参数传入的不是读写阻塞的线程，则函数会返回FALSE，GetLasterror返回ERROR_NOT_FOUND。
        注意，hThread需要有THREAD_TERMINATE权限，否则CancelSynchronousIo会返回失败，
        GetLastError返回ERROR_ACCESS_DENIED。用CreateThread或_beginthreadex方法创建/打开的线程，
        是THREAD_ALL_ACCESS的，当然也包含了THREAD_TERMINATE权限。
        但是当使用OpenThread打开线程时，需注意通过参数控制打开具有THREAD_TERMINATE权限的线程。
        
异步读写文件
    以异步方式打开设备
        用CreateFile打开设备，并在dwFlagsAndAttributes参数中指定FILE_FLAG_OVERLAPPED标志。
    以异步方式读写
        BOOL ReadFile( HANDLE hFile, LPVOID lpBuffer,   
                       DWORD nNumberOfBytesToRead, 
                       LPDWORD lpNumberOfBytesRead,   
                       LPOVERLAPPED lpOverlapped); 
        BOOL WriteFile( HANDLE hFile, LPCVOID lpBuffer, 
                        DWORD nNumberOfBytesToWrite,   
                        LPDWORD lpNumberOfBytesWritten, 
                        LPOVERLAPPED lpOverlapped); 
        异步读写时，会检查文件是否已FILE_FLAG_OVERLAPPED方式打开的。
        lpNumberOfBytesRead/lpNumberOfBytesWritten参数在异步读写时，是没有意义的，因为函数返回时，
        还不能知道读写了多少数据，所以这个值传NULL就行。（通过下面的lpOverlapped检查读写了多少字节）
        pOverlapped指向OVERLAPPED结构。
        struct OVERLAPPED ：
            [out] DWORD Internal;           //返回错误码
            [out] DWORD InternalHigh;       //返回读写了多少字节
            [in]  DWORD Offset;             //异步读写位置（异步读写使用该指针，而忽略文件指针）
            [in]  DWORD OffsetHigh;         //异步读写位置（对于非文件设备，应该将这两个值设为0）
            [in]  HANDLE hEvent;
        当读写函数返回时，会先将Internal的值设为STATUS_PENDING（pend：悬挂、等候的意思）。
        非文件设备，不能指定读写位置，必须将Offset和OffsetHigh设为0。
        注意事项：
            1.驱动程序不一定按顺序响应i/o请求列表
              当请求了一次异步读/写后，系统通常把本次请求放到相应设备驱动的i/o请求列表中。
              但设备却不一定是按先入先出的顺序来响应该i/o请求列表的，如对于磁盘文件，为了降低磁头的
              移动和寻道时间，文件系统驱动会在i/o请求队列中优先寻找那些读写位置离当前磁头位置比较近的请求。
            2.文件读写操作不一定真的异步执行
              当请求了一次异步读/写后，系统不一定本次请求放到相应设备驱动的i/o请求列表中。
              例如读写文件时，如果数据已经在告诉缓存中了，那么系统就不会再跟磁盘驱动索要数据了，
              自然也不用把i/o请求放到磁盘驱动的i/o请求列表中了。
              在这种情况下，虽然文件是以异步方式打开的，但读写操作实际仍是同步操作。
              另外，对于某些操作，如向文件追加数据时，是一定以同步方式进行的，不管文件是以何种方式打开。
            3.正确认识ReadFile和WriteFile函数的返回值
              如果请求的I/O操作是以同步方式执行的，那么ReadFile和WriteFile会返回非0值。
              请求请求的I/O操作是以异步方式执行的，那么ReadFile和WriteFile会返回FALSE，
              但这不能判定是读写操作是否真的出错了，而是应该用GetLastError函数来检查（是否出错），
              如果GetLastError返回的是ERROR_IO_PENDING，说明函数执行成功了，i/o请求已被放到相应驱动的队列中了，
              如果是其它值，则通常是表明出错了，如果出错的原因不是因为参数问题，
              那通常是因为还有一定数量的i/o请求尚未完成，因此我们需要等一些i/o请求完成后，再调用ReadFile/WriteFile函数。
            4.在异步i/o返回之前，一定不能释放/销毁参数传入的OVERLAPPED结构。
              所以在声明OVERLAPPED结构对象时，通常避免使用局部变量的形式。
    取消队列中的i/o请求
        方式一：BOOL CancelIo(HANDLE hFile);
            通过该函数，可以将当前线程添加的、有关该文件的所有异步i/o请求从队列中删除。
        方式二：关闭文件
            通过这种方式，可以将有关该文件的所有异步i/o请求从队列中删除。
        方式三：线程终止
            通过这种方式，可以当前线程添加的所有异步i/o请求从队列中删除。
        方式四：BOOL CancelIoEx(HANDLE hFile, LPOVERLAPPED lpOverlapped);
            通过这种方式，可以有关该文件的、与lpOverlapped相关联的i/o请求从队列中删除。
            注意，与CancelIo函数不同的是，该函数不局限于当前线程添加的i/o请求。
            如果lpOverlapped传NULL，则效果同方式二，把文件相关的所有异步i/o请求从队列中删除。
        注：被取消的i/o请求，在OVERLAPPED返回的错误码是ERROR_OPERATION_ABORTED。

接受异步I/O请求完成通知
    1. 触发设备内核对象
       可使用WaitForSingleObject或WaitForMultipleObject等待设备内核对象
       异步读写方法会（在将i/o请求添加到队列之前）将设备内核对象设为未触发状态，
       而当设备驱动程序完成了i/o请求后，会将该内核对象设为触发状态。
       缺点：
            等待设备内核对象会将线程设为阻塞状态，这失去了文件异步读写的意义。
            而且他也不能处理对同一文件的多个异步读写请求的情况，
            因为只要有一个异步读写完成了，等待函数就返回，但很难判断是哪个异步读写返回了。
    2. 触发事件内核对象
       设备驱动完成某i/o请求后，不但能将设备内核对象设为触发状态，
       还能在OVERLAPPED的hEvent参数不为空的时候，调用SetEvent，将hEvent事件内核对象设为触发状态。
       所以，我们除了像方法1那样等待设备内核对象外，也可以等待hEvent事件内核对象。
       另外，为了稍微提高点性能，我们可以再调用SetFileCompletionNotificationModes函数，
       告诉驱动程序，但读写完成后，不用触发相应的设备内核对象。
       优缺点： 
            解决了方法1中，不能处理对同一文件的多个异步读写请求的缺陷，
            但同样，这会阻塞线程，失去了异步读写的意义。
            另外，当多个读写操作公用同一个OVERLAPPED结构时，也不能判断到底哪个读写函数完成了。
    3. 使用可提醒I/O
       当系统创建一个线程的时候，还会同步的创建一个“异步过程调用”（APC）队列，
       该队列是与这个线程对应的，我们可以在发起异步读写请求时，告诉设备驱动程序等i/o读写完成后，
       填充该队列。但使用传统的ReadFile/WriteFile函数是无法做到这一点的，需要调用
       ReadFileEx和WriteFileEx方法：
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
       这两个函数可以说是单独为异步读写而设计的，所以去掉了用以保存读写了多少字节的那个参数（本来异步读写也用不上）
       另外多了个lpCompletionRoutine参数，该参数要求传一个函数指针，当设备驱动程序完成I/O请求后，会填充APC队列，
       其中就包含该函数指针(另外还包含OVERLAPPED结构的指针)————正好是ReadFileEx/WriteFileEx的后两个参数。
       传入的回调函数的形式为： VOID WINAPI CompletionRoutine(DWORD dwError,DWORD dwNumBytes,OVERLAPPED *po);
       其中dwError和dwNumBytes参数，就是OVERLAPPED结构中的前两个成员：错误码和传输字节数。
       当线程执行到特定的等待函数时，线程就会检查APC队列，并调用队列项中的回调函数，
       这些特定的等待函数：
            DWORD SleepEx(DWORD dwMilliseconds, BOOL bAlertable);
            DWORD WaitForSingleObjectEx(HANDLE hHandle, DWORD dwMilliseconds, BOOL bAlertable);
            DWORD WaitForMultipleObjectsEx(DWORD nCount, const HANDLE* lpHandles,
                                           BOOL bWaitAll, DWORD dwMilliseconds, BOOL bAlertable);
            DWORD WINAPI SignalObjectAndWait(。。。);
            BOOL WINAPI GetQueuedCompletionStatusEx(。。。);
            DWORD MsgWaitForMultipleObjectsEx(。。。);
            可以看到，这些函数最后都有个bAlertable参数，可以控制是否将线程置为“可提醒状态”。
            这些函数也是为配合使用线程的“异步过程调用”队列而专门设计的。
            当执行这些函数的时候，会首先检查线程的APC队列，如果不为空，就会先执行APC队列项中的回调函数，
            当APC队列中的所有项都处理完成后，这些等待函数也不会进入阻塞状态了，而是成功返回。
            只有在调用这些等待函数时，APC队列为空的情况下，他们才会像一般的等待函数那样阻塞线程。
            这样等待的函数，会关注APC队列，当其不为空时，也会结束等待状态，并调用APC队列项中的等待函数。
            可通过这些等待函数的返回，查看他们是因为什么而结束等待的（也可用GetLastError），
            如果是WAIT_IO_COMPLETION，那表明等待函数结束的原因是处理了APC队列中的至少一项。
       缺点：
            因为使用了回调函数，会让代码写起来更复杂些。
            更大的问题是，该回调函数作为ReadFileEx或WriteFileEx的最后一个参数，
            这就决定了回调函数也是在发起请求的i/o线程中进行的。
            如果一个线程发起多个i/o请求，那该线程就得对所有的这些请求响应，
            即使其它线程都处于空闲状态。
            因为这种缺陷，所以这种方案不能有效的使用cpu资源，所以不推荐使用。
       优点：
            这里的优点，并不是讨论使用这种方法来等待i/o完成相对于使用前两种方法的优点，
            而是讨论基于基于APC机制，可以给我们带来哪些好处，
            这里提到一个对下面的讨论非常有用的函数 
            DWORD QueueUserAPC(PAPCFUNC pfnAPC,HANDLE hThread,ULONG_PTR dwData);
                其中PAPCFUNC的定义为 typedef VOID WINAPI (*PAPCFUNC)(ULONG_PTR dwParam);
                被唤醒的线程会执行该回调函数。
                第二个参数hThread是一个线程的句柄，
                告诉系统我们想要该项添加到哪个线程的APC队列中，
                这个线程可以是系统中的任何线程，如果hThread是在另一个进程中的，
                则pfnAPC所指向的函数地址，也必须是那个进程中的函数地址。
                QueueUserAPC函数的最后一个参数dwData，就是传给回调函数的值。
                该函数的返回值虽是DWORD类型的，但其实只有0和非0两种，0表成功。
            正是借助这个函数，让我们找到了一种线程间发送通知的方法，甚至可以跨进程，
            利用这种方法，可以让程序优雅的退出线程。
            当线程处于可提醒等待状态时，如果是因为别的线程（不一定是本进程的）调用
            QueueUserAPC而使得本线程被激活，则等待函数返回的值为WAIT_IO_COMPLETION，
            （如果是等待到了内核对象，则返回值为WAIT_OBJECT_0+n），
            此时，本线程就可以做一些清理工作，完成结束退出线程，
            此时虽然回调函数pfnAPC函数会被调用，但此时通常无需让它做任何工作，函数为空即可。
            有关 QueueUserAPC，参：
            file://..\..\WIN32\WSAWaitForMultipleEvents 和 MsgWaitForMultipleObjectsEx.txt
    4.  使用I/O完成端口
        设计理念：
            微软设计完成端口的背景是，多线程并发响应模型并不能如期望的那般发挥其优良的性能
            （多线程并发响应：每来一个客户端请求，服务端就创建一个响应线程），
            这是因为，当服务端有太多的线程同时存在时，线程切换花费了太多的时间，
            以至于cpu都没多少时间来真正执行线程任务了，另外，线程的创建和销毁也会花费一定的cpu时间。
            那个有都少个线程才算合理呢？答案是，同时运行的线程数=cpu核心数，注意这里指的是可被执行的线程，
            而不包括被阻塞的线程，一旦可运行线程数超过了cpu核心数，就会有线程处于就绪状态，
            等待cpu，而这就会使cpu花费时间来进行线程切换。
            I/O完成端口的解决办法就是使用线程池。
        CreateIoCompletionPort函数说明：
            HANDLE CreateIoCompletionPort(
                    HANDLE FileHandle,
                    HANDLE ExistingCompletionPort,
                    ULONG_PTR CompletionKey,
                    DWORD NumberOfConcurrentThreads );
            FileHandle：
                确切的说，应该是IO设备内核对象的句柄，因为除了文件内核对象，
                其它如socket、管道、邮件槽等内核对象也能使用完成端口。
                如果是文件内核对象，该文件内核对象必须是使用FILE_FLAG_OVERLAPPED方式打开的。
                如果传入的参数是INVALID_HANDLE_VALUE，则函数只是创建完成端口，而不与IO设备内核对象相关联，
                此时，ExistingCompletionPort参数必须传NULL，而CompletionKey参数则会被忽略。
            ExistingCompletionPort：
                完成端口内核对象的句柄
                如果传入一个已存在的完成端口内核对象的句柄，则函数将FileHandle与该完成端口相关联，
                函数返回的也将是该参数传入的那个完成端口的句柄，而不是创建一个新的完成端口内核对象。
                如果传入的是NULL，则函数创建一个完成端口内核对象，并将第一个参数传入的文件句柄(设备句柄)与之关联。
            CompletionKey：
                系统内部不会使用该参数，而仅仅是记录该参数，但完成端口检测到输入/输出完成事件时，将该参数再返回给用户使用。
            NumberOfConcurrentThreads：
                告诉完成端口在同一时间，最多能有多少线程处于可运行状态，如果传0，则I/O端口会使用默认值，即cpu数量。
                当ExistingCompletionPort不为空时，该参数被忽略。
            根据这几个参数相互制约的特点，可以将该函数分成两种应用情形：
                创建(不与任何设备关联的)完成端口内核对象：
                    第一个参数传INVALID_HANDLE_VALUE，相应的，第二个参数传NULL，
                    第三个参数因为被忽略，所以可以传0，只使用第四个参数。
                将文件(设备)内核对象关联到完成端口：
                    第一个参数传文件(设备)内核对象的句柄，第二个参数传已存在的完成端口的句柄，
                    因为此时第四个参数被回忽略，所以可以传0，第三个参数传自己需要的值。
            CreateIoCompletionPort不需要传SECURITY_ATTRIBUTES
                这是唯一的一个创建内核对象，不需要指定该参数的函数。
                这是因为该函数的设计初衷是仅供当前进程使用，不会涉及到多进程。
        随完成端口而创建的数据结构：
            设备列表
                每条记录包含：hDevice dwCompletionKey
                表示当前完成端口都对哪些文件(设备)内核对象感兴趣。
                hDevice即CreateIoCompletionPort传入的第一个参数。
                dwCompletionKey即CreateIoCompletionPort传入的第三个参数。
                每当CreateIoCompletionPort调用完成后，就会填充该列表。
                当进程将某设备关闭后，则系统将该表中的对应项删除。
                当一个异步I/O请求完成时，系统会检查每个完成端口的设备列表（一般一个进程中只会创建一个完成端口内核对象），
                看其是否对当前设备感兴趣，如果是，就会填充下面的I/O完成队列。
            I/O完成队列
                每条记录包含：dwByteTransferred dwCompletionKey pOverlapped dwError
                dwByteTransferred记录已传输的字节数，
                dwCompletionKey即将设备关联到完成端口时传入的值。
                pOverlapped设创建文件(设备)内核对象时指定的。
                dwError表错误码，其实就是pOverlapped指向结构的第一个成员的值。
                当完成端口关注的设备完成异步i/o请求时，会填充该队列。
                对于内部实际以同步方式完成的异步i/o请求，如果不希望将之添加到完成端口中，
                则可以调用SetFileCompletionNotificationModes函数，并传入FILE_SKIP_COMPLETION_PROT_ON_SUCESS标志，以提高性能。
                当等待线程队列中的一个线程得到执行时，就会删除本队列中的一项。
            等待线程栈
                每条记录包含：dwThreadId
                当某个线程调用GetQueuedCompletionStatus方法等待该完成端口时，即将其线程id记录在此表中。
                要将某个已存在于此表中的线程线程彻底移除，有三种途径：
                    当线程结束
                    将该线程与一个新的完成端口关联（即再次调用GetQueuedCompletionStatus方法）
                    销毁当前完成端口，则该等待线程栈自然也随之释放
                当某个文件(设备)的I/O完成时，就从该列表中唤醒一个线程，
                同时唤醒的线程的数量是受CreateIoCompletionPort函数的NumberOfConcurrentThreads参数制约的。
                之所以使用栈结构，是与线程池的特点相适应的，这里面存放的是可以使用的线程资源。
                线程池中线程的数量，按照经验，应该是CreateIoCompletionPort中NumberOfConcurrentThreads值的2倍大小。
            已释放线程列表
                每条记录包含：dwThreadId
                等待线程队列中的每个线程得到执行后，就将之从等待线程队列中移出，放到本队列中。
                当本线程再次调用GetQueuedCompletionStatus方法时，又将其重放放入等待线程队列中。
                当本线程因调用其他函数而阻塞，就会将该线程id移到已暂停线程列表中。
            已暂停线程列表
                每条记录包含：dwThreadId
                当挂起的线程被唤醒，结束阻塞状态后，将之放回到已释放线程列表中。
            总结：
                1+1+3：一个兴趣设备列表，一个设备读写完成缓存列表，三个线程id列表。
        GetQueuedCompletionStatus函数说明：
           BOOL GetQueuedCompletionStatus(
                    HANDLE CompletionPort,
                    LPDWORD lpNumberOfBytes,
                    PULONG_PTR lpCompletionKey,
                    LPOVERLAPPED* lpOverlapped,
                    DWORD dwMilliseconds );
            CompletionPort：
                表对哪个完成端口进行监视等待。
            lpNumberOfBytes、lpCompletionKey、lpOverlapped：
                这三个参数跟I/O完成队列的记录项是一致的。
            dwMilliseconds：
                等待超时时间。
            确定等待返回的原因：
                如果返回FALSE,表明出错了。
                如果lpOverlapped不为空，则其中记录了错误码。
                否则用GetLassError获取错误码(如WAIT_TIMEOUT表等待超时)。
        GetQueuedCompletionStatusEx函数说明：
            BOOL GetQueuedCompletionStatusEx(
                    [in]  HANDLE CompletionPort,
                    [out] LPOVERLAPPED_ENTRY lpCompletionPortEntries,
                    [in]  ULONG ulCount,
                    [out] PULONG ulNumEntriesRemoved,
                    [in]  DWORD dwMilliseconds,
                    [in]  BOOL fAlertable );
            与GetQueuedCompletionStatus不同的是，该函数会一下取出I/O完成队列中的多个/所有项。
            CompletionPort:
                表对哪个完成端口进行监视等待。
            lpCompletionPortEntries：
                指向OVERLAPPED_ENTRY数组，盛放从I/O完成队列中取出的各个记录。
                struct OVERLAPPED_ENTRY
                    ULONG_PTR lpCompletionKey;
                    LPOVERLAPPED lpOverlapped;
                    ULONG_PTR Internal;                 //无用
                    DWORD dwNumberOfBytesTransferred;
            ulCount：
                OVERLAPPED_ENTRY数组的长度
            ulNumEntriesRemoved：
                实际取出了多少项
            dwMilliseconds：
                超时等待时间
            fAlertable：
                是否将线程设为可提醒状态
                如果设为FALSE，函数会一直等待，直到I/O完成队列不为空，或超时。
                如果为TRUE，则会像本章上一节所讲的那样，线程进入可提醒状态。
        PostQueuedCompletionStatus函数说明：
            BOOL PostQueuedCompletionStatus(
                    HANDLE CompletionPort,
                    DWORD dwNumberOfBytesTransferred,
                    ULONG_PTR dwCompletionKey,
                    LPOVERLAPPED lpOverlapped );
            该函数用于手动模拟i/o读写完成，将相应的数据放到指定完成端口的I/O完成队列中。
            通过该函数，就可以跟线程池中的函数进行通信，如：要让线程池中的所有函数都退出，
            可以多次调用该函数，并指定特定的dwCompletionKey值，当池中的线程执行时，
            发现该特定值，则该线程就退出了，则该线程就从完成端口的线程列表中移除了，
            如此N次，线程池中的所有线程都能正常的退出了。
            注意：使用这种方式跟线程池中的线程通信时，应该注意到其栈式调用的特点。
        
        
