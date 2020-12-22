# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/10 15:22
# Warning    ：The Hard Way Is Easier
import logging
from flask import Flask
from flask import request
from logging import FileHandler
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

"""
debug模式下， info debug信息才会打印出来。
生成模式下，flask默认的日志登记是error。

日志功能： 不是线程安全的。

调用Flask自带的日志方法：
app.logger.info()
current_app.logger.info()   # 蓝图中使用

"""

log_formatter = logging.Formatter(
    "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")


@app.route('/')
def hello():
    app.logger.info("this is a info log")
    app.logger.debug("this is a debug log")
    app.logger.error("this is a error log")

    # 添加日志文件，将日志内容保存到文件中，自动生成该文件
    # 不添加formatter, 默认只输出message信息

    handler = FileHandler("./flask.log")
    app.logger.setFormatter(handler)
    app.logger.info("this is a info log")
    app.logger.debug("this is a debug log")
    app.logger.error("this is a error log")

    # 按照文件大小分割日志
    # 参数含义： 文件初始名称，单个文件最大容量，文件最大个数
    # 第一个文件被写满后，会被重命名为 name.log.1;然后继续想name.log内写入内容
    handler = RotatingFileHandler("./rotate.log",
                                  maxBytes=10, backupCount=10)
    handler.formatter = log_formatter
    app.logger.addHandler(handler)
    app.logger.info("this is a info log")
    app.logger.debug("this is a debug log")
    app.logger.error("this is a error log")

    # 按照日期分割文件
    handler = TimedRotatingFileHandler(
        "time.log", when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True
    )
    handler.formatter = log_formatter
    app.logger.addHandler(handler)

    app.logger.info("this is a info log")
    app.logger.debug("this is a debug log")
    app.logger.error("this is a error log")
    return "hello world!"


if __name__ == '__main__':
    app.run(debug=True)
