@echo off
set a=0
netsh interface show interface|findstr "��������"|findstr "����" && set a=1

if %a% == 1 (
netsh  interface set interface ��������  disable
netsh  interface set interface ������������ enable
echo "�л���������������"
) else (
netsh  interface set interface ��������  enable
netsh  interface set interface ������������ disable
echo "�л�����������"
)
pause
