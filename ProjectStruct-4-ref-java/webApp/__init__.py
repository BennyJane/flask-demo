# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
import os
from flask import Flask
from flask import url_for

from config import projectConfigs
from .extensions import register_ext
from .log import register_logging
from .hooks import register_hooks
from .apis import register_routes_apis
from .errors import register_errors
from .views import register_route_views


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(projectConfigs[config_name])

    register_errors(app)
    register_ext(app)  # 绑定扩展
    register_logging(app)  # 添加日志功能
    register_hooks(app)  # 添加中间间
    register_routes_apis(app)  # 添加api模块
    register_route_views(app)  # 添加视图模块

    # 添加默认视图；实际开发过程中可以删除
    @app.route("/")
    def index():
        return f"<h1>项目模块</h1> <h2>视图模块： <a href='{url_for('index.index')}'>go</a></h2><h2>API模块： <a href='{url_for('api_v1.index')}'>go</a></h2>"

    return app  # 必须返回Flask实例
