# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def register_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
