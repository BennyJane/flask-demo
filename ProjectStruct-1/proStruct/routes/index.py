# -*- coding: utf-8 -*-
# @Time : 2020/10/10
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : ProjectStruct-1

from flask import Blueprint
from proStruct.services.tasks import add

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
    return '<h1>index_bp.index</h1>'


@index_bp.route('/add')
def async_add():
    add.delay(10, 15)
    return '<h1>celery消息中间件：　执行异步任务</h1>'
