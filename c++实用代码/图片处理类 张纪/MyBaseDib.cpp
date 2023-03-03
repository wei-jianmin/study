// MyBaseDib.cpp : implementation file
//

#include "stdafx.h"
#include "MyBaseDib.h"
#include <cmath>


/////////////////////////////////////////////////////////////////////////////
// CMyBaseDib
CZJBaseDib::CZJBaseDib()
{
 	m_iStyle=0;
	m_lpDib=NULL;
	m_lpColorTable=NULL;
	m_pImgData=NULL;  
	m_lpBmpInfoHead=NULL;
	m_hPalette = NULL;
	m_nWidth=0;
	m_nHeight=0;
}
//拷贝构造函数
CZJBaseDib::CZJBaseDib(CZJBaseDib &Dib)
{
	Copy(Dib.GetDimensions(),Dib.m_nBitCount,Dib.m_lpColorTable,Dib.m_pImgData);
}

CZJBaseDib::~CZJBaseDib()
{
	//删除资源
 	Empty();
}

void CZJBaseDib::CutEdge(int NewWidth,int NewHeight)  // 切边
{
	if(m_pImgData==NULL) return;
	if(NewWidth >= m_nWidth) return;
    int nCutW = (m_nWidth - NewWidth)/2;
	int nCutH = (m_nHeight- NewHeight)/2;
	//构造缓冲
	int width=NewWidth ;
	int height=NewHeight ;                         
	int lineByteout=(width*m_nBitCount/8+3)/4*4;
	int lineByteoutSrc=(m_nWidth*m_nBitCount/8+3)/4*4;
	unsigned char* pImgDataOut=new  unsigned char[lineByteout *height]; 
	memset(pImgDataOut,255,lineByteout *height);
	
    for(int i =0; i < height; ++i)
	{
		byte* dest = pImgDataOut + i*lineByteout;
		byte* src  = m_pImgData  + (nCutH+i)*lineByteoutSrc + nCutW *m_nBitCount/8;
		memcpy(dest,src,lineByteout);
	}
    this->Empty();
	this->Copy(CSize(width,height),m_nBitCount,m_lpColorTable,pImgDataOut);   //构造缩放后的新图像

	delete [] pImgDataOut;
}
void CZJBaseDib::ZoomNormal(int nWidth, int	nHeight,int iType)  
{
	if(m_pImgData==NULL) return;
	double fx=nWidth*1.0/m_nWidth;
	double fy=nHeight*1.0/m_nHeight;
	//构造原图像副本
	int widthin=m_nWidth;
	int heightin=m_nHeight;
	int lineByteout=(m_nWidth*m_nBitCount/8+3)/4*4;
	unsigned char* pImgDataOut=new  unsigned char[lineByteout *m_nHeight]; //申请缓冲区，存放图像数据副本(大小不受影响)
	memcpy(pImgDataOut,m_pImgData, lineByteout *m_nHeight);
  
	//修改原图像
	m_nWidth =nWidth;    //计算新的高度和宽度
	m_nHeight =nHeight; 
	int lineByte=(m_nWidth*m_nBitCount/8+3)/4*4; //计算修改后的图像每行字节数
	unsigned char* pImgData=new  unsigned char[lineByte *m_nHeight]; //申请缓冲区
	LPRGBQUAD lpColorTable=NULL;
	if(m_nColorTableLength!=0){
		lpColorTable=new RGBQUAD[ m_nColorTableLength]; //如果有颜色表，则保存副本
		memcpy(lpColorTable,m_lpColorTable,sizeof(RGBQUAD) * m_nColorTableLength);
	}
	this->Copy(CSize(m_nWidth,m_nHeight),m_nBitCount,lpColorTable,pImgData);   //构造缩放后的新图像

    
    
	int i,j; //循环变量，图像坐标
	int k;   //循环变量,像素的每个通道
	int pix=m_nBitCount /8;   //如果是彩色的，则要复制3个字节点了
	//图像拖放
	if(iType==0)  //最近邻插值
	for(i=0;i<m_nHeight;i++)
	{
		for(j=0;j<m_nWidth;j++)
		{
			int ixout= int(j/fx+0.5);
			int iyout= int(i/fy +0.5);
			if((0<=ixout && ixout<widthin) &&(0 <=iyout &&iyout<heightin) )  //映射回去应该小于原始高度和宽度才合理
			{
				for(k=0;k<pix;k++)
				{
					if(int(i/fy)>0 && int(i/fy)<heightin &&int(j/fx)>0 &&int(j/fx)<widthin)
				
						*(m_pImgData+i*lineByte+j*pix+k)    //新的像素点
					=*(pImgDataOut+int(i/fy+0.5)*lineByteout+int(j/fx +0.5)*pix+k);//原图的像素点\for(k=0;k<pixelByte;k++)
					
				}
			
			}
			else                     //不合理的直接填充白色
			{
				for(k=0;k<pix;k++)
					*(m_pImgData+i*lineByte+j*pix+k) =255   ;//新的像素点
			
			}			
		}
	}
	else          //双线差值
	{
		// AfxMessageBox("");
		int clr1,clr2,clr3,clr4;   //表示包围像素点的四个顶点像素灰度值
		int x1,x2,y1,y2;           //对角线像素坐标
		double fxtmp=0;
		double fytmp=0;
		double u=0;
		double v=0;
		int clrx1=0;
		int clrx2=0;
		int clrxy=0;
		for(i=0;i<m_nHeight;i++)
		{
			for(j=0;j<m_nWidth;j++)
			{
				
				fxtmp=j/fx;    //计算对应回去的坐标(浮点型，有小数)
				fytmp=i/fy;
				//对应后的坐标一定围在四个坐标之间，获得x1....y2坐标(但是构建的坐标有可能处于原图像对角线上，造成x2,y2不存在，访问内存越界)
				
				x1=int(fxtmp); y1=int(fytmp);x2=int(fxtmp+1); 	y2=int(fytmp+1);
				
                u=fxtmp- int(fxtmp);  //横左边方向的小数
				v=fytmp -int(fytmp);  //纵坐标方向的小数
				for(k=0;k<pix;k++)
				{
					// 如果坐标在图像的右下角
					if ( (x1 >= widthin - 1) && (y1 >= heightin - 1) )
					{
						clr1 = *(pImgDataOut+y1*lineByteout+x1*pix+k);;	// (x1, y1) 
						*(m_pImgData+i*lineByte+j*pix+k) = clr1; 
					}
					// 如果图像在最后一列外侧
					else if ( x1 >= widthin - 1 )
					{
						clr1 = *(pImgDataOut+y1*lineByteout+x1*pix+k);	// (x1, y1)
						clr3 = *(pImgDataOut+y2*lineByteout+x1*pix+k);	// (x1, y2)
						*(m_pImgData+i*lineByte+j*pix+k) = int(clr1 * (1 - v) + clr3 * v); 
					}			
					// 如果图像在最后一行外侧
					else if ( y1 >= heightin - 1 )
					{
						clr1 = *(pImgDataOut+y1*lineByteout+x1*pix+k);	// (x1, y1)
						clr2 = *(pImgDataOut+y1*lineByteout+x2*pix+k);	// (x2, y1)
						*(m_pImgData+i*lineByte+j*pix+k) =int(clr1 * (1 - u) + clr2 * u) ;
					}
					else
					{
						clr1 = *(pImgDataOut+y1*lineByteout+x1*pix+k);	// (x1, y1)
						clr2 = *(pImgDataOut+y1*lineByteout+x2*pix+k);	// (x2, y1)
						clr3 = *(pImgDataOut+y2*lineByteout+x1*pix+k);	// (x1, y2)
						clr4 = *(pImgDataOut+y2*lineByteout+x2*pix+k);	// (x2, y2)
						
						double f1, f2;
						
						f1 = clr1 * (1 - u) + clr2 * u;
						f2 = clr3 * (1 - u) + clr4 * u;
						*(m_pImgData+i*lineByte+j*pix+k) = int(f1 * (1 - v) + f2 * v );
					}
				}
				
			}
		}
		
	}

	delete []lpColorTable;
	delete []pImgData;
}
//外部传入一个位图数据构造副本

