import time
from .celery_app import celery_blog


@celery_blog.task
def core_task():
    print(' == task start ==')
    time.sleep(5)
    print('== task end ==')
