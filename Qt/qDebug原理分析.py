1.  #define qDebug QMessageLogger(QT_MESSAGELOG_FILE, QT_MESSAGELOG_LINE, QT_MESSAGELOG_FUNC).debug
    传入参数：
        QT_MESSAGELOG_FILE : 文件名
        QT_MESSAGELOG_LINE ：行号
        QT_MESSAGELOG_FUNC ：函数签名 例如: void MainWindow::on_btn1_clicked()
    QMessageLogger构造函数：
        QMessageLogger类中有个 QMessageLogContext context 私有成员变量
        QMessageLogger构造时，把参数传来的文件名、行号、函数名等信息存到 context 成员变量中
    debug()成员函数
        QDebug QMessageLogger::debug() const
        {
            QDebug dbg = QDebug(QtDebugMsg);
            QMessageLogContext &ctxt = dbg.stream->context;  // QMessageLogContext是QDebug的友元
            ctxt.copy(context);
            return dbg;
        }
2.  QDebug(QtDebugMsg)
    成员变量
        QDebug有个私有成员变量 struct Stream* stream
        Stream结构维护了如下成员变量：
            QTextStream ts;
            QString buffer;
            int ref;
            QtMsgType type;
            bool space;
            bool message_output;
            QMessageLogContext context;
        Stream结构构造函数（简化）：
            Stream(QIODevice *device) : ts(device),                        type(QtDebugMsg), space(true), message_output(false)
            Stream(QString   *string) : ts(string,  QIODevice::WriteOnly), type(QtDebugMsg), space(true), message_output(false)
            Stream(QtMsgType  t)      : ts(&buffer, QIODevice::WriteOnly), type(t),          space(true), message_output(true)
    友元类
        QMessageLogger是QDebug的友元类
        正式因为这个原因，所以才能在 QMessageLogger::debug() 中访问 QDebug 的私有成员 stream
    构造函数
        QDebug(QIODevice *device) : stream(new Stream(device))
        QDebug(QString *string)   : stream(new Stream(string))
        QDebug(QtMsgType t)       : stream(new Stream(t)) 
    <<符号函数
        QDebug & operator<<(const char* t) 
        { 
            stream->ts << QString::fromUtf8(t); 
            if (stream->space) stream->ts << ' '; 
            return *this;
        }
    析构函数（简化）
        if ( stream->space && stream->buffer.endsWith(' ') )  stream->buffer.chop(1);  //删除结尾的空格
        if ( stream->message_output )  qt_message_output(stream->type, stream->context, stream->buffer);
        delete stream;

3.  定义QDebug()的输出格式
    qSetMessagePattern("%{appname} %{type} %{time [yyyy-MM-dd hh:mm:ss]} %{file} %{line} %{function} %{message}");
    qSetMessagePattern设置的输出格式默认只会在debug模式下生效，在release模式下就失效了
    我们要想在release模式下生效，只需要在项目pro文件中添加 DEFINES+=QT_MESSAGELOGCONTEXT 后，重新编译即可
                