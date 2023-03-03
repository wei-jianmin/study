1. 从后往前找，定位到 PK\5\6（0x06054b50） 位置
2. 之后的数据符合结构体 （目录索引结构）
     {
	WORD	this_disk;
	WORD	start_disk;
	WORD	entries_in_this_disk;
	WORD	entries_in_central_directory_disk;
	DWORD	size_of_central_directory;
	DWORD	offset_to_central_directory;
      }
3.  如果 entries_in_central_directory_disk==0xFFFF 或 offset_to_central_directory==0xFFFFFFFF
     则为ZIP64格式（这里不介绍）
4.  将文件指针定位到 offset_to_central_directory 位置，然后读结构体 （文件索引结构）
      {
	DWORD	sig;    //固定值，ZIP_CENTRAL_DIRECTORY_SIG = 0x02014b50
	WORD	version_made_by;
	WORD	version_to_extract;
	WORD	general;
	WORD	method;
	WORD	last_mod_file_tile;
	WORD	last_mode_file_date;
	DWORD	crc-32;
	DWORD	csize;		//文件压缩后大小
	DWORD	usize;		//文件原始大小
	WORD	namesize;	//小于0说明有错
	WORD	metasize;		//小于0说明有错
	WORD	commentsize;	//小于0说明有错
	WORD	disk_number_start;
	WORD	int_file_atts;
	DWORD	ext_file_atts;
	DWORD	offset;		//文件在zip中的偏移
	BYTE[namesize]	name;	//zip中文件的名字
	BYTE[metasize]	meta;
	BYTE[commentsize]   comment;
      }
      meta的结构：
      {
	WORD type;	
	WORD size;
	BYTE[size]  data;
      }
      如果meta.type == ZIP64_EXTRA_FIELD_SIG == 0x0001
      则需要根据meta.data，重新得到前面结构的usize、csize、offset
      具体计算方法为：
	如果之前的usize == 0xFFFFFFFF 且 meta.data 剩余长度不小于8
		usize = 从 meta.data 取出8个字节
	如果之前的csize == 0xFFFFFFFF 且 meta.data 剩余长度不小于8
		csize = 从 meta.data 取出8个字节
	如果之前的offset == 0xFFFFFFFF 且 meta.data 剩余长度不小于8
		offset = 从 meta.data 取出8个字节
5.   ofd中的文件数据符合下面的结构 (文件结构)
      {
	DWORD	sig;	// 固定值 ZIP_LOCAL_FILE_SIG（0x04034b50）
	WORD	version;
	WORD	general;   // 如果最低位为1（与 ZIP_ENCRYPTED_FLAG 相与），说明文件是加密的
	WORD	method;	 // 如果是0，说明是未压缩的，如果是8，说明是压缩的，可用zlib解压
	WORD	file_time;
	WORD	file_date;
	DWORD	crc-32;
	DWORD	csize;
	DWORD	usize;
	WORD	namelength;
	WORD	extralength;
	BYTE[namelength]	   name;
	BYTE[extralength]	   extra;
	BYTE[usize]	   file_data;   //可能是压缩的，也可能是未压缩的
      }