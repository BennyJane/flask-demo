# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
from flask import Flask
from flask import after_this_request
from pprint import pprint

app = Flask(__name__)
"""
========================================
Flask中响应对象被创建，并在一个可能的回调链中传递，
而该回调链中任意一个回调，都可以修改修改或替换响应结果


- 在视图函数内部使用该装饰器: after_this_request
- 多装饰器调用顺序： 按照定义顺序，从上往下执行
========================================
"""


@app.route("/")
def index():
    @after_this_request
    def callback(response):
        pprint(vars(response))  # 查看response类的属性
        # 新增返回值内容
        new_response_text = b"   -->   execute callback function"
        # 重新设置返回内容长度
        response.headers['Content-Length'] = len(new_response_text) + int(response.headers['Content-Length'])
        # 在返回值中添加新的内容
        response.response.append(new_response_text)
        print("running callback...")
        return response

    @after_this_request
    def callback2(response):
        print("running callback2...")
        return response

    print("running index view...")
    return "after_this_request test"


if __name__ == '__main__':
    app.run(debug=True)
