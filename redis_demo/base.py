import redis
import time
'''
参考文章: 
https://www.jianshu.com/p/2639549bedc8

# 菜鸟教程
https://www.runoob.com/w3cnote/python-redis-intro.html
'''

# 普通链接

def common():
    conn = redis.Redis(host="192.168.1.124", port=6379, password='j3&r8t5gd5^7$9lM6Gf9A')
    # ex 设置过期时间
    conn.set("x1", "hello", ex=5)  # ex代表seconds，px代表ms
    n = 0
    while True:
        time.sleep(1)
        val = conn.get('x1')
        print(val)
        n += 1
        if n > 10:
            break


def connectPool():
    pool = redis.ConnectionPool(host="192.168.1.124", port=6379, password='j3&r8t5gd5^7$9lM6Gf9A', max_connections=1024)
    conn = redis.Redis(connection_pool=pool)

    conn.set('first_key', 'first_value', ex=3)
    print(conn.get('first_key'))


# connectPool()

'''
全局配置
'''
Caches = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.1.124:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PASSWORD": "密码"
        }
    }
}


'''
=======================================================
菜鸟教程: 
redis: 提供两个类Redis与StrictRedis用于实现大部分官方命令, Redis是StrictRedis的子类,用于向后兼容旧版本.
redis get取出来的结果默认是字节, 可以通过设定 decode_responses=True 改成字符串

r = redis.Redis(host=host, port=port, password=password, decode_response=True)


连接池:
redis-py 使用 connection pool 来管理对一个 redis server 的所有操作, 避免每次建立, 释放连接的开销.
默认,每个Redis实例都会维护一个自己的连接池. 
-- 可以直接建立一个连接池, 然后作为参数 Redis, 就可以实现多个Redis 实例共享一个连接池

import redis

pool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
r = redis.Redis(host=host, port=6379, decode_responses=True)
r.set('name', 'value)
r.get('name')


redis 基本命令 String
set(name, value, ex=None, px=None, nx=False, xx=False)
    -- 向redis中添加key-value, 默认没有就添加, 存在就修改
    -- ex 过期时间 秒 s
    -- px 过期时间 毫秒 ms
    -- nx 默认为False, 为True, 则只添加, 不更新;只有当name不存在的时候,才会执行
    -- xx 设置为True, 只更新,不添加; 只有当name存在的时候, 才会执行set操作
r.set('key', 'value', ex=3)

setnx(name,value)
    -- 只添加,不更新

setex(name, time, value)
    -- time 过期时间, 秒 or timedelta 对象
    -- XX 低版本中为 setex(name, value, time)

psetex(name, time_ms, value)
    -- time_ms 毫秒

mset(*args, **kwargs)
    -- 批量设置值
    

=======================================================
'''

r = redis.Redis(host="127.0.0.1", port=6379, password='life123456')
r.setex('benny', 5, 'blog')
print(r.get('benny'))

# 获取当前所有的缓存键值
print(r.keys('*'))


