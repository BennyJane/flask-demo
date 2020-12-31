# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/31 12:21
# Warning    ：The Hard Way Is Easier
import os
import json
import requests
import traceback

NOTIFY_NEW_MESSAGE_TEMPLATE = "<font color='comment'>[每日提醒]</font>： \n" \
                              "**你知道今天是什么日子吗？** \n" \
                              "{msg}"


class WXNotify:
    webhook = os.getenv("WEBHOOK")
    if not webhook:
        raise Exception("请在环境变量中配置微信机器人的URL：WEBHOOK=URL ")
    headers = {
        "Content-Type": "application/json"
    }

    markdown_type = {
        "msgtype": "markdown",
        "markdown": {
            "content": ""}
    }

    def __init__(self):
        """"""

    def new_message(self, params):
        self.markdown_type["markdown"]["content"] = NOTIFY_NEW_MESSAGE_TEMPLATE.format(**params).strip()
        message_params = json.dumps(self.markdown_type, ensure_ascii=True)  # 需要转化为JSON格式数据
        try:
            res = requests.post(self.webhook, headers=self.headers, data=message_params)
            if res.status_code != 200:
                raise Exception("企业微信通知消息发送失败： {}".format(params))
        except Exception as e:
            print(e)
        return True


wx_notify = WXNotify()
