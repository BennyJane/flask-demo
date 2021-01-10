# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
from pprint import pprint
from wsgiref.simple_server import make_server

"""
WSGI: Python Web server Gateway Interface, 让Web服务器与Python程序能够进行数据交流而定义的一套接口标准/规范

Web程序（或者被称为WSGI程序），基本要求： 
1. 必须是一个可调用对象，该可调用对象接收两个参数（由WSGI服务器在调用该可调用对象时，传入这两个参数）
    - environ: 包含了请求的所有信息的字典
    - start_response: 在可调用对象内被调用的函数，用于发起响应，参数时状态码、响应头部等
2. 可调用对象必须要返回一个可迭代对象（iterable）
"""


# 函数实现方式
def hello(environ, start_response):
    print("[environ]: ", environ)
    pprint(environ)
    status = '200 OK'
    response_headers = [("Content-type", "text/html")]
    print("[start_response]: ", start_response)
    start_response(status, response_headers)

    # 获取URL路径信息
    name = environ['PATH_INFO'] or "web"
    return [b"<h1>Hello, %s!</h1>" % name.encode()]


# 类实现方式
class AppClass:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):  # 类的可迭代性
        status = '200 OK'
        response_headers = [("Content-type", "text/html")]
        self.start(status, response_headers)
        yield b"<h1>Hello, Web!</h1>"


if __name__ == '__main__':
    server = make_server('localhost', 8001, hello)
    server.serve_forever()
