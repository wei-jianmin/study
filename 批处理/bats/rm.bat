:::文件及文件夹删除命令 
@echo off
if "%1"=="" (
	echo.
	echo rm * 删除当前目录下所有文件
	echo rm ** 删除当前目录下所有文件及文件夹
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