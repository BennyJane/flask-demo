# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2021/1/1 11:42
# Warning    ：The Hard Way Is Easier
import time
import functools


def decorator_log(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        print("start time: %s" % time.time())
        result = f(*args, **kwargs)
        return result

    return inner
