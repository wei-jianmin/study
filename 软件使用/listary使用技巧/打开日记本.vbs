set fso = createobject("scripting.filesystemobject")  
Set objShell = CreateObject("Wscript.Shell")
base_name = "F:\工作日志"

folder_name = base_name & "\" & year(date) & "年" & month(date) & "月"

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