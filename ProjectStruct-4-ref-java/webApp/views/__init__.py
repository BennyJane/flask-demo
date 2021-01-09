# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier


def register_route_views(app):
    from .index import index_bp
    app.register_blueprint(index_bp, url_prefix="/index")
