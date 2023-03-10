-l library  在连接时搜索名为library的库。
你在命令中的哪个位置写这个选项是有区别的。
链接器会按照指定的顺序搜索和处理库和对象文件
因此，foo.o -lz bar.o, 搜索库z 在文件foo.o之后，但在bar.o之前。
如果bar.o引用了z中的函数，这些函数可能不会被加载

gcc连接测试：
    a.cpp 含有main函数，extern int g; 并调用func函数
    b.cpp/b.h 含有func函数，含有 int g = 2 全局变量
    c.cpp/c.h 含有func函数，含有 int g = 3 全局变量
    将 b 和 c 生成PIC动态库
    如果先连接 c.so 后连接 b.so ，则调用到的是 c 中的func
    如果先连接 b.so 后连接 c.so , 则调用到的是 b 中的func
    这说明 按照指定的连接顺序，链接目标文件
    如果已经在前面的动态库中找到了未定义的符号，
    则即使后面的动态库中再次出现该符号，也不使用了，而是仍用前面找好的
    所以，考虑到要连接的多个动态库可能存在同名符号的情况，
    越是基础的、通用的、如果出现符号冲突时，优先级越低的，连接位置应该越靠后
    另外，含有main的目标文件（根据测试结果猜测）总是最先被链接，而不管其真实连接位置如何
    也就是说，当main中也有func函数时，则总是调到自己的func函数，即使b.so优先main文件被链接
    使用ldd命令列出的依赖库，即是库的查找顺序（也就是说连接顺序不同，ldd的结果也不同）

gcc编译主程序时，会建立符号表
当符号表中存在为实现的符号时，会通过之后的链接对象(.o文件或库文件)来完善该符号表
在链接新对象时，根据之前建立的符号表，从链接对象中

