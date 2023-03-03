/***************************************************************************** 
* FileName: cu_loger.h
* Description:
* Version: 
* Author:  ZhangW
* Date:  // 2019/7/29
*****************************************************************************/

#ifndef CU_LOGER_H_
#define CU_LOGER_H_


#include <log4cplus/loglevel.h>
#include <log4cplus/logger.h>
#include "../corelib.utils.h"

#define LOG_LAST_ERR //LOG4CPLUS_ERROR(log4cplus::Logger::getRoot(),"["<<__FUNCTION__<<"] last_error ="<<std::hex<<//COesCommon::last_err)
//#define LOG_FUNC_NAME LOG4CPLUS_TRACE(log4cplus::Logger::getRoot(),"["<<__FUNCTION__<<"]")

//带函数名的日志方法，不能用于COesCommon类中
#define LOG4CPLUS_TRACE_EX(logEvent) LOG4CPLUS_MACRO_BODY_EX (logEvent, TRACE)
#define LOG4CPLUS_DEBUG_EX(logEvent) LOG4CPLUS_MACRO_BODY_EX (logEvent, DEBUG)
#define LOG4CPLUS_INFO_EX(logEvent) LOG4CPLUS_MACRO_BODY_EX (logEvent, INFO)
#define LOG4CPLUS_WARN_EX(logEvent) LOG4CPLUS_MACRO_BODY_EX (logEvent, WARN)
#define LOG4CPLUS_ERROR_EX(logEvent) LOG4CPLUS_MACRO_BODY_EX (logEvent, ERROR)
#define LOG4CPLUS_FATAL_EX(logEvent) LOG4CPLUS_MACRO_BODY_EX (logEvent, FITAL)
#define LOG4CPLUS_MACRO_BODY_EX(logEvent,logLevel)	\
	do {\
	if(log4cplus::Logger::getRoot().isEnabledFor(log4cplus::logLevel##_LOG_LEVEL)){\
	log4cplus::tostringstream stm;\
	stm<<__FUNCTION__<<"#!#"<<logEvent;\
	utils::CuLoger::WriteLog(stm,log4cplus::logLevel##_LOG_LEVEL);\
	}\
	} while (0)

namespace utils
{
	class LogFuncName
	{
	public:
		LogFuncName(const char* func_name)
		{
			func_name_ = func_name;
			LOG4CPLUS_TRACE(log4cplus::Logger::getRoot(),">>> ["<<func_name_.c_str()<<"]");
		}
		~LogFuncName()
		{
			LOG4CPLUS_TRACE(log4cplus::Logger::getRoot(),"<<< ["<<func_name_.c_str()<<"]");
		}
	private:
		std::string func_name_;
	};
	class CORELIB_UTILS_API CuLoger
	{
	public:
		static void WriteLog(const log4cplus::tostringstream& msg,log4cplus::LogLevel level);
	};

}

#define LOG_FUNC_NAME utils::LogFuncName _auto_log_func_name_(__FUNCTION__)

#endif //CU_LOGER_H_