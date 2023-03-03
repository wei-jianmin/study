/***************************************************************************** 
* FileName: machine_helper.hpp
* Description:
* Version: 
* Author:  ZhangW
* Date:  // 2019/7/29
*****************************************************************************/
#ifndef MACHINE_HELPER_HPP_
#define MACHINE_HELPER_HPP_
//获取mac用
#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#ifdef WIN32		
#include <winsock2.h>
#include <windows.h>
#include <Iphlpapi.h>
#include <stdio.h>
#include <Iptypes.h>
#pragma comment(lib,"Iphlpapi.lib")
#else   
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <linux/if.h>
#endif

namespace utils
{
class MachineHelper
{
public:
	//返回1代表成功 需自己申请空间
	static int GetMacAddr(std::string &addr)
	{
		/* implementation for Linux */
#ifdef WIN32
		char szMac[64];
		std::string strAdapterInfo;
		PIP_ADAPTER_INFO pAdapterInfo;
		DWORD dwRetVal = 0;
		unsigned long ulOutBufLen;

		strAdapterInfo.assign(sizeof(IP_ADAPTER_INFO),0);
		pAdapterInfo = (IP_ADAPTER_INFO *)strAdapterInfo.c_str();
		ulOutBufLen = sizeof(IP_ADAPTER_INFO);

		addr.clear();
		if (GetAdaptersInfo( pAdapterInfo, &ulOutBufLen) == ERROR_BUFFER_OVERFLOW) {
			strAdapterInfo.resize(ulOutBufLen,0);
			pAdapterInfo = (IP_ADAPTER_INFO *)strAdapterInfo.c_str(); 
		}

		if ((dwRetVal = GetAdaptersInfo( pAdapterInfo, &ulOutBufLen)) == NO_ERROR) {
			if (pAdapterInfo) {
				memset(szMac, 0, 64);
				sprintf(szMac, "%02X:%02X:%02X:%02X:%02X:%02X", 
					pAdapterInfo->Address[0], 
					pAdapterInfo->Address[1],
					pAdapterInfo->Address[2],
					pAdapterInfo->Address[3],
					pAdapterInfo->Address[4],
					pAdapterInfo->Address[5]);
				addr.append(szMac);
			}
			//strmactrim(addr);
		}
		else {
			return 0;
		}
#else 
		struct ifreq ifr;
		struct ifreq *IFR;
		struct ifconf ifc;
		unsigned int uNICCount = 0;
		char buf[1024];
		char szbuff[16];
		struct sockaddr_in *pAddr;
		int s, i,j;
		int ok = 0;

		s = socket(AF_INET, SOCK_DGRAM, 0);
		if (s==-1) {
			return 0;
		}
		ifc.ifc_len = sizeof(buf);
		ifc.ifc_buf = buf;
		ioctl(s, SIOCGIFCONF, &ifc);
		uNICCount = ifc.ifc_len / sizeof(struct ifreq);
		// printf("NIC total is : %d\n", uNICCount);

		IFR = ifc.ifc_req;
		strcpy(addr,"");    
		for (i = 0;i < uNICCount; i++,IFR++)
		{   
			strcpy(ifr.ifr_name, IFR->ifr_name);
			//printf( "%d NIC %s ",i,IFR->ifr_name); 
			if (ioctl(s, SIOCGIFFLAGS, &ifr) == 0)
			{
				if (! (ifr.ifr_flags & IFF_LOOPBACK)) 
				{
					if (ioctl(s, SIOCGIFHWADDR, &ifr) == 0) 
					{               
						sprintf(szbuff,"%.2X:%.2X:%.2X:%.2X:%.2X:%.2X",
							(unsigned char)ifr.ifr_hwaddr.sa_data[0],
							(unsigned char)ifr.ifr_hwaddr.sa_data[1],
							(unsigned char)ifr.ifr_hwaddr.sa_data[2],
							(unsigned char)ifr.ifr_hwaddr.sa_data[3],
							(unsigned char)ifr.ifr_hwaddr.sa_data[4],
							(unsigned char)ifr.ifr_hwaddr.sa_data[5]);  
						strcat(addr,szbuff);            
						ok = 1; 
						break;
					}
					else
					{
						close(s);
						return 0;
					}
				}
			}   
		}
		//strmactrim(addr);
		close(s);  
		if (ok==0) return 0;

#endif
		/* Not implemented platforms */
		return 1;
	}
};
}

#endif //MACHINE_HELPER_HPP_