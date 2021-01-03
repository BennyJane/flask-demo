# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from .base import BaseConfig



class DevelopmentConfig(BaseConfig):
    SERVER_PORT = 5000
    SERVER_HOST = '127.0.0.1'
    DEBUG = True
    CONFIG_NAME = 'DEVELOPMENT'

