# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier

import textwrap
import sqlalchemy as sqla
from sqlalchemy import (
    Boolean, Column, create_engine, DateTime, ForeignKey, Integer,
    MetaData, String, Table, Text,
)
from sqlalchemy.engine import url
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import relationship, sessionmaker, subqueryload
from sqlalchemy.orm.session import make_transient
from sqlalchemy.pool import NullPool
from sqlalchemy.schema import UniqueConstraint

# 需要安装 sqlalchemy-utils类；使用加密类型
from sqlalchemy_utils import EncryptedType

from sqlalchemy_demo.orm_models import db
from sqlalchemy_demo.orm_models import app


class Database(db.Model):

    """An ORM object that stores Database related information"""

    __tablename__ = 'dbs'
    type = 'table'
    __table_args__ = (UniqueConstraint('database_name'),)

    id = Column(Integer, primary_key=True)
    verbose_name = Column(String(250), unique=True)
    # short unique name, used in permissions
    database_name = Column(String(250), unique=True)
    sqlalchemy_uri = Column(String(1024))
    password = Column(EncryptedType(String(1024), config.get('SECRET_KEY')))
    cache_timeout = Column(Integer)
    select_as_create_table_as = Column(Boolean, default=False)
    expose_in_sqllab = Column(Boolean, default=False)
    allow_run_sync = Column(Boolean, default=True)
    allow_run_async = Column(Boolean, default=False)
    allow_csv_upload = Column(Boolean, default=False)
    allow_ctas = Column(Boolean, default=False)
    allow_dml = Column(Boolean, default=False)
    force_ctas_schema = Column(String(250))
    allow_multi_schema_metadata_fetch = Column(Boolean, default=False)
    extra = Column(Text, default=textwrap.dedent("""\
    {
        "metadata_params": {},
        "engine_params": {},
        "metadata_cache_timeout": {},
        "schemas_allowed_for_csv_upload": []
    }
    """))
    perm = Column(String(1000))
    impersonate_user = Column(Boolean, default=False)
    export_fields = ('database_name', 'sqlalchemy_uri', 'cache_timeout',
                     'expose_in_sqllab', 'allow_run_sync', 'allow_run_async',
                     'allow_ctas', 'allow_csv_upload', 'extra')
    export_children = ['tables']

    def __repr__(self):
        return self.verbose_name if self.verbose_name else self.database_name

    @property
    def name(self):
        return self.verbose_name if self.verbose_name else self.database_name


if __name__ == '__main__':
    app.run(debug=True)