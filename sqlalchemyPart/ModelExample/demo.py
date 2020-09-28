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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


'''
一对多： 
'''


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)  # FIXME 时间戳的定义

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # todo 只需要在一侧写，就可以在两个表中使用关联关系 ==》 在 backref 中声明了 posts 作为动态关系
    category = db.relationship('Category',
                               backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        # todo 初始化的时候，添加当前时间
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


'''
为了创建初始数据库，只需要从交互式 Python shell 中导入 db 对象并且调用 SQLAlchemy.create_all() 方法来创建表和数据库:

>>> from yourapplication import db
>>> db.create_all()

官方文档：http://www.pythondoc.com/flask-sqlalchemy/quickstart.html
'''
