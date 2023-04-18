参： gmt 0018

术语
    设备密钥
        存储在设备内部的用于设备管理的非对称密钥对, 包含签名密钥对和加密密钥对。
    用户密钥
        存储在设备内部的用于应用密码运算的非对称密钥, 包含签名密钥对和加密密钥对。
    密钥加密密钥
        对密钥进行加密保护的密钥。
    会话密钥 
        处于层次化密钥结构中的最低层, 仅在一次会话中使用的密钥。
    私钥访问控制码
        用于验证私钥使用权限的口令字。

设备密钥与用户密钥
    设备密钥只能在设备初始化时生成或安装, 用户密钥通过密码设备管理工具生成或安装
    设备密钥和用户密钥存放于密钥存储区, 索引号从 ０ 开始检索, 
    每个索引号对应一个签名密钥对和一个加密密钥对。 
    其中, 索引号为 ０ 表示设备密钥。 索引号 １ 开始表示用户密钥。

        -----------------------------------------
        密钥对索引号      公钥          私 钥
        -----------------------------------------
        0x00            设备签名公钥 设备签名私钥
                        设备加密公钥 设备加密私钥
        -----------------------------------------                
        0x01            用户签名公钥 用户签名私钥
                        用户加密公钥 用户加密私钥
        -----------------------------------------        
            
密钥加密密钥
    密钥加密密钥通过密码设备管理工具生成或安装, 密钥长度为 １２８ 位, 
    存放于密钥存储区, 使用索引号从 １ 开始
    
会话密钥
    会话密钥使用设备接口函数生成或导入, 会话密钥使用句柄检索

安全要求
    在任何时间、 任何情况下， 除公钥外的密钥均不能以明文形式出现在密码设备外；
    密码设备内部存储的密钥应具备权限控制机制， 防止非法使用和导出。
    密码设备应具有初始和就绪两个状态；
    未安装设备密钥的密码设备应处于初始状态， 已安装设备密钥的密码设备应处于就绪状态；
    在初始状态下， 除可读取设备信息、 设备密钥的生成或恢复操作外， 
    不能执行任何操作， 生成或恢复设备密钥后， 密码设备处于就绪状态；
    在就绪状态下， 除设备密钥的生成或恢复操作外， 应能执行任何操作；
    在就绪状态下进行的密钥操作， 设备操作员应经过密码设备的认证。
    密码设备内部存储的私钥的使用权限设置应由设备管理员完成， 
    可采用口令字方式， 口令字编码长度应不低于８ 字符， 同时口令字内容应为字符与数字的混合体。
    
