grub-install 
    当你的电脑不能启动了（BootLoader坏了，或想换成grub的BootLoader）
    此时可以使用这个工具安装grub引导
    grub-install只是一个脚本，内部真正执行工作的是grub-mkimage和grub-setup
    因此你也可以直接用着两个命令安装grub
    grub2-install 是个elf文件
grub2-install
    grub2-install 都做了什么事情:
    A. grub2-install 会查找可用的module, 默认是查找 /usr/lib/grub/i386-pc 这个目录，
       这些module 会被copy 到/boot/grub2/i386-pc 下，
       如果grub的这些module 不在默认路径下，
       那么就可以通过 --directory  参数来指定Module以及image的路径, 
       除非默认的找不到才需要设置，否则一般都用默认的路径。
    B. grub2-install 安装grub的时候，
       会copy grub需要的module 到/boot 分区的相应路径下，
       所以在修复模式安装grub的时候，可能需要指定 --boot-directory，
       或者要安装grub到其他的device, 也需要指定这个参数 。
    C. grub安装的时候，还支持一个 --root-directory 的参数，
       这个参数不在”man grub2-install"的帮助文档中，
       个人对这个参数的理解是： 没有指定--boot-directory的情况下，
       --root-directory参数的值才有意义 ，
       当没有指定--boot-directory，但是指定了--root-directory，
       那么会在--root-directory指定的目录下创建boot 子目录， 作为--boot-directory 来使用. 
       这个--root-directory 和系统引导时候的root 没有任何关系.
    D. 如果重装grub,
       通常可能希望重新创建device map 关系，这时候可以用参数：--recheck来实现，
       这个参数的作用是：如果有必要，删除存在的device map, 然后创建一个新的，
       比如我们把grub 安装到了一个新的device 上可能就需要这么做。
    E. 强制进行grub的安装，即便发现有问题. 这时候可以用参数 --force
    F. grub2-install 在执行的时候，还会调用其他的grub相关的命令，
       这些参数一般不需要更改. 这里就不介绍了.
grub-mkimage
    kernel.img和一些模块动态编译成core.img
grub-mkconfig
    调用grub-mkdevicemap和grub-probe生成grub.cfg
grub2-mkconfig
    一般用法：grub2-mkconfig -o /boot/grub2/grub.config
    会参考/etc/grub.d/，/etc/default/grub，生成grub.config文件
    而/boot/grub.d下的10_linux脚本文件会探测/boot下的内核文件
    /boot/grub2/grub.config : bios会使用这个引导
    /boot/efi/EFI/centos/grub.cfg : efi会使用这个引导
grub_probe
    从给定的设备上探测设备信息
grub_setup
    被grub_install调用，安装grub
grub-mkdevicemap  ?
    为grub自动产生新的device.map，
    grub-mkdevicemap程序可以创建device.map文件，
    在执行grub-install时会自动执行他以创建映像关系，
    如果文件不存在，则会读取/boot/grub/devicd.map这个文件，
    如果映像文件存在，则grub读取他创建BIOS drives to OS drives
update-grub
    update-grub主要是在每次配置文件有更新后生成新的grub.cfg，
    其实update-grub是调用grub-mkconfig，
    在系统中还有一个update-grub2，发现他是调用update-grub
grub-set-default
    设置在下次进入系统时从哪个内核选项进去
grub2 
    grub2采用模块化的设计，主要配置文件是/boot/grub/grub.cfg
    但是这个文件的权限是444，连root也不让修改，这是刻意为之的，
    不要修改文件权限，grub.cfg的内容更新由update-grub命令来更新，
    其实就是执行grub-mkconfig -o /boot/grub/grub.cfg来更新
/boot/grub/grub.cfg、/boot/efi/EFI/centos/grub.cfg
    此文件是只读的不允许手动修改，grub-mkconfig在大多数情况下生成grub.cfg
    这个配置文件是系统引导时候会读取的，如果这个文件缺失，那么会导致引导失败
    到/etc/default/grub 这个文件里面添加自定义的grub配置项. 
    更改完成之后，可以用 grub2-mkconfig -o /boot/grub2/grub.cfg  
    把自定义的变更apply 到grub的配置文件中
