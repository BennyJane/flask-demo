# -*- coding: utf-8 -*-
# @Time : 2020/10/23
# @Author : Benny Jane
# @Email : 暂无
# @File : base02.py
# @Project : Flask-Demo

from abc import ABCMeta


class test1(object):
    __metaclass__ = ABCMeta

    def test1(self):
        print('test1')


class UpperAttrMetaclass(type):

    def __new__(cls, name, bases, dct={}):
        a = super(UpperAttrMetaclass, cls).__new__(cls, name, l, dct)
        return a


b = UpperAttrMetaclass('hehe', (test1,), {})(3)
