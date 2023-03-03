参：https://blog.csdn.net/qq_37653144/article/details/81942026
信号机制
    信号机制是一种使用信号来进行进程之间传递消息的方法
    信号的全称为软中断信号，简称软中断
    信号的本质是软件层次上对中断的一种模拟（软中断）
    它是一种异步通信的处理机制，事实上，进程并不知道信号何时到来
    在头文件<signal.h>中定义了64种信号，
    这些信号的名字都以SIG开头，且都被定义为正整数，称为信号编号
    可以用“kill -l”查看信号的具体名称，参：file://imgs/Linux信号.png
    编号为1~31的信号为早期Linux所支持的信号，是不可靠信号（非实时的），
    编号为34~63的信号时后来扩充的，称为可靠信号（实时信号）
    不可靠信号与可靠信号的区别在于前者不支持排队
    （这意味着如果内核已经注册了这个信号，那么便不会再去注册，
    对于进程来说，便不会知道本次信号的发生），可能会造成信号丢失
    而后者的注册机制是每收到一个可靠信号就会去注册这个信号，不会丢失。
信号的产生
    ·当用户按下某些终端按键后引发终端产生信号，如“Ctrl+C”等。
    ·硬件产生的异常信号，例如除数为0、无效的内存访问等。
     这种异常信号通常会由硬件检测并通知Linux内核，然后内核产生信号发送给相关进程。
    ·进程使用系统调用函数kill可以给一个进程或者进程组发送一个信号，
     此时发送和接收信号的进程/进程组的所有者必须相同。
    ·用户调用kill命令将信号发送给其他进程，如经常使用kill终止进程一样。
    ·当检测到某种软件条件已经发生，并将其通知有关进程的时候也会产生信号，
     例如SIGURG信号就是在接收到一个通过网络传送的外部数据时产生的。
信号处理方式
    Linux的每一个信号都有一个缺省的动作，典型的缺省动作是终止进程
    当一个信号到来的时候收到这个信号的进程会根据信号的具体情况提供一下三种不同的处理方式：
    ·对于需要处理的信号，指定处理函数，由该函数来处理。
    ·忽略某个信号，对该信号不做任何处理。
    ·对该信号的处理保留系统的默认值，这种缺省操作大多数使得进程终止，
     进程通过系统调用signal函数来指定进程对某个信号的处理行为。
信号处理过程
    Linux内核给一个进程发送软中断的方法是：
    在进程所在的进程表项的信号域设置对应信号的位（在PCB中设置）。
    如果信号发送给一个正在睡眠的进程，
    如果进程的优先级是可中断的，则唤醒进程，
    否则仅设置PCB中信号域相应的位而不唤醒进程。
    一个进程检查是否收到信号的时机是：
    一个进程在即将从内核态切换到用户态时；
    或者再一个进程要进入或离开一个适当的低调度优先级睡眠状态时。
    内核处理一个进程收到的软中断信号是在该进程的上下文中，
    因此进程必须处于运行状态。
    如果进程收到一个需要捕获的信号，
    会在进程从内核态返回到用户态时执行用户定义的函数，
    而且内核会在用户栈上创建一个新的空间来处理，
    该空间将返回地址的值设置成用户定义的处理函数的地址，
    这样进程从内核返回栈顶时就返回到用户定义的函数处，
    从函数返回再弹出栈顶时，才返回原先进入内核的地方。
