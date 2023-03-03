#include <sdf.h>
#include <sdf_type.h>
#include <sdf_dev_manage.h>
#include <stdio.h>
#include <string.h>
#include <malloc.h>

extern unsigned char rsa_keypair_2048[];
extern unsigned char sm1_standard_ecb_enc_key0[] ;
extern unsigned char sm1_standard_ecb_enc_srcdat0[];
extern unsigned char sm1_standard_ecb_enc_dstdat0[];

struct asymm_dec_str
{
	unsigned char * psrcdat;
	unsigned char * pstddat;
	unsigned char * pkey;	
	unsigned int len;
};
extern struct asymm_dec_str sm2_dec_str[11];

extern void print_data(const char *string, unsigned char*data, int size);

#define RSA_KEY
#define ECC_KEY
#define KEK_KEY

u32 Create_Key(void *hSessionHandle)
{
	u32 r;
	int i;
	RSArefPublicKey rsapubkey;
	RSArefPrivateKey rsarefprikey;
	ECCrefPublicKey eccrefpubkey;
	ECCrefPrivateKey eccrefprikey;
	char key[16];
	struct asymm_dec_str *pstr;
	unsigned int offset;

	u8 keypair[] = {
		//x
		0x19, 0x79, 0x5d, 0xf7, 0x01, 0xf3, 0x9d, 0x1f, 0xb2, 0x20, 0xc4, 0x5f, 0xa7, 0xfa, 0x4e, 0xbf, 
		0xad, 0xd1, 0x70, 0x25, 0x37, 0xb9, 0x46, 0xcd, 0x3d, 0x48, 0x04, 0xb3, 0x7f, 0xbc, 0x3e, 0xa5,
		//y
		0x2b, 0x2c, 0xee, 0xd6, 0xcc, 0x04, 0x2b, 0x5b, 0xbb, 0x56, 0x8d, 0xed, 0x3b, 0x36, 0x73, 0xf2, 
		0x88, 0xe1, 0x9c, 0xc4, 0x9a, 0xe3, 0xc3, 0x50, 0xd2, 0xb8, 0x09, 0x03, 0xd8, 0x6d, 0x91, 0x2c,
		//d
		0x3f, 0x91, 0x68, 0xe8, 0x6d, 0x2a, 0xac, 0xaa, 0x2c, 0x81, 0xd8, 0xba, 0x24, 0x9b, 0xc9, 0x5a, 
		0x60, 0xe0, 0x47, 0x50, 0xa2, 0xee, 0xaa, 0x63, 0x26, 0x2b, 0x54, 0xc4, 0x75, 0x51, 0xb8, 0xdc
	};
	u8 rsa1024key[] = {
		/* m */
		0xe3,0xa9,0xa2,0x45,0x95,0x78,0x40,0x60,0xb7,0x01,0x70,0xbe,0x26,0x86,0x9b,0x28,
		0xf8,0x55,0x8d,0xd1,0x63,0xb6,0x26,0x3d,0xba,0x5b,0x3d,0x27,0xf2,0x5c,0x3f,0x4f,
		0x00,0x5c,0x18,0x4b,0x35,0x70,0x18,0xf6,0xe3,0xbe,0x50,0x51,0x29,0x2b,0x79,0xf3,
		0x6c,0x2a,0xe5,0x9a,0x8e,0x56,0x4e,0x59,0x93,0x7e,0xfd,0x27,0x6d,0x6d,0xb8,0xc9,
		0x16,0xa2,0x7b,0x5c,0x21,0x63,0x9d,0xf3,0x13,0x33,0x86,0x5d,0x0c,0x4c,0x4d,0x54,
		0x59,0x24,0xb3,0x96,0xeb,0xb4,0xa8,0x4d,0x0d,0x44,0x40,0xb1,0xc0,0xdf,0x98,0x4c,
		0x70,0xa3,0xd4,0xef,0x5e,0x02,0x66,0x8c,0xa9,0xcc,0x31,0xc7,0x52,0x8c,0xca,0x7e,
		0x06,0xf3,0x94,0x75,0x47,0x98,0x4b,0x54,0x7a,0x68,0x95,0x94,0xc2,0x33,0x99,0xb7,
		/* e */
		//0x01,0x00,0x01
		/* p */
		0xbf,0xcb,0xf1,0xf1,0xea,0x02,0x01,0xed,0x56,0x81,0xb0,0x17,0x6c,0x10,0x9d,0x20,
		0x65,0xe7,0xad,0x49,0x8d,0x3e,0xcd,0x72,0xb2,0x09,0xff,0x93,0xa1,0x29,0x80,0x17,
		0x67,0x0e,0x27,0x10,0x66,0x83,0x4b,0xfa,0x63,0x25,0x93,0x90,0x49,0x58,0x3f,0x69,
		0x5b,0xec,0xb3,0x63,0x02,0x5e,0x1a,0x86,0x6a,0x4a,0x51,0x6d,0xdf,0x5e,0x71,0xdc,
		/* q */
		0xdd,0xba,0x63,0xd1,0xe0,0x3f,0x56,0x4d,0xad,0xda,0xf9,0x4a,0x36,0xae,0x6e,0xed,
		0xb4,0x60,0x60,0x09,0x9a,0x44,0x2c,0x63,0xbf,0xc9,0x16,0x3c,0xae,0x64,0x3c,0xfe,
		0xe1,0xcc,0x73,0x7f,0x1a,0x33,0x05,0x53,0x4d,0x95,0xd6,0x03,0x42,0x83,0x82,0x03,
		0xff,0xa7,0x17,0x90,0x22,0xc7,0xd0,0x9c,0xaa,0x79,0xd3,0xfb,0x60,0x6f,0x36,0xd5,
		/* dp */
		0x07,0x6d,0x22,0x64,0xb1,0xa4,0x37,0x51,0x12,0x3d,0x47,0xf4,0x74,0xa5,0xf8,0x56,
		0xec,0x5d,0x75,0x0e,0xb4,0x2a,0xb7,0xe5,0x24,0xe8,0x78,0x83,0x9f,0xdc,0xd0,0xfb,
		0x88,0x18,0x4d,0xbb,0x8c,0xfb,0x58,0xef,0xee,0xe1,0x62,0x3b,0x83,0x22,0x8e,0x3d,
		0xc5,0x4b,0x92,0xbb,0xee,0x45,0x3f,0xde,0x61,0x3d,0x3f,0x07,0x7e,0x4b,0x1a,0x4f,
		/* dq */
		0xcd,0x95,0xf2,0xa4,0x0a,0xd6,0x14,0x0a,0xe0,0x92,0xce,0x94,0x26,0xf4,0x8b,0xab,
		0x75,0x1f,0x22,0xa5,0x45,0x9a,0x61,0x73,0xd2,0x7d,0x25,0x8d,0xce,0xb7,0x9c,0x07,
		0xb5,0xb9,0x17,0xe7,0xd1,0xaa,0xdb,0x4a,0x8e,0x2f,0x2f,0xd2,0x47,0x6f,0x90,0x7c,
		0xf7,0x0a,0x6b,0xcd,0x55,0x4e,0x86,0x63,0x95,0x27,0xa8,0x53,0x2e,0xa5,0x86,0xa2,
		/* coef */
		0xcc,0xda,0x66,0xda,0xb6,0xbc,0x8c,0x3f,0xc9,0x2c,0xdc,0xb8,0x35,0x2d,0x0c,0x19,
		0x70,0x61,0x2c,0x62,0x32,0x1a,0x22,0x09,0x9a,0x4d,0xeb,0x04,0xf2,0x1d,0x3b,0x0f,
		0x5a,0xb6,0x61,0xcd,0xec,0x6c,0x22,0x62,0x26,0x3e,0xd7,0xc1,0x3e,0x5b,0x8c,0xcc,
		0x09,0x60,0xf9,0x57,0x04,0xae,0x37,0xa7,0x1f,0xa1,0x6b,0x34,0x44,0xc4,0xeb,0x23,
		/* d */
		0x31,0x48,0x97,0x89,0x3c,0x53,0x1a,0xfa,0x2b,0xd4,0x8d,0xc3,0x0b,0x3e,0x3e,0x65,
		0x46,0x8d,0xbe,0xb2,0x77,0x67,0x0a,0x20,0xe4,0x19,0xf1,0x54,0x34,0xf6,0xa3,0xd2,
		0xd8,0x7a,0x68,0xfe,0x29,0x92,0xde,0x00,0x3f,0x9a,0x5c,0x3c,0x29,0x1f,0xd7,0xc0,
		0x28,0x4d,0x86,0xd9,0x36,0xbb,0xbc,0x09,0xcd,0xd0,0x35,0xd0,0xe0,0x3a,0x02,0xbf,
		0x98,0x06,0x65,0x0e,0x2a,0x5b,0x6a,0xdd,0x2b,0x9e,0xe1,0x7c,0x8e,0x29,0xfe,0xce,
		0x01,0xf0,0x3d,0x93,0xe6,0x93,0x53,0xcf,0xc7,0xc4,0x66,0xa3,0x7a,0x0b,0x7f,0xdc,
		0x6b,0xe1,0x1b,0x46,0x70,0x3b,0xe2,0xc6,0xd2,0x13,0xc4,0xb8,0x11,0xa9,0x6c,0x28,
		0x57,0xfd,0xf1,0xdc,0x5b,0x1e,0x12,0xbc,0xc2,0x85,0xa4,0x4b,0x96,0xd8,0x8b,0x78};
/*
	for(i=1; i<=SDF_MAX_KEY_INDEX; i++)
	{
		r = SDF_GetPrivateKeyAccessRight(hSessionHandle, i, "hss.locate(gusu)", 16);
		if(r) return r; 
	}

*/
#ifdef KEK_KEY
	for(i=1; i<(SDF_MAX_KEY_INDEX); i++)
	{
		printf("create kek key index:%x\n", i);
		r = EVDF_CreateKEK(hSessionHandle, i, 128);
		if(r)
		{
			printf("create kek[%d] fail:%x\n", i, r);
			return r;		
		}
	}
#endif	
	
#ifdef RSA_KEY
	for(i=1; i<(SDF_MAX_KEY_INDEX-2); i++)
	{
		printf("create rsa key pair index:%x\n", i);
		r = EVDF_CreateKeyPair_RSA(hSessionHandle, 1, i, 2048, &rsapubkey);
		if(r)
		{
			printf("create rsa sign key pair fail:%x\n", r);
			return r;
		}

		r = EVDF_CreateKeyPair_RSA(hSessionHandle, 0, i, 2048, &rsapubkey);
		if(r)
		{
			printf("create rsa enc key pair fail:%x\n", r);
			return r;			
		}
	}

	printf("create rsa key pair index:%x\n", (SDF_MAX_KEY_INDEX-2));
	r = EVDF_CreateKeyPair_RSA(hSessionHandle, 1, (SDF_MAX_KEY_INDEX-2), 1024, &rsapubkey);
	if(r)
	{
		printf("create rsa sign key pair fail:%x\n", r);
		return r;
	}

	r = EVDF_CreateKeyPair_RSA(hSessionHandle, 0, (SDF_MAX_KEY_INDEX-2), 1024, &rsapubkey);
	if(r)
	{
		printf("create rsa enc key pair fail:%x\n", r);
		return r;			
	}

	printf("create rsa key pair index:%x\n", (SDF_MAX_KEY_INDEX-1));
	memset(&rsapubkey, 0x00, sizeof(RSArefPublicKey));
	memset(&rsarefprikey, 0x00, sizeof(RSArefPrivateKey));
	offset = 128;
	rsarefprikey.bits = 1024;
	memcpy(rsarefprikey.m+offset, rsa1024key, rsarefprikey.bits/8);
	c_reverse(rsarefprikey.m+offset, rsarefprikey.bits/8);
	
	memcpy(rsarefprikey.prime[0]+offset/2, rsa1024key+(rsarefprikey.bits/16)*2, rsarefprikey.bits/16);
	c_reverse(rsarefprikey.prime[0]+offset/2, rsarefprikey.bits/16);

	memcpy(rsarefprikey.prime[1]+offset/2, rsa1024key+(rsarefprikey.bits/16)*3, rsarefprikey.bits/16);
	c_reverse(rsarefprikey.prime[1]+offset/2, rsarefprikey.bits/16);
	
	memcpy(rsarefprikey.pexp[0]+offset/2, rsa1024key+(rsarefprikey.bits/16)*4, rsarefprikey.bits/16);
	c_reverse(rsarefprikey.pexp[0]+offset/2, rsarefprikey.bits/16);

	memcpy(rsarefprikey.pexp[1]+offset/2, rsa1024key+(rsarefprikey.bits/16)*5, rsarefprikey.bits/16);
	c_reverse(rsarefprikey.pexp[1]+offset/2, rsarefprikey.bits/16);

	memcpy(rsarefprikey.coef+offset/2, rsa1024key+(rsarefprikey.bits/16)*6, rsarefprikey.bits/16);
	c_reverse(rsarefprikey.coef+offset/2, rsarefprikey.bits/16);

	memcpy(rsarefprikey.d+offset, rsa1024key+(rsarefprikey.bits/16)*7, rsarefprikey.bits/8);
	c_reverse(rsarefprikey.d+offset, rsarefprikey.bits/8);

	r = EVDF_ImportKeyPair_RSA( hSessionHandle, 0, (SDF_MAX_KEY_INDEX-1), &rsarefprikey);
	if(r)
	{
		printf("import rsa enc key pair fail:%x\n", r);
		return r;	
	}

	r = EVDF_ImportKeyPair_RSA( hSessionHandle, 1, (SDF_MAX_KEY_INDEX-1), &rsarefprikey);
	if(r)
	{
		printf("import rsa sign key pair fail:%x\n", r);
		return r;	
	}	
#endif

#ifdef ECC_KEY
	for(i=1; i<(SDF_MAX_KEY_INDEX-1); i++)
	{
		printf("create ecc key pair index:%x\n", i);
		r = EVDF_CreateKeyPair_ECC(hSessionHandle, 1, i, &eccrefpubkey);
		if(r)
		{
			printf("create ecc sign key pair fail:%x\n", r);
			return r;
		}

		r = EVDF_CreateKeyPair_ECC(hSessionHandle, 0, i, &eccrefpubkey);
		if(r)
		{
			printf("create ecc enc key pair fail:%x\n", r);
			return r;
		}
	}


	pstr = &sm2_dec_str[0];
	memset(&eccrefprikey, 0, sizeof(ECCrefPrivateKey));
	memcpy(eccrefprikey.K+32, pstr->pkey+64, 32);
	eccrefprikey.bits = 256;
	memset(&eccrefpubkey, 0, sizeof(ECCrefPublicKey));
	memcpy(eccrefpubkey.x+32, pstr->pkey, 32);
	memcpy(eccrefpubkey.y+32, pstr->pkey+32, 32);
	eccrefpubkey.bits = 256;
	
	r = EVDF_ImportKeyPair_ECC(hSessionHandle, 1, (SDF_MAX_KEY_INDEX-1), &eccrefpubkey, &eccrefprikey);
	if(r)
	{
		printf("import ecc sign key pair 4 fail:%x\n", r);
		return r;		
	}

	r = EVDF_ImportKeyPair_ECC(hSessionHandle, 0, (SDF_MAX_KEY_INDEX-1), &eccrefpubkey, &eccrefprikey);
	if(r)
	{
		printf("import ecc enc key pair 4 fail:%x\n", r);
		return r;		
	}
#endif	

#if 1
	r = EVDF_ImportKEK(hSessionHandle, SDF_MAX_KEY_INDEX, sm1_standard_ecb_enc_key0, 128);
	if(r)
	{
		printf("create kek[%d] fail:%x\n", i, r);
		return r;		
	}

	rsarefprikey.bits = 2048;
	memcpy(rsarefprikey.m, rsa_keypair_2048, RSAref_MAX_LEN);
	c_reverse(rsarefprikey.m, RSAref_MAX_LEN);	
	memcpy(rsarefprikey.prime[0], rsa_keypair_2048+RSAref_MAX_PLEN*2, RSAref_MAX_PLEN);
	c_reverse(rsarefprikey.prime[0], RSAref_MAX_LEN/2);
	memcpy(rsarefprikey.prime[1], rsa_keypair_2048+RSAref_MAX_PLEN*3, RSAref_MAX_PLEN);
	c_reverse(rsarefprikey.prime[1], RSAref_MAX_LEN/2);	
	memcpy(rsarefprikey.pexp[0], rsa_keypair_2048+RSAref_MAX_PLEN*4, RSAref_MAX_PLEN);
	c_reverse(rsarefprikey.pexp[0], RSAref_MAX_LEN/2);
	memcpy(rsarefprikey.pexp[1], rsa_keypair_2048+RSAref_MAX_PLEN*5, RSAref_MAX_PLEN);
	c_reverse(rsarefprikey.pexp[1], RSAref_MAX_LEN/2);
	memcpy(rsarefprikey.coef, rsa_keypair_2048+RSAref_MAX_PLEN*6, RSAref_MAX_PLEN);
	c_reverse(rsarefprikey.coef, RSAref_MAX_LEN/2);
	memcpy(rsarefprikey.d, rsa_keypair_2048+RSAref_MAX_PLEN*7, RSAref_MAX_LEN);
	c_reverse(rsarefprikey.d, RSAref_MAX_LEN);
	
	r = EVDF_ImportKeyPair_RSA( hSessionHandle, 0, SDF_MAX_KEY_INDEX, &rsarefprikey);
	if(r)
	{
		printf("import rsa enc key pair fail:%x\n", r);
		return r;	
	}

	r = EVDF_ImportKeyPair_RSA( hSessionHandle, 1, SDF_MAX_KEY_INDEX, &rsarefprikey);
	if(r)
	{
		printf("import rsa sign key pair fail:%x\n", r);
		return r;	
	}
#endif

	memset(&eccrefprikey, 0, sizeof(ECCrefPrivateKey));
	memcpy(eccrefprikey.K+32, keypair+64, 32);
	eccrefprikey.bits = 256;
	memset(&eccrefpubkey, 0, sizeof(ECCrefPublicKey));
	memcpy(eccrefpubkey.x+32, keypair, 32);
	memcpy(eccrefpubkey.y+32, keypair+32, 32);
	eccrefpubkey.bits = 256;
	
	r = EVDF_ImportKeyPair_ECC(hSessionHandle, 1, SDF_MAX_KEY_INDEX, &eccrefpubkey, &eccrefprikey);
	if(r)
	{
		printf("import ecc sign key pair fail:%x\n", r);
		return r;		
	}

	r = EVDF_ImportKeyPair_ECC(hSessionHandle, 0, SDF_MAX_KEY_INDEX, &eccrefpubkey, &eccrefprikey);
	if(r)
	{
		printf("import ecc enc key pair fail:%x\n", r);
		return r;		
	}
	
	return 0;
}


