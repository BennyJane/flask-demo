# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/24 19:55
# Warning    ：The Hard Way Is Easier
import math
import time
import uuid
import redis

LOCK_PREFIX = "lock:"
LOCK_TYPE = "purchase"

"""
===========================================================
简易锁：
===========================================================
"""


def acquire_lock(conn, lockname, acquire_timeout=10):
    """
    获取redis锁，并设置阻塞时间
    :param conn: 数据库连接
    :param lockname: 锁名称，加锁类型
    :param acquire_timeout: 获取锁的阻塞时间
    :return:
    """
    identifier = str(uuid.uuid4())  # 随机生成锁ID; 有一定重复率

    end = time.time() + acquire_timeout
    while time.time() < end:  # 阻塞，不断尝试获取锁（获取|超时）
        if conn.setnx(LOCK_PREFIX + lockname, identifier):
            return identifier
        time.sleep(.001)
    return False


# TODO 比上述方法较好，释放锁方法可以使用同一个函数
def acquire_lock_with_timeout(conn, lockname, acquire_timeout=10, lock_timeout=10):
    """
    获取redis锁，设置阻塞时间，已经锁过期时间
    :param conn: 数据库连接
    :param lockname: 锁名称，加锁类型
    :param acquire_timeout: 获取锁的阻塞时间
    :param lock_timeout: 锁过期时间
    :return:
    """
    identifier = str(uuid.uuid4())
    lockname = LOCK_PREFIX + lockname
    lock_timeout = int(math.ceil(lock_timeout))

    end = time.time() + acquire_timeout
    while time.time() < end:
        if conn.setnx(lockname, identifier):  # 如果添加新键成功，返回True
            conn.expire(lockname, lock_timeout)  # 设置键的过期时间
            return identifier
        elif conn.ttl(lockname) < 0:  # 如果键已经存在，且距离当前的过期时间为负数，重新设置过期时间
            conn.expire(lockname, lock_timeout)
        time.sleep(.001)
    return False


def release_lock(conn, lockname, identifier):
    """
    释放锁
    :param conn: 数据库连接
    :param lockname: 锁类型
    :param identifier: 锁ID
    :return:
    """
    pipe = conn.pipeline(True)  # 设置操作为原子性
    lockname = LOCK_PREFIX + lockname
    if isinstance(identifier, str):
        identifier = identifier.encode()  # bytes，redis中取出对象为bytes

    while True:  # 阻塞
        try:
            pipe.watch(lockname)  # 使用watch监听键
            if pipe.get(lockname) == identifier:  # 确保锁没有被更新过
                pipe.multi()
                pipe.delete(lockname)
                pipe.execute()
                return True  # 事务执行成功返回True

            pipe.unwatch()
            break
        except redis.exceptions.WatchError:  # 锁被修改，重试
            pass

    return False  # 进程已经失去锁， 没有完成解锁


def do_something_with_lock(conn, ):
    action_name = "market: "
    locked = acquire_lock(conn, action_name)
    if not locked:
        return False  # 没有获取锁，直接返回
    pipe = conn.pipeline(True)
    try:
        # todo
        pipe.execute()
        return True
    finally:
        release_lock(conn, action_name, locked)


if __name__ == '__main__':
    pass
