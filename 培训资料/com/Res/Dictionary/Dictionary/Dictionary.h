#pragma once
#include "IDictionary.h"

class CDictionary:public IDictionary{public:	virtual void Initialize();	virtual void Loadlibrary();	virtual void InsertWord();	virtual void DeleteWord();	virtual void LookupWord();	virtual void RestoreLibrary();	virtual void FreeLibrary();private:	int m_data;};