Linux信号的使用方法
    注册信号
        指的是在目标进程中注册，该目标进程中有未决信号的信息。
        对于已经有自己的中断处理例程的信号而言，
        其注册就是一个用户进程自己定义的处理函数去替换Linux内核预定义的函数动作。
        例如“Ctrl+C”是中止当前进程的运行，
        按下组合键后会产生一个中断，当前进程会接收到一个SIGINT信号，
        然后找到对应的处理例程是终止当前进程。
        我们也可以自己注册信号，将SIGINT信号对应的处理例程改为我们想要的操作。
        struct sigpending{
            struct sigqueue *head, **tail;
            sigset_t signal;
        };
        struct sigqueue{
            struct sigqueue *next;
            siginfo_t info;
        }；
        其中 sigqueue结构组成的链称之为未决信号链，
        sigset_t称之为未决信号集，
        *head,**tail分别指向未决信号链的头部与尾部，
        siginfo_t info是信号所携带的信息。
        信号注册的过程就是将信号值加入到未决信号集sigset_t中，
        将信号所携带的信息加入到未决信号链的某一个sigqueue中去
        因此，对于可靠的信号，可能存在多个未决信号的sigqueue结构，
        对于每次信号到来都会注册
        而不可靠信号只注册一次，只有一个sigqueue结构。
        只要信号在进程的未决信号集中，
        表明进程已经知道这些信号了，还没来得及处理，或者是这些信号被阻塞。
        在Linux中，可以通过signal和sigaction函数注册信号
        并指定接收到该信号时需要完成的动作
        对于已经有自己的功能动作的信号而言其注册就是
        用一个用户自己定义的动作去替换Linux内核预定义的动作。
    signal函数
        signal函数可以为一个特定的信号（除了无法捕获的SIGKILL和SIGSTOP信号）
        注册相应的处理函数。
        如果正在运行的程序源代码里注册了针对某一信号的处理程序，
        不论当时程序执行到何处，一旦进程接收到该信号，相应的调用就会发生。
        #include <signal.h>
        void (*signal(int signum, void (*handler)(int)))(int);
        参数signum表示所注册函数针对的信号名称，
        参数handler通常是指向调用函数的函数指针，即所谓的信号处理函数。
        信号处理函数handler可能是用户自定义的一个函数，
        也可能是两个在头文件<signal.h>中进行定义的值：
        ·SIG_IGN：忽略signum指出的信号。
        ·SIG_DFL：调用系统定义的缺省信号处理。
        当signal函数调用成功后返回信号以前的处理配置，
        如果调用失败则返回SIG_ERR（-1）。
        需要注意的是并非程序执行到signal调用时就立即对指定的信号进行操作，
        因为信号的产生式无法预期的，
        利用signal设置信号处理函数只是告诉系统对这个信号用什么程序来处理。
    sigaction函数
        关于该函数更清晰的说明，参：https://www.cnblogs.com/52php/p/5813867.html
        相较于signal函数，sigaction函数在完成信号注册工作的同时提供了更多功能选择。
        #include <signal.h>
        int sigaction(int signum, const struct sigaction *act, struct sigaction *oldact);
        其中，参数signum指定要处理的信号，
        act和oldact都是指向信号动作结构的指针，该结构定义如下：
        struct sigaction {
            void (*sa_handler)(int);
            void (*sa_sigaction)(int, siginfo_t *, void *);
            sigset_t sa_mask;
            int sa_flags;
        };
        sa_handler用于指向信号处理函数的地址，参数sa_sigaction是指向函数的指针。
        它指向的函数有三个参数，其中第二个为siginfo_t结构体，定义如下
        struct siginfo_t {
            int si_signo;        //Signal number
            int si_errno;        //Errno value
            int si_code;         //Signal code
            pid_t si_pid;        //Sending process ID
            uid_t si_uid;        //Real user ID of sending process
            int si_status;       //Exit value or signal
            clock_t si_utime;    //User time consumed
            clock_t si_stime;    //System time consumed
            signal_t si_value;   //Signal value
            int si_int;          //POSIX.1b signal
            void *si_ptr;        //POSIX1.b signal
            void *si_addr;       //Memory location that caused fault
            int si_band;         //Band event
            int si_fd;           //File descriptor
        };
        sa_flags用于指示信号处理函数的不同选项，
        可以通过“|”连接不同的参数，从而实现所需的选项设置。
        具体的可选参数如下表所示
        sa_flags	    对应设置
        SA_NOCLDSTOP	用于指定信号SIGCHLD，当子进程被中断时，不产生此信号，当且仅当子进程结束时产生该信号
        SA_NOCLDWAIT	当信号为SIGCHLD时，此选项可以避免子进程的僵死
        SA_NODEFER	    当信号处理程序正在运行时，不阻塞信号处理函数自身的信号功能
        SA_NOMASK	    同SA_NODEFER
        SA_ONESHOT	    当用户注册的信号处理函数被调用过一次之后，该信号的处理程序恢复为缺省的处理函数
        SA_RESETHAND	同SA_ONESHOT
        SA_RESTART	    使本来不能进行自动重新运行的系统调用自动重新启动
        SA_SIGINFO	    表明信号处理函数是由sa_sigaction指定，而不是由sa_handler指定，它将显示更多处理函数的信息
        实例如下：
            #include <stdio.h>
            #include <stdlib.h>
            #include <signal.h>
            void signalDeal(int sig, siginfo_t *info, void *t) {
                if (sig == SIGINT) {
                    printf("Ctrl+C被按下\n");
                }
                else if (sig == SIGQUIT) {
                    printf("Ctrl+/被按下\n");
                }
                else {
                    printf("其他信号\n");
                }
            }
            int main(int argc, char *argv[])
            {
                struct sigaction act;
                act.sa_sigacion = signalDeal;
                sigempty(&act.sa_mask);
                act.sa_flags = SA_SIGINFO;
                sigaction(SIGINT, &act, NULL);
                sigaction(SIGQUIT, &act, NULL);
                while (1) {}
                return 0;
            }
    发送信号
        kill函数
            kill函数将信号发送给进程或者进程组。
            #include <signal.h>
            #include <sys/types.h>
            int kill(pid_t pid, int sig);
            其中pid参数的取值如下
            pid	        含义
            pid > 0	    将信号发送给进程号为pid的进程
            pid = 0	    将信号发送给与目前进程相同进程组的所有进程
            pid < 0 && pid != -1	向进程组ID为pid绝对值的进程组中的所有进程发送信号
            pid = -1	除发送给自身进程外，还向所有进程ID大于1的进程发送信号
            sig参数对应的是信号编码，当其为0（即空信号）时，实际不发送任何信号，
            但照常进行错误检查。因此可用于检查目标进程是否存在，
            以及当前进程是否具有向目标发送信号的权限。
        raise函数
            raise函数向自身所在进程发送一个信号。
            #include <signal.h>
            int raise(int sig);
        sigqueue函数
            sigqueue主要是针对实时信号提出的（当然也支持非实时信号）信号发送函数，
            通常与函数sigaction配合使用。
            #include <signal.h>
            int sigqueue(pid_t pid, int sig, const union sigval value);     
            typedef union sigval {
                int sival_int;
                void *sival_ptr;
            }sigval_t;
              sigqueue比kill传递了更多的附加信息，
              但sigqueue只能向一个进程发送信号，不能发送信号给一个进程组。
    Linux信号集
        在Linux系统的实际应用中，常常需要将多个信号组合起来使用，
        这种用来表示多个信号的数据类型被称为信号集（signal set），
        其定义格式为sigset_t。
        #include <signal.h>
        typedef struct {
            unsigned long sig[_NSIG_WORDS];
        }sigset_t;
        有5个函数用于信号集的操作：
        //前4个函数若调用成功则返回0，否则返回-1
        #include <signal.h>service
        //用于将参数set所指向的信号集设为空，即不包含任何信号
        int sigemptyset(sigset_t *set);    
        //用于将参数set所指向的信号集设定为满，即包含所有的信号
        int sigfillset(sigset_t *set);    
        //用于将参数signum所代表的信号添加到参数set所指向的信号集中
        int sigaddset(sigset_t *set, int signum);    
        //用于将参数signum所代表的信号从参数set所指向的信号集中删除
        int sigdelset(sigset_t *set, int signum);    
        //用于检查参数signum是否位于参数set所指向的信号集中，
        //如果为真则返回1，为假则返回0，出错则返回-1
        int sigismember(const sigset_t *set, int signum);  
    信号的阻塞和挂起
        在实际应用中，有时候既不希望进程在接收到信号时立刻中断，
        也不希望该信号完全被忽略，而是希望进程延迟处理。
        这可以通过阻塞信号的方法来实现。
        Linux提供了sigprocmask函数和和sigsuspend函数用于信号的阻塞和挂起。
        #include <signal.h>
        int sigprocmask(int how, const sigset_t *set, sigset_t *oldset);
        int sigsuspend(const sigset_t *mask);
        函数sigprocmask的参数set、oldset指向信号集。
        set指向一个信号集时，参数how表示sigprocmask函数如何对set所指向的
        信号集以及信号掩码进行操作。当参数set的值为NULL时，how的取值无效。
        当oldset不为NULL时，函数将进程当前的信号掩码写入oldset指向的信号集。
        how	        对应函数功能
        SIG_BLOCK	将set所指向的信号集中所包含的信号加到当前的信号掩码中，
                    即信号掩码与set信号集做逻辑或运算
        SIG_UNBLOCK	将set所指向的信号集中所包含的信号从当前的信号掩码中删除
        SIG_SETMASK	设定新的当前信号掩码为set所指向的信号集中所包含的信号
        函数sigsuspend的作用是挂起信号。
        在调用该函数后，进程停止执行，等待着开放信号的唤醒。
        
