#ifndef HTTPXSERVER_H
#define HTTPXSERVER_H

#include <QMap>
#include <QObject>
#include <QTimer>
#include <QTcpServer>
#include "httphelper.h"
class QSslSocket;
class QTcpSocket;

class HttpXServer : public QTcpServer
{
    Q_OBJECT
    struct _HttpData
    {
        bool is_trunked;
        bool is_keepalive;
        int time,content_totallen,content_templen;
        QString version,content_type,boundary;
        QByteArray data;
    };
public:
    explicit HttpXServer(bool ssl_mode = false, QObject *parent = nullptr);
    ~HttpXServer();
    bool SetServerCert(const QString &cert_path);
    bool SetServerKey(const QString &key_path);
    bool listen(const QHostAddress &address = QHostAddress::Any, quint16 port = 0);
    enum ErrorType {send,recv,accept,unknown};
signals:
    void RecvFinish(QTcpSocket* sock, const QByteArray& data);
    void Error(ErrorType error_type,const QString msg);
    void SendFinish();
    void TraceInfo(const QString &info);
protected:
    virtual void incomingConnection(qintptr handle);
public slots:
    bool SendBack(QTcpSocket* sock, const QByteArray& data);
private slots:
    void ReadData();
    void RecvPartData(QTcpSocket* sock,const QByteArray &data);
    void TimerlyCloseSockets();
private:
    bool SetSslConfiguration(QSslSocket * sock);
    _HttpData GetHttpData(HttpRequestParser &parser);
private:
    bool _ssl_mode;
    bool _is_ok;
    QString _cert_path,_key_path;
    QMap<QTcpSocket*,_HttpData> _sock_data_map; //存放的是未完全接受完成的socket数据
    QMap<QTcpSocket*,int> _keep_alive_socks;
    QTimer * _timer;
};

#endif // HTTPXSERVER_H
