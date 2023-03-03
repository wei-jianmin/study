@echo off
:circle
set /p str="请输入要赋值的文件的路径"

if not exist %str% (
	msg * "指定的文件不存在%
	exit
)
for /f "tokens=*" %%i in ('dir/b "%str%"') do set str2=%%i
copy %str% %str2%
goto circle
