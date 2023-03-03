Set unNamedArguments = WScript.Arguments.UnNamed
set WshShell = WScript.CreateObject("WScript.Shell")
Set fso = CreateObject("scripting.filesystemobject")
strFolder = "E:/链接/"       '后面要有符号"/"
for count = 0 to wscript.arguments.count-1 Step 1
  filename = unNamedArguments.Item(count)
  pos = InStrRev(filename,"\")
  if(pos=0) then
	msgbox "路径不正确"
    WScript.Quit
  end if
  strl = left(filename,pos-1)
  strr = right(filename,len(filename)-pos)
  st=inputbox("请输入要快捷方式的名字","发送到常用快捷方式",strr)
  if st="" then
	msgbox "取消创建快捷路径"
    WScript.Quit
  end if

  lnkPath = strFolder & st & ".lnk"
  lnkPath = fso.GetParentFolderName(lnkPath)
  If Not fso.FolderExists(lnkPath) Then
	if 1=msgbox("目录不存在，是否创建？", vbokcancel, "提示") then
  		CreateFolderEx(lnkPath)
	else
		WScript.Quit
	end if
  end if

  set oShellLink = WshShell.CreateShortcut(strFolder & st & ".lnk")
  oShellLink.TargetPath = filename
  oShellLink.WindowStyle = 1
  oShellLink.WorkingDirectory = strl
  oShellLink.Save
next
 
Function CreateFolderEx(path)
    If fso.FolderExists(path) Then
        Exit Function
    End If
    If Not fso.FolderExists(fso.GetParentFolderName(path)) Then
        CreateFolderEx fso.GetParentFolderName(path)
    End If
    fso.CreateFolder(path)
End Function