u32 Import_KEK_Key_Check(void *hSessionHandle)
{
	u32 r;
	void * hKeyHandle;

	r = SDF_ImportKeyWithKEK(hSessionHandle,SGD_SM1_ECB,SDF_MAX_KEY_INDEX,sm1_standard_ecb_enc_dstdat0,16,&hKeyHandle);
	if(r)
	{
		printf("ImportKeyWithKEK fail:%x\n", r);
		return r;
	}

	return r;
}

u32 Import_ECC_KeyPair_Check(void *hSessionHandle)
{
	u32 r;
	ECCrefPublicKey eccpubkey;
	ECCrefPrivateKey eccprikey;
	ECCSignature sig;
	int i;
	unsigned char data[32];	
	u8 keypair[] = {
		//x
		0x19, 0x79, 0x5d, 0xf7, 0x01, 0xf3, 0x9d, 0x1f, 0xb2, 0x20, 0xc4, 0x5f, 0xa7, 0xfa, 0x4e, 0xbf, 
		0xad, 0xd1, 0x70, 0x25, 0x37, 0xb9, 0x46, 0xcd, 0x3d, 0x48, 0x04, 0xb3, 0x7f, 0xbc, 0x3e, 0xa5,
		//y
		0x2b, 0x2c, 0xee, 0xd6, 0xcc, 0x04, 0x2b, 0x5b, 0xbb, 0x56, 0x8d, 0xed, 0x3b, 0x36, 0x73, 0xf2, 
		0x88, 0xe1, 0x9c, 0xc4, 0x9a, 0xe3, 0xc3, 0x50, 0xd2, 0xb8, 0x09, 0x03, 0xd8, 0x6d, 0x91, 0x2c,
		//d
		0x3f, 0x91, 0x68, 0xe8, 0x6d, 0x2a, 0xac, 0xaa, 0x2c, 0x81, 0xd8, 0xba, 0x24, 0x9b, 0xc9, 0x5a, 
		0x60, 0xe0, 0x47, 0x50, 0xa2, 0xee, 0xaa, 0x63, 0x26, 0x2b, 0x54, 0xc4, 0x75, 0x51, 0xb8, 0xdc
	};

	printf("%s()-start\n", __func__);

	for(i=0; i<32; i++)
		data[i] = (u8)(i+0x80);

	memset(&eccprikey, 0, sizeof(ECCrefPrivateKey));
	memcpy(eccprikey.K+32, keypair+64, 32);
	eccprikey.bits = 256;
	r = SDF_ExternalSign_ECC(hSessionHandle, SGD_SM2_1, &eccprikey, data, 32, &sig);
	if(r)
	{
		printf("external ecc sign fail:%x\n", r);
		return r;
	}

	r = SDF_InternalVerify_ECC(hSessionHandle, SDF_MAX_KEY_INDEX, data, 32, &sig);
	if(r)
	{
		printf("internal ecc verify fail:%x\n", r);
		return r;
	}

	printf("%s()-success\n", __func__);
	return r;
}


