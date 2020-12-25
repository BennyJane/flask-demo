# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/25 10:34
# Warning    ：The Hard Way Is Easier
import uuid
import json
import time

from redis_demo.redis_libs.redis_lock_simple import release_lock

from redis_demo.redis_libs.redis_lock_simple import acquire_lock_with_timeout

QUIT = False

"""
=============================================================
延迟任务
=============================================================
"""


def execute_later(conn, queue, name, args, delay=0):
    """
    向延迟任务队列（zset）中添加任务
    :param conn:  数据库连接
    :param queue: 待执行的任务属于的任务队列名称
    :param name: 执行任务的回调函数
    :param args: 回调函数的参数
    :param delay: 延迟时间，单位秒
    :return:
    """
    identifier = str(uuid.uuid4())
    item = json.dumps([identifier, queue, name, args], ensure_ascii=False)
    if delay > 0:
        conn.zadd("delayed:", {item: time.time() + delay})
    else:  # 非延迟任务直接添加到任务队列中执行
        conn.rpush("queue:" + queue, item)
    return identifier


def poll_queue(conn):
    while not QUIT:
        # 取出延迟队列中分值最小的任务
        item = conn.zrange("delayed:", 0, 0, withscores=True)
        if not item or item[0][1] > time.time():
            time.sleep(.01)
            continue
        item = item[0][0]
        identifier, queue, function, args = json.loads(item)

        # 需要使用锁，确保安全性
        locked = acquire_lock_with_timeout(conn, identifier)
        if not locked:
            continue

        # 从延迟队列转移到任务队列
        if conn.zrem("delayed:", item):
            conn.rpush("queue:" + queue, item)

        release_lock(conn, identifier, locked)
