#include <stdio.h>
#include <dlfcn.h>

extern "C" void oes()
{
    puts("func in oes");
    puts("call qt func");
    void * h = dlopen("./qt.so.1",RTLD_NOW);
    if(h)
    {
        puts("load qt ok");
        typedef void (*pfunc)(void);
        pfunc f = (pfunc)dlsym(h,"func");
        if(f)
            f();
        else
            puts("get func error");
        dlclose(h);
    }
    else
    {
        puts("load qt.so error");
    }
    return;
}

