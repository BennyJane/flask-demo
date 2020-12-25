# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : career-planning-info
# Time       ：2020/12/15 19:59
# Warning    ：The Hard Way Is Easier
from flask_sqlalchemy import get_debug_queries

from proStruct import db, Book


def register_template_ext(app):
    ### 添加模板过滤器
    """添加模板过滤器"""
    # app.add_template_filter(f, name="f_name")

    """添加模板函数"""

    # 添加URL管理函数
    app.add_template_global(UrlManager.buildUrl, "buildUrl")
    app.add_template_global(UrlManager.buildStaticUrl, "buildStaticUrl")
    app.add_template_global(random_string, name="random_string")
    app.add_template_global(AUTHOR, name="author")
    app.shell_context_processor(make_shell_context)

    app.context_processor(make_template_context)


def make_shell_context():
    '''将db，数据模型类直接传入shell上下文， 便于调试； 不要再手动引入'''
    return dict(db=db, Book=Book)


def make_template_context():
    book = Book.query.first()
    customValue = '传入模板中直接使用的变量|函数；最后return对象必须是dict'
    return dict(book=book, customValue=customValue)
