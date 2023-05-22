#include <stdlib.h>
#include <WINSOCK2.h> 
#include <shellapi.h>

#include <string.h>
#include <windows.h>
#include <Iphlpapi.h>
#include <Mprapi.h>  
#include <stdio.h>
#include <stdlib.h>
#include <WINSOCK2.h> 
#include <shellapi.h>
#include "TunHandler.h"
#include "Win32Helper.h"

#pragma comment(lib,"WS2_32.LIB") 
#pragma comment(lib, "Iphlpapi.lib")
#pragma comment( lib, "Mprapi.lib" )

//ͨ������������ȡGUID
int GetAdapterGUID(const char *AdapterName, char *pBuf, int nLen)
{
	int nRet = -1;
	ULONG ulOutBufLen = 0;
	PIP_ADAPTER_INFO pAdapterInfo = NULL;
	PIP_ADAPTER_INFO pAdapter = NULL;

	//��ȡ������������Ϣ
	if (GetAdaptersInfo(NULL, &ulOutBufLen) == ERROR_BUFFER_OVERFLOW)
	{
		pAdapterInfo = (PIP_ADAPTER_INFO)malloc(ulOutBufLen);
		if(pAdapterInfo)
		{
			if(GetAdaptersInfo(pAdapterInfo, &ulOutBufLen) == NO_ERROR)
			{
				pAdapter = pAdapterInfo;
				while(pAdapter)
				{
					if (0 == strncmp(AdapterName, pAdapter->Description, strlen(AdapterName)))
					{
						strncpy_s(pBuf, nLen, pAdapter->AdapterName, nLen - 1);
						nRet = 0;
						break;
					}
					pAdapter = pAdapter->Next;
				}

			}
			
			free(pAdapterInfo);
		}
	}

	return nRet;
}

//ͨ�����������ƻ�ȡIndex
int MyGetAdapterIndex(const char *AdapterName)
{
	int index = -1;
	ULONG ulOutBufLen = 0;
	PIP_ADAPTER_INFO pAdapterInfo = NULL;
	PIP_ADAPTER_INFO pAdapter = NULL;

	//��ȡ������������Ϣ
	if (GetAdaptersInfo (NULL, &ulOutBufLen) == ERROR_BUFFER_OVERFLOW)
	{
		pAdapterInfo = (PIP_ADAPTER_INFO)malloc(ulOutBufLen);
		if(pAdapterInfo)
		{
			if (GetAdaptersInfo(pAdapterInfo, &ulOutBufLen) == NO_ERROR)
			{
				pAdapter = pAdapterInfo;
				while(pAdapter)
				{
					if (0 == strncmp(AdapterName, pAdapter->Description, strlen(AdapterName)))
					{
						index = pAdapter->Index;
						break;
					}
					pAdapter = pAdapter->Next;
				}
			}
			free(pAdapterInfo);
		}
	}

	return index;
}

//ͨ��Index��ȡMetric1�����·��Ҫ�õ�Metric1
unsigned long GetMetric1(int Index)
{
	PMIB_IPFORWARDTABLE pIpRouteTab = NULL;
	ULONG dwActualSize = 0;
	DWORD  Metric1 = -1;

	//��ȡ·�ɱ�
	if(GetIpForwardTable(pIpRouteTab, &dwActualSize, TRUE) == ERROR_INSUFFICIENT_BUFFER)
	{
		pIpRouteTab = (PMIB_IPFORWARDTABLE)malloc(dwActualSize);

		if(GetIpForwardTable(pIpRouteTab, &dwActualSize, TRUE) == NO_ERROR)
		{
			for (DWORD i = 0; i < pIpRouteTab->dwNumEntries; i++)
			{
				if(pIpRouteTab->table[i].dwForwardIfIndex == Index)
				{
					Metric1 = pIpRouteTab->table[i].dwForwardMetric1;
					break;
				}
			}
		}
	}

	if(pIpRouteTab)
	{
		free(pIpRouteTab);
	}
	return Metric1;
}

//���������IP	��������ΪNULL�������� ADAPTER_NAME �������������������
int ClearIP(const char* AdapterName)
{
	ULONG ulOutBufLen = 0;
	PIP_ADAPTER_INFO pAdapterInfo = NULL;
	PIP_ADAPTER_INFO pAdapter = NULL;

	if(NULL == AdapterName)
	{
		AdapterName = ADAPTER_NAME;
	}

	if (GetAdaptersInfo (NULL, &ulOutBufLen) == ERROR_BUFFER_OVERFLOW)
	{
		pAdapterInfo = (PIP_ADAPTER_INFO)malloc(ulOutBufLen);
		if(pAdapterInfo)
		{
			if (GetAdaptersInfo(pAdapterInfo, &ulOutBufLen) == NO_ERROR)
			{
				pAdapter = pAdapterInfo;
				while(pAdapter)
				{
					if (0 == strncmp(AdapterName, pAdapter->Description, strlen(AdapterName)))
					{
						IP_ADDR_STRING *IP = &pAdapter->IpAddressList;
						while(IP)
						{
							ULONG Context = IP->Context;
							DeleteIPAddress(Context);
							IP = IP->Next;
						}
						break;
					}
					pAdapter = pAdapter->Next;
				}
			}
			else
			{
				return -1;
			}
			
			//free(pAdapterInfo);
		}
	}

	return 0;
}

//��ȡ�������������������� �硰��̫��1��֮�������
int GetLanAdapterName(int index, char *lanName)
{
	HANDLE   hMprConfig;
	DWORD   dwRet=0;
	PIP_INTERFACE_INFO   plfTable=NULL;
	IP_ADAPTER_INDEX_MAP   AdaptMap;
	DWORD   dwBufferSize=0;

	WCHAR   szFriendName[256];
	DWORD   tchSize=sizeof(WCHAR)*256;
	ZeroMemory(&szFriendName,tchSize);

	dwRet=MprConfigServerConnect   (NULL,&hMprConfig);
	dwRet=GetInterfaceInfo(NULL,&dwBufferSize);

	if(dwRet == ERROR_INSUFFICIENT_BUFFER)
	{
		plfTable=(PIP_INTERFACE_INFO)HeapAlloc(GetProcessHeap(),HEAP_ZERO_MEMORY,dwBufferSize);
		GetInterfaceInfo(plfTable,&dwBufferSize);
	}

	 for(int i=0; i<plfTable->NumAdapters; i++)
	 {
		 AdaptMap=plfTable->Adapter[i];
		 if(AdaptMap.Index == index)
		 {
			 dwRet=MprConfigGetFriendlyName(hMprConfig,AdaptMap.Name,(PWCHAR)szFriendName,tchSize);
			 int nLen = WideCharToMultiByte( CP_ACP,NULL, szFriendName,-1,NULL,0,NULL,FALSE );
			 WideCharToMultiByte (CP_ACP,NULL,szFriendName,-1,lanName,nLen,NULL,FALSE);
		 }
	 }
	 return 0;
}