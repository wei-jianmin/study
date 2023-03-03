
#include "StdAfx.h"
#include "mylog.h"	/******************ע����ͷ�ļ�һ��****************************/

mylog_op::mylog_op(TCHAR * logname/* =log.txt */,bool smartLayout/* =false */,short writeMode/* =false */,bool msgboxOnlyInDbgMode/* =false */,bool addTimeInLog/* =true */,bool indent/*=true*/)
{
	timeFlag=false;
	filepath.clear();
	wfilepath.clear();
	logName.clear();
	wLogName.clear();
#ifdef _UNICODE
	wLogName.assign(logname);
#else
	logName.assign(logname);
#endif
	timeFlag=addTimeInLog;
	timeFlag2=false;
	separate=false;
	writemode=writeMode;
	msgmode=msgboxOnlyInDbgMode;
	pathError=true;
	sLayout=smartLayout;
	lpBuffer=NULL;
	tmpNoTimeflag=false;
	tmpSeparate=false;
	level=0;
	autoIndent=indent;
	setpath(_T(""));
}
mylog_op::~mylog_op(void)
{
	if(lpBuffer!=NULL)
		LocalFree(lpBuffer);
}

void mylog_op::setTimeStrategy(bool addTimeInLog)
{
	timeFlag=addTimeInLog;
}
void mylog_op::setLayoutStrategy(bool smartLayout)
{
	sLayout=smartLayout;
}
void mylog_op::writeSplitLine(TCHAR ch,int length)
{	
	if(length<=0)
		return;
	//writemode: 0-��д��1-ֻ�ڵ���ģʽд��2-ֻ�ڷ���ģʽд,>=3 ��д
	if(writemode == 0)
		return;
	if(writemode == 1)
	{
#ifndef _DEBUG	//�Ƿ���ģʽ
		return;
#endif
	}
	if(writemode == 2)
	{
#ifdef  _DEBUG	//�ǵ���ģʽ
		return;
#endif
	}
	CString strFilePath;

#ifdef _UNICODE
	strFilePath=(TCHAR *)wfilepath.data();
#else
	strFilePath=(TCHAR *)filepath.data();
#endif
	TCHAR *pstr;
	pstr=new TCHAR[length+1];
	int i;
	for(i=0;i<length;i++)
		pstr[i]=ch;
	pstr[i]='\0';

#ifdef _UNICODE
#pragma region ��infoת���ɶ��ַ�
	int len=WideCharToMultiByte(CP_ACP,0,pstr,(int)wcslen(pstr),NULL,0,NULL,NULL);
	char * chs;
	chs=new char[len+1];
	WideCharToMultiByte(CP_ACP,0,pstr,(int)wcslen(pstr),chs,len,NULL,NULL);
	chs[len]='\0';
#pragma endregion
#else
	char *chs;
	chs=pstr;
#endif

	file.open(strFilePath,fstream::in|fstream::app);	//��д��׷�ӵķ�ʽ��
	if(file.is_open())
	{
		if(separate || tmpSeparate)
		{
			file<<endl<<chs<<endl<<endl;
			separate=false;
		}
		file.close();
	}
	delete pstr;
	pstr=NULL;
#ifdef _UNICODE
	delete chs;
	chs=NULL;
#endif
}
void mylog_op::setMsgboxStrategy(short msgboxMode)
{
	msgmode=msgboxMode;
}
bool mylog_op::setpath(int index)
{
	if(index == 0)
		return setpath(_T(""));
	else if(index == 1)
		return setpath(_T("temp"));
	else
		MessageBox(NULL,_T("������־�ļ�·��ʱ��ʹ���˲��Ϸ��Ĳ���\r\n\r\n֧�ֵĲ���Ϊ��\r\n  0 - ��־�����ڵ�ǰĿ¼\r\n  1 - ��־������ϵͳ��ʱĿ¼"),_T("����·������"),MB_OK);
		return false;
}
bool mylog_op::setpath(const TCHAR *  logPath)
{
	//char szCurPath[MAX_PATH]={0};
	CString str=logPath;
	TCHAR szCurPath[MAX_PATH]={0};
	bool userPath=false;
	if (str.CompareNoCase(_T("temp"))==0)
	{
		//HINSTANCE hs;
		//hs=AfxGetInstanceHandle();
		//hs=AfxGetApp()->m_hInstance;  ��Ч
#ifdef _UNICODE
		//GetModuleFileName(hs,(LPWCH)szCurPath,MAX_PATH);
		//GetTempPath(MAX_PATH/2,(wchar_t *)szCurPath);
		GetTempPath(MAX_PATH,szCurPath);	//��õ�temp·����β���з�б��
#else
		//GetModuleFileName(hs,szCurPath,MAX_PATH);
		GetTempPath(MAX_PATH,szCurPath);
#endif
		pathError=false;
	}
	else if(str.IsEmpty())
	{
#ifdef _UNICODE
		GetModuleFileName((HMODULE)AfxGetInstanceHandle(),(LPWCH)szCurPath,MAX_PATH);
		//��ȡ��·�����ļ������������д���
		//GetTempPath(MAX_PATH,(LPWCH)szCurPath);
#else
		GetModuleFileName((HMODULE)AfxGetInstanceHandle(),szCurPath,MAX_PATH);
		//GetTempPath(MAX_PATH,szCurPath);
#endif
		pathError=false;
	}
	else
	{
		userPath=true;
		file.open(str,fstream::in|fstream::app);	//��д��׷�ӵķ�ʽ��
		str.ReleaseBuffer();
		if(file.is_open())
		{
			file<<"  "<<endl;
			file.close();
			pathError=false;
		}
		else
		{
			filepath.clear();
			wfilepath.clear();
			pathError=true;
			MessageBox(NULL,_T("������־�ļ�·��ʱ��ʹ���˲��Ϸ���·����"),_T("����·������"),MB_OK);
			return false;
		}	
	}
	CString strPath;
if(userPath)	//���ʹ���û�·��������־·��ֱ��ʹ�ô���Ĳ���
	strPath.Format(_T("%s"),logPath);
else		//����
{
	strPath.Format(_T("%s"),szCurPath);
	int nPos=strPath.ReverseFind('\\');	//������˳�򣬵�һ���ַ���λ��Ϊ
	int len=strPath.GetLength();	//���������
   strPath=strPath.Left(nPos+1);		//�������ȡ��ǰ·��ʱ�����ļ���
}
//	CString path2,strFilePath;
//	path2=strPath.Left(nPos+1);	//ȡ���һ����б��֮ǰ���ַ���
// 	if(!userPath)
// 	strFilePath=path2+_T("log.txt");
	CString strFilePath;
#ifdef _UNICODE
	wfilepath=strPath.GetBuffer();
	if(!userPath)
	{
		wfilepath+=wLogName;
	}
	strFilePath=wfilepath.data();
#else

	filepath=strPath.GetBuffer();
	if(!userPath)
	{
		filepath+=logName;
	}
	strFilePath=filepath.data();
#endif
	strPath.ReleaseBuffer();
	CFileFind finder;
	CFileStatus fsta;
	CFile f;
	if(finder.FindFile(strFilePath))
	{
		CTime NowTime = CTime::GetCurrentTime();
		if(CFile::GetStatus(strFilePath,fsta))	//��CFindFileҲ�ܻ���ļ��Ĵ������޸�ʱ�����Ϣ����MFC���ο��ֲ�
		{
			if(fsta.m_mtime.GetDay()!=NowTime.GetDay())
			{
				//CString t;
				//t.Format(_T("%d  %d"),fsta.m_ctime.GetDay(),NowTime.GetDay());
				//AfxMessageBox(t);
				f.Remove(strFilePath);
				timeFlag2=true;
				write(_T("����־��Ϣ"));
			}
			else
				separate=true;
		}
	}
	else
	{
		timeFlag2=true;
		write(_T("����־��Ϣ"));
	}

	return true;

}
void mylog_op::setLogName(const TCHAR *name)
{
#ifdef _UNICODE	//ʹ�ö��ַ�
		wLogName.assign(name);
		setpath(wLogName.c_str());
#else
		logName.assign(name);
		setpath(logName.c_str());
#endif
		
}
bool mylog_op::write(const TCHAR * data)
{
#pragma region �ж��Ƿ����д��־������
	if(pathError)
	{
		AfxMessageBox(_T("���ȵ���setpath������Ϊ��־ָ�����·��"));
		return false;
	}
	CString info=data;

	if(writemode == 0) 
		return true;
	if(writemode == 1)
	{
#ifndef _DEBUG	//�Ƿ���ģʽ
		return true;
#endif
	}
	if(writemode == 2)
	{
#ifdef  _DEBUG	//�ǵ���ģʽ
		return	true;
#endif
	}
#pragma endregion

#pragma region ���Щ��־·��
	CString strFilePath;

#ifdef _UNICODE
	strFilePath=(TCHAR *)wfilepath.data();
#else
	strFilePath=(TCHAR *)filepath.data();
#endif
#pragma endregion

	bool blankLine=false;
	//if(info.IsEmpty())
	//	blankLine=true;
#pragma region ���д����Ϣǰ�и�ʽ�����ַ����������д���
	CString strleft;
	strleft=info.Left(3);
	if(info.CompareNoCase(_T("-"))==0 ||info.CompareNoCase(_T("="))==0 &&sLayout)
	{
		info=_T(" ");
		tmpNoTimeflag=true;
	}
	else if(info.CompareNoCase(_T("#"))==0 &&sLayout)
		tmpSeparate=true;
	else if((strleft.CompareNoCase(_T("---"))==0||strleft.CompareNoCase(_T("==="))==0) && sLayout)
	{
		CString strRight;
		strRight=info.Right(3);
		blankLine=true;
		if(strRight.CompareNoCase(_T("---"))==0 || strRight.CompareNoCase(_T("==="))==0)
			info+=_T("\r\n");
	}
	else if(info.GetLength()>=1  && sLayout)
	{
		strleft=info.Left(2);
		if(strleft.CompareNoCase(_T(">>"))==0)
		{
			strleft=_T("===");
			info=strleft+info;
		}
		else if(strleft.CompareNoCase(_T("<<"))==0)
		{
			strleft=info.Mid(2,1);
			if(strleft.CompareNoCase(_T("="))!=0 && strleft.CompareNoCase(_T("-"))!=0)
				info.Insert(2,_T("==="));
		}
		else
		{
			strleft=info.Left(1);
			if(strleft.CompareNoCase(_T(">"))==0)
			{
				strleft=_T("---");
				info=strleft+info;
			}
			else if(strleft.CompareNoCase(_T("<"))==0)
			{
				strleft=info.Mid(1,1);
				if(strleft.CompareNoCase(_T("="))!=0 && strleft.CompareNoCase(_T("-"))!=0)
					info.Insert(1,_T("---"));
			}
			else if(strleft.CompareNoCase(_T("��"))==0)
			{
				strleft=_T("===");
				info=strleft+info;
			}
			else if(strleft.CompareNoCase(_T("��"))==0)
			{
				strleft=info.Mid(1,1);
				if(strleft.CompareNoCase(_T("="))!=0 && strleft.CompareNoCase(_T("-"))!=0)
					info.Insert(1,_T("==="));
			}
			//else if(strleft.CompareNoCase(_T(":"))==0 || strleft.CompareNoCase(_T("��"))==0 || strleft.CompareNoCase(_T("_"))==0 )
			//{
			//	info=info;
			//}
			else if(!autoIndent)
			{
				info.Insert(0,_T("    "));
			}
		}
	}
#pragma endregion

#pragma region ����֮ǰ�Ƿ�ӿ���
	if((strleft.Compare(_T("---"))==0||strleft.Compare(_T("==="))==0) && sLayout && level==0)
		blankLine=true;
#pragma endregion

#pragma region ��־�㼶����
	strleft=info.Left(4);
	CString strPrifix;
	if(strleft.CompareNoCase(_T("<---"))==0||strleft.CompareNoCase(_T("<<=="))==0||strleft.CompareNoCase(_T("��==="))==0)
		if(level>0)
			level--;
	if(sLayout && autoIndent)
	{
		for(int i=0;i<level;i++)
		{
			strPrifix+=_T("|   ");
		}
	}
	if(strleft.CompareNoCase(_T("--->"))==0||strleft.CompareNoCase(_T("===>"))==0||strleft.CompareNoCase(_T("===��"))==0)
		level++;

#pragma endregion

#pragma region ������ǰ���ʱ��
	if(timeFlag && !tmpNoTimeflag)	//���Ҫ��¼д��־��ʱ��
	{
		CString strNowTime;
		SYSTEMTIME systime;
		//CTime NowTime = CTime::GetCurrentTime();
		GetLocalTime(&systime);
		if(timeFlag2)
		{
			timeFlag2=false;
			//strNowTime.Format(_T("## %4d-%02d-%02d  "),NowTime.GetYear(),NowTime.GetMonth(),NowTime.GetDay());
			strNowTime.Format(_T("## %4d-%02d-%02d  "),systime.wYear,systime.wMonth,systime.wDay);
		}
		else
			strNowTime.Format(_T("## %02d:%02d:%02d.%03d  "),systime.wHour,systime.wMinute,systime.wSecond,systime.wMilliseconds);
		strNowTime+=strPrifix;
		strNowTime+=info;
		info=strNowTime;
		//	info+=_T("\n");
	}
#pragma endregion

#pragma region ����־��Ϣת������ȷ�ı���
#ifdef _UNICODE
#pragma region ��infoת���ɶ��ַ�
	wchar_t *pwstr=L"";
	pwstr=info.GetBuffer();
	int len=WideCharToMultiByte(CP_ACP,0,pwstr,(int)wcslen(pwstr),NULL,0,NULL,NULL);
	char * chs;
	chs=new char[len+1];
	WideCharToMultiByte(CP_ACP,0,pwstr,(int)wcslen(pwstr),chs,len,NULL,NULL);
	chs[len]='\0';
	info.ReleaseBuffer();
#pragma endregion
#else
	char *chs;
	chs=info.GetBuffer();
#endif
#pragma endregion

#pragma region ����־��Ϣд���ļ�
	static bool givetip=true;
	file.open(strFilePath,fstream::in|fstream::app);	//��д��׷�ӵķ�ʽ��,��֧������·��
	if(file.is_open())
	{
		if(separate || tmpSeparate)
		{
			file<<endl<<"######################################################################"<<endl<<endl;
			separate=false;
		}
		if(blankLine)
			file<<endl;
		if(!tmpSeparate)
			file<<chs<<endl;
		file.close();
	}
	else
		if(givetip)
		{
			CString err=getErrInfo(GetLastError());
			AfxMessageBox(_T("��־�ļ��򿪴���:\r\n")+err+_T("\r\n")+strFilePath);
			
			givetip=false;
		}
#pragma endregion

#pragma region �ƺ�
#ifdef _UNICODE
	delete chs;
#else
	info.ReleaseBuffer();
	chs=NULL;
#endif
	tmpSeparate=false;
	tmpNoTimeflag=false;
#pragma endregion
	return true;
}

