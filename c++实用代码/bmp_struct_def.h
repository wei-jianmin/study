/*
 * Copyright (c) 2018,EqTeam
 * All rights reserved.
 * FileName:  bmp_struct_def.h
 * Remark:  ������bmp��ʽͼƬ����ؽṹ
 * Version:  V1.0
 * Author:  WeiJM
 * Date:  2018/12/4
 */
#ifndef BMPSTRUCTDEF
#define BMPSTRUCTDEF
#pragma pack(1)		//ȡ���ֽڶ���
namespace ess{
	//�ļ�ͷ
	typedef struct tagBITMAPFILEHEADER {
		uint16_t   bfType;
		uint32_t   bfSize;
		uint16_t   bfReserved1;
		uint16_t   bfReserved2;
		uint32_t   bfOffBits;
	} BITMAPFILEHEADER;
	
	//��Ϣͷ
	typedef struct tagBITMAPINFOHEADER{
		uint32_t    biSize;
		int32_t		biWidth;
		int32_t		biHeight;
		uint16_t    biPlanes;
		uint16_t    biBitCount;
		uint32_t    biCompression;		//Ӱ��ͼƬ��ʽ
		uint32_t    biSizeImage;		
		int32_t		biXPelsPerMeter;	
		int32_t		biYPelsPerMeter;	
		uint32_t    biClrUsed;			//Ӱ���ɫ����ɫ��
		uint32_t    biClrImportant;
	} BITMAPINFOHEADER;

	//��ɫ��
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
#pragma pack()	//�ָ��ֽڶ���
#endif