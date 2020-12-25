# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : career-planning-info
# Time       ：2020/12/15 19:46
# Warning    ：The Hard Way Is Easier
import datetime
import hashlib
import os
import time
import math
from flask import current_app

from _compat import win


class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        release_version = current_app.config.get('RELEASE_VERSION')
        release_version = str(int(time.time())) if not release_version else release_version
        path = "/static{}?ver={}".format(path, release_version)
        return UrlManager.buildUrl(path)

    @staticmethod
    def buildImageUrl(path):
        app_config = current_app.config['APP']
        # 默认Linux环境下
        upload_path = current_app.config['UPLOAD']['prefix_url']
        if win:
            upload_path = current_app.config['UPLOAD']['win_prefix_url']

        url = "{}{}{}".format(app_config['domain'], upload_path, path)
        return url


def iPagination(params):
    ret = {
        "is_prev": 1,
        "is_next": 1,
        "from": 0,
        "end": 0,
        "current": 0,
        "total_pages": 0,
        "page_size": 0,
        "total": 0,
        "url": params['url']
    }

    total = params['total']
    page_size = params['page_size']
    page = params['page']
    half_page_display = int(params['half_page_display'])
    total_pages = int(math.ceil(total / page_size))
    total_pages = total_pages if total_pages > 0 else 1
    if page <= 1:
        ret['is_prev'] = 0

    if page >= total_pages:
        ret['is_next'] = 0

    if page - half_page_display > 0:
        ret['from'] = page - half_page_display
    else:
        ret['from'] = 1

    if page + half_page_display <= total_pages:
        ret['to'] = page + half_page_display
    else:
        ret['to'] = total_pages
    ret['current'] = page  # 其实就是 page的值
    ret['total'] = total
    ret['total_pages'] = total_pages
    ret['page_size'] = page_size
    ret['range'] = range(ret['from'], ret['to'] + 1)
    return ret


def produce_id():
    path = os.getcwd()
    src = path + str(time.time())
    m = hashlib.md5()
    m.update(src.encode('utf-8'))
    return m.hexdigest()


def setSHA256(password):
    # 加密密码 ssh56
    hhb = hashlib.sha256()
    # 有返回值, 但没有必要添加
    hhb.update(bytes(password, encoding='utf-8'))
    return hhb.hexdigest()


def getFormatDate(date=None, _format="%Y-%m-%d %H:%M:%S"):
    if date is None:
        date = datetime.datetime.now()
    return date.strftime(_format)
