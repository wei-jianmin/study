:::�༭����Դ�ļ� 
@echo off
if not "%1"=="" (
	if exist %~dp0%1.bat (
		start notepad %~dp0%1.bat
	) else (
		if exist %cd%\%1 (
			start explorer %cd%\%1
		) else (
			echo �ļ�������
		)
	)
)