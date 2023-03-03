#include "Errors.hpp"
INIT_ERRORS

//using namespace utils;

std::map<unsigned int,std::string> err_map;

#define URL_RETURN_ERROR	0x00000001
#define GET_SEAL_ERROR		0x00000002
#define SIGN_ERROR			0x00000003
#define URL_RET_FMT_ERR		0x00000004
#define DOSIGN_ERROR		0x00000005
#define URL_ERROR			0x00000006
#define ORI_ERROR			0x00000007
#define ADD_ERROR			0x00000008

BEGIN_SET_ERR_MAP
	SET_ERR_MAP_VALUE(URL_ERROR,"url错误")
	SET_ERR_MAP_VALUE(URL_RETURN_ERROR,"url返回错误码")
	SET_ERR_MAP_VALUE(GET_SEAL_ERROR,"获取印章失败")
	SET_ERR_MAP_VALUE(SIGN_ERROR,"签章失败")
	SET_ERR_MAP_VALUE(DOSIGN_ERROR,"后台计算签名失败")
	SET_ERR_MAP_VALUE(URL_RET_FMT_ERR,"url返回数据格式错误")
	SET_ERR_MAP_VALUE(ORI_ERROR,"原始错误")
	SET_ERR_MAP_VALUE(ADD_ERROR,"附加错误")
END_SET_ERR_MAP

void init_err_map()
{
	err_map[URL_ERROR] = "url错误";
	err_map[URL_RETURN_ERROR] = "url返回错误码";
	err_map[GET_SEAL_ERROR] = "获取印章失败";
	err_map[SIGN_ERROR] = "签章失败";
	err_map[DOSIGN_ERROR] = "后台计算签名失败";
	err_map[URL_RET_FMT_ERR] = "url返回数据格式错误";
	err_map[ORI_ERROR] = "原始错误";
	err_map[ADD_ERROR] = "附加错误";
}

Errors post(int e)
{
	return Errors(e);
}

Errors get_seal(int e)
{
	Errors err = post(e);
	if(err != 0)
	{
		err.pushError(GET_SEAL_ERROR);
		return err;
	}
	return 0;
}

Errors do_sign(int e)
{
	Errors err = post(e);
	if(err != 0)
	{
		err.pushError(DOSIGN_ERROR);
		return err;
	}
	return 0;
}

Errors sign(int e)
{
	Errors es;
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

Errors sign2(int e)
{
	Errors es;
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


Errors ff(int x)
{
	if(x==0)
		return ORI_ERROR;
	else
	{
		Errors e = ff(x-1);
		e += ADD_ERROR;
		return e;
	}
}

int main()
{
	init_err_map();
	std::string s;
	Errors es;

	es = es+3;
	es += 4;
	s = es.getErrorString();
	puts(s.c_str());
	puts("");
	es.clear();

	es = ff(55);
	s = es.getErrorString();
	puts(s.c_str());
	puts("");
	es.clear();

	es = sign(URL_RET_FMT_ERR);
	unsigned int err = es.getErrorCode();
	s = Errors::getErrorString(err,err_map);
	puts(s.c_str());
	s = Errors::getErrorString(err);
	puts(s.c_str());
	puts("");
	
	es = sign2(URL_RETURN_ERROR);
	err = es.getErrorCode();
	s = Errors::getErrorString(err,err_map);
	puts(s.c_str());
	s = Errors::getErrorString(err);
	puts(s.c_str());
	puts("");

	es = sign(URL_RET_FMT_ERR);
	err = es.getErrorCode();
	s = Errors::getErrorString(err,err_map);
	puts(s.c_str());
	s = Errors::getErrorString(err);
	puts(s.c_str());
	puts("");

	es = sign2(URL_RET_FMT_ERR);
	err = es.getErrorCode();
	s = Errors::getErrorString(err,err_map);
	puts(s.c_str());
	s = Errors::getErrorString(err);
	puts(s.c_str());
	puts("");

	getchar();
	return 0;
}