# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier


class ResponseDescriptor:
    """存储属性与托管属性名称保持一致，可以不用实现__get__协议"""

    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        instance.__dict__[self.storage_name] = value


class RspJson:
    # 使用描述符管理实例属性
    code = ResponseDescriptor("code")
    data = ResponseDescriptor("data")
    msg = ResponseDescriptor("msg")

    def __init__(self, code=-1, data=None, msg=""):
        self.code = code
        self.data = {} if data is None else data
        self.msg = msg

    @property
    def result(self):
        return {
            "code": self.code,
            "data": self.data,
            "msg": self.msg,
        }
