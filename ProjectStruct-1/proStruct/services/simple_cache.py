import functools

"""
todo
# 添加redis缓存方法
# python内置的缓存函数?? <流畅的python内有讲解>
"""


# 类似于 @property的效果，实际上是实现了__get__的描述符
class _memoried(object):
    """自定义的本地缓存方法,使用字典存储
    使用场景:
    1. 缓存数据库查询对象
    2.
    """

    def __init__(self, func, watch=()):
        self.func = func
        self.cache = {}
        self.is_method = False
        self.watch = watch  # 用来添加非传入参数（非*arg, **kwargs）, 例如装饰类方法，在方法内直接调用self.attr属性

    def __call__(self, *args, **kwargs):
        key = [args, frozenset(kwargs.items())]
        if self.is_method:
            key.append(tuple([getattr(args[0], v, None) for v in self.watch]))
        key = tuple(key)
        if key in self.cache:
            return self.cache[key]
        try:
            value = self.func(*args, **kwargs)
            self.cache[key] = value
            return value
        except TypeError:
            return self.func(*args, **kwargs)

    def __repr__(self):
        """返回函数的文档字符串"""
        return self.func.__doc__

    def __get__(self, instance, owner):
        if not self.is_method:
            self.is_method = True
        """支持实例方法"""
        return functools.partial(self.__call__, instance)


def memoried(func=None, watch=None):
    """
    具体的使用方法：
        @memoried
        def add(x=10, y=20):
            s = x + y
            return s
        # 直接调用 add方法，不会触发 __get__ 方法
        r = add(5, 6)


        class base:
            @memoried(watch=("x", ))
            def add(self, x=10, y=20):
                return x + y
            @memoried
            def div(self, x=10, y=20):
                return x / y

        b = base()
        # 调用 __get__ 方法获取add属性
        b.add
        # 根据上一步返回，执行 __call__ 方法
        b.add(5 , 6)
    """
    if func:  # 被装饰的函数,直接返回类实例,替换原函数
        return _memoried(func)
    else:  # 被装饰的类方法, 返回装饰器 wrapper
        def wrapper(f):
            return _memoried(f, watch)

        return wrapper


# 参考文章
'''
https://blog.csdn.net/q389797999/article/details/92090200
https://www.cnblogs.com/flashBoxer/p/9771797.html
https://www.cnblogs.com/wickedpriest/p/11984887.html
https://www.cnblogs.com/andy1031/p/10923834.html
'''
