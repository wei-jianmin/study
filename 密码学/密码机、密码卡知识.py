�Σ� gmt 0018

����
    �豸��Կ
        �洢���豸�ڲ��������豸����ķǶԳ���Կ��, ����ǩ����Կ�Ժͼ�����Կ�ԡ�
    �û���Կ
        �洢���豸�ڲ�������Ӧ����������ķǶԳ���Կ, ����ǩ����Կ�Ժͼ�����Կ�ԡ�
    ��Կ������Կ
        ����Կ���м��ܱ�������Կ��
    �Ự��Կ 
        ���ڲ�λ���Կ�ṹ�е���Ͳ�, ����һ�λỰ��ʹ�õ���Կ��
    ˽Կ���ʿ�����
        ������֤˽Կʹ��Ȩ�޵Ŀ����֡�

�豸��Կ���û���Կ
    �豸��Կֻ�����豸��ʼ��ʱ���ɻ�װ, �û���Կͨ�������豸���������ɻ�װ
    �豸��Կ���û���Կ�������Կ�洢��, �����Ŵ� �� ��ʼ����, 
    ÿ�������Ŷ�Ӧһ��ǩ����Կ�Ժ�һ��������Կ�ԡ� 
    ����, ������Ϊ �� ��ʾ�豸��Կ�� ������ �� ��ʼ��ʾ�û���Կ��

        -----------------------------------------
        ��Կ��������      ��Կ          ˽ Կ
        -----------------------------------------
        0x00            �豸ǩ����Կ �豸ǩ��˽Կ
                        �豸���ܹ�Կ �豸����˽Կ
        -----------------------------------------                
        0x01            �û�ǩ����Կ �û�ǩ��˽Կ
                        �û����ܹ�Կ �û�����˽Կ
        -----------------------------------------        
            
��Կ������Կ
    ��Կ������Կͨ�������豸���������ɻ�װ, ��Կ����Ϊ ������ λ, 
    �������Կ�洢��, ʹ�������Ŵ� �� ��ʼ
    
�Ự��Կ
    �Ự��Կʹ���豸�ӿں������ɻ���, �Ự��Կʹ�þ������

��ȫҪ��
    ���κ�ʱ�䡢 �κ�����£� ����Կ�����Կ��������������ʽ�����������豸�⣻
    �����豸�ڲ��洢����ԿӦ�߱�Ȩ�޿��ƻ��ƣ� ��ֹ�Ƿ�ʹ�ú͵�����
    �����豸Ӧ���г�ʼ�;�������״̬��
    δ��װ�豸��Կ�������豸Ӧ���ڳ�ʼ״̬�� �Ѱ�װ�豸��Կ�������豸Ӧ���ھ���״̬��
    �ڳ�ʼ״̬�£� ���ɶ�ȡ�豸��Ϣ�� �豸��Կ�����ɻ�ָ������⣬ 
    ����ִ���κβ����� ���ɻ�ָ��豸��Կ�� �����豸���ھ���״̬��
    �ھ���״̬�£� ���豸��Կ�����ɻ�ָ������⣬ Ӧ��ִ���κβ�����
    �ھ���״̬�½��е���Կ������ �豸����ԱӦ���������豸����֤��
    �����豸�ڲ��洢��˽Կ��ʹ��Ȩ������Ӧ���豸����Ա��ɣ� 
    �ɲ��ÿ����ַ�ʽ�� �����ֱ��볤��Ӧ�����ڣ� �ַ��� ͬʱ����������ӦΪ�ַ������ֵĻ���塣
    