/boot/grub2/grub.cfg
    https://blog.csdn.net/ctthuangcheng/article/details/56679683
    附注：在进到选择系统菜单时，按e可进行入编辑grub模式，按c可进入cmd模式
    grub.cfg脚本支持的变量（部分）
        这里只列出常用的一些变量，
        完整的列表可以参考GRUB2手册中的"Special environment variables"部分
        ?
            上一条命令的返回值，零表示成功，非零表示失败[与bash一样]。
            由GRUB2自动设置。你只能使用此变量，而不能修改它。
        check_signatures
            是否在加载文件时强制验证签名，可以设为'yes'或'no'
        chosen
            当前被执行的菜单项名称
            (紧跟"menuentry"命令之后的字符串或者'--id'选项的参数)，
            例如'Windows 7'。由GRUB2自动设置。你
            只应该使用此变量，而不应该修改它。
        cmdpath
            当前被加载的"core.img"所在目录(绝对路径)。
            例如：UEFI启动可能是'(hd0,gpt1)/EFI/UBUNTU'或'(cd0)/EFI/BOOT'，
            BIOS启动可能是'(hd0)'。由GRUB2自动设置。
            你只应该使用此变量，而不应该修改它。
        debug
            设为'all'时表示开启调试输出[会显示大量信息,谨慎开启]
        default
            默认选中第几个菜单项(从'0'开始计数)
        fallback
            如果默认菜单项启动失败，
            那么就启动第几个菜单项(从'0'开始计数)
        gfxmode
            设置"gfxterm"模块所使用的视频模式，
            可以指定一组由逗号或分号分隔的模式以供逐一尝试：
            每个模式的格式必须是：'auto'(自动检测),'宽x高','宽x高x色深'之一，
            并且只能使用VBE标准指定的模式
            [640x480,800x600,1024x768,1280x1024]x[16,24,32]。
            可以在GRUB SHELL中使用"videoinfo"命令列出当前所有可用模式。
            默认值是'auto'。
        gfxpayload
            设置Linux内核启动时的视频模式，
            可以指定一组由逗号或分号分隔的模式以供逐一尝试：
            每个模式的格式必须是：'text'(普通文本模式,不能用于UEFI平台),
            'keep'(继承"gfxmode"的值),'auto'(自动检测),'宽x高','宽x高x色深'之一，
            并且只能使用VBE标准指定的模式[640x480,800x600,1024x768,1280x1024]x[16,24,32]。
            在BIOS平台上的默认值是'text'，在UEFI平台上的默认值是'auto'。
            除非你想明确设置Linux控制台的分辨率
            (要求内核必须"CONFIG_FRAMEBUFFER_CONSOLE=y")，
            或者打算在BIOS平台上使用图形控制台
            (要求内核必须"CONFIG_FRAMEBUFFER_CONSOLE=y")，
            否则不要设置此变量。
        gfxterm_font
            设置"gfxterm"模块所使用的字体，默认使用所有可用字体
        grub_cpu
            此GRUB所适用的CPU类型。
            例如：'i386', 'x86_64'。由GRUB2自动设置。
            你只应该使用此变量，而不应该修改它。
        grub_platform
            此GRUB所适用的平台类型。例如：'pc', 'efi'。
            由GRUB2自动设置。你只应该使用此变量，而不应该修改它。
        lang
            设置GRUB2的界面语言，必须搭配"locale_dir"变量一起使用。
            简体中文应设为'zh_CN'。
        locale_dir
            设置翻译文件(*.mo)的目录，通常是'$prefix/locale'，
            若未明确设置此目录，则禁止国际化。
        pager
            如果设为'1'，那么每一满屏后暂停输出，等待键盘输入。
            缺省是''，表示不暂停。
        prefix
            绝对路径形式的'/boot/grub'目录位置(也就是GRUB2的安装目录)，
            例如'(hd0,gpt1)/grub'或'(hd0,msdos2)/boot/grub'。
            初始值由GRUB在启动时根据"grub-install"在安装时提供的信息自动设置。
            你只应该使用此变量，而不应该修改它。
        root
            设置"根设备"。任何未指定设备名的文件都视为位于此设备。
            初始值由GRUB在启动时根据"prefix"变量的值自动设置。
            在大多数情况下，你都需要修改它。
        superusers
            设置一组"超级用户"(使用空格/逗号/分号进行分隔)，
            以开启安全认证的功能。
        theme
            设置菜单界面的主题风格文件的位置，
            例如："/boot/grub/themes/starfield/theme.txt"。
            关于如何定制界面风格(背景图片/字体/颜色/图标等)的细节，
            可以参考GRUB2手册中的" Theme file format"部分。
        timeout
            在启动默认菜单项前，等待键盘输入的秒数。
            默认值是'5'秒。
            '0'表示直接启动默认菜单项(不显示菜单)，'-1'表示永远等待
    grub.cfg脚本支持的命令
        对于GRUB-2.0.2版本来说，所有可用的命令有大约200个之多
        更多的命令说明可以参考GRUB2手册
        参：https://www.gnu.org/software/grub/manual/grub/grub.html
        中的"The list of available commands"页面中列出的几个二级页面
        menuentry 
            menuentry "title" [--class=class …] [--users=users] 
                              [--unrestricted]  [--hotkey=key] 
                              [--id=id] [arg …] 
                              { command; … }
            定义一个名为"title"的菜单项。
            当此菜单项被选中时，GRUB将会把环境变量"chosen"的值设为"id"
            (使用了[--id=id]选项)或"title"(未使用[--id=id]选项)，
            然后执行花括号中的命令列表，
            如果列表中最后一个命令执行成功，并且已经载入了一个内核，
            那么将执行"boot"命令。
            可以使用 --class 选项指定菜单项所属的"样式类"。
            而可以使用指定的主题样式显示菜单项。
            可以使用 --users 选项指定只允许特定的用户访问此菜单项。
            如果没有使用此选项，则表示允许所有用户访问。
            可以使用 --unrestricted 选项指明允许所有用户访问此菜单项。
            可以使用 --hotkey 选项设置访问此菜单项的热键(快捷键)。
            "key"可以是一个单独的字母，
            或者'backspace','tab','delete'之一。
            可以使用 --id 选项为此菜单项设置一个全局唯一的标识符。
            "id"必须由ASCII字母/数字/下划线组成，且不得以数字开头。
            [arg …]是可选的参数列表。
            你可以把它们理解为命令行参数。
            实际上"title"也是命令行参数，
            只不过这个参数是个必须参数而已。
            这些参数都可以在花括号内的命令列表中使用，
            "title"对应着"$1"，其余的以此类推。
        terminal_input 
            terminal_input [--append|--remove] 
                           [terminal1] [terminal2] …
            如果不带任何选项与参数，
            则表示列出当前激活的输入终端，
            以及所有其他可用的输入终端。
            可以使用 --append 选项将指定的终端
            加入到激活的输入终端列表中，
            所有列表中的终端都可以用于向GRUB提供输入。
            可以使用 --remove 选项将指定的终端
            从激活的输入终端列表中删除。
            如果不使用任何选项，但是指定了一个或多个终端参数，
            则表示将当前激活的输入终端设置为参数指定的终端。
        terminal_output
            terminal_output [--append|--remove] 
                            [terminal1] [terminal2] …
            如果不带任何选项与参数，则表示列出当前激活的输出终端，
            以及所有其他可用的输出终端。
            可以使用 --append 选项将指定的终端
            加入到激活的输出终端列表中，
            所有列表中的终端都将接受到GRUB的输出。
            可以使用 --remove 选项将指定的终端
            从激活的输出终端列表中删除。
            如果不使用任何选项，但是指定了一个或多个终端参数，
            则表示将当前激活的输出终端设置为参数指定的终端。
        authenticate [userlist]
            检查当前用户是否位于"userlist"或环境变量"superusers"中。
            [注意]如果环境变量"superusers"的值为空，此命令将返回'真'。
        background_color color
            设置当前激活的输出终端的背景颜色。
            "color"可以使用HTML风格的颜色表示法("#RRGGBB"或"#RGB")。
            [注意]仅在使用'gfxterm'作为输出终端的时候，才能改变背景色。
        background_image
            background_image [[--mode 'stretch'|'normal'] file]
            将当前激活的输出终端的背景图片设置为"file"文件。
            除非使用了"--mode 'normal'"选项，
            否则图片将被自动缩放以填满整个屏幕。
            如果不带任何选项与参数，则表示删除背景图片。
            [注意]仅在使用'gfxterm'作为输出终端的时候，才能改变背景图片。
        boot
            启动已经被载入的OS或链式加载器。
            仅在运行于交互式命令行的时候才是需要的。
            在一个菜单项结束时是隐含的。
        cat [--dos] file
            显示文件"file"的内容。如果使用了"--dos"选项，
            那么"回车/换行符"将被显示为一个简单的换行符。
            否则，回车符将被显示为一个控制符(<d>)。
        chainloader [--force] file
            链式加载"file"文件。
            通常使用磁盘块表示法，例如用'+1'表示当前根分区的第一个扇区。
            可以使用 --force 选项强制载入文件，而不管它是否有正确的签名。
            通常用于加载有缺陷的启动载入器(例如 SCO UnixWare 7.1)。
        configfile file
            将"file"作为配置文件加载。如果"file"中定义了菜单项，
            那么立即显示一个包含它们的菜单。
            [注意]"file"文件对环境变量所做的任何变更都将在从此文件返回后失效。
        cpuid [-l]
            检查CPU特性。仅在x86系统上可用。
            如果使用了 -l 选项，那么如果CPU是64位则返回真，否则返回假。
        drivemap 
            drivemap -l|-r|[-s] from_drive to_drive
            如果不使用任何选项，表示将"from_drive"映射到"to_drive"。
            这主要用于链式加载Windows之类的操作系统，
            因为它们只能从第一个硬盘启动。
            出于方便的原因，分区后缀将被忽略，
            因此你可用安全地将"${root}"作为磁盘使用。
            可以使用 -s 选项，执行反向映射，也就是交换这两个磁盘。
            例如： drivemap -s (hd0) (hd1)
            可以使用 -l 选项，列出当前已有的映射。
            可以使用 -r 选项，把映射重置为默认值，
            也就是撤销所有当前已有的映射。
        echo [-n] [-e] string …
            显示所要求的文本并换行(除非使用了 -n 选项)。
            如果有多个字符串，依次输出它们，并用空格分隔每一个。
            和bash的习惯一样，可以在双引号内使用"${var}"来引用变量的值，
            也可以使用 -e 选项激活对反斜杠转义符的解释( \\ \a \r \n \t ...)。
        export envvar
            导出环境变量"envvar"，
            以使其对于使用"configfile"命令载入的配置文件可见。
        false
            不做任何事，只返回一个失败的结果。
            主要用在if/while之类的控制构造中。
        gettext string
            把"string"翻译为环境变量"lang"指定的语言。
            MO格式的翻译文件从环境变量"locale_dir"指定的目录加载。
        halt [--no-apm]
            关闭计算机。如果指定了 --no-apm 选项，表示不执行APM BIOS调用。
            否则，计算机使用APM关闭。
        help [pattern …]
            显示内建命令的帮助信息。
            如果没有指定"pattern"，那么将显示所有可用命令的简短描述。
            如果指定了"pattern"，
            那么将只显示名字以这些"pattern"开头的命令的详细帮助信息。
        initrd[efi] file
            为以32位协议启动的Linux内核载入一个"initial ramdisk"，
            并在内存里的Linux设置区域设置合适的参数。
            [注意]这个命令必须放在"linux"命令之后使用。
        initrd16 file
            为以16位协议启动的Linux内核载入一个"initial ramdisk"，
            并在内存里的Linux设置区域设置合适的参数。
            [注意]这个命令必须放在"linux16"命令之后使用。
        insmod module
            载入名为"module"的GRUB2模块。
        linux[efi] file …
            使用32位启动协议从"file"载入一个Linux内核映像，
            并将其余的字符作为内核的命令行参数逐字传入。
            [注意]使用32位启动协议意味着'vga='启动选项将会失效。
            如果你希望明确设置一个特定的视频模式，
            那么应该使用"gfxpayload"环境变量。
            虽然GRUB可以自动地检测某些'vga='参数，
            并把它们翻译为合适的"gfxpayload"设置，但是并不建议这样做。
        linux16 file …
            以传统的16位启动协议从"file"载入一个Linux内核映像，
            并将其余的字符作为内核的命令行参数逐字传入。
            这通常用于启动一些遵守Linux启动协议的特殊工具(例如MEMDISK)。
            [注意]使用传统的16位启动协议意味着：
            (1)'vga='启动选项依然有效，
            (2)不能启动纯64位内核
            (也就是内核必须要'CONFIG_IA32_EMULATION=y'才行)。
        loadfont file …
            从指定的"file"加载字体，除非使用了绝对路径，
            否则"file"将被视为"$prefix/fonts/file.pf2"文件。
        loopback [-d] device file
            将"file"文件映射为"device"回环设备。例如：
            loopback loop0 /path/to/image
            ls (loop0)/
            可以使用 -d 选项，删除先前使用这个命令创建的设备。
        ls [arg …]
            如果不使用参数，那么列出所有对GRUB已知的设备。
            如果参数是包含在括号内的一个设备名，
            那么列出该设备根目录下的所有文件。
            如果参数是以绝对路径给出的目录，那么列出这个目录的内容。
        lsfonts
            列出已经加载的所有字体
        lsmod
            列出已经加载的所有模块
        normal [file]
            进入普通模式，并显示GRUB菜单。
            [说明]只要当前没有处于救援模式，
            其实就已经是在普通模式中了，
            所以通常并不需要明确使用此命令。
            在普通模式中，命令模块[command.lst]与加密模块[crypto.lst]
            会被自动按需载入(无需使用"insmod"命令)，
            并且可使用完整的GRUB脚本功能。
            但是其他模块则可能需要明确使用"insmod"命令来载入。
            如果给出了"file"参数，那么将从这个文件中读入命令
            (也就是作为"grub.cfg"的替代)，
            否则将从"$prefix/grub.cfg"中读入命令(如果存在的话)。
            你也可以理解为"file"的默认值是'$prefix/grub.cfg'。
            可以在普通模式中嵌套调用此命令，以构建一个嵌套的环境。
            不过一般不这么做，而是使用"configfile"命令来达到这目的。
        normal_exit
            退出当前的普通模式。如果这个普通模式实例不是嵌套在
            另一个普通模式里的话，就会返回到救援模式。
        parttool partition commands
            对分区表进行各种修改。目前只能作用于MBR分区表(DOS分区表)，
            而不能用于GPT分区表。目前仅支持以下三种用法：
            (1)设置或去掉分区的激活标记(仅对Windows系统有意义)。
            例如："parttool (hd0,msdos2) +boot"表示为(hd0,msdos2)
            分区加上激活标记，而"parttool (hd0,msdos2) -boot"则表示
            去掉(hd0,msdos2)分区的激活标记。
            (2)设置或去掉分区的隐藏标记(仅对Windows系统有意义)。
            例如："parttool (hd0,msdos2) +hidden"表示为
            (hd0,msdos2)分区加上隐藏标记，
            而"parttool (hd0,msdos2) -hidden"则表示
            去掉(hd0,msdos2)分区的隐藏标记。
            (3)更改分区的类型。其值必须是0x00-0xFF范围内的值。
            且应该使用'0xNN'格式的十六进制数。
            例如："parttool (hd0,msdos2) type=0x83"
            表示将(hd0,msdos2)分区类型修改为'0x83'(Linux分区)。
        password user clear-password
            定义一个名为user的用户，并使用明文口令'clear-password'。
            不建议使用此命令。
        password_pbkdf2
            password_pbkdf2 user hashed-password
            定义一个名为user的用户，并使用哈希口令'hashed-password'
            (通过"grub-mkpasswd-pbkdf2"工具生成)。
            这是建议使用的命令，因为它安全性更高。
        probe 
            probe [--set var] --driver|--partmap|--fs|
                              --fs-uuid|--label device
            提取"device"设备的特定信息。
            如果使用了 --set 选项，则表示将提取的结果保存在"var"变量中，
            否则将提取的结果直接显示出来。
        read [var]
            从用户读取一行输入。如果给定环境变量"var"，
            则把它设为所读取的行(不包括结尾的换行符)。
        reboot
            重新启动
        rmmod module
            卸载"module"模块
        search
            search [--file|--label|--fs-uuid] [--set [var]] [--no-floppy] name
            通过文件[--file]、卷标[--label]、文件系统UUID[--fs-uuid]来查找设备。
            如果使用了 --set 选项，那么会将第一个找到的设备设置为环境变量"var"的值。
            默认的"var"是'root'。
            可以使用 --no-floppy 选项来禁止查找软盘设备，因为这些设备非常慢。
        set [envvar=value]
            将环境变量"envvar"的值设为'value'。
            如果没有使用参数，则打印出所有环境变量及其值。
        source file
            直接将"file"文件的内容插入到当前位置。
            与"configfile"不同，此命令既不切换执行环境，也不会显示一个新的菜单。
        test expression [ expression ]
            计算"expression"的值，并在结果为真时返回零值，
            或者在结果为假时返回非零值，主要用在if/while之类的控制构造中。
            可用的"expression"模式如下(与bash类似)：
                string1 == string2  [string1与string2完全相同]
                string1 != string2  [string1与string2不完全相同]
                string1 < string2  [string1在字母顺序上小于string2]
                string1 <= string2  
                    [string1在字母顺序上小于string2或与string2完全相同]
                string1 > string2  
                    [string1在字母顺序上大于string2]
                string1 >= string2  
                    [string1在字母顺序上大于string2或与string2完全相同]
                integer1 -eq integer2  [integer1等于integer2]
                integer1 -ge integer2  [integer1大于或等于integer2]
                integer1 -gt integer2  [integer1大于integer2]
                integer1 -le integer2  [integer1小于或等于integer2]
                integer1 -lt integer2  [integer1小于integer2]
                integer1 -ne integer2  [integer1不等于integer2]
                prefixinteger1 -pgt prefixinteger2  
                    [剔除非数字字符首部之后，integer1大于integer2]
                prefixinteger1 -plt prefixinteger2  
                    [剔除非数字字符首部之后，integer1小于integer2]
                file1 -nt file2  [file1的修改时间比file2新]
                file1 -ot file2  [file1的修改时间比file2旧]
                -d file  [file存在并且是一个目录]
                -e file  [file存在]
                -f file  [file存在并且不是一个目录]
                -s file  [file存在并且文件尺寸大于零]
                -n string  [string的长度大于零]
                string     [string的长度大于零]
                -z string  [string的长度等于零]
                ( expression )  将expression视为一个整体(分组)
                ! expression   非(NOT)
                expression1 -a expression2   与(AND)
                expression1 -o expression2   或(OR)
        true
            不做任何事，只返回一个成功的结果。
            主要用在if/while之类的控制构造中。
        unset envvar
            撤销环境变量"envvar"
        videoinfo [[WxH]xD]
            列出所有当前可用的视频模式。
            如果指定了分辨率(或者还附加了色深)，那么仅显示与其匹配的模式。            
