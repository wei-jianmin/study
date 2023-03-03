:::编译并运行一个java文件 
@echo off
if "%2"=="" (
javac -Xdiags:verbose %1
if not ERRORLEVEL 1 (
	java %~n1
)
) else (
echo 只接受一个参数
)