set fso = createobject("scripting.filesystemobject")  
Set objShell = CreateObject("Wscript.Shell")

'׼����־·������
nowday=date
base_name = "F:\������־"
folder_name = base_name & "\" & year(nowday) & "��" & month(nowday) & "��"
file_name = folder_name & "\" & day(nowday) & ".txt"
index_name = base_name & "\filepath.txt"

'msgbox folder_name
'msgbox file_name

'׼����־�ļ��У����ڴ����ļ���ʱ��������־�ļ�
prepare_folder

'׼����־�ļ�
prepare_file2

'�����δ�������־�ļ���·����¼/���µ� index_name
cmd_str = "cmd.exe /c echo " & file_name & ">" & index_name
objShell.run cmd_str,0,true

'���ռ��ļ�
'if fso.fileExists("notepad2") then
objShell.Run "notepad2 /ns /g 2 " & file_name

'��������� file_name���򴴽�
'������� file_name ʱ�������� index_name��
'�����м�¼���ļ�������,��¼�ڴ����� file_name ��
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
			cmd_str = "cmd.exe /c echo ��-----��-----��-----��-----��-----��-----��-----��----��������----��-----��-----��-----��-----��-----��-----��-----��  >>" & file_name
			'msgbox cmd_str
			objShell.run cmd_str,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
		else	
			fso.createtextfile(file_name) 
		end if
	end if
end sub

'��������� file_name���򴴽�
'������� file_name ʱ�������� index_name��
'�����м�¼���ļ�������,��¼�ڴ����� file_name ��
'�� prepare_file �������ǣ�ǰ�߽���ʷ��־��¼�ڵ�ǰ���֮ǰ��
'����������ʷ�ռǼ�¼�ڵ�ǰ���֮��
sub prepare_file2()
	if fso.fileExists(file_name) = false then
		if fso.fileExists(index_name) then
			set f = fso.opentextfile(index_name,1,false)
			last_filepath = f.readline()
			f.close()
			objShell.run "cmd.exe /c date /t >>" & file_name,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			cmd_str = "cmd.exe /c echo ��-----��-----��----��ʷ��־----��-----��-----��  >>" & file_name
			objShell.run cmd_str,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			cmd_str = "cmd.exe /c type " & last_filepath & " >>" & file_name
			objShell.run cmd_str,0,true
			'msgbox cmd_str
		else	
			fso.createtextfile(file_name) 
		end if
	end if
end sub

'������ͬ�� prepare_file2���������ڣ�
'ÿ��1�ţ�������֮ǰ����ʷ��־��ֻ��¼��ʷ��־�ļ���
'�ú����и�ȱ�ݣ������ÿ�µ�1�Ų�ִ�б��ű����� ...
sub prepare_file3()
	if fso.fileExists(file_name) = false then
		if fso.fileExists(index_name) then
			set f = fso.opentextfile(index_name,1,false)
			last_filepath = f.readline()
			f.close()
			objShell.run "cmd.exe /c date /t >>" & file_name,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			cmd_str = "cmd.exe /c echo ��-----��-----��----��ʷ��־----��-----��-----��  >>" & file_name
			objShell.run cmd_str,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
            if day(nowday) = 1 then
                cmd_str = "cmd.exe /c echo " & last_filepath & " >>" & file_name
            else
                cmd_str = "cmd.exe /c type " & last_filepath & " >>" & file_name
            end if
			objShell.run cmd_str,0,true
			'msgbox cmd_str
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
        '�����ļ���ʱ����������־����¼�������һ����־��·��
        if fso.fileExists(index_name) then
			set f = fso.opentextfile(index_name,1,false)
			last_filepath = f.readline()
			f.close()
			objShell.run "cmd.exe /c date /t >>" & file_name,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			cmd_str = "cmd.exe /c echo ��-----��-----��----��ʷ��־----��-----��-----��  >>" & file_name
			objShell.run cmd_str,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
            cmd_str = "cmd.exe /c echo " & last_filepath & " >>" & file_name
			objShell.run cmd_str,0,true
			'msgbox cmd_str
		else	
			fso.createtextfile(file_name) 
		end if
	end if
end sub