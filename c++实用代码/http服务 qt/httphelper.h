#ifndef HTTPPARSER_H
#define HTTPPARSER_H

#include <QDataStream>
#include <QMap>

class HttpRequestParser
{
public:
    HttpRequestParser();
    HttpRequestParser(const QByteArray &data);
    bool Parse(const QByteArray &data);
    QString HttpVersion();
    QString Method();
    QString Url();
    void Clear();
    QString QueryString();
    QMap<QString,QString> Headers();
    QString Header(const QString& key);
    bool IsKeepAlive();
    bool IsTrunked();
    QString Boundary();
    QByteArray Body();
    QString ContentType();
    QString BodyFormat();
    QByteArray OriginalData();
    quint32 ContentLength();
    bool IsOk();
private:
    bool _ok,_is_keepalive,_is_trunked;
    QString _version,_method,_url,_query,_body_format,_boundary;
    QByteArray _http_text,_body;
    quint32 _content_length;
    QMap<QString,QString> _http_headers;
};


#define HTTP_CONTETN_TYPE_JSON "application/json"
#define HTTP_CONTETN_TYPE_TEXT "text/plain"
#define HTTP_CONTETN_TYPE_HTML "text/html"
#define HTTP_CONTETN_TYPE_IOCN "image/x-icon"
class HttpEchoMaker
{
public:
    explicit HttpEchoMaker(const QString& content_type="");
    bool SetStatus(const QString &status_code="200",const QString &discription="");
    bool AddHeader(const QString& key,const QString& value);
    bool SetContentType(const QString &content_type);
    bool SetEchoData(const QByteArray& data);
    void Clear();
    const QString Header();
    QByteArray MakeHttpEcho();
private:
    QString _status,_head,_content_type;
    QByteArray _body;
};

class MyDataStream : public QDataStream
{
public:
    MyDataStream();
    explicit MyDataStream(QIODevice * dev);
    MyDataStream(QByteArray * b, QIODevice::OpenMode flags);
    MyDataStream(const QByteArray & b);
    QByteArray readLine(int maxlen=-1);
    QByteArray readAll();
    qint64 peek(char *data, qint64 maxSize);
};

#endif // HTTPPARSER_H
