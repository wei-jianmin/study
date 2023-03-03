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
			COesCommon::WriteLog(stm,log4cplus::logLevel##_LOG_LEVEL);\
		}\
	} while (0)