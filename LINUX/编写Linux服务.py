<catalog s0/s4/s8 catalog_line_prefix=+>
+Linuxע���������ַ�ʽ
    һ����init.d����ʽ��һ��systemd����ʽ
    1. /etc/init.d����Ӧ�ķ����������Ϊ �� service ������ start
    2. systemd ��Ӧ�ķ����������Ϊ : systemctl start ������
       �ű�λ��/etc/systemd/system�������Ӧ�Ĵ�ΪһЩ.services�ļ�
       
    ���ڵ�1�з�ʽ��Linux��chkconfigʱ����ʹ��һ��perl�ű�(/sbin/insserv)�����ű���ʽ�Ƿ�淶

    ��ñ6����������Ϊ �� �����Լ�BIOS -> MBR���� -> GRUB�˵� -> �����ں� -> init���̳�ʼ��
    ��ñ7����������Ϊ �� �����Լ�BIOS -> MBR���� -> GRUB2�˵� -> �����ں� -> systemd���̳�ʼ��

    +systemd�ǶԴ�ͳsysvinit�ĸĽ�
        systemd ����������Ľ� sysvinit ��ȱ�㣬����ubuntu��upstart�Ǿ������֣�Ԥ�ƻ�ȡ������
        systemd��Ŀ���ǣ��������������ٽ��̣������ܽ�������̲���������
        systemd�����ܼ��ٶ�shell�ű���������
        ��ͳsysvinitʹ��inittab������������Щshell�ű�������ʹ��shell�ű�����Ϊ��Ч�ʵ����޷����е�ԭ��

    +init��Systemd������
        init�� 
            һ������ʱ�䳤��init�Ǵ���������ֻ��ǰһ�����������꣬�Ż�������һ������
            ���������ű����ӣ�Init����ֻ��ִ�������ű��������������飬�ű���Ҫ�Լ�������������������ʹ�ýű���úܳ�
            ��Linux�ں˼������У�λ�� /sbin/init   ,��ϵͳ�е�һ�����̣�PID��ԶΪ1
        systemd��
            �����������񣬼���ϵͳ��Դ���ġ�
            �����ܲ����������̣�����ϵͳ�����ȴ�ʱ��
            ��Linx�ں˼������У�λ�� /usr/lib/systemd/systemd  ����ϵͳ�е�һ�����̣�PID��ԶΪ1
            ����Ubuntu16/Ubuntu20/UOS�����ֵ�һ�������̶���/sbin/init����Ҳ��������systemd����
            ����centos�����Է��ֵ�һ����������systemd
    
    +systemd Ϊʲô������ô�������
        https://www.zhihu.com/question/25873473
            ������������, Ƶ�������ƺͽӿڡ�systemd���¹��ܣ���ö��ȼ����汾����
            ������������
            ������
        
    +Rhel6 vs Rhel7 �������
        Rhel6 �� service �� chkconfig ������������� SystemV �ܹ��µ�һ�����ߡ�
        Rhel7 ���� systemctl  ������������ں���֮ǰ�� service �� chkconfig �Ĺ�����һ�壨Ubuntu16��Ҳ�иù��ߣ�
        ����                  Rhel6 ��ָ��                          Rhel7��ָ��
        ����ĳ����            service  httpd   start                systemctl  start   httpd
        ֹͣĳ����            service  httpd   stop                 systemctl  stop   httpd
        ʹ���񿪻�������      chkconfig  --level   5  httpd   on    systemctl  enable  httpd
        ʹ���񿪻���������    chkconfig  --level   5  httpd   off   systemctl  disable  httpd
        ����ĳ����            service  httpd   restart              systemctl  restart  httpd
        ������״̬          service  httpd  status                systemctl  status  httpd
        ��ʾ�����������ķ���  chkconfig  --list                     systemctl  list-unit-files | grep enabled
        �����Զ������        chkconfig  --add  test                systemctl  load  test
        ɾ��ĳ����            chkconfig  --del  httpd               ͣ��Ӧ�ã�ɾ���������ļ�
        ��ѯ�����Ƿ񿪻�����  chkconfig  --list | grep httpd        systemctl  is-enabled   httpd
        �鿴����ʧ�ܵķ���    ��                                    systemctl  --failed

        ����������øó��򿪻����������ǿ���ִ������ systemctl enable ������
        ��������൱���� /etc/systemd/system/multi-user.target.wants Ŀ¼���һ�������ӣ�
        ָ�� /usr/lib/systemd/system Ŀ¼�µ� httpd.service �ļ���
        ������Ϊ����ʱ��Systemdִֻ�� /etc/systemd/system/multi-user.target.wants Ŀ¼����������ļ�

        systemd��һЩ�������
        �г����п��õ�Ԫ ��  systemctl list-unit-files
        �г��������еĵ�Ԫ�� systemctl list-unit-files | grep enabled 
        �г����п��÷���   systemctl list-unit-files  --type=service
        �г��������еķ��� systemctl list-unit-files  --type=service | grep enabled 
        ����httpd����      systemctl mask httpd

