@echo off
cd %~dp0
set /p fn=����Ҫ���Ƶ��ļ� : 
for /l %%i in (1,1,100) do call :fcpy %fn% %%i
pause

:fcpy
copy /y "%~1" "%~d1%~p1%~n1%2%~x1"
goto :eof