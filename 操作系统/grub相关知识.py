grub-install 
    ����ĵ��Բ��������ˣ�BootLoader���ˣ����뻻��grub��BootLoader��
    ��ʱ����ʹ��������߰�װgrub����
    grub-installֻ��һ���ű����ڲ�����ִ�й�������grub-mkimage��grub-setup
    �����Ҳ����ֱ�������������װgrub
    grub2-install �Ǹ�elf�ļ�
grub2-install
    grub2-install ������ʲô����:
    A. grub2-install ����ҿ��õ�module, Ĭ���ǲ��� /usr/lib/grub/i386-pc ���Ŀ¼��
       ��Щmodule �ᱻcopy ��/boot/grub2/i386-pc �£�
       ���grub����Щmodule ����Ĭ��·���£�
       ��ô�Ϳ���ͨ�� --directory  ������ָ��Module�Լ�image��·��, 
       ����Ĭ�ϵ��Ҳ�������Ҫ���ã�����һ�㶼��Ĭ�ϵ�·����
    B. grub2-install ��װgrub��ʱ��
       ��copy grub��Ҫ��module ��/boot ��������Ӧ·���£�
       �������޸�ģʽ��װgrub��ʱ�򣬿�����Ҫָ�� --boot-directory��
       ����Ҫ��װgrub��������device, Ҳ��Ҫָ��������� ��
    C. grub��װ��ʱ�򣬻�֧��һ�� --root-directory �Ĳ�����
       ����������ڡ�man grub2-install"�İ����ĵ��У�
       ���˶��������������ǣ� û��ָ��--boot-directory������£�
       --root-directory������ֵ�������� ��
       ��û��ָ��--boot-directory������ָ����--root-directory��
       ��ô����--root-directoryָ����Ŀ¼�´���boot ��Ŀ¼�� ��Ϊ--boot-directory ��ʹ��. 
       ���--root-directory ��ϵͳ����ʱ���root û���κι�ϵ.
    D. �����װgrub,
       ͨ������ϣ�����´���device map ��ϵ����ʱ������ò�����--recheck��ʵ�֣�
       ��������������ǣ�����б�Ҫ��ɾ�����ڵ�device map, Ȼ�󴴽�һ���µģ�
       �������ǰ�grub ��װ����һ���µ�device �Ͽ��ܾ���Ҫ��ô����
    E. ǿ�ƽ���grub�İ�װ�����㷢��������. ��ʱ������ò��� --force
    F. grub2-install ��ִ�е�ʱ�򣬻������������grub��ص����
       ��Щ����һ�㲻��Ҫ����. ����Ͳ�������.
grub-mkimage
    kernel.img��һЩģ�鶯̬�����core.img
grub-mkconfig
    ����grub-mkdevicemap��grub-probe����grub.cfg
grub2-mkconfig
    һ���÷���grub2-mkconfig -o /boot/grub2/grub.config
    ��ο�/etc/grub.d/��/etc/default/grub������grub.config�ļ�
    ��/boot/grub.d�µ�10_linux�ű��ļ���̽��/boot�µ��ں��ļ�
    /boot/grub2/grub.config : bios��ʹ���������
    /boot/efi/EFI/centos/grub.cfg : efi��ʹ���������
grub_probe
    �Ӹ������豸��̽���豸��Ϣ
grub_setup
    ��grub_install���ã���װgrub
grub-mkdevicemap  ?
    Ϊgrub�Զ������µ�device.map��
    grub-mkdevicemap������Դ���device.map�ļ���
    ��ִ��grub-installʱ���Զ�ִ�����Դ���ӳ���ϵ��
    ����ļ������ڣ�����ȡ/boot/grub/devicd.map����ļ���
    ���ӳ���ļ����ڣ���grub��ȡ������BIOS drives to OS drives
update-grub
    update-grub��Ҫ����ÿ�������ļ��и��º������µ�grub.cfg��
    ��ʵupdate-grub�ǵ���grub-mkconfig��
    ��ϵͳ�л���һ��update-grub2���������ǵ���update-grub
grub-set-default
    �������´ν���ϵͳʱ���ĸ��ں�ѡ���ȥ
grub2 
    grub2����ģ�黯����ƣ���Ҫ�����ļ���/boot/grub/grub.cfg
    ��������ļ���Ȩ����444����rootҲ�����޸ģ����ǿ���Ϊ֮�ģ�
    ��Ҫ�޸��ļ�Ȩ�ޣ�grub.cfg�����ݸ�����update-grub���������£�
    ��ʵ����ִ��grub-mkconfig -o /boot/grub/grub.cfg������
/boot/grub/grub.cfg��/boot/efi/EFI/centos/grub.cfg
    ���ļ���ֻ���Ĳ������ֶ��޸ģ�grub-mkconfig�ڴ�������������grub.cfg
    ��������ļ���ϵͳ����ʱ����ȡ�ģ��������ļ�ȱʧ����ô�ᵼ������ʧ��
    ��/etc/default/grub ����ļ���������Զ����grub������. 
    �������֮�󣬿����� grub2-mkconfig -o /boot/grub2/grub.cfg  
    ���Զ���ı��apply ��grub�������ļ���
