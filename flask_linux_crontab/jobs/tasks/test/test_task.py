# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/31 10:23
# Warning    ：The Hard Way Is Easier
import time
from utils import wx_notify


class JobTask(object):
    def run(self, params):
        action = params['action'] if "action" in params else ""
        if any([action == 'output', action == ""]):
            print("[test.test_task]: 正在运行...")
        elif action == "notify":
            params = {"msg": "平凡而渺小的一天"}
            wx_notify.new_message(params)
