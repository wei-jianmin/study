1.  #define qDebug QMessageLogger(QT_MESSAGELOG_FILE, QT_MESSAGELOG_LINE, QT_MESSAGELOG_FUNC).debug
    ���������
        QT_MESSAGELOG_FILE : �ļ���
        QT_MESSAGELOG_LINE ���к�
        QT_MESSAGELOG_FUNC ������ǩ�� ����: void MainWindow::on_btn1_clicked()
    QMessageLogger���캯����
        QMessageLogger�����и� QMessageLogContext context ˽�г�Ա����
        QMessageLogger����ʱ���Ѳ����������ļ������кš�����������Ϣ�浽 context ��Ա������
    debug()��Ա����
        QDebug QMessageLogger::debug() const
        {
            QDebug dbg = QDebug(QtDebugMsg);
            QMessageLogContext &ctxt = dbg.stream->context;  // QMessageLogContext��QDebug����Ԫ
            ctxt.copy(context);
            return dbg;
        }
2.  QDebug(QtDebugMsg)
    ��Ա����
        QDebug�и�˽�г�Ա���� struct Stream* stream
        Stream�ṹά�������³�Ա������
            QTextStream ts;
            QString buffer;
            int ref;
            QtMsgType type;
            bool space;
            bool message_output;
            QMessageLogContext context;
        Stream�ṹ���캯�����򻯣���
            Stream(QIODevice *device) : ts(device),                        type(QtDebugMsg), space(true), message_output(false)
            Stream(QString   *string) : ts(string,  QIODevice::WriteOnly), type(QtDebugMsg), space(true), message_output(false)
            Stream(QtMsgType  t)      : ts(&buffer, QIODevice::WriteOnly), type(t),          space(true), message_output(true)
    ��Ԫ��
        QMessageLogger��QDebug����Ԫ��
        ��ʽ��Ϊ���ԭ�����Բ����� QMessageLogger::debug() �з��� QDebug ��˽�г�Ա stream
    ���캯��
        QDebug(QIODevice *device) : stream(new Stream(device))
        QDebug(QString *string)   : stream(new Stream(string))
        QDebug(QtMsgType t)       : stream(new Stream(t)) 
    <<���ź���
        QDebug & operator<<(const char* t) 
        { 
            stream->ts << QString::fromUtf8(t); 
            if (stream->space) stream->ts << ' '; 
            return *this;
        }
    �����������򻯣�
        if ( stream->space && stream->buffer.endsWith(' ') )  stream->buffer.chop(1);  //ɾ����β�Ŀո�
        if ( stream->message_output )  qt_message_output(stream->type, stream->context, stream->buffer);
        delete stream;

3.  ����QDebug()�������ʽ
    qSetMessagePattern("%{appname} %{type} %{time [yyyy-MM-dd hh:mm:ss]} %{file} %{line} %{function} %{message}");
    qSetMessagePattern���õ������ʽĬ��ֻ����debugģʽ����Ч����releaseģʽ�¾�ʧЧ��
    ����Ҫ����releaseģʽ����Ч��ֻ��Ҫ����Ŀpro�ļ������ DEFINES+=QT_MESSAGELOGCONTEXT �����±��뼴��
                