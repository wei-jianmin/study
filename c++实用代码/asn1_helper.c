static const unsigned char *jump_asn1_item_tag(const unsigned char* ptag,unsigned char &type,bool &constructed,unsigned char &tag)
{
	type = ptag[0] & 0xC0;
	type >>= 6;
	constructed = (ptag[0] & 0x20)==1 ? true : false;
	tag = ptag[0] & 0x1F;
	return ptag+1;
}

//要求plength指向length的开始位置
//当value_len 返回 -1时，表明是变长数据
static const unsigned char *jump_asn1_item_length(const unsigned char* plength,long &value_len)
{
	long len_len=0;
	if(plength==NULL)
		return NULL;

	try
	{
		if(plength[0]<0x80)	//定长
		{
			len_len = 1;
			value_len = plength[0];
		}
		else if(plength[0]==0x80)	//变长
		{
			value_len = -1;
			len_len = 1;
		}
		else	//定长
		{
			value_len = 0;
			len_len = 1 + (plength[0] & 0x7F);
			for(int i=1; i<len_len; i++)
			{
				value_len <<= 8;
				value_len += plength[i];	// = p[ 1/*tag*/ + 1/*0x8X*/ + (i-1) ]
			}
		}
		return plength+len_len;
	}
	catch(...)
	{
		return NULL;
	}
}
//要求plength指向length的开始位置
//当value_len = -1时，表明是变长数据，函数执行后，value_len返回实际长度
static const unsigned char *jump_asn1_item_value(const unsigned char* pvalue,long &value_len)
{
	if(pvalue==NULL)
		return NULL;
	try
	{
		if(value_len >= 0)
			return pvalue+value_len;
		else
		{
			unsigned long len=0;
			do
			{
				if(pvalue[len]==0 && pvalue[len+1]==0)
					break;
			}while(++len);

			value_len = len+2;

			return pvalue+value_len;
		}
	}
	catch(...)
	{
		return NULL;
	}
}

static const unsigned char *jump_asn1_item(const unsigned char* pitem,unsigned long & item_len)
{
	long value_len=0;
	if(pitem==NULL)
		return NULL;
	try
	{
		const unsigned char * ptagdata=NULL;
		const unsigned char * plendata=NULL;
		const unsigned char * pvaldata=NULL;
		const unsigned char * pretdata=NULL;
		unsigned char type;
		bool constructed;
		unsigned char tag_val;
		unsigned long len_len = 0;
		ptagdata = pitem;
		plendata = jump_asn1_item_tag(ptagdata,type,constructed,tag_val);
		pvaldata = jump_asn1_item_length(plendata,value_len);
		len_len = pvaldata-plendata;
		pretdata = jump_asn1_item_value(pvaldata,value_len);
		item_len = 1+len_len+value_len;
		return pretdata;
	}
	catch(...)
	{
		return NULL;
	}
}

#if 0
//解析章结构，获取图片数据
bool getsealpic(const unsigned char* pseal,int& sealpic_w,int& sealpic_h,std::string& sealpic)
{
    bool constructed;
    unsigned char type,tag;
    const unsigned char* ucp = NULL;
    unsigned long item_len = 0;
    long value_len = 0;
    const unsigned char* ptmp = NULL;
    const unsigned char* psealpic = NULL;
    long sealpic_len = 0;
    char sealw[4],sealh[4];
    memset(sealh,0,4);
    memset(sealw,0,4);
    ucp = jump_asn1_item_tag((unsigned char*)pseal,type,constructed,tag);
    ucp = jump_asn1_item_length(ucp,value_len);
    ucp = jump_asn1_item_tag(ucp,type,constructed,tag);
    ucp = jump_asn1_item_length(ucp,value_len);
    ucp = jump_asn1_item(ucp,item_len);
    ucp = jump_asn1_item(ucp,item_len);
    ucp = jump_asn1_item(ucp,item_len);
    ucp = jump_asn1_item_tag(ucp,type,constructed,tag);
    ucp = jump_asn1_item_length(ucp,value_len);
    ucp = jump_asn1_item(ucp,item_len);
    ucp = jump_asn1_item_tag(ucp,type,constructed,tag);
    ucp = jump_asn1_item_length(ucp,sealpic_len);
    psealpic = ucp;
    ucp = jump_asn1_item_value(ucp,sealpic_len);
    ucp = jump_asn1_item_tag(ucp,type,constructed,tag);
    ucp = jump_asn1_item_length(ucp,value_len);
    ptmp = ucp;
    ucp = jump_asn1_item_value(ucp,value_len);
    memcpy(sealw,ptmp,value_len);
    ucp = jump_asn1_item_tag(ucp,type,constructed,tag);
    ucp = jump_asn1_item_length(ucp,value_len);
    ptmp = ucp;
    ucp = jump_asn1_item_value(ucp,value_len);
    memcpy(sealh,ptmp,value_len);
    sealpic.assign((const char*)psealpic,sealpic_len);
    sealpic_w = sealw[0]+sealw[1]*256+sealw[2]*65536;
    sealpic_h = sealh[0]+sealh[1]*256+sealh[2]*65536;
    return true;
}
#endif