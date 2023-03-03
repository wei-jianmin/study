::将一个数值，从低位起，每3位之间加一个,分隔符，最终结果放在res变量中
@echo off
set res=

::setlocal enabledelayedexpansion

if "%1"=="" goto :eof

set res=
set _p=%1
set _jmp=0

for /L %%j in (1,1,16) do (
	if !_jmp! gtr 0 (
		set /a _jmp=!_jmp!-1
	) else (
		set /a _i=!_p!/10*10
		set /a _j=!_p!-!_i!
		if !_p! equ 0 (
			if %%j equ 4 (
				set res=.!res!
				set _jmp=1
			)
			if %%j leq 5 (
				set res=0!res!
			) else (
				set res= !res!
			)
		) else (
			if %%j equ 4 (
				set res=.!res!
				set _jmp=1
			)
			if %%j equ 8 (
				set res=,!res!
				set _jmp=1
			)
			if %%j equ 12 (
				set res=,!res!
				set _jmp=1
			)
			set res=!_j!!res!
		)
		set /a _p=!_p!/10
	)
)

if "-%res%-"=="-                -" (
 set res=               0
)
if "-%res%-"=="-           0.000-" (
 set res=               0
)