:::工具集帮助 
::帮助描述在第一行，以:::开头，结尾要多加一个无用字符，如空格
::没有帮助描述的命令，不会显示在命令列表中

@echo off
set tab=	
for /f "delims=" %%i in ('dir /b %~dp0*.bat') do call :func %%i

:func
if "%1"=="" goto :eof
set /p l1=<"%~dp0%1"
if "%l1:~0,3%"==":::" (
echo %~n1%tab%%tab%%l1:~3,-1%
)
goto :eof