======================================================================  

+�ɵķ���ʽ

    +����������������ģ�
        �Σ�https://www.jianshu.com/p/5af068656d4b

        1. ����ű����Ƿ��� /etc/init.d Ŀ¼�µ�

        2. ��Щ�ű�����α��Զ�ִ�еģ�
           �� /etc�£��� rc0~6.d��rcS.dĿ¼
           ����ЩĿ¼���г����ӣ�ָ�� /etc/init �µĽű��ļ�
           �ű��ļ���������ʽ�� "K/S 2λ������ �Զ�������"
           K : kill , �Զ�����ָ��Ľű�����Я�� stop ����
           S ��start ���Զ�����ָ��Ľű�����Я�� start ����
           �Զ�ִ��ʱ���Ȱ�����˳��ִ�����е� K ��ͷ�Ľű�
           �ٰ�����˳��ִ�����е� S ��ͷ�Ľű�
           
        3. rc0~6.d��rcS.dĿ¼������
           /etc/rcS.d/ #��������Ҫ�Զ�������һЩ��������
           /etc/rc0.d/ #����ģʽ0����Ҫ�����ķ���
           /etc/rc1.d/ #����ģʽ1����Ҫ�����ķ���
           /etc/rc2.d/ #����ģʽ2����Ҫ�����ķ���
           /etc/rc3.d/ #����ģʽ3����Ҫ�����ķ���
           /etc/rc4.d/ #����ģʽ4����Ҫ�����ķ���
           /etc/rc5.d/ #����ģʽ5����Ҫ�����ķ���
           /etc/rc6.d/ #����ģʽ6����Ҫ�����ķ���

        4. /etc/rc.local  
           ���Ǹ��ű��ļ�����ϵͳ��ʼ������Ľű�����֮����ִ��
   
    ======================================================================  

    +/etc/init Ŀ¼�µĽű���ʽ������

       #! /bin/bash
       ### BEGIN INIT INFO
       #
       # Provides:	 location_server
       # Required-Start:	$local_fs  $remote_fs
       # Required-Stop:	$local_fs  $remote_fs
       # Default-Start: 	2 3 4 5
       # Default-Stop: 	0 1 6
       # Short-Description:	initscript
       # Description: 	This file should be used to construct scripts to be placed in /etc/init.d.
       #
       ### END INIT INFO
     
       case "$1" in
          start)
            ;;
          restart)
            ;;
          stop)
            ;;
          status)
            ;;
          reload)
            ;;
          force-reload)
            ;;
          *)
            ;;
       esac        
       
       ע�� 
          ### BEGIN INIT INFO �α�����ڣ��������ע�����ʱ����
          ע�����ʱ��������ⲿ�ֵ���Ϣ����������ļ�
          Required-Start ָ���ڷ�������ǰ����Щ����Ӧ�ñ���ǰ׼����
          ϵͳ����ʱ��������Щ��������֯�����������˳��
          $local_fs���������ļ�ϵͳӦ�ñ�׼����
          Required-Stop��ָ��Ӧ������Щ����(ֹͣ)֮ǰֹͣ
          Default-Start��Default-Stop��Ӱ����/etc/rc0~6.d��ЩĿ¼�´���ʲô����

    ======================================================================

    +LSB��ʼ���ű�
        ����� ### BEGIN INIT INFO �Σ�����LSB��ʼ���ű�
        Debian �� 2015 ��ֹͣ�˶� LSB ��֧��
        ���� LSB ��׼�ĳ�ʼ���ű���Ҫ��
            �����ṩ���²�����������ֹͣ������������ǿ�����¼��غ�״̬
            ������ȷ���˳�״̬���롣
            �ĵ�����ʱ������
            [��ѡ]ʹ�� Init.d ������¼��Ϣ��log_success_msg��log_failure_msg��log_warning_msg
        ֧�ֵĹؼ���
            Provides
                ָ���÷�������ƣ���������ű�����������������Դ�����Ϊ����
            Required-Start
                ָ����Ҫ�ڴ˷���֮ǰ��׼���õķ���
            Required-Stop
                ָ����Ҫ�ڴ˷���ص�֮ǰ���ȹص��ķ���һ����Required-Start����ָ���ķ���һ��
            Should-Start
                �����Щ������ڣ���Ӧ�ڱ�����ű�֮ǰ����������Щ���񲻴��ڣ�Ҳ��Ӱ�쵱ǰ����Ŀ���
            Should-Stop
                ͬ�ϣ������Щ������ڣ���Ӧ�����ڱ�����ر�
            Default-Start
                Ӱ���� /etc/rc0~6.d ��ЩĿ¼�´��� S ��ͷ������
            Default-Stop
                Ӱ���� /etc/rc0~6.d ��ЩĿ¼�´��� K ��ͷ������
            Short-Description
                �Խű��ļ�������ֻ��ռһ��
            Description
                �Խű���Ϊ����ϸ��������ռ���У�ÿ������Ӧ���� # ��ͷ,�� # ����������ո��һ��tab
            X-Interactive: true
                �����ó�ʼ���ű��������û�����������Ҫ�û����룩����ȷ���˽ű���ʹ��tty������
        һЩ�������������
            $local_fs ���й��صı����ļ�ϵͳ
            $network  �����������
            $named ����ת������DNS��NIS+��LDAP
            $portmap ?SunRPC/ONCRPC�˿�ӳ�����
            $remote_fs  ���й��ص�Զ���ļ�ϵͳ
            $syslog  ϵͳ��־
            $time ϵͳʱ��������ú�
            $all  ��������Щ��Required-Start����û��ָ��$all�ķ���

    ====================================================================== 

    +���ű�ע��ɷ���
        RedHatϵ�Ĳ���ϵͳ�Դ� chkconfig ���ߣ����Խ�����Ľű�ע��ɷ���
            ʹ�÷����Σ�https://www.runoob.com/linux/linux-comm-chkconfig.html
                ����Red Hat��˾��ѭGPL�����������ĳ���
                ���ɲ�ѯ����ϵͳ��ÿһ��ִ�еȼ��л�ִ����Щϵͳ�������а������ೣפ����
                chkconfig [--add][--del][--list][ϵͳ����] �� 
                chkconfig [--level <�ȼ�����>][ϵͳ����][on/off/reset]
                --add     ������ָ����ϵͳ������ chkconfig ָ����Թ���������ͬʱ��ϵͳ�����������ļ�������������ݡ�
                --del     ɾ����ָ����ϵͳ���񣬲����� chkconfig ָ�������ͬʱ��ϵͳ�����������ļ���ɾ��������ݡ�
                --level<�ȼ�����>     ָ����ϵͳ����Ҫ����һ��ִ�еȼ��п�����رϡ�
            ʹ�÷����Σ�https://www.cnblogs.com/tianyiwuying/p/7519632.html
        Debianϵ�Ĳ���ϵͳ��֮��Ӧ���� update-rc.d
            �Σ�https://blog.csdn.net/weixin_34041003/article/details/93055408
            ���ɾ������
                ��ӣ� sudo update-rc.d ������ defaults
                ɾ���� sudo update-rc.d -f ������ remove
            ע�����󣬻�������λ���Զ���������ļ���
                /etc/init.d/ (ԭ��)
                /etc/rc0~6.d/ (��ָ��/etc/init.d����Ӧ�ļ�������)
                /run/systemd/generator.late/graphical.target.wants/
                /run/systemd/generator.late/multi-user.target.wants/
                /run/systemd/generator.late/
                ��������generator.lateĿ¼�´�����.service�ļ�����һ��
                ��service�ļ�Ҳ�ǵ���/etc/init.d�µ���Ӧ�ű���������start/stop����
        Debian��Ҳ����װchkconfig����
            �Σ�https://blog.csdn.net/wildwolf_001/article/details/115250102
        
    ======================================================================

    +����/ͣ�÷���   
        ��ʷ�汾�е�linux�Է���Ĳ�����ͨ��service����ɵġ�
        �������û��Զ���ķ�������Ҫ��Ϊ���ӵĲ�����
        Ŀǰlinux�µķ��а��Ѿ�������systemctl����������
        man service ���Է��֣���ʵ����ȥ /ect/init.d ������Ӧ�ű����е���
        �����ԣ�������ע��󣬲���ͨ��service����
        
