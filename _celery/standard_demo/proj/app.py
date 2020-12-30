from flask import Flask
from proj.tasks import core_task
app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'


@app.route('/')
def index():
    core_task.delay()
    print('== view end ==')
    return 'hello world'


if __name__ == '__main__':
    app.run(debug=True)
