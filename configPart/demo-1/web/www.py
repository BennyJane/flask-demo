from application import app

'''
蓝图功能: 对所有的url进行蓝图功能配置
'''
from web.view.index import route_base

app.register_blueprint(route_base, url_prefix='/')
