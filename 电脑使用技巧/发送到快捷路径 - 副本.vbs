Set unNamedArguments = WScript.Arguments.UnNamed
set WshShell = WScript.CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
strFolder = "E:/Desktop/���ÿ��·��/" '����Ҫ�з���"/"
for count = 0 to wscript.arguments.count-1 Step 1
  filename = unNamedArguments.Item(count)
  objFSO.GetFile(filename)
  Set objFile = objFSO.GetFile(filename)
  st=inputbox("������Ҫ��ݷ�ʽ������","���͵����ÿ�ݷ�ʽ",objFSO.GetBaseName(filename))
  if st="" then
    WScript.Quit
  end if
  set oShellLink = WshShell.CreateShortcut(strFolder & st & ".lnk")
  oShellLink.TargetPath = filename
  oShellLink.WindowStyle = 1
  oShellLink.WorkingDirectory = objFSO.GetParentFolderName(filename)
  oShellLink.Save
NEXT




