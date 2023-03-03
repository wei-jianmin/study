#include "httphelper.h"
#include <QTextStream>
#include <QDataStream>

HttpRequestParser::HttpRequestParser()
{
    Clear();
}

HttpRequestParser::HttpRequestParser(const QByteArray &data)
{
    Clear();
    Parse(data);
}

bool HttpRequestParser::Parse(const QByteArray &data)
{
    _ok=false;
    if(data.isEmpty())
        return false;
    _http_text = data;
    MyDataStream ss(&_http_text,QIODevice::ReadOnly);
    QString str_line;
    //处理第一行
    str_line = ss.readLine();
    _method = str_line.section(' ',0,0);
    if(_method.compare("post",Qt::CaseInsensitive)!=0 &&
            _method.compare("get",Qt::CaseInsensitive)!=0)
        return false;
    QString url = str_line.section(' ',1,1);
    _url = url.section('/',0,0);
    _query = url.section('/',1,-1);
    _version = str_line.section(' ',2,2).section('/',1,1);

    //处理头
    str_line = ss.readLine();
    while (str_line.isEmpty() == false) {
        if(str_line=="\n")
            break;
        int pos = str_line.indexOf(':');
        if(pos==-1)
        {
            str_line = ss.readLine();
            continue;
        }
        _http_headers[str_line.section(':',0,0).toLower()] = str_line.section(':',1,1).toLower().trimmed();
        str_line = ss.readLine();
    }
    //正文
    _body = ss.readAll();
    //其它
    if(_http_headers["content-length"].isEmpty() == false)
        _content_length = _http_headers["content-length"].toInt();
    else
        _content_length = _body.length();
    QString con = _http_headers["connection"];
    if(con.isEmpty())
    {
        _is_keepalive = false;
    }
    else
    {
        if(con.compare("keep-alive")==0)
            _is_keepalive = true;
        else
            _is_keepalive = false;
    }
    QString cont = _http_headers["content-type"];
    _boundary = "";
    if(cont.startsWith("multipart/form-data"))
    {
        _body_format = cont.section(';',0,0);
        QString bound = cont.section(';',1,1).trimmed();
        if(bound.startsWith("boundary"))
        {
            _boundary = bound.section('=',1,1);
        }
    }
    else
    {
        _body_format = cont;
    }
    QString trc = _http_headers["transfer-encoding"];
    if(trc.isEmpty() || trc.compare("chunked")!=0)
    {
        _is_trunked = false;
    }
    else\
    {
        _is_trunked = true;
    }
    _ok = true;
    return true;
}

QString HttpRequestParser::HttpVersion()
{
    return _version;
}

QString HttpRequestParser::Method()
{
    return _method;
}

QString HttpRequestParser::Url()
{
    return _url;
}

void HttpRequestParser::Clear()
{
    _ok = false;
    _is_keepalive = false;
    _is_trunked = false;
    _version.clear();;
    _method.clear();
    _url.clear();
    _query.clear();
    _body_format.clear();
    _boundary.clear();
    _http_text.clear();
    _body.clear();
    _content_length = 0;
    _http_headers.clear();
}

QString HttpRequestParser::QueryString()
{
    return _query;
}

QMap<QString, QString> HttpRequestParser::Headers()
{
    return _http_headers;
}

QString HttpRequestParser::Header(const QString &key)
{
    return _http_headers[key];
}

bool HttpRequestParser::IsKeepAlive()
{
    return _is_keepalive;
}

bool HttpRequestParser::IsTrunked()
{
    return _is_trunked;
}

QString HttpRequestParser::Boundary()
{
    return _boundary;
}

QByteArray HttpRequestParser::Body()
{
    return _body;
}

QString HttpRequestParser::ContentType()
{
    return _body_format;
}

QString HttpRequestParser::BodyFormat()
{
    return _body_format;
}

QByteArray HttpRequestParser::OriginalData()
{
    return _http_text;
}

quint32 HttpRequestParser::ContentLength()
{
    return _content_length;
}

bool HttpRequestParser::IsOk()
{
    return _ok;
}

//=========================================================================================

HttpEchoMaker::HttpEchoMaker(const QString &content_type)
{
    _content_type = content_type;
    _status = "HTTP/1.1 200 \r\n";
}

