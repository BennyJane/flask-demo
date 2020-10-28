import time
from proStruct.celery import celery_app


@celery_app.task
def add(x, y):
    print(x, y)
    time.sleep(5)
    v = x + y
    return v