参：https://blog.csdn.net/lvqingyao520/article/details/81478086 
信号的处理过程    
    进程收到一个信号后不会被立即处理，而是在恰当 时机进行处理！
    什么是适当的时候呢？
    比如说中断返回的时候，或者内核态返回用户态的时候（这个情况出现的比较多）。
    信号不一定会被立即处理，
    操作系统不会为了处理一个信号而把当前正在运行的进程挂起（切换进程），
    挂起（进程切换）的话消耗太大了，如果不是紧急信号，是不会立即处理的。
    操作系统多选择在内核态切换回用户态的时候处理信号，
    这样就利用两者的切换来处理了（不用单独进行进程切换以免浪费时间）。
    总归是不能避免的，因为很有可能在睡眠的进程就接收到信号，
    操作系统肯定不愿意切换当前正在运行的进程，
    于是就得把信号储存在进程唯一的PCB（task_struct）当中。
    
参：https://blog.csdn.net/Chiang2018/article/details/82078965  
常见信号处理方式：
    （1）SIGCHLD在子进程退出时，将发送该信号给父进程，
         父进程可根据该信号完成对子进程PCB资源的回收。
    （2）SIGSTOP、SIGKILL不能被屏蔽、安装。
    （3）SIGSTOP和SIGCOUNT是配对的，一个进程收到SIGSTOP后会暂停执行，
         并屏蔽除SIGKILL外所有信号，在收到SIGCOUNT后，才会继续执行
    （4）信号可以唤醒处于sleep（）的进程
