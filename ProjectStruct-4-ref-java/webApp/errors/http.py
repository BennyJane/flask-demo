# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
import traceback

from flask import request
from flask import jsonify
from flask import current_app
from flask import render_template

from .api_exception import RspJson

"""
========================================
兼容处理api模块与普通视图函数的异常情况
========================================
"""


def filter_api_error(code, msg, status_code):
    if request.path and "api" in request.path:
        req = RspJson(code=code, msg=msg)
        return jsonify(req.result), status_code


def bad_request(e):
    api_error = filter_api_error(1, "请求报错", 400)
    if not api_error:
        return render_template('errors/400.html', description=e.description), 400
    return api_error


def not_found(e):
    api_error = filter_api_error(1, "请求接口不存在", 404)
    if not api_error:
        return render_template('errors/404.html'), 404
    return api_error


def method_not_allowed(e):
    api_error = filter_api_error(1, "请求方式不支持", 405)
    if not api_error:
        return render_template('errors/405.html'), 405
    return api_error


def internal_server_error(e):
    api_error = filter_api_error(1, "服务器内部报错", 500)
    if not api_error:
        return render_template('errors/500.html'), 500
    return api_error


def allException(e):  # 全局异常处理

    error_info = str(e)
    config = current_app.config
    if config.get("DEBUG"):  # 开发模式下，打印输出异常发生的位置
        current_app.logger.debug(traceback.format_exc())
    api_error = filter_api_error(1, error_info, 500)
    if not api_error:
        return render_template('errors/500.html', error_info=error_info), 500
    return api_error
