@echo off
set /p k=请指定文件：
setlocal enabledelayedexpansion
set "PriLine="
set "DupNum=1"
(for /f "delims=" %%i in ('sort %k%') do (
  if "!PriLine!" equ "%%i" (
    set /a DupNum+=1
  ) else (
    if !DupNum! gtr 1 (
      echo,!PriLine!
    )
    set DupNum=1
  )
  set "PriLine=%%i"
))>new4.txt
if !DupNum! gtr 1 (
  >>new4.txt echo,!PriLine!
)