# -*- coding: utf-8 -*-
# @Time : 2020/10/10
# @Author : Benny Jane
# @Email : 暂无
# @File : wsgi.py
# @Project : ProjectStruct-1

from proStruct import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
