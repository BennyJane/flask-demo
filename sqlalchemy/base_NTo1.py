# -*- coding: utf-8 -*-
# @Time : 2020/10/16
# @Author : Benny Jane
# @Email : 暂无
# @File : base_1ToN.py
# @Project : sqlalchemy
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

base_dir = os.path.abspath(os.path.dirname(__file__))
# 必须是 __name__
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'base.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET'] = 'BENNY'
# app.config['ENV'] = 'development'
db = SQLAlchemy(app)

'''
多对一：居民与城市
    - 不使用 backref:一对多，多对一，的代码基本一样

'''
Column = db.Column
relationship = db.relationship


class City(db.Model):  # 真实数据表的名字为 author
    id = Column(db.INTEGER, primary_key=True)
    name = Column(db.String(255), nullable=False)

    # 建立双向关系， back_populates,两侧都添加该语句
    citizens = relationship('Citizen', back_populates='city')

    def __repr__(self):
        return '<%s OF %s>' % (self.name, type(self).__name__)


class Citizen(db.Model):  # 真实数据表的名字为 book
    id = Column(db.INTEGER, primary_key=True)
    name = Column(db.String(255), index=True)

    city_id = Column(db.Integer, db.ForeignKey('city.id'))
    city = relationship("City", back_populates='citizens')

    # fixme 写法： 省略了 populates
    # city = relationship("City")

    def __repr__(self):
        return f'<{self.name} OF {type(self).__name__}>'


db.drop_all()
db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