======================================================================

+�µķ���ʽ

    +service�ű���д��ʽ��/lib/systemd/system��
        �Σ�https://www.jianshu.com/p/92208194d700
        �Σ�https://www.cnblogs.com/mafeng/p/10316351.html
        �Σ�https://www.cnblogs.com/virgosnail/p/12675880.html
        �Σ�https://blog.csdn.net/weixin_57400332/article/details/123627742

        �ű���Ϊ3�����֣�[Unit] [Service] [Install]
        Unit  ��������Ϣ����������ǰ����ļ�����
            Description������������Ϣ��
            Documentation���ĵ������Ϣ��
            �����ĸ�ѡ��ֻ�漰����˳�򣬲��漰������ϵ��
            After������sshd����Ӧ������Щ����֮��������
            Before������sshd����Ӧ������Щ����֮ǰ������
            Requires����ʾǿ������ϵ�����sshd��������ʧ�ܻ��쳣�˳�����Requires���õķ���Ҳ�����˳���
            Wants����ʾ��������ϵ�����sshd��������ʧ�ܻ��쳣�˳�����Ӱ��Wants���õķ���
        Service   �����鶨�����������ǰ����
            Service�ǽű��Ĺؼ�����
            Type=forking : ��̨����ģʽ
            PIDFile=/xxx/xxx.xxx : ���PID�ļ���λ��
            ExecStart=/bin/echo xxx : ���Ƿ������еľ���ִ������
            ExecReload=/bin/echo xxx �� ���Ƿ���������ִ������
            EexcStop=/bin/echo xxx : ���Ƿ���ֹͣ��ִ������
            һЩ�ڵ�Ľ��ܣ�
                Type��
                    ��Service���У�������ʽʹ��Typeָ����������Բο�man systemd.service��
                    Type�����¼��ֿ�ѡ�simple��forking��oneshot��dbus��notify��idel
                    simple
                        ����Ĭ�ϵ�Type����Type��BusName���ö�û�����ã�ָ����ExecStart���ú�simple����Ĭ�ϵ�Type���á�
                        simpleʹ��ExecStart�����Ľ�����Ϊ����������̡��ڴ�������systemd��������������
                        ����÷���Ҫ������������simple����forking����
                        ���ǵ�ͨѶ����Ӧ�����ػ���������֮ǰ����װ�ã�e.g. sockets,ͨ��sockets�����
                    forking
                        ���ʹ�������Type����ExecStart�Ľű�����������fork()��������һ��������Ϊ��������һ���֡�
                        ��һ�г�ʼ����Ϻ󣬸����̻��˳����ӽ��̻������Ϊ������ִ�С�
                        ���Ǵ�ͳUNIX�����̵���Ϊ�����������ñ�ָ����
                        ����ͬʱ����PIDFileѡ����ָ��pid�ļ���·�����Ա�systemd�ܹ�ʶ�������̡�
                    oneshot
                        onesh����Ϊʮ������simple�����ǣ���systemd����֮ǰ�����̾ͻ��˳���
                        ����һ���Ե���Ϊ�����ܻ���Ҫ����RemainAfterExit=yes���Ա�systemd��Ϊj�����˳�����Ȼ���ڼ���״̬��
                    dbus
                        �������Ҳ��simple�����ƣ��������ڴ�������һ��nameֵ��ͨ������BusName=����name���ɡ�
                    notify
                        ͬ���أ���simple���Ƶ����á�����˼�壬�����û����ػ�����������ʱ����������Ϣ(ͨ��sd_notify(3))��systemd
                Type��
                    Type=simple  ˵����
                        ����Щ����� systemctl start *** �������ʹִ�гɹ�������Ҳû�����У�ԭ�����ڴ������ã�
                        simpleΪĬ��ֵ������д����дĬ��ֵΪoneshot��������ָ��ExecStart=�����õĽ�����Ϊ�����̣�
                        ��Ϊ������������ڴ������������֮���ִ�з���Ķ������ļ�֮ǰ��������������Ԫ��
                        ��ע�⣬����ζ�ż�ʹ�޷��ɹ����÷���Ķ������ļ�(���磬��Ϊѡ����User=�����ڣ����߷���������ļ���ʧ)��
                        �򵥷����systemctl start������Ҳ������ɹ���
                    Type=exec   ˵����
                        exec����������simple�����Ƿ���������ῼ����������������ļ�ִ�к����������õ�Ԫ��
                        ����ζ������������ļ���ʧ����ѡ����User=�����ڣ�systemctl start ������
                    Type=forking  ˵����
                        �������Ϊforking����Ὣexecut=�����õĽ��̽�����fork������Ϊ��������һ���֣�
                        ����ζ��������ɺ󸸽����˳����ӽ�����Ϊ������������У����������˳�ʱ�����������Ĭ�ϸõ�Ԫ�Ѿ�������
                        ͨ������PIDFlie=ѡ��Ա�systemd�ܹ��ɿ���ʶ��������Ҫ����
                    Type=oneshot  ˵��
                        ���û��ָ��Type=��ExecStart=�Ļ���Type=oneshot��Ĭ�ϵġ�
                        ��ע�⣬���ʹ�ô�ѡ���û��RemainAfterExit=������Զ������롰�����Ԫ״̬��
                        ����ֱ�Ӵӡ����ת������ͣ�á�������������Ϊû������Ӧ�������еĽ��̡�
                    Type=notify  ˵����
                        notify����Ϊ������exec���ǣ��������������ʱ��Ԥ�ƻ�ͨ��sd_notify(3)���Ч�ĵ��÷���֪ͨ��Ϣ��
                        ���ʹ�֪ͨ��Ϣ��systemd��������������װ�á�
                        ���ʹ�ô�ѡ�NotifyAccess=(������)Ӧ����Ϊ�򿪶�systemd�ṩ��֪ͨ�׽��ֵķ��ʡ�
                        ���NotifyAccess=ȱʧ������Ϊnone��������ǿ������Ϊmain��
                    Type����ѡ��ٷ����飺
                        ͨ�����龡���ܶԳ�ʱ�����еķ���ʹ��Type=simple����Ϊ������򵥡�����ѡ�
                        ���ǣ��������ַ������Ͳ��ᴫ����������ʧ�ܣ�
                        ���Ҳ������ڷ����ʼ����ɺ��������Ԫ��������
                        (���磬����ͻ�����Ҫͨ��ĳ����ʽ��IPC���ӵ����񣬲���IPCͨ�����ɷ���������
                        ������ͨ���׽��ֻ����߼�������Ʒ�ʽ��ǰ����)��
                        �����������¿����ǲ����ġ�
                        �����������notify��dbus(���߽��ڷ����ṩD-Bus�ӿڵ������)����ѡѡ�
                        ��Ϊ����������������뾫ȷ�ذ��ź�ʱ���Ƿ���ɹ������Լ���ʱ����������Ԫ��
                        notify����������Ҫ���������е���ʽ֧��(��Ϊsd_notify()���Ч��API��Ҫ�ɷ������ʵ���ʱ�����)���������֧�֣�
                        ��ô�ֲ���һ���������:��֧�ִ�ͳ��UNIX��������Э�顣
                        ��󣬶�������ȷ������������ļ������õ�������Լ�����������ļ�����ִ�л����ִ�г�ʼ��
                        (�������ʼ����̫����ʧ��)�������exec������һ��ѡ�
                        ��ע�⣬ʹ�ü�������κ����Ͷ����ܻ��ӳ��������̣���Ϊ�����������Ҫ�ȴ������ʼ����ɡ�
                        ��ˣ����鲻Ҫ����Ҫ��ʹ�ü�����������κ����͡�
                        (��Ҫע�⣬���ڳ�ʱ�����еķ���ͨ��������ʹ��idle��oneshot��)
                ExitType=
                    ExitType=main  ˵����
                        �������Ϊmain(Ĭ��ֵ)���������������Ϊ�õ�Ԫ��������(��������=)�˳�ʱ��ֹͣ����ˣ���������Type=oneshotһ��ʹ�á�
                    ExitType=cgroup  ˵����
                        �������Ϊcgroup��ֻҪcgroup��������һ������û���˳����÷��񽫱���Ϊ�������С�
                    �ٷ�ʹ�ý��飺
                        �����������֪�ķֲ�ģ�Ͳ��ҿ��Կɿ���ȷ��������ʱ��ͨ������ʹ��ExitType=main��
                        ExitType= cgroup��ָ�ֲ�ģ������δ֪�ҿ���û���ض������̵�Ӧ�ó���
                        ���ǳ��ʺ���ʱ���Զ����ɵķ����������滷���е�ͼ��Ӧ�ó���
                RemainAfterExit=
                    RemainAfterExit=yes/no  ˵����
                        ����һ������ֵ����ֵָ�������Ƿ�Ӧ����Ϊ��ģ���ʹ�������н��̶����˳���Ĭ��Ϊno��
                    GuessMainPID=
                        ����һ������ֵ����ֵָ��������ܿɿ���ȷ���������PID��systemd�Ƿ�Ӧ�ó��Բ²�����
                        ��������������=�ֲ沢��δ����PIDFile=������Դ�ѡ���Ϊ�����������ͻ���ʽ���õ�PIDFile����PID file������֪�ġ�
                        ���һ���ػ����̰���������̣��²��㷨���ܻ�ó�����ȷ�Ľ��ۡ�
                        ����޷�ȷ����PID������Ĺ��ϼ����Զ��������޷��ɿ�������Ĭ��Ϊ�ǡ�
                    PIDFile=
                        ����ͨ����һ���ļ�·���������ָ������·������Ĭ�����·��Ϊ/run/��ͨ����Type=forkingһ��ʹ�ã�
                        �������������д��˴����õ��ļ���������ļ���Ȼ���ڣ������ڷ���رպ�ɾ�����ļ���
                    �ٷ����飺
                        ��ע�⣬���ִ���Ŀ��Ӧ�ñ���PID�ļ����ڿ��ܵ�����£�ʹ��Type=notify��Type=simple��
                        �ⲻ��Ҫʹ��PID�ļ���ȷ���������Ҫ���̣������ⲻ��Ҫ�ķֲ档
                ExecStart=
                    �����˷���ʱִ�еĴ��в���������������������Ĺ��򣬸�ֵ���ֳ��������������(�μ�����ġ������С�����)��
                     ����Type=��oneshot������ֻ�ܸ���һ�������ʹ��Type=oneshotʱ������ָ������������
                     ����ͨ����ͬһ��ָ�����ṩ�����������ָ��������ߣ����Զ��ָ����ָ���Ի����ͬ��Ч����
                     ��������ַ����������ѡ�������Ҫ�����������б���ǰ����Ĵ�ѡ���Ч��
                     ���û��ָ��ExecStart=����������RemainAfterExit = yes������һ��ExecStop= line����
                     (ͬʱȱ��ExecStart=��ExecStop=�ķ�����Ч��) 
                     ����ÿ��ָ���������һ�����������ǿ�ִ���ļ��ľ���·���򲻴��κ�б�ܵļ��ļ�����
                     ��ѡ�أ����ļ�����������������ַ���Ϊǰ׺:
                ExecStartPre=, ExecStartPost=
                    �ֱ���ExecStart=�е�����֮ǰ��֮��ִ�еĸ������
                    �﷨��ExecStart=��ͬ��ֻ�������������У�����������һ����һ���ش���ִ�е�
                    �����Щ�����е��κ�һ��(���ԡ�-��Ϊǰ׺)ʧ�ܣ�������������ִ�У��õ�Ԫ������Ϊʧ�ܡ�
                    ExecStart=�����������û��ǰ׺��-����ExecStartPre=����ɹ��˳������С�
                     ExecStartPost =ֻ���ڳɹ�������ExecStart=��ָ��������󣬲��������
                     ����Type=(��������Type=simple��Type=idle�������Ѿ�����������Type=oneshot��
                     ���һ��ExecStart=���̳ɹ��˳�������Type=forking����ʼ���̳ɹ��˳���
                     ��READY=1�������͸�Type=notify�����߶���Type=dbus��BusName=�ѱ�����)�� 
                     ��ע�⣬ExecStartPre=���ܲ�����������ʱ�����еĽ��̡�
                     ������ͨ��ExecStartPre=���õĽ��̷ֲ�Ľ��̽�����һ�������������֮ǰ����ֹ�� 
                     ��ע�⣬����ڷ�����ȫ����֮ǰ����ExecStartPre =��ExecStart=����ExecStartPost =��ָ����
                     �κ�����ʧ��(����û���ԡ�-����Ϊǰ׺����μ�����)��ʱ��
                     �����ִ����ExecStopPost =��ָ�������������ExecStop=��ָ������� 
                     ��ע�⣬ExecStartPost =��ִ����Ϊ�˿���Before=/After=����Լ����
                ExecReload=
                    ExecReload=kill -HUP $MAINPID
                        �ؼ���ʹ�ã����Ϊһ������
                ExecStop=
                    ��ѡ��������дҲ�У�
                    ��ע�⣬ExecStop=��ָ����������ڷ����״γɹ�����ʱִ�С�
                    ��������δ����������������ʧ�ܣ�
                    ���磬��ΪExecStart=��ExecStartPre =��ExecStartPost =��ָ�����κ�����ʧ��(����û��ǰ׺��-����������)��ʱ��
                    �򲻻�������ǡ��������޷���ȷ�������ٴιر�ʱ��ʹ��ExecStopPost =�������
                    ��Ҫע�⣬�������ɹ���������ʹ�����еĽ���������ֹ����ֹ��ֹͣ����Ҳʼ�ջ�ִ�С�
                    ֹͣ�������׼���ô���������������systemd֪���ڵ���ֹͣ����ʱ�������Ѿ��˳���
                    ��ô$MAINPID����ȡ�����á� ������������ʵ��Ϊֹͣ������Ȼ��������������
                    ����ζ���ڷ��������������������л�ִ��ExecStop=��ExecStopPost =��� 
                    ���齫����������������ɾ���ֹ�ķ���ͨ�ŵ���������º������裬��ʹ��ExecStopPost =�����档
                RestartSec=
                    ����������������֮ǰ��˯��ʱ��(����������=�����õ�)��
                    ��������Ϊ��λ���޵�λֵ����ʱ����ֵ���硰5min 20s����Ĭ��Ϊ100ms��
                TimeoutStartSec=
                    ���õȴ�������ʱ�䡣����ػ��������û�������õ�ʱ���ڷ���������ɵ��źţ��÷��񽫱���Ϊʧ�ܣ������ٴιرա�
                RuntimeMaxSec=
                    ���÷������е��ʱ�䡣���ʹ�������ַ��������ҷ����Ѽ����ָ��ʱ�䣬��������ֹ���������״̬��
                    ��ע�⣬�����ö�Type=oneshot����û���κ�Ӱ�죬��Ϊ���ǻ��ڼ�����ɺ�������ֹ��
                Restart=
                    ���õ���������˳�����ֹ��ﵽ��ʱʱ�Ƿ�Ӧ������������
                    �������Ϊon-success����ֻ���ڷ�����̸ɾ��˳�ʱ�Ż�����������
                    ѡ���б���file://��дLinux����_ͼ1.png
                RemainAfterExit��Ĭ��ֵno
                    Ĭ��ֵΪno��������ò���booleeanֵ��������0��no��off��1��yes��on��ֵ��
                    �����������Ƿ�Ӧ������Ϊ����ģ����㵱�����еĽ��̶��˳��ˡ�
                    ����֮������������ڸ���systemd�����Ƿ�Ӧ���Ǳ���Ϊ����״̬�������ܽ����Ƿ��˳���
                    ��Ϊtrueʱ����������˳���systemd��Ȼ�����������Ϊ����״̬����֮�����ֹͣ��
                GuessMainPID
                    ����booleanֵָ��systemd���޷�ȷ�еĲ��������ʱ���Ƿ���Ҫ�²�����main pid��
                    ����Type=forking�����ò���PIDFileû�б����ã��������ѡ��ᱻ���ԡ�
                    ��Ϊ������ΪType������ѡ�������ʾ��ָ����PID�ļ���systemd�����ܹ�֪��main pid��
                PIDFile
                    ����һ������·�����ļ���ָ���ػ����̵�PID�ļ�����Type=forking�����õ�ʱ�򣬽����ȡ������á�
                    ������������systemd���ȡ�ػ����̵�������id��systemd����Ը��ļ�д�����ݡ�
                BusName
                    ʹ��һ��D-Bus����������,��Ϊ�÷���Ŀɷ������ơ���Type=dbus��ʱ�򣬸����ñ�ǿ��ʹ�á�
                BusPolicy
                    �����ѡ�ָ����һ���Զ����kdbus�ս�㽫�ᱻ���������һᱻָ��ΪĬ�ϵ�dbus�ڵ㰲װ�������ϡ�
                    �������Զ����ս���������һ�����Թ��򼯺ϡ���Щ���򽫻������߷�Χ�ڱ�ǿ��ָ������ѡ��ֻ����kdbus������ʱ��Ч��
                ExecStart
                    ������������ʱ��systemctl start youservice.service������ִ�����ѡ���ֵ�����ֵһ���ǡ�ExecStart=ָ�� ����������ʽ��
                    ��Type=oneshot��ʱ��ֻ��һ��ָ����Բ��ұ��������ԭ����oneshotֻ�ᱻִ��һ�Ρ�
                ExecStartPre��ExecStartPost
                    ����˼�壬���������õ���������ExecStart��ִ��֮ǰ��֮��ִ�С�
                ExecReload
                    ��������ʱִ�С�
                ExecStop
                    ����ֹͣʱִ�С�
                ExecStopPost
                    ����ֹͣ��ִ�С�
            �ڵ�������
                3.2.1 ��������
                    type �ֶζ����������͡�
                    simple��Ĭ��ֵ��ExecStart�ֶ������Ľ���Ϊ�����̣���������ű��� �� nohup & ��ʽ��������ʱ����ʱ�����ű�����Զ� kill ��ǰ����
                        forking��ExecStart�ֶν���fork()��ʽ��������ʱ�����̽����˳����ӽ��̽���Ϊ�����̣�
                        oneshot��������simple����ִֻ��һ�Σ�Systemd �����ִ���꣬�������������񣬱����������ֻҪ����һ�ξ��У�
                        dbus��������simple������ȴ� D-Bus �źź�����
                        notify��������simple������������ᷢ��֪ͨ�źţ�Ȼ�� Systemd ��������������
                        idle��������simple������Ҫ�ȵ���������ִ���꣬�Ż������÷���һ��ʹ�ó�����Ϊ�ø÷�����������������������������
                3.2.2 ������ֹͣ����������
                        EnvironmentFile���������������ļ����ļ��ڲ����ò�����ʽΪkey=value��ֵ�ԣ�������service�ļ�����$key����ʽ���������
                        ExecStart����������ʱִ�е����
                        ExecReload����������ʱִ�е����
                        ExecStop��ֹͣ����ʱִ�е����
                        ExecStartPre����������֮ǰִ�е����
                        ExecStartPost����������֮��ִ�е����
                        ExecStopPost��ֹͣ����֮��ִ�е����
                3.2.3 ֹͣģʽ
                        KillMode ��ʾֹͣ����ʱ�ķ�ʽ
                        control-group��Ĭ��ֵ����ǰ����������������ӽ��̣����ᱻɱ��
                        process��ֻɱ������
                        mixed�������̽��յ� SIGTERM �źţ��ӽ����յ� SIGKILL �ź�
                        none��û�н��̻ᱻɱ����ֻ��ִ�з���� stop ����
                3.2.4 PrivateTmp
                        ���ֶ��������÷����Ƿ�ʹ��˽�е� tmpĿ¼��
                        ��Ŀ¼�� /tmpĿ¼�£�Ŀ¼����ʽ���£�
                        /tmp/systemd-private-66ae5e5313ba4417b83b427fddb36e47-xxx.service-s65dIw/
                        ��������ʱ����һ��Ŀ¼������ֹͣʱɾ����ʱĿ¼��
                        ���ø����Ժ�д��ʱ�ļ�ʱ���ܻ�д�����Ŀ¼�£���Ҫע��һ��
                        php-fpm��ʱ�ļ�·�����⣨Sytemd PrivateTmp�Ŀӣ�
                        Systemd Unit�ļ���PrivateTmp�ֶ����-Jason.Zhi
        Install
            ������ΰ�װ�����ļ���
            WantedBy����ʾ�������ڵķ����飻
            WantedBy=multi-user.target ��ʾ�������� multi-user.target �û��飻
            multi-user.target ��������з��񶼽�����������
            ִ�� systemctl enable sshd.service ʱ
            ���� sshd.service �ļ���һ���������ӱ��浽 /etc/systemd/system Ŀ¼�µ� 
            multi-user.target.wants ��Ŀ¼�У�
        
    ======================================================================  

    +service�ű�������
        [Unit]
        Description=tzvirtd-Cloud cryptographic server management
        After=network-online.target
        Wants=network-online.target

        [Service]
        User=root
        Group=root
        LimitNOFILE=65536
        Type=simple
        ExecStart=/usr/dong/tzvirtd/tzvirtd/OutPut/bin/Debug/tzvirtd.bin
        ExecStop=/bin/kill -s TERM ${MAINPID}
        ExecReload=
        Restart=always
        TimeoutStopSec=120

        [Install]
        WantedBy=multi-user.target

    +��򻯵�serviceģ��
        [Unit]
        Description=simulator
        [Service]
        Type=simple
        ExecStart=/home/chenfan/simulator/start.sh
        ExecStop=/home/chenfan/simulator/stop.sh
        [Install]
        WantedBy=multi-user.target
    
    +Demo
        [Unit]
        Description=Esign Service
        After=network.target
        [Service]
        Type=forking
        User=root
        ExecStart=/usr/local/bin/esign-startup.sh
        Restart=on-failure
        [Install]
        WantedBy=default.target

        esign-startup.sh ���ݣ�
        #!/bin/bash
        JAR_PATH=/usr/local/app/esign/esign.war
        LOG_PATH=/usr/local/app/esign/start.log
        nohup java -Xms2048M -Xmx8192M -XX:MetaspaceSize=256M -XX:MaxMetaspaceSize=512M  
                   -jar $JAR_PATH > $LOG_PATH 2>&1 &
    ======================================================================    

    +����systemdĿ¼�Ľ���
        /etc/systemd  
        /run/systemd 
        /lib/systemd
            /system   �� �ܶ�ϵͳ���������Ŀ¼��
            /network
            /system-generators
            /system-preset
            /system-shutdown
        /usr/lib/systemd
            /user
            /network
            /scripts
            /catalog
            /user-generators
        /var/lib/systemd
        /bin/systemd
        /usr/shared/systemd
        ��ϵ��
            �� /etc/systemd vs  /usr/lib/systemd
            Systemd Ĭ�ϴ�Ŀ¼/etc/systemd/system/��ȡ�����ļ�
            �����ŵĴ󲿷��ļ����Ƿ������ӣ�ָ��Ŀ¼/usr/lib/systemd/system
            systemctl enable ������������������Ŀ¼֮�䣬�����������ӹ�ϵ
            �� /lib/systemd/system  vs  /usr/lib/systemd/system
            ����ָ�����ͬһĿ¼�������ӷ����²��ǣ�
            �� /etc/systemd/system  vs  /run/systemd/system  vs  /lib/systemd/system
            �Σ�https://www.cnblogs.com/TonvyLeeBlogs/articles/13762400.html
            ��unit���ļ�λ��һ����Ҫ������Ŀ¼:
            ���������������������������������������������������Щ�����������������������������������������������������������
            ��Path                    �� Description                 ��
            ���������������������������������������������������੤����������������������������������������������������������
            ��/etc/systemd/system     �� Local configuration         ��
            ���������������������������������������������������੤����������������������������������������������������������
            ��/run/systemd/system     �� Runtime units               ��
            ���������������������������������������������������੤����������������������������������������������������������
            ��/lib/systemd/system     �� Units of installed packages ��
            ���������������������������������������������������ة�����������������������������������������������������������
            ������Ŀ¼�������ļ����ȼ����δӸߵ��ͣ����ͬһѡ�������ط��������ˣ����ȼ��ߵĻḲ�����ȼ��͵�
            ϵͳ��װʱ��Ĭ�ϻὫunit�ļ�����/lib/systemd/systemĿ¼��
            ���������Ҫ�޸�ϵͳĬ�ϵ����ã�����nginx.service��һ�������ַ�����
            1. ��/etc/systemd/systemĿ¼�´���nginx.service�ļ�������д�������Լ������á�
            2. ��/etc/systemd/system���洴��nginx.service.dĿ¼��
               �����Ŀ¼�����½��κ���.conf��β���ļ���Ȼ��д�������Լ������á��Ƽ�����������
            /run/systemd/system���Ŀ¼һ���ǽ���������ʱ��̬����unit�ļ���Ŀ¼��һ������޸�
            
======================================================================    

+�������ı�������
    ���Եģ��������еķ�����
        ͨ������������ֱ������WebsignServer������ͨ��keepalive����WebsignServer��������
        ԭ����������滷��û׼����
        ���⣬�� /etc/profile �� /etc/rc.local ������keepalive�ķ���Ҳ����
        �ӱ�����ʾ����Ҳ���޷������滷����������
    ���еķ���
        1. дһ��keepalive����
            ԭ����� ps -a | grep ������ ; if [ $? -eq 0 ]; then ִ��Ŀ����� fi
        2. дһ�� /ect/xdg/autostart/*.desktop �ļ�
            ����Ϊ
            [Desktop Entry]
            Exec=���Լ���Ӧ�ó������·����
            Type=Application
            
            ���淽������������²��Կ��ã�������Ҫ.destkop�ļ���ִ��Ȩ�ޣ���Ҳ��˵��
            1. ���� cd /home/xxx/.config��xxxΪ�û�����
            2. �½�autostart�ļ��У�����Լ��½���
            3. ���뵽autostart�ļ���
            4. �½�һ����׺Ϊdesktop���ļ