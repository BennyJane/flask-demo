# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2021/1/2 22:15
# Warning    ：The Hard Way Is Easier
import os
import time
import random
from functools import partial
from multiprocessing import Pool
from sqlalchemy_demo.orm_models import db
from flask_sql.sql_func import SqlFunc

sqlFunc = SqlFunc(db.session)

res = sqlFunc.select_sql("student", ["id", 'name'], condition="where id = 8")
print(res)

