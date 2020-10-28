from flask import Flask, render_template

import config
from ueditor import bp

app = Flask(__name__)
app.config.from_object(config)
app.config['FLASK_ENV'] = 'development'
app.register_blueprint(bp)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/index')
def index():
    raise Exception('this is a raise error!!')
    return 'error'

@app.errorhandler(Exception)
def dealError(e):
    print(e, 'this is error handler')
    return ''


if __name__ == '__main__':
    app.run(port=9000, debug=True)
