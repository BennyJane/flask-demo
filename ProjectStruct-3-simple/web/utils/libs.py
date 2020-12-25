import os
import time
import random
import hashlib
import datetime


def produceId():
    filePath = os.getcwd()
    src = filePath + str(time.time())
    m = hashlib.md5()
    m.update(src.encode('utf-8'))
    return m.hexdigest()


def getFormatDate(date=None, _format="%Y-%m-%d %H:%M:%S"):
    if date is None:
        date = datetime.datetime.now()
    return date.strftime(_format)


def random_string(length):
    text = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return text
