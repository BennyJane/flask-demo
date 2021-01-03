import os
from flask import Flask

from web.utls import read_yaml

base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

os.environ['FLASK_CONFIG_PATH'] = os.path.join(base_dir, "config\config.yaml")
os.environ['FLASK_ENV'] = "development"

base_config_path = os.path.join(base_dir, "config\config.yaml")


def create_app(config_path=None):
    if config_path is None:
        config_path = os.getenv("FLASK_CONFIG_PATH", base_config_path)
    conf = read_yaml(config_path)
    flask_env = os.getenv("FLASK_ENV", "development").upper()

    app = Flask(__name__)
    app.config.update(conf.get(flask_env))

    from web.index import route_base
    app.register_blueprint(route_base, url_prefix='/')
    return app
