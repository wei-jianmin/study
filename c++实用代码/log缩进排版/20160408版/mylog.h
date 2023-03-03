#ifndef _LOGOP_H_
#define _LOGOP_H_

#include <fstream>
#include <string>
using std::fstream;
using std::string;
using std::wstring;
using std::endl;
#ifndef m_logw
#define m_logw(s) m_log.write(_T(#s));  //如果使用该宏，要注意防止宏覆盖
//#define m_logw(s) m_log.msgbox(_T(#s));
#endif
#ifndef logw
#define logw(s) log.write(_T(#s));  //如果使用该宏，要注意防止宏覆盖
#endif
#define WRITE_STRATEGY()
class mylog_op
{
public:
	//构造函数默认参数：只能排版，在发布版中写日志、显示弹出框，添加时间标志
	mylog_op(TCHAR * logname=_T("log.txt"),bool smartLayout=true,short writeMode=1,bool msgboxMode=1,bool addTimeInLog=true,bool indent=true);
	bool setpath(const TCHAR *  logPath=_T("temp"));	//设置日志保存路径，参数值为空字串，则保存在当前目录，使用默认值时，保存在系统临时文件夹
	bool setpath(int index);			//设置日志保存路径,0:当前目录，:系统临时目录
	void setLogName(const TCHAR * name);		//设置保存日志的名字，默认为log.txt，需在setpath前调用
	void setTimeStrategy(bool addTimeInLog);	//设置是否在日志前自动添加时间
	void setWriteStrategy(short writeMode);	//设置是否允许写日志
	void setMsgboxStrategy(short msgboxMode);	//设置消息框是否允许弹出
	void setMsgboxPrifixInfo(const TCHAR *info);	//设置消息框信息前缀
	void setIndentStrategy(bool indentMode);	//设置自动缩进
	void setLayoutStrategy(bool smartLayout);	//设置只能排版
	void writeSplitLine(TCHAR ch,int length);		//向日志中写入多个重复字符
	bool write(const TCHAR * data=_T(""));		//写日志
	bool writeEx(const TCHAR * format,...);		//写日志
	void msgbox(const TCHAR * format,...);		//弹出消息框
	TCHAR * getErrInfo(DWORD errorNo);		//获得错误代码对应的错误信息
	void showError(DWORD errorNo);		//显示错误代码对应的错误信息
	void showError();			//显示上一步调用windowAPI的执行结果信息
	void about();				//关于
public:
	~mylog_op(void);
private:
	string filepath;	//文件保存路径	
	wstring wfilepath;	//文件保存路径
	string logName;		//日志文件名
	wstring wLogName;	//日志文件名	
	bool pathError;		//日志路径是否设置成功
	fstream file;		//日志文件
	bool timeFlag; 		//写日志是，是否自动添加时间
	bool timeFlag2;		//写日志时，在前面添加日期还是时间
	bool separate;		//写日志前是否先写一行###################
	short writemode; 	//写日志操作控制writeInDbgMode;
	short msgmode;  	//弹出框显示控制msgInDbgMode
	bool sLayout;	    //智能排版控制
	TCHAR *lpBuffer;   	//错误信息
	bool tmpSeparate;	//写日志控制,加分割线
	bool tmpNoTimeflag;	//写日志控制，不在日志前添加时间
	int level;			//缩进等级
	bool autoIndent;	//自动缩进控制
	string msgPrifixInfo;	//文件保存路径	
	wstring wmsgPrifixInfo;	//文件保存路径
};
#endif

