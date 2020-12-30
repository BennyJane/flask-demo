# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/30 23:00
# Warning    ：The Hard Way Is Easier
import sys
import argparse
import traceback

from flask_script import Manager
from flask_script import Command


class runJobs(Command):
    capture_all_args = True

    def run(self, *args, **kwargs):
        args = sys.argv[2:]

        parser = argparse.ArgumentParser(add_help=True)

        parser.add_argument("-n", "--name", dest="name", metavar="name", help="指定Job类别名称", required=True)
        parser.add_argument("-a", "--act", dest="action", metavar="action", help="Job子任务", required=True)
        parser.add_argument("-p", "--params", dest="param", nargs="*", metavar="param", help="业务参数", default="",
                            required=False)

        params = parser.parse_args(args)
        with open("./action.log", 'a') as f:
            f.write(params)
        params_dict = params.__dict__
        ret_params = {key: value for key, value in params_dict.items()}
        if "name" not in ret_params or not ret_params["name"]:
            return self.tips()


if __name__ == '__main__':
    runJobs()