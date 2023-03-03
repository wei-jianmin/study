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
//�������캯��
CZJBaseDib::CZJBaseDib(CZJBaseDib &Dib)
{
	Copy(Dib.GetDimensions(),Dib.m_nBitCount,Dib.m_lpColorTable,Dib.m_pImgData);
}

CZJBaseDib::~CZJBaseDib()
{
	//ɾ����Դ
 	Empty();
}

void CZJBaseDib::CutEdge(int NewWidth,int NewHeight)  // �б�
{
	if(m_pImgData==NULL) return;
	if(NewWidth >= m_nWidth) return;
    int nCutW = (m_nWidth - NewWidth)/2;
	int nCutH = (m_nHeight- NewHeight)/2;
	//���컺��
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
	this->Copy(CSize(width,height),m_nBitCount,m_lpColorTable,pImgDataOut);   //�������ź����ͼ��

	delete [] pImgDataOut;
}
void CZJBaseDib::ZoomNormal(int nWidth, int	nHeight,int iType)  
{
	if(m_pImgData==NULL) return;
	double fx=nWidth*1.0/m_nWidth;
	double fy=nHeight*1.0/m_nHeight;
	//����ԭͼ�񸱱�
	int widthin=m_nWidth;
	int heightin=m_nHeight;
	int lineByteout=(m_nWidth*m_nBitCount/8+3)/4*4;
	unsigned char* pImgDataOut=new  unsigned char[lineByteout *m_nHeight]; //���뻺���������ͼ�����ݸ���(��С����Ӱ��)
	memcpy(pImgDataOut,m_pImgData, lineByteout *m_nHeight);
  
	//�޸�ԭͼ��
	m_nWidth =nWidth;    //�����µĸ߶ȺͿ��
	m_nHeight =nHeight; 
	int lineByte=(m_nWidth*m_nBitCount/8+3)/4*4; //�����޸ĺ��ͼ��ÿ���ֽ���
	unsigned char* pImgData=new  unsigned char[lineByte *m_nHeight]; //���뻺����
	LPRGBQUAD lpColorTable=NULL;
	if(m_nColorTableLength!=0){
		lpColorTable=new RGBQUAD[ m_nColorTableLength]; //�������ɫ���򱣴渱��
		memcpy(lpColorTable,m_lpColorTable,sizeof(RGBQUAD) * m_nColorTableLength);
	}
	this->Copy(CSize(m_nWidth,m_nHeight),m_nBitCount,lpColorTable,pImgData);   //�������ź����ͼ��

    
    
	int i,j; //ѭ��������ͼ������
	int k;   //ѭ������,���ص�ÿ��ͨ��
	int pix=m_nBitCount /8;   //����ǲ�ɫ�ģ���Ҫ����3���ֽڵ���
	//ͼ���Ϸ�
	if(iType==0)  //����ڲ�ֵ
	for(i=0;i<m_nHeight;i++)
	{
		for(j=0;j<m_nWidth;j++)
		{
			int ixout= int(j/fx+0.5);
			int iyout= int(i/fy +0.5);
			if((0<=ixout && ixout<widthin) &&(0 <=iyout &&iyout<heightin) )  //ӳ���ȥӦ��С��ԭʼ�߶ȺͿ�Ȳź���
			{
				for(k=0;k<pix;k++)
				{
					if(int(i/fy)>0 && int(i/fy)<heightin &&int(j/fx)>0 &&int(j/fx)<widthin)
				
						*(m_pImgData+i*lineByte+j*pix+k)    //�µ����ص�
					=*(pImgDataOut+int(i/fy+0.5)*lineByteout+int(j/fx +0.5)*pix+k);//ԭͼ�����ص�\for(k=0;k<pixelByte;k++)
					
				}
			
			}
			else                     //�������ֱ������ɫ
			{
				for(k=0;k<pix;k++)
					*(m_pImgData+i*lineByte+j*pix+k) =255   ;//�µ����ص�
			
			}			
		}
	}
	else          //˫�߲�ֵ
	{
		// AfxMessageBox("");
		int clr1,clr2,clr3,clr4;   //��ʾ��Χ���ص���ĸ��������ػҶ�ֵ
		int x1,x2,y1,y2;           //�Խ�����������
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
				
				fxtmp=j/fx;    //�����Ӧ��ȥ������(�����ͣ���С��)
				fytmp=i/fy;
				//��Ӧ�������һ��Χ���ĸ�����֮�䣬���x1....y2����(���ǹ����������п��ܴ���ԭͼ��Խ����ϣ����x2,y2�����ڣ������ڴ�Խ��)
				
				x1=int(fxtmp); y1=int(fytmp);x2=int(fxtmp+1); 	y2=int(fytmp+1);
				
                u=fxtmp- int(fxtmp);  //����߷����С��
				v=fytmp -int(fytmp);  //�����귽���С��
				for(k=0;k<pix;k++)
				{
					// ���������ͼ������½�
					if ( (x1 >= widthin - 1) && (y1 >= heightin - 1) )
					{
						clr1 = *(pImgDataOut+y1*lineByteout+x1*pix+k);;	// (x1, y1) 
						*(m_pImgData+i*lineByte+j*pix+k) = clr1; 
					}
					// ���ͼ�������һ�����
					else if ( x1 >= widthin - 1 )
					{
						clr1 = *(pImgDataOut+y1*lineByteout+x1*pix+k);	// (x1, y1)
						clr3 = *(pImgDataOut+y2*lineByteout+x1*pix+k);	// (x1, y2)
						*(m_pImgData+i*lineByte+j*pix+k) = int(clr1 * (1 - v) + clr3 * v); 
					}			
					// ���ͼ�������һ�����
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
//�ⲿ����һ��λͼ���ݹ��츱��

CZJBaseDib::CZJBaseDib(CSize size, int nBitCount, LPRGBQUAD lpColorTable,
						   unsigned char *pImgData)
{
	//���û��λͼ���ݴ�����Ϊ�ǿյ�DIB����ʱ������DIB�ڴ�
	m_iStyle=0;
	m_lpDib=NULL;
	m_lpColorTable=NULL;
	m_pImgData=NULL; 
	m_lpBmpInfoHead=NULL; 
	m_hPalette = NULL;
	
	Copy(size,nBitCount,lpColorTable,pImgData);//�����λͼ���ݴ���	
}

CZJBaseDib& CZJBaseDib::operator=( CZJBaseDib& Dib)
{
	this->m_iStyle=Dib.m_iStyle;
	this->Copy(Dib.GetDimensions(),Dib.m_nBitCount,Dib.m_lpColorTable,Dib.m_pImgData);
	return *this;
}

//�ɲ���(ÿ������ռ��λ��)������ɫ����(��ɫ��ṹ�������)
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
//���ɵ�ɫ��(�����Ҷ�ͼ�������)
void CZJBaseDib::MakePalette()
{
	//�����ɫ����Ϊ0���������߼���ɫ��
	if(m_nColorTableLength == 0) 
		return;
	//ɾ���ɵĵ�ɫ�����
	if(m_hPalette != NULL) ::DeleteObject(m_hPalette);
	//���뻺�����������߼���ɫ��
	LPLOGPALETTE pLogPal = (LPLOGPALETTE) new char[2 * sizeof(WORD) +
		m_nColorTableLength * sizeof(PALETTEENTRY)];
	pLogPal->palVersion = 0x300;  //�����ֵ�ƺ��ǹ̶���
	pLogPal->palNumEntries = m_nColorTableLength;
	LPRGBQUAD m_lpDibQuad = (LPRGBQUAD) m_lpColorTable;
	for(int i = 0; i < m_nColorTableLength; i++) {
		pLogPal->palPalEntry[i].peRed = m_lpDibQuad->rgbRed;
		pLogPal->palPalEntry[i].peGreen = m_lpDibQuad->rgbGreen;
		pLogPal->palPalEntry[i].peBlue = m_lpDibQuad->rgbBlue;
		pLogPal->palPalEntry[i].peFlags = 0;
		m_lpDibQuad++;
	}	
	//�����߼���ɫ��
	m_hPalette = ::CreatePalette(pLogPal);	
	//�ͷŻ�����
	delete pLogPal;	
}	


// ͼ��ĳߴ磬��CSize���ͱ��
CSize CZJBaseDib::GetDimensions()
{	
	if(m_lpDib == NULL) return CSize(0, 0);
	return CSize(m_nWidth, m_nHeight);
}
//ɾ����Դ
void CZJBaseDib::Empty()
{
	//�ͷ�m_lpDib��ָ��Ļ�����
	if(m_lpDib != NULL)
	{
 		if(m_iStyle==0)  //0������������  1ֻ��ģʽ,��������������
		 delete [] m_lpDib;
	}
	//�ͷ��߼���ɫ�建����
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
//��men���ڴ�������Ϊ�Լ��Ļ�������pMen����֪��BMP������(�ʼ����ר��)
bool CZJBaseDib::GetMallocMen(LPBYTE pMen)
{
	//��ʼ��
	m_iStyle=1;  //ֻ��ģʽ
	Empty();     //ֻ��ģʽ��������ͷ��ⲿ����Դ
    if(pMen)  
	{
		if(pMen[0])  //������
		m_lpDib=pMen;
		else
		{
			return FALSE;
		}
	}

	//1Ϊ��Ա������ֵ
	m_lpBmpInfoHead=(BITMAPINFOHEADER*)(m_lpDib + sizeof(BITMAPFILEHEADER));
 	m_nHeight = m_lpBmpInfoHead->biHeight;  //��ȡ�߿�(ʹ���ļ�ͷ)
 	m_nWidth = m_lpBmpInfoHead->biWidth;
	m_nBitCount=m_lpBmpInfoHead->biBitCount; 


	//2������ɫ����
	m_nColorTableLength=
		ComputeColorTabalLength(m_nBitCount);
	
	//3�����߼���ɫ��
	m_hPalette = NULL;
	if(m_nColorTableLength!=0){
		m_lpColorTable=(LPRGBQUAD)(m_lpDib+sizeof(BITMAPINFOHEADER)+sizeof(BITMAPFILEHEADER));
		MakePalette();
	}	
	//4m_pImgDataָ��DIB��λͼ������ʼλ��
	m_pImgData = (LPBYTE)m_lpDib+sizeof(BITMAPINFOHEADER) +sizeof(BITMAPFILEHEADER)
			+sizeof(RGBQUAD) * m_nColorTableLength;
	
	return TRUE;

} 
//�滻λͼ����,��������Ϣͷ,�ǳ���Ҫ��һ������
void CZJBaseDib::Copy(CSize size, int nBitCount,  
							  LPRGBQUAD lpColorTable,unsigned char *pImgData)
{ 
	
	Empty();
	//0��Ա������ֵ
	m_nWidth=size.cx;
	m_nHeight=size.cy;
	m_nBitCount=nBitCount;
	m_nColorTableLength=ComputeColorTabalLength(nBitCount);//������ɫ��ĳ���
	int lineByte=(m_nWidth*nBitCount/8+3)/4*4;//ÿ��������ռ�ֽ�������չ��4�ı���
	int imgBufSize=m_nHeight*lineByte;//λͼ���ݵĴ�С

	LPRGBQUAD	lpColorTableOut=0;
	if(m_nColorTableLength!=0)    //���������ƣ�������ɫ����
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

	//1Ϊm_lpDib���·���ռ䣬�Դ���µ�DIB
	m_lpDib=new BYTE [sizeof(BITMAPINFOHEADER) + sizeof(RGBQUAD) * m_nColorTableLength+imgBufSize];

	//2��д�ļ�ͷ�ṹ
	m_lpBmpInfoHead = (LPBITMAPINFOHEADER) m_lpDib;

	//3��дλͼ��ϢͷBITMAPINFOHEADER�ṹ
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
	//��ɫ���ÿ�
	m_hPalette = NULL;

	//4�������ɫ������ɫ�����������ɵ�DIB�������ɵ�ɫ��
	if(m_nColorTableLength!=0){
		m_lpColorTable=(LPRGBQUAD)(m_lpDib+sizeof(BITMAPINFOHEADER));
		memcpy(m_lpColorTable,lpColorTableOut,sizeof(RGBQUAD) * m_nColorTableLength);
		MakePalette();
	}

	//5m_pImgDataָ��DIB��λͼ������ʼλ��
	m_pImgData = (LPBYTE)m_lpDib+sizeof(BITMAPINFOHEADER)+sizeof(RGBQUAD) * m_nColorTableLength;

	//6����λͼ���ݿ������µ�DIB��
	memcpy(m_pImgData,pImgData,imgBufSize);

	if(m_nColorTableLength!=0) 
	delete lpColorTableOut;
}

//дλͼ����
BOOL CZJBaseDib::WriteBmp(LPCTSTR lpszPathName)
{
	//дģʽ���ļ�
	CFile file;
	if (!file.Open(lpszPathName, CFile::modeCreate | CFile::modeReadWrite 
		| CFile::shareExclusive))
		return FALSE;
	
	//��д�ļ�ͷ�ṹ
	BITMAPFILEHEADER bmfh;
	bmfh.bfType = 0x4d42;  // 'BM' �̶�
	bmfh.bfSize = 0;
	bmfh.bfReserved1 = bmfh.bfReserved2 = 0;
	bmfh.bfOffBits = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) +
		sizeof(RGBQUAD) * m_nColorTableLength;	
	try {
		//�ļ�ͷ�ṹд���ļ�
		file.Write((LPVOID) &bmfh, sizeof(BITMAPFILEHEADER));
		
		//�ļ���Ϣͷ�ṹд���ļ�
		file.Write(m_lpBmpInfoHead,  sizeof(BITMAPINFOHEADER));
		
		//�������ɫ��Ļ�����ɫ��д���ļ�
		if(m_nColorTableLength!=0)
			file.Write(m_lpColorTable, sizeof(RGBQUAD) * m_nColorTableLength);
		
		//λͼ����д���ļ�
		int imgBufSize=(m_nWidth*m_nBitCount/8+3)/4*4*m_nHeight;
		file.Write(m_pImgData, imgBufSize);
	}
	catch(CException* pe) {
		pe->Delete();
		file.Close();
		AfxMessageBox(L"write error");
		return FALSE;
	}
	
	//��������
	file.Close();
	return TRUE;
}


BOOL CZJBaseDib::ReadBmp(LPCTSTR lpszPathName)
{
	 //MessageBox(NULL,lpszPathName,"",MB_OK);
	//��ģʽ��ͼ���ļ�
	CFile file;
	if (!file.Open(lpszPathName, CFile::modeRead | CFile::shareDenyWrite))
		return FALSE;
	
	BITMAPFILEHEADER bmfh;
	try {
		//����ռ�
		Empty();
		
		//��ȡBITMAPFILEHEADER�ṹ������bmfh��
		int nCount=file.Read((LPVOID) &bmfh, sizeof(BITMAPFILEHEADER));
		
		// �ж��Ƿ�ΪBMP��ʽ
		char NAME[24];
		memset(NAME, 0, 24);
		memcpy(NAME,(char*)&bmfh,2);
		CString sName(NAME);
		if(sName != "BM")
			return FALSE;

		//Ϊm_lpDib����ռ�
		m_lpDib=new BYTE[file.GetLength() -sizeof(BITMAPFILEHEADER)];
		
		//��ȡ����ʱ���ɺ����ļ�ͷ
		file.Read(m_lpDib, file.GetLength() -sizeof(BITMAPFILEHEADER));	
		m_lpBmpInfoHead = (LPBITMAPINFOHEADER)m_lpDib;
		
		//Ϊ��Ա������ֵ
		m_nWidth=m_lpBmpInfoHead->biWidth;
		m_nHeight=m_lpBmpInfoHead->biHeight;
		m_nBitCount=m_lpBmpInfoHead->biBitCount; 
		
		//������ɫ����
		m_nColorTableLength=ComputeColorTabalLength(m_lpBmpInfoHead->biBitCount);
			
		//�����߼���ɫ��
		m_hPalette = NULL;
		if(m_nColorTableLength!=0){
			m_lpColorTable=(LPRGBQUAD)(m_lpDib+sizeof(BITMAPINFOHEADER));
			MakePalette();
		}	
		//m_pImgDataָ��DIB��λͼ������ʼλ��
		m_pImgData = (LPBYTE)m_lpDib+sizeof(BITMAPINFOHEADER) 
			+sizeof(RGBQUAD) * m_nColorTableLength;
			
	}
	catch(CException* pe) {
		//AfxMessageBox("Read error");
		pe->Delete();
		return FALSE;
	}
	file.Close();
	//��������
	return TRUE;
}


BOOL CZJBaseDib::Draw(CDC* pDC, CPoint origin, CSize size)
{
	//�ɵĵ�ɫ����
	HPALETTE hOldPal=NULL;
	
	//���DIBΪ�գ��򷵻�0
	if(m_lpDib == NULL) return FALSE;
	
	//���DIB�е�ɫ�壬��ѡ���豸������
	if(m_hPalette != NULL) {
		hOldPal=::SelectPalette(pDC->GetSafeHdc(), m_hPalette, TRUE);
	}
	
	//����λͼ����ģʽ
	pDC->SetStretchBltMode(COLORONCOLOR);
	
	//��DIB��pDC��ָ����豸�Ͻ�����ʾ
	::StretchDIBits(pDC->GetSafeHdc(), origin.x, origin.y, size.cx, size.cy,
		0, 0, m_lpBmpInfoHead->biWidth, m_lpBmpInfoHead->biHeight,m_pImgData,
		(LPBITMAPINFO) m_lpBmpInfoHead, DIB_RGB_COLORS, SRCCOPY);
	
	//�ָ��ɵĵ�ɫ��
	if(hOldPal!=NULL)
		::SelectPalette(pDC->GetSafeHdc(), hOldPal, TRUE);
	
	//��������
	return TRUE;
}

void CZJBaseDib::GetHuiClor()    //��ȡ�Ҷ�
{
    //1�����ռ�
	int nBit=m_nBitCount/3;   //��ɫ
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
				if(k==0) sum+= 0.11 *(*p);   //�Ҷȼ��㹫ʽ
				if(k==1) sum+= 0.59*(*p);
				if(k==2) sum+= 0.30*(*p);
				p++;
			}
			*p2=int(sum);   //��ֵ
		}
		//������ɫ����
		m_nColorTableLength=ComputeColorTabalLength(nBit);
		
		//��ɫͼ��û����ɫ�������Ҫ����
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

	//�������飬�����ֵ����Ҫ��ϵ��
	float col[4], row[4];

	//׼����ֵ��x��������Դ
	col[0]=xpos+1;
	col[1]=xpos;
	col[2]=1-xpos;
	col[3]=2-xpos;

	//׼����ֵ��y��������Դ
	row[0]=ypos+1;
	row[1]=ypos;
	row[2]=1-ypos;
	row[3]=2-ypos;

	//ѭ������
	int i;

	//��ʱ����
	float t;

	//��ˮƽ����ϵ��������м���
	for(i=0;i<4;i++){
		t=fabs(col[i]);
		if (t>=0&&t<1)
			col[i]=pow(t,3)-2*pow(t,2)+1;
		else if (t>=1&&t<2)
			col[i]=-pow(t,3)+5*pow(t,2)-8*t+4;
		else
			col[i]=0;
	}

	//�Դ�ֱ����ϵ��������м���
	for(i=0;i<4;i++){
		t=fabs(row[i]);
		if (t>=0&&t<1)
			row[i]=pow(t,3)-2*pow(t,2)+1;
		else if (t>=1&&t<2)
			row[i]=-pow(t,3)+5*pow(t,2)-8*t+4;
		else
			row[i]=0;
	}

	//������õ�ϵ�����Ӧͼ���������������
	float tempArray[4], temp;
	//��x������
	for(i=0;i<4;i++)
		tempArray[i]=row[0]*array[0][i]+row[1]*array[1][i]+row[2]*array[2][i]+row[3]*array[3][i];

	//��y������
	temp=0;
	for (i=0;i<4;i++)
		temp+=tempArray[i]*col[i];

	//����ֵ�����ͼ��Ҷȼ���Χ�����
	if (temp>255)
		temp=255;
	if (temp<0)
		temp=0;

	//��������ֵ����ֵ���
	return (unsigned char)temp;

}
void CZJBaseDib::RotateAngle(double angle) 
{
	/*˵������ת��ʽ���뱣֤ԭ����ͼ�����Ĳ����ã���ˣ���Ҫ��Դͼ��ԭ��ƽ�Ƶ�ͼ�����ĵ�,
	����������ϵ;
	������Ϻ󣬿��ܳ��������Ǹ������������Ҫ�����µ����ĵ㣬������任�ٽ�����ƽ�ƻ�ͼ��
	��ԭ����ϵ��������Ȼ���������ˣ�Ҳֻ�����������ǶԵģ�
	����ǰ��ӳ�䷽������Դͼ���Ӧ�������ֵ����������ֵ�������Ҫ�������̵ġ���任��ʽ����
	ѡ��һ�ֲ�ֵ������������Ĺ���*/

	if(angle <0) angle = angle *(-1);
	if(angle >360) angle = int(angle) %360;

	if(m_pImgData==NULL)  return;
	// ԭʼͼ���ĸ��ǵ�����
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
	
	// ������ת�Ƕȵ����Һ�����ֵ
    double fSin = sin(angle*2*Pi/360);
    double fCos = cos(angle*2*Pi/360);
	
	// ͼ�񾭹���ת���ĸ��ǵ�����
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
	
	// ������ת��ͼ��Ĵ�С
	int outWidth,outHeight;
	outWidth = (UINT)( max( fabs(tranX4-tranX1), fabs(tranX3-tranX2) ) + 1.5 );
	outHeight = (UINT)( max( fabs(tranY4-tranY1), fabs(tranY3-tranY2) ) + 1.5 );

	int lineByteout=(outWidth*m_nBitCount/8+3)/4*4;  //�ֱ����ÿ���ֽ���
	int lineByte=(m_nWidth*m_nBitCount/8+3)/4*4;

	BYTE *pBuf = new BYTE[lineByteout * outHeight ];
	memset(pBuf, 255, lineByteout * outHeight);  //��ȫ�����ϰ�ɫ��Ȼ����任��ֵ
	
	// ������������
	double num1 = -0.5*outWidth*fCos - 0.5*outHeight*fSin + 0.5*m_nWidth;
	double num2 = 0.5*outWidth*fSin - 0.5*outHeight*fCos + 0.5*m_nHeight;
	
	BYTE*	p = NULL;	// �������ص���ʼλ��
	//int		x = 0;				// �任������غ�����
	//int		y = 0;				// �任�������������
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
			double x= (i * fCos + j * fSin + num1 );   //��任
			double y= (-i * fSin + j * fCos + num2);
			// ���뵱ǰ��������ĸ�������
			int	x1, x2, y1, y2;
			x1 = (int)x;
			x2 = x1 + 1;
			y1 = (int)y;
			y2 = y1 + 1;
			double u, v;

			u = x - x1;  //�������ϵ��
			v = y - y1;
			if (x >= 0 && x <= m_nWidth && y >= 0 && y <= m_nHeight)  //λ��Դͼ�����޸�
			{
				for(int k=0; k< nBix; ++k)
				{
					p = pBuf + j * lineByteout  + i* nBix +k;  // ���ص�ַ

					// ��������ֵ ʹ��˫���Բ�ֵ
					if(x2== m_nWidth && (y2)<m_nHeight)  //���ұ� �����ֵ
					{
						p1=m_pImgData + y1 * lineByte  + x1* nBix +k;	
						p3=m_pImgData + y2 * lineByte  + x1* nBix +k;
						*p = (BYTE)((*p1) *(1-v)+ (*p3) *  v);
					}
					else if((y2)==m_nHeight && (x2)<m_nWidth)  //���ϱ�  �����ֵ
					{
						p1=m_pImgData + y1 * lineByte  + x1* nBix +k;
						p2=m_pImgData + y1 * lineByte  + (x2)* nBix +k;
						*p = (BYTE)((*p1) *(1-u) + (*p2) *u );
					}
					else if((y2)==m_nHeight && (x2)== m_nWidth)  //���Ͻ� �޷���ֵ
					{
						p1=m_pImgData + y1 * lineByte  + x1* nBix +k;
						*p = *p1;
					}
					else    //�������� 
					{
						/*˫���Բ�ֵ*/
						p1=m_pImgData + y1 * lineByte  + x1* nBix +k;
						p2=m_pImgData + y1 * lineByte  + (x2)* nBix +k;
						p3=m_pImgData + (y2) * lineByte  + x1* nBix +k;
						p4=m_pImgData + (y2) * lineByte  + (x2)* nBix +k;
						
						BYTE a,b;
						a=(*p1) *(1-u) + (*p2) *u ;
						b=(*p3) * (1-u)+ (*p4) *u ;
						*p =(BYTE)(a *(1-v) + b*v);



						// ����ڲ�ֵ
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

	//ÿ������ռ�ֽ���������ͼ�������ͼ����ͬ
	int pixelByte=m_nBitCount/8;

	// ����ͼ��ÿ��������ռ�ֽ���
	int lineByte=(m_nWidth*pixelByte+3)/4*4;

	// ��ת�Ƕȣ����ȣ�, ����ת�ǶȴӶ�ת��������
	float	fRotateAngle= 2*3.1415926*angle/360;

	// ����ͼ���ĸ��ǵ����꣬��ͼ������Ϊ����ϵԭ��
	float	fSrcX1,fSrcY1,fSrcX2,fSrcY2,fSrcX3,fSrcY3,fSrcX4,fSrcY4;

	// ��ת���ĸ��ǵ����꣬��ͼ������Ϊ����ϵԭ��
	float	fDstX1,fDstY1,fDstX2,fDstY2,fDstX3,fDstY3,fDstX4,fDstY4;

	// ������ת�Ƕȵ�����
	float fSina = (float) sin((double)fRotateAngle);

	// ������ת�Ƕȵ�����
	float fCosa = (float) cos((double)fRotateAngle);

	// ����ԭͼ���ĸ��ǵ����꣬��ͼ������Ϊ����ϵԭ��
	fSrcX1 = (float) (- (m_nWidth  - 1) / 2);
	fSrcY1 = (float) (  (m_nHeight - 1) / 2);
	fSrcX2 = (float) (  (m_nWidth  - 1) / 2);
	fSrcY2 = (float) (  (m_nHeight - 1) / 2);
	fSrcX3 = (float) (- (m_nWidth  - 1) / 2);
	fSrcY3 = (float) (- (m_nHeight - 1) / 2);
	fSrcX4 = (float) (  (m_nWidth  - 1) / 2);
	fSrcY4 = (float) (- (m_nHeight - 1) / 2);

	// ������ͼ�ĸ��ǵ����꣬��ͼ������Ϊ����ϵԭ��
	fDstX1 =  fCosa * fSrcX1 + fSina * fSrcY1;
	fDstY1 = -fSina * fSrcX1 + fCosa * fSrcY1;
	fDstX2 =  fCosa * fSrcX2 + fSina * fSrcY2;
	fDstY2 = -fSina * fSrcX2 + fCosa * fSrcY2;
	fDstX3 =  fCosa * fSrcX3 + fSina * fSrcY3;
	fDstY3 = -fSina * fSrcX3 + fCosa * fSrcY3;
	fDstX4 =  fCosa * fSrcX4 + fSina * fSrcY4;
	fDstY4 = -fSina * fSrcX4 + fCosa * fSrcY4;

	// ��ת�����ͼ����
	int imgWidthOut  = (LONG) ( max( fabs(fDstX4 - fDstX1), fabs(fDstX3 - fDstX2) ) + 0.5);

	// ��ת�����ͼ��߶�
	int imgHeightOut = (LONG) ( max( fabs(fDstY4 - fDstY1), fabs(fDstY3 - fDstY2) ) + 0.5);

	// ��ת�����ͼ��ÿ�е��ֽ���
	int lineByteOut=(imgWidthOut*pixelByte+3)/4*4;

	//���仺�����������ת���
	unsigned char * pImgOut = new unsigned char[lineByteOut* imgHeightOut];

	// �������������������Ժ�ÿ�ζ�������
	float f1 = (float) (-0.5 * (imgWidthOut - 1) * fCosa 
		+ 0.5 * (imgHeightOut - 1) * fSina + 0.5 * (m_nWidth  - 1));
	float f2 = (float) (-0.5 * (imgWidthOut - 1) * fSina 
		- 0.5 * (imgHeightOut - 1) * fCosa + 0.5 * (m_nHeight - 1));
	// ѭ�����������ͼ������
	int	i, j;
	//ѭ�����������ص�ÿ��ͨ��
	int k;
	//���ͼ��������ͼ���д���ֵ��λ�����꣬���븡����
	int	coordinateX, coordinateY;
	//��Ŵ���ֵ��16�����ص�����
	unsigned char array[4][4];
	//�����м����
	int Iu, Iv;
	//ѭ����������ȷ��Ҫ��ֵ��λ��ȡ4x4������
	int x, y;

	// ���������ֵ
	for(i = 0; i < imgHeightOut; i++)
	{
		for(j = 0; j < imgWidthOut; j++)
		{		
			// ���ͼ������(j,i)ӳ�䵽����ͼ�������
			coordinateX = j * fCosa - i * fSina + f1;
			coordinateY = j * fSina + i * fCosa + f2;

			//������ȡ��
			Iu=(int)coordinateX;
			Iv=(int)coordinateY;

			// �ж��Ƿ���ԭͼ��Χ��
			if( (coordinateX >= 1) && (coordinateX < m_nWidth-3) && (coordinateY >= 1) 
				&& (coordinateY < m_nHeight-3))
			{
				//��ͼ��ÿ��ͨ�������ݽ��зֱ��ֵ����ɫͼ��pixelByteΪ3��
				//�Ҷ�ͼ��pixelByteΪ1
				for(k=0;k<pixelByte;k++){
					//����ǰ����������Χ4*4�������ؿ���������array
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
				// ���ڲ���ԭͼ�ڵ����أ���ֵΪ255
				for(k=0;k<pixelByte;k++)
					*(pImgOut+i*lineByteOut+j*pixelByte+k) = 255;
			}

		}

	}

	Copy(CSize(imgWidthOut,imgHeightOut),m_nBitCount,m_lpColorTable,pImgOut);

	delete[]pImgOut;

}
void CZJBaseDib::SetDimensions(CSize size)   //�޸Ĵ�С,�����Ĳ��ױ�
{
	int nWidh=size.cx;
	int nHeight=size.cy;   //Ҫ�޸ĵĴ�С
	
	int lineByt=(m_nWidth *m_nBitCount/8+3)/4*4;  //�ֱ����ÿ���ֽ���
	int lineByteout=(nWidh *m_nBitCount/8+3)/4*4;  
	BYTE *pBuf= new BYTE[nHeight *lineByteout];
	memset(pBuf,0,sizeof(BYTE)*(nHeight *lineByteout));   //������ɫ
    //�ֱ��������￪ʼ����λͼ����
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
				 *p = *(m_pImgData+(i)*lineByt +(j)*(nBit)+k);  //��ֵ
				 long a= *p;
			}
		}
	Copy(size,m_nBitCount,m_lpColorTable,pBuf);
	delete []pBuf;
}





/////////////////////////////////////////////////////////////////////////////
// CMyBaseDib commands
