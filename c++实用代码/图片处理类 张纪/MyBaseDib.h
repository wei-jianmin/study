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
	CZJBaseDib();				 // Ĭ�ϵĹ��캯��
	int m_nWidth;                //ͼ��Ŀ�����Ϊ��λ
	int m_nHeight;               //ͼ��ĸߣ�����Ϊ��λ
	unsigned char * m_pImgData;  //ͼ������ָ��	
	LPRGBQUAD m_lpColorTable;    //ͼ����ɫ��ָ��
	int m_nBitCount;             //ÿ����ռ��λ��
	LPBYTE m_lpDib;              //ָ��DIB��ָ�루����λͼ��ʼ��ַ��
	LPBITMAPINFOHEADER m_lpBmpInfoHead;         //ͼ����Ϣͷָ��
	HPALETTE m_hPalette;	     //��ɫ����
	int m_nColorTableLength;     //��ɫ����
	int m_iStyle;                //ģʽ 0:�޸�ģʽ  1:ֻ��ģʽ(�����������ɳ����ͷ�����)
	

// Operations
public:
	//���캯��
	CZJBaseDib(CSize size, int nBitCount, LPRGBQUAD lpColorTable, 
		unsigned char *pImgData);
	//�������캯��
	CZJBaseDib(CZJBaseDib &Dib); 
	int GetSize()    // ����BMP�������Ĵ�С
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
	bool GetMallocMen(LPBYTE pMen);   //��pMen���ڴ�������Ϊ�Լ��Ļ�����(�ʼ����ר��,ʹ��pMen�����ݣ������ı���)
	//DIB������
	BOOL ReadBmp(LPCTSTR lpszPathName);
	//DIBд����
	BOOL WriteBmp(LPCTSTR lpszPathName);
	void ZoomNormal(int nWidth, int	nHeight,int type);  //���� 
	//DIB��ʾ����
	BOOL Draw(CDC* pDC, CPoint origin, CSize size); 
	//�߼���ɫ�����ɺ���
	void MakePalette();
	//��ȡDIB�ĳߴ磨��ߣ�
	virtual CSize GetDimensions();
	void SetDimensions(CSize size);   //�޸Ĵ�С,�����Ĳ��ױ�
	//����ռ�
	virtual void Empty();	
	//���µ������滻��ǰDIB��������Ϣͷ
	virtual void Copy(CSize size, int nBitCount, LPRGBQUAD lpColorTable,unsigned char *pImgData);
	virtual CZJBaseDib& operator =( CZJBaseDib& Dib);
	//������ɫ��ĳ���
	int ComputeColorTabalLength(int nBitCount);
	void GetHuiClor();    //��ȡ�Ҷ�
	void RotateAngle(double angle) ;    // ˫������ת
	void RotateCube(int angle);         //���������ֵ��ת
	void CutEdge(int newWidth,int newHeight);  // �б�

	//���������ֵ
	unsigned char interpolationCube(unsigned char array[4][4], float xpos, float ypos);

public:
	virtual ~CZJBaseDib();

};


#endif // !defined(AFX_MYBASEDIB_H__40EDBE23_597C_4987_B7D2_3BD4F17678BE__INCLUDED_)
