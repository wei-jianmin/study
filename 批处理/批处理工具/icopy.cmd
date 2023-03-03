@echo off
echo usage:copy files from tmp dir to system32 dir
pause
for /F %%i in ('dir /B') do call:dosth %%i
pause
:dosth
if not "%1"=="icopy.cmd"  copy * %windir%\system32
goto :eof