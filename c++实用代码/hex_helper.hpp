/***************************************************************************** 
* FileName: hex_helper.hpp
* Description:
* Version: 
* Author:  ZhangW 
* Date:  // 2019/7/29 
*****************************************************************************/
#ifndef HEX_HELPER_HPP_
#define HEX_HELPER_HPP_
namespace utils
{
class HexHelper
{
public:
//********转十六进制字符串
static int HexToHexStr(const unsigned char *str, unsigned long strLen, char *result)
{
	if ((NULL == str) || (0 == strLen))
	{
		return 0;
	}
	if (NULL == result)
	{
		return 2 * strLen + 1;
	}
	unsigned char c;
	char h;
	int i = 0;
	while ( strLen-- )
	{
		c = *str++;

		//取字符的高四位
		h = (c>>4)&0x0F;
		if (h < 10)
		{
			//如果是 0-9 
			result[i++] = h + 48;//'0'
		} 
		else
		{
			//如果是 A-F
			result[i++] = h + 55;//'A' -16
		}
		//取字符的低四位
		h = c&0x0F;
		if (h < 10)
		{
			//如果是 0-9 
			result[i++] = h + 48;
		} 
		else
		{
			//如果是 A-F
			result[i++] = h + 55;
		}
	}
	result[i++] = 0;
	return i;
}


static int HexStrToHex(const char *str, long Len, char *result)
{
	if (Len % 2 == 1)
	{
		printf("warning: COesCommon::HexStrToHex,输入参数长度有误，长度-1\n");
		--Len;
	}
	unsigned char c;

	int i = 0;
	int index = 0;
	while (index < Len)
	{
		c = *(str + index);

		int high=0;

		if (c >= '0' && c <= '9')
		{
			high = (int)(c - '0');
		}
		else if (c >= 'A' && c <= 'F')
		{
			high = (int)(c - 'A') + 10;//加上10计算十进制值
		}

		int low=0;

		c = *(str + index + 1);

		if (c >= '0' && c <= '9')
		{
			low = (int)(c - '0');
		}
		else if (c >= 'A' && c <= 'F')
		{
			low = (int)(c - 'A') + 10;
		}

		int temp = (high << 4) + low;

		result[i] = (char)temp;

		i++;
		index += 2;
	}

	return i;
}

static int str_to_hexsimilarstr(const char* pstr,char*phexstr)
{
	if(phexstr==NULL || phexstr==NULL)
		return -1;

	int str_len = strlen(pstr);
	int j = 0;
	for(int i=0;i<str_len;i++)
	{
		phexstr[j++] = (unsigned char)pstr[i]>>4 | 0x30;
		phexstr[j++] = (pstr[i] & 0x0F) | 0x30;
	}
	return j;	
}

};

}
#endif //HEX_HELPER_HPP_