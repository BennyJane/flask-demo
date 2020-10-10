### ModelExample: 主要是ORM的具体写法


## 常用配置项
**SQLALCHEMY_DATABASE_URI**      
    连接数据， mysql://username:password@host/databasename/tablenaem?charset=utf-8  
**SQLALCHEMY_BINDS**  
    一个将会绑定多种数据库的字典，详细信息见  
**SQLALCHEMY_ECHO**  
    调试时候设置为True  
**SQLALCHEMY_POOL_SIZE**  
    数据库连接池大小，默认为5  
**SQLALCHEMY_POOL_TIMEOUT**  
    连接超时时间  
**SQLALCHEMY_POOL_RECYCLE**  
    自动回收连接的秒数  
**SQLALCHEMY_MAX_OVERFLOW**  
    **控制在连接池达到最大值后，可以创建的连接数。 当这些额外的链接回收到连接池后 会被抛开和抛弃  
SQLALCHEMY_TRACK_MODIFICATIONS**  
    如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。  
    ** 一般设置为False  


## config格式
```python
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'flask1'
USERNAME = 'root'
PASSWORD = '123456'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD, host=HOST,port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
```
## 绑定app

```                                          
from flask import Flask
import configs
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__file__)
app.config.from_object(configs)
db.init_app(app)

```

## 数据类型

数据类型	说明
Integer	整型
String	字符串
Text	文本
DateTime	日期
Float	浮点型
Boolean	布尔值
PickleType	存储一个序列化（ Pickle ）后的Python对象
LargeBinary	巨长度二进制数据


## 使用 flask-migrate
```
# manager.py
from flask_script import Manager, Server
from app import app
from flask_migrate import Migrate, MigrateCommand
from ext import db
from first import models # 模型文件必须导入进来，否则运行报错

manager = Manager(app)
Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand) # 创建数据库映射命令
manager.add_command('start', Server(port=8000, use_debugger=True)) # 创建启动命令

if __name__ == '__main__':
    manager.run()

```
### 启动方式
进入项目根目录， 在命令行中输入以下代码：
python manager.py db init
python manager.py db migrate
python manager.py db upgrade


##  表的增删查改
```
# 原生sql语句操作
sql = 'select * from user'
result = db.session.execute(sql)

# 查询全部
User.query.all()
# 主键查询
User.query.get(1)
# 条件查询
User.query.filter_by(User.username='name')
# 多条件查询
from sqlalchemy import and_
User.query.filter_by(and_(User.username =='name',User.password=='passwd'))
# 比较查询
User.query.filter(User.id.__lt__(5)) # 小于5
User.query.filter(User.id.__le__(5)) # 小于等于5
User.query.filter(User.id.__gt__(5)) # 大于5
User.query.filter(User.id.__ge__(5)) # 大于等于5
# in查询
User.query.filter(User.username.in_('A','B','C','D'))
# 排序
User.query.order_by('age') # 按年龄排序，默认升序，在前面加-号为降序'-age'
# 限制查询
User.query.filter(age=18).offset(2).limit(3)  # 跳过二条开始查询，限制输出3条

# 增加
use = User(id,username,password)
db.session.add(use)
db.session.commit() 

# 删除
User.query.filter_by(User.username='name').delete()

# 修改
User.query.filter_by(User.username='name').update({'password':'newdata'})
```


