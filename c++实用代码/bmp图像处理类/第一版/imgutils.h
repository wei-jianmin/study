#ifndef _IMGUTILS_H_
#define _IMGUTILS_H_
#include <vector>
namespace iu{
#ifndef NULL
#define NULL 0
#endif 
#define TAKE_LOW_BYTE(w) (w & 0xff)
#define TAKE_HIGH_BYTE(w) ((w & 0xff00) >> 8)
#define TAKE_LOW_WORD(dw) (dw & 0xffff)
#define TAKE_HIGH_WORD(dw) ((dw & 0xffff0000) >> 16)
//����bmpͼ��ÿ���ֽ���
#define CALC_LINE_BITS(bpp,w) ((((w * bpp) + 31) >> 5) << 2)

typedef char i8;
typedef short i16;
typedef long i32;
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned long u32;
typedef bool pix1;
typedef unsigned char pix8;

struct data_recored{ u16 row,col,data;};
typedef struct std::vector<data_recored> data_recoreds;

struct section
{
	u16 x0,x1;
};
typedef std::vector<section> sections;
struct color_block
{
	u16 l,t,w,h;
};
typedef std::vector<color_block> color_blocks;
union pix32
{
	struct
	{
		u8 b,g,r,a;
	} c;
	u32 v;
};

#pragma pack(1)		//ȡ���ֽڶ���
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
#pragma pack()		//�ָ��ֽڶ���

struct img_meta
{
	u16 _bpp;		//bits per pix : 1 8 24 32��
	u16 _w,_h;		//ͼ����������
	u8* _data;		//ͼ������
	u8* _pallet;	//��ɫ��,��ɫ��8λλͼ����
};

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

class img_util : protected img_meta
{
public:
	img_util();
	img_util(const char* file_path);
	img_util(u16 bpp,u16 w,u16 h,u8* data=NULL,u8* pallet=NULL);
	~img_util();

public:
	bool is_data_ok();
	bool load_from_file(const char* file_path);
	bool save_as_file(const char* file_path);
	bool attach_img_data(u16 bpp,u16 w,u16 h,u8* data,u8* pallet=NULL);
	bool detach_img_data();
	bool reset_img_info(u16 bpp,u16 w,u16 h,u8* data=NULL,u8* pallet=NULL);
	bool setpix1(u16 r,u16 c,pix1 b1);
	bool setpix8(u16 r,u16 c,pix8 b8);
	bool setpix24(u16 r,u16 c,pix32 b24);
	bool setpix32(u16 r,u16 c,pix32 b32);
	pix1 getpix1(u16 r,u16 c);
	pix8 getpix8(u16 r,u16 c);
	pix32 getpix24(u16 r,u16 c);
	pix32 getpix32(u16 r,u16 c);
	pix32 get_pallet_color(u8 index);
	bool set_pallet_color(u8 index,pix32 color);

private:
	void _init(u16 bpp,u16 w,u16 h,u8* data/*=NULL*/,u8* pallet/*=NULL*/);
	u8* _locate_pix(u16 r,u16 c);
	bool _IsBig_Endian();
	bool _load_from_file(const char* file_path);
	void _clear_data();
	bool _check_r_c(u16 r,u16 c);

protected:
	char _file_name[256];
	bool _big_endian;
	bool _data_ok;		//�������ݲ��ֿ���������д
	bool _attach_flag;
	u32 _data_len;		//
	u16 _pallet_len;	//��ɫ���ֽ���
	u16 _line_width;	//���ֽ���
};

//ֻ����24/32λͼ��
class img_util_ex : public img_util
{
public:
	img_util_ex();
	img_util_ex(const char* file_path);
	img_util_ex(u16 bpp,u16 w,u16 h,u8* data=NULL,u8* pallet=NULL);
public:
	sections scan_color_sections(u16 line_index,u16 lstw=100,u8 tolarance=5,bool greedymode=true);
	color_blocks scan_color_blocks(u16 lstw=100,u16 lsth=5,u8 tolarance=5);
	void set_block_color(color_block blk,pix32 color);
	pix32 get_block_color(color_block blk);		//��������ƽ����ɫ
	pix32 everate_block_color(color_block blk);	//ʹ������ɫƽ����
	bool save_data_in_block(color_block blk,u16 data,u8 flag=0xae);
	bool save_data_in_block_2( color_block blk,u16 data,u8 flag=0xae);
	u16  recognize_data();
private:
	i32 _if_line_with_flag(u16 line_index,u16 col_offset=0,u8 flag=0xae);
	bool _pix32_similar(pix32 p1,pix32 p2,u8 tolarance);
	void _check_sections(sections& secs,u8 tolarance,u16 begin_line_index,u16 end_line_index);
	bool _OddOnes(u8 x);
	bool _PixCmp(pix32 p1,pix32 p2,bool b[3]);
	bool _PixCmp(pix32 p1,pix32 p2,bool b0,bool b1,bool b2);
	pix32 _get_equal_pixs_inline(u16 line_index,u16 &col,u16 line_width);
	color_block _get_sub_block(color_block &blk,u8 index);
    u8 _check_pending_pixs(pix32 base_pix, bool bflag, bool gflag, bool rflag);
    i32 _abstract_data_inline(u16 line_index, u16 col_index, pix32 base_pix);
};

sections get_inter_sections(sections s1,sections s2, unsigned short lst_width=1);

void fill_bool_array_with_parity(bool flags[27],u8 data1,u8 data2,u8 data3);
void fill_bool_array_with_parity( bool flags[9],u8 data);

bool _save_data_in_pixs(bool bdata[27],pix32 pix[10]);
bool _save_data_in_pix(bool bdata[3],pix32 &pix,pix32 prev_pix,pix32 base_pix);
}
#endif
