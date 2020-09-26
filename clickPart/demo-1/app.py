from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return f"<h5>{__file__}:{__name__}</h5><h1>flask-click 包使用</h1>"


if __name__ == '__main__':
    app.run(debug=True)
