# -*- coding: utf-8 -*-
# @Time : 2020/10/10
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : ProjectStruct-1
import memcache

"""
需要安装memcached服务器,同时需要安装python-memcached第三方包
"""


class MemCache:
    memCache = memcache.Client(["127.0.0.1:11211"], debug=True)

    @classmethod
    def set(cls, key, value, timeout=60):
        return cls.memCache.set(key, value, timeout)

    @classmethod
    def get(cls, key):
        return cls.memCache.get(key)

    @classmethod
    def delete(cls, key):
        return cls.memCache.delete(key)


if __name__ == '__main__':
    MemCache.set("name", "benny")
    # MemCache.delete("name")
    res = MemCache.get("name")
    print(res)
