import redis
import inspect


class RedisConn:
    def __init__(self, host, port):
        self._conn = redis.Redis(host=host, port=port)

    """
    ====================================================
    生产/消费者模型
    ====================================================
    """

    def listen_task(self, target_queue, task=None):
        """从队列中获取数据,并执行相应的任务"""
        while True:  # 不间断运行
            try:
                # blpop: 队列为空, 阻塞； timeout=0, 则无限阻塞
                task_params = self._conn.blpop(target_queue, timeout=0)[1]
                # bytes -> str
                task_params = str(task_params, encoding="utf-8")
                # 执行任务
                print("runing {}".format(task_params))
                if inspect.isfunction(task) or inspect.ismethod(task):
                    task(task_params)
            except Exception as e:
                print(e)

    def add_task(self, target_queue, task):
        """向队列中添加数据"""
        self._conn.lpush(target_queue, task)

    """
    ====================================================
    订阅/发布模型
    ====================================================
    """

    def publish_msg(self, target_channel, msg):
        """发布消息"""
        ps = self._conn.pubsub()
        ps.subscribe(target_channel)
        self._conn.publish(target_channel, msg)

    def listen_msg(self, target_channel):
        """接收订阅的消息"""
        ps = self._conn.pubsub()
        ps.subscribe(target_channel)
        for item in ps.listen():
            if item['type'] == 'message':
                print("get msg {}".format(item['data']))