CZJBaseDib::CZJBaseDib(CSize size, int nBitCount, LPRGBQUAD lpColorTable,
						   unsigned char *pImgData)
{
	//如果没有位图数据传入认为是空的DIB，此时不分配DIB内存
	m_iStyle=0;
	m_lpDib=NULL;
	m_lpColorTable=NULL;
	m_pImgData=NULL; 
	m_lpBmpInfoHead=NULL; 
	m_hPalette = NULL;
	
	Copy(size,nBitCount,lpColorTable,pImgData);//如果有位图数据传入	
}

CZJBaseDib& CZJBaseDib::operator=( CZJBaseDib& Dib)
{
	this->m_iStyle=Dib.m_iStyle;
	this->Copy(Dib.GetDimensions(),Dib.m_nBitCount,Dib.m_lpColorTable,Dib.m_pImgData);
	return *this;
}

//由参数(每个像素占用位数)计算颜色表长度(颜色表结构数组个数)
int CZJBaseDib::ComputeColorTabalLength(int nBitCount)
{
	int colorTableLength;
	switch(nBitCount) {
	case 1:
		colorTableLength = 2;
		break;
	case 4:
		colorTableLength = 16;
		break;
	case 8:
		colorTableLength = 256;
		break;
	case 16:
	case 24:
	case 32:
		colorTableLength = 0;
		break;
	default:
		ASSERT(FALSE);
	}
	
	ASSERT((colorTableLength >= 0) && (colorTableLength <= 256)); 
	return colorTableLength;
}
//生成调色板(仅当灰度图像才有用)
void CZJBaseDib::MakePalette()
{
	//如果颜色表长度为0，则不生成逻辑调色板
	if(m_nColorTableLength == 0) 
		return;
	//删除旧的调色板对象
	if(m_hPalette != NULL) ::DeleteObject(m_hPalette);
	//申请缓冲区，生成逻辑调色板
	LPLOGPALETTE pLogPal = (LPLOGPALETTE) new char[2 * sizeof(WORD) +
		m_nColorTableLength * sizeof(PALETTEENTRY)];
	pLogPal->palVersion = 0x300;  //这个数值似乎是固定的
	pLogPal->palNumEntries = m_nColorTableLength;
	LPRGBQUAD m_lpDibQuad = (LPRGBQUAD) m_lpColorTable;
	for(int i = 0; i < m_nColorTableLength; i++) {
		pLogPal->palPalEntry[i].peRed = m_lpDibQuad->rgbRed;
		pLogPal->palPalEntry[i].peGreen = m_lpDibQuad->rgbGreen;
		pLogPal->palPalEntry[i].peBlue = m_lpDibQuad->rgbBlue;
		pLogPal->palPalEntry[i].peFlags = 0;
		m_lpDibQuad++;
	}	
	//创建逻辑调色板
	m_hPalette = ::CreatePalette(pLogPal);	
	//释放缓冲区
	delete pLogPal;	
}	


