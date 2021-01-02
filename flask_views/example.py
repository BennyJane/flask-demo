import os
from flask import Flask
from flask import request
from flask.views import View
from flask.views import MethodView
from flask_bases.utils import decorator_log

app = Flask(__name__)
# 设置当前的环境变量
os.environ.setdefault("FLASK_ENV", "development")

"""
========================================================================================================================
继承MethodView来来实现视图函数，
可以直接编写(get post...)请求方法
========================================================================================================================
"""


class baseView(MethodView):
    decorators = [decorator_log]

    def get(self):
        res = request.args
        return "base view, age:{}".format(res.get("age"))

    def post(self):
        res = request.form
        input_data = ",".join(res.values())
        return f"base view post:{input_data}"


# app.add_url_rule('/base/<int:age>', view_func=baseView.as_view("base"))
app.add_url_rule('/base', view_func=baseView.as_view("base"))

"""
========================================================================================================================
继承View来来实现视图函数,
重写dispatch_request，自己实现各个请求方法的处理
========================================================================================================================
"""


class MyView(View):
    methods = ['GET']

    def dispatch_request(self, name):
        return 'Hello %s!' % name


class SecondView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'GET':
            return 'data: \n %s' % ("".join([":".join(item) for item in request.args.items()]))
        data = request.form
        return 'data:\n %s' % ("".join([' : '.join(item) for item in data.items()]))


app.add_url_rule('/hello/<name>', view_func=MyView.as_view('myview'))
app.add_url_rule('/view/post/', view_func=SecondView.as_view("secondview"))

if __name__ == '__main__':
    app.run(debug=True, )
