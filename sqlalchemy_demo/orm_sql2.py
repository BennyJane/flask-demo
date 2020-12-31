# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/31 14:28
# Warning    ：The Hard Way Is Easier
import os
import time
import random
from functools import partial
from multiprocessing import Pool
from sqlalchemy_demo.orm_models import db
from sqlalchemy_demo.orm_models import Student, Teacher

"""
基于orm_models.py 的数据模型，测试ORM中 with_for_update函数，即SQL事务 select for update
使用time.sleep()模拟，查询获取数据，到最后插入数据之间的阻塞状况，使用随机数模拟不同阻塞情况
使用多进程的进程池的map方法，模拟高并发情况

### 使用 with_for_update:
因为同时开启多个独立进程，所有每个进程查询数据的时间基本一致，获取的初始值一样，
使用确定的值作为阻塞时长(不能太小)，明确不同进程的提交先后顺序，
多次运行可以看出,每个进程都向数据库提交了数据，但最终只保留最后一次提交的结果

TIP：该测试案例不要使用随机数作为阻塞时长，因为结果每次运行都不一样(其实，也就是只有增加1/2/3三种情况)；
     主要还是打印输出结果的执行命令并不是真正数据库commit的时间，从该时间判断会很混乱
     
### 使用 with_for_update
使用随机数模拟不同阻塞情况，同一时间只有一个进程能获取数据库数据并更新；
当其提交后，其他进程才能操作同一数据；
最后发现，不同进程是依次完成的，每个进程的提交都是独立的，不会相互覆盖。


参数：
    nowait=False, 阻塞时是否不等待，直接断开链接，默认等待；True，则直接断开
    read=False, 
    of=None,
    skip_locked=False,
    key_share=False,

:param nowait: boolean; will render ``FOR UPDATE NOWAIT`` on Oracle
 and PostgreSQL dialects.

:param read: boolean; will render ``LOCK IN SHARE MODE`` on MySQL,
 ``FOR SHARE`` on PostgreSQL.  On PostgreSQL, when combined with
 ``nowait``, will render ``FOR SHARE NOWAIT``.

:param of: SQL expression or list of SQL expression elements
 (typically :class:`_schema.Column`
 objects or a compatible expression) which
 will render into a ``FOR UPDATE OF`` clause; supported by PostgreSQL
 and Oracle.  May render as a table or as a column depending on
 backend.

:param skip_locked: boolean, will render ``FOR UPDATE SKIP LOCKED``
 on Oracle and PostgreSQL dialects or ``FOR SHARE SKIP LOCKED`` if
 ``read=True`` is also specified.

 .. versionadded:: 1.1.0

:param key_share: boolean, will render ``FOR NO KEY UPDATE``,
 or if combined with ``read=True`` will render ``FOR KEY SHARE``,
 on the PostgreSQL dialect.

"""


# 先插入数据
def insert_data():
    db.drop_all()
    db.create_all()
    students = []
    for i in range(1, 10):
        student = Student(id=i, name=f"student-{i}")
        students.append(student)
    db.session.add_all(students)
    teachers = []
    for i in range(1, 10):
        tea = Teacher(id=i, name=f"teacher-{i}", age=25)
        tea.students = [random.choice(students) for _ in range(random.randint(1, 5))]
        teachers.append(tea)
    db.session.add_all(teachers)
    db.session.commit()


# 输出当前数据库信息
def current_info(res, asc, is_end=False):
    if not is_end:
        info = f"start-进程ID：{os.getpid()}，运行时间： {time.time()}, 当前数值： {res.age}, 增加值：{asc}"
    else:
        info = f"END  -进程ID：{os.getpid()}，运行时间： {time.time()}, 当前数值： {res.age}, 增加值：{asc}"
    print(info)


def add_without_lock(num: int):
    res = db.session.query(Teacher).filter(Teacher.id == 1).first()
    current_info(res, num)

    if not res.age:
        res.age = num
    else:
        res.age += num
    time.sleep(num)  # 使用增加值模拟阻塞时长，明确了sql提交的先后顺序
    db.session.commit()

    current_info(res, num, is_end=True)


# print(db.session)
def multi_process_bug(pool_num, ):
    res = db.session.query(Teacher).filter(Teacher.id == 1).first()
    print("[多进程修改前]：", res.age)
    db.session.commit()

    pool = Pool(pool_num)
    pool.map(add_without_lock, [1, 2, 3])
    res = db.session.query(Teacher).filter(Teacher.id == 1).first()

    # 理论上应该增加6
    print("[多进程修改同一个数据]：", res.age)


def add_age(num, use_lock=True):
    """添加锁机制"""
    if use_lock:
        res = db.session.query(Teacher).filter(Teacher.id == 1).with_for_update().first()
    else:
        res = db.session.query(Teacher).filter(Teacher.id == 1).first()
    current_info(res, num, is_end=False)

    if not res.age:
        res.age = num
    else:
        res.age += num
    if use_lock:
        time.sleep(random.randint(1, 5))
    else:
        time.sleep(num)
    db.session.commit()

    current_info(res, num, is_end=True)


def multi_process_correct(process_num: int, use_lock: bool = True):
    teacher = db.session.query(Teacher).filter(Teacher.id == 1).first()
    print("[多进程修改前]：", teacher.age)
    db.session.commit()  # 必须在这里提交；终止上面的查询；否则下面的筛选还使用的旧数据；如果commit放在异步任务后，会使用当前查询数据覆盖数据库数据
    pool = Pool(process_num)
    add_age_func = partial(add_age, use_lock=use_lock)
    pool.map(add_age_func, [1, 2, 3])
    pool.close()
    pool.join()
    # time.sleep(2)

    teacher = db.session.query(Teacher).filter_by(id=1).first()
    print("[多进程修改后]：", teacher.age)


if __name__ == '__main__':
    # insert_data()
    pool_num = 5
    multi_process_correct(pool_num, use_lock=True)
    pass
