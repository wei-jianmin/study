@echo off&setlocal Enabledelayedexpansion
if exist "ok.txt" ren "ok.txt" "%random%ok.txt"
set /p file=请把要处理的文本文件拖到本窗口:&set "file=!file:"=!"
for /f "delims=" %%a in ('more /s "%file%"') do echo %%a>>"ok.txt"
start ok.txt&exit