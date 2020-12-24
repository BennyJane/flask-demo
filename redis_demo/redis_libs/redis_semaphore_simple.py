# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/24 22:58
# Warning    ：The Hard Way Is Easier
import time
import uuid

"""
使用信号量实现锁机制： 限制同一资源的访问进程数量
"""


def acquire_semaphore(conn, semname, limit, timeout=10):
    # semname：信号量的键名
    identifier = str(uuid.uuid4())
    now = time.time()

    pipeline = conn.pipeline(True)  # 创建事务
    # pipeline.zremrangebyscore(semname, '-inf', now - timeout)
    # PY3中极值的表达方式: "inf" 单纯的字符串，无法有数值类型比较
    # 清理过期信号量持有者
    pipeline.zremrangebyscore(semname, -1 * float("inf"), now - timeout)
    pipeline.zadd(semname, {identifier: now})  # 添加信号量，即获取信号量
    pipeline.zrank(semname, identifier)  # 获取新增信号量的排名
    if pipeline.execute()[-1] < limit:
        return identifier

    conn.zrem(semname, identifier)  # 超出限制范围，需要删除新增的信号量
    return None


def release_semaphore(conn, semname, identifier):
    return conn.zrem(semname, identifier)


if __name__ == '__main__':
    print(2 ^ 100 > float("inf"))
    print(-2 ^ 100 < -1 * float("inf"))
    pass
