@echo off
set /p pa=������Ҫת��Ϊ��·�������֣�
for /f  "delims=?" %%i in ("%pa%") do (echo "%%i"
echo ת����
echo "%%~si")|msg %username%
::msg %username% /time:5