// 图像的尺寸，用CSize类型表达
CSize CZJBaseDib::GetDimensions()
{	
	if(m_lpDib == NULL) return CSize(0, 0);
	return CSize(m_nWidth, m_nHeight);
}
//删除资源
void CZJBaseDib::Empty()
{
	//释放m_lpDib所指向的缓冲区
	if(m_lpDib != NULL)
	{
 		if(m_iStyle==0)  //0创建自身缓冲区  1只读模式,引用其他缓冲区
		 delete [] m_lpDib;
	}
	//释放逻辑调色板缓冲区
	if(m_hPalette != NULL)
	{
		::DeleteObject(m_hPalette);
		m_hPalette = NULL;
	}
	m_lpDib=NULL;
	m_lpColorTable=NULL;
	m_pImgData=NULL; 
	m_lpBmpInfoHead=NULL; 
	m_nWidth=0;
	m_nHeight=0;
}
//将men的内存区域作为自己的缓冲区，pMen是已知的BMP缓冲区(质检程序专用)
bool CZJBaseDib::GetMallocMen(LPBYTE pMen)
{
	//初始化
	m_iStyle=1;  //只读模式
	Empty();     //只读模式不会造成释放外部的资源
    if(pMen)  
	{
		if(pMen[0])  //有数据
		m_lpDib=pMen;
		else
		{
			return FALSE;
		}
	}

	//1为成员变量赋值
	m_lpBmpInfoHead=(BITMAPINFOHEADER*)(m_lpDib + sizeof(BITMAPFILEHEADER));
 	m_nHeight = m_lpBmpInfoHead->biHeight;  //获取高宽(使用文件头)
 	m_nWidth = m_lpBmpInfoHead->biWidth;
	m_nBitCount=m_lpBmpInfoHead->biBitCount; 


	//2计算颜色表长度
	m_nColorTableLength=
		ComputeColorTabalLength(m_nBitCount);
	
	//3生成逻辑调色板
	m_hPalette = NULL;
	if(m_nColorTableLength!=0){
		m_lpColorTable=(LPRGBQUAD)(m_lpDib+sizeof(BITMAPINFOHEADER)+sizeof(BITMAPFILEHEADER));
		MakePalette();
	}	
	//4m_pImgData指向DIB的位图数据起始位置
	m_pImgData = (LPBYTE)m_lpDib+sizeof(BITMAPINFOHEADER) +sizeof(BITMAPFILEHEADER)
			+sizeof(RGBQUAD) * m_nColorTableLength;
	
	return TRUE;

} 
//替换位图数据,并更新信息头,非常重要的一个操作
void CZJBaseDib::Copy(CSize size, int nBitCount,  
							  LPRGBQUAD lpColorTable,unsigned char *pImgData)
{ 
	
	Empty();
	//0成员变量赋值
	m_nWidth=size.cx;
	m_nHeight=size.cy;
	m_nBitCount=nBitCount;
	m_nColorTableLength=ComputeColorTabalLength(nBitCount);//计算颜色表的长度
	int lineByte=(m_nWidth*nBitCount/8+3)/4*4;//每行像素所占字节数，扩展成4的倍数
	int imgBufSize=m_nHeight*lineByte;//位图数据的大小

	LPRGBQUAD	lpColorTableOut=0;
	if(m_nColorTableLength!=0)    //避免自身复制，构造颜色表副本
	{
		lpColorTableOut=new RGBQUAD[m_nColorTableLength];
		// memcpy(lpColorTableOut,lpColorTable,m_nColorTableLength*sizeof(RGBQUAD));
		for(int i=0; i<m_nColorTableLength;i++){
			lpColorTableOut[i].rgbBlue=i;
			lpColorTableOut[i].rgbGreen=i;
			lpColorTableOut[i].rgbRed=i;
			lpColorTableOut[i].rgbReserved=0;
		}
	}

	//1为m_lpDib重新分配空间，以存放新的DIB
	m_lpDib=new BYTE [sizeof(BITMAPINFOHEADER) + sizeof(RGBQUAD) * m_nColorTableLength+imgBufSize];

	//2填写文件头结构
	m_lpBmpInfoHead = (LPBITMAPINFOHEADER) m_lpDib;

	//3填写位图信息头BITMAPINFOHEADER结构
	m_lpBmpInfoHead->biSize = sizeof(BITMAPINFOHEADER);
	m_lpBmpInfoHead->biWidth = m_nWidth;
	m_lpBmpInfoHead->biHeight = m_nHeight;
	m_lpBmpInfoHead->biPlanes = 1;
	m_lpBmpInfoHead->biBitCount = m_nBitCount;
	m_lpBmpInfoHead->biCompression = BI_RGB;
	m_lpBmpInfoHead->biSizeImage = 0;
	m_lpBmpInfoHead->biXPelsPerMeter = 0;
	m_lpBmpInfoHead->biYPelsPerMeter = 0;
	m_lpBmpInfoHead->biClrUsed = m_nColorTableLength;
	m_lpBmpInfoHead->biClrImportant = m_nColorTableLength;
	//调色板置空
	m_hPalette = NULL;

	//4如果有颜色表，则将颜色表拷贝至新生成的DIB，并生成调色板
	if(m_nColorTableLength!=0){
		m_lpColorTable=(LPRGBQUAD)(m_lpDib+sizeof(BITMAPINFOHEADER));
		memcpy(m_lpColorTable,lpColorTableOut,sizeof(RGBQUAD) * m_nColorTableLength);
		MakePalette();
	}

	//5m_pImgData指向DIB的位图数据起始位置
	m_pImgData = (LPBYTE)m_lpDib+sizeof(BITMAPINFOHEADER)+sizeof(RGBQUAD) * m_nColorTableLength;

	//6将新位图数据拷贝至新的DIB中
	memcpy(m_pImgData,pImgData,imgBufSize);

	if(m_nColorTableLength!=0) 
	delete lpColorTableOut;
}

