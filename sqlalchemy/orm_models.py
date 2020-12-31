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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'base.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET'] = 'BENNY'
app.config['ENV'] = 'development'
db = SQLAlchemy(app)

Column = db.Column
relationship = db.relationship

association_table = db.Table('association',
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
    students = relationship('Student',
                            secondary=association_table,
                            back_populates="teachers")

    def __repr__(self):
        return f'<{self.name} OF {type(self).__name__}>'


@app.shell_context_processor
def add_shell_context():
    return dict(db=db,
                Student=Student, Teacher=Teacher)


db.drop_all()
db.create_all()

"""
参考文章
https://blog.csdn.net/weixin_41790086/article/details/80540773
https://blog.csdn.net/qq_43713303/article/details/106766700?utm_medium=distribute.pc_relevant.none-task-blog-title-2&spm=1001.2101.3001.4242
======================================================================================================================
两种查询方式：
db.session.query()
Model.query()
======================================================================================================================
"""
from sqlalchemy import func, and_, or_

db.session.query(Student).all()  # 查找该模型的所有对象，包含所有字段
db.session.query(Student).filter_by(id=1).all()  # 添加筛选条件
db.session.query(Student.name, Student.id).all()  # 只查询模型的指定字段（指定属性）
"""
聚合函数:
func 其实没有任何聚合函数，底层还是调用mysql(对应数据库的）的聚合函数
func.avg
func.sum
func.sum
func.max
func.min
"""

db.session.query(func.count(Student.teachers)).first()
db.session.query(func.avg(Student.id)).first()

"""
filter: 过滤条件， 查询过滤器
- 需要通过模型类调用属性
- 需要使用运算符号判断，双等号...
"""

db.session.query(Student).filter(Student.id == 1).first()  # ==
db.session.query(Student).filter(Student.id != 1).first()  # !=
db.session.query(Student.name.like('%benny%')).first()  # like  ilike

db.session.query(Student.name.in_(['benny', 'tom', 'jane'])).first()  # in_
# in_ 嵌套子查询，作用在一个query上，不需要调用查询执行器
db.session.query(Student.name.in_(
    db.session.query(Teacher.name).filter(Teacher.name.like('%a%'))
)).first()
db.session.query(Student.name.notin_(["benny"])).first()  # notin_

db.session.query(Student).filter(Student.name == None).first()  # is null  || is not null
db.session.query(Student).filter(Student.name != None).first()
db.session.query(Student).filter(Student.name.is_(None)).first()  # is_
db.session.query(Student).filter(Student.name.isnot(None)).first()  # isnot

db.session.query(Student).filter(and_(Student.name == 'benny', Student.id == 1)).first()  # and_
db.session.query(Student).filter(Student.name == 'benny', Student.id == 1).first()  # and_ 等效做法
db.session.query(Student).filter(Student.name == 'benny').filter(Student.id == 1).first()  # and_ 等效做法

db.session.query(Student).filter(or_(Student.name == 'benny', Student.id == 1)).first()

db.session.query(Student).filter_by(id=1).update({'name': 'benny'})  # update

db.session.add_all([])  # 批量添加

if __name__ == '__main__':
    app.run(debug=True)