/etc/default/grub
    控制grub-mkconfig的操作,里面是以键值对存在的选项，如果值有空格或者其他字符需要用引号引起来
    此文件包含menu.list的前半部分内容，以及每行内核配置后面追加的配置，在更新时会合并到grub.cfg中
    参数如下:
      GRUB_DEFAULT 
        默认的菜单选择项，值可以是数字，默认从0开始，值也可以是title后面的字符串，
        当值是‘saved’时有特殊含义：
        默认的菜单选则项会被保存在GRUB_SAVEDEFAULT中，下次启动时会从这个值启动。
        当值为saved是可以用grub-set-default和grub-reboot来设置默认启动项，
        grub-set-default直到下次修改前都有效，grub-reboot下次启动时生效
      GRUB_SAVEDEFAULT
        只有这个值是true，GRUB_DEFAULT是saved时才会起作用
      GRUB_TIMEOUT
        选择菜单的显示时间，默认是5，值是0表示不显示菜单选项，值是-1表示无限期的等待做出选择
      GRUB_HIDDEN_TIMEOUT
        grub2第一次执行时会寻找其他操作系统，如果没有检测到则会将菜单隐藏，
        如果有其他操作系统才会显示菜单，如果参数大于0，则会等待响应的秒数，
        但是不会显示菜单，可以按住shift显示菜单。
      GRUB_DISTRIBUTOR
        菜单中的描述名称，采用命令lsb_release判断，应该是红帽系列的，如果不是就归为Debian
      GRUB_CMDLINE_LINUX
        此行将追加到所有的linux 定义内核行的后面，不论是救援模式还是一般模式
      GRUB_CMDLINE_LINUX_DEFAULT
        次选项只会追加在一般模式后面，同上
      GRUB_TERMINAL=console
        启用console，默认注释状态
      GRUB_DISABLE_LINUX_UUID=true
        在grub中指定root时可以使用UUID，默认注释
      GRUB_GFXMODE=640x480
        图形化菜单的分辨率，默认注释
      GRUB_DISABLE_LINUX_RECOVERY=true
        禁止显示救援模式
