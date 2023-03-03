/*
 * Copyright (c) 2018,EqTeam
 * All rights reserved.
 * FileName:  bmp_struct_def.h
 * Remark:  定义了bmp格式图片的相关结构
 * Version:  V1.0
 * Author:  WeiJM
 * Date:  2018/12/4
 */
#ifndef BMPSTRUCTDEF
#define BMPSTRUCTDEF
#pragma pack(1)		//取消字节对齐
namespace ess{
	//文件头
	typedef struct tagBITMAPFILEHEADER {
		uint16_t   bfType;
		uint32_t   bfSize;
		uint16_t   bfReserved1;
		uint16_t   bfReserved2;
		uint32_t   bfOffBits;
	} BITMAPFILEHEADER;
	
	//信息头
	typedef struct tagBITMAPINFOHEADER{
		uint32_t    biSize;
		int32_t		biWidth;
		int32_t		biHeight;
		uint16_t    biPlanes;
		uint16_t    biBitCount;
		uint32_t    biCompression;		//影响图片格式
		uint32_t    biSizeImage;		
		int32_t		biXPelsPerMeter;	
		int32_t		biYPelsPerMeter;	
		uint32_t    biClrUsed;			//影响调色板颜色数
		uint32_t    biClrImportant;
	} BITMAPINFOHEADER;

	//颜色表
	typedef struct tagRGBQUAD {
		unsigned char    rgbBlue;
		unsigned char    rgbGreen;
		unsigned char    rgbRed;
		unsigned char    rgbReserved;
	} RGBQUAD;

	typedef struct BMPHEADER_tab {
		BITMAPFILEHEADER fileHeader;
		BITMAPINFOHEADER infoHeader;
	} BMPHEADER;
} 
#pragma pack()	//恢复字节对齐
#endif