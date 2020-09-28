# -*- coding: utf-8 -*-
# @Time : 2020/9/27
# @Author : Benny Jane
# @Email : 暂无
# @File : demo.py
# @Project : Flask-Demo
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'dmeo2.db')  # windows下三斜杠； linux下四斜杠
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

"""
以下表关系：
一个用户对应多篇文章（一对多）
一篇文章对应多个标签，一个标签对应多个文章（多对多）
"""
"""
一对一关系中，需要设置relationship中的uselist=Flase，其他数据库操作一样。
一对多关系中，外键设置在多的一方中，关系（relationship）可设置在任意一方。
多对多关系中，需建立关系表，设置 secondary=关系表
"""


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))


article_tag_table = db.Table('article_tag',
                             db.Column("article_id", db.Integer, db.ForeignKey('article.id'), primary_key=True),
                             db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
                             )


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref="articles")

    tags = db.relationship("Tag", secondary=article_tag_table, backref='tags')


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))


if __name__ == '__main__':
    db.create_all()
