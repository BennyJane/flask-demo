# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : views.py
# @Project : Flask-Demo

from simpleApp import app


@app.route('/', methods=['get'])
def index():
    return "<h1>Hello World!!</h1>"
