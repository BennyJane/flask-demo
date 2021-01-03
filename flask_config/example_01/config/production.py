# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/4 11:09
# Warning：The Hard Way Is Easier
from .base import BaseConfig


class ProductionConfig(BaseConfig):
    SERVER_PORT = 8000
    SERVER_HOST = '119.185.2.1'
    DEBUG = False
    CONFIG_NAME = 'PRODUCTION'
