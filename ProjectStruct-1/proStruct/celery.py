import os
from celery import Celery
from .settings import config

config_name = os.getenv("FLASK_CONFIG", 'development')

config_obj = config.get(config_name)
celery_app = Celery('celery_proStruct')
celery_app.config_from_object(config_obj)
