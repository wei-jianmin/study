@echo off
setlocal enabledelayedexpansion

set tab=
set /a sum1=0
set /a sum2=0
set /a filecount=0
set /a dircount=0
set /a filecount2=0
set hasfolder="n"

echo.	
echo �޸�ʱ��          �ļ�����        �ļ���С(K)       ռ�ÿռ�(K)  �ļ�����
echo --------------------------------------------------------------------------

::��ʾ�ļ�

for /f "delims=" %%i in ('dir /a-d /b') do call :show_file "%%i"

for /f "delims=" %%k in ('dir /ad /b') do set hasfolder="y"
if %hasfolder% == "y" echo.

::��ʾ�ļ���
for /f "delims=" %%j in ('dir /ad /b') do (
 set /a total=0
 set /a size=0
 for /f "delims=" %%i in ('dir /a-d /b /s "%%j"') do (
   set /a filecount2=!filecount2!+1
   set /a total=!total!+%%~zi
   set /a sz=%%~zi/4096*4096+4096
   set /a size=!size!+!sz!
 )
 call :show_dir "%%j" !total! !size!
)

echo.
call _split_num %sum1%
echo ��ǰĿ¼�ļ����� : %filecount%
echo ��ǰĿ¼�ļ����� : %dircount%
echo �ļ��ܸ���       : %filecount2%
echo �ļ��ܴ�С(KB)   : %res: =%
call _split_num %sum2%
echo ռ�ÿռ��С(KB) : %res: =%
goto :eof

:show_file
 set /a filecount=%filecount%+1
 set /a filecount2=%filecount2%+1
 call _split_num %~z1
 set str1=%res%
 set /a size=%~z1/4096*4096+4096
 set /a sum1=%sum1%+%~z1
 set /a sum2=%sum2%+%size%
 call _split_num %size%
 set str2=%res%
 echo %~t1  %~a1  %str1%  %str2%  %~1
 goto :eof


:show_dir
  set /a dircount=%dircount%+1
  set /a sum1=%sum1%+%2
  set /a sum2=%sum2%+%3
  call _split_num %2
  set str1=%res%
  call _split_num %3
  set str2=%res%
  echo %~t1  %~a1  %str1%  %str2%  %~1
  goto :eof