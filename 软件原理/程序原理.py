GCC编译的多个阶段：
    编译器将代码文件进行预处理(.i)、汇编(.s)后，下一步就是编译成机器语言，
    结果是生成"可重定位的目标文件(.o)"，最后把这些目标文件链接成可执行文件。
    #cpp工具完成预处理，cc1工具完成汇编，as工具用于生成目标文件，ld工具完成链接。
    gcc -E 预处理
    gcc -S 预处理+汇编
    gcc -c 预处理+汇编+生成目标文件
    gcc    预处理+汇编+生成目标文件+链接
    
目标文件简介
    目标文件一般是由汇编器生成的.o后缀的文件，大概有三种不同的形式：
    可重定位目标文件、可执行目标文件、共享目标文件
    
可重定位的目标文件简介
    windows下是.obj，linux下是.o
    它跟可执行文件的内容和结构相似，所以一般跟可执行文件采用同一种格式存储。
    目标文件结构，参<可执行文件格式/ELF格式详解>
    注：代码段及数据段存放的是实际的函数代码内容和数据数据值，而函数名、变量名这些索引信息，是在符号表中记录的，
    符号表中记录了函数名/变量名，是否在本目标文件中存在，如果存在，则记录他们在哪个段(节)的什么位置
        
可执行文件格式
    Windows下的是PE（Portable Executable）
    Linux下的是ELF（Executable Linkable Format），
    它们都是COFF（Common file format）格式的变种。
    ELF格式详解
        ELF文件结构
            ELF文件头（64字节大小）
                unsigned char e_ident[EI_NIDENT];   16字节大小，该文件使用的平台、大小端规则
                uint16_t      e_type;               文件类型, 表示该文件属于可执行文件、可重定位文件、core dump文件或者共享库        
                uint16_t      e_machine;            机器类型        
                uint32_t      e_version;            通常都是1    
                ElfN_Addr     e_entry;              8字节大小，表示程序执行的入口地址       
                ElfN_Off      e_phoff;              8字节大小，表示Program Header的入口偏移量（以字节为单位）     
                ElfN_Off      e_shoff;              8字节大小，表示Section Header的入口偏移量（以字节为单位）      
                uint32_t      e_flags;              保存了这个ELF文件相关的特定处理器的flag
                uint16_t      e_ehsize;             表示ELF Header大小（以字节为单位）       
                uint16_t      e_phentsize;          表示Program Header大小（以字节为单位）
                uint16_t      e_phnum;              表示Program Header的数量 （十进制数字）        
                uint16_t      e_shentsize;          表示Section Header大小（以字节为单位）      
                uint16_t      e_shnum;              表示Section Header的数量 （十进制数字）  
                uint16_t      e_shstrndx;           表示字符串表的索引，字符串表用来保存ELF文件中的字符串，比如段名、变量名。
            Program Header Table(程序头)
                根据其内容在内存中是否可读写等属性，可以将不同的section划分成不同的segment。
                其中每个segment可以由一个或多个section组成。
                可执行程序加载时会用到segment提供的信息。
                对于动态库，因为其本身不能直接执行，所以在动态库中没有程序头表。
                Program Header Table中存的就是各个segment的相关信息：
                    该segment相对ELF文件的偏移量  
                    该segment在虚拟内存中的偏移量
                    该segment的大小
                    该segment在内存中的大小
                    该segment在内存中需要以多少对齐
                    。。。
            ★ sections
                .text           代码段 
                .data           初始化的数据段 
                .bss            未初始化的数据段 
                .rodata         常量段 
                .init_array     程序运行时,执行.init_array中的指令。
                .fini_array     程序退出时,执行.fini_array中的指令   
                .comment        GCC编译器信息 
                .symtab         符号表   Elf64_Symbol结构体列表 
                    表项内容：
                        st_name  在符号名称表(.dynstr)中的索引
                        st_value 函数地址或是一个常量值
                        st_size  从 st_value 地址开始,共占的长度大小
                        st_info  用于标示此符号的属性,占一个字节,低四位标志作用域,高四位标示符号类型
                            第四位：
                                0  STB_LOCAL    目标文件以外不可见，相同名称的局部符号可以存在于多个文件中,互不影响
                                1  STB_GLOBAL   全局符号对所有将组合的目标文件都是可见的
                                2  STB_WEAK     弱符号与全局符号类似,不过他们的定义优先级比较低。
                            高四位：
                                1  STT_OBJECT   符号与某个数据对象相关,比如一个变量、数组等等
                                2  STT_FUNC     符号与某个函数或者其他可执行代码相关
                                3  STT_SECTION  符号与某个节区相关，这种类型的符号表项主要用于重定位,通常具有 STB_LOCAL 绑定
                                4  STT_FILE     给出了与目标文件相关的源文件的名称，文件符号具有 STB_LOCAL 绑定
                        st_other 固定值为0。
                        st_shndx 该符号表项相关的节区头部表索引
                .dynsym         符号名称表   
                .got            全局偏移表   为全局符号提供偏移地址(指向过程链接表)
                .plt            过程链接表   每个表项都是一段代码,作用是跳转至真实的函数地址
                .eh_frame       调试信息     以DWARF格式保存的一些调试信息
                .strtab         字符串表(只读数据段)  保存函数名、文件名等信息
                .shstrtab       节头字符串表(section header string table)   存储各个section的名字
                    对于字符串的定义,是以NULL(\0)开头,以NULL结尾。
                    举例：00 2E 73 68 73 74 72 74 61 62 00 2E 69 6E 74 65 72 70 00 2E 64 79 6E 73 79 6D 00
                    从这里可以得到3个字符串即：
                    2E 73 68 73 74 72 74 61 62 (.shstrtab);
                    2E 69 6E 74 65 72 70 (.interp);
                    2E 64 79 6E 73 79 6D (.dynsym);
                    假如索引为0,那么字符串的内容就是 2E 73 68 73 74 72 74 61 62 (.shstrtab)
                .rel.text       代码重定位信息   代码段中引用的外部函数和全局变量的重定位条目 
                .rel.data       已经初始化数据的重定位信息
                .rela.eh_frame  字节对齐的重定位信息之eh_frame的重定位信息
                。。。
                附注：
                    当使用支持异常的语言（例如C ++）时，必须向运行时环境提供附加信息，
                    以描述在处理异常期间必须解除的调用帧。
                    此信息包含在目标文件的特殊部分中，例如.eh_frame和.eh_frame_hdr。
                    以“.”开头的节区名称是系统保留的。
                    应用程序可以使用没有前缀的节区名称,以避免与系统节区冲突
                    目标文件中也可以包含多个名字相同的节区
            Section Header Table
                记录上面各个section的相关信息
                    该section中存放的内容类型/结构类型，如符号表(STRTAB)、可重定位段等
                        SYMTAB  此节区包含一个符号表，一般用于链接编辑(指ld而言)的符号,尽管也可用来实现动态链接。
                        STRTAB  此节区包含字符串表，目标文件可能包含多个字符串表节区
                        REL     此节区包含重定位表项,其中没有补齐(addends)，目标文件中可以拥有多个重定位节区。
                        RELA    此节区包含重定位表项,其中可能会有补齐内容(addend)，目标文件可能拥有多个重定位节区。
                        HASH    此节区包含符号哈希表。所有参与动态链接的目标都必须包含一个符号哈希表。
                        DYNAMIC 此节区包含动态链接的信息。目前一个目标文件中只能包含一个动态节区
                        DYNSYM  保存动态链接符号的一个最小集合
                        PROGBITS此节区包含程序定义的信息,其格式和含义都由程序来解释
                        。。。
                    该section的属性，如可读、可写、可执行等
                    该section在程序运行时的内存地址
                    该section相对ELF文件开始位置的偏移量
                    该section的大小
                    该section需要的地址对齐信息
                    有些section下保存的长度固定的条目，如符号表，对于这样的setcion，还记录条目的长度
                    。。。
    
