@echo off&setlocal Enabledelayedexpansion
if exist "ok.txt" ren "ok.txt" "%random%ok.txt"
set /p file=���Ҫ������ı��ļ��ϵ�������:&set "file=!file:"=!"
for /f "delims=" %%a in ('more /s "%file%"') do echo %%a>>"ok.txt"
start ok.txt&exit