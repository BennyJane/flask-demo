# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
from .before_hook import before_first
from .before_hook import before_first_request_f
from .after_hook import after_first


def register_hooks(app):
    # 直接使用装饰器函数
    """
    ========================================
    在第一次请求处理之前被执行 （服务器启动后，只会执行一次；注意：每个app启动都会执行一次）
    TIP: 可以实现一些初始化操作，但需要考虑使用分布式锁
    ========================================
    """
    # app.before_first_request(before_first_request_f)

    """
    ========================================
    执行视图函数前，触发的钩子函数
    ========================================
    """
    app.before_request(before_first)

    """
    ========================================
    请求成功，请求后触发的钩子函数
    ========================================
    """
    # app.after_request(after_first)
