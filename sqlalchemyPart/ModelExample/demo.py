from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

demo = Flask(__name__)

db = SQLAlchemy(demo)

'''
===============================  ORM    =============================== 
'''
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# 继承自 db.Model , 混合类 UserMixin
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # 添加主键
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.String(30))

    def set_password(self, password):
        # 生成密码的hash值
        # todo 查看源码，分析 method， salt_length
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

    def validate_password(self, password):
        # 验证密码
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    # todo 一对多，外键关联
    # 实现额外的功能： 可以通过该字段直接该分类下的所有文章
    posts = db.relationship("Post", back_populates="category")

    def delete(self):
        # 将当前分类下所有posts绑定到默认分类上，并删除当前分类
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)  # 删除当前分类
        db.session.commit()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)  # 长文本
    # 时间戳
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_comment = db.Column(db.Boolean, dafault=True)  # 布尔值
    # todo 外键关联
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # 实现额外的功能： 可以通过该字段直接获取post的分类
    category = db.relationship('Category', back_populates="posts")
    # todo
    comments = db.relationship('Comment', back_populates="post", cascade="all, delete-orphan")


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)

    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True) # todo 添加索引

    # todo 两个外键
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    post = db.relationship('Post', back_populates='comments')
    # todo 自连接
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphon')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    '''
    Same with:
    replies = db.relationship('Comment', backref=db.backref('replied', remote_side=[id]),
    cascade='all,delete-orphan')
    '''


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))


if __name__ == '__main__':
    demo.run(debug=True)
