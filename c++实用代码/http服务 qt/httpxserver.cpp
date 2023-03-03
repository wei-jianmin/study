#include "httpxserver.h"
#include <QFile>
#include <QSslSocket>
#include <QTcpSocket>
#include <QSsl>
#include <QSslConfiguration>
#include <string.h>
#include <QSslKey>
#include <QDataStream>
#include "httphelper.h"

#define KEEP_ALIVE_TIME 30000

HttpXServer::HttpXServer(bool ssl_mode,QObject *parent) : QTcpServer(parent)
{
    _ssl_mode = ssl_mode;
    _cert_path = "cert.cer";
    _key_path = "key.key";
    _timer = new QTimer(this);
    _timer->setInterval(10000);
    connect(_timer,SIGNAL(timeout()),this,SLOT(TimerlyCloseSockets()));
    _timer->start();
    //刚创建的时候还没有连接信号，所以不能在构造函数中发信号
    //emit TraceInfo(QString("HttpXServer sslmode is %1, default ssl cer is cert.cer,default ssl key is key.key").arg(_ssl_mode));
}

HttpXServer::~HttpXServer()
{
    close();
}

bool HttpXServer::SetServerCert(const QString &cert_path)
{
    _cert_path = cert_path;
    emit TraceInfo(QString("====> SetServerCert %1 <====").arg(cert_path));
    return true;
}

void HttpXServer::TimerlyCloseSockets()
{
    QMap<QTcpSocket*,int>::const_iterator iter = _keep_alive_socks.begin();
    QList<QTcpSocket*> lst;
    while(iter != _keep_alive_socks.end())
    {
        if(abs(iter.value() - QTime::currentTime().msecsSinceStartOfDay()) > KEEP_ALIVE_TIME)
        {
            if(iter.key()->isValid())
                iter.key()->disconnectFromHost();
            lst.push_back(iter.key());
        }
        iter++;
    }
    foreach(QTcpSocket* sock,lst)
    {
        _keep_alive_socks.remove(sock);
    }
}

bool HttpXServer::SetServerKey(const QString &key_path)
{
    _key_path = key_path;
    emit TraceInfo(QString("====> SetServerKey %1 <====").arg(key_path));
    return true;
}

bool HttpXServer::listen(const QHostAddress &address, quint16 port)
{
    if(_ssl_mode)
    {
        if(QFile::exists(_cert_path)==false || QFile::exists(_key_path)==false)
        return false;
    }
    bool b = QTcpServer::listen(address,port);
    emit TraceInfo(QString("====> listening on port %1 ,sslmode = %2 result = %3 <====").arg(serverPort()).arg(_ssl_mode).arg(b));
    return b;
}

bool HttpXServer::SendBack(QTcpSocket* sock, const QByteArray &data)
{
    if(sock == NULL)
        return false;
    if(_ssl_mode)
    {
        QSslSocket *sock_ = reinterpret_cast<QSslSocket*>(sock);
        if(sock_ == NULL) return false;
        emit TraceInfo(QString("====> SendBack : sslmode : handle = %1\n%2 ......(datalength=%3) <====").arg(sock_->socketDescriptor()).arg(QString(data.left(100))).arg(data.length()));
        sock_->write(data);
        if(_keep_alive_socks.contains(sock))
            sock->flush();
        else
            sock->disconnectFromHost();
    }
    else
    {
        if(sock == NULL) return false;
        emit TraceInfo(QString("====> SendBack : handle = %1\n%2 ......(datalength=%3) <====").arg(sock->socketDescriptor()).arg(QString(data.left(100))).arg(data.length()));
        sock->write(data);
        if(_keep_alive_socks.contains(sock))
            sock->flush();
        else
            sock->disconnectFromHost();
    }
    return true;
}

void HttpXServer::incomingConnection(qintptr handle)
{
    emit TraceInfo(QString("====> incomingConnection handle = %1 <====").arg(handle));
    if(_ssl_mode)
    {
        QSslSocket * sock = new QSslSocket;
        sock->setSocketDescriptor(handle);
        if(SetSslConfiguration(sock)==false)
        {
            delete sock;
            return;
        }
        addPendingConnection(sock);
        connect(sock,SIGNAL(readyRead()),this,SLOT(ReadData()));
        sock->startServerEncryption();
    }
    else
    {
        QTcpSocket * sock = new QTcpSocket;
        sock->setSocketDescriptor(handle);
        addPendingConnection(sock);
        connect(sock,SIGNAL(readyRead()),this,SLOT(ReadData()));
    }
}

HttpXServer::_HttpData HttpXServer::GetHttpData(HttpRequestParser &parser)
{
    _HttpData hd;
    hd.data = parser.OriginalData();
    hd.version = parser.HttpVersion();
    hd.time = QTime::currentTime().msecsSinceStartOfDay();
    hd.is_keepalive = parser.IsKeepAlive();
    hd.content_type = parser.ContentType();
    hd.boundary = parser.Boundary();
    hd.is_trunked = parser.IsTrunked();
    hd.content_totallen = parser.ContentLength();
    hd.content_templen = parser.Body().length();
    return hd;
}

