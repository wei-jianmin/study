#ifndef FS_HELPER_H_
#define FS_HELPER_H_
#include <stdio.h>
#include <utils/equtils/inc/str_help.hpp>

#ifdef _WINDOWS
#include <Windows.h>
#endif

#ifndef UTF_LOCAL_CVT
#define UTF_LOCAL_CVT
#ifdef _WINDOWS
//utf-8->本地路径化
#define UTF2LOCAL(path)				UTA(path)
#define LOCAL2UTF(path)				ATU(path)
#else
//utf-8->本地路径化
#define UTF2LOCAL(path)				path
#define LOCAL2UTF(path)				path
#endif
#endif
namespace utils
{
	class FsHelper
	{
	public:
		static std::string GetTmpPath()
		{
			std::string str_path;

#ifdef _WINDOWS
			char szPath[1024]={0};
			BOOL bRet = SHGetSpecialFolderPathA(NULL, szPath, CSIDL_COMMON_APPDATA, FALSE);
			str_path = szPath;
			str_path = LOCAL2UTF(str_path);
#else
			str_path = "/tmp";
#endif
			return FORMATPATH(str_path);
		}

		static std::string GetOesTmpPath()
		{
			std::string oes_tmp_path;
			std::string tmp_path = GetTmpPath();
			oes_tmp_path = tmp_path + "/oesplugin";
			//创建文件夹
			if(utils::FsUtils::IsDirectory(oes_tmp_path) == false)
			{
				utils::FsUtils::CreateDirectory(oes_tmp_path);
			}
			return FORMATPATH(oes_tmp_path);
		}

		static bool SaveDataToPathname(const std::string &pathname,const std::string &data)
		{
			std::string _pathname = UTF2LOCAL(pathname);
			FILE * pf = fopen(_pathname.c_str(),"wb");
			if(pf)
			{
				fwrite(data.c_str(),data.length(),1,pf);
				fclose(pf);
				return true;
			}
			return false;
		}

		static bool SaveDataToTempPath(const std::string &filename,const std::string &data)
		{
			std::string pathname;
			pathname = GetTmpPath();
			pathname += "/";
			pathname += filename;
			return SaveDataToPathname(pathname,data);
		}
		
		static bool GetFileData(const std::string &pathname,std::string &data)
		{
			FILE * pf = fopen(pathname.c_str(),"rb");
			if(pf)
			{
				fseek(pf,0,SEEK_END);
				unsigned int l = ftell(pf);
				data.clear();
				data.assign(l,0);
				fseek(pf,0,SEEK_SET);
				unsigned char* pdata = (unsigned char*)data.c_str();
				fread(pdata,l,1,pf);
				fclose(pf);
				return true;
			}
			else
				return false;
		}
	};

}

#endif