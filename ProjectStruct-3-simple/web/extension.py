# -*- coding: utf-8 -*-
# @Time : 2020/10/28
# @Author : Benny Jane
# @Email : 暂无
# @File : app.py
# @Project : ProjectStruct-3-simple

from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from web.utils.redis_lib import RedisManager

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
redis_manager = RedisManager()


def register_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    redis_manager.init_app(app)
