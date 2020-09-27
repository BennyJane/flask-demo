# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : demo.py
# @Project : Flask-Demo
import os
from pathlib import Path  # 该方法只能再 3.6以上版本使用

from dotenv import load_dotenv, find_dotenv

'''
github: https://github.com/theskumar/python-dotenv#setting-config-on-remote-servers
参数：
verbose: 当没有找到 .env文件的时候，是否报错
dotenv_path: 执行 .env文件的路径

Importation:
** 加载的环境变量都是字符串，如果需要 数值，布尔值等，需要自己转换
** .env 文件中不能出现中文，否则会报编码错误的
** 如果不明确指定文件路径，使用 [load_dotenv] 默认只会加载.env 文件，不会加载 .flaskenv文件
** 多次调用 [load_dotenv]， 加载的环境变量会合并，但同名的变量，取先加载的变量
** FLASK_APP 的值，指定了Flask实例化后的app的位置，如果在__init__.py 内，则为模块的名称； 如果在其他的py文件中，则需要写成 module.otherName
** 修改.env 内的文件，不会自动更新(在没有调用 load_dotenv的情况下)
'''
FLASK_ENV = os.getenv("FLASK_ENV")
SECRET_KEY = os.getenv("SECRET_KEY")
FLASKENV_TEST = os.getenv("FLASKENV_TEST")
print(FLASKENV_TEST)



class LoadEnvFile:
    @staticmethod
    def first():
        # 自动搜索 .env 文件
        load_dotenv(verbose=True, encoding='utf-8')

    @staticmethod
    def second():
        # 同上：
        # TODO find_dotenv() 方法默认只查找 .env 文件
        # load_dotenv(find_dotenv(), verbose=True, override=True)
        load_dotenv(find_dotenv('.flaskenv'), verbose=True, override=True)

    @staticmethod
    def third():
        # 指定。env 文件的位置
        env_path = Path('.env')  # ".env"
        load_dotenv(dotenv_path=env_path, verbose=True)
        env_path = Path('.flaskenv')
        load_dotenv(dotenv_path=env_path, verbose=True)


def example1():
    LoadEnvFile.first()

    ENV_TEST = os.getenv("ENV_TEST")
    # os.environ 也可以获取内容
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # TODO 默认只会加载 .env 文件内的环境变量 ==》 flask 运行时候会加载 .flaskenv文件
    FLASKENV_TEST = os.getenv("FLASKENV_TEST")
    print(locals())


def example2():
    LoadEnvFile.second()

    SECRET_KEY = os.getenv("FLASK_APP")
    ENV_TEST = os.getenv("FLASK_ENV")
    FLASKENV_TEST = os.getenv("FLASKENV_TEST")
    print(locals())


def example3():
    LoadEnvFile.third()

    SECRET_KEY = os.getenv("SECRET_KEY")
    ENV_TEST = os.getenv("ENV_TEST")
    FLASKENV_TEST = os.getenv("FLASKENV_TEST")
    print(locals())

# example3()
if __name__ == '__main__':
    example1()
    # example2()
    # example3()
