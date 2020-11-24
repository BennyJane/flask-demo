import functools

"""
参考文章:
https://wiki.python.org/moin/PythonDecoratorLibrary#Collect_Data_Difference_Caused_by_Decorated_Function
"""


def singleton(cls):
    """Use class as singleton"""
    cls.__new_original__ = cls.__new__

    @functools.wraps(cls.__new__)
    def singleton_new(cls, *args, **kwargs):
        instance = cls.__dict__.get('__instance__')
        if instance is not None:
            return instance

        cls.__instance__ = instance = cls.__new_original__(cls, *args, **kwargs)
        instance.__init_original__(*args, **kwargs)
        return instance

    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__
    return cls


@singleton
class Foo:
    def __new__(cls, *args, **kwargs):
        cls.x = 10
        return object.__new__(cls)

    def __init__(self):
        assert self.x == 10
        self.x = 15


if __name__ == '__main__':
    assert Foo().x == 15
    Foo().x = 20
    assert Foo().x == 20
