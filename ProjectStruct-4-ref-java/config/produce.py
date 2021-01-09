# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import os
import logging
from .base import BaseConfig
from _compat import modifyPath
from _compat import sqlite_prefix
from _compat import root_path as project_root_path


class ProduceConfig(BaseConfig):
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = '8001'

    # 日志配置
    LOG_FILE_PATH = os.path.join(project_root_path, modifyPath('logs/web/web_common.log'))
    LOG_LEVEL = logging.INFO  # 日志登记
    LOG_FILE_SIZE = 10 * 1204 * 1024
    LOG_FILE_COUNT = 10

    # MYSQL数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    if not SQLALCHEMY_DATABASE_URI:  # 没有添加mysql数据库连接时，创建sqlite数据库连接
        SQLALCHEMY_DATABASE_URI = sqlite_prefix + os.path.join(project_root_path, 'data-dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENCODING = "utf8mb4"
