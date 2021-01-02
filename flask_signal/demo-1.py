# -*- coding: utf-8 -*-
# @Time : 2020/10/22
# @Author : Benny Jane
# @Email : 暂无
# @File : example.py
# @Project : Flask-Demo

"""
想要使用flask的信号得先安装插件
pip install blinker

"""

from flask import Flask, signals, request

app = Flask(__name__)


# 触发信号要执行的函数
def sig(*args, **kwargs):
    print('request args', request.args.to_dict())
    print('触发这个信号', args, kwargs)


# 给你要连接的函数绑定信号的类型（这里就举一个例子）
signals.request_started.connect(sig)


@app.route('/<num:int>')
@app.route('/')
def index(num):
    print('starting request')
    print('request args', request.args)
    print(request.data)
    print(request.values)
    print(num)
    return '123'


if __name__ == '__main__':
    app.run(debug=True)
