# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : cli.py
# @Project : Flask-Demo
import logging
import os
from _compat import modifyPath
from config import get_config_from_env
from logging.handlers import RotatingFileHandler

basedir = os.path.abspath(os.path.dirname(__file__))


def register_logging(config_name=None):
    current_env = os.getenv('FLASK_ENV', 'development')
    config = get_config_from_env()
    log_file_path = config.LOG_FILE_PATH
    log_level = config.LOG_LEVEL
    log_file_size = config.LOG_FILE_SIZE
    log_file_count = config.LOG_FILE_COUNT

    logger = logging.getLogger(config.PROJECT_NAME)

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s [%(module)s.%(filename)s %(lineno)s] [%(levelname)s] : %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    log_path = os.path.split(log_file_path)[0]
    if not os.path.exists(modifyPath(log_path)):
        os.makedirs(log_path)
    if log_file_path and current_env == 'produce':
        handler = RotatingFileHandler(log_file_path, maxBytes=log_file_size, backupCount=log_file_count)
    elif log_level is None:
        logger.handlers = [logging.NullHandler()]
        return logger
    if current_env == 'development':
        handler = logging.StreamHandler()

    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    logger.handlers = [handler]
    return logger


