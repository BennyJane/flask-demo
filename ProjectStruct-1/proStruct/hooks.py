# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : ProjectStruct-1
# Time       ：2020/12/25 18:34
# Warning    ：The Hard Way Is Easier
def register_hooks(app):
    # 直接使用装饰器函数
    app.before_request(before_first)

    app.after_request(after_first)  # 请求成功，请求后触发的钩子函数


def before_first():
    """return非空对象，会直接返回，不再调用视图函数"""
    return None


def after_first(response):
    return response
