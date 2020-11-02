import logging
import json


def validate_json(data=None):
    try:
        json.loads(data)
    except Exception as e:
        logging.info(e)
        raise Exception("该数据不能序列化")
