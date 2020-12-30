from flask import Blueprint
from application import app

route_base = Blueprint("base_view", __name__)


@route_base.route('/')
def index():
    config_name = app.config['CONFIG_NAME']
    html = f'<h1>当前配置文件名称: {config_name}</h1>'
    return html