//写位图数据
BOOL CZJBaseDib::WriteBmp(LPCTSTR lpszPathName)
{
	//写模式打开文件
	CFile file;
	if (!file.Open(lpszPathName, CFile::modeCreate | CFile::modeReadWrite 
		| CFile::shareExclusive))
		return FALSE;
	
	//填写文件头结构
	BITMAPFILEHEADER bmfh;
	bmfh.bfType = 0x4d42;  // 'BM' 固定
	bmfh.bfSize = 0;
	bmfh.bfReserved1 = bmfh.bfReserved2 = 0;
	bmfh.bfOffBits = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) +
		sizeof(RGBQUAD) * m_nColorTableLength;	
	try {
		//文件头结构写进文件
		file.Write((LPVOID) &bmfh, sizeof(BITMAPFILEHEADER));
		
		//文件信息头结构写进文件
		file.Write(m_lpBmpInfoHead,  sizeof(BITMAPINFOHEADER));
		
		//如果有颜色表的话，颜色表写进文件
		if(m_nColorTableLength!=0)
			file.Write(m_lpColorTable, sizeof(RGBQUAD) * m_nColorTableLength);
		
		//位图数据写进文件
		int imgBufSize=(m_nWidth*m_nBitCount/8+3)/4*4*m_nHeight;
		file.Write(m_pImgData, imgBufSize);
	}
	catch(CException* pe) {
		pe->Delete();
		file.Close();
		AfxMessageBox(L"write error");
		return FALSE;
	}
	
	//函数返回
	file.Close();
	return TRUE;
}


