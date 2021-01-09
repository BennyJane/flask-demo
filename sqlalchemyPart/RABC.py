# -*- coding: utf-8 -*-
# @Time : 2020/11/25
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py.py
# @Project : Flask-Demo
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
Column = db.Column

"""
1. 每个权限对应的数值，一般使用2的整数倍，便于使用二进制的按位 与 或逻辑计算判断是否具有某个权限
    # 16进制 0x开头
    # 8进制 0开头
2. 用户与角色之间是一对多关系； 外键在一侧
3. 自定义查询类， 抽取常用的查询方法
"""


class Permission:
    permission1 = 0x01  # -》 00000001
    permission2 = 0x02  # -》 00000010
    permission3 = 0x04  # -》 00000100
    permission4 = 0x08  # -》 00001000
    permission5 = 0x10  # -》 00010000

    # 管理员，具有所有权限， 赋予较大值, 转化为二进制，所有位都是1
    # 0xff 255 -》 二进制 11111111
    ADMINISTER = 0xff


class RoleQuery(BaseQuery):
    def isDefault(self):
        return self.filter(default=True)


class Role(db.Model):
    __tablename__ = 'roles'
    query_class = RoleQuery
    # 核心字段
    id = Column(db.Integer, primary_key=True)
    permissions = Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    name = Column(db.String(64), unique=True)
    # 只有一个角色的 default 字段要设为 True，其他都设为 False。用户注册时，其角色会被 设为默认角色
    # TODO 将角色划分为了 默认角色与非默认角色两大类
    default = Column(db.Boolean, default=False, index=True)

    @staticmethod
    def insert_roles():
        """实现该静态方法，在项目初始化的时候，调用该方法，实现基础数据的插入与更新"""
        roles = {
            # 定义了各个角色具有的权限，从Permission类中获得16进制的值，采用 二进制的 或 ； 只有同位置上有一个1， 就取1
            'Role1': (Permission.permission1, True),
            'Role2': (Permission.permission1 | Permission.permission2, True),
            'Role3': (Permission.permission1 | Permission.permission2 |
                      Permission.permission3, True),
            'Administrator': (Permission.ADMINISTER, True),
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class UserQuery(BaseQuery):
    def search(self, keyword):
        key = u'%{0}%'.format(keyword.strip())
        return self.filter(User.username.ilike(key))


class User(db.Model):
    __tablename__ = 'users'
    query_class = UserQuery  # 自定义了User类的查询类

    # 核心字段
    id = db.Column(db.Integer, primary_key=True)
    role_id = Column(db.Integer, db.ForeignKey('roles.id'))

    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # 设置查询结果的默认排序方式
    __mapper_args__ = {'order_by': [id.desc()]}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.role is None:  # 这里利用关联关系，通过设置用户关联的role，达到设置role_id的目的
            # 每个普通用户注册都会执行该语句，设置索引，提高搜索速度
            # todo 可参考的优化： 将默认角色，管理员角色的id设置为固定值(比如0), 这里就可以直接设置用户角色id，而省去执行查询 --》 注册也不是频繁的操作
            self.role = Role.query.filter_by(defalut=True).first()
            if self.email == 'admin_email(从配置文件中获取)':  # 只有在插入管理者账号的时候，才会执行该数据库搜索语句
                self.role = Role.query.filter_by(permissions=Permission.ADMINISTER).first()

    @staticmethod
    def insert_user():
        user = User(username='从配置文件中获取', email='从配置文件中获取', password='从配置文件中获取')
        db.session.add(user)
        db.session.commit()

    def can(self, permissions):
        """判断当前用户角色是否拥有该权限"""
        # & 与： 二进制同位置必须同是1， 最后才能取1
        return self.role is not None and (self.role.permissions & permissions) == permissions

    @staticmethod
    def reset_password(new_password):  # 单独提供了重置管理员密码的方法
        user = User.query.filter_by(email="从配置文件中获取").first()  # 管理员id硬编码了，不好
        user.password = new_password
        db.session.commit()

    @property
    def password(self):
        """将密码属性，通过property设置为类, 方便管理该属性的读写"""
        raise AttributeError('该属性不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hashm, password)
