# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 15:26:20 2018

@author: 46362
"""


print("First...")
class MyType(type):
    print("MyType begin ...")
    def __init__(self, *args, **kwargs):
        print("Mytype __init__", self, *args, **kwargs , sep="\r\n", end="\r\n\r\n")
        type.__init__(self, *args, **kwargs)  # 调用type.__init__
        
    def __call__(self, *args, **kwargs):
        print("Mytype __call__", *args, **kwargs)
        obj = self.__new__(self)   # 第一个self是Foo，第二个self是F("Alex")
        print("obj ",obj, *args, **kwargs)
        print(self)
        self.__init__(obj,*args, **kwargs)
        return obj
    
    def __new__(cls, *args, **kwargs):
        print("Mytype __new__", cls, *args, **kwargs, sep="\r\n", end="\r\n\r\n")
        return type.__new__(cls, *args, **kwargs)
    print("MyType end ...")
    
print('Second...')
class Foo(metaclass=MyType):
    print("begin...")
    def __init__(self, name):
        self.name = name
        print("Foo __init__")
        
    def __new__(cls, *args, **kwargs):
        print("Foo __new__", end="\r\n\r\n")
        return object.__new__(cls)
    print("over...")
    
    def __call__(self, *args, **kwargs):
        print("Foo __call__", self, *args, **kwargs, end="\r\n\r\n")
    
print("third...")
f = Foo("Alex")
print("f",f, end="\r\n\r\n")
f()
print("fname",f.name)

"""
First...
MyType begin ...
MyType end ...
Second...
begin...
over...
Mytype __new__
<class '__main__.MyType'>
Foo
()
{'__module__': '__main__', '__qualname__': 'Foo', '__init__': <function Foo.__init__ at 0x10ad89268>, '__new__': <function Foo.__new__ at 0x10ad89488>, '__call__': <function Foo.__call__ at 0x10ad86ae8>}

Mytype __init__
<class '__main__.Foo'>
Foo
()
{'__module__': '__main__', '__qualname__': 'Foo', '__init__': <function Foo.__init__ at 0x10ad89268>, '__new__': <function Foo.__new__ at 0x10ad89488>, '__call__': <function Foo.__call__ at 0x10ad86ae8>}

third...
Mytype __call__ Alex
Foo __new__

obj  <__main__.Foo object at 0x10ae2ac88> Alex
<class '__main__.Foo'>
Foo __init__
f <__main__.Foo object at 0x10ae2ac88>

Foo __call__ <__main__.Foo object at 0x10ae2ac88>

fname Alex

"""