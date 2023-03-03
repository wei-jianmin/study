/* �ļ�˵����
 * �������еĺ���������ע���У��漰�������ע����ע��������ֵ
 * ע�����ָ����ע���༭�������ġ��ļ��С�����
 * ע����ָ����ע���༭�����Ҳ�ġ��ļ�������
 * ע���(��)ֵָ����ע���༭�������Ҳࡰ�ļ�������������
 */
//-------------------------------------------------------------------------//
/* ����˵����
 * ������ֻ֧�ֶ�DWORD���ͻ��ַ������ͼ�ֵ�Ķ�ȡ
 * ����ע�����ԭ����ֵ��ʲô���ͣ�������ת��Ϊ�ַ������ͽ��з���
 * ���ص��ַ���ĩβ����������ӻ��з�
 * �����ĵ�������������ڴ��ͷ�����
 * �����������ֵΪ�գ���ͨ��getLastErrorMsg��getLastError��ѯ����ԭ��
 */
const char* regRead(const char* KeyAddr, const char* KeyName);
/* ����˵����
 * KeyAddr����һ������Ϊ��
 * ���KeyNameΪ�գ����ٹ�KeyValue��ֻ����KeyAddr��ע�������в���
   ���delΪ��0��˵������ɾ��ע��������������������ע����������Ĭ�ϣ�
 * ���KeyName��Ϊ�գ���˵���ǶԼ����в���
   ���KeyValueΪ�գ��򽫼�ֵ��Ϊ���ַ���
   ���delΪ��0��˵������ɾ������������������޸�/���ע����ֵ������Ĭ�ϣ�
 * ע�����������Ϊȫд��ʽ����HKEY_CLASSES_ROOT��Ҳ����ʹ�ü�д��ʽ����HKCR
 * ע���·���е�·���ָ�������Ϊ/��Ҳ����Ϊ\\���ڲ�ͳһ����Ϊ\\��ʽ
 */
unsigned long regWrite(const char* KeyAddr, const char* KeyName, const char* KeyValue, const int del=0);
/* ����˵����
 * ���غ���ִ�еĴ������
 */
unsigned long getLastError();
/* ����˵����
 * ���غ���ִ�еĳ���ԭ������
 * �ַ���ĩβ�Զ����л��з�
 */
const char* getLastErrorMsg();

/*  ʹ�þ���(ʹ�ö�̬��)��
	#define DLLADDR ".\\dffs.dll"
	#define msg(s) MessageBoxA(NULL,s,"��ʾ",MB_OK)

	//����ָ�붨��
	typedef const char* (* pfun)(const char* KeyAddr, const char* KeyName);
	typedef unsigned long (* pfun2)(const char* KeyAddr, const char* KeyName, const char* KeyValue, const int del);
	typedef const char* (* pfun3)();

	//���ض�̬�⣬�����⺯��
	HINSTANCE hlib = LoadLibrary(DLLADDR);
	if(!hlib)
	{
		DWORD dw=GetLastError();
		msg("���ؿ�ʧ��");
		return -1;
	}
	pfun reg_r = (pfun)GetProcAddress(hlib,"regRead");
	if(!reg_r)
	{
		msg("��ȡ��������ʧ��");
		return -1;
	}
	pfun2 reg_w = (pfun2)GetProcAddress(hlib,"regWrite");
	if(!reg_w)
	{
		msg("��ȡ��������ʧ��");
		return -1;
	}
	pfun3 get_err = (pfun3)GetProcAddress(hlib,"getLastErrorMsg");
	if(!get_err)
	{
		msg("��ȡ��������ʧ��");
		return -1;
	}

	//���ÿ⺯�����޸�ע���
	unsigned long  ret2;
	//ɾ��ע�����
	ret2=reg_w("HKCR\\Test","","",1);
	msg(get_err());
	//���ע�����
	ret2=reg_w("HKCR\\Test","","",0);
	msg(get_err());
	//���ע����,�Զ����ΪDWORD����
	ret2=reg_w("HKCR\\Test","val","123",0);
	msg(get_err());
	//�޸�ע����
	ret2=reg_w("HKCR\\Test","val","456",0);
	msg(get_err());
	//���ע�������Զ����Ϊ�ַ�������
	ret2=reg_w("HKCR\\Test","str","ab12",0);
	msg(get_err());
	//�޸�ע����
	ret2=reg_w("HKCR\\Test","str","12ab",0);
	msg(get_err());

	//���ÿ⺯������ȡע����ֵ
	const char* ret;
	ret=reg_r("HKCR\\Test","val");
	if(ret!=NULL)
		msg(ret);
	msg(get_err());
	ret=reg_r("HKCR\\Test","str");
	if(ret!=NULL)
		msg(ret);
	msg(get_err());
	
	//���ÿ⺯�����޸�ע���
	//ɾ��ע����
	ret2=reg_w("HKCR\\Test","val","",1);
	msg(get_err());
	//ɾ��ע�����
	ret2=reg_w("HKCR\\Test","","",1);
	msg(get_err());

	//�ͷſ�
	FreeLibrary(hlib);
*/

/*  ʹ�þ���(ʹ�þ�̬��):
    ��ͷ�ļ���ӵ���Ŀ�У�������Ŀ�����������䣺
    #include ".\\regist_op.h"
    #pragma comment(lib,".\\dffs.lib")
    Ȼ��dll�ļ�������Ŀ��
    Ȼ�󼴿�ֱ��ʹ��ע�����������ˣ��磺
    regWrite("HKCR/test123","","",0);
    printf("%s",getLastErrorMsg());
*/




