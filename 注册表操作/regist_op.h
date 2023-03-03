/* 文件说明：
 * 本代码中的函数操作及注释中，涉及三个术语：注册表项、注册表键、键值
 * 注册表项指的是注册表编辑器中左侧的“文件夹”部分
 * 注册表键指的是注册表编辑器中右侧的“文件”部分
 * 注册表(键)值指的是注册表编辑器中是右侧“文件”的数据内容
 */
//-------------------------------------------------------------------------//
/* 函数说明：
 * 本函数只支持对DWORD类型或字符串类型键值的读取
 * 无论注册表中原来的值是什么类型，函数都转化为字符串类型进行返回
 * 返回的字符串末尾不会主动添加换行符
 * 函数的调用者无需关心内存释放问题
 * 如果函数返回值为空，可通过getLastErrorMsg或getLastError查询错误原因
 */
const char* regRead(const char* KeyAddr, const char* KeyName);
/* 函数说明：
 * KeyAddr参数一定不能为空
 * 如果KeyName为空，则不再管KeyValue，只参照KeyAddr对注册表项进行操作
   如果del为非0，说明进行删除注册表项操作，否则进行添加注册表项操作（默认）
 * 如果KeyName不为空，则说明是对键进行操作
   如果KeyValue为空，则将键值设为空字符串
   如果del为非0，说明进行删除键操作，否则进行修改/添加注册表键值操作（默认）
 * 注册表主键可以为全写形式，如HKEY_CLASSES_ROOT，也可以使用简写形式，如HKCR
 * 注册表路径中的路径分隔符可以为/，也可以为\\，内部统一处理为\\形式
 */
unsigned long regWrite(const char* KeyAddr, const char* KeyName, const char* KeyValue, const int del=0);
/* 函数说明：
 * 返回函数执行的错误代码
 */
unsigned long getLastError();
/* 函数说明：
 * 返回函数执行的出错原因描述
 * 字符串末尾自动带有换行符
 */
const char* getLastErrorMsg();

/*  使用举例(使用动态库)：
	#define DLLADDR ".\\dffs.dll"
	#define msg(s) MessageBoxA(NULL,s,"提示",MB_OK)

	//函数指针定义
	typedef const char* (* pfun)(const char* KeyAddr, const char* KeyName);
	typedef unsigned long (* pfun2)(const char* KeyAddr, const char* KeyName, const char* KeyValue, const int del);
	typedef const char* (* pfun3)();

	//加载动态库，导出库函数
	HINSTANCE hlib = LoadLibrary(DLLADDR);
	if(!hlib)
	{
		DWORD dw=GetLastError();
		msg("加载库失败");
		return -1;
	}
	pfun reg_r = (pfun)GetProcAddress(hlib,"regRead");
	if(!reg_r)
	{
		msg("获取导出函数失败");
		return -1;
	}
	pfun2 reg_w = (pfun2)GetProcAddress(hlib,"regWrite");
	if(!reg_w)
	{
		msg("获取导出函数失败");
		return -1;
	}
	pfun3 get_err = (pfun3)GetProcAddress(hlib,"getLastErrorMsg");
	if(!get_err)
	{
		msg("获取导出函数失败");
		return -1;
	}

	//调用库函数，修改注册表
	unsigned long  ret2;
	//删除注册表项
	ret2=reg_w("HKCR\\Test","","",1);
	msg(get_err());
	//添加注册表项
	ret2=reg_w("HKCR\\Test","","",0);
	msg(get_err());
	//添加注册表键,自动添加为DWORD类型
	ret2=reg_w("HKCR\\Test","val","123",0);
	msg(get_err());
	//修改注册表键
	ret2=reg_w("HKCR\\Test","val","456",0);
	msg(get_err());
	//添加注册表键，自动添加为字符串类型
	ret2=reg_w("HKCR\\Test","str","ab12",0);
	msg(get_err());
	//修改注册表键
	ret2=reg_w("HKCR\\Test","str","12ab",0);
	msg(get_err());

	//调用库函数，读取注册表键值
	const char* ret;
	ret=reg_r("HKCR\\Test","val");
	if(ret!=NULL)
		msg(ret);
	msg(get_err());
	ret=reg_r("HKCR\\Test","str");
	if(ret!=NULL)
		msg(ret);
	msg(get_err());
	
	//调用库函数，修改注册表
	//删除注册表键
	ret2=reg_w("HKCR\\Test","val","",1);
	msg(get_err());
	//删除注册表项
	ret2=reg_w("HKCR\\Test","","",1);
	msg(get_err());

	//释放库
	FreeLibrary(hlib);
*/

/*  使用举例(使用静态库):
    将头文件添加到项目中，并在项目中添加如下语句：
    #include ".\\regist_op.h"
    #pragma comment(lib,".\\dffs.lib")
    然后将dll文件放在项目中
    然后即可直接使用注册表操作函数了，如：
    regWrite("HKCR/test123","","",0);
    printf("%s",getLastErrorMsg());
*/




