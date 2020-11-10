# -*- coding: utf-8 -*-
# @Time : 2020/10/21
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : Flask-Demo
import datetime
import uuid

# token 过期时间与刷新token过期时间
import jwt
ACCESS_TOKEN_EXPIRE_DATE = datetime.timedelta(minutes=5)
REFRESH_TOKEN_EXPIRE_DELTA = datetime.timedelta(days=7)


# noinspection PyTypeChecker
class JWTManager(object):
    def __init__(self, expire_date=1, fresh_expire_date=7, algorithm="SHA256"):
        self.token_expire = expire_date
        self.fresh_expire = fresh_expire_date
        self.algorithm = algorithm
        self.auth_header = "Authorization"
        self.token_prefix = "Bearer"

    def encode_token(self, identity, secret, fresh):
        """
        :param identity: 用户ID，用于区别不同用户
        :param secret: 用于JWT编码的盐
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
            "fresh": fresh,
            # 区别不同的应用场景
            "type": "access"
        }
        bytes_str = jwt.encode(token_data, secret, self.algorithm)
        return bytes_str.decode('utf-8')

    def encode_fresh_token(self, identity, secret):
        now = datetime.datetime.now()
        token_data = {
            "exp": now + self.fresh_expire,
            "iat": now,
            "nbf": now,
            "jti": str(uuid.uuid4()),
            "identity": identity,
            "type": "refresh"
        }
        bytes_str = jwt.encode(token_data, secret, self.algorithm)
        return bytes_str.decode("utf-8")

    def decode_jwt(self, token, secret):
        try:
            res = jwt.decode(token, secret, self.algorithm)
            return res
        except jwt.InvalidTokenError:
            raise Exception("token 验证错误")

    def verify_jwt(self, request, secret):
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
        return self.decode_jwt(token, secret)

