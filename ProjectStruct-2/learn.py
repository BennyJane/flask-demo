# -*- coding: utf-8 -*-
# @Time : 2020/10/15
# @Author : Benny Jane
# @Email : 暂无
# @File : learn.py
# @Project : ProjectStruct-2
import sys
from pprint import pprint

from flask import Flask

# module_name = 'my_flask_app'  # 需要在构造文件里面的属性 才会出现在模块属性中
module_name = 'autoapp'  # ===》 可以通过属性搜索到 app
# module_name = 'autoapp.py'  # ==> 错误，不是模块
__import__(module_name)
module = sys.modules[module_name]

for attr_name in ("app", "application"):
    app = getattr(module, attr_name, None)

    if isinstance(app, Flask):
        print(app)
# print(dir(module))
# pprint(module.__dict__)


PY2 = int(sys.version[0]) == 2
print(sys.version_info)
print(sys.platform)
print(sys.version)
print(sys.modules)
