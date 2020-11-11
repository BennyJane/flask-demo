# -*- coding: utf-8 -*-
# @Time : 2020/10/21
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : Flask-Demo
import datetime
import functools
import uuid

import jwt
from flask import request, jsonify

"""
token加密主要通过jwt包来完成，
- token的刷新，通过一个专门的接口实现，当access_token 失效后，会利用fresh_token来获取新的token，
同时将 jwt中字段fresh修改为false，将当前token标记为非新鲜token。
- 需要一个装饰器，用来限制一些安全级别较高的端口，必须使用未刷新过的token，也就是新鲜token才能访问


bug:
jwt不支持 sha256算法
"""


# noinspection PyTypeChecker
class JWTManager(object):
    def __init__(self, secret=None, expire_date=1, fresh_expire_date=7, algorithm="HS256"):
        if not secret:
            secret = "skdfsahuisksdfkl"
        self.secret = secret  # 用于JWT编码的盐
        self.token_expire = datetime.timedelta(minutes=expire_date)
        self.fresh_expire = datetime.timedelta(days=fresh_expire_date)
        self.algorithm = algorithm
        self.auth_header = "Authorization"
        self.token_prefix = "Bearer"

    def encode_token(self, identity, fresh):
        """
        :param identity: 用户ID，用于区别不同用户
        :param fresh: 刷新token
        :param algorithm: 加密算法
        :return: 编码后的JWT
        """
        now = datetime.datetime.utcnow()
        token_data = {
            "exp": now + self.token_expire,
            "iat": now,
            "nbf": now,
            "jti": str(uuid.uuid4()),
            "identity": identity,
            "fresh": fresh,  # bool， 登录，修改密码时，设置为true；刷新token后，设置为false
            # 区别不同的应用场景
            "type": "access"
        }
        bytes_str = jwt.encode(token_data, self.secret, self.algorithm)
        return bytes_str.decode('utf-8')

    def encode_fresh_token(self, identity):
        now = datetime.datetime.now()
        token_data = {
            "exp": now + self.fresh_expire,
            "iat": now,
            "nbf": now,
            "jti": str(uuid.uuid4()),
            "identity": identity,
            "type": "refresh"
        }
        bytes_str = jwt.encode(token_data, self.secret, self.algorithm)
        return bytes_str.decode("utf-8")

    def decode_jwt(self, token):
        try:
            res = jwt.decode(token, self.secret, self.algorithm)
            return res
        except jwt.InvalidTokenError:
            # todo 区别具体原因
            raise Exception("token 验证错误")

    def verify_jwt(self):
        """验证request请求中包含的token"""
        auth_header = request.headers.get(self.auth_header, None)
        if not auth_header:
            raise Exception("token请求参数不正确")
        parts = auth_header.split()
        if parts[0] != self.token_prefix:
            msg = "格式错误，应该为 'Bearer <JWT>'"
            raise Exception(msg)
        elif len(parts) != 2:
            msg = "格式错误，应该为 'Bearer <JWT>'"
            raise Exception(msg)
        token = parts[1]
        return self.decode_jwt(token)

    def jwt_required(self, f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                jwt_data = self.verify_jwt()
            except Exception as e:
                return jsonify({'msg': f"{str(e)}"}), 422

            if jwt_data['type'] != 'access':
                return jsonify({'msg': '只有access token可以访问该端口'}), 401
            return f(*args, **kwargs)

        return wrapper
