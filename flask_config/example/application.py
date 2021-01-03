import os
from flask import Flask
from flask_script import Manager

from web.view.index import route_base


class Application(Flask):
    # 重构 Flask的 __init__ 方法
    def __init__(self, import_name, template_folder=None, root_path=None):
        '''
        :param import_name:  包 or 模块的名称
        :param template_folder: 模板文件路径
        :param root_path: 内部会根据 import_name 来获取
        '''
        super().__init__(import_name, template_folder=template_folder, root_path=root_path)
        self.config.from_pyfile('./config/base_setting.py')
        if "ops_config" in os.environ:
            self.config.from_pyfile("./config/{}_setting.py".format(os.environ['ops_config']))


# import_name = "manager" 也可以运行
app = Application(__name__, template_folder=f'{os.getcwd()}/web/templates')
app.register_blueprint(route_base, url_prefix='/')

manager = Manager(app)

import sys
from pprint import pprint
print(__name__)
print(__file__)
# pprint(sys.modules)


if __name__ == '__main__':
    app.run(debug=True)
