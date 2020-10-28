# -*- coding: utf-8 -*-
# @Time : 2020/10/23
# @Author : Benny Jane
# @Email : 暂无
# @File : base02.py
# @Project : Flask-Demo

# demo2_a = 1000

# b = b + 10

def demo2():
    demo2_a = demo2_a + 10
    print(locals())
    print(demo2_a)



if __name__ == '__main__':
    demo2()