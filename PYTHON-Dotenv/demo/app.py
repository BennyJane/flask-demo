# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : demo.py
# @Project : Flask-Demo

from flask import Flask

from settings import FLASK_ENV, SECRET_KEY

app = Flask(__name__)
app.config['FLASK_ENV'] = FLASK_ENV
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    return "<h5>app.py内完成Flask的实例化  .flaskenv:</h5><h1>FLASK_APP=demo.app</h1>"

# if __name__ == '__main__':
#     app.run(debug=True)
