### Flask项目添加定时任务
利用服务器Linux的crontab任务来实现。


#### 测试
```shell script
# 在项目根目录终端输入
python app.py runjob -n test/test_task -a output

```


#### Linux定时任务配置
- 每天早上7点发送一条提醒消息

项目代码位于服务器：/web/www/notify目录下；该目录下还有存储日志的文件夹:logs；
需要修改bash_jobs.sh文件中的激活的python环境路径；
```shell script
# 执行下面命令，将文件移动用户根目录下，并重名为.bash_jobs;
mv bash_jobs ~/.bash_jobs

# 将当前目录下cron文件内的定时任务加载到系统中
crontab cron

# 队列Job
# 需要根据服务器上路径，修改下面的文件路径
0 7 * * * { . ~/.bash_jobs && cd /web/www/notify && python app.py runjob -n test/test_task -a notify ;} >> /web/www/logs/test.`date +\%Y_\%m_\%d`.log 2>&1
```

