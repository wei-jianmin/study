<catalog s0>
QApplication�Ĺ���
    QApplication app(argc,argv);
    ...
    return app.exec();
    app.exec()ʹ�ó�������¼�ѭ��״̬����Ӧ�û�������
���Ӷ����ϵ
    ����ĸ��ӹ�ϵ����QObject��ʵ�ֵģ�������ɾ��ʱ�������ɾ���Ӷ��󡣶��ڿ��ӿؼ���������ɾ��ʱ��
    ����ζ�Ų����ø���������Ļ����ʧ�����Ӷ���Ҳ�����Ļ����ʧ   
�����ض��常�������
    ��һ��������뵽һ��������ʱ��qt���Զ������������ĸ��������һ����qt�ٷ��ĵ�����������
    tips for using layouts
    when use a layout, you don`t need to pass a parent when constructing the child widgets.
    the layout will auto reparent the widgets (using set parent()) .
    so they are children of the widget on which the layout is installed.
    ��λ���˵��layout���Զ�����widgets��parent��
    ���⣬��ʹLayout�Ĺ������Ϊ�գ�Ҳ����setLayoutʱ��ͬʱΪLayout�����ӿؼ�ͳһ����parrent��
    
    ����setLayout�Ĳ���˵����
    ���widget���Ѿ���װ��һ��layout�����widget�в��ܰ�װ�ڶ���layout��
    �������ɾ����һ��layout����layout()��ȡ��Ȼ��delete����Ȼ�����ʹ��setLayout��
    �����һ��layout�Ѿ���װ��widget_A�У����н�֮setLayout��widget_B�У�
    ������õ��Ǹ�����������Ч�ģ���layout������������widget_B�У�������widget_A�С�
    �ܽ᣺widget��layout��һ���ܲ�һ���ӵĹ�ϵ��
    һ��widget��һ���ӣ��ɵ��ܲ������ߣ��µ��ܲ��Ų�����
    һ��layout��һ���ܲ����ȷŵ�A�ӣ��ַŵ�B�ӣ���������B�ӡ�

    �Աȣ�
    QLayout *p = new QLayout(parent)    ͬʱ�����ò���+���ø�����Ĺ���
    parent->setLayout(p)                �����캯������parent��������
    p->setParent(parent);               �����ø����󣬲������ò��ֵ�����
    �����ԣ�
    QLayout *p = new QLayout(parent) �� pΪ��Ϊparrent��Layout
    p->addWidget(w1);                   �Ὣw1�ĸ���Ϊparent
    p->setParrent(parent2);             
    p->addWidget(w2);                   �Ὣw2�ĸ���Ϊparent2
���
    ֻ��label�������û�飨setBuddy��,������label��ý���ʱ��������ת�Ƶ��������    
ʹ�����Զ���ؼ��Ĵ�С�仯����ʾ���أ����������С:
    layout()->setSizeConstraint(QLayout::SetFixedSize);
    ������ʹ�û������޸Ĵ���Ĵ�С�����ֲ��ָ�������ڴ�С��       
ʹ��QUiLoader������̬�Ի���
    QUiLoader���Զ�̬����ui�ļ��������ǿ��Զ�̬�ĸı������棬
    ���������±�����򡣵�����Ҳ���������ʱ�Ĺ�������
    ����ͨ��uiֱ�����ø��������ˣ�����Ҫͨ����̬���ڶ����
    findChild�����ĺ�������ȡ�����е��Ӳ���
    QUiLoader uiLoader;
    QFile file("a.ui");
    QWidget * dialog =  uiLoader.load(&file);
    if(dialog)
        QLabel *tbl = dialog->findChild<QLabel*>("label1");
    findChild��ģ�庯�������Է�������������ͺ�������ƥ����Ӷ���
    ʹ��QUiLoader����Ҫ��pro�ļ�������uitoolsģ�飺CONFIG+=uitools
����QAction
    һ����������һ���źŷ�����������ͨ��widget��ȣ�
    ������Ȼ�ĸ��ŵ��˵��򹤾����ϣ�Ҳ�ܶ�������
    ���޷�ͨ���������ʦ�Ϸţ�������ͨ�����봴������
    �����������ص�Ԫ�س����ľ����ı����ݺ�ͼ�꣬
    ���⻹֧�ֿ�ݼ��������ͣ��ʾ��
    ���ÿ�ݼ���
    setShortcut(QKeySequence::New); ʹ���½���ϵͳĬ�Ͽ�ݼ�(Ctrl+N)
    setShortcut("Ctrl+Q");          ʹ��ָ���Ŀ�ݼ�
�źŲ�
    QObject::sender()���ط����źŵĶ����ָ�롣
    ����QAction *act = qobject_cast<QAction*>(sender());
    emit��qt�Ĺؼ��֣��ᱻc++Ԥ������ת�ɱ�׼c++���룬emit �źź���(); ���Է����źţ���ֱ�ӵ��òۺ�����ȣ�
    ʹ���źŲ۵ķ�ʽ�������źŲ۵�ʹ��ǰ���Ǽ̳���QObject�࣬����ͷ�ļ�������Q_OBJECT�ꡣ
    ͨ��connect���ӵ��źŲۣ�����ͨ��disconnect�жϹ�����
�˵�
    �˵�QMenuBar
        QMainWindow��menuBar��Ա���������ڵ�һ�ε���ʱ��ͨ�����
        layout()->menuBar�ж��Ƿ��Ѵ����˲˵������û�У��ú������Զ������˵���
        �ú�������һ��ָ��QMenuBar��ָ�롣
        QMenuBar�ĳ�Ա����addMenu�����ص��Ǹ�QMenuָ�롣
        QMenu����addAction��addSeparator��addMenu(�Ӳ˵���)�ȷ���
    �Ҽ��˵�
        Ϊwidget��ؼ������Ҽ��˵�������
        �ؼ�����setContextMenuPolicy(Qt::CustomContextMenu)ʹ֮����Ӧ����Ҽ�
        ���ؼ���������һ�ʱ���ᷢ��
        QLabel::customContextMenuRequested(const QPoint & pos)�ź�,
        ��Ӧ���źţ�������Ӧ�Ĳۺ����е���QMenu��exec���������ɵ����˵���
        Ҳ�������¼̳�ʵ��QWidget::contextMenuEvent(QContextMenuEvent * event)
        ���һ��ؼ�ʱ������øú�����
    QAction
        ÿ���̳���Widget�Ķ�����addAction���������������κοؼ����ø÷����������塣
        ���ڲ˵������QAction���������Ӳ˵��
        ���ڹ����������QAction������ӹ����
        ����QAction�����������ı���ͼ�����ʾ���������ź����ӵ����ϡ�
    ����Ҽ��˵�
        ����widget�ؼ�������֧���Ҽ��˵�
        void setContextMenuPolicy ( Qt::ContextMenuPolicy policy )
        Qt::ContextMenuPolicyö�����Ͱ�����
            Qt::DefaultContextMenu
                �����Ҽ��¼���Ӧ����contextMenuEvent()�������Ҽ��˵���
                ��ζ��Ҫ��дcontextMenuEvent( QContextMenuEvent * event )������
            Qt::NoContextMenu
                û���Լ����Ҽ��˵�������ʾ���ؼ����Ҽ��˵���
            Qt::PreventContextMenu
                ��NoContextMenu��ȣ�������˳�ӵ�parent��
                ��ζ�����е�����һ��¼���������QWidget::mousePressEvent()
                ��QWidget::mouseReleaseEvent()����
            Qt::ActionsContextMenu
                �Ѳ���������action��ͨ��addAction������ӣ������˵���ʾ������
            Qt::CustomContextMenu
                �ᷢ��QWidget::customContextMenuRequested(const QPoint & pos)�źţ�
                ��Ҫ�����ź���˵���Ӧ�Ĳۺ������ӡ�
    addAction����
        �˵������Լ�ʵ�ֵ�addAction������Ҳ�м̳���QWidget��addAction������
        ���߽���һ��QAction*������
        ������̳���QWidget��addAction����ͨ������Ϊ��ӵ�QAction*�������ø�����
        ���Ը��˵���Ӳ˵���ʱ��һ��ʹ�ò˵��Լ�ʵ�ֵ�addAction������
        ��QWidget��addAction������Ҫ���contextMenuEvent(Qt::ActionsContextMenu)ʹ��              
״̬��
    ͬ�˵���һ��������statusBar�������״̬��QStatusBarָ�룬
    ����������û��״̬��ʱ�����Զ�����״̬����
    ״̬���ṩaddWidget����(��ָ����չ����)��ͬQLayoutһ����
    �����Զ�Ϊ��ӵ�����Ŀؼ��ض��常����ΪQStatusBar��      
����
    ���ڵ�����
        newһ������ʹ����ʹ��ָ�������󣬲��Ҳ��ֶ�deleteҲûӰ�죬
        ��ΪQt������д��ڽ��и��٣�����closeAllWindows���ر���̳���
        �����д��ڣ����������еĴ��ھܾ��˹ر��¼���
    ���ڵĹر��������˳�
        ͨ������ʵ��QWidget::closeEvent������������;��ȡ��������ڵ�
        �رղ��������ҿ���ȷ�������ǲ������Ҫ�ر�������ڡ�
        �����һ�����ڹرպ�QAppliction���Զ��������������Ҫ��
        ����ͨ��QApplication::LastWindowClosed(false)����������Ϊ��
        ��������Ӧ�ó��������������У�ֱ������QApplication::quit();
        ���û��ر�һ������ʱ��Ĭ����Ϊ�������������������ᱣ�����ڴ��С�
        �ڴ��ڵĹ��캯���У�ʹ��setAttribute(Qt::WA_DeleteOnClose);
        ���Ը���Qt�ڹرմ���ʱ�������ڶ���ɾ����
        Qt::WA_DeleteOnClose�����ǿ�����QWidget�����õģ�
        ����Ӱ��������ڲ�������Ϊ�ģ������֮һ��
    ��ģ̬����
        ͨ��show��ʽ��ʽ�Ĵ��ڣ�Ϊ��ģ̬���ڡ�
        show()������һ�����صĴ��ڱ�Ϊ��ʾ�ġ��������Ϸ��ġ�����ģ�
        ��������ڱ��������ʾ�ģ���show()�Ͳ���������
        show()��hide()�Ƕ�Ӧ�ġ�
        raise()������һ�������Ѿ���ʾ�Ĵ��ڳ�Ϊ���㴰��
        activeWindow()������һ�������Ѿ���ʾ�Ĵ��ڳ�Ϊ����Ĵ���
    ģ̬����
        ���ڶ���.exec()����ʹ����ģ̬��ʾ
        ����Ի��򱻽���(QDialog::Accepted)����exec����true��
        ���򷵻�false(QDialog::Rejected)��
        ȷ����ȡ����ťͨ�����õ���accept()������reject()�����رմ��ڡ�
    QApplication::topLevelWidgets()���Ի�ȡ���еĶ��㴰�ڡ�
    ��������
        qt�����˸����������࣬���������д�����ʼ������Ҫ������ʾ����ʱ��
        ����Ԥ����ʾһ���������ڡ�
        QSplashScreen��һ�����õ����������࣬������ʾ�򵥵�ͼƬ�����֡�      
ע���Զ�������
    �Զ�������ͣ����û��ע�ᣬ�ǲ�����Ϊ�źŲ۲����ģ�Ҳ���ܺ�QVariant֮��ת��
    �����Զ�������ע��һ�£��Ϳ����ˡ�
    ע��ķ����ǳ��򵥣�Q_DECLARE_METATYPE(�Զ�������);       
���ÿؼ�ʹ��
    QMainWindow
        QMainWindow������������Ա����������QWidget���ڲ���ռ�ã���
        ��׼Qt���ڲ������Զ��崰�ڲ��������в��ֹ�������QWidget��
        �зִ���(splitter)�����ĵ����ڲ����ȡ���
    QTabWidget
        ������QStackedWidget�����ṩ����Tab��
    QTextBrowser
        QTextBrowser�Ǹ�ֻ����QTextEdit���࣬��������ʾ����ʽ���ı���
        ��QLabel��ͬ�������ڱ�Ҫ��ʱ����ʾ��������ͬʱ��֧�ּ��̺���굼����
        QtAssist�����øÿؼ����ְ����ĵ��ġ�
    QTextEdit
        QTextEdit������������ʾ�༭��ͨ�ı��͸��ı�����֧�ּ��а塣
    QProgressDialog
        ���õĽ��ȶԻ���
    QInputDialog
        ���õ�����Ի���
    QPushButton
        ����Button�࣬��Ȼ����֧��toogle�źţ���ֻ����checkable״̬�£�
        �Żᷢ�����źš�
    QButtonGroup
        ʹcheckable��ť����--ֻ��һ������ѡ��״̬��
    QAction
        QAction�������κδ�����������
    QActionGroup
        QAction��Buttonһ����Ҳ�ǿ�������checkable�ģ�ʹ��QActionGroup��
        ����ʹ���QAction����--ֻ��һ������ѡ��״̬��
    QTableWidget
        QTableWidget�ĵ�Ԫ�����ԣ����������ı������뷽ʽ�ȣ�������QTableWidgetItem�С�
        QTableWidgetItem����һ�����ڲ����࣬����һ������������ࡣ
        ���û���һ���յ�Ԫ��������һЩ�ı���ʱ��QTableWidget���Զ�����һ��
        QTableWidgetItem��������Щ�ı���ʵ���ϣ�QTableWidget����ÿ����Ҫ�����ʱ��
        �������ݵ�����ԭ��ģʽ��¡������
        QTableWidget::clear�����������������������������ֻ��������ݣ������������ʽ��
        QTableWidget�ж���Ӵ��ڲ�����ɡ������Ķ����и�ˮƽ��QHeaderView����������࣬
        �и���ֱ��QHeaderView����������QStrollBar���������м䣬���и���Ϊ�ӿڵ����ⴰ�ڲ�����
        ������Щ���ڲ������з��������ʵ���
        ͨ��QWidget::item()���������Ի��һ��QTableWidgetItemָ�롣
        setItem(int row, int column, QTableWidgetItem *item)�����������������һ����Ԫ��
        ����setItemʱ��QTableWidget���õ�QTableWidgetItem������Ȩ��������ȷ��ʱ���Զ�����ɾ����            
������ʹ��
    QString
        QString::arg("�滻�ַ���")��ʹ���Լ��Ĳ����滻��С���ֵ�%n�����������滻���QString��      
��������
    ��ui��ƹ���ʦ���Ҽ��˵����д�ѡ�
    ���Զ�����һ��NewLabel���̳���QLabel������Խ�QLabel�ؼ�����Ϊ�Զ����NewLabel
    �������������и�ȫ�ְ���ѡ����ư����Զ������ͷ�ļ�ʱ��ʹ��<>����""��
    ���������Զ������ͣ���ui���ʦ�����²��ܱ༭�Զ�������Ժ��źŲۡ�
    Ҫ����ui���ʦ������ʹ���Զ�����źŲۣ��������Ҽ��˵���ѡ��"�ı��ź�/��"���ڵ��������������Զ�����źŲۡ�
��������
    ��ui���ʦ�����У��Ҽ�������ؼ�ʱ����"����Ϊ"ѡ����Խ�����������ı���Ϊ����������  
�Զ�������
    ����Q_PROPERTY��Ŀ��������Ԫ����ϵͳ���˽�����ݳ�Ա
    ��ʹ��qss��ƿؼ���ʽʱ�����ԶԲ�ͬ��������Ʋ�ͬ����ʽ���������ؼ������Ըı�ʱ����ʽҲ��֮�仯��
    �޸�Ҳ���Ժ�Ҫ����ˢ��һ�¿ؼ����µ���ʽ�Ż���ʾ���磺btn->style()->polish(btn); 
�Զ���ʵ��ȫ�´��ڲ���
    ���벿��
        ͨ�����໯QWidget��������ʵ��һЩ�������ƴ��ڲ�������Ӧ������¼��Ĵ�������
        QLabel��QPushButton��QTabWidget���������ַ���ʵ�ֵġ�
        ���ʹ��Q_PROPERTYע�������ԣ�����Qt���ʦ��ʹ��������ڲ���ʱ��
        ��Qt���ʦ���Ա༭�����Щ�̳���QWidget���������棬������ʾ��Щ�Զ������ԡ�
    Q_OBJECT���Ǳ���ġ�
    һ����Ҫ�̳�mousePressEvent��mouseMoveEvent��paintEvent����������
    ����paintEvent
        �����ڵ�һ����ʾʱ���򴰿ڴ�С�ı�ʱ���򴰿ڱ��ڵ����ֵ�����ʾʱ�������һ�������¼���
        Ҳ����ͨ������QWidget��update()��repaint()����ǿ�Ʋ���һ�������¼���
        repaint��Ҫ�������ػ棬��update���ǰѻ����¼����ڶ�����(������������¼����Զ��ϲ�)��
        �����´δ����¼�ʱ���ŵ���һ�������¼���
        ���Ϊ����������Qt::WA_Staticcontents���ԣ��Ǹ����ڸı��Сʱ��������ڱ��
        ������¼�������Ϊ��������������������ڱ�С��������������¼���
        ���û�����ù������ԣ���ÿ���ı䴰�ڴ�Сʱ�����ڵ������ɼ���������һ�������¼���
    ��Qt���ʦ�м����Զ��崰�ڲ���
        ��������
            ѡ��һ������Qt���ڲ��������ô��ڲ���Ҫ�������Զ���Ĵ��ڲ��������ƵĽӿڡ�
            Ȼ���Ҽ��ÿؼ������ÿؼ�����Ϊ�Զ���ؼ���
            ȱ�����޷����Զ�������Խ��з��ʣ�Ҳû��������Զ��崰�ڲ���������л��ơ�
        �������
            ��������Ŀ��-��������Ŀ��-��qt���ʦ�Զ���ؼ��� ����һ�����xxx.dll��xxx.a
            Ȼ���������ļ�����qt/qt5.1.1/5.1.1/mingw48_32/plugins/designer��
                �Զ���Ŀؼ��Ǽ̳���QDesignerCustomWidgetInterface�ӿڵġ�
                ����Ҫͨ����Q_INTERFACES������moc���̳е�QDesignerCustomWidgetInterface�Ǹ��ӿڣ�
                ��Ҫ�Լ�ʵ��QDesignerCustomWidgetInterface�ĸ����ӿڡ�
                Qt���ʦ�����createWidget()���������Զ���ؼ�ʵ����
                ���Զ���ؼ��ࣨͷ�ļ�����ĩβ��ʹ��Q_EXPORT_PLUGIN2(�������,�������)�꣬
                �Ե�����Ҫ�ĺ�����ȷ��Qt���ʦ����ʹ�øò����
                ������Զ������ؼ�������ѡ���QDesignerCustomWidgetCollectionInterface������
�¼�����
    ��������
        �¼��Ǵ��ڻ�qt��������ģ�������¼��������ػ��¼�����ʱ���¼��ȡ�
        �󲿷��¼����û����������ģ�����Щ�¼�����ϵͳ���в����ģ��綨ʱ���¼���
        ��ʹ��qt���ʱ��ͨ������Ҫ�����¼�����Ϊ������ĳЩ��Ҫ������ʱ��qt���ڲ����ᷢ�źš�
        �������Զ���ؼ���������ϣ���ı�ԭ���ؼ�Ĭ����Ϊʱ���ͻ�ʹ�õ��¼���
        һ��ʹ�ÿؼ�ʱ����Ҫʹ���źţ�ʵ��(����)�ؼ�ʱ����Ҫʹ���¼���
    �¼�����
        Qt�е��¼���ֱ�ӻ��Ӽ̳���QEvent��
        �¼������ǣ�qt�ᴴ��һ���¼������¼�ѭ�����ջ����QOjbect���event������
        ������¼�����Ŀ�����
        ��ָ�����ǣ�event���������������¼������Ǹ����¼����ͣ�������Ӧ���¼���������
        �¼��������ķ���ֵ��ӳ�¼��Ƿ񱻽��ܲ��õ��˴���
        ��QWidget��event��������ꡢ���̡��ػ��¼��ֱ�̳�mousePressEvent()��
        keyPressEvent()��paintEvent()��Щ�ض����¼����������д���
        ������Ϣ�ɲο����źŲ�ԭ��һ�ڡ�
    ����ʵ���¼�������
        ??�����¼�����QEvent�����ࡣqt�е��¼�������100���֣���ͨ��QEvent::type()�����¼����͡�
        ??QObject������virtual bool event(QEvent*e)������
        �ú������յ�������¼������ʶ�𲢴������¼�e����Ӧ����true��
        ??QWidget�е�event()ʵ���˰Ѿ���������͵��¼�����ǰ�����ض����¼���������
        ��mousePressEvent()��keyPressEvent()��paintEvent()�ȡ�
        ??Tab����shift+Tab���Ǹ����⣬��Widget::event()�У�����keyPressEvent()֮ǰ��
        ����ר�Ŵ����ﵽ�ؼ�����ת�Ƶ�Ч����
        ??��������Զ���ı༭���ؼ��У���tab�����������ã���Ӧ������keyPressEvent�¼���
        ����Ӧ������event�¼������������ж� event->type() == QEvent::KeyPress��
        �����ȣ������ QKeyEvent *key_event = static_cast<QKeyEvent*>(event);
        ע�⴦����󣬲�Ҫ���ǵ���QWidget::event()��������QWidget���������¼���
        ??����event�¼�ʱ���������true��������¼���������ˣ�
        �������false����ϵͳ�����Զ����ø����event������
        ??Ҫ���ÿؼ���Ӧ�����¼�����������event��keyPressEvent�⣬������ʹ��QAction��
        QAction֧��setShortcut�������������ÿ�ݼ���
    ��װ�¼�������
        QObjectʵ�������������յ��¼�֮ǰ��������һ��QObjectʵ���ȼ�����Щ�¼���
        ������һ�������ؼ������������ڰ��س����󣬽����Զ�ת�Ƶ���һ�������
        һ�ְ취������keyPressEvent��if(event->key()==Qt::Key_Enter) focusNextChild();
        ��һ�ְ취��ʹ���¼�����������������¼����յ��¼�ǰ���������ĸ����ڼ����¼���
        �������Ϊ��
            1. ����installEventFilter(QObject*)���������ڶ���ע��Ϊ���Ӷ���
            2. �ڼ��Ӷ���(����Ϊ������)��eventFilter�����д���Ŀ�����(�ӿؼ�)���¼���
        ���Ϊһ������װ�˶���¼������������װ���ȵ��ã��Ȱ�װ�ĺ���á�
    5���¼����˷��������ȼ��ɵ͵��ߣ�
        1. �����ض��¼���������������mousePressEvent��
        2. ����event(),���ֵ����ȼ��ȵ�һ�ָ���
        3. ��װ�¼������������ֵ����ȼ��ȵڶ��ָ���
        4. ΪqApp��Ψһ��QAppliction����ע���¼���������
           ��ʱӦ�ó����У�ÿһ�������ÿ���¼����ڷ��͵������¼�������֮ǰ��
           �����ȷ�������¼��������������������ȼ��ȵ����ָ���
           ���������ַ�����ϵ�ʽ����������֪���ڱ���ǰ������ʲô�¼���
        5. ���໯QAppliction��������ʵ��notify()
           qt�ڲ�����QAppliction::notify()������һ���¼���
           �������¼���Դͷ��
    �¼��Ĵ�������
        QWidget��event�����Ѿ�������������͵��¼�����������QMouseEvent�ȣ����ݸ��ض����¼���������
        ��mousePressEvent(),QWidget��������mousePressEvent()�������Ϳ��Զ�������¼��������ˡ�
        tab������һ�����������QWidget::event�ڵ���keyPressEvent����֮ǰ�����Ȱѽ��㴫�ݸ���һ�����ڲ�����
        �����������Ҫ��������ؼ�ʵ��tab�������ܣ�������keyPressEvent�����ǲ����õģ��Ѿ����ˣ���
        ��Ҫ����event()�������������浥������tab�����������Ȼ��ǵ�return QWidget::event(event);
        ������event�������Ȼת����QWidget::event(),
        ������¼���������Ŀ�����֮ǰû�еõ�����Ҳû�б�Ŀ�������
        ��ô�ͻ��ظ�����¼�������̣�ֻ������λ��ԭĿ�����ĸ����󣬵����µ�Ŀ�����
        �ظ���ֱ�����ʱ����ȫ�õ������򵽴������Ķ���Ϊֹ��
        ���ڴ����еİ����¼������û�����һ������ʱ������¼��ᷢ�͸���ǰӵ�н���Ŀؼ���
        ����ؼ�û�д�����¼����򷢸����ĸ��ؼ���֪������QDialog����
    �¼�ѭ��
        ������QAppliction::exec()ʱ�����������¼�ѭ������ѭ���в��ϼ���Ƿ����¼�������
        �������߳�Ӧ���¼����У�������Щ�¼����͸���Ӧ��QObject��
        ������һ���¼�ʱ�����ܻ�ͬʱ����һЩ�������¼�����ʱ�ò���������
        ��Щ�¼���׷�ӵ�Qt���¼�������
    ĳ���¼���Ӧ��ʱ�����Ӧ�Դ�ʩ
        ����ڴ���һ���ض��¼��Ϻ�ʱ���࣬�ͻᵼ�½����޷���Ӧ��
        ������һ���¼���Ӧ�б����ļ�����ֱ���ļ�������ϣ��Żᴦ����ϵͳ�����������¼���
        һ�ֽ���취���ǿ��ǽ������޹ز����ŵ����߳��д���
        ��һ�ֱȽϼ򵥵Ľ���취�����ļ���������о�������QAppliction::processEvents()��
        �����������Qt��ȥ��������û��������¼���Ȼ���ٽ�����Ȩ�������ú����ĵ����ߡ�
        ʵ���ϣ�exec()�ڲ����ǲ�ͣ����processEvents()��whileѭ����
        ʹ�õڶ��ַ�������һ��Ǳ�����⣺���������ļ���ȫ������֮ǰ���û��ر��˴��ڣ�
        �Ӷ����²���Ԥ�ϵĺ������������ļ��������ʽ�ǽ�qApp->processEvents()����
        qApp->processEvents(QEventLoop::ExcludeUserInputEvents)��������Qt�������¼�����
        �е��û������¼�����������¼��ͼ����¼�����
    �Զ����¼�
        1. �̳�QEvent�࣬���ö���Q_OBJECT�꣬
           ע��QEvent�Ĺ��캯���и�ö�����͵�QEvent::Type�����������¼����ͣ�
           �����Զ������ͣ����ö��ֵӦ����1000~65535֮�䣬
           �Ƽ�ʹ��int QEvent::registerEventType()��̬������ȡһ��ϵͳ������¼����ͣ�
           �ú�������ֵ����1000~65535֮�䡣
        2. ���þ�̬����QCoreApplication::postEvent(QObject *receiver, QEvent *event, int priority)
           receiverΪ�¼������ߣ�eventΪ�Զ����¼�����priority���ȼ�һ�����Ĭ��ֵ����
           ����postEvent���̺߳�receiver������ͬһ���߳��У�Ҳ�����ڲ�ͬ���߳���
           ������QCoreApplication::postEvent(&mainWindow,new MyEvent());
           ���õ���MyEvent���ͷ����⣬�ڽ����߳��л��æ�ͷŸö���
           ������MyEvent�����������д�ϵ�����Զ����¼�����α��ͷŵġ�
        3. �����¼������ߵ�event����
           �����¼����ͣ��ж�������Զ�����¼����ʹ�������true��
           ���򣬵��ø����event���������ء�
        ������            
            1.  ����Qt Widgets Application
            2.  �Զ����¼�
                #include <QEvent>
                class MyEvent : public QEvent
                {
                public:
                    MyEvent(int data);
                    ~MyEvent();
                    int data() {return _data;}
                private:
                    int _data;
                };
                MyEvent::MyEvent(int data) : QEvent(QEvent::Type(1001))
                {
                    _data = data;
                }
            3.  �����̣߳����߳��з����¼�
                #include<QThread>
                #include <QWidget>
                class MyThread : public QThread
                {
                public:
                    MyThread(QWidget *main_window);
                protected:
                    void run();
                private:
                    QWidget* _pmw;  //�¼�������
                };
                #include <QCoreApplication>
                MyThread::MyThread(QWidget *main_window)
                {
                    _pmw = main_window;
                }
                void MyThread::run()
                {
                    static int i=1;
                    while(_pmw)
                    {
                        sleep(3);
                        QCoreApplication::postEvent(_pmw,new MyEvent(i));
                    }
                }
            4.  ���ؽ�����MainWindow��event����
                bool MainWindow::event(QEvent *event)
                {
                   if(event->type() == 1001)
                   {
                       MyEvent* e = static_cast<MyEvent*>(event);
                       //�����Զ����¼�
                       return true;
                   }
                   return QMainWindow::event(event);
                }
            5.  main�����У�
                #include "myevent.h"
                #include "mythread.h"
                int main(int argc, char *argv[])
                {
                    QApplication a(argc, argv);
                    MainWindow w;
                    w.show();
                    //a.postEvent(&w,new MyEvent(3)); ���̷߳����Զ����¼�
                    MyThread t(&w);  //���߳��з����Զ����¼�
                    t.start();
                    return a.exec();
                }           
��ʽ��
    �����﷨
        ѡ���������ԣ�ֵ;��
        ��ֻ��һ������ֵʱ��ĩβ�ķֺſ���ʡ�ԣ���������������÷ֺŸ���
    ѡ����
        ����ѡ����
            ͨ��ѡ����           "*"
                ƥ������е�����widget
            ��ѡ����             "����"
                ƥ��ָ���༰������������
                �� QPushButton{color:red;}
                �����������ռ���ʱ���������ռ��������--����
                �� utils--QPushButton
                ֮���Բ���::����������Ϊ:��ʾ��һ��ѡ����
            ��ѡ����2            ".����"
                ƥ��ָ���ࣨ��ƥ���������ࣩ
                �ȼ��� *[class~="QPushButton"]
            ����ѡ����(idѡ����) "#������"
                ���ݶ�����ƥ���ض����� (��Сд����)
                ��#button_1 {color:red;}
                ���Ը���ѡ�������ã���QPushButton#okButton
                ע�⣺��������Ȼ�淶�������пո񣬵�����Ķ����������пո�
            ����ѡ����           "[����=ֵ]"  "[����|=ֵ]"  "[����~=ֵ]"
                "[����=ֵ]" ƥ��ĳ����Ϊ�ض�ֵ�����пؼ�
                "[����|=ֵ]" ƥ��ĳ�������ض�ֵ��ͷ�����пؼ�
                "[����~=ֵ]" ƥ��ĳ���԰����ض�ֵ�����пؼ�
                             ����İ�����ֵָҪ�ǵ����ģ��༴ֵ��ǰ��Ҫ���������пո����
                             ����[objectName~="button"] {color:red;}
                ���������ָ������Q_PROPERTY���������ԣ�������Ҫ��QVAirant::toString()֧��
                ���Ը���ѡ�������ã���QPushButton[flat="false"]
        ����ѡ����
            ���ѡ����           " " ���ո�
                ���ָ���Ǹ�����Ԫ��
                ���ѡ��������ͨ���ո�һֱ������ȥ����: ѡ����1 ѡ����2 ѡ����3{����:ֵ;}
                ����ѡ��������ʹ������һ�ֻ���ѡ����
            ��Ԫ��ѡ����         ">"
                >ǰ����Ȼ�����пո񣬵�������д�ո�
                ��Ԫ��ѡ����ֻ�����¼���Ԫ�أ������Ǹ�����Ԫ��
                ��Ԫ��ѡ��������ͨ��">"һֱ������ȥ��ֻ����һ��">"
                ">"ǰ�����ʹ������һ�ֻ���ѡ������һ��ʹ����ѡ����2��
            ����ѡ����           ","
                ��ÿ������ѡ����ƥ�䵽�Ŀؼ��ŵ�ͬһ�����������
                ��ʽ�� ѡ����1,ѡ����2,ѡ����3{����:ֵ;}
        ����ѡ����
            �ӿؼ�ѡ����         "::"
                ������ӿؼ�����ָ�������Ϳؼ��������Ԫ�أ�
                ��QSpinBox�����¼�ͷ���ı���Ĺ�������
                ��ʽ�� ��ѡ����::�ӿؼ�{����:ֵ;}  ��ѡ����2::�ӿؼ�{����:ֵ;}
                ������ QComboBox::down-arrow{ image:url(:/res/arrowdown.png);}
            α��ѡ����           ":"
                ��ʽ�� ��ѡ����:״̬{����:ֵ;}  ��ѡ����2:״̬{����:ֵ;}
                ������ ����������ڰ�ť��ʱ QPushButton:hover{color:white;}
                       ״̬�����ã�ȡ������QPushButton:!hover{color:white;}
                ���״̬����ͨ��":"�������ӣ��� QCheckBox:hover:checket{color:red;}
                ��ʾ��ѡ����ڡ�Ϊchecked������������桱ʱ��ǰ��ɫΪ��ɫ��
                α��ѡ����Ҳ֧��","ȡ��������QCheckBox:hover,QCheckBox:checket{color:red;}
                α��ѡ����Ժ��ӿؼ�ѡ�������ã���QComboBox::drop-down:hover{ ...; }
        û��ѡ���������
            ���ûָ��ѡ���൱��ѡ���˱������������Ӷ���
    ѡ�����Ľ�Ϲ���
        ����QDialog QComboBox,QLineEdit �ᱻ���Ϊ (QDialog QComboBox),QLineEdit
    �����
        ���һ���ؼ��������������ʽ����������ʽ�Ḳ��ǰ�����ʽ��
    �̳���
        ��CSS��ͬ��һ��widgetĬ�ϲ����Զ��̳и��ؼ����������ɫ��
        �෴�ģ�ͨ������widget��setFont()��setPalette()�����Ӱ�쵽���ӿؼ���
        ͨ��QCoreApplication::setAttribute(Qt::AA_UseStyleSheetPropagationInWidgetStyles,bool);
        ���Կ�����ʽ��ļ̳��ԡ�
    ���ȼ�
        ���ؼ�ֱ�����õ���ʽ > ��QAppliction���õ���ʽ�� ��ʹQAppliction�е�ѡ�������ȼ�����
        ѡ����Խ���⡢Խ��ȷ�������ȼ�Խ��
        idѡ���� > ��ѡ����2 > ��ѡ���� > ͨ��� > �̳� > Ĭ��
    ��ģ��
        ���е�widget�������Ա�����һ�������ӡ���
        һ�������ӡ����� ��߾�(margin)���߿��ϸ(border)���ڱ߾�(padding)����������(content)
        ��߾�ָ�߿���Χһ�������ڣ������������ؼ�
        �߿����Լ�����ɫ�����ܺ��ӱ���ɫ��Ӱ��
        �ڱ߾��ܺ��ӱ���ɫӰ��
        �ؼ���width��height��ָ�������Ϻ��ӵĿ�Ȼ�߶ȣ�
        width = ����߾� + ��߿��� + ���ڱ߾� + ���ݿ�� + ���ڱ߾� + �ұ߿��� + ����߾�
    ���ÿؼ�����
        ��Qt4.3��ʼ���ؼ������е�Q_PROPERTY���ԣ���ͨ����qproperty-<������>�����﷨��ʽ���ã�
        �磺 MyLabel {qproperty-pixmap : url(pixmap.png);}
             QPushButton {qproperty-iconSize : 20px 20px; }
             MyGroupBox { qproperty-titleColor: rgb(100, 200, 100); }
    ��ʽ���봰�ڻ����¼�
        ���⣬���ش��ڻ����¼��������������иı�ÿؼ�����ɫ��ͬʱ���ֶԸÿؼ���������ʽ��
        �������ʽ�������Ӱ��ؼ�����ɫ��������Ϊ��paint���ƺ����У������������ʽ��
        ����ʽ��������ڵ�����paint����֮��
        ���⣬������ʽ����setStyleSheetҲ���������������ػ档
    ��ʽ��ʹ�ý���
        ����ʹ��ȫ����ʽ�������Ǹ�ÿ���ؼ��ֱ�������ʽ��һ�Ǳ���ͳһ����
        ���Ǵ��ڲ�ʵ�ִ����Ϸ���������ֶദ������ʽ���ͻᴴ�������ʽ�����
        ���Ͷദ������ʽ�¼�����������ػ棬���Դ�Ч�ʷ��濼����������ദ������ʽ��
ģ����ͼ�ṹ
    ��MVC�Ĺ�ϵ
        MVC��������Ԫ�أ�(����)ģ�͡���ͼ�����ƣ��û��ڽ����ϵĲ�������
        QT��InterView��ܣ�����ͼ�Ϳ��ƽ����һ��ͳ��Ϊ��ͼ��
        ��������ģ��/��ͼ�ṹ��
        InterView��ܻ������˴���ĸ��
        ͨ���������Զ���������Ŀ(item)����ʾ�ͱ༭��ʽ��
    ģ�͡���ͼ������Ĺ�ϵ
        ���ݸı�ʱ��ģ�ͷ����ź�֪ͨ��ͼ
        ���û��Խ�������˲�������ͼ�ᷢ���ź�
    ģ��
        ������ģ�ͣ�QList������ջģ�ͣ�QStack����������򵥵�����ģ��
        �����ģ������֮���ƣ�ֻ����ά��������Ԫ��֮��Ĺ�ϵ������һЩ
        ����������Щģ���࣬���������ṩ���ڲ�����Ԫ�ص���ɾ�Ĳ�Ĺ���
        ���⣬ģ����һ�㶼���ṩ�����źŽӿڣ�
        ���ڲ����ݷ���ĳ���ض��仯��ʱ�򣬾ͻᷢ����Ӧ���ź�
        ģ�ͳ�������ͼ����ʹ���⣬Ҳ�ǿ��Ե���ʹ�õģ����ڼ�¼��������
        ���е�ģ�Ͷ�����QAbstractItemModel�ࡣ
        QAbstractItemModel
            QAbstractTableModel         ��ģ�ͣ�����ģ�����ֱ���ã�
                QSqlQueryModel
                    QSqlTableModel
                        QSqlRelationTableModel
            QAbstractProxyModel
                QIdentityProxyModel
                QSortFilterProxyModel
            QAbstractListModel          �б�ģ�ͣ�����ģ�����ֱ���ã�
                QStringListModel
                    QHelpIndexModel
            QStandardItemModel          ��׼ģ�ͣ�����ģ�����ֱ���ã�
            QHelpContentModel            
            QFileSystemModel            ��ģ�ͣ�����ģ�����ֱ��ʹ�ã�
            QDirModel                   ��ģ�ͣ�����ģ�����ֱ��ʹ�ã�
        QAbstractItemModel�����
            ������ģ�ͣ�QList������ջģ�ͣ�QStack����������򵥵�����ģ��
            QAbstractItemModel����֮���ƣ�ֻ����ά�������ݹ�ϵ������һЩ
            QAbstractItemModel���ṩ�ж��ڲ�����Ԫ�ص���ɾ�Ĳ�Ĺ��ܣ�
            ��insertRow��match��sort��index��columnCount��
            QAbstractItemModel�������࣬���Ƕ��ڲ�ά��������Ԫ��֮��Ĺ�ϵ
            �����˸�����һЩ�Ļ��֣������͡��б��͡�Ŀ¼�͵ȵȣ�
            ע�⣬���ÿ������ģ�ͣ�һ��Ҳ�ᶨ��ר�е������������Ԫ�أ�
            �Ӷ�Ϊÿ������ģ�͵�ר�еĹ�����ԣ��ṩ�ײ�֧�֡�
            ֵ��һ����ǣ�QAbstractItemModel���ṩ�˷����źŵ�������
            ���ڲ������ݷ���ĳЩ�仯ʱ���ᷢ���ض����ź���������Щ�仯
        QStandardItemModel����
            ά���������ݳ�Ա������ΪQStandardItem
                itemͨ���������֡�ͼ���ѡ���
                ÿ��item�������Լ��ı���ɫ�����塢ǰ��ɫ
                Ĭ�ϵģ�ÿ��item��enabled��selectable��checkable��editable
                ���ͨ������setFlags����������Щ���ԣ���Щ������
                ���Ե���setCheckState�ı���ѡ��״̬
                ÿ��item����һ����ά����item��ʹ����֧�ֲ㼶Ƕ�ף�
                    �ӱ�ͨ��setRowCount��setColumnCount�ı��С
                    ����ͨ��setChild��һ��item��ŵ��ӱ��У�
                    ��ͨ��child��ȡ�ӱ�item��ָ��
                    ���⻹֧��insertRow,insertColumn,appendRow,appendColumn��
                    removeRow,takeRow,removeColumn,takeColumn,sortChildren��
            ʹ�ø�ģ�ͣ�����Է����ʵ�ֳ�һ����ģ��
                ʹ��appendRow�����Խ����items����ģ����
                ʹ��item����ĳ��item
            Ҳ���Է����ʵ�ֳ�һ����ģ��
                ͨ������ĳߴ紫�ݸ�QStandardItemModel���캯����
                ��ʹ��setItem��������Ŀ��λ������
                ���Ե���setRowCount��setColumnCount���ı��ĳߴ�
                ���Ե���insertRow,insertColumn,removeRow,removeColumn
            ʹ��setHorizontalHeaderLabels/setVerticalHeaderLabels���ñ�ͷ
            ��ʹ��findItems��λԪ�أ�ʹ��sort����ʹ��clear���
        �̳г����ģ��
            ��Ϊ���е����������ǲ�ȷ���ģ�����������֡����ֻ�ͼƬ��
            �������ݴ洢ά��Ӧ���Ƕ����ڼ̳����еġ�
            �̳�ʱ����ʵ��rowCount(),columnCount(),data()����������
            ��������ʵ��headerData()����--
            --��Ϊ��ͷ�ǲ����ڱ��еģ����Բ���ͨ��data()/setData()���ʡ�
            �����ģ��֧�ֱ༭���ܣ���Ӧ��ʵ��setData()������
            ��ʵ��ʵ��flags()�������ú�������ֵ�����Ŀ�Ƿ�ɱ༭��
        �̳г����б�ģ��
            ��������rowCount(),data()����������
            ��������ʵ��headerData()����
            �����ģ��֧�ֱ༭���ܣ���Ӧ��ʵ��setData()������
            ��ʵ��ʵ��flags()�������ú�������ֵ�����Ŀ�Ƿ�ɱ༭��
            �����֧���б�������Ŀ����Ӧ��ʵ��insertRows()��removeRows()��
                ʵ��insertRowsʱ���ڽ��в嵽�ṹǰ��Ӧ�ȵ���beginInsertRows()
                ֮��Ӧ��������endInsertRows()
                ʵ��removeRows()ʱ��ͬ������beginRemoveRows��endRemoveRows
                ��������Ϊ���ܹ���ģ�ͱ仯ʱ���Զ�֪ͨ��������ͼ��
        QDirModel��QModelIndex
            QDirModel��һ�������֮�󣬾����ڹ��캯����ö���˸�Ŀ¼�µ������ļ�
            ��QDirModel��ϵ���е���QModelIndex
                QModelIndex��¼ģ����Ԫ�ص�����ֵ��
                ����һ������·���õ�һ��������
                Ҳ���Ը���һ�������õ�һ������·����
                �������������QDirModel���Ի�ȡ�ļ��ķŶ���Ϣ��
                �����֡�ͼ�ꡢ�ļ���Ϣ��
                Ҳ�ɸ����������ɾ���ļ����ж��Ƿ������ļ�����Ϊֻ���ȡ�
            QDirModel���ڱ��߳���ִ�е�
                ������ö����Ŀ¼ʱ�����ܻῨ����ǰ�̣߳�
                ���½�����ʱû����Ӧ��
            QDirModel�����к��еĸ���
                �д�����ǵڼ���·����  ---����
                    ��C�̻�D�������ĸ�Ŀ¼���ǵ�0��·����������=0��
                    ��C:/123��һ��·����������=1��
                ����ģ���У�QModelIndexû��ʹ���У�����0��
                ����ģ���У�������Ŀ¼/�ļ�������parent()��
                �д�����Ǹ��ļ��ǵ�ǰĿ¼�µĵڼ����ļ���������ʽ�йأ�
                    ��C��һ���ǵ�0���ļ���������=0��
                    ��D��һ���ǵ�1���ļ���������=1
        QFileSystemModel��QDirModel������
            QFileSystemModel��ӵ�ж����̵߳�
                �����ļ�Ŀ¼�Ļ�ȡҲ���첽��ʽ��
                ���磬���㴴���� QFileSystemModel�Ķ���
                ����setRootPath��rowCount����ֵ��Ȼ�� 0��
                ��Ϊö��Ŀ¼�Ĳ������첽�Ŀ��ܻ�û��ʼ�أ�����QDirModel��һ��
            ��Model����Ŀ¼�����б仯��ʱ�� 
            ��ͨ��һЩModel���ź�֪ͨ�����ڵ�ItemView��
            �Ӷ��������첽��Ŀ¼ö�ٹ��̡�
            ����һ���ô����� QFileSystemModel�����˶�Ŀ¼�仯�ļ��ӣ�
                ����ͨ�� QFileSystemWatcher ����ʵ�ֵģ�
                ������QFileSystemModel�Ͳ��õ���Ŀ¼�ļ��仯�ˣ�
                ���б仯����ItemView��Ȼ���յ����µ��źš�
        QSortFilterProxyModel���
            ����֮���Գ�Ϊ����ģ�ͣ�����Ϊ����������������ģ�ͣ���ֻ�ǹ�������ģ�ͣ�
            ���仰˵����������item���ݣ������Ǵ������ˡ��������ݣ�
            ����ҪsetSourceModel������������ģ���������
            ֮����ͼ�ؼ�����ֱ�Ӹ�ԭʼ����ģ�Ͱ󶨣�������ô�������ģ�Ͱ󶨡�
            �ô���ģ��ͨ������filterAcceptsRow���������ݴ�����int sourceRow,
            ��ȡģ����Ӧ�ڵ��ֵ��ͨ������boolֵ�������Ƿ�Ѹ���(��)���˵���
            ��������ʱ�����ڸı���������ο�ֵ����Ա�������󣬵���invalidateFilter
            ���ߴ���ģ�͹��������Ѹı䣬ģ���ڲ�����filterAcceptsRow������
            ���¹��˺�����ݣ��������ָı䷴ӳ����ͼ�ؼ��ϡ�
    ��ͼ
        ������ͼ�඼����QAbstractItemView
        QAbstractItemView
            QTreeView          ��
                QTreeWidget
            QHeaderView
                QUndoView
                QListWidget
            QListView          �б�
                QUndoView
                QListWidget
            QColumnView        �����б�
            QTableView         ��
                QTableWidget
    ����
        ����Ļ���ΪQAbstractItemDelegete
            QAbstractItemDelegete
                QItemDelegate
                    QSqlRelationalDelegate
                QStyledItemDelegate
    ģ������
        Ϊ�˱�֤���ݵĴ�ȡ�ͱ�ʾ�ķ��룬InterView������ģ�������ĸ��
        Ҳ����˵��ģ����������ϵģ������ͼ��Ŧ����
        ÿ����Ϣ��Ŀͨ��ģ����������ȡ����ͼ�ʹ���ʹ����������ȡ���ݡ�
        ͨ��ģ����������ȡ������Ŀ���������������ԣ��кš��кš���������
            �б�ģ�͵�������ֻ�õ�������
            ��ģ�����������õ��к�������
            ��ģ�����������õ��к͸���������
        ģ������ֻ���ṩ����ʱ�����Ĺ��ܣ���Ϊ����ģ���ǿ��ܻ�ı�ģ�
        ģ�Ϳ��ܻ���ڲ��Ľṹ����������֯����ʱģ��������ʧЧ��
        �������Ҫ����ʹ�ã�����ʹ��QPersistentModelIndex������ģ��������
    ��������ͼ��ģ�͵Ŀؼ�
        ��QListWidget��QTreeWidget��QBableWidget��
        ���Ǽ�������ͼ��ģ�͵Ĺ���
        ʹ����Щ����Ȼ��㣬��Ҳʧȥ��ģ��/��ͼ�ṹ������ԡ�
    ����ģ�ͺͿؼ�
        ����tableView��listView�����Ŀؼ����ǿ���ͨ��setModel������
        ��ģ�ͽ��й����ġ�
        ���������һ��QLineEdit��QLineEdit��QLabel�����Ŀؼ���ģ���������
        ��ʲô�취�أ� ��������ʹ��QDataWidgetMapper�࣬
        ͨ��������addMapping(QWidget *widget, int section)��
        addMapping(QWidget*widget,int section,QByteArray &propertyName)
        ���������ɽ�ģ�������������Ŀؼ����й���
        widget��������Ҫ�����Ŀؼ���section����һ�������Ӧģ���еĵڼ���
        ���ڶ�Ӧ�ڼ��У������ͨ��setCurrentIndex(int index)����
        propertyName��������ָ��ʹ��ģ����ȡ���������޸Ŀؼ���ʲô���ԣ�
        �����ʹ�øò�������Ĭ���޸ĵ��ǿؼ����������ԡ�
        ���⣬�����ģ�͹�����һ����������ı����ϣ�
        ����Կ����޸��ı�������ʱ��Ҫ��Ҫͬ����ģ����ȥ��
        ����ͨ��setSubmitPolicy(SubmitPolicy policy)������ͬ�����ԣ�
        ������Զ�ͬ�������ı�����޸ģ����Զ�ͬ������Ӧ��ģ����Ŀ�У�
        ������ֶ�ģʽ���������submit�����󣬲Ż��ı�������ͬ����ģ�͡�
        ע�⣺һ���ؼ�ͬʱֻ�ܹ�����һ��ģ�ͣ�
        һ��ģ���е�item��ͬʱֻ�ܹ�����һ���ؼ���
    ����
        ��setItemDelegate�����Է��������ࣨ�������ࣩ�д˳�Ա������
            QAbstractItemView
            QDataWidgetMapper
            QFileDialog
            QComboBox
        listView��tableView��treeView�ȿؼ�������ֻ�ǰ��С�����
        ��ʽչʾ��һЩ�����ռ䣬���ͷ��չ����ť�������ߵȣ�
        �����嵽ÿ��item���ݵ���ʾ��ȫ�ǿ�����չ�ֵģ�
        ��������Ŀ����Ϊ���ÿؼ���ʹ�����ܹ������ɵĶ���item��չʾ��ʽ��
        Ĭ�ϣ�������QItemDelegate�����������
        ����̳���QAbstractItemDelegate��
        ��ʵ����paint()��sizeHint()�ȱ�Ҫ������
        ����Ҳ���Լ̳и��࣬����������Ҫ�Ĵ����࣬
        ��Ϊһ���ؼ������µĴ�����ʱ��ԭ�еĴ����ཫ�������
        QAbstractItemView�����Զ��������������Ϊ�Լ����Ӷ���
        ���Ե��ɵĴ����౻�����ʱ���������ֻ�Ǳ���������������Զ�ɾ��
        ��ô��
            createEditor 
                ��������item��ĳЩ�������ʾΪ�ض��Ŀؼ�ʱ���������ظ÷���
                ���༭ĳ��Ŀʱ���Ż���õ��÷���
                �����ʹ��option������column��row������Ϊ����������
                �����Ƿ�Ҫ�����¿ؼ�������ʲô����´���ʲô�ؼ���
                Ҳ����ʹ��item��data(Qt::DisplayRole)��Ϊ��������
            setEditorData 
                ���ظ÷�������ģ�������е�����չ����item��
            setModelData
                ���ظ÷�������item�е����ݣ��༭�󣩻ش浽����ģ����
            paint
                һ�㲻���ظ÷�����ע��paint�����ļ���������������const��
                ���Բ����޸���Щ���������Ҫʹ�ã��ɸ��ݲ�������һ���ڲ�����
                ��ֱ�ӵ���painter�����Ļ��Ʒ������������ڱ������ƣ�
                ������ʱ����һ�����⣬���϶�������ʱ�������Զ����ø÷�����
                ���Իᵼ����ʾ������ң��ɿ������źŲ۽���������������������
            updateEditorGeometry
                ��������������ô����Ŀؼ������������ľ��Ǵ����Ŀؼ�����λ��
                һ����editor->setGeometry(option.rect);
    ֧���Ϸ�
        �����QListWidget��QTableWidget��QTreeWidget��
        ����ֱ�ӵ������·���ʹ��֧���Ϸ�
            setSectionMode(QAbstractItemView::SingleSelection);
            setDragEnabled(true);
            setAcceptDrops(true);
            setDropIndicatorShown(true);
        �������ͼ-ģ��֧���Ϸţ���������ͼ�е������Ϸ����⣬
        ����Ҫ����ʵ��ģ�͵���ط������ξ�ͨQt4��� ��2�� 481ҳ��
        �ؼ�������������mimeData��dropMimeData,
        ǰ�����϶�ʱ��item���ݷ�����а壬
        ������������ʱ���Ӽ��а�ȡ���ݷŵ�ģ��item��
    ѡ��
        ʹ��QAbstractItemView::setSelectionModel(QItemSelectionModel*)����ѡ��ģ��
        QItemSelectionModel֧��setModel(QAbstractItemModel*)������ģ�͹���
        select(const QModelIndex&, QItemSelectionModel::SelectionFlags)
        select(const QItemSelection&, QItemSelectionModel::SelectionFlags)
        setCurrentIndex(const QModelIndex&, QItemSelectionModel::SelectionFlags)
        ���������������Կ���ѡ������
        ��ѡ�����仯ʱ��QItemSelectionModel�ᷢ����Ӧ�ź�
        ��������У�QItemSelection��һ������QModelIndex topLeft:bottomRightȷ���ķ�Χ
        ��֧��merge���������԰ѱ��QItemSelection�ϲ�����ǰQItemSelection        
�༭���Զ���ȫ
    QCompleter����ΪQLineEdit��QComboBox�ṩ�����Զ���ȫ���ܣ�
    �������ؼ�֧��setCompleter(QCompleter*)������
    ��QCompleter����֧��setModel(QAbstractItemModel*)��
    ����ָ��������ģ��Ϊ���գ�Ϊ�ؼ��ṩ���뽨�顣
    ����
    QDirModel * dir_modle = new QDirModel(this);
    QCompleter *comp = new QCompleter(this);
    comp->setModel(dir_modle);
    ui->lineEdit->setCompleter(comp);  
ʵ�ֳ���/��������
    �Զ�����Ӧ�ĳ��������࣬�̳���QUndoCommand�࣬
    �̳�ʵ��void undo(); void redo(); ����������
    ����QUndoStack��Ա��������������־Ϳ��Կ������Ǹ�ջ�ṹ
    ֧��ջ����push(QUndoCommand *cmd), ��undo()/redo()������
    createUndoAction/createRedoAction������
    �����ڵ���redo��redo��ͬʱ��������һ��redo��undo��QAction
    ʹ�����ӿɲο�����ͨQt4��� ��2�桷452ҳǰ��   
ͼƬ������2D��ͼ
    QPainter
        ֧�ֻ��Ƶ㡢�ȡ����Ρ�����Ρ�·���ȣ�
        �ߺ�����ʹ��QPen���л��ƣ���ˢ(QBrush)�������
        ���ʶ������͡���ȡ��ʼ⡢�˵㣬
        ��ˢ�������ģʽҲ��ɫ
        ʹ��QFont����������ֵ�����
        ��������Կ�ͨ��QFontInfo���ȡ
        ����Ķ���ʹ��QFontMetrics���ȡ
        QFontDatabase��ɵõ�ϵͳ��֧�ֵ�������Ϣ���б�
        QPainterʹ��RenderHint�������Ƿ񷴾��
        QPainter����QPaintDevice *��Ϊ��������Ϊ������
    QImage
        �̳���QPaintDevice���Ż���I/O����������ֱ�Ӳ�����������
        ������QPainterֱ����QImage�ϻ�ͼ��
        ���˻�������(QFont�����ײ� GUI),�������Ʋ����������߳������
        ��������߳��л������֣�������QPainterPath
        QImage���������ʽ��������
        QIamgeͨ��scanLine����ָ���е�����
        bits()�������ص�һ�����ص�ָ�룬ÿ��������QImage�ж�����������ʾ��
    QPixmap
        �̳���QPaintDevice����Ҫ��������Ļ����ʾͼ������
        Ҳ�ܶ�ͼ�����һЩͼ��任�������š����֡����Ρ�
        ���Է�����QImage��ת����windows�ϣ�QPixmap������HBITMAP��ת
        QPixmap��Ҫ������Ļ��̨��������ͼ��
        QPixmap���������QLabel(pixmap)��QAbstractbutton(icon)������ʾ��
        QImage���������ʽ��������
    QBitmap
        ��QPixmap�̳У�ֻ�ܴ����ֵͼ�񣨵�ɫλͼ��
    QPicture
        �ǿ��Լ�¼���ط�QPainter�������
    QPainterPath
        ͼ���ࣨ���Ρ���Բ��ֱ�ߡ����ߵȣ�
        QPainterPath�����ִ�и��ֻ���ͼ�ε�����
        QPainter��drawPath�������ɽ���QPainterPath����
        ��ͼ·��������䡢��ʾ�������ü���
        ʹ�þ�����
          QLinearGradient myGradient;
          QPen myPen;
          QRectF boundingRectangle;
          QPainterPath myPath;
          myPath.addEllipse(boundingRectangle);
          QPainter painter(this);
          painter.setBrush(myGradient);
          painter.setPen(myPen);
          painter.drawPath(myPath);
    ͼ���ϣ�ͼ�����ģʽ��
        ֻ֧��ARGB32��ARGB32_premultiplied��ʽ,����ʹ�ú���
        �����˻��ģʽ�󣬶����еĻ�ͼ��������Ч���续�ʡ���ˢ�����䡢ͼƬ
        ���ģʽ�Σ�QPainter::CompositeMode
        ��ػ���㷨�ξ�ͨQt4��� �ڶ��� 202ҳ
    ����任
        Qt��������QPainter���ƣ�ͬʱҲ��QPaintDevice��QPaintEngine�����
        QPaintdevice�������л�ͼ�豸��Ļ��࣬
        QWidget��QPixmap��QImage��QPrinter�ȶ��������ࡣ
        QPainter����QPaintDevice�ϻ滭������֮�����ӳ���ϵ
        ͨ��QPainter��scale()��rotate()��translate()��hsear()�Ⱥ�����
        ���Ըı���ӳ���ϵ��
        ���б任�����ı任�������ͨ��QPainter��worldMatrix()����ȡ��,
        QPainter��save()��restore()��������ѹջ�͵�ջ��ǰ�ı任����
        ���Կ����ڽ��б任ǰ��ѹջһ�£�Ҫ�ָ�ʱ��ֻ�赯ջ���ɡ�
        Ϊ��ʵ�ָ����ӵı任������ͨ��setMatrix���ñ任����
����
    QFont��ʾ���壬�������������ʱ��qt��ʹ��ָ�������壬
    ���û�У����Ѱ��һ����ӽ����Ѱ�װ���塣
    ������Ϣ��ͨ��QFontInfoȡ��
    QFontMetrics����Ի��������������
    exactMatch���������жϵײ㴰��ϵͳ���Ƿ�����ȫ��Ӧ������
    QAppliction��setFont������������Ӧ�ó����Ĭ������
    ������Ϣ�ο���ͨQt4���P184
�Ϸ�
    ͨ��QApplication::startDragTime�����û��������೤ʱ��ſ�ʼһ���ϷŲ�����Ĭ��500ms
    ͨ��QApplication::startDragDistance��������ƶ��������زſ�ʼ�϶���Ĭ��4pix
    ��Ϊ�϶���Դ
        ��mousePressEvent������
        QMimeData *mimeData = new QMimeData;
        mimeData->setText(...);
        QDrag *drag = new QDrag(this);
        drag->setMimeData(mimeData);
        drag->setPixmap(�϶�ʱʹ�õ�ͼƬ);
        Qt::dropAction act = drag->start();
        QMimeData��MIME�������ݵ�һ�������࣬���а����Ҳ���õ�����
        QMimeData�п��Դ�ţ�ͬʱֻ����һ�֣�image/text/html/urls/����������
        Qt::dropAction�Ǹ�ö��ֵ,��ʶ���ƶ����ݡ������϶����ݵ�
    ��ΪĿ�ĵ�  
        ���ȵ���setAcceptDrops(bool)���ô��ڲ����Ƿ�ӿ��Ϸ�
        ���֧�֣�����̳�ʵ��dragEventEvent��dropEvent�����¼�����
        dragEventEvent��������Ŀ��widgetʱ������
        ����QDragEnterEvent* event������
            QDragEnterEvent�̳���QDropEvent�������̳���QEvent
            QMimeData * p = event->mimeData();
            Ȼ���жϴ����������Ƿ����Ҫ��
            ���ϵĻ�����event->accept(),����event->ignore();
            ǰ������һ��accept��ǣ�QEvent�ķ�������
            �����¼��Ľ�������Ҫ���¼���
            ��������¼����ܱ�������widget��
            ���߻Ὣ����ɽ����Ϸŵ���״��
        dropEvent��������QDropEvent*event����
            QMimeData * p = event->mimeData();
            �õ�QMimeData�е����ݣ������ÿؼ�ʹ�ø�����
            ��Ҫ������Ȼʹ��event->accept()��
            ������¼��������������widget��
            �����ڲ����ϵ��������ͣ�����event->ignore()
    ��Ϊ���϶��Ķ���
        Ϊ�˽������������ݣ���ʵ��dragMoveEvent��dropEvent����
    �����µ��ϷŲ�������      
�ļ�����
    ��ȡ�ļ���Ϣ
        ͨ��QFileInfo�����Ի�ȡ�ļ������ļ�·������ȡȨ�ޡ�
        �Ƿ�ΪĿ¼��������ӡ��ļ���С��������ʱ�����Ϣ��
        ��Щ��Ϣ�ᱻ���棬������뻺�棬ʹ��setCaching(false)
        �����ļ������м䱻�ı䣬���Ի��ṩ��refresh����
    �����ļ��仯
        ʹ��QFileSystemWatcher�������ļ���Ŀ¼�ĸı�
        ͨ��addPath��addPaths����������һ�������ļ�/Ŀ¼
        �����ӵ��ļ����޸Ļ�ɾ��ʱ���ᷢ��fileChanged�źš� 
�����߳�
    �����̵߳ķ���
        ��https://www.cnblogs.com/findumars/p/5641570.html
        ����һ���̳�QThread
            1.�̳�QThread������ʵ��run����
            2.����QThread�������ʵ��
            3.����ʵ����start���������̡߳�
            ??����ʵ����terminate���������߳�
            ??����terminate�󣬲���������ֹ����̣߳�����ȡ����ϵͳ�ĵ��Ȳ���
            ??����wait�����ȴ��̰߳�ȫ�˳�
            ��ע�����terminate�������߳�ִ�е�����һ����ֹ�����²���Ԥ֪�ĺ�����Բ��ᳫʹ��
        ���������̳�QRunnable
            1.�̳�QRunnable�࣬ʵ��run����
            2.ʹ��QThreadPool::globalInstance()->start(QRunnable*)����һ���߳�����
            ˵��
                QRunnable�಻�̳��κλ��࣬������û���źŲ۵�����
                QRunnableĬ�����Զ�ɾ���ģ�����ͨ��setAutoDelete�����޸�
                QThreadPool���Զ�ͬһ��QRunnableʵ����������߳�ִ��
                ��QThreadPoolִ�������һ��QRunnableʵ��ʱ����������Զ�ɾ���ģ���QThreadPool��ɾ����
                ÿ��qt������һ��ȫ�ֵ�QThreadPool���󣬿�ͨ��QThreadPool::globalInstance()��ȡ��ָ��
            ��ȱ�����
                �����̳߳ؼ�����QThreadPoolά���̳߳ض��У�������ǰ�����̵߳���Ŀ
                ʹ�� QThread::idealThreadCount()����֪���̳߳�Ĭ��ʹ���˶��ٸ��߳�
                һ���������ã�qt��ѡ�������̸߳�������ȻҲ����ͨ��maxThreadCount�����ֶ�����
                ��ȱ������޷��ֶ�ǿ�ƹ�ͣĳ��QRunnable����ΪQRunnableֻ����������е�һЩ����
        ��������ʹ��moveToThread
            ����QObject�еķ�����void QObject::moveToThread(QThread *targetThread)
            ��������Ĺ����ǽ���ǰ��(�̳���QObject���Ҳ�����parrent)����children�Ƶ�����ָ�����߳���
            ʹ�þ�����
                QThread thread;
                thread.start();              
                Worker work;                    //Worker�Ǽ̳���QObject�Ķ���
                work.moveToThread(&thread);     //��Worker������thread�߳�
                ֮��work������¼���������thread�н��У����仰˵
                ���źŴ���work�еĲۺ���ʱ���òۺ�������thread��ִ�е�
                ע��QThread���������ڲ���С��Worker���������ڣ���������ǰ������
            ���moveToThread��������0����ζ��û���߳���ִ��work�б��źŴ����Ĳۺ���
            �÷������Ƽ�ʹ��
        �����ģ�QtConcurrent::run
            QtConcurrent�Ǹ������ռ�(qt4.4��ʼ����)�����ṩ����һЩ�߲�api��
            ����ȡ������������д���������������ź����ȵײ������
            QFuture<T> run(QThreadPool *pool, Function function, ...)
            QFuture<T> run(Function function, ...)  //��ͬ�ڽ������pool��ֵΪQThreadPool::globalInstance()
            ʹ���̳߳�ִ��ָ���ĺ�����ע����Ϊ�̳߳�������еĹ�ϵ���������ܲ�������ִ��
            run������function������������Ǹ�������ָ��(��������)��
            run��������...������ʵ����qtΪ��ͬ�����Ĳ��������˲�ͬ��run���������֧��5��������
            ����ֵQFuture�࣬���ڱ�ʾ�첽����Ľ����result�������ڻ�ȡ���ؽ����
            pause()��resume()��cancel����������ͣ���ƣ�waitForFinished���ڵȴ��߳̽�����
            ע��result��waitForFinished����������������������ֱ���п��õķ���ֵ���߳̽�����
            ���̳߳�һ����ͨ��QtConcurrent::run�����������߳��޷��ֶ�������
    �̵߳Ļ�����ͬ��
        ������QMutex
            QMutex�ṩ��һ�ֱ����ٽ����ķ�����ÿ��ֻ����һ��(�߳�)��������ٽ���
            ����̶߳��ɷ���ͬһ��QMutex���󣬵�ֻҪ��һ���߳�lockס�ö���
            �����߳���lockʱ���ͻῨס��ֻ�е�֮ǰlock�ɹ����߳�unlock֮��
            �Ż����µ��߳�lock�ɹ���
            QMutex���ṩtryLock��������������������ѱ������߳����������������ء�
            QMutexLocker�Ǹ�����QMutex�Ĺ��ߣ�QMutexLocker(QMutex*)��
            ���ڹ���ʱ�������mutex��lock����������ʱ�Զ�����unlock������
            QMutex�Ĺ��캯������ָ��һ��RecursionMode������
            �����QMutex::Recursiveģʽ����һ���߳̿��Զ�ͬһ��mutex������Σ�
            ����ֻ���ڽ�����Ӧ������mutex�Ż���������
            ������� QMutex::NonRecursive��Ĭ�ϣ�����ֻ��ͬʱ����һ�Ρ�
            ��Ա������                
                void lock()
                void unlock()
                bool try_lock()
                bool tryLock(int timeout = 0)
                bool try_lock_for(std::chrono::duration<Rep, Period> duration)
                bool try_lock_until(std::chrono::time_point<Clock, Duration> timePoint)
        ��д��QReadWriteLocker
            ����QMutex����ʵ���Ǹ�����ռ/����������
            ����Ϊ��ռ��������ʱ�������߳��޷�����Ϊ��ռ����������������ֻ�ܵȴ�
            ����Ϊ�������������ǣ������߳̿�����Ϊ���������ٴ���������������Ϊ��ռ��������
            QReadLocker/QWriteLocker�����QMutexLocker���Ǹ�ʹ�ö�д���ĸ���С���ߣ�
            �ڹ���ʱ����д��������������ʱ����д���Զ�������
        �ź���QSemaphore
            ��Ա������
            QSemaphore(int n = 0)           
            void acquire(int n = 1)  //����һ����������Դ����Դ��������ʱ����
            void release(int n = 1)  //�ͷ�һ����������Դ
            bool tryAcquire(int n = 1)  //������ȡ����Դ��������ʱ����ʧ�ܷ���
            bool tryAcquire(int n, int timeout) //ͬ�ϣ�ֻ�����и���ȴ�ʱ��
            int available()          //���ص�ǰ���õ���Դ����
            ע��release�������Դ�������Դ������QSemphore�ڹ���ʱָ��ֻ��0����Դ
            �Կ���֮��ʹ��release����������n��������Դ��
        ��������QWaitCondition
            ��������������һ�ǻ��⣬���ǵȴ���
            ��������Ϊ�̼߳���ڹ������ݣ��ȴ�������Ϊ�̼߳����������
            ǰ��Ĺؼ��κͶ�д�������ǽ���̶߳���Դ�Ļ���������⣬
            ��������������Ϊ�˽���߳����������⡣
            Ϊ�˷�ֹ�����������������Ǻ������ؼ���/��д����һ��ʹ�á�
            ��Ա������
                void wakeOne()
                void wakeAll()
                void notify_one()    //Ϊ������STL����ͬ��wakeOne
                void notify_all()    //Ϊ������STL����ͬ��wakeAll
                bool wait(QMutex *lockedMutex, unsigned long time)
                bool wait(QReadWriteLock *lockedRWLock, unsigned long time)
            ��wait������˵����
                ��������Ὣ�������������ȴ��������ⰵ����һ��ǰ�ᣬ
                ����Ϊ��������������������������ȱ������ģ�
                �������������ǿ��ظ������ģ���wait�����������أ�
                Ȼ�����������ɽ���״̬������ǰ�߳���ᱻ����
                ������ǰ�̷���wakeOne��wakeAll�źţ�
                ���ߵȴ�ʱ�䳬ʱ����ǰ�߳̽����ٱ�����
                �������Ϊʱ�䳬ʱ�������ȴ�����wait����false
                wait���غ��������ص�֮ǰ������״̬
                ����ζ�ţ�����ǿ��ظ����������������ұ��Ϲ�3������
                ���������������������δ����״̬��
                ���������غ��������ָ�Ϊ3������״̬��
            ���������Ĺ�ϵ
                �����Ա�����ɼ��������������ܵ���ʹ�ã��������������ʹ��
                ����һ�Ƕȣ�������Ϊ����������Ϊ����������������ǿ���ߣ�
                ������Ϊ�����ڶ�������������������������������ȴ�һ��������
                �����ڶ���Դ��Ϊ0���ź�������aqure������
                �Ӷ�����A�̵߳ȴ�����cpu�ø������̣߳�
                ������ĳ��B�߳���ִ�к�ʹ�������������ˣ��Ϳ�ִ�л��Ѳ�����
                �����ͷ��ź�����Դ���Ӷ�ʹ�õȴ���A�߳̽����ȴ�
            �����൱���ͷ��ź�����Դ
        �ź��� vs ������ vs ��������
            ������������Ϊ����Դ��Ϊ1���ź���
            ���������ǿ���ǿ�����������ܵĹ���
            �������� �� QMutex.lock + QSemaphore(0).acquire + QMutex.unlock
    �̵߳����ȼ�����
        ���и����ȼ����̱߳����ȵ���
        ���̻߳���QThread����setPriority(Priority priority)����
        Ҳ������QThread��start������ָ�����ȼ�������
        ��0-7�˸����ȼ���qtĬ��Ϊ7������ϵͳĬ��Ϊ3��
        ��0��6���ȼ��������ߣ��������ȼ�Ϊ7ʱ�����ʾ�̳д����̵߳����ȼ���
        ע�⣺Linux�µ�qt�߳�û�����ȼ�֮��
            ��Linuxϵͳ�У��߳���ѭPosix��׼��posix��3�е��Ȳ��ԣ�
            ���е��������������ȼ����ƣ��������ֵ��Ȳ��Զ�ֻ����root�û���ʹ��
            ����һ�ֵ��Ȳ���û���������ȼ����ƣ����ֵ��Ȳ����κ��û�����ʹ�ã�
            ����Linux��Ĭ�ϵ��Ȳ��ԣ���Qt����ʹ�õ����ֵ��Ȳ��ԣ�
            ��û���ṩ���ĵ��Ȳ��Եķ���
            �����ζ����linux�£���Ȼ����Ϊ�߳������˲�ͬ�����ȼ���
            ���ⲻ�����ã����е��߳���Ȼ������ͬһ���ȼ��¡�
    �߳���������
        ������ǰ�᣺��һ������û������������ڶ�����������δ�����ȴ�������
    ���ȼ���ת����
        һ�������ȼ��̺߳�һ�������ȼ��̵߳ȴ�ͬһ������
        ����������ȼ��߳��õ������������ȼ��߳̾͵õȴ������ȼ��߳�
        ���Ǻ���ģ�����������ȼ��߳��ڵ�ǰcpuʱ��Ƭ����ʱ��û�ͷ�����
        һ����ʱ�ϳ��������ȼ��߳̾Ϳ���һֱռ��cpu��
        �������������ȼ��̵߳ò���ִ�У����������ȼ��߳�Ҳ��Ϊ���ȴ����ò���ִ����
        ֻ�ܰװױ�������������ȼ��߳�
        ����������к�ǿ�������Ժ�ż���ԣ�������ֻ�ܾ���ע�Ⲣ�������������
    �̱߳��ش洢
        �и��̱߳��ش洢�Ĳ�����ʹ��ȫ�ֵ�QMap<thread_id,thread_data>
        qt�ṩ��QThreadStorage�����ڴ洢�̵߳ĵ������ݡ�
        ��Ա������            
            bool hasLocalData() const
            T &localData()
            T localData() const
            void setLocalData(T data)  //Tֻ��Ϊָ�����ͣ���ͨ��new�ڶ�����䣩
            QThreadStorage��ӹ�data�����߳��˳����ٴε���setLocalDataʱ���Զ��ͷ�dataָ��
    GUI�߳����GUI�߳�
        ���н����Qt�����У����߳���GUI�̳߳䵱����qtֻ����һ��GUI�߳�
        ������ʱ�Ĳ���Ӧ���ɷ�GUI�߳���ɣ���֤����ʵʱ��Ӧ
    �̼߳�ͨ��
        ���������̰߳�ȫ
            ����������
                ���һ�������ܱ�����߳�ͬʱ���ã���Ϊÿ���߳��ṩһ�ݵ���������
                �����������ǿ�����ġ������뺯�����̰߳�ȫ�ġ�
                һ��������ֻ���ܱ������̴߳�ϣ������ܱ��жϺ�����ϡ�
                Ҫ�뺯�������룬��Ȼ����ʹ��ȫ�����ͱ�����̬��������ֻ��ʹ�þֲ�����
                ����Ҳ���ܷ���ȫ�����͵���Դ�����ĳ���ض�·�����ļ����ж�д������
                ע�⣺���һ���̵߳�����malloc/free����������������ǲ�������ģ�
                ��Ϊmalloc��ʹ��ȫ������������ģ����и�ȫ�ֱ�����¼����Щ��ռ�õģ�
                ������Щλ�÷����¿ռ䣬��Ϊ���malloc�����ڲ�ʹ����ȫ��������
                ���������ǿ�����ģ����ⲿ���������˲�������ĺ�����������ⲿ����Ҳ��������
                �ܶ��׼I/O�⺯����Ϊʹ����ȫ�����ݽṹ�����Ҳ�ǲ��ɳ���ġ�
            �����̰߳�ȫ
                ���һ��������ͬʱ������̵߳��ã��������еĵ���������ͬһ�����ݣ�
                ��α������ʱ���д�����ô������������̰߳�ȫ��
                ����λ�������ǣ�������ʹ����ȫ�����ͱ����������ٽ���Դ��
                ��ͬʱ�����������ƣ���֤��Щ�ٽ���Դֻ�ܱ���ͬ�߳�����ʹ��
                ע��ʹ��malloc��������Ϊmalloc�����漰ʹ��ȫ�ֱ���������Ϊ���̰߳�ȫ��
                ��Ҫʹ��������������������߳�ִ��malloc�ڼ��յ����ź��жϣ�cpu�ͻ�ת�������жϺ���
                ����жϴ�������Ҳ��malloc�����ҽ����ˣ���ʹ��ͬһ������malloc���б�����
                ������������ǿ�����ģ�����ͻ��ж���Ӧ�����������޷����أ����������
            �������
                ���һ�����е����к����ڸ���ʵ���пɱ�����߳�ͬʱ���ã���������ǿ������
                ���仰˵�����ǲ�ͬ�̸߳��Գ���(������)һ����ʵ����
                �����߳̿�����ʹ������е���ʵ�������õ��������̵߳Ĳ��������ʲôӰ�졣
                ����һ�������ʹ���˾�̬�������ⲿ��Դ����һ���ǲ�������ģ�
                ��������࣬��Ϊʹ���˽��棨�ⲿ��Դ��������һ���ǲ�������ġ�
                ���C++��ֻʹ������ĳ�Ա�����������Ȼ�ǿ�����ġ�
                �󲿷ֵ�Qt�ǽ�����Ҳ�ǿ�����ġ�
                һ��������룬�������������̰߳�ȫ�ġ�
                ��Ϊ��������޶�����ÿ���̸߳��Գ���һ����ʵ���������
                ���̰߳�ȫ���ע����̲߳���ͬһ����ʵ���������
                ͨ���κ�û�б�ȫ�����õ�C++�����ǿ�����ġ�---��ô��⣿Ϊʲô��
                ��������ֻ�ܱ�֤�����ڲ�ͬ�߳��в�����ͬ�Ĵ���Ķ����ǰ�ȫ�ģ�
                ���ܱ�֤����ͬ�̲߳���ͬһ����������ǰ�ȫ�ģ�
                �������Qt�ķ�ͼ�ν����඼����һ������̫�ϸ��Ҫ��
                ���Ƕ������ǿ�����ģ�����Ĳ�ͬʵ����ͬʱ���ڲ�ͬ���߳��У�
                �ܶ�Qt�ķ�ͼ���û������࣬����QImage��QString��һЩ�����࣬
                ��ʹ������ʽ������Ϊһ���Ż�������
                ��Ȼ�������Ż�ͨ���������ɲ�������ģ�
                ����Qtʹ��ԭ�ӻ����������ָ����ʵ���̰߳�ȫ���ü�����
                �������Qt����ʽ�������ɿ�����ģ�
                ֻ����һ���߳��У�һ�������̣߳�ʵ�������󣬲����������߳���ʵ��������Ķ���
                ����������ǲ�������ģ�����������ڲ�ͬ������ͬһ���ڴ浼�µ�
                ���е�QWidget���������඼�ǲ��������
                ����qt�еĽ�����ʵ��������ֻ�������߳��У� GUI�̣߳�
                ��Ҫ�����߳���ֱ�Ӳ������������Ҫʹ���ź���ۼ���������������
            ���̰߳�ȫ
                ���һ����������ͬʱ������̲߳���������������̰߳�ȫ��
                ��ͬ�̶߳�ͬһ����Ķ�����в�����
                �����ڲ�ͬ�̵߳���ͬһ����������Ա�������ǰ�ȫ�ģ����������ģ�
                ��˵���������̰߳�ȫ��
                Qt���̰߳�ȫ���������������������ź�����QThreadStorage<T>
        �߳����¼�ѭ��
            GUI�߳���Ψһ������QAppliction���󣬲��Ҷ�������exec�������߳�
            ��ʼ�̣߳�GUI�̣߳�ͨ��QCoreApplication::exec���������¼�ѭ����
            ����GUI�߳�ͨ��QThread::exec���������¼�ѭ����
            �Զ���ļ̳�QThread���࣬�ڼ̳�ʵ��run����ʱ���Լ������Ƿ����exec��
            �Զ����̶߳����start�����ڲ����ǵ��õ�run������
            ���run�в�����exec�����߳�ִ����run��������Զ�������
            �������exec�����̲߳������(run�������᷵��),��������exec�¼�ѭ����
            ����ע�⣬�Զ����̶߳���͸���ͨ��QObject����һ���������ڵ�ǰ�̵߳ģ�
            ֻ�����е�run���������������̵߳ġ�
            ��QCoreApplication���ƣ�QThreadҲ�ṩ�˳�����exit(int)��quit()�ۡ�
            ����һ��QObject�������¼����ɶ��������̵߳��¼�ѭ�������ɷ���
            ע�⣺���һ��QObject�������QApplication���󴴽�֮ǰ���죬
            ��ͨ��QObject::thread()�����鿴�������߳�ʱ���ᷢ���߳�idΪ0��
            �����䲻�����κ��̣߳����������Ķ����ǲ��ܴ����źŲ۵�
            ������ͨ��QObject::moveToThread()�����ı�QObject����������߳�
            ע�⣬������QObject�����и��������޷�ʹ��moveToThread������
        ���߳��е�QObject����󽻻�
            �����ֶ������̰߳�ȫ��QCoreApplication::postEvent()����
            �������̴߳����Ķ�������Ϣ�������Ϣ���ջᱻ���ɵ���Ӧ�̵߳�ʱ��ѭ����
            QCoreApplication::postEvent()��Ϊ���Ƿ��Ͷ�����Ϣ������ֱ�ӵ��ã�
            ����ֻ�����̵߳Ķ�������Ϣ��
            ���ʹ���¼�����������ע���ض���Ҫ�ͱ���ض�����ͬһ���̲߳��С�
            ���һ��QObject�Ͷ������ڱ������߳�ʹ�ã�����ʱ����һ���߳���ɾ���ö���
            ����ʸö���ĺ����ǲ���ȫ�ģ����Ҫɾ����Ӧ��ʹ��QObject::deleteLater,
            �ú����ᷢ��һ�����Ӻ�ɾ�����¼��������ղ�Ŀ��QObject�������̵߳��¼�ѭ������
            ע����̵߳���QObject����ʱ��ע�������������ʱ��������Ӧ�¼����������߳���
            �����õģ�������Ҫʱ��ע���̰߳�ȫ���⡣
            QObject�Ӷ���������丸���������߳��д�����������ʹ�������߳��еĶ�����Ϊ������
            �¼�������ֻ�����ڵ��̣߳����ʹ�����ʱ������������ģ���ࡣΪʲô������
        �źŲ����ӷ�ʽ
            ֱ����ʽ
                �ۺ����ڷ����źŵ��߳��б�����(��ʹĿ����������������̵߳�),
                ���ԣ�����źŷ�����������߲���ͬһ�߳�ʱ��ʹ���������ӷ�ʽӦע���̰߳�ȫ��
            �Ŷӷ�ʽ
                �����¼���Ŀ����������̵߳��¼�ѭ�������¼������յ�����Ӧ�ۺ�����
            �Զ���ʽ
                �ڲ��жϣ����Ŀ������ڷ����ź��߳��У���ʹ���Ŷӷ�ʽ����ͬ�߳��У���ʹ��ֱ����
    ���̴�������̼�ͨ��
        ʹ��QProcess  
            QProcess�����ǰ�Linux�ײ��������ص�API�������������ķ�װ��
            QProcess��������һ���ⲿ������֮ͨ�š�
            start�����ⲿ����
                ������QProcess�����ʹ��start���������ⲿ���򣬲���ָ�������в���
                start��QProcess�������롰����״̬��������ʱ���ⲿ����û�����ã�
                ���ⲿ���������ú�QProcess���롰����״̬����������started�źš�
                waitForStarted�����������ȴ���ֱ��started�źŷ�����
            ���½��̵ı�׼�������������
                QProcess�̳���QIODevice����ͨ��write�������½��̵ı�׼����д����
                Ҳ��ͨ��read/readLine/getChar�Ⱥ������½��̵ı�׼��������ݡ�
                һЩ����QIODevice*�����ĺ��������Դ���QProcess����
                ���½��̵������Ϊ����Դ����QXmlReader��
                �����½��̵ı�׼�����Ӧע�⣬���̾�������Ԥ��������ͨ��(stdout��stderr)��
                ����ͨ��serreadChannel���õ�ǰ�Ķ�ͨ������ͨ���пɶ�����ʱ������readyRead�ź�
                ����Ǳ�׼���ͨ�������ݣ���ͬʱ���ᷢ��readyReadStandardOutput�źţ�
                ����Ǵ������ͨ�������ݣ���ͬʱ���ᷢ��readyReadStandardError�źš�
                �ɷֱ���readAllStandardOutput��readAllStandardError������ȡ��Ӧͨ�����ݡ�
                ����QProcess�������������ͨ���ϲ������ñ�׼���ͨ�����������ڽ���ǰ��
                ����setReadChannelMode��������MergedChannels������
                Ҳ������closeWriteChannel��closeReadChannel�����ķ����Ѳ��õ�ͨ���رա�
                �ر�ͨ������Ӧͨ���Ķ�д������ʧ�ܡ�
                ���ɰ��½��̵��������ͨ��ӳ��Ϊ�����ļ���
                ���⻹����������waitForReadyRead��waitForBytesWritten��
                ���������ص�QIODevice����Ӧ������
            �����˳��ź�
                ���½����˳�ʱ��QProcess�ص���ʼ״̬��������״̬����������finished�źš�
                finished�ź�ͨ�������ķ�ʽ��Я���˽����˳�ʱ���˳�����˳�״̬��
                Ҳ����ͨ��exitCode��exitStatus������������ȡ��
                Qt���˳�״ֻ̬�����֣������˳�(0)�ͱ����˳�(1)��
                �������������в������󣨲���Ӧ���Ǵ����е���������setError�����ķ�������
                QProcess������error()�źţ�����ͨ��error������ȡ���һ�εĴ����룬
                ��ͨ��state()������ȡ��ʱ����������״̬��
                ���⻹����������waitForFinished��ֱ���е�finished�źš�
            �½��̻�������
                ��ͨ��setEnvironment��setWorkingDirectoryΪ�½������û��������͹���·����
        ���̼�ͨ��
            �����ϵĽ��̼�ͨ�Ű�����������ͨ�������ļ������ݿ⽻����Ϣ��
            ����˵�Ľ��̼�ͨ�ţ�����ָ����һ��Ч�ʵ�ͨ���ֶΣ�ͨ���в���ϵͳ�ں�֧�֡�
            ������ԣ�������Ϣ���С��ź���������洢��sock�ܵ��ȡ�
            Linux����ͨ�ŵ���Ҫ�ֶ�
                �ܵ��������ܵ�
                    �ܵ������ھ�����Ե��ϵ�Ľ��̼�ͨ�ţ������ܵ���ʹ�����н��̼�ͨ�š�
                �ź�
                    ��Ҫ����֪ͨĳ�¼������ˡ�
                ��Ϣ����
                    ��Ϣ����������POSIX��Ϣ���к�System V��Ϣ���С�
                    ��Ϣ���п˷����źų�����Ϣ���٣��ܵ�ֻ�ܳ����޸�ʽ�ֽ�������������С���޵�ȱ��
                �����ڴ�
                    ����Ч�ʵ�IPC��ʽ������������ͨ�Ż��ƣ����ź��������ʹ��
                �ź���
                    ��Ҫ���ڽ��̼�ͬ�����̼߳�ͬ��
                �׽���
                    ��ͨ�á����Կ��������ƽ̨��������
            Qt�Խ��̼�ͨ�ŵ�֧��
                �����ڴ� QSharedMemory
                    QShareMemory�����캯����Ҫָ��������������(�Զ���)��
                    Ҳ���Ե���setkey�������������ù����������֡�
                    ͨ��create(size)����������������֧��lock��unlock������
                    ͨ��data()������ȡ��������ָ�롣
                    ͨ��attach��detach�����Ѵ��ڵĹ���洢����
                �׽���   QLocalSocket��QLocalServer
                    ��windows�У�QLocalSocketʵ��Ϊ�����ܵ�����Unix��ʵ��Ϊ����socket
            ���ͽ��̼�ͨ��D-Bus
                D-Bus��һ�ָ��ߵĶ�������Ϣ����Э�飬���е���ʱ���Ϳ������ص㣬�ǳ��ʺϱ���ͨ�š�
                ���߻���
                    D-Bus�ɼ���������ɣ�����һ���־õ�ϵͳ���ߺͶ���Ự����
                    ϵͳ������һ��ʼϵͳ����ʱ���Զ����в���ϵͳ�ͺ�̨����ʹ�á�
                    �Ự�������û���¼�����������¼�û�˽�У������û�Ӧ�ó�����ͨ�š�
                    ���һ��Ӧ�ó�����Ҫ��ȡ����ϵͳ���ߵ���Ϣ��Ҳ����ֱ�����ӵ�ϵͳ���ߣ�
                    ����ʱ�����͵���Ϣ�յ����ơ�
                ͨ������ͨ��ʱ��Ӧ�ó���ɻ�ȡ�������õĶ�������
                ͬʱ�Լ�Ҳ��Ϊһ����Ծ�ı��������
                D-Bus�����������ж�Զ�ͨ������ĳ�������Ҳ������������������ֱ��ͨ�š�
                D-Bus���������
                    ��Ϣ
                    ������
                        ͨ������ͨ��ʱ����Ҫ�и����������Ӷ����Ա�ͬһ�����ϵ�����Ӧ�û�ȡ��
                        �е�����ip�������������Ե�ָ����ַ�����ĸ���֣���ɡ�
                        ���������Ǳ���ģ����û��ʹ�õ����ߣ��������������
                    ����·��
                        һ��Ӧ��ͨ����¶����Ϊ����Ӧ���ṩ�ض����񣬴�QObject������
                        ����url�еĽӿ�·���������淶�����ļ�ϵͳ�е�·������
                    �ӿ�
                        ����C++��java�нӿڵĸ���ǵ����ߺͱ������ߵĵ���Լ����
                Qt��D-Bus
                    Qt�ṩ��һ��QtDBusģ�飬�ڲ���װ��D-BusЭ�顣
                    Ӧ�ó����ͨ����Ϊ���������ṩ����������������������������
                    �����������������������Զ�̶���
                    ����QtDBus�����źŲ۽�������չ������Զ���źźͱ����źŹҵ�Զ�̲��С�
qt�źŲ�ԭ��
    ����QObject::connect����ʱ��
    ����QMetaObject��QMetaObjectPrivate��
    ���Ի���й��źŷ����ߡ��źź������źŽ����ߡ��ۺ������ض���Ϣ��
    ��Щ��Ϣ�ᱻ��ӵ������ߵ�"�źŲ��б�"(ConnectionList)�С��������ο�QObjectPrivate
    ÿ���߳��и��¼����У����߳��¼�ѭ���У�����ö��У�
    ������������ź�(QMetaCallEvent�¼�)�����ҵ��ź���Ӧ�Ķ���
    ���Ҹö����źŲ��б�����ɶ���Ӧ�۵ĵ��á�
    ע�������߷����ź�ʱ�������źŲ����ӷ�ʽ��
    ����ۺ�����Ӧ�Ķ����������߳��У��������߳��׳�QMetaCallEvent�¼���
    �����źź��������յ��õ���ǰ����invoke������
    ��QMetaMethod::invoke(QObject *object,
                          Qt::ConnectionType connectionType,
                          QGenericReturnArgument returnValue,
                          QGenericArgument val0,...)
    ������(qmetaobject.cpp)
    ���ȡQThread::currentThread()��object->thread()��
    �Ƚ������Ƿ�һ�£������һ����connectionType=AutoConnection��
    ����connectionType=Qt::QueuedConnection
    ֮�������ֱ�ӵ��÷�ʽ����
    callFunction(object, QMetaObject::InvokeMetaMethod, idx_relative, param);
    ����Ǽ�ӵ��÷�ʽ����
    QCoreApplication::postEvent(object, 
                                new QMetaCallEvent(
                                    idx_offset, idx_relative, callFunction,
                                    0, -1, nargs, types, args));
        ԭ�ͣ�static void postEvent(QObject *receiver, QEvent *event, 
                                    int priority = Qt::NormalEventPriority);  
        QThreadData * data = &receiver->d_func()->threadData;
        data->postEventList.addEvent(QPostEvent(receiver, event, priority));
        event->posted = true;
        ++receiver->d_func()->postedEvents;
        data->canWait = false;
    Ҳ����˵��postEvent���¼�����QMetaCallEvent��ӵ�Ŀ��object�����̶߳���
    (QThread/QThreadData)���¼��б�(postEventList)��.
    ���̵߳��¼�ѭ���Ӹ��¼��б���ȡ���¼����󣬸����¼������м�¼��Ŀ��������Ϣ
    ����event��������������ɶԲۺ����ĵ��á�
        QCoreApplication��exec�������ڲ����õ���QEventLoop��exec������
        ��QEventLoop��exec�����У����Ի�ȡ��ǰ�̵߳��߳���Ϣ
            Q_D(QEventLoop);  d->threadData
        QEventLoop��exec�����ڲ��ֵ���QEventLoop::processEvents
            Q_D(QEventLoop);
            d->threadData->eventDispatcher.load()->processEvents(flags);
                class QThreadData���г�Ա����
                QAtomicPointer<QAbstractEventDispatcher> eventDispatcher;
                    QAbstractEventDispatcher(�̳���QObject)���г�Ա������
                    void installNativeEventFilter(QAbstractNativeEventFilter *filterObj);
                    void removeNativeEventFilter(QAbstractNativeEventFilter *filterObj);
                    bool filterNativeEvent(const QByteArray &eventType, void *message, long *result);
                    virtual bool processEvents(QEventLoop::ProcessEventsFlags flags) = 0;
                    virtual bool hasPendingEvents() = 0; //Qt6: remove, mark final or make protected
                    virtual void registerSocketNotifier(QSocketNotifier *notifier) = 0;
                    virtual void unregisterSocketNotifier(QSocketNotifier *notifier) = 0;
                    virtual bool registerEventNotifier(QWinEventNotifier *notifier) = 0;
                    virtual void unregisterEventNotifier(QWinEventNotifier *notifier) = 0;
                    ������
                QPostEventList postEventList;  //�¼��б�
                QVector<void *> tls;  //�����ֲ߳̾��洢
        windows�£������������뵽QWindowsGuiEventDispatcher::processEvents
        �̶�����QEventDispatcherWin32::processEvents
        �ڸú����У�����Windows������Ϣ���в���ȡ��Ϣ
        �ú����ֻ���õ���Ϣ����ص�����qt_internal_proc��
        �ú����ᴦ��WM_QT_SOCKETNOTIFIER(WM_USER)��
        WM_QT_ACTIVATENOTIFIERS(WM_USER+1)��
        WM_QT_SENDPOSTEDEVENTS(WM_USER+2)��WM_TIMER��4����Ϣ��
        �������͵���Ϣ�����DefWindowProc��������
        ����WM_QT_SENDPOSTEDEVENTS������Ϣ����Ӧ�źŲۣ���
        �����q->sendPostedEvents(); 
        QEventDispatcherWin32 *q = 
            (QEventDispatcherWin32 *) GetWindowLongPtr(hwnd, GWLP_USERDATA);
        ���������ִ�QEventDispatcherWin32::processEvents���뵽
        QEventDispatcherWin32::sendPostedEvents�����У�
        ���̶����뵽 QCoreApplicationPrivate::sendPostedEvents�У�
        �̶�����QCoreApplication::sendEvent(r, e);
        rΪQPostEvent�м�¼��receiver��
        QPostEvent����QThreadData��postEventList�м�¼�ġ�
        QCoreApplication::sendEvent����QCoreApplication::notifyInternal2����
        ���̶�����QCoreApplication::notify��notify�����Ǹ��ǳ���ĺ�����
        ���ᴦ�����event�¼����͡�
        ���receiver��widget���ͣ�������յ��õ�QWidget::event(event);
        ��event�У�������ո���Ԫ������Ϣ�����õ���Ӧ�Ĳۺ�����
        ������Ƿ�widget���ͣ����ͨ��QObject::event�����յ��õ��ۺ�����
������
    �ı������ɫ
        ��setPalette�����Զ��������ɫ
            QApplication a(argc, argv);
            a.setStyle(new QWindowsStyle);
            QPalette pl(QColor(255,0,155));
            pl.setBrush(QPalette::WindowText,QColor(255,125,125));
            pl.setBrush(QPalette::Button,QColor(0,255,125));
            pl.setBrush(QPalette::Light,QColor(255,125,255));
            pl.setBrush(QPalette::ButtonText,QColor(125,0,0));
            pl.setBrush(QPalette::Shadow,QColor(0,125,0));
            pl.setBrush(QPalette::Highlight,QColor(0,0,125));
            pl.setBrush(QPalette::HighlightedText,QColor(255,0,0));
            a.setPalette(pl);   //����ͨ���ڶ��������޶�ֻ����ĳһ�༰������
            ע1��Ĭ�Ϸ���ܸı䰴ť����ɫ��QWindowsStyle�����Ըı䰴ť����ɫ
            �ȿ�Ϊapplication���õ�ɫ�壬Ҳ����Ϊĳ��widget���õ�ɫ��
            ע2����qt5�У����÷��ķ���������a.setStyle(new QWindowsStyle);
            ���Ǹ�ΪQStringList ls = QStyleFactory::keys();
            a.setStyle(QStyleFactory::create(ls[0]));
    �Զ�������
        ����ʹ��Qt�Դ��ķ����QWindowsStyle��
        ����Ҳ���Լ̳�QWindowsStyle����дpolish(QPalette&)������
        ʵ���Լ���CustomStyle,������setPalette����ʱ�������polish������
        ���⻹������polish(QWidget*)��polish(QApplication*)��Ϊָ���ĳ����ؼ���ɫ
���Ĵ��ڲ���
    һ��Qt������Ӧ�ó��������һ�����Ĵ��ڲ�����
    �����Ĵ��ڲ���Ҳ��������QMainWindow���е����ԡ�
    ��QtCreator�У�QtΪ�������Զ�������һ����Ϊcentralwidget��
    QWidget���͵����Ĳ������ο�ui_mainwindow.h�ļ�����
    QWidget * QMainWindow::centralWidget () const���ɻ�����Ĳ�����
    ���Ĳ����������������ͣ�
        Qt�ṩ�ı�׼���ڲ�������QWidget��QTextWidget��
        �û��Զ���Ĵ��ڲ���
        ������--QSplitter
            QSplitter��Ϊһ�������������ɶ��Qt���ڲ���
            ��ʱ���Ĳ�����һ�����ݶ�����ڲ�����������
        �����ؼ�����--QWorkspace
            ��һ��MDIӦ�ó����У�Ӧ�ó��������ڵ����Ĳ�����һ��QWorkspace����
        ���ĵ�����--QMdiArea
            Qt4.3�������÷���QWorkspace����
    ����������Ѿ������Ĳ����ˣ��ڵ���QMainWidget�ĵ�setCentralWidget����
    Ϊ����������һ���µ����Ĳ�������ôԭ�������Ĳ����ᱻ���������ٵ���
    �������������ԭ�������Ĳ����Ļ�������delete�ö��󣩣�����ɱ�����
    ��QMainWindow��ֱ�Ӳ���ؼ�����ѡ��this��Ϊ�ؼ��Ĺ��캯��������
    ��QPushButton* pbtn = new QPushButton(this);
    �ᷢ�ְ�ťû����ʾ������������Ϊ���Ĵ��ڲ������ֶ���ӵİ�ť����ס�ˡ�
    ���Խ���İ취�ǣ������Ĳ�����Ϊ��ť�Ĺ��캯��������
    QPushButton* pbtn = new QPushButton(ui->centralWidget);
    ��QPushButton* pbtn = new QPushButton(centralWidget());
    ���Ĳ��������ã�
        ���Ĳ���������һ�����þ��ǣ��������ڴ�С�仯ʱ�����Ĳ���Ҳ��֮�仯��
        ��һ����ӵ��Զ���ؼ������û��ʹ��ר�ŵĲ��������ǲ����洰�ڴ�С�仯�ġ�
        ���Ƶģ�setMenuBar��setToolBarҲ�����ƵĹ��ܣ�ʹ�˵�����״̬�����洰�ڴ�С�仯��
QWidgetֱ����Ϊ���ڲ���
    ��QWidget�����Զ����QWidget�����ࣩ��Ϊ���ڲ�����
    �ڴ�������ӣ�û��Ч����������ʽ��Ҳû���á�
    ��ΪQWidget��paintEvent����ֱ�Ӿ�û���κδ���ʵ�֣�
    Ҫ����QWidget���Զ���������֧����ʽ��
    ������paintEvent�м������´��룺
        QStyleOption opt;
        opt.init(this);
        QPainter p(this);
        style()->drawPrimitive(QStyle::PE_Widget,&opt,&p,this);
    ��ʾ:���Կ��Ǽ̳�QFrameȡ���̳�QWidget��QFrame֧����ʽ��
connectSlotsByName
    QMetaObject::connectSlotsByName(QObject *o);
    ����o��Ԫ���󣬵õ���ۺ����б�
    �������on_��ͷ�ģ��ͱ���o�ĺ����б�
    �������ƥ��Ķ��󣬾�ʹ��connect���������źŲۡ�
    �������������źŲ۵ķ�����������ԣ�
    �����źŵ�ֻ�����Լ��ĺ��ӣ����źŵĽ�����ֻ�����Լ���
ʹ����Դ�����ļ�(.qrc)
    qt����֧�����/�½�.qrc��ʽ����Դ�����ļ�
    ������Դ�ļ���
        ��������õ�cpp��Դ�ļ���ֻ�谴���¸�ʽ������Դ����
        :/ + (��Դ��������)ǰ׺ + �ļ���
        �磺QImage img; img.load(":/new/prefix1/image.png");
        ��������ö����Ƶ�rcc��Դ�ļ��������ڳ���ʼ��ʱ��
        ��һ��ע��(����)��Դ�Ĳ�����
        QResource::registerResource("path/xxx.rcc");
        ����������Զ�̬���ظö�������Դ�ļ���ʶ�����������Դ
    �޸���Դ�����ļ���
        .qrc�����ļ�ͨ��qt��Դ�ļ����������Ա༭��
        ͨ����Դ�����������Դǰ���������ǰ׺��
        ��Դ�ļ������Ͱ�����������ͼƬ����������Ƶ�ȡ�
        ���⣬��Դ�����ļ�(.qrc)��xml��ʽ��,�磺
        <RCC>
            <qresource prefix="/new/prefix1">
                <file>main.cpp</file>
                <file>C:/24.bmp</file>
            </qresource>
        </RCC>
        ���ԣ�ԭ���ϣ���Ҳ���Բ�ʹ����Դ��������
        ����ֱ���޸�.qrc�ļ��ķ�ʽ������µ���Դ�ļ�
    ������Դ�ļ���
        �����cpp�ļ�
            �����qt���̣�ֻ����.pro�ļ������ RESOURCES += myres.qrc,
            qt���Զ�ʹ��rcc����������Ӧ��.cpp�ļ���
            Ĭ������£�rcc ���߻�Ը�����Դ�ļ���ZIPѹ����
            Ȼ��ѹ�����ZIP���ݵ�ÿ���ֽ�ת���ɱ��� 0x6f��ֵ��ʽ��
            �����ļ�ѹ��������ݶ�Ӧһ��C++��̬���� qt_resource_data[]��
            �����ע�ᡢȡ��ע�ᡢ��ʼ��������Ⱥ�������Դ�����ṹ�壬
            �����γ�һ�� qrc_xxx.cpp�ļ���
            �����vs��Ҳ���Խ���qt��rcc.exe������԰�.qrc�ļ������.cpp�ļ���
            rcc -name aa -no-compress "$(InputPath)" -o aa.cpp
            ���ַ�ʽ�ĺô���ִ���ٶȿ죬ʹ�÷���ȣ�������Ҳ�����ԣ�
            һ�ǻ��������ɵĿ�ִ���ļ��������
            ����ռ���ڴ��
            ����������滻ͼƬ�������Ƥ������ܲ�����
        ������Դ�������ļ� 
            ʹ��qt��rcc.exe���Ҳ���԰�.qrc�ļ�����ɶ�������Դ�ļ�.rcc
            rcc -binary myresource.qrc -o myresource.rcc
            ʹ�����ַ�ʽ�����Է�����滻rcc�ļ��ﵽ�����򻻷���Ч�������������±����ִ���ļ�
        rcc�﷨�� rcc  [options] <inputs>
          Options:
            -o file              ָ������ļ���Ĭ�����������̨��
            -project             �Զ�����һ��.qrc�ļ����ļ��ѵ�ǰĿ¼�µ������ļ�������Ϊ��Դ
            -binary              ָ�����ɶ����Ƶ���Դ�ļ�
            -name name           �õ�������Դ��ʼ�����������ְ���name
            -no-compress         �ر��Զ�ѹ��
            -threshold level     ѹ����Դʱ�������ֵ
            -compress level      ѹ���ȼ�
            -root path           �����ɵ���Դ������ǰ׷��pathǰ׺
            -namespace           �ñ������ɵ���Դ�ļ�cpp�в��������ֿؼ���(QT_BEGIN_NAMESPACE)
            -version             ��ʾ�汾��Ϣ
            -help                ��ʾ����
    ֱ�����ñ���ͼƬ�ļ�
        ����������Դ�ļ��⣬����Ҳ����ֱ�����ñ����ļ�����
        QImage img; img.load("C:/image.png");
        �����ַ�ʽ�и��ܴ�����⣬�����û����������滻��ԴͼƬ
        ���Ǹ�ȱ�㣬��Ϊ���ױ��û������޸ģ���ͬʱҲ�ɰ��⿴���Ǹ��ŵ�
        
        
======================================================================================            