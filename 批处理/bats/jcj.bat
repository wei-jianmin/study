:::���벢����һ��java�ļ� 
@echo off
if "%2"=="" (
javac -Xdiags:verbose %1
if not ERRORLEVEL 1 (
	java %~n1
)
) else (
echo ֻ����һ������
)