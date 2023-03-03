@echo off
set a=0
netsh interface show interface|findstr "本地连接"|findstr "启用" && set a=1

if %a% == 1 (
netsh  interface set interface 本地连接  disable
netsh  interface set interface 无线网络连接 enable
echo "切换到无线网络连接"
) else (
netsh  interface set interface 本地连接  enable
netsh  interface set interface 无线网络连接 disable
echo "切换到本地连接"
)
pause
