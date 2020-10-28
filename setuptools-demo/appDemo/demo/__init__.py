from flask import Flask

app = Flask(__file__)
app.config.SECRET_KEY = 'DEV'


@app.route('/')
def index():
    return 'setuptools-demo'


if __name__ == '__main__':
    app.run(debug=True)
