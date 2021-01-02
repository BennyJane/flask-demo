# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2021/1/2 23:37
# Warning    ：The Hard Way Is Easier

"""
模仿源码代码结构：


"""


class Metaclass(type):
    def __new__(cls, name, bases, d):
        print('__new__')
        # return super().__new__(cls, name, bases, d)
        return type.__new__(cls, name, bases, d)


middle_class = type.__new__(Metaclass, "temporary_class", (), {"name":"benny"})


class A(middle_class):
    pass


if __name__ == '__main__':
    print(A.name)
