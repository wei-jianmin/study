PaExec
在服务中启动带有界面的程序
    参:https://cloud.tencent.com/developer/article/1424933
    4.2 突破SESSION 0隔离创建用户进程
        引言：
            病毒木马通常会把自己注入系统服务进程或是伪装成系统服务进程，并运行在SESSION 0中。
            处于SESSION 0中的程序能正常执行普通程序的绝大部分操作，但是个别操作除外。
            例如，处于SESSION 0中的系统服务进程，无法与普通用户进程通信，
            不能通过Windows消息机制进行通信，更不能创建普通的用户进程。
            在Windows XP、Windows Server 2003，以及更老版本的Windows操作系统中，
            服务和应用程序使用相同的会话（SESSION）来运行，
            而这个会话是由第一个登录到控制台的用户来启动的，该会话就称为SESSION 0。
            将服务和用户应用程序一起在SESSION 0中运行会导致安全风险，因为服务会使用提升后的权限来运行，
            而用户应用程序使用用户特权（大部分都是非管理员用户）运行，
            这会使得恶意软件把某个服务作为攻击目标，通过“劫持”该服务以达到提升自己权限级别的目的。
            从Windows VISTA开始，只有服务可以托管到SESSION 0中，用户应用程序和服务之间会进行隔离，
            并需要运行在用户登录系统时创建的后续会话中。
            如第一个登录用户创建 Session 1，第二个登录用户创建Session 2，以此类推。
            使用不同会话运行的实体（应用程序或服务）如果不将自己明确标注为全局命名空间，
            并提供相应的访问控制设置，那么将无法互相发送消息，共享UI元素或共享内核对象。
            虽然Windows 7及以上版本的SESSION 0给服务层和应用层间的通信造成了很大的难度，
            但这并不代表没有办法实现服务层与应用层间的通信与交互。
            微软提供了一系列以WTS（Windows Terminal Service，Windows终端服务）开头的函数，
            从而可以完成服务层与应用层的交互。
        相关函数：
            1．WTSGetActiveConsoleSessionId函数
                检索控制台会话的标识符Session Id。
                控制台会话是当前连接到物理控制台的会话。
                该函数可以用来获取当前活动的会话ID，
                有时候我们通过枚举explorer的相关信息，来获取相关进程的信息，
                但windows是个多用户操作系统，
                当多个用户登录时会使通过枚举explorer而得到的用户信息不准确。
                所以应当先用WTSGetActiveConsoleSessionId获得当前会话ID，
                再通过枚举进程，通过比较sessionID进而得到的消息比较可靠。
                函数声明
                    DWORD WTSGetActiveConsoleSessionId(void)
                参数  
                    无参数
                返回值
                    如果执行成功，则返回连接到物理控制台的会话标识符。
                    如果没有连接到物理控制台的会话（例如，物理控制台会话正在附加或分离），
                    则此函数返回0xFFFFFFFF。
            2．WTSQueryUserToken函数
                获取由Session Id指定的登录用户的主访问令牌。
                要想成功调用此功能，则调用应用程序必须在本地系统账户的上下文中运行，并具有SE_TCB_NAME特权。
                函数声明
                    BOOL WTSQueryUserToken(_In_  ULONG   SessionId, _Out_ PHANDLE phToken)
                参数
                    SessionId [in]
                        远程桌面服务会话标识符。在服务上下文中运行的任何程序都将具有一个值为0的会话标识符。
                    phToken [out]
                        如果该功能成功，则会收到一个指向登录用户令牌句柄的指针。
                        请注意，必须调用CloseHandle函数才能关闭该句柄。
                返回值
                    如果函数成功，则返回值非零，phToken参数指向用户的主令牌；如果函数失败，则返回值为零。
            3．DuplicateTokenEx函数
                创建一个新的访问令牌，它与现有令牌重复。此功能可以创建主令牌或模拟令牌。
                函数声明
                    BOOL WINAPI DuplicateTokenEx(
                        _In_     HANDLE                       hExistingToken,
                        _In_     DWORD                        dwDesiredAccess,
                        _In_opt_ LPSECURITY_ATTRIBUTES        lpTokenAttributes,
                        _In_     SECURITY_IMPERSONATION_LEVEL ImpersonationLevel,
                        _In_     TOKEN_TYPE                   TokenType,
                        _Out_    PHANDLE                      phNewToken)
                参数
                    hExistingToken [in]
                        使用TOKEN_DUPLICATE访问权限打开访问令牌的句柄。
                    dwDesiredAccess [in]
                        指定新令牌的请求访问权限。
                        要想请求对调用者有效的所有访问权限，请指定MAXIMUM_ ALLOWED。
                    lpTokenAttributes [in，optional]
                        指向SECURITY_ATTRIBUTES结构的指针，该结构指定新令牌的安全描述符，
                        并确定子进程是否可以继承令牌。
                        如果lpTokenAttributes为NULL，则令牌获取默认的安全描述符，并且不能继承该句柄。
                    ImpersonationLevel [in]
                        指定SECURITY_IMPERSONATION_LEVEL枚举中指示新令牌模拟级别的值。
                    TokenType [in]
                        从TOKEN_TYPE枚举中指定以下值之一。
                        值                   含    义
                        TokenPrimary         新令牌是可以在CreateProcessAsUser函数中使用的主令牌
                        TokenImpersonation   新令牌是一个模拟令牌
                    phNewToken [out]
                        指向接收新令牌的HANDLE变量的指针。
                        新令牌使用完成后，调用CloseHandle函数来关闭令牌句柄。
                    返回值
                        如果函数成功，则函数将返回一个非零值；
                        如果函数失败，则返回值为零。
            4．CreateEnvironmentBlock函数
                检索指定用户的环境变量，然后可以将此块传递给CreateProcessAsUser函数。
                函数声明
                    BOOL WINAPI CreateEnvironmentBlock(
                        _Out_    LPVOID *lpEnvironment,
                        _In_opt_ HANDLE hToken,
                        _In_     BOOL   bInherit)
                参数
                    lpEnvironment [out]
                        当该函数返回时，已接收到指向新环境块的指针。
                    hToken [in，optional]
                        Logon为用户，从LogonUser函数返回。
                        如果这是主令牌，则令牌必须具有TOKEN_QUERY和TOKEN_DUPLICATE访问权限。
                        如果令牌是模拟令牌，则必须具有TOKEN_QUERY权限。
                        如果此参数为NULL，则返回的环境块仅包含系统变量。
                    bInherit[in]
                        指定是否可以继承当前进程的环境。
                        如果该值为TRUE，则该进程将继承当前进程的环境；
                        如果此值为FALSE，则该进程不会继承当前进程的环境。
                    返回值
                        如果函数成功，则函数将返回TRUE；如果函数失败，则返回FALSE。
            5．CreateProcessAsUser函数
                创建一个新进程及主线程，新进程在由指定令牌表示的用户安全上下文中运行。
                函数声明
                    BOOL WINAPI CreateProcessAsUser(
                        _In_opt_    HANDLE                hToken,
                        _In_opt_    LPCTSTR               lpApplicationName,
                        _Inout_opt_ LPTSTR                lpCommandLine,
                        _In_opt_    LPSECURITY_ATTRIBUTES lpProcessAttributes,
                        _In_opt_    LPSECURITY_ATTRIBUTES lpThreadAttributes,
                        _In_        BOOL                  bInheritHandles,
                        _In_        DWORD                 dwCreationFlags,
                        _In_opt_    LPVOID                lpEnvironment,
                        _In_opt_    LPCTSTR               lpCurrentDirectory,
                        _In_        LPSTARTUPINFO         lpStartupInfo,
                        _Out_       LPPROCESS_INFORMATION lpProcessInformation)
                参数
                    hToken [in，optional]
                        表示用户主令牌的句柄。
                        句柄必须具有TOKEN_QUERY、TOKEN_DUPLICATE和TOKEN_ASSIGN_PRIMARY访问权限。
                    lpApplicationName [in，optional]
                        要执行模块的名称。该模块可以基于Windows应用程序。
                    lpCommandLine [in，out，optional]
                        要执行的命令行。 该字符串的最大长度为32K个字符。 
                        如果lpApplicationName为NULL，则lpCommandLine模块名称的长度限制为MAX_PATH个字符。
                    lpProcessAttributes [in，optional]
                        指向SECURITY_ATTRIBUTES结构的指针，该结构指定新进程对象的安全描述符，
                        并确定子进程是否可以继承返回进程的句柄。
                        如果lpProcessAttributes为NULL或lpSecurityDescriptor为NULL，
                        则该进程将获得默认的安全描述符，并且不能继承该句柄。
                    lpThreadAttributes [in，optional]
                        指向SECURITY_ATTRIBUTES结构的指针，该结构指定新线程对象的安全描述符，
                        并确定子进程是否可以继承返回线程的句柄。
                        如果lpThreadAttributes为NULL或lpSecurityDescriptor为NULL，
                        则线程将获取默认的安全描述符，并且不能继承该句柄。
                    bInheritHandles [in]
                        如果此参数为TRUE，则调用进程中的每个可继承句柄都由新进程继承；
                        如果参数为FALSE，则不能继承句柄。请注意，继承的句柄具有与原始句柄相同的值和访问权限。
                    dwCreationFlags [in]
                        控制优先级和进程创建的标志。
                    lpEnvironment [in，optional]
                        指向新进程环境块的指针。如果此参数为NULL，则新进程将使用调用进程的环境。
                    lpCurrentDirectory [in，optional]
                        指向进程当前目录的完整路径。
                        如果此参数为NULL，则新进程将具有与调用进程相同的当前驱动器和目录。
                    lpStartupInfo [in]
                        指向STARTUPINFO或STARTUPINFOEX结构的指针。
                        用户必须具有对指定窗口站和桌面的完全访问权限。
                    lpProcessInformation [out]
                        指向一个PROCESS_INFORMATION结构的指针，用于接收新进程的标识信息。
                        PROCESS_INFORMATION中的句柄必须在不需要时使用CloseHandle关闭。
                返回值
                    如果函数成功，则函数将返回一个非零值；如果函数失败，则返回零。
        实现原理 
            由于SESSION 0的隔离，使得在系统服务进程内不能直接调用CreateProcess等函数创建进程，
            而只能通过CreateProcessAsUser函数来创建。这样，创建的进程才会显示UI界面，与用户进行交互。
            在SESSION 0中创建用户桌面进程具体的实现流程如下所示。
            首先，调用WTSGetActiveConsoleSessionId函数来获取当前程序的会话ID，即Session Id。
            调用该函数不需要任何参数，直接返回Session Id。
            根据Session Id继续调用WTSQueryUserToken函数来检索用户令牌，并获取对应的用户令牌句柄。
            在不需要使用用户令牌句柄时，可以调用CloseHandle函数来释放句柄。
            其次，使用DuplicateTokenEx函数创建一个新令牌，并复制上面获取的用户令牌。
            设置新令牌的访问权限为MAXIMUM_ALLOWED，这表示获取所有令牌权限。
            新访问令牌的模拟级别为SecurityIdentification，而且令牌类型为TokenPrimary，
            这表示新令牌是可以在CreateProcessAsUser函数中使用的主令牌。
            最后，根据新令牌调用CreateEnvironmentBlock函数创建一个环境块，用来传递给CreateProcessAsUser使用。
            在不需要使用进程环境块时，可以通过调用DestroyEnvironmentBlock函数进行释放。
            获取环境块后，就可以调用CreateProcessAsUser来创建用户桌面进程。
            CreateProcessAsUser函数的用法以及参数含义与CreateProcess函数的用法和参数含义类似。
            新令牌句柄作为用户主令牌的句柄，指定创建进程的路径，设置优先级和创建标志，
            设置STARTUPINFO结构信息，获取PROCESS_INFORMATION结构信息。
            经过上述操作后，就完成了用户桌面进程的创建。
            但是，上述方法创建的用户桌面进程并没有继承服务程序的系统权限，只具有普通权限。
            要想创建一个有系统权限的子进程，这可以通过设置进程访问令牌的安全描述符来实现，
            具体的实现步骤在此就不详细介绍了。
        编码实现 
            // 突破SESSION 0隔离创建用户进程
            BOOL CreateUserProcess(char *lpszFileName)
            {
                // 变量 (略)
                do
                {
                    // 获得当前Session Id
                    dwSessionID = ::WTSGetActiveConsoleSessionId();
                    // 获得当前会话的用户令牌
                    if (FALSE == ::WTSQueryUserToken(dwSessionID, &hToken))
                    {
                        ShowMessage("WTSQueryUserToken", "ERROR");
                        bRet = FALSE;
                        break;
                    }
                    // 复制令牌
                    if (FALSE == ::DuplicateTokenEx(hToken, MAXIMUM_ALLOWED, NULL,
                        SecurityIdentification, TokenPrimary, &hDuplicatedToken))
                    {
                        ShowMessage("DuplicateTokenEx", "ERROR");
                        bRet = FALSE;
                        break;
                    }
                    // 创建用户会话环境
                    if (FALSE == ::CreateEnvironmentBlock(&lpEnvironment,
                        hDuplicatedToken, FALSE))
                    {
                        ShowMessage("CreateEnvironmentBlock", "ERROR");
                        bRet = FALSE;
                        break;
                    }
                    // 在复制的用户会话下执行应用程序，创建进程
                    if (FALSE == ::CreateProcessAsUser(hDuplicatedToken,
                        lpszFileName, NULL, NULL, NULL, FALSE,
                        NORMAL_PRIORITY_CLASS | CREATE_NEW_CONSOLE | CREATE_UNICODE_ENVIRONMENT,
                        lpEnvironment, NULL, &si, &pi))
                    {
                        ShowMessage("CreateProcessAsUser", "ERROR");
                        bRet = FALSE;
                        break;
                    }
                } while (FALSE);
                // 关闭句柄，释放资源 (略)
                return bRet;
            }