#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>

int main()
{
    for(int i=0;i<5;i++)
    {
        printf("in loop %d\n",i);
        puts("do fork");
        pid_t pid = fork();  //fork后，之后的代码在主进程和子进程中都会执行，子进程使用exit(0)及时结束自己
        if(pid!=0)    //在主进程中，fork返回的pid，是子进程的id（只能通过这种方法获得紫禁城的id），不为0
        {
            printf("i am parrent, my child pid is %d,my pid is %d\n",pid,getpid());
            puts("main wait");
            waitpid(pid,NULL,0);  //等待子进程的id
            puts("main wait ok");
        }
        else    //在子进程中，fork返回的pid为0，要想获得自己的或父进程的id，用getpid()、getppid()
        {
            printf("i am child, my pid is %d, ppid is %d\n",getpid(),getppid());
            exit(0);    //子进程使用exit(0)及时结束自己
        }
        puts("-----------------------------");  //子进程主动结束了(exit(0))，所以这一句只会在父进程中执行
    }
    puts("wait key");
    getchar();
    return 0;
}
