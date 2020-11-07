from flask import Flask, jsonify
from validators.validatorDemo import Regexp, DataRequired, AddDefault
from validators.decorates import frontValidator

app = Flask(__name__)
app.config['FLASK_ENV'] = "development"
checkFields = {
    "index": {
        "site": [DataRequired(), ],
        "month": [DataRequired(), Regexp(regex="\d+_\d*", msg="字段不能为空")]
    }
}


@app.route("/")
def index():
    fields = {
        "site": [DataRequired(), ],
        "month": [DataRequired(msg="字段不能为空"), Regexp(regex="\d{4}-\d{2}", msg="字段格式不正确")]
    }
    frontValues = frontValidator(fields)
    print(frontValues)
    return "index page"


@app.route('/rename', methods=['POST'])
def rename():
    fields = {
        "name": [DataRequired(msg="姓名不能为空"), ],
        "old": [AddDefault(default=10), ],
    }
    frontValues = frontValidator(fields)
    return jsonify(frontValues)


@app.errorhandler(Exception)
def allException(e):
    res = {"code": -1, "message": str(e), "status": 200}
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