bool mylog_op::writeEx(const TCHAR * format,...)
{
	if(pathError)
	{
		AfxMessageBox(_T("���ȵ���setpath������Ϊ��־ָ�����·��"));
		return false;
	}
	va_list arg_ptr;
	TCHAR buff[1024]={0};
	va_start(arg_ptr,format);	//�ѹ̶�������ַ���ȷ����ε��ڴ���ʼ��ַ��
	_vstprintf(buff,format,arg_ptr);
	va_end(arg_ptr);
	CString strBuff; 
	strBuff.Format(_T("%s"),buff);
	return write(strBuff);
}
void mylog_op::setWriteStrategy(short writeMode)
{
	writemode=writeMode;
}
void mylog_op::setIndentStrategy(bool indentMode)
{
	autoIndent=indentMode;
}
void mylog_op::msgbox(const TCHAR * format,...)
{
	if(msgmode == 0)
		return;
	if(msgmode ==1)	
	{
#ifndef _DEBUG
		return;
#endif
	}
	if(msgmode ==2)	
	{
#ifdef _DEBUG
		return;
#endif
	}
	va_list arg_ptr;
	TCHAR buff[1024]={0};
	va_start(arg_ptr,format);	//�ѹ̶�������ַ���ȷ����ε��ڴ���ʼ��ַ��
	_vstprintf(buff,format,arg_ptr);
	va_end(arg_ptr);
	CString strBuff(buff);
	CString preInfo;
#ifdef _UNICODE
	preInfo=wmsgPrifixInfo.c_str();
#else
	preInfo=msgPrifixInfo.c_str();
#endif
	preInfo+=strBuff;
	AfxMessageBox(preInfo);
	return;

}
void mylog_op::setMsgboxPrifixInfo(const TCHAR *info)
{
#ifdef _UNICODE	//ʹ�ö��ַ�
	wmsgPrifixInfo.assign(info);
#else
	msgPrifixInfo.assign(info);
#endif
}

