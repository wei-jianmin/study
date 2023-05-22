#include <stdio.h>
/**
 * @brief The LogHelper class
 * 1. 构造函数可以接受[日志路径名]作为可选参数
 * 2. 支持单独的open方法，接受日志路径名参数
 * 3. 文件总是以追加方式打开，可以调用clear方法清空文件内容
 * 4. 提供close方法，但即使不调用，也会在类析构时自动调用
 * 5. 通过set_auto_flush方法，设置是否每次写日志后自动调用flush方法，默认为否
 */
class LogHelper
{
public:
    LogHelper(const char* p=NULL)
	{ 
		 _pf=NULL;
        open(p);
	}
    bool open(const char* p)
	{
		if(p==NULL || strlen(p)==0 || _pf!=NULL)   return false;
		memset(_name,0,256);
		strcpy(_name,p);
        _pf = fopen(p,"a+");
		_auto_flush = false;
		if(_pf)    return true;
		return false;
	}
	void close()
	{
		memset(_name,0,256);
		if(_pf)    fclose(_pf);
		_pf = NULL;
	}
	~LogHelper() 
	{ 
		if(_pf)    fclose(_pf); 
	}
	void set_auto_flush(bool flag) 
	{ 
		_auto_flush = flag; 
	}
	int write(const char* format,...)
	{
		if(!_pf) return 0;
		va_list args;
		va_start(args,format);
		char buf[2048]={0};
		vsnprintf_s(buf,2048,2045,format,args);
		va_end(args);
		int len = fwrite(buf,strlen(buf),1,_pf);
		fwrite("\n",1,1,_pf);
		if(_auto_flush) fflush(_pf);
		return len;
	}
	bool flush()
	{
		if(_pf==NULL)    return false;
		fflush(_pf);
		return true;
	}
	bool clear()
	{
		if(_pf==NULL)    return false;
		fclose(_pf);
		_pf = fopen(_name,"w");
		if(_pf==NULL)    return false;
		fclose(_pf);
		_pf = fopen(_name,"a+");
		if(_pf==NULL)    return false;
		return true;
	}
private:
	FILE *_pf;
	char _name[256];
	bool _auto_flush;
};
