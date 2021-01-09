# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
from flask import g
from flask import Flask
from flask import request
from flask import after_this_request
from pprint import pprint

app = Flask(__name__)

"""
========================================
Flask中响应对象被创建，并在一个可能的回调链中传递，
而该回调链中任意一个回调，都可以修改修改或替换响应结果


旧版本的实现方法：
- 借助g，存储回调函数链
- 在after_request注册函数内依次调用该回调链中的函数
========================================
"""


@app.route("/")
def index():
    print("running index view...")
    return "after_this_request test"


@app.route("/test")
def test():
    print("running test view...")
    return "after_this_request test"


# TODO 模仿Flask中 after_request等钩子函数的内存存储方式： 列表
def custom_after_this_request(f):
    if not hasattr(g, "after_request_callbacks"):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f


@app.before_request
def detect_user_language():
    print("running before_request...")
    language = request.cookies.get("user_lang")
    if language is not None:
        language = "zh"

        @custom_after_this_request
        def remember_language(response):
            print("running remember_language callback...")
            response.set_cookie("user_lang", language)
            return response
    g.language = language


# 在每个函数执行结束后都会遍历回调函数列表，并执行
@app.after_request
def call_after_request_callbacks(response):
    print("running after_request start ...")
    for callback in getattr(g, "after_request_callbacks", []):
        response = callback(response)
    print("running after_request end ...")
    return response


if __name__ == '__main__':
    app.run(debug=True)
