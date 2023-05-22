#include "log4cplus/logger.h"
#include "log4cplus/configurator.h"
#pragma comment(lib,"log4cplusU-mt.lib")
int main()
{
	
	log4cplus::PropertyConfigurator::doConfigure(LOG4CPLUS_TEXT("E:/Desktop/test/log.properties"));
	log4cplus::Logger logger = log4cplus::Logger::getRoot();
	LOG4CPLUS_INFO(logger, LOG4CPLUS_TEXT("Hello world"));
	puts("wait enter");
	getchar();
	return 0;
}