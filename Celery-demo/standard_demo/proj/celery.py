from celery import Celery


class CeleryConfig:
    broker = 'redis://localhost:6379'
    backend = 'redis://localhost:6379'
    imports = ('proj.tasks',)


# todo 第一个参数以及 imports 必须是异步任务所在模块的名称
celery_app = Celery('app')
celery_app.config_from_object(CeleryConfig)
