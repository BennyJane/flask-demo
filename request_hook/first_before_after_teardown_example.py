# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    # raise Exception("test error..")
    return "request hook example..."


@app.before_first_request
def before_first_f():
    print("before_first_request")


"""
========================================
before_request: 内部使用数组存储，使用append添加；执行的时候，按照绑定顺序执行
========================================
"""


@app.before_request
def before_request_f():
    print("before_request 1")


@app.before_request
def before_request_f2():
    print("before_request 2")


"""
========================================
before_request: 内部使用数组存储，使用append添加；执行的时候，按照绑定的相反顺序执行
！！内部使用reversed()颠倒了顺序
========================================
"""


@app.after_request
def after_request_f(response):
    print("after_request 1")
    return response


@app.after_request
def after_request_f2(response):
    print("after_request 2")
    return response


"""
========================================
teardown_request: 内部使用数组存储，使用append添加；执行的时候，按照绑定的相反顺序执行
！！内部使用reversed()颠倒了顺序
- 必须接受一个参数，其实就是异常信息；可用于处理异常信息
- 不需要有返回值
- DEBUG=True情况下，不会发生作用；视图函数出现异常后直接抛出错误，after_request teardown_request都不会执行
- DEBUG=False情况下，有作用，视图函数出现异常后，after_request teardown_request仍然会被执行
========================================
"""


@app.teardown_request
def teardown_f(e):
    print("teardown_request")
    print(str(e))


@app.teardown_request
def teardown_f2(e):
    print("teardown_request 2")
    print(str(e))


if __name__ == '__main__':
    app.run(debug=True)
