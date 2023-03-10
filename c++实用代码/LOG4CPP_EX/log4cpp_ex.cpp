#include "log4cpp_ex.h"
static void WriteLog(const log4cplus::tostringstream& msg,log4cplus::LogLevel level)
{
	log4cplus::tstring info,str_left,str_right;
	log4cplus::tstring::size_type pos;

	info = msg.str();
	pos = info.find(LOG4CPLUS_TEXT("#!#"));
	if(pos != log4cplus::tstring::npos)		//是有效值(包含所在函数标记)
	{
		str_left = info.substr(0,pos);
		str_right = info.substr(pos+3);
		
		info.empty();
		info = LOG4CPLUS_TEXT("[");

		pos = str_left.rfind(LOG4CPLUS_TEXT("::"));
		if(pos != log4cplus::tstring::npos)	//包含类名及函数名
		{
			info += str_left.substr(pos+2);
		}
		else								//只有所在函数名，没有类名
		{
			info += str_left;
		}
		
		info += LOG4CPLUS_TEXT("] ");
		info += str_right;
	}

	log4cplus::Logger::getRoot().forcedLog(level, info, __FILE__, __LINE__); 
	return;
}