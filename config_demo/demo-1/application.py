import os
from flask import Flask, request
from flask_script import Manager


class Application(Flask):
    # 重构 Flask的 __init__ 方法
    def __init__(self, import_name, template_folder=None, root_path=None):
        '''
        :param import_name:  包 or 模块的名称 todo 需要进一步探讨??
        :param template_folder: 模板文件路径
        :param root_path: 内部会根据 import_name 来获取
        '''
        super().__init__(import_name, template_folder=template_folder, root_path=root_path)
        self.config.from_pyfile('./config/base_setting.py')
        if "ops_config" in os.environ:
            self.config.from_pyfile("./config/{}_setting.py".format(os.environ['ops_config']))


app = Application(__name__, template_folder=f'{os.getcwd()}/web/templates')
manager = Manager(app)