/etc/grub.d/目录
    该目录下都是一些脚本文件
    update-grub命令执行时会读取此目录下的文件，并将配置合并至grub.cfg中，
    （注：在centOS7下没有找到update-grub命令）
    grub.cfg中的菜单顺序是由此目录中的文件顺序决定的，
    文件开头数字较小的会先执行，全英文名字的文件将会在最后执行，
    自定义选项在40_custom中定义，或者建立一个新文件，
    此目录下的文件必须有执行权限才会被update-grub读取，并把配置合并到grub.cfg中。     
grub vs grub2
    配置文件的名称改变了。
    在grub中，配置文件为grub.conf或menu.lst(grub.conf的一个软链接)，
    在grub2中改名为grub.cfg
    grub2使用img文件(boot.img/core.img/diskboot.img/kernel.img)，
    不再使用grub中的stage1、stage1.5和stage2
boot.img
    文件被写入到MBR中，因为MBR的大小是512字节，所以boot.img总是512字节大小
    但是写入到MBR的内容和boot.img的内容并不完全相同, 
    MBR的内容是boot.img经过转换后的内容；
    因为MBR中的内容除了包含code, 还有磁盘的分区信息
core.img
    diskboot.img 以及kernel.img , 在grub2-install的时候被结合成为core.img, 
    同时还会 把一些 模块的代码以及 ”加载模块的代码“ 也加入到core.img中.
    所以core.img 并不是grub rpm package的文件，而是grub安装时候生成的文件
    这个文件生成之后不能简单的存放到/boot分区，
    因为在系统启动的时候，运行到core 之前只有MBR中的512-64=448字节的代码，
    无法识别/boot分区, 所以 这个core.img 是需要 hard-code 到磁盘中的
