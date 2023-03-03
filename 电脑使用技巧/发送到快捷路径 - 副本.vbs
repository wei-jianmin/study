Set unNamedArguments = WScript.Arguments.UnNamed
set WshShell = WScript.CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
strFolder = "E:/Desktop/常用快捷路径/" '后面要有符号"/"
for count = 0 to wscript.arguments.count-1 Step 1
  filename = unNamedArguments.Item(count)
  objFSO.GetFile(filename)
  Set objFile = objFSO.GetFile(filename)
  st=inputbox("请输入要快捷方式的名字","发送到常用快捷方式",objFSO.GetBaseName(filename))
  if st="" then
    WScript.Quit
  end if
  set oShellLink = WshShell.CreateShortcut(strFolder & st & ".lnk")
  oShellLink.TargetPath = filename
  oShellLink.WindowStyle = 1
  oShellLink.WorkingDirectory = objFSO.GetParentFolderName(filename)
  oShellLink.Save
NEXT