/boot/grub2/grub.cfg
    https://blog.csdn.net/ctthuangcheng/article/details/56679683
    ��ע���ڽ���ѡ��ϵͳ�˵�ʱ����e�ɽ�����༭grubģʽ����c�ɽ���cmdģʽ
    grub.cfg�ű�֧�ֵı��������֣�
        ����ֻ�г����õ�һЩ������
        �������б���Բο�GRUB2�ֲ��е�"Special environment variables"����
        ?
            ��һ������ķ���ֵ�����ʾ�ɹ��������ʾʧ��[��bashһ��]��
            ��GRUB2�Զ����á���ֻ��ʹ�ô˱������������޸�����
        check_signatures
            �Ƿ��ڼ����ļ�ʱǿ����֤ǩ����������Ϊ'yes'��'no'
        chosen
            ��ǰ��ִ�еĲ˵�������
            (����"menuentry"����֮����ַ�������'--id'ѡ��Ĳ���)��
            ����'Windows 7'����GRUB2�Զ����á���
            ֻӦ��ʹ�ô˱���������Ӧ���޸�����
        cmdpath
            ��ǰ�����ص�"core.img"����Ŀ¼(����·��)��
            ���磺UEFI����������'(hd0,gpt1)/EFI/UBUNTU'��'(cd0)/EFI/BOOT'��
            BIOS����������'(hd0)'����GRUB2�Զ����á�
            ��ֻӦ��ʹ�ô˱���������Ӧ���޸�����
        debug
            ��Ϊ'all'ʱ��ʾ�����������[����ʾ������Ϣ,��������]
        default
            Ĭ��ѡ�еڼ����˵���(��'0'��ʼ����)
        fallback
            ���Ĭ�ϲ˵�������ʧ�ܣ�
            ��ô�������ڼ����˵���(��'0'��ʼ����)
        gfxmode
            ����"gfxterm"ģ����ʹ�õ���Ƶģʽ��
            ����ָ��һ���ɶ��Ż�ֺŷָ���ģʽ�Թ���һ���ԣ�
            ÿ��ģʽ�ĸ�ʽ�����ǣ�'auto'(�Զ����),'��x��','��x��xɫ��'֮һ��
            ����ֻ��ʹ��VBE��׼ָ����ģʽ
            [640x480,800x600,1024x768,1280x1024]x[16,24,32]��
            ������GRUB SHELL��ʹ��"videoinfo"�����г���ǰ���п���ģʽ��
            Ĭ��ֵ��'auto'��
        gfxpayload
            ����Linux�ں�����ʱ����Ƶģʽ��
            ����ָ��һ���ɶ��Ż�ֺŷָ���ģʽ�Թ���һ���ԣ�
            ÿ��ģʽ�ĸ�ʽ�����ǣ�'text'(��ͨ�ı�ģʽ,��������UEFIƽ̨),
            'keep'(�̳�"gfxmode"��ֵ),'auto'(�Զ����),'��x��','��x��xɫ��'֮һ��
            ����ֻ��ʹ��VBE��׼ָ����ģʽ[640x480,800x600,1024x768,1280x1024]x[16,24,32]��
            ��BIOSƽ̨�ϵ�Ĭ��ֵ��'text'����UEFIƽ̨�ϵ�Ĭ��ֵ��'auto'��
            ����������ȷ����Linux����̨�ķֱ���
            (Ҫ���ں˱���"CONFIG_FRAMEBUFFER_CONSOLE=y")��
            ���ߴ�����BIOSƽ̨��ʹ��ͼ�ο���̨
            (Ҫ���ں˱���"CONFIG_FRAMEBUFFER_CONSOLE=y")��
            ����Ҫ���ô˱�����
        gfxterm_font
            ����"gfxterm"ģ����ʹ�õ����壬Ĭ��ʹ�����п�������
        grub_cpu
            ��GRUB�����õ�CPU���͡�
            ���磺'i386', 'x86_64'����GRUB2�Զ����á�
            ��ֻӦ��ʹ�ô˱���������Ӧ���޸�����
        grub_platform
            ��GRUB�����õ�ƽ̨���͡����磺'pc', 'efi'��
            ��GRUB2�Զ����á���ֻӦ��ʹ�ô˱���������Ӧ���޸�����
        lang
            ����GRUB2�Ľ������ԣ��������"locale_dir"����һ��ʹ�á�
            ��������Ӧ��Ϊ'zh_CN'��
        locale_dir
            ���÷����ļ�(*.mo)��Ŀ¼��ͨ����'$prefix/locale'��
            ��δ��ȷ���ô�Ŀ¼�����ֹ���ʻ���
        pager
            �����Ϊ'1'����ôÿһ��������ͣ������ȴ��������롣
            ȱʡ��''����ʾ����ͣ��
        prefix
            ����·����ʽ��'/boot/grub'Ŀ¼λ��(Ҳ����GRUB2�İ�װĿ¼)��
            ����'(hd0,gpt1)/grub'��'(hd0,msdos2)/boot/grub'��
            ��ʼֵ��GRUB������ʱ����"grub-install"�ڰ�װʱ�ṩ����Ϣ�Զ����á�
            ��ֻӦ��ʹ�ô˱���������Ӧ���޸�����
        root
            ����"���豸"���κ�δָ���豸�����ļ�����Ϊλ�ڴ��豸��
            ��ʼֵ��GRUB������ʱ����"prefix"������ֵ�Զ����á�
            �ڴ��������£��㶼��Ҫ�޸�����
        superusers
            ����һ��"�����û�"(ʹ�ÿո�/����/�ֺŽ��зָ�)��
            �Կ�����ȫ��֤�Ĺ��ܡ�
        theme
            ���ò˵�������������ļ���λ�ã�
            ���磺"/boot/grub/themes/starfield/theme.txt"��
            ������ζ��ƽ�����(����ͼƬ/����/��ɫ/ͼ���)��ϸ�ڣ�
            ���Բο�GRUB2�ֲ��е�" Theme file format"���֡�
        timeout
            ������Ĭ�ϲ˵���ǰ���ȴ����������������
            Ĭ��ֵ��'5'�롣
            '0'��ʾֱ������Ĭ�ϲ˵���(����ʾ�˵�)��'-1'��ʾ��Զ�ȴ�
    grub.cfg�ű�֧�ֵ�����
        ����GRUB-2.0.2�汾��˵�����п��õ������д�Լ200��֮��
        ���������˵�����Բο�GRUB2�ֲ�
        �Σ�https://www.gnu.org/software/grub/manual/grub/grub.html
        �е�"The list of available commands"ҳ�����г��ļ�������ҳ��
        menuentry 
            menuentry "title" [--class=class ��] [--users=users] 
                              [--unrestricted]  [--hotkey=key] 
                              [--id=id] [arg ��] 
                              { command; �� }
            ����һ����Ϊ"title"�Ĳ˵��
            ���˲˵��ѡ��ʱ��GRUB����ѻ�������"chosen"��ֵ��Ϊ"id"
            (ʹ����[--id=id]ѡ��)��"title"(δʹ��[--id=id]ѡ��)��
            Ȼ��ִ�л������е������б�
            ����б������һ������ִ�гɹ��������Ѿ�������һ���ںˣ�
            ��ô��ִ��"boot"���
            ����ʹ�� --class ѡ��ָ���˵���������"��ʽ��"��
            ������ʹ��ָ����������ʽ��ʾ�˵��
            ����ʹ�� --users ѡ��ָ��ֻ�����ض����û����ʴ˲˵��
            ���û��ʹ�ô�ѡ����ʾ���������û����ʡ�
            ����ʹ�� --unrestricted ѡ��ָ�����������û����ʴ˲˵��
            ����ʹ�� --hotkey ѡ�����÷��ʴ˲˵�����ȼ�(��ݼ�)��
            "key"������һ����������ĸ��
            ����'backspace','tab','delete'֮һ��
            ����ʹ�� --id ѡ��Ϊ�˲˵�������һ��ȫ��Ψһ�ı�ʶ����
            "id"������ASCII��ĸ/����/�»�����ɣ��Ҳ��������ֿ�ͷ��
            [arg ��]�ǿ�ѡ�Ĳ����б�
            ����԰��������Ϊ�����в�����
            ʵ����"title"Ҳ�������в�����
            ֻ������������Ǹ�����������ѡ�
            ��Щ�����������ڻ������ڵ������б���ʹ�ã�
            "title"��Ӧ��"$1"��������Դ����ơ�
        terminal_input 
            terminal_input [--append|--remove] 
                           [terminal1] [terminal2] ��
            ��������κ�ѡ���������
            ���ʾ�г���ǰ����������նˣ�
            �Լ������������õ������նˡ�
            ����ʹ�� --append ѡ�ָ�����ն�
            ���뵽����������ն��б��У�
            �����б��е��ն˶�����������GRUB�ṩ���롣
            ����ʹ�� --remove ѡ�ָ�����ն�
            �Ӽ���������ն��б���ɾ����
            �����ʹ���κ�ѡ�����ָ����һ�������ն˲�����
            ���ʾ����ǰ����������ն�����Ϊ����ָ�����նˡ�
        terminal_output
            terminal_output [--append|--remove] 
                            [terminal1] [terminal2] ��
            ��������κ�ѡ������������ʾ�г���ǰ���������նˣ�
            �Լ������������õ�����նˡ�
            ����ʹ�� --append ѡ�ָ�����ն�
            ���뵽���������ն��б��У�
            �����б��е��ն˶������ܵ�GRUB�������
            ����ʹ�� --remove ѡ�ָ�����ն�
            �Ӽ��������ն��б���ɾ����
            �����ʹ���κ�ѡ�����ָ����һ�������ն˲�����
            ���ʾ����ǰ���������ն�����Ϊ����ָ�����նˡ�
        authenticate [userlist]
            ��鵱ǰ�û��Ƿ�λ��"userlist"�򻷾�����"superusers"�С�
            [ע��]�����������"superusers"��ֵΪ�գ����������'��'��
        background_color color
            ���õ�ǰ���������ն˵ı�����ɫ��
            "color"����ʹ��HTML������ɫ��ʾ��("#RRGGBB"��"#RGB")��
            [ע��]����ʹ��'gfxterm'��Ϊ����ն˵�ʱ�򣬲��ܸı䱳��ɫ��
        background_image
            background_image [[--mode 'stretch'|'normal'] file]
            ����ǰ���������ն˵ı���ͼƬ����Ϊ"file"�ļ���
            ����ʹ����"--mode 'normal'"ѡ�
            ����ͼƬ�����Զ�����������������Ļ��
            ��������κ�ѡ������������ʾɾ������ͼƬ��
            [ע��]����ʹ��'gfxterm'��Ϊ����ն˵�ʱ�򣬲��ܸı䱳��ͼƬ��
        boot
            �����Ѿ��������OS����ʽ��������
            ���������ڽ���ʽ�����е�ʱ�������Ҫ�ġ�
            ��һ���˵������ʱ�������ġ�
        cat [--dos] file
            ��ʾ�ļ�"file"�����ݡ����ʹ����"--dos"ѡ�
            ��ô"�س�/���з�"������ʾΪһ���򵥵Ļ��з���
            ���򣬻س���������ʾΪһ�����Ʒ�(<d>)��
        chainloader [--force] file
            ��ʽ����"file"�ļ���
            ͨ��ʹ�ô��̿��ʾ����������'+1'��ʾ��ǰ�������ĵ�һ��������
            ����ʹ�� --force ѡ��ǿ�������ļ������������Ƿ�����ȷ��ǩ����
            ͨ�����ڼ�����ȱ�ݵ�����������(���� SCO UnixWare 7.1)��
        configfile file
            ��"file"��Ϊ�����ļ����ء����"file"�ж����˲˵��
            ��ô������ʾһ���������ǵĲ˵���
            [ע��]"file"�ļ��Ի��������������κα�������ڴӴ��ļ����غ�ʧЧ��
        cpuid [-l]
            ���CPU���ԡ�����x86ϵͳ�Ͽ��á�
            ���ʹ���� -l ѡ���ô���CPU��64λ�򷵻��棬���򷵻ؼ١�
        drivemap 
            drivemap -l|-r|[-s] from_drive to_drive
            �����ʹ���κ�ѡ���ʾ��"from_drive"ӳ�䵽"to_drive"��
            ����Ҫ������ʽ����Windows֮��Ĳ���ϵͳ��
            ��Ϊ����ֻ�ܴӵ�һ��Ӳ��������
            ���ڷ����ԭ�򣬷�����׺�������ԣ�
            �������ð�ȫ�ؽ�"${root}"��Ϊ����ʹ�á�
            ����ʹ�� -s ѡ�ִ�з���ӳ�䣬Ҳ���ǽ������������̡�
            ���磺 drivemap -s (hd0) (hd1)
            ����ʹ�� -l ѡ��г���ǰ���е�ӳ�䡣
            ����ʹ�� -r ѡ���ӳ������ΪĬ��ֵ��
            Ҳ���ǳ������е�ǰ���е�ӳ�䡣
        echo [-n] [-e] string ��
            ��ʾ��Ҫ����ı�������(����ʹ���� -n ѡ��)��
            ����ж���ַ���������������ǣ����ÿո�ָ�ÿһ����
            ��bash��ϰ��һ����������˫������ʹ��"${var}"�����ñ�����ֵ��
            Ҳ����ʹ�� -e ѡ���Է�б��ת����Ľ���( \\ \a \r \n \t ...)��
        export envvar
            ������������"envvar"��
            ��ʹ�����ʹ��"configfile"��������������ļ��ɼ���
        false
            �����κ��£�ֻ����һ��ʧ�ܵĽ����
            ��Ҫ����if/while֮��Ŀ��ƹ����С�
        gettext string
            ��"string"����Ϊ��������"lang"ָ�������ԡ�
            MO��ʽ�ķ����ļ��ӻ�������"locale_dir"ָ����Ŀ¼���ء�
        halt [--no-apm]
            �رռ���������ָ���� --no-apm ѡ���ʾ��ִ��APM BIOS���á�
            ���򣬼����ʹ��APM�رա�
        help [pattern ��]
            ��ʾ�ڽ�����İ�����Ϣ��
            ���û��ָ��"pattern"����ô����ʾ���п�������ļ��������
            ���ָ����"pattern"��
            ��ô��ֻ��ʾ��������Щ"pattern"��ͷ���������ϸ������Ϣ��
        initrd[efi] file
            Ϊ��32λЭ��������Linux�ں�����һ��"initial ramdisk"��
            �����ڴ����Linux�����������ú��ʵĲ�����
            [ע��]�������������"linux"����֮��ʹ�á�
        initrd16 file
            Ϊ��16λЭ��������Linux�ں�����һ��"initial ramdisk"��
            �����ڴ����Linux�����������ú��ʵĲ�����
            [ע��]�������������"linux16"����֮��ʹ�á�
        insmod module
            ������Ϊ"module"��GRUB2ģ�顣
        linux[efi] file ��
            ʹ��32λ����Э���"file"����һ��Linux�ں�ӳ��
            ����������ַ���Ϊ�ں˵������в������ִ��롣
            [ע��]ʹ��32λ����Э����ζ��'vga='����ѡ���ʧЧ��
            �����ϣ����ȷ����һ���ض�����Ƶģʽ��
            ��ôӦ��ʹ��"gfxpayload"����������
            ��ȻGRUB�����Զ��ؼ��ĳЩ'vga='������
            �������Ƿ���Ϊ���ʵ�"gfxpayload"���ã����ǲ���������������
        linux16 file ��
            �Դ�ͳ��16λ����Э���"file"����һ��Linux�ں�ӳ��
            ����������ַ���Ϊ�ں˵������в������ִ��롣
            ��ͨ����������һЩ����Linux����Э������⹤��(����MEMDISK)��
            [ע��]ʹ�ô�ͳ��16λ����Э����ζ�ţ�
            (1)'vga='����ѡ����Ȼ��Ч��
            (2)����������64λ�ں�
            (Ҳ�����ں˱���Ҫ'CONFIG_IA32_EMULATION=y'����)��
        loadfont file ��
            ��ָ����"file"�������壬����ʹ���˾���·����
            ����"file"������Ϊ"$prefix/fonts/file.pf2"�ļ���
        loopback [-d] device file
            ��"file"�ļ�ӳ��Ϊ"device"�ػ��豸�����磺
            loopback loop0 /path/to/image
            ls (loop0)/
            ����ʹ�� -d ѡ�ɾ����ǰʹ�������������豸��
        ls [arg ��]
            �����ʹ�ò�������ô�г����ж�GRUB��֪���豸��
            ��������ǰ����������ڵ�һ���豸����
            ��ô�г����豸��Ŀ¼�µ������ļ���
            ����������Ծ���·��������Ŀ¼����ô�г����Ŀ¼�����ݡ�
        lsfonts
            �г��Ѿ����ص���������
        lsmod
            �г��Ѿ����ص�����ģ��
        normal [file]
            ������ͨģʽ������ʾGRUB�˵���
            [˵��]ֻҪ��ǰû�д��ھ�Ԯģʽ��
            ��ʵ���Ѿ�������ͨģʽ���ˣ�
            ����ͨ��������Ҫ��ȷʹ�ô����
            ����ͨģʽ�У�����ģ��[command.lst]�����ģ��[crypto.lst]
            �ᱻ�Զ���������(����ʹ��"insmod"����)��
            ���ҿ�ʹ��������GRUB�ű����ܡ�
            ��������ģ���������Ҫ��ȷʹ��"insmod"���������롣
            ���������"file"��������ô��������ļ��ж�������
            (Ҳ������Ϊ"grub.cfg"�����)��
            ���򽫴�"$prefix/grub.cfg"�ж�������(������ڵĻ�)��
            ��Ҳ�������Ϊ"file"��Ĭ��ֵ��'$prefix/grub.cfg'��
            ��������ͨģʽ��Ƕ�׵��ô�����Թ���һ��Ƕ�׵Ļ�����
            ����һ�㲻��ô��������ʹ��"configfile"�������ﵽ��Ŀ�ġ�
        normal_exit
            �˳���ǰ����ͨģʽ����������ͨģʽʵ������Ƕ����
            ��һ����ͨģʽ��Ļ����ͻ᷵�ص���Ԯģʽ��
        parttool partition commands
            �Է�������и����޸ġ�Ŀǰֻ��������MBR������(DOS������)��
            ����������GPT������Ŀǰ��֧�����������÷���
            (1)���û�ȥ�������ļ�����(����Windowsϵͳ������)��
            ���磺"parttool (hd0,msdos2) +boot"��ʾΪ(hd0,msdos2)
            �������ϼ����ǣ���"parttool (hd0,msdos2) -boot"���ʾ
            ȥ��(hd0,msdos2)�����ļ����ǡ�
            (2)���û�ȥ�����������ر��(����Windowsϵͳ������)��
            ���磺"parttool (hd0,msdos2) +hidden"��ʾΪ
            (hd0,msdos2)�����������ر�ǣ�
            ��"parttool (hd0,msdos2) -hidden"���ʾ
            ȥ��(hd0,msdos2)���������ر�ǡ�
            (3)���ķ��������͡���ֵ������0x00-0xFF��Χ�ڵ�ֵ��
            ��Ӧ��ʹ��'0xNN'��ʽ��ʮ����������
            ���磺"parttool (hd0,msdos2) type=0x83"
            ��ʾ��(hd0,msdos2)���������޸�Ϊ'0x83'(Linux����)��
        password user clear-password
            ����һ����Ϊuser���û�����ʹ�����Ŀ���'clear-password'��
            ������ʹ�ô����
        password_pbkdf2
            password_pbkdf2 user hashed-password
            ����һ����Ϊuser���û�����ʹ�ù�ϣ����'hashed-password'
            (ͨ��"grub-mkpasswd-pbkdf2"��������)��
            ���ǽ���ʹ�õ������Ϊ����ȫ�Ը��ߡ�
        probe 
            probe [--set var] --driver|--partmap|--fs|
                              --fs-uuid|--label device
            ��ȡ"device"�豸���ض���Ϣ��
            ���ʹ���� --set ѡ����ʾ����ȡ�Ľ��������"var"�����У�
            ������ȡ�Ľ��ֱ����ʾ������
        read [var]
            ���û���ȡһ�����롣���������������"var"��
            �������Ϊ����ȡ����(��������β�Ļ��з�)��
        reboot
            ��������
        rmmod module
            ж��"module"ģ��
        search
            search [--file|--label|--fs-uuid] [--set [var]] [--no-floppy] name
            ͨ���ļ�[--file]�����[--label]���ļ�ϵͳUUID[--fs-uuid]�������豸��
            ���ʹ���� --set ѡ���ô�Ὣ��һ���ҵ����豸����Ϊ��������"var"��ֵ��
            Ĭ�ϵ�"var"��'root'��
            ����ʹ�� --no-floppy ѡ������ֹ���������豸����Ϊ��Щ�豸�ǳ�����
        set [envvar=value]
            ����������"envvar"��ֵ��Ϊ'value'��
            ���û��ʹ�ò��������ӡ�����л�����������ֵ��
        source file
            ֱ�ӽ�"file"�ļ������ݲ��뵽��ǰλ�á�
            ��"configfile"��ͬ��������Ȳ��л�ִ�л�����Ҳ������ʾһ���µĲ˵���
        test expression [ expression ]
            ����"expression"��ֵ�����ڽ��Ϊ��ʱ������ֵ��
            �����ڽ��Ϊ��ʱ���ط���ֵ����Ҫ����if/while֮��Ŀ��ƹ����С�
            ���õ�"expression"ģʽ����(��bash����)��
                string1 == string2  [string1��string2��ȫ��ͬ]
                string1 != string2  [string1��string2����ȫ��ͬ]
                string1 < string2  [string1����ĸ˳����С��string2]
                string1 <= string2  
                    [string1����ĸ˳����С��string2����string2��ȫ��ͬ]
                string1 > string2  
                    [string1����ĸ˳���ϴ���string2]
                string1 >= string2  
                    [string1����ĸ˳���ϴ���string2����string2��ȫ��ͬ]
                integer1 -eq integer2  [integer1����integer2]
                integer1 -ge integer2  [integer1���ڻ����integer2]
                integer1 -gt integer2  [integer1����integer2]
                integer1 -le integer2  [integer1С�ڻ����integer2]
                integer1 -lt integer2  [integer1С��integer2]
                integer1 -ne integer2  [integer1������integer2]
                prefixinteger1 -pgt prefixinteger2  
                    [�޳��������ַ��ײ�֮��integer1����integer2]
                prefixinteger1 -plt prefixinteger2  
                    [�޳��������ַ��ײ�֮��integer1С��integer2]
                file1 -nt file2  [file1���޸�ʱ���file2��]
                file1 -ot file2  [file1���޸�ʱ���file2��]
                -d file  [file���ڲ�����һ��Ŀ¼]
                -e file  [file����]
                -f file  [file���ڲ��Ҳ���һ��Ŀ¼]
                -s file  [file���ڲ����ļ��ߴ������]
                -n string  [string�ĳ��ȴ�����]
                string     [string�ĳ��ȴ�����]
                -z string  [string�ĳ��ȵ�����]
                ( expression )  ��expression��Ϊһ������(����)
                ! expression   ��(NOT)
                expression1 -a expression2   ��(AND)
                expression1 -o expression2   ��(OR)
        true
            �����κ��£�ֻ����һ���ɹ��Ľ����
            ��Ҫ����if/while֮��Ŀ��ƹ����С�
        unset envvar
            ������������"envvar"
        videoinfo [[WxH]xD]
            �г����е�ǰ���õ���Ƶģʽ��
            ���ָ���˷ֱ���(���߻�������ɫ��)����ô����ʾ����ƥ���ģʽ��            
