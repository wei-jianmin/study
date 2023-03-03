当一个进程初始化的时候，他并没有任何与线程池有关的开销。
但是一旦调用了新的线程池函数，系统就会为进程创建相应的内核资源，
其中的一些资源在进程终止之前都将一直存在：
系统会以进程的名义来分配线程、其它内核对象以及内部数据结构。

线程池的工作模式：
  维护一个任务队列
  维护一个线程池
  线程池中的函数依次从任务队列中取任务并执行
  线程池中的函数执行完一个函数后，继续从任务队列中取下一个函数
  如果任务队列为空，线程取不到函数，则等待
  线程池应该提供接口让用户添加任务
  任务队列满时，无法添加新任务（失败或阻塞）
  
线程池的使用情形：
    以异步方式调用函数：
        这种方式可以认为是让线程池中的线程立即处理任务队列中的工作项。
        简单方式：
            BOOL TrySubmitThreadpoolCallback(PTP_SIMPLE_CALLBACK pfns, PVOID pv, PTP_CALLBACK_ENVIRON pcbe);
                使用该函数，会自动创建一个工作项，并将之添加到线程池的任务队列中，
                该函数的前两个参数，会由工作项来记录，
                当工作项被分配给某个线程时，线程会执行pfns函数，并将pv参数传给该函数
                pfns回调函数的原型为：
                    void _stdcall callback_func(PTP_CALLBACK_INSTANCE Instance, PVOID Context);
                    PTP_CALLBACK_INSTANCE结构未知，所以在回调函数中我们基本也使用该参数
                pcbe参数现在可临时传NULL，后面会对该参数进行详细介绍
            注意，我们不用手动调用CreateThread这样的函数来创建线程，
            系统内部会自动分配适当数目的线程来执行任务队列中的工作项。
            系统可能会根据任务的执行情况，新增或销毁线程，所以线程池中的线程数不是一成不变的。
            当内存不足或配额限制，该函数可能会调用失败。所以如果一个任务函数需要等待另一个任务函数的信号，则用这种方式可能有问题。
            如果需要将函数对应的工作项重复提交到任务队列，则需要使用下面这种创建工作项和提交工作项分开的模式。
        显式的控制工作项（注：可称为立即工作项/简单工作项模式）：
            PTP_WORK CreateThreadpoolWork(PTP_WORK_CALLBACK pfnwk, PVOID pv, PTP_CALLBACK_ENVIRON pcbe);
                手动创建一个工作项，工作项中会记录传入的这三个参数
                pfnwk的函数原型为：
                    void __stdcall callback_func(PTP_CALLBACK_INSTANCE Instance, PVOID Context, PTP_WORK Work);
                    该回调函数与上面使用简单方式时的回调函数相比，多了个PTP_WORK参数，该参数值 = CreateThreadpoolWork的返回值
            VOID SubmitThreadpoolWork(PTP_WORK pwk);
                把上面创建的工作项添加到任务列表中
            VOID WaitForThreadpoolWorkCallbacks(PTP_WORK pwk, BOOL fCancelPendingCallbacks);
                fCancelPendingCallbacks为TRUE : 撤销提交的工作项
                    如果工作项还没被线程池执行，则该工作项(从任务队列中)标记为"已取消"，函数立即返回
                    如果工作项正在被线程池执行，则阻塞，等执行的工作项完成后，函数返回
                    如果传入一个没有提交（到任务列表中）的工作项，则函数立即返回
            VOID CloseThreadpoolWork(PTP_WORK pwk);
                当不再需要一个工作项的时候，应该调用此函数。如果该工作项的回调函数正在执行，还未完成，
                则会等到回调函数完成后，该工作项再自动删除（该函数仍立即返回），否则，会立即删除该工作项。
                如果在一个任务列表中的工作项，调用了该方法，则在线程池处理到该任务项的时候，会崩溃。
        每隔一段时间，调用函数（注：可称为计时器[等待的]工作项模式）
            适用情形：
                上面的情形，当一个工作项被提交后，工作项没有任何等待条件，只要正在运行的线程数没有达到限定值，
                （工作项）对应的工作线程就立即执行。
                而现实中，有时我们希望给工作线程（或工作项）等待一个触发条件，如等待一段时间或等待一个内核对象。
                要实现这种等待的要求，用上面的模式也可以很容易做到
                ————只要把计时器内核对象或其他内核对象放到工作线程的开始位置即可。
                但我们还有更直接的办法，即用这里的等待计时器/内核对象/IO的工作项模式。
            优点：
                如上，如果为每个任务项(工作线程)创建一个可等待的计时器对象，则会创建多个计时器对象，造成系统资源浪费。
                如果多个任务项(工作线程)之间公用一个计时器对象，那个该计时器对象就是一种临界资源，又会引来线程同步的问题。
                可等待工作项，就是把可等待计时器的特性融入了进来，这样，我们就无需再在工作线程中专门创建可等待计时器了。
            PTP_TIMER CreateThreadpoolTimer(PTP_TIMER_CALLBACK pfnti, PVOID pv, PTP_CALLBACK_ENVIRON pcbe);
                可以看到，CreateThreadpoolWork返回的是PTP_WORK，表立即工作项，而这里返回的是PTP_TIMER，表可等待工作项。
                他的第一个参数也是特有的，跟CreateThreadpoolWork不同（后两个参数一致）
                PTP_TIMER_CALLBACK : (与PTP_SIMPLE_CALLBACK的区别在于第三个参数PTP_TIMER上)
                    void __stdcall callback_func(PTP_CALLBACK_INSTANCE Instance, PVOID Context, PTP_TIMER Timer);
                        传入的Timer参数 = 上面的CreateThreadpoolTimer的返回值，
                        这是个计时器对象，可以在工作线程（该回调函数）中使用。
            VOID SetThreadpoolTimer(PTP_TIMER pti, PFILETIME pftDueTime, DWORD msPeriod, DWORD msWindowLength);
                把上面创建的工作项添加到任务列表中 #这句话在这里的理解应该时，等到了设定时间后，系统自动将该工作项放入任务列表中
                猜测这里面应该根据传入的pftDueTime、msPeriod、msWindowLength参数，对计时器对象pti进行设置。
                如果线程池超负荷，则可能延误计时器工作项。
                pftDueTime
                    第一次调用该回调函数在什么时候
                    <0时(!=-1)： 表相对时间，以微秒为单位
                    -1时：  表立即开始
                    >0时：  表绝对时间，以100纳秒为单位，从1600年1月1日开始计算（可以预见正常没人会这么用）
                    注意到这是个输入输出参数，所以猜测计时器工作项会不断的修改该值。
                msPeriod
                    第一次调用之后，每隔多久重复调用一次，如果传0，则不重复（就调用一次）
                msWindowLength
                    新触发时间 = in (原触发时间，原触发时间+msWindowLength)，微秒为单位
                    如果预计可能有多个计时器工作项将在相同时间点上被触发，则可以使用这个参数，让这些计时器的触发时间有一定随机性。
                    该参数的另一个作用是，可以将多个触发时间相近的计时器工作项合并为一组，让一个线程来处理他们
                        例：如果不使用该参数（设为0），任务列表中只有两个计时器工作项，单次触发，触发时间分别在第5微秒、第8微秒
                        则执行时，会在第5微秒，从线程池中获取一个线程，处理那个触发的工作项，再把线程放回线程池，再等到第8微秒，
                        再从线程池取出一个线程，处理新触发的工作项。
                        如果使用该参数，让msWindowLength=4，那系统会智能的算出：第一个工作项可以在第5~9微秒的任意时刻触发，
                        第二个工作项允许在第8~12微秒的任意时刻触发，所以选择在第8~9微秒的某个时刻，让这两个工作项同时触发，
                        然后从线程池取出一个线程，让它依次执行完这两个工作项，这样，该线程就不必在中途返回线程池了。
                重复调用该函数，pti仍使用之前的值，其它参数使用新值，这样可以重置计时器工作项。
            BOOL IsThreadpoolTimerSet(PTP_TIMER pti);
                检查某个计时器工作项是否被触发
            VOID WaitForThreadpoolTimerCallbacks(PTP_TIMER pti, BOOL fCancelPendingCallbacks);
                效果同 WaitForThreadpoolWorkCallbacks
            VOID CloseThreadpoolTimer(PTP_TIMER pti);
                效果同 CloseThreadpoolWork 
        内核触发时，调用函数
                    


            

            
    
