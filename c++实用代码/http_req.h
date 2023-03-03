/*
 * Copyright (c) 2018,EqTeam
 * All rights reserved.
 * FileName:  HttpReq.h
 * Remark:   https://www.cnblogs.com/linbc/p/5034286.html
 *			 https://blog.csdn.net/moxiaowei5201/article/details/73369376
 * Version:  V1.0
 * Author:  WeiJM
 * Date:  2018/12/5
 */
#ifndef _HTTP_REQ_H
#define _HTTP_REQ_H

#include <utils/stlex/stlex.h>	
#include "../corelib.utils.h"

namespace utils
{

#define TIMESTAMP_QUERY 0
#define X_WWW_FORM_URLENCODED 1
#define APPLICATION_JSON 2
class CORELIB_UTILS_API HttpReq
{
public:
	static int PostData(const stdex::string& url,
		const stdex::string& data,
		stdex::string &reponse,
		const stdex::string& user_name,
		const stdex::string& password,int content_type=0);

private:
	static stdex::string GetParamFromUrl(const char* strUrl);
	static int GetPortFromUrl(const char* strUrl);
	static stdex::string GetIPFromUrl(const char* strUrl);
	static stdex::string GetHostAddrFromUrl(const char* strUrl);
	static int post(const stdex::string& host, const stdex::string& port, 
		const stdex::string& page, const stdex::string& data, 
		const stdex::string& user_name,const stdex::string& password,
		stdex::string& reponse_data,int content_type=TIMESTAMP_QUERY);
};

}

#endif
