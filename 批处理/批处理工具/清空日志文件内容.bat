@echo off
for /f "delims=" %%i in ('dir /s /b *.log') do echo.>%%i
for /f "delims=" %%j in ('dir /s /b *.txt') do echo.>%%j