BOOL CZJBaseDib::ReadBmp(LPCTSTR lpszPathName)
{
	 //MessageBox(NULL,lpszPathName,"",MB_OK);
	//读模式打开图像文件
	CFile file;
	if (!file.Open(lpszPathName, CFile::modeRead | CFile::shareDenyWrite))
		return FALSE;
	
	BITMAPFILEHEADER bmfh;
	try {
		//清理空间
		Empty();
		
		//读取BITMAPFILEHEADER结构到变量bmfh中
		int nCount=file.Read((LPVOID) &bmfh, sizeof(BITMAPFILEHEADER));
		
		// 判断是否为BMP格式
		char NAME[24];
		memset(NAME, 0, 24);
		memcpy(NAME,(char*)&bmfh,2);
		CString sName(NAME);
		if(sName != "BM")
			return FALSE;

		//为m_lpDib分配空间
		m_lpDib=new BYTE[file.GetLength() -sizeof(BITMAPFILEHEADER)];
		
		//读取数据时，可忽略文件头
		file.Read(m_lpDib, file.GetLength() -sizeof(BITMAPFILEHEADER));	
		m_lpBmpInfoHead = (LPBITMAPINFOHEADER)m_lpDib;
		
		//为成员变量赋值
		m_nWidth=m_lpBmpInfoHead->biWidth;
		m_nHeight=m_lpBmpInfoHead->biHeight;
		m_nBitCount=m_lpBmpInfoHead->biBitCount; 
		
		//计算颜色表长度
		m_nColorTableLength=ComputeColorTabalLength(m_lpBmpInfoHead->biBitCount);
			
		//生成逻辑调色板
		m_hPalette = NULL;
		if(m_nColorTableLength!=0){
			m_lpColorTable=(LPRGBQUAD)(m_lpDib+sizeof(BITMAPINFOHEADER));
			MakePalette();
		}	
		//m_pImgData指向DIB的位图数据起始位置
		m_pImgData = (LPBYTE)m_lpDib+sizeof(BITMAPINFOHEADER) 
			+sizeof(RGBQUAD) * m_nColorTableLength;
			
	}
	catch(CException* pe) {
		//AfxMessageBox("Read error");
		pe->Delete();
		return FALSE;
	}
	file.Close();
	//函数返回
	return TRUE;
}


BOOL CZJBaseDib::Draw(CDC* pDC, CPoint origin, CSize size)
{
	//旧的调色板句柄
	HPALETTE hOldPal=NULL;
	
	//如果DIB为空，则返回0
	if(m_lpDib == NULL) return FALSE;
	
	//如果DIB有调色板，则选进设备环境中
	if(m_hPalette != NULL) {
		hOldPal=::SelectPalette(pDC->GetSafeHdc(), m_hPalette, TRUE);
	}
	
	//设置位图伸缩模式
	pDC->SetStretchBltMode(COLORONCOLOR);
	
	//将DIB在pDC所指向的设备上进行显示
	::StretchDIBits(pDC->GetSafeHdc(), origin.x, origin.y, size.cx, size.cy,
		0, 0, m_lpBmpInfoHead->biWidth, m_lpBmpInfoHead->biHeight,m_pImgData,
		(LPBITMAPINFO) m_lpBmpInfoHead, DIB_RGB_COLORS, SRCCOPY);
	
	//恢复旧的调色板
	if(hOldPal!=NULL)
		::SelectPalette(pDC->GetSafeHdc(), hOldPal, TRUE);
	
	//函数返回
	return TRUE;
}

