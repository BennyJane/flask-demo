# -*- coding: utf-8 -*-
# @Time : 2020/10/28
import os
from flask import Flask

from web.config import config
from web.extension import register_ext
from web.log import register_logging
from web.views import register_bp
from web.errors import register_errors

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
register_errors(app)