mod文件
    grub2安装之后，会有很多的模块文件(.mod) 被copy 到/boot/grub2/i386-pc 下面，
    这些mod文件主要是提供给grub使用的，
    （内核所需要的模块文件，主要放置在/lib/modules目录下）
    比如normal.mod 文件如果丢失，那么grub 就无法正常完成引导过程
    再比如 我们遇到过grub的命令行模式下，需要的命令(例如reboot, boot 等)找不到，
    这是因为相应的mod 没有被grub加载
    此时，可以使用手动方式进行加载，然后就可以使用相应的命令了，
    手动加载grub mod文件的命令为： insmod  MODULE_FILE_PATH
/boot下的initramfs文件
    在2.6版本的linux内核中，都包含一个压缩过的cpio格式的打包文件。
    当内核启动时，会从这个打包文件中导出文件到内核的rootfs文件系统，
    然后内核检查rootfs中是否包含有init文件，
    如果有则执行它，作为PID为1的第一个进程。
    这个init进程负责启动系统后续的工作，
    包括定位、挂载“真正的”根文件系统设备（如果有的话）。
    如果内核没有在 rootfs中找到init文件，
    则内核会按以前版本的方式定位、挂载根分区，
    然后执行/sbin/init程序完成系统的后续初始化工作。
    这个压缩过的cpio格式的打包文件就是initramfs。
    编译2.6版本的linux内核时，编译系统总会创建initramfs，
    然后把它与编译好的内核连接在一起。
    内核源代码树中的usr目录就是专门用于构建内核中的initramfs的，
    其中的initramfs_data.cpio.gz文件就是initramfs。
    缺省情况下，initramfs是空的，X86架构下的文件大小是134个字节。
