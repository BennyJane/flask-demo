# -*-coding: utf-8-*-

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES  # 导入


mail = Mail()
db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)  # 创建set


def create_app(config_name):
    app = Flask(__name__)
    mail.init_app(app)
    db.init_app(app)

    configure_uploads(app, photos)  # 初始化
    return app

'''
在大型项目中使用  flask-uploads
'''