u32 Import_RSA_KeyPair_Check(void *hSessionHandle)
{
	u32 r;
	int i;
	unsigned char cipher_key[0x200];
	unsigned int cipher_keylen;
	RSArefPublicKey pubkey;
	void *hKey1;
	void *hKey2;
	void *hKey3;
	unsigned char data[16];
	unsigned char encdata[16];
	unsigned char decdata[16];
	unsigned int datalen;
	unsigned int enclen;
	unsigned int declen;

	printf("%s()-start\n", __func__);
	
	pubkey.bits = 2048;
	memcpy(pubkey.m, rsa_keypair_2048, RSAref_MAX_LEN);
	c_reverse(pubkey.m, RSAref_MAX_LEN);	
	r = SDF_GenerateKeyWithEPK_RSA(hSessionHandle, 128, &pubkey, cipher_key, &cipher_keylen, &hKey1);
	if(r)
	{
		printf("generate session key with rsa esk fail:%x\n", r);
		return r;
	}

	r = SDF_ImportKeyWithISK_RSA(hSessionHandle, SDF_MAX_KEY_INDEX, cipher_key, cipher_keylen, &hKey2);
	if(r)
	{
		printf("import session key with rsa isk fail:%x\n", r);
		return r;
	}

	for(i=0; i<16; i++)
		data[i] = (unsigned char)i;	
	datalen = 16;
	
	r = SDF_Encrypt(hSessionHandle, hKey1, SGD_SM1_ECB, NULL, data, datalen, encdata, &enclen);
	if(r)
	{
		printf("encrypt data fail:%x\n", r);
		return r;
	}
#ifdef LOG	
	print_data("encrypt data:", encdata, enclen);
#endif

	r = SDF_Decrypt(hSessionHandle, hKey2, SGD_SM1_ECB, NULL, encdata, enclen, decdata, &declen);
	if(r)
	{
		printf("decrypt data fail:%x\n", r);
		return r;		
	}
#ifdef LOG	
	print_data("decrypt data:", decdata, declen);
#endif

	if((declen != datalen) || memcmp(data, decdata, datalen))
	{
		printf("%s()-source data != dec data\n", __func__);
		return 1;
	}
	
	r = SDF_DestroyKey(hSessionHandle, hKey1);
	if(r)
	{
		printf("destroy session key1 fail:%x\n", r);
		return r;
	}

	r = SDF_DestroyKey(hSessionHandle, hKey2);
	if(r)
	{
		printf("destroy session key2 fail:%x\n", r);
		return r;
	}	

	printf("%s()-success\n", __func__);
	return r;
}