void mylog_op::about()
{
	MessageBox(NULL,_T("    ������κ����\r\n\r\n    QQ��\r\n\r\n    Emain��wei-jianmin@163.com     "),_T("����"),MB_OK);
}

void mylog_op::showError(DWORD errorNo)
{
	if(msgmode == 0)
		return;
	if(msgmode == 1)
	{
#ifndef _DEBUG
		return;
#endif
	}
	if(msgmode == 2)
	{
#ifdef _DEBUG
		return;
#endif
	}
	CString str;
	str=getErrInfo(errorNo);
	AfxMessageBox(str);
}
TCHAR * mylog_op::getErrInfo(DWORD errorNo)
{
	if(lpBuffer!=NULL)
	{
		LocalFree(lpBuffer);
		lpBuffer=NULL;
	}
	FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER|FORMAT_MESSAGE_FROM_SYSTEM,NULL,errorNo,LANG_NEUTRAL,(LPTSTR)&lpBuffer,0,NULL);
	return lpBuffer;
}
void mylog_op::showError()
{
	if(msgmode == 0)
		return;
	if(msgmode == 1)
	{
#ifndef _DEBUG	//˵�����ڷ���ģʽ
		return;
#endif
	}
	if(msgmode == 2)
	{
#ifdef _DEBUG	//˵�����ڵ���ģʽ
		return;
#endif
	}
	DWORD errorNo=GetLastError();
	CString str;
	str=getErrInfo(errorNo);
	AfxMessageBox(str);
}

