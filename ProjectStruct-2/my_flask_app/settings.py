# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env

'''
当前配置方式特点： 主要配置文件都是从.env配置中读取， 
开发，部署，测试需要各自维护一个.env文件，内容各自不同；


==》 更合理：将需要修改的，私密变量通过.env来维护，其他三种情况下相同的变量，公用一套变量
'''


env = Env()
# 遍历
# 参数： path 指定目录， recurse 是否递归查找.env文件
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
# 非开发模式需要注释该行代码
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
SECRET_KEY = env.str("SECRET_KEY")
SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT")
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
# redis配置
CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False