void CZJBaseDib::GetHuiClor()    //提取灰度
{
    //1创建空间
	int nBit=m_nBitCount/3;   //彩色
	int lineByte=(m_nWidth*m_nBitCount/8+3)/4*4;  
	int line=(m_nWidth*nBit/8+3)/4*4;  
	BYTE *pBuf = new BYTE[line*m_nHeight];
	for(int i=0; i<m_nHeight; ++i)
		for(int j=0; j<m_nWidth; ++j)
		{
			BYTE * p= m_pImgData+ i*lineByte+j*3;
			BYTE *p2=pBuf+i*line+j;
			double sum=0;
			for(int k=0; k<3; ++k)
			{
				if(k==0) sum+= 0.11 *(*p);   //灰度计算公式
				if(k==1) sum+= 0.59*(*p);
				if(k==2) sum+= 0.30*(*p);
				p++;
			}
			*p2=int(sum);   //赋值
		}
		//计算颜色表长度
		m_nColorTableLength=ComputeColorTabalLength(nBit);
		
		//彩色图像没有颜色表，因此需要生成
		LPRGBQUAD	lpColorTableOut=0;
		if(m_nColorTableLength!=0){
		lpColorTableOut=new RGBQUAD[m_nColorTableLength];
			for(int i=0; i<m_nColorTableLength;i++){
				lpColorTableOut[i].rgbBlue=i;
				lpColorTableOut[i].rgbGreen=i;
				lpColorTableOut[i].rgbRed=i;
				lpColorTableOut[i].rgbReserved=0;
			}
	}	
	Copy(GetDimensions(),nBit,lpColorTableOut,pBuf);
	delete []pBuf;
}
unsigned char CZJBaseDib::interpolationCube(unsigned char array[4][4], float xpos, float ypos)
{

	//申请数组，计算插值所需要的系数
	float col[4], row[4];

	//准备插值的x方向数据源
	col[0]=xpos+1;
	col[1]=xpos;
	col[2]=1-xpos;
	col[3]=2-xpos;

	//准备插值的y方向数据源
	row[0]=ypos+1;
	row[1]=ypos;
	row[2]=1-ypos;
	row[3]=2-ypos;

	//循环变量
	int i;

	//临时变量
	float t;

	//对水平方向系数数组进行计算
	for(i=0;i<4;i++){
		t=fabs(col[i]);
		if (t>=0&&t<1)
			col[i]=pow(t,3)-2*pow(t,2)+1;
		else if (t>=1&&t<2)
			col[i]=-pow(t,3)+5*pow(t,2)-8*t+4;
		else
			col[i]=0;
	}

	//对垂直方向系数数组进行计算
	for(i=0;i<4;i++){
		t=fabs(row[i]);
		if (t>=0&&t<1)
			row[i]=pow(t,3)-2*pow(t,2)+1;
		else if (t>=1&&t<2)
			row[i]=-pow(t,3)+5*pow(t,2)-8*t+4;
		else
			row[i]=0;
	}

	//将计算好的系数与对应图像数据数组作卷积
	float tempArray[4], temp;
	//先x方向卷积
	for(i=0;i<4;i++)
		tempArray[i]=row[0]*array[0][i]+row[1]*array[1][i]+row[2]*array[2][i]+row[3]*array[3][i];

	//再y方向卷积
	temp=0;
	for (i=0;i<4;i++)
		temp+=tempArray[i]*col[i];

	//将插值结果在图像灰度级范围内输出
	if (temp>255)
		temp=255;
	if (temp<0)
		temp=0;

	//函数返回值，插值结果
	return (unsigned char)temp;

}
void CZJBaseDib::RotateAngle(double angle) 
{
	/*说明：旋转公式必须保证原点在图像中心才能用，因此，需要将源图像原点平移到图像中心点,
	建立新坐标系;
	计算完毕后，可能出现坐标是负数的情况，需要计算新的中心点，采用逆变换再将坐标平移回图像
	的原坐标系，这样自然消除负数了，也只有这样做才是对的；
	采用前向映射方法查找源图像对应点的像素值来计算像素值，因此需要整个过程的“逆变换公式”；
	选择一种插值方法，完成最后的工作*/

	if(angle <0) angle = angle *(-1);
	if(angle >360) angle = int(angle) %360;

	if(m_pImgData==NULL)  return;
	// 原始图像四个角的坐标
	int srcX1, srcX2, srcX3, srcX4;
	int srcY1, srcY2, srcY3, srcY4;
	const double Pi=3.1415926;
	srcX1 = 0;
	srcY1 = 0;
	srcX2 = m_nWidth - 1;
	srcY2 = 0;
	srcX3 = 0;
	srcY3 = m_nHeight - 1;
	srcX4 = m_nWidth - 1;
	srcY4 = m_nHeight - 1;
	
	// 计算旋转角度的正弦和余弦值
    double fSin = sin(angle*2*Pi/360);
    double fCos = cos(angle*2*Pi/360);
	
	// 图像经过旋转后四个角的坐标
	double tranX1, tranX2, tranX3, tranX4;
	double tranY1, tranY2, tranY3, tranY4;
	
	tranX1 = fCos * srcX1 + fSin * srcY1;
	tranY1 = -fSin * srcX1 + fCos * srcY1;
	tranX2 = fCos * srcX2 + fSin * srcY2;
	tranY2 = -fSin * srcX2 + fCos * srcY2;
	tranX3 = fCos * srcX3 + fSin * srcY3;
	tranY3 = -fSin * srcX3 + fCos * srcY3;
	tranX4 = fCos * srcX4 + fSin * srcY4;
	tranY4 = -fSin * srcX4 + fCos * srcY3;
	
	// 计算旋转后图像的大小
	int outWidth,outHeight;
	outWidth = (UINT)( max( fabs(tranX4-tranX1), fabs(tranX3-tranX2) ) + 1.5 );
	outHeight = (UINT)( max( fabs(tranY4-tranY1), fabs(tranY3-tranY2) ) + 1.5 );

	int lineByteout=(outWidth*m_nBitCount/8+3)/4*4;  //分别计算每行字节数
	int lineByte=(m_nWidth*m_nBitCount/8+3)/4*4;

	BYTE *pBuf = new BYTE[lineByteout * outHeight ];
	memset(pBuf, 255, lineByteout * outHeight);  //先全部填上白色，然后逆变换插值
	
	// 计算两个常量
	double num1 = -0.5*outWidth*fCos - 0.5*outHeight*fSin + 0.5*m_nWidth;
	double num2 = 0.5*outWidth*fSin - 0.5*outHeight*fCos + 0.5*m_nHeight;
	
	BYTE*	p = NULL;	// 复制像素的起始位置
	//int		x = 0;				// 变换后的像素横坐标
	//int		y = 0;				// 变换后的像素纵坐标
	double fx=0;
	double fy=0;
	BYTE a,b;
	a=b=0;
	BYTE *p1,*p2,*p3,*p4;
	p1=p2=p3=p4=0;
	
	int nBix= m_nBitCount/8;
	for (int j = 0; j < outHeight; j++)
	{
		for (int i = 0; i < outWidth; i++) 
		{
			double x= (i * fCos + j * fSin + num1 );   //逆变换
			double y= (-i * fSin + j * fCos + num2);
			// 距离当前点最近的四个点坐标
			int	x1, x2, y1, y2;
			x1 = (int)x;
			x2 = x1 + 1;
			y1 = (int)y;
			y2 = y1 + 1;
			double u, v;

			u = x - x1;  //计算比例系数
			v = y - y1;
			if (x >= 0 && x <= m_nWidth && y >= 0 && y <= m_nHeight)  //位于源图像内修改
			{
				for(int k=0; k< nBix; ++k)
				{
					p = pBuf + j * lineByteout  + i* nBix +k;  // 像素地址

					// 计算像素值 使用双线性插值
					if(x2== m_nWidth && (y2)<m_nHeight)  //最右边 纵向插值
					{
						p1=m_pImgData + y1 * lineByte  + x1* nBix +k;	
						p3=m_pImgData + y2 * lineByte  + x1* nBix +k;
						*p = (BYTE)((*p1) *(1-v)+ (*p3) *  v);
					}
					else if((y2)==m_nHeight && (x2)<m_nWidth)  //最上边  横向插值
					{
						p1=m_pImgData + y1 * lineByte  + x1* nBix +k;
						p2=m_pImgData + y1 * lineByte  + (x2)* nBix +k;
						*p = (BYTE)((*p1) *(1-u) + (*p2) *u );
					}
					else if((y2)==m_nHeight && (x2)== m_nWidth)  //右上角 无法插值
					{
						p1=m_pImgData + y1 * lineByte  + x1* nBix +k;
						*p = *p1;
					}
					else    //正常区间 
					{
						/*双线性插值*/
						p1=m_pImgData + y1 * lineByte  + x1* nBix +k;
						p2=m_pImgData + y1 * lineByte  + (x2)* nBix +k;
						p3=m_pImgData + (y2) * lineByte  + x1* nBix +k;
						p4=m_pImgData + (y2) * lineByte  + (x2)* nBix +k;
						
						BYTE a,b;
						a=(*p1) *(1-u) + (*p2) *u ;
						b=(*p3) * (1-u)+ (*p4) *u ;
						*p =(BYTE)(a *(1-v) + b*v);



						// 最近邻差值
						/*p1=m_pImgData +int(yy+0.5) * lineByte  +int(xx+0.5)* nBix +k;
						*p = *p1;*/
					}
					
				}
				
				
			}
			
		}
	}

	Copy(CSize(outWidth,outHeight),m_nBitCount,m_lpColorTable,pBuf);

	delete[]pBuf;
}