信号的产生    
    （1）、使用kill（）函数向指定进程发送一个信号，函数声明如下：
            //from /usr/include/asm-generic/signal.h
            int kill(pid_t pid,int sig);    
            可以使用kill(pid_t pid,0)来检测指定进程是否存在。成功返回0，失败返回-1。
    （2）、 使用raise（）函数给当前进程发送一个信号，函数声明如下：
            //from /usr/include/asm-generic/signal.h
            int raise(int sig);
            函数执行成功，返回0，失败返回-1。
    （3）、使用alarm（）函数可以持续的按照一定间隔发送一个SIGALARM信号，
            信号发给调用者（当前）进程，函数声明如下：
            //from /usr/include/asm-generic/signal.h
            unsigned int alarm(unsigned int seconds);
            函数使用时，若seconds值为0，则表示取消先前发出的信号。
            函数第一次调用时，执行成功返回0，失败返回-1。
            若之前已有调用，再次调用alarm（）则表示重置时间间隔，
            执行成功则返回距上次信号发送，剩余间隔时间。
            另外需要强调的是，子进程并不会继承父进程的alarm信号，
            但在调用exec（）函数执行新代码时，原来的设置的信号仍然有效。
            用alarm（）来当做定时器是不靠谱的，信号小于32的信号都是不可靠信号
            而且根据信号的处理时机也可知该时间并不精确
    （4）、 使用ualarm()持续产生SIGALARM信号，函数声明如下：
            //from /usr/include/asm-generic/signal.h
            __useconds_t ualarm(__useconds_t value，__useconds_t interval);
            函数将在value 微妙内产生SIGALARM信号，
            并在之后每interval微妙时，再次产生该信号。
安装信号
    （1）、 signal（）安装信号，函数声明如下：
            //from /usr/include/asm-generic/signal.h
            __sighandler_t signal(int sig,__sighandler_t handler);
            函数第1参数为收到的信号，第2个参数为接收此信号后的处理代码入口或以下几个宏：
             #define SIG_ERR  ((__sighandler_t  )  -1)   //返回错误
             #define SIG_DEF  ((__sighandler_t  )  0)    //执行信号默认参数
             #define SIG_IGN  ((__sighandler_t  )  1)    //忽略信号
    （2）、 sigaction()安装信号
            sigaction（）函数相对于signal（）函数来说，更为安全可靠，获取的信息更多，
            函数声明如下：
            //from /usr/include/asm-generic/signal.h
            struct sigaction
            {
                union
                {
                    //SIGDFL,SIG_IGN,类似于signal
                    __sighandler_t sa_handler; 
                    //当sa_flags为SA_SIGINFO时，使用此变量设置信号处理函数，
                    //并将获取信号发送时的信息保存在结构体info中，
                    //包括信号发送进程ID
                    void (*sa_sigaction)(int sig,struct siginfo_t* info,void*);
                }
                sigset_t sa_mask;        //屏蔽的信号集
                unsigned long sa_flags;  //特殊标志
                ...
            };
            int sigaction(int sig,struct sigaction* act,struct sigaction* oact);
            函数的第1个参数为信号值，第2个参数为欲设置的信号处理方式，
            第3个参数为原先的信号处理方式信息。
            另外sa_flags可以设置为以下值：
            SA_NOCLDSTOP:表示子进程在退出时，不生成SIGCHLD信号
            SA_RESTART:将指定的可中断函数将失败
            SA_RESETHAND:信号的处理方法将被重置为默认处理方式，即SIG_DFL
