import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from flask_sqlalchemy import SQLAlchemy
from contextlib import contextmanager
from flask import Flask

app = Flask(__name__)

db = SQLAlchemy()
db.init_app(app)


@contextmanager
def session_scope(nullpoll):
    if nullpoll:
        engine = sqlalchemy.create_engine("SQLALCHEMY_DATABASE_URI", pollclass=NullPool)
        session_class = sessionmaker()
        session_class.configure(bind=engine)
        session = session_class()
    else:
        # 提交一次
        session = db.session()
        session.commit()

    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
        raise
    finally:
        session.close()


if __name__ == '__main__':
    app.run(debug=True)
