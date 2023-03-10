#include <stdlib.h>
#include <stdio.h>
#include <list>
#include <iostream>
#include <string>
using namespace std;

class IAutoRelease
{
public:
	virtual void regist(IAutoRelease * child)=0;
	virtual void setName(const string & name)=0;
	virtual const char* getName()=0;
	virtual ~IAutoRelease(){};
};

class AutoRelease:public IAutoRelease
{
public:
	AutoRelease(IAutoRelease * parrent,const char* name);
	virtual ~AutoRelease();
	void setName(const string & name);
	const char* getName();
private:
	virtual void regist(IAutoRelease * child);
private:
	string name_;
	list<IAutoRelease*> childs_;
};

AutoRelease::AutoRelease(IAutoRelease * parrent,const char* name)
{
	name_ = name;
	if(parrent)
		parrent->regist(this);
}

AutoRelease::~AutoRelease()
{
	while(childs_.size()>0)
	{
		IAutoRelease * child = childs_.front();
		childs_.pop_front();
		//printf("delete %s\n",child->getName());
		delete child;
	}
}

void AutoRelease::setName(const string & name)
{
	name_ = name;
}

const char* AutoRelease::getName()
{
	return name_.c_str();
}

void AutoRelease::regist(IAutoRelease * child)
{
	if(child)
		childs_.push_back(child);
}

class A:public AutoRelease
{
public:
	A(IAutoRelease * parrent,const char* name):AutoRelease(parrent,name){ printf("A:%s construct\n",name); }
	~A(){ printf("A:%s destruct\n",getName());  }
};

class B:public AutoRelease
{
public:
	B(IAutoRelease * parrent,const char* name):AutoRelease(parrent,name){ printf("B:%s construct\n",name); }
	~B(){ printf("B:%s destruct\n",getName());  }
};

class C:public AutoRelease
{
public:
	C(IAutoRelease * parrent,const char* name):AutoRelease(parrent,name){ printf("C:%s construct\n",name); }
	~C(){ printf("C:%s destruct\n",getName()); }
};

int main()
{
	{
		A a(NULL,"a");
		/*
		A * pa1 = new A(&a,"a1");
		A * pa2 = new A(&a,"a2");
		B * pb11 = new B(pa1,"b11");
		B * pb12 = new B(pa1,"b12");
		B * pb21 = new B(pa2,"b21");
		B * pb22 = new B(pa2,"b22");
		C * pc11 = new C(pb11,"c11");
		C * pc12 = new C(pb12,"c12");
		C * pc21 = new C(pb21,"c21");
		C * pc22 = new C(pb22,"c22");
		*/
		IAutoRelease * pa1 = new A(&a,"a1");
		IAutoRelease * pa2 = new A(&a,"a2");
		IAutoRelease * pb11 = new B(pa1,"b11");
		IAutoRelease * pb12 = new B(pa1,"b12");
		IAutoRelease * pb21 = new B(pa2,"b21");
		IAutoRelease * pb22 = new B(pa2,"b22");
		IAutoRelease * pc11 = new C(pb11,"c11");
		IAutoRelease * pc12 = new C(pb12,"c12");
		IAutoRelease * pc21 = new C(pb21,"c21");
		IAutoRelease * pc22 = new C(pb22,"c22");
	}
	system("pause");
	return 0;
}