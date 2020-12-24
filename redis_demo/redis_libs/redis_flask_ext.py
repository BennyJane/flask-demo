# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/11 10:15
# Warning    ：The Hard Way Is Easier
import redis
import logging
import datetime
from flask import Flask
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class RedisManager(object):
    def __init__(self, app=None):
        self.conn = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """通过调用init_app()方法，绑定到app实例"""
        config = app.config
        pools = redis.ConnectionPool(host=config.get('REDIS_HOST'),
                                     port=config.get('REDIS_PORT'),
                                     password=config.get('REDIS_PASSWORD'),
                                     db=config.get('REDIS_DB') or 0,
                                     )
        self.conn = redis.Redis(connection_pool=pools)


@contextmanager
def redis_lock(conn, action_name, timeout=20 * 60 * 60):
    try:
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        key = f"{action_name}:lock:{today_str}"
        # 只有不存在的键key，才能执行成功 ==》 如果有客户端已经设置该键，则其他客户端不可操作
        _lock = conn.set(key, value=1, nx=True, ex=timeout)
        yield _lock  # # 新增键会返回True; 键已存在，返回None
    except KeyError as e:  # 捕获未获取锁的异常
        logger.info(e)
        return
    except Exception as e:  # 捕获获取锁，但执行过程中报错的情况
        logger.debug(e)
    logger.info("释放锁 ...")
    conn.delete(key)  # 释放锁，只有获取锁的线程才需要释放锁


if __name__ == '__main__':
    # 下面仅仅展示使用方式，并不能直接运行成功
    app = Flask(__name__)
    redis_manager = RedisManager()
    redis_manager.init_app(app)

    with redis_lock(redis_manager.conn, "test") as lock:
        if not lock:
            raise KeyError("无法获取锁")
        logger.info("获取锁 ...")
        # todo 执行功能函数
