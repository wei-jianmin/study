:::�ļ����ļ���ɾ������ 
@echo off
if "%1"=="" (
	echo.
	echo rm * ɾ����ǰĿ¼�������ļ�
	echo rm ** ɾ����ǰĿ¼�������ļ����ļ���
	echo.
	echo -------------------------------------
	echo.
	del /?
) else (
	if "%1"=="**" (
		del /q * > NUL
		del /s /q * > NUL 

		for /f "delims=" %%d in ('dir /ad/b') do (
			rd /s /q %%d > NUL
		)
	) else (
		if "%1"=="*" (
			del *
		) else (
			del %*
		)
	)
)