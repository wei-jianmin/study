@echo off
set /a i=63910631
echo ��С %i%
set /a b=%i%/4096*4096+4096
echo ռ�ÿռ� %b%

set /a k=%b%/1000
	echo k=%k%
set /a b=%b%-%k%*1000
	echo b=%b%
set /a m=%k%/1000
	echo m=%m%
set /a k=%k%-%m%*1000
	echo k=%k%
set /a g=%m%/1000
	echo g=%g%
set /a m=%m%-%g%*1000
	echo m=%m%
if %g% gtr 0 (
	echo ռ�ÿռ� %g%,%m%,%k%,%b%
) else (
	if %m% gtr 0 (
		echo ռ�ÿռ� %m%,%k%,%b%
	) else (
		if %k% gtr 0 (
			echo ռ�ÿռ� %k%,%b%
		) else (
			echo ռ�ÿռ� %b%
		)
	)
)
pause



set tab=	
echo 1%tab%---
echo 12%tab%---
echo 123%tab%---		
echo 1234%tab%---
echo 12345%tab%---
echo 123456%tab%---
echo 1234567%tab%---
echo 12345678%tab%---
echo 123456789%tab%---
