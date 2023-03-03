:::切换目录 
@echo off

set disk0=%cd%
set disk1=%~f1
set d0=%disk0:~0,2%
set d1=%disk1:~0,2%

::小写转大写
if "%d1%" == "a:" set d1=A: && goto :ok
if "%d1%" == "b:" set d1=B: && goto :ok
if "%d1%" == "c:" set d1=C: && goto :ok
if "%d1%" == "d:" set d1=D: && goto :ok
if "%d1%" == "e:" set d1=E: && goto :ok
if "%d1%" == "f:" set d1=F: && goto :ok
if "%d1%" == "g:" set d1=G: && goto :ok
if "%d1%" == "h:" set d1=H: && goto :ok
if "%d1%" == "i:" set d1=I: && goto :ok
if "%d1%" == "j:" set d1=J: && goto :ok
if "%d1%" == "k:" set d1=K: && goto :ok
if "%d1%" == "l:" set d1=L: && goto :ok
if "%d1%" == "m:" set d1=M: && goto :ok
if "%d1%" == "n:" set d1=N: && goto :ok
if "%d1%" == "o:" set d1=O: && goto :ok
if "%d1%" == "p:" set d1=P: && goto :ok
if "%d1%" == "q:" set d1=Q: && goto :ok
if "%d1%" == "r:" set d1=R: && goto :ok
if "%d1%" == "s:" set d1=S: && goto :ok
if "%d1%" == "t:" set d1=T: && goto :ok
if "%d1%" == "u:" set d1=U: && goto :ok
if "%d1%" == "v:" set d1=V: && goto :ok
if "%d1%" == "w:" set d1=W: && goto :ok
if "%d1%" == "x:" set d1=X: && goto :ok
if "%d1%" == "y:" set d1=Y: && goto :ok
if "%d1%" == "z:" set d1=Z: && goto :ok

:ok

if %d0% == %d1% (
	cd %1
) else (
	%d1%
	cd %1
)
l