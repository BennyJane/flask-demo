#!/bin/bash

set -e

cd `dirname $0`
echo `pwd`

# 需要先激活Python的虚拟环境

# 启动celery

#celery -A tasks:celery worker -l error
celery -A tasks:celery worker
# 后台运行
#celery multi start w1 -A task:celery -l info --logfile = celerylog.log --pidfile = celerypid.pid
echo "启动celery"