/*
u32 KEK_Key_Check(void *hSessionHandle)
{
	u32 r;
	int i, j;
	u8  ucKey[16] = {0};
	u32 uiKeyLength;
	void * hKeyHandle;
	
	r = SDF_GenerateKeyWithKEK(hSessionHandle, 128, SGD_SM1_ECB, SDF_MAX_KEY_INDEX, ucKey, &uiKeyLength, &hKeyHandle);
	if(r)
	{
		printf("generate kek key fail:%x\n", r);
		return r;			
	}

	r = SDF_DestroyKey(hSessionHandle, hKeyHandle);
	if(r)
	{
		printf("destroy session key fail:%x\n", r);
		return r;
	} 
	
	return 0;
}

u32 RSA_Key_Check(void *hSessionHandle)
{
	u32 r;
	int i, j;
	unsigned char data[256];
	unsigned char encdata[256];
	unsigned char decdata[256];
	unsigned int datalen;
	unsigned int enclen;
	unsigned int declen;

	for(i=1; i<SDF_MAX_KEY_INDEX; i++)
	{
		datalen = 256;
		enclen = 256;
		declen = 256;
		for(j=0; j<datalen; j++)
			data[j] = (u8)(j*i+0xa0);
		r = SDF_InternalPublicKeyOperation_RSA(hSessionHandle, i, data, datalen, encdata, &enclen);
		if(r)
		{
			printf("internal rsa public key operation fail:%x\n", r);
			return r;
		}

		r = SDF_InternalPrivateKeyOperation_RSA(hSessionHandle, i, encdata, enclen, decdata, &declen);
		if(r)
		{
			printf("internal rsa private key operation fail:%x\n", r);
			return r;
		}
		if((declen != datalen) || memcmp(data, decdata, datalen))
		{
			printf("%s()-source data != dec data\n", __func__);
			return 1;
		}
	}

	return 0;
}

u32 ECC_Key_Check(void *hSessionHandle)
{
	u32 r;
	ECCrefPublicKey eccpubkey;
	ECCrefPrivateKey eccprikey;
	ECCSignature sig;
	int i, j;
	unsigned char data[32];
	unsigned char encdata[256];
	unsigned char decdata[256];
	int declen;
	ECCCipher *pecccipher = (ECCCipher *)encdata;	

	for(i=1; i<SDF_MAX_KEY_INDEX; i++)
	{
		for(j=0; j<32; j++)
			data[j] = (u8)(j*i+0x18);
		memset(&sig, 0, sizeof(sig));
		
		r = SDF_InternalSign_ECC(hSessionHandle, i, data, 32, &sig);
		if(r)
		{
			printf("internal ecc sign data fail:%x\n", r);
			return r;
		}

		r = SDF_InternalVerify_ECC(hSessionHandle, i, data, 32, &sig);
		if(r)
		{
			printf("internal ecc verify fail:%x\n", r);
			return r;
		}
	}

	return 0;
}

u32 Import_Key_Check(void *hSessionHandle)
{
	u32 r;
	int i, j;
	unsigned char data[256];
	unsigned char encdata[256];
	unsigned char decdata[256];
	unsigned int datalen;
	unsigned int enclen;
	unsigned int declen;
	ECCSignature sig;
	ECCCipher *pecccipher = (ECCCipher *)encdata;	

	datalen = 256;
	enclen = 256;
	declen = 256;
	for(j=0; j<datalen; j++)
		data[j] = (u8)(j*i+0x13);
	r = SDF_InternalPublicKeyOperation_RSA(hSessionHandle, SDF_MAX_KEY_INDEX, data, datalen, encdata, &enclen);
	if(r)
	{
		printf("%s()-internal rsa public key operation fail:%x\n", __func__, r);
		return r;
	}

	r = SDF_InternalPrivateKeyOperation_RSA(hSessionHandle, SDF_MAX_KEY_INDEX, encdata, enclen, decdata, &declen);
	if(r)
	{
		printf("%s()-internal rsa private key operation fail:%x\n", __func__, r);
		return r;
	}
	if((declen != datalen) || memcmp(data, decdata, datalen))
	{
		printf("%s()-rsa: source data != dec data\n", __func__);
		return 1;
	}	

	for(j=0; j<32; j++)
		data[j] = (u8)(j*i+0x21);
	memset(&sig, 0, sizeof(sig));
	
	r = SDF_InternalSign_ECC(hSessionHandle, SDF_MAX_KEY_INDEX, data, 32, &sig);
	if(r)
	{
		printf("%s()-internal ecc sign data fail:%x\n", __func__,  r);
		return r;
	}

	r = SDF_InternalVerify_ECC(hSessionHandle, SDF_MAX_KEY_INDEX, data, 32, &sig);
	if(r)
	{
		printf("%s()-internal ecc verify fail:%x\n", __func__, r);
		return r;
	}	

	return 0;
}

*/

