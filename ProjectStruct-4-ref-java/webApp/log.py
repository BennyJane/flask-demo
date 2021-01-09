# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
import os
import logging
from logging.handlers import RotatingFileHandler
from _compat import root_path

project_name = os.path.split(os.path.dirname(__file__))[1]


def register_logging(app):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_path = os.path.join(root_path, f'logs/{project_name}')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    file_handler = RotatingFileHandler("{}/web.log".format(log_path),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # 需要设置整个日志的等级，开发调试模式下，默认为debug； 没有设置会导致无法输出日志
    app.logger.setLevel(logging.DEBUG)
    if not app.debug:
        # 生产模式下，需要设置合适等级
        # app.logger.setLevel(logging.ERROR)
        app.logger.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
