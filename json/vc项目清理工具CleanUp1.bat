echo Clear Temp Files ----------------------------------------

@echo on 

DEL *.pdb /f /q /s 

DEL *.obj /f /q /s 

DEL *.ilk /f /q /s 

DEL *.log /f /q /s 

DEL *.idb /f /q /s 

DEL *.pch /f /q /s 

DEL *.ncb /f /q /s 

DEL *.opt /f /q /s

DEL *.tmp /f /q /s 

DEL *.ldb /f /q /s 

DEL *.aps /f /q /s 

DEL *.bsc /f /q /s

DEL *.dep /f /q /s

DEL *.exp /f /q /s

del /s /q /f *.tlb

del /s /q /f *.tlh

del /s /q /f *.tli

DEL *.intermediate.manifest /f /q /s

DEL *.ipch /f /q /s

DEL *.lastbuildstate /f /q /s

DEL *.lock /f /q /s

DEL *.manifest /f /q /s

DEL *.map /f /q /s

DEL *.meta /f /q /s

DEL BuildLog.htm /f /q /s

DEL *.sdf /f /q /s 

del *.tlog /f /q /s

del *.res /f /q /s

del *.opensdf /f /q /s

del *.suo /f /q /s

for /f "delims=" %%a in ('dir /s /b /ad') do (rd /q "%%a" 2>nul && echo 删除空文件夹 "%%a")

for /f "delims=" %%a in ('dir /s /b /ad "ipch"') do (rd /q /s "%%a" && echo 删除文件 "%%a")

echo Clear Temp Files ----------------------------------------

pause


