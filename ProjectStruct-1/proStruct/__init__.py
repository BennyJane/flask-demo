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
# from flask_sqlalchemy import get_debug_queries

from proStruct import views
from .command import register_cli
from .extensions import register_ext, db
from .log import register_logging
from .errors import register_errors
from .models.model import Book
from .settings import config
from .www import register_blueprint


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_logging(app)
    register_ext(app)
    register_blueprint(app)
    register_cli(app, db)  # 需要在db绑定app后在执行
    register_errors(app)

    # flask 钩子 before_request
    # register_request_handlers(app)
    # 非必须==> 如何不适用 模板| shell，可以添加
    register_shell_context(app)
    register_template_context(app)

    if len(app.view_functions.keys()) < 2:
        # 确保初始化项目的时候存在一个视图页面; flask 默认添加有  static路由
        with app.app_context():
            app.add_url_rule('/', endpoint='/', view_func=views.index)
    return app


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        '''将db，数据模型类直接传入shell上下文， 便于调试； 不要再手动引入'''
        return dict(db=db, Book=Book)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        book = Book.query.first()
        customValue = '传入模板中直接使用的变量|函数；最后return对象必须是dict'
        return dict(book=book, customValue=customValue)

# def register_request_handlers(app):
#     @app.after_request
#     def query_profiler(response):
#         '''处理查询时间过长的问题'''
#         for q in get_debug_queries():
#             if q.duration >= app.config['BLUELOG_SLOW_QUERY_THRESHOLD']:
#                 app.logger.warning(
#                     'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
#                     % (q.duration, q.context, q.statement)
#                 )
#         return response
