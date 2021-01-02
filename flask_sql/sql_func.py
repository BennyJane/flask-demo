# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : Flask-Demo
# Time       ：2021/1/2 21:28
# Warning    ：The Hard Way Is Easier

class SqlExecuteError(Exception):
    """sql执行报错"""


# insert update delete 语句执行后，都需要调用commit才会真正提交到数据库
class SqlFunc(object):
    def __init__(self, session=None):
        """Flask中输入示例：session = db.session"""
        self.session = session if session else None
        self.db = session

    def init_db(self, session):
        """绑定"""
        if session:
            self.session = session

    def select_sql(self, name: str, fields: list, condition: str = "") -> list:
        target_fields = ", ".join(fields)
        sql = "select {} from {} {}".format(target_fields, name, condition)
        print(sql)
        try:
            result = self.db.execute(sql).fetchall()
        except Exception as e:
            # TODO 日志打印输出失败的真正原因
            raise SqlExecuteError("查询数据报错")
        return result

    def update_sql(self, name: str, fields: list, values: list, condition: str = "") -> None:
        if len(fields) != len(values):
            raise Exception("字段与数值长度不一致")
        update_fields = ", ".join(["{}='{}'".format(item[0], item[1]) for item in zip(fields, values)])
        sql = "update {} set {} {} ".format(name, update_fields, condition)
        try:
            self.db.execute(sql)
        except Exception as e:
            raise SqlExecuteError("更新数据失败")

    def insert_sql(self, name: str, fields: list, values: list, condition: str = "") -> None:
        if len(fields) != len(values):
            raise Exception("字段与数值长度不一致")
        fields_str = ", ".join(["`{}`".format(item) for item in fields])  # 最好使用``反引号处理
        values_str = ", ".join(["'{}'".format(item) for item in values])

        sql = "insert into {} ( {} ) values ( {} ) {}".format(name, fields_str,
                                                              values_str, condition)
        try:
            self.db.execute(sql)
        except Exception as e:
            raise SqlExecuteError("插入数据失败")

    def delete_sql(self, name: str, condition: str) -> None:
        sql = f"delete from {name} " + condition
        try:
            self.db.execute(sql)
        except Exception as e:
            raise SqlExecuteError("删除数据失败")

    @property
    def commit(self):
        self.db.commit()

    def execute_sql(self, sql: str, action="select"):
        try:
            if action == "select":
                result = self.db.execute(sql).fetchall()
                return result
            else:
                if any(["drop" in sql, "create" in sql]):  # 禁止执行删除、创建操作
                    return
                self.db.execute(sql)
        except Exception as e:
            raise SqlExecuteError("SQL执行失败")
