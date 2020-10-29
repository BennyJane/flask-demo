# -*- coding: utf-8 -*-
# @Time : 2020/10/28
# @Author : Benny Jane
# @Email : 暂无
# @File : index.py
# @Project : ProjectStruct-3-simple

from flask import Blueprint, render_template

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
    return "Hello World!"


@index_bp.route('/base')
def base():
    return render_template('base.html')
