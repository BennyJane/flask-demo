# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : ProjectStruct-3-simple
# Time       ：2020/12/25 16:52
# Warning    ：The Hard Way Is Easier
from web import app

config = app.config

if __name__ == '__main__':
    app.run(debug=config.DEBUG, port=config.PORT, host=config.HOST)
