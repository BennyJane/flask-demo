import random
from flask import Flask, redirect

import config
from redisCore import RedisConn

app = Flask(__name__)
app.config.from_pyfile('config.py')

produce_queue = app.config["REDIS_PRODUCE_QUEUE"]
pubsub_channel = app.config["REDIS_PUBSUB_CHANNEL"]
redisConn = RedisConn(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"])


@app.route('/')
def index():
    html = """
<br>
<center><h3>Redis Message Queue</h3>
<br>
<a href="/prodcons">生产消费者模式</a>
<br>
<br>
<a href="/pubsub">发布订阅者模式</a>
</center>
"""
    return html


@app.route('/prodcons')
def prodcons():
    elem = random.randrange(10)
    redisConn.add_task(produce_queue, elem)
    return redirect('/')


@app.route('/procons/list')
def proconsList():
    redisConn.listen_task(produce_queue)


@app.route('/pubsub')
def pubsub():
    elem = random.randrange(10)
    redisConn.publish_msg(pubsub_channel, elem)
    return redirect('/')


@app.route('/pubsub/list')
def pubsubList():
    redisConn.listen_msg(target_channel=pubsub_channel)


if __name__ == '__main__':
    app.run(debug=True, port=9002)
