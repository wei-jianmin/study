::将一个数值，从低位起，每3位之间加一个,分隔符，最终结果放在res变量中
@echo off

if "%1"=="" goto :eof

set _tab=	
set /a _b=%1

set /a _k=%_b%/1000
set /a _b=%_b%-%_k%*1000

if %_b% gtr 99 (
	set _strb=%_b%
) else (
	if %_b% gtr 9 (
		set _strb=0%_b%
	) else (
		set _strb=00%_b%
	)
)

set /a _m=%_k%/1000
set /a _k=%_k%-%_m%*1000
if %_k% gtr 99 (
	set _strk=%_k%
) else (
	if %_k% gtr 9 (
		set _strk=0%_k%
	) else (
		set _strk=00%_k%
	)
)

set /a _g=%_m%/1000
set /a _m=%_m%-%_g%*1000
if %_m% gtr 99 (
	set _strm=%b%
) else (
	if %_m% gtr 9 (
		set _strm=0%_m%
	) else (
		set _strm=00%_m%
	)
)

if %_g% gtr 0 (
	if %_g% gtr 99 (
		set res=%_g%,%_strm%,%_strk%.%_strb%
	) else (
		set res=%_g%,%_strm%,%_strk%.%_strb%
	)
) else (
	if %_m% gtr 0 (
		set res=%_m%,%_strk%.%_strb%%_tab%
	) else (
		if %_k% gtr 0 (
			if %_k% == %_strk% (
				set res=%_k%.%_strb%%_tab%%_tab%
			) else (
				set res=%_k%.%_strb%%_tab%%_tab%
			)
		) else (
			if %_b% == %_strb% (
				set res=0.%_b%%_tab%%_tab%
			) else (
				set res=0.%_b%%_tab%%_tab%
			)
		)
	)
)