elf文件格式简介
    参：https://blog.csdn.net/mergerly/article/details/94585901
    对象文件有三类：
    1. 可重定位的对象文件(Relocatable file)，这是由汇编器汇编生成的 .o 文件
    2. 可执行的对象文件(Executable file)
    3. 可被共享的对象文件(Shared object file)，这些就是所谓的动态库文件，也即 .so 文件
    elf文件的各个部分
    总述：
        elf文件在链接时和运行时，有不同的视图
        这句话的意思是，elf既规定的文件的链接结构，又规定来文件的执行结构
        elf既包含文件的链接信息，又包含文件的执行信息。
        在文件链接时，只需关注文件的链接结构，无需关注文件的执行结构，反之亦然。
        链接视图以节（Section）为单位，执行视图以段（Segment）为单位
        另外，segment是一个或多个section的集合，sections按一定规则映射到segment
        我们知道，内存的权限管理的粒度是以页为单位的，页内的内存具有同样的权限等属性，
        每页的大小一般为4k。如果不使用段的概念，直接将程序中的节放到内存中，
        则因为不同的节可能具有不同的权限属性，所以就得将每个节放在整数倍的内存页中，
        这就可能导致内存的浪费（如一个节的大小是4200B，则一页放不下，需要占用两页）
        于是提出段的概念，将多个具有相同权限（flag值）的section分到一个segment
        就可以辅助/指导将这些具有相同权限属性的节（如有的只读的，有的是可写的，
        有的是可执行的等等），连续的放到内存页中，避免内存浪费
    ELF头
        描述整个文件的组织
        使用 readelf -h 可以查看 ELF头信息，包括：
        e_ident     ： ELF的一些标识信息，前四位为.ELF,其他的信息比如大小端等
        e_machine   ： 文件的目标体系架构，比如ARM
        e_version   :  0为非法版本，1为当前版本
        e_entry     ： 程序入口的虚拟地址
        e_phoff     ： 程序头部表偏移地址
        e_shoff     ： 节区头部表偏移地址
        e_flags     ： 保存与文件相关的，特定于处理器的标志
        e_ehsize    ： ELF头的大小
        e_phentsize ： 每个程序头部表的大小
        e_phnum     ： 程序头部表的数量
        e_shentsize ： 每个节区头部表的大小
        e_shnum     ： 节区头部表的数量
        e_shstrndx  ： 节区字符串表位置
    程序头表（program header table） （也可称为段头表：segment header table）
        执行时有用，描述文件中的各种segments，告诉系统如何创建进程映像
        readelf -l / --segments 可查看文件的执行视图（段头信息）
    sections/segments
        segments 从运行的角度来描述elf文件
        sections 从链接的角度来描述elf文件
        也就是说，在链接阶段，我们可以忽略 program header table 来处理此文件
        在运行阶段，我们可以忽略 section header table 来处理此程序
        有些节是系统预订的，一般以.号开头，有必要了解一些常用的系统节区：
        系统预订的节（不全）
            名称		类型		属性			含义
            .bss		SHT_NOBITS	SHF_ALLOC+SHF_WRITE	包含将出现在程序的内存映像中的为初始化数据。根据定义，当程序开始执行，系统将把这些数据初始化为 0。此节区不占用文件空间。
            .comment	SHT_PROGBITS	(无)			包含版本控制信息。
            .data		SHT_PROGBITS	SHF_ALLOC+SHF_WRITE	这些节区包含初始化了的数据，将出现在程序的内存映像中。
            .data1		SHT_PROGBITS	SHF_ALLOC+SHF_WRITE	这些节区包含初始化了的数据，将出现在程序的内存映像中。
            .debug		SHT_PROGBITS	(无)			此节区包含用于符号调试的信息。
            .dynamic	SHT_DYNAMIC				此节区包含动态链接信息。节区的属性将包含 SHF_ALLOC 位。是否 SHF_WRITE 位被设置取决于处理器。
            .dynstr		SHT_STRTAB	SHF_ALLOC		此节区包含用于动态链接的字符串，大多数情况下这些字符串代表了与符号表项相关的名称。
            .dynsym		SHT_DYNSYM	SHF_ALLOC		此节区包含了动态链接符号表。
            .fini		SHT_PROGBITS	SHF_ALLOC+SHF_EXECINSTR	此节区包含了可执行的指令，是进程终止代码的一部分。程序正常退出时，系统将安排执行这里的代码。
            .got		SHT_PROGBITS				此节区包含全局偏移表。
            .hash		SHT_HASH	SHF_ALLOC		此节区包含了一个符号哈希表。
            .init		SHT_PROGBITS	SHF_ALLOC+SHF_EXECINSTR	此节区包含了可执行指令，是进程初始化代码的一部分。
                                        当程序开始执行时，系统要在开始调用主程序入口之前（通常指 C 语言的 main 函数）执行这些代码。
            .interp		SHT_PROGBITS				此节区包含程序解释器的路径名。如果程序包含一个可加载的段，段中包含此节区，那么节区的属性将包含 SHF_ALLOC 位，否则该位为 0。
            .line		SHT_PROGBITS	(无)			此节区包含符号调试的行号信息，其中描述了源程序与机器指令之间的对应关系。其内容是未定义的。
            .note		SHT_NOTE	(无)			此节区中包含注释信息，有独立的格式。
            .plt		SHT_PROGBITS				此节区包含过程链接表（procedure linkage table）。
            .relname	SHT_REL
            .relaname	SHT_RELA 				这些节区中包含了重定位信息。如果文件中包含可加载的段，段中有重定位内容，节区的属性将包含 SHF_ALLOC 位，否则该位置 0。
                                        传统上 name 根据重定位所适用的节区给定。例如 .text 节区的重定位节区名字将是：.rel.text 或者 .rela.text。
            .rodata
            .rodata1	SHT_PROGBITS	SHF_ALLOC		这些节区包含只读数据，这些数据通常参与进程映像的不可写段。
            .shstrtab	SHT_STRTAB				此节区包含节区名称。
            .strtab		SHT_STRTAB				此节区包含字符串，通常是代表与符号表项相关的名称。如
                                        果文件拥有一个可加载的段，段中包含符号串表，节区的属性将包含SHF_ALLOC 位，否则该位为 0。
            .symtab		SHT_SYMTAB				此节区包含一个符号表。如果文件中包含一个可加载的段，并且该段中包含符号表，那么节区的属性中包含SHF_ALLOC 位，否则该位置为 0。
            .text		SHT_PROGBITS	SHF_ALLOC+SHF_EXECINSTR	此节区包含程序的可执行指令。
            类型		介绍	  参：https://www.jianshu.com/p/53ccc77abc6a		
            .text		保存的是编译后的程序机器码
            .rodata		保存的是只读数据，比如printf语句中的格式化字符串，用于stwich语句的jump table等；
            .data		保存的是被初始化的全局变量和静态变量；	局部变量被保存在运行时栈中，所以既不会出现在.data段，也不会出现在.bss段；
            .bss		全称为Better Save Space；保存的是未被初始化额全局变量和静态变量，及被初始化为0的初始变量；在目标文件中不占据实际空间；
            .systab		符号表；保存的是在程序中定义或者引用的函数、全局变量；每个重定位文件都有一份符号表systab；跟编译器中的符号表相比，这里的.symtab符号表里不包括局部变量符号；
            .rel.text	保存的是.text节(指令里)中需要重新修改的位置信息；任何一个调用外部函数或者引用全局变量的指令的位置信息都需要被修改；
                    调用局部函数的指令的位置信息不需要修改；在可执行目标文件中，不需要重定位信息，通常是被忽略的，除非指令显式地告知链接器要保存它；
            .rel.data	保存的是在这个目标文件里定义或者引用的任何全局变量的重定位信息；任何一个初始化值是全局变量地址或者在外部定义的函数地址的全局变量都需要别重新定位；
            .debug		调试信息表，条目保存的是在程序中定义的局部变量或者通过typedef定义的变量、在程序中定义或者引用的全局变量、源代码文件等；只有编译器驱动程序使用了-g选项，才会出现的；
            .line		保存的是源代码中的行数到.text中的机器指令的映射关系；只有编译器驱动程序使用了-g选项，才会出现的；
            .strtab		保存的是在.symtab节和.debug节中的符号表中的字符串，及在节头表中定义的节名字的字符串；是由以null结尾的字符序列；
        重要的系统节：
            符号表 .dynsym
                用来定位、重定位程序中符号定义和引用的信息。
                简单的理解就是符号表记录了该文件中的所有符号，所谓的符号就是经过修饰了的函数名或者变量名，不同的编译器有不同的修饰规则。
                例如符号_ZL15global_static_a，就是由global_static_a变量名经过修饰而来。
                符号表 表项的结构成员：
                    st_name : 符号表项名称，如果该值非0,则索引(offset) "符号名字符串表"，以获得真实名称
                    st_value: 符号的地址。依赖上下文，可以是一个绝对值、一个地址等等。
                    st_size : 符号的尺寸大小，如一个数据对象的占用字节数
                    st_info : 符号的类型和绑定属性
                    st_other: 为0,未定义
                    st_shndx: 给出相关的SHT的索引
            字符串表 .dynstr .shstrtab
                上面的符号表中的st_name，就是索引的该表中记录的字符串
                .dynstr 存储的是符号表名称的字符串， .shstrtab 存储的是section名称的字符串
            重定位表
                重定位的概念
                    程序从代码到可执行文件这个过程中，要经历编译器，汇编器和链接器对代码的处理。
                    然而编译器和汇编器通常为每个文件创建程序地址从0开始的目标代码，但是几乎没有计算机会允许从地址0加载你的程序。
                    如果一个程序是由多个子程序组成的，那么所有的子程序必需要加载到互不重叠的地址上。
                    重定位就是为程序不同部分分配加载地址，调整程序中的数据和代码以反映所分配地址的过程。
                    简单的言之，则是将程序中的各个部分映射到合理的地址上来。
                    换句话来说，重定位是将符号引用与符号定义进行连接的过程。
                    例如，当程序调用了一个函数时，相关的调用指令必须把控制传输到适当的目标执行地址。
                    具体来说，就是把符号的value进行重新定位。
                重定位表项的结构成员：
                    r_offset : 重定位动作所适用的位置
                    r_info   : 要进行重定位的符号表表项的索引，以及重定位的方法（哪些位需修改、以及如何计算它们的取值）
                使用 readelf -r 可查看重定位信息，例：
                    文件：libcpp.reader.core-s.a(mucbz.o)
                    重定位节 '.rela.text' 位于偏移量 0x6400 含有 42 个条目：
                      偏移量          信息           类型           符号值        	符号名称 + 加数
                    000000000222  002000000004 R_X86_64_PLT32    0000000000000000 fz_count_archive_entri - 4
                    00000000024d  002100000004 R_X86_64_PLT32    0000000000000000 fz_malloc_array - 4
                    。。。（省略若干行）
                    重定位节 '.rela.data.rel.local' 位于偏移量 0x67f0 含有 29 个条目：
                      偏移量          信息           类型           符号值        	符号名称 + 加数
                    000000000000  000500000001 R_X86_64_64       0000000000000000 .rodata + 0
                    000000000008  000500000001 R_X86_64_64       0000000000000000 .rodata + 5
                    。。。（省略若干行）
                    重定位节 '.rela.debug_info' 位于偏移量 0x6aa8 含有 581 个条目：
                      偏移量          信息           类型           符号值        	符号名称 + 加数
                    000000000006  00180000000a R_X86_64_32       0000000000000000 .debug_abbrev + 0
                    00000000000c  001b0000000a R_X86_64_32       0000000000000000 .debug_str + 68c
                    。。。（省略若干行）
                    文件：libcpp.reader.core-s.a(muimg.o)
                    重定位节 '.rela.text' 位于偏移量 0x5850 含有 29 个条目：
                      偏移量          信息           类型           符号值        	符号名称 + 加数
                    00000000002b  001c00000004 R_X86_64_PLT32    0000000000000000 fz_drop_image - 4
                    00000000007f  001d00000004 R_X86_64_PLT32    0000000000000000 fz_image_resolution - 4
                    000000000089  000b00000002 R_X86_64_PC32     0000000000000000 .rodata + 12c
                    。。。（省略若干行）
                    说明：
                    上面的偏移量，对应重定位表项的结构成员 r_offset，
                    而信息、类型，对应重定位表项的结构成员 r_info，信息即要进行重定位的符号表表项的索引，与其后的符号名称相对应		
    节头表（section header table，SHT）
        链接时有用，记录来各节的信息，如大小/偏移等。
        可通过 readelf -S 来查看文件中都有哪些section
        针对每个section，都设置有一个条目（entry），记录节的名称、类型、大小、偏移等信息
        SHT每个条目的结构及详细介绍请参见原网页

链接过程详解
	

