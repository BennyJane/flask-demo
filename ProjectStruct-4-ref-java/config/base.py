# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
import os
from _compat import sqlite_prefix
from _compat import root_path as project_root_path


class BaseConfig:
    PROJECT_NAME = "web-common-service"
    HOST = '127.0.0.1'
    PORT = '8001'

    JSON_AS_ASCII = False  # 默认Flask返回JSON，会将中文转化为Ascii字符，需要关闭

    SESSION_KEY = 'BENNY JANE'
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = sqlite_prefix + ':memory'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # 支持上传的文件类型
    UPLOAD_TYPE = ('image', 'doc', 'video')
    UPLOAD_ALLOW_TYPE = {
        "image": ("png", 'jpg', 'gif', 'webp'),
        "doc": ('doc', 'docx', 'pdf', 'csv', 'xls'),
        "video": (),
    }

    UPLOAD_PATH = os.path.join(project_root_path, 'uploads')

    # 接口白名单
    WHITE_PAI_LIST = [
        'static',
    ]
