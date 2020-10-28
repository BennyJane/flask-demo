# -*- coding: utf-8 -*-
# @Time : 2020/10/10
# @Author : Benny Jane
# @Email : 暂无
# @File : model.py
# @Project : ProjectStruct-1
from datetime import datetime

from proStruct.extensions import db

'''
TIP: 小项目可以直接将单个model.py文件proStruct目录下
'''


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    brief = db.Column(db.Text, default='')
    create_at = db.Column(db.DateTime, default=datetime.date)

    def __repr__(self):
        return f'<{self.__name__} {self.id}>'