void HttpXServer::ReadData()
{
    if(hasPendingConnections())
    {
        while(hasPendingConnections())
        {
            if(_ssl_mode)
            {
                QTcpSocket *sock_ = nextPendingConnection();
                QSslSocket *sock = reinterpret_cast<QSslSocket*>(sock_);
                if(sock)
                {
                    emit TraceInfo(QString("====> ReadData : hasPendingConnections : sslmode : handle = %1 <====").arg(sock->socketDescriptor()));
                    connect(sock, &QAbstractSocket::disconnected,sock, &QObject::deleteLater);
                    QByteArray str = sock->readAll();
                    emit TraceInfo(QString("====> ReadData : readfrom socked is \n%1 ...... <====").arg(QString(str.left(100))));
                    HttpRequestParser parser;
                    parser.Parse(str);
                    //if(parser.IsKeepAlive())
                    //    _keep_alive_socks[sock]=QTime::currentTime().msecsSinceStartOfDay();
                    if(parser.ContentLength() > parser.Body().length())
                        _sock_data_map[sock] = GetHttpData(parser);
                    else
                        emit RecvFinish(sock,str);
                }
            }
            else
            {
                QTcpSocket *sock = nextPendingConnection();
                if(sock)
                {
                    emit TraceInfo(QString("====> ReadData : hasPendingConnections : handle = %1 <====").arg(sock->socketDescriptor()));
                    connect(sock, &QAbstractSocket::disconnected,sock, &QObject::deleteLater);
                    QByteArray str = sock->readAll();
                    qDebug()<<str;
                    emit TraceInfo(QString("====> ReadData : readfrom socked is \n%1 ...... <====").arg(QString(str.left(100))));
                    HttpRequestParser parser;
                    parser.Parse(str);
                    //if(parser.IsKeepAlive())
                    //    _keep_alive_socks[sock]=QTime::currentTime().msecsSinceStartOfDay();
                    if(parser.ContentLength() > parser.Body().length())
                        _sock_data_map[sock] = GetHttpData(parser);
                    else
                        emit RecvFinish(sock,str);
                }
            }
        }
    }
    else
    {
        if(_ssl_mode)
        {
            QSslSocket *sock = reinterpret_cast<QSslSocket*>(sender());
            if(sock)
            {
                emit TraceInfo(QString("====> ReadData : convert from sender : sslmode : handle = %1 <====").arg(sock->socketDescriptor()));
                QByteArray str = sock->readAll();
                emit TraceInfo(QString("====> ReadData : readfrom socked is \n%1 ...... <====").arg(QString(str.left(100))));
                QMetaObject::invokeMethod(this,"RecvPartData",Qt::AutoConnection,QGenericReturnArgument(),Q_ARG(QTcpSocket*,sock),Q_ARG(QString,str));
            }
        }
        else
        {
            QTcpSocket *sock = reinterpret_cast<QTcpSocket*>(sender());
            if(sock)
            {
                emit TraceInfo(QString("====> ReadData : convert from sender : handle = %1 <====").arg(sock->socketDescriptor()));
                QByteArray str = sock->readAll();
                emit TraceInfo(QString("====> ReadData : readfrom socked is \n%1 ...... <====").arg(QString(str.left(100))));
                QMetaObject::invokeMethod(this,"RecvPartData",Qt::AutoConnection,QGenericReturnArgument(),Q_ARG(QTcpSocket*,sock),Q_ARG(QString,str));
            }
        }
    }
}

void HttpXServer::RecvPartData(QTcpSocket* sock,const QByteArray &data)
{
    if(_sock_data_map.find(sock) != _sock_data_map.end())
    {
        if(_sock_data_map[sock].is_trunked)
        {
            //TODO : 对于truncked数据，需要额外处理一下
        }
        else
            _sock_data_map[sock].data += data;
        _sock_data_map[sock].content_templen += data.length();
        if(_sock_data_map[sock].content_templen >= _sock_data_map[sock].content_totallen)
        {
            emit RecvFinish(sock,_sock_data_map[sock].data);
            _sock_data_map.remove(sock);
        }
    }
}

bool HttpXServer::SetSslConfiguration(QSslSocket * sock)
{
    QSslConfiguration sslConfiguration;
    QFile certFile(_cert_path);
    QFile keyFile(_key_path);
    certFile.open(QIODevice::ReadOnly);
    keyFile.open(QIODevice::ReadOnly);
    if(certFile.isOpen()==false || keyFile.isOpen()==false)
        return false;

    char buf[50]={0};
    QSsl::EncodingFormat cert_format,key_format;
    certFile.peek(buf,50);
    if(strstr(buf,"--BEGIN") != NULL)
        cert_format = QSsl::Pem;
    else
        cert_format = QSsl::Der;
    memset(buf,0,50);
    keyFile.peek(buf,50);
    if(strstr(buf,"--BEGIN") != NULL)
        key_format = QSsl::Pem;
    else
        key_format = QSsl::Der;
    QSslCertificate certificate(&certFile, cert_format);
    QSslKey sslKey(&keyFile, QSsl::Rsa, key_format);
    certFile.close();
    keyFile.close();
    sslConfiguration.setPeerVerifyMode(QSslSocket::VerifyNone);
    sslConfiguration.setLocalCertificate(certificate);
    sslConfiguration.setPrivateKey(sslKey);
    sslConfiguration.setProtocol(QSsl::TlsV1SslV3);
    sock->setSslConfiguration(sslConfiguration);
    return true;
}
