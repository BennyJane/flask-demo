# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
import os
import sys

__all__ = ["win", "modifyPath", "root_path", "sqlite_prefix",
           "get_key_form_env"
           ]


def isWindows():
    window_platform = False
    if sys.platform.startswith('win'):
        window_platform = True
    return window_platform


win = isWindows()


def modifyPath(relativePath: str) -> str:
    """
    :param relativePath:  目标文件的相对路径,默认输入linux下路径: logs/api; 开头不能有斜杠
    :return:
    """
    if win:
        path = '\\'.join(relativePath.split('\/'))
    else:
        path = '/'.join(relativePath.split('\\'))
    return path


root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# linux与windows下斜杠数量不同： linux 4 win 3
sqlite_prefix = 'sqlite:///' if win else 'sqlite:////'


# 从环境变量中获取key的值
def get_key_form_env(key):
    return os.getenv(key, None)
