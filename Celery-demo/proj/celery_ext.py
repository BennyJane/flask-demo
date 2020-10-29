from celery import Celery


class CeleryConfig:
    BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    CELERY_IMPORTS = ('proj.tasks',)


# todo 第一个参数以及 imports 必须是异步任务所在模块的名称
app = Celery('app')
app.config_from_object(CeleryConfig)

