rem @echo off
echo ver=1.5
set /p s=��ָ���ļ���
set /p i=��ָ��Ҫ���ҵ��ַ�����
echo " ">new.txt
for /f "delims=" %%a in ('type %s%') do call :func %i% "%%a"
new.txt

:func
set s=%1
set l=%~2
::set flag=false
::echo %l%|find "%1%" &set flag=true
::if  %flag%==true (
echo "%l%"|find "%s%"
if %ERRORLEVEL% EQU 0 (
echo %l%>>new.txt
::set flag=false
pause
)
goto :eof