接口函数
    设备管理类函数
        打开设备 
            int SDF_OpenDevice(void  phDeviceHandle) ;
        关闭设备    
            int SDF_CloSeDevice(void hDeviceHandle) ;
        创建会话
            int SDF_OpenSeSSion(void hDeviceHandle, void phSessionHandle) ;
        关闭会话
            int SDF_CloSeSeSSion(void hSessionHandle) ;       
        获取设备信息
            int SDF_GetDeviceinFo (void hSessionHandle, DEViceinfO pStDeviceinfo) ;
        产生随机数
            int SDF_GenerateRanDom (  void hSessionHandle,
                                      unsigned int uiLength,
                                      unSigneDchar pucRanDom) ;
        获取私钥使用权限
            int SDF_GetPrivateKeyAcceSSRight (  void hSessionHandle,
                                                unsigned int uiKeyindex,
                                                unSignedchar  pucPaSSword,
                                                unsigned int uiPwDLength) ;
        释放私钥使用权限
            int SDF_ReleaSePrivateKeyAcceSSRight ( void hSessionHandle,
                                                    unsigned int uiKeyinDex) ;
    密钥管理类函数
        导出 RSA 签名公钥 
            int SDF_ExportSignPublicKey_RSA(  voidhSessionHandle,
                                                unsigned int uiKeyinDex,
                                                RSAreFPublicKey pucPublicKey) ;
        导出 RSA 加密公钥 
            int SDF_ExportEncPublicKey_RSA(   voidhSessionHandle,
                                                unsigned int uiKeyinDex,
                                                RSAreFPublicKey pucPublicKey) ;
        产生 RSA 密钥对并输出
            int SDF_GenerateKeyPair_RSA(    voidhSessionHandle,
                                            unsigned int uiKeyBitS,
                                            RSAreFPublicKey pucPublicKey,
                                            RSAreFPrivateKey pucPrivateKey) ;
        生成会话密钥并用内部 RSA 公钥加密输出 
            int SDF_GenerateKeyWithiPK_RSA (    void hSessionHandle,
                                                unsigned int uiiPKinDex,
                                                unsigned int uiKeyBitS,
                                                unSigneDchar pucKey,
                                                unsigned int puiKeyLength,
                                                void phKeyHanDle) ;
        生成会话密钥并用外部 RSA 公钥加密输出 
            int SDF_GenerateKeyWithEPK_RSA (    void hSessionHandle,
                                                unsigned int uiKeyBitS,
                                                RSAreFPublicKey pucPublicKey,
                                                unSigneDchar pucKey,
                                                unsigned int puiKeyLength,
                                                void phKeyHanDle) ;
        导入会话密钥并用内部 RSA 私钥解密 
            int SDF_importKeyWithiSK_RSA (      void hSessionHandle,
                                                unsigned int uiiSKinDex,
                                                unsigned char  pucKey,
                                                unsigned int puiKeyLength,
                                                void  phKeyHanDle) ;
        基于 RSA 算法的数字信封转换 
            int SDF_ExchangeDigitEnvelopeBaSeOnRSA(     void hSessionHandle,
                                                        unsigned int uiKeyinDex,
                                                        RSAreFPublicKey  pucPublicKey,
                                                        unsigned char  pucDEinput,
                                                        unsigned int uiDELength,
                                                        unsigned char  pucDEOutput,
                                                        unsigned int  puiDELength) ;
        导出 ECC 签名公钥 
            int SDF_ExportSignPublicKey_ECC(  void hSessionHandle,
                                                unsigned int uiKeyinDex,
                                                ECCreFPublicKey  pucPublicKey) ;
        导出 ECC 加密公钥 
            nt SDF_ExportEncPublicKey_ECC(void hSessionHandle,
                                            unsigned int uiKeyinDex,
                                            ECCreFPublicKey  pucPublicKey) ;
        产生 ECC 密钥对并输出
            int SDF_GenerateKeyPair_ECC(    void hSessionHandle,
                                            unsigned int uiAlgID,
                                            unsigned int uiKeyBitS,
                                            ECCreFPublicKey  pucPublicKey,
                                            ECCreFPrivateKey  pucPrivateKey) ;
        生成会话密钥并用内部 ECC 公钥加密输出
            int SDF_GenerateKeyWithiPK_ECC (    void hSessionHandle,
                                                unsigned int uiiPKinDex,
                                                unsigned int uiKeyBitS,
                                                ECCCipher  pucKey,
                                                void  phKeyHanDle) ;
        生成会话密钥并用外部 ECC 公钥加密输出
            int SDF_GenerateKeyWithEPK_ECC (    void hSessionHandle,
                                                unsigned int uiKeyBitS,
                                                unsigned int uiAlgID,
                                                ECCreFPublicKey  pucPublicKey,
                                                ECCCipher  pucKey,
                                                void  phKeyHanDle) ;
        导入会话密钥并用内部 ECC 私钥解密
            int SDF_importKeyWithiSK_ECC (      void hSessionHandle,
                                                unsigned int uiiSKinDex,
                                                ECCCipher  pucKey,
                                                void  phKeyHanDle) ;
        生成密钥协商参数并输出 
            int SDF_GenerateAgreementDataWithECC (  void hSessionHandle,
                                                    unsigned int uiiSKinDex,
                                                    unsigned int uiKeyBitS,
                                                    unSigneDchar pucSponSoriD,
                                                    unsigned int uiSponSoriDLength,
                                                    ECCreFPublicKey pucSponSorPublicKey,
                                                    ECCreFPublicKey pucSponSorTmpPublicKey,
                                                    void phAgreementHanDle) ;
        计算会话密钥 
            int SDF_GenerateKeyWithECC (    void hSessionHandle,
                                            unSigneDchar pucReSponSeiD,
                                            unsigned int uiReSponSeiDLength,
                                            ECCreFPublicKey pucReSponSePublicKey,
                                            ECCreFPublicKey pucReSponSeTmpPublicKey,
                                            void hAgreementHanDle,
                                            void phKeyHanDle) ;
        产生协商数据并计算会话密钥 
            int SDF_GenerateAgreementDataAnDKeyWithECC (    void hSessionHandle,
                                                            unsigned int uiiSKinDex,
                                                            unsigned int uiKeyBitS,
                                                            unSigneDchar pucReSponSeiD,
                                                            unsigned int uiReSponSeiDLength,
                                                            unSigneDchar pucSponSoriD,
                                                            unsigned int uiSponSoriDLength,
                                                            ECCreFPublicKey pucSponSorPublicKey,
                                                            ECCreFPublicKey pucSponSorTmpPublicKey,
                                                            ECCreFPublicKey pucReSponSePublicKey,
                                                            ECCreFPublicKey pucReSponSeTmpPublicKey,
                                                            void phKeyHanDle) ;
        基于 ECC 算法的数字信封转换
            int SDF_ExchangeDigitEnvelopeBaSeOnECC(   void hSessionHandle,
                                                        unsigned int uiKeyinDex,
                                                        unsigned int uiAlgID,
                                                        ECCreFPublicKey  pucPublicKey,
                                                        ECCCipher  pucEncDatain,
                                                        ECCCipher  pucEncDataOut) ;
        生成会话密钥并用密钥加密密钥加密输出 
            int SDF_GenerateKeyWithKEK (    void hSessionHandle,
                                            unsigned int uiKeyBitS,
                                            unsigned int uiAlgID,
                                            unsigned int uiKEKinDex,
                                            unSigneDchar  pucKey,
                                            unsigned int  puiKeyLength,
                                            void  phKeyHanDle) ;
        导入会话密钥并用密钥加密密钥解密 
            int SDF_importKeyWithKEK (  void hSessionHandle,
                                        unsigned int uiAlgID,
                                        unsigned int uiKEKinDex,
                                        unSigneDchar  pucKey,
                                        unsigned int puiKeyLength,
                                        void  phKeyHanDle) ;
        导入明文会话密钥 
            int SDF_importKey (     void hSessionHandle,
                                    unSigneDchar  pucKey,
                                    unsigned int uiKeyLength,
                                    void  phKeyHanDle) ;
        销毁会话密钥 
            int SDF_DeStroyKey (void hSessionHandle, void hKeyHanDle) ;
    非对称算法运算类函数
        外部公钥 RSA 运算 
            int SDF_ExternalPublicKeyOperation_RSA(     void hSessionHandle,
                                                        RSAreFPublicKey  pucPublicKey,
                                                        unSigneDchar  pucDatainput,
                                                        unsigned int uiinputLength,
                                                        unSigneDchar  pucDataOutput,
                                                        unsigned int  puiOutputLength) ;
        外部私钥 RSA 运算 
            int SDF_ExternalPrivateKeyOperation_RSA(    void hSessionHandle,
                                                        RSAreFPrivateKey  pucPrivateKey,
                                                        unSigneDchar  pucDatainput,
                                                        unsigned int uiinputLength,
                                                        unSigneDchar  pucDataOutput,
                                                        unsigned int  puiOutputLength) ;        
        内部公钥 RSA 运算 
            int SDF_internalPublicKeyOperation_RSA(     void hSessionHandle,
                                                        unsigned int uiKeyinDex,
                                                        unSigneDchar pucDatainput,
                                                        unsigned int uiinputLength,
                                                        unSigneDchar pucDataOutput,
                                                        unsigned int puiOutputLength) ;        
        内部私钥 RSA 运算 
            int SDF_internalPrivateKeyOperation_RSA(    void hSessionHandle,
                                                        unsigned int uiKeyinDex,
                                                        unSigneDchar pucDatainput,
                                                        unsigned int uiinputLength,
                                                        unSigneDchar pucDataOutput,
                                                        unsigned int puiOutputLength) ;        
        外部密钥 ECC 签名 
            int SDF_ExternalSign_ECC(   void hSessionHandle,
                                        unsigned int uiAlgID,
                                        ECCreFPrivateKey pucPrivateKey,
                                        unSigneDchar pucData,
                                        unsigned int uiDataLength,
                                        ECCSignature pucSignature) ;        
        外部密钥 ECC 验证 
            int SDF_ExternalVeriFy_ECC(     void hSessionHandle,
                                            unsigned int uiAlgID,
                                            ECCreFPublicKey pucPublicKey,
                                            unSigneDchar pucDatainput,
                                            unsigned int uiinputLength,
                                            ECCSignature pucSignature) ;        
        内部密钥 ECC 签名 
            int SDF_internalSign_ECC(   void hSessionHandle,
                                        unsigned int uiiSKinDex,
                                        unSigneDchar pucData,
                                        unsigned int uiDataLength,
                                        ECCSignature pucSignature) ;        
        内部密钥 ECC 验证 
            int SDF_internalVeriFy_ECC(     void hSessionHandle,
                                            unsigned int uiiSKinDex,
                                            unSigneDchar pucData,
                                            unsigned int uiDataLength,
                                            ECCSignature pucSignature) ;        
        外部密钥 ECC 公钥加密 
            int SDF_ExternalEncrypt_ECC(    void hSessionHandle,
                                            unsigned int uiAlgID,
                                            ECCreFPublicKey  pucPublicKey,
                                            unsigned char  pucData,
                                            unsigned int uiDataLength,
                                            ECCCipher  pucEncData) ;        
        外部密钥 ECC 私钥解密
            int SDF_ExternalDecrypt_ECC(    void hSessionHandle,
                                            unsigned int uiAlgID,
                                            ECCreFPrivateKey  pucPrivateKey,
                                            ECCCipher  pucEncData,
                                            unsigned char  pucData,
                                            unsigned int  puiDataLength) ;        
    对称算法运算类函数 
        对称加密 
            int SDF_Encrypt(   void hSessionHandle,
                                void hKeyHandle,
                                unsigned int uiAlgID,
                                unsigned char  pucIV,
                                unsigned char  pucData,
                                unsigned int uiDataLength,
                                unsigned char  pucEncData,
                                unsigned int  puiEncDataLength) ;        
        对称解密 
            int SDF_Decrypt (  void hSessionHandle,
                                void hKeyHandle,
                                unsigned int uiAlgID,
                                unsigned char  pucIV,
                                unsigned char  pucEncData,
                                unsigned int uiEncDataLength,
                                unsigned char  pucData,
                                unsigned int  puiDataLength) ;        
        计算 ＭAC
            int SDF_CalculateＭAC( void hSessionHandle,
                                    void hKeyHandle,
                                    unsigned int uiAlgID,
                                    unSigneDchar pucIV,
                                    unSigneDchar pucData,
                                    unsigned int uiDataLength,
                                    unSigneDchar pucＭAC,
                                    unsigned int puiＭACLength) ;
    杂凑运算类函数 
        杂凑运算初始化 
            int SDF_HaShinit( void hSessionHandle,
                                unsigned int uiAlgiD
                                ECCreFPublicKey pucPublicKey,
                                unSigneDchar puciD,
                                unsigned int uiiDLength) ;        
        多包杂凑运算 
            int SDF_HaShUpDate(  void hSessionHandle,
                                    unSigneDchar pucData,
                                    unsigned int uiDataLength) ;        
        杂凑运算结束 
            int SDF_HaShFinal(  void hSessionHandle,
                                unSigneDchar pucHaSh,
                                unsigned int puiHaShLength) ;        
    用户文件操作类函数 
        创建文件
            int SDF_CreateFile( void hSessionHandle,
                                unsigned char  pucFilename,
                                unsigned int uinameLen,
                                unsigned int uiFileSize) ;
        读取文件
            int SDF_ReaDFile(   void hSessionHandle,
                                unsigned char  pucFilename,
                                unsigned int uinameLen,
                                unsigned int uiOFFSet,
                                unsigned int  puiFileLength,
                                unsigned char  pucBuFFer) ;        
        写文件 
            int SDF_WriteFile(  void hSessionHandle,
                                unsigned char  pucFilename,
                                unsigned int uinameLen,
                                unsigned int uiOFFSet,
                                unsigned int uiFileLength,
                                unsigned char  pucBuFFer) ;        
        删除文件
            int SDF_DeleteFile( void hSessionHandle,
                                unSigneDchar pucFilename,
                                unsigned int uinameLen) ;    