set fso = createobject("scripting.filesystemobject")  
Set objShell = CreateObject("Wscript.Shell")
base_name = "F:\������־"

folder_name = base_name & "\" & year(date) & "��" & month(date) & "��"

prepare_folder
objShell.Run "explorer " & folder_name



sub prepare_folder()
	if fso.folderExists(base_name) = false then
		msgbox "û�л����ļ��У� " & base_name
		return
	end if

	
	if fso.folderExists(folder_name) = false then
		fso.createfolder(folder_name)
	end if
end sub