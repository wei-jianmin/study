set fso = createobject("scripting.filesystemobject")  
Set objShell = CreateObject("Wscript.Shell")

base_name = "F:\������־"

nowday=formatdatetime(now,2)
folder_name = base_name & "\" & year(nowday) & "��" & month(nowday) & "��"
file_name = folder_name & "\" & day(nowday) & ".txt"
index_naMe = base_name & "\filepath.txt"

'msgbox folder_name
'msgbox file_name

prepare_folder
prepare_file

'�����δ�������־�ļ���·����¼����
cmd_str = "cmd.exe /c echo " & file_name & ">" & index_name
objShell.run cmd_str,0,true

'if fso.fileExists("notepad2") then
objShell.Run "notepad2 /g -1 " & file_name

sub prepare_file()
	if fso.fileExists(file_name) = false then
		if fso.fileExists(index_name) then
			set f = fso.opentextfile(index_name,1,false)
			last_filepath = f.readline()
			f.close()
			cmd_str = "cmd.exe /c copy " & last_filepath & " " & file_name
			objShell.run cmd_str,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			cmd_str = "cmd.exe /c echo ��-----��-----��---��������---��-----��-----�� >>" & file_name
			'msgbox cmd_str
			objShell.run cmd_str,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
		else	
			fso.createtextfile(file_name) 
		end if
	end if

end sub

sub prepare_folder()
	if fso.folderExists(base_name) = false then
		msgbox "û�л����ļ��У� " & base_name
		return
	end if

	
	if fso.folderExists(folder_name) = false then
		fso.createfolder(folder_name)
	end if
end sub