信号集处理
    函数sigprocmask（）用来设置当前进程屏蔽的信号集合，函数声明如下
    int sigprocmask(int how,sigset_t* set,sigset_t* oset);
    函数的第1个参数为更改信号集的方式，可以使用以下几个值
    #define  SIG_BLOCK  0  //第2个参数代表的信号集添加到当前进程屏蔽的信号集中
    #define  SIG_UNBLOCK 1 //第2个参数代表的信号集从当前进程屏蔽的信号集中删除
    #define  SIG_SETMASK 2 //设置第2个参数代表的信号集为当前进程屏蔽的信号集
    函数执行成功返回0，否则返回-1
    除了sigprocmask（）函数，还有其他方式，例如
    /*清空set代表的信号集*/
    int sigemptyset(sigset_t* set)
    /*添加信号sig到信号集set中*/
    int sigaddset(sigset_t* set,int sig);
    /*从信号集set中删除信号sig*/
    int sigdelset(sigset_t* set,int sig);
    /*检测信号sig是否在信号集set中*/
    int sigismember(sigset_t* set,int sig);
    /*检测信号集set是否为空信号集*/
    int sigisemptyset(sigset_t* set);
    /*将信号集left与信号集right按照逻辑与的方式合并到信号集set中*/
    int sigandset(sigset_t* set,sigset_t* left,sigset_t* right)；
    /*将信号集left与信号集right按照逻辑或的方式合并到信号集set中*/
    int sigandset(sigset_t* set,sigset_t* left,sigset_t* right)；
    
参：https://blog.csdn.net/challenglistic/article/details/124413135 
1、进程收到信号就会立即处理吗？
    进程收到某种信号的时候，并不是立即处理的。
    比如远处看到红绿灯变成红灯，我们会立即停下吗？
    并不会，我们会把看到红灯这件事记录在大脑中，等走到路口再停下
    进程当前可能在执行优先级更高的东西，所以要选择合适的时候再处理这个信号。
2、没有被立即处理的信号放在哪？
    我们看到红灯的时候，会把看到红灯这件事存在大脑中。
    既然信号不能被立即处理，已经到来的信号会被暂时保存起来，以供在合适的时候处理，
    应该保存在哪里呢？？——》进程控制块 task_struct
3、谁负责把信号存到指定位置？
    信号的本质就是数据，发送信号 ——> 向进程控制块 task_struct写入数据 ——>
    但是进程控制块属于内核，内核不相信任何人，所以由谁来写入数据 ——> OS！！
4、信号从产生到被处理所经历的过程
    信号发送的过程可以通过下面这张图来表示:
             信号产生前          信号发送后（未被处理）    信号发送后（被处理）
        __________|_____________________|_________________________|_______________
            信号产生的方式       信号保存的方式             信号处理的方式
    后面会针对每一步都会作详细的介绍，
    整个过程一共分成了三步：
    (1) 信号发送
        信号发送的方式多种多样，可以是键盘发送，如Ctr + C发送2号信号、Ctrl + \ 发送3号信号
        也可以是通过命令行指令发送，如
        kill -9 进程pid         #给对应的进程发送9号信号
         注意：第二种方式是通用的方法，2号信号也可以这样发送，如 kill -2  进程pid
    (2) 信号保存
        前面也提到了，信号是保存在进程控制块里面的，由OS来保存，具体的保存方式是 位图保存
        我们常见的信号有31个，也就是前31个，
        我们可以理解为进程使用无符号32位的整型来保存我们收到的信号
        （实际上Linux中位图的保存没有这么简单，这个在“信号保存”的博客中也会说明）
        当没有收到信号时，所有的比特位都是0，类似于 0000 0000 ....
        当我们收到了2号信号时，那就类似于 0100 0000 ....
        struct task_struct
        {
            uint32_t sigs;    //0000 0000 0000 ...
        }
    (3) 信号捕捉和处理
        后面会提到一个阻塞的概念，被阻塞的信号无法被捕捉到，既然无法被捕捉，自然就无法被处理，
        你托中间人给 同事甲 送生日礼物，中间人把礼物丢了，同事甲自然就没法处理礼物了