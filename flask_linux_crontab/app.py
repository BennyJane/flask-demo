# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/31 9:38
# Warning    ：The Hard Way Is Easier
import sys
import traceback
from flask import Flask
from flask_script import Manager

from jobs.launcher import runJobs

app = Flask(__name__)
manager = Manager(app)
manager.add_command("runjob", runJobs())  # 查看源码案例


def main():
    manager.run()



if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc()
