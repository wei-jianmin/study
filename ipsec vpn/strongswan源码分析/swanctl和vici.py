swanctl 调用 command_dispatch（command.c）处理参数
command_dispatch（command处理完参数后，调用call_command    
call_command 调用 vici_connect(uri)  //uri是command的文件全局变得
vici_connect 调用 lib->streams->connect(uri 或 VICI_DEFAULT_URI)
lib->streams->connect 参 : file://stream机制.py