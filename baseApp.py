from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "<h5>app.py内完成Flask的实例化  .flaskenv:</h5><h1>FLASK_APP=demo.app</h1>"


a = 10

def sum():
    # a = 20
    a = 20
    print(a)

# sum()

from base02 import demo2, demo2_a
print('==== before running ===')
print(demo2_a)
demo2()

# if __name__ == '__main__':
#     app.run(debug=True)
