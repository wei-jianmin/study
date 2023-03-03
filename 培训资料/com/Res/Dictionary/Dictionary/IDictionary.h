#pragma once
class IDictionary
{
public:	virtual void Initialize()     = 0;	virtual void Loadlibrary()    = 0;	virtual void InsertWord()     = 0;	virtual void DeleteWord()     = 0;	virtual void LookupWord()     = 0;	virtual void RestoreLibrary() = 0;	virtual void FreeLibrary()    = 0;
};