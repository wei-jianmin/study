@echo off
::功能：把文件中含有===和repeat字样的行取出来写到一个新文件中
echo " ">D:\6.txt
for /f "delims=" %%a in ('type "D:\0.txt"') do call :func "%%a"
D:\6.txt

:func
set l=%1
set flag=false
echo %l%|find "==="&&set flag=true
if  %flag%==true (
echo %l%>>D:\6.txt
set flag=false
)
echo %l%|find "repeat"&&set flag=true
if  %flag%==true (
echo %l%>>D:\6.txt
set flag=false
)
goto :eof
