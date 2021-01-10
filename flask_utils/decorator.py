# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
import time
import functools


def task_spend_time(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        spend = end - start
        print(f"{f.__name__} 运行时长： {spend}")
        return result

    return inner
