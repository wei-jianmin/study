:::���߼����� 
::���������ڵ�һ�У���:::��ͷ����βҪ���һ�������ַ�����ո�
::û�а������������������ʾ�������б���

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

