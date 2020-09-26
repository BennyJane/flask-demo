# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py
# @Project : Flask-Demo


from flask import Flask

from settings import FLASK_ENV, SECRET_KEY

app = Flask(__name__)
app.config['FLASK_ENV'] = FLASK_ENV
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    return "<h5>__init__.py内完成Flask的实例化 .flaskenv:</h5><h1>FLASK_APP=demo</h1>"
