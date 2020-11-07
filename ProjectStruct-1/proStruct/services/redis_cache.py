# -*- coding: utf-8 -*-
# @Time : 2020/10/10
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : ProjectStruct-1

try:
    import redis
except Exception:
    pass

pool = redis.ConnectionPool(host="127.0.0.1", port=6379)
redisCur = redis.Redis(connection_pool=pool)


class RedisCache:
    def __init__(self, host=None, port=None):
        self.host = host if host else "127.0.0.1"
        self.port = port if port else 6379
        self.__pool = redis.ConnectionPool(host=self.host, port=self.port)
        self.redisCur = redis.Redis(connection_pool=self.__pool)

    def test_link(self):
        try:
            self.redisCur.set("test_link", "redis")
            self.redisCur.get("test_link")
            print("redis已经连接成功！")
        except Exception:
            print("redis 连接失效")

    # @contextlib.contextmanager
    def multiOrder(self):
        pipe = self.redisCur.pipeline()
        self.redisCur.set("name", "zsy")
        print(self.redisCur.get("name"))
        self.redisCur.set("name", "benny")
        print(self.redisCur.get("name"))
        pipe.execute()
        # try:
        #     yield ""
        # except Exception as e:
        #     print(e)
        # finally:
        #     pipe.execute()

    def set(self, name, value):
        self.redisCur.set(name, value)

    def get(self, name):
        self.redisCur.get(name)


if __name__ == '__main__':
    redis_cli = RedisCache()
    redis_cli.test_link()
    redis_cli.multiOrder()
    # with redis_cli.multiOrder() as pipe:
    #     redis_cli.set("name", "zsy")
    #     # redis_cli.set("name", "benny")
    #     print(redis_cli.get("name"))
    # # redis_cli.get("name")
    # print(redis_cli.get("name"))