bool HttpEchoMaker::SetStatus(const QString &status_code, const QString &discription)
{
    if(status_code.isEmpty())
        return false;
    _status = "HTTP/1.1 ";
    _status += status_code;
    if(discription.isEmpty() == false)
    {
        _status += " ";
        _status += discription;
    }
    _status += "\r\n";
    return true;
}

bool HttpEchoMaker::SetContentType(const QString &content_type)
{
    _content_type = content_type;
}

bool HttpEchoMaker::AddHeader(const QString &key, const QString &value)
{
    _head += key;
    _head += ": ";
    _head += value;
    _head += "\r\n";
}

bool HttpEchoMaker::SetEchoData(const QByteArray &data)
{
    _body = data;
}

void HttpEchoMaker::Clear()
{
    _status.clear();
    _head.clear();
    _content_type.clear();
    _body.clear();
}

const QString HttpEchoMaker::Header()
{
    QString head;
    head = _head;
    if(_content_type.isEmpty()==false)
    {
        head = "Content-type: ";
        head += _content_type;
        head += "\r\n";
    }
    head += "Access-Control-Allow-Origin: *\r\n";
    head += "Access-Control-Allow-Methods:GET,POST,PUT,PATCH,DELETE,OPTIONS\r\n";
    return head;
}

QByteArray HttpEchoMaker::MakeHttpEcho()
{
    if(_content_type.isEmpty()==false)
    {
        _head = "Content-type: ";
        _head += _content_type;
        _head += "\r\n";
    }
    QByteArray str;
    str = _status.toUtf8();
    str += _head.toUtf8();
    str += "Access-Control-Allow-Origin: *\r\n";
    str += "Access-Control-Allow-Methods:GET,POST,PUT,PATCH,DELETE,OPTIONS\r\n";
    str += "\r\n";
    str += _body;
    return str;
}

MyDataStream::MyDataStream() : QDataStream()
{

}

MyDataStream::MyDataStream(QIODevice * dev) : QDataStream(dev)
{

}

MyDataStream::MyDataStream(QByteArray *b, QIODevice::OpenMode flags) : QDataStream(b,flags)
{

}

MyDataStream::MyDataStream(const QByteArray &b) : QDataStream(b)
{

}

QByteArray MyDataStream::readLine(int maxlen)
{
    int i = 0;
    char c = '\0';
    int n;
    QByteArray ba;

    while (c != '\n')
    {
        if(maxlen != -1)
        {
            if(i >= maxlen -1)
                break;
        }
        n = readRawData(&c, 1);
        if (n > 0)    /*如果能读到字符*/
        {
            if (c == '\r')   /*如果读到的字符是\r*/
            {
                n = peek(&c, 1); /*看后面的那个字符是不是\n*/
                if ((n > 0) && (c == '\n'))  /*如果是\n,则把这个字符读到c中--原来里面的\r被覆盖*/
                    readRawData(&c, 1);
                else
                    c = '\n';      /*如果后面的字符不是\n，则c重新赋值为\n--原来里面的\r被覆盖*/
            }
            ba.append(c);      /*将c存到buf中，进行下次循环，当c是\n时，循环结束*/
            i++;
        }
        else
            c = '\n';
    }
    ba.append('\0');

    return ba;     //返回读到的字节
}

qint64 MyDataStream::peek(char *data, qint64 maxSize)
{
    char c = '\0';
    int i,n;
    qint64 pos;
    QIODevice *dev = device();
    pos = dev->pos();
    i=0;
    while (1)
    {
        n = readRawData(&c, 1);
        if (n > 0)    /*如果能读到字符*/
        {
            data[i]=c;      /*将c存到buf中，进行下次循环，当c是\n时，循环结束*/
            if(i >= maxSize)
            {
                break;
            }
            i++;
        }
        else
            break;
    }
    dev->seek(pos);
    return i;     //返回读到的字节
}

QByteArray MyDataStream::readAll()
{
    char c = '\0';
    int n;
    QByteArray ba;

    while (1)
    {
        n = readRawData(&c, 1);
        if (n > 0)    /*如果能读到字符*/
            ba.append(c);      /*将c存到buf中，进行下次循环，当c是\n时，循环结束*/
        else
            break;
    }
    return ba;     //返回读到的字节
}
