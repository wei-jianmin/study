�ڶ���
    2.1 ���໯QDialog
        ʹ�����ǰ������
            ��ͷ�ļ���ʹ��ǰ����������cpp�ļ�����������ͷ�ļ���
            �������Ա���ͷ�ļ���������ж���ط��������ͷ�ļ���
            ���Լ�С�����������߱����ٶȡ�
        ���
            ��UI�������У�����Ϊlabel���û�飨setBuddy��,
            ������label��ý���ʱ��������ת�Ƶ��������
        ������
            ����������addWidget�����������Զ�Ϊ����ӵ��Ӷ������ø���
            tips for using layouts
            when use a layout, you don`t need to pass a parent when constructing the child widgets.
            the layout will auto reparent the widgets (using set parent()) .
            so they are children of the widget on which the layout is installed.
        �źŲ۵��ص�
            ��һ���ź������˶����ʱ���۵ĵ���˳��һ��������˳��һ�¡�
            ���ӵ��źŲۣ�������disconnectȡ������
    2.3 ������ƶԻ���
        ���Ӷ������
            ���Ӷ����������QObject��ʵ�ֵ�
            ɾ�������󣬻�ݹ�ɾ�����Ӷ���
            ɾ���Ӷ��󣬻��Զ����丸����ġ��Ӷ����б��н�֮ɾ����
            ���ڴ��ڲ������Ӷ������ʾ�ڸ������С�
        �Ի���ķ��ؽ��
            accept()�رնԻ��򣬷���QDialog::Accepted(=1),
            reject()�رն���󣬷���QDialog::rejected(=0)��
    2.4 �ı���״�ĶԻ���
        �Ѵ����sizeConstraint������ΪQLayout::SetFixedSize��
        TODO: ѧϰ������
            QTabWidget QStackedWidget QToolBox
            QListWidget QTableWidget QTreeWidget
            QListView QTreeView QTableView
    2.5 ��̬�Ի���
        ��̬�Ի��򼴶�̬����.ui�ļ���
        QUILoader��Ա��������
            void addPluginPath(const QString &path)
            void clearPluginPaths()
            //���������������Ʋ������Ŀ¼��������������ؼ��������Զ���ؼ���
            QStringList availableLayouts() const
            QStringList availableWidgets() const
            //���溯���г����еĿ��ÿؼ����������������Դ��ĺ������ģ�
            virtual QAction *createAction(QObject *parent = Q_NULLPTR, const QString &name = QString())
            virtual QActionGroup *createActionGroup(QObject *parent = Q_NULLPTR, const QString &name = QString())
            virtual QLayout *createLayout(const QString &className, QObject *parent = Q_NULLPTR, const QString &name = QString())
            virtual QWidget *createWidget(const QString &className, QWidget *parent = Q_NULLPTR, const QString &name = QString())
            //������Щ�������ڴ����ؼ�����������action�ȣ�QUILoader����.ui�ļ�������������ʱ�����ǻص�����Щ����
            void setWorkingDirectory(const QDir &dir)
            QDir workingDirectory() const
            //���溯���������õ�ǰ����Ŀ¼��������Դ����ͼ�꣩ʱ���Դ�Ϊ����·��
            QWidget *load(QIODevice *device, QWidget *parentWidget = Q_NULLPTR)
            //����ĺ�������ui�ļ�����̬��������
        ʹ�þ�����
            QUILoader uiloader;
            QWidget * dlg = uiloader.load(QIODevice *device, QWidget *parentWidget = Q_NULLPTR);
            QButton* btn1 = dlg->findchild<QButton*>("btn1");
            ......
            

        
        
        
            