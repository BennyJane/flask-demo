# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/24 11:44
# Warning    ：The Hard Way Is Easier
from flask import Flask

app = Flask(__name__)

"""使用类实现中间件"""


class MyMiddleWare:
    """每次视图函数被调用都会触发该请求"""

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        def custom_response(status, headers, exc_info=None):
            res = start_response(status, headers)  # 执行触发的视图函数
            return res

        print("【class】before request ...")
        result = self.wsgi_app(environ, custom_response)
        print("【class】 after request ...")
        return result


app.wsgi_app = MyMiddleWare(app.wsgi_app)

"""使用闭包函数实现中间件"""


def middleFunc(app):
    wsgi_app = app

    def wrapper(environ, start_response):
        def custom_response(status, headers, exc_info=None):
            res = start_response(status, headers)  # 执行触发的视图函数
            return res

        print("【function】 before request ...")
        result = wsgi_app(environ, custom_response)
        print("【function】 after request ...")
        return result

    return wrapper


app.wsgi_app = middleFunc(app.wsgi_app)


@app.route("/")
def index():
    print("this is index")
    return "hello world!"


if __name__ == '__main__':
    app.run(debug=True)
