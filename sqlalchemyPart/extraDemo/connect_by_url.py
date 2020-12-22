# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/10 20:52
# Warning    ：The Hard Way Is Easier
import logging
from sqlalchemy.engine import create_engine

logger = logging.getLogger(__name__)


def test_sqlalchemy_url(url):  # 检测URL是否正确
    try:
        engine = create_engine(url, echo=False)
        conn = engine.raw_connection()
        conn.cursor()
    except Exception as e:
        logger.error(e)
        return False
    return True


def get_data_by_url(sqlalchemy_url, sql):
    try:
        engine = create_engine(sqlalchemy_url, echo=False)
        conn = engine.raw_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
    except Exception as e:
        logger.debug(e)
        return []
    return data


if __name__ == '__main__':
    pass
