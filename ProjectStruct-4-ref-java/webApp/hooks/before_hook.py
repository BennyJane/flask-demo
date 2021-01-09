# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier

"""
========================================
在第一请求触发前执行（服务器启动后，只会执行一次；注意：每个app启动都会执行一次）
========================================
"""


def before_first_request_f():
    """在第一请求触发前执行"""


def before_first():
    """return非空对象，会直接返回，不再调用视图函数"""
    return None
