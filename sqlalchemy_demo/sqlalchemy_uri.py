# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
import sqlalchemy as sqla
from sqlalchemy import (
    Boolean, Column, create_engine, DateTime, ForeignKey, Integer,
    MetaData, String, Table, Text,
)
from sqlalchemy.engine import url
from sqlalchemy.engine.url import make_url
# 需要安装 sqlalchemy-utils类；使用加密类型 ; 另外需要安装cryptography
from sqlalchemy_utils import EncryptedType

from sqlalchemy_demo.orm_models import db
from flask_utils.decorator import task_spend_time

"""
========================================
完成对数据库字段的加密显示： 参考superset项目
========================================
"""
PASSWORD_MASK = "********"


class Database(db.Model):
    """An ORM object that stores Database related information"""

    __tablename__ = 'dbs'
    type = 'table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    database_name = Column(String(250))
    sqlalchemy_uri = Column(String(1024))
    # password = Column(EncryptedType(String(1024), config.get('SECRET_KEY')))
    """
    ========================================
    使用sqlalchemy-utils的EncryptedType对数据表字段加密： 需要输入session_key字段用于加密
    - 程序直接调用obj.password显示的非加密（明文密码），只在数据库显示为加密字符串
    ========================================
    """
    password = Column(EncryptedType(String(1024), "sessionkeybennyjane"))

    def set_sqlalchemy_uri(self, uri):
        # 使用make_url解析数据库连接URI
        conn = sqla.engine.url.make_url(uri.strip())  # <class 'sqlalchemy.engine.url.URL'>
        # print(conn)
        # print(vars(conn))  # 显示类URL实例的属性

        if conn.password != PASSWORD_MASK:
            # 保留uri内的原始密码
            self.password = conn.password
        conn.password = PASSWORD_MASK if self.password else None
        self.sqlalchemy_uri = str(conn)  # 使用PASSWORD替换原链接中的密码

    @classmethod
    def get_password_masked_url_from_uri(cls, uri):
        """获取隐藏密码的数据链接： 确保密码没有明文显示出来"""
        url = make_url(uri)  # 返回一个字典对象
        return cls.get_passwd_masked_url(url)

    @classmethod
    def get_passwd_masked_url(cls, url):
        """检测数据库连接密码是否已经被隐藏"""
        from copy import deepcopy
        url_copy = deepcopy(url)  # 字典对象：使用深拷贝
        if url_copy.password is not None and url_copy.password != PASSWORD_MASK:
            url_copy.password = PASSWORD_MASK
        return url_copy

    @property
    def sqlalchemy_uri_decrypted(self):
        """获取携带明文密码的数据库"""
        conn = sqla.engine.url.make_url(self.sqlalchemy_uri)
        conn.password = self.password  # 还原密码
        return str(conn)


@task_spend_time
def insert_data_one_commit():
    """插入100条数据
    耗时： 0.34952259063720703 0.23205018043518066
    """
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@192.168.1.202/bi_base?charset=utf8'
    for i in range(100):
        database = Database(database_name="test{}".format(i))
        database.set_sqlalchemy_uri(SQLALCHEMY_DATABASE_URI)
        db.session.add(database)
    db.session.commit()


@task_spend_time
def insert_data_many_commit():
    """插入100条数据
    耗时： 5.722044944763184
    """
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@192.168.1.202/bi_base?charset=utf8'
    for i in range(100):
        database = Database(database_name="test{}".format(i))
        database.set_sqlalchemy_uri(SQLALCHEMY_DATABASE_URI)
        db.session.add(database)
        db.session.commit()  # 每次都提交一次


def get_origin_url():
    database = db.session.query(Database).filter(Database.id == 1).first()
    print(database.sqlalchemy_uri_decrypted)
    print(database.password)


if __name__ == '__main__':
    db.create_all()
    insert_data_many_commit()
    insert_data_one_commit()
    # get_origin_url()
    # app.run(debug=True)

    pass
