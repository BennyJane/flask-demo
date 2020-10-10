# -*- coding: utf-8 -*-
# @Time : 2020/10/10
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : ProjectStruct-1

from .index import index_bp

'''
可以在这里管理整个routes包内的所有蓝图, 
但单独提取出来放到www模块中统一管理所有模块的蓝图， 方便管理
'''


def init_app(app):
    app.register_blueprint(index_bp, url_prefix='/index')
