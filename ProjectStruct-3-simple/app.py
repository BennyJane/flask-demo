# -*- coding: utf-8 -*-
# @Time : 2020/10/28
# @Author : Benny Jane
# @Email : 暂无
# @File : app.py
# @Project : ProjectStruct-3-simple
import os

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

from config import config
from extension import register_ext
from log import register_logging
from web.views import register_bp

config_name = os.getenv("FLASK_CONFIG", 'development')
app = Flask(__name__)
app.config.from_object(config[config_name])
register_logging(app)
register_ext(app)
register_bp(app)


@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


# @app.errorhandler(CSRFProtect)
# def handle_csrf_error(e):
#     return render_template('errors/400.html', description=e.description), 400