/etc/default/grub
    ����grub-mkconfig�Ĳ���,�������Լ�ֵ�Դ��ڵ�ѡ����ֵ�пո���������ַ���Ҫ������������
    ���ļ�����menu.list��ǰ�벿�����ݣ��Լ�ÿ���ں����ú���׷�ӵ����ã��ڸ���ʱ��ϲ���grub.cfg��
    ��������:
      GRUB_DEFAULT 
        Ĭ�ϵĲ˵�ѡ���ֵ���������֣�Ĭ�ϴ�0��ʼ��ֵҲ������title������ַ�����
        ��ֵ�ǡ�saved��ʱ�����⺬�壺
        Ĭ�ϵĲ˵�ѡ����ᱻ������GRUB_SAVEDEFAULT�У��´�����ʱ������ֵ������
        ��ֵΪsaved�ǿ�����grub-set-default��grub-reboot������Ĭ�������
        grub-set-defaultֱ���´��޸�ǰ����Ч��grub-reboot�´�����ʱ��Ч
      GRUB_SAVEDEFAULT
        ֻ�����ֵ��true��GRUB_DEFAULT��savedʱ�Ż�������
      GRUB_TIMEOUT
        ѡ��˵�����ʾʱ�䣬Ĭ����5��ֵ��0��ʾ����ʾ�˵�ѡ�ֵ��-1��ʾ�����ڵĵȴ�����ѡ��
      GRUB_HIDDEN_TIMEOUT
        grub2��һ��ִ��ʱ��Ѱ����������ϵͳ�����û�м�⵽��Ὣ�˵����أ�
        �������������ϵͳ�Ż���ʾ�˵��������������0�����ȴ���Ӧ��������
        ���ǲ�����ʾ�˵������԰�סshift��ʾ�˵���
      GRUB_DISTRIBUTOR
        �˵��е��������ƣ���������lsb_release�жϣ�Ӧ���Ǻ�ñϵ�еģ�������Ǿ͹�ΪDebian
      GRUB_CMDLINE_LINUX
        ���н�׷�ӵ����е�linux �����ں��еĺ��棬�����Ǿ�Ԯģʽ����һ��ģʽ
      GRUB_CMDLINE_LINUX_DEFAULT
        ��ѡ��ֻ��׷����һ��ģʽ���棬ͬ��
      GRUB_TERMINAL=console
        ����console��Ĭ��ע��״̬
      GRUB_DISABLE_LINUX_UUID=true
        ��grub��ָ��rootʱ����ʹ��UUID��Ĭ��ע��
      GRUB_GFXMODE=640x480
        ͼ�λ��˵��ķֱ��ʣ�Ĭ��ע��
      GRUB_DISABLE_LINUX_RECOVERY=true
        ��ֹ��ʾ��Ԯģʽ
