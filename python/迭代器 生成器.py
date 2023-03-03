迭代器
    iter(iterable) -> iterator
    iter(callable, sentinel) -> iterator
    参数说明：
        iterable：
            可迭代类，基本类型中的字符串、列表、元组、集合、字典都是可迭代类
            自定义类实现了__iter__()和__next__()方法（两者缺一不可）时，该类为迭代器类
                该类可以被for-in枚举，并可以作为iter()方法的参数，表明该类属于可迭代类型，
                用 isinstance(o,Iterator) 方法测试，返回为 True，表明该类属于迭代器类
                迭代器类属于可迭代类（子集）：
                    迭代器类不能通过index索引某个元素，不支持获取元素总个数，
                    只能通过next()单向前进
                    迭代器的这种流特性，使得它可以表示一个无限的数据流，如全体自然数
                    而这是用list所不能实现的
                #关于__iter__()和__next__()方法：
                __iter__函数向系统声明这个类可迭代，__next__定义了具体的迭代器，
                正式的说法是：
                实现了__iter__方法的对象是可迭代对象，实现了__next__方法的对象是迭代器
                在代码执行过程中，for循环函数会自动检查系统信息，识别__iter__函数，
                然后自动调用对应的__next__函数，生成一个迭代器
            自定义的类，如果定义了iter()方法或getitem()方法，该类为可迭代类
                经测试，自定义类如果只实现了__getitem__成员方法，
                该类可以被for-in枚举，并可以作为iter()方法的参数，表明该类属于可迭代类型，
                但用 isinstance(o,Iterator) 方法测试，返回为 False，表明该类不是迭代器类，
                对字符串、列表、集合等类型用 isinstance(o,Iterator) 方法测试，返回为 False
                表明这些类型都只是可迭代类，但不是迭代器类
                猜测这些容器类型内部，也是只实现了__getitem__成员方法
                进一步说，list、tuple、dict、set、str，及实现了getitem()方法的自定义类，
                都可统一称之为‘集合类型’，他们提供了按索引号获取元素的手段。
    测试自定义可迭代类：
        测试一：
            from collections import Iterable
            class myclass_1:
                def __init__(self,*args):
                    self._list=[1,2,3,4]
                    self._index=0
                def __getitem__(self,index):
                    return self._list[index%4-1]  #对返回数据类型不限制
            c1 = myclass_1()
            for i in c1: print(i)       #会循环输出1、2、3、4
            iter(c1)                    #不报错
        测试二：
            from collections import Iterable
            class myclass_2:
                def __init__(self,*args):
                    self._list=[1,2,3,4]
                    self._index=0
                def __iter__(self):
                    return self         #要求返回的是可迭代对象类型
                def __next__(self):     #该方法必须配合__ter__方法而存在
                    self._index=self._index+1
                    if self._index>4:
                        self._index=1
                    return self._list[self._index%4-1]
            c2 = myclass_2()
            for i in c2:  print(i)      #会循环输出1、2、3、4
            iter(c2)                    #不报错
            经测试，__next__()方法必须存在，否则在后面使用for-in与iter()时会报错
            报错信息：iter() returned non-iterator of type 'myclass_2'
        测试三：
            测试代码（对测试一、测试二的整合与扩展）
                from collections.abc import Iterator
                #0. 定义函数，对参数进行测试
                def tell(o):
                  if isinstance(o,Iterator): 
                      print("{0} is Iterator".format(type(o)))
                  else:
                      print("{0} is not Iterator".format(type(o)))
                  try:
                      print("for迭代结果: ",end='')
                      for i in o:  
                          print(i,end='  ')       #会循环输出1、2、3、4
                      print("\n")
                  except:
                      print("\n")
                  iter(o)                         #不报错
                #1. 定义迭代器类1，并进行测试
                class myclass_1:
                    def __init__(self,*args):
                        self._list=[1,2,3,4]
                        self._index=1
                    def __getitem__(self,index):
                        if index>4:
                            raise StopIteration()
                        return self._list[index]  #对返回数据类型不限制
                c1 = myclass_1()
                tell(c1)
                #2. 定义迭代器类2，并进行测试
                class myclass_2:
                    def __init__(self,*args):
                        self._list=[1,2,3,4]
                        self._index=0
                    def __iter__(self):
                        return self         #要求返回的是可迭代对象类型
                    def __next__(self):     #该方法必须配合__ter__方法而存在
                        self._index=self._index+1
                        if self._index>4:
                            raise StopIteration()
                        return self._list[self._index%4-1]
                c2 = myclass_2()
                tell(c2)
                #3. 测试字符串
                c3="asdf"
                tell(c3)
                #4. 测试列表
                c4=[1,2,3,4]
                tell(c4) 
                #5. 测试集合
                c5={1,2,3,4,5}
                tell(c5)
            输出结果
                <class '__main__.myclass_1'> is not Iterator
                for迭代结果: 1  2  3  4
                <class '__main__.myclass_2'> is Iterator
                for迭代结果: 1  2  3  4
                <class 'str'> is not Iterator
                for迭代结果: a  s  d  f
                <class 'list'> is not Iterator
                for迭代结果: 1  2  3  4
                <class 'set'> is not Iterator
                for迭代结果: 1  2  3  4  5
            结果总结
                ● 自定义类1，只实现了__getitem__成员方法，
                该类可以被for-in枚举，并可以作为iter()方法的参数，
                表明该类属于可迭代类型，
                但用 isinstance(o,Iterator) 方法测试，返回为 False
                ● 自定义类2，实现了__iter__()和__next__()方法，
                该类可以被for-in枚举，并可以作为iter()方法的参数，
                表明该类属于可迭代类型，
                用 isinstance(o,Iterator) 方法测试，返回为 True
                ● 字符串、列表、集合等类型，属于可迭代类型
                但用 isinstance(o,Iterator) 方法测试，返回为 False
                猜测这些容器类型内部，只实现了__getitem__成员方法
                
生成器
    在 Python 中，使用了 yield 的函数被称为生成器（generator）
    举例：
        def func():
            print("---1---")
            yield 1    #yield会把后面的数据包装成generator对象进行返回
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
    说明： 
        当执行完 f1=func()时，并没有打印出"---1---"
        而像如执行 f4=func4()时，是有"abc"打印输出的
        这说明在f1=func()时，在func()中，第一条语句执行前
        就执行了一条（也可能是多条）隐藏语句，
        该隐藏语句返回了generator对象
        当执行完第一条next(f1)后，才还是有"---1---"输出。
        另外，从f6=func6()中可以发现，
        迭代器函数是支持嵌套返回的，返回的类型仍然是迭代器对象
    