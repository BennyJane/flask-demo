import redis


class RedisHelper(object):
    def __init__(self, channel=None):
        self.__conn = redis.Redis(host='127.0.0.1', port=6379)
        self.channel = channel

    def publish(self, msg):
        """发布订阅消息"""
        self.__conn.publish(self.channel, msg)
        return True

    def subscribe(self):
        """订阅频道方法"""
        pub = self.__conn.pubsub()
        pub.subscribe(self.channel)
        pub.parse_response()
        return pub
