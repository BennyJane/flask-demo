# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : cli.py
# @Project : Flask-Demo
import click


def register_cli(app):
    cli_func = (initdb,)
    for f in cli_func:
        app.cli.command()(f)


# 初始化数据库 is_flag 布尔值，
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    from proStruct.extensions import db
    if drop:
        click.confirm("This operation will delete the database, do you want to continue?", abort=True)
        db.drop_all()
        click.echo("Drop tables.")
    db.create_all()
    click.echo("Initialize database.")
