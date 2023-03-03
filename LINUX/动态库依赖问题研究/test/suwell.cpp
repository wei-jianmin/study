#include <stdio.h>
#include <dlfcn.h>
#include <string.h>

int main(int argc,char* argv[])
{
    puts("func in suwell main");
    puts("call qt func");
    void * h = NULL;
    if(argc>1 && strstr(argv[1],"qt"))
    {
        h = dlopen("./qt.so",RTLD_NOW);
        puts("try load qt");
    }
    else
    {
        puts("not need load qt");
    }
    if(h)
    {
        puts("load qt ok");
        typedef void (*pfunc)(void);
        pfunc f = (pfunc)dlsym(h,"func");
        if(f)
            f();
        else
            puts("get func error");
    }
    else
    {
        puts("load qt.so error");
    }
    void* h2 = NULL;
    if(argc>1 && strstr(argv[1],"oes"))
    {
        h2 = dlopen("./oes.so",RTLD_NOW);
        puts("try load oes");
    }
    else
        puts("not need load oes");
    if(h2)
    {
        puts("load oes ok");
        typedef void (*pfunc)(void);
        pfunc f = (pfunc)dlsym(h2,"oes");
        if(f)
            f();
        else
            puts("get oes error");
    }
    else
    {
        puts("load oes.so error");
    }
    if(h)
        dlclose(h);
    if(h2)
        dlclose(h2);
    return 0;
}

