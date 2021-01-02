import os
from flask import Flask
from flask import request
from flask.views import View
from flask.views import MethodView
from flask_bases.utils import decorator_log

app = Flask(__name__)

os.environ.setdefault("FLASK_ENV", "development")


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
