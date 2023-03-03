#include <boost/asio.hpp>
#include "base64.h"
#include  "cu_loger.h"

#ifdef _WINDOWS	//Ϊ��ʹ��gethostbyname,inet_ntoa����
#include <WinSock2.h>
#else
#include <netdb.h>
#include <sys/socket.h>
#endif
#include "http_req.h"
namespace utils
{
using boost::asio::ip::tcp;
#define URLSIZE 1024 

/**
 * @param[in]  
 * @param[out] 
 * @param[i/o] 
 * @return     �ɹ�����0
 * @brief      
 * @author WeiJianMin
 * @time 2018/12/6
 */
int HttpReq::PostData(const stdex::string& url,
					  const stdex::string& data,
					  stdex::string &reponse,
					  const stdex::string& user_name,
					  const stdex::string& password,
					  int content_type)
{
	stdex::string host,port,param,ip;
	char buf[6]={0};
	host = GetHostAddrFromUrl(url.c_str());
	ip = GetIPFromUrl(url.c_str()); 
	sprintf(buf,"%d",GetPortFromUrl(url.c_str()));
	port = buf;
	param = GetParamFromUrl(url.c_str());
	return post(/*host*/ip,port,param,data,user_name,password,reponse,content_type);
}

/**
 * @param[in]  
 * @param[out] 
 * @param[i/o] 
 * @return     �ɹ�����0
 * @brief      
 * @author WeiJianMin
 * @time 2018/12/6
 */
int HttpReq::post(const stdex::string& host, const stdex::string& port, 
				   const stdex::string& page, const stdex::string& data, 
				   const stdex::string& user_name,const stdex::string& password,
				   stdex::string& reponse_data,int content_type)
{
  if(host.empty() || port.empty())
  {
    reponse_data = "param error.";
    return -1;
  }
  try
  {
    boost::asio::io_service io_service;
    //���io_service���ڸ��õ����
    if(io_service.stopped())
      io_service.reset();

    // ��dnsȡ�������µ�����ip
    tcp::resolver resolver(io_service);
    tcp::resolver::query query(host.c_str(), port.c_str());
    tcp::resolver::iterator endpoint_iterator = resolver.resolve(query);
    
    // �������ӵ����е�ĳ��ipֱ���ɹ� 
    tcp::socket socket(io_service);
    boost::asio::connect(socket, endpoint_iterator); 

    // Form the request. We specify the "Connection: close" header so that the
    // server will close the socket after transmitting the response. This will
    // allow us to treat all data up until the EOF as the content.
    boost::asio::streambuf request;
    std::ostream request_stream(&request);

	stdex::string str_base,str_base_base64;
	str_base = user_name + ":" + password;
	if(str_base.length()>3)
	{
		int base64_len = utils::Base64::TestBase64EncLength(str_base.length(),0); 
		str_base_base64.resize(base64_len,0);
		utils::Base64::base64_decode_ex((unsigned char*)str_base.c_str(),(unsigned char*)str_base_base64.c_str());
	}
	else
	{
		str_base_base64 = str_base;	
	}

	request_stream << "POST " << page.c_str() << " HTTP/1.0\r\n";
    request_stream << "Host: " << host.c_str()<< ":" << port << "\r\n";
    request_stream << "Accept: */*\r\n";
    request_stream << "Content-Length: " << data.length() << "\r\n";
	if(content_type == X_WWW_FORM_URLENCODED)
		request_stream << "Content-Type: application/x-www-form-urlencoded\r\n";
	else if(content_type == APPLICATION_JSON)
		request_stream << "Content-Type: application/json\r\n";
	else
		request_stream << "Content-Type: application/timestamp-query\r\n";
	request_stream << "Content-Transfer-Encoding:binary\r\n";
	if(str_base_base64.empty() == false)
	{
		request_stream << "Authorization:Basic ";
		request_stream << str_base_base64;
		request_stream << "\r\n";
	}
    request_stream << "Connection: close\r\n\r\n";
    request_stream << data;


    // Send the request.
    boost::asio::write(socket, request);

    // Read the response status line. The response streambuf will automatically
    // grow to accommodate the entire line. The growth may be limited by passing
    // a maximum size to the streambuf constructor.
    boost::asio::streambuf response;
    boost::asio::read_until(socket, response, "\r\n");

    // Check that response is OK.
    std::istream response_stream(&response);
    stdex::string http_version;
    response_stream >> http_version;
    unsigned int status_code;
    response_stream >> status_code;
    stdex::string status_message;
    std::getline(response_stream, status_message);
    if (!response_stream || http_version.substr(0, 5) != "HTTP/")
    {
      reponse_data = "Invalid response";
      return -2;
    }
    // ������������ط�200����Ϊ�д�,��֧��301/302����ת
    if (status_code != 200)
    {
      reponse_data = "Response returned with status code != 200 " ;
      return status_code;
    }

    // ��˵�еİ�ͷ���Զ�������
    stdex::string header;
    stdex::vector<stdex::string> headers;        
    while (std::getline(response_stream, header) && header != "\r")
      headers.push_back(header);

    // ��ȡ����ʣ�µ�������Ϊ����
    boost::system::error_code error;
    while (boost::asio::read(socket, response,
        boost::asio::transfer_at_least(1), error))
    {           
    }

    //��Ӧ������
    if (response.size())
    {
      std::istream response_stream(&response);
      std::istreambuf_iterator<char> eos;
	  reponse_data = stdex::string(std::istreambuf_iterator<char>(response_stream), eos);                        
    }

    if (error != boost::asio::error::eof)
    {
      reponse_data = error.message();
      return -3;
    }
  }
  catch(std::exception& e)
  {
	  reponse_data = e.what();
      return -4;  
  }
  return 0;
}
//
//int main(int argc, char* argv[])
//{
//  string host = "127.0.0.1";   
//  string port = "80";
//  string page = "/auth/login";
//  string data = "user_name=linbc&password=a";
//  string reponse_data;
//
//  int ret = post(host, port, page, data, reponse_data);
//  if (ret != 0)
//    std::cout << "error_code:" << ret << std::endl;
//
//  std::cout << reponse_data << std::endl;
//
//  return 0;
//}


//��HTTP����URL�л�ȡHTTP�������������ֵ����Ϊ�գ�û�в�����  
stdex::string HttpReq::GetParamFromUrl(const char* strUrl)  
{     
	char url[URLSIZE] = {0};  
	strcpy(url, strUrl);  

	char* strAddr = strstr(url, "http://");//�ж���û��http://  
	if(strAddr == NULL) {  
		strAddr = strstr(url, "https://");//�ж���û��https://  
		if(strAddr != NULL) {  
			strAddr += 8;  
		}  
	} else {  
		strAddr += 7;  
	}  

	if(strAddr == NULL) {  
		strAddr = url;  
	}  

	int iLen = strlen(strAddr);  
    stdex::string str_param(iLen+1,0);
	char* strParam = (char*)str_param.c_str();  
	int iPos = -1;  
	for(int i=0; i<iLen+1; i++) {  
		if(strAddr[i] == '/') {  
			iPos = i;  
			break;  
		}  
	}  
	if(iPos == -1) {  
		strcpy(strParam, "");;  
	} else {  
		strcpy(strParam, strAddr+iPos/*+1*/);  
	}  
	return str_param;  
}  


//��HTTP����URL�л�ȡ�˿ں�  
int HttpReq::GetPortFromUrl(const char* strUrl)  
{  
	int iPort = -1;  
    stdex::string strHostAddr = GetHostAddrFromUrl(strUrl);   
	if(strHostAddr.empty()) {  
		return -1;  
	}  

	char strAddr[URLSIZE] = {0};  
	strcpy(strAddr, strHostAddr.c_str());  

	char* strPort = strchr(strAddr, ':');  
	if(strPort == NULL) {  
		iPort = 80;  
	} else {  
		iPort = atoi(++strPort);  
	}  
	return iPort;  
}  


//��HTTP����URL�л�ȡIP��ַ  
stdex::string HttpReq::GetIPFromUrl(const char* strUrl)  
{  
    stdex::string str_ret="";
    if(strUrl == NULL)
        return str_ret;

	stdex::string strHostAddr = GetHostAddrFromUrl(strUrl); 
    if(strHostAddr.empty())
        return str_ret;

	int iLen = strHostAddr.length();
    stdex::string str_addr(iLen+1,0);
	char* strAddr = (char*)str_addr.c_str();  
	int iCount = 0;  
	int iFlag = 0;  //��ʶ�Ƿ���ip��ַ��ʽ�ģ��Ƿ��Ǵ����֣�
	for(int i=0; i<iLen+1; i++) {  
		if(strHostAddr[i] == ':') {  
			break;  
		}  

		strAddr[i] = strHostAddr[i];  
		if(strHostAddr[i] == '.') {  
			iCount++;  
			continue;  
		}  
		if(iFlag == 1) {  
			continue;  
		}  

		if((strHostAddr[i] >= '0') && (strHostAddr[i] <= '9')) {  
			iFlag = 0;  
		} else {  //ֻҪ�м���һ���ַ��������֣����ж��϶�����ip��ַ��ʽ��
			iFlag = 1;  
		}  
	}  

	if(str_addr.length() <= 1) {
		return str_ret;  
	}  

	//�ж��Ƿ�Ϊ���ʮ����IP��ַ������ͨ��������ַ��ȡIP��ַ  
	if((iCount == 3) && (iFlag == 0)) 
	{  
		return str_addr;  
	} 
	else 
	{  
		struct hostent *he = gethostbyname((const char*)str_addr.c_str());  
		if (he == NULL) 
		{  
			return str_ret;  
		}
		else 
		{  
			struct in_addr** addr_list = (struct in_addr **)he->h_addr_list;            
			for(int i = 0; addr_list[i] != NULL; i++) 
			{
                str_ret = inet_ntoa(*addr_list[i]);  
				return 	str_ret;
            } 
			return str_ret;  
		}  
	}  
}  

/*��HTTP����URL�л�ȡ������ַ����ַ���ߵ��ʮ����IP��ַ  
 * �ж��Ƿ���http://��https://��ͷ,����ǣ��������ÿ�ͷ
 * ֮����/��Ϊ�ָ�������ȡ��һ���ִ�����
 */
stdex::string HttpReq::GetHostAddrFromUrl(const char* strUrl)  
{ 
    stdex::string str_ret="";
    if(strUrl == NULL)
        return str_ret;

	char url[URLSIZE] = {0};  
	strcpy(url, strUrl);  

	char* strAddr = strstr(url, "http://");//�ж���û��http://  
	if(strAddr == NULL) {  
		strAddr = strstr(url, "https://");//�ж���û��https://  
		if(strAddr != NULL) {  
			strAddr += 8;  
		}  
	} else {  
		strAddr += 7;  
	}  

	if(strAddr == NULL) {  
		strAddr = url;  
	}  

	int iLen = strlen(strAddr);  
    stdex::string str_host_addr(iLen+1,0);
	char* strHostAddr = (char*)str_host_addr.c_str();  
	const char *psp = "/:#?!";		//2019��3��27�� WJM 
	for(int i=0; i<iLen+1; i++) {  
		//if(strchr(psp,strAddr[i])!=NULL) {  
		if(strAddr[i] == '/') {
			break;  
		} else {  
			strHostAddr[i] = strAddr[i];  
		}  
	}  
	return str_host_addr;  
}  

}
