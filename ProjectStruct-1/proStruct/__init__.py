# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : Flask-Demo
import os

from flask import Flask
# 非蓝图视图函数的引进来，再通过add_url_rule来进行绑定 todo 使用current_app 会报错
# 必须将试图函数全部引入到__init__文件内 ==》 将视图函数引入到app实例化的文件内
from config import projectConfigs
from proStruct import views
from .cli import register_cli
from .extensions import register_ext, db
from .log import register_logging
from .errors import register_errors
from .models.model import Book
from .www import register_blueprint
from .hooks import register_hooks
from .template_ext import register_template_ext


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", 'development')
    app = Flask(__name__)
    app.config.from_object(projectConfigs[config_name])

    register_logging(app)
    register_ext(app)
    register_blueprint(app)
    register_cli(app, db)  # 需要在db绑定app后在执行
    register_errors(app)

    register_hooks(app)
    register_template_ext(app)

    if len(app.view_functions.keys()) < 2:
        # 确保初始化项目的时候存在一个视图页面; flask 默认添加有  static路由
        with app.app_context():
            app.add_url_rule('/', endpoint='/', view_func=views.index)
    return app