u32 Install_Key(void)
{
	u32 r;
	void *hDevcieHandle = NULL;
	void *hSessionHandle = NULL;

again:
	r = SDF_OpenDevice(&hDevcieHandle);
	if(r)
	{
		printf("SDF_OpenDevice fail:%x\n", r);
		return r;
	}
	//while(1);
	r = SDF_OpenSession(hDevcieHandle, &hSessionHandle);
	if(r)
	{
		printf("SDF_OpenSession fail:%x\n", r);
		goto err;
	}
	//while(1);
	r = Create_Key(hSessionHandle);
	if(r)
		goto err;
#if 0
	r = KEK_Key_Check(hSessionHandle);
	if(r)
	{
		SDF_CloseSession(hSessionHandle);
		SDF_CloseDevice(hDevcieHandle);	
		goto again;
	}	

	r = RSA_Key_Check(hSessionHandle);
	if(r)
	{
		SDF_CloseSession(hSessionHandle);
		SDF_CloseDevice(hDevcieHandle);	
		goto again;
	}	

	r = ECC_Key_Check(hSessionHandle);
	if(r)
	{
		SDF_CloseSession(hSessionHandle);
		SDF_CloseDevice(hDevcieHandle);	
		goto again;
	}	

	r = Import_Key_Check(hSessionHandle);
	if(r)
	{
		SDF_CloseSession(hSessionHandle);
		SDF_CloseDevice(hDevcieHandle);	
		goto again;
	}
#endif
	
err:
	if(hSessionHandle)
		SDF_CloseSession(hSessionHandle);
	if(hDevcieHandle)
		SDF_CloseDevice(hDevcieHandle);	

	return r;
}

