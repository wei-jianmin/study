����openssl 1.1.1 ��¼
    �Σ�https://blog.csdn.net/zhounixing/article/details/105519536
    �Σ�https://blog.csdn.net/fksec/article/details/52667055
    �Σ�https://blog.csdn.net/lixiang987654321/article/details/81154613
    �Σ�https://blog.csdn.net/u012332816/article/details/81742516
    1. ���ذ�װperl��nasm��dmake
    2. ����perlִ��configure������MakeFile�ļ�
       ���ɶ�̬openssl��
           perl configure VC-WIN64A shared no-asm
       ���ɾ�̬openssl��
           perl Configure VC-WIN32 no-asm no-shared 
                          --prefix="C:/openssl_lib/win32-release" 
                          --openssldir="C:/openssl_lib/win32-release/ssl" 
       ����Debug��Ķ�̬��
           Perl Configure -DDEBUG -D_DEBUG -DOPENSSL_DEBUG_KEYGEN -DSSL_DEBUG 
                          -DALG_DEBUG -DCIPHER_DEBUG  -DTLS_DEBUG  -DKSSL_DEBUG 
                          debug-VC-WIN32 no-asm --prefix=C:\MyProgramFiles\OpenSSLv1.0.2h 
                          --openssldir=C:\MyProgramFiles\OpenSSLv1.0.2h\SSL
    3. ִ��nmake����MakeFile���������Ŀ
    4. ִ��namke test�����Ա�����
    5. ִ��namek install����ɰ�װ
ʹ��openssl��̬��
    vs������ʹ��openssl��̬��
        ����ʱ����Щ����δ���壬
        ��Щ���������� Crypt32.lib Ws2_32.lib ����������
    ��MinGW��ʹ��openssl��̬��
        �ᱨ������ error: undefined reference to `_chkstk'
        ��Ϊ������openssl��̬�����������vs�ı��빤�����ɵ�
        ��__chkstk�� Windows �ض����ܣ���ȷ����ջ�ռ�������ʱ����ӳ��
        �������� WindowsĿ��� LLVM ����������
        ����޷���MinGW����vs���ɵľ�̬��
        ���������ֱ������ĺ�������������Ҳ��һ����
        ��Ҳ������lib��һ���������ֱ�����֮�䲻ͨ��
        ������ֱ�ӵĽ���취���ǲ���MinGW����vs���ɵľ�̬��