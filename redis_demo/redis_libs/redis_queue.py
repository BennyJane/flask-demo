# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/24 23:56
# Warning    ：The Hard Way Is Easier
import json
import time
import logging

logger = logging.getLogger(__name__)

EMAIL_QUEUE = "queue:email"
QUIT = False

"""
=============================================================
基础版本：只能处理固定的队列任务： 队列固定、任务固定，
因为process_task_with_queue函数中将 任务函数 硬编码  
=============================================================
"""


def add_task_into_queue(conn, **kwargs):
    """将任务察插入队列"""
    data = dict(kwargs)
    data['time'] = time.time()
    conn.rpush(EMAIL_QUEUE, json.dumps(data))


def process_task_with_queue(conn):
    """从队列中不断取出任务执行"""
    while not QUIT:
        packed = conn.blpop([EMAIL_QUEUE], 30)  # 阻塞30秒
        if not packed:
            continue  # 没有获取数据
        params = json.loads(packed[1])
        try:
            # TODO 将params传入目标函数并执行
            pass
        except Exception as e:
            logger.debug(e)
        else:
            logger.info("success")


"""
=============================================================
2.0版本：支持不同队列与函数的执行
任何队列中存储信息为： [function, [arg0, arg1, arg2 ...]]
=============================================================
"""


def worker_diff_queue(conn, queue, callbacks):
    while not QUIT:
        packed = conn.blpop([queue], 30)
        if not packed:
            continue
        name, args = json.loads(packed[1])
        if name not in callbacks:
            logger.debug("找不到回调函数")
        callbacks[name](*args)


"""
=============================================================
3.0版本：支持队列优先级
conn.blpop(key [key, key ...])  会优先从第一个非空队列中取值
=============================================================
"""


def priory_multi_queue(conn, queues, callbacks):
    while not QUIT:
        packed = conn.blpop(queues, 30)
        if not packed:
            continue
        name, args = json.loads(packed[1])
        if name not in callbacks:
            logger.debug("Unknown callback %s" % name)
            continue
        callbacks[name](*args)
