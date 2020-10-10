# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : views.py
# @Project : Flask-Demo
from flask import render_template
from proStruct import app


@app.route('/', methods=['get'])
def index():
    return "<h1>Hello World!!</h1>"


@app.route('/index', methods=['get'])
def nextPage():
    return render_template('base.html')
