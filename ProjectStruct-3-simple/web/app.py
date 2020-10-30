# -*- coding: utf-8 -*-
# @Time : 2020/10/28
# @Author : Benny Jane
# @Email : 暂无
# @File : app.py
# @Project : ProjectStruct-3-simple
import os

from flask import Flask, render_template

from web.config import config
from web.extension import register_ext
from web.log import register_logging
from web.views import register_bp

# 需要将映射到数据库中的模型导入到manage.py中, 否则.migrate过程中无法检测到数据变更.
# https://flask-migrate.readthedocs.io/en/latest/
# http://www.mamicode.com/info-detail-2258414.html
# 必须将数据表引入到app实例模块中
# https://www.jianshu.com/p/e4fc86fa21e8
from web.models import User, Book, Link

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
