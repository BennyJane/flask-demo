# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/24 14:52
# Warning    ：The Hard Way Is Easier
import re
from bson import ObjectId
from mongdb_demo import config
from pymongo import MongoClient
from pymongo import DESCENDING


def is_object_id(id: str) -> bool:
    """
    检测id是否是有效的ObjectId字符串
    :param id: ObjectId string
    """
    return re.search('^[a-zA-Z0-9]{24}$', id) is not None


class DbManager(object):
    """数据库管理类： 处理CRUD操作"""

    def __init__(self):
        self.mongo = MongoClient(
            host=config.MONGO_HOST,
            port=config.MONGO_PORT,
            username=config.MONGO_USERNAME,
            password=config.MONGO_PASSWORD,
            authSource=config.MONGO_AUTH_DB or config.MONGO_DB,
            connect=False
        )
        self.db = self.mongo[config.MONGO_DB]

    def save(self, col_name: str, item: dict, **kwargs) -> None:
        """
        保存item到指定的集合中
        :param col_name: 集合名称
        :param item: 对象
        """
        col = self.db[col_name]

        # in case some fields cannot be saved in MongoDB
        if item.get('stats') is not None:
            item.pop('stats')

        return col.save(item, **kwargs)

    def remove(self, col_name: str, cond: dict, **kwargs) -> None:
        """
        根据规定条件，删除对象
        :param col_name: 集合名称
        :param cond: 条件或筛选器
        """
        col = self.db[col_name]
        col.remove(cond, **kwargs)

    def update(self, col_name: str, cond: dict, values: dict, **kwargs):
        """
        更新多个对象
        :param col_name: 集合名称
        :param cond: 条件或筛选器
        :param values: 待更新的内容
        """
        col = self.db[col_name]
        col.update(cond, {'$set': values}, **kwargs)

    def update_one(self, col_name: str, id: str, values: dict, **kwargs):
        """
        更新指定id的对象
        :param col_name: 集合名称
        :param id: _id
        :param values: 待更新的内容
        """
        col = self.db[col_name]
        _id = id
        if is_object_id(id):
            _id = ObjectId(id)
        col.find_one_and_update({'_id': _id}, {'$set': values})

    def remove_one(self, col_name: str, id: str, **kwargs):
        """
        根据指定id删除对象
        :param col_name: 集合名称
        :param id: _id
        """
        col = self.db[col_name]
        _id = id
        if is_object_id(id):
            _id = ObjectId(id)
        col.remove({'_id': _id})

    def list(self, col_name: str, cond: dict, sort_key=None, sort_direction=DESCENDING, skip: int = 0,
             limit: int = 100,
             **kwargs) -> list:
        """
        Return a list of items given specified condition, sort_key, sort_direction, skip, and limit.
        根据给定的condition, sort_key, sort_direction, skip, and limit返回结果列表
        :param col_name: 集合名称
        :param cond: 条件或筛选器
        :param sort_key: 排序关键字
        :param sort_direction: 排序描述
        :param skip: 跳过数量
        :param limit: 获取数量限制
        """
        if sort_key is None:
            sort_key = '_i'
        col = self.db[col_name]
        data = []
        for item in col.find(cond).sort(sort_key, sort_direction).skip(skip).limit(limit):
            data.append(item)
        return data

    def _get(self, col_name: str, cond: dict) -> dict:
        """
        根据条件返回一个对象
        :param col_name: 集合名称
        :param cond: 条件
        """
        col = self.db[col_name]
        return col.find_one(cond)

    def get(self, col_name: str, id: (ObjectId, str)) -> dict:
        """
        根据指定ID返回一个对象
        :param col_name: 集合名称
        :param id: _id
        """
        if type(id) == ObjectId:
            _id = id
        elif is_object_id(id):
            _id = ObjectId(id)
        else:
            _id = id
        return self._get(col_name=col_name, cond={'_id': _id})

    def get_one_by_key(self, col_name: str, key, value) -> dict:
        """
        根据key/value返回一个对象
        :param col_name: 集合名称
        :param key: key
        :param value: value
        """
        return self._get(col_name=col_name, cond={key: value})

    def count(self, col_name: str, cond) -> int:
        """
        根据条件返回指定集合的数量
        :param col_name:集合名称
        :param cond: 条件或筛选器
        """
        col = self.db[col_name]
        return col.count(cond)

    def aggregate(self, col_name: str, pipelines, **kwargs):
        """
        聚合函数
        参考文章: https://docs.mongodb.com/manual/reference/command/aggregate/
        :param col_name: 集合名称
        :param pipelines: pipelines
        """
        col = self.db[col_name]
        return col.aggregate(pipelines, **kwargs)

    def create_index(self, col_name: str, keys: dict, **kwargs):
        col = self.db[col_name]
        col.create_index(keys=keys, **kwargs)

    def distinct(self, col_name: str, key: str, filter: dict):
        col = self.db[col_name]
        return sorted(col.distinct(key, filter))


db_manager = DbManager()
