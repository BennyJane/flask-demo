# -*-coding: utf-8-*-

from flask import Flask
# from flask_bootstrap import Bootstrap
from flask_mail import Mail
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from config import config
from flask_uploads import UploadSet, configure_uploads, IMAGES  # 导入

# bootstrap = Bootstrap()
mail = Mail()
# moment = Moment()
db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)  # 创建set


def create_app(config_name):
    app = Flask(__name__)
    # app.config.from_object(config[config_name])
    # config[config_name].init_app(app)

    # bootstrap.init_app(app)
    mail.init_app(app)
    # moment.init_app(app)
    db.init_app(app)

    configure_uploads(app, photos)  # 初始化

    return app