/etc/grub.d/Ŀ¼
    ��Ŀ¼�¶���һЩ�ű��ļ�
    update-grub����ִ��ʱ���ȡ��Ŀ¼�µ��ļ����������úϲ���grub.cfg�У�
    ��ע����centOS7��û���ҵ�update-grub���
    grub.cfg�еĲ˵�˳�����ɴ�Ŀ¼�е��ļ�˳������ģ�
    �ļ���ͷ���ֽ�С�Ļ���ִ�У�ȫӢ�����ֵ��ļ����������ִ�У�
    �Զ���ѡ����40_custom�ж��壬���߽���һ�����ļ���
    ��Ŀ¼�µ��ļ�������ִ��Ȩ�޲Żᱻupdate-grub��ȡ���������úϲ���grub.cfg�С�     
grub vs grub2
    �����ļ������Ƹı��ˡ�
    ��grub�У������ļ�Ϊgrub.conf��menu.lst(grub.conf��һ��������)��
    ��grub2�и���Ϊgrub.cfg
    grub2ʹ��img�ļ�(boot.img/core.img/diskboot.img/kernel.img)��
    ����ʹ��grub�е�stage1��stage1.5��stage2
boot.img
    �ļ���д�뵽MBR�У���ΪMBR�Ĵ�С��512�ֽڣ�����boot.img����512�ֽڴ�С
    ����д�뵽MBR�����ݺ�boot.img�����ݲ�����ȫ��ͬ, 
    MBR��������boot.img����ת��������ݣ�
    ��ΪMBR�е����ݳ��˰���code, ���д��̵ķ�����Ϣ
