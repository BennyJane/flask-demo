# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/23 23:12
# Warning    ：The Hard Way Is Easier
import time
import redis
import threading

CHANNEL_NAME = "channel:base"

conn = redis.Redis()


def publisher(n):
    time.sleep(1)
    for i in range(n):
        print("[i]: {}".format(i))
        conn.publish(CHANNEL_NAME, i)
        time.sleep(1)


def run_pubsub():
    # 使用新的线程运行publisher函数，异步
    threading.Thread(target=publisher, args=(3,)).start()
    pubsub = conn.pubsub()  # 创建发布订阅对象
    pubsub.subscribe([CHANNEL_NAME])  # 订阅指定频道
    count = 0
    for item in pubsub.listen():  # 遍历pubsub.listen()结果，来监听订阅信息
        print(item)  # 订阅=》 接收订阅反馈消息； 发布的消息； 退订 =》 退订的反馈消息
        count += 1
        if count == 4:
            pubsub.unsubscribe()  # 取消所有订阅
        if count == 5:
            break


if __name__ == '__main__':
    run_pubsub()
