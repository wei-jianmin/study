#pragma once
#include <string>
using std::string;
class myini_op
{
public:
	myini_op();
	~myini_op(void);
	const char* getIniPath();
	bool Init(const char * path=".",const char *name="config.ini");
	bool write(const char * appName,const char * keyName,const char * value);
	const char* readString(const char * appName,const char * keyName,const char * defaultValue="");
	int readInt(const char * appName,const char * keyName,const int defaultValue=0);
private:
	string iniPath;
	string iniName;
	bool errPath;
};
