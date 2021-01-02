# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2021/1/1 11:41
# Warning    ：The Hard Way Is Easier


# TOOD Flask中views.py源码分析
from flask import request

http_method_funcs = frozenset(
    ["get", "post", "head", "options", "delete", "put", "trace", "patch"]
)


class View(object):
    methods = []
    provide_automatic_options = None
    decorators = ()

    def dispatch_request(self):
        raise NotImplementedError

    # 实用类方法，不需要实例化即可调用
    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):

        def view(*args, **kwargs):
            # FIXME 实例化当前类，必须实例化后，才能调用dispatch_request方法
            # 如果重写了__init__实例方法，则需要在调用as_view时，传入实例化所需要的参数
            self = view.view_class(*class_args, **class_kwargs)
            return self.dispatch_request(*args, **kwargs)  # dispatch_request 就是与实际路由绑定的视图函数

        # 手动调用装饰器函数
        if cls.decorators:
            view.__name__ = name
            view.__module__ = cls.__module__
            for decorator in cls.decorators:
                view = decorator(view)

        # 更新函数属性，
        view.view_class = cls
        view.__name__ = name
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        view.methods = cls.methods
        view.provide_automatic_options = cls.provide_automatic_options
        return view


# 元类，元编程： 在模块加载时，更新子类的类属性
class MethodViewType(type):
    """重写元类的__init__方法"""

    def __init__(cls, name, bases, d):
        """
        cls： 指元类的实例，当前环境下就是 MethodVIew
        :param name: 当前模块中继承MethodViewType的子类名称，当前环境下就是 MethodVIew
        :param bases: 父类元组，当前环境下就是 View
        :param d: 类属性
        """
        super(MethodViewType, cls).__init__(name, bases, d)  # 调用元类的__init__方法，确保类创建类的流程实现
        print("methodviewtype", cls, name, bases, d)

        # 如果待创建类中没有methods属性，则自动生成
        if "methods" not in d:
            methods = set()

            for base in bases:
                if getattr(bases, 'methods', None):
                    methods.update(bases.methods)

            # 检查
            for key in http_method_funcs:
                if hasattr(cls, key):
                    methods.add(key.upper())

            if methods:
                cls.methods = methods


def with_metaclass(meta, *bases):
    """使用metaclass类创建一个基类"""

    # 实现了一个中间层基类(元类 temporary_class), 继承自MethodViewType, View
    class metaclass(type):
        def __new__(metacls, name, this_bases, d):
            print('__new__', metacls, name, meta, bases, d)
            return meta(name, bases, d)  # 调用

    print(meta, *bases)
    middle_class = type.__new__(metaclass, "temporary_class", (), {})
    print('middle_class', middle_class, middle_class.mro(), type(middle_class))
    # 非绑定调用metaclass的__new__方法，查看middle_class的元类，可知其继承自metaclass
    return type.__new__(metaclass, "temporary_class", (), {})
    # return metaclass("temporary_class", (), {})
    # return middle_class


class MethodView(with_metaclass(MethodViewType, View)):
    """继承的元类MethodViewType，使得MethodView不需要手动维护methods属性；
       元类会自动将同名的方法，添加到methods属性内
    """

    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)

        # If the request method is HEAD and we don't have a handler for it
        # retry with GET.
        if meth is None and request.method == "HEAD":
            meth = getattr(self, "get", None)

        assert meth is not None, "Unimplemented method %r" % request.method
        return meth(*args, **kwargs)


class MyView(MethodView):
    def get(self):
        return "hello world!!"


if __name__ == '__main__':
    # print(MethodView.__class__.__class__)
    # print(type(MethodView))
    # print(MethodView.__mro__)
    # print(MethodView.mro())

    print(getattr(MyView, "methods"))
    pass
