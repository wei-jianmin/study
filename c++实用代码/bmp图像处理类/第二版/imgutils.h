#ifndef _IMGUTILS_H_
#define _IMGUTILS_H_
#define _CRT_SECURE_NO_WARNINGS

#include <vector>

namespace iu {

#ifndef NULL
#define NULL 0
#endif 

//重定义数据类型
typedef char i8;
typedef short i16;
typedef long i32;
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned long u32;
typedef bool pix1;
typedef unsigned char pix8;

//定义结构类型
struct section;
struct color_block;
struct data_recored;
typedef std::vector<section> sections;
typedef std::vector<color_block> color_blocks;
typedef std::vector<data_recored> data_recoreds;
struct BMPFILEHEADER;
struct BMPINFOHEADER;
union pix32;

struct img_meta
{
	u16 _bpp;		//bits per pix : 1 8 24 32等
	u16 _w,_h;		//图像宽高像素数
	u8* _data;		//图像数据
	u8* _pallet;	//调色板,单色或8位位图有用
};

class img_util : private img_meta
{
public:
	img_util();
	img_util(const char* file_path);
	img_util(u16 bpp,u16 w,u16 h,u8* data=NULL,u8* pallet=NULL);
	~img_util();
	friend class img_util_ex;
public:
	enum color_channel{all_chanel=0,red_channel,green_channel,blue_channel};
public:
	bool is_data_ok();
	bool load_from_file(const char* file_path);
	bool set_img_info(u16 bpp,u16 w,u16 h,const u8* data_ref=NULL,const u8* pallet_ref=NULL);
	bool attach_img_data(u16 bpp,u16 w,u16 h,u8* data,u8* pallet=NULL);
	bool detach_img_data();
	bool save_as_file(const char* file_path);
	void clear() { _clear_data(); }

	//读取/设置图像信息
	bool setpix1(u16 r,u16 c,pix1 b1);
	bool setpix8(u16 r,u16 c,pix8 b8);
	bool setpix24(u16 r,u16 c,pix32 b24,color_channel channel_index=all_chanel);
	bool setpix32(u16 r,u16 c,pix32 b32,color_channel channel_index=all_chanel);
	pix1 getpix1(u16 r,u16 c);
	pix8 getpix8(u16 r,u16 c);
	pix32 getpix24(u16 r,u16 c);
	pix32 getpix32(u16 r,u16 c);
	pix32 get_pallet_color(u8 index);
	bool set_pallet_color(u8 index,pix32 color);
	u16  get_bmp_width() { if(_data_ok) return _w; else return 0; }
	u16  get_bmp_height() { if(_data_ok) return _h; else return 0; }
	u16  get_bmp_pixbits() { if(_data_ok) return _bpp; else return 0; }

private:
	void _init(u16 bpp,u16 w,u16 h,const u8* data_ref/*=NULL*/,const u8* pallet_ref/*=NULL*/);
	u8* _locate_pix(u16 r,u16 c);
	bool _IsBig_Endian();
	bool _load_from_file(const char* file_path);
	void _clear_data();
	bool _check_r_c(u16 r,u16 c);

protected:
	char _file_name[256];
	bool _big_endian;
	bool _data_ok;		//表明数据部分可以正常读写
	bool _attach_flag;
	u32 _data_len;		//
	u16 _pallet_len;	//调色板字节数
	u16 _line_width;	//行字节数
};

//只处理24/32位图像
class img_util_ex : public img_util
{
public:
	img_util_ex();
	img_util_ex(const char* file_path);
	img_util_ex(u16 bpp,u16 w,u16 h,u8* data=NULL,u8* pallet=NULL);
public:
	sections scan_color_sections(u16 line_index,u16 lstw=100,u8 tolarance=5,bool greedymode=true,color_channel channel_index=all_chanel);
	color_blocks scan_color_blocks(u16 lstw=100,u16 lsth=5,u8 tolarance=5,color_channel channel_index=all_chanel);
	void set_block_color(color_block blk,pix32 color,color_channel channel_index=all_chanel);
	pix32 get_block_everate_color(color_block blk);		//获得区块的平均颜色
	pix32 everate_block_color(color_block blk,color_channel channel_index=all_chanel);			//使区块颜色平均化
	pix8  everage_block_channel_color(color_block blk,color_channel channel_index=all_chanel);
	bool save_data_in_block(color_block blk,u16 data,u8 flag=0xae);
	bool save_data_in_block_2( color_block blk,u16 data,u8 flag=0xae);
	data_recoreds  recognize_data();
	bool save_color_channel_as_file(const char* file_name,color_channel channel_index=all_chanel);
private:
	i32 _if_line_with_flag(u16 line_index,u16 col_offset=0,u8 flag=0xae);
	bool _pix32_similar(pix32 p1,pix32 p2,u8 tolarance,color_channel channel_index=all_chanel);
	void _check_sections(sections& secs,u8 tolarance,u16 begin_line_index,u16 end_line_index,color_channel channel_index=all_chanel);
	bool _OddOnes(u8 x);
	bool _PixCmp(pix32 p1,pix32 p2,bool b[3]);
	bool _PixCmp(pix32 p1,pix32 p2,bool b0,bool b1,bool b2);
	pix32 _get_equal_pixs_inline(u16 line_index,u16 &col,u16 line_width);
	color_block _get_sub_block(color_block &blk,u8 index);
    u8 _check_pending_pixs(pix32 base_pix, bool bflag, bool gflag, bool rflag);
    i32 _abstract_data_inline(u16 line_index, u16 col_index, pix32 base_pix);
};


//工具函数
sections get_inter_sections(sections s1,sections s2, unsigned short lst_width=1);
void fill_bool_array_with_parity(bool flags[27],u8 data1,u8 data2,u8 data3);
void fill_bool_array_with_parity( bool flags[9],u8 data);

struct data_recored
{ 
	u16 row,col,data; 
};

struct section
{
	u16 x0,x1;
};

struct color_block
{
	u16 l,t,w,h;
};

union pix32
{
	struct
	{
		u8 b,g,r,a;
	} c;
	u32 v;
};

#pragma pack(1)		//取消字节对齐
struct BMPFILEHEADER 
{  
	u16 bfType;    
	u32 bfSize; 
	u16 bfReserved1; 
	u16 bfReserved2; 
	u32 bfOffBits;
};

struct BMPINFOHEADER
{
	u32 biSize; 
	i32 biWidth; 
	i32 biHeight; 
	i16 biPlanes; 
	i16 biBitCount; 
	u32 biCompression; 
	u32 biSizeImage; 
	i32 biXPelsPerMeter; 
	i32 biYPelsPerMeter; 
	u32 biClrUsed; 
	u32 biClrImportant;
};
#pragma pack()		//恢复字节对齐

}

#endif