void CZJBaseDib::RotateCube(int angle)
{

	//每像素所占字节数，输入图像与输出图像相同
	int pixelByte=m_nBitCount/8;

	// 输入图像每行像素所占字节数
	int lineByte=(m_nWidth*pixelByte+3)/4*4;

	// 旋转角度（弧度）, 将旋转角度从度转换到弧度
	float	fRotateAngle= 2*3.1415926*angle/360;

	// 输入图像四个角的坐标，以图像中心为坐标系原点
	float	fSrcX1,fSrcY1,fSrcX2,fSrcY2,fSrcX3,fSrcY3,fSrcX4,fSrcY4;

	// 旋转后四个角的坐标，以图像中心为坐标系原点
	float	fDstX1,fDstY1,fDstX2,fDstY2,fDstX3,fDstY3,fDstX4,fDstY4;

	// 计算旋转角度的正弦
	float fSina = (float) sin((double)fRotateAngle);

	// 计算旋转角度的余弦
	float fCosa = (float) cos((double)fRotateAngle);

	// 计算原图的四个角的坐标，以图像中心为坐标系原点
	fSrcX1 = (float) (- (m_nWidth  - 1) / 2);
	fSrcY1 = (float) (  (m_nHeight - 1) / 2);
	fSrcX2 = (float) (  (m_nWidth  - 1) / 2);
	fSrcY2 = (float) (  (m_nHeight - 1) / 2);
	fSrcX3 = (float) (- (m_nWidth  - 1) / 2);
	fSrcY3 = (float) (- (m_nHeight - 1) / 2);
	fSrcX4 = (float) (  (m_nWidth  - 1) / 2);
	fSrcY4 = (float) (- (m_nHeight - 1) / 2);

	// 计算新图四个角的坐标，以图像中心为坐标系原点
	fDstX1 =  fCosa * fSrcX1 + fSina * fSrcY1;
	fDstY1 = -fSina * fSrcX1 + fCosa * fSrcY1;
	fDstX2 =  fCosa * fSrcX2 + fSina * fSrcY2;
	fDstY2 = -fSina * fSrcX2 + fCosa * fSrcY2;
	fDstX3 =  fCosa * fSrcX3 + fSina * fSrcY3;
	fDstY3 = -fSina * fSrcX3 + fCosa * fSrcY3;
	fDstX4 =  fCosa * fSrcX4 + fSina * fSrcY4;
	fDstY4 = -fSina * fSrcX4 + fCosa * fSrcY4;

	// 旋转后输出图像宽度
	int imgWidthOut  = (LONG) ( max( fabs(fDstX4 - fDstX1), fabs(fDstX3 - fDstX2) ) + 0.5);

	// 旋转后输出图像高度
	int imgHeightOut = (LONG) ( max( fabs(fDstY4 - fDstY1), fabs(fDstY3 - fDstY2) ) + 0.5);

	// 旋转后输出图像每行的字节数
	int lineByteOut=(imgWidthOut*pixelByte+3)/4*4;

	//分配缓冲区，存放旋转结果
	unsigned char * pImgOut = new unsigned char[lineByteOut* imgHeightOut];

	// 两个常数，这样不用以后每次都计算了
	float f1 = (float) (-0.5 * (imgWidthOut - 1) * fCosa 
		+ 0.5 * (imgHeightOut - 1) * fSina + 0.5 * (m_nWidth  - 1));
	float f2 = (float) (-0.5 * (imgWidthOut - 1) * fSina 
		- 0.5 * (imgHeightOut - 1) * fCosa + 0.5 * (m_nHeight - 1));
	// 循环变量，输出图像坐标
	int	i, j;
	//循环变量，像素的每个通道
	int k;
	//输出图像在输入图像中待插值的位置坐标，必须浮点型
	int	coordinateX, coordinateY;
	//存放待插值的16个像素的数组
	unsigned char array[4][4];
	//两个中间变量
	int Iu, Iv;
	//循环变量，对确定要插值的位置取4x4邻域用
	int x, y;

	// 立方卷积插值
	for(i = 0; i < imgHeightOut; i++)
	{
		for(j = 0; j < imgWidthOut; j++)
		{		
			// 输出图像像素(j,i)映射到输入图像的坐标
			coordinateX = j * fCosa - i * fSina + f1;
			coordinateY = j * fSina + i * fCosa + f2;

			//对坐标取整
			Iu=(int)coordinateX;
			Iv=(int)coordinateY;

			// 判断是否在原图范围内
			if( (coordinateX >= 1) && (coordinateX < m_nWidth-3) && (coordinateY >= 1) 
				&& (coordinateY < m_nHeight-3))
			{
				//将图像每个通道的数据进行分别插值，彩色图像pixelByte为3，
				//灰度图像pixelByte为1
				for(k=0;k<pixelByte;k++){
					//将当前处理像素周围4*4邻域像素拷贝至数组array
					for(y=Iv-1;y<Iv+3;y++){
						for (x=Iu-1;x<Iu+3;x++){
							array[y-Iv+1][x-Iu+1]=*(m_pImgData+y*lineByte+x*pixelByte+k);
						}
					}
					*(pImgOut + i * lineByteOut + j*pixelByte+k)
						=interpolationCube(array, coordinateX-Iu, coordinateY-Iv);
				}
			}
			else
			{
				// 对于不在原图内的像素，赋值为255
				for(k=0;k<pixelByte;k++)
					*(pImgOut+i*lineByteOut+j*pixelByte+k) = 255;
			}

		}

	}

	Copy(CSize(imgWidthOut,imgHeightOut),m_nBitCount,m_lpColorTable,pImgOut);

	delete[]pImgOut;

}
void CZJBaseDib::SetDimensions(CSize size)   //修改大小,不够的补白边
{
	int nWidh=size.cx;
	int nHeight=size.cy;   //要修改的大小
	
	int lineByt=(m_nWidth *m_nBitCount/8+3)/4*4;  //分别计算每行字节数
	int lineByteout=(nWidh *m_nBitCount/8+3)/4*4;  
	BYTE *pBuf= new BYTE[nHeight *lineByteout];
	memset(pBuf,0,sizeof(BYTE)*(nHeight *lineByteout));   //先填充黑色
    //分别计算从哪里开始复制位图数据
	int xoff=(nWidh < m_nWidth? 0:(nWidh-m_nWidth)/2);
    int yoff=(nHeight < m_nHeight? 0:(nHeight-m_nHeight)/2);
	int nBit=m_nBitCount /8;
	BYTE* p=0;
	for(int i=0; i< m_nHeight; ++i)
		for(int j=0; j<m_nWidth; ++j)
		{
			if(j >nWidh-1 || i>nHeight-1)  continue;
			for(int k=0; k< nBit; ++k)
			{
                 p= pBuf+ (i+yoff)*lineByteout +(j+xoff)*(nBit)+k;
				 *p = *(m_pImgData+(i)*lineByt +(j)*(nBit)+k);  //赋值
				 long a= *p;
			}
		}
	Copy(size,m_nBitCount,m_lpColorTable,pBuf);
	delete []pBuf;
}





/////////////////////////////////////////////////////////////////////////////
// CMyBaseDib commands