u32 Init_Key(void)
{
	u32 r;
	int i;
	void *hDevcieHandle = NULL;
	void *hSessionHandle = NULL;
	unsigned char firm_version[64] = {0};
	unsigned char root_key[16]    = {0xAF,0x86,0x18,0x23,0x8C,0x94,0xA1,0x19,0xAE,0x6D,0xE9,0x22,0xDB,0xB9,0x35,0x4D};

	r = SDF_OpenDevice(&hDevcieHandle);
	if(r)
	{
		printf("SDF_OpenDevice fail:%x\n", r);
		return r;
	}

	r = SDF_OpenSession(hDevcieHandle, &hSessionHandle);
	if(r)
	{
		printf("SDF_OpenSession fail:%x\n", r);
		goto err;
	}
	
	r = EVDF_GetFirmwareVersion(hSessionHandle, firm_version);
	if(r)
	{
		printf("SDF_OpenSession fail:%x\n", r);
		goto err;
	}
	printf("soft version:%32.32s\n", &firm_version[0]);
	printf("hard version:%32.32s\n", &firm_version[32]);
	
	r = EVDF_InitKeyFileSystem(hSessionHandle, (char*)"11111111", NULL, 128, (char *)"11111111", (char *)"11111111");
	if(r)
	{
		printf("SDF_InitKeyFileSystem fail:%x\n", r);
		goto err;
	}	

	r = KeySlot_State_Test(hSessionHandle);
	if(r)
	{
		printf("KeySlot_State_Test fail:%x\n", r);
		goto err;
	}
	
	for(i=1; i<=(SDF_MAX_KEY_INDEX); i++)
	{
		r = SDF_GetPrivateKeyAccessRight(hSessionHandle, i, "11111111", 8);
		if(r)
		{
				printf("SDF_GetPrivateKeyAccessRight(11111111) fail:%x\n", r);
				r = SDF_GetPrivateKeyAccessRight(hSessionHandle, i, "123456", 16);
				if(r)
				{
						printf("SDF_GetPrivateKeyAccessRight(123456) fail:%x\n", r);
				}	
		}
  }
  
#if 1	
	r = Create_Key(hSessionHandle);	
	if(r)
	{
		printf("Create_Key fail:%x\n", r);
	}
//#else

	r = Import_KEK_Key_Check(hSessionHandle);
	if(r)
	{
		printf("Import_KEK_Key_Check fail:%x\n", r);
	}

	r = Import_ECC_KeyPair_Check(hSessionHandle);
	if(r)
	{
		printf("Import_ECC_KeyPair_Check fail:%x\n", r);
	}

	r = Import_RSA_KeyPair_Check(hSessionHandle);
	if(r)
	{
		printf("Import_RSA_KeyPair_Check fail:%x\n", r);

	}
#endif
/*
	r = ECC_Key_Check(hSessionHandle);
	if(r)
	{
		printf("ECC_Key_Check fail:%x\n", r);
	}
*/

	r = KeySlot_State_Test(hSessionHandle);
	if(r)
	{
		printf("KeySlot_State_Test fail:%x\n", r);
		goto err;
	}
	
err:
	if(hSessionHandle)
		SDF_CloseSession(hSessionHandle);
	if(hDevcieHandle)
		SDF_CloseDevice(hDevcieHandle);	

	return r;	
}

