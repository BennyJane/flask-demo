# -*- coding: utf-8 -*-
# @Time : 2020/10/10
# @Author : Benny Jane
# @Email : 暂无
# @File : www.py
# @Project : ProjectStruct-1

from .routes import index_bp
from .routes.api import api_bp


def register_blueprint(app):
    app.register_blueprint(index_bp, url_prefix='/index')
    app.register_blueprint(api_bp, url_prefix='/api')
