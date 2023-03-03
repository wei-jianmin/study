//检测输出是否被重定向
	HANDLE hStdin = GetStdHandle(STD_OUTPUT_HANDLE);  
	bool flag = false;
	if(FILE_TYPE_CHAR != GetFileType(GetStdHandle(STD_OUTPUT_HANDLE)))
	{
		flag = true;
	}
