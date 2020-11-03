import functools

"""
todo
# 添加redis缓存方法
# python内置的缓存函数?? <流畅的python内有讲解>
"""


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
        self.watch = watch

    def __call__(self, *args, **kwargs):
        key = [args, frozenset(kwargs.items())]
        if self.is_method:
            key.append(tuple([getattr(args[0], v, None) for v in self.watch]))
        print("key", key)
        key = tuple(key)
        if key in self.cache:
            return self.cache[key]
        try:
            print("running func")
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
        print("__get__", instance, owner)
        return functools.partial(self.__call__, instance)


def memoried(func=None, watch=None):
    if func:  # 被装饰的函数,直接返回类实例,替换原函数
        return _memoried(func)
    else:  # 被装饰的类方法, 返回装饰器 wrapper
        def wrapper(f):
            return _memoried(f, watch)

        return wrapper


@memoried
def add(x=10, y=20):
    s = x + y
    return s


class base:
    @memoried(watch=("x", ))
    def add(self, x=10, y=20):
        return x + y

    def div(self, x=10, y=20):
        return x / y

    # def __call__(self, *args, **kwargs):
    #     super.__call__(*args, **kwargs)
    #     print("__call__", self)


r = add(5, 6)
print(r)
print(add(5, 6))

b = base()
# b()


print(b.div())
r2 = b.add()
print(r2)
print(b.add())

# 参考文章
'''
https://blog.csdn.net/q389797999/article/details/92090200
https://www.cnblogs.com/flashBoxer/p/9771797.html
https://www.cnblogs.com/wickedpriest/p/11984887.html
https://www.cnblogs.com/andy1031/p/10923834.html
'''
