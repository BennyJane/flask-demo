# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
from flask import Blueprint

api_bp_v1 = Blueprint("api_v1", __name__)

# 导入v1蓝图内所有定义的视图函数
from .index import index
