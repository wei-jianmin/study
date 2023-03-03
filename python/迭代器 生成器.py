������
    iter(iterable) -> iterator
    iter(callable, sentinel) -> iterator
    ����˵����
        iterable��
            �ɵ����࣬���������е��ַ������б�Ԫ�顢���ϡ��ֵ䶼�ǿɵ�����
            �Զ�����ʵ����__iter__()��__next__()����������ȱһ���ɣ�ʱ������Ϊ��������
                ������Ա�for-inö�٣���������Ϊiter()�����Ĳ����������������ڿɵ������ͣ�
                �� isinstance(o,Iterator) �������ԣ�����Ϊ True�������������ڵ�������
                �����������ڿɵ����ࣨ�Ӽ�����
                    �������಻��ͨ��index����ĳ��Ԫ�أ���֧�ֻ�ȡԪ���ܸ�����
                    ֻ��ͨ��next()����ǰ��
                    �����������������ԣ�ʹ�������Ա�ʾһ�����޵�����������ȫ����Ȼ��
                    ��������list������ʵ�ֵ�
                #����__iter__()��__next__()������
                __iter__������ϵͳ���������ɵ�����__next__�����˾���ĵ�������
                ��ʽ��˵���ǣ�
                ʵ����__iter__�����Ķ����ǿɵ�������ʵ����__next__�����Ķ����ǵ�����
                �ڴ���ִ�й����У�forѭ���������Զ����ϵͳ��Ϣ��ʶ��__iter__������
                Ȼ���Զ����ö�Ӧ��__next__����������һ��������
            �Զ�����࣬���������iter()������getitem()����������Ϊ�ɵ�����
                �����ԣ��Զ��������ֻʵ����__getitem__��Ա������
                ������Ա�for-inö�٣���������Ϊiter()�����Ĳ����������������ڿɵ������ͣ�
                ���� isinstance(o,Iterator) �������ԣ�����Ϊ False���������಻�ǵ������࣬
                ���ַ������б����ϵ������� isinstance(o,Iterator) �������ԣ�����Ϊ False
                ������Щ���Ͷ�ֻ�ǿɵ����࣬�����ǵ�������
                �²���Щ���������ڲ���Ҳ��ֻʵ����__getitem__��Ա����
                ��һ��˵��list��tuple��dict��set��str����ʵ����getitem()�������Զ����࣬
                ����ͳһ��֮Ϊ���������͡��������ṩ�˰������Ż�ȡԪ�ص��ֶΡ�
    �����Զ���ɵ����ࣺ
        ����һ��
            from collections import Iterable
            class myclass_1:
                def __init__(self,*args):
                    self._list=[1,2,3,4]
                    self._index=0
                def __getitem__(self,index):
                    return self._list[index%4-1]  #�Է����������Ͳ�����
            c1 = myclass_1()
            for i in c1: print(i)       #��ѭ�����1��2��3��4
            iter(c1)                    #������
        ���Զ���
            from collections import Iterable
            class myclass_2:
                def __init__(self,*args):
                    self._list=[1,2,3,4]
                    self._index=0
                def __iter__(self):
                    return self         #Ҫ�󷵻ص��ǿɵ�����������
                def __next__(self):     #�÷����������__ter__����������
                    self._index=self._index+1
                    if self._index>4:
                        self._index=1
                    return self._list[self._index%4-1]
            c2 = myclass_2()
            for i in c2:  print(i)      #��ѭ�����1��2��3��4
            iter(c2)                    #������
            �����ԣ�__next__()����������ڣ������ں���ʹ��for-in��iter()ʱ�ᱨ��
            ������Ϣ��iter() returned non-iterator of type 'myclass_2'
        ��������
            ���Դ��루�Բ���һ�����Զ�����������չ��
                from collections.abc import Iterator
                #0. ���庯�����Բ������в���
                def tell(o):
                  if isinstance(o,Iterator): 
                      print("{0} is Iterator".format(type(o)))
                  else:
                      print("{0} is not Iterator".format(type(o)))
                  try:
                      print("for�������: ",end='')
                      for i in o:  
                          print(i,end='  ')       #��ѭ�����1��2��3��4
                      print("\n")
                  except:
                      print("\n")
                  iter(o)                         #������
                #1. �����������1�������в���
                class myclass_1:
                    def __init__(self,*args):
                        self._list=[1,2,3,4]
                        self._index=1
                    def __getitem__(self,index):
                        if index>4:
                            raise StopIteration()
                        return self._list[index]  #�Է����������Ͳ�����
                c1 = myclass_1()
                tell(c1)
                #2. �����������2�������в���
                class myclass_2:
                    def __init__(self,*args):
                        self._list=[1,2,3,4]
                        self._index=0
                    def __iter__(self):
                        return self         #Ҫ�󷵻ص��ǿɵ�����������
                    def __next__(self):     #�÷����������__ter__����������
                        self._index=self._index+1
                        if self._index>4:
                            raise StopIteration()
                        return self._list[self._index%4-1]
                c2 = myclass_2()
                tell(c2)
                #3. �����ַ���
                c3="asdf"
                tell(c3)
                #4. �����б�
                c4=[1,2,3,4]
                tell(c4) 
                #5. ���Լ���
                c5={1,2,3,4,5}
                tell(c5)
            ������
                <class '__main__.myclass_1'> is not Iterator
                for�������: 1  2  3  4
                <class '__main__.myclass_2'> is Iterator
                for�������: 1  2  3  4
                <class 'str'> is not Iterator
                for�������: a  s  d  f
                <class 'list'> is not Iterator
                for�������: 1  2  3  4
                <class 'set'> is not Iterator
                for�������: 1  2  3  4  5
            ����ܽ�
                �� �Զ�����1��ֻʵ����__getitem__��Ա������
                ������Ա�for-inö�٣���������Ϊiter()�����Ĳ�����
                �����������ڿɵ������ͣ�
                ���� isinstance(o,Iterator) �������ԣ�����Ϊ False
                �� �Զ�����2��ʵ����__iter__()��__next__()������
                ������Ա�for-inö�٣���������Ϊiter()�����Ĳ�����
                �����������ڿɵ������ͣ�
                �� isinstance(o,Iterator) �������ԣ�����Ϊ True
                �� �ַ������б����ϵ����ͣ����ڿɵ�������
                ���� isinstance(o,Iterator) �������ԣ�����Ϊ False
                �²���Щ���������ڲ���ֻʵ����__getitem__��Ա����
                
