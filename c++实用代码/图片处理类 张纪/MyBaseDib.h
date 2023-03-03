#if !defined(AFX_MYBASEDIB_H__40EDBE23_597C_4987_B7D2_3BD4F17678BE__INCLUDED_)
#define AFX_MYBASEDIB_H__40EDBE23_597C_4987_B7D2_3BD4F17678BE__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
// MyBaseDib.h : header file

/////////////////////////////////////////////////////////////////////////////
// CMyBaseDib document


class CZJBaseDib 
{

// Attributes
public:
	CZJBaseDib();				 // 默认的构造函数
	int m_nWidth;                //图像的宽，像素为单位
	int m_nHeight;               //图像的高，像素为单位
	unsigned char * m_pImgData;  //图像数据指针	
	LPRGBQUAD m_lpColorTable;    //图像颜色表指针
	int m_nBitCount;             //每像素占的位数
	LPBYTE m_lpDib;              //指向DIB的指针（整个位图起始地址）
	LPBITMAPINFOHEADER m_lpBmpInfoHead;         //图像信息头指针
	HPALETTE m_hPalette;	     //调色板句柄
	int m_nColorTableLength;     //颜色表长度
	int m_iStyle;                //模式 0:修改模式  1:只读模式(析构函数不可尝试释放数据)
	

// Operations
public:
	//构造函数
	CZJBaseDib(CSize size, int nBitCount, LPRGBQUAD lpColorTable, 
		unsigned char *pImgData);
	//拷贝构造函数
	CZJBaseDib(CZJBaseDib &Dib); 
	int GetSize()    // 返回BMP数据区的大小
	{
		if(m_lpDib==NULL)
			return 0;
		return  m_nWidth *m_nHeight;
	}
	BYTE* GetImgData(){return m_pImgData;}
	int GetBitCount(){return m_nBitCount;}
	LPRGBQUAD GetLprgbQuad(){return m_lpColorTable;}
	int GetWidth(){if(m_lpDib==NULL) return 0; return m_nWidth;}
	int GetHeight(){if(m_lpDib==NULL) return 0; return m_nHeight;}
	bool GetMallocMen(LPBYTE pMen);   //将pMen的内存区域作为自己的缓冲区(质检程序专用,使用pMen的数据，但不改变它)
	//DIB读函数
	BOOL ReadBmp(LPCTSTR lpszPathName);
	//DIB写函数
	BOOL WriteBmp(LPCTSTR lpszPathName);
	void ZoomNormal(int nWidth, int	nHeight,int type);  //缩放 
	//DIB显示函数
	BOOL Draw(CDC* pDC, CPoint origin, CSize size); 
	//逻辑调色板生成函数
	void MakePalette();
	//获取DIB的尺寸（宽高）
	virtual CSize GetDimensions();
	void SetDimensions(CSize size);   //修改大小,不够的补白边
	//清理空间
	virtual void Empty();	
	//用新的数据替换当前DIB，更新信息头
	virtual void Copy(CSize size, int nBitCount, LPRGBQUAD lpColorTable,unsigned char *pImgData);
	virtual CZJBaseDib& operator =( CZJBaseDib& Dib);
	//计算颜色表的长度
	int ComputeColorTabalLength(int nBitCount);
	void GetHuiClor();    //提取灰度
	void RotateAngle(double angle) ;    // 双线性旋转
	void RotateCube(int angle);         //立方卷积插值旋转
	void CutEdge(int newWidth,int newHeight);  // 切边

	//立方卷积插值
	unsigned char interpolationCube(unsigned char array[4][4], float xpos, float ypos);

public:
	virtual ~CZJBaseDib();

};


#endif // !defined(AFX_MYBASEDIB_H__40EDBE23_597C_4987_B7D2_3BD4F17678BE__INCLUDED_)
