### Flask项目添加定时任务
利用服务器Linux的crontab任务来实现。


#### 测试
```shell script
# 在项目根目录终端输入
python app.py runjob -n test/test_task -a test

```


#### Linux定时任务配置
- 每分钟执行测试消息
- 每天早上7点发送一条提醒消息

项目代码位于服务器：/web/www/notify目录下；该目录下还有存储日志的文件夹:logs
```shell script
# 队列Job
1 * * * * { . ~/.bash_jobs && cd /web/www/notify && python app.py runjob -m test/test_task -a output ;} >> /web/www/logs/test.`date +\%Y_\%m_\%d`.log 2>&1
0 7 * * * { . ~/.bash_jobs && cd /web/www/notify && python app.py runjob -m test/test_task -a notify ;} >> /web/www/logs/test.`date +\%Y_\%m_\%d`.log 2>&1
2 * * * * { . ~/.bash_jobs && cd /web/www/notify && python app.py runjob -n test/test_task -a notify ;} >> /web/www/logs/test.`date +\%Y_\%m_\%d`.log 2>&1
```

