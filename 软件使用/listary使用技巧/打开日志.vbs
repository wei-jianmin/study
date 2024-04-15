set fso = createobject("scripting.filesystemobject")  
Set objShell = CreateObject("Wscript.Shell")

'准备日志路径变量
nowday=date
base_name = "F:\工作日志"
folder_name = base_name & "\" & year(nowday) & "年" & month(nowday) & "月"
file_name = folder_name & "\" & day(nowday) & ".txt"
index_name = base_name & "\filepath.txt"

'msgbox folder_name
'msgbox file_name

'准备日志文件夹，并在创建文件夹时，创建日志文件
prepare_folder

'准备日志文件
prepare_file2

'将本次创建的日志文件的路径记录/更新到 index_name
cmd_str = "cmd.exe /c echo " & file_name & ">" & index_name
objShell.run cmd_str,0,true

'打开日记文件
'if fso.fileExists("notepad2") then
objShell.Run "notepad2 /ns /g 2 " & file_name

'如果不存在 file_name，则创建
'如果创建 file_name 时，还存在 index_name，
'则将其中记录的文件的内容,记录在创建的 file_name 中
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
			cmd_str = "cmd.exe /c echo ↑-----↑-----↑-----↑-----↑-----↑-----↑-----↑----遗留问题----↑-----↑-----↑-----↑-----↑-----↑-----↑-----↑  >>" & file_name
			'msgbox cmd_str
			objShell.run cmd_str,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
		else	
			fso.createtextfile(file_name) 
		end if
	end if
end sub

'如果不存在 file_name，则创建
'如果创建 file_name 时，还存在 index_name，
'则将其中记录的文件的内容,记录在创建的 file_name 中
'与 prepare_file 的区别是，前者将历史日志记录在当前光标之前，
'本函数将历史日记记录在当前光标之后
sub prepare_file2()
	if fso.fileExists(file_name) = false then
		if fso.fileExists(index_name) then
			set f = fso.opentextfile(index_name,1,false)
			last_filepath = f.readline()
			f.close()
			objShell.run "cmd.exe /c date /t >>" & file_name,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			cmd_str = "cmd.exe /c echo ↓-----↓-----↓----历史日志----↓-----↓-----↓  >>" & file_name
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

'基本等同于 prepare_file2，区别在于：
'每月1号，不导入之前的历史日志，只记录历史日志文件名
'该函数有个缺陷，即如果每月的1号不执行本脚本，则 ...
sub prepare_file3()
	if fso.fileExists(file_name) = false then
		if fso.fileExists(index_name) then
			set f = fso.opentextfile(index_name,1,false)
			last_filepath = f.readline()
			f.close()
			objShell.run "cmd.exe /c date /t >>" & file_name,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			cmd_str = "cmd.exe /c echo ↓-----↓-----↓----历史日志----↓-----↓-----↓  >>" & file_name
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
		msgbox "没有基本文件夹： " & base_name
		return
	end if

	
	if fso.folderExists(folder_name) = false then
		fso.createfolder(folder_name)
        '创建文件夹时，将创建日志，记录上月最后一次日志的路径
        if fso.fileExists(index_name) then
			set f = fso.opentextfile(index_name,1,false)
			last_filepath = f.readline()
			f.close()
			objShell.run "cmd.exe /c date /t >>" & file_name,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			objShell.run "cmd.exe /c echo. >>" & file_name,0,true
			cmd_str = "cmd.exe /c echo ↓-----↓-----↓----历史日志----↓-----↓-----↓  >>" & file_name
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