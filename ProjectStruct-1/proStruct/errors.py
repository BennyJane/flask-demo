# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : errors.py
# @Project : Flask-Demo
import traceback
from flask import current_app
from flask import render_template
from flask_wtf.csrf import CSRFError


def register_errors(app):
    # 直接调用装饰器
    app.errorhandler(400)(bad_request)
    app.errorhandler(404)(not_found)
    app.errorhandler(405)(method_not_allowed)
    app.errorhandler(500)(internal_server_error)
    app.errorhandler(CSRFError)(handle_csrf_error)
    app.errorhandler(Exception)(allException)  # 全局异常捕获


def handle_csrf_error(e):
    return render_template('errors/400.html', description=e.description), 400


def bad_request(e):
    return render_template('errors/400.html'), 400


def not_found(e):
    return render_template('errors/404.html'), 404


def method_not_allowed(e):
    return render_template('errors/405.html'), 404


def internal_server_error(e):
    return render_template('errors/500.html'), 500


def allException(e):  # 全局异常处理
    error_info = str(e)
    config = current_app.config
    if config.get("IS_DEBUG"):  # 开发模式下，打印输出异常发生的位置
        current_app.logger.debug(traceback.format_exc())
    return render_template('errors/500.html', error_info=error_info), 500
