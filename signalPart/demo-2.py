# -*- coding: utf-8 -*-
# @Time : 2020/10/22
# @Author : Benny Jane
# @Email : 暂无
# @File : demo-1.py
# @Project : Flask-Demo

from flask import Flask, signals, request
from flask.signals import Namespace

app = Flask(__name__)

'''
自定义信号：
- 将信号定义在Flask默认的命名空间内
from flask.signals import _signals
custom_signal = _signals..signal('custom-signal')

- 将信号定义在自定的命名空间内
from flask.signals import Namespace

_signals = Namespace()

#: Sent when a user is logged in. In addition to the app (which is the sender), it is passed `user`, which is the user being logged in.
user_logged_in = _signals.signal('logged-in')
'''

# 实例化命名空间
_signal = Namespace()
# 自定义一个信号
customSignal = _signal.signal('custom-signal')


# 触发信号要执行的函数
def sig(*args, **kwargs):
    # 可以接受send（）函数传入的参数
    print(f'触发信号函数： {sig.__name__}， 参数：', args, kwargs)


# 设置信号触发的回调函数；
# 设置 receiver
customSignal.connect(sig)


@app.route("/")
def index():
    print(f'正在执行的视图函数： {index.__name__}')
    print('index视图函数中传入参数：', request.args)
    customSignal.send('only-one-position', name='index', status='request')
    return 'index'


if __name__ == '__main__':
    app.run(debug=True)
