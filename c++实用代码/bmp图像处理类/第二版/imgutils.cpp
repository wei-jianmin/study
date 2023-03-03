#include "imgutils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 
namespace iu{
	
#define TAKE_LOW_BYTE(w) (w & 0xff)
#define TAKE_HIGH_BYTE(w) ((w & 0xff00) >> 8)
#define TAKE_LOW_WORD(dw) (dw & 0xffff)
#define TAKE_HIGH_WORD(dw) ((dw & 0xffff0000) >> 16)
//计算bmp图像每行字节数
#define CALC_LINE_BITS(bpp,w) ((((w * bpp) + 31) >> 5) << 2)


bool _save_data_in_pixs(bool bdata[27],pix32 pix[10]);
bool _save_data_in_pix(bool bdata[3],pix32 &pix,pix32 prev_pix,pix32 base_pix);

union byte_util
{
	struct 
	{
		unsigned char b7:1;
		unsigned char b6:1;
		unsigned char b5:1;
		unsigned char b4:1;
		unsigned char b3:1;
		unsigned char b2:1;
		unsigned char b1:1;
		unsigned char b0:1;
	} b;
	unsigned char c;
};

union byte2_util
{
	struct 
	{
		unsigned char b17:1;
		unsigned char b16:1;
		unsigned char b15:1;
		unsigned char b14:1;
		unsigned char b13:1;
		unsigned char b12:1;
		unsigned char b11:1;
		unsigned char b10:1;
		unsigned char b07:1;
		unsigned char b06:1;
		unsigned char b05:1;
		unsigned char b04:1;
		unsigned char b03:1;
		unsigned char b02:1;
		unsigned char b01:1;
		unsigned char b00:1;
	} b;
	unsigned short s;
};

union byte4_util
{
	struct 
	{
		unsigned char b37:1;
		unsigned char b36:1;
		unsigned char b35:1;
		unsigned char b34:1;
		unsigned char b33:1;
		unsigned char b32:1;
		unsigned char b31:1;
		unsigned char b30:1;
		unsigned char b27:1;
		unsigned char b26:1;
		unsigned char b25:1;
		unsigned char b24:1;
		unsigned char b23:1;
		unsigned char b22:1;
		unsigned char b21:1;
		unsigned char b20:1;
		unsigned char b17:1;
		unsigned char b16:1;
		unsigned char b15:1;
		unsigned char b14:1;
		unsigned char b13:1;
		unsigned char b12:1;
		unsigned char b11:1;
		unsigned char b10:1;
		unsigned char b07:1;
		unsigned char b06:1;
		unsigned char b05:1;
		unsigned char b04:1;
		unsigned char b03:1;
		unsigned char b02:1;
		unsigned char b01:1;
		unsigned char b00:1;
	} b;
	unsigned long l;
};

img_util::img_util()
{
	_bpp=_w=_h=0;
	_line_width = 0;
	_pallet_len = 0;
	_data_len = 0;
	_data=_pallet=NULL;
	_data_ok = false;
	_attach_flag = false;
	_big_endian = _IsBig_Endian();
	memset(_file_name,0,256);
}

img_util::img_util( u16 bpp,u16 w,u16 h,u8* data/*=NULL*/,u8* pallet/*=NULL*/ )
{
	_attach_flag = false;
	_init(bpp,w,h,data,pallet);
	_big_endian = _IsBig_Endian();
	memset(_file_name,0,256);
}

img_util::img_util( const char* file_path )
{
	_attach_flag = false;
	_big_endian = _IsBig_Endian();
	_load_from_file(file_path);
	strcpy(_file_name,file_path);
}

//
void img_util::_init(u16 bpp,u16 w,u16 h,const u8* data_ref/*=NULL*/,const u8* pallet_ref/*=NULL*/)
{
	_data_ok=false;
	if(bpp==0 || w==0 || h==0)
		return;
		
	_bpp = bpp;
	_w = w;
	_h = h;
	_line_width = CALC_LINE_BITS(bpp,w);
	_data_len = _line_width*_h;
	if(bpp==1)
	{
		_pallet_len=8;
	}
	else if(bpp==8)
	{
		_pallet_len = 1024;
	}
	else if(bpp==24 ||bpp==32)
	{
		_pallet_len = 0;
	}
	else
	{
		return;
	}

	_data = (u8*)malloc(_data_len);
	if(data_ref)
		memcpy(_data,data_ref,_data_len);
	else
		memset(_data,0,_data_len);
	if(_pallet_len>0)
	{
		_pallet = (u8*)malloc(_pallet_len);
		if(pallet_ref)
			memcpy(_pallet,pallet_ref,_pallet_len);
		else
			memset(_pallet,0,_pallet_len);
	}
	_data_ok = true;
}

u8* img_util::_locate_pix( u16 r,u16 c )
{
	if(_data_ok==false)
		return NULL;
	if(_check_r_c(r,c) == false)
		return NULL;
	if(_data==NULL)
		return NULL;

	r = _h - 1 - r;	//实际图像文件，最底下算第1行
	u32 offset=0;
	offset += _line_width*r;
	if(_bpp==1)
	{
		offset += c/8;
	}
	else if(_bpp==8)
	{
		offset += c;
	}
	else if(_bpp==24)
	{
		offset += c*3;
	}
	else if(_bpp==32)
	{
		offset += c*4;
	}
	else
		return NULL;
	return _data+offset;
}

bool img_util::set_img_info(u16 bpp,u16 w,u16 h,const u8* data_ref/*=NULL*/,const u8* pallet_ref/*=NULL*/)
{
	if(_data_ok) 
	{
		_clear_data();
	}

	_init(bpp,w,h,data_ref,pallet_ref);
	if(_data_ok)
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool img_util::_check_r_c(u16 r,u16 c)
{
	if(r >= _h)
		return false;
	if(c >= _w)
		return false;
	return true;
}

bool img_util::setpix1( u16 r,u16 c,pix1 b1 )
{
	if(_bpp!=1)
		return false;
	u8 * p = _locate_pix(r,c);
	if(p==NULL) return false;
	u8 pix = 1;
	pix <<= 7-(c%8);
	if(b1)
	{
		*p |= pix;
	}
	else
	{
		pix = ~pix;
		*p = *p & pix;
	}
	return true;
}

bool img_util::setpix8( u16 r,u16 c,pix8 b8 )
{
	if(_bpp!=8)
		return false;
	u8 * p = _locate_pix(r,c);
	if(p==NULL) return false;
	*p = b8;
	return true;
}

bool img_util::setpix24( u16 r,u16 c,pix32 b24,color_channel channel_index/*=0*/)
{
	if(_bpp!=24)
		return false;
	u8 * p = _locate_pix(r,c);
	if(p==NULL) return false;
	switch(channel_index)
	{
	case 0:
		*p = b24.c.b;
		*(p+1) = b24.c.g;
		*(p+2) = b24.c.r;
		break;
	case 1:
		*(p+2) = b24.c.r;
		break;
	case 2:
		*(p+1) = b24.c.g;
		break;
	case 3:
		*p = b24.c.b;
		break;
	}
	return true;
}

bool img_util::setpix32( u16 r,u16 c,pix32 b32,color_channel channel_index/*=0*/ )
{
	if(_bpp!=32)
		return false;
	u8 * p = _locate_pix(r,c);
	if(p==NULL) return false;
	switch(channel_index)
	{
	case 0:
		*p = b32.c.b;
		*(p+1) = b32.c.g;
		*(p+2) = b32.c.r;
		*(p+3) = b32.c.a;
		break;
	case 1:
		*(p+2) = b32.c.r;
		break;
	case 2:
		*(p+1) = b32.c.g;
		break;
	case 3:
		*p = b32.c.b;
		break;
	}
	return true;
}

iu::pix1 img_util::getpix1( u16 r,u16 c )
{
	if(_bpp!=1)
		return false;
	u8 * p = _locate_pix(r,c);
	if(p==NULL) return false;
	u8 c2 = c%8;
	u8 c3 = 1<<(7-c2);
	u8 pixs = *p;
	u8 pix = pixs & c3;
	if(pix != 0)
		return true;
	else
		return false;
}

iu::pix8 img_util::getpix8( u16 r,u16 c )
{
	if(_bpp!=8)
		return 0;
	pix8 pix=0;
	u8 * p = _locate_pix(r,c);
	if(p==NULL) return pix;
	pix = *(u8*)p;
	return pix;
}

iu::pix32 img_util::getpix24( u16 r,u16 c )
{
	pix32 pix;
	pix.v=0;
	if(_bpp!=24)
		return pix;
	u8 * p = _locate_pix(r,c);
	if(p==NULL) return pix;
	pix.v=*(u32*)p;
	pix.c.a=0;
	return pix;
}

iu::pix32 img_util::getpix32( u16 r,u16 c )
{
	pix32 pix;
	pix.v=0;
	if(_bpp!=32)
		return pix;
	u8 * p = _locate_pix(r,c);
	if(p==NULL) return pix;
	pix.v=*(u32*)p;
	return pix;
}

img_util::~img_util()
{
	_clear_data();
}

void img_util::_clear_data()
{
	_bpp=_w=_h=0;
	if(_attach_flag)
	{
		_data = NULL;
		_pallet = NULL;
		_data_ok = false;
		_attach_flag = false;
		return;
	}
	if(_data) free(_data);
	if(_pallet) free(_pallet);
	_data_ok = false;
}

bool img_util::is_data_ok()
{
	return _data_ok;
}

bool img_util::load_from_file( const char* file_path )
{
	if(_data_ok)
	{
		_data_ok = false;
		_clear_data();
	}
	return _load_from_file(file_path);
}

bool img_util::save_as_file( const char* file_path )
{
	if(!_data_ok)
		return false;
	BMPFILEHEADER fileh;
	BMPINFOHEADER infoh;
	memset(&fileh,0,sizeof(fileh));
	memset(&infoh,0,sizeof(infoh));
	if(_bpp == 1)
	{
		fileh.bfOffBits = 62;
	}
	else if(_bpp == 8)
	{
		fileh.bfOffBits = 1078;
	}
	else if(_bpp == 24 || _bpp == 32)
	{
		fileh.bfOffBits = 54;
	}
	fileh.bfReserved1 = 0;
	fileh.bfReserved2 = 0;
	fileh.bfSize = sizeof(BMPFILEHEADER)+sizeof(BMPINFOHEADER)+_pallet_len+_data_len;
	fileh.bfType = 0x4d42;
	infoh.biBitCount = _bpp;
	infoh.biClrImportant = 0;
	infoh.biClrUsed = 0;
	infoh.biCompression = 0;
	infoh.biHeight = _h;
	infoh.biPlanes = 1;
	infoh.biSize = sizeof(BMPINFOHEADER);
	infoh.biSizeImage = 0;
	infoh.biWidth = _w;
	infoh.biXPelsPerMeter = 2835;
	infoh.biYPelsPerMeter = 2835;

	if(file_path == NULL)
		file_path = _file_name;
	FILE * pf = fopen(file_path,"wb");
	if(pf==NULL)
	{
		char buf[512]={0};
		sprintf(buf,"save_as_file : file open error : %s",file_path);
		puts(buf);
		return	 false;
	}
	fwrite(&fileh,sizeof(fileh),1,pf);
	fwrite(&infoh,sizeof(infoh),1,pf);
	if(_pallet)
	{
		fwrite(_pallet,_pallet_len,1,pf);
	}
	if(_data)
	{
		fwrite(_data,_data_len,1,pf);
	}
	fclose(pf);
	return true;
}

pix32 img_util::get_pallet_color(u8 index)
{
	pix32 pix;
	pix.v = 0;
	if(!_data_ok)
		return pix;
	if(_pallet == NULL)
		return pix;
	if(_bpp==1)
	{
		if(index==0 || index==1)
		{
			pix.c.b = _pallet[4*index];
			pix.c.g = _pallet[4*index+1];
			pix.c.r = _pallet[4*index+2];
			pix.c.a = 0;
		}
	}
	else if(_bpp==8)
	{
		if(index>=0 && index<=255)
		{
			pix.c.b = _pallet[4*index];
			pix.c.g = _pallet[4*index+1];
			pix.c.r = _pallet[4*index+2];
			pix.c.a = 0;
		}
	}
	return pix;
}

bool img_util::set_pallet_color(u8 index,pix32 color)
{
	if(!_data_ok)
		return false;
	if(_pallet == NULL)
		return false;
	if(_bpp==1)
	{
		if(index==0 || index==1)
		{
			_pallet[4*index] = color.c.b;
			_pallet[4*index+1] = color.c.g;
			_pallet[4*index+2] = color.c.r;
			_pallet[4*index+3] = 0;
			return true;
		}
	}
	else if(_bpp==8)
	{
		if(index>=0 && index<=255)
		{
			_pallet[4*index] = color.c.b;
			_pallet[4*index+1] = color.c.g;
			_pallet[4*index+2] = color.c.r;
			_pallet[4*index+3] = 0;
			return true;
		}
	}
	return false;
}

bool img_util::attach_img_data( u16 bpp,u16 w,u16 h,u8* data,u8* pallet/*=NULL*/ )
{
	if(_data_ok)
	{
		_data_ok = false;
		_clear_data();
	}

	_data_ok=false;
	if(bpp==0 || w==0 || h==0 || data==NULL)
		return false;

	_bpp = bpp;
	_w = w;
	_h = h;
	_line_width = CALC_LINE_BITS(bpp,w);
	_data_len = _line_width*_h;
	if(bpp==1)
	{
		_pallet_len=2;
		if(pallet==NULL)
			return false;
	}
	else if(bpp==8)
	{
		_pallet_len = 256;
		if(pallet==NULL)
			return false;
	}
	else if(bpp==24 ||bpp==32)
	{
		_pallet_len = 0;
	}
	else
	{
		return false;
	}

	_data = data;
	_pallet = pallet;
	_data_ok = true;
	_attach_flag = true;

	return _data_ok;
}

bool img_util::detach_img_data()
{
	_clear_data();
	return true;
}

bool img_util::_IsBig_Endian()
{
	unsigned short test = 0x1234;
	if(*( (unsigned char*) &test ) == 0x12)
		return true;
	else
		return false;
}//IsBig_Endian()

bool img_util::_load_from_file( const char* file_path )
{
	FILE *pf = fopen(file_path,"rb");
	if(pf==NULL)
	{
		char buf[512]={0};
		sprintf(buf,"_load_from_file : file open error : %s",file_path);
		puts(buf);
		_data_ok = false;
		return false;
	}

	BMPFILEHEADER fileh;
	BMPINFOHEADER infoh;
	fseek(pf,0,SEEK_END);
	int filelen = ftell(pf);
	if(filelen < 60)
	{
		_data_ok = false;
		fclose(pf);
		return false;
	}

	fseek(pf,0,SEEK_SET);
	fread(&fileh,sizeof(BMPFILEHEADER),1,pf);
	fread(&infoh,sizeof(BMPINFOHEADER),1,pf);
	if(filelen > fileh.bfSize)
	{
		if(fileh.bfSize>0)
			filelen = fileh.bfSize;
	}

	if(TAKE_LOW_BYTE(fileh.bfType)!='B' || TAKE_HIGH_BYTE(fileh.bfType)!='M')
	{
		_data_ok = false;
		fclose(pf);
		return false;
	}

	u16 bpp,w,h;
	bpp = infoh.biBitCount;
	w = infoh.biWidth;
	h = infoh.biHeight;
	u32 offset = fileh.bfOffBits;
	_init(bpp,w,h,NULL,NULL);
	u32 data_len = filelen - fileh.bfOffBits;
	if(data_len > _data_len)
		data_len = _data_len;

	if(bpp==1 || bpp==8)
	{
		fread(_pallet,_pallet_len,1,pf);
		fseek(pf,offset,SEEK_SET);
		fread(_data,data_len,1,pf);
		_data_ok = true;
	}
	else if(bpp==24 || bpp==32)
	{
		fseek(pf,offset,SEEK_SET);
		fread(_data,data_len,1,pf);
		_data_ok = true;
	}
	fclose(pf);
	return true;
}

img_util_ex::img_util_ex() : img_util()
{

}

img_util_ex::img_util_ex( const char* file_path ) : img_util(file_path)
{

}

img_util_ex::img_util_ex( u16 bpp,u16 w,u16 h,u8* data/*=NULL*/,u8* pallet/*=NULL*/ )
						:img_util(bpp,w,h,data,pallet)
{

}

iu::sections img_util_ex::scan_color_sections(u16 line_index, u16 lstw/*=100*/,u8 tolarance/*=5*/,bool greedymode/*=true*/,color_channel channel_index/*=0*/)
{
	section s;
	sections secs;
	secs.clear();
	if(_bpp!=24 && _bpp!=32)
		return secs;
	if(!_data_ok)
		return secs;
	if(_w < lstw)
		return secs;
	if(_data==NULL)
		return secs;
	pix32 base_pix,this_pix;
	u16 base_pos = 0;
	u16 i;
	if(_bpp==24)
	{
		base_pix = getpix24(line_index,0);
		for(i=1;i<_w;i++)
		{
			this_pix = getpix24(line_index,i);
			if(_pix32_similar(base_pix,this_pix,tolarance,channel_index))
			{
				if(greedymode)		//贪婪模式，寻求更大的区间
					continue;
				else				//满足模式，只要空间达到要求，即记录
				{
					if(i-base_pos<lstw)	 //达不到最小标准时
						continue;
				}
			}
			if(i-base_pos>=lstw)
			{
				s.x0 = base_pos;
				s.x1 = i;
				secs.push_back(s);
			}
			base_pix = getpix24(line_index,i);
			base_pos = i;
		}
	}
	else if(_bpp==32)
	{
		base_pix = getpix32(line_index,0);
		for(i=1;i<_w;i++)
		{
			this_pix = getpix32(line_index,i);
			if(_pix32_similar(base_pix,this_pix,tolarance,channel_index))
			{
				if(greedymode)		//贪婪模式，寻求更大的区间
					continue;
				else				//满足模式，只要空间达到要求，即记录
				{
					if(i-base_pos<lstw)	 //达不到最小标准时
						continue;
				}
			}
			if(i-base_pos>=lstw)
			{
				s.x0 = base_pos;
				s.x1 = i;
				secs.push_back(s);
			}
			base_pix = getpix32(line_index,i);
			base_pos = i;
		}
	}
	if(i-base_pos>=lstw)
	{
		s.x0 = base_pos;
		s.x1 = i;
		secs.push_back(s);
	}
	return secs;
}

//确认下区间中没有其他颜色，例如有一条横线掺杂在区间中
void img_util_ex::_check_sections(sections& secs,u8 tolarance,u16 begin_line_index,u16 end_line_index,color_channel channel_index/*=0*/)
{
	section s;
	u16 line_index=begin_line_index;
	pix32 base_pix,this_pix;
	std::vector<u16> bad_secs;
	bool break_flag;
	if(_bpp == 24)
	{
		for(int i=0;i<secs.size();i++)	//取每个区间
		{
			s = secs[i];
			base_pix = getpix24(begin_line_index,s.x0);
			break_flag = false;
			for(int j=s.x0;j<s.x1;j++)	//反斜线扫描本区间
			{
				if(line_index > end_line_index)
					line_index = begin_line_index;
				this_pix = getpix24(line_index,j);
				if(_pix32_similar(this_pix,base_pix,tolarance,channel_index) == false)	//发现坏点
				{
					bad_secs.push_back(i);	//记录本区间
					break_flag = true;
					break;					//退出本区间扫描
				}
				++line_index;
			}
			if(break_flag)
				continue;
			line_index=end_line_index;
			base_pix = getpix24(end_line_index,s.x0);
			for(int j=s.x0;j<s.x1;j++)	//正斜线扫描本区间
			{
				if(line_index<=begin_line_index)
					line_index = end_line_index;
				this_pix = getpix24(line_index,j);
				if(_pix32_similar(this_pix,base_pix,tolarance,channel_index) == false)	//发现坏点
				{
					bad_secs.push_back(i);	//记录本区间
					break;					//退出本区间扫描
				}
				--line_index;
			}
		}
	}
	else if(_bpp == 32)
	{
		for(int i=0;i<secs.size();i++)	//取每个区间
		{
			s = secs[i];
			break_flag = false;
			base_pix = getpix32(begin_line_index,s.x0);
			for(int j=s.x0;j<s.x1;j++)	//扫描本区间
			{
				++line_index;
				if(line_index>=end_line_index)
					line_index = begin_line_index;
				this_pix = getpix32(line_index,j);
				if(_pix32_similar(this_pix,base_pix,tolarance,channel_index) == false)	//发现坏点
				{
					bad_secs.push_back(i);	//记录本区间
					break_flag = true;
					break;					//退出本区间扫描
				}
			}
			if(break_flag)
				continue;
			line_index=end_line_index;
			base_pix = getpix32(end_line_index,s.x0);
			for(int j=s.x0;j<s.x1;j++)	//正斜线扫描本区间
			{
				if(line_index<=begin_line_index)
					line_index = end_line_index;
				this_pix = getpix32(line_index,j);
				if(_pix32_similar(this_pix,base_pix,tolarance,channel_index) == false)	//发现坏点
				{
					bad_secs.push_back(i);	//记录本区间
					break;					//退出本区间扫描
				}
				--line_index;
			}
		}
	}
	
	while(bad_secs.size()>0)
	{
		u16 i = bad_secs.back();
		bad_secs.pop_back();
		secs.erase(secs.begin()+i);
	}
}

//Odd
bool img_util_ex::_OddOnes(u8 x)  
{
    x = x ^ (x >> 4);
    x = x ^ (x >> 2);
    x = x ^ (x >> 1);
	return x & 1;  
}

bool img_util_ex::_PixCmp(pix32 p1,pix32 p2,bool b[3])
{
	return _PixCmp(p1,p2,b[0],b[1],b[2]);
}

bool img_util_ex::_PixCmp(pix32 p1,pix32 p2,bool b0,bool b1,bool b2)
{
	if(b0)
	{
		if(abs(p1.c.b-p2.c.b) != 2)
			return false;
	}
	else
	{
		if(abs(p1.c.b-p2.c.b) != 1)
			return false;
	}
	if(b1)
	{
		if(abs(p1.c.g-p2.c.g) != 2)
			return false;
	}
	else
	{
		if(abs(p1.c.g-p2.c.g) != 1)
			return false;
	}
	if(b2)
	{
		if(abs(p1.c.r-p2.c.r) != 2)
			return false;
	}
	else
	{
		if(abs(p1.c.r-p2.c.r) != 1)
			return false;
	}
	return true;
}

pix32 img_util_ex::_get_equal_pixs_inline(u16 line_index,u16 &col,u16 line_width)
{
	pix32 p0;
	p0.v = 0;
	if(_bpp==24)
	{
		p0 = getpix24(line_index,col);
		while(col<line_width)
		{
			++col;
			pix32 p1 = getpix24(line_index,col);
			if(p0.v != p1.v)
				break;
		}
	}
	else if(_bpp==32)
	{
		p0 = getpix32(line_index,col);
		while(col<line_width)
		{
			++col;
			pix32 p1 = getpix32(line_index,col);
			if(p0.v != p1.v)
				break;
		}
	}
	return p0;
}

i32 img_util_ex::_abstract_data_inline(u16 line_index,u16 col_index,pix32 base_pix)
{
    pix32 pix0;
    pix32 pix1;

    u16 col = col_index;
    if(col_index == 0)
        pix1 = base_pix;
    else if(_bpp==24)
	{
		pix1 = getpix24(line_index,col_index-1);
	}
	else if(_bpp==32)
	{
		pix1 = getpix32(line_index,col_index-1);
	}
	else
	{
		return -1;
	}

    bool flags[18]={false};
    for(int i=0;i<6;i++)
    {
        pix0.v = pix1.v;
        pix1 = _get_equal_pixs_inline(line_index,col,_w);
        if(abs(pix1.c.b-pix0.c.b)==1)
            flags[i*3+0] = false;
        else if(abs(pix1.c.b-pix0.c.b)==2)
            flags[i*3+0] = true;
        else
            return -1;
        if(abs(pix1.c.g-pix0.c.g)==1)
            flags[i*3+1] = false;
        else if(abs(pix1.c.g-pix0.c.g)==2)
            flags[i*3+1] = true;
        else
            return -1;
        if(abs(pix1.c.r-pix0.c.r)==1)
            flags[i*3+2] = false;
        else if(abs(pix1.c.r-pix0.c.r)==2)
            flags[i*3+2] = true;
        else
            return -1;
    }
    byte_util b1,b2;
   flags[0] ? b1.b.b0=1 : b1.b.b0=0;
   flags[1] ? b1.b.b1=1 : b1.b.b1=0;
   flags[2] ? b1.b.b2=1 : b1.b.b2=0;
   flags[3] ? b1.b.b3=1 : b1.b.b3=0;
   flags[4] ? b1.b.b4=1 : b1.b.b4=0;
   flags[5] ? b1.b.b5=1 : b1.b.b5=0;
   flags[6] ? b1.b.b6=1 : b1.b.b6=0;
   flags[7] ? b1.b.b7=1 : b1.b.b7=0;
   if(_OddOnes(b1.c) != flags[8])
       return -1;

   flags[9] ? b2.b.b0=1 : b2.b.b0=0;
   flags[10] ? b2.b.b1=1 : b2.b.b1=0;
   flags[11] ? b2.b.b2=1 : b2.b.b2=0;
   flags[12] ? b2.b.b3=1 : b2.b.b3=0;
   flags[13] ? b2.b.b4=1 : b2.b.b4=0;
   flags[14] ? b2.b.b5=1 : b2.b.b5=0;
   flags[15] ? b2.b.b6=1 : b2.b.b6=0;
   flags[16] ? b2.b.b7=1 : b2.b.b7=0;
   if(_OddOnes(b2.c) != flags[17])
       return -1;

   return (b1.c<<8)+b2.c;
}

/*
 * 思路：
 * 取到一次像素变化后，判断
 */
i32 img_util_ex::_if_line_with_flag( u16 line_index,u16 col_offset/*=0*/,u8 flag/*=0xae*/ )
{
	i8 diff_b,diff_g,diff_r;
	u16 col=col_offset;
	u16 base_col=0;
	pix32 pix0,pix1,pix2,pix3;
	pix0.v = pix1.v = 0;
	bool bflags[9]={false};
	fill_bool_array_with_parity(bflags,flag);
	if(_bpp == 24 || _bpp == 32)
	{
		pix0 = _get_equal_pixs_inline(line_index,col,_w);
		while(col < _w)
		{
			base_col=col;
			pix1 = _get_equal_pixs_inline(line_index,col,_w);
			if(_PixCmp(pix0,pix1,bflags[0],bflags[1],bflags[2])==false)
			{
				pix0.v = pix1.v;
				continue;
            };
			base_col = col;
			pix2 = _get_equal_pixs_inline(line_index,col,_w);
			if(_PixCmp(pix1,pix2,bflags[3],bflags[4],bflags[5])==false)
			{
				pix0.v = pix1.v;
				col = base_col;
				continue;
			}
			pix3 = _get_equal_pixs_inline(line_index,col,_w);
			if(_PixCmp(pix2,pix3,bflags[6],bflags[7],bflags[8])==false)
			{
				pix0.v = pix1.v;
				col = base_col;
				continue;
			}
			return col;
		}
	}
	return -1;
}

//channel_index : 0 all_channel,1 red_channel,2 green_channel,3 blue_channel,4 alpha_channel
bool img_util_ex::_pix32_similar(pix32 p1,pix32 p2,u8 tolarance,color_channel channel_index)
{
	switch(channel_index)
	{
	case 0:
		if(abs(p1.c.r-p2.c.r)>tolarance)
			return false;
		if(abs(p1.c.g-p2.c.g)>tolarance)
			return false;
		if(abs(p1.c.b-p2.c.b)>tolarance)
			return false;
		if(abs(p1.c.a-p2.c.a)>0)
			return false;
		return true;
	case 1:
		if(abs(p1.c.r-p2.c.r)>tolarance)
			return false;
		return true;
	case 2:
		if(abs(p1.c.g-p2.c.g)>tolarance)
			return false;
		return true;
	case 3:
		if(abs(p1.c.b-p2.c.b)>tolarance)
			return false;
		return true;
	case 4:
		if(abs(p1.c.a-p2.c.a)>0)
			return false;
		return true;
	default:
		return false;
	}
}
 
iu::color_blocks img_util_ex::scan_color_blocks( u16 lstw/*=100*/,u16 lsth/*=5*/,u8 tolarance/*=5*/,color_channel channel_index/*=0*/)
{
	bool secs_ok;
	section sec;
	color_block blk;
	color_blocks blks;
	blks.clear();
	if(_bpp!=24 && _bpp!=32)
		return blks;
	if(!_data_ok)
		return blks;
	if(_w < lstw)
		return blks;
	if(_data==NULL)
		return blks;

	for(int i=0;i<_h;i+=lsth)
	{
		//第i行，扫描颜色一致的区间段，满足模式
		sections secs1 = scan_color_sections(i,lstw,tolarance,false,channel_index);
		//第j(=i+最小高度)行，扫描颜色一致的区间段，贪婪模式
		sections secs2 = scan_color_sections(i+lsth-1,lstw,tolarance,true,channel_index);
		//区间段求交集
		sections secs = get_inter_sections(secs1,secs2,lstw);
		_check_sections(secs,tolarance,i,i+lsth-1,channel_index);	//滤除有杂色的块
		for(int j=0;j<secs.size();j++)
		{
			sec = secs[j];
			blk.l = sec.x0;
			blk.t = i;
			blk.w = sec.x1 - sec.x0;
			blk.h = lsth;
			blks.push_back(blk);
		}
	}

	return blks;
}

void img_util_ex::set_block_color(color_block blk,pix32 color,color_channel channel_index)
{
	if(_bpp!=24 && _bpp!=32)
		return;
	if(_bpp == 24)
	{
		for(int i= blk.t;i<(blk.t+blk.h);i++)
		{
			for(int j=blk.l;j<(blk.l+blk.w);j++)
			{
				setpix24(i,j,color,channel_index);
			}
		}
	}
	else if(_bpp == 32)
	{
		for(int i= blk.t;i<(blk.t+blk.h);i++)
		{
			for(int j=blk.l;j<(blk.l+blk.w);j++)
			{
				setpix32(i,j,color,channel_index);
			}
		}
	}
}

iu::pix32 img_util_ex::get_block_everate_color( color_block blk )
{
	u32 red,grn,blu;
	u16 count=0;
	pix32 pix;
	red=grn=blu=0;
	if(_bpp==24)
	{
		for(int c=blk.l;c<(blk.l+blk.w);c+=blk.w/5)
		{
			for(int r=blk.t;r<(blk.t+blk.h);r+=blk.h/2)
			{
				pix = getpix24(r,c);
				red += pix.c.r;
				grn += pix.c.g;
				blu += pix.c.b;
				++count;
			}
		}
	}
	else if(_bpp==32)
	{
		for(int c=blk.l;c<(blk.l+blk.w);c+=blk.w/5)
		{
			for(int r=blk.t;r<(blk.t+blk.h);r+=blk.h/2)
			{
				pix = getpix32(r,c);
				red += pix.c.r;
				grn += pix.c.g;
				blu += pix.c.b;
				++count;
			}
		}
	}
	pix.c.r = red/count;
	pix.c.g = grn/count;
	pix.c.b = blu/count;
	pix.c.a = 0;
	return pix;
}

pix32 img_util_ex::everate_block_color( color_block blk,color_channel channel_index )
{
	pix32 pix = get_block_everate_color(blk);
	if(pix.c.r==255)
		pix.c.r=254;
	if(pix.c.g==255)
		pix.c.g=254;
	if(pix.c.b==255)
		pix.c.b=254;
	if(pix.c.r==0)
		pix.c.r=1;
	if(pix.c.g==0)
		pix.c.g=1;
	if(pix.c.b==0)
		pix.c.b=1;
	set_block_color(blk,pix,channel_index);

	switch(channel_index)
	{
	case 1:
		pix.c.g = pix.c.b = pix.c.a = 0;
		break;
	case 2:
		pix.c.r = pix.c.b = pix.c.a = 0;
		break;
	case 3:
		pix.c.r = pix.c.g = pix.c.a = 0;
		break;
	case 4:
		pix.c.r = pix.c.g = pix.c.b = 0;
	default:
		break;
	}
	return pix;
}

iu::pix8 img_util_ex::everage_block_channel_color(color_block blk,color_channel channel_index)
{
	pix32 pix = get_block_everate_color(blk);
	if(pix.c.r==255)
		pix.c.r=254;
	if(pix.c.g==255)
		pix.c.g=254;
	if(pix.c.b==255)
		pix.c.b=254;
	if(pix.c.r==0)
		pix.c.r=1;
	if(pix.c.g==0)
		pix.c.g=1;
	if(pix.c.b==0)
		pix.c.b=1;
	set_block_color(blk,pix,channel_index);

	switch(channel_index)
	{
	case 1:
		return pix.c.r;
	case 2:
		return pix.c.g;
	case 3:
		return pix.c.b;
	case 4:
		return pix.c.a;
	default:
		return 0;
	}
	return 0;
}

/*
 * 理论：第一块像素为参照，后续每块像素能存3位数据，
 * 数据开始标记占8位，存储的data占16位，共24位
 * 每8位之后又有一个奇偶标志位，24位数据就有3位奇偶标志位
 * 共27位数据，需要9个后续段
 * 数据存储方法：
 * 以前一个像素为参照，b/g/r各存储一位数据
 * 后一个像素发生变化
 */
bool img_util_ex::save_data_in_block( color_block blk,u16 data,u8 flag/*=0xae=10101110*/)
{
	if(blk.w/10 < blk.h)	//block中至少要有10个块
		return false;
	everate_block_color(blk);
	bool bdata[27]={false};
	u8 bdata_index = 0;
	fill_bool_array_with_parity(bdata,flag,TAKE_HIGH_BYTE(data),TAKE_LOW_BYTE(data));
	pix32 pix;
	if(_bpp == 24)
	{
		pix = getpix24(blk.l,blk.t);
	}
	else if(_bpp == 32)
	{
		pix = getpix32(blk.l,blk.t);
	}
	pix32 pix2;
	u16 i=1;
	i8 off_b,off_g,off_r;
	pix2.v = 0;
	if(pix.c.b >= 128) off_b = -1; else off_b = 1;
	if(pix.c.g >= 128) off_g = -1; else off_g = 1;
	if(pix.c.r >= 128) off_r = -1; else off_r = 1;
	while(true)
	{
		//从第1个块开始取（第0个块存的是基础色）
		color_block b = _get_sub_block(blk,i);	//blk的宽度为高度的10倍及以上时，才能保证存入所有bdata
		if(b.w==0)
			break;
		//以pix为参照，以bdata中每3位为一个单位，得到pix2的值
		if(bdata[((i-1)*3)%26])		
		{
			pix2.c.b = pix.c.b + off_b; 
			off_b = -off_b;
		}
		else
		{
			pix2.c.b = pix.c.b;
		}
		if(bdata[((i-1)*3+1)%26])	
		{
			pix2.c.g = pix.c.g + off_g; 
			off_g = -off_g;
		}
		else
		{
			pix2.c.g = pix.c.g;
		}
		if(bdata[((i-1)*3+2)%26])
		{
			pix2.c.r = pix.c.r + off_r; 
			off_r = -off_r;
		}
		else
		{
			pix2.c.r = pix.c.r;
		}
		//将计算得到的pix2的值存入到块中
		set_block_color(b,pix2);
		//pix更新
		pix.v = pix2.v;
		++i;
	}
	return true;
}

/*
 * 以第一个像素为参照，后续像素发生变化
 * b/g/r各存储一位数据
 * 如果变化值为1，则表明该值为false
 * 如果变化值为2，则表明该值为true
 * 如果不符合，则表明没有存储信息
 */
bool img_util_ex::save_data_in_block_2( color_block blk,u16 data,u8 flag/*=0xae=10101110*/)
{
	if(blk.w/10 < blk.h)	//block中至少要有10个块
		return false;
	pix32 p = everate_block_color(blk);
	bool bdata[27]={false};
	pix32 pix[10];

	fill_bool_array_with_parity(bdata,flag,TAKE_HIGH_BYTE(data),TAKE_LOW_BYTE(data));
	for(int i=0;i<10;i++)
	{
		pix[i].v = p.v;
	}
	_save_data_in_pixs(bdata,pix);
	for(int i=0;i<10;i++)
	{
		color_block b = _get_sub_block(blk,i);
		set_block_color(b,pix[i]);
	}
	return true;
}

bool _save_data_in_pixs(bool bdata[27],pix32 pix[10])
{
	for(int i=0;i<=8;i++)
	{
		_save_data_in_pix(bdata+i*3,pix[i+1],pix[i],pix[0]);
	}
	return true;
}

bool _save_data_in_pix(bool bdata[3],pix32 &pix,pix32 prev_pix,pix32 base_pix)
{
	bool big_b,big_g,big_r;
	i8 offset;
	big_r = big_g = big_b = false;
	if(base_pix.c.r >= 128)
		big_r = true;
	if(base_pix.c.g >= 128)
		big_g = true;
	if(base_pix.c.b >= 128)
		big_b = true;

	if(bdata[0]) offset=2;
	else offset = 1;
	if(prev_pix.c.b > base_pix.c.b)
		pix.c.b = prev_pix.c.b - offset;
	else if(prev_pix.c.b < base_pix.c.b)
		pix.c.b = prev_pix.c.b + offset;
	else if(big_b)
		pix.c.b = prev_pix.c.b - offset;
	else
		pix.c.b = prev_pix.c.b + offset;

	if(bdata[1]) offset=2;
	else offset = 1;
	if(prev_pix.c.g > base_pix.c.g)
		pix.c.g = prev_pix.c.g - offset;
	else if(prev_pix.c.g < base_pix.c.g)
		pix.c.g = prev_pix.c.g + offset;
	else if(big_g)
		pix.c.g = prev_pix.c.g - offset;
	else
		pix.c.g = prev_pix.c.g + offset;

	if(bdata[2]) offset=2;
	else offset = 1;
	if(prev_pix.c.r > base_pix.c.r)
		pix.c.r = prev_pix.c.r - offset;
	else if(prev_pix.c.r < base_pix.c.r)
		pix.c.r = prev_pix.c.r + offset;
	else if(big_r)
		pix.c.r = prev_pix.c.r - offset;
	else
		pix.c.r = prev_pix.c.r + offset;
	return true;
}




color_block img_util_ex::_get_sub_block(color_block &blk,u8 index)
{
	color_block b;
	b.l = blk.l+blk.h*index;
	b.t = blk.t;
	b.w = blk.h;
	b.h = blk.h;
	if(b.l+b.w > blk.l+blk.w)
		b.w = b.h = 0;
	return b;
}

iu::data_recoreds img_util_ex::recognize_data()
{
	data_recoreds datas;
    i32 col,value;
    pix32 pix;
    pix.c.b = pix.c.g = pix.c.r = 255;
    for(int i=0;i<_h;i++)
    {
		col = 0;
		do
		{
			col = _if_line_with_flag(i,col);
			if(col<=0)
				break;
			value = _abstract_data_inline(i,col,pix);
			if(value > 0)
			{
				data_recored rec;
				rec.col = col;
				rec.row = i;
				rec.data = value;
				datas.push_back(rec);
				//return value;
			}
		}while(1);
    }

	printf("recs size = %d\n",datas.size());
	for(int i=0;i<datas.size();i++)
	{
		int offset = (_h-1-datas[i].row)*_line_width + datas[i].col*3 + 54;
		printf("%x : %d %d : %x\n",offset,datas[i].row,datas[i].col,datas[i].data);
	}
	return datas;
}

bool img_util_ex::save_color_channel_as_file(const char* file_name,color_channel channel_index/*=all_chanel*/)
{
	if(channel_index==all_chanel)
		return save_as_file(file_name);
	if(_bpp==24 || _bpp==32)
	{
		img_util bmp8;
		u8 pallet[256*4]={0};
		for(int i=0;i<256;i++)
		{
			pallet[4*i] = i;
			pallet[4*i+1] = i;
			pallet[4*i+2] = i;
			pallet[4*i+3] = 0;
		}
		bmp8.set_img_info(8,_w,_h,NULL,pallet);
		pix32 pix;
		switch(channel_index)
		{
		case 1:
			for(int r=0;r<_h;r++)
			{
				for(int c=0;c<_w;c++)
				{
					u8 * p = _locate_pix(r,c);
					if(p)
					{
						pix.v=*(u32*)p;
						bmp8.setpix8(r,c,pix.c.r);
					}
				}
			}
			break;
		case 2:
			for(int r=0;r<_h;r++)
			{
				for(int c=0;c<_w;c++)
				{
					u8 * p = _locate_pix(r,c);
					if(p)
					{
						pix.v=*(u32*)p;
						bmp8.setpix8(r,c,pix.c.g);
					}
				}
			}
			break;
		case 3:
			for(int r=0;r<_h;r++)
			{
				for(int c=0;c<_w;c++)
				{
					u8 * p = _locate_pix(r,c);
					if(p)
					{
						pix.v=*(u32*)p;
						bmp8.setpix8(r,c,pix.c.b);
					}
				}
			}
			break;
		default:
			return false;
		}
		return bmp8.save_as_file(file_name);
	}
	else
		return false;
}

/*
 * 两组区间段取交集
 */
iu::sections get_inter_sections( sections s1,sections s2, unsigned short lst_width/*=1*/)
{
	sections ss;
	section r1,r2,r;
	for(int i=0;i<s1.size();i++)
	{
		r1 = s1[i];
		for(int j=0;j<s2.size();j++)
		{
			r2 = s2[j];
			if(r2.x0>=r1.x0 && r2.x0<=r1.x1)	//r2.x0 在 r1之内
			{
				if(r2.x1 <= r1.x1)	//r2.x1 在 r1 之内
				{
					r = r2;
					if(r.x1-r.x0>=lst_width)
						ss.push_back(r);
				}
				else	//r2.x1 在 r1 的右边
				{
					r.x0 = r2.x0;
					r.x1 = r1.x1;
					if(r.x1-r.x0>=lst_width)
						ss.push_back(r);
					break;			//跳出本循环，让r1指向下个区间
				}
			}
			else if(r2.x0 < r1.x0)	//r2.x0在r1的左边
			{
				if(r2.x1 <= r1.x0)	//r2.x0在r1的左边
				{
					continue;		//让r2指向下个区间
				}
				else if(r2.x1 > r1.x1)	//r2.x1在r1的右边
				{
					r = r1;			//区间r2包含r1
					if(r.x1-r.x0>=lst_width)
						ss.push_back(r);
					break;			//跳出本循环，让r1指向下个区间
				}
				else			//区间r1和r2有交叉
				{
					r.x0 = r1.x0;
					r.x1 = r2.x1;
					if(r.x1-r.x0>=lst_width)
						ss.push_back(r);
				}
			}
			else	//r2.x0在r1的右边
			{
				break;	//跳出本循环，让r1指向下个区间
			}
		}
	}
	return ss;
}

//从高位开始取
void fill_bool_array_with_parity( bool flags[27],u8 data1,u8 data2,u8 data3 )
{
	bool odd=false;			//有偶数个为真的元素
	for(int i=0;i<=7;i++)
	{
		flags[i] = (data1 & 0x80 >> i) > 0;
		if(flags[i])		//每存入一个真的元素，则真元素个数的奇偶性发生变化
			odd = !odd;
	}
	flags[8] = odd;
	odd=false;
	for(int i=0;i<=7;i++)	//存第9~16
	{
		flags[i+9] = (data2 & 0x80 >> i) > 0;
		if(flags[i+9])		//每存入一个真的元素，则真元素个数的奇偶性发生变化
			odd = !odd;
	}
	flags[17] = odd;
	odd=false;
	for(int i=0;i<=7;i++)	//存第18~25
	{
		flags[i+18] = (data3 & 0x80 >> i) > 0;
		if(flags[i+18])		//每存入一个真的元素，则真元素个数的奇偶性发生变化
			odd = !odd;
	}
	flags[26] = odd;
	if(flags[26])			//每存入一个真的元素，则真元素个数的奇偶性发生变化
		odd = !odd;
}

//从高位开始取
void fill_bool_array_with_parity( bool flags[9],u8 data)
{
	bool odd=false;			//有偶数个为真的元素
	for(int i=0;i<=7;i++)
	{
		flags[i] = (data & 0x80 >> i) > 0;
		if(flags[i])		//每存入一个真的元素，则真元素个数的奇偶性发生变化
			odd = !odd;
	}
	flags[8] = odd;
	odd=false;
}

}