u32 Restore_Factory_Setting(void)
{
	u32 r;
	int i;
	void *hDevcieHandle = NULL;
	void *hSessionHandle = NULL;

	r = SDF_OpenDevice(&hDevcieHandle);
	if(r)
	{
		printf("SDF_OpenDevice fail:%x\n", r);
		return r;
	}

	r = SDF_OpenSession(hDevcieHandle, &hSessionHandle);
	if(r)
	{
		printf("SDF_OpenSession fail:%x\n", r);
		goto err;
	}

	r = EVDF_RestoreFactorySetting(hSessionHandle, (char*)"11111111");
	if(r)
	{
		printf("SDF_RestoreFactorySetting fail:%x\n", r);
		goto err;
	}

err:
	if(hSessionHandle)
		SDF_CloseSession(hSessionHandle);
	if(hDevcieHandle)
		SDF_CloseDevice(hDevcieHandle);	

	return r;
}



u32 Get_Version(void)
{
	u32 r;
	int i;
	void *hDevcieHandle = NULL;
	void *hSessionHandle = NULL;
	unsigned char firm_version[64] = {0};

	r = SDF_OpenDevice(&hDevcieHandle);
	if(r)
	{
		printf("SDF_OpenDevice fail:%x\n", r);
		return r;
	}

	r = SDF_OpenSession(hDevcieHandle, &hSessionHandle);
	if(r)
	{
		printf("SDF_OpenSession fail:%x\n", r);
		goto err;
	}
	
	r = EVDF_GetFirmwareVersion(hSessionHandle, firm_version);
	if(r)
	{
		printf("SDF_OpenSession fail:%x\n", r);
		goto err;
	}
	printf("soft version:%32.32s\n", &firm_version[0]);
	printf("hard version:%32.32s\n", &firm_version[32]);
	
err:
	if(hSessionHandle)
		SDF_CloseSession(hSessionHandle);
	if(hDevcieHandle)
		SDF_CloseDevice(hDevcieHandle);	

	return r;	
}

