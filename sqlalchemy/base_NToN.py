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
多对多：学生与老师
    - 可以看做，两个1对多关系的叠加
    - 创建关联表，不需要存储数据，只用来存储两侧模型的外键对应关系
    - 操作关系属性，来添加关联关系

# 创建双向关系
    - 在两张表内分别创建 集合关系属性，便于查询，这些字段不存在数据库内
    - teachers = db.relationship('Teacher', 
                                secondary=association_table,
                                back_populates='students')
        - 第一参数，关联表的模型类名称
        - secondary : 指明关联表名称 =》 变量名称
        - back_populates: 另一侧关系属性的名称
'''
Column = db.Column
relationship = db.relationship

'''
==============================================================
关联表: 使用 db.Table 来创建表
    - 第一个参数时，关联表的名称
    - 需要定义两个外键， 分别存储两张表的主键id对应关系
    - 该表需要定义在 两个需要建立关系的表的前面

    - 关联表可以将 多对多关系，拆解为两个一对多关系
    - 使用： 查找一个学生对应的多个老师？
        - 先通过学生id，使用1对多关系，在关联表中查询包含该id的所有记录
        - 然后，通过查询的记录，获取老师记录(id)
        - 最后，根据老师ID，通过多对1关系，查询所有老师的记录
==============================================================
'''
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

if __name__ == '__main__':
    app.run(debug=True)

'''
# FLASK_APP=base_NToN:app
# flask shell

student = Student(name='benny')
student1 = Student(name='tom')
student2 = Student(name='jane')
teacher = Teacher(name='lihu')
teacher1 = Teacher(name='xiaoming')
teacher2 = Teacher(name='dongxi')

student.teachers=[teacher, teacher1]
student1.teachers=[teacher2, teacher1]
student2.teachers=[teacher, teacher2, teacher1]
db.session.add_all=[student, student1, student2, teacher, teacher1, teacher2]
db.session.commit()

student.teachers
teacher.students
'''
