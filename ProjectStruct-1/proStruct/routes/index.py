# -*- coding: utf-8 -*-
# @Time : 2020/10/10
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : ProjectStruct-1

from flask import Blueprint

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
    return '<h1>index_bp.index</h1>'
