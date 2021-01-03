import os
from flask import Flask

from web.index import route_base
from config import projectConfigs

os.environ['FLASK_ENV'] = 'development'


# os.environ['FLASK_ENV'] = 'production'


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", 'development')
    app = Flask(__name__)
    app.config.from_object(projectConfigs[config_name])

    return app


# import_name = "manager" 也可以运行
app = create_app()
app.register_blueprint(route_base, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
