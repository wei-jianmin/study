:::�����ļ����� 
@echo off
for %%s in (%*) do (
	copy /y NUL %%s >NUL
)