#ifndef _LOGOP_H_
#define _LOGOP_H_

#include <fstream>
#include <string>
using std::fstream;
using std::string;
using std::wstring;
using std::endl;
#ifndef m_logw
#define m_logw(s) m_log.write(_T(#s));  //���ʹ�øú꣬Ҫע���ֹ�긲��
//#define m_logw(s) m_log.msgbox(_T(#s));
#endif
#ifndef logw
#define logw(s) log.write(_T(#s));  //���ʹ�øú꣬Ҫע���ֹ�긲��
#endif
#define WRITE_STRATEGY()
class mylog_op
{
public:
	//���캯��Ĭ�ϲ�����ֻ���Ű棬�ڷ�������д��־����ʾ���������ʱ���־
	mylog_op(TCHAR * logname=_T("log.txt"),bool smartLayout=true,short writeMode=1,bool msgboxMode=1,bool addTimeInLog=true,bool indent=true);
	bool setpath(const TCHAR *  logPath=_T("temp"));	//������־����·��������ֵΪ���ִ����򱣴��ڵ�ǰĿ¼��ʹ��Ĭ��ֵʱ��������ϵͳ��ʱ�ļ���
	bool setpath(int index);			//������־����·��,0:��ǰĿ¼��:ϵͳ��ʱĿ¼
	void setLogName(const TCHAR * name);		//���ñ�����־�����֣�Ĭ��Ϊlog.txt������setpathǰ����
	void setTimeStrategy(bool addTimeInLog);	//�����Ƿ�����־ǰ�Զ����ʱ��
	void setWriteStrategy(short writeMode);	//�����Ƿ�����д��־
	void setMsgboxStrategy(short msgboxMode);	//������Ϣ���Ƿ�������
	void setMsgboxPrifixInfo(const TCHAR *info);	//������Ϣ����Ϣǰ׺
	void setIndentStrategy(bool indentMode);	//�����Զ�����
	void setLayoutStrategy(bool smartLayout);	//����ֻ���Ű�
	void writeSplitLine(TCHAR ch,int length);		//����־��д�����ظ��ַ�
	bool write(const TCHAR * data=_T(""));		//д��־
	bool writeEx(const TCHAR * format,...);		//д��־
	void msgbox(const TCHAR * format,...);		//������Ϣ��
	TCHAR * getErrInfo(DWORD errorNo);		//��ô�������Ӧ�Ĵ�����Ϣ
	void showError(DWORD errorNo);		//��ʾ��������Ӧ�Ĵ�����Ϣ
	void showError();			//��ʾ��һ������windowAPI��ִ�н����Ϣ
	void about();				//����
public:
	~mylog_op(void);
private:
	string filepath;	//�ļ�����·��	
	wstring wfilepath;	//�ļ�����·��
	string logName;		//��־�ļ���
	wstring wLogName;	//��־�ļ���	
	bool pathError;		//��־·���Ƿ����óɹ�
	fstream file;		//��־�ļ�
	bool timeFlag; 		//д��־�ǣ��Ƿ��Զ����ʱ��
	bool timeFlag2;		//д��־ʱ����ǰ��������ڻ���ʱ��
	bool separate;		//д��־ǰ�Ƿ���дһ��###################
	short writemode; 	//д��־��������writeInDbgMode;
	short msgmode;  	//��������ʾ����msgInDbgMode
	bool sLayout;	    //�����Ű����
	TCHAR *lpBuffer;   	//������Ϣ
	bool tmpSeparate;	//д��־����,�ӷָ���
	bool tmpNoTimeflag;	//д��־���ƣ�������־ǰ���ʱ��
	int level;			//�����ȼ�
	bool autoIndent;	//�Զ���������
	string msgPrifixInfo;	//�ļ�����·��	
	wstring wmsgPrifixInfo;	//�ļ�����·��
};
#endif

