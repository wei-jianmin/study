// TunTest.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include "TunHandler.h"
#include "Win32Helper.h"
#include "Proto.h"
#include <WS2tcpip.h>
#include <iostream>
#include <winsock2.h>
#include <windows.h>

#define MAX_PACKET_BUFFER 1024 * 8
#define TUN_ADDR	"10.1.1.35"
#define TUN_GW		"10.1.1.1"
#define TUN_MASK	"255.255.255.0"
#define TUN_DHCP	"10.1.1.1"

int main(int argc, CHAR* argv[])
{
	void* pTunDevice;

	pTunDevice = OpenTun(TUN_ADDR, TUN_MASK, TUN_DHCP);

	DelTunRouteAll();

	AddTunRoute("192.168.65.0", "255.255.255.0", TUN_GW);

	unsigned char buffer[MAX_PACKET_BUFFER] = { 0 };

	WinCreateEvent();

	while (1)
	{
		int readLen = ReadTun(buffer, MAX_PACKET_BUFFER);

		IPHDR* IpHdr = reinterpret_cast<IPHDR*>(buffer);
		// 只处理ICMP
		if (IpHdr->protocol != IP_PROTO_ICMP){
			continue;
		}

		// 输出源目的地址
		in_addr s;
		in_addr d;
		s.S_un.S_addr = IpHdr->saddr;
		d.S_un.S_addr = IpHdr->daddr;
		char sipstr[30] = { 0 };
		char dipstr[30] = { 0 };
		InetNtop(AF_INET, &s.S_un.S_addr, sipstr,sizeof(sipstr));
		InetNtop(AF_INET, &d.S_un.S_addr, dipstr, sizeof(dipstr));
		std::cout << "len " << readLen << " " << sipstr << " -> ";
		std::cout << dipstr << std::endl;

		// 交换 IP 头源目的地址
		uint32_t Address = IpHdr->saddr;
		IpHdr->saddr = IpHdr->daddr;
		IpHdr->daddr = Address;

		// 修改 ICMP 为应答包
		ICMPHDR* IcmpHdr = reinterpret_cast<ICMPHDR*>(buffer);
		IcmpHdr->type = 0;
		IcmpHdr->check_sum += 8;

		// 送回协议栈
		WriteTun(buffer, readLen);
	}
	return 0;
}

