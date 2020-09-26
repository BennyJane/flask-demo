# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : errors.py
# @Project : Flask-Demo
from FlaskAppFile import app
from flask import render_template


@app.errorhandler(400)
def bad_request(e):
    return render_template("errros/400.html"), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500