�ӿں���
    �豸�����ຯ��
        ���豸 
            int SDF_OpenDevice(void�� �� phDeviceHandle) ;
        �ر��豸    
            int SDF_CloSeDevice(void�� hDeviceHandle) ;
        �����Ự
            int SDF_OpenSeSSion(void�� hDeviceHandle, void�� ��phSessionHandle) ;
        �رջỰ
            int SDF_CloSeSeSSion(void�� hSessionHandle) ;       
        ��ȡ�豸��Ϣ
            int SDF_GetDeviceinFo (void�� hSessionHandle, DEViceinfO ��pStDeviceinfo) ;
        ���������
            int SDF_GenerateRanDom (  void�� hSessionHandle,
                                      unsigned int uiLength,
                                      unSigneDchar ��pucRanDom) ;
        ��ȡ˽Կʹ��Ȩ��
            int SDF_GetPrivateKeyAcceSSRight (  void�� hSessionHandle,
                                                unsigned int uiKeyindex,
                                                unSignedchar �� pucPaSSword,
                                                unsigned int uiPwDLength) ;
        �ͷ�˽Կʹ��Ȩ��
            int SDF_ReleaSePrivateKeyAcceSSRight ( void�� hSessionHandle,
                                                    unsigned int uiKeyinDex) ;
    ��Կ�����ຯ��
        ���� RSA ǩ����Կ 
            int SDF_ExportSignPublicKey_RSA(  void��hSessionHandle,
                                                unsigned int uiKeyinDex,
                                                RSAreFPublicKey ��pucPublicKey) ;
        ���� RSA ���ܹ�Կ 
            int SDF_ExportEncPublicKey_RSA(   void��hSessionHandle,
                                                unsigned int uiKeyinDex,
                                                RSAreFPublicKey ��pucPublicKey) ;
        ���� RSA ��Կ�Բ����
            int SDF_GenerateKeyPair_RSA(    void��hSessionHandle,
                                            unsigned int uiKeyBitS,
                                            RSAreFPublicKey ��pucPublicKey,
                                            RSAreFPrivateKey ��pucPrivateKey) ;
        ���ɻỰ��Կ�����ڲ� RSA ��Կ������� 
            int SDF_GenerateKeyWithiPK_RSA (    void�� hSessionHandle,
                                                unsigned int uiiPKinDex,
                                                unsigned int uiKeyBitS,
                                                unSigneDchar ��pucKey,
                                                unsigned int ��puiKeyLength,
                                                void�� ��phKeyHanDle) ;
        ���ɻỰ��Կ�����ⲿ RSA ��Կ������� 
            int SDF_GenerateKeyWithEPK_RSA (    void�� hSessionHandle,
                                                unsigned int uiKeyBitS,
                                                RSAreFPublicKey ��pucPublicKey,
                                                unSigneDchar ��pucKey,
                                                unsigned int ��puiKeyLength,
                                                void�� ��phKeyHanDle) ;
        ����Ự��Կ�����ڲ� RSA ˽Կ���� 
            int SDF_importKeyWithiSK_RSA (      void�� hSessionHandle,
                                                unsigned int uiiSKinDex,
                                                unsigned char �� pucKey,
                                                unsigned int puiKeyLength,
                                                void�� �� phKeyHanDle) ;
        ���� RSA �㷨�������ŷ�ת�� 
            int SDF_ExchangeDigitEnvelopeBaSeOnRSA(     void�� hSessionHandle,
                                                        unsigned int uiKeyinDex,
                                                        RSAreFPublicKey �� pucPublicKey,
                                                        unsigned char �� pucDEinput,
                                                        unsigned int uiDELength,
                                                        unsigned char �� pucDEOutput,
                                                        unsigned int �� puiDELength) ;
        ���� ECC ǩ����Կ 
            int SDF_ExportSignPublicKey_ECC(  void�� hSessionHandle,
                                                unsigned int uiKeyinDex,
                                                ECCreFPublicKey �� pucPublicKey) ;
        ���� ECC ���ܹ�Կ 
            nt SDF_ExportEncPublicKey_ECC(void�� hSessionHandle,
                                            unsigned int uiKeyinDex,
                                            ECCreFPublicKey �� pucPublicKey) ;
        ���� ECC ��Կ�Բ����
            int SDF_GenerateKeyPair_ECC(    void�� hSessionHandle,
                                            unsigned int uiAlgID,
                                            unsigned int uiKeyBitS,
                                            ECCreFPublicKey �� pucPublicKey,
                                            ECCreFPrivateKey �� pucPrivateKey) ;
        ���ɻỰ��Կ�����ڲ� ECC ��Կ�������
            int SDF_GenerateKeyWithiPK_ECC (    void�� hSessionHandle,
                                                unsigned int uiiPKinDex,
                                                unsigned int uiKeyBitS,
                                                ECCCipher �� pucKey,
                                                void�� �� phKeyHanDle) ;
        ���ɻỰ��Կ�����ⲿ ECC ��Կ�������
            int SDF_GenerateKeyWithEPK_ECC (    void�� hSessionHandle,
                                                unsigned int uiKeyBitS,
                                                unsigned int uiAlgID,
                                                ECCreFPublicKey �� pucPublicKey,
                                                ECCCipher �� pucKey,
                                                void�� �� phKeyHanDle) ;
        ����Ự��Կ�����ڲ� ECC ˽Կ����
            int SDF_importKeyWithiSK_ECC (      void�� hSessionHandle,
                                                unsigned int uiiSKinDex,
                                                ECCCipher �� pucKey,
                                                void�� �� phKeyHanDle) ;
        ������ԿЭ�̲�������� 
            int SDF_GenerateAgreementDataWithECC (  void�� hSessionHandle,
                                                    unsigned int uiiSKinDex,
                                                    unsigned int uiKeyBitS,
                                                    unSigneDchar ��pucSponSoriD,
                                                    unsigned int uiSponSoriDLength,
                                                    ECCreFPublicKey ��pucSponSorPublicKey,
                                                    ECCreFPublicKey ��pucSponSorTmpPublicKey,
                                                    void�� ��phAgreementHanDle) ;
        ����Ự��Կ 
            int SDF_GenerateKeyWithECC (    void�� hSessionHandle,
                                            unSigneDchar ��pucReSponSeiD,
                                            unsigned int uiReSponSeiDLength,
                                            ECCreFPublicKey ��pucReSponSePublicKey,
                                            ECCreFPublicKey ��pucReSponSeTmpPublicKey,
                                            void�� hAgreementHanDle,
                                            void�� ��phKeyHanDle) ;
        ����Э�����ݲ�����Ự��Կ 
            int SDF_GenerateAgreementDataAnDKeyWithECC (    void�� hSessionHandle,
                                                            unsigned int uiiSKinDex,
                                                            unsigned int uiKeyBitS,
                                                            unSigneDchar ��pucReSponSeiD,
                                                            unsigned int uiReSponSeiDLength,
                                                            unSigneDchar ��pucSponSoriD,
                                                            unsigned int uiSponSoriDLength,
                                                            ECCreFPublicKey ��pucSponSorPublicKey,
                                                            ECCreFPublicKey ��pucSponSorTmpPublicKey,
                                                            ECCreFPublicKey ��pucReSponSePublicKey,
                                                            ECCreFPublicKey ��pucReSponSeTmpPublicKey,
                                                            void�� ��phKeyHanDle) ;
        ���� ECC �㷨�������ŷ�ת��
            int SDF_ExchangeDigitEnvelopeBaSeOnECC(   void�� hSessionHandle,
                                                        unsigned int uiKeyinDex,
                                                        unsigned int uiAlgID,
                                                        ECCreFPublicKey �� pucPublicKey,
                                                        ECCCipher �� pucEncDatain,
                                                        ECCCipher �� pucEncDataOut) ;
        ���ɻỰ��Կ������Կ������Կ������� 
            int SDF_GenerateKeyWithKEK (    void�� hSessionHandle,
                                            unsigned int uiKeyBitS,
                                            unsigned int uiAlgID,
                                            unsigned int uiKEKinDex,
                                            unSigneDchar �� pucKey,
                                            unsigned int �� puiKeyLength,
                                            void�� �� phKeyHanDle) ;
        ����Ự��Կ������Կ������Կ���� 
            int SDF_importKeyWithKEK (  void�� hSessionHandle,
                                        unsigned int uiAlgID,
                                        unsigned int uiKEKinDex,
                                        unSigneDchar �� pucKey,
                                        unsigned int puiKeyLength,
                                        void�� �� phKeyHanDle) ;
        �������ĻỰ��Կ 
            int SDF_importKey (     void�� hSessionHandle,
                                    unSigneDchar �� pucKey,
                                    unsigned int uiKeyLength,
                                    void�� �� phKeyHanDle) ;
        ���ٻỰ��Կ 
            int SDF_DeStroyKey (void�� hSessionHandle, void�� hKeyHanDle) ;
    �ǶԳ��㷨�����ຯ��
        �ⲿ��Կ RSA ���� 
            int SDF_ExternalPublicKeyOperation_RSA(     void�� hSessionHandle,
                                                        RSAreFPublicKey �� pucPublicKey,
                                                        unSigneDchar �� pucDatainput,
                                                        unsigned int uiinputLength,
                                                        unSigneDchar �� pucDataOutput,
                                                        unsigned int �� puiOutputLength) ;
        �ⲿ˽Կ RSA ���� 
            int SDF_ExternalPrivateKeyOperation_RSA(    void�� hSessionHandle,
                                                        RSAreFPrivateKey �� pucPrivateKey,
                                                        unSigneDchar �� pucDatainput,
                                                        unsigned int uiinputLength,
                                                        unSigneDchar �� pucDataOutput,
                                                        unsigned int �� puiOutputLength) ;        
        �ڲ���Կ RSA ���� 
            int SDF_internalPublicKeyOperation_RSA(     void�� hSessionHandle,
                                                        unsigned int uiKeyinDex,
                                                        unSigneDchar ��pucDatainput,
                                                        unsigned int uiinputLength,
                                                        unSigneDchar ��pucDataOutput,
                                                        unsigned int ��puiOutputLength) ;        
        �ڲ�˽Կ RSA ���� 
            int SDF_internalPrivateKeyOperation_RSA(    void�� hSessionHandle,
                                                        unsigned int uiKeyinDex,
                                                        unSigneDchar ��pucDatainput,
                                                        unsigned int uiinputLength,
                                                        unSigneDchar ��pucDataOutput,
                                                        unsigned int ��puiOutputLength) ;        
        �ⲿ��Կ ECC ǩ�� 
            int SDF_ExternalSign_ECC(   void�� hSessionHandle,
                                        unsigned int uiAlgID,
                                        ECCreFPrivateKey ��pucPrivateKey,
                                        unSigneDchar ��pucData,
                                        unsigned int uiDataLength,
                                        ECCSignature ��pucSignature) ;        
        �ⲿ��Կ ECC ��֤ 
            int SDF_ExternalVeriFy_ECC(     void�� hSessionHandle,
                                            unsigned int uiAlgID,
                                            ECCreFPublicKey ��pucPublicKey,
                                            unSigneDchar ��pucDatainput,
                                            unsigned int uiinputLength,
                                            ECCSignature ��pucSignature) ;        
        �ڲ���Կ ECC ǩ�� 
            int SDF_internalSign_ECC(   void�� hSessionHandle,
                                        unsigned int uiiSKinDex,
                                        unSigneDchar ��pucData,
                                        unsigned int uiDataLength,
                                        ECCSignature ��pucSignature) ;        
        �ڲ���Կ ECC ��֤ 
            int SDF_internalVeriFy_ECC(     void�� hSessionHandle,
                                            unsigned int uiiSKinDex,
                                            unSigneDchar ��pucData,
                                            unsigned int uiDataLength,
                                            ECCSignature ��pucSignature) ;        
        �ⲿ��Կ ECC ��Կ���� 
            int SDF_ExternalEncrypt_ECC(    void�� hSessionHandle,
                                            unsigned int uiAlgID,
                                            ECCreFPublicKey �� pucPublicKey,
                                            unsigned char �� pucData,
                                            unsigned int uiDataLength,
                                            ECCCipher �� pucEncData) ;        
        �ⲿ��Կ ECC ˽Կ����
            int SDF_ExternalDecrypt_ECC(    void�� hSessionHandle,
                                            unsigned int uiAlgID,
                                            ECCreFPrivateKey �� pucPrivateKey,
                                            ECCCipher �� pucEncData,
                                            unsigned char �� pucData,
                                            unsigned int �� puiDataLength) ;        
    �Գ��㷨�����ຯ�� 
        �ԳƼ��� 
            int SDF_Encrypt(   void�� hSessionHandle,
                                void�� hKeyHandle,
                                unsigned int uiAlgID,
                                unsigned char �� pucIV,
                                unsigned char �� pucData,
                                unsigned int uiDataLength,
                                unsigned char �� pucEncData,
                                unsigned int �� puiEncDataLength) ;        
        �Գƽ��� 
            int SDF_Decrypt (  void�� hSessionHandle,
                                void�� hKeyHandle,
                                unsigned int uiAlgID,
                                unsigned char �� pucIV,
                                unsigned char �� pucEncData,
                                unsigned int uiEncDataLength,
                                unsigned char �� pucData,
                                unsigned int �� puiDataLength) ;        
        ���� ��AC
            int SDF_Calculate��AC( void�� hSessionHandle,
                                    void�� hKeyHandle,
                                    unsigned int uiAlgID,
                                    unSigneDchar ��pucIV,
                                    unSigneDchar ��pucData,
                                    unsigned int uiDataLength,
                                    unSigneDchar ��puc��AC,
                                    unsigned int ��pui��ACLength) ;
    �Ӵ������ຯ�� 
        �Ӵ������ʼ�� 
            int SDF_HaShinit( void�� hSessionHandle,
                                unsigned int uiAlgiD
                                ECCreFPublicKey ��pucPublicKey,
                                unSigneDchar ��puciD,
                                unsigned int uiiDLength) ;        
        ����Ӵ����� 
            int SDF_HaShUpDate(  void�� hSessionHandle,
                                    unSigneDchar ��pucData,
                                    unsigned int uiDataLength) ;        
        �Ӵ�������� 
            int SDF_HaShFinal(  void�� hSessionHandle,
                                unSigneDchar ��pucHaSh,
                                unsigned int ��puiHaShLength) ;        
    �û��ļ������ຯ�� 
        �����ļ�
            int SDF_CreateFile( void�� hSessionHandle,
                                unsigned char �� pucFilename,
                                unsigned int uinameLen,
                                unsigned int uiFileSize) ;
        ��ȡ�ļ�
            int SDF_ReaDFile(   void�� hSessionHandle,
                                unsigned char �� pucFilename,
                                unsigned int uinameLen,
                                unsigned int uiOFFSet,
                                unsigned int �� puiFileLength,
                                unsigned char �� pucBuFFer) ;        
        д�ļ� 
            int SDF_WriteFile(  void�� hSessionHandle,
                                unsigned char �� pucFilename,
                                unsigned int uinameLen,
                                unsigned int uiOFFSet,
                                unsigned int uiFileLength,
                                unsigned char �� pucBuFFer) ;        
        ɾ���ļ�
            int SDF_DeleteFile( void�� hSessionHandle,
                                unSigneDchar ��pucFilename,
                                unsigned int uinameLen) ;    