initrd
    initrd 字面上的意思就是"boot loader initialized RAM disk"，
    换言之，这是一块特殊的RAM disk，
    在载入Linux kernel 前，由boot loader予以初始化，
    启动过程会优先执行initrd的init程序，initrd完成阶段性目标后
initrd和initramfs的区别是什么
    initrd是init ram disk，initramfs是init ram file system，
    前者把内存模拟成磁盘，后者直接把内存模拟成文件系统
    ------------------------------------
    kernel启动init的两种方案
    第一种是，ramdisk，就是把一块内存（ram）当做磁盘（disk）去挂载，
    然后找到ram里的init进行执行。
    第二种是，ramfs，直接在ram上挂载文件系统，执行文件系统中的init。
    initrd（init ramdisk）就是ramdisk的实现，initramfs就是ramfs的实现
    ------------------------------------
    不要被文件名迷惑，kernel 2.6 以来都是 initramfs 了，
    只是很多还沿袭传统使用 initrd 的名字
    initrd 是2.4 及更早的用法（
    现在你能见到的 initrd 文件实际差不多都是 initramfs 了），
    运行过程大概是内核启动，执行一些 initrd 的内容
    ，加载模块啥的，然后交回控制权给内核，
    最后再切到用户态去运行用户态的启动流程。
    initramfs 的工作方式更加简单直接一些，
    启动的时候加载内核和 initramfs 到内存执行，
    内核初始化之后，切换到用户态执行 initramfs 的程序/脚本，
    加载需要的驱动模块、必要配置等，
    然后加载 rootfs 切换到真正的 rootfs 上去执行后续的 init 过程
    从格式看，老的 initrd 是一个压缩的内存文件系统，
    现在的 initramfs 是一个 gzip 压缩的 cpio 文件系统打包
    ------------------------------------
    https://www.cnblogs.com/mywolrd/archive/2009/02/06/1930704.html
    Linux 2.6 核心将一个小的 ram-based initial root filesystem(initramfs) 包进内核
    且若这个文件系统包含一个程序 init，核心会将它当作第一个程序执行
    此时，找寻其它文件系统并执行其它程序已不再是内核的问题，而是新程序的工作。
    ramdisk vs ramfs:
    ramdisk (如 initrd) 是 基于ram的块设备，
    这表明它是一块固定大小的内存，它可以被格式化及挂载，就像磁盘一样。
    这表明 ramdisk 的内容需先格式化并用特殊的工具(像是 mke2fs 及 losetup)做前置作业，
    而且如同所有的块设备，它需要文件系统驱动程序在执行时期解释数据。
    几年前，Linus Torvalds 有一个巧妙的想法：
    Linux 的缓存是否可以被挂载一个文件系统？
    只要保持文件在缓存中且不要将它们清除，直到它们被删除或系统重新启动？
    Linus 写了一小段程序将缓存包起来，称它为 ramfs，
    而其它的 kernel 开发者建立一个加强版本称为 tmpfs
    (它可以写数据到 swap，及限制挂载点的大小，所以在它消耗完所有可用的内存前它会填满)。
    initramfs 就是 tmpfs 的一个实例。   
/sbin/init
    在内核加载完毕，并完成硬件检测与驱动程序加载后，此时主机硬件已经准备完毕，
    内核会主动呼叫第一个进程，也就是 /sbin/init    