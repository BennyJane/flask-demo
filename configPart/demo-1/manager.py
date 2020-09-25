import time
from _datetime import datetime
from flask_script import Server, Command
from application import app, manager
from web.www import *

'''
flask_script: 官网 https://flask-script.readthedocs.io/en/latest/
1. manager.add_command() 不能为空字符串
2. 三种方式添加命令
'''

'''
================== 第一种
'''
manager.add_command("runserver",
                    Server(host="localhost", port=app.config['SERVER_PORT'], use_debugger=app.config['DEBUG'],
                           use_reloader=True))

'''
================== 第二种
'''


@manager.command
def hello():
    print("hello world!")


'''
================== 第三种
'''


class currentTime(Command):
    def run(self):
        now = datetime.today()
        print(now)


manager.add_command("time", currentTime())


# manager.add_command("hello", hello())


def main():
    manager.run()


if __name__ == '__main__':
    try:
        import sys

        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()
