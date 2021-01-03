from flask import Blueprint
from flask import current_app
from flask import url_for

route_base = Blueprint("base_view", __name__)


@route_base.route('/')
def index():
    html = f'<h3><a href="{url_for(".config", _external=True)}">查看配置文件名称</a></h3>'
    return html


@route_base.route('/config/')
def config():
    config_name = current_app.config['CONFIG_NAME']
    html = f'<h1>当前配置文件名称: {config_name}; <a href="{url_for(".index", _external=True)}">返回</a></h1>'
    return html
