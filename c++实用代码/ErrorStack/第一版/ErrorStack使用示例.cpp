#include "ErrorStack.hpp"
INIT_ERROR_STACK

std::map<unsigned int,std::string> err_map;

#define URL_ERROR			0x00000000
#define URL_RETURN_ERROR	0x00000001
#define GET_SEAL_ERROR		0x00000002
#define SIGN_ERROR			0x00000003
#define URL_RET_FMT_ERR		0x00000004
#define DOSIGN_ERROR		0x00000005

void init_err_map()
{
	err_map[URL_ERROR] = "url错误";
	err_map[URL_RETURN_ERROR] = "url返回错误码";
	err_map[GET_SEAL_ERROR] = "获取印章失败";
	err_map[SIGN_ERROR] = "签章失败";
	err_map[DOSIGN_ERROR] = "后台计算签名失败";
	err_map[URL_RET_FMT_ERR] = "url返回数据格式错误";
}

ErrorStack post(int e)
{
	return ErrorStack(e);
}

ErrorStack get_seal(int e)
{
	ErrorStack err = post(e);
	if(err != 0)
	{
		err.pushError(GET_SEAL_ERROR);
		return err;
	}
	return 0;
}

ErrorStack do_sign(int e)
{
	ErrorStack err = post(e);
	if(err != 0)
	{
		err.pushError(DOSIGN_ERROR);
		return err;
	}
	return 0;
}

ErrorStack sign(int e)
{
	ErrorStack es;
	es = get_seal(e);
	if(es != 0)
	{
		es.pushError(SIGN_ERROR);
		return es;
	}
	es = do_sign(e);
	if(es != 0)
	{
		es.pushError(SIGN_ERROR);
		return es;
	}
	return 0;
}

ErrorStack sign2(int e)
{
	ErrorStack es;
	es = get_seal(0);
	if(es != 0)
	{
		es.pushError(SIGN_ERROR);
		return es;
	}
	es = do_sign(e);
	if(es != 0)
	{
		es.pushError(SIGN_ERROR);
		return es;
	}
	return 0;
}

int main()
{
	init_err_map();

	ErrorStack es = sign(URL_RET_FMT_ERR);
	unsigned int err = es.getErrorCode();
	std::string s = ErrorStack::getErrorString(err_map,err);
	puts(s.c_str());
	
	es = sign2(URL_RETURN_ERROR);
	err = es.getErrorCode();
	s = ErrorStack::getErrorString(err_map,err);
	puts(s.c_str());

	es = sign(URL_RET_FMT_ERR);
	err = es.getErrorCode();
	s = ErrorStack::getErrorString(err_map,err);
	puts(s.c_str());

	es = sign2(URL_RET_FMT_ERR);
	err = es.getErrorCode();
	s = ErrorStack::getErrorString(err_map,err);
	puts(s.c_str());

	getchar();
	return 0;
}