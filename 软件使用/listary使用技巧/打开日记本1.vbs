set fso = createobject("scripting.filesystemobject")  
Set objShell = CreateObject("Wscript.Shell")
base_name = "F:\工作日志"

nowday=formatdatetime(now,2)

folder_name = base_name & "\" & year(nowday) & "年" & month(nowday) & "月"

prepare_folder
objShell.Run "explorer " & folder_name



sub prepare_folder()
	if fso.folderExists(base_name) = false then
		msgbox "没有基本文件夹： " & base_name
		return
	end if

	
	if fso.folderExists(folder_name) = false then
		fso.createfolder(folder_name)
	end if
end sub