# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning：The Hard Way Is Easier
import os

from .development import DevelopmentConfig
from .production import ProductionConfig

projectConfigs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}


def get_config_from_env(config_name=None):
    """根据环境变量获取当前配置信息"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
        if config_name not in projectConfigs.keys():
            config_name = 'development'
    return projectConfigs[config_name]
