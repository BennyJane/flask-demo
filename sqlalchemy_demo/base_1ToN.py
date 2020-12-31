# -*- coding: utf-8 -*-
# @Time : 2020/10/16
# @Author : Benny Jane
# @Email : 暂无
# @File : base_1ToN.py
# @Project : sqlalchemy
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

base_dir = os.path.abspath(os.path.dirname(__file__))
# print(__file__)     # 打印当前文件路径
# print(__name__)     # 打印所在文件名称， 文件内打印： __main__
# print(base_dir)
# 必须是 __name__
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'base.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET'] = 'BENNY'
# app.config['ENV'] = 'development'
db = SQLAlchemy(app)

'''
一对多：作者与书
- 真实表的名称一定是小写
    - 默认将类名称的小写作为表的名称: Foo -> foo
    - 多单词类名称，以下划线分割开： bookCategory -> book_category
- 在N的一侧，定义外键, 格式： 表名称.字段名称 
    - 外键值为另一侧的id，类型为数值型
    - 此时，表的名称必须输入真实表的名称，小写
- 在1的一侧，定义关系属性，使用db.relationship('表名称')
    - 关系属性为集合，对应多个值
    - 名称没有限制，仅仅作为一种快捷查询，该字段不会出现在数据库中    


## 表数据操作
- 添加表数据
    - author = Author(name='benny')
    - book = Book(title='a dog', body='a simple book!')
    - db.session.add(author) db.session.add(book)   # db.session.add_all([author, book])
    - db.session.commit()

## 建立关系
- 直接给外键赋值
    - book.author_id=1
    - db.session.commit()       # 更新操作，可以直接提交commit， 而不用再次使用add方法
- 操作关系属性，将关系属性，赋给实际对象；
    - 集合关系可以像列表一样操作： 
        - author.books.append(book) db.session.commit()
        - author.books.pop() 删除关系； commit()
        - author.books.remove(book)
        - db.session.commit()  更新关系，需要commit
    - 标量关系操作
        - book.author = author 
        - book.author=None   解除关系
        - commit()
        
    - 关系对象，只需要操作一侧，另一侧会自动获得正确的值 ==》 
        当作者下添加一本书，则书的author_id自动更改为该作者名称，无需再次操作
     

## 添加双向关系
    - 返回列表的关系属性，称为 集合关系属性
    - 返回单个值的关系属性，称为 标量关系属性
    - 使用 back_populates建立双向关系，
        - 必须在两侧显示的定义关联关系
        - back_populates='another_field_name' 值，是建立双向关系中的另一个字段的名称

## 删除操作
    - 默认(不添加级联关系前)， 删除一个book，则author对象的books列表中相应不会出现该book
    

## backref: 仅仅在一侧就可以定义另一侧的关系属性
    - songs = relationship("Song", backref="singer")
    - 建立双向关系，relationship("另一个类名", backref="另一侧增加的关系属性名称")
    - 仍然需要单独定义主键，主键永远在多的一侧
    - backref：可以定义在双向关系的任意一侧(已经测试)
    - 当需要对关系另一侧的关系属性进行属性设置的时候，使用 backref() 函数
    - backref()函数
        - song = relationship("Song", backref=backref("singer", uselist=False))
        - 定义1对1关系


'''
Column = db.Column
relationship = db.relationship


class Author(db.Model):  # 真实数据表的名字为 author
    id = Column(db.INTEGER, primary_key=True)
    name = Column(db.String(255), nullable=False)

    # 建立双向关系， back_populates,两侧都添加该语句
    books = relationship('Book', back_populates='author')

    def __repr__(self):
        return '<%s OF %s>' % (self.name, type(self).__name__)


class Book(db.Model):  # 真实数据表的名字为 book
    id = Column(db.INTEGER, primary_key=True)
    title = Column(db.String(255), index=True)
    body = Column(db.Text)

    # s
    author_id = Column(db.Integer, db.ForeignKey('author.id'))
    author = relationship("Author", back_populates='books')

    def __repr__(self):
        return f'<{self.title} OF {type(self).__name__}>'


'''
==============================================================
模型类名称与实际表名称的关系
==============================================================
'''


class BaseStudent(db.Model):
    # 真实数据表的名字为 base_student
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50))


class Base_Teacher(db.Model):
    # 真实数据表的名字为 user_permit
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50))


'''
==============================================================
backref的使用
==============================================================
'''


class Singer(db.Model):
    # 真实数据表的名字为 singer
    id = Column(db.INTEGER, primary_key=True)
    name = Column(db.String(255), nullable=False)

    # 建立双向关系， backref 只需要在一侧添加
    # songs = relationship('Song', backref='singer')

    def __repr__(self):
        return '<%s OF %s>' % (self.name, type(self).__name__)


class Song(db.Model):  # 真实数据表的名字为 book
    id = Column(db.INTEGER, primary_key=True)
    title = Column(db.String(255), index=True)
    body = Column(db.Text)

    # 主键
    sing_id = Column(db.Integer, db.ForeignKey('singer.id'))
    singer = relationship("Singer", backref="songs")

    def __repr__(self):
        return f'<{self.title} OF {type(self).__name__}>'


# shell_context_processor
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Author=Author, Book=Book,
                BaseStudent=BaseStudent, Base_Teacher=Base_Teacher,
                Singer=Singer, Song=Song)


db.drop_all()
db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

'''
author = Author(name='benny')
author1 = Author(name='tom')
book = Book(title='a dog', body='a simple book!')
book1 = Book(title='a cat', body='a simple book!')
book2 = Book(title='a bird', body='a simple book!')
db.session.add_all([author, author1, book1, book2,book])
db.session.commit()

author.books=[book, book1, book3]
db.session.commit()
author.books

author.books.pop()
author.books

author.books.remove(book1)
author.books

au = Author.query.first()
au

book = Book.query.first()
book

================================================

singer = Singer(name='tom')
song = Song(title='a dog', body='a simple book!')
song1 = Song(title='a cat', body='a simple book!')
song2 = Song(title='a bird', body='a simple book!')

db.session.add_all([singer, song, song1, song2])
db.session.commit()
singer.songs
song.singer

singer = Singer.query.first()
song = Song.query.first()
'''
