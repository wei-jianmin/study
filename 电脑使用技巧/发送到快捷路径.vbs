Set unNamedArguments = WScript.Arguments.UnNamed
set WshShell = WScript.CreateObject("WScript.Shell")
Set fso = CreateObject("scripting.filesystemobject")
strFolder = "E:/����/"       '����Ҫ�з���"/"
for count = 0 to wscript.arguments.count-1 Step 1
  filename = unNamedArguments.Item(count)
  pos = InStrRev(filename,"\")
  if(pos=0) then
	msgbox "·������ȷ"
    WScript.Quit
  end if
  strl = left(filename,pos-1)
  strr = right(filename,len(filename)-pos)
  st=inputbox("������Ҫ��ݷ�ʽ������","���͵����ÿ�ݷ�ʽ",strr)
  if st="" then
	msgbox "ȡ���������·��"
    WScript.Quit
  end if

  lnkPath = strFolder & st & ".lnk"
  lnkPath = fso.GetParentFolderName(lnkPath)
  If Not fso.FolderExists(lnkPath) Then
	if 1=msgbox("Ŀ¼�����ڣ��Ƿ񴴽���", vbokcancel, "��ʾ") then
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




