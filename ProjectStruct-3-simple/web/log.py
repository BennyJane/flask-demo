# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : command.py
# @Project : Flask-Demo
import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import request

basedir = os.path.abspath(os.path.dirname(__file__))
project_name = os.path.split(os.path.dirname(__file__))[1]


def register_logging(app):
    class RequestFormatter(logging.Formatter):
        # 通过继承，修改打印信息： 报错的url 与 远程地址
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_path = os.path.join(basedir, f'logs/{project_name}')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    file_handler = RotatingFileHandler(os.path.join(log_path, f'logs/{project_name}.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)

    '''
    ====================================================================================================
    添加邮件通知任务
    ====================================================================================================
    '''

    mailhost = app.config.get('MAIL_SERVER', '')
    fromaddr = app.config.get('MAIL_USERNAME', '')
    toaddrs = app.config.get('ADMIN_EMAIL', '')

    if all([mailhost, fromaddr, toaddrs]):
        mail_handler = SMTPHandler(
            mailhost=mailhost,
            fromaddr=fromaddr,
            toaddrs=toaddrs,
            subject='Bluelog Application Error',
            credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(request_formatter)
        if not app.debug:
            app.logger.addHandler(mail_handler)