������
    �� Python �У�ʹ���� yield �ĺ�������Ϊ��������generator��
    ������
        def func():
            print("---1---")
            yield 1    #yield��Ѻ�������ݰ�װ��generator������з���
            print("---2---")
            yield "abc"
            print("---3---")
            yield [1,2,3]
            print("---finish---")
        def func2():
            yield 2
        def func3()
            return 3
        def func4()
            print("abc")
        def func5()
            func()
        def func6()
            return func()
        f1 = func()
        f2 = func2()
        f3 = func3()
        f4 = func4()
        f5 = func5()
        f6 = func6()
        type(f1) #<class 'generator'>
        type(f2) #<class 'generator'>
        type(f3) #<class 'int'>
        type(f4) #<class 'NoneType'>
        type(f5) #<class 'NoneType'>
        type(f6) #<class 'generator'>
    ˵���� 
        ��ִ���� f1=func()ʱ����û�д�ӡ��"---1---"
        ������ִ�� f4=func4()ʱ������"abc"��ӡ�����
        ��˵����f1=func()ʱ����func()�У���һ�����ִ��ǰ
        ��ִ����һ����Ҳ�����Ƕ�����������䣬
        ��������䷵����generator����
        ��ִ�����һ��next(f1)�󣬲Ż�����"---1---"�����
        ���⣬��f6=func6()�п��Է��֣�
        ������������֧��Ƕ�׷��صģ����ص�������Ȼ�ǵ���������
    