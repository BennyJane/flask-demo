# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : Flask-Demo

from flask import Flask

app = Flask(__name__)


# 必须将试图函数全部引入到__init__文件内 ==》 将视图函数引入到app实例化的文件内
from FlaskAppFile import views

if __name__ == '__main__':
    app.run()
