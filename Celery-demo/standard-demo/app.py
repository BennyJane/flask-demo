import time

# from celery import Celery
from flask import Flask

# from celery_ext import celery_app
from celery_ext import celery_app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

broker = 'redis://localhost:6379'
backend = 'redis://localhost:6379'

# 第一个参数必须设置为任务所在的模块的名称
# celery_app = Celery("app", broker=broker, backend=backend)


@celery_app.task
def core_task():
    print(' == task start ==')
    time.sleep(5)
    print('== task end ==')


@app.route('/')
def index():
    core_task.delay()
    print('== view end ==')
    return 'hello world'


if __name__ == '__main__':
    app.run(debug=True)
