# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2020/12/30 23:00
# Warning    ：The Hard Way Is Easier
import sys
import argparse
import importlib
import traceback
from flask_script import Command


class runJobs(Command):
    capture_all_args = True
    task_class_name = "JobTask"
    dynamic_import_method = "importlib"
    # 导入字符串表达
    IMPORT_EXEC_FORMAT = "from jobs.tasks.{} import %s " % task_class_name  # 如果当前作用域存在同名，可以考虑通过as 重命名
    IMPORT_LIB_FORMAT = "jobs.tasks.{}"

    def run(self, *args, **kwargs):
        args = sys.argv[2:]

        # 设置终端接收命令
        parser = argparse.ArgumentParser(add_help=True)
        parser.add_argument("-n", "--name", dest="name", metavar="name", help="指定Job类别名称", required=True)
        parser.add_argument("-a", "--action", dest="action", metavar="action", help="Job子任务", required=True)
        parser.add_argument("-p", "--param", dest="param", nargs="*", metavar="param", help="业务参数", default="",
                            required=False)

        params = parser.parse_args(args)  # 返回Namespace类的实例，通过 vars() 或者 实例的__dict__获取传入参数
        # Namespace(action='write', name='test', param=['data', 'benny', 'same'])
        # print(params)
        params_dict = params.__dict__
        ret_params = {key: value for key, value in params_dict.items()}
        if "name" not in ret_params or not ret_params["name"]:
            return self.tips()
        module_name = ret_params["name"].replace("/", ".")
        if self.dynamic_import_method == "importlib":
            target_class = self.dynamic_by_importlib(module_name)
        else:
            target_class = self.dynamic_by_importlib(module_name)
        if target_class:
            target_class().run(ret_params)

    def dynamic_by_exec(self, name: str):
        import_string = self.IMPORT_STRING_FORMAT.format(name)
        try:
            exec(import_string, locals())  # 将模块导入到当前作用域内
            return locals().get(self.task_class_name)  # locals() 获取当前作用域内的所有变量：dict
        except Exception as e:
            traceback.print_exc()

    def dynamic_by_importlib(self, name: str):
        import_string = self.IMPORT_LIB_FORMAT.format(name)
        target_module = importlib.import_module(import_string)  # 获取对象类型： module
        return target_module.__getattribute__(self.task_class_name)  # 只能通过__getattribute__直接获取属性
