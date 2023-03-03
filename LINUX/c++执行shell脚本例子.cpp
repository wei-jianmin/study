#include <iostream>
#include <cstring>
#include <cstdio>
#include<unistd.h>
#include<stdlib.h>
using namespace std;

int shell_call(std::string &cmdstr);

int main(int argc, char **argv)
{

    string shell_command = "./ntp_server.sh";
    shell_call(shell_command);

    return 0;
}

int shell_call(std::string &cmdstr) {
    int maxline = 1024;             //读取的shell命令最大长度
    char line[maxline];             //存储读取到的shell命令
    FILE *fpin;  
	int ret;        
    
    //popen()会调用fork()产生子进程，然后从子进程中调用/bin/sh -c 来执行参数command 的指令
    if((fpin = popen(cmdstr.c_str(), "r")) == NULL) 
    {
        printf("popen error\n");
        exit(-1);
    }

    while(true) 
    {
        //从文件流中读取信息到line中
        if(fgets(line, sizeof(line), fpin) == NULL)
            break;
		
		//将line中信息送入输出缓冲区显示
        if(fputs(line, stdout) == EOF) 
        {
            printf("fputs error\n");
            exit(-1);
        }
    }
	
    if((ret = pclose(fpin)) == -1) {
        printf("pclose error\n");
        exit(-1);
    }
    return ret;
}
