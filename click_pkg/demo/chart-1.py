# -*- coding: utf-8 -*-
import click

'''
========================== 基础用法
'''


@click.command()
@click.option("--count", default=1, help="Number of greeting.")
@click.option("--name", default="benny", help="Your name")
def hello(count, name):
    for i in range(count):
        click.echo(f"Hello {name}！")


# hello()


'''
========================== 嵌套命令：01
'''


# 创建Group对象
@click.group()
def cli():
    click.echo("this is a group of click.")


@click.command()
def initdb():
    click.echo("Initialized the database.")


@click.command()
def dropdb():
    click.echo("Dropped the database.")


# 给Group赋予多个子命令
cli.add_command(initdb)
cli.add_command(dropdb)
'''
========================== 嵌套命令：02
对于简单的脚本
'''


@click.group()
def cliGroup():
    click.echo("cli group")


@cliGroup.command()
def init():
    click.echo("init")


@cliGroup.command()
def deletedb():
    click.echo("delete db")


'''
========================== 添加参数
'''


@click.command()
@click.option("--count", default=3, help="number")
@click.option("name")
def outPut(count, name):
    for x in range(count):
        click.echo(f"hello {name}")


if __name__ == '__main__':
    # 必须被调用, 也可以直接在上面调用 TODO 不需要传入参数
    hello()
    cli()
    pass
