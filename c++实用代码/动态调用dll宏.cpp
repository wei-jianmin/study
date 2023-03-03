#define LoadDll(DllName) \
	HINSTANCE hdll; \
	hdll=LoadLibrary(_T(#DllName)); \
	DWORD errNo=GetLastError(); \
	if(NULL==hdll) \
	{ \
		CString str; \
		str.Format(_T("dll加载失败,错误代号%d"),errNo); \
		AfxMessageBox(str); \
		return ; \
	}
#define LoadFunc2(FuncName,...) \
	lp##FuncName FuncName=(lp##FuncName)GetProcAddress(hdll,#FuncName); \
	errNo=GetLastError(); \
	if(FuncName == NULL) \
	{ \
		
		CString str,str2; \
		str.Format(_T("%s函数调用失败"),_T(#FuncName)); \
		str2.Format(_T(",错误代号%d;"),errNo); \
		str+=str2; \
		AfxMessageBox(str); \
		return ; \
	}
#define CallFunc(FuncName,...) \
	lp##FuncName FuncName=(lp##FuncName)GetProcAddress(hdll,#FuncName); \
	errNo=GetLastError(); \
	if(FuncName == NULL) \
	{ \
		CString str,str2; \
		str.Format(_T("%s函数调用失败"),_T(#FuncName)); \
		str2.Format(_T(",错误代号%d;"),errNo); \
		str+=str2; \
		AfxMessageBox(str); \
		return ; \
	} \
	FuncName(__VA_ARGS__);

int main()
{
	LoadDll(mydll.dll)
	CallFunc(Version)
	CallFunc(LoacteSite,_T("hao123.com"),-1)
	return 0;
}