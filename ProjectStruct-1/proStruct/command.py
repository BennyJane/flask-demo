# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : command.py
# @Project : Flask-Demo
import click

'''
这一部分可以直接写在 __init__.py 文件内， 不用传入db， 直接使用__init__.py 中引入的db全局变量
'''


# 将多个
def register_cli(app, db):
    command1(app, db)


# 在该文件中直接引入db，会报错； ==》 db还没有绑定app
def command1(app, db):
    # 初始化数据库 is_flag 布尔值，
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm("This operation will delete the database, do you want to continue?", abort=True)
            db.drop_all()
            click.echo("Drop tables.")
        db.create_all()
        click.echo("Initialize database.")
