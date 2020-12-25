# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : career-planning-info
# Time       ：2020/12/15 20:08
# Warning    ：The Hard Way Is Easier
import traceback
from flask import current_app
from flask import render_template


def register_errors(app):
    # 直接调用装饰方法
    app.errorhandler(400)(bad_request)
    app.errorhandler(404)(page_not_found)
    app.errorhandler(500)(internal_server_error)
    app.errorhandler(Exception)(allException)


def bad_request(e):
    return render_template('errors/400.html'), 400


def page_not_found(e):
    return render_template('errors/404.html'), 404


def internal_server_error(e):
    return render_template('errors/500.html'), 500


def allException(e):  # 全局异常处理
    current_app.logger.debug(str(e))
    config = current_app.config
    if config.get("IS_DEBUG"):  # 开发模式下，打印输出异常发生的位置
        current_app.logger.debug(traceback.format_exc())
    return render_template('errors/500.html'), 500
