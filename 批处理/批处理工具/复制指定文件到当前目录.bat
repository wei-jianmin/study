@echo off
:circle
set /p str="������Ҫ��ֵ���ļ���·��"

if not exist %str% (
	msg * "ָ�����ļ�������%
	exit
)
for /f "tokens=*" %%i in ('dir/b "%str%"') do set str2=%%i
copy %str% %str2%
goto circle
