# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : views.py
# @Project : Flask-Demo
<<<<<<< HEAD:ProjectStruct-1/FlaskAppFile/views.py
def indexView():
=======
from flask import render_template
from proStruct import app


@app.route('/', methods=['get'])
def index():
>>>>>>> 8ad499873906fa020ec77180e6f503ad800db241:ProjectStruct-1/proStruct/views.py
    return "<h1>Hello World!!</h1>"


@app.route('/index', methods=['get'])
def nextPage():
    return render_template('base.html')