core.img
    diskboot.img �Լ�kernel.img , ��grub2-install��ʱ�򱻽�ϳ�Ϊcore.img, 
    ͬʱ���� ��һЩ ģ��Ĵ����Լ� ������ģ��Ĵ��롰 Ҳ���뵽core.img��.
    ����core.img ������grub rpm package���ļ�������grub��װʱ�����ɵ��ļ�
    ����ļ�����֮���ܼ򵥵Ĵ�ŵ�/boot������
    ��Ϊ��ϵͳ������ʱ�����е�core ֮ǰֻ��MBR�е�512-64=448�ֽڵĴ��룬
    �޷�ʶ��/boot����, ���� ���core.img ����Ҫ hard-code �������е�
mod�ļ�
    grub2��װ֮�󣬻��кܶ��ģ���ļ�(.mod) ��copy ��/boot/grub2/i386-pc ���棬
    ��Щmod�ļ���Ҫ���ṩ��grubʹ�õģ�
    ���ں�����Ҫ��ģ���ļ�����Ҫ������/lib/modulesĿ¼�£�
    ����normal.mod �ļ������ʧ����ôgrub ���޷����������������
    �ٱ��� ����������grub��������ģʽ�£���Ҫ������(����reboot, boot ��)�Ҳ�����
    ������Ϊ��Ӧ��mod û�б�grub����
    ��ʱ������ʹ���ֶ���ʽ���м��أ�Ȼ��Ϳ���ʹ����Ӧ�������ˣ�
    �ֶ�����grub mod�ļ�������Ϊ�� insmod  MODULE_FILE_PATH
