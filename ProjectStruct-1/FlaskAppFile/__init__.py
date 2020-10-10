# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : Flask-Demo
import os
from flask import Flask
from FlaskAppFile.settings import config
# 非蓝图视图函数的引进来，再通过add_url_rule来进行绑定 todo 使用current_app 会报错
from FlaskAppFile.views import indexView



def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    with app.app_context():
        app.add_url_rule('/', endpoint='/', view_func=indexView)
    return app