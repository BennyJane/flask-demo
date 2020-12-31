# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/31 14:28
# Warning    ：The Hard Way Is Easier
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

base_dir = os.path.abspath(os.path.dirname(__file__))
# 必须是 __name__
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'base.db')
# TODO 数据库事务测试，使用sqlite无效，需要使用mysql
# 为了方便使用，mysql直接硬编码
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:5eNyj6Nf@localhost:13306/sql_exercise?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET'] = 'BENNY'
app.config['ENV'] = 'development'
db = SQLAlchemy(app)

Column = db.Column
relationship = db.relationship

association_table = db.Table('association',
                             Column("id", db.INTEGER, primary_key=True, autoincrement=True),
                             db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                             db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')))


class Student(db.Model):  # 真实数据表的名字为 author
    id = Column(db.INTEGER, primary_key=True)
    name = Column(db.String(255), nullable=False)

    teachers = relationship("Teacher",
                            secondary=association_table,
                            back_populates='students')

    def __repr__(self):
        return '<%s OF %s>' % (self.name, type(self).__name__)


class Teacher(db.Model):  # 真实数据表的名字为 book
    id = Column(db.INTEGER, primary_key=True)
    name = Column(db.String(255), index=True)
    age = Column(db.INTEGER)
    students = relationship('Student',
                            secondary=association_table,
                            back_populates="teachers")

    def __repr__(self):
        return f'<{self.name} OF {type(self).__name__}>'


@app.shell_context_processor
def add_shell_context():
    return dict(db=db,
                Student=Student, Teacher=Teacher)


if __name__ == '__main__':
    app.run(debug=True)
