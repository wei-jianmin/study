MSDN-TLS
    TLS索引通常在进程或DLL初始化期间分配。
    分配后，进程的每个线程都可以使用TLS索引访问其自己的TLS存储插槽。
    该线程在随后的TlsGetValue调用中指定相同的索引，以检索存储的值。
    常数TLS_MINIMUM_AVAILABLE定义每个进程中可用的最小TLS索引数。
    对于所有系统，此最小值至少应为64。
    TLS索引跨进程边界无效。 
    DLL无法假定在一个进程中分配的索引在另一进程中有效。
    TLS索引存储在DLL的全局或静态变量中。
TLS--线程局部存储(Thread Local Storage)
    用来将数据与一个正在执行的指定线程关联起来
    如果需要在一个线程内部的各个函数调用都能访问、
    但其它线程不能访问的变量
    (被称为static memory local to a thread 线程局部静态变量)，
    就需要新的机制来实现。这就是TLS。
进程级的数据
    进程中的全局变量与函数内定义的静态(static)变量，
    是各个线程都可以访问的共享变量。
    在一个线程修改的内存内容，对所有线程都生效。
    这是一个优点也是一个缺点。
    说它是优点，线程的数据交换变得非常快捷。
    说它是缺点，一个线程死掉了，其它线程也性命不保; 
    多个线程访问共享数据，需要昂贵的同步开销，
    也容易造成同步相关的BUG。
TLS的实现
    线程局部存储在不同的平台有不同的实现，可移植性不太好。
    幸好要实现线程局部存储并不难，
    最简单的办法就是建立一个全局表，通过当前线程ID去查询相应的数据，
    因为各个线程的ID不同，查到的数据自然也不同了。
    大多数平台都提供了线程局部存储的方法，无需要我们自己去实现：
    linux的实现:
    　　int pthread_key_create(pthread_key_t *key, void (*destructor)(void*));
    　　int pthread_key_delete(pthread_key_t key);
    　　void *pthread_getspecific(pthread_key_t key);
    　　int pthread_setspecific(pthread_key_t key, const void *value);
TSL的功能
    主要是为了避免多个线程同时访存同一全局变量或者静态变量时所导致的冲突，
    尤其是多个线程同时需要修改这一变量时。
    为了解决这个问题，我们可以通过TLS机制，
    为每一个使用该全局变量的线程都提供一个变量值的副本，
    每一个线程均可以独立地改变自己的副本，而不会和其它线程的副本冲突。
    从线程的角度看，就好像每一个线程都完全拥有该变量。
    而从全局变量的角度上来看，就好像一个全局变量被克隆成了多份副本，
    而每一份副本都可以被一个线程独立地改变。
动态TLS和静态TLS
    动态TLS
        Windows中每创建一个线程，系统会为该线程分配一个64*sizeof(DWORD)长度的数组
        这块区域是线程相关联的，可以认为是线程专有空间，可以最多存64个32位值，
        而进程中也有一组标志位，4个字节（64位），反映当前正在执行线程的TSL数组使用情况。
        例如：如果线程中的TSL的第n个元素被使用，则进程中，第n个标志位为1。
        一般通过调用一组4个API函数来使用动态TLS：
            TlsAlloc
                DWORD WINAPI TlsAlloc(void);
                通过检索进程中的标志位，确定线程TLS数组中哪个元素是空的（可以使用），并返回其索引
                如果TlsAlloc无法在列表中找到一个FREE标志，那么它会返回TLS_OUT_OF_INDEXES
                
            TlsSetValue
                BOOL WINAPI TlsSetValue(
                    __in      DWORD dwTlsIndex, //索引值，表示在数组中的具体位置
                    __in_opt  LPVOID lpTlsValue //要设置的值
                    );
                当一个线程调用TlsSetValue函数成功时，它会修改自己的PVOID数组，
                但它无法修改另一个线程的TLS值。
                在调用TlsSetValue时，我们应该总是传入前面在调用TlsAlloc时返回的索引。
                因为Windows为了效率牺牲了对输入值的错误检测。
            TlsGetValue
                LPVOID WINAPI TlsGetValue(
                    __in  DWORD dwTlsIndex //索引值
                    );
                这个函数会返回在索引为dwTlsIndex的TLS元素中保存的值。
                TlsGetValue只会查看属于调用线程的数组。
            TlsFree
                BOOL WINAPI TlsFree(
                    __in  DWORD dwTlsIndex //索引值
                    );
                这个函数告诉系统已经预定的这个TLS元素现在不需要了，
                函数会将进程内的位标志数组中对应的INUSE标志重新设回FREE。
                此外，函数还会将所有线程中该元素的内容设为0.
        通常，如果DLL要使用TLS，那它会在DllMain函数处理DLL_PROCESS_ATTACH的时候调用TlsAlloc，
        在DllMain处理DLL_PROCESS_DETACH的时候调用TlsFree。
        而TlsSetValue和TlsGetValue的调用则最有可能发生在DLL所提供的其他函数中。
        而向应用程序中添加TLS的一种方法是直到需要时才添加。
        
小结：
    用TlsAlloc()得到的索引值，一般用全局变量存储，
    不管是不是在同一个线程中，每次调用该函数，返回的索引值都是不一样的，
    一般在主线程中调用该函数获取索引值，
    这个索引值，所有的线程都可使用，
    Windows中每创建一个线程，系统会为该线程分配一个TLS_MINIMUM_AVAILABLE*sizeof(DWORD)长度的数组，
    TLS_MINIMUM_AVAILABLE的最小值为64（vs2008中实测该值为1088），
    所以不同的线程，虽然使用同一个索引值，但实际是把数据(一般是地址)存在各自的数组中
    