/boot�µ�initramfs�ļ�
    ��2.6�汾��linux�ں��У�������һ��ѹ������cpio��ʽ�Ĵ���ļ���
    ���ں�����ʱ������������ļ��е����ļ����ں˵�rootfs�ļ�ϵͳ��
    Ȼ���ں˼��rootfs���Ƿ������init�ļ���
    �������ִ��������ΪPIDΪ1�ĵ�һ�����̡�
    ���init���̸�������ϵͳ�����Ĺ�����
    ������λ�����ء������ġ����ļ�ϵͳ�豸������еĻ�����
    ����ں�û���� rootfs���ҵ�init�ļ���
    ���ں˻ᰴ��ǰ�汾�ķ�ʽ��λ�����ظ�������
    Ȼ��ִ��/sbin/init�������ϵͳ�ĺ�����ʼ��������
    ���ѹ������cpio��ʽ�Ĵ���ļ�����initramfs��
    ����2.6�汾��linux�ں�ʱ������ϵͳ�ܻᴴ��initramfs��
    Ȼ����������õ��ں�������һ��
    �ں�Դ�������е�usrĿ¼����ר�����ڹ����ں��е�initramfs�ģ�
    ���е�initramfs_data.cpio.gz�ļ�����initramfs��
    ȱʡ����£�initramfs�ǿյģ�X86�ܹ��µ��ļ���С��134���ֽڡ�
