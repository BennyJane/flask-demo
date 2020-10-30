# -*- coding: utf-8 -*-
# @Time : 2020/10/28
# @Author : Benny Jane
# @Email : 暂无
# @File : models.py
# @Project : ProjectStruct-3-simple


from .extension import db

column = db.Column


class User(db.Model):
    id = column(db.INTEGER, primary_key=True)
    name = column(db.String(32), nullable=False)


class Book(db.Model):
    id = column(db.INTEGER, primary_key=True)
    name = column(db.String(32), nullable=False)


class Link(db.Model):
    id = column(db.INTEGER, primary_key=True)
    url = column(db.String(255), nullable=False)