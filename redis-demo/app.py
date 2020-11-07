import random
import logging
from flask import Flask, redirect
import redis

app = Flask(__name__)
rcon = redis.StrictRedis(host='localhost', db=0)
prodcons_queue = 'task:prodcons:queue'
pubsub_channel = 'task:pubsub:channel'


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
    rcon.lpush(prodcons_queue, elem)
    logging.info("lpush {} -- {}".format(prodcons_queue, elem))
    return redirect('/')


@app.route('/pubsub')
def pubsub():
    ps = rcon.pubsub()
    ps.subscribe(pubsub_channel)
    elem = random.randrange(10)
    rcon.publish(pubsub_channel, elem)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=9001)
