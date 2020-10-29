# encoding: utf-8
from celery import Celery
from flask import Flask

app = Flask(__name__)

# celery相关的配置
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"


# 运行本文件：
# 在windows操作系统上：
# celery -A tasks.celery worker --pool=solo --loglevel=info
# 在类*nix操作系统上：
# celery -A tasks.celery worker --loglevel=info

def make_celery():
    celery_app = Celery('base', backend=CELERY_RESULT_BACKEND,
                        broker=CELERY_BROKER_URL)

    class ContextTask(celery_app.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super(ContextTask, self).__call__(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


celery = make_celery()

