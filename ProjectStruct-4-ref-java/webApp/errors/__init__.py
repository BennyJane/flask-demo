# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
from flask_wtf.csrf import CSRFError
from .http import bad_request
from .http import not_found
from .http import method_not_allowed
from .http import internal_server_error
from .http import allException


def register_errors(app):
    # 直接调用装饰器,实现请求处理
    app.errorhandler(400)(bad_request)
    app.errorhandler(404)(not_found)
    app.errorhandler(405)(method_not_allowed)
    app.errorhandler(500)(internal_server_error)
    # 全局异常捕获：用于捕获自定义异常以及未知异常
    app.errorhandler(Exception)(allException)
