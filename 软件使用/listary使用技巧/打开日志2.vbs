set fso = createobject("scripting.filesystemobject")  
Set objShell = CreateObject("Wscript.Shell")
base_name = "E:/工作日志"

nowday=formatdatetime(now,2)
folder_name = base_name & "/" & year(nowday) & "年" & month(nowday) & "月"
file_name = folder_name & "/" & day(nowday) & ".txt"

'msgbox folder_name
'msgbox file_name

prepare_folder
prepare_file
objShell.Run "notepad2 " & file_name

sub prepare_file()
	if fso.fileExists(file_name) = false then
		fso.createtextfile(file_name) 
	end if
end sub

sub prepare_folder()
	if fso.folderExists(base_name) = false then
		msgbox "没有基本文件夹： " & base_name
		return
	end if

	
	if fso.folderExists(folder_name) = false then
		fso.createfolder(folder_name)
	end if
end sub