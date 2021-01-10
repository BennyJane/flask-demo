# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2021/1/2 22:15
# Warning    ：The Hard Way Is Easier
from sqlalchemy_demo.orm_models import db
from flask_sql.sql_func import SqlFunc

"""
========================================
测试SQL拼凑函数
========================================
"""

sqlFunc = SqlFunc(db.session)

sqlFunc.update_sql("student", ["name"], ["student-10"], condition="where id = 9")

res = sqlFunc.select_sql("student", ["id", 'name'], condition="where id = 9")
print(res)

sqlFunc.update_sql("student", ["name"], ["student-9"], condition="where id = 9")
# print(sqlFunc.select_sql("student", ["id", 'name'], condition="where id = 9"))
sqlFunc.commit

# 删除
sqlFunc.delete_sql("student", condition="where id = 10")
sqlFunc.commit

# 新增数据，需要提交操作 commit
sqlFunc.insert_sql("student", ['id', 'name'], [10, 'student-10'])
sqlFunc.commit

# 删除
sqlFunc.delete_sql("student", condition="where id = 10")
sqlFunc.commit

res = sqlFunc.execute_sql("select * from student")
print(res)
