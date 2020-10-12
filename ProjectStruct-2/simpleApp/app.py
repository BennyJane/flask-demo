# -*- coding: utf-8 -*-
# @Time : 2020/10/12
# @Author : Benny Jane
# @Email : 暂无
# @File : app.py
# @Project : ProjectStruct-2
import logging
import sys

from flask import Flask


def create_app(config_object="simpleApp.settings"):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    configure_logger(app)
    return app


def register_extensions(app):
    return None


def register_blueprints(app):
    app.register_blueprint()
    return None


def configure_logger(app):
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
