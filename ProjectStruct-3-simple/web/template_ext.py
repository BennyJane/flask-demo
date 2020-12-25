# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : career-planning-info
# Time       ：2020/12/15 19:59
# Warning    ：The Hard Way Is Easier
from web.utils.common import UrlManager
from web.utils.libs import random_string


def register_template_ext(app):
    ### 添加模板过滤器
    """添加模板过滤器"""
    # app.add_template_filter(f, name="f_name")

    """添加模板函数"""

    # 添加URL管理函数
    app.add_template_global(UrlManager.buildUrl, "buildUrl")
    app.add_template_global(UrlManager.buildStaticUrl, "buildStaticUrl")
    app.add_template_global(random_string, name="random_string")
