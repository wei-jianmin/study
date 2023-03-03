:::创建文件命令 
@echo off
for %%s in (%*) do (
	copy /y NUL %%s >NUL
)