readelf工具
    -h  显示ELF文件头
    -l  显示程序头表(Program Header Table)
    -S  显示Section Header Table
    -e  = -h -l -S
    -g  显示section groups
    -t  显示各section的描述（跟-S差不多）
    -s  显示符号表
    --dyn-syms  显示动态符号表
    -d  显示dynamic节
    -V  显示version节
    -r  显示重定位信息
    -A  显示架构信息
    -c  显示archive(归档)文件的符号/文件索引
    -x  <number|name>  将<number|name>节显示为字节流
    -p  <number|name>  将<number|name>节显示为字符串
    -R  <number|name>  将<number|name>节显示为重定位后的字节流
    
objdump工具
    使用binutils的工具objdump可查看目标文件内部结构
    -h显示各个段的基本信息，
    -x显示各个段更全的信息
    -d显示可执行部分的汇编代码
    -D显示全部的汇编代码
    -f显示文件头概要
    -t显示符号表
    -T显示动态符号表
    -r显示重定位信息
    -g显示调试信息
    -e显示调试信息（按ctags格式）
    -R显示动态重定位信息
        
静态库
    静态库只是将一堆目标文件进行打包
    连接静态库时，并不是把整个静态库都连接到程序中，
    而是看都会用到静态库中的哪些目标文件，用到哪个，就链接哪个
    
链接器工作
    符号解析
        扫描每一个给定的目标文件（的符号表），综合分析后，最终判断是否有未定义的符号
        如果有未定义的符号，则报错，链接过程终止
        如果多个目标文件中存在同名的符号，链接器(ld)会给出重定义错误提示
    重定位
        将指定的所有目标文件按顺序合成（代码段合成、数据段合成等）
        符号表中存放的将是整合后的符号信息
        ELF文件/sections/.rel.text       代码重定位信息，代码段中引用的外部函数和全局变量的重定位条目 
        ELF文件/sections/.rel.data       已经初始化数据的重定位信息
        这两个节下存的都是Elf32_Rel结构的重定位信息条目
        struct Elf32_Rel
            int offset      //需要修改的引用节的偏移
                              如果该条件在.rel.text下，
                              则引用节就是指的.text节
                              offset就是.text节中的偏移位置
            int symbol:24   //标识被修改引用应该指向的符号
            int type:8      //告诉连接器如何修改新的引用
                ELF有11种不同的重定位类型：我们只关心常用的两种      
                R_386_PC32（相对地址引用）和R_386_32（绝对地址引用）
        对重定位的举例说明：
            在.text节（代码段）中，有句 func2()；
            但该func2是在别处（别的目标文件或动态库中）定义的。
            所以在重定位前，该函数的地址是未知的，
            所以func2()对应的汇编代码可能就是：
            call 0x00000000;    //对于找不到的符号，在符号表中有记录
            假定 这个0x0000000（代表函数地址）字节位置在.text节的偏移位置为7（第7个字节处），
            则在将该文件编译成目标文件时，在重定位表中，就会记录这样一条：
            offset=7  symbol=func2   type=...
            这样，当各个目标文件合成时，如果func2已经已知了（func2在别的目标文件中），
            则就可以对上面的重定位条目进行处理了：
            只需把func2换成真正的地址就行（通过查合并后的符号表可得），
            处理完后，该条目就可以从重定位表中移除了，
            而如果func2在别的动态库中，则该条目就会留存到动态链接时完成。
            一句话说明，就是把代码段中的外部函数或外部变量地址，变成有效的地址。
            
        
        
