@echo off
for /f "delims=" %%i in ('dir /b *.*') do if not %%i==%~nx0 echo.>%%i
