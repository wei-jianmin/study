@echo off
set /p pa=请输入要转化为短路径的名字：
for /f  "delims=?" %%i in ("%pa%") do (echo "%%i"
echo 转换后：
echo "%%~si")|msg %username%
::msg %username% /time:5
