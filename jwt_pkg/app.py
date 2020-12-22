# -*- coding: utf-8 -*-
# @Time : 2020/10/21
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : Flask-Demo
import datetime

from flask import Flask, request, jsonify

from jwt_pkg.jwt_manager import JWTManager

app = Flask(__name__)
SECRET = "TEST"
# token 过期时间与刷新token过期时间
ACCESS_TOKEN_EXPIRE_DATE = datetime.timedelta(minutes=5)
REFRESH_TOKEN_EXPIRE_DELTA = datetime.timedelta(days=7)
jwtManager = JWTManager(secret=SECRET, expire_date=1)


@app.route('/auth/login', methods=['POST'])
def login():
    test = {"name": "test", "password": "test"}

    username = request.json.get("username", None)
    if not username:
        return jsonify({'msg': "参数缺失", "code": '-1', "data": {}})
    password = request.json.get('password', None)
    if not password:
        return jsonify({'msg': "参数缺失", "code": '-1', "data": {}})

    if username == test['name'] and password == test['password']:
        access_token = jwtManager.encode_token(username, fresh=True)
        refresh_token = jwtManager.encode_fresh_token(username)
        ret = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return jsonify(ret), 200
    return jsonify({"msg": "无效用户名or密码"}), 401


@app.route('/')
def index():
    return "hello jwt!"


# 需要验证token才能的访问的页面
@app.route('/auth/protected')
@jwtManager.jwt_required
def jwt_protected():
    return "this is a protected page!"


@app.route('/refresh', methods=['POST'])
def refresh():
    jwt_data = jwtManager.verify_jwt()
    if jwt_data is None:
        return jsonify({"msg": "token验证失败"}), 401
    elif jwt_data['type'] != 'refresh':
        return jsonify({"msg": "该接口只接受刷新token"}), 401
    elif jwt_data['identity'] is None:
        return jsonify({"msg": "token验证失败"}), 401
    current_user = jwt_data.get("identity")
    ret = {
        "access_token": jwtManager.encode_token(identity=current_user, fresh=False)
    }
    return jsonify(ret), 200


if __name__ == '__main__':
    app.run(debug=True, port=9001)
