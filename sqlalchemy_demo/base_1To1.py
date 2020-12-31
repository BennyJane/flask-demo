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
一对一：国家与首都
    - 建立双向关系，两侧都是标量关系属性; 
        - 在1对多关系属性基础上，转化而来
        - 只需要在 1 的一侧，将集合关系属性 修改为标量关系
        - 多的一侧本身就是标量关系，不需要修改
    - 仍然需要定义外键，任意一侧都可以
    - relationship 关系属性上，添加 uselist=False, 限制返回单一的标量
    - relationship 省略了 populates

'''
Column = db.Column
relationship = db.relationship


class Country(db.Model):  # 真实数据表的名字为 author
    id = Column(db.INTEGER, primary_key=True)
    name = Column(db.String(255), nullable=False)

    # 建立双向关系， back_populates,两侧都添加该语句
    capital = relationship('Capital', uselist=False)

    def __repr__(self):
        return '<%s OF %s>' % (self.name, type(self).__name__)


class Capital(db.Model):  # 真实数据表的名字为 book
    id = Column(db.INTEGER, primary_key=True)
    name = Column(db.String(255), index=True)

    # s
    country_id = Column(db.Integer, db.ForeignKey('country.id'))
    country = relationship("Country")

    def __repr__(self):
        return f'<{self.name} OF {type(self).__name__}>'


@app.shell_context_processor
def add_shell_context():
    return dict(db=db,
                Country=Country, Capital=Capital)


db.drop_all()
db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

'''
# flask shell 
country = Country(name='China')
capital = Capital(name='beijing')
db.session.add_all([country, capital])
country.capital=capital
db.session.commit()


'''