initrd
    initrd �����ϵ���˼����"boot loader initialized RAM disk"��
    ����֮������һ�������RAM disk��
    ������Linux kernel ǰ����boot loader���Գ�ʼ����
    �������̻�����ִ��initrd��init����initrd��ɽ׶���Ŀ���
initrd��initramfs��������ʲô
    initrd��init ram disk��initramfs��init ram file system��
    ǰ�߰��ڴ�ģ��ɴ��̣�����ֱ�Ӱ��ڴ�ģ����ļ�ϵͳ
    ------------------------------------
    kernel����init�����ַ���
    ��һ���ǣ�ramdisk�����ǰ�һ���ڴ棨ram���������̣�disk��ȥ���أ�
    Ȼ���ҵ�ram���init����ִ�С�
    �ڶ����ǣ�ramfs��ֱ����ram�Ϲ����ļ�ϵͳ��ִ���ļ�ϵͳ�е�init��
    initrd��init ramdisk������ramdisk��ʵ�֣�initramfs����ramfs��ʵ��
    ------------------------------------
    ��Ҫ���ļ����Ի�kernel 2.6 �������� initramfs �ˣ�
    ֻ�Ǻܶ໹��Ϯ��ͳʹ�� initrd ������
    initrd ��2.4 ��������÷���
    �������ܼ����� initrd �ļ�ʵ�ʲ�඼�� initramfs �ˣ���
    ���й��̴�����ں�������ִ��һЩ initrd ������
    ������ģ��ɶ�ģ�Ȼ�󽻻ؿ���Ȩ���ںˣ�
    ������е��û�̬ȥ�����û�̬���������̡�
    initramfs �Ĺ�����ʽ���Ӽ�ֱ��һЩ��
    ������ʱ������ں˺� initramfs ���ڴ�ִ�У�
    �ں˳�ʼ��֮���л����û�ִ̬�� initramfs �ĳ���/�ű���
    ������Ҫ������ģ�顢��Ҫ���õȣ�
    Ȼ����� rootfs �л��������� rootfs ��ȥִ�к����� init ����
    �Ӹ�ʽ�����ϵ� initrd ��һ��ѹ�����ڴ��ļ�ϵͳ��
    ���ڵ� initramfs ��һ�� gzip ѹ���� cpio �ļ�ϵͳ���
    ------------------------------------
    https://www.cnblogs.com/mywolrd/archive/2009/02/06/1930704.html
    Linux 2.6 ���Ľ�һ��С�� ram-based initial root filesystem(initramfs) �����ں�
    ��������ļ�ϵͳ����һ������ init�����ĻὫ��������һ������ִ��
    ��ʱ����Ѱ�����ļ�ϵͳ��ִ�����������Ѳ������ں˵����⣬�����³���Ĺ�����
    ramdisk vs ramfs:
    ramdisk (�� initrd) �� ����ram�Ŀ��豸��
    ���������һ��̶���С���ڴ棬�����Ա���ʽ�������أ��������һ����
    ����� ramdisk ���������ȸ�ʽ����������Ĺ���(���� mke2fs �� losetup)��ǰ����ҵ��
    ������ͬ���еĿ��豸������Ҫ�ļ�ϵͳ����������ִ��ʱ�ڽ������ݡ�
    ����ǰ��Linus Torvalds ��һ��������뷨��
    Linux �Ļ����Ƿ���Ա�����һ���ļ�ϵͳ��
    ֻҪ�����ļ��ڻ������Ҳ�Ҫ�����������ֱ�����Ǳ�ɾ����ϵͳ����������
    Linus д��һС�γ��򽫻��������������Ϊ ramfs��
    �������� kernel �����߽���һ����ǿ�汾��Ϊ tmpfs
    (������д���ݵ� swap�������ƹ��ص�Ĵ�С�������������������п��õ��ڴ�ǰ��������)��
    initramfs ���� tmpfs ��һ��ʵ����   
/sbin/init
    ���ں˼�����ϣ������Ӳ�����������������غ󣬴�ʱ����Ӳ���Ѿ�׼����ϣ�
    �ں˻��������е�һ�����̣�Ҳ���� /sbin/init    