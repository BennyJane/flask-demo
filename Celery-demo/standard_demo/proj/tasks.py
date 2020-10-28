import time
from .celery import celery_app


@celery_app.task
def core_task():
    print(' == task start ==')
    time.sleep(5)
    print('== task end ==')
