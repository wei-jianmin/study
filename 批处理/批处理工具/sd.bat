@echo offsetlocal enabledelayedexpansion
cd.>b.txt
for /f "delims=" %%i in  ('more a.txt^|findstr /i /c:"aaa"'