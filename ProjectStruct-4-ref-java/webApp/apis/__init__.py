# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
from .v1 import api_bp_v1


def register_routes_apis(app):
    app.register_blueprint(api_bp_v1, url_prefix="/api/v1")
