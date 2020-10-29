from celery import Celery


class CeleryConfig:
    BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    CELERY_IMPORTS = ['proj.tasks',]


# todo 第一个参数以及 imports 必须是异步任务所在模块的名称
celery_blog = Celery('blog')
celery_blog.config_from_object(CeleryConfig)


# from celery import Celery
#
# celery_blog = Celery('blog',
#              broker='redis://localhost:6379',
#              backend='redis://localhost:6379',
#              include=['proj.tasks'])
#
# # Optional configuration, see the application user guide.
# celery_blog.conf.update(
#     result_expires=3600,
# )

# if __name__ == '__main__':
#     app.start()
